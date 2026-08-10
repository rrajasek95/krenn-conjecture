# The scalar-shore source-provenance quotient is dual to target-free caps

Research evidence only. Krenn's conjecture and **SP-CLEAN-BRIDGE** remain
open. This note reduces one source-provenance gate; it does not construct the
required two-chart overlap row.

## Outcome

Continue on the maximal rank-\((1,1)\) scalar shore.  Let

\[
 {cal Q}=\{K\in\operatorname {Mat}_{3\times3}:
       \lambda^{\mathsf T}K=0,\ K\mu=0\},
 \qquad
 \delta(K)=(K_{00},K_{11},K_{22}).                         \tag{1}
\]

Every cap in \({\cal Q}\) is clean and has direct scalar zero.  The complete
contracted rows give a physical response map \(\Phi:{\cal Q}\to C\) and a
top map \(M:C\to\mathbb C^3\) satisfying

\[
                         M\Phi=\delta.                       \tag{2}
\]

Let \(K_0=\ker\Phi\).  A coefficient functional on the response family is
represented by an ambient matrix \(F\): its value on \(\Phi(K)\) is
\(\langle F,K\rangle\).  Such a functional is induced by one functional on
the three diagonal target anchors if and only if

\[
 \boxed{\qquad F\in\Delta+{cal Q}^{\perp},\qquad}
                                                                    \tag{3}
\]

where \(\Delta\) is the diagonal-matrix subspace.  Consequently the exact
family-level provenance quotient and its dual are

\[
 \boxed{
 {mathfrak P}_{\cal Q}(\Phi)
   ={K_0^\perp\over\Delta+{cal Q}^{\perp}},
 \qquad
 {mathfrak P}_{\cal Q}(\Phi)^*\cong{\ker\delta\over K_0}.}
                                                                    \tag{4}
\]

Thus the entire remaining scalar-shore source-provenance obstruction is
detected by target-free physical caps.  If \(r=\operatorname {rank}\delta\),

\[
             \dim{mathfrak P}_{\cal Q}(\Phi)
              =4-r-\dim K_0.                                \tag{5}
\]

Away from coordinate gates, \(r=3\) unless \(\lambda,\mu\) have one common
missing coordinate, in which case \(r=2\).  Hence the obstruction has
dimension at most one in the generic scalar gate and at most two in the
common-missing gate.  This is strictly smaller than the ambient fifteen-edge
Hessian problem.

## Proof of the criterion

Pair matrices entrywise.  Restriction to \({\cal Q}\) has kernel
\({\cal Q}^{\perp}\).  A target functional \(c=(c_0,c_1,c_2)\) pulls back
along \(\delta\) as the diagonal matrix
\(\operatorname {diag}(c_0,c_1,c_2)\).  Therefore

\[
 \langle F,K\rangle=c\cdot\delta(K)\quad(K\in{cal Q})
 \quad\Longleftrightarrow\quad
 F-\operatorname {diag}(c)\in{cal Q}^{\perp},             \tag{6}
\]

which proves (3).  A functional on \(\Phi({\cal Q})\) is precisely a
functional on \({\cal Q}\) annihilating \(K_0\), giving the numerator in
(4).  Equation (2) implies \(K_0\subseteq\ker\delta\), so the denominator
lies in that numerator.

For finite-dimensional paired spaces, the dual of a quotient \(V/U\) is
\(U^\perp/V^\perp\).  Here

\[
 (\Delta+{cal Q}^{\perp})^\perp
    ={cal Q}\cap\Delta^\perp=\ker\delta,
 \qquad
 (K_0^\perp)^\perp=K_0,                                    \tag{7}
\]

which proves the dual identification.  Since \(\dim{cal Q}=4\), (5)
follows.

## The one- and two-class normal forms

When \(\operatorname {rank}\delta=3\), the target-free cap space is one
dimensional.  Let \(K_*\) span it and put \(R_*=\Phi(K_*)\).  Then:

* if \(R_*=0\), every response-family coefficient functional already has a
  diagonal-anchor realization;
* if \(R_*\ne0\), the sole obstruction is its value on \(R_*\).

When all coordinates of \(\lambda,\mu\) are nonzero, \(K_*\) is the
alternating directed triangle from
`rank-one-rank-one-scalar-gate-diagonal-cycle.md`.

In the rank-two case, let \(k\) be the common missing coordinate and let
\(\{i,j,k\}=\{0,1,2\}\).  Put

\[
 x=\lambda_j e_i-\lambda_i e_j,
 \qquad y=\mu_j e_i-\mu_i e_j.                              \tag{8}
\]

Then

\[
             \ker\delta
              =\operatorname {span}\{e_k y^{\mathsf T},
                                      x e_k^{\mathsf T}\}. \tag{9}
\]

Thus the two possible provenance classes are represented by one fixed-row
and one fixed-column target-free rank-one cap.  If either physical response
vanishes, its class disappears automatically.

