# Independent audit of the inactive-root full transverse overlap

Audit date: 2026-07-29.

## Verdict

**PASS AFTER CORRECTION.** The revised source preserves the sound
first-boundary algebra: the Omega factorization, its bad-locus
classification, every displayed two-cut divided-power coefficient in
(8)--(12), and the source-level cap jets and connection in (14)--(16) all
check exactly. It now presents these as a conditional \(h=3\), \(8\to6\)
description and no longer advertises an exhaustive inactive-root,
common-coloop, selector, or conjecture-level reduction.

The original draft was missing four bridges; the revision now records each
as an explicit limitation rather than silently using it.

1. The curvature supplied by the uniform selection theorem has arbitrary
   physical colours; it is not automatically the \(0000\) component used in
   (17), nor does selection supply two diagonal charts having both displayed
   clean endpoints.
2. The scalar-zero point in Sections 2--3 is the diagonal binary boundary
   \(E_{00}-I\), whereas the common-coloop formula used in (30) is valid in
   the stated form for an off-diagonal contraction.  These have different
   diagonal target coefficients.
3. The flag-circuit argument proves only a trichotomy involving two
   full-rank **local quotient maps**.  It does not turn them into the two
   overlapping clean curvature charts required by (23).
4. Sections 2--3 are specific to \(h=3\), hence to the first \(8\to6\)
   pair boundary.  No reduction from arbitrary \(h\) to this packet while
   retaining the remaining common power is proved.

The revised residue--Omega assertion is now a precisely conditioned,
strictly stronger intersection lemma: the compatible literal common-coloop
configuration, the identification of its response with a scalar-zero Omega
endpoint, and \(K_{cc}\ne0\) are hypotheses. Equation (23) remains the
separate direct inactive-root target.

## 1. One-chart Omega packet: PASS at \(h=3\)

With the source notation of (1)--(2), polarization gives

\[
\begin{aligned}
 &(\lambda F+\mu R)^{[3]}
       -(\lambda\sigma)^2
          \bigl(\lambda X_0-\mu(X_1+X_2)\bigr)\\
 &\quad=\lambda\mu\left[
       \lambda R\bigl(F^{[2]}-\sigma^2q^{[2]}\bigr)
       +\mu R^{[2]}F\right].
\end{aligned}
\]

The pure endpoint terms vanish by the two clean equations and the target
substitution uses the literal physical equation
\(Rq^{[2]}=-(X_1+X_2)\).  Thus (3)--(5) have the displayed normalization.

On the line from \(E_{00}\) to \(E_{00}-I\), the direct scalar and three
target coordinates are proportional to

\[
                 \lambda,\qquad (\lambda,-\mu,-\mu).
\]

Consequently activity is exactly \(\lambda\mu\ne0\).  For a two-column
map, absence of a kernel vector in \((\mathbb C^*)^2\) is exactly the
listed alternative: independent columns, or rank one with exactly one
zero column.  Dependent nonzero columns have a relation with both
coefficients nonzero, and two zero columns make the whole pencil clean.
Hence (6) is correct in this diagonal first-boundary normalization.

## 2. Two-cut coefficients and cap connection: PASS

In the two-exposed-site quotient, direct expansion gives

\[
\begin{aligned}
[e_re_s]q^{[2]}&=Uz+tv,&
[e_re_s]q^{[3]}&=Uz^{[2]}+tvz,\\
[e_re_s]R^{[3]}&=\gamma\rho^{[2]}+\alpha\beta\rho,&
[e_re_s]R^{[2]}F
 &=M\rho^{[2]}+(L\beta+H\alpha+f\gamma)\rho+f\alpha\beta.
\end{aligned}
\]

Multiplication by the remaining interior, one-star, and direct terms then
gives exactly both formulas in (8), both formulas in (9), all four rows of
(11), and the two Omega coefficients in (12).  There is no missing factor
of two.  Because a degree-six tensor on the six residual sites uses every
site once, collecting every two-site colour cut is injective, so (12a) is
also valid at \(h=3\).

An independent exact-rational check evaluated all seven relevant
coefficients in 100 deterministic assignments in the truncated algebra

\[
 \mathbb Q[e_r,e_s]/(e_r^2,e_s^2)
\]

and obtained equality in every trial.  This was a small in-memory check and
introduced no dependency or repository script.

The jets in (14)--(15) also expand literally.  Writing the indices only
implicitly, cancellation leaves

\[
\begin{aligned}
(Az+xy)t-(Bz+xt)y&=(At-By)z,\\
U(Az+xy)+t(Av+Ey+Fx)-F(Bz+xt)-y(Bv+Et+Ux)
 &= (At-By)v+(AU-BF)z.
\end{aligned}
\]

This proves (16).  The trace identities (18)--(19) are correct under their
explicit scalar-zero hypotheses \(A_{11}+A_{22}=0\) and
\(B_{11}+B_{22}=0\).  In particular, the linear connection transports its
residue; it supplies no vanishing equation.  Section 7 correctly says so.

