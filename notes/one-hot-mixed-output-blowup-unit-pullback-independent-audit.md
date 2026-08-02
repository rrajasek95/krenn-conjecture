# Independent audit: the mixed-output blow-up pulls back trivially

Commit `011e237` is mathematically correct within its stated scope.  On a
fixed normalized properly coloured one-hot source torus, the pullback of the
mixed-output ideal is the unit ideal; the target blow-up nevertheless has
the asserted initial projective direction; and invariant functions regular
at that target limit cannot distinguish it from the finite orbit.

This does not address a blow-up of a larger source compactification, a
non-invariant covariant, or a rational gauge whose normalization is singular
at the exceptional point.

## 1. Pullback of the center

Let the three colour classes of a properly three-edge-coloured cubic graph
be \(P_0,P_1,P_2\), and write

\[
 A=k[w_e^{\pm1}:e\in E]/
       (\prod_{e\in P_c}w_e-1:c=0,1,2).                  \tag{1}
\]

For a perfect matching \(M\), its colour word determines it uniquely.  At a
vertex, the prescribed colour selects the unique incident edge of that
colour, so two matchings with the same word must have every edge in common.
Consequently its output coordinate pulls back to the single monomial

\[
                         y_{m(M)}\longmapsto w^M
                                  =\prod_{e\in M}w_e.     \tag{2}
\]

Every \(w_e\) is a unit in (1), so \(w^M\) is a unit with inverse
\(w^{-M}\).  If the graph has any non-colour perfect matching, (2) is the
pullback of a mixed-coordinate generator.  Hence

\[
                          H^*I_{\rm mix}=A.               \tag{3}
\]

This is an equality of ideals, not merely a radical or generic equality.
The all-unit point proves the chart itself is nonempty.

The Rees algebra of the unit ideal is \(A[s]\), with \(s\) in degree one,
and

\[
                         \operatorname{Proj}A[s]=\operatorname{Spec}A.
                                                               \tag{4}
\]

Thus the pulled-back source blow-up is the identity and has empty
exceptional divisor.  The universal property still gives a unique morphism
from this unchanged source chart to the target blow-up because the pulled-
back ideal is invertible.

The same proof applies to the ideal of the whole GHZ point: adjoining pure
coordinate deviations to the center does not remove the mixed unit already
present in (3).

## 2. Target exceptional direction

Let \(\nu_e\) be the audited integral edge valuations, normalized by

\[
                         \sum_{e\in P_c}\nu_e=0.          \tag{5}
\]

Orient every edge of each \(P_c\).  On an oriented edge \(u\to v\), put

\[
                         h_{u,c}=\nu_{uv},\qquad h_{v,c}=0. \tag{6}
\]

Since each port \((v,c)\) occurs exactly once, this defines an integral
cocharacter, and (5) gives \(\sum_vh_{v,c}=0\).  It therefore belongs to
the diagonal torus fixing \(\Delta\).  Its weight on a supported source edge
is \(h_{u,c}+h_{v,c}=\nu_{uv}\), so

\[
                            A(t)=h(t)A_*                   \tag{7}
\]

for the all-unit source \(A_*\).

For a mixed matching \(M\), equivariance gives output weight

\[
                              d_M=\sum_{e\in M}\nu_e.     \tag{8}
\]

Put \(d=\min_Md_M\).  In a target blow-up chart based at a minimum matching
\(M_0\), every coordinate ratio has order \(d_M-d\ge0\).  Therefore the
special point of the lifted arc is

\[
                 \left[\sum_{M:d_M=d}e_{m(M)}\right].     \tag{9}
\]

The coefficients in (9) are one: word uniqueness makes every supported
coefficient a single matching monomial, and all edge weights of \(A_*\) are
one.  This verifies both the projective direction and its one-parameter-
subgroup provenance.  The target exceptional point comes from the Laurent
boundary of the source chart; it is not an exceptional point of the source
blow-up, which is trivial by (4).

## 3. Exact invariant-function scope

The mixed ideal is stable under the target-fixing torus, so its action lifts
to the target blow-up.  Equation (7) and equivariance give

\[
             \widetilde H(A(t))=h(t)\widetilde H(A_*),
 \qquad
             \lim_{t\to0}h(t)\widetilde H(A_*)=\xi_\nu.  \tag{10}
\]

Every regular invariant function is constant on the orbit and hence on its
closure, proving equality at \(\widetilde H(A_*)\) and \(\xi_\nu\).

The rational statement in the audited note is also correct with its stated
regularity hypothesis.  If an invariant rational function is regular at
\(\xi_\nu\), pull it back along the trait (10).  Its pullback is regular at
the closed point and is constant at the generic point by torus invariance;
therefore its special value is the same constant.  Regularity propagates
along the punctured orbit, so this is also the value at the finite orbit
representative wherever evaluated.

No corresponding claim holds for a non-invariant blow-up coordinate or a
semi-invariant.  Such a covariant can record the normal weights
\(d_M-d\).  Likewise, a rational expression with a pole at \(\xi_\nu\) is
outside the conclusion.  These exclusions are essential and are correctly
acknowledged in `011e237`.

On the source side, the normalized chart is a single target-torus orbit:
orient the colour edges and place \(w_e^{-1}\) at one endpoint.  Thus
\(k(U_G)^{T_\Delta}=k\), independently confirming that any invariant
rational expression in the pulled-back blow-up ratios is constant.

## 4. Finite audit and minor presentation defects

The independent standard-library checker
[verify_one_hot_mixed_blowup_unit_pullback_independent_audit.py](../computations/verify_one_hot_mixed_blowup_unit_pullback_independent_audit.py)
rebuilds the prism expansion through \(n=18\) without importing the audited
checker.  It independently verifies:

- word uniqueness and explicit Laurent inverses for all mixed generators;
- nonnegative orders of every target blow-up ratio;
- the complete minimum-weight exceptional directions;
- an independently split integral target-fixing cocharacter; and
- full action rank on every normalized source chart.

Both the original and independent checkers pass normal Python, `-O`, `-I`,
and `-S`; every per-order mode of the original checker also passes.  The
independent digest is

    48f53b5b1d118c108e184c4ff6f16d4ba01098e2eb27ee4b19f9132bcdaa6107

There are three non-substantive LaTeX transcription errors in the audited
note: equation (12) has a comma where multiplication spacing was intended,
equation (16) has `,1` in the exponent instead of an indicator symbol, and
equation (18) is missing the backslash in `\left[`.  They do not affect the
checker or any mathematical assertion, but should be repaired in a later
documentation pass.
