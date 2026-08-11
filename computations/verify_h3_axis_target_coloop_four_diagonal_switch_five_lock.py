#!/usr/bin/env python3
"""Compute the literal five-row lock on the four diagonal return packets.

The minimax common-q audit leaves four return records.  Each of their four
private top words has one selected q matching and exactly two diagonal
alternate matchings.  A top-preserving switch is alternate minus selected.

For a q matching Q and residual word w, its five lock coordinates are the
top coefficient and the four ordered response faces obtained by deleting
one q edge and inserting the actually selected endpoint-star cells.  This
checker computes those columns with full word labels.  The resulting map
has rank two and six literal zero switch columns per record, so the five
rows do not close the final diagonal switching packet.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_axis_target_coloop_return_common_q_top_companion.py":
        "6ad4388d645c7bd25fc5359b22798dff953579b2e0923c7317425bb7973e5664",
    "notes/h3-axis-target-coloop-return-common-q-top-companion.md":
        "136e24f8f57cfc14b0b23385bf951e132d3c4f29910ebbf8bdeb91a6ec772847",
    "computations/verify_h3_axis_target_coloop_double_companion_transfer.py":
        "94eaf974b2224221d59d05d99ef8cadb03908ee8f3734c28549650c9c026193c",
    "notes/h3-axis-target-coloop-double-companion-transfer.md":
        "914456b7ebe0f58d148b16fbaeb3666bd3fc85e33b2746892523c66ee7b69761",
}
EXPECTED_LEDGER_SHA256 = (
    "1b2bc65653177b77e81b59604a9b292b1e831d93627f78ea409f6dea4928abf1"
)

P, S = 6, 7
PURE_ZERO = (0,) * 8
PURE_ONE = (1,) * 8
PURE_TWO = (2,) * 8
RESPONSES = ((1, 1), (1, 2), (2, 1), (2, 2))
FEATURES = ("top", "R11", "R12", "R21", "R22")


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(relative, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(spec is not None and spec.loader is not None,
            f"cannot load dependency: {relative}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def endpoint_support(matching, word):
    """Return head -> {(residual site, residual colour)} for P and S."""

    p_support = set()
    s_support = set()
    for left, right in matching:
        if P in (left, right):
            site = right if left == P else left
            p_support.add((word[P], site, word[site]))
        if S in (left, right):
            site = right if left == S else left
            s_support.add((word[S], site, word[site]))
    return p_support, s_support


def selected_endpoint_support(second, residual, candidate, first_word):
    p_support = set()
    s_support = set()
    for matching, word in (
        (residual["L"], PURE_ONE),
        (residual["M"], PURE_TWO),
        (residual["B"], first_word),
        (residual["N"], first_word),
        (candidate, second.SECOND_HYBRID),
    ):
        p_cells, s_cells = endpoint_support(matching, word)
        p_support.update(p_cells)
        s_support.update(s_cells)
    return p_support, s_support


def lock_column(matching, word, p_support, s_support):
    column = [1]
    for p_head, s_head in RESPONSES:
        coefficient = 0
        for left, right in matching:
            coefficient += int(
                (p_head, left, word[left]) in p_support
                and (s_head, right, word[right]) in s_support
            )
            coefficient += int(
                (p_head, right, word[right]) in p_support
                and (s_head, left, word[left]) in s_support
            )
        column.append(coefficient)
    return tuple(column)


def matrix_rank(columns):
    if not columns:
        return 0
    matrix = [list(map(Fraction, row)) for row in zip(*columns)]
    rows = len(matrix)
    cols = len(matrix[0])
    rank = 0
    for col in range(cols):
        pivot = next((row for row in range(rank, rows)
                      if matrix[row][col]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        scale = matrix[rank][col]
        matrix[rank] = [entry / scale for entry in matrix[rank]]
        for row in range(rows):
            if row == rank or not matrix[row][col]:
                continue
            scale = matrix[row][col]
            matrix[row] = [entry - scale * pivot_entry
                           for entry, pivot_entry
                           in zip(matrix[row], matrix[rank])]
        rank += 1
        if rank == rows:
            break
    return rank


def audit():
    top = load(
        "computations/verify_h3_axis_target_coloop_return_common_q_top_companion.py",
        "return_top_companion_dependency",
    )
    second = load(
        "computations/verify_h3_axis_target_coloop_second_endpoint_hybrid.py",
        "second_endpoint_hybrid_dependency",
    )
    first = load(
        "computations/verify_h3_axis_target_coloop_endpoint_hybrid_cancellation.py",
        "first_endpoint_hybrid_dependency",
    )
    routing = load(
        "computations/verify_h3_axis_target_coloop_other_bright_matching_routing.py",
        "target_coloop_routing_dependency",
    )
    _, returns = top.reconstruct_returns(second, first, routing)
    q_matchings = tuple(routing.perfect_matchings(range(6)))

    boundary_records = []
    column_histogram = Counter()
    switch_histogram = Counter()
    ranks = Counter()
    kernels = Counter()
    boundary_words = Counter()
    diagonal_completion_choices = 0
    rainbow_witness_words = Counter()
    rainbow_mate_routes = Counter()
    one_shared_affine_rows = Counter()
    representative = None

    for residual, candidate in returns:
        first_word, _, cells = top.selected_q_support(
            second, residual, candidate
        )
        rows = top.supported_top_rows(q_matchings, cells)
        private = [
            (word, monomials[0]) for word, monomials in rows.items()
            if word != (0,) * 6 and len(monomials) == 1
        ]
        diagonal_data = []
        offdiagonal_forcing = False
        for word, monomial in private:
            selected = frozenset(edge for edge, _ in monomial)
            diagonal_alternates = tuple(
                matching for matching in q_matchings
                if frozenset(matching) != selected
                and all(word[left] == word[right]
                        for left, right in matching)
            )
            if not diagonal_alternates:
                offdiagonal_forcing = True
            diagonal_data.append(
                (word, tuple(sorted(selected)), diagonal_alternates)
            )
        if offdiagonal_forcing:
            continue

        require(len(private) == 4,
                "the sharp boundary stopped having four private words")
        require(all(len(alternates) == 2
                    for _, _, alternates in diagonal_data),
                "the sharp boundary stopped having two diagonal mates")
        boundary_records.append((residual, candidate))
        p_support, s_support = selected_endpoint_support(
            second, residual, candidate, first_word
        )

        switch_columns = []
        record_rows = []
        for word, selected, alternates in diagonal_data:
            boundary_words["".join(map(str, word))] += 1
            selected_column = lock_column(
                selected, word, p_support, s_support
            )
            alternate_columns = tuple(
                lock_column(matching, word, p_support, s_support)
                for matching in alternates
            )
            column_histogram[("selected", selected_column)] += 1
            for column in alternate_columns:
                column_histogram[("alternate", column)] += 1
                switch = tuple(alt - base for alt, base
                               in zip(column, selected_column))
                require(switch[0] == 0,
                        "a top-preserving switch acquired top boundary")
                switch_histogram[switch] += 1
                switch_columns.append(switch)
            record_rows.append({
                "word": "".join(map(str, word)),
                "selected_matching": selected,
                "selected_column": selected_column,
                "alternate_matchings": alternates,
                "alternate_columns": alternate_columns,
            })

        rank = matrix_rank(switch_columns)
        ranks[rank] += 1
        kernels[len(switch_columns) - rank] += 1
        require(rank == 2 and len(switch_columns) - rank == 6,
                "the boundary five-lock rank/kernel changed")
        require(sum(1 for column in switch_columns
                    if column == (0, 0, 0, 0, 0)) == 6,
                "the six literal zero switch columns changed")
        require(all(column[3:] == (0, 0) for column in switch_columns),
                "a diagonal switch acquired an R21/R22 face")

        # The six-column incidence kernel does not lift multiplicatively.
        # The zero top row for each private selected monomial forces at
        # least one of its two diagonal alternate monomials to be nonzero.
        # Choose one such active alternate in each of the four rows.  All
        # 2^4 choices create a nonzero rainbow (00,11,22) perfect matching.
        # Its word has two sites of each colour, so there is exactly one
        # all-diagonal perfect matching in that word.  The already selected
        # off-diagonal q cell also fails to make a second supported term.
        for choice in product(range(2), repeat=4):
            active_cells = set(cells)
            for selected_choice, (word, _, alternates) in zip(
                    choice, diagonal_data):
                matching = alternates[selected_choice]
                active_cells.update(
                    (edge, (word[edge[0]], word[edge[1]]))
                    for edge in matching
                )
            # Test against the source-complete diagonal envelope: every
            # 00/11/22 cell on every physical residual edge is allowed,
            # whether active or not.  Only the named chosen cells are
            # assumed nonzero.  Hence a private monomial must both be unique
            # in the full envelope and use only active factors.
            completion_cells = set(cells)
            residual_edges = {
                edge for matching in q_matchings for edge in matching
            }
            completion_cells.update(
                (edge, (colour, colour))
                for edge in residual_edges for colour in range(3)
            )
            completion_rows = top.supported_top_rows(
                q_matchings, completion_cells
            )
            rainbow = []
            for word, monomials in completion_rows.items():
                if tuple(word.count(colour) for colour in range(3)) != (
                        2, 2, 2):
                    continue
                if len(monomials) != 1:
                    continue
                monomial = monomials[0]
                if not monomial <= active_cells:
                    continue
                if Counter(label[0] for _, label in monomial) != Counter({
                        0: 1, 1: 1, 2: 1}):
                    continue
                require(all(left == right for _, (left, right) in monomial),
                        "a rainbow witness acquired an off-diagonal factor")
                diagonal_matchings = tuple(
                    matching for matching in q_matchings
                    if all(word[left] == word[right]
                           for left, right in matching)
                )
                require(len(diagonal_matchings) == 1,
                        "a (2,2,2) word lost its unique diagonal matching")
                require(frozenset(diagonal_matchings[0])
                        == frozenset(edge for edge, _ in monomial),
                        "the private rainbow term changed matching")
                rainbow.append(word)
            require(rainbow,
                    f"a diagonal completion choice escaped: {choice}")
            witness = min(rainbow)
            rainbow_witness_words["".join(map(str, witness))] += 1
            witness_monomial = completion_rows[witness][0]
            selected_matching = frozenset(
                edge for edge, _ in witness_monomial
            )
            anchor_matchings = tuple(
                set(edge for edge in residual[key]
                    if P not in edge and S not in edge)
                for key in ("K", "L", "M")
            )
            anchor_union = set().union(*anchor_matchings)
            for matching in q_matchings:
                if frozenset(matching) == selected_matching:
                    continue
                offdiagonal = tuple(
                    edge for edge in matching
                    if witness[edge[0]] != witness[edge[1]]
                )
                require(offdiagonal,
                        "a rainbow alternate stopped being off-diagonal")
                if any(edge not in anchor_union for edge in offdiagonal):
                    route = "external_offdiagonal"
                else:
                    multiplicities = tuple(
                        sum(edge in anchor for anchor in anchor_matchings)
                        for edge in offdiagonal
                    )
                    if max(multiplicities) >= 2:
                        route = "two_shared_anchor_migration"
                    else:
                        route = "one_shared_L_pair_affine_return"
                        l_tail = {
                            edge for edge in residual["L"]
                            if P not in edge and S not in edge
                        }
                        require(set(offdiagonal) == l_tail
                                and len(offdiagonal) == 2,
                                "the one-shared residual left L's q tail")
                        require(set(matching) == l_tail | {
                            routing.edge(2, 3)
                        }, "the one-shared residual changed its closing edge")
                        require(all(sum(edge in anchor
                                        for anchor in anchor_matchings) == 1
                                    for edge in offdiagonal),
                                "an L-pair residual acquired a shared edge")
                        one_shared_affine_rows[
                            ("".join(map(str, witness)),
                             tuple(sorted(matching)))
                        ] += 1
                    rainbow_mate_routes[route] += 1
                    continue
                rainbow_mate_routes[route] += 1
            diagonal_completion_choices += 1
        if representative is None:
            representative = {
                "source_kind": residual["source_kind"],
                "rho3": residual["rho3"],
                "M": residual["M"], "K": residual["K"],
                "L": residual["L"], "B": residual["B"],
                "C": candidate,
                "p_endpoint_support": tuple(sorted(p_support)),
                "s_endpoint_support": tuple(sorted(s_support)),
                "rows": record_rows,
            }

    require(len(boundary_records) == 4,
            f"the diagonal boundary record count changed: {len(boundary_records)}")
    require(Counter((residual["source_kind"], residual["rho3"])
                    for residual, _ in boundary_records) == Counter({
        ("q_only", 1): 2,
        ("same_skeleton", 1): 2,
    }), "the diagonal boundary source split changed")
    require(ranks == Counter({2: 4}) and kernels == Counter({6: 4}),
            "the four-record lock profile changed")
    require(switch_histogram == Counter({
        (0, 0, 0, 0, 0): 24,
        (0, 0, 1, 0, 0): 4,
        (0, 1, 1, 0, 0): 4,
    }), f"the switch-column histogram changed: {switch_histogram}")
    require(diagonal_completion_choices == 64,
            "the four-record 2^4 completion count changed")
    require(rainbow_mate_routes == Counter({
        "external_offdiagonal": 840,
        "two_shared_anchor_migration": 40,
        "one_shared_L_pair_affine_return": 16,
    }), f"the rainbow-mate route split changed: {rainbow_mate_routes}")
    require(sum(one_shared_affine_rows.values()) == 16
            and all(key[0] == "001122" for key in one_shared_affine_rows),
            f"the one-shared affine row changed: {one_shared_affine_rows}")

    ledger = {
        "feature_order": FEATURES,
        "boundary_records": len(boundary_records),
        "boundary_words": dict(sorted(boundary_words.items())),
        "switch_column_histogram": {
            str(key): value for key, value in sorted(switch_histogram.items())
        },
        "rank_per_record": 2,
        "kernel_dimension_per_record": 6,
        "literal_zero_switches_per_record": 6,
        "opposite_crossed_faces_R21_R22": 0,
        "multiplicative_diagonal_completion": {
            "choices_per_record": 16,
            "total_choices": diagonal_completion_choices,
            "feasible_choices": 0,
            "private_rainbow_word_histogram": dict(
                sorted(rainbow_witness_words.items())
            ),
            "alternate_mate_routes": dict(
                sorted(rainbow_mate_routes.items())
            ),
            "one_shared_affine_rows": {
                str(key): value
                for key, value in sorted(one_shared_affine_rows.items())
            },
        },
        "representative": representative,
        "conclusion": (
            "The unary plus four response deletion lock is not injective "
            "on the four diagonal packets.  Six of eight top-preserving "
            "switch directions per record are literal five-row kernel "
            "columns.  The remaining two see only R11/R12, so no opposite "
            "crossed wedge or target constant is forced at incidence level. "
            "However none of the 16 diagonal realizations per record lifts: "
            "each creates a private rainbow (00,11,22) top monomial.  Thus "
            "every physical completion must introduce a further "
            "off-diagonal q cell.  External mates and two-shared anchor "
            "mates enter pinned routes; the sole residual is the literal "
            "001122 matching PS|L_qtail|23 with two one-shared L edges."
        ),
    }
    digest = sha256(
        json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return ledger, digest


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def main():
    pin_dependencies()
    ledger, digest = audit()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"the frozen diagonal-lock ledger changed: {digest}")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")
    print("h3 target-coloop four diagonal switch five-lock: PASS")


if __name__ == "__main__":
    main()
