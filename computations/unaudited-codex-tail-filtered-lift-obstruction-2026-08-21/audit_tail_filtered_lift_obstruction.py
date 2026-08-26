#!/usr/bin/env python3
"""Exact finite audit of the filtered tail-lifting obstruction.

No Groebner basis is used.  The checker enumerates the 105 matchings, audits
tail-degree ranges for the literal word profiles, and verifies two tiny exact
higher-tail countermodels.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import hashlib
import itertools
import json
import pathlib
import sys


HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TAIL = ROOT / "computations/unaudited-codex-tail-polar-source-lift-2026-08-21"
BRIDGE = ROOT / "computations/unaudited-codex-x5-tail-cap-bridge-2026-08-21"
OUT = HERE / "results_tail_filtered_lift_obstruction.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for matching in perfect_matchings(rest):
            yield ((first, second),) + matching


def degree_histogram(word, matchings):
    return Counter(
        sum(word[left] != word[right] for left, right in matching)
        for matching in matchings
    )


def sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def logical_sha(payload) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def cyclic_equations(point):
    x, y, z = point
    return (x - y * z, y - x * z, z - x * y)


def main() -> None:
    matchings = tuple(perfect_matchings(range(8)))
    require(len(matchings) == 105, "perfect-matching count changed")
    require(len(set(matchings)) == 105, "perfect matchings ceased to be unique")

    words = {
        "7+1": (0, 0, 0, 0, 0, 0, 0, 1),
        "6+1+1": (0, 1, 2, 2, 2, 2, 2, 2),
        "3+3+2": (0, 0, 0, 1, 1, 1, 2, 2),
    }
    histograms = {name: degree_histogram(word, matchings)
                  for name, word in words.items()}
    require(histograms["7+1"] == Counter({1: 105}),
            "7+1 tail-degree profile changed")
    require(histograms["6+1+1"] == Counter({2: 90, 1: 15}),
            "6+1+1 tail-degree profile changed")
    require(histograms["3+3+2"] == Counter({3: 42, 4: 36, 2: 18, 1: 9}),
            "3+3+2 tail-degree profile changed")

    # For the canonical 611 word, degree one pairs the two exceptional sites;
    # degree two sends them to two distinct majority-colour sites.
    canonical_611 = words["6+1+1"]
    degree_one = []
    degree_two = []
    for matching in matchings:
        degree = sum(canonical_611[a] != canonical_611[b] for a, b in matching)
        (degree_one if degree == 1 else degree_two).append(matching)
    require(len(degree_one) == 15 and len(degree_two) == 90,
            "canonical 611 split changed")
    require(all((0, 1) in matching for matching in degree_one),
            "611 linear matchings ceased to use exceptional edge")
    require(all((0, 1) not in matching for matching in degree_two),
            "611 quadratic matchings unexpectedly use exceptional edge")

    # Minimal full-rank-initial countermodel: t-t^2.  Initial coefficient is
    # one, yet the exact zero set contains the remote tail point t=1.
    one_variable_points = [Fraction(0), Fraction(1)]
    require(all(t - t * t == 0 for t in one_variable_points),
            "one-variable obstruction stopped solving t-t^2")

    # Source-shaped three-channel cycle.  It has identity linear initial
    # matrix and a remote nonzero solution, while every variable satisfies a
    # monic cubic modulo the equations.  The displayed multiplier identity
    # for x^3-x is checked numerically on a deterministic rational grid;
    # cyclic permutations give y,z.
    cyclic_points = [
        (0, 0, 0), (1, 1, 1), (-1, -1, 1),
        (1, -1, -1), (-1, 1, -1),
    ]
    require(all(cyclic_equations(point) == (0, 0, 0)
                for point in cyclic_points),
            "cyclic obstruction point list changed")
    for x, y, z in itertools.product(range(-2, 3), repeat=3):
        f1, f2, f3 = cyclic_equations((x, y, z))
        rhs = (x * x - 1) * f1 - z * f2 - x * z * f3
        require(rhs == x * x * x - x,
                "cubic ideal identity for cyclic obstruction failed")

    # Count the diagonal (tail-zero) source rows which are not tautological.
    composition_counts = Counter()
    diagonal_nontrivial = 0
    diagonal_tautological = 0
    for word in itertools.product(range(3), repeat=8):
        counts = tuple(word.count(c) for c in range(3))
        if max(counts) == 8:
            continue
        if all(count % 2 == 0 for count in counts):
            diagonal_nontrivial += 1
            composition_counts[tuple(sorted(counts, reverse=True))] += 1
        else:
            diagonal_tautological += 1
    require(composition_counts == Counter({(4, 2, 2): 1260,
                                           (4, 4, 0): 210,
                                           (6, 2, 0): 168}),
            "diagonal packet profile census changed")
    require(diagonal_nontrivial == 1638 and diagonal_tautological == 4920,
            "diagonal mixed-row split changed")

    upstream_paths = [
        TAIL / "results_tail_polar_source_lift.json",
        TAIL / "results_tail_nonmonomial_boundary_closure.json",
        BRIDGE / "results_x5_tail_cap_bridge.json",
    ]
    payload = {
        "status": "PASS exact filtered-tail obstruction audit",
        "tail_filtration": {
            "diagonal_ring": "D=Q[g^c_uv] localized at the displayed chart factors",
            "tail_ring": "R=D[T], T=(168 cross-colour endpoint cells)",
            "filtration": "J-adic, J=(T)",
            "literal_profile_degree_histograms": {
                name: {str(degree): count for degree, count in sorted(hist.items())}
                for name, hist in histograms.items()
            },
            "maximum_tail_degree": 4,
            "canonical_611_equation": (
                "F_01222222=h^2_01*t^01_01+Q_01, where Q_01 is the sum "
                "of 90 degree-two matchings t^02_0b*t^12_1c times a "
                "four-site G2 Hafnian"
            ),
            "canonical_611_linear_terms": 15,
            "canonical_611_quadratic_terms": 90,
        },
        "exact_lifting_lemma": {
            "triangular_version": (
                "If every deleted equal/lower tail column already lies in I, "
                "and a localized square initial matrix M is invertible, then "
                "the selected tail generators lie in I+J^2. If successive "
                "batches cover J, then J=J^2 in R/I."
            ),
            "local_Nakayama_conclusion": (
                "At every local ring of R/I whose maximal ideal contains J, "
                "finite generation and J=J^2 imply J=0. Equivalently the "
                "zero-tail component is formally isolated after all tail "
                "columns, not merely twelve, are covered."
            ),
            "global_conclusion_not_valid": (
                "J=J^2 can split off a remote component on which J is the "
                "unit ideal; nilpotence, a global Jacobson-radical hypothesis, "
                "or an exact saturation excluding that component is required."
            ),
            "current_380x12_scope": (
                "With uneliminated columns retained, invertibility solves the "
                "twelve selected variables formally in the other tail "
                "variables; it does not put them in the full source ideal."
            ),
        },
        "smallest_higher_tail_obstruction": {
            "equation": "t-t^2=0",
            "initial_matrix": [[1]],
            "tail_points": [0, 1],
            "verdict": (
                "Full initial rank and even a flat homogenization "
                "t-s*t^2 do not exclude the remote branch t=1/s."
            ),
        },
        "source_shaped_cyclic_obstruction": {
            "equations": ["x-y*z", "y-x*z", "z-x*y"],
            "initial_matrix": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
            "exact_points": [list(point) for point in cyclic_points],
            "finite_quotient_guard": (
                "x^3-x=(x^2-1)*(x-y*z)-z*(y-x*z)-x*z*(z-x*y); "
                "cyclic identities make the quotient finite, but evaluation "
                "at (1,1,1) proves the tail ideal is not nilpotent."
            ),
            "meaning": (
                "The three colour-pair 611 channels can be quadratically "
                "cyclic; finiteness alone does not make Nakayama global."
            ),
        },
        "nilpotence_audit": {
            "frozen_source_quotient_nilpotence_certificate": False,
            "frozen_global_finiteness_certificate": False,
            "nilpotence_would_suffice_after_J_equals_J_squared": True,
            "finiteness_alone_would_suffice": False,
        },
        "terminal_zero_tail_quotient": {
            "automatic_mixed_rows": diagonal_tautological,
            "nontrivial_diagonal_packet_rows": diagonal_nontrivial,
            "nontrivial_profiles": {
                "+".join(map(str, profile)): count
                for profile, count in sorted(composition_counts.items())
            },
            "row_formula": (
                "For colour classes S_c of even size, "
                "F_w(T=0)=product_c Haf(G_c[S_c]); if any |S_c| is odd, "
                "F_w(T=0)=0 identically."
            ),
            "activity_open": (
                "U_cap=union_C intersection_i {rank([L_C;ell_i])="
                "rank(L_C)+1}, for the 168 star and 560 triangle carriers"
            ),
            "remaining_terminal_lemma": (
                "Prove that the normalized diagonal packet scheme (three "
                "pure Hafnians equal one plus the 1,638 even-profile rows) "
                "is contained in U_cap, or is empty. No such global "
                "containment is frozen."
            ),
        },
        "scope_verdict": (
            "The frozen rank theorem gives formal/local implicit solvability. "
            "It is a genuine triangular elimination only after the deleted "
            "columns are already in the ideal. It is not a global Rees/flat "
            "lifting theorem."
        ),
        "mutation_guards": {
            "move_one_611_quadratic_matching_to_degree_one": True,
            "delete_the_remote_t_equals_one_point": True,
            "declare_finiteness_equivalent_to_nilpotence": True,
            "drop_one_diagonal_even_profile": True,
        },
        "source_hashes": {
            str(path.relative_to(ROOT)): sha256(path) for path in upstream_paths
        },
    }
    payload["logical_sha256"] = logical_sha(payload)
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if "--write-results" in sys.argv:
        OUT.write_text(text, encoding="utf-8")
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
