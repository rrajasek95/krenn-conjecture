#!/usr/bin/env python3
"""Export the exact N8 normalized degree-seven DFS roots and word packet.

This is an input exporter only.  It reconstructs the frozen six-column
critical contraction, clears its common denominator two, and closes the
literal closure22 plus five contraction words under the exact order-four
support stabilizer.  It performs no DFS or span calculation.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
NORMALIZED = ROOT / "computations/verify_n8_normalized_critical_contraction.py"
CLOSURE = (
    ROOT
    / "computations/unaudited-codex-rootless-fine-macaulay-2026-08-22"
    / "results_second_order_lift_support.json"
)
SEED = HERE / "degree7_tail_seed.txt"
WORDS = HERE / "degree7_word_packet.txt"
ALL_WORDS = HERE / "degree7_all_mixed_words.txt"
RESULTS = HERE / "results_degree7_inputs.json"

EXPECTED_NORMALIZED_SHA256 = (
    "4e2ce4b12626edaedd9a8a5a4a9635ab5c74a5f139ecf52507018ca5478acd62"
)
EXPECTED_CLOSURE_SHA256 = (
    "343b5f531d6303b2d651123a8a5e4f1653b060cb6f7f66bc61cbd22b7fa4d10d"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_normalized():
    require(sha256(NORMALIZED.read_bytes()).hexdigest() == EXPECTED_NORMALIZED_SHA256,
            "normalized contraction checker digest changed")
    spec = importlib.util.spec_from_file_location("n8_normalized", NORMALIZED)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def word_label(module, code):
    return "".join(map(str, module.D5.decode_word(code)))


def orbit(module, code):
    return {transform[code] for transform in module.D5.WORD_TRANSFORMS}


def build():
    module = load_normalized()
    require(sha256(CLOSURE.read_bytes()).hexdigest() == EXPECTED_CLOSURE_SHA256,
            "closure22 manifest digest changed")

    polynomials = {
        code: module.normalized_generator(code)
        for code in range(3 ** 8)
        if len(set(module.D5.decode_word(code))) > 1
    }
    image = defaultdict(Fraction)
    for scalar, code, multiplier in module.CONTRACTION:
        for row, coefficient in module.invariant_column_image(
                (code, multiplier), polynomials).items():
            image[row] += scalar * coefficient
    image = {row: value for row, value in image.items() if value}
    require(image.pop(b"") == 1, "contraction constant changed")
    require(len(image) == 564, "tail orbit count changed")
    require(Counter(map(len, image))
            == Counter({2: 6, 3: 16, 4: 48, 5: 104, 6: 254, 7: 136}),
            "tail degree histogram changed")
    require(Counter(image.values())
            == Counter({Fraction(-1): 4, Fraction(-1, 2): 512,
                        Fraction(1, 2): 48}),
            "tail coefficient histogram changed")

    closure_labels = json.loads(CLOSURE.read_text())["combined_closure_words"]
    closure_codes = {
        module.D5.word_code(tuple(map(int, label)))
        for label in closure_labels
    }
    contraction_codes = {code for _, code, _ in module.CONTRACTION}
    closure_packet = set().union(*(orbit(module, code) for code in closure_codes))
    contraction_packet = set().union(
        *(orbit(module, code) for code in contraction_codes)
    )
    require(not (closure_packet & contraction_packet),
            "closure22 unexpectedly acquired a contraction word")
    packet = closure_packet | contraction_packet
    canonical_words = {
        min(orbit(module, code)) for code in packet
    }
    require(len(closure_packet) == 62 and len(contraction_packet) == 16,
            "packet component census changed")
    require(len(packet) == 78 and len(canonical_words) == 22,
            "packet word/orbit census changed")

    seed_lines = ["KRENN_N8_NORMALIZED_TAIL_V1 7 564 2"]
    for row, coefficient in sorted(image.items()):
        cleared = coefficient * 2
        require(cleared.denominator == 1 and cleared,
                "tail denominator did not clear")
        seed_lines.append(f"ROW {row.hex()} {cleared.numerator}")
    seed_text = "\n".join(seed_lines) + "\n"

    word_lines = ["KRENN_N8_WORD_PACKET_V1 78 22"]
    for code in sorted(packet):
        word_lines.append(f"WORD {code} {word_label(module, code)}")
    word_text = "\n".join(word_lines) + "\n"

    all_mixed = sorted(polynomials)
    all_canonical_words = {
        min(orbit(module, code)) for code in all_mixed
    }
    require(len(all_mixed) == 6558 and len(all_canonical_words) == 1672,
            "all-mixed word/orbit census changed")
    all_word_lines = ["KRENN_N8_WORD_PACKET_V1 6558 1672"]
    for code in all_mixed:
        all_word_lines.append(f"WORD {code} {word_label(module, code)}")
    all_word_text = "\n".join(all_word_lines) + "\n"

    ledger = {
        "format": "n8-normalized-degree7-dfs-inputs-v1",
        "homogeneous_total_degree": 7,
        "tail_rows": len(image),
        "cleared_denominator": 2,
        "tail_degree_histogram": dict(sorted(Counter(map(len, image)).items())),
        "tail_cleared_coefficient_histogram": dict(sorted(
            Counter(int(value * 2) for value in image.values()).items()
        )),
        "closure22_stabilizer_literal_words": len(closure_packet),
        "contraction_stabilizer_literal_words": len(contraction_packet),
        "packet_literal_words": len(packet),
        "packet_stabilizer_orbits": len(canonical_words),
        "contraction_orbit_representatives": [
            word_label(module, min(orbit(module, code)))
            for code in sorted(contraction_codes)
        ],
        "seed_sha256": sha256(seed_text.encode()).hexdigest(),
        "word_packet_sha256": sha256(word_text.encode()).hexdigest(),
        "all_mixed_literal_words": len(all_mixed),
        "all_mixed_stabilizer_orbits": len(all_canonical_words),
        "all_mixed_word_packet_sha256": sha256(all_word_text.encode()).hexdigest(),
        "normalized_checker_sha256": EXPECTED_NORMALIZED_SHA256,
        "closure22_manifest_sha256": EXPECTED_CLOSURE_SHA256,
        "scope": (
            "Input export only for the closure22^H plus five-contraction-orbit "
            "degree-seven homogeneous DFS. No membership conclusion."
        ),
    }
    return seed_text, word_text, all_word_text, ledger


def main():
    seed_text, word_text, all_word_text, ledger = build()
    SEED.write_text(seed_text, encoding="ascii")
    WORDS.write_text(word_text, encoding="ascii")
    ALL_WORDS.write_text(all_word_text, encoding="ascii")
    RESULTS.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n")
    print(
        "n8 degree7 DFS inputs: PASS; "
        f"tail={ledger['tail_rows']}, words={ledger['packet_literal_words']}, "
        f"orbits={ledger['packet_stabilizer_orbits']}"
    )
    print(f"seed sha256: {ledger['seed_sha256']}")
    print(f"word packet sha256: {ledger['word_packet_sha256']}")
    print(f"all-mixed packet sha256: {ledger['all_mixed_word_packet_sha256']}")


if __name__ == "__main__":
    main()
