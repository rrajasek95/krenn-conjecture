#!/usr/bin/env python3
"""Lane-local canonical re-numbering of the diagonal-case encoder.

UNAUDITED — lane L1, 2026-08-20. Pinned krenn-conjecture HEAD f9a3bd6.

WHY
---
The audit encoder `a9_enc.py` allocates CNF variables lazily and interleaved:
at N = 8 the first gate variable is index 8 while the last base variable is
index 5,506. The Lean ledger design (algal's `LedgerWellFormedFrom`) requires
each gate's output variable to be the next fresh index with all of its inputs
strictly earlier, so the interleaved numbering cannot be replayed by a
well-formed ledger. Reproducing `a9_enc.py`'s allocation order inside Lean
instead would be a silent-corruption hazard: a mismatch yields a *different*
theorem rather than an error.

WHAT THIS DOES
--------------
Pre-allocates every base variable `p(c, S)` (`S` an even-size subset of `V`)
in canonical order BEFORE the build runs, so that

    p(c, S)  ->  1 + c * E + rank(S)          E = #{even subsets of V}

with `rank` the position of `S` in increasing bitmask order, and every gate
variable `g(c, S, w, u)` receives an index > 3E, allocated in build order.
Nothing else changes: `build()` is the audit encoder's, untouched.

The emitted formula is therefore the SAME CLAUSE SET as the audit encoder's,
up to the variable bijection. `verify_equivalence()` checks exactly that, and
the driver refuses to write anything unless it passes.

NOT a modification of the committed package. The committed
`certified_package/` artifacts are untouched; this writes only into the lane
directory and exists to be the Lean pipeline's input.
"""
from __future__ import annotations

import os
import sys

PKG = ("/Users/rishi/workplace/krenn-conjecture/computations/"
       "unaudited-promotion-diag-2026-08-20/certified_package")
sys.path.insert(0, os.path.join(PKG, "encoders"))
sys.path.insert(0, PKG)

import a9_enc as A  # noqa: E402


def even_masks(n: int):
    """Even-size subsets of an n-set, in increasing bitmask order."""
    return [m for m in range(1 << n) if A.popcount(m) % 2 == 0]


class CanonEnc(A.Enc):
    """`a9_enc.Enc` with base variables pre-allocated in canonical order."""

    def build(self):
        evens = even_masks(self.n)
        self.even_masks = evens
        self.rank = {m: i for i, m in enumerate(evens)}
        # canonical block: p(c, S) = 1 + c*E + rank(S), for c = 0,1,2
        for c in range(3):
            for m in evens:
                self.p(c, m)
        self.n_base = self.nv
        assert self.n_base == 3 * len(evens), (self.n_base, len(evens))
        # gates are allocated by the audit encoder's own build, hence all > n_base
        super().build()
        for v, key in self.vname.items():
            if key[0] == "g":
                assert v > self.n_base, ("gate before base block", v, key)
            else:
                assert v <= self.n_base
        return self

    # ---------------------------------------------------------------- ledger
    def gate_table(self):
        """(output, inputA, inputB) for every gate, in allocation order.

        `g(c, m, w, u)` is the conjunction of `p(c, {w,u})` and
        `p(c, m - w - u)`, which is exactly what the two A3g clauses say. Both
        inputs are base variables, so `inputA, inputB <= n_base < output` and
        the ledger well-formedness invariant holds by construction.
        """
        rows = []
        for v in range(self.n_base + 1, self.nv + 1):
            kind, c, m, w, u = self.vname[v]
            assert kind == "g"
            a = self.vmap[("p", c, (1 << w) | (1 << u))]
            b = self.vmap[("p", c, m & ~((1 << w) | (1 << u)))]
            assert a <= self.n_base and b <= self.n_base
            rows.append((v, a, b))
        return rows

    def varmap_lines(self):
        out = [f"# canonical variable map, n={self.n} k={self.k} "
               f"Rs={self.Rs} z={self.z} ys={self.ys}",
               f"# base block: p(c,S) = 1 + c*{len(self.even_masks)} + rank(S), "
               f"rank over even masks in increasing order",
               f"# n_base {self.n_base}  n_vars {self.nv}  n_clauses {len(self.cls)}"]
        for v in range(1, self.n_base + 1):
            _, c, m = self.vname[v]
            out.append(f"p {v} {c} {m}")
        for v, a, b in self.gate_table():
            _, c, m, w, u = self.vname[v]
            out.append(f"g {v} {c} {m} {w} {u} and {a} {b}")
        return out


def verify_equivalence(n, Rs, k):
    """The canonical CNF is the audit CNF up to the variable bijection.

    Builds both, derives the bijection from the shared `(kind, ...)` keys, maps
    the audit clauses through it, and compares the clause sets. Also checks the
    two encoders agree on variable and clause counts.
    """
    old = A.Enc(n, Rs, k=k).build()
    new = CanonEnc(n, Rs, k=k).build()
    if old.nv != new.nv or len(old.cls) != len(new.cls):
        return False, f"size mismatch {old.nv}/{new.nv} {len(old.cls)}/{len(new.cls)}"
    perm = {}
    for v, key in old.vname.items():
        if key not in new.vmap:
            return False, f"key missing in canonical encoder: {key}"
        perm[v] = new.vmap[key]
    if len(set(perm.values())) != len(perm):
        return False, "bijection is not injective"

    def mapcl(cl):
        return tuple(sorted((perm[abs(l)] if l > 0 else -perm[-l]) for l in cl))

    a = sorted(mapcl(cl) for cl in old.cls)
    b = sorted(tuple(sorted(cl)) for cl in new.cls)
    if a != b:
        return False, "clause sets differ under the bijection"
    return True, f"OK vars={new.nv} base={new.n_base} clauses={len(new.cls)}"


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    k = 4
    probes = ([((), (), ()), ((3, 4), (5,), ()), (tuple(range(3, n - 1)),) * 3]
              if n == 8 else
              [((), (), ()), ((3,), (), (4,)), (tuple(range(3, n - 1)),) * 3])
    for Rs in probes:
        ok, msg = verify_equivalence(n, Rs, k)
        print(f"n={n} Rs={Rs}: {'PASS' if ok else 'FAIL'} {msg}")
        if not ok:
            sys.exit(1)
