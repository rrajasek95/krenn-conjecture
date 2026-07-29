# The eighth split at \(k=3\): nine-double, three-singleton closure

## 1. Result

At \(h=8,k=3\), the collision profile

\[
                              2^9 1^3                     \tag{1}
\]

is impossible on the no-extra-singular residual stratum.  The proof
continues the formal-five-double duality construction.  For every choice
of five double values it produces a two-dimensional relation pencil in
\(\mathbb C[z]_{\le3}\).  The three singleton rows factor the Wronskian
of that pencil as a fixed cubic times a linear polynomial.  The four
outside-double rows then become four Robin equations on that same linear
polynomial.  Varying the five/four partition forces six roots of a
polynomial of degree at most four, and two formal endpoint evaluations
give the final contradiction.

The argument uses only the standing structural assumptions: exceptional
values are distinct and pairwise nonopposite, every repeated exceptional
value is nonzero, and none meets the distinguished poles \(\pm\mu\).
The singleton values themselves need not be nonzero.

## 2. The cubic relation pencil

Let \({\cal D}\) be the set of nine double values and \({\cal R}\) the
set of three singleton values.  Fix a five-set \(T\subset{\cal D}\), put

\[
 Q_T(z)=\prod_{t\in T}(z+t),\qquad
 C(z)=\prod_{u\in{\cal D}\setminus T}(z-u),\qquad
 L(z)=\prod_{r\in{\cal R}}(z-r),                       \tag{2}
\]

and write \(A=C^2L\).  Thus \(A\) has degree eleven and seven distinct
roots.  The formal-five-double theorem gives an exact two-dimensional
space

\[
                    {\cal S}_T\subset\mathbb C[z]_{\le3}. \tag{3}
\]

For every \(S\in{\cal S}_T\), the derivative of the associated dual
rational function is

\[
 G_S'(z)={ (z+\mu)^3Q_T(z)^2S(z)\over C(z)^3L(z)^2}.     \tag{4}
\]

Equation (4) is precisely (15)--(19) of the formal-five-double note with
the repeated-root gcd of \(A\) removed.  Since it is a rational
derivative, its residue at every finite pole is zero.

Choose a basis \(p,q\) of \({\cal S}_T\) and define

\[
                         W_T=pq'-p'q.                    \tag{5}
\]

The basis polynomials are independent, so \(W_T\ne0\), and cancellation
of the top derivative terms gives

\[
                         \deg W_T\le 2\cdot3-2=4.        \tag{6}
\]

## 3. The singleton rows

At a singleton \(r\in{\cal R}\), factor (4) as

\[
                         {B_r(z)S(z)\over(z-r)^2},       \tag{7}
\]

where \(B_r(r)\ne0\).  Its residue is zero exactly when

