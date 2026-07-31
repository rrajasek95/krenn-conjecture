# Diagonal anchors leave a two-arm common-coloop resultant boundary

## 1. Outcome

Retain the common-coloop notation on \(2h\) residual sites,

\[
 a_{ij}q^{[h]}+p_i s_jq^{[h-1]}=\delta_{ij}X_i,
 \qquad 0\le i,j\le2,                                      \tag{1}
\]

and the aligned one-corner affine fibre from
[the clean-fibre reduction](common-coloop-clean-cap-affine-fibre.md).
Let \(t\) be its missing label.  This note gives one positive reduction
and one sharp near-full-nine guard.

At \(h=3\), write

\[
 D_{\bar K}(z)=z\bar r q_0+\bar r^{[2]}.
\]

The exact missing-axis equation is

\[
 \Theta_t(z)=zU_t+V_t=0,                                   \tag{2}
\]

where

\[
 U_t=\chi_t\bar r q_0+\rho_t\bar r^{[2]},
 \qquad V_t=\chi_t\bar r^{[2]}.                            \tag{3}
\]

Thus two literal coefficient rows at the **same attainable scalar** give
an ordinary \(2\)-by-\(2\) resultant.  For coefficient functionals
\(\lambda_1,\lambda_2\), put

\[
 u_i=\lambda_i(U_t),\qquad v_i=\lambda_i(V_t),\qquad
 \Delta_{12}=u_1v_2-u_2v_1.                                \tag{4}
\]

Every clean cap in the fibre satisfies

\[
 \boxed{\Delta_{12}=0.}                                    \tag{5}
\]

If \(\Delta_{12}\ne0\), the two coefficient rows exclude the fibre.
If the coefficient matrix is nonzero and has rank one, it leaves at most
one candidate \(z\), which must still be attainable, nonzero, solve the
full tensor equation, and avoid all three diagonal activity hyperplanes.
The two nonmissing diagonal target words give canonical choices
\(\lambda_r=[Y_r]\) and \(\lambda_s=[Y_s]\).  The full-nine equations do
not automatically make either choice detect (3); detection is the positive
subcase, not a hidden conclusion.

On two synchronized physical charts, write their attainable scalars along
one physical line parameter \(\tau\) as

\[
 z_\nu(\tau)=a_\nu\tau+b_\nu\qquad(\nu=1,2).                \tag{6}
\]

After any source-provenant coefficient extraction, the two equations are

\[
 f_\nu(\tau)=a_\nu u_\nu\tau+(b_\nu u_\nu+v_\nu)=0.        \tag{7}
\]

Consequently a common cap forces the line-dependent resultant

\[
 \boxed{
 (a_1u_1)(b_2u_2+v_2)-(a_2u_2)(b_1u_1+v_1)=0.}             \tag{8}
\]

For a literally shared scalar \(z=\tau\), (8) is (5).  This is a
pre-\(A\) statement: \((U_t,V_t)\) retain the actual tensors
\(\bar r^{[2]}\) and \(\bar r q_0\).  No factor
\(A=q_0^{[2]}\) is cancelled.

The guard in Section 4 shows exactly how much full-nine input is still
missing.  It is a literal common-coloop (7/9) packet with all three
diagonal anchors and four off-diagonal rows exact, but

\[
                  \rho_2\bar r^{[2]}=2Y_2\ne0.              \tag{9}
\]

Its only failed rows are the two arms \((0,2)\) and \((2,1)\).  Their
response parts are the two images \(e_0^{(x)}\bar s_2A\) and
\(e_1^{(x)}\bar p_2A\); on the zero-top \(A\)-annihilation subbranch the
corresponding full rows force \(\bar s_2A=\bar p_2A=0\).  With nonzero top,
the direct terms must instead be retained in the same arm equations.  This
is complementary to the exact \(A\)-annihilation counterguard in
[the previous overlap attack](common-coloop-a-to-D-overlap-attack.md): that
guard has the two annihilations and the missing diagonal anchor, but omits
the two other diagonal targets.  Neither half controls (9).  The first
untested compatibility is their **simultaneous source-provenant
interaction before multiplication by \(A\)**.

No full-nine active cap is constructed or excluded here, and Krenn's
conjecture remains open.

## 2. The coefficient and line-resultant reductions

Equation (2) is the \(h=3\) specialization of the exact projected equation
in the previous attack.  Applying \(\lambda_i\) gives

\[
                         zu_i+v_i=0.                          \tag{10}
\]

Two equations (10) have a common solution only if their augmented
coefficient rows are dependent, proving (5).  When some \(u_i\ne0\), the
only candidate is \(z=-v_i/u_i\); the other row agrees with it precisely
when (5) holds.  If both slopes vanish, both constants must vanish.  This
proves every rank case without treating \(z\) as independent of the
affine fibre.

Substitution of (6) into (10) gives (7).  The determinant of its two
coefficient rows is (8), proving the two-chart assertion.  A nonflat
physical overlap becomes useful here only if its literal coefficient row
makes this determinant nonzero, or reduces the common candidate to an
inactive value.  Power-free connection transport by itself need not do
so; it may carry the same row on both charts.

