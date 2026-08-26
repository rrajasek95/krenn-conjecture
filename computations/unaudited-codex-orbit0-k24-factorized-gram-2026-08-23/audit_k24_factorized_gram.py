#!/usr/bin/env python3
"""Audit the K24 Gram interface and the 1,757-index scope correction."""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROVIDER_SOURCE = HERE / "k24_factorized_gram_provider.py"
STRUCTURE_RESULT = (ROOT / "computations/unaudited-codex-orbit0-k24-terminal-structure-2026-08-23"
                    / "results_k24_terminal_structure.json")
OUT = HERE / "results_k24_factorized_gram.json"
SAMPLE_CHECKPOINT = HERE / "checkpoint_sample_k24_column_closure.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, f"cannot load {path}")
    spec.loader.exec_module(module)
    return module


G = load("k24_factorized_provider_audit", PROVIDER_SOURCE)
F = G.F


def fixed_column_family():
    """Count columns `(w,2P-M)` for P containing one fixed mixed M."""
    word = (0, 1, 0, 1, 0, 1, 0, 1)
    selected = F.BASE.term_ids(word, F.M0)
    require(len(selected) == 4 and all(cell not in F.A for cell in selected),
            "fixed selected matching is not anchor-free")
    selected_ports = {3 * site + word[site] for site in range(8)}
    vertices = tuple(port for port in range(24) if port not in selected_ports)
    require(len(vertices) == 16, len(vertices))
    m0 = set(F.M0)

    def allowed(left, right):
        i, a = divmod(vertices[left], 3)
        j, b = divmod(vertices[right], 3)
        return (i != j
                and not ((min(i, j), max(i, j)) in m0 and a == b))

    adjacency = tuple(sum(1 << right for right in range(16)
                          if right != left and allowed(left, right))
                      for left in range(16))

    @lru_cache(None)
    def count(mask):
        if mask == 0:
            return 1
        first_bit = mask & -mask
        first = first_bit.bit_length() - 1
        remainder = mask ^ first_bit
        choices = adjacency[first] & remainder
        answer = 0
        while choices:
            mate_bit = choices & -choices
            choices ^= mate_bit
            answer += count(remainder ^ mate_bit)
        return answer

    def first_completion(mask):
        if mask == 0:
            return ()
        first_bit = mask & -mask
        first = first_bit.bit_length() - 1
        remainder = mask ^ first_bit
        choices = adjacency[first] & remainder
        while choices:
            mate_bit = choices & -choices
            choices ^= mate_bit
            tail_mask = remainder ^ mate_bit
            if count(tail_mask):
                second = mate_bit.bit_length() - 1
                return ((vertices[first], vertices[second]),) + first_completion(tail_mask)
        raise RuntimeError("positive matching count had no first completion")

    family_size = count((1 << 16) - 1)
    matching = first_completion((1 << 16) - 1)
    cells = list(selected)
    remaining_cells = []
    for left, right in matching:
        i, a = divmod(left, 3)
        j, b = divmod(right, 3)
        if i > j:
            i, j, a, b = j, i, b, a
        cell = F.BASE.CELL_ID[(i, j, a, b)]
        require(cell not in F.A, "completion used an anchor")
        cells.append(cell)
        remaining_cells.append(cell)
    require(len(cells) == 12, len(cells))
    multiplier = bytes(sorted(tuple(selected)
                              + tuple(cell for cell in remaining_cells
                                      for _ in range(2))))
    require(len(multiplier) == 20, len(multiplier))
    column = (word, multiplier)
    outputs = G.top_outputs(column)
    require(len(outputs) == 105,
            "alternating fixed word lost a K24 completion")
    selected_row = bytes(sorted(multiplier + selected))
    require(selected_row in outputs and G.D24.row_k_degree(selected_row) == 24,
            "fixed family column lost doubled matching head")
    return word, selected, family_size, count.cache_info().currsize, column


def difference_kernel(word):
    terms = tuple(term for term in F.BASE.word_terms(word)
                  if G.D24.row_k_degree(term) == 4)
    kernel = Counter()
    for left in terms:
        for right in terms:
            difference = Counter(left)
            difference.subtract(right)
            key = tuple(sorted((cell, coefficient)
                               for cell, coefficient in difference.items()
                               if coefficient))
            kernel[key] += 1
    return len(terms), len(kernel), Counter(kernel.values())


