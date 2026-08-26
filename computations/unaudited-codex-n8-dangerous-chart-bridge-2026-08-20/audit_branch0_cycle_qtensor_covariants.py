#!/usr/bin/env python3
"""Exact comparison of the generic-cycle factors with four-qubit invariants.

This is a structural audit, not a packet closure.  The sixteen entries are
the literal superpair quadrics Q_s.  We pull the standard degree-two H and
the three 4-by-4 flattening determinants through the same source-derived
Cramer solves used by the generic-cycle resultant tree, then through the
A-open affine b3 solve.  Exact factor/gcd profiles decide whether the
recurring factors are associates or divisors; numerical analogy is not used.
"""

from __future__ import annotations

from hashlib import sha256
import argparse
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
GENERIC_PATH = (HERE.parent / "unaudited-codex-root-integration-2026-08-20" /
                "discover_branch0_k4_cycle_cramer_generic.py")
TREE_PATH = HERE / "audit_branch0_cycle_generic_b3_resultant_tree.py"
GCD_PATH = HERE / "export_branch0_cycle_generic_q4098_r4885_gcd.py"
FULL_PATH = HERE / "export_branch0_cycle_generic_azero_bzero_full_source_exact.py"
CORE_PATH = (HERE.parent / "unaudited-codex-n8-orbit0-normalized-78-2026-08-20" /
             "audit_polarized_superpair_core_identity.py")
RESULT = HERE / "results_branch0_cycle_qtensor_covariants.json"


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


GENERIC = load("cycle_qtensor_generic", GENERIC_PATH)
TREE = load("cycle_qtensor_tree", TREE_PATH)
GCD_SOURCE = load("cycle_qtensor_gcd", GCD_PATH)
FULL_SOURCE = load("cycle_qtensor_full", FULL_PATH)
CORE = load("cycle_qtensor_literal_q", CORE_PATH)


def primitive(poly: sp.Expr, variables: tuple[sp.Symbol, ...]) -> sp.Expr:
    return sp.Poly(sp.expand(poly), *variables, domain="QQ").primitive()[1].as_expr()


def profile(poly: sp.Expr, variables: tuple[sp.Symbol, ...]) -> list[int]:
    value = sp.Poly(poly, *variables, domain="QQ")
    return [len(value.terms()), value.total_degree()]


def polynomial_sha(poly: sp.Expr, variables: tuple[sp.Symbol, ...]) -> str:
    value = primitive(poly, variables)
    return sha256(str(sp.expand(value)).encode("ascii")).hexdigest()


def source_solutions():
    raw_rows, _ = GENERIC.SOURCE.data()
    rows = {label: GENERIC.expression(poly) for label, poly, _ in raw_rows}
    upper = [rows[f"cofactor_{edge}_0"] for edge in range(1, 5)]
    p_solution = sp.solve(upper, GENERIC.P, dict=True, simplify=False)[0]
    c50 = GENERIC.numerator(rows["cofactor_5_0"], p_solution)
    a0_solution = sp.solve(c50, GENERIC.A0, dict=True, simplify=False)[0]
    t023 = GENERIC.numerator(
        GENERIC.numerator(rows["t_023"], p_solution), a0_solution)
    a5_solution = sp.solve(t023, GENERIC.A5, dict=True, simplify=False)[0]
    return rows, p_solution, a0_solution, a5_solution


