# Cancellation mates are invisible to every first-slice collision jet

## Outcome

The first-slice cubic obstruction for three one-factors stops exactly at
singleton uniqueness.  If a selected extra matching has an opposite-weight
mate with the same vertex colouring, then no functorial local collision
calculation can distinguish the two terms: their sum remains zero after
arbitrary site-dependent polynomial basis changes, arbitrary first-slice
contractions, and arbitrary differentiation.  In particular every cubic
Bianchi equation—and in fact every higher one—vanishes on the packet.

There is a minimal simple physical countermodule at eight sites.  Three
edge-disjoint rank-one coordinate factors form the cube; their three local
vectors are a basis at every vertex, so they give a nonzero term of the
three-copy alternating invariant.  Every pairwise factor union has two
alternating four-cycles.  One binary switch matching has an external
rank-one mate of opposite weight, and its complete colouring fibre consists
of exactly those two terms.  The two terms use different incident edges at
every vertex and their symmetric difference is one alternating eight-cycle.

Thus first-slice/collision equations cannot kill an arbitrary locally
independent rank-one rainbow triple once cancellation mates are allowed.
They kill the pairwise-Hamilton singleton chart from
`first-slice-cubic-three-factor-obstruction.md`, but a continuation must
couple different colouring fibres through their shared source edges.  Merely
taking more derivatives of one cancelled fibre cannot do this.

This is a countermodule to a localization implication, not a Krenn
counterexample: other mixed fibres of the displayed source are nonzero.

## 1. Functorial mate invisibility

Let `F_c` be one decorated matching fibre of a source.  Each matching
`M in F_c` contributes

\[
                       z(M)e_c,
 \qquad e_c=\bigotimes_{v\in B}e_{c_v}.                  \tag{1}
\]

Suppose a nonempty packet `S subseteq F_c` has

\[
                             \sum_{M\in S}z(M)=0.         \tag{2}
\]

Let `g_v(t)` be arbitrary local linear maps with polynomial or formal-power-
series coefficients.  For any set of sites `D`, also choose arbitrary
polynomial covectors `lambda_v(t)` at the sites in `D`.  Apply the local maps
to (1), contract the sites in `D`, and retain the other tensor slots.  The
whole packet becomes

\[
 \left(\sum_{M\in S}z(M)\right)
 \left(\prod_{v\in D}\lambda_v(t)(g_v(t)e_{c_v})\right)
 \bigotimes_{v\notin D}g_v(t)e_{c_v}=0.                  \tag{3}
\]

This proves the following exact no-go statement.

**Lemma 1.1 (same-fibre jet invisibility).**  A zero-sum packet of
same-colouring matching terms remains zero under every local collision,
every iterated first-slice contraction, and every coefficient or derivative
of the resulting formal family.  Division by any common local torus factor
does not change the conclusion wherever the normalized slice is defined.

Every Maurer--Cartan/Bianchi equation obtained by comparing mixed
derivatives of such a family is included in Lemma 1.1.  The statement is
stronger than diagonal-torus homogeneity: the `g_v(t)` may mix all three
colours independently at every site.

There is an important boundary to the lemma.  If the first-star expansion
is kept **before** summing its neighbor components, two mates using different
incident edges remain separate nonzero terms.  Equation (3) only says their
sum is zero.  No target-derived Bianchi identity makes either component
zero; a further source relation must connect that component to another
colouring fibre.

## 2. The eight-site cube packet

Use sites `0,...,7` and the three perfect matchings

\[
\begin{aligned}
P_0&=01|23|45|67,\\
P_1&=03|12|47|56,\\
P_2&=04|15|26|37.                                      \tag{4}
\end{aligned}
\]

Put the unit cell `e_r tensor e_r` on every edge of `P_r`.  These twelve
underlying edges are distinct.  At each vertex, the three selected local
rank-one factors are exactly `e_0,e_1,e_2`; hence

