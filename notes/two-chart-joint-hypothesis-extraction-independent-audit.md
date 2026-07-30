# Independent audit: automatic two-chart hypothesis extraction

## Verdict

**PASS WITH ONE SCOPE CORRECTION.**  Conditional on the selected physical
minor from
[the unconditional curvature theorem](unconditional-curvature-line-selection.md),
the automatic packet in
[the extraction note](two-chart-joint-hypothesis-extraction.md) is correct.
Goodness gives four deleted-star injections; both full-nine systems retain
the common physical labels; the all-label overlap and shared four-cut data
are literal source identities; the activity criterion is exact; and a
rootless chart has individual three-site selectors even when its selected
cell is diagonal.

The correction is a scope completion.  The second chart may be generically
active with selected entry \(B=0\) and nonzero trace.  The original
inactive-boundary discussion assumed a nonzero selected entry, so it did
not cover this trace-only case.  The source note now records that separate
ledger.  This does not change the exact conditions for the desired
diagonal unary--complementary Omega packet.

## 1. Goodness and physical-label full-nine transport

The curvature theorem selects two **good pairs** \(pq\) and \(pr\).
Goodness of a pair means injectivity of both deleted endpoint-star maps,
so the four claimed injections are immediate.

For either physical pair \(xy\), extraction at endpoint colours gives

\[
 a^{xy}_{ij}q_{xy}^{[h]}+p_i s_jq_{xy}^{[h-1]}
       =\delta_{ij}X_i .
\]

Since \(q q^{[h-1]}=h q^{[h]}\), this is exactly

\[
 \left(p_i s_j+{a^{xy}_{ij}\over h}q_{xy}\right)
 q_{xy}^{[h-1]}=\delta_{ij}X_i .
\]

Thus all nine rows occur on both charts.  No row operation or colour-basis
change is used: the three diagonal rows are literally the global physical
labels \(0,1,2\).  Swapping \(q,r\) to make \(A\ne0\) also swaps
\(b,c\) and \(F,U\), changing the sign of the minor but not independently
relabeling either chart.

## 2. All-label overlap packet

For every fixed label quadruple \((i,j,k,l)\), direct expansion gives

\[
 f_{ij}t_k-g_{ik}y_j=(A_{ij}t_k-B_{ik}y_j)z
\]

and

\[
 U_{kl}f_{ij}+t_kH_{ij;l}-F_{jl}g_{ik}-y_jN_{ik;l}
 =(A_{ij}t_k-B_{ik}y_j)v_l
 +(A_{ij}U_{kl}-B_{ik}F_{jl})z .
\]

The product terms cancel pairwise.  The two chart expansions also share
literally

\[
 L=A_{ij}t_k+B_{ik}y_j+C_{jk}x_i,\qquad
 M=A_{ij}U_{kl}+B_{ik}F_{jl}+E_{il}C_{jk}.
\]

These identities precede multiplication by a divided power and hold for
all physical labels, including the diagonal-anchor labels and zero
entries.  At the selected labels the final coefficient is
\(AU-BF\ne0\).  There is no hidden chartwise normalization or label
transport in this step.

## 3. Exact activity calculation

On \(K(u,v)=uE_{ae}+vI\),

\[
 s(u,v)=\alpha u+\tau v,\qquad
 \kappa_i(u,v)=u\delta_{ia}\delta_{ie}+v .
\]

The target-coordinate product is \(v^3\) off diagonal and
\((u+v)v^2\) on the diagonal, hence is never the zero polynomial.
Generic activity is therefore equivalent to
\((\alpha,\tau)\ne(0,0)\).  The minor forces \((A,B)\ne(0,0)\);
after swapping \(q,r\), \(A\ne0\), so the first chart is active.  The
second chart is active exactly when

\[
                    (B,\operatorname{tr}A_{pr})\ne(0,0).
\]

In particular, \(B=0\), \(\operatorname{tr}A_{pr}\ne0\) is a genuine
trace-only active case, not part of the \(\alpha\ne0\) ledger.

## 4. Rootless selectors, including \(a=e\)

At a scalar-zero point, the uniform clean-error identity reads
\(\mathcal E(K)=r(K)^{[h]}\).  If the direct scalar is identically zero,
the same formula holds at every point.  Rootlessness therefore supplies
some (indeed every applicable) \(K\) with

