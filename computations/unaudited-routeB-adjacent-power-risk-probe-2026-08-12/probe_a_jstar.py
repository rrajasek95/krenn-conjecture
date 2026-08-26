#!/usr/bin/env python3
"""RISK PROBE A/D: reproduce b63c76c's J_* claim from committed constructors.

Committed constructor (snapshot of commit b63c76c):
  computations/verify_diagonal_rees_saturation_cap_jet_bockstein.py
    diagonal_data(block, a):
        alpha = block[a][a]; tau = trace(block); beta = tau - alpha
        k0 = E_aa ; k1 = tau*k0 - alpha*I ; k2 = alpha*k0 - alpha*I
    check_cap_jet_representatives():
        J1 = k1 ; J2 = -beta*k0 + (h-1)*k2
        T(J) := diag(J)   [ "diag(j1) == expected_j1" etc. ]
        direct scalar <J,block> := matrix_pair(J, block)

Claim under test (notes/2026-08-12-two-gate-resolution-sketch.md, b63c76c):
    J_* = (beta - 2*alpha)*J1 + (beta + alpha)*J2
    T(J_*)  = -3*alpha*beta*Delta      with Delta = (1,1,1)
    h*T(J_*) = -9*alpha*beta*Delta

Everything is exact Fraction arithmetic.  No repo writes.
"""

from __future__ import annotations

import importlib.util
import sys
from fractions import Fraction as Q
from itertools import product
from pathlib import Path

SNAP = Path(__file__).resolve().parent / "snapshot"


