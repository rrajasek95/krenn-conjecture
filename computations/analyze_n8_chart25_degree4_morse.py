#!/usr/bin/env python3
"""Target-directed zero-fill Morse contraction for chart-25 degree four."""

from array import array
from collections import Counter, defaultdict, deque
from fractions import Fraction
from functools import lru_cache
import importlib.util
import math
from pathlib import Path
import pickle
import sys


HERE = Path(__file__).resolve().parent
PEEL_CACHE = HERE / "certificates" / "n8_chart25_degree4_morse_peel.pkl"
SCHUR_CACHE_TEMPLATE = "n8_chart25_degree4_schur_{prime}.pkl"
QQ = Fraction


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


D4 = load("n8_chart25_d4_morse", "analyze_n8_chart25_degree4_bockstein.py")
BASE = D4.BASE


@lru_cache(maxsize=None)
def minimum_terms(word):
    degree = D4.word_minimum_degree(word)
    return tuple(term for term in BASE.word_terms(word)
                 if BASE.row_degree(term) == degree)


@lru_cache(maxsize=None)
def leading_entries(column):
    entries = Counter()
    for actual_column in BASE.column_orbit(column):
        word, multiplier = actual_column
        if BASE.row_degree(multiplier) + D4.word_minimum_degree(word) != 4:
            continue
        for term in minimum_terms(word):
            row = bytes(sorted(multiplier + term))
            if row == BASE.canonical_row(row):
                entries[row] += 1
    return dict(entries)


@lru_cache(maxsize=None)
def candidate_columns(row):
    seen = set()
    candidates = []
    for raw_column in BASE.incident_columns(row):
        word, multiplier = raw_column
        if BASE.row_degree(multiplier) + D4.word_minimum_degree(word) != 4:
            continue
        column = BASE.canonical_column(raw_column)
        if column in seen:
            continue
        seen.add(column)
        entries = leading_entries(column)
        if row in entries:
            candidates.append((column, entries))
    candidates.sort(key=lambda item: (len(item[1]), repr(item[0])))
    return tuple(candidates)


class MorseSearch:
    def __init__(self, maximum_support=12, maximum_depth=200):
        self.maximum_support = maximum_support
        self.maximum_depth = maximum_depth
        self.rules = {}
        self.attempts = Counter()

    def find(self, row, visiting=None, depth=0):
        if row in self.rules:
            return True
        if depth >= self.maximum_depth:
            self.attempts["depth"] += 1
            return False
        if visiting is None:
            visiting = set()
        if row in visiting:
            self.attempts["cycle"] += 1
            return False
        visiting.add(row)
        try:
            for column, entries in candidate_columns(row):
                if len(entries) > self.maximum_support:
                    break
                self.attempts[len(entries)] += 1
                children = [other for other in entries if other != row]
                checkpoint = set(self.rules)
                if all(self.find(child, visiting, depth + 1)
                       for child in children):
                    self.rules[row] = (column, entries)
                    return True
                # A failed branch may have installed valid independent rules;
                # keeping them can only enlarge the already-contracted set.
                del checkpoint
            return False
        finally:
            visiting.remove(row)


def exact_solution(residual, rules):
    """Back-substitute through a dependency DAG, then replay exactly."""
    needed = set(residual)
    order = []
    state = {}

    def visit(row):
        marker = state.get(row, 0)
        if marker == 2:
            return
        if marker == 1:
            raise RuntimeError("Morse rule cycle")
        state[row] = 1
        column, entries = rules[row]
        for child in entries:
            if child != row:
                visit(child)
        state[row] = 2
        order.append(row)

    for row in residual:
        visit(row)
    # A rule column for a parent contains only children preceding it in order.
    # Eliminate parents in reverse topological order, propagating into children.
    remainder = defaultdict(QQ, residual)
    solution = defaultdict(QQ)
    for row in reversed(order):
        value = remainder.get(row, QQ(0))
        if not value:
            continue
        column, entries = rules[row]
        scalar = -value / entries[row]
        solution[column] += scalar
        for output, coefficient in entries.items():
            updated = remainder.get(output, QQ(0)) + scalar * coefficient
            if updated:
                remainder[output] = updated
            else:
                remainder.pop(output, None)
    if remainder:
        raise RuntimeError(f"Morse quotient replay left {len(remainder)} rows")
    return dict(solution), order