\[
                         r(K)^{[h]}\ne0.
\]

The complete nine rows and endpoint injectivity imply

\[
 \operatorname{rank}P_{\bar x},\operatorname{rank}S_{\bar x}\ge2
 \quad\text{for every residual site }x
\]

by the uniform full-nine exceptional-shore theorem.  This excludes the
rank-at-most-one-away-from-one-site Rado failure.  Support of an endpoint
star on at most two sites would make the \(h\)-edge power
\(r(K)^{[h]}\) zero for \(h\ge3\), excluding the other sparse failure.
Both endpoints thus have individual three-site selectors.

This proof never uses \(a\ne e\), invertibility of \(K\), or a ternary
target.  In the diagonal trace case \(K=\alpha(E_{aa}-I)\) is rank two
with binary target, but the argument is unchanged.  If the two resulting
rank-three Rado matroids lack disjoint bases, the maximal-shore theorem
classifies the failure as common-coloop, line-plus-plane, rank-\((1,1)\),
or one of the endpoint-dark shores.  This is a routing statement, not a
claim that those gates are closed.

## 5. Inactive and Omega routing

Assume first \(\alpha\ne0\).  Off diagonal, the inactive divisor consists
of \(E_{ae}\) and the distinct scalar-zero point

\[
                         K_*=\tau E_{ae}-\alpha I.
\]

The latter is automatically invertible and has ternary target
\(-\alpha(X_0+X_1+X_2)\).  No fixed-label unary--complementary pencil can
be renamed into existence.

On the diagonal, the colour-boundary points are \(E_{aa}\) and
\(E_{aa}-I\), with direct scalars \(\alpha\) and \(\alpha-\tau\).
Consequently the precise Omega packet in the conditional lemma requires

\[
 a=e,\qquad \tau=\alpha,\qquad
 \mathcal E(E_{aa})=\mathcal E(E_{aa}-I)=0 ,
\]

together with the standing \(\alpha\ne0\).  These give a clean unary
nonzero-scalar endpoint, a clean complementary scalar-zero binary
nilpotent endpoint, and activity away from the two endpoints.  Curvature
implies none of the label, trace, or cleanliness equations.

For the trace-only case \(\alpha=0,\tau\ne0\), \(s=\tau v\).
Off diagonal, \(E_{ae}\) is the sole inactive point and both its scalar
and target vanish.  On the diagonal, \(E_{aa}\) is scalar-zero with unary
target while \(E_{aa}-I\) has nonzero scalar with binary target.  The
roles are opposite to the desired Omega orientation, so this case cannot
be silently passed through item 4 of the conditional lemma.

## 6. Literal block guard

The Section 5 guard checks at its deliberately non-GHZ scope.  At the
selected zero labels,

\[
 A=1,\quad B=0,\quad F=P_{00}=0,\quad U=1,\quad AU-BF=1.
\]

The auxiliary identity blocks make both deleted stars of \(pq\) and
\(pr\) injective.  The displayed triples are disjoint Rado bases:
\(\{t,u,v\}\), \(\{r,s,w\}\) for \(pq\), and
\(\{q,t,u\}\), \(\{s,v,w\}\) for \(pr\).  Nevertheless

\[
 s_{pq}=u+3v,\qquad s_{pr}=0 .
\]

For any fixed physical colour, identity blocks pull back to one endpoint
row; the one cyclic permutation block adds at most one other row.  Thus
every fixed-colour family has rank at most two although ordinary selectors
are abundant.  As these are actual physical blocks, every power-free
overlap and shared \((L,M)\) formula holds identically.

The guard is not an exact ternary GHZ source and does not satisfy the two
full-nine systems.  It proves only that the minor, goodness, ordinary
selector incidence, and universal block identities do not by themselves
force second-chart activity or fixed-colour alignment.  It does not prove
independence from the full automatic packet; the source note states this
limitation correctly.

## Final ledger and board effect

The proposed lemma may drop as separate hypotheses: both pair-goodness
conditions/four injections, both physical-label full-nine systems and
their diagonal rows, all-label overlap and shared four-cut data,
first-chart activity, and individual rootless endpoint selectors.

Still live are: second-chart activity; disjoint, separated, fixed-colour,
or own-edge compatibility; and branch-specific inactive routing.  The
trace-only second-chart ledger is a distinct subcase.  No audited identity
automatically upgrades any of these remaining items.
