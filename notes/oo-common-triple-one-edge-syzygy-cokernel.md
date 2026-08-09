# The literal common-triple one-edge module has no curvature--anchor class

## 1. Outcome

Normalize a rank-one/rank-one outgoing overlap to have head `0` on `pq`
and head `1` on `pr`.  The common eligible ruling label is `2`.  Take the
literal common-triple coefficient first, retaining both source-labelled
presentations of all six off-diagonal and three diagonal full-nine rows in
each chart.  Then allow one physical edge through a fixed remaining site as
the coefficient/Koszul multiplier.

The resulting universal module has no class whose physical readout is

\[
 \bigl(A_{pq}(a,0)A_{rs}(1,\ell)
       -A_{pr}(a,1)A_{qs}(0,\ell)\bigr)X_2.              \tag{1}
\]

This holds for every common tail colour (a) and fourth-site colour
\(\ell\).  More precisely, the literal residual-site block has seven
columns and rank seven.  Two source-labelled chart copies have rank seven
and a seven-dimensional kernel consisting only of the componentwise chart
comparisons.  The source realization of (1) raises the rank from seven to
eight.

There is a strong counterguard.  Even if the fixed-site restriction is
dropped and all 28 physical edges are admitted, the column rank is 21, its
kernel is the seven-dimensional vertex-potential space, and adjoining (1)
raises the rank to 22.  An explicit six-matching integral cokernel covector
detects (1).

Thus the proposed one-edge linear/Koszul step is exhausted and fails.  A
successful OO comparison needs a second coefficient/Hasse cell, at least a
two-edge multiplier, or a genuinely localized nonlinear relation.  This is
a no-go for that bounded candidate module, not a proof of the OO
full-nine coupling lemma or of Krenn's conjecture.

## 2. The normalized literal cut

Use physical sites

\[
             p=0,\quad q=1,\quad r=2,\quad s=3,
             \qquad D=\{4,5,6,7\}.                       \tag{2}
\]

For (a,\ell\in\{0,1,2\}), the curvature word is

\[
                     w=(a,0,1,\ell,2,2,2,2).             \tag{3}
\]

It is mixed because the `q` and `r` colours are distinct.  The `pq`
full-nine presentation of this coefficient lies in row `(a,0)`, while the
`pr` presentation lies in row `(a,1)`.  Exhausting the 18 row labels gives

\[
\begin{array}{c|cc}
a&pq&pr\\ \hline
0&00\text{ diagonal}&01\text{ off-diagonal}\\
1&10\text{ off-diagonal}&11\text{ diagonal}\\
2&20\text{ off-diagonal}&21\text{ off-diagonal}.
\end{array}                                                \tag{4}
\]

The other 16 rows are of a different fine multidegree.  Even when one of
the two labels in (4) is diagonal, its coefficient at (3) has zero target:
the global word is still mixed.  In particular, the missing `22` anchor is
not already present in the common-triple coefficient.

This is the first degree gate.  It is not obtained by replacing the nine
rows with abstract matrix units; it follows by filtering the two literal
full-nine tensors by their physical endpoint colours.

## 3. Matching-by-matching coefficient module

Let (H_w) be the universal eight-site hafnian coefficient at the fixed
word (3).  Its 105 terms are distinct labelled physical perfect matchings.
For a physical edge (e), put

\[
                         C_e=e\,\partial_eH_w.             \tag{5}
\]

The derivative is the literal first physical-edge coefficient, and the
factor (e) is its one-edge reinsertion.  Fine multidegree preservation
forces the reinserted edge to be the same (e): the derivative removes the
two fixed site-colour slots at the endpoints of (e), and no other physical
edge restores those two slots.

After the common-triple cut, take the first coefficient at `s`.  Then

\[
 e\in\{sp,sq,sr,s4,s5,s6,s7\},                            \tag{6}
\]

so (5) gives exactly seven candidate columns.  Every column is the
indicator sum of the 15 perfect matchings containing its labelled edge.

Both chart presentations are reconstructed independently.  In each global
word, the `pq` presentation partitions the 105 matchings into 15 direct and
90 two-star terms, and the `pr` presentation does the same.  Their unions
are the same literal matching polynomial.  Consequently

\[
                         C_e^{pq}=C_e^{pr}.                \tag{7}
\]

Equation (7), checked term by term before any sector identification, is the
common-triple power-free comparison at this coefficient.  Taking (5) for
the seven edges in (6) is its normal companion.  The direct and two-star
pieces are not promoted to independent generators.

The source realization of the desired readout is

\[
 T_{a\ell}=
 \bigl(A_{pq}(a,0)A_{rs}(1,\ell)
       -A_{pr}(a,1)A_{qs}(0,\ell)\bigr)
       \operatorname {Haf}(D;2,2,2,2).                    \tag{8}
\]

