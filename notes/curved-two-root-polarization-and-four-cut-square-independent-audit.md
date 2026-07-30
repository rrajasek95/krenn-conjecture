# Independent audit: two-root polarization and four-cut curvature square

## Verdict

The algebraic packet in
[curved-two-root-polarization-and-four-cut-square.md](curved-two-root-polarization-and-four-cut-square.md)
is **correct, subject to four local wording repairs**.  Equations (7),
(10), (15)--(19), and (21)--(24) have the right divided-power
coefficients, exponents, endpoint order, and target normalization.  The
quantity \(\kappa=AU-BF\) is exactly a coordinate of the canonical physical
transition, provided the displayed colours and fourth-site coordinate are
chosen as witnesses to a nonzero transition.

The repairs do not change any equation or the final bounded residual.  They
only prevent the note from promoting a selected coefficient row to global
cleanliness, or a nonzero coefficient response to an injectivity statement,
and they retain the degenerate cases in the two-root pencil.

## 1. Polarization and the first boundary

Linearity of cap data gives

\[
 F(uK_0+vK_1)=uF_0+vF_1,
 \qquad
 s(uK_0+vK_1)=us_0+vs_1,
 \qquad
 T(uK_0+vK_1)=uT_0+vT_1.
\]

The divided-power expansion of the first term is

\[
 (uF_0+vF_1)^{[h]}
 =\sum_{j=0}^h u^{h-j}v^jF_1^{[j]}F_0^{[h-j]}.
\]

In \((us_0+vs_1)^{h-1}(uT_0+vT_1)\), the coefficient of
\(u^{h-j}v^j\) is

\[
 \binom{h-1}{j}s_0^{h-1-j}s_1^jT_0
 +\binom{h-1}{j-1}s_0^{h-j}s_1^{j-1}T_1.
\]

This proves (7), including both boundary conventions.  The endpoint clean
equations are exactly \(E_0=E_h=0\), so removal of the factor \(uv\) in
(9) is valid.

For \(h=3\), \(E_1\) and \(E_2\) are respectively

\[
 F_1F_0^{[2]}-2s_0s_1T_0-s_0^2T_1,
 \qquad
 F_1^{[2]}F_0-s_1^2T_0-2s_0s_1T_1,
\]

so (10) and \({\cal E}=uv(uR_0+vR_1)\) are correct.  The projective kernel
classification in (11a) is also correct: independent \(R_0,R_1\) give no
kernel; a nonzero dependent pair gives one kernel point; and
\(R_0=R_1=0\) makes the whole pencil clean.  The last case yields an active
point only when the activity product is not identically zero.  In
particular, if both endpoints have \(s_0=s_1=0\), the entire joining pencil
is scalar-inactive even though the mixed Hermite equations (12) remain
valid.

When both scalar coordinates vanish, (12) follows from (10).  When exactly
one vanishes, the correct specialization is (13), not (12).  The physical
rows \(F_iq^{[h-1]}=T_i\) at two scalar-zero points prove the quotient
relation stated after (14): applying the linear map
\(Z\mapsto Zq^{[h-1]}\) carries precisely the same scalar relations to the
targets.

## 2. Two-site physical and clean rows

Put \(k=h-1\).  In the selected \((r,c),(s,d)\) row, direct divided-power
expansion gives

\[
 [q^{[k]}]_{rs}=Uz^{[k-1]}+tvz^{[k-2]},
 \qquad
 [q^{[k+1]}]_{rs}=Uz^{[k]}+tvz^{[k-1]}.
\]

Therefore

\[
 [Fq^{[k]}]_{rs}
 =Mz^{[k]}+(Lv+Ht+fU)z^{[k-1]}+ftvz^{[k-2]}.
\]

Since

\[
 Fq^{[h-1]}-(h-1)sq^{[h]}=T,
\]

these three identities prove every term, exponent, and the coefficient
\(-ks\) in (15).  The target coefficient is
\(\delta_{cd}\kappa_c(K)X_c^D\).

Likewise

\[
 [F^{[k+1]}]_{rs}=Mf^{[k]}+LHf^{[k-1]},
\]

and \(s^{h-1}=s^k\), which proves (16).  At \(s=0\), (15) really does have
a nonzero right side for every pair of residual sites assigned a colour
\(c\) with \(\kappa_c(K)\ne0\).  It follows that the complete selected
two-site coefficient response is nonzero, and it excludes \(F=0\) when
\(T\ne0\).  It does **not**, without a definition and an additional
argument, prove injectivity of a deleted-star map or nonvanishing of the
interior restriction alone.  Thus “faithful on every pair deletion” should
be read only as coefficientwise target visibility, not as a new
faithfulness theorem.

The guard comparison is valid at this exact scope.  If \(s=F=0\) but a
target coefficient \(\kappa_c\) is nonzero, every source term in the pure
\((c,c)\) row of (15) vanishes while its right side does not.

## 3. Endpoint-ordered four-cut data and curvature

For the \(pq\) coordinate cap, the effective quadratic is

