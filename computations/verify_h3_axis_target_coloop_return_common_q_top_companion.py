#!/usr/bin/env python3
"""Audit the first mandatory common-q top companion on all 852 returns.

The second endpoint hybrid leaves a nonzero return term C with endpoint
ports P2,S3.  Together with the earlier B term, the three pure anchors,
and their literal q tails, this gives a finite selected decorated-q support.
This checker expands every coefficient of q^[3] on that support.

At exact carrier support every return has a private nonzero monomial in a
zero top word, hence the localized coefficient ideal is the unit ideal.
A genuine source must therefore add at least one literal q-matching mate.
The checker also audits the especially short PS:00 hybrid when its third
q edge is already selected.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_axis_target_coloop_second_endpoint_hybrid.py":
        "9a6d826940b76fcb1edf33fb44eba6bfabdeb3797ec08850bd5ac944aafa232f",
    "notes/h3-axis-target-coloop-second-endpoint-hybrid.md":
        "af2dd864b0286bc2fed0aa4c39975d813395910669b3ab0ef308c4e686659745",
    "computations/verify_h3_axis_target_coloop_endpoint_hybrid_cancellation.py":
        "8187cd44d88ffcc17c532483519aca935824315f7cad9b859d051c58ac10cce9",
    "notes/h3-axis-target-coloop-endpoint-hybrid-cancellation.md":
        "76c8100f9200c52209a98ca785a42f62a1cf410e1150903c2c4f864ba40f0f15",
}
EXPECTED_LEDGER_SHA256 = (
    "f32eeb746710c7a393fa14565674ec11dbbac6833f4ccfc4c245c9597561465e"
)

P, S = 6, 7
PURE_ZERO = (0,) * 8
PURE_ONE = (1,) * 8
PURE_TWO = (2,) * 8


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


def q_cells(matching, word):
    return frozenset(
        (edge, (word[edge[0]], word[edge[1]]))
        for edge in matching if P not in edge and S not in edge
    )


def reconstruct_returns(second, first, routing):
    _, bright, residuals, _ = second.reconstruct_first_residuals(
        first, routing
    )
    returns = []
    for residual in residuals:
        anchor_union = set(residual["M"]) | set(residual["K"]) | set(
            residual["L"]
        )
        for candidate in bright:
            if routing.edge(P, 0) in candidate:
                continue
            external = set(candidate) - anchor_union
            if any(P in edge or S in edge for edge in external):
                continue
            if routing.crossed_port(candidate):
                continue
            if any(second.SECOND_HYBRID[left]
                   != second.SECOND_HYBRID[right]
                   for left, right in external):
                continue
            if (routing.partner(candidate, P),
                    routing.partner(candidate, S)) != (2, 3):
                continue
            returns.append((residual, candidate))
    require(len(returns) == 852,
            f"the second-return count changed: {len(returns)}")
    return tuple(bright), tuple(returns)


def selected_q_support(second, residual, candidate):
    first_word = [1] * 8
    first_word[3] = residual["rho3"]
    first_word[S] = 2
    first_word = tuple(first_word)
    sources = {
        "K": q_cells(residual["K"], PURE_ZERO),
        "L": q_cells(residual["L"], PURE_ONE),
        "M": q_cells(residual["M"], PURE_TWO),
        "B": q_cells(residual["B"], first_word),
        "C": q_cells(candidate, second.SECOND_HYBRID),
    }
    return first_word, sources, set().union(*sources.values())


def supported_top_rows(q_matchings, cells):
    rows = defaultdict(list)
    for matching in q_matchings:
        choices = [tuple(label for edge0, label in cells if edge0 == edge)
                   for edge in matching]
        if not all(choices):
            continue
        for labels in product(*choices):
            word = [None] * 6
            monomial = []
            compatible = True
            for edge, label in zip(matching, labels):
                for vertex, colour in zip(edge, label):
                    if word[vertex] is not None and word[vertex] != colour:
                        compatible = False
                    word[vertex] = colour
                monomial.append((edge, label))
            if compatible:
                rows[tuple(word)].append(frozenset(monomial))
    return rows


def geometry_and_hybrid(second, routing, q_matchings, residual, candidate,
                        cells):
    b_tail = tuple(edge for edge in residual["B"]
                   if P not in edge and S not in edge)
    c_tail = tuple(edge for edge in candidate
                   if P not in edge and S not in edge)
    edge_b = next(edge for edge in b_tail if 3 in edge)
    edge_c = next(edge for edge in c_tail if 0 in edge)
    if set(edge_b) & set(edge_c):
        return "overlap", (), Counter()

    complement = tuple(sorted(set(range(6)) - set(edge_b) - set(edge_c)))
    available = tuple(
        colour for colour in range(3)
        if (complement, (colour, colour)) in cells
    )
    if not available:
        return "missing_complement", (), Counter()

    mate_counts = Counter()
    first_word = [1] * 6
    first_word[3] = residual["rho3"]
    anchor_q_union = set(
        edge for key in ("M", "K", "L")
        for edge in residual[key] if P not in edge and S not in edge
    )
    for colour in available:
        word = [None] * 6
        for vertex in edge_c:
            word[vertex] = second.SECOND_HYBRID[vertex]
        for vertex in edge_b:
            require(word[vertex] is None,
                    "the disjoint hybrid edges unexpectedly overlapped")
            word[vertex] = first_word[vertex]
        for vertex in complement:
            require(word[vertex] is None,
                    "the complementary hybrid edge unexpectedly overlapped")
            word[vertex] = colour
        word = tuple(word)
        selected = frozenset((edge_b, edge_c, complement))

        supported = []
        for matching in q_matchings:
            monomial = frozenset(
                (edge, (word[edge[0]], word[edge[1]]))
                for edge in matching
            )
            if monomial <= cells:
                supported.append(monomial)
        require(len(supported) == 1,
                "the PS:00 top hybrid stopped being a private selected row")
        require(frozenset(edge for edge, _ in supported[0]) == selected,
                "the private hybrid monomial changed its matching")

        for matching in q_matchings:
            if frozenset(matching) == selected:
                continue
            offdiagonal = tuple(
                edge for edge in matching
                if word[edge[0]] != word[edge[1]]
            )
            if not offdiagonal:
                category = (
                    "all_diagonal_anchor_contained"
                    if set(matching) <= anchor_q_union
                    else "all_diagonal_external"
                )
            elif any(edge not in anchor_q_union for edge in offdiagonal):
                category = "external_offdiagonal"
            else:
                category = "anchor_contained_offdiagonal"
            mate_counts[(residual["rho3"], colour, category)] += 1
    return "supported_complement", available, mate_counts


def audit():
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
    _, returns = reconstruct_returns(second, first, routing)
    q_matchings = tuple(routing.perfect_matchings(range(6)))
    require(len(q_matchings) == 15, "the six-site matching count changed")

    geometry = Counter()
    available_colours = Counter()
    mate_categories = Counter()
    private_counts = Counter()
    witness_scores = Counter()
    witness_words = Counter()

    for residual, candidate in returns:
        _, sources, cells = selected_q_support(second, residual, candidate)
        rows = supported_top_rows(q_matchings, cells)
        private = [
            (word, monomials[0]) for word, monomials in rows.items()
            if word != (0,) * 6 and len(monomials) == 1
        ]
        require(private, "a return lost every private top coefficient")
        private_counts[len(private)] += 1

        pure = sources["K"] | sources["L"] | sources["M"]
        b_exclusive = sources["B"] - pure
        c_exclusive = sources["C"] - pure
        ranked = []
        for word, monomial in private:
            sides = int(bool(monomial & b_exclusive)) + int(
                bool(monomial & c_exclusive)
            )
            exclusive_cells = len(monomial & (b_exclusive | c_exclusive))
            ranked.append(((sides, exclusive_cells), word, monomial))
        score, word, _ = max(ranked, key=lambda item: (item[0], item[1]))
        require(score[0] >= 1,
                "the chosen private top row lost both return tails")
        witness_scores[(residual["rho3"], *score)] += 1
        witness_words[(residual["rho3"], "".join(map(str, word)))] += 1

        kind, available, counts = geometry_and_hybrid(
            second, routing, q_matchings, residual, candidate, cells
        )
        geometry[(residual["rho3"], kind)] += 1
        if available:
            available_colours[(residual["rho3"], available)] += 1
        mate_categories.update(counts)

    require(private_counts == Counter({
        4: 8, 5: 14, 6: 36, 7: 8, 8: 148, 9: 78, 10: 64,
        11: 90, 12: 76, 14: 143, 15: 12, 17: 70, 20: 66, 26: 39,
    }), f"the private-row distribution changed: {private_counts}")
    require(witness_scores == Counter({
        (0, 2, 3): 134, (0, 2, 2): 44, (0, 1, 2): 20,
        (1, 2, 3): 264, (1, 2, 2): 58, (1, 1, 2): 122,
        (1, 1, 1): 12,
        (2, 2, 3): 134, (2, 2, 2): 44, (2, 1, 2): 20,
    }), f"the return-tail witness scores changed: {witness_scores}")
    require(sum(value for key, value in witness_scores.items()
                if key[1] == 2) == 678,
            "the two-tail private-row count changed")
    require(geometry == Counter({
        (0, "supported_complement"): 158,
        (1, "supported_complement"): 288,
        (2, "supported_complement"): 158,
        (1, "missing_complement"): 84,
        (0, "overlap"): 40,
        (1, "overlap"): 84,
        (2, "overlap"): 40,
    }), f"the top-hybrid geometry changed: {geometry}")

    expected_mates = Counter({
        (0, 0, "anchor_contained_offdiagonal"): 135,
        (0, 0, "external_offdiagonal"): 873,
        (0, 1, "anchor_contained_offdiagonal"): 295,
        (0, 1, "external_offdiagonal"): 1637,
        (0, 2, "anchor_contained_offdiagonal"): 225,
        (0, 2, "external_offdiagonal"): 1791,
        (1, 0, "anchor_contained_offdiagonal"): 95,
        (1, 0, "external_offdiagonal"): 1081,
        (1, 1, "anchor_contained_offdiagonal"): 1233,
        (1, 1, "external_offdiagonal"): 2463,
        (1, 2, "anchor_contained_offdiagonal"): 477,
        (1, 2, "external_offdiagonal"): 2127,
        (2, 0, "all_diagonal_anchor_contained"): 11,
        (2, 0, "all_diagonal_external"): 61,
        (2, 0, "anchor_contained_offdiagonal"): 60,
        (2, 0, "external_offdiagonal"): 876,
        (2, 1, "all_diagonal_anchor_contained"): 27,
        (2, 1, "all_diagonal_external"): 387,
        (2, 1, "anchor_contained_offdiagonal"): 202,
        (2, 1, "external_offdiagonal"): 1316,
        (2, 2, "all_diagonal_anchor_contained"): 29,
        (2, 2, "all_diagonal_external"): 403,
        (2, 2, "anchor_contained_offdiagonal"): 196,
        (2, 2, "external_offdiagonal"): 1388,
    })
    require(mate_categories == expected_mates,
            f"the supported-hybrid mate split changed: {mate_categories}")
    require(not any("all_diagonal" in key[2] and key[0] != 2
                    for key in mate_categories),
            "rho=0 or 1 acquired an all-diagonal mate")

    ledger = {
        "returns": len(returns),
        "private_top_rows_per_return": {
            str(key): value for key, value in sorted(private_counts.items())
        },
        "private_rows_touching_both_return_tails": 678,
        "private_rows_touching_one_return_tail": 174,
        "short_PS00_hybrid_geometry": {
            str(key): value for key, value in sorted(geometry.items())
        },
        "supported_PS00_hybrids": 604,
        "missing_complementary_q_cell": 84,
        "overlapping_B_C_tail_edges": 164,
        "available_diagonal_colours": {
            str(key): value for key, value in sorted(available_colours.items())
        },
        "supported_hybrid_alternate_mates": {
            str(key): value for key, value in sorted(mate_categories.items())
        },
        "conclusion": (
            "At exact M,L,K,B,C carrier support every return has a private "
            "nonzero monomial in a zero q^[3] word, so its localized "
            "coefficient ideal is the unit ideal.  Every physical completion "
            "must add a literal q-matching companion.  This does not prove "
            "the arbitrary-support return packet empty."
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
    require(digest == EXPECTED_LEDGER_SHA256,
            f"the frozen return-top ledger changed: {digest}")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")
    print("h3 target-coloop return common-q top companion: PASS")


if __name__ == "__main__":
    main()
