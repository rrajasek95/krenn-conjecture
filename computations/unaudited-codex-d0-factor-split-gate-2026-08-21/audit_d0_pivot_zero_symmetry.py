#!/usr/bin/env python3
"""Exact Laurent symmetry and minimal-pair cover of the D0 pivot-zero face."""

from __future__ import annotations

from functools import reduce
from hashlib import sha256
import importlib.util
import json
from math import gcd
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
BASE = HERE / "export_and_audit_d0_factor_split_gate.py"
INTERFACE = HERE / "results_d0_pivot_zero_interface.json"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load():
    spec = importlib.util.spec_from_file_location("d0_pivot_zero_symmetry_base", BASE)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    require(spec.loader is not None, "missing base loader")
    spec.loader.exec_module(module)
    return module


def logical_hash(value):
    return sha256(json.dumps(value, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def parse(sp, value):
    return sp.sympify(value.replace("^", "**"))


def encode(sp, value):
    return str(sp.expand(value)).replace("**", "^")


def profile(sp, value, variables):
    poly = sp.Poly(value, *variables)
    return {"terms": len(poly.terms()), "total_degree": int(poly.total_degree()),
            "multidegree": [int(poly.degree(variable)) for variable in variables],
            "sha256": sha256(encode(sp, poly.as_expr()).encode()).hexdigest()}


def canonical_image(E, value, variables):
    """Return a primitive polynomial representative of the Laurent image."""
    image = E.image_dict(value, variables)
    minima = tuple(min(exponents[index] for exponents in image)
                   for index in range(len(variables)))
    shifted = {tuple(exponents[index] - minima[index]
                     for index in range(len(variables))): coefficient
               for exponents, coefficient in image.items()}
    content = reduce(gcd, (abs(value) for value in shifted.values()))
    shifted = {exponents: coefficient // content
               for exponents, coefficient in shifted.items()}
    leading = shifted[min(shifted)]
    if leading < 0:
        shifted = {exponents: -coefficient
                   for exponents, coefficient in shifted.items()}
    answer = E.sp.Integer(0)
    for exponents, coefficient in shifted.items():
        term = E.sp.Integer(coefficient)
        for variable, exponent in zip(variables, exponents):
            term *= variable**exponent
        answer += term
    return E.sp.expand(answer)


def main():
    E = load()
    sp = E.sp
    data = json.loads(INTERFACE.read_text())
    frozen = data.pop("logical_sha256")
    require(logical_hash(data) == frozen, "pivot-zero interface digest mismatch")
    b0, d1, d4 = sp.symbols("b0 d1 d4")
    variables = (b0, d1, d4)

    polynomials = {}
    residual = data["coefficient_pivot"]["C0_open_residual_factors"]
    for index, record in enumerate(residual):
        polynomials[f"R{index}"] = parse(sp, record["polynomial"])
    for record in data["forced_consistency_minors"]:
        for factor in record["factorization"]["factors"]:
            terms = factor["profile"]["terms"]
            if terms == 256:
                polynomials["S256"] = parse(sp, factor["polynomial"])
            elif terms == 42:
                polynomials["S42"] = parse(sp, factor["polynomial"])
    require(set(polynomials) == {"R0", "R1", "R2", "R3", "S42", "S256"},
            "factor extraction failed")

    symmetry = {}
    images = {}
    for name, value in polynomials.items():
        matches = []
        for target, target_value in polynomials.items():
            relation = E.relation(value, target_value, variables)
            if relation is not None:
                matches.append((target, relation))
        if matches:
            require(len(matches) == 1, f"ambiguous Laurent image for {name}")
            symmetry[name] = {"target": matches[0][0],
                              "relation": matches[0][1]}
        else:
            image = canonical_image(E, value, variables)
            image_name = f"T({name})"
            images[image_name] = image
            symmetry[name] = {"target": image_name,
                              "relation": E.relation(value, image, variables),
                              "new_factor": profile(sp, image, variables),
                              "new_polynomial": encode(sp, image)}

    # The exact equations after stripping declared live factors are
    #   R0 R1 R2 R3 = 0,
    #   R0 S256 = 0,
    #   R1 R2 R3 S42 = 0.
    # Their inclusion-minimal factor choices are exactly these seven pairs.
    pairs = {
        tuple(sorted(pair)) for pair in (
            ("R0", "R1"), ("R0", "R2"), ("R0", "R3"), ("R0", "S42"),
            ("R1", "S256"), ("R2", "S256"), ("R3", "S256"))
    }
    require(len(pairs) == 7, "minimal-pair census changed")
    require(all(symmetry[name]["target"] in polynomials for name in polynomials),
            "Laurent symmetry leaves the frozen factor set")

    def pair_image(pair):
        return tuple(sorted(symmetry[name]["target"] for name in pair))

    require(all(pair_image(pair) in pairs for pair in pairs),
            "minimal-pair cover is not symmetry stable")
    unseen = set(pairs)
    pair_orbits = []
    while unseen:
        representative = min(unseen)
        orbit = {representative, pair_image(representative)}
        require(all(pair_image(value) in orbit for value in orbit),
                "pair orbit failed involutivity")
        unseen -= orbit
        # Common source-live factors.  The optional product of the R factors
        # not set to zero makes a disjoint generic chart; it is not used in
        # the closed-cover statement.
        selected_r = {name for name in representative if name.startswith("R")}
        complement_r = [name for name in ("R0", "R1", "R2", "R3")
                        if name not in selected_r]
        base_live = sp.expand(b0*d1*d4*(b0**2+d4**2))
        generic_live = base_live
        for name in complement_r:
            generic_live *= polynomials[name]
        generic_live = sp.expand(generic_live)
        pair_orbits.append({
            "representative": list(representative),
            "orbit": [list(value) for value in sorted(orbit)],
            "orbit_size": len(orbit),
            "common_source_live_product": encode(sp, base_live),
            "generic_complement_R_factors": complement_r,
            "optional_generic_live_product_profile": profile(sp, generic_live, variables),
            "optional_generic_live_product": encode(sp, generic_live),
        })

    factor_orbits = []
    unseen_factors = set(polynomials)
    while unseen_factors:
        name = min(unseen_factors)
        target = symmetry[name]["target"]
        orbit = {name, target}
        require(symmetry[target]["target"] == name, f"factor involution failed: {name}")
        unseen_factors -= orbit
        factor_orbits.append({"representative": min(orbit),
                              "members": sorted(orbit), "size": len(orbit)})

    result = {
        "status": "exact D0 pivot-zero Laurent symmetry PASS",
        "interface_logical_sha256": frozen,
        "involution": {"b0": "-b0^-1", "d1": "-d1", "d4": "d4^-1"},
        "factors": {name: {"profile": profile(sp, value, variables),
                           "polynomial": encode(sp, value)}
                    for name, value in sorted(polynomials.items())},
        "factor_images": symmetry,
        "factor_orbits": factor_orbits,
        "minimal_pair_count": len(pairs),
        "minimal_pairs": [list(pair) for pair in sorted(pairs)],
        "pair_orbits": pair_orbits,
        "cover_logic": ["R0*R1*R2*R3=0", "R0*S256=0",
                        "R1*R2*R3*S42=0"],
        "scope_guard": ("The seven closed factor-pair ideals are a necessary "
                        "algebraic cover of the two-row pivot-zero consistency "
                        "interface. Optional complementary-R live products are "
                        "recorded only for later generic charts; no emptiness is claimed."),
        "mutation_control": ("Dropping either consistency product changes the seven-pair "
                             "census; applying the Laurent map twice fixes every factor/pair."),
    }
    result["logical_sha256"] = logical_hash(result)
    (HERE / "results_d0_pivot_zero_symmetry.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("D0 pivot-zero symmetry PASS", result["logical_sha256"])
    print("factor orbits", [record["members"] for record in factor_orbits])
    print("pair orbits", [record["orbit"] for record in pair_orbits])


if __name__ == "__main__":
    main()
