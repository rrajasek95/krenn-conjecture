#!/usr/bin/env python3
"""Extract and audit a source-faithful chart-25 degree-four dual.

The large calculation in ``analyze_n8_chart25_degree4_morse.py`` stores the
contracted degree-four quotient and the transferred lower-kernel image for a
prime.  This script turns that state into a *full* left functional on the
degree-two, degree-three, and degree-four row spaces.  Consequently the audit
can test the functional directly on every original column; it does not have
to trust a chosen basis of the 31,584 lower-kernel tails.

Modes::

    python3 -u extract_n8_chart25_degree4_dual.py extract 1009
    python3 -u extract_n8_chart25_degree4_dual.py audit 1009
    python3 -u extract_n8_chart25_degree4_dual.py reconstruct 1009 1013 1019

``reconstruct`` uses ordinary symmetric rational reconstruction followed by
an exact ``Fraction`` replay.  Failure of rational reconstruction is an
honest request for more primes, not evidence against the obstruction.
"""

from array import array
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import importlib.util
import heapq
import json
import math
from pathlib import Path
import pickle
import sys


HERE = Path(__file__).resolve().parent
CERTIFICATES = HERE / "certificates"
QQ = Fraction


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MORSE = load("n8_chart25_d4_dual_morse",
             "analyze_n8_chart25_degree4_morse.py")
D4 = MORSE.D4
BASE = MORSE.BASE


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def schur_path(prime):
    return CERTIFICATES / MORSE.SCHUR_CACHE_TEMPLATE.format(prime=prime)


def dual_path(prime):
    return CERTIFICATES / f"n8_chart25_degree4_dual_mod_{prime}.pkl"


def rational_path(primes):
    suffix = "_".join(map(str, primes))
    return CERTIFICATES / f"n8_chart25_degree4_dual_qq_{suffix}.pkl"


def load_data():
    census = D4.load_or_build_census()
    return census, MORSE.global_peel(census)


def fully_reduce(vector, pivots, prime):
    """Reduce at every pivot, even when an earlier free row is present."""
    vector = dict(vector)
    for pivot in sorted(pivots):
        value = vector.get(pivot, 0)
        if value:
            MORSE.subtract_scaled(vector, pivots[pivot], value, prime)
    return vector


def reduce_until_free(vector, pivots, prime):
    """Sparse triangular reduction without repeatedly scanning ``min``.

    Pivot tails never move to a smaller coordinate.  A heap therefore visits
    only coordinates actually exposed by reductions, which is crucial for
    the 17,224 transferred vectors with long tails.
    """
    vector = dict(vector)
    queue = list(vector)
    heapq.heapify(queue)
    while queue:
        pivot = heapq.heappop(queue)
        value = vector.get(pivot, 0)
        if not value:
            continue
        reducer = pivots.get(pivot)
        if reducer is None:
            return vector
        for index, coefficient in reducer.items():
            old = vector.get(index, 0)
            new = (old - value * coefficient) % prime
            if new:
                vector[index] = new
                if not old:
                    heapq.heappush(queue, index)
            else:
                vector.pop(index, None)
    return vector


def echelon_union(first, second, prime):
    """Re-echelon two triangular spanning families in a common quotient.

    The transfer calculation deliberately stops reducing a vector as soon as
    it reaches its first free coordinate.  A later cancellation can therefore
    expose a higher pivot in a transferred basis vector.  Its pivot label may
    overlap a higher pivot even though the *combined span* is correct.  A
    fresh complete reduction is required before dual back-substitution.
    """
    # ``first`` is already a triangular basis.  Re-reducing its 64,221
    # vectors completely would be quadratic and changes no span.
    pivots = dict(first)
    origins = Counter({"higher": len(first)})
    for position, old_pivot in enumerate(sorted(second), 1):
        vector = reduce_until_free(second[old_pivot], pivots, prime)
        if vector:
            pivot = min(vector)
            inverse = pow(vector[pivot], -1, prime)
            pivots[pivot] = {
                index: coefficient * inverse % prime
                for index, coefficient in vector.items()
            }
            origins["transfer"] += 1
        if position % 2000 == 0:
            print("common echelon transfer", position, "/", len(second),
                  "rank", origins["transfer"], flush=True)
    return pivots, origins


def fundamental_dual(pivots, free, prime):
    """Return the canonical annihilator taking value one on ``free``."""
    dual = {free: 1}
    for pivot in reversed(sorted(pivots)):
        value = sum(coefficient * dual.get(index, 0)
                    for index, coefficient in pivots[pivot].items()
                    if index != pivot) % prime
        if value:
            dual[pivot] = -value % prime
    return dual


