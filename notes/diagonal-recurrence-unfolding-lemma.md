# Unique matching forces feasibility in the recurrence shadow

Let `V` be finite and let `F` be a family of even subsets of `V`.  Put

\[
 E(F)=\{uv:\{u,v\}\in F\}.
\]

Assume `emptyset in F` and the two per-pivot rules used in
`proofs/diagonal-hafnian-recurrence-obstruction.md`: for every even
`S` of size at least four and every `u in S`, with

\[
 d_F(S,u)=\#\{v\in S\setminus\{u\}:uv\in E(F),\ 
                         S\setminus\{u,v\}\in F\},       \tag{1}
\]

one has

\[
 S\in F\Longrightarrow d_F(S,u)\geq1,
 \qquad
 S\notin F\Longrightarrow d_F(S,u)\ne1.                \tag{2}
\]

These are exactly the nonzero-sum and zero-not-a-singleton consequences of
the hafnian recurrence.  No weights, signs, or realizability assumptions
are made below.

## Lemma 1 (perfect-matching unfolding)

For every even `S subseteq V`:

1. if `S in F`, then the graph `(S,E(F)[S])` has a perfect matching;
2. if `(S,E(F)[S])` has a unique perfect matching, then `S in F`.

Consequently, if `S notin F` but `E(F)[S]` is matchable, then it has at
least two perfect matchings.  Equivalently, every supported perfect
matching on an infeasible set has an alternating cycle mate.

### Proof

Both assertions are proved simultaneously by induction on the even number
`|S|`.  They are immediate for the empty set.  For a two-set they both say
precisely that the pair belongs to `E(F)`.

Suppose first that `|S|>=4` and `S in F`.  Fix any `u in S`.  By the first
rule in (2), there is a vertex `v` such that `uv in E(F)` and
`S-{u,v} in F`.  By induction, `E(F)[S-{u,v}]` has a perfect matching.
Adding `uv` proves assertion 1.

Now suppose that `E(F)[S]` has a unique perfect matching `M`, and let `uv`
be the edge of `M` incident with an arbitrary fixed `u`.  The matching
`M-uv` is the unique perfect matching of `E(F)[S-{u,v}]`: any second one
would extend with `uv` to a second perfect matching of `S`.  Induction gives
`S-{u,v} in F`, so the term indexed by `v` in (1) is present.

There is no other term.  Indeed, if `uw in E(F)` and
`S-{u,w} in F` for some `w!=v`, assertion 1 at the smaller set would give a
perfect matching of `S-{u,w}`; adjoining `uw` would give a perfect matching
of `S` distinct from `M`.  Hence `d_F(S,u)=1`.  The second rule in (2)
forbids `S notin F`, proving assertion 2.  This closes the simultaneous
induction.  `QED`

## Corollary 2 (the exact cancellation-cycle alternative)

Let `F_0,F_1,F_2` satisfy (2), and suppose no proper ordered disjoint cover

\[
                         V=S_0\mathbin{\dot\cup}S_1
                              \mathbin{\dot\cup}S_2       \tag{3}
\]

has `S_r in F_r` for every `r`.  If a proper partition (3) is equipped,
for every nonempty `S_r`, with a perfect matching using edges of
`E(F_r)[S_r]`, then at least one nonempty color class `S_r` has a second
supported perfect matching.  The symmetric difference of the two contains
a nonempty even alternating cycle wholly inside that color class.

### Proof

If every `E(F_r)[S_r]` had a unique perfect matching, Lemma 1 would put
every `S_r` in `F_r` (and the empty classes are feasible by hypothesis),
contradicting the no-cover assumption.  Thus some nonempty class is
matchable but not uniquely matchable.  The standard symmetric-difference
decomposition of two perfect matchings gives the asserted alternating
cycle.  `QED`

## Computational consequence

Lemma 1 permits redundant raw-perfect-matching clauses to be compiled into
the Boolean audit without changing its model set.  In particular, on every
six-set the audit may state explicitly that feasibility has a supported
perfect matching and that infeasibility forbids a unique one.  This is an
induction consequence of (1)--(2), not a stronger hafnian axiom; it exposes
the cancellation cycles which a SAT solver would otherwise have to
rederive through several recurrence levels.

The corollary does not by itself prove the desired disjoint feasible cover:
the alternating mate can introduce further supported edges and cycles.
Its exact contribution is to replace the vague phrase "cancellation must
occur" by a forced, color-contained alternating cycle at every failed
matching cover.