It has six matching terms.  Its positive three terms are exactly the
`pq`-direct projection of (C_{rs}); its negative three terms are the
`pr`-direct projection of (C_{qs}).  This is the literal direct-double
curvature part of the normal packet.  Using either projection by itself
would split a physical row and is therefore not allowed.

If a source-provenant one-edge class produced the formal expression (1),
substitution of the missing diagonal row would send it to (8).  Hence it is
enough, and slightly stronger, to test (8) in the literal source matching
module.

## 4. Exact rank, kernel, and cokernel

Use the 105 labelled matchings as feature rows.  For all nine choices of
\((a,\ell)\), exact rational elimination gives

\[
\begin{array}{c|c|c|c|c}
\text{block}&\text{columns}&\text{rank}&\text{kernel}&
        \text{cokernel}\\ \hline
s\text{-edge, one chart}&7&7&0&98\\
s\text{-edge, two labelled charts}&14&7&7&98\\
\text{all physical edges, one chart}&28&21&7&84\\
\text{all physical edges, two charts}&56&21&35&84.
\end{array}                                                \tag{9}
\]

Adjoining (T_{a\ell}) raises the first and third ranks to eight and 22,
respectively.  Thus (T_{a\ell}) is not in either image.

The seven kernel vectors of the doubled (s)-edge block are exactly

\[
                         C_e^{pq}-C_e^{pr}.                \tag{10}
\]

There is no one-chart syzygy at all.  For the all-edge block, every
zero-sum vertex potential (\alpha=(\alpha_0,\ldots,\alpha_7)) gives

\[
 \sum_{u<v}(\alpha_u+\alpha_v)C_{uv}=0,
 \qquad \sum_u\alpha_u=0.                                \tag{11}
\]

The seven potentials (e_i-e_7), (0\le i<7), are independent.  Since
the all-edge kernel has dimension seven, (11) is the complete kernel.
These are Euler incidence relations, not a curvature--anchor syzygy.

There are also small integral cokernel certificates.  For the sharp
`s`-edge block, let

\[
\begin{aligned}
 M_+&=pq\mid rs\mid45\mid67,\\
 M_0&=p4\mid q5\mid rs\mid67.
\end{aligned}                                             \tag{12}
\]

The covector (\delta_{M_+}-\delta_{M_0}) kills every column in (6): the
two matchings lie in the same `rs` column, and neither lies in another
`s`-edge column.  Its value on (T_{a\ell}) is one.

Even all 28 edge columns are killed by the six-term covector

\[
\begin{aligned}
 \Lambda={}&-\delta_{pr\mid qs\mid45\mid67}
 +\delta_{pr\mid q4\mid s5\mid67}
 +\delta_{ps\mid qr\mid45\mid67}\\
 &-\delta_{ps\mid q4\mid r5\mid67}
 -\delta_{p4\mid qr\mid s5\mid67}
 +\delta_{p4\mid qs\mid r5\mid67}.                       \tag{13}
\end{aligned}
\]

Every physical edge has total coefficient zero in (13), so
\(\Lambda(C_e)=0\) for all 28 edges.  The first term is the negative
curvature-anchor matching and the other five are outside (8), giving

\[
                         \Lambda(T_{a\ell})=1.             \tag{14}
\]

Equations (12)--(14) are characteristic-zero upper certificates, not only
modular rank evidence.

## 5. Consequence and scope

The common-triple-first ordering matters.  The calculation retains the two
literal source partitions until (7) is checked, then takes the `s`
coefficient.  It does not start from an isolated fixed-site tensor, which
would forget whether a term came from the `pq` direct sector or the `pr`
two-star sector.

Within that source-faithful order, (9)--(14) exhaust every
multidegree-preserving linear correction with one physical-edge
reinsertion, as well as every ordinary Koszul relation among those columns.
The diagonal full-nine labels were included in the 18-row filter; their
failure is the target-grade statement in (4), not an omission from the
matrix.

The result does **not** exclude:

* a two-edge multiplier or a second principal-parts coefficient;
* a denominator-marked/Rees or Hasse--Schmidt comparison cell;
* a nonlinear relation after localizing active cofactors, good-star minors,
  and curvature; or
* a higher operation whose Leibniz corrections supply new source rows.

Those are now necessary rather than optional for this route.  Repeating
the one-edge search with a larger abstract row space would only split the
literal source sectors and invalidate the provenance gate.

## 6. Reproduction

Run

```text
python3 computations/verify_oo_common_triple_one_edge_syzygy_cokernel.py
python3 -O computations/verify_oo_common_triple_one_edge_syzygy_cokernel.py
```

The dependency-free checker expands all 105 matchings, both 15/90 chart
partitions, all 18 row labels, all nine normalized \((a,\ell)\) types, the
seven-edge and 28-edge blocks, the complete kernel descriptions, and the
two integral cokernel covectors.  Its frozen ledger digest is

```text
c66fed782204351ab33d3a36ed2bff8b263043dd0fa0a8358ef61f92e84c751f
```
