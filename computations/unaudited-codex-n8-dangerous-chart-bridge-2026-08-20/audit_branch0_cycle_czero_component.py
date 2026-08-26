#!/usr/bin/env python3
"""Exact source replay of an H-live four-cycle defect component.

We work in the branch-0 block chart

    M_e = [[a_e,b_e],[-(1+a_e*d_e)/b_e,d_e]]

and on the defect cycle S={1,2,3,4}.  The residual clone torus fixes
b2=b4=b5=1 and a common scale fixes d2=1.  Over

    Q(r,t,u),  r^2+2*r-1=0,

the formulas below give a two-parameter generic point with c_e=0 on every
defect edge.  This script evaluates the literal six permanent, four
triangle, twelve selected-cofactor rows and the pure Hafnian.  Thus the
k4-cycle closure before localizing the c_e is NONUNIT; this makes no claim
about the true both-term-live interior, and uses no Groebner nonunit inference.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from itertools import permutations, product
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_branch0_cycle_czero_component.json"
SOURCE = (HERE.parent
          / "unaudited-codex-n8-orbit0-normalized-78-2026-08-20"
          / "probe_cofactor_orientation_classes.py")
ALIGNED_SOURCE = (HERE.parent
                  / "unaudited-codex-orbit0-t2-radical-2026-08-20"
                  / "audit_joint_aligned_zero_chart_census.py")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


PROBE = load("n8_cycle_czero_source", SOURCE)
ALIGNED = load("n8_cycle_czero_aligned", ALIGNED_SOURCE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


@dataclass(frozen=True)
class K:
    """a+b*r in Q[r]/(r^2+2r-1)."""

    a: Fraction = Fraction(0)
    b: Fraction = Fraction(0)

    def __add__(self, other):
        other = as_k(other)
        return K(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return K(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-as_k(other))

    def __rsub__(self, other):
        return as_k(other) - self

    def __mul__(self, other):
        other = as_k(other)
        # r^2=1-2r.
        return K(self.a * other.a + self.b * other.b,
                 self.a * other.b + self.b * other.a
                 - 2 * self.b * other.b)

    __rmul__ = __mul__

    def __bool__(self):
        return bool(self.a or self.b)

    def encode(self):
        return [[self.a.numerator, self.a.denominator],
                [self.b.numerator, self.b.denominator]]


def as_k(value):
    if isinstance(value, K):
        return value
    return K(Fraction(value), Fraction(0))


ZERO_K = K()
ONE_K = K(Fraction(1))
R = K(Fraction(0), Fraction(1))


@dataclass(frozen=True)
class L:
    """A Laurent polynomial in t,u with coefficients in Q(r)."""

    terms: tuple = ()

    @classmethod
    def from_dict(cls, values):
        cleaned = tuple(sorted((tuple(exponent), as_k(coefficient))
                               for exponent, coefficient in values.items()
                               if coefficient))
        return cls(cleaned)

    def dictionary(self):
        return dict(self.terms)

    def __add__(self, other):
        other = as_l(other)
        answer = Counter(self.dictionary())
        answer.update(other.dictionary())
        return L.from_dict(answer)

    __radd__ = __add__

    def __neg__(self):
        return L.from_dict({exponent: -coefficient
                            for exponent, coefficient in self.terms})

    def __sub__(self, other):
        return self + (-as_l(other))

    def __rsub__(self, other):
        return as_l(other) - self

    def __mul__(self, other):
        other = as_l(other)
        answer = Counter()
        for left, lc in self.terms:
            for right, rc in other.terms:
                answer[(left[0] + right[0], left[1] + right[1])] += lc * rc
        return L.from_dict(answer)

    __rmul__ = __mul__

    def __pow__(self, power):
        require(power >= 0, "negative Laurent-object power")
        answer = ONE
        for _ in range(power):
            answer *= self
        return answer

    def __bool__(self):
        return bool(self.terms)

    def encode(self):
        return [{"t_power": exponent[0], "u_power": exponent[1],
                 "coefficient": coefficient.encode()}
                for exponent, coefficient in self.terms]


def as_l(value):
    if isinstance(value, L):
        return value
    return L.from_dict({(0, 0): as_k(value)})


ZERO = L()
ONE = as_l(1)
T = L.from_dict({(1, 0): ONE_K})
T_INV = L.from_dict({(-1, 0): ONE_K})
U = L.from_dict({(0, 1): ONE_K})
RR = as_l(R)


def evaluate(raw, values):
    answer = ZERO
    for monomial, coefficient in raw.items():
        term = as_l(coefficient)
        for index in monomial:
            term *= values[index]
        answer += term
    return answer


def point():
    # Edge order is 01,02,03,12,13,23 and entry order is a,b,c,d.
    a = (
        2 * (RR + 2) * (1 - U) * T_INV,
        -RR - 2,
        -ONE,
        -T_INV,
        (RR + 2) * T_INV,
        ZERO,
    )
    b = (
        T,
        (RR + 2) * (U - 1) - T,
        ONE,
        U * T_INV,
        ONE,
        ONE,
    )
    c = (-T_INV, ZERO, ZERO, ZERO, ZERO, -ONE)
    d = (ZERO, RR, ONE, T, -RR * T, ZERO)
    return tuple(value for edge in range(6)
                 for value in (a[edge], b[edge], c[edge], d[edge]))


def mod7(value, r=2, t=1, u=5):
    total = 0
    for exponent, coefficient in value.terms:
        scalar = (int(coefficient.a) + int(coefficient.b) * r) % 7
        total += scalar * pow(t, exponent[0], 7) * pow(u, exponent[1], 7)
    return total % 7


def main():
    values = point()
    equations, hafnian = PROBE.equations((0,) * 6)
    labels = ([f"permanent_{edge}" for edge in range(6)]
              + [f"triangle_{triple}" for triple in ("012", "013", "023", "123")]
              + [f"cofactor_{edge}_{position}"
                 for edge in range(6) for position in (0, 3)])
    evaluated = tuple(evaluate(row, values) for row in equations)
    h_value = evaluate(hafnian, values)
    require(len(evaluated) == len(labels) == 22,
            "literal branch-0 row count changed")
    require(not any(evaluated), "a literal branch-0 source row is nonzero")
    require(h_value, "the pure Hafnian vanished identically")

    blocks = tuple(values[4 * edge:4 * edge + 4] for edge in range(6))
    defect_edges = (1, 2, 3, 4)
    require(tuple(blocks[edge][2] for edge in defect_edges)
            == (ZERO,) * 4, "a defect c entry is nonzero")
    require(all(blocks[edge][0] and blocks[edge][1] and blocks[edge][3]
                for edge in defect_edges),
            "a generically localized defect entry vanished")
    require(all(blocks[edge][1] for edge in range(6)),
            "a generically localized b entry vanished")
    require((blocks[2][1], blocks[4][1], blocks[5][1], blocks[2][3])
            == (ONE, ONE, ONE, ONE), "the gauge conditions changed")

    expected_mod7 = (3, 3, 6, 6, 4, 0, 1, 1, 5, 2, 1, 5)
    actual_mod7 = tuple(
        [mod7(blocks[edge][0]) for edge in range(6)]
        + [mod7(blocks[edge][1]) for edge in (0, 1, 3)]
        + [mod7(blocks[edge][3]) for edge in (1, 3, 4)]
    )
    require(actual_mod7 == expected_mod7,
            f"the p=7 specialization changed: {actual_mod7}")
    require(mod7(h_value) == 4, "the p=7 Hafnian specialization changed")

    # On c1=c2=c3=c4=0 the live term changes from the all-offdiagonal
    # term mask 63 to the diagonal-on-cycle mask 33 (edges 0 and 5 remain
    # offdiagonal).  This pair is in the already enumerated aligned orbit of
    # the support-six representative (branch,term)=(51,63).
    aligned_actions = tuple(
        (switches, permutation)
        for switches in product((0, 1), repeat=4)
        for permutation in permutations(range(4))
        if ALIGNED.act_mask(51, switches, permutation) == 0
        and ALIGNED.act_mask(63, switches, permutation) == 33
    )
    require(len(aligned_actions) == 16,
            "the (51,63) to (0,33) aligned orbit map changed")

    # Hostile mutation: deleting a single summand of a0 destroys a source row.
    mutated = list(values)
    mutated[0] = mutated[0] - 2 * (RR + 2) * T_INV
    mutated_rows = tuple(evaluate(row, mutated) for row in equations)
    require(any(mutated_rows), "hostile mutation did not fire")

    result = {
        "status": "UNAUDITED exact branch-0 four-cycle component",
        "number_field": "Q(r,t,u), r^2+2r-1=0",
        "defect_support": list(defect_edges),
        "aligned_chart": {"branch_mask": 0, "term_mask": 33,
                          "orbit_representative": [51, 63],
                          "mapping_action_count": len(aligned_actions)},
        "gauge": ["b2=1", "b4=1", "b5=1", "d2=1"],
        "blocks": [[value.encode() for value in block] for block in blocks],
        "literal_source_rows": labels,
        "zero_row_count": len(evaluated),
        "pure_hafnian": h_value.encode(),
        "p7_specialization": {
            "r_t_u": [2, 1, 5],
            "a0_through_a5_b0_b1_b3_d1_d2_d3_d4": list(actual_mod7),
            "pure_hafnian": mod7(h_value),
        },
        "hostile_mutation_nonzero_rows": sum(bool(row) for row in mutated_rows),
        "conclusion": (
            "The k4-cycle closure obtained without localizing the four c_e "
            "entries contains this H-live characteristic-zero component. It "
            "is the aligned (branch,term)=(0,33) chart, in the orbit of "
            "(51,63), so the existing aligned pairwise theorem handles it. "
            "It is not a point of the true both-term-live interior."
        ),
        "scope": (
            "This gives one explicit two-parameter component on the c=0 face. "
            "It does not decide the localization in which every 1+a_e*d_e, "
            "equivalently every c_e, is also required nonzero."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("branch-0 k4-cycle c=0 component: PASS")
    print("rows / H terms / mutation rows:", len(evaluated),
          len(h_value.terms), sum(bool(row) for row in mutated_rows))
    print("H:", h_value.encode())
    print("p7 specialization:", actual_mod7, "H", mod7(h_value))
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
