#!/usr/bin/env python3
"""Bounded exact/modular lazy CEGAR for the first atlas boundary at D12."""

from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
import importlib.util
import json
from pathlib import Path
import resource
import time


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
EXPORT_PATH = HERE / "export_chart1_boundary.py"
ATLAS_PATH = (ROOT / "computations/unaudited-codex-n8-chart-c4-boundary-atlas-2026-08-23"
              / "audit_c4_boundary_atlas.py")
RESULT = HERE / "results_d12_lazy_cegar.json"
CHECKPOINT = HERE / "checkpoint_d12_lazy_cegar.json"
QQ = Fraction
PRIME = 1_073_741_827
TIME_CAP = 300.0
RSS_CAP = 12 * 1024 ** 3


class BoundedStop(Exception):
    pass


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise RuntimeError(path)
    spec.loader.exec_module(module)
    return module


E = load(EXPORT_PATH, "chart1_boundary_cegar_export")
A = load(ATLAS_PATH, "chart1_boundary_cegar_atlas")
D5 = E.D5


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def peak_rss():
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return int(value if value > 10_000_000 else value * 1024)


def check_cap(started, label):
    elapsed = time.monotonic() - started
    rss = peak_rss()
    if elapsed > TIME_CAP or rss > RSS_CAP:
        raise BoundedStop({"label": label, "elapsed_seconds": elapsed,
                           "peak_rss_bytes": rss})


def transformed_identifier(identifier, element):
    vp, cp = element
    i, j, a, b = D5.COORDINATES[identifier]
    ni, nj, na, nb = vp[i], vp[j], cp[a], cp[b]
    if ni > nj:
        ni, nj, na, nb = nj, ni, nb, na
    return E.COORDINATE_ID[ni, nj, na, nb]


def transformed_code(code, element):
    vp, cp = element
    source = D5.decode_word(code)
    target = [None] * 8
    for site, colour in enumerate(source):
        target[vp[site]] = cp[colour]
    return D5.word_code(tuple(target))


class Provider:
    def __init__(self):
        chart_rows = tuple(sorted(A.SOURCE.target_orbit_rows()))
        full_group = A.stabilizer(chart_rows[0])
        self.group = tuple(element for element in full_group
                           if A.transform_edge((0, 6), element) == (0, 6))
        require(len(self.group) == 32, "boundary stabilizer changed")
        self.transforms = tuple(tuple(transformed_identifier(i, element)
                                      for i in range(252))
                                for element in self.group)
        self.mixed_codes = tuple(code for code in range(3 ** 8)
                                 if len(set(D5.decode_word(code))) > 1)
        self.term_index = defaultdict(list)
        for code in self.mixed_codes:
            for term in self.generator(code):
                self.term_index[term].append(code)
        self.pure = tuple(self.generator(D5.word_code((colour,) * 8))
                          for colour in range(3))

    @lru_cache(None)
    def generator(self, code):
        return dict(E.normalized_generator(code))

    @lru_cache(None)
    def row_orbit(self, row):
        return tuple(sorted(set(bytes(sorted(transform[value] for value in row))
                                    for transform in self.transforms)))

    def canonical_row(self, row):
        return self.row_orbit(row)[0]

    @lru_cache(None)
    def column_orbit(self, column):
        code, multiplier = column
        return tuple(sorted(set(
            (transformed_code(code, element),
             bytes(sorted(transform[value] for value in multiplier)))
            for element, transform in zip(self.group, self.transforms)
        )))

    def canonical_column(self, column):
        return self.column_orbit(column)[0]

    @lru_cache(None)
    def invariant_entries(self, column):
        answer = defaultdict(int)
        for code, multiplier in self.column_orbit(column):
            for term, coefficient in self.generator(code).items():
                row = bytes(sorted(multiplier + term))
                require(len(row) <= 12, "D12 column exceeded homogeneous degree")
                if row == self.canonical_row(row):
                    answer[row] += coefficient
        return dict(answer)

    @staticmethod
    def quotient(row, divisor):
        answer = list(row)
        for value in divisor:
            try:
                answer.remove(value)
            except ValueError:
                return None
        return bytes(answer)

    @lru_cache(None)
    def incident_columns_for_row(self, row):
        answer = set()
        for degree in range(min(4, len(row)) + 1):
            seen = set()
            for positions in combinations(range(len(row)), degree):
                term = bytes(row[position] for position in positions)
                if term in seen:
                    continue
                seen.add(term)
                multiplier = self.quotient(row, term)
                if multiplier is None or len(multiplier) > 8:
                    continue
                for code in self.term_index.get(term, ()):
                    answer.add(self.canonical_column((code, multiplier)))
        return tuple(sorted(answer))

    def incident_columns(self, functional):
        answer = set()
        for row in functional:
            answer.update(self.incident_columns_for_row(row))
        return answer

    @lru_cache(None)
    def target_coefficient(self, row, colour=0):
        if colour == 3:
            return int(not row)
        total = 0
        for term, coefficient in self.pure[colour].items():
            remainder = self.quotient(row, term)
            if remainder is not None:
                total += coefficient * self.target_coefficient(remainder, colour + 1)
        return total

    def full_target(self, started):
        actual = Counter()
        for left, cl in self.pure[0].items():
            for middle, cm in self.pure[1].items():
                prefix = bytes(sorted(left + middle))
                for right, cr in self.pure[2].items():
                    actual[bytes(sorted(prefix + right))] += cl * cm * cr
            check_cap(started, "expand_full_target")
        invariant = {}
        for row, coefficient in actual.items():
            representative = self.canonical_row(row)
            previous = invariant.setdefault(representative, coefficient)
            require(previous == coefficient, "Fh target lost boundary invariance")
        require(sum(actual.values()) == 90 * 105 * 105
                and actual.get(b"") == 1,
                "expanded Fh target changed")
        return actual, invariant


