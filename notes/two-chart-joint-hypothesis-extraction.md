# What one curvature minor jointly extracts on the two physical charts

## 1. Outcome

Let an entry-minimal exact source on \(2m\geq 8\) sites be put in the
output of the
[unconditional curvature theorem](unconditional-curvature-line-selection.md).
Thus \(q,r\) are good
neighbours of \(p\), \(s\) is a fourth site, and for fixed physical
colours \(a,b,c,d\)

\[
 A=A_{pq}(a,b),\quad B=A_{pr}(a,c),\quad
 F=A_{qs}(b,d),\quad U=A_{rs}(c,d),
 \qquad \kappa=AU-BF\ne0.                                    \tag{1}
\]

After exchanging \(q,r\), one may and will assume \(A\ne0\).  Put
\(h=m-1\geq3\).  The exact joint extraction statement is as follows.

**Theorem 1.1 (automatic two-chart packet).**  For the two canonical
physical lines

\[
 K_{pq}(u,v)=uE_{ab}+vI,\qquad
 K_{pr}(u,v)=uE_{ac}+vI,                                      \tag{2}
\]

the selected source already supplies simultaneously:

1. all four deleted endpoint-star maps are injective;
2. both complete normalized full-nine systems, with the three diagonal
   target rows in the original common physical labels;
3. the power-free full-matrix overlap connection, its normal-row
   companion, the common \((L,M)\) four-cut packet, and every fixed-label
   coefficient of those identities; and
4. a nonzero activity polynomial on the \(pq\)-line.

The \(pr\)-line is generically active if and only if

\[
                 (B,\operatorname {tr}A_{pr})\ne(0,0).         \tag{3}
\]

Thus one minor gives one generically active chart, not necessarily two.
If both \(A\) and \(B\) are nonzero, both charts are generically active;
this is a sufficient strengthening, not an output of (1).

Moreover, on either chart whose clean-error coordinates have gcd one,
each of its two endpoint stars automatically has a three-site physical
Hall--Rado selector.  This conclusion is valid for a diagonal selected
cell as well as an off-diagonal one.  If the two endpoint selector
matroids on that chart do not have disjoint bases, their failure is
already routed by the uniform maximal-shore theorem to the audited
common-coloop, line-plus-plane, rank-\((1,1)\), or endpoint-dark gates.

Consequently the rootless part of the proposed two-chart lemma does not
need separate assumptions for full-nine provenance, diagonal anchors,
overlap identities, endpoint injectivity, or individual endpoint
selectors.  The genuine extraction assumptions left there are:

* generic activity of the second line, if the conclusion is to localize
  both charts at activity;
* any disjoint, separated, or fixed-colour compatibility stronger than
  the ordinary individual selectors; and
* in the rooted ledger, the clean diagonal unary--complementary routing.

The last routing is much stronger than merely having selected a diagonal
entry.  For one oriented chart with selected coefficient
\(\alpha\ne0\), second label \(e\), and block trace \(\tau\), the exact
inactive boundary is:

* if \(a\ne e\), the only colour-boundary point is \(E_{ae}\), and the
  other possible inactive point is the scalar-zero cap
  \(K_*=\tau E_{ae}-\alpha I\); there is no diagonal
  unary--complementary pencil to rename into existence;
* if \(a=e\), the line contains \(E_{aa}\) and \(E_{aa}-I\), but the
  latter is scalar-zero exactly when \(\tau=\alpha\).  The desired Omega
  packet additionally requires both displayed points to be clean.

In particular, the cases \(a=b\) and \(a\ne b\) do not differ for
ordinary rootless selector extraction.  They remain genuinely different
for the scalar-zero target used after selection and for inactive-root
routing: the off-diagonal scalar-zero matrix is automatically invertible
and ternary, whereas the diagonal one has the separate ternary/binary
trace split.

## 2. Proof of the automatic packet

For a physical pair \(x,y\), let \(q_{xy}\) be the internal quadratic,
let \(p_i,s_j\) be its two endpoint-star rows, and put
\(a^{xy}_{ij}=A_{xy}(i,j)\).  Sorting the exact top matching identity by
the two endpoint colours gives all nine equations

\[
 a^{xy}_{ij}q_{xy}^{[h]}+p_i s_jq_{xy}^{[h-1]}
       =\delta_{ij}X_i.                                       \tag{4}
\]

Equivalently, for

\[
             B^{xy}_{ij}=p_i s_j+{a^{xy}_{ij}\over h}q_{xy},
\]

one has

\[
             B^{xy}_{ij}q_{xy}^{[h-1]}=\delta_{ij}X_i.         \tag{5}
\]

