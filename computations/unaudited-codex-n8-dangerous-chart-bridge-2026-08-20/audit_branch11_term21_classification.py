#!/usr/bin/env python3
"""Exact classification of the final aligned survivor (branch 11, term 21)."""

from __future__ import annotations

from fractions import Fraction as F
from hashlib import sha256
import importlib.util
from itertools import combinations, permutations, product
import json
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
RADICAL = HERE.parent / "unaudited-codex-orbit0-t2-radical-2026-08-20"
SOURCE = HERE.parent / "unaudited-codex-n8-orbit0-normalized-78-2026-08-20"
OUT = HERE / "results_branch11_term21_classification.json"
BRANCH = 11
TERM = 21
GENERIC_Q = frozenset((0, 1, 2, 3, 4, 6, 7, 8, 10, 11, 14))
CONSTANT_Q = frozenset((1, 4, 7, 8, 11, 14))
LINEAR_Q = frozenset((0, 3, 6, 10))
QUADRATIC_Q = frozenset((2,))
GENERIC_X = frozenset((0, 1, 2, 4, 5, 7, 8, 9, 10, 12, 13, 15,
                       16, 17, 18, 20, 23))
ZERO_X = frozenset((1, 2, 4, 7, 9, 10, 12, 15, 17, 18, 20, 23))


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


ALIGNED = load("n8_b11t21_class_aligned",
               RADICAL / "audit_joint_aligned_zero_chart_census.py")
CORE = load("n8_b11t21_class_core",
            SOURCE / "audit_polarized_superpair_core_identity.py")
PROBE = load("n8_b11t21_class_probe",
             SOURCE / "probe_cofactor_orientation_classes.py")
S6 = load("n8_b11t21_class_s6",
          HERE / "audit_support6_component_pairwise_obstruction.py")


class K:
    """Q(r), r^2=2r+1, represented as (constant, r coefficient)."""

    zero = (F(0), F(0))
    one = (F(1), F(0))
    r = (F(0), F(1))

    @staticmethod
    def add(*values):
        return (sum(value[0] for value in values),
                sum(value[1] for value in values))

    @staticmethod
    def scale(value, scalar):
        scalar = F(scalar)
        return (scalar * value[0], scalar * value[1])

    @staticmethod
    def neg(value):
        return (-value[0], -value[1])

    @staticmethod
    def mul(left, right):
        return (left[0] * right[0] + left[1] * right[1],
                left[0] * right[1] + left[1] * right[0]
                + 2 * left[1] * right[1])

    @classmethod
    def inv(cls, value):
        conjugate = (value[0] + 2 * value[1], -value[1])
        norm = value[0] * conjugate[0] - value[1] * value[1]
        require(norm != 0, "attempted inversion of zero in Q(r)")
        return cls.scale(conjugate, 1 / norm)


def pt_clean(poly):
    return {degree: value for degree, value in poly.items() if value != K.zero}


def pt_add(*polys):
    result = {}
    for poly in polys:
        for degree, value in poly.items():
            result[degree] = K.add(result.get(degree, K.zero), value)
    return pt_clean(result)


def pt_mul(*polys):
    result = {0: K.one}
    for poly in polys:
        updated = {}
        for ld, left in result.items():
            for rd, right in poly.items():
                degree = ld + rd
                updated[degree] = K.add(updated.get(degree, K.zero),
                                        K.mul(left, right))
        result = pt_clean(updated)
    return result


def const(value):
    return {} if value == K.zero else {0: value}


def linear(value):
    return {} if value == K.zero else {1: value}


def evaluate(poly, entries):
    result = {}
    for monomial, coefficient in poly.items():
        term = {0: K.scale(K.one, coefficient)}
        for variable in monomial:
            term = pt_mul(term, entries[variable])
        result = pt_add(result, term)
    return result


def q(value):
    return CORE.q_orientation(tuple((value >> (3 - site)) & 1
                                    for site in range(4)))


def encode_k(value):
    return [[entry.numerator, entry.denominator] for entry in value]


def encode_pt(poly):
    return [{"T_degree": degree, "coefficient_1_r": encode_k(value)}
            for degree, value in sorted(poly.items())]


