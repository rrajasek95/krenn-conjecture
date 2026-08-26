#!/usr/bin/env python3
"""Independent exact referee of the branch-1 uniform-d=0 classification."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from math import isqrt
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CORE_PATH = (ROOT / "computations" /
             "unaudited-codex-n8-orbit0-normalized-78-2026-08-20" /
             "audit_polarized_superpair_core_identity.py")
CLASSIFICATION = (ROOT / "computations" /
                  "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20" /
                  "results_branch1_dzero_classification.json")
ALIGNED_PATH = HERE / "audit_joint_aligned_zero_chart_census.py"
OUT = HERE / "results_referee_branch1_dzero_classification.json"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


CORE = load("n8_b1_referee_core", CORE_PATH)
ALIGNED = load("n8_b1_referee_aligned", ALIGNED_PATH)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def derivative(poly, variable):
    answer = Counter()
    for monomial, coefficient in poly.items():
        multiplicity = monomial.count(variable)
        if multiplicity:
            reduced = list(monomial)
            reduced.remove(variable)
            answer[tuple(reduced)] += multiplicity * coefficient
    return CORE.clean(answer)


class Quadratic:
    """Q[z]/(z^2-p*z-1), represented in basis (1,z)."""

    def __init__(self, p):
        self.p = Fraction(p)
        self.zero = (Fraction(0), Fraction(0))
        self.one = (Fraction(1), Fraction(0))

    def add(self, *values):
        return (sum(value[0] for value in values),
                sum(value[1] for value in values))

    def scale(self, value, scalar):
        scalar = Fraction(scalar)
        return (scalar * value[0], scalar * value[1])

    def mul(self, left, right):
        return (left[0] * right[0] + left[1] * right[1],
                left[0] * right[1] + left[1] * right[0]
                + self.p * left[1] * right[1])

    def inv(self, value):
        conjugate = (value[0] + self.p * value[1], -value[1])
        norm = value[0] * conjugate[0] - value[1] * value[1]
        require(norm != 0, "quadratic division by zero")
        return self.scale(conjugate, 1 / norm)


def pt_clean(poly, field):
    return {degree: coefficient for degree, coefficient in poly.items()
            if coefficient != field.zero}


def pt_add(field, *polys):
    answer = {}
    for poly in polys:
        for degree, coefficient in poly.items():
            answer[degree] = field.add(answer.get(degree, field.zero),
                                       coefficient)
    return pt_clean(answer, field)


def pt_mul(field, *polys):
    answer = {0: field.one}
    for poly in polys:
        updated = {}
        for left_degree, left in answer.items():
            for right_degree, right in poly.items():
                degree = left_degree + right_degree
                updated[degree] = field.add(
                    updated.get(degree, field.zero), field.mul(left, right))
        answer = pt_clean(updated, field)
    return answer


def evaluate(field, poly, entries):
    answer = {}
    for monomial, coefficient in poly.items():
        term = {0: field.scale(field.one, coefficient)}
        for variable in monomial:
            term = pt_mul(field, term, entries[variable])
        answer = pt_add(field, answer, term)
    return answer


def decode_k(value):
    return tuple(Fraction(numerator, denominator)
                 for numerator, denominator in value)


def decode_pt(value):
    return {record["T_degree"]: decode_k(record["coefficient_1_z"])
            for record in value}


def component_replay(record):
    p = record["quadratic_relation_p_in_z2_equals_pz_plus_1"]
    field = Quadratic(p)
    require(isqrt(p * p + 4) ** 2 != p * p + 4,
            "component quadratic field became reducible")
    b = tuple(decode_k(value) for value in record[
        "b_01_02_03_12_13_23"])
    alpha = tuple(decode_k(value) for value in record[
        "a_over_T_01_02_03_12_13_23"])
    entries = []
    for edge in range(6):
        entries.extend(({1: alpha[edge]}, {0: b[edge]},
                        {0: field.scale(field.inv(b[edge]), -1)}, {}))

    h = CORE.pure_hafnian()
    rows = [CORE.e_pair(*edge) for edge in CORE.SUPER_EDGES]
    rows += [CORE.t_triple(*triple)
             for triple in combinations(range(4), 3)]
    branch_bits = (1, 0, 0, 0, 0, 0)
    for edge, bit in enumerate(branch_bits):
        for position in ((1, 2) if bit else (0, 3)):
            rows.append(derivative(h, 4 * edge + position))
    require(not any(evaluate(field, row, entries) for row in rows),
            "an independently rebuilt source row is nonzero")
    require(evaluate(field, h, entries) == {0: field.scale(field.one, 4)},
            "independent pure-H replay changed")

    q_values = tuple(evaluate(field, CORE.q_orientation(tuple(
        (index >> (3 - site)) & 1 for site in range(4))), entries)
                     for index in range(16))
    cofactors = tuple(evaluate(field, derivative(h, index), entries)
                      for index in range(24))
    stored_q = tuple(decode_pt(record["Q_polynomials"][str(index)])
                     for index in range(16))
    stored_c = tuple(decode_pt(record["cofactor_polynomials"][str(index)])
                     for index in range(24))
    require(q_values == stored_q and cofactors == stored_c,
            "stored Q/cofactor polynomial ledger mismatch")
    q_generic = tuple(index for index, value in enumerate(q_values) if value)
    q_zero = tuple(index for index, value in enumerate(q_values)
                   if value.get(0, field.zero) != field.zero)
    require(q_generic == (0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 12)
            and q_zero == (3, 5, 6, 9, 10, 12),
            "branch-1 support specialization changed")
    degrees = {index: tuple(value) for index, value in enumerate(q_values)}
    require({index for index, degree in degrees.items() if degree == (0,)}
            == {3, 5, 6, 9, 10, 12}
            and {index for index, degree in degrees.items() if degree == (1,)}
            == {1, 2, 4, 8}
            and degrees[0] == (2,),
            "Q-degree partition changed")

    # Mutating one stored Q0 coefficient must be detected.
    mutated_q0 = dict(stored_q[0])
    mutated_q0[2] = field.add(mutated_q0[2], field.one)
    require(mutated_q0 != q_values[0], "Q0 mutation did not fire")
    return {"p": p, "generic_Q_support": list(q_generic),
            "T_zero_Q_support": list(q_zero),
            "raw_rows_zero": True, "H": 4,
            "Q_and_cofactor_ledgers_match": True,
            "mutation_fired": True}


def component_census():
    rows = ALIGNED.derived_rows(1, 63, deduplicate=False)
    entries = ALIGNED.aligned_entries(63)
    h = ALIGNED.clear_denominators(ALIGNED.substitute(
        CORE.pure_hafnian(), entries))
    variables = ALIGNED.variables() + ",u"
    ideal = ",".join(encoded for _, _, encoded in rows)
    command = (
        f"ring R=0,({variables}),dp;ideal I={ideal},b2-1,b4-1,b5-1,"
        f"u*({ALIGNED.singular(h)})-1,z*{ALIGNED.live_product(63)}-1;"
        "ideal G=std(I);LIB \"primdec.lib\";list L=minAssGTZ(I);"
        'print("BEGIN");print(dim(G));print(size(L));'
        "for(int i=1;i<=size(L);i++){ideal J=L[i];ideal K=std(J);"
        "print(dim(K));};print(\"END\");"
    )
    completed = subprocess.run(["Singular", "-q", "-c", command],
                               text=True, capture_output=True,
                               timeout=60, check=False)
    require(completed.returncode == 0 and not completed.stderr.strip(),
            "independent minAss run failed: " + completed.stderr[-500:])
    lines = completed.stdout.splitlines()
    begin, end = lines.index("BEGIN"), lines.index("END")
    body = [line for line in lines[begin + 1:end]
            if not line.startswith("//")]
    require(body == ["1", "2", "1", "1"],
            "independent minimal-prime census changed")
    return {"dimension": 1, "minimal_prime_count": 2,
            "minimal_prime_dimensions": [1, 1]}


def main():
    frozen = json.loads(CLASSIFICATION.read_text())
    require(frozen["simultaneous_chart"]["cofactor_orientation_mask"] == 1
            and "all-six" in frozen["simultaneous_chart"]["warning"],
            "branch/permanent-mask scope guard changed")
    census = component_census()
    components = [component_replay(record) for record in frozen["components"]]
    require([record["p"] for record in components] == [14, -2],
            "quadratic component order changed")
    result = {
        "status": "UNAUDITED independent branch-1 d=0 referee",
        "producer_logical_sha256": frozen["result_sha256"],
        "chart": "cofactor mask1, uniform d=0, permanent offdiag mask63",
        "independent_component_census": census,
        "component_replays": components,
        "wlog_small_member_logic": (
            "For Q-cross-compatible supports S,D, |S|+|D|<=16, hence "
            "min(|S|,|D|)<=8. A generic size-11 branch-1 point is never "
            "the chosen low member; it could only pair with an as-yet-"
            "unknown support-at-most-five point. At T=0 it is the known "
            "support-six stratum, globally closed by its partner certificate."
        ),
        "scope": (
            "This classifies only the uniform d=0 chart and does not infer "
            "absence of an unknown support-at-most-five partner."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("branch-1 d=0 independent referee: PASS")
    print("dimension / components:", census["dimension"],
          census["minimal_prime_count"])
    print("generic / T=0 Q support:", 11, 6)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
