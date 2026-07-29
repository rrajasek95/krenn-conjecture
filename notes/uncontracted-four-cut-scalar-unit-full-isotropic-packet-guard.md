# The scalar-unit E1 boundary survives every isotropic dressed row

## 1. Outcome

The isotropic dressed-cap export is ternary unless the contracted direct
block is a scalar matrix unit.  This note gives an exact guard at that sharp
boundary.  It satisfies the **entire family** of nine-row packets for every
isotropic contraction, even after both opposite \(x\)- and \(y\)-star
triples are made injective, dense on the core, and diagonally
product-active.

Work at \(m=5\), so the common complement \(D\) has six sites
\(\{0,1,2,3,4,5\}\), and take

\[
                         U=E_{22}.                     \tag{1}
\]

For arbitrary \(\alpha,\beta\in\mathbb C^3\), isotropy is exactly

\[
                 \alpha^{\mathsf T}U\beta
                    =\alpha_2\beta_2=0.                \tag{2}
\]

Let \(A=(a_{ab})\) be completely arbitrary.  The construction below has a
nonzero second divided power \(z^{[2]}\), but its dressed multiplier obeys

\[
                         F_{\alpha,\beta}z=0.           \tag{3}
\]

Consequently the arbitrary direct block \(A\) is invisible in all nine
dressed rows.

**Theorem 1.1 (full-isotropic-packet guard).**  The data in Section 2
satisfy, for every pair \(\alpha,\beta\) obeying (2), all nine equations

\[
 F_{\alpha,\beta}
    \left(x_ay_b+\frac{a_{ab}}2z\right)
       =\delta_{ab}\alpha_a\beta_aX_a^D,
       \qquad 0\leq a,b\leq2.                           \tag{4}
\]

The same remains true after the core-supported padding in Section 4.  For
the padded rows:

1. every \(x_a\) and every \(y_b\) is supported on at least three sites;
2. both triples \((x_0,x_1,x_2)\) and \((y_0,y_1,y_2)\) are injective; and
3. every diagonal product \(x_cy_c\) is nonzero.

If one formally continues the nine displayed equations (4) beyond their
isotropic domain, the other eight positions still hold, while the
\((2,2)\) position fails by exactly

\[
                         -\alpha_2\beta_2X_2^D.         \tag{5}
\]

Thus the coefficient suppressed by isotropy is the literal blind spot of
the *packet (4)*.  This does not say that the construction satisfies the
full non-isotropic contraction of the original 81 rows.  It is a guard
against an E1 proof move, not an exact Krenn source or a counterexample to
the conjecture.

## 2. The six-site packet

Write \(e_c^{(i)}\) for colour \(c\) at site \(i\), with products at a
repeated physical site equal to zero.  Put

\[
 z=e_0^{(2)}e_0^{(3)}+e_1^{(0)}e_1^{(4)},              \tag{6}
\]

\[
\begin{array}{c|ccc}
c&0&1&2\\ \hline
t_c&e_0^{(0)}&e_1^{(1)}&0\\
v_c&e_0^{(1)}&e_1^{(2)}&0,
\end{array}                                             \tag{7}
\]

and take the basic opposite stars

\[
\begin{array}{c|ccc}
c&0&1&2\\ \hline
x_c&e_0^{(4)}&e_1^{(5)}&0\\
y_c&e_0^{(5)}&e_1^{(3)}&0.
\end{array}                                             \tag{8}
\]

For a contraction pair define

\[
 T=\sum_c\alpha_ct_c,\qquad
 V=\sum_c\beta_cv_c,\qquad
 F_{\alpha,\beta}=TVz.                                 \tag{9}
\]

This is exactly the dressed multiplier
\(TVz^{[m-4]}\) at \(m=5\).  The coefficient in front of \(z\) in (4) is
\((m-3)^{-1}=1/2\).

The quadratic in (6) is not power-degenerate.  Its two cells are disjoint,
so

\[
 z^{[2]}
 =e_1^{(0)}e_0^{(2)}e_0^{(3)}e_1^{(4)}
 \ne0.                                                  \tag{10}
\]

## 3. Exact verification of every isotropic packet

Expand (9).  The mixed pair \(t_0v_1\) collides with both cells of \(z\),
while \(t_1v_0=0\) already at site \(1\).  The two surviving terms are

\[
 F_{\alpha,\beta}
  =\alpha_0\beta_0
       e_0^{(0)}e_0^{(1)}e_0^{(2)}e_0^{(3)}
   +\alpha_1\beta_1
       e_1^{(0)}e_1^{(1)}e_1^{(2)}e_1^{(4)}.           \tag{11}
\]

Each monomial in (11) collides with each cell of \(z\).  This proves (3),
despite (10).

The basic rows (8) complete the two surviving monomials in exactly one
way:

\[
\begin{aligned}
 F_{\alpha,\beta}x_0y_0&=\alpha_0\beta_0X_0^D,\\
 F_{\alpha,\beta}x_1y_1&=\alpha_1\beta_1X_1^D.         \tag{12}
\end{aligned}
\]