def add_scaled(target, source, scalar, prime=None):
    for key, value in source.items():
        result = target.get(key, 0) + scalar * value
        if prime is not None:
            result %= prime
        if result:
            target[key] = result
        else:
            target.pop(key, None)


def solve_span(provider, rows, columns, target, prime=None):
    ordered_rows = tuple(sorted(rows, key=lambda row: (len(row), row)))
    row_index = {row: index for index, row in enumerate(ordered_rows)}
    pivots = {}
    for position, column in enumerate(columns):
        if prime is None:
            vector = {row_index[row]: QQ(value)
                      for row, value in provider.invariant_entries(column).items()}
            expression = {position: QQ(1)}
        else:
            vector = {row_index[row]: value % prime
                      for row, value in provider.invariant_entries(column).items()
                      if value % prime}
            expression = None
        while vector:
            pivot = min(vector)
            value = vector[pivot]
            if pivot not in pivots:
                if prime is None:
                    inverse = 1 / value
                    vector = {key: coefficient * inverse
                              for key, coefficient in vector.items()}
                    expression = {key: coefficient * inverse
                                  for key, coefficient in expression.items()}
                    pivots[pivot] = (vector, expression)
                else:
                    inverse = pow(value, prime - 2, prime)
                    pivots[pivot] = ({key: coefficient * inverse % prime
                                     for key, coefficient in vector.items()}, None)
                break
            basis, basis_expression = pivots[pivot]
            add_scaled(vector, basis, -value, prime)
            if prime is None:
                add_scaled(expression, basis_expression, -value)

    if prime is None:
        work = {row_index[row]: QQ(value) for row, value in target.items() if value}
        solution = {}
    else:
        work = {row_index[row]: value % prime for row, value in target.items()
                if value % prime}
        solution = None
    while work:
        pivot = min(work)
        value = work[pivot]
        if pivot not in pivots:
            break
        basis, expression = pivots[pivot]
        add_scaled(work, basis, -value, prime)
        if prime is None:
            add_scaled(solution, expression, value)
    if not work:
        return len(pivots), {}, solution, {}, QQ(0)
    if prime is not None:
        return len(pivots), work, None, None, None

    selected = min(work)
    dual_index = {selected: QQ(1)}
    for pivot in sorted(pivots, reverse=True):
        basis, _expression = pivots[pivot]
        value = -sum(coefficient * dual_index.get(index, QQ(0))
                     for index, coefficient in basis.items() if index != pivot)
        if value:
            dual_index[pivot] = value
    dual = {ordered_rows[index]: value for index, value in dual_index.items()}
    pairing = sum(QQ(value) * dual.get(row, QQ(0)) for row, value in target.items())
    require(pairing != 0, "exact dual lost target pairing")
    return len(pivots), work, {}, dual, pairing


def exact_member_replay(provider, columns, solution, actual_target, started):
    image = defaultdict(QQ)
    for position, coefficient in solution.items():
        for code, multiplier in provider.column_orbit(columns[position]):
            for term, value in provider.generator(code).items():
                row = bytes(sorted(multiplier + term))
                result = image[row] + coefficient * value
                if result: image[row] = result
                else: image.pop(row, None)
        check_cap(started, "exact_member_replay")
    target = {row: QQ(value) for row, value in actual_target.items() if value}
    require(dict(image) == target, "selected invariant member failed literal replay")
    return {
        "selected_column_orbits": len(solution),
        "expanded_actual_columns": sum(len(provider.column_orbit(columns[index]))
                                       for index in solution),
        "expanded_rows": len(image),
        "solution": [[columns[index][0], columns[index][1].hex(),
                      value.numerator, value.denominator]
                     for index, value in sorted(solution.items())],
    }


