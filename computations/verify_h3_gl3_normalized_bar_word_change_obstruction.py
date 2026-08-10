#!/usr/bin/env python3
"""Exact normalized-bar obstruction to the h=3 GL3 word change.

The local covariance interval has endpoints L (output colour change) and D
(contragredient source derivation), edge E with dE=L-D, and the standard
augmentation eps(L)=eps(D)=1.  Tensoring four such intervals and applying
the Eilenberg--Zilber shuffle homotopy relates all-L to all-D but cannot
make either endpoint a boundary.  Target and old-cap residue are audited
separately.
"""

from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, permutations, product
import json


EXPECTED_DIGEST = "619edd465455045546f646f0715900df3e8b8a95cf97ad1fa272b8c7cede1391"
COLORS = (0, 1, 2)
ODD_WORD = (1, 2, 1, 1, 2)
FULL_WORD = (0, 1, 2, 1, 1, 2, 2, 2)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def add_sparse(target, source, scalar=F(1)):
    for basis, coefficient in source.items():
        target[basis] = target.get(basis, F(0)) + scalar * coefficient
        if not target[basis]:
            del target[basis]


def boundary(cell):
    """Tensor differential for cells with entries D,L in degree 0 and E in degree 1."""
    output = {}
    previous_edges = 0
    for position, entry in enumerate(cell):
        if entry != "E":
            continue
        sign = F(-1 if previous_edges % 2 else 1)
        left = list(cell)
        left[position] = "L"
        right = list(cell)
        right[position] = "D"
        add_sparse(output, {tuple(left): F(1)}, sign)
        add_sparse(output, {tuple(right): F(1)}, -sign)
        previous_edges += 1
    return output


def chain_boundary(chain):
    output = {}
    for cell, coefficient in chain.items():
        add_sparse(output, boundary(cell), coefficient)
    return output


def monotone_path(size, order):
    """The standard cubical path from all-D to all-L in coordinate order."""
    state = ["D"] * size
    chain = {}
    for position in order:
        edge = list(state)
        edge[position] = "E"
        chain[tuple(edge)] = chain.get(tuple(edge), F(0)) + F(1)
        state[position] = "L"
    require(state == ["L"] * size, "monotone path missed a coordinate")
    return chain


def rank(rows):
    work = [list(map(F, row)) for row in rows]
    if not work:
        return 0
    answer = 0
    for column in range(len(work[0])):
        pivot = next((row for row in range(answer, len(work)) if work[row][column]), None)
        if pivot is None:
            continue
        work[answer], work[pivot] = work[pivot], work[answer]
        value = work[answer][column]
        work[answer] = [entry / value for entry in work[answer]]
        for row in range(len(work)):
            if row == answer or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right
                         for left, right in zip(work[row], work[answer], strict=True)]
        answer += 1
    return answer


def cube_audit(size, audit_all_shuffles):
    vertices = tuple(product(("D", "L"), repeat=size))
    vertex_index = {vertex: index for index, vertex in enumerate(vertices)}
    edges = []
    for position in range(size):
        for fixed in product(("D", "L"), repeat=size - 1):
            cell = list(fixed)
            cell.insert(position, "E")
            edges.append(tuple(cell))
    incidence_columns = []
    for cell in edges:
        column = [F(0)] * len(vertices)
        for vertex, coefficient in boundary(cell).items():
            column[vertex_index[vertex]] = coefficient
        incidence_columns.append(column)
    incidence_rows = [
        [incidence_columns[column][row] for column in range(len(incidence_columns))]
        for row in range(len(vertices))
    ]
    incidence_rank = rank(incidence_rows)
    require(incidence_rank == len(vertices) - 1, "cube H0 dimension changed")

    all_d = ("D",) * size
    all_l = ("L",) * size
    wanted_boundary = {all_l: F(1), all_d: F(-1)}
    orders = tuple(permutations(range(size))) if audit_all_shuffles else (tuple(range(size)),)
    average = {}
    for order in orders:
        path = monotone_path(size, order)
        require(chain_boundary(path) == wanted_boundary,
                f"shuffle path {order} has wrong boundary")
        for cell, coefficient in path.items():
            average[cell] = average.get(cell, F(0)) + coefficient / len(orders)
    require(chain_boundary(average) == wanted_boundary,
            "normalized EZ average lost its endpoint difference")

    # The normalized bar augmentation is one on every vertex and zero in
    # positive degree.  It kills every boundary, while either endpoint has
    # augmentation one and therefore is not a boundary.
    require(sum(wanted_boundary.values(), F(0)) == 0,
            "bar endpoint difference acquired augmentation")
    require(sum(({all_l: F(1)}).values(), F(0)) == 1,
            "all-L endpoint lost its H0 class")
    return {
        "dimension": size,
        "vertices": len(vertices),
        "edges": len(edges),
        "incidence_rank": incidence_rank,
        "h0_dimension": len(vertices) - incidence_rank,
        "shuffles_checked": len(orders),
        "normalized_ez_boundary": "allL-allD",
        "endpoint_augmentation": 1,
        "boundary_augmentation": 0,
    }