def dot_mod(entries, values, prime):
    if hasattr(values, "get"):
        return sum(coefficient * values.get(index, 0)
                   for index, coefficient in entries.items()) % prime
    return sum(coefficient * values[index]
               for index, coefficient in entries.items()) % prime


def combined_lower_entries(family, column, row_indices):
    entries = {}
    if family == 2:
        entries.update(BASE.invariant_entries(column, row_indices[0]))
    offset = len(row_indices[0])
    entries.update({offset + index: value for index, value in
                    D4.DEG3.invariant_entries(column,
                                               row_indices[1]).items()})
    return entries


def modular_tail_scalar(column, degree4_index, lambda4, prime):
    return dot_mod(MORSE.old_tail_entries(column, degree4_index),
                   lambda4, prime)


def extend_through_peel(alpha, projector, peel, prime):
    supports, coefficients, pivot_column, pivot_order = peel[:4]
    number_rows = len(peel[8])
    values = array("H", [0]) * number_rows
    for row, (coordinate, potential) in projector["row_coordinates"].items():
        values[row] = potential * alpha.get(coordinate, 0) % prime
    for pivot in reversed(pivot_order):
        column = pivot_column[pivot]
        support = supports[column]
        entries = coefficients[column]
        diagonal = None
        total = 0
        for row, coefficient in zip(support, entries):
            if row == pivot:
                diagonal = coefficient
            else:
                total += coefficient * values[row]
        require(diagonal is not None and diagonal % prime,
                "peel pivot lost its diagonal")
        values[pivot] = -total * pow(diagonal, -1, prime) % prime
    return values


def solve_lower_dual(census, lambda4, prime):
    """Solve the lower transpose and audit every dependent lower column."""
    rows2, rows3, rows4 = census["rows"]
    columns2, columns3, _ = census["columns"]
    row_indices = ({row: index for index, row in enumerate(rows2)},
                   {row: index for index, row in enumerate(rows3)})
    degree4_index = {row: index for index, row in enumerate(rows4)}
    pivots = {}
    right_sides = {}
    rank_origins = Counter()
    dependent = 0
    total = len(columns2) + len(columns3)
    position = 0
    for family, columns in ((2, columns2), (3, columns3)):
        for column in columns:
            position += 1
            vector = {index: value % prime for index, value in
                      combined_lower_entries(family, column,
                                             row_indices).items()
                      if value % prime}
            # <lambda_lower, vector> = -<lambda4, tail>.
            right = -modular_tail_scalar(column, degree4_index,
                                          lambda4, prime) % prime
            while vector:
                pivot = min(vector)
                value = vector[pivot]
                if pivot not in pivots:
                    inverse = pow(value, -1, prime)
                    pivots[pivot] = {
                        index: coefficient * inverse % prime
                        for index, coefficient in vector.items()
                    }
                    right_sides[pivot] = right * inverse % prime
                    rank_origins[family] += 1
                    break
                MORSE.subtract_scaled(vector, pivots[pivot], value, prime)
                right = (right - value * right_sides[pivot]) % prime
            else:
                dependent += 1
                require(right == 0,
                        f"lower-kernel tail violates dual at column {position}")
            if position % 5000 == 0:
                print("lower transpose", position, "/", total,
                      "rank", len(pivots), "dependent", dependent,
                      flush=True)
    values = array("H", [0]) * (len(rows2) + len(rows3))
    for pivot in reversed(sorted(pivots)):
        tail = sum(coefficient * values[index]
                   for index, coefficient in pivots[pivot].items()
                   if index != pivot) % prime
        values[pivot] = (right_sides[pivot] - tail) % prime
    require(len(pivots) == 27904, "lower rank changed")
    require(dependent == 31584, "lower-kernel dimension changed")
    return values, dict(rank_origins), dependent


def target_pair(census, lower, degree4, prime):
    values = (lower[:len(census["rows"][0])],
              lower[len(census["rows"][0]):], degree4)
    pairing = 0
    for rows, residual, functional in zip(census["rows"],
                                           census["residuals"], values):
        index = {row: position for position, row in enumerate(rows)}
        for row, coefficient in residual.items():
            scalar = (coefficient.numerator
                      * pow(coefficient.denominator, -1, prime)) % prime
            pairing += scalar * functional[index[row]]
    return pairing % prime