\[
 A(z+e_rt+e_sv+e_re_sU)
 +(x+e_rB+e_sE)(y+e_rC+e_sF).
\]

Its interior, \(r\)-row, \(s\)-row, and double coefficient are exactly

\[
 f=Az+xy,\quad L=At+By+Cx,\quad H=Av+Ey+Fx,
 \quad M=AU+BF+EC.
\]

For the endpoint-ordered \(pr\) cap the corresponding expression is

\[
 B(z+e_qy+e_sv+e_qe_sF)
 +(x+e_qA+e_sE)(t+e_qC+e_sU),
\]

which gives

\[
 g=Bz+xt,\quad L=By+At+Cx,\quad N=Bv+Et+Ux,
 \quad M=BF+AU+EC.
\]

Thus (17)--(18) preserve endpoint order and share literal \(L,M\).
Cancellation of the product terms gives

\[
 ft-gy=(At-By)z,
\]

and direct expansion of the four-site coefficient gives

\[
 Uf+tH-Fg-yN=(At-By)v+(AU-BF)z,
\]

so (19) is correct with no factorial normalization hidden in it.

The canonical curvature-minor identity identifies

\[
 AU-BF
 =A_{pq}(a,b)A_{rs}(c,d)
  -A_{pr}(a,c)A_{qs}(b,d)
\]

with the \((b,c;s,d)\)-coordinate of the physical transition.  Hence a
nonzero transition permits a choice of \(b,c,s,d\) with \(\kappa\ne0\).
Nonzero \(\kappa\) is not automatic for an arbitrary preselected pair of
coordinate caps; it is exact after making this witness choice.  The primary
note's conditional sentence after (20) retains this distinction.

## 4. Clean rows, target exchange, and the square residual

For a coordinate cap \(E_{ab}\), its scalar is \(A\), and its selected
diagonal target is present exactly when \(a=b=c=d\).  Since
\(k=m-2=h-1\), (16) therefore gives

\[
 Mf^{[k]}+LHf^{[k-1]}=\delta A^kX_a^D.
\]

The same calculation for \(E_{ac}\) gives the second equation in (4) with
\(B^k\).  Applying (15) in the two endpoint orders gives (21pq) and
(21pr), including the correction factors \(-kA\), \(-kB\), and the same
right side \(\delta X_a^D\).

Subtracting those two presentations and using (19) gives exactly (22).
The divided-power identities

\[
 zz^{[k-1]}=kz^{[k]},
 \qquad
 zz^{[k-2]}=(k-1)z^{[k-1]}
\]

cancel the \(\kappa\)-terms with coefficients \(k-k\) and the
\(\Delta\)-terms with coefficients \(1+(k-1)-k\).  Thus the two target
rows are exchange-redundant, as claimed.  Subtraction of the two clean
rows gives (24) verbatim; it is a consequence of the pair of clean rows,
not a third independent equation.

The assignment in Section 4.1 correctly satisfies the **selected mixed
colour rows**: it gives

\[
 f=z,\quad g=L=H=N=M=\Delta=0,\quad\kappa=1,
\]

and the only surviving target presentation is
\(zz^{[k-1]}-kz^{[k]}=0\).  Because the other exposed-colour rows and the
monochromatic target rows are not specified, this does not prove that two
full cap tensors are clean.  The final paragraph of Section 4.1 correctly
calls it a selected-colour square guard; the preceding sentence saying
“Thus both coordinate caps are clean” needs the same restriction.

## 5. Required local repairs

No displayed equation needs repair.  Four prose changes make the result
fully exact.

1. In the outcome, replace the assertion that dependence of \(R_0,R_1\)
   always supplies “their resulting projective root” by the three cases in
   (11a), and retain the hypothesis that the activity product is not
   identically zero when \(R_0=R_1=0\).
2. Where the outcome treats one or both nilpotent endpoints, cite
   “(12)--(13)”; (12) applies only when both scalar coordinates vanish.
   Likewise replace the “third clean point” summary in Section 5 by the
   exact residual-kernel statement, since a kernel at an already-known
   endpoint is not a third distinct point.
3. Replace “faithful on every pair deletion” and “two-deletion-faithful” by
   “nonzero on every pure \((c,c)\) two-site coefficient row for which
   \(\kappa_c\ne0\).”  This is exactly what (15) proves.
4. In Section 4.1 replace “Thus both coordinate caps are clean” by “Thus
   both selected mixed-flag clean rows vanish.”  Cap-wide cleanliness is
   deliberately not imposed by that guard.

With these repairs, the note proves the advertised exact residual and does
not overclaim an active root, a faithful deletion map, or a global square
guard.

## 6. Audit artifact

The primary note audited here had SHA-256

```text
4916ad19e49f3d6cd3fdeb0eb3326a38551be2f553159e3dc9fc718a1f6a09a1
```

No computer algebra assumption is needed: the checks above are direct
matching/divided-power coefficient expansions, and (23) audits the only
factorial shifts in the target exchange.
