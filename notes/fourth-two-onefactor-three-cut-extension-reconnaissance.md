# Two-extra diagonal one-factor reconnaissance for a third complete cut

## Status

This note records **finite exact reconnaissance only**.  It is not a theorem
about arbitrary aggregate edge tensors, arbitrary diagonal factors, or even
arbitrary rational weights in the family below.

No three-cut example was found in the stated finite scope.  The maximum was
two active complete cuts.

## Family and exact test

Start from the sharp order-eight two-cut source

\[
\begin{aligned}
M_0&=01,23,45,67,\\
M_1&=02,14,36,57,\\
M_2&=04,13,27,56,
\end{aligned}
\]

where every edge of \(M_c\) carries the diagonal cell of colour \(c\) with
weight one.  Append two decorated one-factors.  Each appended factor is a
choice

\[
 (M,c,w),\qquad
 M\in\operatorname{PM}(K_8),\quad
 c\in\{0,1,2\},\quad
 w\in\{-3,-2,-1,1,2,3\}.
\]

There are \(105\cdot3\cdot6=1890\) choices.  The scan enumerates every
unordered pair with repetition, hence exactly

\[
 \binom{1890+1}{2}=1{,}786{,}995
\]

factor-pair records.  Different records can yield the same aggregate edge
family, so this is a record count, not a claim of that many distinct tensors.
When factors overlap, all contributions on the shared edge are retained and
added by the weighted matching expansion.

For each record and each \(z\in\{0,1,2,3,4,5\}\), the program constructs the
complete cofactor-insertion space and every high-sector residual row.  It
uses Gaussian elimination over \(\mathbb Q\), with Python `Fraction`
coefficients, to test both

1. whether every residual row belongs to the insertion space, and
2. whether the monochromatic target has nonzero defect modulo that space.

A cut is counted only when both conditions hold.  Thus neither the
completeness test nor the target-defect test is modular or floating point.

## Replay

Run

```text
.venv/bin/python computations/search_fourth_two_onefactor_three_cut_extensions.py \
  --mode full --weights=-3,-2,-1,1,2,3 --workers 4
```

The exact replay reports

```text
mode=full weights=(-3, -2, -1, 1, 2, 3) pool=1890 \
nominal_pairs=1786995 scanned=1786995 \
max_active_complete_cuts=2 stopped=False
maximizing_records_seen=1075
```

One maximizing record is obtained by adding two further copies of
\((M_0,0,-3)\).  Its six cut records are

```text
((False, 2), (False, 2), (True, 1),
 (True, 1), (False, 3), (False, 1))
```

so the active complete cuts are still \(z=2,3\).

## Exact conclusion and limitation

Within this finite family, two additional constant-colour one-factors with
weights in \(\{-3,-2,-1,1,2,3\}\) never produce three simultaneous active
complete cuts.  This strengthens the failed falsification search around the
known two-cut model, but it does not prove that three cuts are impossible.
In particular, it leaves open nonconstant edge cells, nondiagonal cells,
other rational weights, more added factors, and aggregate edge families not
reachable from the fixed base source.
