#!/usr/bin/env python3
"""Audit the first induced S3 dual against the relative C4 switch DGA."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
import importlib.util
import json
from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
NORMALIZED = ROOT / "computations/verify_n8_normalized_critical_contraction.py"
ONE_PAGE = ROOT / "computations/unaudited-codex-n8-s3-dual-next-attachments-2026-08-23/results_s3_dual_one_page.json"
SWITCH_NOTE = ROOT / "notes/uniform-chart-cross-companion-relative-switch-dga-gate.md"
SWITCH_CHECK = ROOT / "computations/verify_uniform_chart_cross_companion_relative_switch_dga_gate.py"
CAP_NOTE = ROOT / "notes/h3-jd-normalized-cube-physical-cap-homology.md"
CAP_CHECK = ROOT / "computations/verify_h3_jd_normalized_cube_physical_cap_homology.py"
LOW_SCRIPT = ROOT / "computations/unaudited-codex-n8-s3-source-component-2026-08-23/audit_s3_source_component.py"
HPL_SCRIPT = ROOT / "computations/unaudited-codex-n8-s3-source-hpl-audit-2026-08-23/audit_s3_source_hpl.py"
TERMINAL_C6_NOTE = ROOT / "notes/2026-08-14-terminal-c6-labelled-boundary-transfer-trichotomy.md"
TERMINAL_C6_CHECK = ROOT / "computations/verify_uniform_terminal_c6_labelled_boundary_transfer_trichotomy.py"
E3_NOTE = ROOT / "notes/h3-axis-target-coloop-even-cycle-e3-boundary.md"
E3_CHECK = ROOT / "computations/verify_h3_axis_target_coloop_even_cycle_e3_boundary.py"
RESULT = HERE / "results_induced_switch_dga.json"
EXPECTED = {
    NORMALIZED: "4e2ce4b12626edaedd9a8a5a4a9635ab5c74a5f139ecf52507018ca5478acd62",
    ONE_PAGE: "b31faacf0929605bb72dc8a1424832d18c452c7f45eee7bc669d63a33567727d",
    SWITCH_NOTE: "2b9fbe0c648cadc5913e57e4b6d678205c7f7fbc66f57e58e371f9ad10ef2cb8",
    SWITCH_CHECK: "e0a8251128174d50b450b3bf85ce0a6870af00d4ab5565e7849fc3c8644c31c6",
    CAP_NOTE: "aedbf960e7d1758f765d92fb9a8a883c11b89d792986e0db1c5c7ecd266f87f8",
    CAP_CHECK: "2488998937c4aac2915a9335c48d40398b419ee654092d9a9942157abd04b9e3",
    LOW_SCRIPT: "a4d22563904e8dde445067b9e8c466cd048ea471ffdaac566b66202eec1ae189",
    HPL_SCRIPT: "a983e37145dbf480262868a45b91aa42c07d9d72f74e85a395ea099220687479",
    TERMINAL_C6_NOTE: "f61a1a53490a16368da48448708efefdaae514389a1af6269ba353b5406a06ab",
    TERMINAL_C6_CHECK: "c9809fe9c8aa1c9c8d2439bad10bf69cda1d83a290a86eb9184cf779f28e2dde",
    E3_NOTE: "52897d6063ff5ca46c714a5262c87fae4d243779ccdaee6caa4498c70dd8f2f9",
    E3_CHECK: "d42f7b266764f1c7d371a64f323fff1c5b50a9d73b30d343112603d1924435c8",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_source():
    spec = importlib.util.spec_from_file_location("s3_switch_normalized", NORMALIZED)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, "cannot load normalized source")
    spec.loader.exec_module(module)
    return module.D5


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, f"cannot load {path}")
    spec.loader.exec_module(module)
    return module


def multiply(*rows):
    return bytes(sorted(sum((tuple(row) for row in rows), ())))


def source_polynomial(D5, code):
    polynomial = Counter()
    raw = defaultdict(list)
    for literal_value in D5.iter_word_terms(code):
        literal = bytes(literal_value)
        normalized = bytes(sorted(cell for cell in literal if D5.IS_OFF_SUPPORT[cell]))
        polynomial[normalized] += 1
        raw[normalized].append(literal)
    return polynomial, raw


def physical_edges(D5, literal):
    return tuple(sorted(tuple(D5.COORDINATES[cell][:2]) for cell in literal))


def alternating_switch_profile(D5, left, right):
    """Classify two literal perfect matchings by their alternating cycle."""
    left_edges = set(physical_edges(D5, left))
    right_edges = set(physical_edges(D5, right))
    common = left_edges & right_edges
    difference = left_edges ^ right_edges
    adjacency = defaultdict(set)
    for u, v in difference:
        adjacency[u].add(v)
        adjacency[v].add(u)
    require(all(len(neighbours) == 2 for neighbours in adjacency.values()),
            "symmetric difference stopped being alternating cycles")
    components = []
    unseen = set(adjacency)
    while unseen:
        seed = min(unseen)
        stack = [seed]
        component = set()
        while stack:
            vertex = stack.pop()
            if vertex in component:
                continue
            component.add(vertex)
            stack.extend(adjacency[vertex] - component)
        unseen -= component
        components.append(sorted(component))
    return {
        "common_edges": [list(edge) for edge in sorted(common)],
        "symmetric_difference_edges": [list(edge) for edge in sorted(difference)],
        "alternating_cycle_lengths": sorted(len(component) for component in components),
        "is_one_C4_switch": len(components) == 1 and len(components[0]) == 4,
    }


def decoded(D5, row):
    return [list(D5.COORDINATES[cell]) for cell in row]


def audit(mutate=False):
    for path, digest in EXPECTED.items():
        require(sha256(path.read_bytes()).hexdigest() == digest,
                f"source drift: {path}")
    D5 = load_source()
    page = json.loads(ONE_PAGE.read_text())
    require(page["logical_sha256"]
                == "f9624e2016376f80208d402c32628c084b4e7a27f31e0790c8cd9aabea142c65"
            and page["all_killers"]["rank_profile"] == {
                "1009": {"columns": 333, "with_target": 334},
                "1013": {"columns": 333, "with_target": 334},
            }
            and page["all_killers"]["internal_response_packets"] == [],
            "one-page induced class changed")
    induced = {
        bytes.fromhex(row): value
        for row, value in page["all_killers"]["induced_dual"]
    }
    require(induced == {
        bytes.fromhex("1eb7bd"): 1,
        bytes.fromhex("2045ae"): 1,
        bytes.fromhex("2799b7"): -1,
    }, "induced dual changed")

    polynomials = {}
    raw = {}
    for code in (10, 2919, 3270, 3645, 3780, 3790):
        polynomials[code], raw[code] = source_polynomial(D5, code)

    # These are the only two old low columns incident to the induced dual.
    multiplier_36 = bytes([D5.COORDINATE_ID[(3, 6, 1, 0)]])
    require(multiplier_36 == bytes.fromhex("b7"), "first multiplier changed")
    column_2919 = Counter()
    for row, value in polynomials[2919].items():
        if len(row) <= 2:
            column_2919[multiply(multiplier_36, row)] += value
    column_3780 = Counter({row: value for row, value in polynomials[3780].items()
                           if len(row) <= 3})
    intersections = {
        "2919_times_A36[1,0]": [[row.hex(), column_2919[row], induced[row]]
                                 for row in sorted(set(column_2919) & set(induced))],
        "3780_times_t": [[row.hex(), column_3780[row], induced[row]]
                          for row in sorted(set(column_3780) & set(induced))],
    }
    require(intersections == {
        "2919_times_A36[1,0]": [["1eb7bd", 1, 1], ["2799b7", 1, -1]],
        "3780_times_t": [["2045ae", 1, 1], ["2799b7", 1, -1]],
    }, "induced-dual incident column restrictions changed")

    # Restore the literal perfect matchings underneath each normalized row.
    def unique_raw(code, normalized):
        require(len(raw[code][normalized]) == 1,
                f"raw completion {code}/{normalized.hex()} is not unique")
        return raw[code][normalized][0]

    first_2919 = unique_raw(2919, bytes.fromhex("1ebd"))
    second_2919 = unique_raw(2919, bytes.fromhex("2799"))
    first_3780 = unique_raw(3780, bytes.fromhex("2045ae"))
    second_3780 = unique_raw(3780, bytes.fromhex("2799b7"))
    require((first_2919.hex(), second_2919.hex(),
             first_3780.hex(), second_3780.hex())
            == ("1e6787bd", "276799a2", "2045aef3", "275999b7"),
            "literal induced-row completions changed")
    switch_2919 = alternating_switch_profile(D5, first_2919, second_2919)
    switch_3780 = alternating_switch_profile(D5, first_3780, second_3780)
    require(switch_2919["alternating_cycle_lengths"] == [6]
            and switch_2919["common_edges"] == [[1, 6]]
            and not switch_2919["is_one_C4_switch"],
            "first induced relation stopped being a C6 switch")
    require(switch_3780["alternating_cycle_lengths"] == [8]
            and switch_3780["common_edges"] == []
            and not switch_3780["is_one_C4_switch"],
            "second induced relation stopped being a C8 switch")

    # The archived positive C6 packet and one-bad E3 theorems have stronger
    # literal hypotheses than an unlabelled even-cycle signature.  Freeze
    # the exact label failures rather than importing either theorem.
    def diagonal_cells(literal):
        return all(D5.COORDINATES[cell][2] == D5.COORDINATES[cell][3]
                   for cell in literal)

    def endpoint_zero_star_cells(literal, endpoint, mate):
        answer = []
        for cell in literal:
            left, right, left_colour, right_colour = D5.COORDINATES[cell]
            if endpoint not in (left, right) or mate in (left, right):
                continue
            colour = left_colour if endpoint == left else right_colour
            if colour == 0:
                answer.append(cell)
        return answer

    def contains_edge(literal, edge):
        return any(tuple(D5.COORDINATES[cell][:2]) == edge for cell in literal)

    require(not diagonal_cells(first_2919) and not diagonal_cells(second_2919),
            "induced C6 accidentally entered the sharp diagonal packet")
    c6_zero_stars = sorted(set(endpoint_zero_star_cells(first_2919, 7, 6)
                               + endpoint_zero_star_cells(second_2919, 7, 6)))
    require([D5.COORDINATES[cell] for cell in c6_zero_stars]
            == [(2, 7, 0, 0), (3, 7, 0, 0)],
            "C6 endpoint-zero-star guard changed")
    require(contains_edge(first_3780, (6, 7))
            and not contains_edge(second_3780, (6, 7)),
            "C8 direct-edge response-base guard changed")

    # Positive control: the original 3072/3969 response companions really
    # are the two C4 children of the common parent 05|87|a7|f3.
    child_left = unique_raw(3780, bytes.fromhex("3072a7"))
    child_right = unique_raw(3780, bytes.fromhex("3969a7"))
    parent = unique_raw(3780, bytes.fromhex("05a7"))
    require((child_left.hex(), child_right.hex(), parent.hex())
            == ("307287a7", "396987a7", "0587a7f3"),
            "response C4 parent/children changed")
    child_switch = alternating_switch_profile(D5, child_left, child_right)
    left_parent = alternating_switch_profile(D5, child_left, parent)
    right_parent = alternating_switch_profile(D5, child_right, parent)
    require(all(record["is_one_C4_switch"]
                for record in (child_switch, left_parent, right_parent)),
            "positive C4 response control failed")

    # Literal chart source does not isolate a Gamma_c carrier: the linear
    # provider for parent coordinate A01[1,2] contains all six C4 children.
    parent_cell = D5.COORDINATE_ID[(0, 1, 1, 2)]
    spectator = bytes([D5.COORDINATE_ID[(3, 4, 1, 2)]])
    require(parent_cell == 0x05 and spectator == bytes.fromhex("a7"),
            "parent/spectator identifiers changed")
    provider_low = Counter()
    for row, value in polynomials[3645].items():
        if len(row) <= 2:
            provider_low[multiply(spectator, row)] += value
    require(len(provider_low) == 7
            and provider_low[bytes.fromhex("05a7")] == 1
            and provider_low[bytes.fromhex("3072a7")] == 1
            and provider_low[bytes.fromhex("3969a7")] == 1,
            "literal C4 provider packet changed")

    # Exactly one further filtered page.  Enumerate every literal source
    # multiple whose y^3 lead meets the induced dual, add those lead columns
    # to the old target-rooted low component and recompute target membership.
    LOW = load("s3_switch_low", LOW_SCRIPT)
    HPL = load("s3_switch_hpl", HPL_SCRIPT)
    all_polynomials = LOW.normalized_polynomials(D5)
    s3 = LOW.parse_kernel("S3")
    h3 = LOW.parse_kernel("H3")
    target = {row: value for row, value in s3.items() if row not in h3}
    low_rows, old_columns_dict = LOW.build_low_component(target, all_polynomials)
    require((len(low_rows), len(old_columns_dict)) == (1311, 330),
            "old target-rooted low component changed")
    degree1_sources = defaultdict(list)
    for code, polynomial in all_polynomials.items():
        for row in polynomial:
            if len(row) == 1:
                degree1_sources[row].append(code)
    attachments = {}
    for target_row in induced:
        require(len(target_row) == 3, "induced dual left cubic low degree")
        for positions in combinations(range(3), 2):
            multiplier = bytes(sorted(target_row[position] for position in positions))
            base = bytes(target_row[position] for position in range(3)
                         if position not in positions)
            for code in degree1_sources[base]:
                key = (code, multiplier)
                if key in attachments:
                    continue
                full = Counter()
                for row, value in all_polynomials[code].items():
                    full[multiply(multiplier, row)] += value
                low = {row: value for row, value in full.items() if len(row) == 3}
                tail = {row: value for row, value in full.items() if len(row) > 3}
                require(low == {target_row: 1}
                        and Counter(map(len, tail)) == Counter({4: 6, 5: 30, 6: 68}),
                        "second-page attachment profile changed")
                attachments[key] = {
                    "hit": target_row,
                    "low": low,
                    "full": full,
                }
    hit_histogram = Counter(record["hit"].hex() for record in attachments.values())
    require(len(attachments) == 13 and hit_histogram == Counter({
        "1eb7bd": 4, "2045ae": 4, "2799b7": 5,
    }), "second-page attachment census changed")
    attachment_records = []
    for (code, multiplier), record in sorted(attachments.items()):
        attachment_records.append({
            "code": code,
            "word": "".join(map(str, D5.decode_word(code))),
            "multiplier": multiplier.hex(),
            "lead_row": record["hit"].hex(),
            "full_y_profile": {str(degree): count for degree, count in sorted(
                Counter(map(len, record["full"])).items()
            )},
        })

    old_columns = list(old_columns_dict.values())
    first_page_units = [
        {bytes.fromhex(row): 1}
        for row in ("0c4fcc", "1557a7", "3072a7")
        for _repeat in range({"0c4fcc": 4, "1557a7": 6, "3072a7": 4}[row])
    ]
    second_page_units = [record["low"] for record in attachments.values()]
    second_columns = old_columns + first_page_units + second_page_units
    rank_profile = {}
    for prime in (1009, 1013):
        rank_profile[str(prime)] = {
            "columns": LOW.modular_rank(
                low_rows, {index: column for index, column in enumerate(second_columns)},
                prime,
            ),
            "with_target": LOW.modular_rank(
                low_rows, {index: column for index, column
                           in enumerate(second_columns + [target])},
                prime,
            ),
        }
    require(set((record["columns"], record["with_target"])
                for record in rank_profile.values()) == {(336, 337)},
            "second-page target rank profile changed")
    next_dual = {
        bytes.fromhex("2790c0"): 1,
        bytes.fromhex("88eaf4"): 1,
        bytes.fromhex("90ea"): -1,
    }
    require(all(sum(next_dual.get(row, 0) * value
                    for row, value in column.items()) == 0
                for column in second_columns)
            and sum(next_dual.get(row, 0) * value for row, value in target.items()) == 1,
            "second-page exact induced dual failed")
    next_packets = HPL.internal_response_restrictions(next_dual)
    require(not next_packets, "second-page dual acquired a triangle response packet")

    # Structural migration audit.  The first two duals have the same
    # two-column C6/C8 incidence signature; the newest dual exits it into a
    # four-column C4 diamond around the y^2 parent 90ea.
    tiny_dual = {
        bytes.fromhex("0c4fcc"): 1,
        bytes.fromhex("1557a7"): 1,
        bytes.fromhex("3072a7"): -1,
    }

    def incident_records(dual):
        records = []
        for (code, multiplier), column in old_columns_dict.items():
            hits = sorted(set(column) & set(dual))
            if not hits:
                continue
            records.append({
                "code": code,
                "word": "".join(map(str, D5.decode_word(code))),
                "multiplier": "t" if multiplier == -1 else f"{multiplier:02x}",
                "column_support": len(column),
                "hits": [[row.hex(), column[row], dual[row]] for row in hits],
                "pairing": sum(dual.get(row, 0) * value
                               for row, value in column.items()),
            })
        return records

    incidence = {
        "lambda0": incident_records(tiny_dual),
        "lambda1": incident_records(induced),
        "lambda2": incident_records(next_dual),
    }
    require([(record["code"], record["multiplier"])
             for record in incidence["lambda0"]] == [(3645, "a7"), (3780, "t")]
            and [(record["code"], record["multiplier"])
                 for record in incidence["lambda1"]] == [(2919, "b7"), (3780, "t")]
            and [(record["code"], record["multiplier"])
                 for record in incidence["lambda2"]]
                == [(10, "ea"), (3270, "90"), (3780, "t"), (3790, "ea")]
            and all(record["pairing"] == 0
                    for records in incidence.values() for record in records),
            "three-dual incidence migration changed")

    # Restore the two lambda0 incidence pairs and the four lambda2 pairs.
    lambda0_pairs = [
        (unique_raw(3645, bytes.fromhex("1557")),
         unique_raw(3645, bytes.fromhex("3072"))),
        (unique_raw(3780, bytes.fromhex("0c4fcc")),
         unique_raw(3780, bytes.fromhex("3072a7"))),
    ]
    lambda0_cycles = [alternating_switch_profile(D5, *pair)
                      for pair in lambda0_pairs]
    require([record["alternating_cycle_lengths"] for record in lambda0_cycles]
            == [[6], [8]], "lambda0 C6/C8 signature changed")
    lambda2_pair_specs = [
        (10, "90", "88f4"),
        (3270, "ea", "27c0"),
        (3780, "90ea", "2790c0"),
        (3790, "90", "88f4"),
    ]
    lambda2_cycles = []
    for code, parent_row, child_row in lambda2_pair_specs:
        profile = alternating_switch_profile(
            D5, unique_raw(code, bytes.fromhex(parent_row)),
            unique_raw(code, bytes.fromhex(child_row)),
        )
        require(profile["is_one_C4_switch"],
                f"lambda2 provider {code} stopped being C4")
        lambda2_cycles.append({
            "code": code,
            "word": "".join(map(str, D5.decode_word(code))),
            "parent_normalized": parent_row,
            "child_normalized": child_row,
            "switch": profile,
        })

    # Label, but do not add, the first inverse-deletion exits of lambda2.
    sources_by_row = defaultdict(list)
    for code, polynomial in all_polynomials.items():
        for row in polynomial:
            sources_by_row[row].append(code)
    first_exits = {}
    for target_row in next_dual:
        for positions in combinations(range(len(target_row)), 2):
            multiplier = bytes(sorted(target_row[position] for position in positions))
            base = bytes(target_row[position] for position in range(len(target_row))
                         if position not in positions)
            for code in sources_by_row[base]:
                key = (code, multiplier)
                if key in first_exits:
                    continue
                full = Counter()
                for row, value in all_polynomials[code].items():
                    full[multiply(multiplier, row)] += value
                low_degree = len(target_row)
                low = {row: value for row, value in full.items()
                       if len(row) == low_degree}
                require(low == {target_row: 1},
                        "lambda2 first exit stopped being singleton at its grade")
                first_exits[key] = {
                    "hit": target_row,
                    "profile": Counter(map(len, full)),
                    "full": full,
                }
    exit_hit_histogram = Counter(record["hit"].hex()
                                 for record in first_exits.values())
    exit_profiles = Counter(tuple(sorted(record["profile"].items()))
                            for record in first_exits.values())
    require(len(first_exits) == 12
            and exit_hit_histogram == Counter({
                "2790c0": 4, "88eaf4": 6, "90ea": 2,
            })
            and exit_profiles == Counter({
                ((3, 1), (4, 6), (5, 30), (6, 68)): 10,
                ((2, 1), (4, 12), (5, 32), (6, 60)): 2,
            }), "lambda2 first-exit census changed")
    first_exit_records = []
    for (code, multiplier), record in sorted(first_exits.items()):
        first_exit_records.append({
            "code": code,
            "word": "".join(map(str, D5.decode_word(code))),
            "multiplier": multiplier.hex(),
            "hit": record["hit"].hex(),
            "profile": {str(degree): count for degree, count
                        in sorted(record["profile"].items())},
        })
    constant_exits = [record for record in first_exit_records
                      if record["hit"] == "90ea"]
    require([(record["code"], record["multiplier"])
             for record in constant_exits] == [(3780, "90ea"), (5108, "90ea")],
            "lambda2 constant-provider exits changed")

    # Resolve the finite H2/C4 diamond in the honest homogeneous degree-six
    # source block.  Every old target-rooted degree-five column is lifted by
    # one t (invisible in normalized y coordinates), while each new exit is
    # the full x^2*g column, not merely its singleton lead.  This includes the
    # complete sibling/parent tails of the four literal lambda2 providers.
    full_old_columns = {}
    for (code, multiplier), _low_column in old_columns_dict.items():
        full = Counter()
        for row, value in all_polynomials[code].items():
            lifted = row if multiplier == -1 else multiply(bytes([multiplier]), row)
            full[lifted] += value
        full_old_columns[(code, multiplier)] = {
            row: value for row, value in full.items() if value
        }
    full_exit_columns = {
        key: {row: value for row, value in record["full"].items() if value}
        for key, record in first_exits.items()
    }
    finite_columns_dict = {
        ("old", code, multiplier): column
        for (code, multiplier), column in full_old_columns.items()
    }
    finite_columns_dict.update({
        ("exit", code, multiplier.hex()): column
        for (code, multiplier), column in full_exit_columns.items()
    })
    finite_rows = tuple(sorted({row for column in finite_columns_dict.values()
                                for row in column} | set(target)))
    finite_nnz = sum(len(column) for column in finite_columns_dict.values())
    require((len(finite_rows), len(finite_columns_dict), finite_nnz)
            == (31431, 342, 35910), "finite H2/C4 block census changed")
    finite_rank_profile = {}
    for prime in (1009, 1013):
        finite_rank_profile[str(prime)] = {
            "columns": LOW.modular_rank(finite_rows, finite_columns_dict, prime),
            "with_target": LOW.modular_rank(
                finite_rows,
                {**finite_columns_dict, ("target", -1, "t"): target},
                prime,
            ),
        }
    require(set((record["columns"], record["with_target"])
                for record in finite_rank_profile.values()) == {(342, 343)},
            "finite H2/C4 target rank profile changed")

    # Every one of the twelve exits has a private full-tail row in this exact
    # finite block.  Correct lambda2 on those private rows to obtain a small
    # integral separator of the complete block, not just a modular witness.
    row_occurrence = Counter(row for column in finite_columns_dict.values()
                             for row in column)
    finite_dual = dict(next_dual)
    finite_exit_records = []
    for key, column in sorted(full_exit_columns.items()):
        hit = first_exits[key]["hit"]
        private = sorted(row for row in column if row_occurrence[row] == 1)
        require(private, "finite H2/C4 exit lost every private tail")
        chosen = private[0]
        pairing = sum(finite_dual.get(row, 0) * value
                      for row, value in column.items())
        require(column[chosen] == 1 and pairing in (-1, 1),
                "finite H2/C4 private correction changed")
        finite_dual[chosen] = -pairing
        finite_exit_records.append({
            "code": key[0],
            "word": "".join(map(str, D5.decode_word(key[0]))),
            "multiplier": key[1].hex(),
            "lead_row": hit.hex(),
            "lead_pairing_before_correction": pairing,
            "private_rows": len(private),
            "selected_private_row": chosen.hex(),
            "selected_private_coefficient": column[chosen],
            "dual_weight": finite_dual[chosen],
        })
    if mutate:
        hostile_row = bytes.fromhex(finite_exit_records[0]["selected_private_row"])
        finite_dual[hostile_row] += 1
    require(all(sum(finite_dual.get(row, 0) * value
                    for row, value in column.items()) == 0
                for column in finite_columns_dict.values())
            and sum(finite_dual.get(row, 0) * value
                    for row, value in target.items()) == 1,
            "finite H2/C4 integral separator failed")
    finite_packets = HPL.internal_response_restrictions(finite_dual)
    require(not finite_packets,
            "finite H2/C4 dual acquired a leading triangle-response packet")
    four_provider_keys = ((10, 0xea), (3270, 0x90), (3780, -1), (3790, 0xea))
    require(all(key in full_old_columns for key in four_provider_keys),
            "finite H2/C4 block omitted a sibling/parent provider")
    four_provider_records = []
    for key in four_provider_keys:
        column = full_old_columns[key]
        four_provider_records.append({
            "code": key[0],
            "word": "".join(map(str, D5.decode_word(key[0]))),
            "multiplier": "t" if key[1] == -1 else f"{key[1]:02x}",
            "full_support": len(column),
            "full_y_profile": dict(sorted(Counter(map(len, column)).items())),
        })

    if mutate:
        switch_2919["alternating_cycle_lengths"] = [4]
    require(switch_2919["alternating_cycle_lengths"] == [6],
            "hostile cycle mutation survived")

    result = {
        "format": "n8-S3-induced-switch-DGA-audit-v1",
        "status": "EXACT_FINITE_H2_C4_DIAMOND_HAS_NEXT_NONRESPONSE_COKERNEL",
        "one_page_input": {
            "old_rank": 330,
            "all14_rank": 333,
            "all14_with_target_rank": 334,
            "induced_dual": [[row.hex(), value]
                             for row, value in sorted(induced.items())],
            "target_pairing": 1,
            "internal_triangle_response_packets": 0,
        },
        "only_incident_low_columns": intersections,
        "physical_landing": {
            "code2919": {
                "word": "11000010",
                "common_multiplier": "A_36[1,0]",
                "raw_matchings": [first_2919.hex(), second_2919.hex()],
                "decoded": [decoded(D5, first_2919), decoded(D5, second_2919)],
                "switch": switch_2919,
            },
            "code3780": {
                "word": "12012000",
                "homogenizing_multiplier": "t",
                "raw_matchings": [first_3780.hex(), second_3780.hex()],
                "decoded": [decoded(D5, first_3780), decoded(D5, second_3780)],
                "switch": switch_3780,
            },
            "verdict": (
                "the induced dual is coupled by one C6 and one C8 alternating "
                "matching switch; neither is a child-parent C4 carrier Gamma_c"
            ),
        },
        "response_C4_positive_control": {
            "parent": parent.hex(),
            "children": [child_left.hex(), child_right.hex()],
            "children_switch": child_switch,
            "left_parent_switch": left_parent,
            "right_parent_switch": right_parent,
            "literal_provider_code": 3645,
            "literal_provider_word": "12000000",
            "provider_low_rows": len(provider_low),
            "guard": (
                "the literal provider contains the parent and all six C4 "
                "children together; it does not expose an individual t_c or Gamma_c"
            ),
        },
        "archived_even_cycle_theorem_guards": {
            "terminal_C6_packet": {
                "applicable": False,
                "failed_hypotheses": [
                    "the induced block contains only word 11000010, not three pure normalization channels plus all six mixed detector words",
                    "both C6 occurrences use off-diagonal decorated cells, whereas the sharp packet is assembled from three diagonal pure matchings",
                    "the C6 relation occurs inside a column multiplied by A_36[1,0], not as the six literal scalar detector rows",
                ],
                "exact_offdiagonal_cells": {
                    "first": [list(D5.COORDINATES[cell]) for cell in first_2919
                              if D5.COORDINATES[cell][2] != D5.COORDINATES[cell][3]],
                    "second": [list(D5.COORDINATES[cell]) for cell in second_2919
                               if D5.COORDINATES[cell][2] != D5.COORDINATES[cell][3]],
                },
            },
            "one_bad_E3_third_base": {
                "applicable": False,
                "failed_hypotheses": [
                    "for cap 67 the C6 occurrences contain endpoint-7 colour-zero star cells A27[00] or A37[00], violating p0=s0=0",
                    "the first C8 occurrence contains the direct edge A67[00], so the pair is not two response bases avoiding the direct edge",
                    "no five-word E2/E3 packet (t^8,d,e,0^8,1^8) or nonzero E2 minor is present in this low source block",
                ],
                "C6_endpoint7_colour0_star_cells": [
                    list(D5.COORDINATES[cell]) for cell in c6_zero_stars
                ],
                "C8_direct_edge_profile": [True, False],
            },
            "verdict": (
                "cycle length alone is insufficient: neither archived positive "
                "packet theorem applies to the induced chart26 class"
            ),
        },
        "relative_DGA_verdict": (
            "The formal relative-switch DGA is source-correct as an occurrence "
            "resolution, but its missing physical landing is load-bearing here. "
            "After all 14 first attachments the exact induced class has no "
            "triangle-response image and lands in C6/C8 sibling differences, so "
            "the archived C4 Gamma_c cannot fill it. A new physical C6/C8 exchange "
            "cell or a higher localized source chain is required."
        ),
        "second_filtered_page": {
            "row_cap": 1311,
            "old_columns": 330,
            "first_page_literal_columns": 14,
            "first_page_distinct_directions": 3,
            "new_literal_attachments": len(attachments),
            "new_attachment_hit_histogram": dict(sorted(hit_histogram.items())),
            "new_attachment_profile_each": {"y3": 1, "y4": 6, "y5": 30, "y6": 68},
            "literal_attachment_records": attachment_records,
            "rank_profile": rank_profile,
            "exact_Q_rank_reason": (
                "the two modular ranks attain the absolute column-rank caps "
                "336 and 337, while the displayed integer dual proves target separation"
            ),
            "target_membership": False,
            "induced_dual": [[row.hex(), value]
                             for row, value in sorted(next_dual.items())],
            "target_pairing": 1,
            "decoded_induced_dual": {row.hex(): decoded(D5, row)
                                     for row in sorted(next_dual)},
            "internal_triangle_response_packets": list(next_packets.values()),
            "verdict": (
                "all 13 literal lead-collision attachments span only the three "
                "new low directions. Rank rises 333->336, but the target raises "
                "it again to 337; the class persists as a new nonresponse dual"
            ),
        },
        "structural_migration_audit": {
            "dual_sequence": [
                {"label": "lambda0", "support": [[row.hex(), value]
                                                  for row, value in sorted(tiny_dual.items())],
                 "y_degree_profile": [3, 3, 3], "incident_columns": incidence["lambda0"],
                 "physical_cycle_lengths": [6, 8]},
                {"label": "lambda1", "support": [[row.hex(), value]
                                                  for row, value in sorted(induced.items())],
                 "y_degree_profile": [3, 3, 3], "incident_columns": incidence["lambda1"],
                 "physical_cycle_lengths": [6, 8]},
                {"label": "lambda2", "support": [[row.hex(), value]
                                                  for row, value in sorted(next_dual.items())],
                 "y_degree_profile": [2, 3, 3], "incident_columns": incidence["lambda2"],
                 "physical_cycle_lengths": [4, 4, 4, 4]},
            ],
            "lambda0_cycle_controls": lambda0_cycles,
            "lambda2_C4_diamond": lambda2_cycles,
            "finite_packet_entry": (
                "lambda2 has the y2 parent 90ea (an H2 term) and two y3 child "
                "directions, represented in four literal C4 provider columns"
            ),
            "lambda2_first_inverse_deletion_exits": {
                "columns": len(first_exits),
                "hit_histogram": dict(sorted(exit_hit_histogram.items())),
                "profile_species": [
                    {"profile": {str(degree): count for degree, count in profile},
                     "columns": multiplicity}
                    for profile, multiplicity in sorted(exit_profiles.items())
                ],
                "records": first_exit_records,
                "constant_provider_exits": constant_exits,
            },
            "all_page_verdict": (
                "NO fixed invariant from the first two pages supports an endless "
                "evaluation separator: at lambda2 the uniform cubic two-column "
                "C6/C8 signature breaks to mixed y2/y3 degree, four C4 columns, "
                "and two distinct first-exit profile species. The sequence enters "
                "the finite H2/two-C4 provider packet instead. This does not prove "
                "that packet is a boundary; it retires only the proposed invariant "
                "all-page migration theorem."
            ),
        },
        "finite_H2_C4_diamond_resolution": {
            "homogeneous_source_degree": 6,
            "rows": len(finite_rows),
            "columns": len(finite_columns_dict),
            "nonzeros": finite_nnz,
            "old_target_rooted_columns_lifted_by_t": len(full_old_columns),
            "new_full_exit_columns": len(full_exit_columns),
            "four_sibling_parent_providers": four_provider_records,
            "rank_profile": finite_rank_profile,
            "exact_Q_rank_reason": (
                "over both primes the source columns and source-plus-target attain "
                "their absolute column-count caps 342 and 343; the displayed "
                "integral dual independently proves target separation"
            ),
            "target_membership": False,
            "integral_dual_support": len(finite_dual),
            "integral_dual": [[row.hex(), value]
                              for row, value in sorted(finite_dual.items())],
            "target_pairing": 1,
            "exit_private_corrections": finite_exit_records,
            "leading_triangle_response_packets": list(finite_packets.values()),
            "triangle_response_scope_guard": (
                "this is the frozen associated-leading cap67/triangle012 response "
                "map: the twelve corrections are higher y-degree private tails and "
                "create no new cubic response packet; arbitrary further multiplied "
                "response modules outside this finite block are not claimed"
            ),
            "verdict": (
                "the complete finite H2/C4 diamond is not a boundary. Its 342 "
                "literal columns are independent, adjoining the target raises rank "
                "to 343, and a 15-term integral dual gives the next cokernel class "
                "without a leading triangle-response image"
            ),
        },
        "scope": (
            "the prior two y<=3 pages plus the exact 31,431-row/342-column "
            "homogeneous degree-six H2/C4 finite block containing all twelve first "
            "exits and complete sibling/parent tails of the four lambda2 providers; "
            "no claim about source columns outside this target-rooted finite block"
        ),
        "source_sha256": {str(path.relative_to(ROOT)): digest
                          for path, digest in EXPECTED.items()},
    }
    result["logical_sha256"] = sha256(json.dumps(
        result, sort_keys=True, separators=(",", ":")
    ).encode("ascii")).hexdigest()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    parser.add_argument("--mutate", action="store_true")
    arguments = parser.parse_args()
    result = audit(arguments.mutate)
    if arguments.write_results:
        RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    if arguments.check_results:
        require(RESULT.exists() and json.loads(RESULT.read_text())
                == json.loads(json.dumps(result, sort_keys=True)),
                "stored result changed")
    print(result["status"])
    print("cycles", result["physical_landing"]["code2919"]["switch"]
          ["alternating_cycle_lengths"],
          result["physical_landing"]["code3780"]["switch"]
          ["alternating_cycle_lengths"])
    print("logical", result["logical_sha256"])


if __name__ == "__main__":
    main()
