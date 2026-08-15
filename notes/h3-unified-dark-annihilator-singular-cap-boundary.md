# The unified dark-annihilator input is universal; its exact output is a singular two-channel cap

## Result

Retain the literal full-nine pair equations

\[
 a_{ij}q^{[3]}+p_i s_jq^{[2]}=\delta_{ij}X_i.            \tag{1}
\]

For a cap matrix \(M\), put

\[
 \sigma(M)=\sum_{ij}M_{ij}a_{ij},\qquad
 r(M)=\sum_{ij}M_{ij}p_is_j.                            \tag{2}
\]

There are two conclusions.

1. The apparently special dark-annihilator boundary is universal.  The
   space

   \[
        D_a=\{M:\operatorname{diag}M=0,
                    \ \sigma(M)=0\}                    \tag{3}
   \]

   has dimension at least five, every member satisfies

   \[
                          r(M)q^{[2]}=0,                 \tag{4}
   \]

   and \(D_a\) contains a nonzero rank-one matrix supported in each of the
   three fixed physical rows.  Thus rank at most two, zero diagonal, zero
   direct scalar and (4), even with a factorized response, cannot by
   themselves imply occupied-cell deletion, a unit, or an active clean cap.

2. The entire plane (3) nevertheless forces a real projective reduction.
   Let \(K_*\) be invertible with

   \[
       \sigma(K_*)=0,\qquad (K_{*,00},K_{*,11},K_{*,22})
                          \in(\mathbb C^*)^3.            \tag{5}
   \]

   Then there are \(M\in D_a\) and \(t\ne0\) for which

   \[
   \boxed{
     K=K_*+tM,quad \operatorname{rank}K\le2,quad
     \sigma(K)=0,quad \operatorname{diag}K=\operatorname{diag}K_*,
     \quad r(K)q^{[2]}=r(K_*)q^{[2]}.}                  \tag{6}
   \]

   Hence the invertibly paired scalar-zero packet always has a singular
   representative with at most two literal endpoint-product channels.

The first statement is a sharp negative answer to a bare
dark-annihilator-to-deletion lemma.  The second is the strongest uniform
positive replacement currently justified.  It does not assert that the
singular cap is clean or active: its direct scalar is still zero.

Checker:
`computations/verify_h3_unified_dark_annihilator_singular_cap_boundary.py`.

## 1. Why the dark plane is automatic

Contract all nine equations (1) against \(M\).  No occurrence or target
projection is used:

\[
 \boxed{
   \sigma(M)q^{[3]}+r(M)q^{[2]}
                         =\sum_iM_{ii}X_i.}             \tag{7}
\]

The off-diagonal matrix space has dimension six.  Imposing the one linear
condition \(\sigma(M)=0\) gives (3), with

\[
                        \dim D_a\ge5.                   \tag{8}
\]

Equation (7) immediately gives (4).  This is just the contraction of the
six zero target rows.

The low-rank supply is equally automatic.  Fix a row \(i\), and let
\(j,k\) be the two other columns.  If
\((a_{ij},a_{ik})\ne(0,0)\), take

\[
                  M_{ij}=a_{ik},\qquad M_{ik}=-a_{ij},  \tag{9}
\]

with every other entry zero.  If both direct entries vanish, take
\(M=E_{ij}\).  In either case \(M\ne0\), \(M\in D_a\), and
\(\operatorname{rank}M=1\).  The three row supports are disjoint, so these
give three independent dark lines.

This observation changes the logical status of the k=1 result in
`ded19a6`.  Its matrix identities

```text
rank(M)<=2, diag(M)=sigma(M)=0, r(M)q^[2]=0
```

are not alone exceptional.  What is exceptional is the canonical quotient
construction and the shared-line ownership

\[
                      r(M)=\ell h,qquad Pu=Sv=\ell.    \tag{10}
\]

Even factorization without the second clause is not enough: every row
matrix (9) has the factorized response

\[
                 r(M)=p_i\bigl(a_{ik}s_j-a_{ij}s_k\bigr). \tag{11}
\]

Similarly, the k=2/3 zero-response kernels in `f7601f6` are stronger than
(3) because their response vanishes before multiplication by \(q^{[2]}\).
But a cap covector with zero response is still not a variation of an
occupied source coefficient.

## 2. Why minimum support does not apply yet

Minimum support deletes an occupied cell only when the **complete physical
derivative tensor** of that cell lies in the span of the other complete
derivatives.  A cap matrix is a dual test on the deleted endpoint colours;
it is not itself a coefficient direction.

The tempting source variation in the nonzero-response branch is

\[
                         q(t)=q+t z,\qquad z=r(M).       \tag{12}
\]

Its top derivative vanishes by (4):

\[
                         \frac d{dt}q(t)^{[3]}\big|_0
                              =zq^{[2]}=0.              \tag{13}
\]

But differentiating every uncontracted row in (1) gives

\[
 \frac d{dt}\left(a_{ij}q(t)^{[3]}+p_i s_jq(t)^{[2]}\right)\Big|_0
       =p_i s_jzq.                                      \tag{14}
\]

