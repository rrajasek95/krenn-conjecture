#!/usr/bin/env python3
"""Exact intrinsic cap normalization for the quadratic same-hole route.

For the literal concentrated packet of 1ca72d6, view outer sites p=5 and
r=7 as the selected pair and leave q=6 among the six residual sites.  The
literal (t,t) row is already the required cap: its direct scalar is zero,
its target is pure t, and its complete ternary response is supported on the
single physical edge 14.  The same-hole P_c/R_c mate is in another outer
label and cannot change this cap.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_one_bad_second_principal_parts_companion_closure.py":
        "3612f9d7c03a3e265792543cd602f27ebf64830390f95b5bddb8d953d238c3f5",
    "computations/verify_h3_one_bad_companion_quadratic_mate_partition.py":
        "b8047fd1e610052fc47fcc0a5e11dd99d582f3ae638ad18825af46d036bc52cb",
    "computations/verify_h3_two_site_port_collision_unit.py":
        "c8b590defb44e16f398c39a986293a4d4d253e6e92047d4761046f2aecf6b489",
}
EXPECTED_LEDGER_SHA256 = (
    "c80336f4edd2bc911dedfea97b594fb04301746dce34b5fa0aa48f8f405e3659"
)

P, Q, R = 5, 6, 7
COMMON = tuple(range(5))
RESIDUAL = COMMON + (Q,)
COLORS = tuple(range(3))
A, C, T = COLORS


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency changed: {relative}: {actual}")


def clean(counter):
    return Counter({key: value for key, value in counter.items() if value})


def restricted_pair_row(base, source, p_colour, r_colour):
    """Full source coefficients with the selected p,r colours fixed."""
    output = Counter()
    for residual_word in itertools.product(COLORS, repeat=len(RESIDUAL)):
        word = [None] * 8
        word[P], word[R] = p_colour, r_colour
        for site, colour in zip(RESIDUAL, residual_word, strict=True):
            word[site] = colour
        coefficient = base.hafnian_tensor(source, tuple(range(8)))[tuple(word)]
        if coefficient:
            output[residual_word] = coefficient
    return output


def main():
    pin_dependencies()
    base = importlib.import_module(
        "verify_h3_one_bad_common_q_cap_extraction_boundary")
    closure = importlib.import_module(
        "verify_h3_one_bad_second_principal_parts_companion_closure")
    cell = base.cell
    one = Fraction(1)

    # Concentrated literal source plus the same-hole quadratic mate.  The
    # mate coefficients may be arbitrary because their outer p/r colours
    # are c, whereas the cap below selects the literal (t,t) row.
    source = clean(closure.build_eight_site_source(base, Fraction(0)))
    source[cell(1, P, C, C)] = Fraction(3)   # P_c at P_t's hole 1
    source[cell(2, R, A, C)] = Fraction(-2)  # R_c at R_a's hole 2

    # Direct 3x3 block on the selected pair p-r.
    direct = [[source.get(cell(P, R, i, k), Fraction(0))
               for k in COLORS] for i in COLORS]
    require(direct == [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
            f"the selected p-r direct block changed: {direct}")

    # Endpoint rows of the literal cap K=E_tt.  Include q=6 among the
    # residual sites so this is a physical six-site cap, not a common-block
    # projection.
    p_t = Counter()
    r_t = Counter()
    for site in RESIDUAL:
        for colour in COLORS:
            left = source.get(cell(P, site, T, colour), Fraction(0))
            right = source.get(cell(R, site, T, colour), Fraction(0))
            if left:
                p_t[(site, colour)] += left
            if right:
                r_t[(site, colour)] += right
    p_t, r_t = clean(p_t), clean(r_t)
    require(p_t == Counter({(1, T): one}), f"P_t changed: {p_t}")
    require(r_t == Counter({(4, T): one}), f"R_t changed: {r_t}")

    response = Counter()
    for (u, colour_u), left in p_t.items():
        for (v, colour_v), right in r_t.items():
            if u == v:
                continue
            response[cell(u, v, colour_u, colour_v)] += left * right
    response = clean(response)
    require(response == Counter({cell(1, 4, T, T): one}),
            f"the cap response lost one-edge support: {response}")

    # K=E_tt is one of the nine literal pair rows.
    K = [[Fraction(int(i == T and k == T)) for k in COLORS]
         for i in COLORS]
    scalar = sum((K[i][k] * direct[i][k]
                  for i in COLORS for k in COLORS), Fraction(0))
    target = tuple(K[i][i] for i in COLORS)
    require(scalar == 0, f"the cap scalar is not zero: {scalar}")
    require(target == (0, 0, 1), f"the cap target is not pure: {target}")

    # Enumerate the complete nine physical p-r row labels.  The selected
    # E_tt row has one target coefficient and one ordinary mixed residue.
    rows = {(i, k): restricted_pair_row(base, source, i, k)
            for i in COLORS for k in COLORS}
    require(len(rows) == 9, "the selected-pair nine-row packet changed")
    selected = rows[T, T]
    target_word = (T,) * len(RESIDUAL)
    ordinary_word = tuple(map(int, "122221"))
    require(selected == Counter({target_word: one, ordinary_word: one}),
            f"the tt row target/residue ledger changed: {selected}")

    # The two terms have fully literal source provenance.
    target_matching = (
        cell(1, P, T, T), cell(4, R, T, T),
        cell(0, Q, T, T), cell(2, 3, T, T),
    )
    ordinary_matching = (
        cell(1, P, T, T), cell(4, R, T, T),
        cell(0, Q, C, C), cell(2, 3, T, T),
    )
    for matching, word in ((target_matching, target_word),
                           (ordinary_matching, ordinary_word)):
        require(all(source.get(entry) == 1 for entry in matching),
                f"a pinned matching factor changed: {matching}")
        require(len({site for entry in matching for site in entry[:2]}) == 8,
                f"the pinned term stopped being a perfect matching: {matching}")
        global_word = [None] * 8
        global_word[P] = global_word[R] = T
        for site, colour in zip(RESIDUAL, word, strict=True):
            global_word[site] = colour
        require(base.hafnian_tensor(source, tuple(range(8)))[tuple(global_word)]
                == 1, f"the pinned row coefficient changed: {global_word}")

    # The same-hole quadratic mate lives in the distinct (c,t,c) row.
    mate_word = tuple(map(int, "21000121"))
    require((mate_word[P], mate_word[Q], mate_word[R]) == (C, T, C),
            "the mate moved into the cap row")
    require((T, T) != (mate_word[P], mate_word[R]),
            "the same-hole mate contaminates K=E_tt")

    # Exact a67ec1d interface: one response edge, no off-target U entries,
    # U_tt=1.  Thus this is its surviving inactive-clean boundary, while the
    # displayed sparse source itself fails the mandatory ordinary row.
    U = [[response.get(cell(1, 4, i, k), Fraction(0))
          for k in COLORS] for i in COLORS]
    require(U == [[0, 0, 0], [0, 0, 0], [0, 0, 1]],
            f"the intrinsic edge-response matrix changed: {U}")
    target_subtracted = Counter(selected)
    target_subtracted[target_word] -= 1
    target_subtracted = clean(target_subtracted)
    require(target_subtracted == Counter({ordinary_word: one}),
            f"the ordinary residue changed: {target_subtracted}")

    ledger = {
        "dependencies": PINS,
        "selected_pair": (P, R),
        "residual_sites": RESIDUAL,
        "nine_row_labels": len(rows),
        "cap": {
            "source_label": "K=E_tt in the physical p-r nine-row packet",
            "scalar": str(scalar),
            "target": tuple(str(value) for value in target),
            "response": {str(key): str(value)
                         for key, value in response.items()},
            "edge_U": [[str(value) for value in row] for row in U],
        },
        "row_readout": {
            "target_word": "22222222",
            "target_coefficient": "1",
            "ordinary_word": "12222212",
            "ordinary_residual_word": "122221",
            "ordinary_coefficient": "1",
            "target_matching": [str(entry) for entry in target_matching],
            "ordinary_matching": [str(entry) for entry in ordinary_matching],
        },
        "same_hole_mate": {
            "source_label": "(c,t,c)",
            "word": "21000121",
            "disjoint_from_cap_label": True,
        },
        "verdict": (
            "the shorter same-hole route already has the intrinsic scalar-"
            "zero pure-target one-edge cap K=E_tt; no new nullhomotopy or "
            "primitive obstruction is needed"
        ),
        "scope": (
            "exact literal quadratic same-hole normal form.  The displayed "
            "sparse coefficient point is not a full source because its "
            "ordinary word 12222212 is nonzero; the complete source row is "
            "precisely what invokes the a67ec1d unit/clean-cap dichotomy. "
            "This does not prove edge support after arbitrary higher-order "
            "deformations of P_t or R_t"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"the same-hole cap ledger changed: {digest}")

    print("h=3 one-bad same-hole intrinsic cap: PASS")
    print("cap source label: physical p-r row K=E_tt")
    print("scalar/target: 0 / (0,0,1)")
    print("whole ternary response: U_tt=1 on edge 14; all other U=0")
    print("ordinary residue: global word 12222212 (coefficient 1 in guard)")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