def modular_extract(prime):
    require(prime < 65536, "array('H') cannot store this prime")
    state_file = schur_path(prime)
    require(state_file.exists(),
            f"missing {state_file}; rerun the Morse contraction for {prime}")
    census, peel = load_data()
    with state_file.open("rb") as stream:
        state = pickle.load(stream)
    projector = state["projector"]
    higher = projector["higher_pivots"]
    transfers = state["transfer_pivots"]
    pivots, union_origins = echelon_union(higher, transfers, prime)
    require(union_origins["higher"] == len(higher),
            "higher projected basis lost rank")
    require(0 < union_origins["transfer"] <= len(transfers),
            "corrected transferred rank is invalid")
    print("corrected union ranks", dict(union_origins),
          "combined", len(pivots), flush=True)
    # Start before the invalid early-stop transfer reduction.  This target is
    # already reduced through the higher family up to its first free row;
    # complete reduction through the corrected union gives its true normal
    # form.
    target = fully_reduce(projector["target_remainder"], pivots, prime)
    print("corrected target remainder", len(target), flush=True)
    require(target, "target unexpectedly lies in the source-faithful image")
    # The least surviving coordinate gives a deterministic fundamental dual.
    free = min(target)
    alpha = fundamental_dual(pivots, free, prime)
    require(dot_mod(target, alpha, prime) != 0,
            "fundamental dual missed its reduced target")
    lambda4 = extend_through_peel(alpha, projector, peel, prime)
    lower, lower_origins, dependent = solve_lower_dual(
        census, lambda4, prime
    )
    pairing = target_pair(census, lower, lambda4, prime)
    require(pairing != 0, "full modular dual has zero target pairing")
    payload = {
        "prime": prime,
        "free_coordinate": free,
        "alpha_support": len(alpha),
        "combined_pivot_origins": dict(union_origins),
        "lower": lower,
        "degree4": lambda4,
        "lower_rank_origins": lower_origins,
        "lower_dependent_columns": dependent,
        "target_pairing": pairing,
    }
    path = dual_path(prime)
    with path.open("wb") as stream:
        pickle.dump(payload, stream, protocol=5)
    print("wrote modular full dual", path, path.stat().st_size,
          "alpha support", len(alpha), "target pairing", pairing, flush=True)
    return payload