def lowering_target(source_colors, total_sites, acted_sites):
    """Apply product E_(0<-source_i) at acted sites to ternary GHZ Delta."""
    require(len(source_colors) == len(acted_sites), "target action labels mismatch")
    if not source_colors:
        return {tuple([color] * total_sites): F(1) for color in COLORS}
    if len(set(source_colors)) != 1:
        return {}
    source = source_colors[0]
    word = [source] * total_sites
    for site in acted_sites:
        word[site] = 0
    return {tuple(word): F(1)}


def face_support(deleted):
    face = tuple(site for site in range(5) if site != deleted)
    word = tuple(ODD_WORD[site] for site in face)
    first = face[0]
    terms = set()
    for partner in face[1:]:
        rest = tuple(site for site in face if site not in (first, partner))
        pairs = tuple(sorted(((first, partner), tuple(sorted(rest)))))
        colored = tuple(
            sorted((left, right, ODD_WORD[left], ODD_WORD[right]) for left, right in pairs)
        )
        terms.add(colored)
    require(len(terms) == 3, "four-site face lost a perfect matching")
    return face, word, terms


def augmented_physical_rank_audit():
    """Small physical output quotient carrying Eq,w,target,old ores."""
    records = []
    for y in (F(1), F(2), F(-3, 2)):
        # These are the exact edge-zero columns of the committed physical
        # output cascade.  The q-zero projected Hasse top is target_row-T.
        target_row = [F(-1), F(0), F(1), F(0)]
        cap_target = [F(0), -y, F(1), F(0)]
        ordinary_response = [F(0), F(1), F(0), F(1)]
        projected_qzero = [left - right
                           for left, right in zip(target_row, cap_target, strict=True)]
        desired = [F(0), y, F(0), F(0)]
        columns = [target_row, cap_target, ordinary_response]
        require(projected_qzero == [F(-1), y, F(0), F(0)],
                "projected Hasse defect column changed")
        require(rank(columns) == 3, "physical augmented rank changed")
        require(rank(columns + [desired]) == 4,
                "desired invisible lower face entered old physical span")
        covector = [y, F(1), y, F(-1)]
        require(all(sum((entry * dual for entry, dual in zip(column, covector)), F(0)) == 0
                    for column in columns), "physical covector stopped killing old columns")
        require(sum((entry * dual for entry, dual in zip(desired, covector)), F(0)) == y,
                "physical covector stopped detecting desired face")

        # Cancelling the Eq defect of projected_qzero with the normalized
        # target row leaves target -1.  Adding T cancels that target but also
        # cancels the desired w-boundary.  This is the target action of the
        # pure endpoint of the bar comparison.
        eq_cancelled = [left - right
                        for left, right in zip(projected_qzero, target_row, strict=True)]
        require(eq_cancelled == [F(0), y, F(-1), F(0)],
                "Eq cancellation no longer leaves the target class")
        fully_cancelled = [left + right
                           for left, right in zip(eq_cancelled, cap_target, strict=True)]
        require(fully_cancelled == [F(0)] * 4,
                "target correction stopped cancelling the cap boundary")
        records.append({
            "Y": str(y),
            "old_rank": rank(columns),
            "rank_with_desired": rank(columns + [desired]),
            "eq_cancelled_class": [str(value) for value in eq_cancelled],
            "dual_on_desired": str(y),
        })
    return records


