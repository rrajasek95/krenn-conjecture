#!/usr/bin/env python3
"""Exact structural split of the corrected Delta boundary.

The corrected pivot pullback factors as ``C8*D10``.  This checker proves
that ``D10`` is affine in ``b1`` and computes the fraction-free resultant
of the smallest retained row, ``P324``, with ``D10``.  After removing only
the already-live ``d1`` and ``A`` factors, that resultant splits into an
affine four-term ``K4`` pivot in ``d3`` and one 64-term residual.
"""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


_SITE = (Path(sys.executable).parent.parent / "lib" /
         f"python{sys.version_info.major}.{sys.version_info.minor}" /
         "site-packages")
if str(_SITE) not in sys.path:
    sys.path.append(str(_SITE))
import sympy as sp


HERE = Path(__file__).resolve().parent
TREE_PATH = HERE / "audit_branch0_cycle_generic_b3_resultant_tree.py"
SOURCE = HERE / "branch0_cycle_generic_qrstu_codim5_exact.msolve"
RESULT = HERE / "results_branch0_cycle_generic_codim5_d10_structural_split.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


TREE = load("codim5_d10_tree", TREE_PATH)


def encode(poly: sp.Expr, variables) -> str:
    value = sp.Poly(sp.expand(poly), *variables, domain="ZZ").primitive()[1]
    pieces = []
    for monomial, coefficient in value.terms():
        coefficient = int(coefficient)
        factors = [] if abs(coefficient) == 1 else [str(abs(coefficient))]
        for variable, power in zip(variables, monomial, strict=True):
            if power:
                factors.append(str(variable) if power == 1
                               else f"{variable}^{power}")
        body = "*".join(factors) or "1"
        pieces.append(("-" if coefficient < 0 else ("+" if pieces else ""))
                      + body)
    return "".join(pieces) or "0"


def digest(poly: sp.Expr, variables) -> str:
    return sha256(encode(poly, variables).encode("ascii")).hexdigest()


def factor_records(poly: sp.Expr, variables) -> list[dict]:
    primitive = sp.Poly(poly, *variables).primitive()[1].as_expr()
    answer = []
    for factor, power in sp.factor_list(primitive)[1]:
        profile = sp.Poly(factor, *variables)
        record = {
            "terms": len(profile.terms()),
            "degree": int(profile.total_degree()),
            "power": int(power),
            "sha256": digest(factor, variables),
        }
        if len(profile.terms()) <= 14:
            record["expression"] = str(factor)
        answer.append(record)
    return answer


def linear_resultant(poly: sp.Expr, variable: sp.Symbol,
                     leading: sp.Expr, constant: sp.Expr) -> sp.Expr:
    source = sp.Poly(poly, variable)
    degree = source.degree()
    answer = sp.expand(sum(
        coefficient*(-constant)**power*leading**(degree-power)
        for (power,), coefficient in source.terms()))
    require(answer != 0, "fraction-free D10 resultant vanished")
    return answer


