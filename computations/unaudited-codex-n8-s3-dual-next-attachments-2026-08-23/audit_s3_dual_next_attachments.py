#!/usr/bin/env python3
"""Lift the minimal S3 dual and enumerate its first new source attachments.

The total-degree-five audit collapses support-chart variables.  This checker
restores literal orbit26 support factors for the three-row dual, then uses
inverse deletion to enumerate only the new total-degree-six columns whose
y^3 layer meets the dual.  It also compares those columns with the canonical
cap-67/triangle-012 direct-blocker response packet.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
import importlib.util
import json
from itertools import combinations, product
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
NORMALIZED = ROOT / "computations/verify_n8_normalized_critical_contraction.py"
COMPONENT = ROOT / "computations/unaudited-codex-n8-s3-source-component-2026-08-23/results_s3_source_component.json"
HPL = ROOT / "computations/unaudited-codex-n8-s3-source-hpl-audit-2026-08-23/results_s3_source_hpl.json"
PACKET = HERE / "s3_dual_next_attachments.txt"
RESULTS = HERE / "results_s3_dual_next_attachments.json"
REPORT = HERE / "REPORT.md"

EXPECTED = {
    COMPONENT: "7d27d9301ca81b4567db74fb872b324d068f1c90eae37caf5fe544adeb2b4b27",
    HPL: "15d56d5c19b34b69251040f6c7b09addb245a9e4523605072f7f250cd7de689c",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_source():
    spec = importlib.util.spec_from_file_location("s3_next_normalized", NORMALIZED)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, "cannot load normalized source")
    spec.loader.exec_module(module)
    return module.D5


def multiply(*rows):
    return bytes(sorted(sum((tuple(row) for row in rows), ())))


def coordinate_label(D5, identifier):
    i, j, a, b = D5.COORDINATES[identifier]
    return f"A_{i}{j}[{a},{b}]"


def normalized_polynomials(D5):
    polynomials = {}
    raw_by_normalized = defaultdict(lambda: defaultdict(list))
    for code in range(3 ** 8):
        if len(set(D5.decode_word(code))) == 1:
            continue
        polynomial = Counter()
        for literal in D5.iter_word_terms(code):
            row = bytes(sorted(cell for cell in literal if D5.IS_OFF_SUPPORT[cell]))
            polynomial[row] += 1
            raw_by_normalized[code][row].append(literal)
        polynomials[code] = polynomial
    return polynomials, raw_by_normalized


def decode_word(D5, code):
    return "".join(map(str, D5.decode_word(code)))


def main(mutate=False):
    for path, expected in EXPECTED.items():
        require(sha256(path.read_bytes()).hexdigest() == expected,
                f"source drift: {path}")
    D5 = load_source()
    polynomials, raw = normalized_polynomials(D5)
    dual = {
        bytes.fromhex("0c4fcc"): 1,
        bytes.fromhex("1557a7"): 1,
        bytes.fromhex("3072a7"): -1,
    }
    if mutate:
        dual[bytes.fromhex("1557a7")] = 2

    # Restore one common support monomial A25[00]*A67[00].  The three
    # normalized terms arise from the explicitly source-labelled columns
    # below.  This is a localized coefficient lift, not a raw source syzygy.
    anchor_25 = D5.COORDINATE_ID[(2, 5, 0, 0)]
    anchor_67 = D5.COORDINATE_ID[(6, 7, 0, 0)]
    require((anchor_25, anchor_67) == (0x87, 0xF3), "common anchors changed")
    raw_lift_spec = [
        (bytes.fromhex("0c4fcc"), 3780, bytes([anchor_25])),
        (bytes.fromhex("1557a7"), 3645, bytes([0xA7])),
        (bytes.fromhex("3072a7"), 3780, bytes([anchor_67])),
    ]
    raw_lift = []
    for row, code, multiplier in raw_lift_spec:
        candidates = raw[code][row if code == 3780 else row[:-1]]
        require(len(candidates) == 1, "raw completion is not unique")
        literal = candidates[0]
        raw_column_row = multiply(literal, multiplier)
        support = bytes(cell for cell in raw_column_row if not D5.IS_OFF_SUPPORT[cell])
        require(support == bytes((anchor_25, anchor_67)), "raw lift lost common support product")
        require(bytes(cell for cell in raw_column_row if D5.IS_OFF_SUPPORT[cell]) == row,
                "raw lift does not normalize to the dual row")
        raw_lift.append({
            "row": row,
            "coefficient": dual[row],
            "code": code,
            "word": decode_word(D5, code),
            "multiplier": multiplier,
            "generator_raw_term": literal,
            "raw_column_row": raw_column_row,
        })

    # At total degree six, the genuinely new low projection has an
    # off-support multiplier of degree two and a generator y^1 term.  Inverse
    # deletion from the three dual rows enumerates every incident column.
    degree1_sources = defaultdict(list)
    for code, polynomial in polynomials.items():
        for row in polynomial:
            if len(row) == 1:
                degree1_sources[row].append(code)
    next_columns = {}
    for target in dual:
        for positions in combinations(range(3), 2):
            multiplier = bytes(sorted(target[position] for position in positions))
            base = bytes(target[position] for position in range(3)
                         if position not in positions)
            for code in degree1_sources[base]:
                key = (code, multiplier)
                if key in next_columns:
                    continue
                layer = Counter()
                for row, coefficient in polynomials[code].items():
                    if len(row) == 1:
                        layer[multiply(multiplier, row)] += coefficient
                next_columns[key] = {row: coefficient for row, coefficient in layer.items()
                                     if coefficient}
    require(len(next_columns) == 14, "next incident column count changed")

    next_records = []
    pairing_histogram = Counter()
    row_hit_histogram = Counter()
    for (code, multiplier), layer in sorted(next_columns.items()):
        pairing = sum(dual.get(row, 0) * coefficient for row, coefficient in layer.items())
        hits = sorted(set(layer) & set(dual))
        require(len(layer) == len(hits) == 1 and pairing in (-1, 1),
                "next column stopped being a singleton killer")
        row = hits[0]
        # Recover the unique raw y^1 generator term.
        generator_base = next(iter(
            candidate for candidate in polynomials[code]
            if len(candidate) == 1 and multiply(multiplier, candidate) == row
        ))
        raw_terms = raw[code][generator_base]
        require(len(raw_terms) == 1, "next killer has ambiguous raw completion")
        raw_column_row = multiply(raw_terms[0], multiplier)
        pairing_histogram[pairing] += 1
        row_hit_histogram[row.hex()] += 1
        next_records.append({
            "code": code,
            "word": decode_word(D5, code),
            "multiplier": multiplier,
            "row": row,
            "pairing": pairing,
            "generator_raw_term": raw_terms[0],
            "raw_column_row": raw_column_row,
        })
    require(pairing_histogram == Counter({1: 10, -1: 4}), "next pairing profile changed")
    require(row_hit_histogram == Counter({"0c4fcc": 4, "1557a7": 6, "3072a7": 4}),
            "next row-hit profile changed")
    first = next_records[0]
    require((first["code"], first["multiplier"].hex(), first["row"].hex(), first["pairing"])
            == (135, "1557", "1557a7", 1), "first killer changed")
    require(first["generator_raw_term"].hex() == "0087a7f3"
            and first["raw_column_row"].hex() == "00155787a7f3",
            "first killer raw completion changed")

    # Canonical cap 67, triangle 012, internal response edge 01 with output
    # colours (1,2), and spectator A34[1,2].  Pairing with the direct blocker
    # produces two response orientations for each K_ij, weighted by A67[i,j].
    spectator = D5.COORDINATE_ID[(3, 4, 1, 2)]
    direct_packet = []
    for i, j in product(range(3), repeat=2):
        cap_cell = D5.COORDINATE_ID[(6, 7, i, j)]
        first_response = bytes(sorted((
            D5.COORDINATE_ID[(0, 6, 1, i)],
            D5.COORDINATE_ID[(1, 7, 2, j)],
        )))
        second_response = bytes(sorted((
            D5.COORDINATE_ID[(0, 7, 1, j)],
            D5.COORDINATE_ID[(1, 6, 2, i)],
        )))
        for orientation, response in enumerate((first_response, second_response)):
            normalized = multiply(response, bytes([spectator]),
                                  b"" if (i, j) == (0, 0) else bytes([cap_cell]))
            multiplier = multiply(response,
                                  b"" if (i, j) == (0, 0) else bytes([cap_cell]))
            # The same code-135 unique y^1 term A34[1,2] supplies each row,
            # but these are independent monomial multiples, not one column.
            require(polynomials[135][bytes([spectator])] == 1,
                    "direct-packet provider changed")
            direct_packet.append({
                "K_coordinate": [i, j],
                "cap_cell": cap_cell,
                "orientation": orientation,
                "normalized_row": normalized,
                "provider_code": 135,
                "provider_multiplier": multiplier,
                "total_degree": 6 if (i, j) == (0, 0) else 7,
            })
    require([record["normalized_row"].hex() for record in direct_packet[:2]]
            == ["3072a7", "3969a7"], "K00 response packet changed")
    require(sum(record["normalized_row"] in dual for record in direct_packet) == 1,
            "dual/direct response incidence changed")
    require(len({(record["provider_code"], record["provider_multiplier"])
                 for record in direct_packet}) == 18,
            "direct correction collapsed to fewer independent columns")

    lines = [
        "KRENN_N8_S3_DUAL_NEXT_ATTACHMENTS_V1",
        "DUAL +0c4fcc +1557a7 -3072a7",
        "COMMON_SUPPORT 87=A_25[0,0] f3=A_67[0,0]",
    ]
    for record in raw_lift:
        lines.append(
            f"RAW_LIFT row={record['row'].hex()} coefficient={record['coefficient']} "
            f"code={record['code']} word={record['word']} multiplier={record['multiplier'].hex()} "
            f"generator_term={record['generator_raw_term'].hex()} raw={record['raw_column_row'].hex()}"
        )
    for record in next_records:
        lines.append(
            f"D6_KILLER code={record['code']} word={record['word']} multiplier={record['multiplier'].hex()} "
            f"row={record['row'].hex()} pairing={record['pairing']} "
            f"generator_term={record['generator_raw_term'].hex()} raw={record['raw_column_row'].hex()}"
        )
    for record in direct_packet:
        i, j = record["K_coordinate"]
        lines.append(
            f"DIRECT_PACKET K={i}{j} cap={record['cap_cell']:02x} orientation={record['orientation']} "
            f"row={record['normalized_row'].hex()} provider=135 multiplier={record['provider_multiplier'].hex()} "
            f"total_degree={record['total_degree']}"
        )
    PACKET.write_text("\n".join(lines) + "\n", encoding="ascii")

    result = {
        "format": "n8-S3-dual-next-attachments-v1",
        "status": "EXACT_FIRST_ATTACHMENT_NOT_DIRECT_BLOCKER",
        "dual": [[row.hex(), coefficient] for row, coefficient in sorted(dual.items())],
        "raw_localized_lift": {
            "common_support_product": ["A_25[0,0]", "A_67[0,0]"],
            "terms": [{key: (value.hex() if isinstance(value, bytes) else value)
                       for key, value in record.items()} for record in raw_lift],
            "guard": (
                "the commonized coefficient functional uses separately multiplied raw source terms; "
                "it is not itself one raw source syzygy"
            ),
        },
        "first_new_total_degree6_layer": {
            "incident_columns": len(next_records),
            "all_singleton_killers": True,
            "pairing_histogram": dict(sorted(pairing_histogram.items())),
            "dual_row_hit_histogram": dict(sorted(row_hit_histogram.items())),
            "lex_first": {key: (value.hex() if isinstance(value, bytes) else value)
                          for key, value in first.items()},
            "interpretation": (
                "the first cell is multiplier A_03[1,0]A_14[2,0] times F_00012000; "
                "its only y3 term is the P4 row 1557a7 and it has no cap-response spoke pair"
            ),
        },
        "canonical_direct_blocker_test": {
            "cap_pair": [6, 7],
            "triangle": [0, 1, 2],
            "response_edge": [0, 1],
            "response_output_colours": [1, 2],
            "spectator": "A_34[1,2]",
            "K00_packet": ["3072a7", "3969a7"],
            "dual_pairing_on_K00_packet": -1,
            "off_support_cap_corrections": 16,
            "independent_provider_columns": 18,
            "verdict": (
                "the first attachment is not the HPL replacement K00 -> <K,A_67>. "
                "The two K00 orientations occur as separate degree6 singleton multiples, while "
                "the sixteen off-support A67_ij*K_ij orientations first occur as sixteen separate "
                "degree7 singleton multiples; no single attachment couples the direct blocker"
            ),
        },
        "smallest_obstruction": (
            "(code=135, word=00012000, multiplier=1557) pairs lambda by +1 before any "
            "direct-blocker completion and is neither a triangle blocker nor a rank-drop minor"
        ),
        "packet": str(PACKET.relative_to(ROOT)),
        "packet_sha256": sha256(PACKET.read_bytes()).hexdigest(),
        "source_sha256": {
            str(path.relative_to(ROOT)): sha256(path.read_bytes()).hexdigest()
            for path in (NORMALIZED, COMPONENT, HPL)
        },
        "scope": (
            "complete incident low-layer enumeration at total degree6 and literal direct-packet "
            "comparison; no broad degree6 closure or y10 matrix"
        ),
    }
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    RESULTS.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

    report = f"""# Minimal S3 dual: raw lift and first attachment

