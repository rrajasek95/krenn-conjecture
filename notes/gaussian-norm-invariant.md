# Hermitian cofactor gaps and exterior-power norm barriers

Let (B) have even cardinality (n=2m), let (V_v=mathbb C^3), and
write

\[
 H_B(A)=\sum_{M\in\mathcal M(B)}\bigotimes_{e\in M}A_e.
\tag{1}
\]

This note tests whether Hermitian positivity can upgrade the minimal-norm
normal form into rank-one edges or three source-disjoint perfect matchings.
There is one useful equality-case lemma: every vertex/color port has a
canonical nonnegative *cofactor gap*, and simultaneous equality forces the
whole source to be diagonal.  The equality is not automatic.  An exact
active binary GHZ gadget has strict gaps, while the balanced phased
Fourier/anchor local minimum has gap (34) at every port.

The two- and three-copy exterior invariants have an additional, decisive
problem.  A product of full-rank Bell tensors on just one perfect matching
is locally isotropic, has the same norm and one-site reduced Gram matrices
as GHZ after scaling, and gives *larger* exterior invariants.  Its local
Cauchy--Binet equality uses three factor labels on the same edge, and its
matching expansion uses only ((M,M,M)).  Thus these positivity inequalities
do not have an equality case that forces source-disjoint matchings.

## 1. The portwise cofactor gap

Orient (A_{uv}) so that vertex (v) is its row endpoint and denote the
result by (A_{v|u}).  For a vertex (v), a color (i), and (u\ne v),
put

\[
 a_u=A_{v|u}(i,i),\qquad
 h_u=H_{B\setminus\{v,u\}}(A)_{i^{n-2}},                 \tag{2}
\]

and define

\[
 s_{v,i}=\sum_{u\ne v}|h_u|^2,\qquad
 o_{v,i}=\sum_{u\ne v}\sum_{j\ne i}|A_{v|u}(i,j)|^2.  \tag{3}
\]

Partitioning the constant-(i) coefficient by the edge incident to (v)
gives the exact equation

\[
                         \sum_{u\ne v}a_uh_u=1.          \tag{4}
\]

Suppose the source is target-torus balanced, so that

\[
 \sum_{u\ne v}\sum_j|A_{v|u}(i,j)|^2=c_i               \tag{5}
\]

is independent of (v).  A minimum of the Frobenius norm on the exact
fiber has (5), without any smoothness assumption.

**Lemma 1.1 (Hermitian cofactor-gap identity).**  Every balanced exact
source satisfies

\[
 \boxed{\quad
 c_i s_{v,i}-1
 =s_{v,i}o_{v,i}
   +\left\|a\wedge\overline h\right\|^2
 \ge 0.\quad}                                             \tag{6}
\]

Here (a=(a_u)_{u\ne v}), (overline h=(\overline{h_u})_{u\ne v}),
and the exterior norm is the standard Hermitian one.

**Proof.**  Equation (5) says

\[
 c_i=\|a\|^2+o_{v,i}.
\]

With the Hermitian inner product linear in the second argument, (4) says

\[
 \langle\overline h,a\rangle=1.
\]

The Gram-determinant identity

\[
 \|a\wedge\overline h\|^2
 =\|a\|^2\|h\|^2-|\langle\overline h,a\rangle|^2
\]

now gives (6).  `QED`

Since (4) makes (s_{v,i}>0), equality in (6) holds precisely when

\[
 A_{v|u}(i,j)=0\quad(j\ne i),\qquad
                         a\parallel\overline h.           \tag{7}
\]

Consequently, if all (3n) gaps vanish, every aggregate edge matrix is
diagonal.  This is a real reduction, although it does not by itself force
the diagonal matrices to have rank one.

There is an equivalent frame-operator interpretation at a norm-minimum.
For fixed (v), put

\[
 \beta_{u,j}=e_j^{(u)}\otimes H_{B\setminus\{v,u\}}(A)
       \in\bigotimes_{x\ne v}V_x
\]

and let (S_v=\sum_{u,j}|\beta_{u,j}\rangle
\langle\beta_{u,j}|).  The row-(i) star equation is a coefficient
representation of (z_i=e_i^{\otimes(B\setminus v)}) in this frame.
The exact star normal equation says it is the least-norm representation,
so

