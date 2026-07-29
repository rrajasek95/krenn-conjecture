# A characteristic-free diagonal obstruction through ten vertices

Let `V` have even cardinality `n`, and let `A_0,A_1,A_2` be symmetric
zero-diagonal scalar edge matrices over a field.  For every even
`S subseteq V`, put

\[
 h_r(S)=\operatorname{haf}A_r[S],\qquad h_r(\varnothing)=1. \tag{1}
\]

If diagonal aggregate edge matrices realized the three-color
monochromatic tensor, then, after harmless nonzero normalizations,

\[
 h_r(V)\ne0\quad(r=0,1,2),\qquad
 h_0(S_0)h_1(S_1)h_2(S_2)=0                         \tag{2}
\]

for every proper ordered partition
`V=S_0 disjoint-union S_1 disjoint-union S_2` into even sets.  No
positivity or absence of cancellation is assumed in (2).

This note proves the following finite theorem.

**Theorem.**  Conditions (2) have no solution for

\[
                         n\in\{6,8,10\}.                    \tag{3}
\]

In particular, arbitrary complex cancellation does not produce a diagonal
three-color realization at any of these orders.

## 1. The recurrence shadow

Write

\[
                         z_r(S)=[h_r(S)\ne0].                \tag{4}
\]

For an even set `S`, a pivot `u in S`, and `v in S\setminus{u}`, define

\[
 t_r(S;u,v)=
 [,a^r_{uv}\,h_r(S\setminus\{u,v\})\ne0,].                \tag{5}
\]

Because the coefficients lie in a field,

\[
 t_r(S;u,v)=z_r(\{u,v\})\wedge
             z_r(S\setminus\{u,v\}).                       \tag{6}
\]

The hafnian expansion at the *chosen* pivot is

\[
 h_r(S)=\sum_{v\in S\setminus\{u\}}
           a^r_{uv}h_r(S\setminus\{u,v\}).                 \tag{7}
\]

Two support consequences are exact over every characteristic:

1. if `z_r(S)=1`, at least one term (5) is nonzero;
2. if `z_r(S)=0`, the terms (5) cannot contain exactly one nonzero term.

The second statement retains arbitrary cancellation: two or more nonzero
terms are allowed to sum to zero.  Applying both statements separately at
every pivot is strictly stronger than pooling all unordered pairs in `S`.
That missing per-pivot condition is why an earlier support relaxation had
spurious eight-vertex survivors.

Equations (4)--(7), the units `z_r(empty)=z_r(V)=1`, and the clauses

\[
 \neg z_0(S_0)\vee\neg z_1(S_1)\vee\neg z_2(S_2)           \tag{8}
\]

for all proper even ordered partitions form a purely Boolean necessary
condition for (2).  Notice that no direct perfect-matching-support clauses,
cut factorization, sign variables, or binomial ratio relations are needed.

## 2. Exhaustive symmetry reduction

The recurrence shadow itself proves that each color contains a supported
perfect matching.  Starting from `z_r(V)=1`, choose a nonzero term in (7),
delete its endpoints, and recurse until the empty set.  All selected
two-sets have `z_r({u,v})=1`.

Relabel vertices so a selected color-zero matching is

\[
                         01|23|45|\cdots .                   \tag{9}
\]

Under the stabilizer of (9), a selected color-one matching is classified
by the alternating-cycle sizes in its union with (9).  These sizes form an
integer partition of `n/2`, and every such partition has one explicit
representative in the checker.  Thus there are respectively `3,5,7`
first-level branches at orders `6,8,10`.

The coincident branch has cycle type `(1,1,...,1)`.  There the full
stabilizer of (9) remains, so a supported color-two matching is classified
by the same integer partitions.  Splitting only that branch gives
respectively `5,9,13` exhaustive SAT calls.  Fixing these edges assumes
only support, not uniqueness or a nonzero uncancelled full monomial sum.

## 3. Exact audit

The checker is

[`computations/verify_diagonal_recurrence_obstruction.py`](../computations/verify_diagonal_recurrence_obstruction.py).
It constructs Tseitin equivalences for (6), encodes the two implications
following (7), adds every clause (8), and solves every symmetry branch with
CaDiCaL through PySAT.  Every branch is `UNSAT`.

Run all three audited orders with

```text
.venv/bin/python computations/verify_diagonal_recurrence_obstruction.py
```

The `n=6` instance has `411` variables and `2,904` base clauses; the
`n=8` instance has `2,988` variables and `23,844` base clauses; the `n=10`
instance has `18,681` variables and `159,336` base clauses.  The script
prints and asserts these counts and all branch outcomes.  The construction
uses Boolean gates in both directions, and `UNSAT` is used only in the sound
direction: the formula is a relaxation of arbitrary field-valued hafnian
data.

This is not yet a uniform all-even proof.  A realization at larger order
does not automatically restrict to a common feasible eight- or ten-vertex
principal set in all three colors.  What (3) supplies is a much stronger
finite base and a compact characteristic-free recurrence statement for a
prospective induction.
