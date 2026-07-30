# Independent audit of the selector/Hall and one-anchor threshold notes

## Verdict

The exact algebra in the two negative guards is correct.  The
matroid-union criterion, the deficient-flat ranks and Hall permanent, the
complete-graph torus identities, the four-cycle Jacobian obstruction, the
coefficient-dark contraction and Lemma 7.1, and every displayed calculation
in the one-anchor packet all survive independent reconstruction.

The conclusions must retain their stated missing-row scope.  The
deficient-flat example is a realization of one selected mixed word, not a
tensor solution.  The complete-graph guard satisfies the six off-diagonal
tensor rows and all target-zero scalar rows but misses the three diagonal
target tensors.  The one-anchor packet satisfies seven of the nine tensor
rows and misses \(X_1,X_2\).  None of these packets is a counterexample to a
statement assuming the full-nine equations.

There is one substantive correction to the proposed two-anchor threshold.
Equations (30)--(34) correctly exhibit a relative diagonal gauge, after a
minor base-point normalization is added.  They prove that two anchors do not
fix the crossed first jet.  They do **not** prove that a crossed target-zero
row removes that gauge: zero is itself invariant under the relative torus.
Nor is the four-cut row \((r,r;s,s)\) literally the crossed endpoint matrix
unit \(E_{rs}\) used in (32).  The three-row packet is therefore a sensible
next exactness target, and Lemma 7.1 proves a contradiction once its much
stronger coefficient-dark hypotheses hold, but sufficiency/minimality on an
active selector-overlap chart remains open.

The audited snapshots were

```text
6663985df121fbea8a998c1cb717222dcc1c9434b7232f1f5717fa586426e659  notes/selector-hall-base-packing-and-block-jacobian-guard.md
797785843ad167a72e52e0bf789da7714b8243ed0bda8b412f7939025dc5dacd  notes/h3-one-anchor-selector-four-cut-guard-and-two-anchor-threshold.md
caf64b6c3f20e269a44ef896eae7493cc676739f47e26f0877fef8860d07d3e0  computations/verify_h3_one_anchor_selector_four_cut_guard.py
```

## Scope ledger

| Statement | Verdict | Exact scope |
|---|---|---|
| Selector base-packing iff inequality | Correct | Abstract rank-three Rado matroids on six sites |
| Coloop-free deficient-flat guard | Correct, with an implicit map made explicit below | One selected target-zero word only |
| Complete-graph torus/Jacobian guard | Correct | Six off-diagonal tensor rows; all non-pure scalar rows; three diagonal tensors missing |
| Coefficient-dark Lemma 7.1 | Correct | A conditional full-nine contradiction assuming all of (39)--(41) |
| One-anchor selector/four-cut guard | Correct | Seven tensor rows: six off-diagonal plus \(00\); \(11,22\) missing |
| Two-anchor relative-torus calculation | Correct after base-point normalization | A flag-stabilizer calculation, not a source realization or a sufficiency theorem |

## 1. Selector matroids and base packing

For a family of subspaces \(L_x\), the independent sets obtained by choosing
one independent representative from each selected \(L_x\) form the Rado
matroid, and its rank is

\[
 r(A)=\min_{J\subseteq A}
       \left(|A\setminus J|+\dim\sum_{x\in J}L_x\right).
\]

The matroid-union theorem says that \(W\) can be written as the union of an
\(M_P\)-independent set and an \(M_S\)-independent set exactly when

\[
                  r_P(A)+r_S(A)\geq |A|\qquad(A\subseteq W).
\]

Because \(|W|=6\) and both ranks are three, the two independent sets in any
such cover must be disjoint three-element bases.  Conversely, a disjoint
base partition is such a cover.  Thus Proposition 2.1 is an iff, not merely
a necessary condition.  The equivalent common-base argument with
\(M_S^*\) gives the same inequality.

The separated version is also correct.  Replacing the local spaces by

\[
 P_x(\ker S_x),\qquad S_x(\ker P_x)
\]

turns literal opposite-star annihilation into another Rado problem.  Its
union inequalities do not ensure that the chosen representatives also lie
in the nonlinear target-zero locus, and neither ordinary nor separated
base packing aligns the fixed diagonal target flags.

## 2. The deficient-flat packet

For the six lines in (G2), both matroids are indeed

\[
                    U_{1,3}|_{\{0,1,2\}}
                    \oplus U_{2,3}|_{\{3,4,5\}}.
\]

An exhaustive calculation of all \(64\) subsets found exactly one strict
union defect:

\[
 A=\{0,1,2\},\qquad r_P(A)+r_S(A)=2<3.
\]

