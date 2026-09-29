# Cofactor diagnostics for square-root rates and a stronger unrestricted exponent

September 28, 2026.

**Status: written proof with exact supporting checks; independent audit
pending.** This is a quantitative follow-up to the existing proof identities,
separate from the Lean formalization. The unrestricted six-site square-root
law remains open.

[Illustrated guide](../explainers/COFACTOR-RATE-TEST.md) ·
[Exact replay](../computations/cofactor-square-root-rate-2026-09-28/README.md) ·
[GHZ project](../research/ghz-rates/README.md)

## 1. What improves

For an arbitrary complex three-color matching source on \(n=2m\ge6\) sites,
normalize its squared edge norm to \(S=1\), and write

\[
 H=\lambda\Delta+E,\quad \Delta=a^n+b^n+c^n,\quad
 \ell=|\lambda|,\quad \varepsilon=\|E\|_2,\quad \xi=\|E\|_1.
\]

The pure mean defines \(\lambda\), so \(E\perp\Delta\),
\(\xi\le3^m\varepsilon\), and
\(\ell^2=FR/3,\ \varepsilon^2=(1-F)R\).

For target color \(h\), let \(M_h\) be the zero-diagonal symmetric matrix
of \(hh\) source entries and let
\[
 C_h[r,q]=\operatorname{haf}(M_h[V\setminus\{r,q\}]),\quad r\ne q,
 \qquad C_h[r,r]=0.
\]
For root color \(i\), set \(B_{ih}[p,r]=A_{pr}(i,h)\), with zero diagonal.
Define the computable cofactor defect

\[
 d(A)=\max_{i,h}\|B_{ih}C_h-\delta_{ih}\lambda I_n\|_F. \tag{1}
\]

**Theorem 1 (source-dependent cubic certificate).** The explicit positive
constants \(T,G\) below give

\[
 \boxed{\varepsilon\ge
 \frac{\ell^3}{3^mT}\min\{1,(d(A)/G)^m\}.}            \tag{2}
\]

**Local consequence.** At any nonzero zero-output source \(A_*\) for which
some \(B_{ih}(A_*)C_h(A_*)\ne0\), every nearby source satisfies
\(\varepsilon\ge c|\lambda|^3\), for some \(c>0\) after normalization.
All endpoint colors and complex perturbations are allowed. No lower
bound on response rank is required.

In particular this gives a local square-root rate law at the single-color
two-triangle source with all six edges equal to one. Both triangle
responses have rank seven, so the earlier regular-triangle theorem did
not cover it. A signed octahedral zero supplies another application
outside the earlier star fidelity-gap test.

**Theorem 1a (all balanced single-color limits).** Every balanced
single-color six-site zero has a local square-root bound, without any
source-matrix or response-rank condition. The constants can be chosen
uniformly on the normalized balanced single-color zero set and a
neighborhood of that set. Here single-color means one common target
color at all sites.

The extra ingredient is an exact polynomial certificate: for a symmetric
zero-diagonal scalar six-by-six matrix \(D_0\) and its hafnian cofactor
matrix \(C_0\), the equation \(D_0C_0=0\) forces the support to have no
perfect matching. Section 4 gives the certificate and the reduction.
It also implies a local square-root bound at **any colored zero-output
source whose same-color support has a perfect matching for at least one
target color**, without a balance hypothesis.

**Theorem 2 (unrestricted exponent).** There is an explicit
\(\gamma_n>0\) such that every normalized source satisfies

\[
 \varepsilon^2\ge\gamma_n\ell^{2q},\qquad
 q=3+\frac m2(k+2),\quad k=3+\frac{3(m-1)}2.
                                                               \tag{3}
\]

Consequently, for nonzero output and \(F>0\),

\[
 \boxed{R\le
 \left(\frac{3^q}{\gamma_n}\right)^\alpha
 \frac{(1-F)^\alpha}{F^{1+\alpha}},\qquad
 \alpha=\frac{16}{3n^2+14n+32}.}                     \tag{4}
\]

| Sites | Previous unrestricted exponent | New exponent |
| --- | --- | --- |
| 6 | \(1/15\) | \(1/14\) |
| 8 | \(1/23\) | \(1/21\) |
| 10 | \(2/65\) | \(2/59\) |