def main():
    structure = json.loads(STRUCTURE_RESULT.read_text())
    require(structure["source_decorations"]["H_top_decoration_orbits"] == 1757
            and structure["source_decorations"]
            ["anchor_free_word_matching_decorations"] == 569736,
            "terminal structure decoration census changed")
    word, selected, family_size, dp_states, sample_column = fixed_column_family()
    require(family_size == 890713, family_size)
    column_orbit_lower_bound = (family_size + len(G.H) - 1) // len(G.H)
    require(column_orbit_lower_bound == 2320 > 1757,
            column_orbit_lower_bound)

    term_count, kernel_support, kernel_coefficients = difference_kernel(word)
    require((term_count, kernel_support, kernel_coefficients)
            == (105, 10081, Counter({1: 9660, 3: 420, 105: 1})),
            (term_count, kernel_support, kernel_coefficients))

    representative = G.canonical_column(sample_column)
    vector = G.orbit_column_vector(representative)
    self_gram = G.gram_entry(representative, representative)
    require(self_gram > 0 and vector, "sample orbit vector vanished")
    first_row = G.top_outputs(representative)[0]
    first_row_neighbours = {
        G.canonical_column(column)
        for column in G.D24.incident_degree24_columns(first_row)
    }
    checkpoint = json.loads(SAMPLE_CHECKPOINT.read_text())
    require(checkpoint["status"] == "COLUMN_CAP"
            and checkpoint["column_cap"] == 50
            and len(checkpoint["known"]) == 1032
            and len(checkpoint["processed"]) == 1
            and len(checkpoint["queue"]) == 1031,
            "sample restart checkpoint changed")

    result = {
        "status": "PASS exact K24 factorized-Gram scope audit",
        "scope_correction": {
            "decorated_matching_H_orbits": 1757,
            "decorated_matching_pairs": 569736,
            "literal_column_key": "(mixed word w, 20-cell multiplier U)",
            "verdict": "1757 indexes local matching decorations, not literal degree-24 columns",
        },
        "fixed_decoration_column_lower_bound": {
            "word": "".join(map(str, word)),
            "selected_matching": selected.hex(),
            "distinct_columns": family_size,
            "matching_DP_states": dp_states,
            "H_column_orbit_lower_bound": column_orbit_lower_bound,
            "proof": "P ranges over anchor-free port PMs containing fixed M; U=2P-M uniquely recovers P",
        },
        "convolution_kernel_control": {
            "top_terms": term_count,
            "ordered_term_pairs": term_count ** 2,
            "distinct_difference_keys": kernel_support,
            "coefficient_histogram": dict(sorted(kernel_coefficients.items())),
            "formula": (
                "<C(w,U),C(w',U')> = # {(M,M'): M-M'=U'-U}, "
                "with M,M' anchor-free terms of H_w,H_w'"
            ),
        },
        "sample_orbit_vector": {
            "representative": G.column_key(representative),
            "column_orbit_size": len(G.column_orbit(representative)),
            "row_orbit_coordinates": len(vector),
            "top_terms_of_representative": len(G.top_outputs(representative)),
            "self_gram": self_gram,
            "first_output_row": first_row.hex(),
            "first_output_incident_H_column_orbits": len(first_row_neighbours),
        },
        "sample_restartable_closure": {
            "status": checkpoint["status"],
            "cap": checkpoint["column_cap"],
            "known_column_orbits": len(checkpoint["known"]),
            "processed_column_orbits": len(checkpoint["processed"]),
            "queued_column_orbits": len(checkpoint["queue"]),
            "checkpoint": str(SAMPLE_CHECKPOINT.relative_to(ROOT)),
        },
        "exact_H_Gram": {
            "orbit_column_vector": (
                "v_C=sum_(c in Orb_H(C)) top(c), stored as total mass on each H-row orbit"
            ),
            "entry": "G_CD=sum_roworbit mass_C*mass_D/orbit_size",
            "target_pairing": "b_C=sum_roworbit mass_C*mass_R/orbit_size",
            "membership": (
                "over Q, for a COMPLETE Gram-connected column component, R is in "
                "the column span iff appending R does not increase Gram rank"
            ),
            "restartable_provider": str(G.PROVIDER_SOURCE.relative_to(ROOT))
                if hasattr(G, "PROVIDER_SOURCE") else str(PROVIDER_SOURCE.relative_to(ROOT)),
        },
        "rank_test_status": (
            "No 1757-square modular rank was run: it would identify different "
            "multipliers and is not a source map. The packaged provider must first "
            "close the target-rooted H-column component after R24 exists."
        ),
        "pinned": {
            str(PROVIDER_SOURCE.relative_to(ROOT)):
                sha256(PROVIDER_SOURCE.read_bytes()).hexdigest(),
            str(STRUCTURE_RESULT.relative_to(ROOT)):
                sha256(STRUCTURE_RESULT.read_bytes()).hexdigest(),
            str(SAMPLE_CHECKPOINT.relative_to(ROOT)):
                sha256(SAMPLE_CHECKPOINT.read_bytes()).hexdigest(),
        },
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode()).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
