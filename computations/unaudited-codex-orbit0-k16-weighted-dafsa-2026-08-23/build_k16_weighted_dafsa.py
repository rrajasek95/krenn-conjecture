#!/usr/bin/env python3
"""Build an exact weighted DAFSA for the collected orbit-zero K16 residual.

Keys are the 24 nondecreasing cell identifiers of each literal H-orbit
representative.  Terminal values are the exact rational orbit masses.  The
incremental minimizer consumes the already-sorted frozen JSON stream and
merges states iff their level, terminal value, and complete labelled suffix
map agree.
"""

from collections import Counter
from hashlib import sha256
import argparse
import importlib.util
import json
from pathlib import Path
import struct


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
INPUT = (ROOT / "computations/unaudited-codex-orbit0-k16-literal-collection-2026-08-22"
         / "results_orbit0_k16_literal_residual.json")
K14_SOURCE = (ROOT / "computations/unaudited-codex-orbit0-k14-interface-audit-2026-08-21"
              / "audit_orbit0_k14_interface.py")
BINARY = HERE / "weighted_k16_literal_orbits.dafsa"
RESULT = HERE / "results_k16_weighted_dafsa.json"

INPUT_SHA = "28a648a2625d208cc86948b27a06f52f38245fe2ebe130c583e619d1d24b9189"
STREAM_SHA = "f92c91ad239f112185b29ec53157bfb02931b06bf481d71e3878b2c31e298328"
KEY_COUNT = 1_848_174
KEY_LENGTH = 24
MAGIC = b"K16WDAFSA1\0\0\0\0\0\0"
HEADER = struct.Struct("<16sIIQQQQ32s32s")
NODE = struct.Struct("<BBHqq")
EDGE = struct.Struct("<BI")

EXPECTED_SAMPLES = {
    1: ("09090d0d1821484c4c5160627d96c3cacacee0e3f3f7f7fb", -384, 1),
    2: ("09090d0d1821484c4c5160627d98c5cacacedee1f3f7f7fb", 384, 1),
    1024: ("09090d0d212248484c5f606a7d8ec2c4c6caced7f3f3f7fb", 384, 1),
    924087: ("09161c2a32344857646f7173797d7d8793a2caceceeef3fb", -384, 1),
    1848174: ("212c2e30373b596064686d6f75797d7d7f8aa5accacef3fb", -384, 1),
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def file_sha256(path):
    digest = sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, f"cannot load {path}")
    spec.loader.exec_module(module)
    return module


def literal_records(path):
    """Stream `(row, numerator, denominator)` without loading the 160 MB JSON."""
    inside = False
    row = None
    numerator = None
    with path.open() as handle:
        for line in handle:
            if not inside:
                if line.startswith('  "literal_orbits": ['):
                    inside = True
                continue
            if line == "  ],\n":
                break
            token = line.strip().rstrip(",")
            if row is None:
                if len(token) == 50 and token[0] == token[-1] == '"':
                    row = bytes.fromhex(token[1:-1])
            elif numerator is None:
                numerator = int(token)
            else:
                denominator = int(token)
                yield row, numerator, denominator
                row = None
                numerator = None
    require(inside and row is None and numerator is None,
            "literal-orbit stream ended mid-record")


class MutableState:
    __slots__ = ("depth", "edges", "final")

    def __init__(self, depth):
        self.depth = depth
        self.edges = {}
        self.final = None


