# N=8 rank-one witnesses: reciprocal edge or four exceptions

> **Strengthened.**  The four-exception branch is no longer the sharp
> conclusion.  Combining it with the essential-star equality case forces at
> least seven active rank-one doubly injective pairs; see
> [the essential-count sharpening](n8-rankone-good-pair-essential-count.md).
> The graph-only counterguard below remains valid for the earlier density and
> `K4,4` claims, but not for the stronger essential-star hypotheses.

## Exact dichotomy

For every site \(v\) and target color \(a\), the forced incident-edge
theorem gives an active neighbor \(f_a(v)\), distinct as \(a\) varies, with

\[
             A_{v f_a(v)}=c_{v,a}\otimes e_a^{(f_a(v))},
 \qquad H_{B\setminus\{v,f_a(v)\}}(A)\ne0.                \tag{1}
\]

There are therefore 24 directed color witnesses at \(N=8\).  Exactly one
of the following holds.

1. **Reciprocal branch.**  Some physical pair \(uv\) is selected in both
   directions.  If \(v\to u\) has head color \(a\) and \(u\to v\) has head
   color \(b\), endpoint order forces
   \[
                         A_{vu}=\lambda e_b^{(v)}
                                      \otimes e_a^{(u)},\quad\lambda\ne0.
                                                               \tag{2}
   \]
   Thus the aggregate block is a single coordinate cell, though \(a\) and
   \(b\) need not agree.
2. **No-reciprocal branch.**  Forgetting orientation maps the 24 witnesses
   injectively to physical pairs.  Hence at least 24 of the 28 aggregate
   blocks are active rank one, and at most four blocks are exceptional
   (zero or rank at least two).

More generally, if \(r\) physical pairs are reciprocal, the 24 arcs occupy
\(24-r\) underlying pairs.  The displayed dichotomy uses only whether
\(r=0\) or \(r>0\).

The statement retains aggregate endpoint order and activity.  It does not
select an individual member of a parallel source family whose aggregate
sum is the block in (1).

## Why existing four-exception classifications do not close it

No committed theorem currently eliminates the no-reciprocal branch.

* `six-vertex-rank-graph.md`, `toric-binomial-rank.md`, and the generalized
  Laurent low-exception audits classify rank graphs for an exact identity
  \(H_6(A)=\Delta_{6,3}\).  Deleting two sites from the present eight-site
  source leaves an arbitrary six-site matching cofactor, not \(\Delta_6\),
  so those hypotheses are unavailable.
* `search_k44_forced_anchor_support.py` is a useful exact support theorem on
  a fixed \(K_{4,4}\): every crossing block is nonzero, the crossing
  higher-rank blocks form a matching, and all six directed color-star
  conditions remain inside that one bipartition.  Four exceptional blocks in
  \(K_8\) do not force any such partition, nor do the 24 selected anchors.
* A coordinate-coordinate reciprocal block is stronger than an ordinary
  one-sided witness, but it still does not make its cap clean.  The exact
  `pair-covector-selection-obstruction.md` shows that even a tensor-active
  coordinate anchor can retain a nonzero higher cumulant for every
  nondegenerate covector.

Thus (2) is a promising normal-form input, not a descent theorem, and the
four-exception branch still needs the full eight-site mixed fibres.

## Sharp graph-only counterguard

On vertices \(\mathbb Z/8\), direct the three color witnesses from \(v\) to

\[
                         v+1,\quad v+2,\quad v+3\pmod8,    \tag{3}
\]

with colors \(0,1,2\), respectively.  No pair is reciprocal.  The underlying
witness graph is

\[
             K_8\setminus\{04,15,26,37\},                \tag{4}
\]

so it attains exactly 24 active rank-one pairs and four exceptions.  Give
each directed edge an arbitrary tail line \(c_{v,a}\) and the prescribed
axis \(e_a\) at its head.  This realizes every conclusion used in the
dichotomy.

No balanced bipartition sends all 24 arcs across the cut: the witness graph
contains triangles, and the checker directly audits all 35 bipartitions
modulo complement.  Hence the committed \(K_{4,4}\) support theorem cannot
be invoked from the dense count alone.

This model is an exact incidence/rank counterguard, not an exact matching
source and not a Krenn counterexample.  It proves that any closure of the
four-exception branch must use coefficient or cofactor provenance beyond the
forced rank-one witnesses.

## Next finite problem

The bounded continuation is to classify the at-most-four exceptional graph
together with the 24 source-labelled head axes, then impose complete N=8
mixed fibres (or an integral Laurent/Koszul certificate) on each stabilizer
orbit.  The reciprocal branch should be kept separate because its literal
coordinate cell gives a stronger pair-cap normal form.

## Reproduction

```sh
python3 computations/verify_n8_rankone_reciprocal_four_exception_dichotomy.py
python3 -O computations/verify_n8_rankone_reciprocal_four_exception_dichotomy.py
```