def actual_replay(solution):
    actual, _ = D4.exact_degree4_tail()
    actual = defaultdict(QQ, actual)
    for position, (column, scalar) in enumerate(solution.items(), 1):
        for actual_column in BASE.column_orbit(column):
            for row in BASE.column_rows(actual_column):
                if BASE.row_degree(row) != 4:
                    continue
                value = actual[row] + scalar
                if value:
                    actual[row] = value
                else:
                    actual.pop(row, None)
        if position % 5000 == 0:
            print("actual replay", position, "/", len(solution),
                  "remaining", len(actual), flush=True)
    if actual:
        raise RuntimeError(f"actual replay left {len(actual)} rows")


def global_peel(census):
    """Construct the maximal zero-fill triangular minor of the d=4 block."""
    if PEEL_CACHE.exists():
        with PEEL_CACHE.open("rb") as stream:
            peel = pickle.load(stream)
        print("loaded zero-fill peel cache", PEEL_CACHE, flush=True)
        return peel
    rows = census["rows"][2]
    columns = census["columns"][2]
    row_index = {row: index for index, row in enumerate(rows)}
    supports = []
    coefficients = []
    incidence = [[] for _ in rows]
    active = array("B")
    support_histogram = Counter()
    for position, column in enumerate(columns, 1):
        entries = leading_entries(column)
        indexed = tuple(sorted((row_index[row], value)
                               for row, value in entries.items()))
        support = tuple(index for index, _ in indexed)
        values = tuple(value for _, value in indexed)
        supports.append(support)
        coefficients.append(values)
        active.append(len(support))
        support_histogram[len(support)] += 1
        for index in support:
            incidence[index].append(position - 1)
        if position % 10000 == 0:
            print("support scan", position, "/", len(columns),
                  "histogram", dict(support_histogram),
                  "minimum-term cache", minimum_terms.cache_info(), flush=True)
    queue = deque(index for index, count in enumerate(active) if count == 1)
    removed = bytearray(len(rows))
    pivot_column = array("i", [-1]) * len(rows)
    pivot_order = []
    while queue:
        column_index = queue.popleft()
        if active[column_index] != 1:
            continue
        pivot = next((index for index in supports[column_index]
                      if not removed[index]), None)
        if pivot is None:
            continue
        removed[pivot] = 1
        pivot_column[pivot] = column_index
        pivot_order.append(pivot)
        for neighbor in incidence[pivot]:
            if active[neighbor]:
                active[neighbor] -= 1
                if active[neighbor] == 1:
                    queue.append(neighbor)
        if len(pivot_order) % 10000 == 0:
            print("zero-fill pivots", len(pivot_order), "/", len(rows),
                  "queue", len(queue), flush=True)
    target_indices = tuple(row_index[row] for row in census["residuals"][2])
    missing = tuple(index for index in target_indices if not removed[index])
    print("zero-fill peel complete pivots", len(pivot_order),
          "target missing", len(missing),
          "support histogram", dict(support_histogram), flush=True)
    peel = (supports, coefficients, pivot_column, pivot_order,
            target_indices, missing, support_histogram, active, removed)
    PEEL_CACHE.parent.mkdir(parents=True, exist_ok=True)
    with PEEL_CACHE.open("wb") as stream:
        pickle.dump(peel, stream, protocol=5)
    print("wrote zero-fill peel cache", PEEL_CACHE,
          PEEL_CACHE.stat().st_size, flush=True)
    return peel


def peel_exact_solution(census, peel):
    (supports, coefficients, pivot_column, pivot_order, _, missing,
     _, _, _) = peel
    if missing:
        raise RuntimeError("target is not contained in zero-fill triangular minor")
    rows = census["rows"][2]
    columns = census["columns"][2]
    row_index = {row: index for index, row in enumerate(rows)}
    remainder = defaultdict(QQ, {
        row_index[row]: value for row, value in census["residuals"][2].items()
    })
    solution = {}
    for position, pivot in enumerate(reversed(pivot_order), 1):
        value = remainder.get(pivot, QQ(0))
        if not value:
            continue
        column_index = pivot_column[pivot]
        support = supports[column_index]
        values = coefficients[column_index]
        diagonal = values[support.index(pivot)]
        scalar = -value / diagonal
        solution[columns[column_index]] = scalar
        for row, coefficient in zip(support, values):
            updated = remainder.get(row, QQ(0)) + scalar * coefficient
            if updated:
                remainder[row] = updated
            else:
                remainder.pop(row, None)
        if position % 10000 == 0:
            print("exact back substitution", position, "/", len(pivot_order),
                  "solution", len(solution), "remainder", len(remainder),
                  flush=True)
    if remainder:
        raise RuntimeError(f"zero-fill replay left {len(remainder)} rows")
    return solution


