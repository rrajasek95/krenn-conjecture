#!/usr/bin/env python3
"""Direct decision of the diagonal exact-source problem over F_2.

UNAUDITED — lane L1, 2026-08-20. Writes only into the lane directory.

WHY
---
Our N = 8 theorem (W29-T1) is proved through a Boolean *abstraction*: the
87-orbit CNFs have one free Boolean per hafnian and are a relaxation of the
algebra. Over a general field that is the only tractable route. But F_2 is
FINITE, so on the F_2 slice the algebra itself is decidable, and we can check
the theorem WITHOUT the abstraction, the normal form, the case ledger, or the
orbit reduction.

That is what this script does. It encodes the *actual* weight bits and the
*actual* hafnians as a circuit, and asks a SAT solver whether a diagonal exact
source exists over F_2.

  variables      x[c][{u,v}]  in F_2, one per colour and unordered pair
                 (a block-diagonal ternary weighting: three independent
                 symmetric weight functions, exactly Section 1 of
                 proof_eight-site-diagonal-obstruction.md)
  hafnians       haf_c(S) = XOR over perfect matchings M of S of
                 AND over e in M of x[c][e]           (Tseitin-encoded)
  constant rows  haf_c(V) = 1 for c = 0,1,2
                 (over F_2, "nonzero" and "= 1" coincide, so this is
                 simultaneously the Phi = 1 and the Phi != 0 form)
  mixed rows     for every ordered partition V = S_0 + S_1 + S_2 into even
                 parts with max |S_c| != N:  haf_0(S_0) haf_1(S_1) haf_2(S_2) = 0
                 i.e. the clause (-h0 or -h1 or -h2); an empty part has
                 haf = 1 and contributes no literal.

Expected, and each is a control on the others:
  N = 4  SAT    -- the exceptional source survives in characteristic two
  N = 6  UNSAT
  N = 8  UNSAT  -- our headline, on the F_2 slice, with no abstraction

A SAT verdict at N = 4 is mandatory: a pipeline that refutes N = 4 would be
refuting something true (hazard-ledger item 18, and Section 7.3 of the proof
document).

Usage:  python3 f2_direct.py [N ...]
"""
from __future__ import annotations

import itertools
import os
import subprocess
import sys
import tempfile

ROOT = "/Users/rishi/workplace/krenn-conjecture"
CAD = f"{ROOT}/computations/unaudited-hygiene-h1-2026-08-15/tools/cadical/build/cadical"


class CNF:
    def __init__(self):
        self.n = 0
        self.cls: list[tuple[int, ...]] = []

    def new(self) -> int:
        self.n += 1
        return self.n

    def add(self, *lits: int) -> None:
        self.cls.append(tuple(lits))

    def const_true(self) -> int:
        v = self.new()
        self.add(v)
        return v

    def AND(self, ins: list[int]) -> int:
        """t <-> conjunction of ins."""
        if len(ins) == 1:
            return ins[0]
        t = self.new()
        for x in ins:
            self.add(-t, x)
        self.add(t, *[-x for x in ins])
        return t

    def XOR2(self, a: int, b: int) -> int:
        """z <-> a xor b."""
        z = self.new()
        self.add(-z, a, b)
        self.add(-z, -a, -b)
        self.add(z, -a, b)
        self.add(z, a, -b)
        return z

    def XOR(self, ins: list[int]) -> int:
        assert ins
        acc = ins[0]
        for x in ins[1:]:
            acc = self.XOR2(acc, x)
        return acc

    def dimacs(self) -> str:
        head = f"p cnf {self.n} {len(self.cls)}\n"
        return head + "".join(" ".join(map(str, c)) + " 0\n" for c in self.cls)


def perfect_matchings(sites: tuple[int, ...]):
    """All perfect matchings of an even-size tuple of sites."""
    if not sites:
        yield ()
        return
    a, rest = sites[0], sites[1:]
    for i, b in enumerate(rest):
        pair = (a, b)
        remain = rest[:i] + rest[i + 1:]
        for m in perfect_matchings(remain):
            yield (pair,) + m