def exact_minimal_primes(rows):
    ideal = ",".join(encoded for _, _, encoded in rows)
    variables = ",".join([f"a{i}" for i in range(6)]
                         + [f"b{i}" for i in range(6)] + ["z"])
    # z localizes the remaining live product after b0=b4=a3=1.
    minus = (
        "b5,b4-1,b0-1,a3-1,z^2-14*z-1,5*a1+z-12,b2-a1,"
        "5*a5-z+12,b1*a1-b3,7*a4+(4*a1+5)*b3,"
        "7*a2+(5*a1-6)*b3,7*a0-(3*a1+9)*b3"
    )
    plus = (
        "b5,b4-1,b0-1,a3-1,z^2+2*z-1,a1-z-2,b2-a1,"
        "a5-z,b1*a1-b3,7*a4-(4*a1-13)*b3,"
        "7*a2+(13*a1-30)*b3,7*a0-(3*a1-15)*b3"
    )
    command = (
        f"ring R=0,({variables}),dp; ideal I={ideal},b0-1,b4-1,a3-1,"
        "z*a1*b2*a5-1; ideal G=std(I); LIB \"primdec.lib\"; "
        "list L=minAssGTZ(I); ideal Pm=" + minus + "; ideal Pp=" + plus
        + "; ideal Gm=std(Pm); ideal Gp=std(Pp); "
        'print("BEGIN");print(size(G));print(dim(G));print(size(L));'
        "for(int i=1;i<=size(L);i++){ideal J=std(L[i]);"
        "ideal rm1=reduce(J,Gm);ideal rm2=reduce(Gm,J);"
        "ideal rp1=reduce(J,Gp);ideal rp2=reduce(Gp,J);"
        'if(size(rm1)==0 and size(rm2)==0){print("MINUS");}'
        'else{if(size(rp1)==0 and size(rp2)==0){print("PLUS");}'
        'else{print("UNKNOWN");};};};print("END");quit;'
    )
    completed = subprocess.run(["Singular", "-q", "-c", command],
                               text=True, capture_output=True,
                               timeout=120, check=False)
    require(completed.returncode == 0 and not completed.stderr.strip(),
            "exact minimal-prime census failed: " + completed.stderr[-1000:])
    lines = completed.stdout.splitlines()
    begin, end = lines.index("BEGIN"), lines.index("END")
    body = [line for line in lines[begin + 1:end]
            if not line.startswith("//")]
    require(body == ["30", "1", "2", "MINUS", "PLUS"],
            f"minimal-prime census changed: {body}")
    return {
        "gauge_groebner_size": 30,
        "gauge_dimension": 1,
        "minimal_prime_count_over_Q": 2,
        "minimal_primes_exactly_match_displayed_families": True,
    }


def component(kind):
    r = K.r
    invr = K.add(r, K.scale(K.one, -2))
    b = (K.one, None, r, K.one, K.one, K.zero)
    b = list(b)
    b[1] = invr
    if kind == "v_equals_r_minus_2":
        a5 = invr
        k0 = K.scale(K.add(K.scale(r, 3), K.scale(K.one, -15)), F(1, 7))
        k2 = K.scale(K.add(K.scale(K.one, 30), K.scale(r, -13)), F(1, 7))
        k4 = K.scale(K.add(K.scale(r, 4), K.scale(K.one, -13)), F(1, 7))
        expected_c = frozenset((3, 9, 10, 12, 15, 21))
    else:
        a5 = K.neg(r)
        k0 = K.scale(K.add(K.scale(r, 3), K.scale(K.one, 9)), F(1, 7))
        k2 = K.scale(K.add(K.scale(K.one, 6), K.scale(r, -5)), F(1, 7))
        k4 = K.scale(K.neg(K.add(K.scale(r, 4), K.scale(K.one, 5))), F(1, 7))
        expected_c = frozenset((3, 4, 7, 17, 18, 21))
    a = (k0, r, k2, K.one, k4, a5)
    entries = []
    term_bits = tuple((TERM >> edge) & 1 for edge in range(6))
    for edge, bit in enumerate(term_bits):
        ap = linear(a[edge]) if edge in (0, 2, 4) else const(a[edge])
        bp = linear(b[edge]) if edge in (1, 3) else const(b[edge])
        if bit:
            cp, dp = const(K.neg(K.inv(b[edge]))), {}
        else:
            cp, dp = {}, const(K.neg(K.inv(a[edge])))
        entries.extend((ap, bp, cp, dp))

    h = CORE.pure_hafnian()
    base = [CORE.e_pair(*edge) for edge in CORE.SUPER_EDGES]
    base += [CORE.t_triple(*triple) for triple in combinations(range(4), 3)]
    for edge, bit in enumerate(tuple((BRANCH >> edge) & 1 for edge in range(6))):
        for position in ((1, 2) if bit else (0, 3)):
            base.append(PROBE.derivative(h, 4 * edge + position))
    require(not any(evaluate(poly, entries) for poly in base),
            kind + " failed a literal source row")
    h_value = evaluate(h, entries)
    require(h_value == {0: K.scale(K.one, 4)},
            kind + " pure H ceased to equal four")
    qs = tuple(evaluate(q(value), entries) for value in range(16))
    cs = tuple(evaluate(PROBE.derivative(h, index), entries)
               for index in range(24))
    q_support = frozenset(index for index, value in enumerate(qs) if value)
    c_support = frozenset(index for index, value in enumerate(cs) if value)
    x_support = frozenset(index for index, value in enumerate(entries) if value)
    require(q_support == GENERIC_Q and c_support == expected_c
            and x_support == GENERIC_X,
            kind + " generic joint support changed")
    q_zero = frozenset(index for index, value in enumerate(qs)
                       if value.get(0, K.zero) != K.zero)
    c_zero = frozenset(index for index, value in enumerate(cs)
                       if value.get(0, K.zero) != K.zero)
    x_zero = frozenset(index for index, value in enumerate(entries)
                       if value.get(0, K.zero) != K.zero)
    require(q_zero == CONSTANT_Q and len(c_zero) == 4 and x_zero == ZERO_X,
            kind + " T=0 support changed")
    return {
        "name": kind,
        "number_field": "Q(r), r^2-2r-1=0",
        "parameter": "T=b3",
        "b_01_02_03_12_13_23": [encode_pt(
            linear(value) if index in (1, 3) else const(value))
            for index, value in enumerate(b)],
        "a_01_02_03_12_13_23": [encode_pt(
            linear(value) if index in (0, 2, 4) else const(value))
            for index, value in enumerate(a)],
        "pure_H": encode_pt(h_value),
        "Q_polynomials": {str(index): encode_pt(value)
                          for index, value in enumerate(qs)},
        "cofactor_polynomials": {str(index): encode_pt(value)
                                 for index, value in enumerate(cs)},
        "T_zero_supports": {
            "entry": sorted(x_zero), "cofactor": sorted(c_zero),
            "Q": sorted(q_zero),
        },
        "T_nonzero_supports": {
            "entry": sorted(x_support), "cofactor": sorted(c_support),
            "Q": sorted(q_support),
        },
    }