def q_tensor() -> list[sp.Expr]:
    p1, p2, p3, p4 = GENERIC.P
    a0, a5 = GENERIC.A0, GENERIC.A5
    b0, b1, b3, d1, d3, d4 = GENERIC.PARAMETERS
    # Literal block order (00,01,10,11) on edges
    # 01,02,03,12,13,23.  This is exactly c=-(1+ad)/b,
    # b2=b4=b5=d2=1, d0=d5=0.
    blocks = (
        (a0, b0, -1/b0, 0),
        (p1/d1, b1, -(1+p1)/b1, d1),
        (p2, 1, -(1+p2), 1),
        (p3/d3, b3, -(1+p3)/b3, d3),
        (p4/d4, 1, -(1+p4), d4),
        (a5, 1, -1, 0),
    )
    edges = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
    edge_index = {edge: index for index, edge in enumerate(edges)}

    def entry(i: int, j: int, ci: int, cj: int) -> sp.Expr:
        if i > j:
            i, j, ci, cj = j, i, cj, ci
        return blocks[edge_index[(i, j)]][2*ci+cj]

    pairs = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))
    answer = []
    for value in range(16):
        bits = tuple((value >> (3-index)) & 1 for index in range(4))
        answer.append(sp.cancel(sum(
            entry(i, j, bits[i], bits[j]) * entry(k, l, bits[k], bits[l])
            for (i, j), (k, l) in pairs)))
    # Literal-source guard: independently replay all sixteen Counter-based
    # q_orientation polynomials from the 24 raw block entries.
    raw_entries = tuple(value for block in blocks for value in block)
    for value, observed in enumerate(answer):
        bits = tuple((value >> (3-index)) & 1 for index in range(4))
        source = CORE.q_orientation(bits)
        replay = sum(coefficient*sp.prod(raw_entries[index]
                                          for index in monomial)
                     for monomial, coefficient in source.items())
        require(sp.cancel(replay-observed) == 0,
                f"literal Q_{value:04b} replay failed")
        if value == 0:
            monomial, coefficient = sorted(source.items())[0]
            mutated = replay - 2*coefficient*sp.prod(
                raw_entries[index] for index in monomial)
            require(sp.cancel(mutated-observed) != 0,
                    "literal Q mutation failed to fire")
    return answer


def determinant4(entries: list[list[sp.Expr]]) -> sp.Expr:
    return sp.Matrix(entries).det(method="domain-ge")


def invariants(q: list[sp.Expr]) -> dict[str, sp.Expr]:
    # Luque--Thibon H, with q indexed lexicographically by four bits.
    h = (q[0]*q[15] - q[1]*q[14] - q[2]*q[13] + q[3]*q[12]
         - q[4]*q[11] + q[5]*q[10] + q[6]*q[9] - q[7]*q[8])
    flattenings = {}
    for left in ((0, 1), (0, 2), (0, 3)):
        right = tuple(index for index in range(4) if index not in left)
        matrix = []
        for row in range(4):
            matrix_row = []
            for column in range(4):
                bits = [0]*4
                bits[left[0]], bits[left[1]] = (row >> 1) & 1, row & 1
                bits[right[0]], bits[right[1]] = ((column >> 1) & 1,
                                                   column & 1)
                index = sum(bit << (3-site) for site, bit in enumerate(bits))
                matrix_row.append(q[index])
            matrix.append(matrix_row)
        flattenings["L" + "".join(map(str, left))] = determinant4(matrix)
    return {"H2": sp.cancel(h), **flattenings}


def hyperdeterminant4(q: list[sp.Expr]) -> sp.Expr:
    """Cayley 2x2x2x2 hyperdeterminant as a quartic discriminant."""
    t = sp.Symbol("hyperdet_t")
    a = [q[index] + t*q[index + 8] for index in range(8)]
    det3 = (
        a[0]**2*a[7]**2 + a[1]**2*a[6]**2
        + a[2]**2*a[5]**2 + a[4]**2*a[3]**2
        - 2*(a[0]*a[7]*(a[3]*a[4] + a[5]*a[2] + a[6]*a[1])
             + a[3]*a[4]*(a[5]*a[2] + a[6]*a[1])
             + a[5]*a[2]*a[6]*a[1])
        + 4*(a[0]*a[6]*a[5]*a[3] + a[7]*a[1]*a[2]*a[4]))
    return sp.cancel(sp.discriminant(sp.together(det3), t))


def choose_factor(poly: sp.Expr, variables: tuple[sp.Symbol, ...], terms: int):
    value = primitive(poly, variables)
    factors = sp.factor_list(value)[1]
    candidates = [factor for factor, exponent in factors
                  if len(sp.Poly(factor, *variables).terms()) == terms]
    require(len(candidates) == 1, f"unique {terms}-term factor missing")
    return candidates[0]


