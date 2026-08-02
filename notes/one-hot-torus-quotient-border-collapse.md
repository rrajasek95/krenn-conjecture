# The normalized one-hot border chart collapses to one torus orbit

## Outcome

There is a sharp counterguard to a fast valuative/GIT proof.  On every
properly three-edge-coloured sparse chart used by the all-even Wick boundary,
the entire normalized one-hot source torus is a **single orbit** of the
diagonal torus fixing ternary GHZ.  In particular, each Laurent family in
the global Wick counterguard is exactly a one-parameter subgroup orbit of
one finite all-unit Krenn source—not merely at six sites, but at every order
produced by vertex-to-triangle expansion.

The finite all-unit source is polystable.  Its output has one unit term for
every supported perfect matching, so it is not GHZ, but the closure of its
output orbit contains GHZ.  Consequently the finite output and GHZ define
the same affine target-quotient point.  Thus taking the target-stabilizer
torus quotient erases precisely the difference between finite membership and
the Laurent boundary:

\[
 [A(t)]=[A_*]\quad\hbox{in the source quotient},
 \qquad
 [H(A_*)]=[\Delta]\quad\hbox{in the target quotient}.
\]

Even a hypothetical properness theorem for the induced quotient map could
therefore not produce an exact source for \(\Delta\).  It would only recover
the already existing finite source \(A_*\), whose output is
\(\Delta+\text{mixed terms}\).

This strengthens the six-site one-parameter-subgroup calculation in
[finite-obstruction.md](finite-obstruction.md): that note also proves source
balance and a nonzero invariant at every even order, but does not identify
the whole normalized all-even chart as one target-torus orbit.

## 1. One-hot chart and target stabilizer

Let \(G=(B,E)\) be a cubic graph with a proper edge colouring

\[
                         E=P_0\sqcup P_1\sqcup P_2,
\]

so every \(P_c\) is a perfect matching.  On an edge \(e=uv\in P_c\), put
the single one-hot source coordinate

\[
                         A_e=w_e e_c\otimes e_c,
                         \qquad w_e\ne0.                    \tag{1}
\]

All other source coordinates vanish.  This is an actual one-hot Krenn
chart: every retained source has one endpoint label at each end, and local
diagonal rescaling preserves that incidence rule.

Let

\[
 T_\Delta=\left\{(\lambda_{v,c}):
            \prod_{v\in B}\lambda_{v,c}=1\quad(c=0,1,2)\right\}. \tag{2}
\]

It acts on (1) by

\[
                    w_{uv}\longmapsto
                    \lambda_{u,c}\lambda_{v,c}w_{uv},       \tag{3}
\]

and fixes \(\Delta=\sum_c e_c^{\otimes B}\).  Normalize the sparse chart by

\[
                     \prod_{e\in P_c}w_e=1
                     \qquad(c=0,1,2).                       \tag{4}
\]

These equations are exactly the requirement that the three pure output
coefficients equal one.

## 2. Transitivity lemma

**Lemma (normalized proper-colour chart is one orbit).**  The torus
\(T_\Delta\) acts transitively on the source torus (1), (4).

**Proof.**  Orient each edge of every \(P_c\), independently.  For an
oriented edge \(u\to v\) of colour \(c\), set

\[
                    \lambda_{u,c}=w_{uv}^{-1},
                    \qquad \lambda_{v,c}=1.                 \tag{5}
\]

Every port \((v,c)\) occurs on exactly one edge of \(P_c\), so (5) defines
all \(\lambda_{v,c}\) without conflict.  Equation (4) gives

\[
                  \prod_v\lambda_{v,c}
                  =\prod_{e\in P_c}w_e^{-1}=1,
\]

so \(\lambda\in T_\Delta\).  Formula (3) sends every \(w_e\) to one.
Thus every normalized point is in the orbit of the all-unit source
\(A_*\). \(\square\)

There is a useful lattice version.  The normalized edge-exponent lattice is

\[
 L_E^0=\{(\nu_e)\in\mathbb Z^E:
                    \sum_{e\in P_c}\nu_e=0\text{ for each }c\}. \tag{6}
\]

Given \(\nu\in L_E^0\), orient the edges and put

\[
 h_{u,c}=\nu_{uv},\qquad h_{v,c}=0
                    \quad(u\to v\in P_c).                  \tag{7}
\]

Then \(\sum_vh_{v,c}=0\), so \(h\) is an integral cocharacter of
\(T_\Delta\), and

\[
                         A_\nu(t)=h(t)A_*.                   \tag{8}
\]

No ramified base change or half-integral exponent is needed.  Equivalently,
the restricted port-weight map surjects onto (6).  Its rank is

\[
                       |E|-3={3|B|\over2}-3.                \tag{9}
\]

This equals the dimension of the normalized sparse chart, so its torus
quotient has dimension zero.

