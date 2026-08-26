# Bounded finite-field screen of the four canonical triangle branches

## Verdict

No branch is closed by this screen, and no candidate X5 point is found.  The
bounded calculation does, however, isolate the actual algebraic residual:

```text
on any 9x9 response-minor open, each of the four blocker memberships is
solvable in the 108 witness variables and imposes no source constraint.
```

Thus the four `361`-variable branches are all just normalized `X5` plus the
live chart on the full-response-rank open.  Blocker-specific information can
only occur on `rank(L_triangle)<=8`.  A solve that does not split this
determinantal boundary is spending almost all of its effort on X5 itself.

Three deterministic normalized finite-field samples per branch give an
identical 252-row tangent-selected nonlinear core.  Exact F4 probes reach
degree 6 and time out without a unit or a witness.

## 1. Literal systems and normalization

The source is the frozen canonical flag

```text
cap pair = 67,    triangle = 012,    A_06[0,1] != 0,
```

with the four blocker right sides

```text
K_00, K_11, K_22, <K,A_67>.
```

Every full branch has

```text
252 source variables
+108 row-span witness variables
+  1 inverse variable
=361 variables,

6558 mixed X5 equations
+  3 pure normalizations
+  9 membership coordinates
+  1 inverse equation
=6571 equations.
```

The screen works over `F_32003`.  For each of the three seeds and each
branch it:

1. assigns deterministic dense source values and sets `A_06[0,1]=1`;
2. solves `H_c=1` exactly and linearly through `A_01[c,c]`;
3. forms the literal `108 x 9` outside-response matrix;
4. solves its nine membership coordinates for the 108 witnesses;
5. verifies all thirteen pure/live/membership equations exactly;
6. inserts literal mixed rows by increasing off-count into
   `J delta = -F`.

All twelve samples have response rank nine.  In fact, the first nine rows,
the nine colour coordinates of response edge `03`, already form a nonzero
minor:

```text
seed 2026082301: Delta_03 = 28548 mod 32003,
seed 2026082302: Delta_03 = 24041 mod 32003,
seed 2026082303: Delta_03 = 23621 mod 32003.
```

This is not merely a numerical observation about witnesses.  Abstractly, on
`Delta_03 != 0`, those nine response rows span the whole 9-dimensional
`K`-coordinate space.  Every one of `K_00,K_11,K_22,<K,A_67>` therefore has
a unique solution using those nine witness slots alone.  Eliminating all 108
witness variables on this open leaves exactly normalized X5 plus the live
cell equation.

## 2. Tangent-selected source core

At every normalized sample, all 239 mixed equations seen before the terminal
row have nonzero residual.  Their profile census is

```text
48 profile 71,
94 profile 62,
97 profile 611.
```

Together with the thirteen base rows, 238 of those mixed rows increase the
coefficient rank to `251`.  The next literal row

```text
F_11211011 = 0                         (profile 611)
```

reduces to `0 = nonzero` in the affine Newton system.  The result is identical
for all three seeds and all four branches:

```text
13 base rows + 239 mixed rows = 252 nonlinear source-labelled equations,
Jacobian coefficient rank before the terminal row = 251.
```

This is a genuine finite-field tangent contradiction at each specialized
base point, not a support test.  It says that none of the twelve points can
be corrected infinitesimally into X5.  It does **not** show that the nonlinear
252-row ideal, or any full branch, is empty.

The complete selected-label ledger and all twelve value/witness hashes are in
[`results_canonical_triangle_ff_screen.json`](results_canonical_triangle_ff_screen.json).

## 3. Bounded nonlinear F4 probes

The common 252-row nonlinear core was exported separately for all four branch
right sides.  Input hashes are recorded in
[`results_core252_msolve_probe.json`](results_core252_msolve_probe.json).

The three diagonal-blocker branches, using 500 pairs per matrix, all complete
the same degree-5 frontier:

```text
degree 4: 18 new generators;
degree 5: 485 new + 15 zero reductions;
degree 5: 500 new + 0 zero reductions;
degree 5: 112 new + 0 zero reductions;
degree 6: 67,570 pairs pending at timeout.
```

The direct blocker, using 1,000 pairs per matrix, has the same total degree-5
growth (`985+112=1097` new, 15 zero reductions) and reaches the same 67,570
degree-6 pair frontier.  The gates were capped at 15 seconds for the three
diagonal branches and 30 seconds for the direct branch.  None returns
`[-1]`, a parametrization, or a positive-dimensional sentinel.  Timeout is
neither SAT nor UNSAT.

## 4. Smallest justified residual

The branch geometry now has a mandatory split:

```text
Delta_03 != 0 (and its 12-edge transports):
    membership eliminates completely;
    residual = normalized full X5 + A_06[0,1] != 0.

all response 9x9 minors = 0:
    rank(L_triangle) <= 8;
    blocker-specific incidence remains and must be studied here.
```

The first line cannot be advertised as a triangle-blocked reduction: it has
forgotten which blocker was selected.  A useful next exact gate must either

1. prove that X5 forces `rank(L_triangle)<=8` on the live canonical chart,
   or
2. work directly on rank strata and retain the appropriate blocker in the
   cokernel.

Running the unsplit 361-variable systems or enlarging the 252-row F4 cores is
not justified by these data; both routes immediately reproduce the global
X5 degree-6 explosion.

## 5. Reproduction and guards

```bash
python3 screen_canonical_triangle_branches.py --check-results
python3 -O screen_canonical_triangle_branches.py --check-results
python3 -I -S screen_canonical_triangle_branches.py --check-results

python3 export_tangent_core_msolve.py triangle_endpoint_colour
python3 export_tangent_core_msolve.py cap_endpoint_colour
python3 export_tangent_core_msolve.py third_colour
python3 export_tangent_core_msolve.py direct
```

The standard, optimized, and isolated tangent replays pass.  Frozen logical
digest:

```text
16b55f4de26583520f74a85207fd5d39ce3cb75cfb0c9fef7f30c5b1d50ac811
```

Scope guard: the normalized samples satisfy the thirteen base equations but
not X5.  Their tangent contradictions are local screens at nonsolutions, not
global branch certificates.  The response-minor elimination statement is
the rigorous source-level conclusion.
