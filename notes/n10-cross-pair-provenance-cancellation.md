# Ordered cross-pair provenance is not separated by the ordinary equations

## Outcome

The ordered two-endpoint grade from the preceding note is too fine to be
recovered from ordinary cylinder data.  It is separated neither by the
target-stabilizing anchored torus nor by the source multidegree after
forgetting the formal variables.

The smallest exact collision uses the endpoint-swapped pair

\[
\begin{aligned}
 m_A&=x_{08;00}x_{19;00},\\
 m_B&=x_{18;00}x_{09;00}.                               \tag{1}
\end{aligned}
\]

These are distinct source monomials on four distinct cells, but their full
matching grades and every quadratic cofactor grade are literally equal.
With weights

\[
 x_{08;00}=x_{19;00}=x_{18;00}=1,
 \qquad x_{09;00}=-1,                                   \tag{2}
\]

their evaluated coefficients satisfy \(m_A+m_B=0\).  The full quadratic
output and all quadratic cofactor contributions cancel exactly.  Both
ordered source grades are nonzero, so ordinary data cannot imply that each
one vanishes separately.

This is not a Krenn counterexample.  The explicit cancelled source has no
complete N=10 high-sector cylinder on any of the six adjacent cuts.  It
disproves only a formal provenance-separation step.  The correct
output-visible datum is the endpoint-symmetrized permanent grade
\(m_A+m_B\), not the two orientations individually.

## 1. Target-stabilizing torus collision

Use one torus coordinate for each vertex-colour pair at N=10.  Constrain the
torus by

1. the 19 occupied coordinates of the anchored forced-pair lift, and
2. the three target characters
   \(\sum_{v=0}^9e_{v,c}\), \(c=0,1,2\).

The exact constraint rank is 18.  Modulo that constraint span, the two cells
of \(m_A\) have opposite characters:

\[
\begin{aligned}
 [\chi(x_{08;00})]&=-e_3-e_{27},\\
 [\chi(x_{19;00})]&= e_3+e_{27}.                         \tag{3}
\end{aligned}
\]

Consequently

\[
                         [\chi(m_A)]=0.                  \tag{4}
\]

No target-stabilizing one-parameter subgroup which fixes the anchored lift
can assign the witness pair a nonzero separating weight.  More strongly,
the endpoint swap has the same character before taking any quotient:

\[
 \chi(m_A)=e_{0,0}+e_{1,0}+e_{8,0}+e_{9,0}=\chi(m_B).   \tag{5}
\]

Among all 4,536 opposite-new, distinct-old quadratic pairs, there are 959
exact quotient-character classes.  The zero class contains 132 ordered
pairs.  Thus the witness collision is part of a substantial character
stratum, not an isolated degeneracy.

## 2. Universal endpoint-swap identity

Let \(v\ne w\) be old vertices.  Fix old endpoint colours \(\alpha,\gamma\)
and new endpoint colours \(\beta,\delta\).  Compare

\[
\begin{aligned}
 m_{v,w}&=x_{v8;\alpha\beta}x_{w9;\gamma\delta},\\
 m_{w,v}&=x_{w8;\gamma\beta}x_{v9;\alpha\delta}.        \tag{6}
\end{aligned}
\]

In either matching, the same old vertices \(v,w\) are removed, they receive
the same old colours, and new vertices 8,9 receive the same new colours.
The remaining old perfect matching is therefore the same \((N-2)\)-site
cofactor.  Hence

\[
              \Phi_{\rm full}(m_{v,w})
                    =\Phi_{\rm full}(m_{w,v}).           \tag{7}
\]

The same statement holds for every cofactor column.  If a hole prevents two
cross cells from occurring, both sides vanish.  Otherwise both orientations
again remove the same two old endpoints and leave the same matching problem:

\[
              \Phi_{\rm cof}(m_{v,w})
                    =\Phi_{\rm cof}(m_{w,v}).            \tag{8}
\]

The checker classifies all 4,536 quadratic-capable grades.  Their nonzero
output images form exactly 2,268 classes of size two, and every class is
precisely the swap (6).  The two monomials in each class use four distinct
cross coordinates.  Thus four cells are minimal for a cancellation between
two nonzero quadratic grades; no three-cell shared-coordinate cancellation
exists in this model.

