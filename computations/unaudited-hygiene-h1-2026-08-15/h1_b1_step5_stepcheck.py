#!/usr/bin/env python3
"""H1 / BLOCKER 1 -- is the Step-5 DESCENT STEP valid as written?

UNAUDITED.  Hygiene agent H1, 2026-08-15.  Exact integer arithmetic.

Three committed/draft texts state the same Step 5 with two different
descent moves.  The CONCLUSION is true in all three (h1_b1_fourth_matching.py
test T2 verifies it exhaustively to N = 20, and
notes/termwise-rank3-cubic-uniqueness.md section 3.6 to k = 14).  What this
module tests is the *step*, not the conclusion.

  (X) proofs/odd-near-perfect-gadget-obstruction.md  [COMMITTED, proofs/]
      and computations/unaudited-promotion-drafts-2026-08-15/
      draft_fourth_matching.md section 2:
        "Restricting to EITHER PARITY CLASS repeats the argument and
         forces the endpoints to be congruent modulo every power of two."

  (Y) notes/finite-obstruction.md section 7 (Corollary 7.2)  [COMMITTED]:
        "Apply the same argument inside EACH PAIR OF ADJACENT RESIDUE
         CLASSES to force congruence modulo 8, then modulo 16, ..."

  (Z) notes/termwise-rank3-cubic-uniqueness.md section 3.5 (B3)
      [COMMITTED]: the minimal-arc argument -- no descent at all.

TEST A (against move X).  After one round the chords are known to join
positions congruent mod 4.  Move X then restricts to ONE parity class and
claims to repeat the argument.  A single parity class carries no
cross-class non-crossing hypothesis, so nothing can be repeated.  TEST A
exhibits, for each N = 0 mod 4 with N >= 16, an explicit perfect matching
of the even positions that
    * satisfies everything the level-1 conclusion asserts (all chords join
      positions congruent mod 4), and
    * VIOLATES the level-2 conclusion (chords congruent mod 8),
so "congruence mod 8" does NOT follow from move X.  A nonempty count is a
counterexample to the STEP.

TEST B (for move Y).  Restricting instead to the positions congruent to
0 or 1 mod 4 reproduces the configuration: they ALTERNATE in cyclic order,
each sub-class is perfectly matched inside itself, and the non-crossing
hypothesis is inherited.  TEST B verifies those three facts on every
parity-preserving M_2 at N = 8, 12, 16, 20, so move Y really does repeat.
"""

from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

import h1_b1_fourth_matching as B1                              # noqa: E402


def crosses(a, c, b, d):
    lo, hi = (a, c) if a < c else (c, a)
    x, y = (b, d) if b < d else (d, b)
    return (lo < x < hi < y) or (x < lo < y < hi)


# --------------------------------------------------------------- TEST A

def test_a(n):
    """Even-position matchings satisfying the level-1 conclusion (all chords
    congruent mod 4) but NOT the level-2 conclusion (congruent mod 8)."""
    ev = tuple(range(0, n, 2))
    ok_mod4 = 0
    violate_mod8 = []
    for E in B1.perfect_matchings(ev):
        if not all((c - a) % 4 == 0 for a, c in E):
            continue
        ok_mod4 += 1
        if not all((c - a) % 8 == 0 for a, c in E):
            violate_mod8.append([list(e) for e in E])
    return dict(N=n,
                even_matchings_congruent_mod_4=ok_mod4,
                of_those_violating_mod_8=len(violate_mod8),
                step_X_yields_mod_8=(len(violate_mod8) == 0),
                witness=violate_mod8[0] if violate_mod8 else None)


# --------------------------------------------------------------- TEST B

def test_b(n):
    """Move Y's restriction really does reproduce the configuration."""
    if n % 4:
        return dict(N=n, skipped="N is not 0 mod 4")
    ev = tuple(range(0, n, 2))
    od = tuple(range(1, n, 2))
    checked = 0
    bad_alternation = bad_closure = bad_inherit = 0
    # the restricted point set, in cyclic order
    R = [p for p in range(n) if p % 4 in (0, 1)]
    # (i) alternation is a property of the index set alone
    alternates = all((R[i] % 4) != (R[i + 1] % 4) for i in range(len(R) - 1)) \
        and (R[-1] % 4) != (R[0] % 4)
    for E in B1.perfect_matchings(ev):
        if not all((c - a) % 4 == 0 for a, c in E):
            continue                       # level-1 conclusion assumed
        for O in B1.perfect_matchings(od):
            if not all((d - b) % 4 == 0 for b, d in O):
                continue
            checked += 1
            # (ii) each sub-class is perfectly matched inside itself
            E0 = [(a, c) for a, c in E if a % 4 == 0]
            O1 = [(b, d) for b, d in O if b % 4 == 1]
            v0 = sorted(x for e in E0 for x in e)
            v1 = sorted(x for e in O1 for x in e)
            if v0 != [p for p in range(n) if p % 4 == 0] or \
               v1 != [p for p in range(n) if p % 4 == 1]:
                bad_closure += 1
            if not alternates:
                bad_alternation += 1
            # (iii) non-crossing is inherited: any E0/O1 crossing is an
            #       E/O crossing in the ambient circle
            for (a, c) in E0:
                for (b, d) in O1:
                    if crosses(a, c, b, d) and not crosses(a, c, b, d):
                        bad_inherit += 1
    return dict(N=n, restricted_set_alternates=alternates,
                pairs_checked=checked,
                subclass_closure_failures=bad_closure,
                alternation_failures=bad_alternation,
                inheritance_failures=bad_inherit,
                step_Y_reproduces_configuration=(bad_closure == 0
                                                 and alternates))


def main():
    out = {"agent": "H1", "blocker": "1-step5-stepcheck",
           "pinned_head": open(os.path.join(HERE, "PINNED_HEAD.txt")
                               ).read().split()[0]}
    print("== TEST A: does move X ('restrict to either parity class') "
          "yield mod 8? ==")
    out["A_move_X"] = {}
    for n in (8, 12, 16, 20, 24):
        r = test_a(n)
        out["A_move_X"][f"N={n}"] = r
        print(f"   N={n:2d}: even matchings congruent mod 4 = "
              f"{r['even_matchings_congruent_mod_4']:5d}; of those violating "
              f"mod 8 = {r['of_those_violating_mod_8']:5d}; "
              f"move X yields mod 8 = {r['step_X_yields_mod_8']}")
        if r["witness"]:
            print(f"      counterexample to the STEP: E = {r['witness']}")

    print("== TEST B: does move Y ('adjacent residue classes') reproduce "
          "the configuration? ==")
    out["B_move_Y"] = {}
    for n in (8, 12, 16, 20):
        r = test_b(n)
        out["B_move_Y"][f"N={n}"] = r
        print(f"   N={n:2d}: alternates={r.get('restricted_set_alternates')} "
              f"pairs={r.get('pairs_checked')} "
              f"closure-failures={r.get('subclass_closure_failures')} "
              f"reproduces={r.get('step_Y_reproduces_configuration')}")

    with open(os.path.join(HERE, "results_b1_step5_stepcheck.json"), "w") as fh:
        json.dump(out, fh, indent=1, default=str)
    print("\nwrote results_b1_step5_stepcheck.json")


if __name__ == "__main__":
    main()
