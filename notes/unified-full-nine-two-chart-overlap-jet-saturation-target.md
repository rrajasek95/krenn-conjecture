# Unified full-nine two-chart overlap--jet saturation target

Research target only.  The theorem stated below is open,
**SP-CLEAN-BRIDGE** remains open, and no certified dependency is changed.

## 1. Outcome

The current main line has one theorem-shaped target.  Start with the
maximum-anchor, then minimum-support exact source selected by the
[anchor--curvature synchronization theorem](anchor-lexicographic-curvature-synchronization.md).
One nonzero physical curvature minor gives an active \(pq\)-chart and the
automatic source-faithful \(pr\)-overlap packet.  The
[tilted second-chart theorem](tilted-second-chart-activity-and-zero-block-boundary.md)
then gives exactly one of:

1. an active canonical or explicitly tilted \(pr\)-chart; or
2. the intrinsic direct-free \(pr\)-auxiliary, which is nowhere active but
   retains its triangular full-nine and overlap rows.

The proposed theorem says that these data force an active clean cap on at
least one genuinely active chart.  It assumes no disjoint selector bases,
fixed-colour selector, diagonal unary--complementary routing, cofactor
kernel, common-coloop factorization, or source-saturation statement.  Those
are possible outputs or local proof obligations, not hypotheses.

This formulation unifies the two values of the clean-coordinate gcd, the
two assignments in the mixed two-chart case, the disjoint-base split, and
all four maximal-shore gates.  Sections 5 and 6 separate the four genuinely
missing components from the already formal implication to
**SP-CLEAN-BRIDGE**.

The calibration in
[the eight-vertex bridge note](clean-bridge-at-eight-is-the-open-case.md)
is essential: at \(N=8\), **SP-CLEAN-BRIDGE** is equivalent to emptiness of
the exact ternary source locus.  The unified theorem is therefore the
shortest organized full-proof target, not a logically weaker shortcut.
The \(h=3\) response-grade split is a bounded structure and falsification
gate for the uniform theorem.  A standalone inactive clean landing does
not satisfy the active-clean hypothesis and does not finish the bridge.

## 2. The automatic physical packet

Let \(|B_0|=2m\geq8\), put \(h=m-1\), and let \(A\) be the synchronized
maximum-anchor, then minimum-support solution of

\[
                         H_{B_0}(A)=\Delta_{B_0,3}.             \tag{1}
\]

The synchronization and curvature theorems supply distinct sites
\(p,q,r,s\), physical colours \(a,b,c,d\), and entries

\[
\begin{aligned}
 A_0&=A_{pq}(a,b)\ne0,& R_0&=A_{pr}(a,c),\\
 F_0&=A_{qs}(b,d),& U_0&=A_{rs}(c,d),
\end{aligned}
\qquad
                 \kappa=A_0U_0-R_0F_0\ne0 .                  \tag{2}
\]

For a pair \(xy\), write \(q_{xy}\) for the internal quadratic, \(p_i,s_j\)
for its endpoint-star rows, and \(a^{xy}_{ij}=A_{xy}(i,j)\).  The
[automatic two-chart extraction theorem](two-chart-joint-hypothesis-extraction.md)
gives, simultaneously on \(pq\) and \(pr\), the literal equations

\[
 a^{xy}_{ij}q_{xy}^{[h]}+p_i s_jq_{xy}^{[h-1]}
       =\delta_{ij}X_i,
 \qquad 0\leq i,j\leq2,                                    \tag{3}
\]

or, with

\[
 B^{xy}_{ij}=p_i s_j+{a^{xy}_{ij}\over h}q_{xy},
 \qquad
 B^{xy}_{ij}q_{xy}^{[h-1]}=\delta_{ij}X_i.                  \tag{4}
\]

The physical labels in the two systems are the same.  In particular, (4)
contains the same three differently labelled diagonal anchors on both
charts.  The same automatic packet contains all fixed-label coefficients of
the power-free connection and normal row.  On the common complement of
\(p,q,r,s\), using the notation of the extraction theorem, these include

\[
\begin{aligned}
 f_{ij}t_k-g_{ik}y_j
   &=(A_{ij}t_k-B_{ik}y_j)z,\\
 U_{kl}f_{ij}+t_kH_{ij;l}-F_{jl}g_{ik}-y_jN_{ik;l}
   &=(A_{ij}t_k-B_{ik}y_j)v_l
     +(A_{ij}U_{kl}-B_{ik}F_{jl})z .                         \tag{5}
\end{aligned}
\]