The constants are conservative. No improvement of the earlier numerical
prefactors or experimentally useful thresholds is claimed.

## 2. A residual bound also controls the size of the polynomial

Let \(g\) be an even polynomial in three complex variables of degree at
most \(2D\), \(D\ge1\), with \(g(0)=1\). Put

\[
 r=\|g(s/\sqrt2)^2-g(s)\|_1,\quad
 K=\binom{2D+3}{3},\quad
 B=2^DK(3+2^D).
\]

The coefficient norm sums absolute coefficients. **If \(r\le1\), then**

\[
 \boxed{\|g-1\|_1\le B,\qquad
 \|g_2\|_1\le Q_D r^{1/(D+1)},\quad
 Q_D=12B\max\{1,(64/7)(D+1)!\}.}                    \tag{5}
\]

There is no initial size assumption on \(g-1\).

To prove the first bound, write \(u(s)=g(s/\sqrt2)-1\) and \(b=\|u\|_1\).
At most \(K\) monomials occur. Orthogonality of monomials on the unit
three-torus, followed by Cauchy–Schwarz on the coefficients, gives

\[
 \|u^2\|_1\ge\sup_{|s_j|=1}|u(s)|^2
 \ge\sum_\nu|u_\nu|^2\ge b^2/K.                     \tag{6}
\]

On the other hand, the residual equals
\(u^2+2u-u(\sqrt2s)\), hence

\[
 b^2/K\le r+(2+2^D)b\le1+(2+2^D)b.
\]

This implies \(b\le K(3+2^D)\). Undoing the substitution costs at most
\(2^D\), proving the first part of (5).