## 3. Curvature and simultaneous endpoints: PASS AFTER CORRECTION

The uniform curvature selection theorem produces colours \(a,b,c,d\) with

\[
 A_{pq}(a,b)A_{rs}(c,d)-A_{pr}(a,c)A_{qs}(b,d)\ne0.
\]

Equation (17) instead assumes

\[
 A_{pq}(0,0)A_{rs}(0,0)-A_{pr}(0,0)A_{qs}(0,0)\ne0.
\]

These are not equivalent by a harmless normalization.  The fixed pure
targets tie the colour labels across all sites, so the four exposed indices
cannot in general be relabelled independently.  Moreover, a unary coordinate
endpoint in the \(pq\)-chart forces its coordinate cap to be diagonal, and a
unary coordinate endpoint in the overlapping \(pr\)-chart imposes another
diagonal condition.  Neither follows from an arbitrary selected curvature
minor.

The revised source now states (17) and the simultaneous clean endpoints as
extra hypotheses of the bounded two-chart lemma. It explicitly says they
are not consequences of the currently proved curvature-line selection.
With those hypotheses, (21)--(24) are a precise statement of an open
conditional implication, not an exhaustive output of the existing proof
spine.

## 4. Residue normalization: PASS AFTER CORRECTION

The canonical cap and flat transport formulas in (28)--(29) are correct at
\(h=3\).  Indeed,

\[
 {\cal P}_{pq}^{ij}=3P_iS_j+A_{ij}q
      =3{\mathfrak f}_{ij}-2A_{ij}q,
\]

and the added \(q_0\)-term has zero residue because
\(t_cq_0q_0=2t_cq_0^{[2]}\) lies in the quotient denominator.  The physical
cap row gives the factor \(3\), and the power-free connection carries the
same residue class to the adjacent cap.

For a general scalar-zero contraction \(K\), however, the correct formula
is

\[
 \operatorname {res}_{q_0}(\overline R_K;t_c)
      =K_{cc}\,\overline Y_c.                         \tag{A1}
\]

For

\[
 K_*=\tau E_{ab}-\alpha I
\]

this becomes

\[
 \operatorname {res}_{q_0}(\overline R_*;t_c)
   =\bigl(\tau\delta_{a,c}\delta_{b,c}-\alpha\bigr)
       \overline Y_c.                                  \tag{A2}
\]

The original source formula (30), \(-\alpha\overline Y_c\) for every \(c\), was
therefore valid when \(a\ne b\), as explicitly assumed in the audited
common-coloop residue note.  It is not valid for the diagonal boundary used
in Sections 2--3.  At the binary scalar-zero point \(E_{00}-I\), after the
corresponding scalar normalization, (A2) reads

\[
 \operatorname {res}(\overline R_*;t_0)=0,
 \qquad
 \operatorname {res}(\overline R_*;t_1)=-\alpha\overline Y_1,
 \qquad
 \operatorname {res}(\overline R_*;t_2)=-\alpha\overline Y_2.
\]

This is exactly the binary target pattern.  Hence (30)--(31) only contradict
a surviving corner whose label has a nonzero diagonal coefficient in the
chosen scalar-zero contraction.  A colour-zero corner is invisible to this
diagonal complementary endpoint.  Conversely, the off-diagonal \(K_*\)
used by the common-coloop theorem sees all three colours, but it is not the
binary endpoint for which Sections 2--3 prove activity
\(\lambda\mu\ne0\) and the two-column bad-locus classification.

This is a substantive compatibility gap, not a scalar typo. The revised
source now uses (A1) as (30), gives the diagonal coefficient of
\(\tau E_{ab}-\alpha I\), distinguishes the off-diagonal common-coloop row
from the diagonal binary Omega endpoint, and conditions (31) on
\(K_{tt}\ne0\).

## 5. Conditioned residue--Omega incidence: PASS AFTER CORRECTION

There is an important positive point: the note does **not** infer residue
vanishing from the linear connection.  Equations (29) and (31) show the
opposite, so any vanishing theorem must use nonlinear second-polar data.
The conditioned lemma also simultaneously retains the pieces separately
deleted by the three cited guards: literal consecutive powers, diagonal
targets, off-diagonal rows, and the bad Omega equations.  In that sense it
is genuinely new rather than a disguised reuse of a refuted implication.

The revised statement introduces every residue object in its hypotheses:
one literal \(h=3\) source must satisfy both the Section 6 chart hypotheses
and the specified common-coloop singleton-corner hypotheses; the response
contraction must be a scalar-zero Omega endpoint; and the surviving label
must satisfy \(\overline Y_c\ne0\) and \(K_{cc}\ne0\). Its conclusion is
therefore defined and (30) would contradict it.

Calling the assertion "matrix-cap exactness" or "faithfulness" does not
by itself define a nonlinear complex, so the revision no longer presents
that terminology as an established equivalence. The precise direct target
for the conditional inactive-root problem remains (23). The residue
statement is explicitly described as a strictly stronger, unproved
intersection lemma, and the note says no theorem routes either remaining
ledger into all of its simultaneous hypotheses.