There is no reason for the nine tensors in (14) to vanish or admit a
source-labelled compensation.  Thus (13) is a top matching-power tangent,
not a tangent to the full EqSystem fibre.

The checker freezes the smallest common-power illustration on six scalar
sites.  Let \(q\) be the six-cycle

```text
01,12,23,34,45,50
```

with unit coefficients, let \(z=02\), and take \(p s=15\).  Then

\[
              zq^{[2]}=0,qquad [p s zq]_{012345}=1.    \tag{15}
\]

After using the chord `02`, the complement has no two-edge matching in the
cycle; after also using `15`, the cycle edge `34` completes the first
uncontracted derivative.  This is a literal common-\(q\) square-free guard
to the implication “top tangent implies source deletion.”  It is not a
full-nine ternary source and is not presented as a counterexample to the
conjecture.

## 3. The determinant split for one dark direction

For a fixed \(M\in D_a\), set

\[
                            N=K_*^{-1}M.                \tag{16}
\]

The cap pencil preserves every contracted target datum:

\[
\begin{aligned}
 \sigma(K_*+tM)&=0,\\
 \operatorname{diag}(K_*+tM)&=\operatorname{diag}K_*,\\
 r(K_*+tM)q^{[2]}&=r(K_*)q^{[2]}.
\end{aligned}                                          \tag{17}
\]

Moreover

\[
              \det(K_*+tM)=\det(K_*)\det(I+tN).        \tag{18}
\]

If this polynomial is nonconstant, it has a nonzero root over
\(\mathbb C\), yielding (6).  If it is constant, the characteristic
polynomial of \(N\) is \(\lambda^3\); Cayley--Hamilton makes \(N\)
nilpotent.  Thus each individual dark direction has the sharp alternative

```text
singular point on its cap pencil  OR  K_*^{-1}M nilpotent.
```

Both cases occur.  With \(K_*=I\) and direct block \(a=E_{01}\), take

\[
 M_1=E_{02}+E_{20},\qquad M_0=E_{10}.                  \tag{19}
\]

Both belong to \(D_a\), while

\[
     \det(I+tM_1)=1-t^2,qquad \det(I+tM_0)=1,qquad M_0^2=0. \tag{20}
\]

So nilpotence is a real direction-level branch, not automatically a
deletion.

## 4. The whole dark plane removes the nilpotent branch

The direction-level alternative becomes positive when all of (3) is used.
Put

\[
                         V=K_*^{-1}D_a.                 \tag{21}
\]

Then \(\dim V\ge5\).  Suppose every member of \(V\) were nilpotent.  For
all \(A,B\in V\), nilpotence of \(A\), \(B\), and \(A+B\) would give

\[
 \operatorname{tr}(A^2)=\operatorname{tr}(B^2)
   =\operatorname{tr}((A+B)^2)=0,
 \qquad\text{hence}\qquad \operatorname{tr}(AB)=0.     \tag{22}
\]

Thus \(V\) would be totally isotropic for the symmetric trace pairing

\[
                         (A,B)\longmapsto\operatorname{tr}(AB). \tag{23}
\]

This pairing is nondegenerate on the nine-dimensional matrix space.  A
totally isotropic subspace is contained in its orthogonal complement, so

\[
                    2\dim V\le9,\qquad \dim V\le4,     \tag{24}
\]

contradicting \(\dim V\ge5\).  Therefore some \(N\in V\) is not
nilpotent.  Its determinant pencil is nonconstant, and Section 3 produces
the singular cap (6).

At that root, \(K\) factors through at most two channels.  If
\(K=UV^{\mathsf T}\) with \(U,V\) having at most two columns, then

\[
 r(K)=\sum_{\alpha=1}^{\operatorname{rank}K}
          p(U_\alpha)s(V_\alpha).                       \tag{25}
\]

The exact terminal is therefore a two-channel scalar-zero packet, not an
abstract nilpotent class.

## 5. Sharp remaining statement

The singular export uses the literal nine rows, the fixed physical
diagonal readouts, and the common \(q^{[2]}\).  It is source-valid and does
not require an occurrence selector.  But it still gives only

\[
       \operatorname{rank}K\le2,quad \sigma(K)=0,quad
       r(K)q^{[2]}=\sum_iK_{*,ii}X_i.                  \tag{26}
\]

The already committed polarized six-site guards show that a two-channel
or pair-cap-shaped equation of the form (26) is not excluded in isolation.
Their explicit first uncontracted row fails, which identifies the exact
remaining leverage:

> **Two-channel full-nine landing.**  A singular cap obtained from (6),
> together with the other eight pair rows sharing the same physical
> endpoint stars and direct block, forces a unit, an active clean cap, or a
> complete-derivative relation that deletes an occupied unprotected cell.

This is strictly sharper than the original unified dark-annihilator task.
The dark input itself is automatic; the nontrivial object to attack is its
source-valid singular representative and the eight uncontracted derivative
rows.