def build(N: int):
    V = tuple(range(N))
    pairs = [(u, v) for u in V for v in V if u < v]
    F = CNF()
    TRUE = F.const_true()

    # edge bits: three independent symmetric weight functions
    x = {(c, p): F.new() for c in range(3) for p in pairs}

    evens = [S for k in range(0, N + 1, 2) for S in itertools.combinations(V, k)]
    haf: dict[tuple[int, tuple[int, ...]], int] = {}
    n_match = 0
    for c in range(3):
        for S in evens:
            if len(S) == 0:
                haf[(c, S)] = TRUE                       # haf(t^c | empty) = 1
                continue
            terms = []
            for m in perfect_matchings(S):
                terms.append(F.AND([x[(c, e)] for e in m]))
                n_match += 1
            haf[(c, S)] = F.XOR(terms)

    # constant rows: haf_c(V) = 1
    for c in range(3):
        F.add(haf[(c, V)])

    # mixed rows: every ordered even partition with max part != N
    n_mixed = 0
    for assign in itertools.product(range(3), repeat=N):
        parts = tuple(tuple(v for v in V if assign[v] == c) for c in range(3))
        if any(len(p) % 2 for p in parts):
            continue
        if max(len(p) for p in parts) == N:
            continue
        lits = [-haf[(c, parts[c])] for c in range(3) if len(parts[c]) > 0]
        assert lits
        F.add(*lits)
        n_mixed += 1
    return F, x, pairs, n_match, n_mixed


def solve(F: CNF):
    d = tempfile.mkdtemp(prefix="f2_")
    p = os.path.join(d, "f.cnf")
    with open(p, "w") as f:
        f.write(F.dimacs())
    r = subprocess.run([CAD, p, "--no-binary"], capture_output=True, text=True)
    model = {}
    if r.returncode == 10:
        for line in r.stdout.splitlines():
            if line.startswith("v "):
                for tok in line[2:].split():
                    n = int(tok)
                    if n:
                        model[abs(n)] = n > 0
    os.unlink(p)
    return {10: "SAT", 20: "UNSAT"}.get(r.returncode, f"rc{r.returncode}"), model


def haf_f2(t: dict, S: tuple[int, ...]) -> int:
    """Hafnian mod 2, computed directly from a weight dict, for verification."""
    if len(S) % 2:
        return 0
    acc = 0
    for m in perfect_matchings(S):
        prod = 1
        for e in m:
            prod &= t.get(e, 0)
        acc ^= prod
    return acc


def verify_model(N, x, pairs, model):
    """Independent re-check of a SAT model against the algebra, no CNF involved."""
    V = tuple(range(N))
    t = [{p: (1 if model.get(x[(c, p)], False) else 0) for p in pairs} for c in range(3)]
    ok_const = all(haf_f2(t[c], V) == 1 for c in range(3))
    bad_mixed = 0
    for assign in itertools.product(range(3), repeat=N):
        parts = tuple(tuple(v for v in V if assign[v] == c) for c in range(3))
        if max(len(p) for p in parts) == N:
            continue
        prod = 1
        for c in range(3):
            prod &= haf_f2(t[c], parts[c])
        if prod:
            bad_mixed += 1
    return ok_const, bad_mixed, t


def main(Ns):
    print("Direct F_2 decision of the DIAGONAL exact-source problem")
    print("(no Boolean abstraction, no normal form, no case ledger)\n")
    for N in Ns:
        F, x, pairs, n_match, n_mixed = build(N)
        verdict, model = solve(F)
        print(f"N={N}: {F.n} vars, {len(F.cls)} clauses, "
              f"{3 * len(pairs)} weight bits, {n_match} matching gates, "
              f"{n_mixed} mixed rows  ->  {verdict}")
        if verdict == "SAT":
            ok_const, bad_mixed, t = verify_model(N, x, pairs, model)
            print(f"      model re-checked directly against the algebra: "
                  f"all constant hafnians = 1: {ok_const}; "
                  f"mixed rows violated: {bad_mixed}")
            for c in range(3):
                sup = sorted(p for p in pairs if t[c][p])
                print(f"      colour {c} support: {sup}")


if __name__ == "__main__":
    Ns = [int(a) for a in sys.argv[1:]] or [4, 6, 8]
    main(Ns)
