#!/usr/bin/env python3
"""Independent strict referee for the affine-251 orbit membership solver.

The deep degree-eight mode independently rebuilds the stabilizer action,
homogenized provider, complete orbit incidence closure, Reynolds matrix,
modular rank test, and separating dual.  It does not invoke the Rust solver.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
import struct
import sys
import time
import traceback
from collections import Counter, defaultdict, deque
from fractions import Fraction
from pathlib import Path

GROUP_ORDER = 1440
N_WORDS = 6561
T = 251
MAX_DEGREE = 12
FIXED_ORIGINAL = 27 * 9 + 1
INPUT_SHA = "75a82d82a979d75507e682fd339e83d4ae35949653d624fb541148bd3957dcff"
SECONDARY_INPUT_SHA = "daa427528bbbeece064b09396023b66f32b804ba6d304178d19ced13e9b38a4e"
ALLOWED_PRIMES = {1073741827, 1073741789, 1073741783}
D8_PINS = {
    "row_orbits": 1418,
    "column_orbits": 116,
    "rank": 107,
    "matrix_nnz": 3848,
}


def reject(message: str) -> None:
    raise AssertionError(message)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            h.update(block)
    return h.hexdigest()


def edges():
    values = list(itertools.combinations(range(8), 2))
    assert len(values) == 28
    ids = {}
    for index, (a, b) in enumerate(values):
        ids[a, b] = ids[b, a] = index
    return values, ids


EDGES, EDGE_ID = edges()


def coordinate_name(original: int) -> str:
    edge, cell = divmod(original, 9)
    a, b = divmod(cell, 3)
    u, v = EDGES[edge]
    return f"x{u}{v}_{a}{b}"


def encode_word(word: tuple[int, ...]) -> int:
    answer = 0
    for value in word:
        answer = 3 * answer + value
    return answer


def decode_word(code: int) -> tuple[int, ...]:
    answer = [0] * 8
    for index in range(7, -1, -1):
        answer[index] = code % 3
        code //= 3
    return tuple(answer)


def build_actions(header: list[str]):
    expected = [coordinate_name(i) for i in range(252) if i != FIXED_ORIGINAL]
    assert header == expected and coordinate_name(FIXED_ORIGINAL) == "x67_01"
    original_to_affine = [T] * 252
    for affine, original in enumerate(i for i in range(252) if i != FIXED_ORIGINAL):
        original_to_affine[original] = affine
    actions = []
    for permutation in itertools.permutations(range(6)):
        for flip in range(2):
            sites = tuple(permutation) + ((6, 7) if not flip else (7, 6))
            colours = (0, 1, 2) if not flip else (1, 0, 2)
            varmap = [0] * 252
            for affine in range(251):
                original = affine if affine < FIXED_ORIGINAL else affine + 1
                edge, cell = divmod(original, 9)
                ca, cb = divmod(cell, 3)
                u, v = EDGES[edge]
                mu, mv = sites[u], sites[v]
                ma, mb = colours[ca], colours[cb]
                if mu > mv:
                    mu, mv, ma, mb = mv, mu, mb, ma
                moved = EDGE_ID[mu, mv] * 9 + ma * 3 + mb
                varmap[affine] = original_to_affine[moved]
            varmap[T] = T
            actions.append((sites, colours, tuple(varmap)))
    assert len(actions) == GROUP_ORDER
    return actions


def parse_provider(path: Path):
    lines = path.read_text().splitlines()
    header = lines[0].split(",")
    assert len(header) == 251 and lines[1] == "32003" and len(lines) == 6563
    variable = {name: index for index, name in enumerate(header)}
    polynomials = []
    parsed = 0
    for raw in lines[2:]:
        aggregate = Counter()
        for token in raw.rstrip(",").replace("-1", "+-1").split("+"):
            if not token:
                continue
            parsed += 1
            if token == "-1":
                aggregate[(T,) * 4] -= 1
            else:
                values = [variable[x] for x in token.split("*") if x != "1"]
                values += [T] * (4 - len(values))
                aggregate[tuple(sorted(values))] += 1
        polynomial = tuple(sorted((term, value) for term, value in aggregate.items() if value))
        assert polynomial
        polynomials.append(polynomial)
    term_index = defaultdict(list)
    for word, polynomial in enumerate(polynomials):
        for term, _ in polynomial:
            term_index[term].append(word)
    assert len(polynomials) == 6561 and parsed == 688908 and len(term_index) == 688906
    return header, polynomials, term_index


class IndependentEngine:
    def __init__(self, actions, polynomials, term_index):
        self.actions = actions
        self.polynomials = polynomials
        self.term_index = term_index
        self.row_cache = {}
        self.column_cache = {}

    def move_row(self, row, action):
        return tuple(sorted(action[2][value] for value in row))

    def row_info(self, row):
        if row in self.row_cache:
            return self.row_cache[row]
        canonical = row
        stabilizer = 0
        for action in self.actions:
            moved = self.move_row(row, action)
            canonical = min(canonical, moved)
            stabilizer += moved == row
        assert stabilizer and GROUP_ORDER % stabilizer == 0
        answer = canonical, stabilizer
        self.row_cache[row] = answer
        self.row_cache.setdefault(canonical, answer)
        return answer

    @staticmethod
    def move_word(word, sites, colours):
        moved = [0] * 8
        for site in range(8):
            moved[sites[site]] = colours[word[site]]
        return tuple(moved)

    def canonical_column(self, column):
        if column in self.column_cache:
            return self.column_cache[column]
        word = decode_word(column[0])
        answer = column
        for sites, colours, varmap in self.actions:
            moved_word = encode_word(self.move_word(word, sites, colours))
            moved_multiplier = tuple(sorted(varmap[x] for x in column[1]))
            answer = min(answer, (moved_word, moved_multiplier))
        self.column_cache[column] = answer
        self.column_cache.setdefault(answer, answer)
        return answer

    @staticmethod
    def divisors(row):
        answer = set()
        for positions in itertools.combinations(range(len(row)), 4):
            selected = set(positions)
            divisor = tuple(row[i] for i in positions)
            multiplier = tuple(row[i] for i in range(len(row)) if i not in selected)
            answer.add((divisor, multiplier))
        return answer

    def incident(self, row):
        answer = set()
        for divisor, multiplier in self.divisors(row):
            for word in self.term_index.get(divisor, ()):
                answer.add(self.canonical_column((word, multiplier)))
        return answer

    def outputs(self, column):
        word, multiplier = column
        return {self.row_info(tuple(sorted(multiplier + term)))[0]
                for term, coefficient in self.polynomials[word] if coefficient}

    def invariant_column(self, column, prime):
        word, multiplier = column
        aggregate = Counter()
        for term, coefficient in self.polynomials[word]:
            row = tuple(sorted(multiplier + term))
            canonical, _ = self.row_info(row)
            aggregate[canonical] += coefficient
        answer = {}
        for row, coefficient in aggregate.items():
            value = coefficient * self.row_info(row)[1] % prime
            if value:
                answer[row] = value
        return answer

    def invariant_column_integer(self, column):
        word, multiplier = column
        aggregate = Counter()
        for term, coefficient in self.polynomials[word]:
            row = tuple(sorted(multiplier + term))
            canonical, _ = self.row_info(row)
            aggregate[canonical] += coefficient
        return {row: coefficient * self.row_info(row)[1]
                for row, coefficient in aggregate.items() if coefficient}


def read_checkpoint(path: Path, degree: int):
    data = memoryview(path.read_bytes())
    offset = 0
    assert bytes(data[:12]) == b"AFF251CL1\0\0\0"
    offset += 12
    assert data[offset] == degree and data[offset + 1] == 1
    offset += 2
    nr, nc, nrf, ncf = struct.unpack_from("<QQQQ", data, offset)
    offset += 32

    def mono():
        nonlocal offset
        length = data[offset]
        values = tuple(data[offset + 1: offset + 1 + length])
        padding = data[offset + 1 + length: offset + 13]
        assert length <= 12 and list(values) == sorted(values) and not any(padding)
        offset += 13
        return values

    rows = [mono() for _ in range(nr)]
    columns = []
    for _ in range(nc):
        word = struct.unpack_from("<H", data, offset)[0]
        offset += 2
        columns.append((word, mono()))
    row_frontier = [mono() for _ in range(nrf)]
    column_frontier = []
    for _ in range(ncf):
        word = struct.unpack_from("<H", data, offset)[0]
        offset += 2
        column_frontier.append((word, mono()))
    assert offset == len(data) and rows == sorted(set(rows)) and columns == sorted(set(columns))
    assert not row_frontier and not column_frontier
    return set(rows), set(columns)


def exact_closure(engine: IndependentEngine, degree: int):
    target = (T,) * degree
    target = engine.row_info(target)[0]
    rows, columns = {target}, set()
    rq, cq = deque([target]), deque()
    while rq or cq:
        while rq:
            for column in engine.incident(rq.popleft()):
                if column not in columns:
                    columns.add(column)
                    cq.append(column)
        while cq:
            for row in engine.outputs(cq.popleft()):
                if row not in rows:
                    rows.add(row)
                    rq.append(row)
    return rows, columns


def subtract_scaled(vector, record, factor, prime):
    for row, coefficient in record.items():
        value = (vector.get(row, 0) - factor * coefficient) % prime
        if value:
            vector[row] = value
        else:
            vector.pop(row, None)


def independent_rank(matrix, target, prime, pivot_last=False):
    basis = {}
    for original in matrix:
        vector = dict(original)
        while vector:
            pivot = max(vector) if pivot_last else min(vector)
            if pivot not in basis:
                inverse = pow(vector[pivot], prime - 2, prime)
                basis[pivot] = {row: value * inverse % prime for row, value in vector.items()}
                break
            subtract_scaled(vector, basis[pivot], vector[pivot], prime)
    residual = dict(target)
    while residual:
        pivot = max(residual) if pivot_last else min(residual)
        if pivot not in basis:
            break
        subtract_scaled(residual, basis[pivot], residual[pivot], prime)
    return len(basis), residual


def parse_dual(path: Path, prime: int, rows):
    lines = path.read_text().splitlines()
    head = lines[0].split()
    assert head[:2] == ["KRENN_AFFINE251_ORBIT_DUAL_V1", str(prime)]
    expected, pairing = map(int, head[2:])
    answer = {}
    for line in lines[1:]:
        tag, row_id, row_hex, value = line.split()
        row_id, value = int(row_id), int(value)
        assert tag == "ROW" and 0 <= row_id < len(rows) and 0 < value < prime
        assert row_hex == "".join(f"{x:02x}" for x in rows[row_id])
        assert row_id not in answer
        answer[row_id] = value
    assert len(answer) == expected
    return answer, pairing


def lift_rational_dual(primary, secondary, p1, p2):
    answer = {}
    for row in set(primary) | set(secondary):
        a, b = primary.get(row, 0), secondary.get(row, 0)
        signed_a = a if a <= p1 // 2 else a - p1
        signed_b = b if b <= p2 // 2 else b - p2
        if signed_a == signed_b:
            answer[row] = Fraction(signed_a)
            continue
        lifted = None
        for denominator in range(2, 1025):
            numerator_a, numerator_b = denominator * a % p1, denominator * b % p2
            numerator_a = numerator_a if numerator_a <= p1 // 2 else numerator_a - p1
            numerator_b = numerator_b if numerator_b <= p2 // 2 else numerator_b - p2
            if numerator_a == numerator_b and abs(numerator_a) < 10_000_000:
                lifted = Fraction(numerator_a, denominator)
                break
        assert lifted is not None
        answer[row] = lifted
    return {row: value for row, value in answer.items() if value}


def validate_result(data, degree=None):
    assert data["schema"] == "KRENN_AFFINE251_ORBIT_MEMBERSHIP_V1"
    assert data["status"] in {"COMPLETE_NONMEMBER_MOD_PRIME", "COMPLETE_MEMBER_MOD_PRIME"}
    assert data["incomplete_reason"] is None and data["closure_complete"] is True
    assert data["variables_affine"] == 251 and data["homogenizing_variable"] == 251
    assert data["provider_equations"] == 6561 and data["provider_terms_parsed"] == 688908
    assert data["provider_distinct_terms"] == 688906 and data["group_order"] == 1440
    assert data["prime"] in ALLOWED_PRIMES and 4 <= data["degree"] <= 12
    if degree is not None:
        assert data["degree"] == degree
    assert data["wall_limit_seconds"] <= 1800 and data["rss_limit_gib"] <= 42
    assert 0 < data["peak_rss_kib"] < 42 * 1024 * 1024
    assert data["elapsed_seconds"] < data["wall_limit_seconds"]
    assert data["row_orbits"] > 0 and data["column_orbits"] > 0
    assert 0 <= data["rank"] <= min(data["row_orbits"], data["column_orbits"])
    if data["status"] == "COMPLETE_NONMEMBER_MOD_PRIME":
        assert data["member_mod_prime"] is False
        assert data["target_residual_nnz"] > 0 and data["target_pairing"] != 0
    else:
        assert data["member_mod_prime"] is True
        assert data["target_residual_nnz"] == 0
    if data["degree"] == 8:
        for key, value in D8_PINS.items():
            assert data[key] == value


def hostile_selftest(data):
    mutations = [
        ("schema", "FORGED"), ("status", "COMPLETE_NONMEMBER_MOD_PRIME" if data["member_mod_prime"] else "COMPLETE_MEMBER_MOD_PRIME"),
        ("group_order", 1439), ("provider_terms_parsed", 688907), ("closure_complete", False),
        ("target_residual_nnz", 0), ("rank", data["column_orbits"] + 1),
        ("wall_limit_seconds", 1801), ("rss_limit_gib", 43),
    ]
    rejected = 0
    for key, value in mutations:
        forged = dict(data)
        forged[key] = value
        try:
            validate_result(forged, data["degree"])
        except (AssertionError, KeyError):
            rejected += 1
    assert rejected == len(mutations)
    return rejected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--input-secondary", type=Path)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--result-secondary", type=Path)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--dual", type=Path, required=True)
    parser.add_argument("--dual-secondary", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--deep", action="store_true")
    parser.add_argument("--exact-dual-only", action="store_true")
    args = parser.parse_args()
    started = time.monotonic()
    assert sha256(args.input) == INPUT_SHA
    if args.input_secondary:
        assert sha256(args.input_secondary) == SECONDARY_INPUT_SHA
        primary_lines = args.input.read_text().splitlines()
        secondary_lines = args.input_secondary.read_text().splitlines()
        assert primary_lines[0] == secondary_lines[0]
        assert primary_lines[1] == "32003" and secondary_lines[1] == "1073741827"
        assert primary_lines[2:] == secondary_lines[2:]
    primary = json.loads(args.result.read_text())
    validate_result(primary)
    hostiles = hostile_selftest(primary)
    secondary = None
    if args.result_secondary:
        secondary = json.loads(args.result_secondary.read_text())
        validate_result(secondary, primary["degree"])
        assert secondary["prime"] != primary["prime"]
        for key in ("status", "row_orbits", "column_orbits", "rank", "matrix_nnz",
                    "target_residual_nnz", "member_mod_prime"):
            assert secondary[key] == primary[key]
    checkpoint_rows, checkpoint_columns = read_checkpoint(args.checkpoint, primary["degree"])
    assert len(checkpoint_rows) == primary["row_orbits"]
    assert len(checkpoint_columns) == primary["column_orbits"]
    deep = None
    assert not (args.deep and args.exact_dual_only)
    if args.deep:
        degree = primary["degree"]
        header, polynomials, term_index = parse_provider(args.input)
        actions = build_actions(header)
        engine = IndependentEngine(actions, polynomials, term_index)
        exact_rows, exact_columns = exact_closure(engine, degree)
        assert exact_rows == checkpoint_rows and exact_columns == checkpoint_columns
        rows = sorted(exact_rows)
        row_id = {row: index for index, row in enumerate(rows)}
        matrix = []
        integer_matrix = []
        nnz = 0
        for column in sorted(exact_columns):
            values = {row_id[row]: value for row, value in engine.invariant_column(column, primary["prime"]).items()}
            matrix.append(values)
            integer_matrix.append({row_id[row]: value for row, value in engine.invariant_column_integer(column).items()})
            nnz += len(values)
        rank, residual = independent_rank(matrix, {row_id[(T,) * degree]: 1}, primary["prime"],
                                          primary.get("pivot_order") == "last")
        assert rank == primary["rank"] and nnz == primary["matrix_nnz"]
        assert len(residual) == primary["target_residual_nnz"]
        dual, declared_pairing = parse_dual(args.dual, primary["prime"], rows)
        assert all(sum(value * dual.get(row, 0) for row, value in column.items()) % primary["prime"] == 0
                   for column in matrix)
        pairing = dual.get(row_id[(T,) * degree], 0)
        assert pairing == declared_pairing == primary["target_pairing"] != 0
        exact_char0 = False
        exact_support = None
        exact_denominator = None
        exact_target_pairing = None
        if secondary is not None:
            assert args.dual_secondary is not None
            dual2, declared_pairing2 = parse_dual(args.dual_secondary, secondary["prime"], rows)
            assert declared_pairing2 == secondary["target_pairing"]
            rational_dual = lift_rational_dual(dual, dual2, primary["prime"], secondary["prime"])
            assert all(sum(value * rational_dual.get(row, 0) for row, value in column.items()) == 0
                       for column in integer_matrix)
            rational_pairing = rational_dual.get(row_id[(T,) * degree], Fraction(0))
            assert rational_pairing != 0
            exact_char0 = True
            exact_support = len(rational_dual)
            exact_denominator = max(value.denominator for value in rational_dual.values())
            exact_target_pairing = str(rational_pairing)
        deep = {
            "exact_row_set_equality": True, "exact_column_set_equality": True,
            "independent_rank": rank, "independent_nnz": nnz,
            "independent_target_residual_nnz": len(residual), "dual_pairing": pairing,
            "row_cache_entries": len(engine.row_cache), "column_cache_entries": len(engine.column_cache),
            "exact_char0_nonmembership": exact_char0,
            "exact_rational_dual_support": exact_support,
            "exact_rational_dual_max_denominator": exact_denominator,
            "exact_rational_target_pairing": exact_target_pairing,
        }
    elif args.exact_dual_only:
        assert secondary is not None and args.dual_secondary is not None
        degree = primary["degree"]
        header, polynomials, term_index = parse_provider(args.input)
        actions = build_actions(header)
        engine = IndependentEngine(actions, polynomials, term_index)
        rows = sorted(checkpoint_rows)
        dual1, declared1 = parse_dual(args.dual, primary["prime"], rows)
        dual2, declared2 = parse_dual(args.dual_secondary, secondary["prime"], rows)
        assert declared1 == primary["target_pairing"] and declared2 == secondary["target_pairing"]
        rational = lift_rational_dual(dual1, dual2, primary["prime"], secondary["prime"])
        rational_rows = {rows[row]: value for row, value in rational.items()}
        target_pairing = rational_rows.get((T,) * degree, Fraction(0))
        assert target_pairing != 0
        incident_columns = set()
        for row in rational_rows:
            incident_columns.update(engine.incident(row))
        for column in incident_columns:
            values = engine.invariant_column_integer(column)
            assert sum(value * rational_rows.get(row, 0) for row, value in values.items()) == 0
        deep = {
            "method": "support-local exact rational dual verification",
            "exact_char0_nonmembership": True,
            "exact_rational_dual_support": len(rational),
            "exact_rational_dual_max_denominator": max(value.denominator for value in rational.values()),
            "exact_rational_target_pairing": str(target_pairing),
            "all_incident_orbit_columns_checked": len(incident_columns),
            "global_annihilation_reason": "every column pairing outside the enumerated support incidence is zero by disjoint support",
            "row_cache_entries": len(engine.row_cache),
            "column_cache_entries": len(engine.column_cache),
        }
    report = {
        "schema": "KRENN_AFFINE251_ORBIT_MEMBERSHIP_AUDIT_V1",
        "status": "PASS",
        "input_sha256": sha256(args.input),
        "secondary_input_sha256": sha256(args.input_secondary) if args.input_secondary else None,
        "symbolic_input_equality_across_export_primes": args.input_secondary is not None,
        "result_sha256": sha256(args.result),
        "secondary_result_sha256": sha256(args.result_secondary) if args.result_secondary else None,
        "checkpoint_sha256": sha256(args.checkpoint),
        "dual_sha256": sha256(args.dual),
        "secondary_dual_sha256": sha256(args.dual_secondary) if args.dual_secondary else None,
        "degree": primary["degree"],
        "prime": primary["prime"],
        "hostile_mutations_rejected": hostiles,
        "dual_prime_agreement": secondary is not None,
        "deep_referee": deep,
        "elapsed_seconds": time.monotonic() - started,
    }
    tmp = args.output.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    os.replace(tmp, args.output)
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, KeyError, ValueError) as exc:
        print(f"REJECT: {exc}", file=sys.stderr)
        traceback.print_exc()
        raise SystemExit(2)
