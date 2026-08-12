#!/usr/bin/env python3
"""Reciprocal-response obstruction to the shared rootless attachment.

The reciprocal Hasse--Bianchi identity is the first plausible source
operation with the same coarse (p,s,q) degree as the E14 endpoint face.
For d=lambda*E_ab and a diagonal row cc it reads

    D_cc E_ab-D_ab E_cc=lambda*X_c.

After cancelling the symmetric quadratic K channel and the pure target, its
response part is lambda*(R_cc-X_c), the already existing diagonal response
row.  In one canonical tail R_cc contains the two endpoint orientations with
equal coefficient, not their difference.

There is a second, independent parity gate.  Ordinary residue in the
committed response/old-cap landing is invariant under endpoint transposition.
It therefore kills every endpoint-odd curvature.  But the desired four-term
attachment A, combined with the rootless bar B, asks for an endpoint-odd row
D=A+B carrying one unit of ordinary residue.  A reciprocal curvature can
supply either the symmetric residue-carrying row or an odd residue-zero row,
never D.  A new reduced-residue correction in the same source grade is still
required.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LEDGER_SHA256 = "4a7b2e6287d2e00827bd21782de430580776c00003efb6494c3e8a341f7089e7"
PINS = {
    "computations/verify_reciprocal_response_hasse_bianchi.py":
        "d5bb78f9a0ca2cfab30932ccfcaeca8c6de9d3bff5351983045e66fee4d1d432",
    "notes/reciprocal-response-hasse-bianchi-frontier.md":
        "16a0bbc94ceb27e6d65dae721d25f39f1c309e94b4677d3052205a84b09ef431",
    "computations/verify_h3_shared_same_word_endpoint_companion_attachment_gate.py":
        "ef6f336c3582c66ca65250a3d812deaed5aa3a6d998ce1e428e0bc03fa2fab37",
    "computations/verify_h3_rootless_one_face_third_cofactor_comparison_vertex_gate.py":
        "37251145d805861b2d1b15b7bf37cf9f98ba30b03fbcffa1daa4fc35789efe84",
    "computations/verify_h3_physical_curvature_qzero_attaching_lower_face_obstruction.py":
        "050bfaa16cedb07248f01f58f8cc59927307861e55da45b759219ccde3d24ee1",
    "computations/verify_h3_derived_terminal_indeterminacy_or_relative_generator.py":
        "9327b57598a5264c11e5c3085e1afceaec8fd72c408f5fc1f1eaa2490a13a8b1",
}

SITES = tuple(range(6))
COLOURS = (0, 1, 2)
CANONICAL_TAIL = ((2, 4), (3, 5))
FEATURES = ("E_plus", "E_minus", "Omega", "q_comp", "target", "ores")


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for second in vertices[1:]:
        remainder = tuple(site for site in vertices
                          if site not in (first, second))
        edge = tuple(sorted((first, second)))
        for tail in perfect_matchings(remainder):
            answer.append(tuple(sorted((edge,) + tail)))
    return tuple(answer)


def qcell(edge: tuple[int, int], colour: int = 1) -> str:
    left, right = edge
    return f"q{left}{right}_{colour}{colour}"


def response(first_colour: int, second_colour: int) -> Counter:
    """Literal R_ij=p_i*s_j*q^[2] on six residual sites."""
    answer = Counter()
    for p_site in SITES:
        for s_site in SITES:
            if p_site == s_site:
                continue
            remainder = tuple(site for site in SITES
                              if site not in (p_site, s_site))
            for matching in perfect_matchings(remainder):
                monomial = tuple(sorted((
                    f"p{first_colour}@{p_site}",
                    f"s{second_colour}@{s_site}",
                    *(qcell(edge) for edge in matching),
                )))
                answer[monomial] += 1
    return answer


def quadratic_response(first: tuple[int, int],
                       second: tuple[int, int]) -> Counter:
    """Literal K_(ij;kl)=p_i*s_j*p_k*s_l*q^[1]."""
    i, j = first
    k, ell = second
    answer = Counter()
    for p_site, s_site, p2_site, s2_site in permutations(SITES, 4):
        remainder = tuple(site for site in SITES if site not in (
            p_site, s_site, p2_site, s2_site
        ))
        require(len(remainder) == 2, "quadratic response complement changed")
        monomial = tuple(sorted((
            f"p{i}@{p_site}", f"s{j}@{s_site}",
            f"p{k}@{p2_site}", f"s{ell}@{s2_site}",
            qcell(tuple(sorted(remainder))),
        )))
        answer[monomial] += 1
    return answer


def endpoint_projection(polynomial: Counter, colour: int = 1):
    tail = tuple(sorted(qcell(edge) for edge in CANONICAL_TAIL))
    plus = tuple(sorted((f"p{colour}@0", f"s{colour}@1", *tail)))
    minus = tuple(sorted((f"p{colour}@1", f"s{colour}@0", *tail)))
    return polynomial[plus], polynomial[minus], plus, minus


def reciprocal_bianchi_audit() -> dict[str, object]:
    rows = tuple((i, j) for i in COLOURS for j in COLOURS)
    symmetry_checks = 0
    for first in rows:
        for second in rows:
            require(quadratic_response(first, second)
                    == quadratic_response(second, first),
                    ("K symmetry changed", first, second))
            symmetry_checks += 1
    require(symmetry_checks == 81, "K symmetry census changed")

    records = []
    for a in COLOURS:
        for b in COLOURS:
            if a == b:
                continue
            for c in COLOURS:
                # With d_ab=lambda and every other direct coefficient zero,
                # D_cc E_ab=lambda*R_cc+K_(ab;cc), while
                # D_ab E_cc=K_(cc;ab).  K symmetry leaves lambda*R_cc.
                rcc = response(c, c)
                plus, minus, plus_term, minus_term = endpoint_projection(
                    rcc, c
                )
                require((plus, minus) == (1, 1),
                        ("diagonal response stopped being signless", a, b, c))
                records.append({
                    "direct_row": [a, b],
                    "diagonal_row": [c, c],
                    "lambda_sign": "+1 (reverse orientation gives -1,-1)",
                    "K_terms_cancel": True,
                    "remaining_response": f"R_{c}{c}",
                    "canonical_tail": [list(edge) for edge in CANONICAL_TAIL],
                    "endpoint_terms": [list(plus_term), list(minus_term)],
                    "endpoint_coefficients": [plus, minus],
                    "orientation_pairing": plus - minus,
                    "pure_target_curvature": f"X_{c}",
                    "target_corrected_row": f"R_{c}{c}-X_{c}=E_{c}{c}",
                })
    require(len(records) == 18, "offdiagonal/diagonal Bianchi census changed")
    return {
        "quadratic_K_symmetry_checks": symmetry_checks,
        "records": records,
        "coarse_operation_degrees": {
            "Q": [0, 0, 3],
            "R": [1, 1, 2],
            "K": [2, 2, 1],
            "order": ["p", "s", "q"],
        },
        "grade_match": (
            "R has the required E14 endpoint degree (p,s,q^2); this is a "
            "genuine candidate grade, not the source of the obstruction"
        ),
        "exact_target_corrected_content": (
            "the reciprocal Bianchi row is the existing diagonal response "
            "E_cc, so its correct-tail endpoint projection is E_plus+E_minus"
        ),
    }


def vector(**entries: int) -> tuple[Q, ...]:
    require(set(entries).issubset(FEATURES), ("unknown feature", entries))
    return tuple(Q(entries.get(feature, 0)) for feature in FEATURES)


def add(*vectors: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(sum((vector[index] for vector in vectors), Q(0))
                 for index in range(len(FEATURES)))


def scale(value, vector: tuple[Q, ...]) -> tuple[Q, ...]:
    value = Q(value)
    return tuple(value * entry for entry in vector)


def dot(left: tuple[Q, ...], right: tuple[Q, ...]) -> Q:
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


def parity_and_residue_gate() -> dict[str, object]:
    # Four geometric coordinates agree with 744cd9a.  Append target/ores.
    rootless_bar = vector(Omega=-1, q_comp=1, ores=1)
    attachment = vector(E_plus=1, E_minus=-1, Omega=1, q_comp=-1)
    required_endpoint_row = add(attachment, rootless_bar)
    require(required_endpoint_row
            == vector(E_plus=1, E_minus=-1, ores=1),
            ("A+B signature changed", required_endpoint_row))

    signless = vector(E_plus=1, E_minus=1)
    endpoint_odd = vector(E_plus=1, E_minus=-1)
    orientation = vector(E_plus=1, E_minus=-1)
    invariant_augmentation = vector(E_plus=1, E_minus=1)
    require(dot(orientation, signless) == 0
            and dot(orientation, endpoint_odd) == 2,
            "orientation parity changed")
    require(dot(invariant_augmentation, endpoint_odd) == 0,
            "endpoint-odd row acquired invariant augmentation")

    # In the pinned committed matching-face landing q-augmentation=ores.
    # Thus an odd response row has ores zero.  Subtracting the rootless bar
    # gives the correct four geometric coordinates but leaves ores=-1.
    odd_minus_bar = add(endpoint_odd, scale(-1, rootless_bar))
    require(odd_minus_bar[:4] == attachment[:4]
            and odd_minus_bar[FEATURES.index("ores")] == -1,
            ("odd response minus bar residual changed", odd_minus_bar))
    reduced_residue = vector(ores=1)
    repaired = add(odd_minus_bar, reduced_residue)
    require(repaired == attachment,
            "one reduced residue correction stopped repairing the attachment")

    # Conversely a normalized symmetric response can carry a unit residue,
    # but cannot enter the endpoint-orientation line.
    normalized_signless = scale(Q(1, 2), signless)
    require(dot(invariant_augmentation, normalized_signless) == 1
            and dot(orientation, normalized_signless) == 0,
            "normalized signless response readouts changed")

    return {
        "feature_order": list(FEATURES),
        "rootless_bar_B": [str(value) for value in rootless_bar],
        "desired_attachment_A": [str(value) for value in attachment],
        "required_endpoint_row_D=A+B": [
            str(value) for value in required_endpoint_row
        ],
        "exact_reciprocal_endpoint_projection": [1, 1],
        "orientation_covector": [1, -1],
        "orientation_on_exact_reciprocal_and_D": [0, 2],
        "committed_response_ores_law": (
            "ordinary residue factors through the endpoint-invariant "
            "augmentation E_plus+E_minus"
        ),
        "endpoint_odd_candidate": [1, -1],
        "ordinary_residue_of_every_endpoint_odd_response": 0,
        "odd_candidate_minus_bar": [str(value) for value in odd_minus_bar],
        "first_missing_correction": [str(value) for value in reduced_residue],
        "after_reduced_residue_correction": [
            str(value) for value in repaired
        ],
        "parity_statement": (
            "over characteristic zero, a transposition-invariant residue "
            "functional kills the transposition-odd endpoint line"
        ),
    }


def source_and_fredholm_scope() -> dict[str, object]:
    return {
        "exact_reciprocal_identity_is_source_tangent_lift": False,
        "reason": (
            "E=0 at a source point does not make D E vanish; the pinned "
            "identity proves at least one reciprocal residual direction is "
            "non-tangent.  Corrected Kodaira-Spencer lifts remain new data"
        ),
        "smallest_positive_refinement": {
            "operation": (
                "an endpoint-oriented Kodaira-Spencer lift whose odd response "
                "face is accompanied by an endpoint-even hidden correction"
            ),
            "hidden_correction": "ores=+1 in the same repeated source grade",
            "combined_boundary": (
                "E_plus-E_minus+Omega-q_comp with W=tgt=ores=ainc=0"
            ),
        },
        "failure_to_Fredholm": {
            "bounded_orientation_or_residue_covector_is_global": False,
            "why_not_yet": (
                "the reciprocal packet does not define the physical five-polar "
                "map or its terminal landing, so its parity covector is not "
                "automatically a Component-III Macaulay annihilator"
            ),
            "conditional_full_source_dichotomy": (
                "for the complete augmented correction map J in this fixed "
                "grade, failure of the missing correction by nonzero terminal "
                "indeterminacy gives the normalized relative generator; if "
                "the terminal functional kills ker J it is well-defined, and "
                "failure of solvability yields a left separator.  Only after "
                "the physical terminal comparison is typed is that separator "
                "the Fredholm annihilator"
            ),
        },
    }


def main() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")
    ledger = {
        "theorem": "reciprocal response/rootless attachment parity gate",
        "reciprocal_Hasse_Bianchi": reciprocal_bianchi_audit(),
        "endpoint_parity_and_old_residue": parity_and_residue_gate(),
        "source_and_Fredholm_scope": source_and_fredholm_scope(),
        "verdict": (
            "the reciprocal response Hasse-Bianchi identity has the right "
            "coarse R degree but target-corrects to the existing signless "
            "diagonal response.  Antisymmetrizing to E_plus-E_minus kills "
            "the transposition-invariant old ordinary residue, while A+B "
            "requires that odd row to carry residue one.  Hence reciprocal "
            "curvature alone does not construct A; one oriented KS lift plus "
            "an independent same-grade reduced-residue correction is needed"
        ),
        "scope": (
            "exact six-site response expansion, all 81 K symmetries, all 18 "
            "offdiagonal/diagonal reciprocal packets, and the committed old-"
            "cap qaug=ores law.  This is not an all-Spencer-resolution no-go"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest))
    print("h3 reciprocal response/rootless attachment: PARITY GATE")
    print("reciprocal R endpoint coefficients: (1,1), not (1,-1)")
    print("K symmetry checks: 81; pure-target correction returns E_cc")
    print("endpoint-odd response old ordinary residue: 0")
    print("A+B requires endpoint-odd ordinary residue: 1")
    print("next datum: oriented KS lift + same-grade reduced residue")
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()
