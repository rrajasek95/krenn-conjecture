#!/usr/bin/env python3
"""Independent exact referee of the final aligned survivor (11,21).

This proves the gauge-localized chart has exactly two one-dimensional
components, replays explicit Q(r)[T] parametrizations from raw rows, derives
their X/C/Q support maps, and restores the two fixed-partner unit identities
from the quotient by forced cell zeros to literal 24-variable identities.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CORE_PATH = (ROOT / "computations" /
             "unaudited-codex-n8-orbit0-normalized-78-2026-08-20" /
             "audit_polarized_superpair_core_identity.py")
ALIGNED_PATH = HERE / "audit_joint_aligned_zero_chart_census.py"
CERTIFICATE = (ROOT / "computations" /
    "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20" /
    "certificate_branch11_term21_fixed_partner_units.json")
PRODUCER_CLASSIFICATION = (ROOT / "computations" /
    "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20" /
    "results_branch11_term21_classification.json")
OUT = HERE / "results_referee_branch11_term21_classification_and_partner_units.json"
BRANCH = 11
TERM = 21
EXPECTED_X = (0, 1, 2, 4, 5, 7, 8, 9, 10, 12, 13, 15, 16, 17, 18,
              20, 23)
EXPECTED_Q = (0, 1, 2, 3, 4, 6, 7, 8, 10, 11, 14)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


CORE = load("n8_b11t21_referee_core", CORE_PATH)
ALIGNED = load("n8_b11t21_referee_aligned", ALIGNED_PATH)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def derivative(poly, variable_index):
    answer = Counter()
    for monomial, coefficient in poly.items():
        multiplicity = monomial.count(variable_index)
        if multiplicity:
            reduced = list(monomial)
            reduced.remove(variable_index)
            answer[tuple(reduced)] += multiplicity * coefficient
    return CORE.clean(answer)


class Quadratic:
    """Q[r]/(r^2-2r-1), in basis (1,r)."""

    zero = (Fraction(0), Fraction(0))
    one = (Fraction(1), Fraction(0))

    @staticmethod
    def add(*values):
        return (sum(value[0] for value in values),
                sum(value[1] for value in values))

    @staticmethod
    def scale(value, scalar):
        scalar = Fraction(scalar)
        return (scalar * value[0], scalar * value[1])

    @staticmethod
    def mul(left, right):
        return (left[0] * right[0] + left[1] * right[1],
                left[0] * right[1] + left[1] * right[0]
                + 2 * left[1] * right[1])

    @classmethod
    def inv(cls, value):
        # Conjugation r -> 2-r.
        conjugate = (value[0] + 2 * value[1], -value[1])
        norm = cls.mul(value, conjugate)[0]
        require(norm != 0, "quadratic division by zero")
        return cls.scale(conjugate, 1 / norm)


K = Quadratic


def pt_clean(poly):
    return {degree: coefficient for degree, coefficient in poly.items()
            if coefficient != K.zero}


def pt_add(*polys):
    answer = {}
    for poly in polys:
        for degree, coefficient in poly.items():
            answer[degree] = K.add(answer.get(degree, K.zero), coefficient)
    return pt_clean(answer)


def pt_mul(*polys):
    answer = {0: K.one}
    for poly in polys:
        updated = {}
        for left_degree, left in answer.items():
            for right_degree, right in poly.items():
                degree = left_degree + right_degree
                updated[degree] = K.add(updated.get(degree, K.zero),
                                        K.mul(left, right))
        answer = pt_clean(updated)
    return answer


def constant(value):
    return {} if value == K.zero else {0: value}


def linear(value):
    return {} if value == K.zero else {1: value}


def evaluate(poly, entries):
    answer = {}
    for monomial, coefficient in poly.items():
        term = constant(K.scale(K.one, coefficient))
        for variable in monomial:
            term = pt_mul(term, entries[variable])
        answer = pt_add(answer, term)
    return answer


def q_row(index):
    bits = tuple((index >> (3 - site)) & 1 for site in range(4))
    return CORE.q_orientation(bits)


def encode_pt(poly):
    return [{"T_degree": degree,
             "coefficient_1_r": [[coefficient[0].numerator,
                                   coefficient[0].denominator],
                                  [coefficient[1].numerator,
                                   coefficient[1].denominator]]}
            for degree, coefficient in sorted(poly.items())]


def raw_branch_rows():
    h = CORE.pure_hafnian()
    rows = [("e_" + "".join(map(str, edge)), CORE.e_pair(*edge))
            for edge in CORE.SUPER_EDGES]
    rows += [("t_" + "".join(map(str, triple)), CORE.t_triple(*triple))
             for triple in combinations(range(4), 3)]
    for edge in range(6):
        bit = (BRANCH >> edge) & 1
        for position in ((1, 2) if bit else (0, 3)):
            rows.append((f"cofactor_{edge}_{position}",
                         derivative(h, 4 * edge + position)))
    require(len(rows) == 22, "raw branch row count changed")
    return tuple(rows)


def component_entries(component):
    r = (Fraction(0), Fraction(1))
    r_minus_2 = K.add(r, K.scale(K.one, -2))
    if component == "v_equals_r_minus_2":
        v = r_minus_2
        alpha = (K.add(K.scale(r, 3), K.scale(K.one, -15)),
                 K.add(K.scale(K.one, 30), K.scale(r, -13)),
                 K.add(K.scale(r, 4), K.scale(K.one, -13)))
    elif component == "v_equals_minus_r":
        v = K.scale(r, -1)
        alpha = (K.add(K.scale(r, 3), K.scale(K.one, 9)),
                 K.add(K.scale(K.one, 6), K.scale(r, -5)),
                 K.add(K.scale(r, -4), K.scale(K.one, -5)))
    else:
        raise RuntimeError("unknown component")
    alpha = tuple(K.scale(value, Fraction(1, 7)) for value in alpha)
    a = (linear(alpha[0]), constant(r), linear(alpha[1]), constant(K.one),
         linear(alpha[2]), constant(v))
    b = (constant(K.one), linear(r_minus_2), constant(r), linear(K.one),
         constant(K.one), {})
    entries = []
    for edge in range(6):
        if (TERM >> edge) & 1:
            entries.extend((a[edge], b[edge],
                            constant(K.scale(K.inv(b[edge][0]), -1)), {}))
        else:
            entries.extend((a[edge], b[edge], {},
                            constant(K.scale(K.inv(a[edge][0]), -1))))
    return tuple(entries)


def replay_component(name):
    entries = component_entries(name)
    rows = raw_branch_rows()
    values = tuple(evaluate(poly, entries) for _, poly in rows)
    require(not any(values), name + " has a nonzero raw branch row")
    h = evaluate(CORE.pure_hafnian(), entries)
    require(h == {0: K.scale(K.one, 4)}, name + " H changed")
    q_values = tuple(evaluate(q_row(index), entries) for index in range(16))
    cofactors = tuple(evaluate(derivative(CORE.pure_hafnian(), index), entries)
                      for index in range(24))
    q_support = tuple(index for index, value in enumerate(q_values) if value)
    q_at_zero = tuple(index for index, value in enumerate(q_values)
                      if value.get(0, K.zero) != K.zero)
    x_support = tuple(index for index, value in enumerate(entries) if value)
    c_support = tuple(index for index, value in enumerate(cofactors) if value)
    require(q_support == EXPECTED_Q
            and q_at_zero == (1, 4, 7, 8, 11, 14)
            and x_support == EXPECTED_X,
            name + " X/Q support ledger changed")
    expected_c = ((3, 9, 10, 12, 15, 21)
                  if name == "v_equals_r_minus_2"
                  else (3, 4, 7, 17, 18, 21))
    require(c_support == expected_c, name + " cofactor support changed")

    # Hostile mutation: change a0/T by 1; some literal source row must fire.
    mutated = list(entries)
    mutated[0] = pt_add(mutated[0], linear(K.one))
    require(any(evaluate(poly, mutated) for _, poly in rows),
            name + " parametrization mutation did not fire")
    return {
        "component": name,
        "raw_rows_zero": True,
        "H": 4,
        "generic_Q_support": list(q_support),
        "T_zero_Q_support": list(q_at_zero),
        "generic_X_support": list(x_support),
        "generic_cofactor_support": list(c_support),
        "parametrization_mutation_fired": True,
    }


def component_census():
    rows = ALIGNED.derived_rows(BRANCH, TERM, deduplicate=False)
    require(len(rows) == 16, "specialized nonzero row count changed")
    ideal = ",".join(encoded for _, _, encoded in rows)
    # z is the live-term saturation inverse, not the quadratic r above.
    command = (
        f"ring R=0,({ALIGNED.variables()}),dp;ideal I={ideal},"
        "b0-1,b4-1,a3-1,z*a1*b2*a5-1;ideal G=std(I);"
        'LIB "primdec.lib";list L=minAssGTZ(I);print("BEGIN");'
        "print(size(G));print(dim(G));print(size(L));"
        "for(int i=1;i<=size(L);i++){ideal J=std(L[i]);"
        "print(dim(J));print(size(J));};print(\"END\");quit;"
    )
    completed = subprocess.run(["Singular", "-q", "-c", command],
                               text=True, capture_output=True,
                               timeout=120, check=False)
    require(completed.returncode == 0 and not completed.stderr.strip(),
            "independent minAss run failed: " + completed.stderr[-500:])
    lines = completed.stdout.splitlines()
    begin, end = lines.index("BEGIN"), lines.index("END")
    body = [line for line in lines[begin + 1:end]
            if not line.startswith("//")]
    require(body == ["30", "1", "2", "1", "14", "1", "14"],
            "independent component census changed: " + repr(body))
    return {"specialized_nonzero_rows": 16, "groebner_size": 30,
            "dimension": 1, "minimal_prime_count": 2,
            "minimal_prime_dimensions": [1, 1],
            "minimal_prime_groebner_sizes": [14, 14]}


def singular(poly):
    if not poly:
        return "0"
    return "+".join(
        f"({coefficient})*" + ("*".join(f"x{index}" for index in monomial)
                               or "1")
        for monomial, coefficient in sorted(poly.items())
    )


def mate_rows(q_zeros):
    h = CORE.pure_hafnian()
    rows = [("e_" + "".join(map(str, edge)), CORE.e_pair(*edge))
            for edge in CORE.SUPER_EDGES]
    rows += [("t_" + "".join(map(str, triple)), CORE.t_triple(*triple))
             for triple in combinations(range(4), 3)]
    rows += [(f"cofactor_{index}", derivative(h, index))
             for index in EXPECTED_X]
    rows += [(f"Q_{index}", q_row(index)) for index in q_zeros]
    require(len(rows) == 38, "mate source row count changed")
    return tuple(rows)


def specialize(poly, zero_cells):
    zeros = frozenset(zero_cells)
    return Counter({monomial: coefficient for monomial, coefficient in poly.items()
                    if not any(index in zeros for index in monomial)})


def extract_between(text, begin, end):
    require(begin in text and end in text.split(begin, 1)[1],
            "missing Singular marker")
    return text.split(begin, 1)[1].split(end, 1)[0].strip()


def replay_partner_certificate(component, forced_q_zeros):
    name = component["component"]
    zeros = tuple(component["forced_partner_zero_cells"])
    raw = mate_rows(forced_q_zeros)
    specialized = tuple((label, singular(specialize(poly, zeros)))
                        for label, poly in raw)
    stored = tuple((row["label"], row["polynomial"])
                   for row in component["generators"])
    require(specialized == stored, name + " mate raw-row ledger changed")
    variables = tuple(f"x{index}" for index in range(24) if index not in zeros)
    require(variables == tuple(component["variables_in_ring_order"]),
            name + " mate variable order changed")

    # Reconstitute the quotient certificate with full raw polynomials.  Its
    # error lies in the ideal generated by the forced zero cells; lift that
    # error and verify the resulting literal full-ring identity.
    declarations, terms = [], []
    for index, ((_, raw_poly), stored_row) in enumerate(
            zip(raw, component["generators"])):
        declarations += [f"poly g{index}=({singular(raw_poly)})",
                         f"poly c{index}=({stored_row['coefficient']})"]
        terms.append(f"c{index}*g{index}")
    zero_ideal = ",".join(f"x{index}" for index in zeros)
    prints = ";".join(
        f'print("BEGIN_{index}");print(string(L[{index + 1},1]));'
        f'print("END_{index}")' for index in range(len(zeros))
    )
    first_nonzero = next(index for index, row in enumerate(component["generators"])
                         if row["coefficient"] != "0")
    command = (
        "ring R=0,(" + ",".join(f"x{index}" for index in range(24)) + "),dp;"
        + ";".join(declarations) + ";"
        + f"poly residue={'+'.join(terms)}-1;ideal Z={zero_ideal};"
        + "matrix L=lift(Z,ideal(residue));ideal C=matrix(Z)*L;"
        + 'if(C[1]-residue==0){print("FULL_PASS");}'
        + 'else{print("FULL_FAIL");};'
        + f"poly mutation=residue-C[1]-c{first_nonzero}*g{first_nonzero};"
        + 'if(mutation!=0){print("MUTATION_PASS");}'
        + 'else{print("MUTATION_FAIL");};' + prints + ";quit;"
    )
    completed = subprocess.run(["Singular", "-q", "-c", command],
                               text=True, capture_output=True,
                               timeout=120, check=False)
    require(completed.returncode == 0 and not completed.stderr.strip(),
            name + " full-ring mate replay failed: " + completed.stderr[-500:])
    tokens = completed.stdout.split()
    require("FULL_PASS" in tokens and "MUTATION_PASS" in tokens,
            name + " full-ring identity/mutation failed")
    corrections = [extract_between(completed.stdout, f"BEGIN_{index}\n",
                                   f"\nEND_{index}")
                   for index in range(len(zeros))]
    return {
        "component": name,
        "forced_partner_zero_cells": list(zeros),
        "source_generator_count": len(raw),
        "source_nonzero_coefficient_count": component["nonzero_coefficient_count"],
        "forced_cell_correction_coefficients": corrections,
        "forced_cell_nonzero_corrections": sum(value != "0"
                                                for value in corrections),
        "literal_full_ring_identity_pass": True,
        "coefficient_deletion_mutation_fired": True,
    }


def main():
    census = component_census()
    components = [replay_component(name) for name in
                  ("v_equals_r_minus_2", "v_equals_minus_r")]
    producer_classification = json.loads(PRODUCER_CLASSIFICATION.read_text())
    producer_claimed = producer_classification.pop("result_sha256")
    producer_logical = json.dumps(producer_classification, sort_keys=True,
                                  separators=(",", ":"))
    require(sha256(producer_logical.encode("ascii")).hexdigest()
            == producer_claimed, "producer classification digest mismatch")
    producer_classification["result_sha256"] = producer_claimed
    require(producer_classification["exact_component_census"] == {
        "gauge_dimension": 1,
        "gauge_groebner_size": 30,
        "minimal_prime_count_over_Q": 2,
        "minimal_primes_exactly_match_displayed_families": True,
    }, "producer component census changed")
    for independent, frozen in zip(components,
                                   producer_classification["components"]):
        require(independent["component"] == frozen["name"]
                and independent["generic_Q_support"] ==
                frozen["T_nonzero_supports"]["Q"]
                and independent["T_zero_Q_support"] ==
                frozen["T_zero_supports"]["Q"]
                and independent["generic_X_support"] ==
                frozen["T_nonzero_supports"]["entry"]
                and independent["generic_cofactor_support"] ==
                frozen["T_nonzero_supports"]["cofactor"],
                "producer classification support ledger mismatch")
        entries = component_entries(independent["component"])
        require([encode_pt(entries[4 * edge]) for edge in range(6)]
                == frozen["a_01_02_03_12_13_23"]
                and [encode_pt(entries[4 * edge + 1]) for edge in range(6)]
                == frozen["b_01_02_03_12_13_23"],
                "producer displayed parametrization mismatch")
    certificate = json.loads(CERTIFICATE.read_text())
    claimed = certificate.pop("result_sha256")
    logical = json.dumps(certificate, sort_keys=True, separators=(",", ":"))
    require(sha256(logical.encode("ascii")).hexdigest() == claimed,
            "partner certificate digest mismatch")
    certificate["result_sha256"] = claimed
    require(tuple(certificate["fixed_left_supports"]["entry_indices"])
            == EXPECTED_X
            and tuple(certificate["fixed_left_supports"]["Q_indices"])
            == EXPECTED_Q,
            "certificate left support ledger changed")
    forced_q_zeros = tuple(sorted(15 - index for index in EXPECTED_Q))
    require(forced_q_zeros ==
            tuple(certificate["partner_forced_rows"]["Q_indices"]),
            "barred Q support force-map changed")
    for replay, frozen in zip(components, certificate["components"]):
        require(replay["component"] == frozen["component"]
                and replay["generic_cofactor_support"] ==
                frozen["forced_partner_zero_cells"],
                "cofactor-to-entry force-map changed")
    mate_audits = [replay_partner_certificate(row, forced_q_zeros)
                   for row in certificate["components"]]

    result = {
        "status": "UNAUDITED independent (11,21) classification and mate referee",
        "chart": "aligned cofactor branch11 / permanent-term21",
        "gauge": "b0=b4=a3=1; live-term product localized",
        "independent_component_census": census,
        "quadratic_field": "Q(r), r^2-2*r-1=0",
        "producer_classification_logical_sha256": producer_claimed,
        "component_replays": components,
        "support_jump": (
            "T=0 has Q support six; every T!=0 point on either line has "
            "Q support eleven."
        ),
        "partner_force_map": {
            "left_X_forces_mate_cofactors_zero": list(EXPECTED_X),
            "bar_of_left_Q_forces_mate_Q_zero": list(forced_q_zeros),
            "left_C_forces_mate_entries_zero_by_component": {
                row["component"]: row["generic_cofactor_support"]
                for row in components
            },
        },
        "producer_partner_certificate_logical_sha256": claimed,
        "partner_certificate_replays": mate_audits,
        "conclusion": (
            "The aligned (11,21) chart consists of the two replayed lines. "
            "Their T=0 points lie in the globally closed support-six orbit, "
            "and neither T!=0 stratum admits any arbitrary packet-compatible "
            "mate."
        ),
        "scope": (
            "This closes the aligned chart, not the surrounding open "
            "24-variable cofactor/permanent chart."
        ),
    }
    result_logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(result_logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("(11,21) classification + arbitrary-mate referee: PASS")
    print("components / mate units:", len(components), len(mate_audits))
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