At the selected labels the last coefficient is \(\kappa\).  The shared
\((L,M)\) four-cut packet consists of other literal coefficients of the
same source identities.  Nothing in (3)--(5) is obtained by independently
normalizing or relabelling the charts.

The first physical line is

\[
                 K_{pq}(u,v)=uE_{ab}+vI.                     \tag{6}
\]

It is generically active.  Put \(R=A_{pr}\).  The proved second-direction
rule is

\[
 J_{pr}=\begin{cases}
 I,&(R_0,\operatorname {tr}R)\ne(0,0),\\
 I+E_{ij},&R\ne0,\ R_0=\operatorname {tr}R=0,\ R_{ij}\ne0.
 \end{cases}                                                 \tag{7}
\]

In either case

\[
                 K_{pr}(u,v)=uE_{ac}+vJ_{pr}                 \tag{8}
\]

is generically active.  If \(R=0\), no \(pr\)-cap line is active.  The
same source nevertheless retains

\[
 p_it_kq_{pr}^{[h-1]}=\delta_{ik}X_i,
 \qquad D=A_0t,
 \qquad
 C_4=U_0f+tH-F_0g-yN=A_0tv+A_0U_0z,                        \tag{9}
\]

and the full-label versions of its triangular overlap rows.  Equations
(3)--(9) are the entire hypothesis packet of the proposed theorem.

## 3. The literal clean, rootless, and boundary modules

### 3.1 Clean ideals and activity localization

Let \({\cal A}\) be the set of genuinely active charts: it always contains
\(pq\), and contains \(pr\) exactly when \(R\ne0\).  For
\(\nu\in{\cal A}\), let

\[
 {\cal E}_\nu(u,v)\in{\cal V}_\nu\otimes S_h,
 \qquad S=\mathbb C[u,v],                                   \tag{10}
\]

be the homogeneous clean error of the physical cap line (6) or (8).  Let
\(L_\nu\subseteq S_h\) be its scalar coordinate span and put

\[
 I_\nu=(L_\nu)\subseteq S,
 \qquad
 a_\nu=s_\nu\kappa_{\nu,0}\kappa_{\nu,1}\kappa_{\nu,2}.
                                                                    \tag{11}
\]

Here \(a_\nu\) is the literal activity polynomial: a point is active
exactly when \(a_\nu\ne0\).  Since all clean coordinates are binary forms
of one degree, the common-divisor criterion gives

\[
 \begin{split}
 \text{\(K_\nu([u:v])\) is active and clean for some \([u:v]\)}
 \quad\Longleftrightarrow\quad
                   (I_\nu:a_\nu^\infty)\ne S .               \tag{12}
 \end{split}
\]

The inactive direct-free auxiliary (9) is not inserted into (12) with the
formal value \(a_{pr}=0\); that would be a vacuous saturation.  It enters
only through its literal source rows.

### 3.2 The rootless residual Macaulay module

Suppose \(\gcd L_\nu=1\).  At any prescribed point, in particular the
direct-scalar-zero point when it exists, rootlessness permits an
\(f_\nu\in L_\nu\) which does not vanish there.  Choose a vector-space
complement

\[
                  L_\nu=\mathbb C f_\nu\oplus L_\nu'.         \tag{13}
\]

The existing residual module and multiplication map are

\[
 Q_{\nu,f}=S_{2h-1}/f_\nu S_{h-1},
 \qquad
 \mu_{\nu,f}:L_\nu'\otimes S_{h-1}\longrightarrow Q_{\nu,f}.
                                                                    \tag{14}
\]

The [residual Macaulay theorem](residual-macaulay-quotient-is-the-common-divisor.md)
proves

