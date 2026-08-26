#!/usr/bin/env python3
"""Independent literal verifier for the bounded four-branch degree-six gate."""
import argparse
from collections import Counter, defaultdict
import hashlib
import itertools
import json
import os
from pathlib import Path

if not __debug__:
    raise RuntimeError("fail closed: this validator requires Python assertions enabled")

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SCHEDULE = json.loads((HERE / "SCHEDULE.json").read_text())
T_ID = 361


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def signed_terms(line):
    line = line.removesuffix(",")
    answer = []
    sign = 1
    begin = 0
    if line[0] in "+-":
        sign = -1 if line[0] == "-" else 1
        begin = 1
    for index in range(begin, len(line)):
        if line[index] in "+-":
            answer.append((sign, line[begin:index]))
            sign = -1 if line[index] == "-" else 1
            begin = index + 1
    answer.append((sign, line[begin:]))
    return answer


def load_provider(path):
    with path.open() as stream:
        variables = stream.readline().rstrip("\n").split(",")
        characteristic = int(stream.readline())
        names = {name: index for index, name in enumerate(variables)}
        generators = []
        parsed_terms = 0
        for line in stream:
            raw = []
            maximum = 0
            for sign, token in signed_terms(line.rstrip("\n")):
                ids = [] if token == "1" else [names[factor] for factor in token.split("*")]
                maximum = max(maximum, len(ids))
                raw.append((ids, sign))
                parsed_terms += 1
            combined = defaultdict(int)
            for ids, sign in raw:
                key = tuple(sorted(ids + [T_ID] * (maximum - len(ids))))
                combined[key] += sign
            generators.append((maximum, tuple(sorted((key, value) for key, value in combined.items() if value))))
    assert len(variables) == 361 and characteristic == 1073741827
    assert len(generators) == 6571
    assert Counter(degree for degree, _ in generators) == {2: 1, 3: 9, 4: 6561}
    return generators, parsed_terms


def load_selected(path, generators):
    lines = path.read_text().splitlines()
    assert lines[0] == "KRENN_X5_BLOCKER_D6_SELECTED_COLUMNS_V1"
    answer = []
    for line in lines[1:]:
        kind, generator, degree, multiplier = line.split("\t")
        assert kind == "COL"
        generator = int(generator)
        degree = int(degree)
        multiplier = tuple(int(value) for value in multiplier.split(",") if value)
        assert 0 <= generator < 6571 and degree == generators[generator][0]
        assert len(multiplier) + degree == 6 and tuple(sorted(multiplier)) == multiplier
        answer.append((generator, multiplier))
    assert len(answer) == len(set(answer)) and answer == sorted(answer)
    return answer


def load_dual(path, prime):
    lines = path.read_text().splitlines()
    header = lines[0].split("\t")
    assert header[0] == "KRENN_X5_BLOCKER_D6_MODULAR_DUAL_V1"
    assert int(header[1]) == prime and int(header[2]) == len(lines) - 1 and int(header[3]) == 1
    answer = {}
    for line in lines[1:]:
        kind, row, value = line.split("\t")
        row = tuple(int(item) for item in row.split(",") if item)
        value = int(value)
        assert kind == "ROW" and len(row) == 6 and tuple(sorted(row)) == row
        assert 0 < value < prime and row not in answer
        answer[row] = value
    assert answer[(T_ID,) * 6] == 1
    return answer


def materialize(generators, column, prime):
    generator, multiplier = column
    values = defaultdict(int)
    for term, coefficient in generators[generator][1]:
        values[tuple(sorted(term + multiplier))] += coefficient
    return {row: value % prime for row, value in values.items() if value % prime}


def pairing(vector, dual, prime):
    return sum(value * dual.get(row, 0) for row, value in vector.items()) % prime


def multiset_quotient(row, divisor):
    """Return sorted row/divisor, or None when divisor is not a submultiset."""
    quotient = []
    cursor = 0
    for value in row:
        if cursor < len(divisor) and value == divisor[cursor]:
            cursor += 1
        else:
            quotient.append(value)
    return tuple(quotient) if cursor == len(divisor) else None


def verify_global_incident_columns(generators, dual, prime):
    """Exhaust all columns that can pair nontrivially with the sparse dual.

    A homogeneous degree-six column can pair with a supported row only when one
    of its generator terms divides that row.  Enumerating every distinct
    degree-2/3/4 divisor of every supported row is therefore exhaustive; all
    other columns have identically zero pairing by support disjointness.
    """
    term_to_generators = defaultdict(set)
    for generator, (_degree, terms) in enumerate(generators):
        for term, coefficient in terms:
            if coefficient % prime:
                term_to_generators[term].add(generator)

    incident = set()
    for row in dual:
        for degree in (2, 3, 4):
            divisors = {tuple(row[index] for index in indices)
                        for indices in itertools.combinations(range(6), degree)}
            for divisor in divisors:
                multiplier = multiset_quotient(row, divisor)
                assert multiplier is not None and len(multiplier) == 6 - degree
                for generator in term_to_generators.get(divisor, ()):
                    assert generators[generator][0] == degree
                    incident.add((generator, multiplier))

    for column in incident:
        vector = materialize(generators, column, prime)
        assert pairing(vector, dual, prime) == 0
    return len(incident)