\[
                 \prod_v\det[e_0\ e_1\ e_2]=1.          \tag{5}
\]

The ordered triple `(P_0,P_1,P_2)` is therefore a nonzero rank-respecting
term of the three-copy alternating invariant.

Every pairwise union in (4) is the disjoint union of two four-cycles.  For
example, switching the `P_0/P_1` choice on exactly one component gives

\[
                         R=01|23|47|56                  \tag{6}
\]

with vertex colouring

\[
                              c=00001111.                \tag{7}
\]

Add the external perfect matching

\[
                         N=05|14|27|36.                  \tag{8}

On every edge of `N`, oriented from `{0,1,2,3}` to `{4,5,6,7}`, put the
rank-one cell `e_0 tensor e_1`.  Give `05` weight `-1` and the other three
cells weight `+1`.  All four underlying edges in (8) are new.  Thus the
whole displayed source has sixteen rank-one one-cell matrices.

Both (6) and (8) have colouring (7), with weights

\[
                              z(R)=1,qquad z(N)=-1.       \tag{9}
\]

Direct matching expansion shows that these are the complete nonzero fibre:

\[
                              F_c^\times=\{R,N\}.         \tag{10}
\]

One quick way to see (10) is to note that a proper nonempty subset of the
four cross edges in `N` does not leave unions of the internal pairs
`01,23` and `47,56` at both shores.  Hence a compatible matching either
uses no `N` edge and is forced to be `R`, or uses all four and is `N`.

The three constant fibres remain singleton:

\[
 F_{0^8}^\times=\{P_0\},\qquad
 F_{1^8}^\times=\{P_1\},\qquad
 F_{2^8}^\times=\{P_2\}.                                \tag{11}
\]

The bichromatic cells in (8) cannot enter a constant-colour matching.
Thus the selected normalized terms and their nonzero three-copy witness are
not artifacts of a failed pure coefficient.

At every vertex the two fibre terms (6), (8) use different incident edges.
Their symmetric difference is the alternating cycle

\[
                 0-1-4-7-2-3-6-5-0.                    \tag{12}
\]

Consequently every edge-resolved first-star component is nonzero, while the
two restored components sum to zero.  The even cycle closes the transport
consistently; taking pair or triple overlaps does not create an endpoint or
an odd holonomy.  Lemma 1.1 gives the stronger coordinate-free statement
that every collision/Bianchi order vanishes on this packet.

The order eight in this construction is minimal for the stated simple
geometry.  Two edge-disjoint perfect matchings decompose into alternating
cycles of length at least four.  On six sites their union can have only one
component, whereas (4) has two components at the first possible order.

## 3. Consequence for the broader three-copy route

The pairwise-Hamilton proof uses two facts: a one-/two-chord witness and
singleton uniqueness of its induced colouring.  The cube packet preserves
the locally independent rank-one rainbow triple but removes both global
features relevant to localization:

1. pairwise unions have independent switch components; and
2. the chosen switch has a same-colouring cancellation mate outside the
   selected triple.

First-slice resolution lowers the selected switch's torus order, but it
lowers the mate by the identical amount.  Collision Bianchi identities then
differentiate the zero equality `1-1=0`.  They cannot turn it into a
nonzero singleton.

Accordingly, a uniform continuation from the three-copy invariant needs an
identity which mixes at least two distinct colouring fibres through common
aggregate edge factors.  The selected-triple Laurent rewrite is one such
coupling, but its reversible even-cycle boundary is real; first-slice jets
alone do not remove it.

## 4. Exact audit

Run

```text
python computations/verify_first_slice_bianchi_cancellation_mate.py
```

The checker verifies all pairwise two-cycle decompositions, local determinant
one at every vertex, singleton constant fibres, the exact binomial fibre
(10) with weights `+1,-1`, distinct incident components at every site, and
the single eight-cycle (12).  It also audits every restriction to at most
three sites: the two terms have the same restricted word and opposite
coefficient, so all first-slice cubic components cancel exactly.