class WeightedDSU:
    """Relations lambda_i = potential[i] lambda_parent(i) over F_p."""

    def __init__(self, size, prime):
        self.parent = array("i", range(size))
        self.potential = array("H", [1]) * size
        self.killed = bytearray(size)
        self.prime = prime

    def find(self, index):
        parent = self.parent[index]
        if parent == index:
            return index, 1
        root, upper = self.find(parent)
        value = self.potential[index] * upper % self.prime
        self.parent[index] = root
        self.potential[index] = value
        return root, value

    def relate(self, left, left_coefficient, right, right_coefficient):
        prime = self.prime
        left_root, left_value = self.find(left)
        right_root, right_value = self.find(right)
        if left_root == right_root:
            if (left_coefficient * left_value
                    + right_coefficient * right_value) % prime:
                self.killed[left_root] = 1
            return
        # lambda_right_root = factor * lambda_left_root.
        factor = (-left_coefficient * left_value
                  * pow(right_coefficient * right_value % prime,
                        -1, prime)) % prime
        self.parent[right_root] = left_root
        self.potential[right_root] = factor
        self.killed[left_root] |= self.killed[right_root]


def modular_core_quotient(census, peel, prime, return_projector=False):
    """Contract the 2-support core, then row-reduce its small hypergraph."""
    (supports, coefficients, _, pivot_order, _, _, _, active, removed) = peel
    dsu = WeightedDSU(len(removed), prime)
    two_columns = 0
    for support, values, count in zip(supports, coefficients, active):
        if count != 2:
            continue
        core = [(row, value % prime) for row, value in zip(support, values)
                if not removed[row]]
        if len(core) != 2:
            raise RuntimeError("active support count mismatch")
        dsu.relate(core[0][0], core[0][1], core[1][0], core[1][1])
        two_columns += 1
    roots = {}
    row_coordinates = {}
    killed_components = set()
    for row in range(len(removed)):
        if removed[row]:
            continue
        root, value = dsu.find(row)
        if dsu.killed[root]:
            killed_components.add(root)
            continue
        if root not in roots:
            roots[root] = len(roots)
        row_coordinates[row] = (roots[root], value)
    print("prime", prime, "two-support columns", two_columns,
          "core rows", len(removed) - len(pivot_order),
          "balanced roots", len(roots),
          "killed components", len(killed_components), flush=True)
    pivots = {}
    projected_zero = 0
    higher_columns = 0
    for position, (support, values, count) in enumerate(
            zip(supports, coefficients, active), 1):
        if count < 3:
            continue
        vector = {}
        for row, coefficient in zip(support, values):
            coordinate = row_coordinates.get(row)
            if coordinate is None:
                continue
            index, potential = coordinate
            value = (vector.get(index, 0)
                     + coefficient * potential) % prime
            if value:
                vector[index] = value
            else:
                vector.pop(index, None)
        if not vector:
            projected_zero += 1
            continue
        higher_columns += 1
        while vector:
            pivot = min(vector)
            value = vector[pivot]
            if pivot not in pivots:
                inverse = pow(value, -1, prime)
                pivots[pivot] = {
                    index: coefficient * inverse % prime
                    for index, coefficient in vector.items()
                }
                break
            for index, coefficient in pivots[pivot].items():
                new = (vector.get(index, 0) - value * coefficient) % prime
                if new:
                    vector[index] = new
                else:
                    vector.pop(index, None)
        if position % 100000 == 0:
            print("prime", prime, "hypergraph scan", position, "/",
                  len(supports), "rank", len(pivots), flush=True)
    rows = census["rows"][2]
    row_index = {row: index for index, row in enumerate(rows)}
    target = {}
    for row, rational in census["residuals"][2].items():
        coordinate = row_coordinates.get(row_index[row])
        if coordinate is None:
            continue
        index, potential = coordinate
        scalar = (rational.numerator
                  * pow(rational.denominator, -1, prime)) % prime
        value = (target.get(index, 0) + scalar * potential) % prime
        if value:
            target[index] = value
        else:
            target.pop(index, None)
    for pivot in sorted(pivots):
        value = target.get(pivot, 0)
        if value:
            subtract_scaled(target, pivots[pivot], value, prime)
    dual_dimension = len(roots) - len(pivots)
    full_rank = len(removed) - dual_dimension
    ledger = {
        "prime": prime,
        "zero_fill_rank": len(pivot_order),
        "two_support_columns": two_columns,
        "balanced_core_components": len(roots),
        "killed_core_components": len(killed_components),
        "higher_projected_columns": higher_columns,
        "higher_projected_zero": projected_zero,
        "higher_projected_rank": len(pivots),
        "dual_dimension": dual_dimension,
        "degree4_rank": full_rank,
        "target_consistent": not target,
        "target_remainder": len(target),
    }
    if not return_projector:
        return ledger
    projector = {
        "prime": prime,
        "row_coordinates": row_coordinates,
        "higher_pivots": pivots,
        "target_remainder": target,
        "root_dimension": len(roots),
    }
    return ledger, projector


