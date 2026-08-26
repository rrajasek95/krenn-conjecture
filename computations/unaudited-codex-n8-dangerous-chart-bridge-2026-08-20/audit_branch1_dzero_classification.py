#!/usr/bin/env python3
"""Exact classification of the branch-1, uniform-d-zero Laurent chart.

This is the simultaneous chart with cofactor-orientation mask 1 and
permanent support on the off-diagonal product in every block:

    M_e=[[a_e,b_e],[-1/b_e,0]],  all b_e nonzero.

After the gauge b2=b4=b5=1 its H-live variety has exactly two irreducible
one-parameter components.  The parameter is T=a5.  T=0 gives the previously
closed support-six stratum; T nonzero gives Q-support exactly eleven.
"""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from math import isqrt
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "unaudited-codex-n8-orbit0-normalized-78-2026-08-20"
DZERO_PATH = SOURCE / "analyze_weight0_dzero_lowq_chart.py"
PROBE_PATH = HERE / "probe_branch1_dzero_components.py"
S6_PATH = HERE / "audit_support6_component_pairwise_obstruction.py"
OUT = HERE / "results_branch1_dzero_classification.json"
BRANCH_MASK = 1
Q_CONSTANT = frozenset((3, 5, 6, 9, 10, 12))
Q_LINEAR = frozenset((1, 2, 4, 8))
Q_QUADRATIC = frozenset((0,))
Q_IDENTICALLY_ZERO = frozenset((7, 11, 13, 14, 15))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


DZERO = load("n8_b1_class_dzero", DZERO_PATH)
PROBE = load("n8_b1_class_probe", PROBE_PATH)
S6 = load("n8_b1_class_s6", S6_PATH)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def singular_component_census():
    equations, raw_h = DZERO.SCREEN.PROBE.equations(
        DZERO.SCREEN.branch_bits(BRANCH_MASK))
    base = tuple(DZERO.clear_denominators(DZERO.substitute(poly))
                 for poly in equations if DZERO.substitute(poly))
    cleared_h = DZERO.clear_denominators(DZERO.substitute(raw_h))
    require(len(base) == 11, "surviving literal row count changed")
    variables = ",".join([f"a{i}" for i in range(6)]
                         + [f"b{i}" for i in range(6)] + ["u", "z"])
    ideal = ",".join(DZERO.singular(poly) for poly in base)
    b_product = "*".join(f"b{i}" for i in range(6))
    command = (
        f"ring R=0,({variables}),dp; ideal I={ideal},"
        f"b2-1,b4-1,b5-1,u*({DZERO.singular(cleared_h)})-1,"
        f"z*{b_product}-1; ideal G=std(I); LIB \"primdec.lib\"; "
        "list L=minAssGTZ(I); print(\"BEGIN\"); print(dim(G)); "
        "print(size(L)); for(int i=1;i<=size(L);i++)"
        "{ideal J=L[i];ideal K=std(J);print(dim(K));}; "
        "print(\"END\"); quit;"
    )
    completed = subprocess.run(["Singular", "-q", "-c", command],
                               text=True, capture_output=True,
                               timeout=60, check=False)
    require(completed.returncode == 0 and not completed.stderr.strip(),
            "Singular component census failed: " + completed.stderr[-1000:])
    lines = completed.stdout.splitlines()
    begin, end = lines.index("BEGIN"), lines.index("END")
    body = [line for line in lines[begin + 1:end]
            if not line.startswith("//")]
    require(body == ["1", "2", "1", "1"],
            f"component census changed: {body}")
    return {"surviving_literal_rows": len(base), "dimension": 1,
            "minimal_prime_count": 2,
            "minimal_prime_dimensions": [1, 1]}


def encode_k(value):
    return [[entry.numerator, entry.denominator] for entry in value]


def encode_pt(poly):
    return [{"T_degree": degree, "coefficient_1_z": encode_k(coefficient)}
            for degree, coefficient in sorted(poly.items())]


