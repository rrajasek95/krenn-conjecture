#!/usr/bin/env python3
"""Exact local algebra audit for the one-hot K8 PEPS/Holant encoding."""

from __future__ import annotations

import argparse
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_onehot_peps_holant.json"
D = 7
Q = 4
PHYS = 3


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def exact_rank(matrix):
    work = [[Fraction(value) for value in row] for row in matrix]
    row = 0
    width = len(work[0]) if work else 0
    for column in range(width):
        pivot = next((i for i in range(row, len(work)) if work[i][column]), None)
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        value = work[row][column]
        for i in range(row + 1, len(work)):
            if not work[i][column]:
                continue
            scale = work[i][column] / value
            for j in range(column, width):
                work[i][j] -= scale * work[row][j]
        row += 1
        if row == len(work):
            break
    return row


def inverse3(matrix):
    work = [[Fraction(value) for value in row] +
            [Fraction(int(i == j)) for j in range(3)]
            for i, row in enumerate(matrix)]
    for column in range(3):
        pivot = next((i for i in range(column, 3) if work[i][column]), None)
        require(pivot is not None, "singular 3 by 3 matrix")
        work[column], work[pivot] = work[pivot], work[column]
        value = work[column][column]
        work[column] = [entry / value for entry in work[column]]
        for i in range(3):
            if i == column or not work[i][column]:
                continue
            scale = work[i][column]
            work[i] = [left - scale * right
                       for left, right in zip(work[i], work[column])]
    return [row[3:] for row in work]


def mat_vec(matrix, vector):
    return [sum(Fraction(a) * Fraction(b) for a, b in zip(row, vector))
            for row in matrix]


def mat_scale(scalar, matrix):
    return [[Fraction(scalar) * Fraction(entry) for entry in row]
            for row in matrix]


def onehot_p(vectors):
    """P on arbitrary vectors, each in C e0 + C^3."""
    vac = [vector[0] for vector in vectors]
    answer = [Fraction(0)] * 3
    for site in range(D):
        scalar = Fraction(1)
        for other in range(D):
            if other != site:
                scalar *= vac[other]
        for color in range(3):
            answer[color] += scalar * vectors[site][color + 1]
    return answer


def p_on_basis(indices):
    nonvacuum = [(site, value) for site, value in enumerate(indices) if value]
    if len(nonvacuum) != 1:
        return [0, 0, 0]
    return [int(nonvacuum[0][1] == color + 1) for color in range(3)]


def candidate_group_audit():
    a = tuple(Fraction(value) for value in (1, 2, 3, 4, 5, 6, 7))
    C = [[Fraction(1), Fraction(1), Fraction(0)],
         [Fraction(0), Fraction(1), Fraction(1)],
         [Fraction(0), Fraction(0), Fraction(1)]]
    w = [[Fraction(site + color + 1) for color in range(3)]
         for site in range(6)]
    w.append([-sum(w[site][color] for site in range(6))
              for color in range(3)])
    require(all(sum(w[site][color] for site in range(7)) == 0
                for color in range(3)), "unipotent sum changed")
    matrices = []
    for site in range(7):
        matrix = [[a[site], 0, 0, 0]]
        for color in range(3):
            matrix.append([a[site] * w[site][color]] +
                          [a[site] * C[color][j] for j in range(3)])
        matrices.append(matrix)
    A = Fraction(1)
    for value in a:
        A *= value
    h = mat_scale(Fraction(1, 1) / A, inverse3(C))

    for indices in product(range(4), repeat=7):
        transformed = []
        for site, index in enumerate(indices):
            transformed.append([matrices[site][row][index] for row in range(4)])
        lhs = mat_vec(h, onehot_p(transformed))
        rhs = list(map(Fraction, p_on_basis(indices)))
        require(lhs == rhs, ("group stabilizer formula failed", indices, lhs, rhs))
    return {
        "a": [str(value) for value in a],
        "C": [[str(value) for value in row] for row in C],
        "sum_w": [str(sum(w[site][color] for site in range(7)))
                  for color in range(3)],
        "basis_tuples_checked": 4**7,
    }


