# An all-exceptional fixed-star rainbow countermodel

## Outcome

Constant fibers, every two-color restriction, overlap of the internal
quadratics `q_p`, and two of the three full common-power row equations at
every fixed star do not force one generic star.  A rational six-site model
passes all of those tests and fails in exactly one genuinely ternary
matching.

Every fixed star is exceptional for the three-hole gauge dichotomy: all
aggregate matrices have rank one, so every deleted rank-three graph is
empty.  The example is also cell-minimal for the retained constant and
binary-face constraints.  Thus an argument on the exceptional locus must
use the third row equation at some star, or an equivalent genuinely
three-color mixed coefficient.  Pairwise binary faces and overlap
consistency cannot supply it.

This is not a Krenn counterexample: the displayed ternary coefficient is
nonzero.  It is an exact structural countermodel locating the first missing
equation.

## 1. Three pairwise-Hamilton one-factors

On vertices `0,...,5`, take

\[
\begin{aligned}
 P_0&=01\mid23\mid45,\\
 P_1&=12\mid34\mid05,\\
 P_2&=03\mid15\mid24.                                    \tag{1}
\end{aligned}
\]

Put the unit cell `e_r tensor e_r` on every edge of `P_r` and no other
cells.  The three one-factors are edge-disjoint.  Each pairwise union
`P_r union P_s` is a Hamilton six-cycle.  A cycle has only its two
alternating perfect matchings, so restriction to any two colors gives
exactly

\[
                         e_r^{\otimes6}+e_s^{\otimes6}.    \tag{2}
\]

Thus all three binary faces are exact, not merely their constant
coefficients.

The union of all three factors has exactly four perfect matchings.  Besides
the three in (1), the fourth is

\[
                         M_*=03\mid12\mid45.              \tag{3}
\]

Its successive edge colors are `2,1,0`, so its vertex-coloring is

\[
                             211200.                      \tag{4}
\]

Consequently the complete tensor is exactly

\[
 \boxed{\quad H_6(A)=\Delta_{6,3}+e_2e_1e_1e_2e_0e_0.\quad} \tag{5}
\]

There are no other contaminating coefficients and no cancellations hidden
in (5).

## 2. What every fixed star sees

Fix a vertex `p`, put `J=B\setminus{p}`, and let `q_p` be the actual
quadratic formed by the common internal edges.  The color-`r` star row is
a single cell: the edge of `P_r` incident with `p`.  Hence its common-power
output is computed from the actual cofactor of that one edge,

\[
                         F_{q_p}(z_{p,r})
                    =z_{p,r}{q_p^2\over2}.                \tag{6}
\]

If `r!=211200[p]`, the rainbow matching (3) does not use row `r` at `p`,
and direct matching expansion gives the full tensor equation

\[
                         F_{q_p}(z_{p,r})=e_r^{\otimes J}. \tag{7}
\]

For the remaining color `r=211200[p]`, exactly one extra basis tensor
survives:

\[
 F_{q_p}(z_{p,r})
   =e_r^{\otimes J}
      +e_{211200|_J}.                                    \tag{8}
\]

Thus every fixed star satisfies two of its three complete row equations,
including all their mixed zero coefficients.  The failed row and failed
word are coherent on overlaps: they are precisely the restrictions of the
single global rainbow word (4).  For example, at `p=0`,

\[
 F_{q_0}(z_{0,0})=e_0^{\otimes5},\qquad
 F_{q_0}(z_{0,1})=e_1^{\otimes5},\qquad
 F_{q_0}(z_{0,2})=e_2^{\otimes5}+e_{11200}.               \tag{9}
\]

This shows exactly why using overlapping stars without all three rows does
not accumulate into a contradiction: the same global error simply moves
to the locally selected row.

## 3. Every star is exceptional

Every nonzero aggregate edge matrix in the construction has one cell and
rank one.  For every `p`, the rank-three graph of `q_p` is empty, as is
every further vertex deletion of that graph.  Therefore every star lies on
the disconnected/nonspanning side of Corollary 4.4 in
`notes/fixed-star-three-hole-gauge-dichotomy.md`.

The nine cells are all indispensable for the retained constraints.  The
all-`r` coefficient has the unique compatible matching `P_r`, so deleting
any color-`r` cell destroys that coefficient.  The countermodel is
therefore entry-minimal among sources satisfying the three constant fibers
(and hence among those satisfying the exact binary faces (2)).

The first missing equation is not another rank, support, or overlap test.
It is the genuinely ternary coefficient

\[
                         [211200]H_6(A)=1                 \tag{10}
\]

or, equivalently, any one of its six fixed-star incarnations (8).

## 4. Exact audit

Run

```text
uv run python computations/verify_all_exceptional_star_rainbow_countermodel.py
```

The checker enumerates all fifteen perfect matchings, verifies the three
Hamilton unions, proves that (1) and (3) are the complete supported-matching
list, checks all `3^6` coefficients in (5), checks every binary face, and
independently recomputes all twelve valid and six failed common-power row
equations from the actual internal quadratics `q_p`.  It also verifies the
empty rank-three graphs and indispensability of every cell.
