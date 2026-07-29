# Independent audit of the final \((8,7,3)\) exchange closure

## 1. Audit conclusion

This note independently audits
[live-three-zero-seventh-split-final-773-exchange-closure.md](live-three-zero-seventh-split-final-773-exchange-closure.md).
The exchange--residue--Wronskian proof is sound.  In particular, none of
the three delicate possibilities changes the conclusion:

1. a zero singleton is compatible with every cubic lift;
2. a common factor of the final polynomial space only strengthens the
   Wronskian inequality, because every common root at a Robin node is
   automatically double;
3. the seven unmatched double labels in the formal full core are exactly
   the numerator factor needed in the residue calculation.

No genericity or division by a value of a residual polynomial is used.

## 2. Initial cores and the exact rational lift

There are seven double classes and three singleton classes.  Every
seven-class set contains at least four doubles.  Selecting one label from
each of its classes therefore leaves at least four singleton mates in the
complement, so the simultaneous-Hermite lemma applies to every one of the

\[
                           \binom{10}{7}=120                \tag{A1}
\]

initial cores.  Since the complementary label polynomial has degree ten
and the Hermite numerator has degree at most fourteen, every core has a
nonzero residual of degree at most four.

It is useful to audit exchange before writing any Robin coefficient.  If
\(m_v\in\{1,2\}\) is the full multiplicity of value \(v\), set

\[
 B_T(z)=\prod_{v\in V}(z-v)^{m_v-\mathbf1_{v\in T}},
 \qquad
 \Delta_T(z)=(z+\mu)^2\prod_{v\in T}(z+v)^2.              \tag{A2}
\]

For \(b\notin T\), the cubic

\[
                            g_b(z)=(z-b)(z+b)^2             \tag{A3}
\]

gives the literal rational-function identity

\[
 {B_{T\cup\{b\}}g_bq\over\Delta_{T\cup\{b\}}}
                         ={B_Tq\over\Delta_T}.             \tag{A4}
\]

This holds for both \(m_b=1\) and \(m_b=2\).  Thus a singleton becoming
fully selected, or one copy of a double becoming selected, is handled by
the same lift.  At a distinct Robin node \(-a\),