Every single-site deletion has aggregate linear rank three, neither matroid
has a coloop, and there are no disjoint base partitions.  Thus the example
is genuinely outside the aggregate-rank-two common-exceptional-site case.
It does not challenge the full-nine rank-two-shore theorem; it only shows
that that theorem does not imply all matroid-union inequalities.

The physical realization described in Section 3 exists, although the
hidden maps are not fully written there.  One explicit completion is useful.
Put

\[
 b_0=b_1=b_2=e_0,\quad b_3=e_1,\quad b_4=e_2,\quad
 b_5=e_1+e_2,
\]

take \(u_z=e_{\omega_z}\), \(\ell_z=e_{\omega_z}^*\), and choose
\(m_z\) independent of \(\ell_z\) with \(m_z(u_z)=0\).  For
\(X=\{0,3,4\}\) set

\[
 P_z(u)=\ell_z(u)b_z,\quad S_z(u)=m_z(u)b_z,
\]

and interchange \(\ell_z,m_z\) for \(z\in Y=\{1,2,5\}\).  Both local
endpoint images are then exactly \(\langle b_z\rangle\); at the selected
word the visible \(P\)-rows on \(X\) are \(e_0,e_1,e_2\), the visible
\(S\)-rows on \(Y\) are the rows of \(V\), and the opposite rows vanish.
Taking \(q_{xy}=\ell_x\otimes\ell_y\) on the three ordered matching edges
and zero elsewhere gives \(F=1,H_{X,Y}=I\).  Hence

\[
 P^{\mathsf T}HS=V=-Fa.
\]

For \(a=-V\), \(\alpha=a_{10}=-1\), \(\tau=-2\), and
\(K_*=I-2E_{10}\).  Direct enumeration gives

\[
 \operatorname{per}(K_*V^{\mathsf T})=-4.
\]

This completes the claimed fixed-block realization, but only at the one
mixed word \(\omega\).  Calling it a selected-word packet is exact; calling
it a partial or full solution of the tensor pair equations would not be.
Likewise, saying it satisfies the *numerical conclusions* of the known
shore-rank restrictions is safe, whereas those full-nine theorems do not
logically apply to this packet.

## 3. Complete-graph torus and the own-edge obstruction

With \(q_{xy}=\ell_x\ell_y\) on every edge of \(K_6\), the fifteen perfect
matchings give

\[
 q^{[3]}=15L.
\]

After \(p_i s_j\) occupies its even and odd sites, the remaining \(K_4\)
has three perfect matchings, so

\[
 p_i s_jq^{[2]}=3L
\]

for all nine pairs.  Therefore \(a_{ij}=-1/5\) makes every left side zero.
This proves all six off-diagonal tensor identities, and every scalar
identity whose target coefficient is zero.  It fails precisely
\(0=X_0,0=X_1,0=X_2\).  The wording “all nine scalar equations at every
mixed coordinate word” is correct but is strictly weaker than the full-nine
tensor system.

At the displayed word, \(F=15,H_{xy}=3\), and the scalar proportionality
matrix is \(3\mathbf 1=-Fa\).  For the \(01\) entry,

\[
 K_*=\frac15I-\frac35E_{01},\qquad
 \operatorname{per}(K_*)=\frac1{125}.
\]

The differential of the block-evaluation map has edge part

\[
                         dQ_{xy}=\dot t_x+\dot t_y
\]

and zero pure-target part.  Its \(15\times6\) edge matrix is the signless
vertex-edge incidence matrix of \(K_6\).  Independent rational row reduction
gave rank six, while adjoining any one of the fifteen coordinate vectors
raised the rank to seven.  Thus no own-edge vector lies in its image.  The
four-cycle covector in (35) is a direct certificate for each edge.

The obstruction persists on the nonzero torus.  Writing a tangent as
\(\eta_z=\dot t_z/t_z\) gives

\[
 dQ_{xy}=t_xt_y(\eta_x+\eta_y).
\]

On a four-cycle \(xy,zw,xz,yw\), weights

\[
 {1\over t_xt_y},\quad {1\over t_zt_w},\quad
 -{1\over t_xt_z},\quad -{1\over t_yt_w}
\]

give the required left-kernel covector.  This makes the phrase “the same
calculation holds on the torus” precise.

The common-kernel statement (37) is also exact: at every even site only a
\(P\)-row proportional to \(\ell_z\) is present, and at every odd site only
an \(S\)-row proportional to \(\ell_z\) is present.  Hence the common local
kernel is \(\ker\ell_z\), which is radical for every incident rank-one
quadratic block.

## 4. Coefficient-dark contraction and Lemma 7.1

After contracting sites \(i,j\) by an endpoint-dark pair, the coefficient
of \(q^{[3]}\) has exactly two matching layers:

