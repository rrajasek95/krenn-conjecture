#!/usr/bin/env python3
"""Exact counterguard to a target-family-only quartic-tail theorem.

The displayed eight-cell q, kernel row h, and controller P satisfy

    Phi_q(h)=0,
    P*q^[2] + P*h*h*q = X_t,
    R=(P*q^[2])(t^5)=1.

Nevertheless H_0=P*(h*h)^[2] is nonzero and is not in im(Phi_q).  Thus the
bright odd rows and/or the eight off-target full families are load-bearing
in any proof that kills the common-radical cap tail.
"""

from __future__ import annotations

from hashlib import sha256
import itertools
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "computations"))

import verify_shared_reciprocal_two_bad_common_radical_cap_tail as cap
import verify_shared_reciprocal_two_bad_common_radical_provenance_system as source


PINS = {
    "computations/verify_shared_reciprocal_two_bad_common_radical_cap_tail.py":
        "f6811c3c7206b4201330a6a05c261648e933a583113394eaf3f980b639623bbb",
    "computations/verify_shared_reciprocal_two_bad_common_radical_provenance_system.py":
        "0f038dc17dbe711797318a1277cf68f751b6bb01423ccbb8eef0888ba96bedea",
}
EXPECTED_LEDGER_SHA256 = (
    "bf798e2c7ce2b0addd0aef0e9eb12cfc4cf6c351ac9bb80c5bf37d699da53094"
)

A, C, T = source.COLOURS
WORDS = tuple(itertools.product(source.COLOURS, repeat=5))


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"counterguard dependency changed: {relative}: {actual}")


def assignment():
    values = {
        # Put r=h*h, so every h_i*h_j cell has coefficient 2.  Then
        # q=g-r for g=12:tt+34:tt+3(13:ta)+4(24:aa), and
        # g^[2]=X_t+P*r^[2] on the four sites outside P.
        source.q_name(1, 2, T, T): 1,
        source.q_name(1, 2, T, A): -2,
        source.q_name(3, 4, T, T): 1,
        source.q_name(3, 4, A, A): -2,
        source.q_name(1, 3, T, A): 1,
        source.q_name(2, 4, A, A): 2,
        source.q_name(1, 4, T, A): -2,
        source.q_name(2, 3, A, A): -2,
        # P=e_t@0 and h=e_t@1+e_a@2+e_a@3+e_a@4.
        "P02": 1,
        "Qt20": 1,
        "Qt30": 1,
        "Qt40": 1,
        "Rt20": 1,
        "Rt30": 1,
        "Rt40": 1,
        "D22": 1,
    }
    # The target entries Qt_1t=Rt_1t=1 are source normalizations, not
    # polynomial variables, and are supplied by source.row_entry.
    return values


def evaluate(polynomial, values):
    answer = 0
    for monomial, coefficient in polynomial.items():
        term = coefficient
        for variable in monomial:
            term *= values.get(variable, 0)
        answer += term
    return answer


def audit_counterguard():
    values = assignment()
    zero = {word: 0 for word in WORDS}

    kernel_rows = {}
    for row in ("Qt", "Rt"):
        evaluations = {
            word: evaluate(source.phi_polynomial(row, word), values)
            for word in WORDS
        }
        require(evaluations == zero,
                f"the displayed {row} row stopped being a kernel row")
        kernel_rows[row] = evaluations

    response = {
        word: evaluate(source.phi_polynomial("P", word), values)
        for word in WORDS
    }
    product = {
        word: evaluate(
            source.product_polynomial("Qt", "Rt", word), values
        ) for word in WORDS
    }
    target = {word: int(word == (T,) * 5) for word in WORDS}
    require({word: response[word] + product[word] for word in WORDS}
            == target,
            "the displayed target full family stopped equalling X_t")
    require(response[(T,) * 5] == 1,
            "the target response R stopped being one")

    tail = {
        word: evaluate(cap.cap_tail_coefficient(word), values)
        for word in WORDS
    }
    tail = {word: value for word, value in tail.items() if value}
    expected_tail_word = (T, T, A, A, A)
    require(tail == {expected_tail_word: 12},
            f"the target-family quartic tail changed: {tail}")

    # Every q cell avoids site 0.  Hence every four-site cofactor except
    # K_0 is zero, and im(Phi_q) is the three-dimensional span of
    # e_colour@0*K_0.  Since K_0 has target coefficient one while H_0 has
    # target coefficient zero, the nonzero H_0 cannot lie in this image.
    cofactor_support = {}
    for hole in source.SITES:
        residual_sites = tuple(site for site in source.SITES if site != hole)
        coefficients = {}
        for residual_word in itertools.product(source.COLOURS, repeat=4):
            full_word = [A] * 5
            for site, colour in zip(residual_sites, residual_word):
                full_word[site] = colour
            coefficients[residual_word] = evaluate(
                source.cofactor_polynomial(hole, tuple(full_word)), values
            )
        cofactor_support[hole] = {
            word: value for word, value in coefficients.items() if value
        }
    require(cofactor_support == {
        0: {
            (T, T, T, T): 1,
            (T, T, A, A): -2,
            (T, A, T, T): -2,
            (T, A, A, A): 10,
        },
        1: {}, 2: {}, 3: {}, 4: {},
    }, f"the counterguard cofactor support changed: {cofactor_support}")
    require(tail[(T, T, A, A, A)] != 0
            and tail.get((T,) * 5, 0) == 0,
            "the tail/image separation witness changed")

    return {
        "q_cells": 8,
        "kernel_row": "h=e_t@1+e_a@2+e_a@3+e_a@4",
        "controller": "P=e_t@0",
        "target_family": "P*q^[2]+P*h*h*q=X_t",
        "target_response_R": response[(T,) * 5],
        "quartic_tail": "12*e_t@0*e_t@1*e_a@2*e_a@3*e_a@4",
        "phi_rank": 3,
        "tail_in_imPhi": False,
    }


def main():
    pin_dependencies()
    counterguard = audit_counterguard()
    ledger = {
        "pins": PINS,
        "counterguard": counterguard,
        "verdict": (
            "kernel rows, D22*R=1, and the complete F22 tensor do not "
            "force the quartic cap tail to vanish or enter im(Phi)"
        ),
        "scope": (
            "exact rational target-family counterguard; it does not "
            "satisfy the two bright odd rows or the other eight full families"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"target-family counterguard changed: {digest}")

    print("shared reciprocal target-family cap-tail counterguard: PASS")
    print("R=1 and F22=X_t, but H_0=12*e_tte_aaa is outside im(Phi)")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