def run():
    started = time.monotonic()
    provider = Provider()
    actual_target, target = provider.full_target(started)
    rows = set(target)
    constant_codes = [code for code in provider.mixed_codes
                      if b"" in provider.generator(code)]
    columns = {provider.canonical_column((code, b"")) for code in constant_codes}
    require(len(columns) == 18 and len(target) > 20_000,
            "D12 initialization changed")
    for column in columns:
        rows.update(provider.invariant_entries(column))

    ledger = []
    terminal = None
    stop = None
    try:
        while len(ledger) < 100:
            check_cap(started, f"round_{len(ledger)}_start")
            ordered_columns = tuple(sorted(columns))
            modular_rank, modular_remainder, _, _, _ = solve_span(
                provider, rows, ordered_columns, target, PRIME)
            check_cap(started, f"round_{len(ledger)}_modular")
            rank, remainder, solution, dual, pairing = solve_span(
                provider, rows, ordered_columns, target)
            require(rank == modular_rank
                    and bool(remainder) == bool(modular_remainder),
                    "exact/modular span status differs")
            check_cap(started, f"round_{len(ledger)}_exact")

            if solution:
                replay = exact_member_replay(
                    provider, ordered_columns, solution, actual_target, started
                )
                terminal = {"status": "EXACT_D12_MEMBER", "replay": replay}
                break

            candidates = provider.incident_columns(dual)
            violating = {}
            for index, column in enumerate(sorted(candidates), 1):
                value = sum(QQ(coefficient) * dual.get(row, QQ(0))
                            for row, coefficient in provider.invariant_entries(column).items())
                if value and column not in columns:
                    violating[column] = value
                if index % 512 == 0:
                    check_cap(started, f"round_{len(ledger)}_scan_{index}")
            record = {
                "round": len(ledger), "rows": len(rows), "columns": len(columns),
                "rank": rank, "target_support": len(target),
                "target_remainder_support": len(remainder),
                "dual_support": len(dual),
                "target_pairing": [pairing.numerator, pairing.denominator],
                "incident_column_orbits": len(candidates),
                "new_violating_column_orbits": len(violating),
                "violation_pairing_histogram": [
                    [[value.numerator, value.denominator], count]
                    for value, count in sorted(Counter(violating.values()).items())
                ],
            }
            ledger.append(record)
            print("round", record["round"], "rows/cols/rank/dual/inc/new=",
                  record["rows"], record["columns"], record["rank"],
                  record["dual_support"], record["incident_column_orbits"],
                  record["new_violating_column_orbits"], flush=True)
            CHECKPOINT.write_text(json.dumps({
                "format": "n8-chart1-boundary-d12-cegar-checkpoint-v1",
                "ledger": ledger,
                "selected_columns": [[code, multiplier.hex()]
                                     for code, multiplier in sorted(columns)],
                "last_dual": [[row.hex(), value.numerator, value.denominator]
                              for row, value in sorted(dual.items())],
            }, indent=2, sort_keys=True) + "\n")
            if not violating:
                # Incidence completeness makes this a full separator. Expand
                # every actual incident column, not just invariant sums.
                for column in candidates:
                    for actual in provider.column_orbit(column):
                        value = QQ(0)
                        for term, coefficient in provider.generator(actual[0]).items():
                            row = bytes(sorted(actual[1] + term))
                            representative = provider.canonical_row(row)
                            value += (dual.get(representative, QQ(0))
                                      / len(provider.row_orbit(representative))) * coefficient
                        require(value == 0, "expanded separator misses an actual column")
                terminal = {
                    "status": "EXACT_D12_NONMEMBER",
                    "dual": [[row.hex(), value.numerator, value.denominator]
                             for row, value in sorted(dual.items())],
                    "target_pairing": [pairing.numerator, pairing.denominator],
                    "incident_column_orbits": len(candidates),
                }
                break
            for column in violating:
                columns.add(column)
                rows.update(provider.invariant_entries(column))
        if terminal is None:
            stop = {"label": "round_guard", "elapsed_seconds": time.monotonic()-started,
                    "peak_rss_bytes": peak_rss()}
    except BoundedStop as error:
        stop = error.args[0]

    payload = {
        "format": "n8-chart1-boundary-d12-lazy-cegar-v1",
        "status": terminal["status"] if terminal else "D12_CEGAR_CAP_UNRESOLVED",
        "prime_guard": PRIME,
        "boundary_stabilizer_order": len(provider.group),
        "actual_target_support": len(actual_target),
        "invariant_target_support": len(target),
        "ledger": ledger,
        "terminal": terminal,
        "bounded_stop": stop,
        "elapsed_seconds": time.monotonic() - started,
        "peak_rss_bytes": peak_rss(),
        "scope": (
            "Full homogeneous degree12 Fh target and every literal mixed-generator column "
            "orbit incident to each selected dual, on chart1 all-anchor A_02[0,0]=0. "
            "D12 membership is not saturation/radical closure; cap is unresolved."
        ),
        "source_sha256": {
            str(EXPORT_PATH.relative_to(ROOT)): sha256(EXPORT_PATH.read_bytes()).hexdigest(),
            str(ATLAS_PATH.relative_to(ROOT)): sha256(ATLAS_PATH.read_bytes()).hexdigest(),
        },
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["logical_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("terminal", payload["status"], "rounds", len(ledger),
          "elapsed", payload["elapsed_seconds"], "rss", payload["peak_rss_bytes"])
    return payload


if __name__ == "__main__":
    run()
