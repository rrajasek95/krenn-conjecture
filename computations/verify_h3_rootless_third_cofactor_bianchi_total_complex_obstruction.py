#!/usr/bin/env python3
r"""Third-cofactor / two-chart PP total-complex audit at rootless h=3.

The genuine unary third cofactor J_M=1 is identified with the top coefficient
of the physical four-principal-parts cube.  The complete Hasse totalization
then has an explicit proper-face tail of type

    (anchor incidence, w, target, ordinary residue) = (-1,0,0,0).

The tail is a formal C_rel in the prolonged presentation and d^2=0 exactly.
It is not a source-valid physical cell.  The selected fourth operator sends
the source equation H_m to the unit, and the physical and zero-endpoint
two-chart cubes have two nonmatching endpoint-decorated ridges.  Their equal
scalar tops therefore cannot be identified by a source-labelled chain map.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from math import gcd
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LEDGER_SHA256 = "493899d93b7eafd6fd520dc01795c1b7051f549421c0d3a2363c1a780a6bac0f"
PINS = {
    "computations/verify_h3_rootless_first_bianchi_selector_operation_no_go.py":
        "98691b0cc5e3b89ebf3373c207cba15953ee0a4cce4dbf7708602d23a9268073",
    "computations/verify_h3_pure_unary_cofactor_incidence_attachment.py":
        "3295183db431e14733eceea645a28113eccd086eebbf256afaa7127cc826b8cd",
    "computations/verify_h3_qzero_denominator_rees_four_cube.py":
        "70600661cd6a14e509a9e6487d4caa833c8bdb4419a2f442efd4b95bed7eebda",
    "computations/verify_h3_full_hasse_cone_d4_descent_obstruction.py":
        "ed2f2b3451074500b39a100da91ffefed27f748636de172d81aabd5cfe394240",
    "computations/verify_h3_full_hasse_koszul_cap_totalization.py":
        "51940ce0ac8387b68e7725508db6da1a1c055ea036335bbf19750580c69e13fb",
    "computations/verify_h3_source_base_change_conormal_obstruction.py":
        "1a921671ab378f68355c2a6196d1951cad30244d78a9e90ec2715ce47ef12bf0",
    "computations/verify_h3_selector_localized_attaching_output_grade_obstruction.py":
        "ab067701e5d0e5266b0769b7ad089ab99e3265381a7ae49677dea31b776fbfe5",
}

SITES = tuple(range(8))
X = 0
D = (1, 2, 3, 4, 5)
P = 6
Q_SITE = 7
R = 3
FORBIDDEN_EDGE = tuple(sorted((P, R)))
PHYSICAL_WORD = (0, 1, 2, 1, 1, 2, 2, 2)
PURE_WORD = (0,) * 8
Y = "Y"
U_TARGET = "u"
ZERO = Q(0)

Monomial = tuple[str, ...]
Polynomial = Counter[Monomial]
Module = dict[tuple[str, tuple[str, ...]], Polynomial]


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"pinned dependency changed: {relative}")


def clean(polynomial: Polynomial) -> Polynomial:
    return Counter({monomial: coefficient
                    for monomial, coefficient in polynomial.items()
                    if coefficient})


def add(*polynomials: Polynomial) -> Polynomial:
    answer: Polynomial = Counter()
    for polynomial in polynomials:
        answer.update(polynomial)
    return clean(answer)


def scale(value, polynomial: Polynomial) -> Polynomial:
    value = Q(value)
    return clean(Counter({monomial: value * coefficient
                          for monomial, coefficient in polynomial.items()}))


def multiply(*polynomials: Polynomial) -> Polynomial:
    answer: Polynomial = Counter({(): Q(1)})
    for polynomial in polynomials:
        output: Polynomial = Counter()
        for left, left_value in answer.items():
            for right, right_value in polynomial.items():
                output[tuple(sorted(left + right))] += left_value * right_value
        answer = clean(output)
    return answer


def variable(name: str) -> Polynomial:
    return Counter({(name,): Q(1)})


def cell_name(edge: tuple[int, int], left: int, right: int) -> str:
    i, j = edge
    require(i < j, edge)
    return f"a{i}{j}_{left}{right}"


def cell(edge: tuple[int, int], word: tuple[int, ...]) -> str:
    i, j = edge
    return cell_name(edge, word[i], word[j])


def perfect_matchings(vertices) -> tuple[tuple[tuple[int, int], ...], ...]:
    vertices = tuple(sorted(vertices))
    if not vertices:
        return ((),)
    first = vertices[0]
    result = []
    for second in vertices[1:]:
        remainder = tuple(site for site in vertices
                          if site not in (first, second))
        edge = tuple(sorted((first, second)))
        for tail in perfect_matchings(remainder):
            result.append((edge,) + tail)
    return tuple(result)


def hafnian(word: tuple[int, ...], direct_free: bool = True) -> Polynomial:
    output: Polynomial = Counter()
    for matching in perfect_matchings(SITES):
        if direct_free and FORBIDDEN_EDGE in matching:
            continue
        output = add(output, multiply(*(
            variable(cell(edge, word)) for edge in matching
        )))
    return output


def derivative(polynomial: Polynomial, variables) -> Polynomial:
    answer = polynomial.copy()
    for name in variables:
        output: Polynomial = Counter()
        for monomial, coefficient in answer.items():
            if name not in monomial:
                continue
            terms = list(monomial)
            terms.remove(name)
            output[tuple(terms)] += coefficient
        answer = clean(output)
    return answer


def subsets(items: tuple[str, ...]):
    for size in range(len(items) + 1):
        for subset in combinations(items, size):
            yield subset


def chart_word(v: int) -> tuple[int, ...]:
    word = [0] * 8
    for site in D:
        if site != v:
            word[site] = PHYSICAL_WORD[site]
    return tuple(word)


def marked_variables(v: int, matching, word: tuple[int, ...]) -> tuple[str, ...]:
    edges = ((P, Q_SITE), (X, v), *matching)
    return tuple(cell(edge, word) for edge in edges)


def rank(rows) -> int:
    work = [list(map(Q, row)) for row in rows]
    width = len(work[0]) if work else 0
    answer = 0
    for column in range(width):
        pivot = next((row for row in range(answer, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[answer], work[pivot] = work[pivot], work[answer]
        pivot_value = work[answer][column]
        work[answer] = [value / pivot_value for value in work[answer]]
        for row in range(len(work)):
            if row == answer or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[answer], strict=True)]
        answer += 1
    return answer


def cube_and_third_cofactor_audit():
    physical = hafnian(PHYSICAL_WORD)
    pure_h = hafnian(PURE_WORD)
    b = add(pure_h, scale(-1, variable(U_TARGET)))
    require(len(physical) == 90 and len(pure_h) == 90,
            "direct-free row term count changed")

    records = []
    omega_rows = []
    ridge_rows = []
    ridge_labels: set[str] = set()
    formal_tail_checks = 0

    for v in D:
        face = tuple(site for site in D if site != v)
        for matching in perfect_matchings(face):
            pword = PHYSICAL_WORD
            cword = chart_word(v)
            physical_marked = marked_variables(v, matching, pword)
            chart_marked = marked_variables(v, matching, cword)
            require(len(set(physical_marked)) == len(set(chart_marked)) == 4,
                    "marked variables collided")

            chart = hafnian(cword)
            physical_top = derivative(physical, physical_marked)
            chart_top = derivative(chart, chart_marked)
            unit = Counter({(): Q(1)})
            require(physical_top == chart_top == unit,
                    ("four-cube top stopped being a unit", v, matching))

            # After differentiating the physical pq:22 row, the remaining
            # six-site polynomial is the unary q^[3].  M={xv}+N is a perfect
            # matching of those sites and its third cofactor is the same top.
            unary = derivative(physical, (physical_marked[0],))
            third_matching_variables = physical_marked[1:]
            j_m = derivative(unary, third_matching_variables)
            require(j_m == physical_top == unit,
                    "unary J_M is not the four-cube top")

            facet_differences = []
            omega: Polynomial = Counter()
            for index in range(4):
                p_face = derivative(
                    physical,
                    tuple(value for position, value in enumerate(physical_marked)
                          if position != index),
                )
                c_face = derivative(
                    chart,
                    tuple(value for position, value in enumerate(chart_marked)
                          if position != index),
                )
                require(p_face == variable(physical_marked[index]),
                        ("physical ridge is not the omitted cell", v, matching, index))
                require(c_face == variable(chart_marked[index]),
                        ("chart ridge is not the omitted cell", v, matching, index))
                difference = add(p_face, scale(-1, c_face))
                facet_differences.append(difference)
                omega = add(omega, scale(-1 if index % 2 else 1, difference))
                for monomial in difference:
                    ridge_labels.update(monomial)

            # Internal decorated cells agree.  The pq and xv endpoint cells
            # do not, so a top-only bridge has a primitive two-ridge defect.
            require(bool(facet_differences[0]) and bool(facet_differences[1])
                    and not facet_differences[2] and not facet_differences[3],
                    ("endpoint ridge pattern changed", v, matching,
                     facet_differences))
            require(len(omega) == 4
                    and gcd(*(abs(int(value)) for value in omega.values())) == 1,
                    ("bridge obstruction is not primitive", omega))

            # Build the complete Hasse-Koszul chain
            #   s_I=sum_S d_S(A) r0[I\S] - B rm[I].
            # Its proper-face tail is the formal relative cell.
            i_tuple = physical_marked
            derivatives = {subset: derivative(physical, subset)
                           for subset in subsets(i_tuple)}

            s_chain: Module = {}
            for subset, coefficient in derivatives.items():
                complement = tuple(value for value in i_tuple
                                   if value not in subset)
                s_chain[("r0", complement)] = coefficient
            s_chain[("rm", i_tuple)] = scale(-1, b)

            def module_add(target: Module, basis, polynomial):
                target[basis] = add(target.get(basis, Counter()), polynomial)
                if not target[basis]:
                    del target[basis]

            def differential(chain: Module) -> Module:
                output: Module = {}
                for (kind, labels), coefficient in chain.items():
                    if kind == "r0":
                        module_add(output, ("Eq", labels),
                                   multiply(coefficient, b))
                    elif kind == "rm":
                        for subset in subsets(labels):
                            complement = tuple(value for value in labels
                                               if value not in subset)
                            module_add(output, ("Eq", complement),
                                       multiply(coefficient,
                                                derivative(physical, subset)))
                    elif kind == "T":
                        module_add(output, ("w", ()),
                                   multiply(coefficient,
                                            scale(-1, variable(Y))))
                    elif kind in ("Eq", "w"):
                        pass
                    else:
                        raise RuntimeError(("unknown basis", kind))
                return output

            require(not differential(s_chain),
                    ("complete Hasse chain stopped being closed", v, matching))

            top_basis = ("r0", ())
            require(s_chain[top_basis] == unit, "top r0 coefficient is not J_M")
            tail_chain = dict(s_chain)
            del tail_chain[top_basis]
            expected_tail_boundary: Module = {
                ("Eq", ()): scale(-1, b),
            }
            require(differential(tail_chain) == expected_tail_boundary,
                    ("formal C_rel tail boundary changed", v, matching))

            top_chain: Module = {
                top_basis: unit,
                ("T", ()): Counter({(): Q(-1)}),
            }
            expected_top_boundary: Module = {
                ("Eq", ()): b,
                ("w", ()): variable(Y),
            }
            require(differential(top_chain) == expected_top_boundary,
                    "top anchor/cap boundary changed")

            total_chain = dict(s_chain)
            total_chain[("T", ())] = Counter({(): Q(-1)})
            require(differential(total_chain)
                    == {("w", ()): variable(Y)},
                    "coupled Hasse/cap chain changed")
            require(not differential(differential(total_chain)),
                    "d^2 failed in the coupled total complex")
            formal_tail_checks += 1

            omega_rows.append(omega)
            ridge_rows.extend(difference for difference in facet_differences
                              if difference)
            records.append({
                "v": v,
                "matching": [list(edge) for edge in matching],
                "physical_top": "J_M=1",
                "chart_top": "1",
                "nonzero_ridge_differences": 2,
                "omega_terms": len(omega),
                "formal_Crel_signature": [-1, 0, 0, 0],
            })

    require(len(records) == formal_tail_checks == 15,
            "wrong selected cube count")

    labels = sorted(ridge_labels)
    ridge_matrix = [[row.get((label,), ZERO) for label in labels]
                    for row in ridge_rows]
    omega_matrix = [[row.get((label,), ZERO) for label in labels]
                    for row in omega_rows]
    require(rank(ridge_matrix) == 6,
            "complete endpoint ridge mismatch rank changed")
    require(rank(omega_matrix) == 5,
            "per-face primitive bridge obstruction rank changed")

    # Source descent is impossible for the ordinary fourth derivative: the
    # zero source equation H_m is sent to the unit J_M.  The same unit creates
    # the formal target and obstructs factorization through the source ideal.
    selected = records[0]
    require(selected["physical_top"] == "J_M=1",
            "descent unit disappeared")
    require(b.get((U_TARGET,), ZERO) == -1,
            "pure conormal stopped being primitive")

    return {
        "selected_cubes": len(records),
        "records": records,
        "identity": "J_M=d_M(d_pq H_m)=d_{pq,xv,N}H_m=1",
        "formal_total_complex": {
            "tail_signature": [-1, 0, 0, 0],
            "top_signature": [1, 1, 0, 0],
            "total_signature": [0, 1, 0, 0],
            "d_tail": "-(H0-u)Eq",
            "d_total": "Yw",
            "d_squared": 0,
        },
        "source_labelled_bridge": {
            "nonzero_ridges_per_cube": 2,
            "ridge_mismatch_rank": rank(ridge_matrix),
            "primitive_omega_rank": rank(omega_matrix),
            "omega_terms_per_cube": 4,
            "missing_faces": ["pq:22->00", "xv:0m_v->00"],
        },
        "descent_obstruction": {
            "fourth_operator_on_source_equation": 1,
            "pure_conormal_u_coefficient": -1,
            "interpretation": (
                "the same unit creates the formal C_rel tail and prevents "
                "the fourth operator from factoring through the source ideal"
            ),
        },
    }


def grade_audit():
    midpoint_words = set()
    for left, right in combinations(range(3), 2):
        for marked in combinations(range(6), 3):
            marked = set(marked)
            midpoint_words.add(tuple(right if site in marked else left
                                     for site in range(6)))
    require(len(midpoint_words) == 60, "all-colour midpoint census changed")

    physical_residual = PHYSICAL_WORD[:6]
    require(physical_residual not in midpoint_words,
            "physical cube word became a selected midpoint")
    chart_residuals = {v: chart_word(v)[:6] for v in D}
    require(all(word not in midpoint_words
                for word in chart_residuals.values()),
            "a zero-endpoint chart word became a selected midpoint")
    pure_reset = (0,) * 6
    require(pure_reset not in midpoint_words,
            "pure reset word became a selected midpoint")

    counts = {
        str(v): [chart_residuals[v].count(colour) for colour in range(3)]
        for v in D
    }
    require([physical_residual.count(colour) for colour in range(3)]
            == [1, 3, 2], "physical residual count changed")
    require(set(map(tuple, counts.values())) == {(2, 2, 2), (2, 3, 1)},
            ("chart residual count types changed", counts))

    # Selector localization changes endpoint characters only.  It leaves
    # these literal residual-word basis labels untouched.
    return {
        "all_binary_midpoint_words": len(midpoint_words),
        "physical_residual_word": "".join(map(str, physical_residual)),
        "physical_counts": [1, 3, 2],
        "chart_residual_counts": counts,
        "pure_reset_word": "000000",
        "midpoint_hits": 0,
        "selector_effect": "endpoint character only; residual word fixed",
        "required_extra_face": "source-labelled residual-word change into 3+3 midpoint",
    }


def audit() -> dict[str, object]:
    pin_dependencies()
    ledger = {
        "third_cofactor_total_complex": cube_and_third_cofactor_audit(),
        "endpoint_midpoint_grade": grade_audit(),
        "verdict": (
            "formal C_rel exists in the prolonged Hasse total complex, but "
            "no source-valid physical C_rel is constructed: the top unit "
            "has a primitive endpoint-ridge chain-map defect, sends H_m to "
            "1, and does not lie in the selected midpoint word summand"
        ),
    }
    digest = sha256(json.dumps(ledger, sort_keys=True,
                               separators=(",", ":")).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    ledger["ledger_sha256"] = digest
    return ledger


def main() -> None:
    ledger = audit()
    total = ledger["third_cofactor_total_complex"]
    print("h=3 third-cofactor/Bianchi total complex: FORMAL YES / PHYSICAL NO")
    print("J_M identification:", total["identity"])
    print("formal C_rel signature:",
          total["formal_total_complex"]["tail_signature"])
    print("d^2:", total["formal_total_complex"]["d_squared"])
    print("endpoint ridge ranks:",
          total["source_labelled_bridge"]["ridge_mismatch_rank"],
          total["source_labelled_bridge"]["primitive_omega_rank"])
    print("midpoint hits:", ledger["endpoint_midpoint_grade"]["midpoint_hits"])
    print("ledger_sha256:", ledger["ledger_sha256"])


if __name__ == "__main__":
    main()