def modular_audit(prime, payload=None):
    census, peel = load_data()
    if payload is None:
        with dual_path(prime).open("rb") as stream:
            payload = pickle.load(stream)
    lower = payload["lower"]
    lambda4 = payload["degree4"]
    supports, coefficients = peel[:2]
    violations = 0
    for position, (support, values) in enumerate(
            zip(supports, coefficients), 1):
        value = sum(coefficient * lambda4[row]
                    for row, coefficient in zip(support, values)) % prime
        violations += bool(value)
        if position % 100000 == 0:
            print("audit degree4", position, "/", len(supports),
                  "violations", violations, flush=True)
    require(violations == 0, "degree-four column replay failed")
    rows2, rows3, rows4 = census["rows"]
    row_indices = ({row: index for index, row in enumerate(rows2)},
                   {row: index for index, row in enumerate(rows3)})
    degree4_index = {row: index for index, row in enumerate(rows4)}
    old_violations = 0
    old_count = 0
    for family, columns in ((2, census["columns"][0]),
                            (3, census["columns"][1])):
        for column in columns:
            old_count += 1
            value = dot_mod(combined_lower_entries(family, column,
                                                   row_indices),
                            lower, prime)
            value += modular_tail_scalar(column, degree4_index,
                                          lambda4, prime)
            old_violations += bool(value % prime)
        print("audit old family", family, "columns", len(columns),
              "total violations", old_violations, flush=True)
    require(old_violations == 0, "old-column source-faithful replay failed")
    pairing = target_pair(census, lower, lambda4, prime)
    require(pairing == payload["target_pairing"] and pairing,
            "target pairing changed")
    ledger = {
        "prime": prime,
        "degree4_columns": len(supports),
        "old_columns": old_count,
        "lower_rank": 27904,
        "lower_kernel_tails": 31584,
        "degree4_violations": violations,
        "old_column_violations": old_violations,
        "target_pairing": pairing,
        "functional_support": (sum(bool(value) for value in lower)
                               + sum(bool(value) for value in lambda4)),
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    print(json.dumps(ledger, indent=2, sort_keys=True), flush=True)
    print("modular dual ledger sha256",
          sha256(encoded.encode("ascii")).hexdigest(), flush=True)
    return ledger


def crt(residues, primes):
    modulus = math.prod(primes)
    value = 0
    for residue, prime in zip(residues, primes):
        partial = modulus // prime
        value += residue * partial * pow(partial, -1, prime)
    return value % modulus, modulus


def rational_reconstruct(residue, modulus):
    """Symmetric rational reconstruction with the standard sqrt bound."""
    bound = math.isqrt(modulus // 2)
    old_r, r = modulus, residue
    old_t, t = 0, 1
    while abs(r) > bound:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_t, t = t, old_t - quotient * t
    numerator, denominator = r, t
    if denominator < 0:
        numerator, denominator = -numerator, -denominator
    if (not denominator or abs(numerator) > bound
            or denominator > bound
            or math.gcd(numerator, denominator) != 1
            or (numerator - residue * denominator) % modulus):
        raise ValueError("rational reconstruction needs more primes")
    return QQ(numerator, denominator)


def reconstruct(primes):
    payloads = []
    for prime in primes:
        with dual_path(prime).open("rb") as stream:
            payloads.append(pickle.load(stream))
    frees = {payload["free_coordinate"] for payload in payloads}
    require(len(frees) == 1, "modular duals chose different free coordinates")
    sizes = {(len(payload["lower"]), len(payload["degree4"]))
             for payload in payloads}
    require(len(sizes) == 1, "modular dual dimensions differ")
    number_lower, number_degree4 = sizes.pop()

    def rebuild(key, size):
        output = []
        failures = 0
        for index in range(size):
            residues = [payload[key][index] for payload in payloads]
            residue, modulus = crt(residues, primes)
            try:
                output.append(rational_reconstruct(residue, modulus))
            except ValueError:
                failures += 1
                output.append(None)
            if (index + 1) % 100000 == 0:
                print("rational reconstruction", key, index + 1, "/", size,
                      "failures", failures, flush=True)
        require(failures == 0,
                f"{failures} {key} coordinates need more primes")
        return output

    lower = rebuild("lower", number_lower)
    degree4 = rebuild("degree4", number_degree4)
    result = {
        "primes": tuple(primes),
        "free_coordinate": next(iter(frees)),
        "lower": lower,
        "degree4": degree4,
    }
    path = rational_path(primes)
    with path.open("wb") as stream:
        pickle.dump(result, stream, protocol=5)
    print("wrote rational candidate", path, path.stat().st_size, flush=True)
    exact_audit(result)


def exact_dot(entries, values):
    return sum((coefficient * values[index]
                for index, coefficient in entries.items()), QQ(0))


def exact_audit(payload):
    census, peel = load_data()
    lower = payload["lower"]
    lambda4 = payload["degree4"]
    supports, coefficients = peel[:2]
    for position, (support, values) in enumerate(
            zip(supports, coefficients), 1):
        value = sum((coefficient * lambda4[row]
                     for row, coefficient in zip(support, values)), QQ(0))
        require(value == 0, f"exact degree-four failure at {position}")
        if position % 100000 == 0:
            print("exact degree4", position, "/", len(supports), flush=True)
    rows2, rows3, rows4 = census["rows"]
    row_indices = ({row: index for index, row in enumerate(rows2)},
                   {row: index for index, row in enumerate(rows3)})
    degree4_index = {row: index for index, row in enumerate(rows4)}
    old_count = 0
    for family, columns in ((2, census["columns"][0]),
                            (3, census["columns"][1])):
        for column in columns:
            old_count += 1
            value = exact_dot(combined_lower_entries(family, column,
                                                     row_indices), lower)
            value += exact_dot(MORSE.old_tail_entries(column, degree4_index),
                               lambda4)
            require(value == 0, f"exact old-column failure at {old_count}")
        print("exact old family", family, "columns", len(columns), flush=True)
    values = (lower[:len(rows2)], lower[len(rows2):], lambda4)
    pairing = QQ(0)
    for rows, residual, functional in zip(census["rows"],
                                           census["residuals"], values):
        index = {row: position for position, row in enumerate(rows)}
        pairing += sum((coefficient * functional[index[row]]
                        for row, coefficient in residual.items()), QQ(0))
    require(pairing != 0, "exact target pairing vanished")
    print("chart25 degree-four exact source-faithful dual: PASS", flush=True)
    print("all degree-four columns", len(supports),
          "all old columns", old_count,
          "lower-kernel tails", 31584,
          "target pairing", pairing, flush=True)


def main():
    require(len(sys.argv) >= 3,
            "usage: extract|audit PRIME, or reconstruct PRIME...")
    mode = sys.argv[1]
    primes = tuple(map(int, sys.argv[2:]))
    if mode == "extract":
        require(len(primes) == 1, "extract takes one prime")
        modular_extract(primes[0])
        return
    if mode == "audit":
        require(len(primes) == 1, "audit takes one prime")
        modular_audit(primes[0])
        return
    require(mode == "reconstruct", "unknown mode")
    require(len(primes) >= 2, "reconstruct needs at least two primes")
    reconstruct(primes)


if __name__ == "__main__":
    main()
