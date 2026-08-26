#!/usr/bin/env python3
"""Restartable H-orbit-mass reducer for -R8'*E0*E1*E2 through K24.

The default command performs only bounded structural/reference checks.  The
seed/reduce entry points are implemented but deliberately not launched here.
"""

from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from heapq import merge
from itertools import product
import ast
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
K16_DIR = ROOT / "computations/unaudited-codex-orbit0-k16-literal-collection-2026-08-22"
K16_SOURCE = K16_DIR / "collect_orbit0_k16_literal_residual.py"
K16_RESULT = K16_DIR / "results_orbit0_k16_literal_residual.json"
C6_SOURCE = (ROOT / "computations/unaudited-codex-orbit0-k16-c6-schur-boundary-2026-08-23"
             / "audit_k16_c6_schur_boundary.py")
RESULT = HERE / "results_filtered_k24_reducer_design.json"
RUN_LIMIT = 100_000


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, path)
    spec.loader.exec_module(module)
    return module


K16 = load("filtered_k24_frozen_k16", K16_SOURCE)
C6 = load("filtered_k24_c6", C6_SOURCE)
F, HQ, D24, H = K16.F, C6.HQ, C6.D24, C6.H


class Context:
    def __init__(self):
        self.anchor_cells = tuple(sorted(F.A))
        self.anchor_position = {cell: i for i, cell in enumerate(self.anchor_cells)}
        self.anchors = []
        self.vectors = []
        self.tails = []
        self.words = []
        for colours in product(range(3), repeat=4):
            if len(set(colours)) == 1:
                continue
            word = F.word_from_pair_colours(colours)
            anchor = F.BASE.term_ids(word, F.M0)
            by_k = {degree: tuple(term for term in F.BASE.word_terms(word)
                                  if F.row_k_degree(term) == degree)
                    for degree in (2, 3, 4)}
            require(tuple(map(len, by_k.values())) == (12, 32, 60),
                    (colours, tuple(map(len, by_k.values()))))
            self.words.append(word)
            self.anchors.append(anchor)
            self.vectors.append(tuple(Counter(anchor)[cell]
                                      for cell in self.anchor_cells))
            self.tails.append(by_k)
        require(len(self.anchors) == 78, len(self.anchors))
        self.anchor_to_pivot = {row: i for i, row in enumerate(self.anchors)}
        self.signature_permutations = {}
        self.pivot_permutations = {}
        for action in H:
            transform = F.EXPORT.TRANSFORMS[action]
            self.signature_permutations[action] = tuple(
                self.anchor_position[transform[cell]] for cell in self.anchor_cells)
            self.pivot_permutations[action] = tuple(
                self.anchor_to_pivot[F.move_row(anchor, action)]
                for anchor in self.anchors)
        self.signature_cache = {}

    def signature(self, row):
        counts = Counter(row)
        return tuple(counts[cell] for cell in self.anchor_cells)

    def move_signature(self, signature, action):
        moved = [0] * 12
        for old, new in enumerate(self.signature_permutations[action]):
            moved[new] = signature[old]
        return tuple(moved)

    def canonical_signature(self, signature):
        if signature not in self.signature_cache:
            self.signature_cache[signature] = min(
                self.move_signature(signature, action) for action in H)
        return self.signature_cache[signature]

    def pivots(self, signature):
        return tuple(i for i, vector in enumerate(self.vectors)
                     if all(left >= right for left, right
                            in zip(signature, vector, strict=True)))

    def child_signature_multiset(self, signature, pivot, tail_degree):
        base = tuple(left - right for left, right
                     in zip(signature, self.vectors[pivot], strict=True))
        answer = Counter()
        for tail in self.tails[pivot][tail_degree]:
            counts = Counter(tail)
            child = tuple(left + counts[cell] for left, cell
                          in zip(base, self.anchor_cells, strict=True))
            answer[self.canonical_signature(child)] += 1
        return answer


CTX = Context()


def fraction_text(value):
    return f"{value.numerator}/{value.denominator}"


def parse_fraction(text):
    numerator, denominator = text.split("/")
    return Fraction(int(numerator), int(denominator))


def flush_run(buffer, directory, label, run_index):
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{label}.run{run_index:06d}.tsv"
    with path.open("w") as stream:
        for row, mass in sorted(buffer.items()):
            if mass:
                stream.write(f"{row.hex()}\t{fraction_text(mass)}\n")
    buffer.clear()
    return path