def main():
    census = singular_component_census()
    components = []
    for p in (14, -2):
        row = PROBE.component(p)
        discriminant = p * p + 4
        require(isqrt(discriminant) ** 2 != discriminant,
                "quadratic component field became reducible")
        q_support = {index for index, value in enumerate(row["Q"]) if value}
        require(q_support == (Q_CONSTANT | Q_LINEAR | Q_QUADRATIC),
                "generic Q polynomial support changed")
        for index in Q_CONSTANT:
            require(set(row["Q"][index]) == {0},
                    "a constant Q ceased to have degree zero")
        for index in Q_LINEAR:
            require(set(row["Q"][index]) == {1},
                    "a linear Q ceased to be a nonzero T multiple")
        require(set(row["Q"][0]) == {2},
                "Q0 ceased to be a nonzero T-square multiple")
        require(not any(row["Q"][index] for index in Q_IDENTICALLY_ZERO),
                "an identically-zero Q coordinate became live")
        require(row["H"] == {0: (PROBE.F(4), PROBE.F(0))},
                "pure H ceased to be the constant four")
        require(all(alpha != (PROBE.F(0), PROBE.F(0))
                    for alpha in row["alpha"]),
                "a T-dependent diagonal cell coefficient vanished")

        c_at_zero = frozenset(index for index, value in enumerate(row["C"])
                              if value.get(0, (0, 0)) != (0, 0))
        c_generic = frozenset(index for index, value in enumerate(row["C"])
                              if value)
        x_at_zero = frozenset(4 * edge + position
                              for edge in range(6) for position in (1, 2))
        x_generic = x_at_zero | frozenset(4 * edge for edge in range(6))
        q_at_zero = Q_CONSTANT
        record_at_zero = (x_at_zero, c_at_zero, q_at_zero)
        canonical = (x_at_zero, frozenset((9, 10, 13, 14)), Q_CONSTANT)
        actions = tuple((permutation, flips)
                        for permutation in __import__("itertools").permutations(range(4))
                        for flips in __import__("itertools").product((0, 1), repeat=4))
        orbit = frozenset(
            (S6.act_support(canonical[0], S6.raw_action_index, *action),
             S6.act_support(canonical[1], S6.raw_action_index, *action),
             S6.act_support(canonical[2], S6.q_action_index, *action))
            for action in actions
        )
        require(record_at_zero in orbit,
                "T=0 point left the support-six joint orbit")

        components.append({
            "minimal_polynomial": f"z^2-{p}*z-1" if p >= 0
                                  else f"z^2+{-p}*z-1",
            "quadratic_relation_p_in_z2_equals_pz_plus_1": p,
            "discriminant": discriminant,
            "parameter": "T=a5",
            "b_01_02_03_12_13_23": [encode_k(value)
                                      for value in row["b"]],
            "a_over_T_01_02_03_12_13_23": [encode_k(value)
                                             for value in row["alpha"]],
            "pure_H": encode_pt(row["H"]),
            "Q_polynomials": {str(index): encode_pt(value)
                              for index, value in enumerate(row["Q"])},
            "cofactor_polynomials": {str(index): encode_pt(value)
                                     for index, value in enumerate(row["C"])},
            "T_zero": {
                "Q_support": sorted(q_at_zero),
                "entry_support": sorted(x_at_zero),
                "cofactor_support": sorted(c_at_zero),
                "support6_joint_orbit": True,
            },
            "T_nonzero": {
                "Q_support": sorted(q_support),
                "Q_support_size": len(q_support),
                "entry_support": sorted(x_generic),
                "cofactor_support": sorted(c_generic),
            },
        })

    require(len(components) == census["minimal_prime_count"],
            "explicit component count does not match minAssGTZ")
    result = {
        "status": "UNAUDITED exact branch-1 d=0 classification",
        "simultaneous_chart": {
            "cofactor_orientation_mask": BRANCH_MASK,
            "cofactor_bits_01_02_03_12_13_23": [1, 0, 0, 0, 0, 0],
            "cell_zero_pattern": "x_e^(11)=d_e=0 on all six blocks",
            "permanent_pattern": "b_e*c_e=-1 on all six blocks",
            "warning": (
                "This is not the joint pair (cofactor mask 1, permanent "
                "mask 1); the permanent support mask is the all-six "
                "off-diagonal pattern."
            ),
        },
        "gauge": "b2=b4=b5=1",
        "exact_component_census": census,
        "components": components,
        "Q_degree_partition": {
            "constant_nonzero": sorted(Q_CONSTANT),
            "linear_nonzero_times_T": sorted(Q_LINEAR),
            "quadratic_nonzero_times_T_squared": sorted(Q_QUADRATIC),
            "identically_zero": sorted(Q_IDENTICALLY_ZERO),
        },
        "classification": (
            "On both irreducible components H=4. At T=0 the point has "
            "Q-support six and belongs to the globally excluded support-six "
            "joint orbit. At every T nonzero the Q-support is exactly eleven."
        ),
        "pairwise_consequence": (
            "A T-nonzero point can satisfy the 4+4 cross-Q packet only with "
            "a partner having Q-support at most five. Excluding all such "
            "partners is a separate global one-colour lemma and is not "
            "claimed here."
        ),
        "scope": (
            "This classifies the stated simultaneous cofactor/cell-zero chart "
            "and all its B4 transforms, after the standard nonzero-b gauge."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("branch-1 d=0 classification: PASS")
    print("dimension / components:", census["dimension"],
          census["minimal_prime_count"])
    print("T=0 / T!=0 Q support sizes:", len(Q_CONSTANT),
          len(Q_CONSTANT | Q_LINEAR | Q_QUADRATIC))
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
