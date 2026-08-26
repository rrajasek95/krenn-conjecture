#!/usr/bin/env python3
"""Classify the 66-row transfer kernel S3 by physical edge skeleton."""

from collections import Counter, defaultdict
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / "computations" / "verify_n8_normalized_critical_contraction.py"
KERNELS = HERE / "direct_fh_transfer_kernels.txt"
PACKET = HERE / "s3_physical_skeleton.txt"
RESULTS = HERE / "results_s3_physical_skeleton.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


spec = importlib.util.spec_from_file_location("n8_normalized", SOURCE)
NORM = importlib.util.module_from_spec(spec)
require(spec.loader is not None, "cannot load source")
spec.loader.exec_module(NORM)
D5 = NORM.D5


def s3_rows():
    active = False
    answer = []
    for line in KERNELS.read_text(encoding="ascii").splitlines():
        fields = line.split()
        if fields[:2] == ["BEGIN", "S3"]:
            active = True
        elif fields[:2] == ["END", "S3"]:
            active = False
        elif active and fields[0] == "ROW":
            answer.append((bytes.fromhex(fields[1]), int(fields[2])))
    require(len(answer) == 66, "S3 support changed")
    return answer


def skeleton(row):
    return tuple(sorted(D5.COORDINATES[cell][:2] for cell in row))


def skeleton_type(edges):
    degrees = Counter(vertex for edge in edges for vertex in edge)
    profile = sorted(degrees.values(), reverse=True)
    if profile == [1] * 6:
        return "3P2"
    if profile == [2, 1, 1, 1, 1]:
        return "P3+P2"
    if profile == [2, 2, 1, 1]:
        return "P4"
    raise RuntimeError(f"unexpected physical skeleton {edges}")


def word_label(code):
    return "".join(map(str, D5.decode_word(code)))


def main():
    rows = s3_rows()
    literal_cubics = defaultdict(list)
    for code in range(3 ** 8):
        if len(set(D5.decode_word(code))) == 1:
            continue
        for literal in D5.iter_word_terms(code):
            normalized = bytes(sorted(cell for cell in literal if D5.IS_OFF_SUPPORT[cell]))
            if len(normalized) == 3:
                literal_cubics[normalized].append(code)

    lines = [
        "KRENN_N8_DIRECT_FH_S3_PHYSICAL_SKELETON_V1",
        "COORDINATE_ENCODING byte=id in lex (edge i<j, ordered colours a,b); monomial=sorted bytes hex",
        "CLASS 3P2=three_disjoint_edges P3+P2=two-edge-path_plus_edge P4=three-edge-path",
    ]
    profile = Counter()
    literal_profile = Counter()
    skeletons = defaultdict(list)
    for row, coefficient in rows:
        physical = skeleton(row)
        kind = skeleton_type(physical)
        witnesses = sorted(set(literal_cubics.get(row, ())))
        profile[kind] += 1
        literal_profile[(kind, bool(witnesses))] += 1
        skeletons[physical].append(row)
        witness_text = ",".join(f"{code}:{word_label(code)}" for code in witnesses) or "-"
        lines.append(
            f"ROW {row.hex()} {coefficient} TYPE={kind} "
            f"EDGES={','.join(f'{i}{j}' for i, j in physical)} LITERAL={int(bool(witnesses))} "
            f"WITNESS={witness_text}"
        )
    PACKET.write_text("\n".join(lines) + "\n", encoding="ascii")

    require(profile == Counter({"3P2": 28, "P3+P2": 28, "P4": 10}),
            "S3 physical profile changed")
    require(literal_profile == Counter({("3P2", True): 14, ("3P2", False): 14,
                                        ("P3+P2", False): 28, ("P4", False): 10}),
            "literal cubic profile changed")
    require(len(skeletons) == 65 and Counter(map(len, skeletons.values())) == Counter({1: 64, 2: 1}),
            "physical skeleton collision profile changed")
    result = {
        "format": "n8-direct-Fh-S3-physical-skeleton-v1",
        "status": "EXACT_LITERAL_CENSUS",
        "rows": len(rows),
        "distinct_physical_skeletons": len(skeletons),
        "physical_type_counts": dict(sorted(profile.items())),
        "literal_generator_cubic_counts": {
            "3P2_literal": 14,
            "3P2_nonliteral_endpoint_colour_collision": 14,
            "P3+P2_nonliteral_physical_collision": 28,
            "P4_nonliteral_physical_collision": 10,
        },
        "coefficient_guard": {
            "literal": dict(sorted(Counter(coefficient for row, coefficient in rows
                                             if row in literal_cubics).items())),
            "nonliteral": dict(sorted(Counter(coefficient for row, coefficient in rows
                                                if row not in literal_cubics).items())),
        },
        "interpretation": (
            "only 14 of the 28 matching-skeleton rows are literal normalized Hafnian terms; "
            "the other 14 fail endpoint-colour compatibility, and every nonmatching row is "
            "necessarily a product/collision term rather than a single source term"
        ),
        "packet": str(PACKET.relative_to(ROOT)),
        "packet_sha256": sha256(PACKET.read_bytes()).hexdigest(),
        "kernel_packet_sha256": sha256(KERNELS.read_bytes()).hexdigest(),
        "source_sha256": sha256(SOURCE.read_bytes()).hexdigest(),
    }
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    RESULTS.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("S3 physical skeleton audit: PASS")
    print("types:", dict(profile), "literal matching:", literal_profile[("3P2", True)])
    print("logical sha256:", result["logical_sha256"])


if __name__ == "__main__":
    main()