## Exact overlap-row test

Let \({\mathscr J}\subseteq K_0^\perp\) be the matrix span of overlap rows
which have actually been proved grade-preserving and source-valid on this
same response family.  The admitted provenance quotient is

\[
 {K_0^\perp\over\Delta+{cal Q}^{\perp}+{mathscr J}},
\]

and its dual is

\[
 \boxed{
 {\{K\in\ker\delta:\langle J,K\rangle=0
                    \text{ for every }J\in{mathscr J}\}\over K_0}.}
                                                                    \tag{10}
\]

Therefore one admitted row kills the generic rank-three class exactly when
\(\langle J,K_*\rangle\ne0\).  In the rank-two common-missing case, the
matrix of evaluations of the admitted rows on
\(e_ky^{\mathsf T},xe_k^{\mathsf T}\), after deleting responses already in
\(K_0\), must have full column rank.  This is a complete test, not merely a
necessary condition.

The known Bianchi row does not automatically pass it.  At one decorated
coefficient its response is the assignment difference

\[
                         J=H-G,
\]

whereas the physical cap-edge/dark-cut response is the assignment sum
\(B=H+G\).  If
\(\langle H,K_*\rangle=\langle G,K_*\rangle\ne0\), then

\[
             \langle J,K_*\rangle=0,
 \qquad     \langle B,K_*\rangle\ne0.                       \tag{11}
\]

The exact integral guard in
`two-chart-selector-provenance-sum-channel-guard.md` realizes this pattern
while retaining the diagonal anchors and the normal/direct-double ledger.
Thus the presently committed static overlap does not kill (4).  A positive
argument must split the assignment-sum channel at the source grade; another
cyclic difference cannot do it.

## Proof impact and remaining row

The recent scalar-shore theorem already exports a nonzero physical dark cut.
Equations (4), (7), and (9) identify the smallest possible next theorem:

> Use the two unused diagonal anchors and the source-faithful second-chart
> overlap to produce an admitted assignment-sum row whose evaluation is
> nonzero on \(R_*\) in rank three, and a full-rank pair of evaluations on
> the fixed-row/fixed-column responses in rank two, modulo any response
> which is already zero.

That statement would remove the scalar selector-family provenance class.
It would not yet produce the degree-five residual Macaulay functional; the
same overlap must then be prolonged through the common power.  Conversely,
any counterguard must keep all nine rows and the second chart while making
one of these one or two evaluations nonzero.  A seven-row guard cannot test
the theorem because it omits exactly the anchors needed here.

There is now one branch on which the required row is unnecessary.  The
[fixed complement-plane closure](n8-rank11-scalar-fixed-plane-provenance-closure.md)
uses the released-site proportionality and the common six-site cofactor to
prove \(\ker\delta\subseteq\ker\Phi\) in both diagonal ranks.  Thus the
provenance quotient is zero whenever the coordinate plane occurs on the
three-site response support.  The remaining assignment-sum test is the
fixed dark-shore plane.  The
[exact one-site guard](n8-rank11-scalar-fixed-dark-plane-one-site-guard.md)
shows that even two distinct full nine-row releases and genuine consecutive
powers can leave the generic target-free response nonzero.  Hence this last
test must use the joint five-site coefficient or the source-labelled
two-chart overlap.  On the guard its joint error is the scalar normal
\(\lambda\mu^{\mathsf T}W\), so even the joint cap-plane contraction is
zero; an individual labelled row is essential.  Another separate-release
assignment-sum construction is insufficient.

The required labelled row is now explicit.  The
[joint carrier theorem](n8-rank11-scalar-fixed-dark-plane-joint-labelled-carrier.md)
gives a two-row unit on the natural exposed-site completion fibre.  In the
unrestricted joint source it reduces the remaining escape to twelve
pure-zero perfect matchings avoiding the selected anchor and three mixed
anchor carriers.  These terms vanish in the rational guard but are not
forced zero in an arbitrary packet.  The scalar provenance problem has
therefore become a finite source-labelled carrier-routing statement rather
than another cap-plane quotient calculation.

## Exact audit

[`verify_rank_one_rank_one_scalar_gate_provenance_quotient.py`](../computations/verify_rank_one_rank_one_scalar_gate_provenance_quotient.py)
exhausts all 28 noncoordinate projective endpoint vectors over
\(\mathbb F_5\), hence 784 ordered pairs.  It verifies the rank split,
\(\dim(\Delta+{cal Q}^{\perp})=5+\operatorname {rank}\delta\), the dual
identity in (4), the explicit cross caps (9), and every possible subspace
\(K_0\subseteq\ker\delta\).  The proof above is field-independent over
\(\mathbb C\); the finite audit is a regression check only.

The exact rank histogram is 48 rank-two pairs and 736 rank-three pairs.
The deterministic ledger digest is

```text
d1d061a3ff2dc414ab14762938d06e70cafafe687540e029fa62afe92469ba41
```
