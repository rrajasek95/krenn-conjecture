#!/usr/bin/env python3
"""Export the first C4-atlas boundary in the all-anchor normalization.

Chart 1 uses the common perfect matching 01|23|45|67 in all three colours.
All twelve selected cells are set to one.  The first missing atlas branch is
A_02[0,0]=0.  The output contains the 6,558 literal mixed amplitudes followed
by three small Rabinowitsch rows s_c*H_c-1; a unit closes precisely the locus
I_mix=0, H_0 H_1 H_2 != 0 on this boundary.
"""

from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
D5_PATH = ROOT / "computations/verify_n8_full_source_pure_product_degree5_lift.py"
INPUT = HERE / "chart1_boundary_a0200_p1073741827.msolve"
LABELS = HERE / "chart1_boundary_a0200_labels.json"
RESULT = HERE / "results_chart1_boundary_export.json"
PRIME = 1_073_741_827


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise RuntimeError(path)
    spec.loader.exec_module(module)
    return module


D5 = load(D5_PATH, "chart1_boundary_literal_source")
COORDINATE_ID = {coordinate: index for index, coordinate in enumerate(D5.COORDINATES)}
MATCHING = ((0, 1), (2, 3), (4, 5), (6, 7))
SUPPORT = frozenset(
    COORDINATE_ID[i, j, colour, colour]
    for colour in range(3) for i, j in MATCHING
)
BOUNDARY = COORDINATE_ID[0, 2, 0, 0]


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def variable_name(identifier):
    i, j, a, b = D5.COORDINATES[identifier]
    return f"x{i}{j}_{a}{b}"


def normalized_generator(code):
    answer = Counter()
    for literal in D5.iter_word_terms(code):
        if BOUNDARY in literal:
            continue
        answer[bytes(value for value in literal if value not in SUPPORT)] += 1
    require(answer and set(answer.values()) == {1},
            f"row {code} acquired a collision or vanished")
    return answer


def monomial_text(monomial, prefix=None):
    factors = ([] if prefix is None else [prefix]) + [
        variable_name(value) for value in monomial
    ]
    return "*".join(factors) if factors else "1"


def polynomial_text(polynomial, prefix=None, constant=-0):
    terms = []
    for monomial, coefficient in sorted(polynomial.items()):
        require(coefficient == 1, "unexpected source coefficient")
        terms.append(monomial_text(monomial, prefix))
    if constant:
        terms.append(str(constant))
    return "+".join(terms).replace("+-", "-")


def main():
    require(len(SUPPORT) == 12 and BOUNDARY not in SUPPORT,
            "chart/boundary interface changed")
    variables = [identifier for identifier in range(252)
                 if identifier not in SUPPORT and identifier != BOUNDARY]
    require(len(variables) == 239, "boundary ring variable count changed")

    rows = []
    labels = []
    term_counts = Counter()
    minimum_degrees = Counter()
    global_terms = set()
    constant_words = []
    boundary_affected = 0
    pure = []
    for code in range(3 ** 8):
        polynomial = normalized_generator(code)
        if len(set(D5.decode_word(code))) == 1:
            pure.append((code, polynomial))
            continue
        rows.append(polynomial_text(polynomial))
        labels.append(f"mixed_word_{''.join(map(str, D5.decode_word(code)))}")
        term_counts[len(polynomial)] += 1
        minimum_degrees[min(map(len, polynomial))] += 1
        global_terms.update(polynomial)
        if b"" in polynomial:
            constant_words.append(code)
        if len(polynomial) != 105:
            boundary_affected += 1
    require(len(rows) == 6558 and len(pure) == 3,
            "literal word partition changed")
    require(term_counts == Counter({105: 5830, 90: 728})
            and minimum_degrees == Counter({0: 78, 1: 648, 2: 1944,
                                            3: 2592, 4: 1296})
            and len(global_terms) == 596816,
            "mixed boundary census changed")

    pure_records = []
    for colour, (code, polynomial) in enumerate(pure):
        require(code == D5.word_code((colour,) * 8), "pure order changed")
        rows.append(polynomial_text(polynomial, prefix=f"s{colour}", constant=-1))
        labels.append(f"pure_live_inverse_colour_{colour}")
        pure_records.append({
            "colour": colour,
            "terms": len(polynomial),
            "degree_histogram": dict(sorted(Counter(map(len, polynomial)).items())),
            "constant_coefficient": polynomial.get(b"", 0),
        })
    require([item["terms"] for item in pure_records] == [90, 105, 105],
            "pure boundary term counts changed")

    variable_names = [variable_name(value) for value in variables] + ["s0", "s1", "s2"]
    with INPUT.open("w") as handle:
        handle.write(",".join(variable_names) + "\n")
        handle.write(str(PRIME) + "\n")
        handle.write(",\n".join(rows) + "\n")
    LABELS.write_text(json.dumps({"labels": labels}, indent=2) + "\n")

    payload = {
        "format": "n8-chart1-boundary-a0200-export-v1",
        "status": "EXACT_SOURCE_EXPORT_READY_BOUNDED_GATE_PENDING",
        "chart": 1,
        "normalization": {
            "support_matching_every_colour": [list(edge) for edge in MATCHING],
            "support_ids": sorted(SUPPORT),
            "support_cells_set_to_one": 12,
            "boundary_id": BOUNDARY,
            "boundary_coordinate": list(D5.COORDINATES[BOUNDARY]),
            "boundary_cell_set_to_zero": "A_02[0,0]",
            "free_source_variables": len(variables),
            "boundary_stabilizer_order": 32,
        },
        "source": {
            "mixed_generators": len(rows) - 3,
            "collected_mixed_terms": sum(size * count for size, count in term_counts.items()),
            "mixed_term_count_histogram": dict(sorted(term_counts.items())),
            "mixed_minimum_degree_histogram": dict(sorted(minimum_degrees.items())),
            "mixed_global_monomial_keys": len(global_terms),
            "constant_mixed_generators": len(constant_words),
            "boundary_affected_mixed_generators": boundary_affected,
            "pure": pure_records,
            "inverse_rows": 3,
        },
        "input": {
            "path": INPUT.name,
            "sha256": sha256(INPUT.read_bytes()).hexdigest(),
            "bytes": INPUT.stat().st_size,
            "variables": len(variable_names),
            "equations": len(rows),
            "characteristic": PRIME,
            "labels_path": LABELS.name,
            "labels_sha256": sha256(LABELS.read_bytes()).hexdigest(),
        },
        "theorem_interface": (
            "A characteristic-zero unit certificate for this extended ideal is equivalent "
            "to emptiness of the chart1 normalized boundary with I_mix=0 and H0*H1*H2 live."
        ),
        "scope": (
            "Literal chart1 all-twelve-anchor normalization and A_02[0,0]=0 only. "
            "A modular unit is discovery until an exact source replay; timeout/nonunit makes "
            "no nonemptiness claim."
        ),
        "source_sha256": {
            str(D5_PATH.relative_to(ROOT)): sha256(D5_PATH.read_bytes()).hexdigest(),
        },
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["logical_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