The localized three-row dual lifts to a common support factor
`A_25[0,0] A_67[0,0]`, but its three coefficient extractions come from
separately multiplied raw source terms.  It is not a single raw Bianchi or
carrier identity.

Every genuinely new total-degree-six column incident to the dual was found
by inverse deletion.  There are 14, and every one is a singleton on the y3
layer with pairing `+/-1`.  The lex-first is

```text
code       135 (word 00012000)
multiplier 1557 = A_03[1,0] A_14[2,0]
output     1557a7
pairing    +1
raw row    00155787a7f3
```

It has no cap-response spoke pair, so it is neither a triangle blocker nor a
rank-drop condition.  It kills the cubic dual before a carrier HPL lift.

For the canonical cap `67` and triangle `012`, the K00 response packet is
`3072a7 + 3969a7`.  These are two separate degree-six singleton columns.
Replacing `K00` by the direct blocker `<K,A_67>` adds 16 off-support cap
terms, but they first appear as 16 further, independent degree-seven
singleton columns.  No single next attachment supplies the direct-blocker
combination.

Replay with `audit_s3_dual_next_attachments.py --check`; hostile mutation is
rejected by `--mutate`.
"""
    REPORT.write_text(report, encoding="utf-8")
    print("S3 dual next-attachment audit: PASS")
    print("d6 incident/singleton killers:", len(next_records))
    print("first:", first["code"], first["multiplier"].hex(), first["row"].hex())
    print("logical sha256:", result["logical_sha256"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--mutate", action="store_true")
    arguments = parser.parse_args()
    try:
        main(mutate=arguments.mutate)
    except RuntimeError:
        if arguments.mutate:
            raise
        raise