def merge_runs(paths, output):
    """External exact merge of sorted row/mass runs."""
    handles = [path.open() for path in paths]
    try:
        streams = (((line.split("\t", 1)[0], line.split("\t", 1)[1].strip())
                    for line in handle) for handle in handles)
        current = None
        mass = Fraction(0)
        with output.open("w") as target:
            for row_hex, value in merge(*streams, key=lambda item: item[0]):
                if current is not None and row_hex != current:
                    if mass:
                        target.write(f"{current}\t{fraction_text(mass)}\n")
                    mass = Fraction(0)
                current = row_hex
                mass += parse_fraction(value)
            if current is not None and mass:
                target.write(f"{current}\t{fraction_text(mass)}\n")
    finally:
        for handle in handles:
            handle.close()


def orbit_rows(row):
    return tuple(sorted({F.move_row(row, action) for action in H}))


def r8_h_records():
    """Split the signed full-stabilizer R8' masses into exact H-orbit slices."""
    raw = json.loads(F.R8P.read_text())
    answer = []
    for row_hex, numerator, denominator in raw["residual"]:
        representative = bytes.fromhex(row_hex)
        full_orbit = set(F.EXPORT.row_orbit(representative))
        coefficient = Fraction(numerator, denominator) / len(full_orbit)
        unseen = set(full_orbit)
        while unseen:
            seed = min(unseen)
            orbit = set(orbit_rows(seed))
            require(orbit <= unseen, "H orbit crossed R8' full orbit")
            answer.append((seed, len(orbit), coefficient))
            unseen.difference_update(orbit)
    require(len(answer) == 485, len(answer))
    return tuple(answer)


def seed_full_product_restartable(run_dir, checkpoint_path,
                                  max_triples=None):
    """Stream -R8'*E0*E1*E2 into K14..K20 H-mass runs.

    The cursor is `(R8 H-slice, flattened 104^3 tail triple)`; no million-row
    packet or residual is materialized.
    """
    words = tuple(F.word_from_pair_colours(row) for row in F.PAIR_COLOURS)
    anchors = tuple(F.BASE.term_ids(word, F.M0) for word in words)
    errors = tuple(tuple(term for term in F.BASE.word_terms(word)
                         if term != anchor)
                   for word, anchor in zip(words, anchors, strict=True))
    require(tuple(map(len, errors)) == (104, 104, 104), tuple(map(len, errors)))
    records = r8_h_records()
    checkpoint = ({"r8_index": 0, "triple_index": 0, "processed": 0,
                   "runs": Counter()}
                  if not checkpoint_path.exists()
                  else json.loads(checkpoint_path.read_text()))
    run_counts = Counter(checkpoint["runs"])
    buffers = {f"K{degree}": defaultdict(Fraction)
               for degree in range(14, 21)}
    triple_count = 104 ** 3
    stopped = False
    for r8_index in range(checkpoint["r8_index"], len(records)):
        r8, orbit_size, coefficient = records[r8_index]
        start = checkpoint["triple_index"] if r8_index == checkpoint["r8_index"] else 0
        mass = -coefficient * orbit_size
        for flat in range(start, triple_count):
            left, remainder = divmod(flat, 104 ** 2)
            middle, right = divmod(remainder, 104)
            row = HQ.canonical_row(bytes(sorted(
                r8 + errors[0][left] + errors[1][middle] + errors[2][right])))
            degree = D24.row_k_degree(row)
            require(14 <= degree <= 20, (degree, row.hex()))
            buffers[f"K{degree}"][row] += mass
            checkpoint["processed"] += 1
            if sum(map(len, buffers.values())) >= RUN_LIMIT:
                for label, buffer in buffers.items():
                    if buffer:
                        flush_run(buffer, run_dir, label, run_counts[label])
                        run_counts[label] += 1
                checkpoint.update(r8_index=r8_index, triple_index=flat + 1,
                                  runs=dict(run_counts))
                checkpoint_path.write_text(json.dumps(checkpoint, indent=2,
                                                       sort_keys=True) + "\n")
            if max_triples and checkpoint["processed"] >= max_triples:
                stopped = True
                checkpoint.update(r8_index=r8_index, triple_index=flat + 1)
                break
        if stopped:
            break
        checkpoint["triple_index"] = 0
        checkpoint["r8_index"] = r8_index + 1
    for label, buffer in buffers.items():
        if buffer:
            flush_run(buffer, run_dir, label, run_counts[label])
            run_counts[label] += 1
    checkpoint.update(runs=dict(run_counts), complete=not stopped)
    checkpoint_path.write_text(json.dumps(checkpoint, indent=2,
                                           sort_keys=True) + "\n")
    return checkpoint