\[
                         S'(r)+Y_rS(r)=0,
             \qquad Y_r={B_r'(r)\over B_r(r)}.           \tag{8}
\]

Both \(p\) and \(q\) satisfy (8), hence \(W_T(r)=0\).  This holds at all
three distinct singleton values.  From (6),

\[
                         W_T(z)=L(z)H_T(z),
             \qquad 0\ne H_T\in\mathbb C[z]_{\le1}.     \tag{9}
\]

No division by a singleton value occurs here, so (9) also covers a zero
singleton.

## 4. The outside-double rows

Fix \(u\in{\cal D}\setminus T\), write \(C=(z-u)C_u\), and put

\[
 B_u(z)={ (z+\mu)^3Q_T(z)^2\over C_u(z)^3L(z)^2},
 \qquad X_u={B_u'(u)\over B_u(u)}.                       \tag{10}
\]

The pole in (4) at \(u\) has order three.  Its zero-residue equation is

\[
 S''(u)+2X_uS'(u)+Z_uS(u)=0,
 \qquad Z_u={B_u''(u)\over B_u(u)}.                      \tag{11}
\]

Applying (11) to \(p,q\) and differentiating (5) gives

\[
                         W_T'(u)+2X_uW_T(u)=0.           \tag{12}
\]

Substitution of (9), followed only by division by the nonzero number
\(L(u)\), turns (12) into a Robin row on the same linear polynomial:

\[
                         H_T'(u)+\Theta_uH_T(u)=0,       \tag{13}
\]

where logarithmic differentiation of (10) yields

\[
 \Theta_u={6\over u+\mu}
     +4\sum_{t\in T}{1\over u+t}
     -6\sum_{x\in({\cal D}\setminus T)\setminus\{u\}}
                    {1\over u-x}
     -3\sum_{r\in{\cal R}}{1\over u-r}.                \tag{14}
\]

In the basis \(1,z\) of \(\mathbb C[z]_{\le1}\), row (13) is

\[
                         (\Theta_u,\ 1+u\Theta_u).       \tag{15}
\]

It is never the zero row.  All four outside-double rows annihilate the
same nonzero \(H_T\), so they are proportional.  In particular, for any
two outside doubles \(u,v\),

\[
 \Theta_u-\Theta_v+(v-u)\Theta_u\Theta_v=0.              \tag{16}
\]

## 5. Moving the fourth outside double

Fix three distinct double values \(u,v,a\).  Let \(b\) range through the
remaining six members of \({\cal D}\).  For each such \(b\), take

\[
                    {\cal D}\setminus T=\{u,v,a,b\}.   \tag{17}
\]

All terms in (14) except those involving \(b\) can be absorbed into
constants \(K_u,K_v\).  Thus

\[
 \Theta_u(b)=K_u-2\Phi_u(b),\qquad
 \Theta_v(b)=K_v-2\Phi_v(b),                            \tag{18}
\]

with

\[
 \Phi_u(b)={2\over u+b}+{3\over u-b}
           ={5u+b\over u^2-b^2}.                        \tag{19}
\]

Set

\[
\begin{aligned}
 D_u(b)&=u^2-b^2,&
 N_u(b)&=K_uD_u(b)-2(5u+b),\\
 D_v(b)&=v^2-b^2,&
 N_v(b)&=K_vD_v(b)-2(5v+b).
\end{aligned}                                           \tag{20}
\]

Clearing the nonzero denominators in (16) gives

\[
 \widehat D(b)=N_uD_v-N_vD_u+(v-u)N_uN_v=0.             \tag{21}
\]

The left side has degree at most four in \(b\).  It vanishes at the six
distinct choices in (17), hence it is the zero polynomial.

Evaluate this polynomial identity at the two formal endpoints \(b=u\)
and \(b=-u\).  Here

\[
 D_u(\pm u)=0,\qquad N_u(u)=-12u,qquad N_u(-u)=-8u,     \tag{22}
\]

and both latter numbers are nonzero because a double value is
structurally nonzero.  Equation (21) therefore gives

\[
 D_v(u)+(v-u)N_v(u)=0,
 \qquad D_v(-u)+(v-u)N_v(-u)=0.                         \tag{23}
\]

But \(D_v(u)=D_v(-u)\), whereas

\[
                         N_v(u)-N_v(-u)=-4u.             \tag{24}
\]

Subtracting (23) yields \(-4u(v-u)=0\), contrary to
\(u\ne0\) and \(v\ne u\).  This proves (1).

The substitutions \(b=\pm u\) are made only after (21) has become a
polynomial identity; they do not assert that either endpoint is an
admissible moving value.  Pairwise nonoppositeness ensures all
denominators used before clearing are nonzero.

## 6. Exact audit

[verify_live_three_zero_eighth_split_k3_nine_double_three_singleton_closure.py](../computations/verify_live_three_zero_eighth_split_k3_nine_double_three_singleton_closure.py)
checks the core and complementary degrees, all \(\binom94\) five/four
partitions, the singleton and double-pole residue identities, the
Wronskian reduction, the logarithmic coefficient (14), the separation
(18), the quartic degree bound, and the endpoint contradiction
(22)--(24).
