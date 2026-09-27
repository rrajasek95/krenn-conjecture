# An explicit rate bound for arbitrary complex endpoint colors

September 26, 2026.

**Status: new written research, with exact supporting checks; not independently
audited or admitted to the certified proof spine.** This note builds on the
[diagonal rate theorem](quantitative-proof-identities-2026-09-26.md). It gives
a quantitative diagonal reduction and then an explicit rate exponent for the
full three-color source model. It does not claim optimality or external review.

## 1. Result and conventions

Let \(n=2m>4\). The source has arbitrary complex coefficients
\(A_{pq}(i,j)\), for distinct sites and three endpoint colors, with the
symmetry \(A_{qp}(j,i)=A_{pq}(i,j)\). Identical parallel cells are aggregated.
Its perfect-matching tensor is \(H=A^{[m]}\). Put

\[
 S=\sum_{p<q,i,j}|A_{pq}(i,j)|^2,
 \quad R=\|H\|_2^2/S^m,
 \quad F=\frac{|H_{a^n}+H_{b^n}+H_{c^n}|^2}{3\|H\|_2^2}.
\]

Assume \(S>0\), \(H\ne0\). Normalize \(S=1\), and define

\[
 \Delta=a^n+b^n+c^n,\quad
 \lambda=(H_{a^n}+H_{b^n}+H_{c^n})/3,\quad
 \ell=|\lambda|,\quad E=H-\lambda\Delta,\quad
 \epsilon=\|E\|_2,\quad \xi=\|E\|_1.
\]

Here tensor coefficient norm means the sum of absolute values in the fixed
orthonormal word basis. Thus

\[
 \xi\le3^m\epsilon,\qquad
 \epsilon^2=(1-F)R,\qquad \ell^2=FR/3.
\]

**Theorem.** There is an explicit positive rational \(c_n^*\), given in
Section 6, such that every normalized source satisfies

\[
 \epsilon\ge c_n^*\ell^{q_n},\qquad
 q_n=\frac{3m^2+7m+2}{2}.
                                                        \tag{1}
\]

Consequently, for every \(F>0\),

\[
 \boxed{R\le
 \left(\frac{3^{q_n}}{(c_n^*)^2}\right)^{\alpha_n}
 \frac{(1-F)^{\alpha_n}}{F^{1+\alpha_n}},\qquad
 \alpha_n=\frac{8}{n(3n+14)}.}                          \tag{2}
\]

| Sites | Amplitude power \(q_n\) | Rate exponent |
|---|---:|---:|
| 6 | 25 | \(1/24\) |
| 8 | 39 | \(1/38\) |
| 10 | 56 | \(1/55\) |

The constants are conservative. The result assumes neither diagonality,
fixed support, a minimum nonzero edge weight, nor a nonzero limiting response
rank. It concerns normalized generation strength in the ordinary matching
model; probability conversion requires a specified physical source model.
The stronger diagonal exponent \(4/(3n+2)\) remains applicable in its domain.

## 2. Constants for the quantitative diagonal reduction

For this part \(n=2m\ge4\), and \(S\le1\) suffices. Write

\[
 D=m-1,\quad N=n-1,\quad P=(n-1)!!.
\]

Let \(I_j\) count partitions of \(j\) labeled objects into singletons and
pairs: \(I_0=I_1=1\), \(I_j=I_{j-1}+(j-1)I_{j-2}\). Define

\[
 \begin{aligned}
 M&=3^N I_N,& U_0&=2^N M,& V_0&=2(P+M),\\
 T&=(4D+1)(1+2^N)(P+U_0)(U_0+V_0),&
 Z&=T/(4M^2),\\
 K_3&=2^N M\left[1+12\max\{1,(64/7)m!Z\}\right],\\
 H_0&=2^{N-1}I_{N-1},&
 G&=n\left[2H_0(K_3+9P)+P^2\right],\\
 L&=24mPG.
 \end{aligned}                                         \tag{3}
\]

These quantities depend only on \(n\). We use large elementary bounds to
make every denominator and degree loss explicit. In particular, \(\ell\le P\)
and \(M\ge P\): a pure amplitude has \(P\) matching terms, and the
singletons/pairs count on odd \(N\) includes \(N!!=P\) partitions with one
singleton.