\[
                  {g_b'(-a)\over g_b(-a)}
                       =-\left({1\over a+b}-{2\over b-a}\right), \tag{A5}
\]

and \(g_b(-b)=g_b'(-b)=0\).  If \(b=0\), then \(g_0=z^3\); it still has
the required double zero and is coprime to every other gauge because no
other value is zero.  This verifies both the ordinary and zero-anchor
exchange steps.

The already independently audited three-lift lemma applies at set sizes
eight, nine, and ten.  At those stages the deletion residual degrees are,
respectively,

\[
                              4,\quad5,\quad6,               \tag{A6}
\]

and the lifted degree bounds are

\[
                              7,\quad8,\quad9.               \tag{A7}
\]

At the first two stages the lift span has dimension at least three.
Killing its two leading coefficients leaves a nonzero polynomial of
degree at most five and then at most six.  At the last stage one retains
an at-least-three-dimensional space

\[
                     K\subset\mathbb C[z]_{\le9}.           \tag{A8}
\]

The audit checker re-enumerates the gcd and ramification inequalities in
the three-lift lemma for all three set sizes, including the possible zero
anchor.  In particular, a common factor cannot absorb enough of the
simple \(+b\) and double \(-b\) roots to evade Riemann--Hurwitz.

## 3. Full-core multiplicities and the extra node

After one label has been formally selected from every class, exactly one
mate remains at each of the seven double values and no label remains at a
singleton.  Hence

\[
 B(z)=\prod_{d\in D}(z-d),\qquad
 \Delta(z)=(z+\mu)^2\prod_{v\in V}(z+v)^2,\qquad
 F_q={Bq\over\Delta}.                                     \tag{A9}
\]

For \(a\in V\), remove the factor \((z+a)^{-2}\) at \(z=-a\).  The
logarithmic derivative of the remaining regular cofactor is

\[
 {B'(-a)\over B(-a)}-{2\over\mu-a}
                   -2\sum_{v\ne a}{1\over v-a}.           \tag{A10}
\]

This is exactly the full-core Robin coefficient obtained by expanding the
multiplicity-weighted baseline.  For a double anchor, the self mate is the
term \(-1/(2a)\) inside \(B'(-a)/B(-a)\).  For a singleton anchor there is
no self term; consequently (A10) remains regular if that singleton is
zero.  Pair-sum admissibility makes \(B(-a)\ne0\).

Thus every \(q\in K\) makes the residue of \(F_q\) vanish at all ten poles
\(-a\), \(a\in V\).  The degrees are

\[
                 \deg B=7,\qquad \deg q\le9,\qquad
                 \deg\Delta=22,                            \tag{A11}
\]

so \(F_q=O(z^{-6})\).  In particular, there is no residue at infinity.
The only remaining pole is the double pole at \(-\mu\); the residue theorem
forces its residue to vanish.  Removing \((z+\mu)^{-2}\) gives, without
division by \(q(-\mu)\),

\[
 q'(-\mu)+\left({B'(-\mu)\over B(-\mu)}
                  -2\sum_{v\in V}{1\over v-\mu}\right)q(-\mu)=0. \tag{A12}
\]

The eleven nodes \(-\mu\) and \(-v\), \(v\in V\), are distinct.  Equality
\(-\mu=-v\) would say \(\mu=v\), while all needed regular factors follow
from \(\mu\ne v\), \(\mu+v\ne0\), and the pair-sum conditions.  A zero
singleton creates the node zero but cannot collide with \(-\mu\).

## 4. Common factors and the Wronskian count

Let \(r=\dim K\ge3\), let \(H=\gcd K\), and put \(e=\deg H\).  If \(H\)
vanishes at one of the eleven Robin nodes \(\xi\), write \(q=Hf\).  Since
the reduced space has no common root at \(\xi\), some \(f(\xi)\ne0\).
Substitution in the common Robin equation gives

\[
                              H'(\xi)f(\xi)=0.              \tag{A13}
\]

Therefore \(H'(\xi)=0\): every such common root has multiplicity at least
two.  If \(b\) is the number of Robin nodes absorbed by \(H\), then

\[
                                  e\ge2b.                   \tag{A14}
\]

At each of the other \(11-b\) nodes, divide the Robin equation by the
nonzero value of \(H\).  In a basis adapted to vanishing order, one section
is nonzero and the other \(r-1\) sections have both value and derivative
zero.  Their vanishing sequence is at least

\[
                               0,2,3,\ldots,r,              \tag{A15}
\]

so the Wronskian weight is at least \(r-1\).  The reduced polynomials have
degree at most \(9-e\), and their nonzero Wronskian has degree at most

\[
                              r(10-e-r).                    \tag{A16}
\]

Consequently

\[
 (11-b)(r-1)\le r(10-e-r)\le r(10-2b-r).                  \tag{A17}
\]

The difference between the outer left and right sides is

\[
                         r^2+r-11+b(r+1).                  \tag{A18}
\]

It is already \(1\) at the smallest case \(r=3,b=0\), and increases with
both variables.  Thus (A17) is impossible.  This independently confirms
the final contradiction.

## 5. Independent exact checker

[verify_live_three_zero_seventh_split_final_773_exchange_audit.py](../computations/verify_live_three_zero_seventh_split_final_773_exchange_audit.py)
does not import the main checker.  It enumerates all 120 legal initial
cores; verifies the rational lift for both multiplicities and at a zero
anchor; exhausts the gcd/Riemann--Hurwitz inequalities at all three
exchange sizes; reconstructs both double- and singleton-anchor full-core
coefficients; checks the local residue functional and degree-six decay;
and exhausts every possible Wronskian parameter \(r,e,b\).