\[
 c_i=\langle z_i,S_v^+z_i\rangle,\qquad
 s_{v,i}=\langle z_i,S_vz_i\rangle.                       \tag{8}
\]

The operator Cauchy--Schwarz inequality gives their product at least one.
Equality holds exactly when (z_i) is an eigenvector of (S_v) on its
support.  In other words, (6) measures the coupling between the constant
GHZ direction and the mixed cofactor sector.  The missing uniform theorem
would have to show that all of those couplings vanish simultaneously.

## 2. Exact adversarial values of the gap

The active six-vertex binary gadget

\[
\begin{array}{c|c@{\qquad}c|c}
01&E_{00}&23&I_2\\
02&-e_0e_1^{\mathsf T}&13&e_0e_1^{\mathsf T}\\
45&E_{00}&05&E_{11}\\
12&E_{11}&34&E_{11}
\end{array}                                                \tag{9}
\]

has output (Delta_{6,2}), and every displayed edge has a nonzero tensor
cofactor.  Lemma 1.1 itself does not require balance if (c_i) is replaced
by the actual port row energy.  Its strict gaps are

\[
\begin{array}{c|c}
(v,i)&d_{v,i}s_{v,i}-1\\ \hline
(0,0),(1,0),(1,1),(4,1)&1\\
(2,1),(3,1)&2,
\end{array}                                                \tag{10}
\]

and all other ports have gap zero.  At ((0,0),(1,0),(2,1),(3,1)) the
strictness includes off-diagonal row energy; at ((1,1),(4,1)) it is pure
diagonal/cofactor misalignment.  Thus exact vanishing of every mixed output
coefficient does not make the gap vanish at an arbitrary tensor-active
source.  This particular source is not a norm minimum: its known
norm-lowering star replacement removes the rank-two edge and all the
cancellation overhead.

The phased six-vertex Fourier/anchor model gives the complementary test.
It is fully isotropic with (c=7), has all three complete constant
coefficients equal to one, has injective star and triangle maps, and is a
smooth local norm minimum for the fiber of its own output.  Exact
Eisenstein-integer calculation gives, at every one of its (18) ports,

\[
 s_{v,i}=5,\qquad o_{v,i}=4,\qquad
 c s_{v,i}-1=34=5\cdot4+14.                               \tag{11}
\]

It even contains the explicit selected mixed fiber
(\omega+\omega^2+1=0).  It does not have GHZ output: other mixed
coefficients remain nonzero.  Therefore (11) does not refute a theorem
using *all* mixed equations at once.  It does prove that balance, local
minimality, exact constant fibers, block normal equations, and an actual
mixed cancellation do not force the Hermitian equality case.

## 3. Squared matching norms retain destructive interference

Let

\[
 t_M=\bigotimes_{e\in M}A_e,\qquad
 D(A)=\sum_M\|t_M\|^2
     =\sum_M\prod_{e\in M}\|A_e\|_F^2.                  \tag{12}
\]

Then

\[
 \|H_B(A)\|^2=D(A)+\sum_{M\ne N}\langle t_N,t_M\rangle.\tag{13}
\]

The positive diagonal (D(A)) does not control the sign of the second
term.  In the exact binary gadget (9), the three supported matching tensors
are

\[
 e_0^{\otimes6}+e_0e_0e_1e_1e_0e_0,\quad
 -e_0e_0e_1e_1e_0e_0,\quad e_1^{\otimes6}.               \tag{14}
\]

Hence (D=4), while (|H|^2=2); the ordered cross term is (-2).

In the phased Fourier/anchor local minimum, a perfect matching containing
(k) Fourier edges has squared norm (9^k).  Among the fifteen perfect
matchings of (K_6), the multiplicities for (k=0,1,2,3) are respectively
(4,6,3,2).  Therefore

\[
 D=4+6\cdot9+3\cdot9^2+2\cdot9^3=1759,                  \tag{15}
\]

whereas exact summation of all (729) output coefficients gives

\[
                         \|H\|^2=1529.                   \tag{16}
\]

The ordered cross term is (-230), even at this smooth balanced local
minimum.  Positivity of (12) therefore cannot be localized to individual
mixed fibers or alternating-cycle orbits.

## 4. The two-copy alternating norm is a purity polynomial

