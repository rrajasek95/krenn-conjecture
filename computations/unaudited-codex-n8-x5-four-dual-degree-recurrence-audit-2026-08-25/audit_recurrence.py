#!/usr/bin/env python3
"""Exact bounded audit of t-extension rules for the four X5 dual families."""
from collections import defaultdict
from fractions import Fraction
import hashlib
import itertools
import json
import math
import os
from pathlib import Path

if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
T = 361
BRANCHES = ("direct", "triangle_endpoint_colour", "third_colour", "cap_endpoint_colour")
PACKAGES = {
    6: REPO / "computations/unaudited-codex-n8-x5-four-blocker-d6-rational-lift-2026-08-25",
    7: REPO / "computations/unaudited-codex-n8-x5-four-blocker-d7-two-prime-lift-2026-08-25",
    8: REPO / "computations/unaudited-codex-n8-x5-four-blocker-d8-two-prime-lift-2026-08-25",
}
D8 = PACKAGES[8]
PROVIDER_ROOT = REPO / "computations/unaudited-codex-n8-x5-four-blocker-d6-cegar-gate-2026-08-25"
PROVIDER_SHA = {
    "direct": "53850c4224fcc901bb5bd0d4c5be58d92ae4f4fb04bfdc887bc4492f4dd41d6c",
    "triangle_endpoint_colour": "06df5052a50099dc400d622323257fef9b3077a791f918c8f1c46d7bf7a5782c",
    "third_colour": "b5ce054d529a5390c366254d08e43595cfa16e04854514f80db1b34f109d4ae8",
    "cap_endpoint_colour": "d040d1525989588bce3b912413aa6841869de63575bb3ebf976de817869e0b64",
}


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def signed_terms(line):
    line = line.removesuffix(",")
    answer, begin, sign = [], 0, 1
    if line[0] in "+-":
        sign, begin = (-1 if line[0] == "-" else 1), 1
    for index in range(begin, len(line)):
        if line[index] in "+-":
            answer.append((sign, line[begin:index]))
            sign, begin = (-1 if line[index] == "-" else 1), index + 1
    answer.append((sign, line[begin:]))
    return answer


def load_provider(branch):
    path = PROVIDER_ROOT / f"provider_{branch}.ms"
    assert sha(path) == PROVIDER_SHA[branch]
    with path.open() as stream:
        variables = stream.readline().rstrip("\n").split(",")
        assert len(variables) == 361 and int(stream.readline()) == 1073741827
        names = {name: index for index, name in enumerate(variables)}
        generators = []
        for line in stream:
            raw, maximum = [], 0
            for coefficient, token in signed_terms(line.rstrip("\n")):
                ids = () if token == "1" else tuple(sorted(names[x] for x in token.split("*")))
                maximum = max(maximum, len(ids))
                raw.append((ids, coefficient))
            combined = defaultdict(int)
            for ids, coefficient in raw:
                combined[tuple(sorted(ids + (T,) * (maximum - len(ids))))] += coefficient
            generators.append((maximum, tuple(sorted((row, c) for row, c in combined.items() if c))))
    assert len(generators) == 6571
    return tuple(generators)


def load_dual(degree, branch):
    path = PACKAGES[degree] / f"exact_lift_{branch}" / "integer_dual.tsv"
    lines = path.read_text().splitlines()
    header = lines[0].split("\t")
    assert int(header[1]) == len(lines) - 1 and int(header[2]) == 1
    dual = {}
    for line in lines[1:]:
        kind, raw, value = line.split("\t")
        row = tuple(map(int, raw.split(",")))
        assert kind == "ROW" and len(row) == degree and row == tuple(sorted(row)) and row not in dual
        dual[row] = int(value)
    assert dual[(T,) * degree] == 1 and set(dual.values()) <= {-1, 1}
    return dual, path


def quotient(row, divisor):
    answer, cursor = [], 0
    for value in row:
        if cursor < len(divisor) and value == divisor[cursor]:
            cursor += 1
        else:
            answer.append(value)
    return tuple(answer) if cursor == len(divisor) else None