def reduce_in_quotient(entries, projector):
    prime = projector["prime"]
    vector = {}
    coordinates = projector["row_coordinates"]
    for row, coefficient in entries.items():
        coordinate = coordinates.get(row)
        if coordinate is None:
            continue
        index, potential = coordinate
        value = (vector.get(index, 0) + coefficient * potential) % prime
        if value:
            vector[index] = value
        else:
            vector.pop(index, None)
    pivots = projector["higher_pivots"]
    # A free coordinate may precede later pivot coordinates.  Stopping at the
    # first free coordinate is sufficient only for a yes/no membership test;
    # it is *not* a quotient projection.  Sweep every pivot so transferred
    # lower-kernel tails cannot retain a hidden A4-image component.
    for pivot in sorted(pivots):
        value = vector.get(pivot, 0)
        if value:
            subtract_scaled(vector, pivots[pivot], value, prime)
    return vector


def regression_full_quotient_reduction():
    projector = {
        "prime": 1009,
        "row_coordinates": {0: (0, 1), 1: (1, 1), 2: (2, 1)},
        "higher_pivots": {1: {1: 1, 2: 3}},
    }
    # Coordinate zero is free and comes before pivot one.  The historical
    # early-stop bug returned all three entries instead of eliminating one.
    reduced = reduce_in_quotient({0: 5, 1: 7, 2: 11}, projector)
    if reduced != {0: 5, 2: (11 - 21) % 1009}:
        raise RuntimeError("full quotient-reduction regression failed")


def old_tail_entries(column, degree4_index):
    entries = Counter()
    for actual_column in BASE.column_orbit(column):
        for row in BASE.column_rows(actual_column):
            if BASE.row_degree(row) == 4 and row == BASE.canonical_row(row):
                entries[degree4_index[row]] += 1
    return dict(entries)


def subtract_scaled(vector, pivot_vector, scalar, prime):
    for index, coefficient in pivot_vector.items():
        value = (vector.get(index, 0) - scalar * coefficient) % prime
        if value:
            vector[index] = value
        else:
            vector.pop(index, None)