In the curvature-only subcase \(\chi_t=0\), equation (2) becomes

\[
                       \Theta_t(z)=z\rho_t\bar r^{[2]}.       \tag{11}
\]

Hence a clean cap with \(z\ne0\) forces the full tensor
\(\rho_t\bar r^{[2]}\) to vanish.  A nonzero value under either literal
anchor coefficient is already a positive exclusion.  Conversely,
vanishing under two coefficient functionals does not imply tensor
vanishing; this note does not revive the false \(A\)-only lemma.

## 3. Uniform order

For arbitrary \(h\ge3\), write

\[
                   \Theta_t(z)=\sum_{k=0}^{h-2}T_kz^k.       \tag{12}
\]

Exact divided-power expansion gives

\[
 \begin{aligned}
 T_0&=\chi_t\bar r^{[h-1]},\\
 T_k&=\chi_t\bar r^{[h-1-k]}q_0^{[k]}
       +\rho_t\bar r^{[h-k]}q_0^{[k-1]}
                       &&(1\le k\le h-2).                    \tag{13}
 \end{aligned}
\]

There are no ordinary binomial coefficients.  After substituting an
attainable affine line and applying literal coefficient functionals, two
charts give scalar polynomials of degree at most \(h-2\).  A common cap
forces their actual-degree Sylvester resultant to vanish.  Degree drops,
zero polynomials, the inactive root, and the three diagonal hyperplanes
must be handled on their separate strata.  Thus the uniform mechanism is
a bounded coefficient/resultant test, not cancellation of a common power.

What remains to prove uniformly is that the two arm rows together with the
two nonmissing diagonal representatives, or a genuinely nonflat overlap
row, supply a detecting coefficient or a decisive resultant.

## 4. A literal diagonal-complete \(7/9\) guard at \(h=3\)

Use residual sites in the order

\[
                         (x,1,2,3,4,5)
\]

and fixed colour axes \(e_i^{(y)}\).  Write \(e^i_{uv}\) for the pure
colour-\(i\) quadratic cell on \((u,v)\).  Set

\[
 \begin{aligned}
 q={}&e^0_{12}+e^0_{45}+e^1_{25}+e^1_{34}
                 +e^2_{x5}+e^2_{13},\\
 p_0={}&e_0^{(x)},&p_1={}&e_1^{(1)},
 &p_2={}&e_2^{(1)}+e_2^{(2)},\\
 s_0={}&e_0^{(3)},&s_1={}&e_1^{(x)},
 &s_2={}&e_2^{(3)}+e_2^{(4)},                                \tag{14}
 \end{aligned}
\]

and take the direct matrix \(a=0\).  Both endpoint triples are injective.
Away from \(x\), their ranks are two and their kernel lines are

\[
                         \mathbb Ce_0,\qquad\mathbb Ce_1.    \tag{15}
\]

Thus \(t=2\) is the aligned missing label.

Direct divided-power multiplication gives the complete pair-row table

\[
\begin{array}{c|ccc}
 &0&1&2\\ \hline
0&000000&0&000200+021221\\
1&0&111111&0\\
2&0&121111+122200&222222.
\end{array}                                                   \tag{16}
\]

Words are displayed in the site order above and every coefficient is one.
Thus all three diagonal rows and the four rows

\[
                     01,\ 10,\ 12,\ 20                       \tag{17}
\]

are exact.  Precisely the two arms \(02\) and \(21\) fail.  Also

\[
                         q^{[3]}=200112,                       \tag{18}
\]

which is harmless in the seven exact rows because \(a=0\).  The guard does
not claim an active direct scalar.

Expose \(x\):

\[
 \begin{aligned}
 q_0&=e^0_{12}+e^0_{45}+e^1_{25}+e^1_{34}+e^2_{13},\\
 \rho&=e_2^{(x)}\rho_2,\qquad \rho_2=e_2^{(5)},\\
 \bar p_2&=e_2^{(1)}+e_2^{(2)},\qquad
 \bar s_2=e_2^{(3)}+e_2^{(4)},\qquad
 \bar r=\bar p_2\bar s_2.                                  \tag{19}
 \end{aligned}
\]

With \(A=q_0^{[2]}\), exact multiplication gives

\[
 \begin{aligned}
 \rho_2\bar r q_0&=Y_2,\\
 \rho_2\bar r^{[2]}&=2Y_2,                                  \tag{20}\\
 \bar s_2A&=00200+21221,\\
 \bar p_2A&=21111+22200.
 \end{aligned}
\]

The last two lines become exactly the two failed rows in (16) after
multiplication by the local kernel axes \(e_0^{(x)}\) and \(e_1^{(x)}\).
They show why this is a two-arm boundary rather than a counterexample to
the full-nine system.

The dependency-free checker
[verify_common_coloop_diagonal_arm_resultant_boundary.py](../computations/verify_common_coloop_diagonal_arm_resultant_boundary.py)
audits every tensor in (16), the endpoint ranks and kernels, (18)--(20),
the affine \(h=3\) determinant, and Sylvester common-root tests through
\(h=8\).  It uses exact rational arithmetic, explicit runtime failures,
and remains active under optimized Python.