\[
                    u(v,w)z^{[2]}+t(v)v'(w)z.
\]

Because all endpoint-star coefficients at the two contracted sites vanish,
the coefficient of \(p_as_bq^{[2]}\) is exactly

\[
                    u(v,w)x_ay_bz+x_ay_bt(v)v'(w).
\]

This reconstructs (40), with no missing combinatorial factors in divided
power convention.

Under (41), the three rows in (43) follow.  The \(s\)-diagonal row forces
the scalar \(u(v_s,w_s)\ne0\); the crossed target-zero row then gives
\(R_r=0\), contradicting the nonzero \(r\)-diagonal target row.  No tensor,
star factor, or matching power is cancelled.  Lemma 7.1 is therefore a
valid full-nine conditional contradiction.

Its assumptions are not consequences of selectors, a Hall permanent, or
matroid union: they require common local kernel vectors, two complete
internal-star products to vanish after cancellation, three fixed-coordinate
target incidences, and a direct \(q_{ij}\)-coefficient forced nonzero by a
diagonal target row.  The lemma must continue to be presented as a guarded
alternative, not as an incidence theorem already available in an exact
source.

## 5. The one-anchor packet

For the packet (5)--(7), \(q^{[2]}\) is the product of its two disjoint
edges and \(q^{[3]}=0\).  Independent support enumeration gives the complete
coefficient table

\[
 \bigl[p_i s_jq^{[2]}\bigr]_{i,j}=
 \begin{pmatrix}X_0&0&0\\0&0&0\\0&0&0\end{pmatrix}.
\]

Thus the six off-diagonal rows and the \(00\) row are exact, and the only
missing equations are \(0=X_1\) and \(0=X_2\).

The colour-zero selector matrices at
\((A_0,A_2,B_1)\) and \((A_1,B_0,B_2)\) are both \(I_3\).  Direct inspection
also confirms that each chosen covector annihilates the opposite endpoint
star at its site.

An independent perfect-matching expansion on the canonical line found

\[
 [Y]{\cal E}=6u^3,\qquad [X_0]{\cal E}=v^3.
\]

For the all-zero word, the only uncancelled matching is the \(v^3\)
response matching.  The other matching has weight \(u^2v\) and is exactly
cancelled by the retained \(X_0\) target term.  Since
\(\gcd(u^3,v^3)=1\),

\[
 v^3S_2\oplus u^3S_2=S_5.
\]

In monomial bases, the combined Macaulay matrix for \(v^3\) and \(6u^3\)
is diagonal up to column order, with diagonal
\((6,6,6,1,1,1)\).  Its determinant is \(216\) and its rank is six.
Equivalently, multiplication by \(6u^3\) has rank three in
\(Q_{v^3}\), so the claimed quotient rank is exact.

On the \(A_0,A_2\) colour-zero cut,

\[
 t_0=U_{00}=M_{00}=0,\qquad v_0=e_0^{(B_2)},\qquad
 L_0=u\,s_1|_D+v e_0^{(A_1)}.
\]

Every \(u\,s_1|_D\) term collides with
\(e_0^{(B_2)}(B_0B_1)_0\), leaving exactly

\[
                         P_{00}=vX_0^D.
\]

The diagonal anchor therefore really survives this cut.  The packet proves
that this one anchor, even with same-colour separated selectors, does not
force residual quotient rank at most two.  It proves no failure of a rank
bound that is allowed to use either missing diagonal row.

The supplied checker runs successfully with Python's standard library and
reproduces the two coordinates and the cut coefficient.  Its coverage is
narrower than the entire pair of notes: it does not check the deficient-flat
or torus guards, Lemma 7.1, the quotient matrix rank, or the two-anchor
calculation.  Its “seven retained pair rows” description is accurate; the
code computes the other two left sides as zero but does not and need not
pretend that their nonzero target equations hold.

## 6. Two anchors and the relative torus

If the two transported rank-one tensors in (30) are diagonal under the
same pair \(G,H\), their left and right factors must occupy coordinate axes.
Invertibility makes the two axes distinct.  This correctly proves partial
two-label flag alignment, conditional on transporting both anchors into the
same chart with the same \(G,H\).

For the path (31), one should add

\[
                         g_r(0)=g_s(0)=1.
\]

Then both diagonal units are fixed, while

\[
 G(t)^{-\mathsf T}E_{rs}H(t)^{-1}
       ={g_s(t)\over g_r(t)}E_{rs},\qquad
 \xi C_{rs}=\alpha(\lambda_s-\lambda_r).
\]

Without that normalization, the derivative has the extra base factor
\(g_s(0)/g_r(0)\), unless \(\alpha\) is redefined to mean the current
normalized entry.  A numerical rational check with
\((\lambda_r,\lambda_s)=(2,5)\) gave zero derivatives on both anchors and
cross derivative \(3\alpha\).