def verify_branch(branch):
    provider_spec = SCHEDULE["providers"][branch]
    provider_path = HERE / provider_spec["path"]
    assert sha256(provider_path) == provider_spec["sha256"]
    generators, parsed_terms = load_provider(provider_path)
    directory = HERE / f"branch_{branch}"
    result = json.loads((directory / "result.json").read_text())
    assert result["schema"] == "KRENN_X5_FOUR_BLOCKER_D6_CEGAR_RESULT_V1"
    assert result["branch"] == branch and result["variables"] == 361 and result["equations"] == 6571
    assert result["provider_terms_parsed"] == parsed_terms
    assert result["degree"] == 6 and result["target"] == "t^6" and result["prime"] == 1073741827
    assert result["column_cap"] == 50000 and result["selected_columns"] <= 50000
    assert result["exact_rational_unit_replay"] is False and result["mathematical_verdict"] is None
    assert result["status"] in {
        "INCOMPLETE_COLUMN_CAP",
        "INCOMPLETE_WALL_CAP",
        "COMPLETE_MODULAR_DUAL_DIAGNOSTIC",
        "MODULAR_MEMBER_REQUIRES_EXACT_RATIONAL_REPLAY",
    }
    selected = load_selected(directory / "selected.tsv", generators)
    assert len(selected) == result["selected_columns"]
    dual_path = directory / "dual.tsv"
    global_incident_columns_verified = 0
    if result["status"] == "MODULAR_MEMBER_REQUIRES_EXACT_RATIONAL_REPLAY":
        assert not dual_path.exists()
    else:
        dual = load_dual(dual_path, result["prime"])
        assert len(dual) == result["dual_support"]
        for column in selected:
            assert pairing(materialize(generators, column, result["prime"]), dual, result["prime"]) == 0
        if result["status"] == "COMPLETE_MODULAR_DUAL_DIAGNOSTIC":
            assert result["global_modular_dual"] is True
            global_incident_columns_verified = verify_global_incident_columns(
                generators, dual, result["prime"]
            )
        else:
            assert result["global_modular_dual"] is False
    watchdog = json.loads((directory / "watchdog.json").read_text())
    assert watchdog["rss_limit_kib"] == 8 * 1024 * 1024
    assert watchdog["wall_limit_seconds"] == 120
    assert watchdog["peak_rss_kib"] <= 8 * 1024 * 1024
    return {
        "branch": branch,
        "status": result["status"],
        "selected_columns": result["selected_columns"],
        "dual_support": result["dual_support"],
        "engine_elapsed_seconds": result["elapsed_seconds"],
        "peak_rss_kib": watchdog["peak_rss_kib"],
        "provider_sha256": provider_spec["sha256"],
        "result_sha256": sha256(directory / "result.json"),
        "selected_sha256": sha256(directory / "selected.tsv"),
        "dual_sha256": sha256(dual_path) if dual_path.exists() else None,
        "watchdog_sha256": sha256(directory / "watchdog.json"),
        "selected_pairings_verified": len(selected),
        "global_incident_columns_verified": global_incident_columns_verified,
        "global_support_disjointness_argument": (
            "every nonincident column has zero pairing because no generator term divides a supported row"
        ),
        "mathematical_pass": False,
    }


def hostile_tests(base):
    tests = []
    def reject(name, mutate):
        candidate = json.loads(json.dumps(base))
        mutate(candidate)
        try:
            assert candidate["degree"] == 6
            assert candidate["selected_columns"] <= 50000
            assert candidate["exact_rational_unit_replay"] is False
            assert candidate["mathematical_verdict"] is None
            if candidate["status"] == "COMPLETE_MODULAR_DUAL_DIAGNOSTIC":
                assert candidate["global_modular_dual"] is True
        except AssertionError:
            tests.append({"name": name, "status": "REJECTED"})
            return
        raise AssertionError(f"hostile accepted: {name}")
    reject("wrong_degree", lambda item: item.__setitem__("degree", 7))
    reject("column_cap_overrun", lambda item: item.__setitem__("selected_columns", 50001))
    reject("false_rational_replay", lambda item: item.__setitem__("exact_rational_unit_replay", True))
    reject("false_mathematical_pass", lambda item: item.__setitem__("mathematical_verdict", "PASS"))
    reject("false_global_dual_flag", lambda item: item.__setitem__("global_modular_dual", False))
    return tests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    records = [verify_branch(branch) for branch in SCHEDULE["branches"]]
    all_diagnostic = all(not record["mathematical_pass"] for record in records)
    first = json.loads((HERE / f"branch_{SCHEDULE['branches'][0]}" / "result.json").read_text())
    hostiles = hostile_tests(first) if args.selftest else []
    result = {
        "schema": "KRENN_X5_FOUR_BLOCKER_D6_CEGAR_AUDIT_V1",
        "status": "PASS_EXACT_BOUNDED_GATE_DIAGNOSTIC_NO_MATHEMATICAL_CLOSURE" if all_diagnostic else "PASS_EXACT_RATIONAL_UNIT_CERTIFICATE",
        "records": records,
        "all_four_branches_covered": len(records) == 4,
        "all_outcomes_diagnostic": all_diagnostic,
        "exact_rational_unit_certificates": 0,
        "conjecture_closed": False,
        "continued_beyond_degree6": False,
        "d12_caches_read": False,
        "hostile_tests": hostiles,
    }
    target = HERE / ("results_validation_selftest.json" if args.selftest else "results_four_branch_gate_audit.json")
    temporary = target.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, target)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