def reduce_orbit_record(row, orbit_mass, degree, policy="all"):
    """Reduce one canonical H-orbit and return exact orbit-mass children.

    Enumerating the labelled orbit is slower than the frozen K14 shortcut but
    makes stabilizer masses explicit and sound at every later degree.
    """
    images = orbit_rows(row)
    coefficient = orbit_mass / len(images)
    irreducible = defaultdict(Fraction)
    children = {d: defaultdict(Fraction) for d in range(degree + 2, 25)}
    for image in images:
        signature = CTX.signature(image)
        available = CTX.pivots(signature)
        if not available:
            irreducible[HQ.canonical_row(image)] += coefficient
            continue
        require(policy == "all", "later-degree reducer only certifies all-pivot average")
        weight = -coefficient / len(available)
        base = Counter(image)
        for pivot in available:
            quotient = Counter(base)
            quotient.subtract(CTX.anchors[pivot])
            require(all(value >= 0 for value in quotient.values()),
                    (row.hex(), pivot))
            multiplier = bytes(sorted(quotient.elements()))
            for tail_degree in (2, 3, 4):
                child_degree = degree + tail_degree
                if child_degree > 24:
                    continue
                for tail in CTX.tails[pivot][tail_degree]:
                    child = HQ.canonical_row(bytes(sorted(multiplier + tail)))
                    children[child_degree][child] += weight
    return irreducible, children


def reduce_degree_restartable(input_tsv, run_dir, degree,
                              checkpoint_path, max_records=None):
    """Restartable degree bucket reduction; output runs require merge_runs."""
    checkpoint = ({"offset": 0, "records": 0, "runs": Counter()}
                  if not checkpoint_path.exists()
                  else json.loads(checkpoint_path.read_text()))
    buffers = {"normal": defaultdict(Fraction)}
    buffers.update({f"K{d}": defaultdict(Fraction)
                    for d in range(degree + 2, 25)})
    run_counts = Counter(checkpoint["runs"])
    with input_tsv.open() as stream:
        stream.seek(checkpoint["offset"])
        while line := stream.readline():
            row_hex, mass_text = line.rstrip().split("\t")
            row, mass = bytes.fromhex(row_hex), parse_fraction(mass_text)
            require(D24.row_k_degree(row) == degree, (row_hex, degree))
            normal, children = reduce_orbit_record(row, mass, degree)
            for child, value in normal.items():
                buffers["normal"][child] += value
            for child_degree, values in children.items():
                for child, value in values.items():
                    buffers[f"K{child_degree}"][child] += value
            checkpoint["records"] += 1
            if sum(map(len, buffers.values())) >= RUN_LIMIT:
                for label, buffer in buffers.items():
                    if buffer:
                        flush_run(buffer, run_dir, label, run_counts[label])
                        run_counts[label] += 1
                checkpoint.update(offset=stream.tell(), runs=dict(run_counts))
                checkpoint_path.write_text(json.dumps(checkpoint, indent=2,
                                                       sort_keys=True) + "\n")
            if max_records and checkpoint["records"] >= max_records:
                break
        for label, buffer in buffers.items():
            if buffer:
                flush_run(buffer, run_dir, label, run_counts[label])
                run_counts[label] += 1
        checkpoint.update(offset=stream.tell(), runs=dict(run_counts), complete=not line)
        checkpoint_path.write_text(json.dumps(checkpoint, indent=2,
                                               sort_keys=True) + "\n")
    return checkpoint


