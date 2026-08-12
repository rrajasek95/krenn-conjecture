#!/usr/bin/env python3
"""Exact audit of the conditional C4 coherence--curvature square.

This is deliberately a theorem-interface checker, not a new chart census.
It verifies the universal E2/E3/E4 polynomial identities, pins the two exact
physical C4 audits on which the scope statement depends, and records the
linear zero-indeterminacy criterion.  In particular it does *not* infer
primitive acyclicity from determinantal coherence.
"""

from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEPENDENCIES = {
    "computations/verify_n8_chart26_c4_exchange_3cell.py":
        "4398d15df3a5f0b34c2745fdb7087a289452ed03983d22431c4f20d116f019c6",
    "computations/verify_n8_chart26_c4_primitive_colon.py":
        "549d66f4405fe0492893b42d235baecade27d04d882eda583b65b646f38a078b",
    "notes/hafnian-path-forest-straightening.md":
        "0713791a87b692da809b5f64fe8d757d6454d59e550a859b8d7b7dea68598921",
    "notes/augmented-hpl-terminal-bockstein-lemma.md":
        "de1d34da41ed3f845003adec41cb2907b8dc4917ed9c75f6b375ea1aea021f89",
}
EXPECTED_LEDGER_SHA256 = (
    "471c4106a4576bbd552e8ab51f1bbd08cda045c6a8b9aa3ad59b9949d6458426"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


class Poly:
    """Tiny exact polynomial ring over Z, enough for the universal minors."""

    def __init__(self, terms=None):
        self.terms = {
            tuple(sorted(monomial)): coefficient
            for monomial, coefficient in (terms or {}).items()
            if coefficient
        }

    @classmethod
    def var(cls, name):
        return cls({(name,): 1})

    def __add__(self, other):
        out = defaultdict(int, self.terms)
        for monomial, coefficient in other.terms.items():
            out[monomial] += coefficient
        return Poly(out)

    def __neg__(self):
        return Poly({monomial: -coefficient
                     for monomial, coefficient in self.terms.items()})

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        out = defaultdict(int)
        for left, left_coefficient in self.terms.items():
            for right, right_coefficient in other.terms.items():
                out[tuple(sorted(left + right))] += (
                    left_coefficient * right_coefficient
                )
        return Poly(out)

    def __rmul__(self, scalar):
        return Poly({monomial: scalar * coefficient
                     for monomial, coefficient in self.terms.items()})

    def __bool__(self):
        return bool(self.terms)


def file_sha256(path):
    return sha256(path.read_bytes()).hexdigest()


def audit():
    for relative, expected in DEPENDENCIES.items():
        actual = file_sha256(ROOT / relative)
        require(actual == expected, f"dependency changed: {relative}: {actual}")

    states = range(4)
    a = {state: Poly.var(f"a{state}") for state in states}
    b = {state: Poly.var(f"b{state}") for state in states}
    h = {state: Poly.var(f"h{state}") for state in states}

    def p(row, left, right):
        return row[left] * h[right] - row[right] * h[left]

    def delta(left, right):
        return a[left] * b[right] - a[right] * b[left]

    e2_instances = 0
    for left in states:
        for right in states:
            if left == right:
                continue
            first = b[left] * p(a, left, right) - a[left] * p(b, left, right)
            second = b[right] * p(a, left, right) - a[right] * p(b, left, right)
            require(not (first - delta(left, right) * h[left]),
                    "first E2 endpoint identity changed")
            require(not (second - delta(left, right) * h[right]),
                    "second E2 endpoint identity changed")
            e2_instances += 2

    def c(left, middle, right):
        by_b = (b[left] * p(a, middle, right)
                - b[middle] * p(a, left, right)
                + b[right] * p(a, left, middle))
        by_a = (-a[left] * p(b, middle, right)
                + a[middle] * p(b, left, right)
                - a[right] * p(b, left, middle))
        curvature = -(delta(middle, right) * h[left]
                      - delta(left, right) * h[middle]
                      + delta(left, middle) * h[right])
        require(not (by_b - by_a), "two E3 presentations changed")
        require(not (by_b - curvature), "E3 Bianchi identity changed")
        return by_b

    e3 = {}
    for omitted in states:
        triple = tuple(state for state in states if state != omitted)
        e3[omitted] = c(*triple)

    for row_name, row in (("M", a), ("N", b)):
        tetrahedron = Poly()
        for omitted in states:
            tetrahedron += ((1 if omitted % 2 == 0 else -1)
                            * (row[omitted] * e3[omitted]))
        require(not tetrahedron, f"{row_name} E4 boundary changed")

    # A homotopy is defined only modulo cycles.  This two-column toy is the
    # exact linear criterion used in the note: d(x,y)=x has kernel <(0,1)>.
    # The first readout kills the ambiguity; the second does not.  Thus d^2
    # or cellular coherence alone cannot imply zero indeterminacy.
    kernel_generator = (0, 1)
    good_readout = (1, 0)
    bad_readout = (0, 1)
    dot = lambda left, right: sum(x * y for x, y in zip(left, right))
    require(dot(good_readout, kernel_generator) == 0,
            "good readout stopped killing homotopy ambiguity")
    require(dot(bad_readout, kernel_generator) == 1,
            "coherence counterguard lost its ambiguity")

    ledger = {
        "universal_identities": {
            "E2_ordered_endpoint_instances": e2_instances,
            "E3_three_state_faces": len(e3),
            "E4_row_Laplace_boundaries": 2,
        },
        "relative_square": {
            "normalized_boundary":
                "P^M_cd/a_c-P^N_cd/b_c=Delta_cd*H_c/(a_c*b_c)",
            "flat_branch":
                "Delta_cd=0 gives one-sided transport after source localization",
            "curved_branch":
                "Delta_cd*H_c is literal; H_c is a carrier on D(Delta_cd)",
        },
        "source_gate": {
            "primitive_division": "common-core source/boundary saturation",
            "flat_base_change": "Delta-Tor control or derived fibre",
            "zero_indeterminacy":
                "terminal readout annihilates flat primitive homology",
        },
        "sharp_negative": (
            "the pinned chart26 primitive-colon audit has coherent E3/E4 "
            "but nonzero primitive C4-colon classes; coherence is not acyclicity"
        ),
        "dependency_digests": DEPENDENCIES,
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return ledger, digest


def main():
    ledger, digest = audit()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"relative C4 square ledger changed: {digest}")
    print("local C4 coherence--curvature relative square: PASS")
    print("coherence is exact; source saturation and zero-indeterminacy remain gates")
    print(json.dumps(ledger, sort_keys=True))
    print("sha256:", digest)


if __name__ == "__main__":
    main()