For a polynomial tensor, \(\|\cdot\|_1\) sums the absolute coefficients over
both word and parameter monomials. Multiplication and the complementary
alternating pairing are bounded by products of these norms.

## 3. Approximate reflection and the cubic response

Delete any original root. Its actual rows define
\(L(s)=s_aY_a+s_bY_b+s_cY_c\), with three formal parameters, regardless of
any linear dependence of the physical rows. On the remaining \(N=2D+1\)
sites let

\[
 \Psi(s)=\sum_{j=0}^{D}\frac{L(s)^{2j+1}}{(2j+1)!}R_0^{[D-j]},
 \quad \Phi(s)=L(s)R_0^{[D]},\quad \mathcal H=\Psi-\Phi.
\]

Use \(R_0\) for the retained quadratic to distinguish it from generation
strength. The literal linear response satisfies

\[
 \Phi(s)=\lambda\sum_h s_hh^\Omega+\mathcal E(s),
 \qquad \|\mathcal E\|_1=\xi.                         \tag{4}
\]

Each full word occurs once, with its root color recorded by its parameter.
For each receiving word, the coefficient norm of \(\Psi\), and also of
\(\mathcal H\), is at most \(M\): a singleton row has norm at most three,
and there are at most \(I_N\) partial matchings.

The universal reflection identity in Section 2 of the
[exact proof](../proofs/krenn-gu-all-orders-two-replica-proof.md) holds without
any purity assumption. Sum its divided odd responses of degrees at least
three, and replace \(\Phi\) by (4). The error term has norm at most
\(M\xi\). For a binary mixed word avoiding color \(h\), this gives

\[
 \|\mathcal H_w\|_1\le M\xi/\ell.
\]

For two pure words it gives

\[
 \|s_b\mathcal H_{a^\Omega}-s_a\mathcal H_{b^\Omega}\|_1
 \le M\xi/\ell,                                    \tag{5}
\]

and the corresponding relation for any two colors. No pointwise division
by a root response is involved: division by a parameter monomial preserves
coefficient norm.

### A common scalar up to a controlled error

Split \(\mathcal H_{a^\Omega}=s_a W+V\), with \(V\) containing no \(s_a\).
The part of (5) not divisible by \(s_a\) bounds \(\|V\|_1\le M\xi/\ell\).
The divisible part bounds
\(\|\mathcal H_{h^\Omega}-s_hW\|_1\le M\xi/\ell\) for \(h\ne a\).
Define

\[
 g=1+W/\lambda.
\]

It is even, has degree at most \(2D\), and
\(\|g-1\|_1\le M/\ell\). On any binary palette,

\[
 \Psi(s)=\lambda(s_a a^\Omega+s_b b^\Omega)g(s)+\mathcal B(s),
 \quad
 \|\mathcal B\|_1\le(P+U_0)\xi/\ell.                \tag{6}
\]

The analogous formula holds when the palette uses a different pair.
The actual binary tensor has norm at most \(U_0\), and its displayed
model part has norm at most \(V_0\).

### Quantitative cancellation of the determinant

The two-copy alternating pairing \(K(\Psi(s),\Psi(t))\) is invariant under
simultaneous orthogonal rotation of the two means. Replacing each tensor by
its model in (6) changes this pairing by at most
\((P+U_0)(U_0+V_0)\xi/\ell\). A 45-degree substitution has coefficient-norm
operator bound \(2^N\) for polynomials of degree at most \(2N\).
Consequently

\[
 \ell^2\left\|(s_at_b-s_bt_a)
 [g(s)g(t)-g((s+t)/\sqrt2)g((-s+t)/\sqrt2)]\right\|_1
 \le(1+2^N)(P+U_0)(U_0+V_0)\xi/\ell.
\]

For every polynomial \(Q\) of degree at most \(4D\),

\[
 \|Q\|_1\le(4D+1)\|(s_at_b-s_bt_a)Q\|_1.            \tag{7}
\]

To prove this elementary division bound, group monomials into chains whose
successive exponents differ by the exponent difference of the two displayed
monomials. Multiplication takes consecutive coefficient differences along
each chain, with zero endpoints. Recover each coefficient by a partial sum.
A chain has at most \(4D+1\) terms, since its total degree is at most \(4D\).
Summing the triangle inequalities proves (7). This bound also holds for
complex coefficients.