Applying (5) to \(pq\) and \(pr\) proves the simultaneous full-nine
claim.  The rows \(i=j\) are the three literal diagonal anchors.  No
selector normalization and no relabelling has been used, so the target
labels on the two charts are the same physical \(0,1,2\).

The overlap data are equally automatic; these are the full-label version
of the
[physical pair-cap connection](overlapping-pair-cap-bianchi-connection.md).
On the common complement of
\(p,q,r,s\), write \(z\) for the internal quadratic and \(x_i,y_j,t_k,v_l\)
for the four star rows.  Put
\[
\begin{gathered}
 A_{ij}=A_{pq}(i,j),\quad B_{ik}=A_{pr}(i,k),\quad
 E_{il}=A_{ps}(i,l),\\
 F_{jl}=A_{qs}(j,l),\quad U_{kl}=A_{rs}(k,l),
\end{gathered}
\]
and use the full-matrix effective quadratics and \(s\)-normal rows

\[
 f_{ij}=A_{ij}z+x_i y_j,\qquad
 g_{ik}=B_{ik}z+x_i t_k,                                      \tag{6}
\]

\[
 H_{ij;l}=A_{ij}v_l+E_{il}y_j+F_{jl}x_i,\qquad
 N_{ik;l}=B_{ik}v_l+E_{il}t_k+U_{kl}x_i .
\]

direct expansion gives, for every \(i,j,k,l\),

\[
\begin{aligned}
 f_{ij}t_k-g_{ik}y_j
   &=(A_{ij}t_k-B_{ik}y_j)z,\\
 U_{kl}f_{ij}+t_kH_{ij;l}-F_{jl}g_{ik}-y_jN_{ik;l}
   &=(A_{ij}t_k-B_{ik}y_j)v_l
     +(A_{ij}U_{kl}-B_{ik}F_{jl})z .                           \tag{7}
\end{aligned}
\]

The normal-row companion and common \((L,M)\) formulas are the other
coefficients of the same literal source expansion.  At the selected
labels, the last coefficient in (7) is exactly \(\kappa\).  Hence the
fixed-label connection and every four-site cut in the proposed overlap
lemma are consequences of using the two actual charts of one source;
they are not further chart-extraction hypotheses.

Goodness of \(pq\) and \(pr\) is part of the curvature-selection output,
so their four endpoint maps are injective.  It remains to audit activity.
Write

\[
 \tau_{pq}=\operatorname {tr}A_{pq},\qquad
 \tau_{pr}=\operatorname {tr}A_{pr}.
\]

On (2), the two direct scalars are

\[
 s_{pq}(u,v)=Au+\tau_{pq}v,\qquad
 s_{pr}(u,v)=Bu+\tau_{pr}v.                                  \tag{8}
\]

For a line \(uE_{ae}+vI\), its three target coordinates are

\[
                 \kappa_i(u,v)=u\delta_{ia}\delta_{ie}+v.    \tag{9}
\]

Their product is \(v^3\) when \(a\ne e\), and
\((u+v)v^2\) when \(a=e\); it is never the zero polynomial.  Therefore
the full activity product is nonzero exactly when the corresponding
linear form in (8) is nonzero.  Since \(\kappa\ne0\) implies
\((A,B)\ne(0,0)\), exchanging \(q,r\) makes \(A\ne0\) and proves activity
on \(pq\).  The same calculation proves the exact second-chart criterion
(3).  Notice that the second chart can be active in the trace-only case
\(B=0\), \(\tau_{pr}\ne0\).  Section 4 explicitly assumes a nonzero
selected coefficient, so its boundary list must not be applied to that
case without the separate calculation recorded there.

## 3. Rootless selectors, including the diagonal case

Fix either good chart and suppose its clean error is rootless.  If its
direct scalar is a nonzero linear form on the line, evaluate at its unique
scalar-zero point \(K_*\).  The uniform clean-error identity gives

\[
                   {\cal E}(K_*)=r(K_*)^{[h]}\ne0.             \tag{10}
\]

If the direct scalar vanishes identically on the line, rootlessness gives
the same nonnilpotence at every point of the line, so one may choose any
one of them.  In either case the contracted response has the form

\[
                  r(K)=P^{\mathsf T}KS                         \tag{11}
\]

for the two injective physical endpoint stars.

The
[uniform full-nine exceptional-shore theorem](full-nine-type3-annihilator-plane-closure.md)
applied to (5) gives

\[
        \operatorname {rank}P_{\bar x},
        \operatorname {rank}S_{\bar x}\ge2
        \qquad\text{for every residual site }x.               \tag{12}
\]