def build(binary_path):
    root = MutableState(0)
    unchecked = []
    previous = b""
    registry = {}
    node_count = 0
    arc_count = 0
    node_language_counts = []
    depth_histogram = Counter()
    input_digest = sha256()
    trie_nodes = 1
    samples = {}
    record_count = 0

    with binary_path.open("w+b") as output:
        output.write(b"\0" * HEADER.size)

        def minimize(down_to):
            nonlocal node_count, arc_count
            for _index in range(len(unchecked) - 1, down_to - 1, -1):
                parent, label, child = unchecked.pop()
                edges = tuple(sorted(child.edges.items()))
                signature = (child.depth, child.final, edges)
                identifier = registry.get(signature)
                if identifier is None:
                    identifier = node_count
                    node_count += 1
                    registry[signature] = identifier
                    depth_histogram[child.depth] += 1
                    arc_count += len(edges)
                    final = child.final
                    numerator, denominator = (final if final is not None else (0, 0))
                    output.write(NODE.pack(child.depth, int(final is not None),
                                           len(edges), numerator, denominator))
                    language_count = int(final is not None)
                    for edge_label, target in edges:
                        require(target < identifier, "DAFSA lost bottom-up order")
                        output.write(EDGE.pack(edge_label, target))
                        language_count += node_language_counts[target]
                    node_language_counts.append(language_count)
                parent.edges[label] = identifier

        for record_count, (row, numerator, denominator) in enumerate(
                literal_records(INPUT), 1):
            require(len(row) == KEY_LENGTH
                    and all(left <= right for left, right in zip(row, row[1:])),
                    f"bad sorted key at {record_count}")
            require(not previous or previous < row,
                    f"literal keys lost strict order at {record_count}")
            common = 0
            while common < KEY_LENGTH and previous and row[common] == previous[common]:
                common += 1
            minimize(common)
            trie_nodes += KEY_LENGTH - common
            parent = root if common == 0 else unchecked[-1][2]
            for depth, label in enumerate(row[common:], common + 1):
                child = MutableState(depth)
                parent.edges[label] = child
                unchecked.append((parent, label, child))
                parent = child
            parent.final = (numerator, denominator)
            previous = row
            input_digest.update(row)
            input_digest.update(numerator.to_bytes(8, "little", signed=True))
            input_digest.update(denominator.to_bytes(8, "little", signed=True))
            if record_count in EXPECTED_SAMPLES:
                samples[record_count] = (row.hex(), numerator, denominator)

        minimize(0)
        root_edges = tuple(sorted(root.edges.items()))
        root_signature = (0, root.final, root_edges)
        root_identifier = registry.get(root_signature)
        if root_identifier is None:
            root_identifier = node_count
            node_count += 1
            registry[root_signature] = root_identifier
            depth_histogram[0] += 1
            arc_count += len(root_edges)
            output.write(NODE.pack(0, 0, len(root_edges), 0, 0))
            language_count = 0
            for label, target in root_edges:
                require(target < root_identifier, "root lost bottom-up order")
                output.write(EDGE.pack(label, target))
                language_count += node_language_counts[target]
            node_language_counts.append(language_count)

        stream_digest = input_digest.digest()
        require(record_count == KEY_COUNT and trie_nodes == 17_606_956,
                (record_count, trie_nodes))
        require(input_digest.hexdigest() == STREAM_SHA, "literal stream digest changed")
        require(samples == EXPECTED_SAMPLES, "stream sample replay changed")
        require(node_language_counts[root_identifier] == KEY_COUNT,
                "root language count changed")
        require(node_count == 768820 and arc_count == 1192523
                and root_identifier == 768819,
                (node_count, arc_count, root_identifier))

        output.seek(0)
        output.write(HEADER.pack(
            MAGIC, 1, KEY_LENGTH, node_count, arc_count, root_identifier,
            record_count, stream_digest, bytes.fromhex(INPUT_SHA)
        ))

    return {
        "keys": record_count,
        "ordinary_trie_nodes": trie_nodes,
        "minimal_dafsa_nodes": node_count,
        "minimal_dafsa_arcs": arc_count,
        "root_id": root_identifier,
        "accepted_keys_from_root": node_language_counts[root_identifier],
        "nodes_by_depth": {str(key): depth_histogram[key]
                           for key in sorted(depth_histogram)},
        "literal_stream_sha256": input_digest.hexdigest(),
        "samples": {str(key): list(samples[key]) for key in sorted(samples)},
    }


def binary_index(path):
    offsets = []
    with path.open("rb") as handle:
        raw = handle.read(HEADER.size)
        require(len(raw) == HEADER.size, "short DAFSA header")
        header = HEADER.unpack(raw)
        magic, version, key_length, nodes, arcs, root, keys, stream, input_sha = header
        require(magic == MAGIC and version == 1 and key_length == KEY_LENGTH
                and nodes == 768820 and arcs == 1192523 and root == 768819
                and keys == KEY_COUNT and stream.hex() == STREAM_SHA
                and input_sha.hex() == INPUT_SHA,
                "DAFSA header changed")
        for _identifier in range(nodes):
            offsets.append(handle.tell())
            record = handle.read(NODE.size)
            require(len(record) == NODE.size, "short DAFSA node")
            _depth, _flags, degree, _numerator, _denominator = NODE.unpack(record)
            handle.seek(degree * EDGE.size, 1)
        require(handle.read(1) == b"", "trailing DAFSA bytes")
    return offsets, header