Cancel with (7), then set \(t=0\). Evenness and \(g(0)=1\) give

\[
 \|g(s/\sqrt2)^2-g(s)\|_1\le T\xi/\ell^3.            \tag{8}
\]

### Only the quadratic part of the scalar is needed

Set \(\rho^2=\ell/(2M)\) and \(\widetilde g(s)=g(\rho s)\).
Then \(\|\widetilde g-1\|_1\le1/2\). The scaling residual starts in degree
four, so (8) gives a better normalized bound:

\[
 \|\widetilde g(s/\sqrt2)^2-\widetilde g(s)\|_1
 \le \rho^4T\xi/\ell^3=Z\xi/\ell.                  \tag{9}
\]

Apply Theorem 1 of the quantitative-identities note. With three variables,
a quadratic has six monomials, and \(D+1=m\). Therefore

\[
 \|\widetilde g_2\|_1
 \le6[(64/7)m!Z\xi/\ell]^{1/m}.
\]

Undoing the scale for this degree costs only \(\rho^{-2}\).
Since \(\ell\rho^{-2}=2M\), (6) now implies, whenever \(x=\xi/\ell\le1\),

\[
 \boxed{\|\Psi_3|_{\rm binary}\|_1\le K_3 x^{1/m}.} \tag{10}
\]

Here \(\Psi_3=L^3R_0^{[m-2]}/3!\). The residual contribution is at most
\(2^N Mx\); we used \(x\le x^{1/m}\) and
\(u^{1/m}\le\max\{1,u\}\). Thus (3) is a rational upper bound for all
constants. This is the critical improvement over trying to undo the auxiliary
scale in every response degree.

## 4. A cubic omission identity controls the cofactor equations

Omit another site \(q\), let \(S_0=\Omega\setminus\{q\}\), and write

\[
 L=U+\sum_h d_h(s)h_q,\quad
 R_0=Q+\sum_hh_qV_h,\quad
 \mathscr E(U)=\sum_{j=0}^{D}\frac{U^{2j}}{(2j)!}Q^{[D-j]},
 \quad F_0=\mathscr E(0),\quad \mathscr E_2=U^2Q^{[D-1]}/2.
\]

Fix distinct receiving colors \(h,k\) and restrict tensors on \(S_0\) to
that palette. The literal boundary residual is

\[
 B(s)=d_h(s)\mathscr E(U)+\mathscr E_{V_h}(U)
                      -\lambda s_hh^{S_0}.
\]

It is the \(q=h\) slice of \(\mathcal E+\mathcal H\). Its degree-one and
degree-three pieces therefore satisfy
\(\|B_1\|_1\le\xi\), \(\|B_3\|_1\le K_3x^{1/m}\).

Apply the two universal even rotation identities (4) of the exact proof.
Substituting the boundary formula cancels the entire \(d_h\) term and gives

\[
 \lambda s_h[k^{S_0}](\mathscr E-F_0)
 =K(F_0,B(\sqrt2s))/\sqrt2-K(\mathscr E,B(s)).
\]

Taking degree three yields the exact identity, valid on every source,

\[
 \boxed{\lambda s_h[k^{S_0}]\mathscr E_2
       =K(F_0,B_3)-K(\mathscr E_2,B_1).}              \tag{11}
\]

The coefficient of \(K(F_0,B_3)\) is \(2-1=1\); retaining this degree
factor is essential. Direct partial-matching counts give
\(\|F_0\|_1\le H_0\), \(\|\mathscr E_2\|_1\le9H_0\).
Consequently

\[
 \|[k^{S_0}]\mathscr E_2\|_1
 \le H_0(K_3+9P)\ell^{-1}x^{1/m}.                   \tag{12}
\]

We used \(\xi=\ell x\le P x^{1/m}\).

For each color \(h\), let \(M_h[p,r]=A_{pr}(h,h)\), and let
\(C_h[r,q]=\operatorname{haf}(M_h[V\setminus\{r,q\}])\), with zero diagonals.
Also put \(B_{ih}[p,r]=A_{pr}(i,h)\), with zero diagonal. The literal
expansions from the exact proof are still valid. On the diagonal,
\((B_{ih}C_h)[p,p]-\delta_{ih}\lambda\) is a coefficient of \(E\).
Off the diagonal, \((B_{ih}C_h)[p,q]\) is a coefficient of the quadratic
in (12), with a factor two when the two root colors coincide.
It follows that