def support6_orbit():
    canonical = (
        frozenset(4 * edge + position for edge in range(6)
                  for position in (1, 2)),
        frozenset((9, 10, 13, 14)),
        frozenset((3, 5, 6, 9, 10, 12)),
    )
    return frozenset(
        (S6.act_support(canonical[0], S6.raw_action_index, permutation, flips),
         S6.act_support(canonical[1], S6.raw_action_index, permutation, flips),
         S6.act_support(canonical[2], S6.q_action_index, permutation, flips))
        for permutation in permutations(range(4))
        for flips in product((0, 1), repeat=4)
    )


def main():
    rows = ALIGNED.derived_rows(BRANCH, TERM)
    require(len(rows) == 15, "(11,21) distinct literal-row count changed")
    census = exact_minimal_primes(rows)
    components = [component("v_equals_r_minus_2"),
                  component("v_equals_minus_r")]
    orbit = support6_orbit()
    require(len(orbit) == 24, "support-six joint orbit size changed")
    for row in components:
        zero = row["T_zero_supports"]
        record = (frozenset(zero["entry"]), frozenset(zero["cofactor"]),
                  frozenset(zero["Q"]))
        require(record in orbit, "T=0 record left support-six orbit")

    result = {
        "status": "UNAUDITED exact aligned (11,21) classification",
        "chart": {
            "cofactor_orientation_mask": BRANCH,
            "permanent_term_mask": TERM,
            "term_bit_1": "[[a,b],[-1/b,0]]",
            "term_bit_0": "[[a,b],[0,-1/a]]",
            "gauge": "b0=b4=a3=1 (three-cell spanning-tree torus gauge)",
        },
        "literal_distinct_row_count": len(rows),
        "exact_component_census": census,
        "components": components,
        "Q_degree_partition": {
            "constant_nonzero": sorted(CONSTANT_Q),
            "linear_nonzero_times_T": sorted(LINEAR_Q),
            "quadratic_nonzero_times_T_squared": sorted(QUADRATIC_Q),
            "identically_zero": sorted(set(range(16)) - GENERIC_Q),
        },
        "T_zero": (
            "Both lines specialize to the already globally excluded exact "
            "support-six joint orbit."
        ),
        "T_nonzero": (
            "Both lines have Q-support eleven. Their two exact joint "
            "signatures are excluded by the companion arbitrary-mate unit "
            "certificates."
        ),
        "conclusion": (
            "The full H-live aligned (11,21) boundary chart, and every B4 "
            "transform, has no compatible second colour in the diagonal "
            "78+48+144 packet."
        ),
        "scope": (
            "This is a complete set-theoretic classification of the aligned "
            "zero-cell chart. The torus gauge uses only cells already "
            "localized nonzero; it makes no claim about off-boundary releases."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("aligned (11,21) classification: PASS")
    print("rows / dimension / minimal primes:", len(rows),
          census["gauge_dimension"], census["minimal_prime_count_over_Q"])
    print("T=0 / T!=0 Q sizes:", len(CONSTANT_Q), len(GENERIC_Q))
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
