#!/usr/bin/env python3
"""Chart-parity reduction of the h=3 full-nine Schur repair.

The literal no-go
`verify_h3_literal_full_nine_schur_polar_no_go.py` proves that the five
marked polar cochains have source-relative connecting matrix I_5, so none
of them lifts as Lambda*T = M*A.  Its stated escape is a
denominator-marked two-edge comparison cell whose tail contributes -I_5.

This checker decides exactly how much of that escape is reachable.  The two
MARKED sector copies ("pq"/direct and "pr"/two-star) carry the same labelled
monomials -- the sectors themselves do not, being 15 and 90 monomials wide --
so the marked leading space has a basis-permuting involution iota swapping
the two copies.  Everything follows from parity:

  * Lambda_v is iota-odd:  Lambda_v . iota = -Lambda_v.
  * Hence Lambda_v annihilates every iota-even vector, over Q.
  * A denominator/face column is MODELLED as chart-neutral, i.e. entering
    the two sector copies diagonally, hence iota-even.  405 such columns
    (five deletion faces, all 81 colourings each) are constructed that way
    and confirmed annihilated; their iota-evenness is true by construction,
    not verified -- the modelling hypothesis is the load-bearing input.
  * For any iota-odd w, Lambda_v(w) = (1/3) * (pq-direct mass of w on
    h_v).  So the repair condition on a family of tails {R_w} is the FULL
    25-entry condition [mass_v(R_w)] = -3 * I_5: each tail must carry
    pq-direct mass -3 on its OWN face and 0 on the other four.  Mass -3 on
    every h_v would give the all-(-1) rank-one matrix, not -I_5.
    THIS mass criterion is the reduction.
  * Within the displayed literal face family the iota-odd part is exactly
    span{S_v}, where S_v = (h_v)_{pq,direct} - (h_v)_{pr,two-star}, and
    there the only solution is -1 on each square.  But -I_5 is NOT confined
    to that span: an explicit witness putting the whole mass -3 on a single
    monomial of each h_v also realizes -I_5 and is independent of the
    squares.  The repair is therefore a five-equation mass condition, not a
    sign.

Consequence: on the modelling hypothesis that denominator and face columns
enter the two chart copies diagonally, they contribute nothing to the
connecting class; any repair must supply genuinely chart-odd mass.

This is a finite h=3, direct-free statement.  The diagonal placement of
denominator/face columns is a modelling hypothesis inherited from the no-go
checker, not something verified here.  It does not construct the attaching
chain and does not prove Krenn's conjecture.
"""

from fractions import Fraction
from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
QQ = Fraction
EXPECTED_LEDGER_SHA256 = (
    "55ea1477db5178cda2954cba16b639abb1cc88f569a4f509a15679495a1a8189"
)