def local_lie_rank():
    # Unknown ordering: seven gl4 blocks, then one gl3 physical block.
    variables = [("g", site, row, column)
                 for site in range(7) for row in range(4) for column in range(4)]
    variables += [("h", row, column) for row in range(3) for column in range(3)]
    index = {variable: position for position, variable in enumerate(variables)}
    equations = []
    basis_inputs = []
    for excitation_count in (0, 1, 2):
        for sites in combinations(range(7), excitation_count):
            for colors in product(range(1, 4), repeat=excitation_count):
                values = [0] * 7
                for site, color in zip(sites, colors):
                    values[site] = color
                basis_inputs.append(tuple(values))

    for inputs in basis_inputs:
        base = p_on_basis(inputs)
        for output in range(3):
            row = [0] * len(variables)
            # Physical infinitesimal h P.
            for source_output in range(3):
                row[index[("h", output, source_output)]] += base[source_output]
            # Virtual infinitesimals, one leg at a time.
            for site in range(7):
                source_basis = inputs[site]
                for target_basis in range(4):
                    modified = list(inputs)
                    modified[site] = target_basis
                    value = p_on_basis(tuple(modified))[output]
                    row[index[("g", site, target_basis, source_basis)]] += value
            if any(row):
                equations.append(row)
    rank = exact_rank(equations)
    require(len(variables) == 121 and rank == 87,
            ("local Lie stabilizer rank changed", len(variables), rank))
    return {
        "ambient_dimension": len(variables),
        "constraint_rank": rank,
        "stabilizer_dimension": len(variables) - rank,
        "inputs_used": len(basis_inputs),
        "scope": "excitation degrees 0,1,2; degrees >=3 vanish automatically",
    }


def ghz_lie_rank():
    # Stabilizer Lie algebra inside gl3^8 for Delta=sum_c e_c^tensor8.
    variables = [(site, row, column)
                 for site in range(8) for row in range(3) for column in range(3)]
    index = {variable: position for position, variable in enumerate(variables)}
    rows = {}
    for site, row, column in variables:
        word = [column] * 8
        word[site] = row
        word = tuple(word)
        rows.setdefault(word, [0] * len(variables))[index[(site, row, column)]] += 1
    matrix = list(rows.values())
    rank = exact_rank(matrix)
    require((len(variables), rank, len(variables) - rank) == (72, 51, 21),
            "GHZ local stabilizer Lie dimension changed")
    return {
        "ambient_dimension": 72,
        "constraint_rank": rank,
        "connected_stabilizer_dimension": 21,
        "full_group": "site diagonal torus with three product-one equations, semidirect common S3",
    }


def bond_slice_audit():
    # A=0 and a=C=identity.  Opposite w on two half-edges stabilizes P but
    # creates forbidden one-sided bond excitations.
    v = (Fraction(1), Fraction(0), Fraction(0))
    w = [v, tuple(-entry for entry in v)] + [(Fraction(0),) * 3] * 5
    require([sum(entry[color] for entry in w) for color in range(3)] ==
            [0, 0, 0], "explicit unipotent is not in the stabilizer")
    first_bond = {
        "00": "1",
        "10": "1",
    }


def fixed_k8_invisible_chord():
    """Two literal restricted sources with the same nonzero K8 tensor."""
    base = frozenset(((0, 1), (2, 3), (4, 5), (6, 7)))
    enlarged = base | {(0, 2)}

    def matchings(vertices):
        vertices = tuple(vertices)
        if not vertices:
            yield ()
            return
        first = vertices[0]
        for position, partner in enumerate(vertices[1:], 1):
            rest = vertices[1:position] + vertices[position + 1:]
            for tail in matchings(rest):
                yield ((first, partner),) + tail

    all_matchings = tuple(frozenset(matching) for matching in matchings(range(8)))
    require(len(all_matchings) == 105, "K8 perfect matching count changed")
    base_live = [matching for matching in all_matchings if matching <= base]
    enlarged_live = [matching for matching in all_matchings if matching <= enlarged]
    require(base_live == enlarged_live == [base],
            "invisible chord became top-visible")
    return {
        "base_edges": [list(edge) for edge in sorted(base)],
        "added_edge": [0, 2],
        "supported_perfect_matchings_before": len(base_live),
        "supported_perfect_matchings_after": len(enlarged_live),
        "common_output": "e_0^tensor8",
        "not_restricted_gauge_equivalent": (
            "the 02 bond block is zero before and nonzero after; invertible "
            "endpoint actions preserve whether an entire bond block is zero"
        ),
    }
    second_bond = {
        "00": "1",
        "10": "-1",
    }
    return {
        "unipotent": [list(map(str, vector)) for vector in w],
        "first_zero_bond_after_action": first_bond,
        "second_zero_bond_after_action": second_bond,
        "local_onehot_output_on_all_other_vacua": "e_0-e_0=0",
        "restricted_bond_slice_preserved": False,
    }


