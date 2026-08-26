#!/usr/bin/env python3
"""Exact census of the 50 joint cofactor/permanent-term aligned charts.

For each 2x2 block choose a live permanent term.  On the aligned boundary
chart, an off-diagonal choice is [[a,b],[-1/b,0]] and a diagonal choice is
[[a,b],[0,-1/a]].  The full B4 action on the cofactor-orientation mask and
the live-term mask has exactly 50 joint orbits.  This checker derives every
specialized row from the raw 24-cell definitions, screens all 50 charts over
two primes and Q, and exact-replays a Singular lift plus a deletion mutation
for every unit chart.  It makes no claim about the full 24-variable open
term charts.

It also independently replays Dangerous' five-row weight-four d=0 ledger
from its frozen JSON, without importing that producer's implementation.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
from itertools import combinations, permutations, product
import json
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SCREEN_PATH = (ROOT / "computations" /
               "unaudited-codex-n8-orbit0-normalized-78-2026-08-20" /
               "screen_lowq_joint_branch_orbits.py")
WEIGHT4_RESULT = (ROOT / "computations" /
                  "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20" /
                  "results_weight4_dzero_unit_identity.json")
OUT = HERE / "results_joint_aligned_zero_chart_census.json"
EDGES = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
VARIABLE_COUNT = 12
ONE = {(0,) * VARIABLE_COUNT: Fraction(1)}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


SCREEN = load("n8_joint_aligned_screen", SCREEN_PATH)
PROBE = SCREEN.PROBE


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def clean(poly):
    return {monomial: coefficient for monomial, coefficient in poly.items()
            if coefficient}


def add(*polys):
    answer = Counter()
    for poly in polys:
        answer.update(poly)
    return clean(answer)


def scale(poly, coefficient):
    coefficient = Fraction(coefficient)
    return clean({monomial: coefficient * value
                  for monomial, value in poly.items()})


def multiply(*polys):
    answer = ONE
    for poly in polys:
        updated = Counter()
        for left, left_coefficient in answer.items():
            for right, right_coefficient in poly.items():
                exponent = tuple(a + b for a, b in zip(left, right))
                updated[exponent] += left_coefficient * right_coefficient
        answer = clean(updated)
    return answer


def variable(index, exponent=1, coefficient=1):
    powers = [0] * VARIABLE_COUNT
    powers[index] = exponent
    return {tuple(powers): Fraction(coefficient)}


def aligned_entries(term_mask):
    entries = []
    for edge in range(6):
        a, b = variable(edge), variable(6 + edge)
        if term_mask >> edge & 1:
            entries.extend((a, b, variable(6 + edge, -1, -1), {}))
        else:
            entries.extend((a, b, {}, variable(edge, -1, -1)))
    return tuple(entries)


def substitute(raw_poly, entries):
    answer = {}
    for monomial, coefficient in raw_poly.items():
        term = scale(ONE, coefficient)
        for raw_variable in monomial:
            term = multiply(term, entries[raw_variable])
        answer = add(answer, term)
    return answer


def clear_denominators(poly):
    if not poly:
        return {}
    shift = tuple(-min([exponent[index] for exponent in poly] + [0])
                  for index in range(VARIABLE_COUNT))
    return {tuple(exponent[index] + shift[index]
                  for index in range(VARIABLE_COUNT)): coefficient
            for exponent, coefficient in poly.items()}


def singular(poly):
    pieces = []
    for exponent, coefficient in sorted(poly.items()):
        factors = []
        for index, power in enumerate(exponent):
            if not power:
                continue
            name = ("a" if index < 6 else "b") + str(index % 6)
            factors.append(name + (f"^{power}" if power != 1 else ""))
        body = "*".join(factors) or "1"
        magnitude = abs(coefficient)
        if magnitude != 1:
            body = f"{magnitude.numerator}/{magnitude.denominator}*{body}"
        prefix = "-" if coefficient < 0 else ("+" if pieces else "")
        pieces.append(prefix + body)
    return "".join(pieces) if pieces else "0"


def branch_bits(mask):
    return tuple((mask >> edge) & 1 for edge in range(6))


def branch_weight(mask):
    bits = branch_bits(mask)
    b01, b02, b03, b12, b13, b23 = bits
    return sum((b01 ^ b02 ^ b12, b01 ^ b03 ^ b13,
                b02 ^ b03 ^ b23, b12 ^ b13 ^ b23))


def raw_labels(mask):
    labels = ["e_" + "".join(map(str, edge)) for edge in EDGES]
    labels += ["t_" + "".join(map(str, triple))
               for triple in combinations(range(4), 3)]
    for edge, bit in enumerate(branch_bits(mask)):
        for position in ((1, 2) if bit else (0, 3)):
            labels.append(f"cofactor_{edge}_{position}")
    return tuple(labels)


def derived_rows(branch, term_mask, deduplicate=True):
    equations, _ = PROBE.equations(branch_bits(branch))
    labels = raw_labels(branch)
    require(len(equations) == len(labels) == 22,
            "raw base/cofactor row count changed")
    entries = aligned_entries(term_mask)
    rows = []
    seen = set()
    for label, raw in zip(labels, equations):
        specialized = clear_denominators(substitute(raw, entries))
        if not specialized:
            continue
        encoded = singular(specialized)
        if deduplicate and encoded in seen:
            continue
        seen.add(encoded)
        rows.append((label, specialized, encoded))
    return tuple(rows)


def act_mask(mask, switches, permutation):
    answer = 0
    edge_index = {edge: index for index, edge in enumerate(EDGES)}
    for index, (left, right) in enumerate(EDGES):
        bit = ((mask >> index) & 1) ^ switches[left] ^ switches[right]
        target = edge_index[tuple(sorted((permutation[left],
                                          permutation[right])))]
        answer |= bit << target
    return answer


def joint_representatives():
    actions = tuple((switches, permutation)
                    for switches in product((0, 1), repeat=4)
                    for permutation in permutations(range(4)))
    unseen = {(branch, term) for branch in range(64) for term in range(64)}
    records = []
    while unseen:
        representative = min(unseen)
        orbit = {(act_mask(representative[0], *action),
                  act_mask(representative[1], *action))
                 for action in actions}
        unseen -= orbit
        records.append((representative[0], representative[1], len(orbit)))
    require(len(actions) == 384 and len(records) == 50
            and sum(row[2] for row in records) == 4096,
            "joint B4 orbit census changed")
    return tuple(records)


def live_product(term_mask):
    return "*".join(("b" if term_mask >> edge & 1 else "a") + str(edge)
                    for edge in range(6))


def variables():
    return ",".join([f"a{index}" for index in range(6)]
                    + [f"b{index}" for index in range(6)] + ["z"])


def status_over(rows, term_mask, characteristic):
    ideal = ",".join(encoded for _, _, encoded in rows)
    program = (
        f"ring R={characteristic},({variables()}),dp;"
        f"ideal I={ideal},z*{live_product(term_mask)}-1;"
        "ideal G=slimgb(I);poly q=reduce(1,G);"
        'if(q==0){print("UNIT");}else{print("NONUNIT");};'
    )
    completed = subprocess.run(["Singular", "-q", "-c", program],
                               text=True, capture_output=True,
                               timeout=30, check=False)
    require(completed.returncode == 0 and not completed.stderr.strip(),
            "Singular status run failed: " + completed.stderr[-500:])
    tokens = completed.stdout.split()
    require(("UNIT" in tokens) ^ ("NONUNIT" in tokens),
            "Singular status marker missing")
    return "UNIT" if "UNIT" in tokens else "NONUNIT"


def exact_lift(rows, term_mask):
    ideal = ",".join(encoded for _, _, encoded in rows)
    program = (
        f"ring R=0,({variables()}),dp;"
        f"ideal I={ideal},z*{live_product(term_mask)}-1;"
        "matrix L=lift(I,ideal(1));matrix MI[1][size(I)]=I;"
        "matrix C=MI*L;print(\"BEGIN_CHECK\");print(string(C[1,1]));"
        "print(\"END_CHECK\");"
        "for(int i=1;i<=nrows(L);i++){if(L[i,1]!=0){"
        "print(\"BEGIN_MULT\");print(i);print(string(L[i,1]));"
        "print(\"END_MULT\");}};"
        "poly MUT=C[1,1];"
        "for(int j=1;j<nrows(L);j++){MUT=MUT-I[j]*L[j,1];};"
        "print(\"BEGIN_MUT\");print(string(MUT-1));print(\"END_MUT\");"
    )
    completed = subprocess.run(["Singular", "-q", "-c", program],
                               text=True, capture_output=True,
                               timeout=30, check=False)
    require(completed.returncode == 0 and not completed.stderr.strip(),
            "Singular lift failed: " + completed.stderr[-500:])
    lines = [line.strip() for line in completed.stdout.splitlines()]
    begin, end = lines.index("BEGIN_CHECK"), lines.index("END_CHECK")
    require("".join(lines[begin + 1:end]) == "1",
            "exact lift did not replay to one")
    multipliers = []
    cursor = 0
    while "BEGIN_MULT" in lines[cursor:]:
        begin = lines.index("BEGIN_MULT", cursor)
        end = lines.index("END_MULT", begin)
        index = int(lines[begin + 1]) - 1
        text = "".join(lines[begin + 2:end])
        labels = [label for label, _, _ in rows] + ["saturation"]
        multipliers.append({"label": labels[index], "polynomial": text})
        cursor = end + 1
    begin, end = lines.index("BEGIN_MUT"), lines.index("END_MUT")
    mutation = "".join(lines[begin + 1:end])
    require(mutation not in ("", "0"),
            "deleting all source-row summands did not fire")
    ledger = json.dumps(multipliers, sort_keys=True,
                        separators=(",", ":"))
    return {
        "used_source_labels": [row["label"] for row in multipliers
                               if row["label"] != "saturation"],
        "source_row_count": sum(row["label"] != "saturation"
                                for row in multipliers),
        "multipliers": multipliers,
        "multiplier_ledger_sha256": sha256(ledger.encode("ascii")).hexdigest(),
        "exact_product_check": "1",
        "deletion_mutation_nonzero": mutation,
    }


def deserialize_weight4(rows):
    return {tuple(record["exponents_a0_a5_b0_b5_z"]):
            Fraction(*record["coefficient"]) for record in rows}


def embed_z(poly):
    return {tuple(exponent) + (0,): coefficient
            for exponent, coefficient in poly.items()}


def referee_weight4():
    frozen = json.loads(WEIGHT4_RESULT.read_text())
    require(frozen["branch_mask"] == 11
            and frozen["source_term_count"] == 5,
            "weight-four frozen header changed")
    rows = {label: embed_z(poly) for label, poly, _
            in derived_rows(11, 63, deduplicate=False)}
    def multiply13(*polys):
        answer = {(0,) * 13: Fraction(1)}
        for poly in polys:
            updated = Counter()
            for left, left_coefficient in answer.items():
                for right, right_coefficient in poly.items():
                    updated[tuple(a + b for a, b in zip(left, right))] += (
                        left_coefficient * right_coefficient
                    )
            answer = clean(updated)
        return answer
    packet = {}
    for record in frozen["source_terms"]:
        label = record["label"]
        stored_row = deserialize_weight4(record["cleared_source_row"])
        multiplier = deserialize_weight4(record["multiplier"])
        require(label in rows and stored_row == rows[label],
                f"weight-four raw row mismatch for {label}")
        packet = add(packet, multiply13(multiplier, stored_row))
    target = deserialize_weight4(frozen["target"])
    require(packet == target, "weight-four five-row ledger did not replay")
    final_record = frozen["source_terms"][-1]
    mutation = add(packet, scale(multiply13(
        deserialize_weight4(final_record["multiplier"]),
        deserialize_weight4(final_record["cleared_source_row"])), -1))
    require(mutation != target, "weight-four deletion mutation did not fire")
    return {
        "producer_logical_sha256": frozen["result_sha256"],
        "used_labels": [record["label"] for record in frozen["source_terms"]],
        "raw_rows_independently_rebuilt": True,
        "packet_equals_target": True,
        "deletion_mutation_fired": True,
    }


def main():
    weight4 = referee_weight4()
    records = []
    status_counts = Counter()
    source_count_histogram = Counter()
    for branch, term_mask, orbit_size in joint_representatives():
        rows = derived_rows(branch, term_mask)
        statuses = {str(characteristic): status_over(
            rows, term_mask, characteristic)
            for characteristic in (1009, 1013, 0)}
        require(len(set(statuses.values())) == 1,
                "prime/Q status mismatch")
        status = statuses["0"]
        record = {
            "branch_mask": branch,
            "branch_weight": branch_weight(branch),
            "permanent_term_mask": term_mask,
            "joint_orbit_size": orbit_size,
            "aligned_zero_cells": [4 * edge + (3 if term_mask >> edge & 1 else 2)
                                   for edge in range(6)],
            "derived_row_count": len(rows),
            "derived_row_labels": [label for label, _, _ in rows],
            "statuses": statuses,
        }
        if status == "UNIT":
            record["exact_lift"] = exact_lift(rows, term_mask)
            source_count_histogram[record["exact_lift"][
                "source_row_count"]] += 1
        records.append(record)
        status_counts[status] += 1
    require(status_counts == {"UNIT": 43, "NONUNIT": 7},
            "50-chart unit census changed")
    survivors = [(record["branch_mask"], record["permanent_term_mask"])
                 for record in records if record["statuses"]["0"] == "NONUNIT"]
    require(survivors == [(0, 12), (0, 30), (0, 63),
                          (1, 12), (1, 38), (1, 63), (11, 21)],
            "aligned-chart survivor set changed")
    result = {
        "status": "UNAUDITED exact 50-orbit aligned-zero chart census",
        "chart_definition": (
            "term bit1: [[a,b],[-1/b,0]]; term bit0: "
            "[[a,b],[0,-1/a]], with the six selected Laurent variables nonzero"
        ),
        "joint_action": "simultaneous full B4 action on branch and term masks",
        "joint_representative_count": len(records),
        "status_counts": dict(status_counts),
        "unit_source_row_count_histogram": {
            str(key): value for key, value in sorted(source_count_histogram.items())},
        "nonunit_survivors": [list(row) for row in survivors],
        "weight4_five_row_referee": weight4,
        "records": records,
        "scope": (
            "Exact only for the displayed aligned zero-cell boundary charts. "
            "A NONUNIT is a survivor, not a point; no result is inferred for "
            "the full 24-variable permanent-term open charts."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("joint aligned-zero chart census: PASS")
    print("unit / nonunit:", status_counts["UNIT"], status_counts["NONUNIT"])
    print("survivors:", survivors)
    print("source-row histogram:", dict(sorted(source_count_histogram.items())))
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