This calculation establishes only the negative fact: two axes can remain
anchored while the crossed first jet drifts.  Three further distinctions are
essential.

1. The Riccati--leakage identity (34) additionally assumes a mixed
   target-zero chart and a source-valid pure-horizontal own-edge tangent.
   The abstract diagonal gauge path is not itself shown to be such a
   physical tangent.
2. A target-zero tensor remains zero after multiplication by
   \(g_s/g_r\).  Consequently the crossed zero row, considered only as a
   transported target equation, does not fix the relative scale.  Any such
   conclusion has to come from a faithful physical overlap equation that is
   injective on the relevant correction module.
3. The crossed endpoint cell in (32) is \(E_{rs}\), whereas the third row
   in the coefficient-dark packet (35) is \((r,r;s,s)\): endpoint cell
   \(E_{rr}\) evaluated on the other cut colour.  Lemma 7.1 explains why
   that four-index row is decisive under (39)--(41), but no argument in the
   note identifies it by itself with the relative character in (32).

Accordingly, the sentence that the first two proposed inputs “fix the
two-label flag and its relative scale,” and the assertion that the crossed
row “must eliminate” \(g_s/g_r\), are overclaims if read as proved facts.
The rigorous conclusion is narrower: two anchors are enough for partial
axis alignment but not for horizontality; the crossed row plus faithful
overlap transport is a proposed next mechanism whose required injectivity
and source provenance remain to be proved.  This narrower conclusion agrees
with the final open-problem paragraph of the note.

## 7. Final dependency assessment

The two notes validly rule out three shortcuts:

* a Hall permanent does not imply disjoint or separated selector bases;
* separated selectors do not imply own-edge transversality; and
* one literal diagonal anchor does not imply the desired cubic quotient
  rank loss.

They also supply one valid conditional full-nine closure, Lemma 7.1.  They
do not establish the incidence hypotheses needed to invoke it in every
exact source, and they do not prove that two anchors plus a crossed zero row
produce the missing overlap jet.  Those are the remaining full-nine steps.

## 8. Dependency and supersession of older targets

These artifacts change the status of four previously advertised routes.
They retire several *standalone implications*, not the valid inputs that
motivated those implications.

| Older target | Status after this audit | Surviving/refined target |
|---|---|---|
| Contradict the no-root branch from a mixed Hall permanent alone | **Retired as a standalone closure.**  The permanent can be nonzero while the endpoint Rado matroids have a coloop-free union defect, and even separated Hall selectors need not admit an own-edge lift. | Keep the Hall permanent as a valid mixed-response certificate, but separately prove the union inequalities, opposite-star separation, mixed target-zero representatives, and Jacobian column membership; alternatively prove the coefficient-dark hypotheses of Lemma 7.1. |
| Use one transported diagonal anchor to force \(\operatorname{rank}(L'S_2\to Q_f)\le2\) | **Retired.**  The seven-row packet has a literal surviving \(X_0\) coefficient, same-colour separated selectors, and nevertheless rank three in \(Q_f\). | Require genuinely additional full-nine information.  Two transported labels provide partial axis alignment, but a source-provenant crossed/overlap equation is still needed and its sufficiency is open. |
| Turn the inverse two-flag selector supplied by a nonzero physical minor directly into a fixed-label rectangle/descent | **Retired as an independent shortcut, not as a structural output.**  Invertibility gives an oblique selector; it supplies neither diagonal flag transport nor physical edge transversality, and a relative torus survives two axes at first order. | Retain the inverse selector only inside a chart carrying literal fixed-label anchors, a proved own-edge lift (or coefficient-dark replacement), and overlap control of cofactor leakage. |
| Force vanishing of every rank-six Macaulay minor from selector incidence, especially after exposing one coordinate \(f\) | **Refined, not discarded.**  The Macaulay/resultant equivalence and the existence of a rank-six physical four-cut minor remain correct diagnostics of rootlessness.  What fails is the proposed one-anchor rank-loss mechanism. | Work in \(Q_f\) with at least multi-anchor, source-provenant overlap/jet data, or prove a direct full-nine common-root argument.  The bare instruction “make selector coordinates meet every minor” is no longer a sufficient theorem-shaped target. |

Thus Hall data, inverse selectors, and Macaulay minors remain valid pieces of
the dependency chain, but none is now a terminal implication.  The
one-anchor rank-drop target is the item genuinely falsified by an exact
guard at its claimed hypothesis level.  The replacement frontier is a
full-nine, multi-anchor overlap statement with explicit incidence and
transport hypotheses.
