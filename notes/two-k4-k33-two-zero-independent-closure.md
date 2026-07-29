# The two-zero star closes the exact-nine \(K_{3,3}\) residual

## 1. Outcome

This note independently closes the last value-level branch left by
[`two-k4-k33-nonzero-star-erasure.md`](two-k4-k33-nonzero-star-erasure.md).
The local statement is exact, not generic: if one four-site star has two
literal-zero components, one nonzero arbitrary component, and one
invertible component, while the other star is completely invertible, then
the eight-cell erased Hessian has precisely one arbitrary edge block in
its kernel.  The edge joins the nonzero exceptional site to the regular
site.

Applied to the top-left singular \(K_{3,3}\), this residual edge misses
either literal-zero endpoint.  At that endpoint all three blocks of the
actual effective quadratic vanish, contradicting the three weighted
coordinate lines of the right \(K_4\).  Consequently all nine blocks in
the singular square are literal zero.  The remaining nonzero cross graph
has matching number two, so the low-matching theorem excludes it.

Together with the exact-nine position reduction, this proves

\[
  \boxed{\#\{(i,j):\det B_{ij}=0\}\ge 10}.             \tag{1}
\]

The independent executable audit is
[`verify_two_k4_k33_two_zero_independent_closure.py`](../computations/verify_two_k4_k33_two_zero_independent_closure.py).

## 2. Square-free setup

Let

\[
 \mathcal R=\bigotimes_{r=0}^3(\mathbb F\oplus V_r),
 \qquad V_r^2=0,\qquad \dim V_r=3,                    \tag{2}
\]

over a characteristic-zero field.  Let \(U,W\) be three-spaces, let
\(K\subset U\) and \(L\subset W\) be arbitrary planes, and write

\[
 p_x=\sum_{r=0}^3P_rx,\qquad s_y=\sum_{r=0}^3S_ry.    \tag{3}
\]

Fix distinct \(h,k,i\in\{0,1,2\}\).  Assume

\[
 P_h=P_k=0,\qquad P_i\ne0,\qquad
 P_3,S_0,S_1,S_2,S_3\text{ are isomorphisms}.         \tag{4}
\]

No relation between \(K,L,P_3(K)\), or \(S_3(L)\) is assumed.

## 3. Two elementary coefficient facts

We use two elementary square-free kernels.  Both follow by comparing the
three blocks on each three-site component.

**Lemma 3.1 (two-term plane bridge).**  Let \(A:M\to A_0\) be nonzero
and \(B:M\to B_0\) injective on a two-plane \(M\).  If

\[
 X\otimes Bx+A x\otimes Y=0\qquad(x\in M)             \tag{5}
\]

with \(X\in T\otimes A_0\) and \(Y\in T\otimes B_0\), with tensor
factors put in the displayed order, then \(X=Y=0\).

**Proof.**  Contract the \(T\)-factor by an arbitrary covector.  It is
enough to treat

\[
 a\otimes Bx+A x\otimes b=0.                          \tag{6}
\]

If either \(a\) or \(b\) is zero, nonzeroness of \(A\) and injectivity
of \(B\) kill the other.  If both are nonzero and \(A\) has rank one,
take a nonzero \(x\in\ker A\); then (6) contradicts \(Bx\ne0\).  If
\(A\) has rank two, pure-factor cancellation in (6), for two independent
values of \(x\), would put the two-plane \(B(M)\) in the line
\(\mathbb F b\).  This is impossible.  Every contraction is therefore
zero, proving the lemma. \(\square\)

**Lemma 3.2 (supported cubic boundary).**  Suppose every
\(S_r:W\to V_r\) is invertible.  Let a cubic \(T\in\mathcal R_3\) have
zero component on the triangle \(012\), so every component of \(T\)
contains site \(3\).  If

\[
                         T s_y=0\qquad(y\in L),        \tag{7}
\]

then

\[
 T=\Omega_{S,L}^{012}\otimes v_3                    \tag{8}
\]

for a unique \(v_3\in V_3\).  Here, for an ordered basis \(u,v\) of
\(L\), the three blocks of the plane boundary are

\[
\begin{aligned}
 (\Omega_{S,L})_{01}&=S_0u\,S_1v-S_0v\,S_1u,\\
 (\Omega_{S,L})_{02}&=-S_0u\,S_2v+S_0v\,S_2u,\\
 (\Omega_{S,L})_{12}&=S_1u\,S_2v-S_1v\,S_2u.
\end{aligned}                                         \tag{9}
\]

In particular, a nonzero tensor in (8) has all three hole components on
\(012\) nonzero.

**Proof.**  Normalize the three injective plane maps
\(S_0|_L,S_1|_L,S_2|_L\) independently.  In each output coefficient
transverse to one of their image planes, (7) first kills the corresponding
outside component.  The remaining equations are the three two-dimensional
Koszul equations; their three scalars agree with signs \(+,-,+\), giving
(9), while the site-3 factor is free.  Conversely (9) times any \(v_3\)
is killed by every \(s_y\), because three vectors from the two-plane
\(S(L)\) are alternating.  Each block in (9) has matrix rank two, hence is
nonzero.  This proves both assertions. \(\square\)

This is also the literal \(3\)-dimensional kernel checked independently
by the executable audit.

## 4. Exact two-zero erasure kernel

**Theorem 4.1.**  Under (4), if \(q\in\mathcal R_2\) satisfies

\[
 q p_xs_y=0\qquad(x\in K\text{ or }y\in L),           \tag{10}
\]

then

\[
                         q\in V_i\otimes V_3.          \tag{11}
\]

Conversely every block in \(V_i\otimes V_3\) satisfies (10).  Thus the
kernel is exactly the nine-dimensional space in (11).

**Proof.**  Since all four \(S_r\) are isomorphisms, the cubic
annihilator of the full star \(s(W)\) is its generalized determinant
line.  The six cells \(K\times W\) therefore give a linear form
\(\rho\in K^*\) such that

\[
                         q p_x=\rho(x)\Omega_S
                                      \qquad(x\in K).  \tag{12}
\]

Look at the three-site component on \(hk3\).  Because \(P_h=P_k=0\),
it reads

\[
 q_{hk}\otimes P_3x=\rho(x)(\Omega_S)_{hk3}.          \tag{13}
\]

The left side has mode rank at most one at site \(3\), whereas a nonzero
generalized determinant has mode rank three there.  Hence
\(\rho(x)=0\) for every \(x\in K\), and then the injectivity of \(P_3\)
also gives \(q_{hk}=0\).  Thus

\[
                              q p_x=0\qquad(x\in K).   \tag{14}
\]

First suppose \(P_i|_K\ne0\).  On the triangle \(hi3\), equation (14)
is

\[
 q_{hi}\otimes P_3x+q_{h3}\otimes P_ix=0
                                      \qquad(x\in K). \tag{15}
\]

Lemma 3.1, with the harmless permutation of the last two tensor factors,
gives \(q_{hi}=q_{h3}=0\).  The same argument on \(ki3\) gives
\(q_{ki}=q_{k3}=0\).  The block \(q_{i3}\) never appears in (14),
because either insertion repeats site \(i\) or site \(3\).  This proves
(11) in the first case.

Now suppose \(P_i|_K=0\).  Equation (14), component by component, gives

\[
 q=Q_h+Q_k+Q_i,qquad Q_r\in V_r\otimes V_3.          \tag{16}
\]

Indeed \(P_3|_K\) detects every block not incident with site \(3\),
while the three site-3 blocks are invisible on the six-cell slab.  Choose
\(z\notin K\).  Since \(P_i\ne0\) and vanishes on the plane \(K\),

\[
                              u_i=P_i z\ne0.           \tag{17}
\]

The remaining two erased cells say that the cubic

\[
                   T=q p_z=Q_hu_i+Q_ku_i              \tag{18}
\]

annihilates \(s(L)\).  It has components missing \(h\) and \(k\), but
its component missing \(i\) is zero.  Lemma 3.2 writes it as
\(\Omega_{S,L}^{012}\otimes v_3\).  Since every one of the three hole
components of a nonzero such boundary is nonzero, the missing component
forces \(v_3=0\), hence \(T=0\).  The two summands in (18) occupy
different three-site components, so \(u_i\ne0\) gives
\(Q_h=Q_k=0\).  Only \(Q_i=q_{i3}\) remains.

Finally, if \(q=q_{i3}\), then both sites complementary to its edge are
\(h,k\), where the first star is identically zero.  Consequently
\(q p_xs_y=0\) for all \(x,y\), not merely for the erased eight cells.
This proves equality in (11). \(\square\)

## 5. Weighted two-\(K_4\) application

Assume the sole exact-nine position mask is the top-left singular square

\[
                         012\mid012\mid012\mid\varnothing.           \tag{19}
\]

Pair a selected row \(r\in\{0,1,2\}\) with the completely invertible
row \(3\).  Let \(a,b\) be the complementary left rows and put
\(c=\kappa(r3)=\kappa(ab)\).  The exact two-/four-cross sector gives the
eight erased cells (10) for

\[
 q_{\rm eff}=\lambda_{ab}q_R+p_{a,c}p_{b,c},          \tag{20}
\]

where

\[
 (q_R)_{uv}=\rho_{uv}
 E_{\kappa(uv),\kappa(uv)},qquad
 \lambda_{ab}\rho_{uv}\ne0.                          \tag{21}
\]

The nonzero factors in (21) follow from the three constant-word
coefficients of each four-site equality shore: the two internal edge
weights in every one-factor have nonzero product (indeed product one
after the usual normalization).  No equality among these weights is used.

The preceding nonzero-star and one-zero erasure theorems already exclude
a selected row having three or two nonzero blocks in the singular square.
Their common determinant-response step uses the full four-site identity:
if \(q p_{x_0}=0\) and
\(q p_{x_1}=\rho(x_1)\Omega_S\), associativity gives
\(\Omega_Sp_{x_0}=0\).  The degree-one annihilator of \(\Omega_S\) is
exactly the diagonal regular star \(s(W)\), so every component of
\(p_{x_0}\) is nonzero and the four-site full-support kernel applies.
This is the repaired invariant argument; it does not use the false claim
that a single three-site fixed-star kernel always has mode rank at most
two.

Suppose it has exactly one, at column \(i\), and literal zeros at columns
\(h,k\).  Theorem 4.1 says that \(q_{\rm eff}\) is supported only on
edge \(i3\).  In particular all three blocks incident with endpoint \(h\)
vanish.

At endpoint \(h\), the three incident blocks of the first term in (20)
have endpoint lines

\[
 \mathbb F e_{\kappa(hj)}\qquad(j\ne h).              \tag{22}
\]

They are the three coordinate lines, and their coefficients
\(\lambda_{ab}\rho_{hj}\) are nonzero.  Every incident block of the
product term has its endpoint image in the fixed plane

\[
 \operatorname{span}\left(
   \operatorname{row}_c(B_{ah})^{\mathsf T},
   \operatorname{row}_c(B_{bh})^{\mathsf T}\right).  \tag{23}
\]

Vanishing of the three effective blocks would put all three lines (22)
in the plane (23), which is impossible.  Therefore no selected row can
contain even one nonzero top-left block.  Repeating this for
\(r=0,1,2\) makes all nine singular-square blocks literal zero.

The seven remaining cross blocks lie in row \(3\) or column \(3\).  Their
position graph has matching number exactly two: one may match left \(3\)
away from right \(3\) and one other left vertex to right \(3\), but no
third disjoint cross edge exists.  To match the unit-weight statement of
the low-matching theorem, normalize the internal shore weights as follows.
For a fixed color, its two complementary \(K_4\) edge weights have product
one.  Choose nonzero diagonal local scalars \(d_{u,c}\) so that
\(\lambda_{uv}d_{u,c}d_{v,c}=1\) on both factor edges.  Their product over
the four sites is one, so this change preserves the constant GHZ
coefficient.  Applying it independently on both shores multiplies every
cross block on the left and right by invertible diagonal matrices; hence
it preserves literal zeros, singularity, and the nonzero position graph.
The unit-weight low-matching cross obstruction therefore excludes this
final branch.  This proves (1).

## 6. Exact audit

Run

```text
python computations/verify_two_k4_k33_two_zero_independent_closure.py
```

The checker independently rebuilds the erased-Hessian matrix, tests
unrelated invertible regular maps and both restriction branches, verifies
that the kernel is exactly the claimed nine coordinates, checks the
three-dimensional supported cubic boundary, retains independent symbolic
internal weights in the endpoint-line determinant, and verifies the final
matching number.  Computation is supplementary; Theorem 4.1 is the
field-uniform proof.