def load(rel, name):
    spec = importlib.util.spec_from_file_location(name, SNAP / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


DIAG = load(
    "computations/verify_diagonal_rees_saturation_cap_jet_bockstein.py",
    "probe_diag",
)

FAILURES = []


def check(cond, msg):
    if not cond:
        FAILURES.append(msg)
        print("  FAIL:", msg)
    return cond


def mat_add(*terms):
    return [[sum(s * m[i][j] for s, m in terms) for j in range(3)]
            for i in range(3)]


def build_rows(block, a, h):
    """J1, J2 exactly as the committed checker builds them."""
    alpha, tau, beta, k0, k1, k2 = DIAG.diagonal_data(block, a)
    j1 = k1
    j2 = mat_add((-beta, k0), (h - 1, k2))
    return alpha, tau, beta, j1, j2


def blocks():
    """Committed sample blocks plus a deterministic generic sweep."""
    yield from DIAG.check_cap_jet_representatives.__defaults__ or ()
    samples = [
        ([[2, 3, -1], [5, 7, 11], [13, 17, 19]], 0),   # committed sample
        ([[3, 2, 5], [7, -5, -6], [13, 17, 2]], 1),    # committed sample
        ([[2, 7, -1], [5, -5, 11], [13, 17, 3]], 2),   # committed, tau=0
        ([[4, 2, 5], [7, 9, -6], [13, 17, -9]], 0),    # committed, beta=0
    ]
    for raw, a in samples:
        yield [[Q(v) for v in row] for row in raw], a
    # deterministic generic sweep over exact rationals
    for d0, d1, d2 in product((Q(1), Q(-3), Q(5, 7), Q(11)),
                              (Q(2), Q(-1), Q(3, 4)),
                              (Q(-5), Q(7, 2))):
        blk = [[d0, Q(1), Q(-2)], [Q(3), d1, Q(5)], [Q(-7), Q(2), d2]]
        for a in range(3):
            if blk[a][a] != 0:
                yield blk, a


print("=" * 72)
print("A. REPRODUCE b63c76c:  T(J_*) = -3*alpha*beta*Delta   (h=3)")
print("=" * 72)

n_generic = 0
n_collision = 0
for block, a in blocks():
    for h in (3,):
        alpha, tau, beta, j1, j2 = build_rows(block, a, h)
        c1 = beta - 2 * alpha
        c2 = beta + alpha
        jstar = mat_add((c1, j1), (c2, j2))
        t = DIAG.diag(jstar)
        want = tuple(-3 * alpha * beta for _ in range(3))
        ok = check(t == want,
                   f"T(J_*) != -3ab*Delta at a={a}, alpha={alpha}, beta={beta}"
                   f": got {t}")
        # h*T
        ht = tuple(h * v for v in t)
        check(ht == tuple(-9 * alpha * beta for _ in range(3)),
              f"hT(J_*) != -9ab*Delta at a={a}")
        # direct scalar readout of J_*
        s = DIAG.matrix_pair(jstar, block)
        check(s == -3 * alpha * beta * tau,
              f"<J_*,block> != -3*a*b*tau at a={a}: got {s}")
        if beta:
            n_generic += 1
        else:
            n_collision += 1

print(f"  checked {n_generic} generic (beta!=0) and {n_collision} "
      f"collision (beta=0) instances at h=3")
print(f"  T(J_*) is a multiple of Delta=(1,1,1) in ALL of them: "
      f"{not FAILURES}")
print("  NOTE: <J_*,block> = -3*alpha*beta*tau  (nonzero unless tau=0);")
print("        the note does not record this ordinary-residue readout.")

print()
print("-" * 72)
print("A2. GENERAL h:  is the b63c76c pair (beta-2a, beta+a) h-specific?")
print("-" * 72)
# Solve for c1,c2 making T(c1 J1 + c2 J2) proportional to Delta.
# comp_a  = beta*(c1-c2)
# comp_ne = -alpha*(c1 + (h-1)*c2)
# equal  <=>  c1*(alpha+beta) + c2*((h-1)*alpha - beta) = 0
# so     (c1,c2) ~ (beta-(h-1)*alpha, alpha+beta)  and value = -h*alpha*beta
for h in range(3, 9):
    block = [[Q(4), Q(1), Q(-2)], [Q(3), Q(2), Q(5)], [Q(-7), Q(2), Q(7)]]
    a = 0
    alpha, tau, beta, j1, j2 = build_rows(block, a, h)
    c1 = beta - (h - 1) * alpha
    c2 = beta + alpha
    jstar = mat_add((c1, j1), (c2, j2))
    t = DIAG.diag(jstar)
    ok = t == tuple(-h * alpha * beta for _ in range(3))
    print(f"  h={h}: (c1,c2)=(beta-{h-1}a, beta+a) -> T = -{h}*a*b*Delta : "
          f"{'OK' if ok else 'FAIL ' + str(t)}")
    check(ok, f"general-h form failed at h={h}")
print("  => b63c76c's (beta-2*alpha, beta+alpha) is the h=3 case of the")
print("     general solution (beta-(h-1)*alpha, beta+alpha), value -h*a*b.")

print()
print("-" * 72)
print("A3. UNIQUENESS + MUTATION CONTROLS")
print("-" * 72)
block = [[Q(4), Q(1), Q(-2)], [Q(3), Q(2), Q(5)], [Q(-7), Q(2), Q(7)]]
a, h = 0, 3
alpha, tau, beta, j1, j2 = build_rows(block, a, h)
print(f"  alpha={alpha} beta={beta} tau={tau}")
# uniqueness: the set of (c1,c2) with T proportional to Delta is a line
sols = []
for c1 in range(-20, 21):
    for c2 in range(-20, 21):
        if (c1, c2) == (0, 0):
            continue
        t = DIAG.diag(mat_add((Q(c1), j1), (Q(c2), j2)))
        if len(set(t)) == 1:
            sols.append((c1, c2))
ratios = {(Q(c1), Q(c2)) if c2 == 0 else Q(c1, c2) for c1, c2 in sols}
print(f"  integer (c1,c2) in [-20,20]^2 with T proportional to Delta: "
       f"{len(sols)} solutions, distinct ratios c1/c2 = {ratios}")
target_ratio = Q(beta - 2 * alpha, beta + alpha) if (beta + alpha) else None
print(f"  b63c76c ratio (beta-2a)/(beta+a) = {target_ratio}")
check(ratios == {target_ratio},
      "the proportional-to-Delta line is NOT unique / does not match b63c76c")

# mutation controls
for dc1, dc2, label in ((1, 0, "c1+1"), (0, 1, "c2+1"), (-1, 0, "c1-1"),
                        (0, -2, "c2-2")):
    t = DIAG.diag(mat_add((beta - 2 * alpha + dc1, j1),
                          (beta + alpha + dc2, j2)))
    same = len(set(t)) == 1
    print(f"  mutation {label:6s}: T = {tuple(str(v) for v in t)}  "
          f"proportional-to-Delta? {same}")
    check(not same, f"mutation {label} still gave a multiple of Delta")

# mutation on the claimed value
t = DIAG.diag(mat_add((beta - 2 * alpha, j1), (beta + alpha, j2)))
check(t != tuple(-3 * alpha * beta + 1 for _ in range(3)),
      "value mutation control degenerate")
print(f"  value control: T(J_*) = {tuple(str(v) for v in t)} vs "
      f"-3ab = {-3*alpha*beta} (mutated -3ab+1 = {-3*alpha*beta+1} rejected)")

print()
print("=" * 72)
print("D. RANK SANITY")
print("=" * 72)


def rank(rows):
    work = [list(map(Q, r)) for r in rows]
    if not work:
        return 0
    pr = 0
    for col in range(len(work[0])):
        piv = next((r for r in range(pr, len(work)) if work[r][col]), None)
        if piv is None:
            continue
        work[pr], work[piv] = work[piv], work[pr]
        v = work[pr][col]
        work[pr] = [e / v for e in work[pr]]
        for r in range(len(work)):
            if r != pr and work[r][col]:
                v = work[r][col]
                work[r] = [x - v * y for x, y in zip(work[r], work[pr])]
        pr += 1
    return pr


ranks = {}
for block, a in blocks():
    alpha, tau, beta, j1, j2 = build_rows(block, a, 3)
    r = rank((DIAG.diag(j1), DIAG.diag(j2)))
    ranks.setdefault(("beta!=0" if beta else "beta==0"), set()).add(r)
print(f"  rank(T(J1),T(J2)) over sampled blocks: {ranks}")
check(ranks.get("beta!=0") == {2}, "generic diagonal target rank is not 2")
check(ranks.get("beta==0") == {1}, "collision diagonal target rank is not 1")
print("  => generic rank two, collision rank one: VERIFIED from the")
print("     committed matrix constructor (not just the hardcoded tuple).")

print()
print("=" * 72)
print("FAILURES:", len(FAILURES))
for f in FAILURES:
    print("  -", f)
print("=" * 72)
sys.exit(1 if FAILURES else 0)
