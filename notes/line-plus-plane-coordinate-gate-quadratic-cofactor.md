# The line--plus--plane coordinate gates have one quadratic cofactor

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome

Continue with the \(b=2\) line--plus--plane shore

\[
 W=A\sqcup\{u,v\},\qquad
 \operatorname{rank}P_A=1,\qquad
 \operatorname{rank}S_A=2,                                 \tag{1}
\]

where \(C_0=\ker P_A\) and \(\mathbb C d=\ker S_A\).  The exact clean
pencil \(K_c=cd^{\mathsf T}\), \(c\in C_0\), leaves two coordinate gates.
Perturbing either gate in its missing physical coordinate gives a complete
factorization of the clean error.

If \(d_i=0\), put

\[
 d(\lambda)=d+\lambda e_i,\qquad
 K_{c,\lambda}=c\,d(\lambda)^{\mathsf T},\qquad c\in C_0.    \tag{2}
\]

Let \(P_x(c)\) be the value of \(P(c)\) at \(x\), let \(S_{i,A}\) be the
restriction of the \(i\)-th right star to \(A\), and let \(q_A\) be the
shore restriction of the residual quadratic.  Then the response
\(r_{c,\lambda}\) has matching number at most two and

\[
\begin{aligned}
 r_{c,\lambda}^{[3]}&=0,\\
 r_{c,\lambda}^{[2]}
   &=2\lambda^2 P_u(c)P_v(c)S_{i,A}^{[2]},\\
 {\cal E}(K_{c,\lambda})
   &=2\lambda^2\sigma(K_{c,\lambda})^{h-2}
      P_u(c)P_v(c)
      \bigl(S_{i,A}^{[2]}q_A^{[h-2]}\bigr).
\end{aligned}                                                \tag{3}
\]

The factor \(2\) is the exact divided-power coefficient.  Formula (3) is
an equality in the physical site-square-zero tensor algebra, without a
choice of colour coordinates.

For the other gate, suppose

\[
 C_0=\{c:c_i=0\},\qquad P_A(c)=c_iP_{i,A}.                  \tag{4}
\]

Write \(c(\lambda)=c_0+\lambda e_i\) with \(c_0\in C_0\), and keep
\(d\in\ker S_A\).  The transposed calculation gives

\[
\begin{aligned}
 r_{c(\lambda),d}^{[3]}&=0,\\
 r_{c(\lambda),d}^{[2]}
   &=2\lambda^2 S_u(d)S_v(d)P_{i,A}^{[2]},\\
 {\cal E}(K_{c(\lambda),d})
   &=2\lambda^2\sigma(K_{c(\lambda),d})^{h-2}
      S_u(d)S_v(d)
      \bigl(P_{i,A}^{[2]}q_A^{[h-2]}\bigr).
\end{aligned}                                                \tag{5}
\]

Thus, away from intersections of the two original coordinate gates, the
remaining obstruction is no longer an unrestricted clean-error equation.
Under the global no-active-clean-cap hypothesis one must retain the fixed
nonzero shore cofactors

\[
 \Omega_i^S=S_{i,A}^{[2]}q_A^{[h-2]}\ne0
 \quad\text{and}\quad
 \Omega_i^P=P_{i,A}^{[2]}q_A^{[h-2]}\ne0,                  \tag{6}
\]

together with the two displayed nonzero local endpoint factors.  If a
cofactor or a fixed local factor vanishes, the corresponding perturbation
family is clean.  Its diagonal-coordinate product is generically nonzero,
and the direct scalar is not identically zero: otherwise the complete
contracted target row, flattened across \(\{u,v\}\mid A\), would equate a
rank-one tensor with two independent pure-label tensors.  A generic member
would therefore be an active clean cap.

For the missing-kernel-label gate, a kernel vector of either local map
\(P_u|_{C_0}\) or \(P_v|_{C_0}\) also gives a clean perturbation line.
Hence any such vector must itself lie on a physical coordinate or
direct-scalar boundary.  This is the exact local residue not seen by the
original projective clean pencil.

The theorem does not prove that the cofactors in (6) are impossible.  It
replaces both coordinate gates by fixed consecutive-power shore classes
and local kernel conditions, which can now be compared directly with the
one-bright cofactor ledger.

## Why the factorization is exact

In (2), \(P_A(c)=0\) and \(S_A(d)=0\).  The unperturbed response is
supported on \(\{u,v\}\), while the new term is
\(\lambda P(c)S_i\) and every one of its edges meets \(u\) or \(v\).
Any product of three response edges repeats one of those two sites.
The unperturbed two-site term also annihilates every other response term.
The only surviving divided square uses one edge through \(u\), one through
\(v\), and two distinct sites of \(A\), giving the second line of (3).
Those two edges already consume \(u,v\), so the remaining
\(q^{[h-2]}\) automatically restricts to \(q_A^{[h-2]}\).  The homogeneous
clean-error sum therefore has only its \(j=2\) term.  Equation (5) is the
same argument with the endpoints exchanged.

It remains to justify the generic direct-scalar assertion used above.
For the first gate, suppose
\(\sigma(c\,d^{\mathsf T})=0\) identically on \(C_0\).  Away from a second
coordinate gate, choose \(c\in C_0\) for which the two nonmissing products
\(c_jd_j,c_kd_k\) are nonzero.  At \(\lambda=0\), the complete contracted
row flattened across \(\{u,v\}\mid A\) is

\[
 P_B(c)S_B(d)\otimes q_A^{[h-1]}
   =c_jd_jX_j+c_kd_kX_k.                                  \tag{7}
\]

The left side has Schmidt rank at most one and the right side has rank two,
a contradiction.  For the fixed-row gate, if
\(\sigma(c\,d^{\mathsf T})\) vanished for every \(c\), apply the same
flattening separately to the two rows \(j\ne i\).  Since both \(p_j,p_k\)
are supported on \(\{u,v\}\), the two nonzero identities would force the
same \(q_A^{[h-1]}\) to be proportional to both \(Y_j^A\) and \(Y_k^A\).
Those fixed-label tensors are independent.  Thus the direct scalar is a
nonzero polynomial on each perturbation family.

## Exact audit

The standard-library checker
[verify_line_plus_plane_coordinate_gate_quadratic_cofactor.py](../computations/verify_line_plus_plane_coordinate_gate_quadratic_cofactor.py)
implements the site-square-zero algebra over exact rationals.  It verifies
the divided-square and clean-error identities for every physical label,
both coordinate gates, \(h=3,4,5\), and 108 deterministic rational
specializations.  Every specialization has a nonzero error witness, and
one aggregate SHA-256 digest pins the complete coefficient ledger.  The
checker passes normally, with -O, and with -I -S.
