# Shared reciprocal pairs: exact four-cover overlap

Let `pq` and `pr` be two reciprocal selected witness pairs in a putative
exact ternary source on eight sites.  Their direct blocks are literal
coordinate matrices

\[
 A_{pq}=\lambda E_{ba},\qquad A_{pr}=\mu E_{dc}.             \tag{1}
\]

Put `C=B\{p,q,r}`, so `|C|=5`.  This note applies the arbitrary-direct-block
four-cover theorem of commit `6a9f784` to both pair deletions.  It gives an
exact finite normal form for the low-rank branch and a clean full-span
alternative.  Since every reciprocal graph with `r>=5` has a shared
endpoint, the theorem applies uniformly throughout that branch.

## 1. A simultaneous common site in every colour

For the deletion of `pq`, let

\[
 D_i^{pq}=\{u\in C\cup\{r\}:e_i\in W_u^{pq}\},
\]

and define `D_i^{pr}` on `C union {q}` similarly.  The full-pair theorem
gives `|D_i|>=4` in each six-site residual set.  Therefore

\[
 |D_i^{pq}\cap C|\ge3,\qquad |D_i^{pr}\cap C|\ge3,
\]

and two three-subsets of a five-set intersect.  Hence, for every target
colour `i`,

\[
 \boxed{D_i^{pq}\cap D_i^{pr}\cap C\ne\varnothing}.         \tag{2}
\]

Thus the two pair responses cannot route a colour through disjoint residual
supports.  This conclusion needs neither a rank hypothesis nor a vanishing
assumption on either direct block.

## 2. Full-span versus coordinate-plane normal form

There is an exhaustive split.

1. Some internal incident space `W_u` in one of the two pair charts has
   dimension three.  This is the **residual full-span branch**.
2. Every `W_u` in both charts has dimension at most two.  Then the sharp
   clause of `6a9f784` applies twice: every `W_u` is a coordinate plane,
   every colour is omitted at exactly two sites, and the three omission
   pairs partition the six residual sites.

In the second branch write

\[
 \alpha:C\cup\{r\}\to\{0,1,2\},\qquad
 \beta:C\cup\{q\}\to\{0,1,2\}                              \tag{3}
\]

for the omitted colours.  Each value occurs exactly twice.  At a common
site `u`, define the common internal core

\[
 V_u=\sum_{v\in C\setminus\{u\}}\operatorname{im}_u A_{uv}.
\]

The two charts differ at `u` only by adding the edge to `r` or the edge to
`q`, so

\[
 V_u\subseteq
 \operatorname{span}\{e_j:j\ne\alpha(u)\}
 \cap
 \operatorname{span}\{e_j:j\ne\beta(u)\}.                  \tag{4}
\]

If `alpha(u)!=beta(u)`, this intersection is the single coordinate line
whose colour is different from both omitted colours.  Therefore every
omission disagreement **axis-purifies the entire common K5 internal core at
that site**.  If the exceptional omitted colours `alpha(r)` and `beta(q)`
differ, the two `(1,2,2)` common-site multiplicity profiles differ, so at
least one such purified site is forced.

## 3. The finite omission census

There are 90 balanced omission maps on six labelled sites.  A pair
`(alpha,beta)` is classified up to permutation of the five common sites by
its `3x3` contingency matrix

\[
 n_{ij}=|\{u\in C:\alpha(u)=i,\ \beta(u)=j\}|,               \tag{5}
\]

together with the two exceptional omitted colours.  Exact enumeration gives

- 8,100 labelled pairs of maps;
- 99 labelled contingency states after quotienting the common-site
  permutation; and
- 16 states after simultaneous target-colour permutation and exchange of
  the two pair charts.

Their number of mismatched common sites has orbit histogram

\[
 \#\text{mismatches}:\quad
 0:1,\ 1:1,\ 2:3,\ 3:3,\ 4:5,\ 5:3.                        \tag{6}
\]

The unique zero-mismatch orbit has
`alpha(r)=beta(q)=i`, the same five coordinate planes in both charts, and
common omission multiplicities `(1,2,2)`.  This is the sole fully aligned
low-rank normal form.  Every other orbit contains at least one common-core
coordinate-line purification from (4).

## 4. Distinguished-site diagonal routing

The rank-at-most-two theorem also says the pure coefficient of the internal
six-site cubic is zero.  For colour `i`, the two endpoint-star factors must
therefore occupy exactly the two sites omitting `i`.

Let

\[
 i=\alpha(r),\qquad j=\beta(q).
\]

In the `pr` deletion chart, the pure-`j` response must cover site `q` through
one of its two endpoint stars.  Hence

\[
             A_{pq}[j,j]\ne0\quad\text{or}\quad
             A_{rq}[j,j]\ne0.                              \tag{7}
\]

Symmetrically, the `pq` chart forces

\[
             A_{pr}[i,i]\ne0\quad\text{or}\quad
             A_{qr}[i,i]\ne0.                              \tag{8}
\]


For a reciprocal coordinate block `lambda E_ba`, a diagonal entry is live
only when `a=b` equals the displayed colour.  Thus an off-diagonal reciprocal
block cannot cover the distinguished omission: the corresponding diagonal
cell on the opposite chord `qr` is forced.  The checker freezes all 144
choices of `(i,j)` and the diagonal/off-diagonal types of the two reciprocal
blocks, verifying the exact support clauses (7)--(8).

## 5. What is now finite, and what remains

For every shared-endpoint reciprocal pair, the exact coefficient problem is
reduced to:

- a residual full-span chart, where some `W_u` is all of `C^3`; or
- one of 16 coordinate-plane omission orbits, with every mismatch producing
  a literal coordinate-line common core and with the distinguished diagonal
  routing clauses (7)--(8).

This is not yet a curved rank-one overlap theorem.  A full incident span can
be assembled from several rank-one blocks without making any single block
rank three, and a purified common core need not purify the two exceptional
edges.  The next bounded attack is now precise: close the full-span branch by
the existing full-nine curvature machinery, and propagate (4), (7), and (8)
around the 16 finite low-rank orbits.  The zero-mismatch orbit is the only
case where no common-core line is obtained for free.

## Reproduction

```sh
python3 computations/verify_shared_reciprocal_fourcover_overlap.py
python3 -O computations/verify_shared_reciprocal_fourcover_overlap.py
```

The checker records `6a9f784`, pins the reciprocal-graph classification, audits
all six-site four-covers, enumerates the complete omission quotient, and
freezes the diagonal-routing truth table.