PQ_SECTOR = ("pq", "direct")
PR_SECTOR = ("pr", "two_star")


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BASE = load(
    "h3_chart_parity_base",
    "verify_h3_direct_free_literal_four_face_full_nine_no_go.py",
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def add_value(vector, key, value):
    updated = vector.get(key, QQ(0)) + QQ(value)
    if updated:
        vector[key] = updated
    else:
        vector.pop(key, None)


def add_vectors(*vectors):
    answer = {}
    for vector in vectors:
        for key, value in vector.items():
            add_value(answer, key, value)
    return answer


def scale(vector, scalar):
    scalar = QQ(scalar)
    if not scalar:
        return {}
    return {key: value * scalar for key, value in vector.items()}


def pairing(vector, cochain):
    return sum(
        (QQ(value) * cochain.get(key, QQ(0)) for key, value in vector.items()),
        QQ(0),
    )


def tagged(sector, polynomial):
    return {(sector, monomial): QQ(value)
            for monomial, value in polynomial.items() if value}


def iota(vector):
    """Swap the two chart sector copies of every labelled monomial."""
    answer = {}
    for (sector, monomial), value in vector.items():
        if sector == PQ_SECTOR:
            flipped = PR_SECTOR
        elif sector == PR_SECTOR:
            flipped = PQ_SECTOR
        else:
            raise RuntimeError("an unexpected chart sector reached iota")
        add_value(answer, (flipped, monomial), value)
    return answer


def even_part(vector):
    return scale(add_vectors(vector, iota(vector)), QQ(1, 2))


def odd_part(vector):
    return scale(add_vectors(vector, scale(iota(vector), -1)), QQ(1, 2))


def rank(vectors):
    """Exact row rank of dense rational vectors."""
    work = [[QQ(value) for value in vector] for vector in vectors]
    if not work:
        return 0
    width = len(work[0])
    pivot_row = 0
    for column in range(width):
        pivot = next(
            (row for row in range(pivot_row, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [
                entry - value * pivot_entry
                for entry, pivot_entry in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def dense(vectors):
    keys = sorted({key for vector in vectors for key in vector}, key=repr)
    return [tuple(QQ(vector.get(key, 0)) for key in keys) for vector in vectors]


def matrix_vector(columns, coefficients):
    answer = {}
    for column, scalar in zip(columns, coefficients):
        if not scalar:
            continue
        for row, value in column.items():
            add_value(answer, row, QQ(scalar) * value)
    return answer


def face_hafnian_vector(deleted_site, colors):
    return {
        monomial: QQ(1)
        for monomial in BASE.face_hafnian(deleted_site, colors)
    }


def build_literal_source():
    """The ten labelled chart columns, their tails and the lower kernel."""
    labels = []
    lower_columns = []
    tail_columns = []
    polar = {}

    for deleted_site in BASE.ODD:
        word = [0] * 8
        for site in BASE.ODD:
            if site != deleted_site:
                word[site] = BASE.MIXED_ODD[site - 1]
        word = tuple(word)
        require("".join(map(str, word))
                == BASE.EXPECTED_GLOBAL_ROWS[deleted_site],
                "one labelled global polar row changed")

        global_boundary = {
            monomial: QQ(1)
            for monomial in BASE.full_nine_polynomial(word)
        }
        require(len(global_boundary) == 90,
                "a direct-free global row lost its 90 matchings")

        marked_edges = (
            BASE.edge(BASE.X, deleted_site, 0, 0),
            BASE.edge(BASE.P, BASE.Q_SITE, 0, 0),
        )
        marked = BASE.sparse_derivative(tuple(global_boundary), marked_edges)
        require(len(marked) == 3 and set(marked.values()) == {1},
                "one marked polar stopped being a three-term hafnian")

        # The marked polar is literally the m-coloured deletion-face hafnian.
        face_colors = BASE.face_word(deleted_site)
        require(dict(marked) == face_hafnian_vector(deleted_site, face_colors),
                "the marked polar stopped equalling the face hafnian h_v")
        polar[deleted_site] = dict(marked)

        pq_direct, pq_stars = BASE.chart_partition(
            word, (BASE.P, BASE.Q_SITE))
        pr_direct, pr_stars = BASE.chart_partition(word, (BASE.P, BASE.R))
        pq_direct_polar = BASE.sparse_derivative(pq_direct, marked_edges)
        pq_star_polar = BASE.sparse_derivative(pq_stars, marked_edges)
        pr_direct_polar = BASE.sparse_derivative(pr_direct, marked_edges)
        pr_star_polar = BASE.sparse_derivative(pr_stars, marked_edges)
        require(pq_direct_polar == marked and not pq_star_polar,
                "pq marked tail left its direct sector")
        require(not pr_direct_polar and pr_star_polar == marked,
                "pr marked tail left its two-star sector")

        labels.extend(((deleted_site, "pq"), (deleted_site, "pr")))
        lower_columns.extend((global_boundary, dict(global_boundary)))
        tail_columns.extend((
            tagged(PQ_SECTOR, pq_direct_polar),
            tagged(PR_SECTOR, pr_star_polar),
        ))

    require(len(labels) == len(lower_columns) == len(tail_columns) == 10,
            "literal source-column count changed")

    kernel = []
    for index in range(5):
        vector = [QQ(0)] * 10
        vector[2 * index] = QQ(1)
        vector[2 * index + 1] = QQ(-1)
        vector = tuple(vector)
        require(not matrix_vector(lower_columns, vector),
                "a pairwise chart comparison left the lower kernel")
        kernel.append(vector)
    lower_rank = rank(dense(
        [{index: column.get(monomial, QQ(0))
          for index, column in enumerate(lower_columns)}
         for monomial in sorted(
             {key for column in lower_columns for key in column}, key=repr)]
    ))
    require(lower_rank == 5,
            "the literal lower block stopped having rank five")
    require(len(lower_columns) - lower_rank == len(kernel) == 5,
            "literal lower kernel is not exactly the five chart differences")
    return labels, lower_columns, tail_columns, kernel, polar


def build_cochains(polar):
    """Lambda_v: +1/6 on each pq-direct term, -1/6 on each pr copy."""
    cochains = []
    for deleted_site in BASE.ODD:
        cochain = {}
        for monomial in polar[deleted_site]:
            cochain[(PQ_SECTOR, monomial)] = QQ(1, 6)
            cochain[(PR_SECTOR, monomial)] = QQ(-1, 6)
        cochains.append(cochain)
    return cochains


def external_squares(polar):
    """S_v = (h_v)_{pq,direct} - (h_v)_{pr,two-star}."""
    return [
        add_vectors(
            tagged(PQ_SECTOR, polar[deleted_site]),
            scale(tagged(PR_SECTOR, polar[deleted_site]), -1),
        )
        for deleted_site in BASE.ODD
    ]


def diagonal_face_columns():
    """Face columns built diagonally, under the chart-neutrality hypothesis.

    A denominator/face column carries no chart label, and the modelling
    hypothesis inherited from the no-go checker is that it therefore enters
    the two sector copies with the same coefficient.  That hypothesis is
    STIPULATED here, not derived: these columns are constructed diagonally,
    so their iota-evenness is true by construction and is not a test.
    """
    columns = []
    labels = []
    for deleted_site in BASE.ODD:
        for colors in product(BASE.COLORS, repeat=4):
            face = face_hafnian_vector(deleted_site, colors)
            columns.append(add_vectors(
                tagged(PQ_SECTOR, face),
                tagged(PR_SECTOR, face),
            ))
            labels.append((deleted_site, "".join(map(str, colors))))
    require(len(columns) == 5 * 81 == 405,
            "the literal chart-neutral face family changed size")
    return labels, columns


def audit():
    labels, lower_columns, tail_columns, kernel, polar = build_literal_source()
    cochains = build_cochains(polar)
    squares = external_squares(polar)

    # 1. Reproduce the connecting matrix independently of the no-go script.
    identity5 = tuple(
        tuple(QQ(1) if row == column else QQ(0) for column in range(5))
        for row in range(5)
    )
    connecting = []
    for cochain in cochains:
        lambda_t = tuple(pairing(column, cochain) for column in tail_columns)
        connecting.append(tuple(
            sum((lambda_t[index] * kernel_vector[index]
                 for index in range(10)), QQ(0))
            for kernel_vector in kernel
        ))
    require(tuple(connecting) == identity5,
            "the source-relative connecting matrix is no longer I_5")

    # 1b. The structural fact, independent of any cochain choice: the tail
    #     of the kernel vector k_v IS the external marked square S_v, and it
    #     is chart-odd.  Hence the connecting class of ANY leading cochain
    #     depends only on that cochain's chart-odd part, and lives on the
    #     five-dimensional chart-odd space spanned by the squares.
    for index, kernel_vector in enumerate(kernel):
        image = matrix_vector(tail_columns, kernel_vector)
        require(image == {key: value for key, value in squares[index].items()
                          if value},
                "the tail of a kernel vector is not the external square")
        require(iota(image) == scale(image, -1),
                "the tail of a kernel vector is not chart-odd")

    # 2. Lambda_v is iota-odd, exactly, as a cochain.
    for cochain in cochains:
        flipped = iota(cochain)
        require(flipped == scale(cochain, -1),
                "a leading polar cochain stopped being chart-odd")

    # 3. Every chart-neutral face column is iota-even and is annihilated.
    face_labels, face_columns = diagonal_face_columns()
    overlapping = 0
    for column in face_columns:
        require(iota(column) == column,
                "a chart-neutral face column stopped being iota-even")
        for index, cochain in enumerate(cochains):
            require(pairing(column, cochain) == 0,
                    "a chart-neutral face column paired nontrivially")
            if any(key in cochain for key in column):
                overlapping += 1
    require(overlapping >= 5,
            "no chart-neutral column met the cochain support; test is vacuous")

    # 4. Parity annihilation is structural, not incidental: check it on the
    #    even part of every literal vector in play, including the tails.
    for vector in list(tail_columns) + list(squares) + list(face_columns):
        recombined = add_vectors(even_part(vector), odd_part(vector))
        require(recombined == {key: value for key, value in vector.items()
                               if value},
                "the iota parity decomposition failed to reconstruct")
        require(iota(even_part(vector)) == even_part(vector),
                "an even part was not iota-even")
        require(iota(odd_part(vector)) == scale(odd_part(vector), -1),
                "an odd part was not iota-odd")
        for cochain in cochains:
            require(pairing(even_part(vector), cochain) == 0,
                    "an iota-even part paired nontrivially with Lambda")
            require(pairing(odd_part(vector), cochain)
                    == pairing(vector, cochain),
                    "the odd part lost the Lambda pairing")

    # 5. Within the DISPLAYED literal face family (a stipulated list, not
    #    all conceivable tails) the iota-odd part is the span of the five
    #    external squares.  Step 5c shows this does NOT extend.
    displayed_family = list(tail_columns) + list(face_columns) + list(squares)
    odd_projections = [odd_part(vector) for vector in displayed_family]
    odd_rank = rank(dense([vector for vector in odd_projections if vector]))
    square_rank = rank(dense(squares))
    require(square_rank == 5,
            "the five external squares stopped being independent")
    require(odd_rank == 5,
            "the displayed-family chart-odd space is not five-dimensional")
    combined_rank = rank(dense(
        [vector for vector in odd_projections if vector] + list(squares)))
    require(combined_rank == 5,
            "the displayed-family chart-odd space left the span of the squares")

    # 5b. The general criterion.  For ANY chart-odd w, oddness forces
    #     w(PR, M) = -w(PQ, M), so
    #         Lambda_v(w) = (1/3) * sum_{M in h_v} w(PQ, M).
    #     Hence a repair tail contributes -1 at v precisely when its total
    #     pq-direct mass on h_v is -3.  This is a statement about every
    #     chart-odd tail, not only the literal family above.
    probes = []
    for offset, deleted_site in enumerate(BASE.ODD):
        for step in range(3):
            probe = {}
            for index, monomial in enumerate(sorted(polar[deleted_site],
                                                    key=repr)):
                weight = QQ(offset + 2 * step + index + 1, 2 * step + 5)
                if step == 2 and index == 0:
                    weight = -weight
                add_value(probe, (PQ_SECTOR, monomial), weight)
                add_value(probe, (PR_SECTOR, monomial), -weight)
            probes.append(probe)
    probes.append(add_vectors(*squares))
    probes.append(scale(add_vectors(*squares), -1))
    for probe in probes:
        require(iota(probe) == scale(probe, -1),
                "a chart-odd probe lost its parity")
        for index, deleted_site in enumerate(BASE.ODD):
            mass = sum(
                (probe.get((PQ_SECTOR, monomial), QQ(0))
                 for monomial in polar[deleted_site]),
                QQ(0),
            )
            value = pairing(probe, cochains[index])
            require(value == mass / 3,
                    "the chart-odd mass formula failed")
    require(len(probes) == 17, "the chart-odd probe family changed size")

    # 5c. -I_5 is NOT confined to the span of the external squares.  Putting
    #     the whole mass -3 on a single monomial of each h_v realizes -I_5
    #     with a family that meets span{S_v} only in zero.  This is why the
    #     reduction is the mass criterion (5) and NOT "a sign on S_v".
    witness = []
    for deleted_site in BASE.ODD:
        monomial = sorted(polar[deleted_site], key=repr)[0]
        witness.append({
            (PQ_SECTOR, monomial): QQ(-3),
            (PR_SECTOR, monomial): QQ(3),
        })
    for vector in witness:
        require(iota(vector) == scale(vector, -1),
                "an off-span witness stopped being chart-odd")
    witness_pairing = tuple(
        tuple(pairing(vector, cochain) for vector in witness)
        for cochain in cochains
    )
    minus_identity5 = tuple(
        tuple(QQ(-1) if row == column else QQ(0) for column in range(5))
        for row in range(5)
    )
    require(witness_pairing == minus_identity5,
            "the off-span witness stopped realizing -I_5")
    require(rank(dense(witness)) == 5,
            "the off-span witness lost full rank")
    require(rank(dense(witness + list(squares))) == 10,
            "the off-span witness stopped being independent of the squares")

    # 6. The pairing of the squares against the cochains is exactly I_5, so
    #    the required -I_5 forces coefficient -1 on every external square.
    square_pairings = tuple(
        tuple(pairing(square, cochain) for square in squares)
        for cochain in cochains
    )
    require(square_pairings == identity5,
            "the external squares no longer pair to I_5")

    # Verify that coefficient -1 on each square realizes -I_5 within the
    # displayed family.  The solution is hard-coded and checked, not
    # solved for; its uniqueness follows from the I_5 pairing matrix.
    repair_coefficients = []
    for target_row in range(5):
        solution = [QQ(-1) if index == target_row else QQ(0)
                    for index in range(5)]
        realized = tuple(
            pairing(matrix_vector(squares, solution), cochain)
            for cochain in cochains
        )
        expected = tuple(QQ(-1) if index == target_row else QQ(0)
                         for index in range(5))
        require(realized == expected,
                "the -I_5 repair is not realized by minus the squares")
        repair_coefficients.append(solution)

    ledger = {
        "source_columns": [
            {"deleted_site": site, "chart": chart} for site, chart in labels
        ],
        "lower_rank": 5,
        "lower_kernel_dimension": len(kernel),
        "connecting_matrix": [
            [[value.numerator, value.denominator] for value in row]
            for row in connecting
        ],
        "kernel_tail_equals_external_square": True,
        "kernel_tail_is_chart_odd": True,
        "lambda_is_chart_odd": True,
        "chart_neutral_columns_tested": len(face_columns),
        "chart_neutral_columns_overlapping_support": overlapping,
        "chart_neutral_pairings_all_zero": True,
        "chart_odd_mass_probes": len(probes),
        "chart_odd_mass_formula": "Lambda_v(w) = (1/3) * pq-direct mass on h_v",
        "minus_one_criterion": "pq-direct mass on h_v equals -3",
        "displayed_family_chart_odd_rank": odd_rank,
        "external_square_rank": square_rank,
        "displayed_family_odd_equals_square_span": combined_rank == square_rank,
        "external_square_pairing": [
            [[value.numerator, value.denominator] for value in row]
            for row in square_pairings
        ],
        "repair_coefficients_on_squares": [
            [[value.numerator, value.denominator] for value in row]
            for row in repair_coefficients
        ],
        "off_span_minus_identity_witness_rank": rank(dense(witness)),
        "off_span_witness_plus_squares_rank":
            rank(dense(witness + list(squares))),
        "minus_identity_confined_to_square_span": False,
        "conclusion": (
            "chart-neutral material is annihilated by the chart-odd polar "
            "cochains, so on the modelling hypothesis that denominator and "
            "face columns enter the two chart copies diagonally they cannot "
            "contribute to the connecting class; the repair reduces to the "
            "mass criterion, namely a chart-odd tail with pq-direct mass -3 "
            "on every h_v.  Within the displayed literal face family the "
            "only such tail is minus the external square, but -I_5 is NOT "
            "confined to that span: an explicit single-monomial witness "
            "realizes -I_5 and is independent of the squares"
        ),
        "scope": (
            "finite h=3 direct-free statement; assumes denominator and face "
            "columns enter the two chart copies with equal coefficient, a "
            "modelling hypothesis inherited from the no-go checker and not "
            "verified here; the attaching chain and its sign are not "
            "constructed"
        ),
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode("ascii")).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "h3 chart-parity repair-reduction ledger changed")
    return ledger, digest


def main():
    ledger, digest = audit()
    print("h=3 chart-parity Schur repair reduction: PASS (exact)")
    print("connecting matrix reproduced:            I_5")
    print("Lambda chart-odd:                       ",
          ledger["lambda_is_chart_odd"])
    print("chart-neutral columns constructed:       %d"
          % ledger["chart_neutral_columns_tested"])
    print("  of which meeting the cochain support:  %d"
          % ledger["chart_neutral_columns_overlapping_support"])
    print("displayed-family chart-odd rank / squares: %d %d"
          % (ledger["displayed_family_chart_odd_rank"],
             ledger["external_square_rank"]))
    print("displayed odd space = span of squares:  ",
          ledger["displayed_family_odd_equals_square_span"])
    print("-I_5 within that family:                 -1 on each square")
    print("-I_5 confined to the square span:       ",
          ledger["minus_identity_confined_to_square_span"])
    print("sha256:", digest)


if __name__ == "__main__":
    main()