The Hall--Rado selector dichotomy then has only two other failures:
support of an endpoint star on at most two sites, or rank at most one away
from one site.  The second is excluded by (12), and the first would make
\(r(K)^{[h]}=0\) for \(h\ge3\), contrary to (10).  Both endpoint stars
therefore have three-site selectors.

Nothing in this proof uses \(a\ne e\), invertibility of \(K_*\), or a
ternary target at \(K_*\).  In the diagonal trace case \(\tau=\alpha\),
\(K_*=\alpha(E_{aa}-I)\) is rank two and its target is binary, but (10)--
(12) are unchanged.  Thus the diagonal binary trace gate is a rooted
packet distinction, not a selector-extraction obstruction.

Ordinary selectors should not be conflated with stronger compatibility.
For the two Rado matroids of one chart, disjoint bases exist exactly under
the matroid-union inequalities.  If they fail, the uniform maximal-shore
theorem gives the exhaustive audited list in
[the maximal-defect note](uniform-selector-union-maximal-defect-shore.md).
If they hold, the selected
local probes can still be oblique.  A selector compatible with one literal
monochromatic target word would require, for some fixed colour \(c\),

\[
 \rho_{x_0}^{(c)}\wedge\rho_{x_1}^{(c)}
        \wedge\rho_{x_2}^{(c)}\ne0                             \tag{13}
\]

at three distinct sites.  Neither injectivity nor the ordinary Rado
theorem implies (13).  Likewise disjoint bases do not supply separated
target-zero representatives or an own-edge Jacobian lift.  These are the
already audited
[fixed-label](h3-one-anchor-selector-four-cut-guard-and-two-anchor-threshold.md)
and
[selector-incidence](selector-hall-base-packing-and-block-jacobian-guard.md)
gates, not missing parts of Theorem 1.1.

The nonzero minor supplies a different object: the inverse of the two
channel columns

\[
                    \binom AF,\qquad\binom BU.                 \tag{14}
\]

It interpolates the two fixed flags \((q,b)\) and \((r,c)\) in the common
\((p,a),(s,d)\) channel.  One of those flags is deleted from each of the
two pair charts, and the resulting forms may have arbitrary components at
all other sites.  Thus this inverse two-flag selector is not a three-site
endpoint selector on either chart and does not establish (13).

## 4. Exact label and inactive-root ledger

Consider one oriented active line

\[
                         K(z)=E_{ae}+zI,
 \qquad \alpha=A_{xy}(a,e)\ne0,
 \qquad \tau=\operatorname {tr}A_{xy}.                         \tag{15}
\]

Its scalar-zero point in projective notation is

\[
                         K_*=\tau E_{ae}-\alpha I.             \tag{16}
\]

The packet classification below is the specialization of the
[inactive-root export ledger](curved-cap-inactive-root-export-and-osculating-ledger.md)
to this line.

If \(a\ne e\), all target coefficients on the affine line equal \(z\).
Hence every inactive clean root is one of:

1. \(E_{ae}\), where the direct scalar is \(\alpha\ne0\), the target is
   zero, and cleanliness exports an exact matching-base-locus quadratic;
2. \(K_*\), where the scalar is zero and the target is
   \(-\alpha(X_0+X_1+X_2)\), so cleanliness exports the nonzero ternary
   nilpotent response packet
   \[
        r_*q^{[h-1]}=-\alpha\Delta_{2h,3},\qquad r_*^{[h]}=0.
                                                                    \tag{17}
   \]

There is no unary point and no binary complementary point on this
projective line.  An off-diagonal rootless scalar-zero packet therefore
cannot be relabelled into the diagonal Omega packet while preserving the
fixed GHZ labels.

If \(a=e\), the colour-boundary points are

\[
                         E_{aa},\qquad E_{aa}-I.                \tag{18}
\]

At \(E_{aa}\), the direct scalar is \(\alpha\ne0\), and a clean point
exports an exact unary source.  At \(E_{aa}-I\), the direct scalar is
\(\alpha-\tau\).  Thus a clean point there exports an exact binary source
when \(\tau\ne\alpha\), while for

\[
                              \tau=\alpha                       \tag{19}
\]

it is the scalar-zero binary nilpotent packet.  When (19) fails, the
separate scalar-zero point (16) has all three target coefficients nonzero
and gives a ternary nilpotent packet if it is clean.

It follows that the diagonal unary--complementary Omega routing assumed
in the conditional overlap lemma requires, on each chart, all three of

\[
 a=e,\qquad \tau=\alpha,\qquad
 {\cal E}(E_{aa})={\cal E}(E_{aa}-I)=0.                         \tag{20}
\]