def first_pivot_ambiguity():
    """Find a K16 anchor signature where two legal pivots have different K18 tails."""
    for left in range(78):
        for right in range(left + 1, 78):
            signature = tuple(a + b for a, b
                              in zip(CTX.vectors[left], CTX.vectors[right], strict=True))
            available = CTX.pivots(signature)
            if len(available) < 2:
                continue
            ledgers = {pivot: CTX.child_signature_multiset(signature, pivot, 2)
                       for pivot in available}
            first = available[0]
            for second in available[1:]:
                if ledgers[first] != ledgers[second]:
                    return {
                        "K_parent": 16,
                        "anchor_signature": list(signature),
                        "pivot_indices": [first, second],
                        "pivot_words": ["".join(map(str, CTX.words[first])),
                                        "".join(map(str, CTX.words[second]))],
                        "K18_child_signature_ledgers_differ": True,
                        "first_support": len(ledgers[first]),
                        "second_support": len(ledgers[second]),
                    }
    raise RuntimeError("no beyond-K16 pivot ambiguity found")


def validate_frozen_k16_reference():
    raw = K16_RESULT.read_bytes()
    require(sha256(raw).hexdigest() ==
            "28a648a2625d208cc86948b27a06f52f38245fe2ebe130c583e619d1d24b9189",
            "frozen K16 byte digest changed")
    data = json.loads(raw)
    logical = dict(data)
    stored = logical.pop("logical_sha256")
    replay = sha256(json.dumps(logical, sort_keys=True,
                               separators=(",", ":")).encode()).hexdigest()
    require(stored == replay ==
            "8eb9f7dbb220afd759533c10a4881a502a43bdb3bfa28c36e3b89cf98a4ee58c",
            (stored, replay))
    require(len(data["literal_orbits"]) == 1_848_174,
            len(data["literal_orbits"]))
    # Bounded semantic sentinels without rebuilding the 838,080 cancellations.
    sentinels = (data["literal_orbits"][:2048]
                 + data["literal_orbits"][-2048:])
    for row_hex, _numerator, _denominator in sentinels:
        row = bytes.fromhex(row_hex)
        require(D24.row_k_degree(row) == 16, row_hex)
        require(not CTX.pivots(CTX.signature(row)), (row_hex, "reducible frozen row"))
    return {
        "byte_sha256": sha256(raw).hexdigest(),
        "logical_sha256": stored,
        "H_orbits": len(data["literal_orbits"]),
        "semantic_sentinel_rows": len(sentinels),
        "labelled_support": data["collection"]["labelled_support_after_collection"],
        "scope": "isolated K14-cancellation K2-tail irreducible component only",
    }


def main():
    reference = validate_frozen_k16_reference()
    ambiguity = first_pivot_ambiguity()
    direct_profiles = {
        "K14_E2+2+2": 12 ** 3,
        "K15_E2+2+3": 3 * 12 ** 2 * 32,
        "K16_E2+2+4": 3 * 12 ** 2 * 60,
        "K16_E2+3+3": 3 * 12 * 32 ** 2,
    }
    result = {
        "status": "PASS bounded filtered-K24 reducer design/reference gate",
        "tail_counts_per_mixed_generator": {"K2": 12, "K3": 32, "K4": 60},
        "direct_seed_profiles_per_R8_H_slice": direct_profiles,
        "full_direct_K16_terms_per_slice": direct_profiles["K16_E2+2+4"]
                                              + direct_profiles["K16_E2+3+3"],
        "recurrence": "after collection, a pivot at Kd emits K(d+2), K(d+3), K(d+4)",
        "frozen_K16_reference": reference,
        "beyond_K16_ambiguity": ambiguity,
        "chosen_later_policy": "average all literal dividing mixed K0 pivots over each labelled H orbit",
        "restart_interface": {
            "input": "sorted TSV: canonical_row_hex<TAB>orbit_mass_fraction",
            "checkpoint": "byte offset, record count, per-degree run counts",
            "runs": "sorted exact Fraction H-orbit-mass runs, externally mergeable",
            "degrees": list(range(14, 25)),
        },
        "scope_guard": (
            "The frozen K16 digest is the isolated K14-pivot K2-tail component. "
            "A full K16 bucket must first add direct 2+2+4 and 2+3+3 seed terms. "
            "No K24 seed/reduction run was launched."
        ),
        "pinned": {
            str(K16_SOURCE.relative_to(ROOT)): sha256(K16_SOURCE.read_bytes()).hexdigest(),
            str(C6_SOURCE.relative_to(ROOT)): sha256(C6_SOURCE.read_bytes()).hexdigest(),
        },
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode()).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"],
                      "frozen_K16": reference,
                      "ambiguity": ambiguity,
                      "logical_sha256": result["logical_sha256"]},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
