#!/usr/bin/env python3
"""Replay the finite GLD19--GLD22 core and pin an optional source checkout.

This is an import-boundary audit, not a proof of a bridge from the local
EqSystem/PAComp objects to the external fixed-Q companion module.
"""

from __future__ import annotations

import argparse
import hashlib
import subprocess
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path


EXTERNAL_COMMIT = "2244a513888bf39294cf749001ff3be60bd280a8"

SOURCE_HASHES = {
    # Load-bearing dependencies named by GLD19--GLD22.
    "claims/arbitrary-order/FIXED_Q_JOINT_MZ_MODULE_QUOTIENT_PAIRED_ATTACHMENT_AND_RANK_ONE_FIBRE_BOUNDARY_THEOREM.md": "4ca4818283b2e624ad3e414b90c59cc4819e0edd04d18b2f3157593ff3db570f",
    "claims/arbitrary-order/FIXED_Q_RESPONSE_VISIBLE_OPERATOR_SLOPE_AND_EDGE_DEPENDENT_CANCELLATION_DIVISOR_THEOREM.md": "54bfa1fa9a89100869553131b4f6b66354583e0d17b79948ac8f4c66a8842ee3",
    # GLD19--GLD22 theorem statements.
    "claims/arbitrary-order/FIXED_Q_FULLY_RESPONSE_INVISIBLE_TWELVE_ROW_COMPLEMENTARY_SUPPORT_DIVISOR_THEOREM.md": "099c88f378db54b2f998e082d02ea8c76c4fbce34ca53e035d464e0a6d0b1552",
    "claims/arbitrary-order/FIXED_Q_RESPONSE_MAP_ZERO_GLOBAL_PHYSICAL_CHANNEL_SUPPORT_AND_COMPLEMENTARY_PURE_ABSORPTION_THEOREM.md": "b1a8f81623aacea0f1a1a9ca2b6015c4c7b9bc0787a23063690dc481da35bf4e",
    "claims/arbitrary-order/FIXED_Q_RESPONSE_MAP_ZERO_DEAD_COLOUR_H_GATE_AND_DENSE_COMPANION_ABSORPTION_THEOREM.md": "6e77435a9184b024187684f8eebd7af8a1ed885c32064e5d9290fa72ac23cc56",
    "claims/arbitrary-order/FIXED_Q_DENSE_PRIVATE_CROSS_MATCHING_ROOT_COMPANION_EXCLUSION_THEOREM.md": "a1bad30fcf1312c55cf8ae137e015bad215458ded136ab4381d4e1fc533240b2",
    # Primary and independently implemented upstream replays.
    "claims/arbitrary-order/verify_fixed_q_fully_response_invisible_complementary_support_divisor.py": "03b839d92cb4ee2329178f9c80af4c1d0794c798491850bb3627ecd8008badef",
    "claims/arbitrary-order/audit_fixed_q_fully_response_invisible_complementary_support_divisor.py": "5293339335eaed1fb0f1f8725a9c4f72334ccc3b5f5bd1adb7363591b4c16302",
    "claims/arbitrary-order/verify_fixed_q_response_map_zero_global_physical_channel_support_and_pure_absorption.py": "2758c4de6abe4f4e8cef72d758970e7d64de5e9ce5fa7d7064416068ca9a9792",
    "claims/arbitrary-order/audit_fixed_q_response_map_zero_global_physical_channel_support_and_pure_absorption.py": "f46c7f6171faeb413596b989696504ebb31d7a10fff353e1b7f06d9bece6cc0d",
    "claims/arbitrary-order/verify_fixed_q_response_map_zero_dead_colour_h_gate_and_dense_companion_absorption.py": "154825ba62d96bcf22782c588285aaf4c8a29f242cbb2d35407ad246816a22ba",
    "claims/arbitrary-order/audit_fixed_q_response_map_zero_dead_colour_h_gate_and_dense_companion_absorption.py": "c7d3cf9853e7f56c394a7804e1f1206114fdc7c182d6c6d8327b022cc85341b4",
    "claims/arbitrary-order/verify_fixed_q_dense_private_cross_matching_root_companion_exclusion.py": "b607ecf7503fc6d4e10a9306eec79cc11f8e3cbbacfb822599865f6cb976efd2",
    "claims/arbitrary-order/audit_fixed_q_dense_private_cross_matching_root_companion_exclusion.py": "c9cfbabeb90ecfcde05dbd30aa624281b40bc7a965e76a0112c6af220a8be6b3",
    # Hostile scope reviews.
    "docs/audits/FIXED_Q_RESPONSE_MAP_ZERO_COMPLEMENTARY_SUPPORT_REVIEW_2026-08-17.md": "2a7db20009a73ead5f6300487cdb0df1579123eb9500f77aec4d9aad03fca406",
    "docs/audits/FIXED_Q_RESPONSE_MAP_ZERO_GLOBAL_PHYSICAL_CHANNEL_SUPPORT_REVIEW_2026-08-18.md": "ecf1d45ae5deff0d22f72f3239fa88e5749aefb03f58ddef22168e75ecabd670",
    "docs/audits/FIXED_Q_RESPONSE_MAP_ZERO_DEAD_COLOUR_H_GATE_AND_DENSE_COMPANION_ABSORPTION_REVIEW_2026-08-18.md": "77be363e409d9a229128efbf92774a484215758d4368acc0305976157b62a059",
    "docs/audits/FIXED_Q_DENSE_PRIVATE_CROSS_MATCHING_ROOT_COMPANION_EXCLUSION_REVIEW_2026-08-19.md": "37385f57f7292c28f73db08cada3055227fb0dee11f60a6dc79da36d3024d9fa",
}