def main() -> None:
    lines = SOURCE.read_text().splitlines()
    require(lines[:2] == ["b0,b1,d1,d3,d4,z", "0"],
            "corrected exact source header changed")
    variable_names = lines[0].split(",")
    b0, b1, d1, d3, d4, z = sp.symbols(" ".join(variable_names))
    variables = (b0, b1, d1, d3, d4)
    encoded_rows = "\n".join(lines[2:]).strip().split(",\n")
    require(len(encoded_rows) == 10, "corrected exact row count changed")
    local = dict(zip(variable_names, (*variables, z), strict=True))
    # P324 is the third retained row and is the smallest by exact term count.
    p851 = sp.sympify(encoded_rows[0].replace("^", "**"), locals=local)
    p1342 = sp.sympify(encoded_rows[1].replace("^", "**"), locals=local)
    p324 = sp.sympify(encoded_rows[2].replace("^", "**"), locals=local)
    require(len(sp.Poly(p851, *variables).terms()) == 851
            and sp.Poly(p851, *variables).total_degree() == 18,
            "P851 profile changed")
    require(len(sp.Poly(p1342, *variables).terms()) == 1342
            and sp.Poly(p1342, *variables).total_degree() == 20,
            "P1342 profile changed")
    require(len(sp.Poly(p324, *variables).terms()) == 324
            and sp.Poly(p324, *variables).total_degree() == 15,
            "P324 profile changed")

    core_rows, _, _ = TREE.SOURCE.derive()
    tb0, tb1, b3, td1, td3, td4 = TREE.SOURCE.SOURCE.PARAMETERS
    require((tb0, tb1, td1, td3, td4) == variables,
            "tree/source variable identity changed")
    compact = [sp.cancel(poly/factor) for poly, factor in zip(
        core_rows, (b1*b3*d1*d3, d4, b3, b1*b3, 1, 1, 1),
        strict=True)]
    pivot = compact[1]
    pivot_leading = sp.diff(pivot, b3)
    pivot_constant = sp.expand(pivot.subs(b3, 0))
    a_divisor = sp.cancel(pivot_leading/(2*b0))
    b_constant = sp.cancel(pivot_constant/2)
    true_delta = sp.expand(b0*a_divisor*b1*d3-b_constant*d1*d4)
    factors = sp.factor_list(true_delta)[1]
    c8 = next(factor for factor, power in factors
              if len(sp.Poly(factor, *variables).terms()) == 8)
    d10 = next(factor for factor, power in factors
               if len(sp.Poly(factor, *variables).terms()) == 10)
    require(sp.expand(c8*d10-true_delta) == 0,
            "corrected DeltaN=C8*D10 identity changed")

    d10_poly = sp.Poly(d10, b1)
    require(d10_poly.degree() == 1, "D10 ceased to be affine in b1")
    l6 = sp.expand(d10_poly.coeff_monomial(b1))
    c4 = sp.expand(d10_poly.coeff_monomial(1))
    require(len(sp.Poly(l6, b0, d1, d3, d4).terms()) == 6
            and len(sp.Poly(c4, b0, d1, d3, d4).terms()) == 4
            and sp.expand(d10-l6*b1-c4) == 0,
            "D10 affine coefficient profile changed")

    resultant = linear_resultant(p324, b1, l6, c4)
    primitive = sp.Poly(resultant, b0, d1, d3, d4).primitive()[1].as_expr()
    result_factors = sp.factor_list(primitive)[1]
    profile = [(len(sp.Poly(factor, b0, d1, d3, d4).terms()),
                int(sp.Poly(factor, b0, d1, d3, d4).total_degree()), int(power))
               for factor, power in result_factors]
    require(profile == [(1, 1, 1), (4, 4, 1),
                        (19, 6, 1), (64, 12, 1)],
            "Res_b1(D10,P324) factor profile changed")
    linear_factor = next(factor for factor, power in result_factors
                         if len(sp.Poly(factor, b0, d1, d3, d4).terms()) == 1)
    k4 = next(factor for factor, power in result_factors
              if len(sp.Poly(factor, b0, d1, d3, d4).terms()) == 4)
    recovered_a = next(factor for factor, power in result_factors
                       if len(sp.Poly(factor, b0, d1, d3, d4).terms()) == 19)
    w64 = next(factor for factor, power in result_factors
               if len(sp.Poly(factor, b0, d1, d3, d4).terms()) == 64)
    require(linear_factor in (d1, -d1), "resultant live monomial changed")
    require(sp.expand(recovered_a-a_divisor) == 0
            or sp.expand(recovered_a+a_divisor) == 0,
            "resultant A factor changed")

    k4_poly = sp.Poly(k4, d3)
    require(k4_poly.degree() == 1, "K4 ceased to be affine in d3")
    k4_leading = sp.expand(k4_poly.coeff_monomial(d3))
    k4_constant = sp.expand(k4_poly.coeff_monomial(1))
    require(sp.factor(k4_leading) == b0*(b0+d4)
            and sp.factor(k4_constant) == d1*d4*(b0**2+d4),
            "K4 affine pivot identity changed")
    require(sp.expand(linear_resultant(p324+1, b1, l6, c4)-resultant) != 0,
            "P324 hostile mutation did not fire")

    resultant851 = linear_resultant(p851, b1, l6, c4)
    primitive851 = sp.Poly(
        resultant851, b0, d1, d3, d4).primitive()[1].as_expr()
    factors851 = sp.factor_list(primitive851)[1]
    profile851 = [(len(sp.Poly(factor, b0, d1, d3, d4).terms()),
                   int(sp.Poly(factor, b0, d1, d3, d4).total_degree()),
                   int(power)) for factor, power in factors851]
    require(profile851 == [(4, 3, 1), (8, 5, 1),
                           (19, 6, 2), (8, 6, 1)],
            "Res_b1(D10,P851) factor profile changed")
    recovered_a851 = next(factor for factor, power in factors851
                          if len(sp.Poly(factor, b0, d1, d3, d4).terms()) == 19)
    require(sp.expand(recovered_a851-a_divisor) == 0
            or sp.expand(recovered_a851+a_divisor) == 0,
            "P851 resultant A factor changed")
    branch_factors851 = [
        ("F4", next(factor for factor, power in factors851
                    if len(sp.Poly(factor, b0, d1, d3, d4).terms()) == 4)),
        ("E8", next(factor for factor, power in factors851
                    if len(sp.Poly(factor, b0, d1, d3, d4).terms()) == 8
                    and sp.Poly(factor, b0, d1, d3, d4).total_degree() == 5)),
        ("J8", next(factor for factor, power in factors851
                    if len(sp.Poly(factor, b0, d1, d3, d4).terms()) == 8
                    and sp.Poly(factor, b0, d1, d3, d4).total_degree() == 6)),
    ]
    branch_tree851 = []
    p851_w_factor_sets = {}
    expected_branch_profiles = {
        "F4": {
            "K4": [(1, 1, 1), (5, 4, 1)],
            "W64": [(1, 1, 1), (1, 1, 4), (2, 1, 1),
                    (5, 4, 1), (35, 8, 1)],
        },
        "E8": {
            "K4": [(1, 1, 1), (1, 1, 2), (14, 7, 1)],
            "W64": [(1, 1, 1), (1, 1, 4), (1, 1, 8),
                    (21, 7, 1), (65, 11, 1)],
        },
        "J8": {
            "K4": [(1, 1, 1), (1, 1, 2), (5, 4, 1)],
            "W64": [(1, 1, 4), (1, 1, 4),
                    (5, 4, 1), (105, 18, 1)],
        },
    }
    for label, factor in branch_factors851:
        k_resultant = linear_resultant(
            factor, d3, k4_leading, k4_constant)
        w_resultant = sp.resultant(w64, factor, d3)
        k_records = factor_records(k_resultant, (b0, d1, d4))
        w_records = factor_records(w_resultant, (b0, d1, d4))
        p851_w_factor_sets[label] = [
            item for item, power in sp.factor_list(
                sp.Poly(w_resultant, b0, d1, d4).primitive()[1].as_expr())[1]
            if len(sp.Poly(item, b0, d1, d4).terms()) > 1]
        require([(row["terms"], row["degree"], row["power"])
                 for row in k_records] == expected_branch_profiles[label]["K4"],
                f"K4/{label} resultant profile changed")
        require([(row["terms"], row["degree"], row["power"])
                 for row in w_records] == expected_branch_profiles[label]["W64"],
                f"W64/{label} resultant profile changed")
        branch_tree851.append({
            "P851_factor": label,
            "factor_terms_degree": [
                len(sp.Poly(factor, b0, d1, d3, d4).terms()),
                int(sp.Poly(factor, b0, d1, d3, d4).total_degree())],
            "factor_sha256": digest(factor, (b0, d1, d3, d4)),
            "factor_expression": str(factor),
            "K4_resultant_factors": k_records,
            "W64_resultant_factors": w_records,
        })
    require(sp.expand(linear_resultant(p851+1, b1, l6, c4)
                      - resultant851) != 0,
            "P851 hostile mutation did not fire")

    resultant1342 = linear_resultant(p1342, b1, l6, c4)
    primitive1342 = sp.Poly(
        resultant1342, b0, d1, d3, d4).primitive()[1].as_expr()
    factors1342 = sp.factor_list(primitive1342)[1]
    profile1342 = [(len(sp.Poly(factor, b0, d1, d3, d4).terms()),
                    int(sp.Poly(factor, b0, d1, d3, d4).total_degree()),
                    int(power)) for factor, power in factors1342]
    require(profile1342 == [(1, 1, 1), (1, 1, 1),
                            (1, 1, 1), (1, 1, 1),
                            (4, 3, 1), (4, 4, 1),
                            (19, 6, 2), (39, 9, 1)],
            "Res_b1(D10,P1342) factor profile changed")
    recovered_k1342 = next(factor for factor, power in factors1342
                           if len(sp.Poly(factor, b0, d1, d3, d4).terms()) == 4
                           and sp.Poly(factor, b0, d1, d3, d4).total_degree() == 4)
    require(sp.expand(recovered_k1342-k4) == 0
            or sp.expand(recovered_k1342+k4) == 0,
            "P1342 resultant K4 factor changed")
    recovered_a1342 = next(factor for factor, power in factors1342
                           if len(sp.Poly(factor, b0, d1, d3, d4).terms()) == 19)
    require(sp.expand(recovered_a1342-a_divisor) == 0
            or sp.expand(recovered_a1342+a_divisor) == 0,
            "P1342 resultant A factor changed")
    branch_factors1342 = [
        ("G4", next(factor for factor, power in factors1342
                    if len(sp.Poly(factor, b0, d1, d3, d4).terms()) == 4
                    and sp.Poly(factor, b0, d1, d3, d4).total_degree() == 3)),
        ("K4", recovered_k1342),
        ("N39", next(factor for factor, power in factors1342
                     if len(sp.Poly(factor, b0, d1, d3, d4).terms()) == 39)),
    ]
    expected_w1342 = {
        "G4": [(1, 1, 4), (1, 1, 4), (5, 4, 1), (35, 8, 1)],
        "K4": [(1, 1, 4), (1, 1, 4), (5, 4, 1), (33, 10, 1)],
        "N39": [(1, 1, 1), (1, 1, 8), (1, 1, 12),
                (5, 4, 1), (21, 7, 1), (574, 24, 1)],
    }
    branch_tree1342 = []
    p1342_w_factor_sets = {}
    for label, factor in branch_factors1342:
        w_resultant = sp.resultant(w64, factor, d3)
        records = factor_records(w_resultant, (b0, d1, d4))
        require([(row["terms"], row["degree"], row["power"])
                 for row in records] == expected_w1342[label],
                f"W64/P1342-{label} resultant profile changed")
        p1342_w_factor_sets[label] = [
            item for item, power in sp.factor_list(
                sp.Poly(w_resultant, b0, d1, d4).primitive()[1].as_expr())[1]
            if len(sp.Poly(item, b0, d1, d4).terms()) > 1]
        branch_tree1342.append({
            "P1342_factor": label,
            "factor_terms_degree": [
                len(sp.Poly(factor, b0, d1, d3, d4).terms()),
                int(sp.Poly(factor, b0, d1, d3, d4).total_degree())],
            "factor_sha256": digest(factor, (b0, d1, d3, d4)),
            "factor_expression": str(factor),
            "W64_resultant_factors": records,
        })

    def monic_key(poly: sp.Expr) -> str:
        return str(sp.Poly(poly, b0, d1, d4, domain=sp.QQ).monic().as_expr())

    factor_by_key = {}
    pair_origins = {}
    for left_label, left_factors in p851_w_factor_sets.items():
        for right_label, right_factors in p1342_w_factor_sets.items():
            for left in left_factors:
                left_key = monic_key(left)
                factor_by_key[left_key] = left
                for right in right_factors:
                    right_key = monic_key(right)
                    factor_by_key[right_key] = right
                    pair = tuple(sorted((left_key, right_key)))
                    pair_origins.setdefault(pair, []).append(
                        [left_label, right_label])
    require(len(pair_origins) == 29,
            f"deduplicated W64 P851/P1342 pair count changed: "
            f"{len(pair_origins)}")
    common_pairs = [pair for pair in pair_origins if pair[0] == pair[1]]
    distinct_pairs = [pair for pair in pair_origins if pair[0] != pair[1]]
    require(len(common_pairs) == 2 and len(distinct_pairs) == 27,
            f"W64 common/distinct pair census changed: "
            f"{len(common_pairs)}/{len(distinct_pairs)}")
    for left_key, right_key in distinct_pairs:
        gcd = sp.gcd(sp.Poly(factor_by_key[left_key], b0, d1, d4, domain=sp.QQ),
                     sp.Poly(factor_by_key[right_key], b0, d1, d4, domain=sp.QQ))
        require(gcd.total_degree() == 0,
                "distinct W64 leaf factors acquired a nonunit gcd")
    common_profiles = sorted(
        (len(sp.Poly(factor_by_key[pair[0]], b0, d1, d4).terms()),
         int(sp.Poly(factor_by_key[pair[0]], b0, d1, d4).total_degree()),
         digest(factor_by_key[pair[0]], (b0, d1, d4)))
        for pair in common_pairs)
    require([(terms, degree) for terms, degree, _ in common_profiles]
            == [(5, 4), (21, 7)],
            f"W64 exact common-component profile changed: "
            f"{[(terms, degree) for terms, degree, _ in common_profiles]}")
    require(sp.expand(linear_resultant(p1342+1, b1, l6, c4)
                      - resultant1342) != 0,
            "P1342 hostile mutation did not fire")

    result = {
        "status": "UNAUDITED exact corrected-Delta D10 structural split",
        "source": SOURCE.name,
        "source_sha256": sha256(SOURCE.read_bytes()).hexdigest(),
        "P324_sha256": digest(p324, variables),
        "P851_sha256": digest(p851, variables),
        "P1342_sha256": digest(p1342, variables),
        "true_delta_identity": "TrueDeltaN=C8*D10",
        "C8_terms_degree": [8, 4],
        "C8_sha256": digest(c8, variables),
        "D10_terms_degree": [10, 5],
        "D10_sha256": digest(d10, variables),
        "D10_affine_identity": "D10=L6*b1+C4",
        "L6": str(l6),
        "C4": str(c4),
        "D10_open_solution": "b1=-C4/L6",
        "D10_companion_divisor": "L6=0",
        "P324_b1_degree": int(sp.degree(p324, b1)),
        "resultant_terms_degree": [
            len(sp.Poly(primitive, b0, d1, d3, d4).terms()),
            int(sp.Poly(primitive, b0, d1, d3, d4).total_degree())],
        "resultant_factor_profile": profile,
        "resultant_identity": "Res_b1(D10,P324)=unit*d1*K4*A*W64",
        "K4": str(k4),
        "K4_sha256": digest(k4, (b0, d1, d3, d4)),
        "K4_affine_identity": (
            "K4=b0*(b0+d4)*d3+d1*d4*(b0^2+d4)"),
        "K4_open_solution": (
            "d3=-d1*d4*(b0^2+d4)/(b0*(b0+d4))"),
        "K4_companion_divisor_on_b0_open": "b0+d4=0",
        "W64_terms_degree": [64, 12],
        "W64_sha256": digest(w64, (b0, d1, d3, d4)),
        "hostile_P324_mutation_fired": True,
        "P851_b1_degree": int(sp.degree(p851, b1)),
        "P851_resultant_terms_degree": [
            len(sp.Poly(primitive851, b0, d1, d3, d4).terms()),
            int(sp.Poly(primitive851, b0, d1, d3, d4).total_degree())],
        "P851_resultant_factor_profile": profile851,
        "P851_resultant_identity": "Res_b1(D10,P851)=unit*F4*E8*A^2*J8",
        "P851_branch_tree": branch_tree851,
        "hostile_P851_mutation_fired": True,
        "P1342_b1_degree": int(sp.degree(p1342, b1)),
        "P1342_resultant_terms_degree": [
            len(sp.Poly(primitive1342, b0, d1, d3, d4).terms()),
            int(sp.Poly(primitive1342, b0, d1, d3, d4).total_degree())],
        "P1342_resultant_factor_profile": profile1342,
        "P1342_resultant_identity": (
            "Res_b1(D10,P1342)=unit*b0*d1*d3*d4*G4*K4*A^2*N39"),
        "P1342_redundant_on_K4": True,
        "P1342_W64_branch_tree": branch_tree1342,
        "W64_P851_P1342_dedup": {
            "raw_factor_pair_count": 49,
            "deduplicated_unordered_pair_count": len(pair_origins),
            "exact_common_factor_count": len(common_pairs),
            "exact_common_factor_profiles": [
                {"terms": terms, "degree": degree, "sha256": factor_sha}
                for terms, degree, factor_sha in common_profiles],
            "distinct_pair_count": len(distinct_pairs),
            "distinct_pair_gcds": "all exactly 1 over QQ",
            "resultant_expansion_stopped": True,
            "stop_reason": (
                "29 deduplicated leaves exceeds the declared 20-leaf cap"),
        },
        "hostile_P1342_mutation_fired": True,
        "structural_quotients": {
            "D10_boundary_L6_open_variables": ["b0", "d1", "d3", "d4"],
            "D10_K4_boundary_b0_plus_d4_open_variables":
            ["b0", "d1", "d4"],
            "D10_W64_boundary_variables": ["b0", "d1", "d3", "d4"],
        },
        "scope": (
            "Exact structure of the D10=0 boundary detected by the modular "
            "slice. The target true-Delta-open residual has D10!=0; this "
            "split does not itself prove that the full core is contained in "
            "D10=0 or close the residual."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("corrected Delta D10 structural split: PASS")
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