Let (W:V\otimes V\to\bigwedge^2V) be (W(x\otimes y)=x\wedge y), and
define the even-order quadratic covariant

\[
 \mathcal A_2(T)=W^{\otimes B}(T\otimes T)
       \in\bigotimes_{v\in B}\bigwedge^2V_v.             \tag{17}
\]

For (S\subseteq B), let

\[
 \rho_S(T)=\operatorname {Tr}_{B\setminus S}|T\rangle
                                      \langle T|.
\]

**Lemma 4.1 (swap expansion).**

\[
 \boxed{\quad
 \|\mathcal A_2(T)\|^2
   =\sum_{S\subseteq B}(-1)^{|S|}\operatorname {Tr}\rho_S(T)^2.
 \quad}                                                   \tag{18}
\]

**Proof.**  If (F_v) swaps the two copies at site (v), then
(W^*W=I-F_v).  Expanding

\[
 \langle T^{\otimes2},\prod_v(I-F_v)T^{\otimes2}\rangle
\]

and using the swap identity

\[
 \langle T^{\otimes2},F_ST^{\otimes2}\rangle
                         =\operatorname {Tr}\rho_S(T)^2
\]

proves (18).  `QED`

For (T=Delta_{B,3}), the empty and full reductions have purity (9),
and every nonempty proper reduction has purity (3).  Since (n) is even,
(18) gives

\[
                     \|\mathcal A_2(\Delta_{B,3})\|^2=12.\tag{19}
\]

Equivalently,

\[
 \mathcal A_2(\Delta_{B,3})
 =2\sum_{0\le i<j\le2}(e_i\wedge e_j)^{\otimes B}.       \tag{20}
\]

This is an exact positive invariant, but the next example shows that GHZ
is not its extremal isotropic equality case.

## 5. One full-rank matching beats GHZ in both exterior invariants

Fix one perfect matching (M), and put

\[
 \Omega_M=\bigotimes_{uv\in M}
              (e_0e_0+e_1e_1+e_2e_2)_{uv}.              \tag{21}
\]

This is itself a matching tensor: put (I_3) on the edges of (M) and
zero elsewhere.  It has only one supported perfect matching.  The
unscaled tensor already has all three constant coefficients equal to one
and its source is locally isotropic, (R_v=I_3).

To compare output Hermitian data with GHZ, scale it to

\[
 T_M=3^{(1-m)/2}\Omega_M.                                \tag{22}
\]

Distribute the scalar equally over the (m) edge matrices if a common
source isotropy constant is desired.  Direct contraction gives

\[
 \|T_M\|^2=3,\qquad \rho_v(T_M)=I_3\quad(v\in B).         \tag{23}
\]

Thus (T_M) has exactly the same norm and all one-site reduced Gram
matrices as (Delta_{B,3}).

On one Bell edge the raw two-copy covariant has squared norm (12), and
the raw three-copy alternating contraction is

\[
 \epsilon^{\otimes\{u,v\}}(I_3,I_3,I_3)=6.               \tag{24}
\]

Both quantities tensor-multiply over (M).  Accounting for the quadratic
and cubic scaling in (22) gives

\[
 \boxed{\quad
 \|\mathcal A_2(T_M)\|^2
       =9\left(\frac43\right)^m,
 \qquad
 I_B(T_M)=6\left(\frac2{\sqrt3}\right)^{m-1}.
 \quad}                                                   \tag{25}
\]

For GHZ the corresponding values are (12) and (6).  Hence for every
(m\ge2), the full-rank one-matching tensor has strictly larger values
despite (23).  At the first conjecturally relevant order, (n=6), its
values are

\[
                   \|\mathcal A_2(T_M)\|^2=\frac{64}{3},
 \qquad I_B(T_M)=8.                                      \tag{26}
\]

GHZ is not a lower exterior-invariant equality case either.  At (n=6),
take the two alternating one-factors

\[
 P=01|23|45,\qquad Q=05|12|34.                            \tag{26a}
\]

Their union is one Hamilton cycle, so it has exactly the two perfect
matchings (P,Q).  Put scalar identity matrices on its edges, with the
edge products chosen so that the two matching tensors are
(\Omega_P) and (-\Omega_Q).  Thus this is an aggregate matching source
with output