\[
 \|B_{ih}C_h-\delta_{ih}\lambda I\|_F
 \le G\ell^{-1}x^{1/m}.                             \tag{13}
\]

Indeed each entry is at most
\([2H_0(K_3+9P)+P^2]\ell^{-1}x^{1/m}\); the Frobenius norm of an
\(n\)-by-\(n\) matrix is at most \(n\) times its largest entry.
For diagonal entries use \(\xi=\ell x\le P^2\ell^{-1}x^{1/m}\).

## 5. Quantitative diagonal reduction without a limiting rank assumption

Suppose

\[
 x\le1,\qquad G\ell^{-1}x^{1/m}\le\ell/2.            \tag{14}
\]

For \(i=h\), (13) says that \(M_hC_h\) is within operator norm \(\ell/2\)
of \(\lambda I\). Hence it is invertible, as is \(C_h\), and

\[
 \|C_h^{-1}\|_{\rm op}
 \le(2/\ell)\|M_h\|_{\rm op}\le4/\ell.
\]

The last inequality follows from \(S\le1\) and
\(\|M_h\|_F\le\sqrt2\le2\). For \(i\ne h\), multiply (13) by this inverse.
Let \(A_0\) be the literal diagonal projection of \(A\). The six ordered
matrices \(B_{ih}\), \(i\ne h\), count each off-color source cell twice.
Thus

\[
 \boxed{\|A-A_0\|_{\rm edge}
 \le8G\ell^{-2}(\xi/\ell)^{1/m}.}                  \tag{15}
\]

This estimates the matrix inverse at each source satisfying (14). It does
not assume that the inverse stays bounded at a zero-output limit.
If (14) fails, the physical error already exceeds one of the thresholds
that will be used in the final contradiction.

The pure amplitudes are preserved exactly by the diagonal projection: an
all-\(h\) word uses only \(h,h\) cells. Also \(\|A_0\|_{\rm edge}\le1\).
The matching expansion and the telescoping identity for a product give

\[
 \|H(A)-H(A_0)\|_2\le mP\|A-A_0\|_{\rm edge}.
\]

Each individual edge block has norm at most one, before and after projection.
Each matching contributes at most \(m\|A-A_0\|\), and there are \(P\)
matchings. With \(\epsilon_0=\|H(A_0)-\lambda\Delta\|_2\), (15) gives

\[
 \epsilon_0\le\epsilon+
 L\epsilon^{1/m}\ell^{-2-1/m},\qquad L=24mPG.        \tag{16}
\]

The factor three uses \(\xi^{1/m}\le3\epsilon^{1/m}\).
Equations (14)–(16) are a separate useful approximate-diagonality theorem.

## 6. Combining with the diagonal rate theorem

Use the constants \(c_n\) and amplitude power
\(k=3+3(m-1)/2\) from Section 8 of the diagonal note. Its covariance
projection constant can be taken from the exactly checked table for six,
eight, and ten sites, or from the explicit factorial bound for every size.
Set

\[
 \begin{aligned}
 b&=\min\{c_n,\,1/(2P^{\lceil k-1\rceil})\},\\
 q&=m(k+2)+1=(3m^2+7m+2)/2,\\
 c_n^*&=\min\left\{
 \frac1{3^mP^{\lceil q-1\rceil}},\quad
 \left(\frac1{6GP^{\lceil k\rceil}}\right)^m,\quad
 \frac{b}{4P^{\lceil q-k\rceil}},\quad
 \left(\frac{b}{4L}\right)^m
 \right\}.                                         \tag{17}
 \end{aligned}
\]

All constants are positive and rational. The ceilings merely replace powers
of \(P\ge1\) by integer upper bounds.

Suppose \(\ell>0\) and \(\epsilon<c_n^*\ell^q\). The first term of the
minimum ensures \(x\le1\). Since

\[
 G\ell^{-1}x^{1/m}
 \le3G(c_n^*)^{1/m}\ell^{k+1},
\]

the second term ensures the inverse condition in (14). Equation (16) and
the last two terms give

\[
 \epsilon_0<\tfrac b4\ell^k+\tfrac b4\ell^k
            =\tfrac b2\ell^k\le\ell/4.
\]