UPSTREAM_REPLAYS = (
    (False, "claims/arbitrary-order/verify_fixed_q_fully_response_invisible_complementary_support_divisor.py"),
    (True, "claims/arbitrary-order/audit_fixed_q_fully_response_invisible_complementary_support_divisor.py"),
    (False, "claims/arbitrary-order/verify_fixed_q_response_map_zero_global_physical_channel_support_and_pure_absorption.py"),
    (True, "claims/arbitrary-order/audit_fixed_q_response_map_zero_global_physical_channel_support_and_pure_absorption.py"),
    (False, "claims/arbitrary-order/verify_fixed_q_response_map_zero_dead_colour_h_gate_and_dense_companion_absorption.py"),
    (True, "claims/arbitrary-order/audit_fixed_q_response_map_zero_dead_colour_h_gate_and_dense_companion_absorption.py"),
    (False, "claims/arbitrary-order/verify_fixed_q_dense_private_cross_matching_root_companion_exclusion.py"),
    (True, "claims/arbitrary-order/audit_fixed_q_dense_private_cross_matching_root_companion_exclusion.py"),
)

PORTS = tuple(range(4))
COLORS = tuple(range(3))
EDGES = tuple(combinations(PORTS, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
COMPLEMENTS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_external_checkout(root: Path, upstream_python: str) -> None:
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    assert head == EXTERNAL_COMMIT, (head, EXTERNAL_COMMIT)
    for relative, expected in SOURCE_HASHES.items():
        actual = sha256(root / relative)
        assert actual == expected, (relative, actual, expected)
    print(f"PASS source pin: {head}, {len(SOURCE_HASHES)} frozen files")

    for isolated, relative in UPSTREAM_REPLAYS:
        command = [upstream_python]
        if isolated:
            command.append("-I")
        command.append(relative)
        completed = subprocess.run(
            command,
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode:
            raise AssertionError(
                f"upstream replay failed: {relative}\n"
                f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
            )
        lines = [line for line in completed.stdout.splitlines() if line.strip()]
        assert lines, relative
        print(f"PASS upstream {Path(relative).name}: {lines[-1]}")


def support(mask: int) -> frozenset[int]:
    return frozenset(color for color in COLORS if mask & (1 << color))


def gl19_rows_clear(be: int, bf: int, ke: int, kf: int) -> bool:
    for first, second in product(COLORS, repeat=2):
        if first == second:
            continue
        if be & (1 << first) and bf & (1 << second):
            return False
        if be & (1 << first) and kf & (1 << second):
            return False
        if ke & (1 << first) and bf & (1 << second):
            return False
    return True


def audit_gld19() -> None:
    rank_at_most_two = tuple(mask for mask in range(8) if mask != 7)
    allowed = []
    zero_five = 0
    successor = (1, 2, 0)
    for be, bf, ke, kf in product(range(8), range(8), rank_at_most_two, rank_at_most_two):
        if gl19_rows_clear(be, bf, ke, kf):
            allowed.append((be, bf, ke, kf))
            assert (be | ke) != 7 or (bf | kf) != 7

        detector = []
        for color in COLORS:
            other = successor[color]
            detector.append(bool(be & (1 << color) and bf & (1 << other)))
        for color in (0, 1):
            other = successor[color]
            detector.append(
                bool(be & (1 << color) and kf & (1 << other))
                or bool(ke & (1 << color) and bf & (1 << other))
            )
        if not any(detector):
            zero_five += 1
            assert (be | ke) != 7 or (bf | kf) != 7

    assert len(allowed) == 201
    assert zero_five > 0
    print(f"PASS GLD19 finite core: 201/3136 twelve-row support cells; {zero_five} five-row-zero controls")


def vertices(mask: int) -> frozenset[int]:
    return frozenset(vertex for vertex in PORTS if mask & (1 << vertex))


def clique(vertex_set: frozenset[int]) -> frozenset[tuple[int, int]]:
    return frozenset(combinations(sorted(vertex_set), 2))


def is_p4(graph: frozenset[tuple[int, int]]) -> bool:
    if len(graph) != 3:
        return False
    degrees = sorted(sum(vertex in edge for edge in graph) for vertex in PORTS)
    if degrees != [1, 1, 2, 2]:
        return False
    seen = {next(iter(graph))[0]}
    while True:
        enlarged = seen | {
            endpoint
            for edge in graph
            if set(edge) & seen
            for endpoint in edge
        }
        if enlarged == seen:
            return len(seen) == 4
        seen = enlarged


def channel_atlas() -> set[tuple[int, ...]]:
    atlas = {(0,) * 6}
    for color in COLORS:
        for graph_mask in range(1, 64):
            graph = frozenset(
                edge for index, edge in enumerate(EDGES) if graph_mask & (1 << index)
            )
            if not is_p4(graph):
                atlas.add(tuple((1 << color) if edge in graph else 0 for edge in EDGES))

    nontrivial = tuple(vertices(mask) for mask in range(16) if mask.bit_count() >= 2)
    for first_color, second_color in combinations(COLORS, 2):
        for first_vertices, second_vertices in product(nontrivial, repeat=2):
            first_edges = clique(first_vertices)
            second_edges = clique(second_vertices)
            atlas.add(
                tuple(
                    ((1 << first_color) if edge in first_edges else 0)
                    | ((1 << second_color) if edge in second_edges else 0)
                    for edge in EDGES
                )
            )
    return atlas


def pair_allowed(be: int, bf: int, ke: int, kf: int) -> bool:
    be_support, bf_support = support(be), support(bf)
    if be and bf:
        return (
            len(be_support) == 1
            and be == bf
            and ke | be == be
            and kf | be == be
        )
    if be:
        return kf == 0 if len(be_support) > 1 else kf | be == be
    if bf:
        return ke == 0 if len(bf_support) > 1 else ke | bf == bf
    return True


def full_family_shape(family: int) -> str:
    chosen = tuple(edge for index, edge in enumerate(EDGES) if family & (1 << index))
    if not chosen:
        return "empty"
    if len(chosen) == 1:
        return "single"
    if len(chosen) == 2:
        assert set(chosen[0]) & set(chosen[1])
        return "adjacent"
    degrees = sorted(sum(vertex in edge for edge in chosen) for vertex in PORTS)
    if degrees == [1, 1, 1, 3]:
        return "star"
    assert degrees == [0, 2, 2, 2]
    return "triangle"


def local_direct_choices(channel: tuple[int, ...], left: tuple[int, int], right: tuple[int, int]) -> tuple[tuple[int, int, int], ...]:
    left_index, right_index = EDGE_INDEX[left], EDGE_INDEX[right]
    choices = []
    for be, bf in product(range(8), repeat=2):
        if not pair_allowed(be, bf, channel[left_index], channel[right_index]):
            continue
        family = 0
        if be | channel[left_index] == 7:
            family |= 1 << left_index
        if bf | channel[right_index] == 7:
            family |= 1 << right_index
        assert family.bit_count() <= 1
        choices.append((be, bf, family))
    return tuple(choices)


def audit_gld20() -> set[tuple[int, ...]]:
    atlas = channel_atlas()
    assert len(atlas) == 517
    color_distribution = Counter(
        (channel[0] | channel[1] | channel[2] | channel[3] | channel[4] | channel[5]).bit_count()
        for channel in atlas
    )
    assert color_distribution == Counter({0: 1, 1: 153, 2: 363})

    ledger = Counter()
    for channel in atlas:
        color_count = (channel[0] | channel[1] | channel[2] | channel[3] | channel[4] | channel[5]).bit_count()
        choices = [local_direct_choices(channel, left, right) for left, right in COMPLEMENTS]
        for first, second, third in product(*choices):
            family = first[2] | second[2] | third[2]
            ledger[(color_count, full_family_shape(family))] += 1

    expected = {
        0: (4096, 1536, 192, 4, 4),
        1: (109248, 58464, 10512, 312, 312),
        2: (141651, 110736, 27864, 432, 2352),
    }
    shapes = ("empty", "single", "adjacent", "star", "triangle")
    for color_count, row in expected.items():
        assert tuple(ledger[(color_count, shape)] for shape in shapes) == row
    assert sum(ledger.values()) == 467715
    assert sum(ledger[(color_count, "empty")] for color_count in COLORS) == 254995
    print("PASS GLD20 finite core: 517 corrected channels; 467715 raw cells; 254995 F=empty")
    return atlas


def dense_or_dominant_channels() -> set[tuple[int, ...]]:
    nontrivial = tuple(vertices(mask) for mask in range(16) if mask.bit_count() >= 2)
    result = set()
    for first_color, second_color in combinations(COLORS, 2):
        for first_vertices, second_vertices in product(nontrivial, repeat=2):
            if len(first_vertices) < 4 and len(second_vertices) < 4:
                continue
            first_edges, second_edges = clique(first_vertices), clique(second_vertices)
            result.add(
                tuple(
                    ((1 << first_color) if edge in first_edges else 0)
                    | ((1 << second_color) if edge in second_edges else 0)
                    for edge in EDGES
                )
            )
    return result


def audit_gld21() -> None:
    channels = dense_or_dominant_channels()
    assert len(channels) == 63
    raw_total = 0
    by_secondary_size = Counter()
    for channel in channels:
        union = 0
        intersection = 7
        for mask in channel:
            union |= mask
            intersection &= mask
        assert union.bit_count() == 2
        dense = all(mask == union for mask in channel)
        assert intersection.bit_count() == (2 if dense else 1)
        missing = next(color for color in COLORS if not union & (1 << color))

        choices = [local_direct_choices(channel, left, right) for left, right in COMPLEMENTS]
        cell_count = 0
        for triple in product(*choices):
            direct = [0] * 6
            for (left, right), choice in zip(COMPLEMENTS, triple, strict=True):
                direct[EDGE_INDEX[left]], direct[EDGE_INDEX[right]] = choice[0], choice[1]
            assert all(not mask & (1 << missing) for mask in direct)
            assert all(not mask & ~intersection for mask in direct)
            assert all((bmask | kmask) != 7 for bmask, kmask in zip(direct, channel, strict=True))
            cell_count += 1
        raw_total += cell_count

        if dense:
            secondary_size = 4
        else:
            edge_counts = [
                sum(bool(mask & (1 << color)) for mask in channel)
                for color in COLORS
                if union & (1 << color)
            ]
            secondary_size = 2 if min(edge_counts) == 1 else 3
        by_secondary_size[secondary_size] += cell_count

    assert raw_total == 1347
    assert by_secondary_size == Counter({2: 36 * 32, 3: 24 * 8, 4: 3})
    print("PASS GLD21 finite core: 63 dominant/dense channels; 1347 raw cells")


# Independent exact ten-site GLD22 fixture.
ROOTS = tuple(range(4))
Q0, Q1 = 4, 5
ROOT_PORTS = tuple(range(6, 10))
TEN_VERTICES = ROOTS + (Q0, Q1) + ROOT_PORTS
ACTIVE = (0, 1)
DEAD = 2


def solve_q_covectors(h: Fraction, tau: tuple[tuple[Fraction, ...], ...], x: tuple[Fraction, ...], y: tuple[Fraction, ...]) -> tuple[tuple[tuple[Fraction, ...], ...], tuple[tuple[Fraction, ...], ...]]:
    determinant = y[0] * x[1] - y[1] * x[0]
    assert determinant
    q0_rows, q1_rows = [], []
    for root in ROOTS:
        wanted0 = (-h * tau[root][0], Fraction(0), Fraction(0))
        wanted1 = (Fraction(0), -h * tau[root][1], Fraction(0))
        q0_rows.append(tuple((wanted0[c] * x[1] - wanted1[c] * x[0]) / determinant for c in COLORS))
        q1_rows.append(tuple((y[0] * wanted1[c] - y[1] * wanted0[c]) / determinant for c in COLORS))
    return tuple(q0_rows), tuple(q1_rows)


def private_fixture(kill_active_diagonals: bool) -> dict[str, object]:
    h = Fraction(11)
    tau = tuple(tuple(Fraction(3 + 5 * root + 2 * color) for color in COLORS) for root in ROOTS)
    x = (Fraction(2), Fraction(5), Fraction(0))
    y = (Fraction(3), Fraction(-15, 2), Fraction(0))
    assert x[0] * y[1] + y[0] * x[1] == 0
    q0_rows, q1_rows = solve_q_covectors(h, tau, x, y)
    root_root = {}
    for left, right in combinations(ROOTS, 2):
        for left_color, right_color in product(COLORS, repeat=2):
            value = Fraction(101 + 23 * left + 29 * right + 7 * left_color + 3 * right_color)
            if kill_active_diagonals and left_color == right_color in ACTIVE:
                value = Fraction(0)
            root_root[(left, right, left_color, right_color)] = value
    return {"h": h, "tau": tau, "x": x, "y": y, "q0": q0_rows, "q1": q1_rows, "rr": root_root}


def ten_edge(data: dict[str, object], left: int, right: int, root_word: tuple[int, ...], port_word: tuple[int, ...]) -> Fraction:
    if left > right:
        left, right = right, left
    tau = data["tau"]
    assert isinstance(tau, tuple)
    if left in ROOTS and right in ROOTS:
        root_root = data["rr"]
        assert isinstance(root_root, dict)
        return root_root[(left, right, root_word[left], root_word[right])]
    if left in ROOTS and right in (Q0, Q1):
        rows = data["q0"] if right == Q0 else data["q1"]
        assert isinstance(rows, tuple)
        return rows[left][root_word[left]]
    if left in ROOTS and right in ROOT_PORTS:
        port = right - ROOT_PORTS[0]
        return tau[left][root_word[left]] if left == port and root_word[left] == port_word[port] else Fraction(0)
    if (left, right) == (Q0, Q1):
        h = data["h"]
        assert isinstance(h, Fraction)
        return h
    if left in (Q0, Q1) and right in ROOT_PORTS:
        shore = data["x"] if left == Q0 else data["y"]
        assert isinstance(shore, tuple)
        return shore[port_word[right - ROOT_PORTS[0]]]
    if left in ROOT_PORTS and right in ROOT_PORTS:
        return Fraction(0)
    raise AssertionError((left, right))


def ten_matching_sum(data: dict[str, object], root_word: tuple[int, ...], port_word: tuple[int, ...], remaining: tuple[int, ...] = TEN_VERTICES) -> Fraction:
    if not remaining:
        return Fraction(1)
    first = remaining[0]
    total = Fraction(0)
    for offset, second in enumerate(remaining[1:], start=1):
        edge = ten_edge(data, first, second, root_word, port_word)
        if edge:
            total += edge * ten_matching_sum(data, root_word, port_word, remaining[1:offset] + remaining[offset + 1 :])
    return total


def tau_product(data: dict[str, object], word: tuple[int, ...]) -> Fraction:
    tau = data["tau"]
    assert isinstance(tau, tuple)
    result = Fraction(1)
    for root, color in enumerate(word):
        result *= tau[root][color]
    return result


def matching_word(edge: tuple[int, int], repeated: int, orientation: int) -> tuple[tuple[int, ...], tuple[int, int]]:
    complement = tuple(root for root in ROOTS if root not in edge)
    if orientation:
        complement = complement[::-1]
    word = [DEAD] * 4
    word[edge[0]] = word[edge[1]] = repeated
    word[complement[0]] = 1 - repeated
    return tuple(word), complement


def audit_gld22() -> None:
    raw = private_fixture(False)
    killed = private_fixture(True)
    diagonal_gates = 0
    dense_detectors = 0
    for edge in combinations(ROOTS, 2):
        for repeated in ACTIVE:
            other = 1 - repeated
            for orientation in (0, 1):
                word, complement = matching_word(edge, repeated, orientation)

                opposite_port = list(word)
                opposite_port[edge[0]] = opposite_port[edge[1]] = other
                opposite_port[complement[0]] = repeated
                opposite_port = tuple(opposite_port)
                double_root = list(opposite_port)
                double_root[edge[0]] = double_root[edge[1]] = repeated
                double_root = tuple(double_root)

                tau = raw["tau"]
                root_root = raw["rr"]
                x, y = raw["x"], raw["y"]
                assert isinstance(tau, tuple) and isinstance(root_root, dict)
                assert isinstance(x, tuple) and isinstance(y, tuple)
                corrected_other = 2 * x[other] * y[other]
                expected_gate = corrected_other * tau[complement[0]][repeated] * tau[complement[1]][DEAD] * root_root[(edge[0], edge[1], repeated, repeated)]
                assert expected_gate
                assert ten_matching_sum(raw, double_root, opposite_port) == expected_gate
                diagonal_gates += 1

                h = killed["h"]
                assert isinstance(h, Fraction)
                expected_detector = -2 * h * tau_product(killed, word)
                assert expected_detector
                assert ten_matching_sum(killed, word, word) == expected_detector
                dense_detectors += 1

    assert diagonal_gates == dense_detectors == 24
    assert (-2) % 2 == 0 and all((-2) % prime for prime in (3, 5, 7))
    print("PASS GLD22 finite core: 24 diagonal gates and 24 ten-site -2hP detectors")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--external",
        type=Path,
        help="optional krenn-gu-research checkout pinned at the audited commit",
    )
    parser.add_argument(
        "--upstream-python",
        default="python",
        help="interpreter with SymPy for the four upstream primary replays",
    )
    arguments = parser.parse_args()

    if arguments.external is not None:
        verify_external_checkout(arguments.external.resolve(), arguments.upstream_python)
    audit_gld19()
    audit_gld20()
    audit_gld21()
    audit_gld22()
    print("PASS import boundary: finite claims replayed; no local PAComp/source bridge asserted")


if __name__ == "__main__":
    main()