Now choose the **fixed, degree-dependent** radius \(\rho^2=1/(2B)\).
Then \(\|\widetilde g-1\|_1\le1/2\) for
\(\widetilde g(s)=g(\rho s)\). The residual has no terms of degree zero
or two, so its new norm is at most \(\rho^4r\). Theorem 1 of
[the polynomial stability note](quantitative-proof-identities-2026-09-26.md#2-stability-of-the-finite-response-scaling-equation)
gives

\[
 \|\widetilde g_2\|_1
 \le6[(64/7)(D+1)!\rho^4r]^{1/(D+1)}.
\]

Multiplying by \(\rho^{-2}=2B\), and harmlessly enlarging the constant,
proves (5). All constants are positive rationals.

The improvement is that the rescaling radius no longer depends on
\(\lambda\). The earlier argument bounded \(g-1\) by \(M/\ell\),
which introduced an additional small-signal loss when undoing the scale.
The scaling residual itself supplies a uniform bound in the regime
where a rate violation could occur.

## 3. Transfer to matching responses and cofactor products

Use \(D=m-1,\ N=n-1,\ P=(n-1)!!\), and the constants from
[the general complex rate proof](general-complex-rate-bound-2026-09-26.md):

\[
 \begin{split}
 I_0&=I_1=1,\quad I_j=I_{j-1}+(j-1)I_{j-2},\\
 M&=3^NI_N,\quad U_0=2^NM,\quad V_0=2(P+M),\\
 T&=(4D+1)(1+2^N)(P+U_0)(U_0+V_0),\\
 H_0&=2^{N-1}I_{N-1}.
 \end{split}
\]

Take \(Q_D\) from (5) and define

\[
 J=2Q_D+(P+U_0)P,\qquad
 G=n\{2H_0(J+9P^2)+P^3\}.                          \tag{7}
\]

Suppose \(\ell>0\) and put \(t=T\xi/\ell^3\). First assume \(t\le1\).
At each root the inherited scalar polynomial has residual at most \(t\),
so (5) gives \(\|g_2\|_1\le Q_D t^{1/m}\).
Equation (6) of the general complex note, restricted to degree three,
therefore gives

\[
 \|\Psi_3|_{\rm binary}\|_1
 \le2Q_D\ell t^{1/m}+(P+U_0)\xi/\ell
 \le J\ell t^{1/m}.                                 \tag{8}
\]

Here \(\xi/\ell=\ell^2t/T\), \(\ell\le P\), \(T\ge1\),
and \(t\le t^{1/m}\).

The exact cubic omission identity from that note is

\[
 \lambda s_h[k^{S_0}]\mathscr E_2
 =K(F_0,B_3)-K(\mathscr E_2,B_1).
\]

The bounds \(\|F_0\|_1\le H_0\),
\(\|\mathscr E_2\|_1\le9H_0\), \(\|B_1\|_1\le\xi\), and (8) give

\[
 \|[k^{S_0}]\mathscr E_2\|_1
 \le H_0(J+9P^2)t^{1/m}.
\]

Off-diagonal entries of the cofactor defect are coefficients of this
quadratic, with a factor at most two. Diagonal entries are coefficients
of \(E\), of modulus at most
\(\xi=\ell^3t/T\le P^3t^{1/m}\). Thus

\[
 \boxed{d(A)\le Gt^{1/m}\quad\text{when }t\le1.}      \tag{9}
\]

If \(t>1\), then \(\varepsilon\ge\xi/3^m>\ell^3/(3^mT)\).
If \(t\le1\), (9) gives
\(t\ge(d(A)/G)^m\), and the same relation between \(\xi\) and
\(\varepsilon\) proves (2). For \(\lambda=0\), (2) is automatic.

At a fixed zero-output source with a nonzero cofactor product,
\(d(A_*)>0\). Continuity gives a neighborhood where it is bounded
below. Equation (2) proves the local consequence. For a source of
arbitrary squared norm \(S>0\), apply the certificate to \(A/\sqrt S\):
the defect scales by \(S^{-m/2}\), as do \(\lambda\) and the error.
The local rate statement uses \(R=\|H\|^2/S^m\).

## 4. Two singular examples and a limiting case of the test

For a single-color source, write its scalar matrix as \(D_0\) and its
cofactor matrix as \(C_0\). All other cofactor defects vanish, and
at zero output the test reduces to \(D_0C_0\ne0\).

**Two triangles.** Put weight one on every edge of triangles \(012\)
and \(345\), and zero elsewhere. Then \(S=6\), \(H=0\), and

\[
 D_0C_0=
 \begin{pmatrix}0&2\mathbf1_{3\times3}\\
                 2\mathbf1_{3\times3}&0\end{pmatrix},
 \qquad \|D_0C_0\|_F^2=72.
\]

The squared normalized defect is \(72/6^3=1/3\).
The two triangle response ranks are \(7,7\), so the six-site derivative
has rank \(49\). The new theorem covers every nearby complex source,
including perturbations outside the two-triangle architecture.

**Signed octahedron.** Split the vertices into \(01|23|45\), put no
edges within a pair, and use the following cross-pair matrices:

\[
 D_{01,23}=D_{01,45}=
 \begin{pmatrix}1&1\\1&-1\end{pmatrix},\qquad
 D_{23,45}=\begin{pmatrix}1&1\\-1&1\end{pmatrix}.
\]

This balanced source has \(S=12\), zero hafnian, and
\(\|D_0C_0\|_F^2=192\), hence squared normalized defect \(1/9\).
It has a perfect matching in its support. Every root has a missing
edge; all its cubic and quintic root responses vanish. Thus it
passes both the previous two-column support test and the higher-response
vanishing test below. Nevertheless the nonzero cofactor product proves
a local square-root bound.

**Prism control.** At the canonical three-color prism limit, all nine
cofactor products are zero. The new test does not settle that case.
Its already established local square-root bound uses a different argument.
Zero defect is therefore not evidence of a counterexample.

**A rank corollary for balanced single-color zeros.** At six sites,
every balanced single-color zero with scalar matrix rank at least five
has a local square-root bound. Indeed, \(D_0C_0=0\) would force
\(\operatorname{rank}C_0\le1\). A symmetric rank-one complex matrix
has the form \(cvv^{\mathsf T}\); its zero diagonal forces \(v=0\),
so \(C_0=0\). But the
[balanced four-site identity](balanced-four-site-response-bound-2026-09-26.md)
gives \(\|C_0\|_F^2=2T_4\ge2S^2/15>0\), a contradiction.
This rank is the rank of the scalar six-by-six source matrix, not the
rank of its matching-output derivative or a triangle response.

### An exact certificate removes the remaining scalar rank condition

**Scalar lemma.** If the support of a complex symmetric zero-diagonal
six-by-six matrix \(D_0\) has a perfect matching, then \(D_0C_0\ne0\).

Relabel a nonzero matching as \(01|23|45\). For nonzero site factors
\(s_p\), put \(D'=S_dD_0S_d\), where \(S_d=\operatorname{diag}(s_p)\).
Writing \(\sigma=\prod_ps_p\), the matching expansion gives

\[
 C'=\sigma S_d^{-1}C_0S_d^{-1},\qquad
 D'C'=\sigma S_d(D_0C_0)S_d^{-1}.
\]

Choose the six factors so that the three matching entries become one.
This does not change whether the matrix product vanishes. The normalized
matrix has twelve unrestricted complex entries:

\[
 D(x)=
 \begin{pmatrix}
 0&1&x_0&x_1&x_2&x_3\\
 1&0&x_4&x_5&x_6&x_7\\
 x_0&x_4&0&1&x_8&x_9\\
 x_1&x_5&1&0&x_{10}&x_{11}\\
 x_2&x_6&x_8&x_{10}&0&1\\
 x_3&x_7&x_9&x_{11}&1&0
 \end{pmatrix}.
\]

For each \(p,q\), let \(f_{pq}(x)=(D(x)C(x))_{pq}\), formed by
the three literal four-site matchings in each cofactor. The
[saved rational certificate](../computations/cofactor-square-root-rate-2026-09-28/scalar-matching-certificate.json)
derives the constant polynomial \(1\) from these polynomials by
244 arithmetic nodes. Each input is a specified \(f_{pq}\); each
subsequent node is an explicit polynomial linear combination of earlier
nodes. The last node is exactly \(1\).

The standard-library replay reconstructs every input from \(D(x)\),
evaluates every combination over \(\mathbb Q[x_0,\ldots,x_{11}]\),
and checks the final polynomial coefficient by coefficient. Thus the
certificate proves \(1\in(f_{pq})\), not merely that a numerical search
found no common zero. Evaluating at any hypothetical complex common
zero would give \(1=0\). This proves the scalar lemma.
The optional SymPy generator only discovers the arithmetic derivation;
its Groebner-basis verdict is not an acceptance input.

Applying the lemma to \(M_h\) immediately gives the colored corollary:
one monochromatic perfect matching in the limiting support forces
\(M_hC_h\ne0\), and Theorem 1 supplies the local square-root bound.

Now consider a normalized balanced single-color source. If its support
has a perfect matching, the scalar lemma applies. Otherwise the
[balanced-support classification](site-balancing-rate-reduction-2026-09-26.md)
says its support is exactly two disjoint triangles, with all six edges
nonzero. For a vertex \(p\) in the first triangle and \(q\) in the
second, the entry \((D_0C_0)_{pq}\) is twice the product of the two
edges at \(p\) and the edge opposite \(q\). It is nonzero.
Therefore every such source has \(D_0C_0\ne0\).

Theorem 1 proves the local claim in Theorem 1a. For uniformity, the
normalized balanced single-color zero set is compact: balance, one-color
support, zero output, and \(S=1\) are closed conditions in a finite
dimensional space. The continuous defect has no zero there, so it has
a positive minimum. It remains bounded below on a neighborhood.
Equation (2) supplies one cubic constant throughout that neighborhood.
The same argument applies to the finite union over the three possible
common target colors. No numerical value for this minimum is claimed.

## 5. Improved approximate diagonality and the global exponent

In addition to \(t\le1\), suppose \(Gt^{1/m}\le\ell/2\).
Then \(M_hC_h\) is within \(\ell/2\) of \(\lambda I\),
and the existing inverse argument gives
\(\|C_h^{-1}\|_{\rm op}\le4/\ell\).
Using (9) on the six off-color matrices gives

\[
 \eta:=\|A-A_{\rm diag}\|_{\rm edge}
       \le8G\ell^{-1}t^{1/m}.                       \tag{10}
\]

The even-color projection from
[the parity refinement](rate-sharpness-followup-2026-09-26.md#1-a-parity-projection-improves-the-general-exponent)
removes the term linear in the off-color entries. With \(C_m=2^mP\),

\[
 \varepsilon_0:=\|H(A_{\rm diag})-\lambda\Delta\|_2
 \le\varepsilon+C_m\eta^2
 \le\varepsilon+K_*\varepsilon^{2/m}\ell^{-2-6/m},
 \quad K_*=576C_mG^2T.                              \tag{11}
\]

We used \(t\le3^mT\varepsilon/\ell^3\) and \(T^{2/m}\le T\).

Let \(c_n>0\) be the explicit diagonal amplitude constant in equation
(32) of the polynomial stability note. Set

\[
 \begin{split}
 k&=3+3(m-1)/2,\quad q=3+\tfrac m2(k+2),\\
 b&=\min\{c_n,\,[2P^{\lceil k-1\rceil}]^{-1}\},\\
 \gamma_n&=\min\left\{
 \frac1{3^{2m}T^2P^{2\lceil q-3\rceil}},
 \frac1{T^2(6GP^{\lceil k/2\rceil})^{2m}},
 \left(\frac b{4P^{\lceil q-k\rceil}}\right)^2,
 \left(\frac b{4K_*}\right)^m\right\}.
 \end{split}                                       \tag{12}
\]

All these constants are positive rationals. To prove (3), suppose
\(\varepsilon<\sqrt{\gamma_n}\ell^q\) with \(\ell>0\).
The first two terms of (12) ensure \(t\le1\) and
\(Gt^{1/m}\le\ell/2\). For the second, use
\((q-3)/m-1=k/2\).
The last two terms and
\(2q/m-2-6/m=k\) give

\[
 \varepsilon_0<(b/2)\ell^k\le\ell/4.
\]

Thus the projected source has nonzero output and fidelity at least
\(48/49\), above the diagonal theorem's \(12/13\) threshold.
Its norm is at most one. Homogeneity of that theorem gives
\(\varepsilon_0\ge c_n\ell^k\), contradicting \(b\le c_n\).
The case \(\ell=0\) is immediate.
Substituting the fidelity and rate identities into (3) proves (4).

At six sites this changes the amplitude power from \(16\) to \(15\).
For a bounded analytic family with target order \(r_0\) and error
order \(s_0\), it therefore forces \(s_0\le15r_0\).
It does not imply the desired bound \(s_0\le3r_0\).

## 6. Sharper conditions on any possible violation

A normalized sequence violating every uniform square-root constant has,
after passing to a subsequence, \(A_j\to A_*\) and
\(\varepsilon_j/\ell_j^3\to0\).
The exact Krenn–Gu theorem forces \(H(A_*)=0\): otherwise the limit
would have a nonzero perfect GHZ output.
Equation (9) now forces

\[
 \boxed{B_{ih}(A_*)C_h(A_*)=0\quad\text{for all }i,h.} \tag{13}
\]

There is a stronger higher-response condition on *any* high-fidelity
zero-output limit, even without the cube-relative error hypothesis.
In the notation of the [star certificate](ghz-star-fidelity-gap-2026-09-27.md),
\(g=1+W/\lambda\), and multiplying its residual estimate by \(\lambda^2\)
gives

\[
 \|\lambda(2W(s/\sqrt2)-W(s))+W(s/\sqrt2)^2\|_1
       \le T\xi/\ell.                              \tag{14}
\]

As \(F\to1\), \(\xi/\ell\to0\); at a zero-output limit, \(\lambda\to0\).
The coefficients of \(W\) depend polynomially on the source. Taking
limits in (14) gives \(W_*^2=0\), hence \(W_*=0\).
The approximate binary model then gives

\[
 \Psi_{2j+1}(A_*)|_{\rm binary}=0
 \quad (1\le j\le m-1)
 \quad\text{at every root}.                         \tag{15}
\]

This extends the highest-response support obstruction to every higher
odd degree. For a candidate square-root violation, (13) must hold as well.
The octahedral example shows that (13) can remove cases left by (15).

Remaining candidates must satisfy these equations along with balance
and the zero-output condition. Theorem 1a excludes all single-color
candidates, including scalar matrix ranks at most four. Moreover, each of
the three same-color support graphs must have matching number at most two:
any monochromatic perfect matching is excluded by the scalar lemma.
We have not classified the remaining common zero set or proved the
required cubic error estimate there. The global
square-root law and the separate unrestricted W-state design problem
remain open. The replay checks exact identities, constants, and examples;
the general inequalities and limiting arguments are the written proof.