The unwanted summand in the first line collides at site \(4\), and the
unwanted summand in the second line collides at site \(3\).  The two
off-diagonal products vanish for equally literal reasons:

\[
 F_{\alpha,\beta}x_0y_1=0,\qquad
 x_1y_0=0.                                             \tag{13}
\]

In the first equation of (13), the colour-zero term of \(F\) collides at
site \(3\) and the colour-one term collides at site \(4\).  In the second,
both displayed forms occupy site \(5\).  Every row involving index \(2\)
has zero basic product.

Equation (3) removes \(a_{ab}z/2\) for every choice of \(A\).  Equations
(12)--(13) therefore prove all rows of (4), except that the \((2,2)\)
difference is

\[
 0-\alpha_2\beta_2X_2^D.                               \tag{14}
\]

Under (2), (14) vanishes.  In the formal continuation of (4), it is nonzero
without isotropy, proving (5), and it is the only residual among those nine
continued equations.  The uncontracted 81-row identity has additional
terms proportional to \(\alpha^{\mathsf T}U\beta\), so this sentence makes
no claim about its non-isotropic residuals.

## 4. Dense injective padding is invisible

Let the core be

\[
                         C=\{0,1,2\}.                  \tag{15}
\]

For \(0\leq a,b\leq2\), define

\[
\begin{aligned}
 K_a&=e_a^{(0)}+e_a^{(1)}+e_a^{(2)},\\
 L_b&=e_b^{(0)}+2e_b^{(1)}+4e_b^{(2)},                 \tag{16}
\end{aligned}
\]

and replace the basic rows by

\[
                         \widetilde x_a=x_a+K_a,\qquad
                         \widetilde y_b=y_b+L_b.        \tag{17}
\]

Every monomial of \(F_{\alpha,\beta}\) in (11) occupies all three core
sites.  Hence

\[
 F_{\alpha,\beta}K_a=F_{\alpha,\beta}L_b=0             \tag{18}
\]

for every \(a,b,\alpha,\beta\).  Expanding (17) and using (18) gives

\[
 F_{\alpha,\beta}\widetilde x_a\widetilde y_b
                         =F_{\alpha,\beta}x_ay_b.       \tag{19}
\]

Thus padding changes none of the packets, including the exact blind spot
(14).

Each form in (17) is nonzero at sites \(0,1,2\), so every row has support
at least three.  At site \(0\), the three \(K_a\)'s and the three \(L_b\)'s
restrict respectively to the basis triples

\[
                         (e_0,e_1,e_2),\qquad
                         (e_0,e_1,e_2).                 \tag{20}
\]

Projection to that site proves injectivity of both triples.  Finally, the
coefficient of \(e_c^{(0)}e_c^{(1)}\) in
\(\widetilde x_c\widetilde y_c\) is

\[
                         1\cdot2+1\cdot1=3,             \tag{21}
\]

and no basic row has a core-core term which could cancel it.  Hence every
diagonal product is nonzero.

The padding shows that support size, injectivity of the two open star
triples, and nonvanishing of \(x_cy_c\) do not recover the coefficient
omitted from the isotropic packets.

## 5. The proof move that remains

The guard diagnoses the scalar-unit boundary precisely.  Every isotropic
contraction of \(U=E_{22}\) erases the coefficient
\(\alpha_2\beta_2\), while the multiplier is allowed to annihilate the
dressed direct term through \(Fz=0\).  Dense padding supplies no remedy.

A successful continuation must therefore retain information which is not
present in the isotropic packets alone.  Concretely, it must do at least
one of the following:

1. couple the uncontracted \(E_{22}\) row to the zero-star selectors or to
   another overlapping packet; or
2. rule out the common-power degeneration
   \[
                         t_cv_cz^{[m-3]}=0              \tag{22}
   \]
   in the scalar-unit colour.

For the displayed guard, \(c=2\) and \(t_2=v_2=0\), so (22) is exactly
where the missing coefficient can hide.  Any argument using only (4), even
for all isotropic \(\alpha,\beta\), cannot see it.

The model does not satisfy the complete four-cut equality and does not
have the connected-spanning-nonbipartite rank-three graph used to reach the
active E1 chart; its rank-three internal graph is empty.  Those provenance
conditions, or another overlapping selector packet, may therefore supply
precisely the information absent from (4).

## 6. Audit

The dependency-free checker
[verify_uncontracted_four_cut_scalar_unit_full_isotropic_packet_guard.py](../computations/verify_uncontracted_four_cut_scalar_unit_full_isotropic_packet_guard.py)
verifies \(z^{[2]}\ne0\) and \(Fz=0\) exactly, then audits (11)--(14) as
formal bilinear polynomials in \(\alpha,\beta\) against two independent test
blocks \(A\).  It also checks the core-annihilation identities, support
counts, triple ranks, nonzero diagonal products, and the unique
formally continued \((2,2)\) residual.  Independence from arbitrary \(A\) follows
symbolically from \(Fz=0\); the universal conclusions are the coefficient
proof above, not a numerical sample.