def lower_kernel_transfer(census, projector):
    """Transfer every kernel generator of the d<=3 block into the d=4 quotient."""
    prime = projector["prime"]
    rows2, rows3, rows4 = census["rows"]
    columns2, columns3, _ = census["columns"]
    index2 = {row: index for index, row in enumerate(rows2)}
    index3 = {row: index for index, row in enumerate(rows3)}
    index4 = {row: index for index, row in enumerate(rows4)}
    offset3 = len(rows2)
    lower_pivots = {}
    lower_tails = {}
    transfer_pivots = {}
    kernel_count = 0
    nonzero_transfers = 0
    total = len(columns2) + len(columns3)
    position = 0
    for family, columns in ((2, columns2), (3, columns3)):
        for column in columns:
            position += 1
            lower = {}
            if family == 2:
                for index, value in BASE.invariant_entries(column,
                                                             index2).items():
                    lower[index] = value % prime
            for index, value in D4.DEG3.invariant_entries(column,
                                                           index3).items():
                lower[offset3 + index] = value % prime
            tail = reduce_in_quotient(old_tail_entries(column, index4),
                                      projector)
            while lower:
                pivot = min(lower)
                value = lower[pivot]
                if pivot not in lower_pivots:
                    inverse = pow(value, -1, prime)
                    lower_pivots[pivot] = {
                        index: coefficient * inverse % prime
                        for index, coefficient in lower.items()
                    }
                    lower_tails[pivot] = {
                        index: coefficient * inverse % prime
                        for index, coefficient in tail.items()
                    }
                    break
                subtract_scaled(lower, lower_pivots[pivot], value, prime)
                subtract_scaled(tail, lower_tails[pivot], value, prime)
            else:
                kernel_count += 1
                while tail:
                    pivot = min(tail)
                    value = tail[pivot]
                    if pivot not in transfer_pivots:
                        inverse = pow(value, -1, prime)
                        transfer_pivots[pivot] = {
                            index: coefficient * inverse % prime
                            for index, coefficient in tail.items()
                        }
                        nonzero_transfers += 1
                        break
                    subtract_scaled(tail, transfer_pivots[pivot], value, prime)
            if position % 500 == 0:
                lower_tail_nnz = sum(map(len, lower_tails.values()))
                print("prime", prime, "lower Schur", position, "/", total,
                      "lower rank", len(lower_pivots),
                      "kernels", kernel_count,
                      "transfer rank", len(transfer_pivots),
                      "lower-tail nnz", lower_tail_nnz, flush=True)
    target = dict(projector["target_remainder"])
    for pivot in sorted(transfer_pivots):
        value = target.get(pivot, 0)
        if value:
            subtract_scaled(target, transfer_pivots[pivot], value, prime)
    state = {
        "projector": projector,
        "transfer_pivots": transfer_pivots,
        "target_remainder_after_transfer": target,
    }
    cache = (HERE / "certificates"
             / SCHUR_CACHE_TEMPLATE.format(prime=prime))
    with cache.open("wb") as stream:
        pickle.dump(state, stream, protocol=5)
    print("wrote Schur state", cache, cache.stat().st_size, flush=True)
    return {
        "prime": prime,
        "lower_rank": len(lower_pivots),
        "lower_kernel_dimension": kernel_count,
        "transfer_rank": len(transfer_pivots),
        "source_faithful_consistent": not target,
        "source_faithful_remainder": len(target),
    }


def main():
    regression_full_quotient_reduction()
    census = D4.load_or_build_census()
    if len(sys.argv) > 1 and sys.argv[1] == "state":
        prime = int(sys.argv[2])
        peel = global_peel(census)
        ledger, projector = modular_core_quotient(
            census, peel, prime, return_projector=True
        )
        print(ledger, flush=True)
        print(lower_kernel_transfer(census, projector), flush=True)
        return
    if len(sys.argv) == 1 or sys.argv[1] == "peel":
        peel = global_peel(census)
        for prime in (1009, 1013, 1019):
            ledger, projector = modular_core_quotient(
                census, peel, prime, return_projector=True
            )
            print(ledger, flush=True)
            print(lower_kernel_transfer(census, projector), flush=True)
        if peel[5]:
            return
        solution = peel_exact_solution(census, peel)
        values = Counter(solution.values())
        denominator_lcm = math.lcm(*(value.denominator
                                     for value in solution.values()))
        print("zero-fill exact solution support", len(solution),
              "denominator lcm", denominator_lcm,
              "distinct values", len(values), flush=True)
        print("common values", values.most_common(20), flush=True)
        actual_replay(solution)
        print("chart25 degree-four exact zero-fill replay: PASS", flush=True)
        return
    residual = census["residuals"][2]
    search = MorseSearch(
        maximum_support=int(sys.argv[1])
    )
    missing = []
    for position, row in enumerate(residual, 1):
        if not search.find(row):
            missing.append(row)
        if position % 100 == 0:
            print("Morse targets", position, "/", len(residual),
                  "rules", len(search.rules), "missing", len(missing),
                  "attempts", dict(search.attempts),
                  "candidate cache", candidate_columns.cache_info(), flush=True)
    print("Morse search complete rules", len(search.rules),
          "missing", len(missing), "attempts", dict(search.attempts), flush=True)
    if missing:
        return
    solution, order = exact_solution(residual, search.rules)
    values = Counter(solution.values())
    denominator_lcm = math.lcm(*(value.denominator
                                 for value in solution.values()))
    print("Morse exact solution support", len(solution),
          "dependency rows", len(order),
          "denominator lcm", denominator_lcm,
          "distinct values", len(values), flush=True)
    print("common values", values.most_common(20), flush=True)
    actual_replay(solution)
    print("chart25 degree-four exact Morse replay: PASS", flush=True)


if __name__ == "__main__":
    main()