def recurring_factors():
    rows, _, _ = TREE.SOURCE.derive()
    b0, b1, b3, d1, d3, d4 = GENERIC.PARAMETERS
    variables = (b0, b1, d1, d3, d4)
    compact = [sp.cancel(poly/factor) for poly, factor in zip(
        rows, (b1*b3*d1*d3, d4, b3, b1*b3, 1, 1, 1), strict=True)]
    leading = sp.diff(compact[1], b3)
    constant = sp.expand(compact[1].subs(b3, 0))
    aa = sp.cancel(leading/(2*b0))
    bb = sp.cancel(constant/2)
    resultant33 = TREE.linear_resultant(compact[5], b3, leading, constant)
    c8 = choose_factor(resultant33, variables, 8)
    q4098 = choose_factor(resultant33, variables, 4098)
    gcd_variables, q2, r4885, *_ = GCD_SOURCE.derive()
    require(gcd_variables == variables and sp.expand(q2-q4098) == 0,
            "Q4098 provenance changed")
    lower, *_ = FULL_SOURCE.derive_lower_cofactors()
    s4331 = choose_factor(TREE.linear_resultant(
        lower[1], b3, leading, constant), variables, 4331)
    t4750 = choose_factor(TREE.linear_resultant(
        lower[2], b3, leading, constant), variables, 4750)
    u3217 = choose_factor(TREE.linear_resultant(
        lower[5], b3, leading, constant), variables, 3217)
    return variables, leading, constant, {
        "A": aa, "B": bb, "C8": c8, "Q4098": q4098,
        "R4885": r4885, "S4331": s4331, "T4750": t4750,
        "U3217": u3217,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", action="store_true")
    parser.add_argument("--slice", action="store_true")
    args = parser.parse_args()
    if args.raw:
        raw_variables = GENERIC.SYMBOLS
        for label, value in invariants(q_tensor()).items():
            top = primitive(sp.cancel(value).as_numer_denom()[0], raw_variables)
            factors = sp.factor_list(top)[1]
            print(label, profile(top, raw_variables),
                  [(profile(factor, raw_variables), int(power),
                    str(sp.factor(factor)) if profile(factor, raw_variables)[0] <= 20
                    else polynomial_sha(factor, raw_variables))
                   for factor, power in factors], flush=True)
        return
    if args.slice:
        _, p_solution, a0_solution, a5_solution = source_solutions()
        raw_q = q_tensor()
        variables, leading, constant, candidates = recurring_factors()
        x = variables[0]
        slices = (
            {variables[1]: 2, variables[2]: 3, variables[3]: 5,
             variables[4]: 7},
            {variables[1]: 3, variables[2]: 2, variables[3]: 7,
             variables[4]: 5},
        )
        records = []
        for slice_index, fixed in enumerate(slices):
            b3_value = sp.cancel((-constant/leading).subs(fixed))
            local_p = {key: sp.cancel(value.subs(fixed).subs(
                GENERIC.PARAMETERS[2], b3_value))
                       for key, value in p_solution.items()}
            local_a0 = {key: sp.cancel(value.subs(fixed).subs(
                GENERIC.PARAMETERS[2], b3_value))
                        for key, value in a0_solution.items()}
            local_a5 = {key: sp.cancel(value.subs(fixed).subs(
                GENERIC.PARAMETERS[2], b3_value))
                        for key, value in a5_solution.items()}
            local_q = []
            for value in raw_q:
                pulled = value.subs(fixed).subs(
                    GENERIC.PARAMETERS[2], b3_value)
                local_q.append(sp.cancel(pulled.subs(local_p).subs(local_a0)
                                         .subs(local_a5)))
            pulled_covariants = invariants(local_q)
            pulled_covariants["Hyperdet24"] = hyperdeterminant4(local_q)
            covariants = {}
            for label, pulled in pulled_covariants.items():
                pulled = sp.cancel(pulled)
                top, bottom = pulled.as_numer_denom()
                top = sp.Poly(top, x, domain="QQ").primitive()[1]
                bottom = sp.Poly(bottom, x, domain="QQ").primitive()[1]
                covariants[label] = (top, bottom)
            candidate_records = {}
            for candidate_label, candidate in candidates.items():
                candidate_poly = sp.Poly(candidate.subs(fixed), x,
                                         domain="QQ").primitive()[1]
                require(candidate_poly.degree() > 0,
                        f"{candidate_label} collapsed on slice {slice_index}")
                tests = {}
                for invariant_label, (top, bottom) in covariants.items():
                    top_gcd = sp.gcd(candidate_poly, top).primitive()[1]
                    bottom_gcd = sp.gcd(candidate_poly, bottom).primitive()[1]
                    tests[invariant_label] = {
                        "numerator_gcd_degree": top_gcd.degree(),
                        "denominator_gcd_degree": bottom_gcd.degree(),
                    }
                candidate_records[candidate_label] = {
                    "degree": candidate_poly.degree(), "tests": tests}
            records.append({
                "fixed": {str(key): value for key, value in fixed.items()},
                "candidate_tests": candidate_records,
                "covariant_degrees": {
                    label: [top.degree(), bottom.degree()]
                    for label, (top, bottom) in covariants.items()},
            })
            print("slice", slice_index, "done", flush=True)
        result = {
            "status": "UNAUDITED exact univariate-slice covariant exclusion",
            "records": records,
            "scope": (
                "Each entry is an exact QQ[b0] gcd after the literal Cramer "
                "and A-open b3 pullback. A global divisibility would survive "
                "every denominator-regular specialization; numerator gcd zero "
                "degree on either recorded slice disproves it. Denominator "
                "gcds explicitly flag nonregular comparisons."),
        }
        logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
        result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
        RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print("result sha256:", result["result_sha256"])
        return
    _, p_solution, a0_solution, a5_solution = source_solutions()
    q = q_tensor()
    inv = invariants(q)
    variables, leading, constant, factors = recurring_factors()
    b3 = GENERIC.PARAMETERS[2]
    records = {}
    for label, value in inv.items():
        # Pull back through source Cramer solves.  Repeated numerator calls
        # preserve the exact denominator provenance used in source rows.
        current = GENERIC.numerator(value, p_solution)
        current = GENERIC.numerator(current, a0_solution)
        current = GENERIC.numerator(current, a5_solution)
        cramer = primitive(current, GENERIC.PARAMETERS)
        resultant = TREE.linear_resultant(cramer, b3, leading, constant)
        aopen = primitive(resultant, variables)
        factorization = sp.factor_list(aopen)[1]
        factor_profile = [
            [len(sp.Poly(factor, *variables).terms()),
             sp.Poly(factor, *variables).total_degree(), int(power),
             polynomial_sha(factor, variables)]
            for factor, power in factorization]
        gcds = {}
        for candidate_label, candidate in factors.items():
            gcd = sp.gcd(sp.Poly(aopen, *variables),
                         sp.Poly(candidate, *variables)).primitive()[1].as_expr()
            gcds[candidate_label] = profile(gcd, variables)
        records[label] = {
            "after_cramer_profile": profile(cramer, GENERIC.PARAMETERS),
            "aopen_profile": profile(aopen, variables),
            "aopen_factor_profile": factor_profile,
            "gcd_profiles_with_recurring_factors": gcds,
            "aopen_sha256": polynomial_sha(aopen, variables),
        }
        print(label, records[label]["after_cramer_profile"],
              records[label]["aopen_profile"], factor_profile)

    recurring = {label: {"profile": profile(value, variables),
                         "sha256": polynomial_sha(value, variables)}
                 for label, value in factors.items()}
    result = {
        "status": "UNAUDITED exact four-qubit covariant comparison",
        "q_tensor_convention": (
            "Q_s=sum over the three complementary superedge pairs; bit order "
            "is 0000..1111 and block order is (00,01,10,11)."),
        "covariants": records,
        "recurring_factors": recurring,
        "scope": (
            "Exact characteristic-zero pullback through the same literal "
            "Cramer and A-open b3 solves. GCD profile [1,0] proves no common "
            "factor. This tests H and all three flattening determinants, not "
            "the degree-24 hyperdeterminant or every possible covariant."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
