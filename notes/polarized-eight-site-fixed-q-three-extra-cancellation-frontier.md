# The exact three-cell cancellation frontier at the fixed polarized seed

## 1. Result and strict scope

Work in the eight-site ternary square-zero algebra and put

\[
\begin{aligned}
q={}&23_{00}+45_{00}+67_{00}
     +01_{11}+36_{11}+57_{11}\\
   &+02_{22}+14_{22}+56_{22},\\
z={}&01_{00}+24_{11}+37_{22}.
\end{aligned}                                                    \tag{1}
\]

As before, \(ij_{cd}\) retains the colour at each ordered endpoint.  Direct
multiplication gives

\[
                         zq^{[3]}=\Delta_{8,3}.                  \tag{2}
\]

Choose three distinct cells \(e<f<g\) outside \(\operatorname{supp}(q)\),
and let \(t,u,v\in\mathbb C^\times\).  Among all

\[
                  \binom{243}{3}=2,362,041                     \tag{3}
\]

unordered triples, there are exactly \(87,214\) triples for which some such
parameters satisfy

\[
                z(q+te+uf+vg)^{[3]}=\Delta_{8,3}.               \tag{4}
\]

They split into two logically different classes.

1. Exactly \(87,027\) triples are made of individually invisible cells and
   preserve (4) identically for all \(t,u,v\).  These are the triangles in
   the previously computed graph of 3,960 compatible invisible pairs.  This
   note records their count but makes no pair-cap claim for them; they are
   closed separately by the
   [compatible-three-cell theorem](polarized-eight-site-fixed-q-compatible-three-extra-pair-cap-obstruction.md).
2. Exactly \(187\) triples contain one individually visible cell and preserve
   (4) only on an explicit binomial parameter locus.  For every one of these
   187 families, at every point of that locus with \(tuv\ne0\), and for every
   \(a\in\mathbb C\) and all linear \(p,s\),

   \[
     \boxed{
     (aQ+4ps)Q^{[3]}\ne\Delta_{8,3},\qquad Q=q+te+uf+vg.
     }                                                          \tag{5}
   \]

Thus the genuinely new three-cell cancellation frontier has no pair-cap
preimage.  Statement (5) itself does not cover the 87,027 identically
compatible triples; the separate theorem cited above now does.  Arbitrary
perturbations with four or more cells and arbitrary quadratics remain open.
This does not prove Krenn's conjecture.

The standalone exact checker is
[`verify_polarized_eight_site_fixed_q_three_extra_frontier.py`](../computations/verify_polarized_eight_site_fixed_q_three_extra_frontier.py).

## 2. Exact Laurent-debt expansion

For a cell \(x\), a pair \(x,y\), and a triple \(x,y,w\), define the top-word
debt vectors

\[
 D_x=z xq^{[2]},\qquad D_{xy}=zxyq,\qquad D_{xyw}=zxyw.          \tag{6}
\]

The desired difference is exactly

\[
\begin{aligned}
z(q+te+uf+vg)^{[3]}-\Delta_{8,3}
={}&tD_e+uD_f+vD_g\\
  &+tuD_{ef}+tvD_{eg}+uvD_{fg}+tuvD_{efg}.                     \tag{7}
\end{aligned}
\]

The checker reconstructs every vector in (6) directly from (1).  The
one-cell debts have the support-size census

\[
              99\cdot0+135\cdot1+9\cdot2,                     \tag{8}
\]

while the 29,403 pair debts have the census

\[
              25,830\cdot0+3,573\cdot1.                       \tag{9}
\]

Every nonzero coefficient in (8), (9), and every triple debt is exactly one.
Consequently, if some top word occurs in only one of the seven Laurent
monomials in (7), then (7) cannot vanish on \((\mathbb C^\times)^3\).

This singleton test rejects exactly 2,274,826 triples.  Only 87,215 triples
survive at the level of word support:

| exact class | count |
|---|---:|
| all seven debt vectors vanish | 87,027 |
| one binomial cancellation equation | 187 |
| exceptional three-equation system | 1 |

The 87,027 zero-debt cases consist precisely of triples of the 99 invisible
cells whose three constituent pairs are among the 3,960 compatible pairs.
For every such triangle the triple debt also vanishes; there is no additional
three-way obstruction.

The one exceptional triple is exactly

\[
                 (e,f,g)=(01_{00},24_{11},37_{22})=z.           \tag{10}
\]

Its three word equations are

\[
             t+u=0,\qquad u+v=0,\qquad tu+tv+uv=0.              \tag{11}
\]

The first two turn the last left-hand side into \(-u^2\), so (11) has no
solution with \(tuv\ne0\).  This proves completeness of the 87,214 count.

## 3. The 187 genuinely new families

The cells are ordered lexicographically, so \(t,u,v\) always multiply
\(e,f,g\), respectively.  The 187 binomial loci have the following exact
census.

| relation | count | lexicographically first triple |
|---|---:|---|
| \(v+tu=0\) | 103 | \((03_{10},15_{10},35_{00})\) |
| \(t+uv=0\) | 48 | \((01_{00},05_{01},17_{01})\) |
| \(1+tv=0\) | 9 | \((04_{20},16_{00},25_{20})\) |
| \(1+tu=0\) | 27 | \((04_{10},15_{10},26_{00})\) |