def query(path, offsets, root, key):
    identifier = root
    with path.open("rb") as handle:
        for expected_depth, label in enumerate(key, 1):
            handle.seek(offsets[identifier])
            depth, flags, degree, numerator, denominator = NODE.unpack(
                handle.read(NODE.size)
            )
            require(depth == expected_depth - 1 and not flags,
                    "query encountered a premature terminal")
            target = None
            for _ in range(degree):
                edge_label, child = EDGE.unpack(handle.read(EDGE.size))
                if edge_label == label:
                    target = child
            if target is None:
                return None
            identifier = target
        handle.seek(offsets[identifier])
        depth, flags, degree, numerator, denominator = NODE.unpack(
            handle.read(NODE.size)
        )
        require(depth == KEY_LENGTH and degree == 0, "terminal shape changed")
        return (numerator, denominator) if flags else None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mutate", action="store_true",
                        help="hostile mutation of the first streamed sample")
    args = parser.parse_args()

    require(file_sha256(INPUT) == INPUT_SHA, "frozen literal residual changed")
    if args.mutate:
        actual = next(literal_records(INPUT))
        hostile = (actual[0], actual[1] + 1, actual[2])
        require((hostile[0].hex(), hostile[1], hostile[2]) == EXPECTED_SAMPLES[1],
                "hostile terminal-weight mutation fired")

    census = build(BINARY)
    offsets, header = binary_index(BINARY)
    root = header[5]
    sample_queries = {}
    for index, (row_hex, numerator, denominator) in EXPECTED_SAMPLES.items():
        value = query(BINARY, offsets, root, bytes.fromhex(row_hex))
        require(value == (numerator, denominator), f"sample query {index} failed")
        sample_queries[str(index)] = [row_hex, numerator, denominator]
    hostile_key = bytes.fromhex(EXPECTED_SAMPLES[1][0])[:-1] + bytes([250])
    require(query(BINARY, offsets, root, hostile_key) is None,
            "hostile absent-key query unexpectedly landed")

    K14 = load("orbit0_k16_dafsa_k14", K14_SOURCE)
    F = K14.FROZEN
    three_words = tuple(F.word_from_pair_colours(row) for row in F.PAIR_COLOURS)
    three_anchors = tuple(F.BASE.term_ids(word, F.M0) for word in three_words)
    factor_set = frozenset(three_anchors)
    factor_stabilizer = tuple(
        action for action in range(len(F.EXPORT.STABILIZER))
        if frozenset(F.move_row(term, action) for term in three_anchors) == factor_set
    )
    require(len(factor_stabilizer) == 384, "factor stabilizer changed")
    orbit_sizes = {}
    labelled_coefficients = {}
    for index, (row_hex, numerator, denominator) in EXPECTED_SAMPLES.items():
        row = bytes.fromhex(row_hex)
        orbit_size = len({F.move_row(row, action) for action in factor_stabilizer})
        orbit_sizes[str(index)] = orbit_size
        labelled_coefficients[str(index)] = [numerator, denominator * orbit_size]

    payload = {
        "format": "n8-orbit0-k16-weighted-dafsa-v1",
        "status": "EXACT_COMPACT_PROVENANCE_PRESERVING_WEIGHTED_DAFSA",
        "input": {
            "literal_H_orbits": KEY_COUNT,
            "labelled_support": 701717184,
            "input_file_sha256": INPUT_SHA,
            "literal_stream_sha256": STREAM_SHA,
            "key_length": KEY_LENGTH,
            "alphabet": "252 ordered literal cell identifiers, repetitions retained",
        },
        "decision_diagram": {
            **census,
            "binary_file": BINARY.name,
            "binary_file_bytes": BINARY.stat().st_size,
            "binary_file_sha256": file_sha256(BINARY),
            "node_compression_ratio_from_trie": [17606956, 768820],
            "root_language_count_replay": KEY_COUNT,
            "terminal_value": "exact rational H-orbit coefficient mass",
            "merge_rule": (
                "same depth, same rational terminal value, and identical complete "
                "label-to-child suffix map"
            ),
        },
        "query_replay": {
            "samples": sample_queries,
            "sample_H_orbit_sizes": orbit_sizes,
            "sample_labelled_coefficients": labelled_coefficients,
            "hostile_absent_key_returns_none": True,
        },
        "literal_source_incidence": {
            "local_application": True,
            "column_query": (
                "For a literal degree-24 source column (word,U), generate its 105 "
                "perfect-matching outputs and query each 24-label key in O(24)."
            ),
            "inverse_query": (
                "A constrained DAG traversal can select residual keys containing "
                "a specified four-cell perfect-matching term as a submultiset; "
                "subtracting that term yields the exact multiplier U."
            ),
            "orbit_mass_guard": (
                "Stored terminal values are H-orbit masses. Divide by the exact "
                "384-action orbit size before literal coefficient arithmetic, or "
                "work consistently in the orbit-mass basis."
            ),
            "limitation": (
                "The DAG stores the collected K16 residual support, not zero-residual "
                "K16 rows or K12-K15 rows. A sound lower-kernel closure still needs "
                "the literal source provider alongside the DAG; the DAG is a compact "
                "target/coefficient oracle, not the full Macaulay matrix."
            ),
        },
        "scope_guard": (
            "Exact compression of the one frozen canonical H-equivariant orbit-zero "
            "K16 residual. It is not pivot-independent, does not decide membership "
            "or localization, and does not cover the other 30 charts."
        ),
        "pinned": {
            str(INPUT.relative_to(ROOT)): INPUT_SHA,
            str(K14_SOURCE.relative_to(ROOT)): file_sha256(K14_SOURCE),
        },
        "source_sha256": file_sha256(Path(__file__)),
    }
    logical = dict(payload)
    logical.pop("source_sha256")
    payload["logical_sha256"] = sha256(
        json.dumps(logical, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    RESULT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("PASS", payload["logical_sha256"], BINARY.stat().st_size)


if __name__ == "__main__":
    main()