\[
 \dim Q_{\nu,f}=h,
 \qquad
 \operatorname {rank}\mu_{\nu,f}
   =h-\deg\gcd(f_\nu,L_\nu').                               \tag{15}
\]

Thus rootlessness makes (14) surjective.  A source-provenant construction
of

\[
 0\ne\lambda_\nu\in Q_{\nu,f}^*,
 \qquad
 \lambda_\nu\circ\mu_{\nu,f}=0                              \tag{16}
\]

is already a contradiction.  The quotient in (14), rather than an
abstract tensor rank loss, is the required rootless output module.

### 3.3 The inactive-root boundary modules

If \(\gcd L_\nu\ne1\) but (12) fails, every common root lies on the literal
activity divisor \(V(a_\nu)\).  The
[exact inactive-root ledger](two-chart-joint-hypothesis-extraction.md#4-exact-label-and-inactive-root-ledger)
separates the off-diagonal, diagonal, and trace-only physical boundaries;
it does not identify them by a colour change.

On a diagonal unary--complementary line for which both endpoints are
actually clean, the already proved factorization is

\[
             {\cal E}_\nu(t,u)=tu\,\Omega_\nu(t,u),
 \qquad \deg\Omega_\nu=h-2.                                 \tag{17}
\]

Writing \(I_{\Omega_\nu}\) for the ideal of scalar coordinates, the
[uniform residue--Omega theorem](uniform-residue-omega-boundary-syzygy.md)
proves the exact no-active-root certificate

\[
 V(\Omega_\nu)\cap D(tu)=\varnothing
 \quad\Longleftrightarrow\quad
             (tu)^{h-2}\in I_{\Omega_\nu}.                  \tag{18}
\]

For two source-provenant charts in that same diagonal normalization, the
same theorem transports through the power-free overlap the canonical
odd-site quotient

\[
 C_{q_0}={{\cal R}_{2h-1}(K)\over{\cal R}_1(K)q_0^{[h-1]}}
                                                                    \tag{19}
\]

and its boundary-polar defect.  On a diagonal third boundary the literal
lifting question is instead expressed by the existing filtered source
module \(M_\nu\), literal boundary submodule \(N_\nu\), evaluation
\(\epsilon_\nu:M_\nu\to V_\nu\), and actual cap family
\({\mathscr U}_\nu\subseteq M_\nu\otimes S\).  For a boundary factor
\(\ell\) of multiplicity \(r\), the
[diagonal Rees criterion](diagonal-rees-saturation-cap-jet-bockstein.md)
is

\[
 \epsilon_\nu^{-1}\!\bigl(\ell^r(V_\nu\otimes S)\bigr)
       \cap{\mathscr U}_\nu
 =\bigl(N_\nu\otimes S+\ell^r(M_\nu\otimes S)\bigr)
       \cap{\mathscr U}_\nu .                               \tag{20}
\]

Equation (20) is proved as a necessary-and-sufficient lifting criterion,
not as a membership theorem for the current source.  The off-diagonal
base-locus/scalar-zero packet has its own literal adjacent-power source
syzygy and the same quotient (19); it is not silently replaced by (17).
The modules (18)--(20) are the exact inactive-root output ledgers.

## 4. Proposed unified theorem

> **Unified tilted/one-sided full-nine two-chart overlap--jet saturation
> theorem (open).**  For every synchronized exact source (1), form the
> automatic packet (2)--(5), the active \(pq\)-chart (6), and the proved
> tilted/direct-free \(pr\)-alternative (7)--(9).  With \({\cal A}\),
> \(I_\nu\), and \(a_\nu\) as in (10)--(11),
>
> \[
>          \boxed{\text{there exists }\nu\in{\cal A}
>          \text{ such that }(I_\nu:a_\nu^\infty)\ne S.}    \tag{21}
> \]
>
> The assertion remains valid when the two active charts have different
> gcd ledgers, when either pair of endpoint selector matroids has or lacks
> disjoint bases, and when a no-disjoint-bases chart lies on any of the
> four maximal-shore gates.  If \(R=0\), (21) means the one-sided
> \(pq\)-conclusion, with (9) used only as a source-faithful auxiliary.

The statement deliberately has no conditional fixed-label incidence and
no assumed diagonal Omega packet.  A proof may derive those configurations,
but must also treat their failure using the same literal full-nine packet.
The theorem is uniform in \(h\ge3\); an \(h=3\) two-column or grade-split
calculation is only a bounded test of (21), not a proof and not a separate
landing theorem.

Concretely, on the first off-diagonal boundary put

\[
                   Q_j=R^{[j]}q^{[3-j]}\qquad(0\le j\le3).
\]

The admitted endpoint row is \(\alpha Q_0+Q_1=0\), while the required
reciprocal clean coefficient is
\(\operatorname {coeff}_{c^6}(\alpha Q_2+Q_3)=0\).  This grade
split is a sharp test for a proposed cross-chart operation: it must
transport the first relation to the second with the physical target
retained.  Neither the identity by itself nor a clean point on the
activity boundary proves (21).

## 5. The four genuinely missing components

These are proof components of (21), not four independent conjecture-level
targets.

### Component I: tilted or one-sided source overlap

Extend the canonical power-free connection (5), its normal row, and the
shared \((L,M)\) packet to the actual direction \(J_{pr}\) in (7).  When
\(R=0\), use the triangular rows (9) to obtain the corresponding one-sided
map into the \(pq\)-ledger.  The map must exist before multiplication by a
common divided power, preserve all physical labels and the selected
curvature coefficient, and retain at least one diagonal target row in the
eventual quotient.  The tilt theorem proves activity and preserves
curvature; it does not prove this source-module transport.

### Component II: complete-anchor incidence or maximal-shore conversion

Use the three diagonal rows in (4), a crossed target-zero row, and the
literal four-cut coefficient in (5) to make the endpoint
wedge/direct-form alignments incompatible with \(\kappa\ne0\), or convert
their failure into a source-visible maximal shore.  On a rootless chart,
ordinary three-site selectors are automatic, but fixed-label, separated,
and own-edge compatibility are not.

On the no-disjoint-bases side, this same component must close the bounded
normal forms already isolated by the shore notes:

* the common-coloop curvature rectangle and its common
  \(q_0^{[h-2]}\)-factorization;
* the line--plus--plane coordinate-gate cofactor conic, including its
  tangent, nonsquare/inactive-kernel, and injective normal forms;
* the rank-\((1,1)\) coordinate quadratic/cubic line and scalar-gate
  adjacent-power comparison; and
* the endpoint-dark one-bright kernel/target separation.

Closing these as consequences of the transported full-nine overlap avoids
promoting four local normal forms to four top-level theorems.

### Component III: rootless Macaulay annihilation with provenance

On at least one rootless chart, construct the functional (16) from the
transported diagonal anchors, crossed row, curvature-normal class, and
selector-compatible cut supplied by Component II.  On the singular
six-site scalar base, the construction must also kill the relevant Hessian
kernel.  On every base it must annihilate the filtered selector-family
provenance class before the common power is applied.  Abstract
Macaulay/Lefschetz surjectivity, a same-orientation cycle sum, or a scalar
match on one cap does not produce (16).

By (15), this component immediately contradicts the rootless ledger.  It
must cover the disjoint-base case directly; the no-disjoint-bases case may
reach it after Component II closes or converts the shore packet.

### Component IV: inactive-boundary and mixed-ledger exactness

Use the actual off-diagonal, diagonal, or trace-only boundary routing to
rule out simultaneous no-active-root certificates.  In the diagonal
case, prove the required memberships in (20) and a source-provenant
adjacent-power target null-homotopy which contradicts (18).  At the trace
collision, carry the unary anchor through its order-\(h\) principal part or
force a visible complementary label.  In the off-diagonal case, perform
the corresponding secondary comparison on the literal scalar-zero
ternary packet rather than renaming it as a diagonal Omega endpoint.

If one active chart is rootless and the other is all-inactive, this
component must couple the bounded certificate (18), or its correct
off-diagonal/trace-only replacement, to the residual functional (16).
Two separate one-chart contradictions are not assumed.  This is the mixed
assignment which a uniform overlap theorem must genuinely handle.

### Recommended construction for Components III--IV (not proved)

The existing
[site-occupancy split](site-occupancy-bockstein-partial-matching-flatness.md)
provides the formal short exact sequence

\[
 0\longrightarrow\mathsf K_x
 \longrightarrow\mathsf P(S)
 \longrightarrow\mathsf P(S\setminus\{x\})
 \longrightarrow0
\]

and its coefficient-exposure sections.  A concrete next construction is to
put cap multiplication and target augmentation into an evaluated
two-chart total differential as a filtration-raising perturbation of the
formal chart-symbol differential, then compute the finite relative
section-defect series.  The first evaluated defect is already known to be
the odd-residue map
\(\Theta\mapsto[\Theta t_cq_0^{[h-2]}]\).  The desired second cross-chart
term should be the curvature-weighted class
\(\kappa\,\operatorname {res}_{q_0}\), with its target coordinate
cancelled in the literal augmented complex.

This is only an architecture.  The occupancy kernel and common chart mode
can carry homology, so the perturbation series has indeterminacy unless the
complete diagonal anchors and crossed row first make the relevant
**relative** kernel contractible.  The required preliminary result is
therefore a contraction or zero-indeterminacy theorem for that anchored
relative module.  Formal statewise splitting alone gives a zero connecting
map, while evaluated one-chart cap multiplication has the nonzero first
defect; neither fact constructs the second operation.  A successful
construction must prove well-definedness before identifying its value with
\(\kappa\) times the residue.

## 6. Why the proposed theorem implies **SP-CLEAN-BRIDGE**

**Proposition 6.1.**  If the theorem in Section 4 holds for every
\(h\ge3\), then **SP-CLEAN-BRIDGE** holds at every even order
\(N=2h+2\ge8\).

**Proof.**  Suppose an exact ternary source exists at order \(N\ge8\).
Choose, among all exact aggregate representatives, one which first
maximizes the number of mutual anchors and then minimizes support.  The
[synchronization theorem](anchor-lexicographic-curvature-synchronization.md)
proves that this same representative has a nonzero physical curvature
transition.  The
[unconditional curvature-line theorem](unconditional-curvature-line-selection.md)
then gives (2) after exchanging \(q,r\) if necessary, and proves that (6)
is generically active.

The automatic extraction theorem supplies (3)--(5) on this same source.
The tilted second-chart theorem supplies (7)--(9), so every hypothesis of
the theorem in Section 4 is now proved.  Equation (21) and (12) give an
active clean cap \(K\) on \(pq\), or on the physical \(pr\)-line when
\(R\ne0\).  In both cases

\[
 s(K)\kappa_0(K)\kappa_1(K)\kappa_2(K)\ne0,
 \qquad {\cal E}(K)=0.                                      \tag{22}
\]

These are exactly the hypotheses of the
[exact clean-pair descent theorem](clean-pair-cap-exact-descent-target.md).
In particular, they are exactly the active-clean conclusion required by
**SP-CLEAN-BRIDGE**.  This proves the proposition.  \(\square\)

The named branch coverage is formal and exhaustive:

1. **Rootless and inactive-root.**  For every active chart, either
   \(\gcd L_\nu=1\), or it has a common projective root.  Under failure of
   (12), every such root is in \(V(a_\nu)\).  These are precisely the
   rootless and all-inactive ledgers.  There is no third gcd case.
2. **Mixed two-chart assignments.**  If \(R\ne0\), the two active charts
   independently have one of those two ledger labels, giving four ordered
   assignments.  Section 4 quantifies over the packet before choosing a
   label, so (21) covers both mixed assignments as well as the two equal
   assignments.  If \(R=0\), the theorem makes only the nonvacuous
   one-sided assertion.
3. **Disjoint bases.**  On a rootless chart, the automatic extraction
   theorem proves that each endpoint star has an ordinary three-site Rado
   selector.  Matroid union says their bases either are disjoint or are
   not.  The proposed theorem assumes neither outcome; Component III is
   the direct disjoint-base output.  Hence the implication above does not
   depend on an unproved fixed-colour or own-edge selector.
4. **Maximal shores.**  When disjoint bases fail, the
   [uniform maximal-shore theorem](uniform-selector-union-maximal-defect-shore.md)
   routes the same full-nine source to the common-coloop,
   line--plus--plane, rank-\((1,1)\), or endpoint-dark gate.  It does not
   replace the source or discard (3)--(5).  Those four gates are therefore
   cases inside Component II, and (21) closes all of them without adding a
   fifth branch to Proposition 6.1.

At \(N=8\), the
[eight-vertex bridge theorem](clean-bridge-at-eight-is-the-open-case.md)
identifies **SP-CLEAN-BRIDGE** with emptiness of the exact ternary source
locus.  Thus Proposition 6.1 does not weaken the first boundary: (21)
would prove that full obstruction.  Its \(h=3\) response-grade identity
can reject candidate overlap maps or expose the missing source class, but
an inactive zero of the clean error is not the conclusion (22).

Once (22) is obtained, the existing exact descent gives an order
\(N-2\) source.  Repeating the synchronized selection after each descent
and using the proved six-site obstruction closes the usual minimal-order
contradiction.  That further consequence uses only the already certified
descent spine; it is not an additional clause of the proposed theorem.

## 7. Dependency and consequence ledger

| Item | Status | Exact role |
|---|---|---|
| Anchor-first representative and curvature synchronization | Proved | Places maximum-anchor extremality and a physical curvature line on the same exact source |
| Unconditional curvature-line theorem | Proved | Supplies \(p,q,r,s\), the nonzero minor \(\kappa\), and the active \(pq\)-line |
| Automatic two-chart packet | Proved | Supplies both full-nine systems, common labels, diagonal anchors, connection, normal row, and shared four-cut data |
| Tilted/direct-free second-chart alternative | Proved | Removes second canonical activity as a hypothesis and gives (7)--(9) |
| Residual Macaulay rank formula | Proved | Turns a source-derived functional (16) into a rootless contradiction |
| Inactive-root routing, Omega certificate, and Rees criterion | Proved as classifications/criteria | Defines the literal boundary modules; does not prove their required incompatibility or memberships |
| Formal site-occupancy split and one-chart section defect | Proved at the stated formal/evaluated scopes | Supplies a candidate perturbative model; does not define the evaluated two-chart Bockstein |
| Uniform maximal-shore classification and latest gate reductions | Audited/research reductions; no bridge claim | Gives exhaustive bounded local normal forms when selector bases are not disjoint |
| Components I--IV | **Open** | Together constitute a proof of the proposed theorem (21) |
| Unified theorem \(\Rightarrow\) active clean cap | Formal by (12) | Gives **SP-CLEAN-BRIDGE** on the selected source |
| Active clean cap \(\Rightarrow N-2\) exact source | Proved | Exact clean-pair descent |
| Repeated descent \(\Rightarrow\) contradiction | Proved conditional on the bridge | Uses re-selection and the certified six-site obstruction |

The branch consequence map is:

| Ledger encountered in a proof | Required literal output | Existing theorem which turns that output into a contradiction |
|---|---|---|
| Rootless, disjoint bases | A functional (16) from the transported anchor/four-cut rows | Residual Macaulay rank formula (15) |
| Rootless, no disjoint bases | Component II closes/converts one of the four maximal shores, then produces (16) or an active clean cap | Maximal-shore classification plus (12) or (15) |
| Inactive--inactive | Failure of the simultaneous bounded boundary certificates in the correct physical routing | Activity localization (12) and the certificate equivalence (18) |
| Rootless--inactive or inactive--rootless | A source-relative coupling of (16) with the applicable boundary module | (15), (18), and the lifting criterion (20) |
| Direct-free \(pr\)-boundary | One-sided transport of a literal diagonal row from (9) into the \(pq\)-ledger | The \(pq\)-instance of (12) or (15) |

## 8. Explicit nonclaims and work allocation

This note does **not** claim any of the following.

* The proposed theorem (21), any of Components I--IV, or
  **SP-CLEAN-BRIDGE** is proved.
* The second canonical chart is always active.  The theorem uses the proved
  tilt, or the direct-free auxiliary without pretending to localize it.
* Every inactive chart has diagonal unary--complementary clean endpoints.
  Off-diagonal and trace-only boundaries remain physically distinct.
* Ordinary Rado selectors are fixed-label, separated, or own-edge
  selectors.
* A vector-valued binary conic has a projective root.  The injective and
  nonsquare-kernel line--plus--plane normal forms are explicitly retained.
* Vanishing after scalar evaluation proves membership in the literal
  boundary module; (20) records precisely the missing source-lifting step.
* Same-power cancellation, multiplication by a common power, or a scalar
  four-cycle match constructs the adjacent-power comparison.
* The maximal-shore gates are separately completed.  They are local test
  cases which a proof of Component II must close with the transported
  overlap.
* An \(h=3\) grade-split calculation, inactive clean landing, level-two
  census, or isolated support obstruction proves the uniform theorem.

Accordingly, the sole primary allocation is Components I--IV as one
overlap theorem.  Further common-coloop strata, isolated cofactor-kernel
enumeration, and level-two/support censuses should be pursued only when
they construct or falsify one of those four literal module maps.