These four examples are representatives of the four coefficient signatures,
not orbit representatives: the stabilizer of the asymmetric pair \((q,z)\)
inside the site-permutation times global-colour-permutation group is trivial.
The complete ordered list is pinned by the digest in Section 6.

Every one of the 187 triples has exactly one nonzero one-cell debt.  In 151
cases that debt cancels a pair debt, producing \(v+tu=0\) or \(t+uv=0\).
In the other 36 cases it cancels the triple debt, producing \(1+tv=0\) or
\(1+tu=0\).  Their physical-pair intersection profiles are

\[
       150\text{ of type }(0,1,1),\qquad
        37\text{ of type }(0,0,0),                              \tag{12}
\]

where the profile is the sorted triple of pairwise endpoint-intersection
sizes.  In particular, these are not hidden members of the earlier
one-cell or compatible two-cell families.

## 4. Projective Gram closure for 180 families

Write a linear mode vector as \(x_{i,c}=(p_{i,c},s_{i,c})\) and set

\[
 \beta((r,w),(r',w'))=rw'+wr'.                                  \tag{13}
\]

For each family the checker expands every top coordinate of

\[
               4psQ^{[3]}+4aQ^{[4]}=\Delta_{8,3}               \tag{14}
\]

as a tagged polynomial in \(t,u,v\).  It uses only the following
parameter-safe consequences.

* If a non-target coordinate has no \(aQ^{[4]}\) term and has exactly one
  tagged Gram contributor \(m(t,u,v)\beta(x_X,x_Y)\), then the Laurent
  monomial \(m\) is nonzero on \(tuv\ne0\), so \(\beta(x_X,x_Y)=0\).
* If a pure target coordinate has no \(aQ^{[4]}\) term, at least one of its
  Gram contributors must be nonzero.  The checker branches over that finite
  list.  Taking extra branches whose coefficient might cancel can only make
  the argument stronger: every actual nonzero contributor appears among the
  checked branches.

On the endpoints of the three selected nonzero Gram edges, each vertex is a
nonzero vector and hence determines a projective line in \(\mathbb C^2\).
A zero Gram edge sends a line \(L\) to \(L^\perp\).  Therefore an odd zero
path between the endpoints of a required nonzero edge is contradictory.  An
odd zero cycle forces an isotropic component and gives the same contradiction.
The checker performs this bipartite-parity test literally for every branch.

It closes 180 of the 187 families.  Their branch histogram is

\[
       159\cdot1+20\cdot2+1\cdot3=202                         \tag{15}
\]

certificates, all of the isotropic-component kind.

## 5. Seven exact saturated unit ideals

The parameter-free closure deliberately stops on seven families because a
pure coordinate has a direct \(aQ^{[4]}\) contribution:

\[
\begin{gathered}
(01_{00},05_{01},17_{01}),\quad
(01_{00},06_{01},13_{01}),\quad
(01_{00},07_{01},15_{01}),\\
(03_{12},17_{12},37_{22}),\quad
(04_{11},12_{11},37_{22}),\\
(06_{12},15_{12},37_{22}),\quad
(07_{12},13_{12},37_{22}).                                    \tag{16}
\end{gathered}
\]

For each case the optional audit writes every coordinate of (14) over
\(\mathbb Q\), adds its binomial relation from Section 3, and saturates the
parameter torus by adjoining

\[
                         h t u v-1=0.                           \tag{17}
\]

There are 53 variables: the 48 coordinates of \(p,s\), the scalar \(a\), the
three parameters, and \(h\).  The seven systems have respectively

\[
                  290,284,284,284,319,284,290                  \tag{18}
\]

equations in the order displayed in (16).  Singular reduces every
characteristic-zero ideal to the one-element basis \([1]\).  Hence none has
a complex solution on \(tuv\ne0\), completing the proof of (5).

## 6. Reproducibility and frozen ledgers

Run the finite census and the 180 projective closures with

```text
python3 computations/verify_polarized_eight_site_fixed_q_three_extra_frontier.py
```

Run the seven full saturated ideals with

```text
python3 computations/verify_polarized_eight_site_fixed_q_three_extra_frontier.py --full-ideals --workers 3
```

The checker asserts, rather than merely prints, the following SHA-256
digests:

| ledger | SHA-256 |
|---|---|
| classification of all 2,362,041 triples | `26d25bdc52cb84a1905f04cbcb49fd515257d7ec0aa243dbdd93e290e50d1046` |
| all 87,214 solution families | `cc7fcbae3ad29af3b35f90faaa9d0a2c5dad616f64c7b24f5b6ec90961831bb1` |
| ordered list of the 187 new families | `0471329f6bf631d816bdeee9dc0419242039ca20475933e4698ef45f658f9abd` |
| all 187 projective-closure outcomes | `649dcab156a6beb2b7575c9e3b65186807f6354ad755a0729776f9e3da7df645` |

The default audit uses only exact integer combinatorics.  The optional ideal
audit uses Singular over \(\mathbb Q\); the torus saturation (17) makes its
unit-ideal conclusion exactly the required complex nonzero-parameter claim.