## 3. The Wick boundary is a Hilbert--Mumford contraction

For a perfect matching \(M\) of \(G\), let \(m(M)\) be its induced colour
word.  Since there is a unique colour-\(c\) edge at every vertex, the word
determines the matching.  Under the cocharacter (7), its output weight is

\[
 \langle h,m(M)\rangle
   =\sum_{v\in B}h_{v,m(M)_v}
   =\sum_{e\in M}\nu_e.                                    \tag{10}
\]

For the Laurent boundary construction, the three \(P_c\) have weight zero
and every other perfect matching has positive weight.  Equivariance and
(10) therefore give

\[
 H(A_\nu(t))=h(t)H(A_*)
  =\Delta+\sum_{M\notin\{P_0,P_1,P_2\}}
                 t^{\sum_{e\in M}\nu_e}e_{m(M)},            \tag{11}
\]

and hence

\[
                         \lim_{t\to0}h(t)H(A_*)=\Delta.      \tag{12}
\]

Thus the apparent source poles are entirely removable modulo
\(T_\Delta\): apply \(h(t)^{-1}\) and the source is the constant finite point
\(A_*\).  What is not removable is the exact-output error.  In that gauge
all supported edge weights are units, so every mixed matching in (11) has
unit coefficient rather than vanishing.

## 4. Why the affine quotient cannot prove exact membership

The all-unit source orbit is closed.  Indeed, each of its \(3|B|/2\)
supported coordinate weights is

\[
                         e_{u,c}+e_{v,c}.
\]

Giving all of them coefficient one sums to

\[
                         \sum_{v,c}e_{v,c},                  \tag{13}
\]

which restricts to zero on the cocharacter lattice of \(T_\Delta\).
All coefficients in this dependence are positive, so zero is in the
relative interior of the supported weight polytope.  The standard torus
criterion makes \(T_\Delta A_*\) polystable.

Let \(\pi_X,\pi_Y\) be the affine source and target quotients.  Transitivity
gives

\[
                         \pi_X(A_\nu(t))=\pi_X(A_*).         \tag{14}
\]

Equation (12) says \(\Delta\) is in the closure of
\(T_\Delta H(A_*)\), hence every invariant polynomial takes the same value
at the two points:

\[
                         \pi_Y(H(A_*))=\pi_Y(\Delta).        \tag{15}
\]

Whenever \(G\) has an extra perfect matching, however,

\[
                         H(A_*)\ne\Delta.                    \tag{16}
\]

Consequently the fiber of the quotient map over \(\pi_Y(\Delta)\) is
strictly larger than the image of the exact fiber \(H^{-1}(\Delta)\) in the
source quotient.  Indeed, if an exact source \(B\) had
\(\pi_X(B)=\pi_X(A_*)\), the common quotient fiber would contain the unique
closed orbit \(T_\Delta A_*\), so
\(A_*\in\overline{T_\Delta B}\).  Equivariance would give
\(H(A_*)\in\overline{T_\Delta\Delta}=\{\Delta\}\), contradicting (16).
Properness of the quotient map controls the larger quotient fiber and says
nothing that removes the mixed terms in (16).  The known boundary family is
an explicit point of this discrepancy.

The same observation closes two nearby shortcuts:

- every \(T_\Delta\)-invariant rational function on the normalized sparse
  chart is constant where defined, so it has source-relative pole order
  zero along (11); and
- Hilbert--Mumford support instability cannot help, because the finite
  source orbit is already polystable.  The useful cocharacter destabilizes
  the **output toward** its closed GHZ limit while its source orbit has no
  affine limit in that direction.

A non-invariant covariant or a gauge slice can still see the mixed normal
weight in (10), but its normalization must become singular at the GHZ
limit.  That returns to a source-faithful chart calculation; it is not a
properness-after-quotient proof.

## 5. Exact finite audit

The dependency-free checker
[verify_one_hot_torus_quotient_border_collapse.py](../computations/verify_one_hot_torus_quotient_border_collapse.py)
constructs the prism and six vertex-to-triangle expansions, through
\(|B|=18\).  At every order it:

- enumerates every perfect matching and verifies (10)--(12);
- constructs the integral target-fixing cocharacter (7);
- row-reduces the restricted action matrix and obtains rank (9);
- checks transitivity on an unrelated exact rational point satisfying (4);
  and
- verifies that the normalized chart quotient has dimension zero.

Normal, optimized, isolated, and no-site-library runs have digest

    ceeab3be40bba8ce8456c3feb5ab59176d762ab55a160709d85b191aa15ed632

This is a counterguard, not a proof of Krenn's conjecture.  It shows that the
most direct pole-order, Hilbert--Mumford, and torus-quotient properness routes
all identify the known finite one-hot source with its GHZ boundary rather
than separating them.