None of these three assertions follows from nonzero curvature.  The first
is a fixed-label condition, the second is a trace equation, and the third
is a pair of clean-root equations.  Even in the all-inactive-root branch,
the gcd need only be supported on the activity divisor; it need not vanish
at every point of that divisor.  This is the exact joint-routing gap.

The omitted trace-only calculation is as follows.  If \(\alpha=0\) and
\(\tau\ne0\), then \(s(u,v)=\tau v\).  Off diagonal, \(E_{ae}\) is the
sole inactive point and both its scalar and target row vanish.  On the
diagonal, \(E_{aa}\) is scalar-zero with unary target, whereas
\(E_{aa}-I\) has nonzero scalar and binary target.  These roles are the
reverse of the desired Omega orientation.  If also \(\tau=0\), the line
is nowhere active.

## 5. A literal source-block guard for the two nonautomatic incidences

There is a small source-provenant guard showing that neither second-chart
activity nor fixed-colour selector alignment follows from the curvature
minor, goodness, disjoint ordinary selectors, and the universal overlap
identities alone.

Use sites \(p,q,r,s,t,u,v,w\), physical colour bases \(0,1,2\), and select

\[
                         a=b=c=d=0.                             \tag{21}
\]

Let

\[
 A_{pq}=I_3,\qquad A_{pr}=0,\qquad A_{qr}=I_3,\qquad
 A_{rs}=I_3,\qquad A_{qs}=P,
 \quad
 P=\begin{pmatrix}0&1&0\\0&0&1\\1&0&0\end{pmatrix}.         \tag{22}
\]

Choose all blocks from each of \(p,q,r\) to the auxiliary sites
\(t,u,v,w\) to be \(I_3\), and take any other unlisted blocks to be zero
(additional identity blocks may be added without changing the argument).
Then

\[
                  A=1,\quad B=0,\quad F=0,\quad U=1,
 \qquad AU-BF=1.                                               \tag{23}
\]

Both \(pq\) and \(pr\) are good: each of their four endpoint stars sees
an invertible block away from the deleted pair.  In fact their local row
spaces are full at enough auxiliary sites that the two endpoint Rado
matroids on either chart have disjoint bases.  For example, on the
\(pq\)-residual use \(\{t,u,v\}\) for the \(p\)-star and
\(\{r,s,w\}\) for the \(q\)-star; on the \(pr\)-residual use
\(\{q,t,u\}\) for the \(p\)-star and \(\{s,v,w\}\) for the \(r\)-star.
Nevertheless

\[
        s_{pq}(u,v)=u+3v,\qquad s_{pr}(u,v)=0,                  \tag{24}
\]

so the second canonical line is nowhere active.

The same guard also separates ordinary and fixed-colour selectors.  On
the identity-block auxiliary sites, a fixed physical colour \(c\) pulls
back to the same endpoint row \(e_c^*\) at every site.  The one permutation
block can enlarge that fixed-colour span by at most one.  Hence no
fixed-colour family has rank three, although the unrestricted local row
space at each identity-block site is all of \((\mathbb C^3)^*\), so
ordinary disjoint selector bases are abundant.

All power-free Bianchi and full-matrix overlap formulas hold literally,
because (22) is an actual collection of physical source blocks.  The
selected minor is entirely diagonal, so (1) also does not force an
off-diagonal label.

This guard is not an exact ternary GHZ source and therefore does not show
that the remaining eight target rows can coexist with (24).  Its exact
scope is the needed one: no deduction from the selected minor, goodness,
ordinary selector incidence, or universal source overlap can establish
second-chart activity, off-diagonal selection, or fixed-colour selector
alignment.  Any such deduction must use additional literal full-nine
target coefficients.  No existing theorem makes that deduction.

## 6. Corrected conditional target

For an arbitrary curvature-selected source, the proposed two-chart
saturation theorem may therefore be stated with a shorter and more honest
hypothesis ledger:

* retain the automatic joint packet of Theorem 1.1 without listing its
  full-nine, anchor, good-star, and overlap components as extra extraction
  assumptions;
* assume only (3) if the proof genuinely localizes both charts at
  activity;
* in a rootless chart, use the automatic individual selectors and split
  disjoint-base failure immediately into the audited maximal shores;
* state separately any fixed-colour, separation, or own-edge incidence
  needed beyond those selectors; and
* in an inactive-root chart, use the universal boundary list in Section 4
  unless the three diagonal Omega-routing conditions (20) have actually
  been proved.

Thus the joint-extraction gap is not “all hypotheses at once.”  It is the
much smaller conjunction of second-chart activity and branch-specific
compatibility/routing.  The distinction \(a=b\) versus \(a\ne b\) belongs
to the scalar-zero target and that routing, not to the already completed
ordinary-selector or source-overlap extraction.