def incident_replay(generators, dual):
    degree = len(next(iter(dual)))
    term_index = defaultdict(set)
    for generator, (_e, terms) in enumerate(generators):
        for term, coefficient in terms:
            if coefficient:
                term_index[term].add(generator)
    columns = set()
    for row in dual:
        for e in (2, 3, 4):
            for positions in itertools.combinations(range(degree), e):
                divisor = tuple(row[i] for i in positions)
                multiplier = quotient(row, divisor)
                for generator in term_index.get(divisor, ()):
                    assert generators[generator][0] == e
                    columns.add((generator, multiplier))
    failures = []
    for generator, multiplier in sorted(columns):
        pairing = 0
        realized = []
        for term, coefficient in generators[generator][1]:
            row = tuple(sorted(term + multiplier))
            contribution = coefficient * dual.get(row, 0)
            pairing += contribution
            if contribution:
                realized.append((row, coefficient, dual[row], contribution))
        if pairing:
            failures.append({
                "generator": generator,
                "multiplier": multiplier,
                "pairing": pairing,
                "realized": realized,
            })
    return len(columns), failures


def incident_columns(generators, support):
    degree = len(next(iter(support)))
    term_index = defaultdict(set)
    for generator, (_e, terms) in enumerate(generators):
        for term, coefficient in terms:
            if coefficient:
                term_index[term].add(generator)
    columns = set()
    for row in support:
        for e in (2, 3, 4):
            for positions in itertools.combinations(range(degree), e):
                divisor = tuple(row[i] for i in positions)
                multiplier = quotient(row, divisor)
                for generator in term_index.get(divisor, ()):
                    columns.add((generator, multiplier))
    return tuple(sorted(columns))


def column_pairing(generators, column, dual):
    generator, multiplier = column
    return sum(
        coefficient * dual.get(tuple(sorted(term + multiplier)), 0)
        for term, coefficient in generators[generator][1]
    )