Thus \(H(A_0)\ne0\), its pure average is still \(\lambda\), and its
fidelity is at least \(12/13\) (in fact this bound gives \(48/49\)).
Apply the diagonal theorem. If \(S_0=\|A_0\|_{\rm edge}^2\le1\), normalize
it first. Homogeneity gives

\[
 \epsilon_0\ge c_n\ell^k/S_0^{m(k-1)/2}
               \ge c_n\ell^k.
\]

This contradicts \(\epsilon_0<(b/2)\ell^k\) and \(b\le c_n\).
For \(\ell=0\), (1) is immediate. This proves (1).
Substituting \(\epsilon^2=(1-F)R\), \(\ell^2=FR/3\) proves (2).
An overall source rescaling leaves \(F\) and \(R\) unchanged.

## 7. Further consequences

### Any target dimension at least three

The exponent does not deteriorate with the number of target colors. For an
equal \(d\)-color GHZ target, \(d\ge3\), define \(\lambda\) as the average
of its \(d\) pure amplitudes, and \(E=H-\lambda\Delta_d\).
For each three-color subset \(T\), let \(\lambda_T\) be the mean of those
three pure amplitudes. The average of all \(\lambda_T\) is \(\lambda\),
so at least one has \(|\lambda_T|\ge|\lambda|\).

Project every site's coordinates onto that subset. The resulting source
has squared edge norm at most one, and its output is exactly the matching
tensor restricted to words in that subset. Subtracting its own best pure
mean gives error

\[
 \epsilon_T=\|H_T-\lambda_T\Delta_T\|_2
 \le\|H_T-\lambda\Delta_T\|_2\le\epsilon.
\]

The three-color amplitude inequality, extended to squared source norm at
most one by homogeneity, therefore gives
\(\epsilon\ge c_n^*|\lambda|^{q_n}\).
Since \(|\lambda|^2=FR/d\),

\[
 \boxed{R\le
 \left(\frac{d^{q_n}}{(c_n^*)^2}\right)^{\alpha_n}
 \frac{(1-F)^{\alpha_n}}{F^{1+\alpha_n}}.}            \tag{18}
\]

Only the constant changes. This remains the same matching model on the
same sites; it does not introduce auxiliary sites or a new conditioning event.

### A bound on the order of cancellation along a degeneration

Consider an analytic family of sources with a nonzero bounded source limit,
and suppose its pure target amplitude has leading order \(t^r\), while
its target-orthogonal error has leading order \(t^s\). A fixed overall
rescaling puts the family in a bounded source ball. The amplitude inequality
implies

\[
                         s\le q_n r.                \tag{19}
\]

Otherwise the error would vanish faster than the proved lower bound.
Thus, at six sites, the error's vanishing order cannot exceed 25 times the
target amplitude's order. This bound is conservative; the familiar prism
has orders one and three. It nevertheless rules out unlimited improvement
of cancellation order relative to a fixed target order, for every architecture.

## 8. What is established and what is not

The written argument closes the explicit-exponent gap for the full
three-color complex matching model, subject to independent review of this
new quantitative proof and its diagonal predecessor. The exponent at six
sites is \(1/24\), rather than the vastly smaller generic effective-algebra
existence estimate. It is weaker than the diagonal exponent \(1/5\) and
much weaker than the local prism exponent \(1/2\).

The new reusable step is the cubic omission identity (11), combined with
auxiliary rescaling before extracting just the quadratic scalar term.
It gives approximate diagonality without requiring a globally well-conditioned
response. The exact cofactor inverse is used only after the error estimate
makes it legitimate.

This does not establish the conjectured sharp global square-root law.
The constants are too conservative to claim a practical experimental optimum.
It does not extend the source model to ancillas or additional heralding events.
No historical-priority claim is made for standard polynomial stability,
coefficient division, or matrix perturbation methods.

The [replay package](../computations/general-complex-rate-2026-09-26/README.md)
checks literal off-color source expansions, the cubic omission identity,
cofactor polarization factors, finite coefficient division, and the exact
constant budgets. It also checks the three-color subset averaging and
orthogonal-projection identities. It pins its mathematical dependencies.
The arbitrary-size conclusion is supplied by the analytic argument, not by
finite testing.