## 6. Four-site flag routing: PASS AFTER CORRECTION

Assume the four-site circuit has aggregate ranks \((1,2)\), and write its
complement as \(\{u,v\}\).  The following linear statements in (32)--(35)
are correct.

1. A selector base for the rank-one endpoint must use both \(u\) and \(v\).
2. If all four off-\(u\)/off-\(v\) endpoint maps have rank three, projection
   of \(L_x^P\) onto the two-dimensional quotient is surjective and
   projection of \(L_x^S\) onto the one-dimensional quotient is nonzero.
3. Consequently \(\theta_x\) has rank two or three.  In rank two it has a
   nonzero core-valued kernel probe; in rank three it is an isomorphism onto
   the three-dimensional direct-sum quotient.

The last alternative is not a "full transverse chart" in the sense of
Sections 4--6.  An isomorphism

\[
 V_x^*\longrightarrow
  ({\mathsf C}^*/U_P)\oplus({\mathsf D}^*/U_S)
\]

only records the two endpoint-star projections at one residual site.  It
does not supply:

* a second source pair sharing one endpoint with the first;
* the direct blocks \(A,B,C,E,F,U\) and their literal connection;
* a nonzero curvature component, much less the \(0000\) component;
* clean unary and scalar-zero endpoints on either pair line;
* compatibility of quotient bases with the fixed physical target labels;
  or
* a common-coloop site and nonzero residue corner.

The revised source now ends the valid trichotomy with **two full-rank local
quotient maps**, not two charts satisfying (23). It lists the missing chart
data and says that a new source-provenance lifting lemma would be required.
The claim that (23) is exhaustive for the remaining selector circuit has
been removed.

There is also an order qualification.  The corrected selector-circuit
theorem is a theorem about two rank-three Rado matroids on a complete
six-site packet.  Its own independent audit explicitly warns that selecting
six sites from a larger residual does not retain the off-site ranks or the
common-power equations. The revised Section 8 explicitly confines the
trichotomy to the complete six-site packet and denies any uniform
extraction.

## 7. Uniform order scope: PASS AFTER CORRECTION

The displayed Omega map exists in this two-column form only at \(h=3\).
For residual size \(2h\), two clean endpoints give instead

\[
 {\cal E}(\lambda K_0+\mu K_1)
   =\lambda\mu
       \sum_{j=1}^{h-1}
         \lambda^{h-1-j}\mu^{j-1}E_j,
\]

with \(h-1\) mixed tensors and a degree-\((h-2)\) vector polynomial after
the two endpoint factors are removed.  For \(h>3\), no-active cleanliness
is not equivalent to the rank or kernel geometry of a map
\(\mathbb C^2\to({\cal R}_W)_6\), and (6), (21), and (23) are not the
uniform bad locus.

The common-coloop residue construction itself has a uniform version using

\[
 A=q_0^{[h-1]},\qquad B=q_0^{[h-2]},
\]

but the present note specializes it to \(A=q_0^{[2]},B=q_0\). No theorem
here extracts an \(h=3\) quotient from the higher-order Omega/resultant
packet while preserving the same source provenance, clean endpoints,
target anchors, curvature, and common power. Revised Sections 1, 8, 9, and
10 explicitly state this limitation and remove the former ledger-closing
and conjecture-level claims.

## 8. Final dependency assessment

| Component | Audited status |
|---|---|
| (3)--(6), one-chart Omega geometry | **PASS**, conditional on the displayed diagonal \(h=3\) endpoints |
| (8)--(12a), every two-cut coefficient | **PASS** |
| (14)--(16), matrix-cap jets and connection | **PASS** |
| (18)--(19), trace realization | **PASS** under the stated scalar-zero trace equations |
| (17), nonzero \(0000\) curvature | **Explicit additional hypothesis**, not supplied by general selection |
| (22)--(24), two-chart kernel target | **Exact conditional formulation, still open** |
| (25)--(29), odd quotient and flat transport | **PASS at \(h=3\)** |
| (30)--(31), scalar-zero residue | **PASS AFTER CORRECTION:** general value \(K_{cc}\overline Y_c\), with explicit visibility hypothesis |
| Conditioned residue--Omega incidence | **Well-posed intersection target, still unproved and not exhaustive** |
| (32)--(35), flag circuit | **PASS as a local quotient trichotomy only** |
| Uniform all-even consequence | **Explicitly disclaimed; common-power extraction remains open** |

The strongest verified result is therefore a clean conditional description
at the first boundary: if two overlapping diagonal full-nine charts with
the displayed clean endpoints and selected nonzero \(0000\) curvature are
already given, simultaneous absence of an active clean point is exactly the
simultaneous bad-Omega condition. Equation (23) is the direct open target.
The residue statement is a separate conditioned intersection target, and a
uniform source-faithful routing theorem remains open.