\[
                         T_-={1\over4}(\Omega_P-\Omega_Q).\tag{26b}
\]

The unscaled difference has squared norm (48) and every one-site reduced
Gram matrix is (16I_3).  Consequently

\[
                 \|T_-\|^2=3,\qquad \rho_v(T_-)=I_3.     \tag{26c}
\]

A one-step rotation of the Hamilton cycle exchanges (P) and (Q), and
hence sends (T_-) to (-T_-).  The three-copy invariant is unchanged by
the site permutation but is cubic in its tensor argument, so

\[
                             I_B(T_-)=0.                  \tag{26d}
\]

Exact enumeration of the two-copy covariant gives

\[
                  \|\mathcal A_2(T_-)\|^2={81\over8}<12.\tag{26e}
\]

The edge magnitudes can be distributed uniformly around the cycle, making
the *source* fully isotropic as well.  Thus, already at six vertices, the
one-matching tensor (22) and the signed two-matching tensor (26b) have the
same norm and one-site reduced data as GHZ but place GHZ strictly between
them for the two-copy norm, and on opposite sides of it for the
three-copy invariant ((8,6,0)).

There is also an exact Cauchy--Binet interpretation.  Factor a positive
scalar multiple (lambda I_3) on an edge as

\[
 \lambda I_3=\sum_{r=0}^2(\sqrt\lambda e_r)
                              \otimes(\sqrt\lambda e_r). \tag{27}
\]

At each endpoint these three half-edge vectors are a tight frame, and the
only nonzero (3\)-fold determinant uses all three labels on that *same*
edge.  In the three-copy matching expansion, the only matching triple is

\[
                              (M,M,M),                    \tag{28}
\]

and its value is nonzero.  Local Hadamard and Cauchy--Binet equality thus
does not favor three distinct source edges; it is perfectly saturated by
a repeated full-rank edge.

## 6. A factorization mismatch in the proposed Cauchy--Binet proof

Full source isotropy says

\[
 \sum_{u\ne v}\rho_v(A_{uv})=cI_3.                       \tag{29}
\]

The columns (or rows) of the incident matrices consequently make a tight
frame at one chosen endpoint.  The determinant expansion of the
three-copy invariant, however, requires one *compatible* rank
factorization

\[
                         A_{uv}=X_{uv}Y_{uv}^{\mathsf T}  \tag{30}
\]

on both endpoints.  Choosing columns makes
(X_{uv}X_{uv}^*=A_{uv}A_{uv}^*), but then the other frame operator is
generally only (I), not (A_{uv}^{\mathsf T}\overline{A_{uv}}).

The symmetric Schmidt choice is compatible, but if
(A=U\Sigma V^*), its endpoint frame operators are

\[
 XX^*=(AA^*)^{1/2},\qquad
 YY^*=(A^{\mathsf T}\overline A)^{1/2},                  \tag{31}
\]

not the reduced Gram operators in (29).  Therefore it is not legitimate
to replace the source determinant expansion by a product of local
Cauchy--Binet sums (c^3).  Even in special cases where the half-edge
frames are tight, the Bell example (27)--(28) shows that equality can be
concentrated on a repeated edge.

## 7. Consequence for the complex-field route

Hermitian positivity supplies the exact sum-of-squares gaps (6).  A proof
that all (3n) gaps vanish at a minimum would reduce the conjecture to the
diagonal source class.  None of the currently available norm identities
forces this: exact binary cancellation gives strict gaps, and the phased
Fourier model shows that balance plus smooth local minimality leaves very
large strict gaps.

Squared norms and reduced density matrices are functions of the *summed*
output and retain cross-matching interference.  The two- and three-copy
exterior quantities likewise do not distinguish a rainbow source from a
repeated full-rank matching; in their natural isotropic comparison, the
repeated matching is stronger than GHZ.  A successful continuation must
therefore use all mixed GHZ cancellation equations to prove the new global
statement

\[
                 c_i s_{v,i}=1\quad\text{for every }v,i, \tag{32}
\]

or otherwise control the cofactor-frame couplings in (8).  No purely
Hermitian or local Cauchy--Binet equality argument establishes (32).

All numerical-looking values in this note are audited exactly by
`computations/verify_gaussian_norm_invariant.py`.
