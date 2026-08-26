#!/usr/bin/env python3
"""Global N=8 support-18 occurrence SAT probe.

Every edge has three Boolean colour-support bits.  The model asks for exactly
18 live edges, coordinate anchor coverage at every site/colour, all three
pure matching rows, and no mixed word with exactly one literal occurrence.
Returned models are independently expanded and audited against the literal
target cap responses.  This is a probe until cap avoidance is internalized.
"""

from __future__ import annotations

from collections import Counter
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations_with_replacement, product
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import traceback


HERE = Path(__file__).resolve().parent
N = 8
COLORS = (0, 1, 2)
TARGET_EDGE = (0, 1)
INCIDENCE = (0, TARGET_EDGE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_local(module_name, filename):
    spec = spec_from_file_location(module_name, HERE / filename)
    require(spec is not None and spec.loader is not None,
            ("failed to load dependency", filename))
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


THEOREM = load_local(
    "n8_support18_theorem_for_global_sat_probe",
    "verify_n8_support18_multi_edge_persistence_theorem.py",
)
ORBIT = THEOREM.ORBIT
BINARY = THEOREM.BINARY
EDGES = tuple(
    (left, right)
    for left in range(N) for right in range(left + 1, N)
)
MATCHINGS = tuple(
    tuple(tuple(sorted(edge)) for edge in raw)
    for raw in ORBIT.BASE.perfect_matchings(tuple(range(N)))
)


def bit_name(edge, colour):
    return f"y_{edge[0]}_{edge[1]}_{colour}"


def smt_and(items):
    items = tuple(items)
    if not items:
        return "true"
    if len(items) == 1:
        return items[0]
    return f"(and {' '.join(items)})"


def smt_or(items):
    items = tuple(items)
    if not items:
        return "false"
    if len(items) == 1:
        return items[0]
    return f"(or {' '.join(items)})"


def occurrence_conditions():
    occurrences = {}
    for matching in MATCHINGS:
        for colours in product(COLORS, repeat=4):
            word = [None] * N
            bits = []
            for edge, colour in zip(matching, colours):
                word[edge[0]] = colour
                word[edge[1]] = colour
                bits.append(bit_name(edge, colour))
            occurrences.setdefault(tuple(word), []).append(tuple(bits))
    return occurrences


OCCURRENCES = occurrence_conditions()


def global_smt(target_support, support_size=18, timeout_seconds=300,
               target_degrees=None, degree_sequence=None):
    lines = ["(set-logic QF_LIA)", "(set-option :produce-models true)"]
    for edge in EDGES:
        for colour in COLORS:
            lines.append(f"(declare-const {bit_name(edge, colour)} Bool)")

    # Fix the target support exactly.
    for colour in COLORS:
        literal = bit_name(TARGET_EDGE, colour)
        lines.append(f"(assert {literal if colour in target_support else f'(not {literal})'})")

    live_terms = []
    live_expression = {}
    nonanchor_terms = []
    for edge in EDGES:
        bits = tuple(bit_name(edge, colour) for colour in COLORS)
        live = smt_or(bits)
        live_expression[edge] = live
        live_terms.append(f"(ite {live} 1 0)")
        at_least_two = smt_or(
            smt_and((bits[first], bits[second]))
            for first, second in ((0, 1), (0, 2), (1, 2))
        )
        nonanchor_terms.append(f"(ite {at_least_two} 1 0)")
    lines.append(f"(assert (= (+ {' '.join(live_terms)}) {support_size}))")
    # Search genuinely beyond the branch-complete three-nonanchor theorem.
    lines.append(f"(assert (>= (+ {' '.join(nonanchor_terms)}) 4))")

    # Source-valid S6 symmetry: the directed target fixes vertices 0 and 1,
    # while vertices 2,...,7 may be relabelled.  Every orbit has a
    # representative with nonincreasing live degree on those six vertices.
    degree_expression = {}
    for vertex in range(N):
        terms = tuple(
            f"(ite {live_expression[edge]} 1 0)"
            for edge in EDGES if vertex in edge
        )
        degree_expression[vertex] = f"(+ {' '.join(terms)})"
    # At occurrence level the two endpoints of the undirected target edge may
    # also be interchanged.  Left/right cap formulae are transposed by this
    # involution, so the avoidance property is preserved.
    lines.append(
        f"(assert (>= {degree_expression[0]} {degree_expression[1]}))"
    )
    for vertex in range(2, N - 1):
        lines.append(
            f"(assert (>= {degree_expression[vertex]} "
            f"{degree_expression[vertex + 1]}))"
        )
    if target_degrees is not None:
        require(len(target_degrees) == 2
                and target_degrees[0] >= target_degrees[1],
                ("invalid target degree branch", target_degrees))
        lines.append(
            f"(assert (= {degree_expression[0]} {target_degrees[0]}))"
        )
        lines.append(
            f"(assert (= {degree_expression[1]} {target_degrees[1]}))"
        )
    if degree_sequence is not None:
        require(len(degree_sequence) == N
                and degree_sequence[0] >= degree_sequence[1]
                and all(degree_sequence[index] >= degree_sequence[index + 1]
                        for index in range(2, N - 1)),
                ("invalid full degree branch", degree_sequence))
        for vertex, degree in enumerate(degree_sequence):
            lines.append(
                f"(assert (= {degree_expression[vertex]} {degree}))"
            )

    # Target support 12 retains exactly the colour involution 1<->2.  Fix a
    # lexicographic half by interpreting the two support-bit vectors as
    # binary integers.  Equality is retained.
    if target_support == (1, 2):
        colour_one = []
        colour_two = []
        for index, edge in enumerate(EDGES):
            weight = 1 << (len(EDGES) - 1 - index)
            colour_one.append(f"(ite {bit_name(edge, 1)} {weight} 0)")
            colour_two.append(f"(ite {bit_name(edge, 2)} {weight} 0)")
        lines.append(
            f"(assert (>= (+ {' '.join(colour_one)}) "
            f"(+ {' '.join(colour_two)})))"
        )

    # Each site/colour has a literal singleton-support coordinate anchor.
    for vertex in range(N):
        incident = tuple(edge for edge in EDGES if vertex in edge)
        for colour in COLORS:
            coordinate_choices = []
            for edge in incident:
                bits = tuple(bit_name(edge, item) for item in COLORS)
                coordinate_choices.append(smt_and(
                    (bits[colour],)
                    + tuple(f"(not {bits[item]})"
                            for item in COLORS if item != colour)
                ))
            lines.append(f"(assert {smt_or(coordinate_choices)})")

    pure_words = {tuple([colour] * N) for colour in COLORS}
    for word, occurrence_bits in sorted(OCCURRENCES.items()):
        terms = tuple(
            f"(ite {smt_and(bits)} 1 0)" for bits in occurrence_bits
        )
        total = terms[0] if len(terms) == 1 else f"(+ {' '.join(terms)})"
        if word in pure_words:
            lines.append(f"(assert (>= {total} 1))")
        elif len(set(word)) > 1:
            lines.append(f"(assert (not (= {total} 1)))")

    lines.extend(("(check-sat)", "(get-model)"))
    completed = subprocess.run(
        ("z3", "-in", f"-T:{timeout_seconds}"),
        input="\n".join(lines), text=True, capture_output=True,
        check=False,
    )
    output = completed.stdout
    status = output.splitlines()[0].strip() if output.splitlines() else ""
    if status == "timeout":
        status = "unknown"
    require(status in ("sat", "unsat", "unknown"),
            ("global support solver failed", completed.returncode,
             output[-2000:], completed.stderr[-2000:]))
    if status != "sat":
        return status, None, len("\n".join(lines))
    values = {
        name: value == "true"
        for name, value in re.findall(
            r"\(define-fun\s+(y_\d+_\d+_\d+)\s+\(\)\s+Bool\s+"
            r"(true|false)\s*\)",
            output,
        )
    }
    require(len(values) == len(EDGES) * len(COLORS),
            ("global support model incomplete", len(values), output[-4000:]))
    supports = {
        edge: tuple(
            colour for colour in COLORS if values[bit_name(edge, colour)]
        )
        for edge in EDGES
    }
    supports = {edge: support for edge, support in supports.items() if support}
    return status, supports, len("\n".join(lines))


def literal_word_histogram(supports):
    words = Counter()
    for matching in MATCHINGS:
        if not all(edge in supports for edge in matching):
            continue
        for colours in product(*(supports[edge] for edge in matching)):
            word = [None] * N
            for edge, colour in zip(matching, colours):
                word[edge[0]] = colour
                word[edge[1]] = colour
            words[tuple(word)] += 1
    return words


def audit_model(supports, target_support):
    require(len(supports) == 18 and supports[TARGET_EDGE] == target_support,
            ("global support model has wrong support", supports,
             target_support))
    words = literal_word_histogram(supports)
    pure = tuple(words[(colour,) * N] for colour in COLORS)
    singletons = tuple(sorted(
        word for word, multiplicity in words.items()
        if len(set(word)) > 1 and multiplicity == 1
    ))
    require(all(pure) and not singletons,
            ("global SAT model failed literal word audit", pure,
             singletons[:8]))
    edges = tuple(sorted(supports))
    shapes, private_caps, faces = THEOREM.response_data(edges, INCIDENCE)
    coordinate_states = {
        edge: support[0] for edge, support in supports.items()
        if len(support) == 1
    }


def support22_degree_sequences():
    sequences = []
    for degree0 in range(3, 8):
        for degree1 in range(3, degree0 + 1):
            for ascending_tail in combinations_with_replacement(range(3, 8), 6):
                tail = tuple(sorted(ascending_tail, reverse=True))
                sequence = (degree0, degree1) + tail
                if sum(sequence) == 44:
                    sequences.append(sequence)
    require(len(sequences) == 182,
            ("support22 degree-sequence count changed", len(sequences)))
    return tuple(sequences)


def audit_support22_degree_branches(worker_count=8):
    sequences = support22_degree_sequences()
    temporary = Path(tempfile.mkdtemp(prefix="n8-global-support22-degree-"))
    children = []
    try:
        for shard in range(worker_count):
            output_path = temporary / f"worker-{shard}.json"
            error_path = temporary / f"worker-{shard}.error"
            pid = os.fork()
            if pid == 0:
                try:
                    results = []
                    for index in range(shard, len(sequences), worker_count):
                        sequence = sequences[index]
                        status, supports, smt_bytes = global_smt(
                            (1, 2), 22, 120, degree_sequence=sequence
                        )
                        results.append({
                            "index": index,
                            "degree_sequence": sequence,
                            "status": status,
                            "supports": (tuple(sorted(supports.items()))
                                         if supports is not None else None),
                            "smt_bytes": smt_bytes,
                        })
                    with output_path.open("w", encoding="utf-8") as handle:
                        json.dump(results, handle, sort_keys=True,
                                  separators=(",", ":"))
                    os._exit(0)
                except BaseException:
                    with error_path.open("w", encoding="utf-8") as handle:
                        handle.write(traceback.format_exc())
                    os._exit(1)
            children.append((pid, shard, output_path, error_path))
        for pid, shard, _output_path, error_path in children:
            _waited, status = os.waitpid(pid, 0)
            require(os.waitstatus_to_exitcode(status) == 0,
                    ("support22 degree worker failed", shard,
                     error_path.read_text(encoding="utf-8")
                     if error_path.exists() else "no traceback"))
        results = []
        for _pid, _shard, output_path, _error_path in children:
            with output_path.open(encoding="utf-8") as handle:
                results.extend(json.load(handle))
        results.sort(key=lambda item: item["index"])
        require(len(results) == len(sequences),
                ("support22 branch result count changed", len(results)))
        return {
            "degree_sequence_count": len(sequences),
            "status_histogram": tuple(sorted(Counter(
                item["status"] for item in results
            ).items())),
            "sat_models": tuple(
                item for item in results if item["status"] == "sat"
            ),
            "unknown_branches": tuple(
                item for item in results if item["status"] == "unknown"
            ),
            "results": tuple(results),
        }
    finally:
        for pid, _shard, _output_path, _error_path in children:
            try:
                os.waitpid(pid, os.WNOHANG)
            except ChildProcessError:
                pass
        shutil.rmtree(temporary, ignore_errors=True)
    zero_coordinate = 0 if target_support == (1, 2) else None
    binary_landings = tuple(
        face for face in faces
        if BINARY.face_lands(face, coordinate_states, zero_coordinate)
    )
    return {
        "supports": tuple(sorted(supports.items())),
        "pure_occurrence_counts": pure,
        "mixed_multiplicity_histogram": tuple(sorted(Counter(
            multiplicity for word, multiplicity in words.items()
            if len(set(word)) > 1
        ).items())),
        "response_shapes": shapes,
        "private_caps": private_caps,
        "binary_faces": faces,
        "binary_landings": binary_landings,
        "cap_free_occurrence_guard": not private_caps and not binary_landings,
    }


def main():
    audit = audit_support22_degree_branches()
    print("support22 degree branches", audit["status_histogram"])
    print("sat/unknown", len(audit["sat_models"]),
          len(audit["unknown_branches"]))
    print("unknown degree sequences", tuple(
        tuple(item["degree_sequence"])
        for item in audit["unknown_branches"]
    ))


if __name__ == "__main__":
    main()