def logical_sha(payload):
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return sha256(raw).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()

    group_control = candidate_group_audit()
    lie = local_lie_rank()
    ghz = ghz_lie_rank()
    bond = bond_slice_audit()
    invisible = fixed_k8_invisible_chord()
    payload = {
        "status": "PASS exact one-hot PEPS/Holant negative audit",
        "onehot_map": {
            "formula": "P(x_1,...,x_7)=sum_k product_(l!=k)phi(x_l) pi(x_k)",
            "domain_dimension": 4**7,
            "rank": 3,
            "kernel_dimension": 4**7 - 3,
        },
        "local_stabilizer": {
            "formula": (
                "g_k=a_k[[1,0],[w_k,C]], a_k!=0, common C in GL3, "
                "sum_k w_k=0; h=((product_k a_k)C)^-1"
            ),
            "group": "Ga^18 semidirect ((Gm)^7 x GL3)",
            "dimension": 34,
            "leg_permutations": "external S7 normalizer, not contained in GL4^7 x GL3",
            "exact_basis_control": group_control,
            "lie_algebra_control": lie,
        },
        "bond_action": {
            "formula": (
                "b_A -> a_i a_j[00+w_i0+0w_j+w_iw_j+"
                "(C_i tensor C_j)A]"
            ),
            "restricted_slice_condition": "w_ij=w_ji=0 on every bond",
            "normalized_action": "A_ij -> (C_i tensor C_j) A_ij",
            "half_edge_scalars": "act trivially on normalized A and cancel against physical scalars",
            "explicit_noninjective_control": bond,
        },
        "target_preserving_restriction": {
            "GHZ_stabilizer": ghz,
            "induced_action": (
                "known site-colour torus T0 of dimension 21, semidirect the "
                "common colour permutation S3; no new continuous Krenn gauge"
            ),
        },
        "peps_applicability": {
            "Acuaviva_et_al": "arXiv:2209.14358",
            "theorem_hypothesis": (
                "uniform local tensor and equality of the induced states on "
                "every allowed contraction graph; conclusion is intersection "
                "of reductive gauge-orbit closures/minimal canonical forms"
            ),
            "mismatch": [
                "Krenn has one fixed K8 contraction, not equality on every geometry.",
                "The 28 bond tensors are edge-dependent; absorbing them destroys uniformity.",
                "P has rank 3 and kernel dimension 16381, so injective/normal PEPS theorems do not apply.",
                "The general minimal form uses orbit closure, which retains border/ghost identifications rather than finite membership.",
                "Its full local gauge orbit leaves the vacuum+VV Krenn bond slice through the 18-dimensional unipotent radical.",
            ],
            "verdict": "fundamental theorem cannot be invoked from equality on this single K8",
        },
        "holant_applicability": {
            "primary_lead": "Backens-Goldberg arXiv:1811.00817",
            "theory_scope": (
                "Holant clones classify expressibility under arbitrary tensor "
                "products, contractions/gadgets, permutations, and in the "
                "conservative classification arbitrary unary functions"
            ),
            "mismatch": [
                "The cited classification is Boolean; the virtual domain here has size four and an open three-state physical leg.",
                "Clone membership permits auxiliary/internal vertices and repeated signatures, absent from the fixed K8 source.",
                "Equality of one K8 open tensor is not Holant indistinguishability on every signature grid.",
                "Holographic transformations preserve the enlarged gadget category, not the literal one-hot bond slice.",
            ],
            "verdict": "clone closure forgets the single-use, no-internal-site incidence restriction",
        },
        "restricted_onehot_clone": {
            "smallest_source_faithful_invariant": (
                "For N=diag(0,1,1,1), every literal bond b obeys "
                "(N tensor I-I tensor N)b=0. Its kernel is exactly "
                "C|00> plus V tensor V. Together with P's excitation-one "
                "condition, live configurations are perfect matchings."
            ),
            "gauge_scope": (
                "The invariant is preserved by the block-diagonal reductive "
                "part and violated by every nonzero stabilizer unipotent w; "
                "therefore it is deliberately not a full PEPS/Holant-gauge invariant."
            ),
            "fixed_geometry_noninjectivity": invisible,
            "closure_verdict": (
                "If arbitrary gadgets/internal P-sites are forbidden, the "
                "remaining typed 'clone' has no composition beyond disjoint "
                "tensoring, relabelling, and edge specialization; its K8 "
                "evaluation is the original hafnian moment map. If arbitrary "
                "contractions are restored, it is an ordinary matching-gadget "
                "clone and no longer represents one fixed K8 source."
            ),
        },
        "terminal_verdict": (
            "No canonical block decomposition follows. Exact local symmetry "
            "shows why: the useful-looking unipotent gauge creates forbidden "
            "half-edge monomers; after intersecting with literal Krenn bonds "
            "only T0 semidirect S3 remains. PEPS/Holant theorems require all "
            "geometries or gadget closure and therefore do not turn one K8 "
            "output equality into gauge equivalence or a clean cap."
        ),
    }
    payload["logical_sha256"] = logical_sha(payload)
    if args.write_results:
        OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("one-hot PEPS/Holant local audit: PASS")
    print("Stab(P): dimension 34 = 18 unipotent + 7 torus + 9 GL3")
    print("Lie constraints: 121 - 87 = 34")
    print("restricted target-preserving bond gauge: T0(dim 21) semidirect S3")
    print("logical sha256:", payload["logical_sha256"])


if __name__ == "__main__":
    main()