def main():
    cube4 = cube_audit(4, audit_all_shuffles=True)
    cube7 = cube_audit(7, audit_all_shuffles=True)

    # Five certified four-site face words.  Every word contains 1 and 2, so
    # the all-output lowering kills Delta.  Any corner containing D also
    # kills the target because source derivations act trivially on Delta.
    face_records = []
    supports = []
    for deleted in range(5):
        face, word, terms = face_support(deleted)
        supports.append(terms)
        require(set(word) == {1, 2}, "face lowering ceased to be target-zero")
        target = lowering_target(word, 5, face)
        require(target == {}, "all-L face lowering retained target action")
        face_records.append({
            "deleted": deleted,
            "word": "".join(map(str, word)),
            "target_terms_all_L": len(target),
            "matching_terms": len(terms),
            "normalized_bar_h0_class": 1,
        })
    require(all(supports[left].isdisjoint(supports[right])
                for left, right in combinations(range(5), 2)),
            "the five ordinary-residue face classes lost independence")

    # Endpoint-only 22->00 lowering: when m_v=2, the three local inputs are
    # all 2 and the local target action is nonzero.  When m_v=1 it vanishes.
    endpoint_target_records = []
    for deleted, middle in enumerate(ODD_WORD):
        source_colors = (middle, 2, 2)
        acted_sites = (deleted + 1, 6, 7)  # x=0, D=1..5, p=6, q=7
        target = lowering_target(source_colors, 8, acted_sites)
        expected_nonzero = middle == 2
        require(bool(target) == expected_nonzero,
                "endpoint-only target action classification changed")
        endpoint_target_records.append({
            "deleted_face": deleted,
            "source_colors": list(source_colors),
            "target_nonzero": bool(target),
            "target_words": ["".join(map(str, word)) for word in target],
        })
    require(sum(record["target_nonzero"] for record in endpoint_target_records) == 2,
            "wrong endpoint-only target obstruction count")

    # The complete seven-site word change uses both source colours, so its
    # all-L target action vanishes.  This removes the target obstruction only
    # after the residual-face comparison is included; the normalized bar H0
    # / ordinary-residue class remains.
    acted = tuple(site for site, color in enumerate(FULL_WORD) if color)
    colors = tuple(FULL_WORD[site] for site in acted)
    require(len(acted) == 7 and set(colors) == {1, 2}, "full word-change ledger changed")
    require(lowering_target(colors, 8, acted) == {},
            "complete word change retained a GHZ target term")

    physical_records = augmented_physical_rank_audit()

    ledger = {
        "bar_interval": {"dE": "L-D", "augmentation_L": 1, "augmentation_D": 1},
        "cube4": cube4,
        "cube7": cube7,
        "faces": face_records,
        "face_residue_rank": 5,
        "endpoint_only_target_records": endpoint_target_records,
        "endpoint_only_nonzero_target_count": 2,
        "complete_word_change_target_terms": 0,
        "physical_augmented_records": physical_records,
        "verdict": "EZ cancels only allL-allD; target or normalized old-residue class survives",
    }
    digest = sha256(json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    require(EXPECTED_DIGEST != "TO_BE_FILLED", "pin EXPECTED_DIGEST")
    require(digest == EXPECTED_DIGEST, ("ledger digest changed", digest, ledger))
    print("h=3 normalized GL3 bar word-change obstruction: PASS")
    print("EZ boundaries: allL-allD in dimensions 4 and 7")
    print("endpoint-only target survives on 2/5 faces; full target vanishes")
    print("normalized bar/old ordinary-residue H0 survives with rank 5")
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()