def solve_candidate_span(generators, named_candidates):
    """Search the Q-span of transported sealed certificates, not new D9 rows."""
    names = [name for name, _dual in named_candidates]
    candidates = [dual for _name, dual in named_candidates]
    union = set().union(*(set(dual) for dual in candidates))
    columns = incident_columns(generators, union)
    matrix = [[Fraction(dual[(T,) * 9]) for dual in candidates] + [Fraction(1)]]
    for column in columns:
        row = [Fraction(column_pairing(generators, column, dual)) for dual in candidates]
        if any(row):
            matrix.append(row + [Fraction(0)])
    pivot_columns, pivot_row = [], 0
    for column in range(len(candidates)):
        found = next((r for r in range(pivot_row, len(matrix)) if matrix[r][column]), None)
        if found is None:
            continue
        matrix[pivot_row], matrix[found] = matrix[found], matrix[pivot_row]
        pivot = matrix[pivot_row][column]
        matrix[pivot_row] = [x / pivot for x in matrix[pivot_row]]
        for r in range(len(matrix)):
            if r != pivot_row and matrix[r][column]:
                factor = matrix[r][column]
                matrix[r] = [x - factor * y for x, y in zip(matrix[r], matrix[pivot_row])]
        pivot_columns.append(column)
        pivot_row += 1
    inconsistent = any(not any(row[:-1]) and row[-1] for row in matrix)
    if inconsistent:
        return {
            "pass": False,
            "candidate_names": names,
            "candidate_count": len(candidates),
            "union_support": len(union),
            "incident_columns": len(columns),
            "equations_with_nonzero_candidate_pairing": len(matrix) - 1,
            "coefficient_rank": len(pivot_columns),
            "diagnosis": "target-normalized annihilator is absent from the transported-certificate span",
        }, None
    solution = [Fraction(0) for _ in candidates]
    for row, column in enumerate(pivot_columns):
        solution[column] = matrix[row][-1]
    combined = defaultdict(Fraction)
    for coefficient, dual in zip(solution, candidates):
        for monomial, weight in dual.items():
            combined[monomial] += coefficient * weight
    combined = {row: value for row, value in combined.items() if value}
    denominator = math.lcm(*(value.denominator for value in combined.values()))
    integer = {row: value.numerator * (denominator // value.denominator) for row, value in combined.items()}
    divisor = math.gcd(*(abs(value) for value in integer.values()))
    integer = {row: value // divisor for row, value in integer.items()}
    target = integer[(T,) * 9]
    if target < 0:
        integer = {row: -value for row, value in integer.items()}
        target = -target
    replay_count, failures = incident_replay(generators, integer)
    assert not failures and target != 0
    return {
        "pass": True,
        "candidate_names": names,
        "candidate_count": len(candidates),
        "union_support": len(union),
        "incident_columns": len(columns),
        "equations_with_nonzero_candidate_pairing": len(matrix) - 1,
        "coefficient_rank": len(pivot_columns),
        "solution_coefficients": [str(x) for x in solution],
        "integer_support": len(integer),
        "integer_target_coefficient": target,
        "literal_incident_columns_replayed": replay_count,
        "integer_weight_set": sorted(set(integer.values())),
    }, integer


def extend_t(dual, count=1):
    return {tuple(sorted(row + (T,) * count)): value for row, value in dual.items()}


def induction_layer_audit(generators, dual):
    """Check finite t-contractions C_k(g), sufficient for every iterated t-extension."""
    degree = len(next(iter(dual)))
    candidates = set()
    for row in dual:
        for generator, (e, terms) in enumerate(generators):
            max_k = max((term.count(T) for term, _c in terms), default=0)
            for k in range(1, max_k + 1):
                contracted_terms = []
                for term, coefficient in terms:
                    if term.count(T) >= k:
                        contracted_terms.append((term[:len(term) - k], coefficient))
                for term, _coefficient in contracted_terms:
                    multiplier = quotient(row, term)
                    if multiplier is not None and T not in multiplier and len(multiplier) == degree - e + k:
                        candidates.add((generator, k, multiplier))
    failures = []
    by_k = defaultdict(lambda: {"candidates": 0, "failures": 0})
    for generator, k, multiplier in sorted(candidates):
        e, terms = generators[generator]
        pairing, realized = 0, []
        for term, coefficient in terms:
            if term.count(T) < k:
                continue
            contracted = term[:len(term) - k]
            row = tuple(sorted(contracted + multiplier))
            contribution = coefficient * dual.get(row, 0)
            pairing += contribution
            if contribution:
                realized.append((row, coefficient, dual[row], contribution))
        by_k[k]["candidates"] += 1
        if pairing:
            by_k[k]["failures"] += 1
            failures.append({
                "generator": generator,
                "generator_degree": e,
                "contraction_k": k,
                "t_free_multiplier": multiplier,
                "pairing": pairing,
                "realized": realized,
            })
    return dict(sorted(by_k.items())), failures


def row_text(row):
    return ",".join(map(str, row))


def simplify_failure(record):
    return {
        "generator": record["generator"],
        **({"generator_degree": record["generator_degree"], "contraction_k": record["contraction_k"],
            "t_free_multiplier": row_text(record["t_free_multiplier"])} if "contraction_k" in record else
           {"multiplier": row_text(record["multiplier"])}),
        "pairing": record["pairing"],
        "realized": [
            {"row": row_text(row), "generator_coefficient": c, "dual_weight": w, "contribution": z}
            for row, c, w, z in record["realized"]
        ],
    }


def atomic_json(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def main():
    results = []
    providers = {}
    sealed = {}
    for branch in BRANCHES:
        generators = load_provider(branch)
        providers[branch] = generators
        duals = {}
        dual_paths = {}
        for degree in (6, 7, 8):
            duals[degree], dual_paths[degree] = load_dual(degree, branch)
        sealed[branch] = duals
        sealed_replays = []
        for degree in (6, 7, 8):
            count, failures = incident_replay(generators, duals[degree])
            assert not failures
            sealed_replays.append({
                "degree": degree,
                "support": len(duals[degree]),
                "incident_columns": count,
                "pairing_failures": 0,
                "target_coefficient": duals[degree][(T,) * degree],
                "t_valuation_histogram": dict(sorted((
                    (valuation, sum(1 for row in duals[degree] if row.count(T) == valuation))
                    for valuation in set(row.count(T) for row in duals[degree])
                ))),
            })
        transports = []
        for source, destination in ((6, 7), (7, 8), (8, 9), (6, 8), (6, 9), (7, 9)):
            candidate = extend_t(duals[source], destination - source)
            count, failures = incident_replay(generators, candidate)
            destination_dual = duals.get(destination)
            matching_rows = (sum(
                1 for row, value in candidate.items()
                if destination_dual is not None and destination_dual.get(row) == value
            ) if destination_dual is not None else None)
            transports.append({
                "source_degree": source,
                "destination_degree": destination,
                "support": len(candidate),
                "incident_columns": count,
                "pairing_failures": len(failures),
                "pass": not failures,
                "first_failure": simplify_failure(failures[0]) if failures else None,
                "equals_sealed_destination_dual": destination in duals and candidate == duals[destination],
                "matching_rows_in_sealed_destination": matching_rows,
            })
        layers = []
        for degree in (6, 7, 8):
            by_k, failures = induction_layer_audit(generators, duals[degree])
            layers.append({
                "base_degree": degree,
                "support": len(duals[degree]),
                "by_contraction": by_k,
                "pairing_failures": len(failures),
                "all_iterated_t_extensions_proved": not failures,
                "first_failure": simplify_failure(failures[0]) if failures else None,
            })
        results.append({
            "branch": branch,
            "provider_sha256": PROVIDER_SHA[branch],
            "dual_sha256": {str(d): sha(dual_paths[d]) for d in (6, 7, 8)},
            "sealed_supports": {str(d): len(duals[d]) for d in (6, 7, 8)},
            "sealed_literal_replays": sealed_replays,
            "transports": transports,
            "finite_induction_layer_audits": layers,
        })
    # The direct D8 functional is the 38-row common core visibly embedded in
    # every coloured D8 certificate.  Test it, and its one-t extension, against
    # each branch's own literal provider rather than assuming provider equality.
    direct_core_cross_branch = []
    for branch in BRANCHES:
        for destination in (8, 9):
            candidate = extend_t(sealed["direct"][8], destination - 8)
            count, failures = incident_replay(providers[branch], candidate)
            direct_core_cross_branch.append({
                "provider_branch": branch,
                "destination_degree": destination,
                "support": len(candidate),
                "incident_columns": count,
                "pairing_failures": len(failures),
                "pass": not failures,
                "first_failure": simplify_failure(failures[0]) if failures else None,
            })
    transported_span_search = []
    for branch in BRANCHES:
        raw_candidates = [
            (f"{branch}_d6_t3", extend_t(sealed[branch][6], 3)),
            (f"{branch}_d7_t2", extend_t(sealed[branch][7], 2)),
            (f"{branch}_d8_t1", extend_t(sealed[branch][8], 1)),
            ("direct_d6_t3", extend_t(sealed["direct"][6], 3)),
            ("direct_d7_t2", extend_t(sealed["direct"][7], 2)),
            ("direct_d8_t1", extend_t(sealed["direct"][8], 1)),
        ]
        named_candidates = []
        seen = set()
        for name, candidate in raw_candidates:
            key = tuple(sorted(candidate.items()))
            if key not in seen:
                seen.add(key)
                named_candidates.append((name, candidate))
        record, integer = solve_candidate_span(providers[branch], named_candidates)
        record["provider_branch"] = branch
        transported_span_search.append(record)
        if integer is not None:
            lines = [f"KRENN_X5_D9_TRANSPORTED_SPAN_INTEGER_DUAL_V1\t{len(integer)}\t{integer[(T,) * 9]}"]
            lines.extend(f"ROW\t{row_text(row)}\t{value}" for row, value in sorted(integer.items()))
            (HERE / f"d9_span_dual_{branch}.tsv").write_text("\n".join(lines) + "\n")
    output = {
        "schema": "KRENN_X5_FOUR_DUAL_DEGREE_RECURRENCE_AUDIT_V1",
        "status": "PASS_EXACT_BOUNDED_RECURRENCE_AUDIT",
        "scope": "Sealed D6-D8 integer duals plus support-induced D9 literal incident columns only; no D9 closure/solve.",
        "theorem_tested": "If lambda annihilates I_d and every t-contraction C_k(g) times every incident t-free multiplier, every iterated t-extension E^n(lambda) annihilates I_(d+n).",
        "records": results,
        "direct_d8_core_cross_branch": direct_core_cross_branch,
        "transported_sealed_certificate_span_search": transported_span_search,
        "d9_full_closure_or_solve": False,
    }
    atomic_json(HERE / "results_recurrence_audit.json", output)
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