Equations (7)--(8) show that the cross block enters through a permanent.  In
the two-old by two-new submatrix its visible quadratic coefficient is

\[
 x_{v8;\alpha\beta}x_{w9;\gamma\delta}
 +x_{w8;\gamma\beta}x_{v9;\alpha\delta}.                \tag{9}
\]

Over signed or complex weights this permanent can vanish with both monomials
nonzero.

## 3. Source multidegree does not descend injectively

In the free polynomial ring, \(m_A\) and \(m_B\) have different
multidegrees.  Formal coefficient extraction therefore distinguishes them.
But the literal matching and cofactor maps have the binomial kernel

\[
                            m_A-m_B.                     \tag{10}
\]

After source coefficients are evaluated, the ordinary cylinder equations
see only the common image multiplied by \(m_A+m_B\).  Relation (2) sets this
visible coefficient to zero while neither formal multidegree is zero.

Therefore a free source grading is useful extra data but is not inferred
from the ungraded finite source.  In particular, the implication

\[
 \text{ordinary four-cylinder equations}
       \Longrightarrow
 \text{each ordered-pair graded equation}                \tag{11}
\]

cannot follow from multidegree bookkeeping alone.

The natural repair is to quotient the provenance grading by (10), retaining
one symmetrized grade per endpoint-swap class.  The counterguard in the
preceding note should be interpreted as acting on this visible permanent
coefficient.  Relation (2) then has zero symmetrized grade and creates no
contradiction.

## 4. Exact cancellation audit

For the explicit four-cell source (2), the checker verifies:

1. its full N=10 tensor is exactly the tensor of the isolated forced-pair
   lift;
2. on every cut, its cofactor-column table is exactly the affine sum of the
   four one-cross column directions—there is no surviving quadratic term;
3. the three pure output coefficients are consequently unchanged; and
4. the actual high-sector cut census is

| cut | cofactor rank | full residual membership |
|---:|---:|---|
| 0 | 19 | false |
| 1 | 19 | false |
| 2 | 20 | false |
| 3 | 20 | false |
| 4 | 20 | false |
| 5 | 21 | false |

The last item is the reason this is not a conjecture counterexample and does
not disprove a more restrictive separation theorem which assumes four
complete cylinders.  It does show that such a theorem would need to use the
simultaneous equations essentially; neither torus characters nor formal
source degrees provide separation on their own.

## 5. N-stability

The identity (7) is local and independent of N: it only uses the fact that
both orientations remove the same two old vertices and leave the same old
cofactor.  Thus the binomial kernel (10) persists for every even order.

As an exact finite check, the script adjoins another isolated diagonal pair,
uses new cross vertices 10,11, and verifies at N=12 that

\[
 \Phi(x_{0,10}x_{1,11})=\Phi(x_{1,10}x_{0,11})          \tag{12}
\]

and that the permanent-zero four-cell block again leaves the full tensor
unchanged.  The obstruction to ordered provenance separation is therefore
N-stable, including on the forced-pair tower.

## 6. Sharp next question

After quotienting by endpoint swap, there are 2,268 visible quadratic grades
at N=10.  The next bounded test is not another ordered-pair search.  It is:

1. group these permanent grades by the anchored target-stabilizing character;
2. project their four candidate-cut guarded rows to the coupled-cylinder
   quotients; and
3. search exactly for the smallest linear cancellation between **distinct
   permanent classes** which also respects the three fixed cuts.

If that projected map is injective on each character class, it gives the
bounded provenance-separation lemma that the ordered grading could not.  If
not, the smallest kernel vector is the next honest countermodel to the
uniform route.

## Reproduction

    python3 computations/verify_n10_cross_pair_provenance_cancellation.py
    python3 -O computations/verify_n10_cross_pair_provenance_cancellation.py
    python3 -I computations/verify_n10_cross_pair_provenance_cancellation.py
    python3 -S computations/verify_n10_cross_pair_provenance_cancellation.py

All character quotients, matching tensors, cofactor tables, ranks, and
cancellation identities are exact over the rationals.
