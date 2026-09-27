# An all-orders two-replica proof of the complex weighted Krenn–Gu conjecture

[PDF](krenn-gu-all-orders-two-replica.pdf) · [LaTeX source](krenn-gu-all-orders-two-replica.tex) · [Audited source](krenn-gu-all-orders-two-replica-proof.md)

**Review status (2026-09-26): complete written argument; internally audited.**
This document gives the entire argument, including the earlier reflection and
diagonal-reduction steps. Full Lean formalization and external peer review
remain pending. It is a typeset presentation of the unchanged audited Markdown
source, which retains its original review header. See the
[current review record](../notes/all-orders-two-replica-review-2026-09-26.md)
for the internal audits and present status.

## 1. Statement and algebraic model

**Theorem 1.1 (Complex weighted Krenn–Gu no-go).**
Let $`V`$ have even cardinality $`n>4`$. At each vertex take three designated
coordinates $`a,b,c`$. In the commutative algebra in which the product of any
two coordinates at the same vertex is zero, let $`A`$ be any quadratic involving
only distinct vertices, with arbitrary complex coefficients. Write
$`A^{[j]}=A^j/j!`$. Then

```math
 A^{[n/2]}=\tau_a a^V+\tau_b b^V+\tau_c c^V,
 \qquad \tau_a\tau_b\tau_c\ne0
 \tag{1}
```

is impossible. Here $`h^S`$ means the product of coordinate $`h`$ over $`S`$.

Coefficients of $`A`$ are aggregate endpoint-color edge weights. Its divided
top power is exactly the perfect-matching tensor: every matching occurs once.
Parallel edges of identical endpoint colors aggregate by addition. Projecting
any larger target palette onto three active colors preserves (1),
so the result covers every target dimension at least three. Unequal nonzero pure
amplitudes, arbitrary edge density, and arbitrary complex weights are allowed.

We use formal Wick moments, defined as sums over pairings of labeled factors
with assigned symmetric covariances. Odd moments are zero. These are polynomial
identities; they require neither positivity nor an invertible covariance.
The proof of Theorem 1.1 is completed in Sections 5
and 6.

## 2. Whole binary higher responses vanish

**Lemma 2.1 (Whole binary higher-response vanishing).**
Let $`\Omega`$ have $`2m+1\ge3`$ vertices, let $`R`$ be an arbitrary quadratic
on $`\Omega`$, and let $`D`$ be a vector space of rows $`L`$ such that

```math
 \Phi(L)=L R^{[m]}=\sum_h f_h(L)h^\Omega.
 \tag{2}
```

Assume all three linear functions $`f_h`$ are nonzero and at least two are
independent. For odd $`p\le2m+1`$, define

```math
 H_p(L)=L^p R^{[(2m+1-p)/2]}.
```

For every $`p\ge3`$, the tensor $`H_p(L)`$ has zero coefficient on every word
using at most two colors, including the terminal degree $`p=2m+1`$.
The same vanishing holds after polarization for products of arbitrary rows
from the same $`D`$.

**Proof.**
Give formal variables $`X_{i,h}`$ their $`R`$ covariances, zero covariances
within a vertex, and give an auxiliary $`g`$ covariance $`L_i(h)`$ with
$`X_{i,h}`$ and zero covariance with itself. A Wick moment with $`p`$ copies
of $`g`$ and one specified coordinate at each vertex is the corresponding
coefficient of $`H_p(L)`$. The $`p!`$ assignments of auxiliary occurrences
are precisely those of the raw power $`L^p`$; the divided power of $`R`$
counts each remaining matching once.

Take two independent identical replicas $`(X,g_1)`$, $`(Y,g_2)`$. Choose
distinct local colors $`\alpha_i,\beta_i`$ at each vertex and set

```math
 \Delta_i=X_{i,\alpha_i}Y_{i,\beta_i}
              -X_{i,\beta_i}Y_{i,\alpha_i}.
```

Over $`\mathbb C(s,t)`$, the orthogonal reflection

```math
 \frac{1}{s^2+t^2}
 \begin{pmatrix}s^2-t^2&2st\\2st&t^2-s^2\end{pmatrix}
```

fixes $`sg_1+tg_2`$ and negates each $`\Delta_i`$. It preserves the replicated
covariance, so the moment of

```math
 (sg_1+tg_2)^{p+1}\prod_{i\in\Omega}\Delta_i
```

is zero: there are an odd number of determinants. Extracting $`s^pt`$ gives

```math
 \sum_{I\subseteq\Omega}(-1)^{|I|}H_p(L)(w_I)\Phi(L)(w'_I)=0,
 \tag{3}
```

where $`w_I`$ uses $`\beta`$ on $`I`$ and $`\alpha`$ elsewhere, and $`w'_I`$
is complementary. Equality over $`\mathbb C(s,t)`$ gives a polynomial identity,
including isotropic parameter values by extension. No operation on the
original source is being made.

With constant local pair $`a,b`$, (3) says

```math
 f_b[a^\Omega]H_p=f_a[b^\Omega]H_p.
```

Two independent $`f`$'s are coprime in $`\mathbb C[D]`$, hence for
$`p=2r+1`$ there is a common homogeneous polynomial $`q_r`$ of degree
$`2r`$ such that $`[h^\Omega]H_p=f_hq_r`$ for every $`h`$; $`q_0=1`$.
For a mixed word $`w`$ avoiding an active color $`h`$, choose
$`\alpha_i=w_i`$, $`\beta_i=h`$. The only constant complementary word in
(3) is $`h^\Omega`$, giving $`f_h[w]H_p=0`$. Polynomial
cancellation proves all binary mixed coefficients zero, even at individual
rows where $`f_h(L)=0`$.

Define finite polynomials

```math
 \Psi(L)=\sum_{r=0}^m\frac{H_{2r+1}(L)}{(2r+1)!},
 \qquad
 g(L)=\sum_{r=0}^m\frac{q_r(L)}{(2r+1)!}.
```

On any binary palette $`a,b`$, $`\Psi(L)`$ thus equals

```math
 g(L)\bigl(f_a(L)a^\Omega+f_b(L)b^\Omega\bigr).
```

For two tensors on $`\Omega`$, let $`K`$ be the product of local alternating
pairings, normalized by $`K(a^\Omega,b^\Omega)=1`$. Wick moments with shifted
variables $`X_i+L_i`$ show that $`K(\Psi(L),\Psi(M))`$ is invariant under
simultaneous $`\mathrm{SO}(2)`$ rotation of the two mean rows: the replica
covariance and each determinant are unchanged. Choose independent
$`f_a,f_b`$. This pairing is

```math
 \bigl(f_a(L)f_b(M)-f_b(L)f_a(M)\bigr)g(L)g(M).
```

The determinant factor is a nonzero polynomial and is rotation invariant.
Cancel it in $`\mathbb C[D\times D]`$, then rotate by $`45`$ degrees and set
$`M=0`$. Since $`g`$ is even and $`g(0)=1`$,

```math
 g(L/\sqrt2)^2=g(L).
```

If $`g`$ had positive degree, the degrees of the two sides would differ.
Thus $`g=1`$, and all $`q_r`$ with $`r\ge1`$ vanish. Together with
(3), this proves whole binary vanishing through the
terminal degree $`2m+1`$. Polarization gives the same statement for products
of arbitrary rows from this same $`D`$.
$`\square`$

For a source (1), delete any root $`p`$. Its three actual
incident rows have responses $`\tau_hh^{V\setminus\{p\}}`$, so their span
satisfies (2) with three independent $`f_h`$. Thus
Lemma 2.1 applies at every original root, before diagonalization.

## 3. Even omission identities and diagonal reduction

**Lemma 3.1 (Even omission).**
In the setting of (2), omit a vertex $`q`$, put
$`S=\Omega\setminus\{q\}`$, and write

```math
 \begin{aligned}
 R&=Q+\sum_h h_q V_h,& L&=U+\sum_h d_hh_q,\\
 E(U)&=\sum_{r=0}^m\frac{U^{2r}}{(2r)!}Q^{[m-r]},&F&=E(0).
 \end{aligned}
```

For any $`L_1,L_2\in D`$ and any active color $`k`$,

```math
 [k^S]\,U(L_1)U(L_2)Q^{[m-1]}=0.
```

This includes $`m=1`$.

**Proof.**
The full coefficient of $`q=h`$ in $`\Psi(L)`$ is

```math
 d_h E(U)+E_{V_h}(U),
```

where subscripts mean directional derivatives in the mean, with $`Q`$
fixed. By Lemma 2.1, its projection onto any palette $`h,k`$
on $`S`$ is $`f_h(L)h^S`$. All the following pairings use this binary
projection implicitly.

Because $`|S|`$ is even, $`K`$ is symmetric and $`K(Z,h^S)=[k^S]Z`$.
The same two-replica rotation gives

```math
 \begin{aligned}
 K(E(U),E(U))&=K(F,E(\sqrt2U)),\\
 K(E(U),E_V(U))&=\frac{1}{\sqrt2}K(F,E_V(\sqrt2U)).
 \end{aligned}
 \tag{4}
```

The second identity follows by differentiating the rotation identity at
means $`U,U+tV`$: the second rotated mean is zero at $`t=0`$ and
$`E'(0)=0`$. Substitute

```math
 E_{V_h}(U)=f_hh^S-d_hE(U)
```

and the corresponding identity for $`\sqrt2L`$ into the second equation
of (4). The first cancels the $`d_h`$ terms, leaving

```math
 f_h(L)[k^S]\bigl(E(U)-F\bigr)=0.
```

Cancel the nonzero polynomial $`f_h`$. Separating homogeneous degrees and
polarizing yields

```math
 [k^S]\,U(L_1)U(L_2)Q^{[m-1]}=0.
 \tag{5}
```

$`\square`$

**Lemma 3.2 (Global diagonal reduction).**
Every endpoint-color edge block of a source (1) is diagonal
in the given target coordinates.

**Proof.**
For a fixed color $`h`$, define

```math
 \begin{aligned}
 M_h[p,r]&=A_{pr}(h,h) &&(p\ne r),& M_h[p,p]&=0,\\
 C_h[r,q]&=\mathrm{haf}\bigl(M_h[V\setminus\{r,q\}]\bigr)
                  &&(r\ne q),& C_h[q,q]&=0,\\
 B_{ih}[p,r]&=A_{pr}(i,h) &&(p\ne r),& B_{ih}[p,p]&=0.
 \end{aligned}
```

Expansion of the original one-defect word at $`p`$ gives

```math
 (B_{ih}C_h)[p,p]=\delta_{i,h}\tau_h.
```

For $`p\ne q`$, expand each $`C_h[r,q]`$ at its retained vertex $`p`$:

```math
 \begin{aligned}
 (B_{ih}C_h)[p,q]
 &=\sum_{\substack{r,s\in V\setminus\{p,q\}\\r\ne s}}
       A_{pr}(i,h)A_{ps}(h,h)\,
       \mathrm{haf}\bigl(M_h[V\setminus\{p,q,r,s\}]\bigr)\\
 &=0.
 \end{aligned}
 \tag{6}
```

The last expression is exactly (5) for two rows of the
original $`p`$ family after omitting $`q`$. Both sums are ordered; there
is no factor $`1/2`$. Consequently

```math
 B_{ih}C_h=\delta_{i,h}\tau_h I.
```

Taking $`i=h`$ proves $`C_h`$ invertible. Taking $`i\ne h`$ then proves
$`B_{ih}=0`$. Every original edge block is therefore diagonal. This uses
neither cofactor nonvanishing assumptions nor a change of basis.
$`\square`$

## 4. The endpoint identity

Fix two colors $`B,H`$ after diagonal reduction and roots $`p\ne q`$.
Put $`U=V\setminus\{p,q\}`$, $`N=|U|`$ (even), and let $`Q`$ be the literal
binary quadratic on $`U`$. Write

```math
 \begin{aligned}
 d&=B_{pq},&e&=H_{pq},&\beta&=\mathrm{haf}(B),\\
 \eta&=\mathrm{haf}(H),&\alpha&=\mathrm{haf}(B[U]),\\
 x&=\sum_{i\in U}B_{pi}b_i,& y&=\sum_{i\in U}B_{qi}b_i,\\
 u&=\sum_{i\in U}H_{pi}h_i,& v&=\sum_{i\in U}H_{qi}h_i,\\
 E(L)&=\sum_{j=0}^{N/2}\frac{L^{2j}}{(2j)!}Q^{[N/2-j]},&F&=E(0).
 \end{aligned}
```

**Theorem 4.1 (Supported endpoint identity).**
For every supported edge $`B_{pq}\ne0`$,

```math
 \beta=B_{pq}\mathrm{haf}\bigl(B[V\setminus\{p,q\}]\bigr).
```

Derivatives of $`E`$ always keep $`Q`$ fixed. Lemma 2.1, applied
to the original $`p`$ and $`q`$ row planes and expanded at the other root,
gives the exact polynomial identities

```math
 \begin{aligned}
 E_y(sx+tu)+dsE(sx+tu)&=s\beta b^U,\\
 E_v(sx+tu)+etE(sx+tu)&=t\eta h^U,\\
 E_x(ay+bv)+daE(ay+bv)&=a\beta b^U,\\
 E_u(ay+bv)+ebE(ay+bv)&=b\eta h^U.
 \end{aligned}
 \tag{7}
```

These include the highest coefficient, which uses the terminal original odd
response of degree $`N+1`$. They are identities in mean parameters on the
unchanged source. Differentiating those parameters is legitimate and gives

```math
 \begin{aligned}
 E_u(ay)&=0,&E_v(sx)&=0,\\
 E_{yu}(sx)&=-dsE_u(sx),\\
 E_{uv}(sx)+eE(sx)&=\eta h^U,\\
 E_{xy}(0)+dF&=\beta b^U.
 \end{aligned}
 \tag{8}
```

On tensors on $`U`$, use the symmetric binary alternating pairing $`K`$,
normalized by $`K(b^U,h^U)=1`$. The polynomial
$`K(E(L_1),E(L_2))`$ is invariant under the full $`\mathrm O(2)`$ action
on the two means. The Wick proof is as in Section 2; a
determinant $`-1`$ transformation contributes $`(-1)^N=1`$.

Introduce independent columns $`P,Q_c,R_c,S_c\in\mathbb C^2`$ and means
$`L_i=P_i x+(Q_c)_iy+(R_c)_iu+(S_c)_iv`$. Set

```math
 \begin{aligned}
 G&=K(E(L_1),E(L_2)),& f&=G\big|_{R_c=S_c=0},\\
 M_{ij}&=\left.\partial_{(R_c)_i}\partial_{(S_c)_j}G\right|_{R_c=S_c=0},
 &T&=M+efI.
 \end{aligned}
```

These are finite polynomials. Orthogonal invariance gives

```math
 M(OP,OQ_c)=O M(P,Q_c)O^T,
```

and similarly for $`T`$. By (8),

```math
 M_{12}=K\bigl(E_u(P_1x+(Q_c)_1y),E_v(P_2x+(Q_c)_2y)\bigr)
```

is divisible by $`P_1(Q_c)_2`$; likewise $`M_{21}`$ is divisible by
$`P_2(Q_c)_1`$.

**Lemma 4.2 (Polynomial orthogonal kernel normal form).**
For the kernel matrix just defined,

```math
 \begin{aligned}
 T&=aI+bPQ_c^T,\\
 a,b&\in\mathbb C[\sigma,\tau,c],\\
 \sigma&=P\cdot P,\qquad \tau=Q_c\cdot Q_c,\qquad c=P\cdot Q_c.
 \end{aligned}
 \tag{9}
```

**Proof.**
In an orthonormal frame where $`P_1=0`$, $`M_{12}=0`$, so $`MP`$ is parallel
to $`P`$. In a frame where $`(Q_c)_2=0`$, $`M_{12}=0`$, so $`M^TQ_c`$ is
parallel to $`Q_c`$. Such frames exist on a dense open set of nonisotropic
columns. Their eigenvalues agree when $`P\cdot Q_c\ne0`$. For two independent
columns in dimension two, these conditions force

```math
 M=a_0I+bPQ_c^T.
```

Indeed, $`M`$ minus the common eigenvalue times $`I`$ annihilates $`P`$ and
has left kernel $`Q_c`$; its rank-one form is a multiple of
$`(P\cdot Q_c)I-PQ_c^T`$. Literal divisibility proves that

```math
 b=\frac{M_{12}}{P_1(Q_c)_2},\qquad a_0=M_{11}-bP_1(Q_c)_1
```

are polynomials. The generic identity therefore extends everywhere.
Uniqueness and covariance make $`a_0,b`$ scalar $`\mathrm O(2)`$ invariants,
and the same is true of $`a=a_0+ef`$.

For completeness, the invariant ring assertion is elementary. In coordinates
$`p_+=P_1+iP_2`$, $`p_-=P_1-iP_2`$ and $`q_+,q_-`$,
$`\mathrm{SO}(2)`$ acts with weights $`+1,-1`$. Its invariant monomials
are generated by $`\sigma,\tau,r=p_+q_-,s=p_-q_+`$, with
$`rs=\sigma\tau`$. Reflection exchanges $`r,s`$. Symmetric polynomials
reduce to $`r+s=2c`$ and $`rs=\sigma\tau`$, giving
$`\mathbb C[\sigma,\tau,c]`$. These three Gram coordinates are algebraically
independent.
$`\square`$

**Proof of Theorem 4.1.**
At $`(Q_c)_1=0`$, differentiate $`M_{12}`$ in $`(Q_c)_1`$ and use
(8). One obtains

```math
 \left.\partial_{(Q_c)_1}M_{12}\right|_{(Q_c)_1=0}
       =-dP_1\left.M_{12}\right|_{(Q_c)_1=0},
 \qquad P_1^2(Q_c)_2(b_c+db)=0.
```

The substitution

```math
 (\sigma,\tau,c)=\bigl(P_1^2+P_2^2,(Q_c)_2^2,P_2(Q_c)_2\bigr)
```

is injective on polynomial rings: every $`\tau\ne0`$ and arbitrary
$`\sigma,c`$ is attained over $`\mathbb C`$. Thus $`b_c+db=0`$.
Since $`d\ne0`$, comparison of the highest power of $`c`$ forces the
finite polynomial $`b`$ to be zero. Therefore $`T=aI`$.

Write

```math
 Z=E_{uv}(P_2x+(Q_c)_2y)+eE(P_2x+(Q_c)_2y).
```

The full expression is $`T_{22}=K(E(P_1x+(Q_c)_1y),Z)`$. Differentiate
this expression in $`(Q_c)_1`$, then set $`(Q_c)_1=0`$.
Equation (7) gives

```math
 \left.\partial_{(Q_c)_1}T_{22}\right|_{(Q_c)_1=0}
 =P_1\beta K(b^U,Z)-dP_1\left.T_{22}\right|_{(Q_c)_1=0}.
```

The pure-$`H`$ coefficient of $`Z`$ is $`\eta`$: positive $`B`$ mean
insertions cannot contribute to an all-$`H`$ word, so it is the same as
at zero, where (8) gives
$`E_{uv}(0)+eF=\eta h^U`$. Thus $`K(b^U,Z)=\eta`$. Using
(9) and the same injective substitution proves

```math
 a_c+da=\beta\eta.
```

Finite polynomial degree and $`d\ne0`$ force $`a=\beta\eta/d`$, independent
of all three Gram variables. At the origin,

```math
 a(0)=K(F,E_{uv}(0)+eF)=\eta K(F,h^U)=\eta\alpha.
```

Since $`\eta\ne0`$, this proves

```math
 \beta=B_{pq}\mathrm{haf}\bigl(B[V\setminus\{p,q\}]\bigr)
 \qquad\text{whenever }B_{pq}\ne0.
 \tag{10}
```

No source deformation, differentiation of source equations along an
unlicensed direction, infinite series, or positivity argument occurs here.
The variables $`P,Q_c`$ are independent proof parameters, not actual graph rows.
$`\square`$

## 5. Every color is a perfect matching

**Corollary 5.1 (Matching rigidity of every active color).**
Each color graph of a source (1) is a weighted perfect matching.

**Proof.**
The ordinary hafnian expansion at a vertex $`p`$ says

```math
 \beta=\sum_{q\ne p}B_{pq}\mathrm{haf}\bigl(B[V\setminus\{p,q\}]\bigr).
```

By (10), every nonzero summand equals $`\beta`$. Since
$`\beta\ne0`$, the number of supported $`B`$ neighbors of $`p`$ is exactly
one. This holds at every vertex, and for each of the three colors by choosing
any other active color as $`H`$.
$`\square`$

Two such matchings cannot share an edge $`pq`$: choosing that edge in color
$`B`$ and the other matching in color $`H`$ off $`p,q`$ gives a mixed word
with nonzero coefficient, the product of nonzero matching weights.
Consequently their union is a simple cubic graph properly colored with three
colors. Any receiving color word supports at most one matching, because each
vertex has exactly one incident edge of its requested color. Therefore a
mixed perfect matching would have a nonzero coefficient and violate
(1).

## 6. The remaining graph lemma

The following standard unweighted obstruction is usually attributed to
Bogdanov; it is also stated as Theorem 7 in the HTML version of
[Chandran–Gajjala–Illickan, Krenn–Gu conjecture for sparse graphs](https://arxiv.org/html/2407.00303).
No new graph-theoretic result is claimed here.

**Lemma 6.1 (Three-matching obstruction).**
Three pairwise disjoint perfect matchings $`F,G,H`$ on $`n>4`$ vertices
have a mixed perfect matching in their union.

**Proof.**
Suppose otherwise. The union $`F\cup G`$ must be a single alternating
Hamilton cycle $`C`$: otherwise choosing $`F`$ on one component and $`G`$
on the others already gives a mixed matching. Label its vertices
$`0,\ldots,n-1`$ cyclically. The matching $`H`$ consists of chords.

A chord with endpoints of opposite parity leaves two even paths when its
endpoints are deleted. Matching those paths along $`C`$ and adding the chord
gives a mixed perfect matching. Hence all $`H`$ chords join equal parities.
The two parity classes must each have even size; otherwise $`H`$ is impossible.

An even-even chord and an odd-odd chord whose endpoints interlace leave four
even paths on deleting their endpoints. Those paths and the two chords give
a mixed perfect matching when $`n>4`$. Thus no such pair interlaces.

Choose a chord and one of its sides with the fewest vertices strictly inside,
over all chords and both sides. Its endpoints have equal parity, so its
interior contains a vertex of the opposite parity. Every vertex of that
opposite parity in the interior must be $`H`$-matched to another interior
vertex; a partner outside would give an interlacing opposite-parity chord.
Therefore some $`H`$ chord lies strictly inside the chosen arc. One side of
that chord has fewer interior vertices, a contradiction.
$`\square`$

This supplies a mixed perfect matching, contradicting Section 5.
Equation (1) is impossible for every even $`n>4`$, completing
the proof of Theorem 1.1.

## 7. Boundaries, provenance, and review scope

For $`n=4`$, the three matchings of $`K_4`$ give the permitted ternary
source. In Section 6, a pair of interlacing chords then exhausts
the vertices and gives the pure third matching, so no contradiction is asserted.
Sections 2–5 remain valid at $`n=4`$, including
their terminal response coefficients. For $`n=2`$, the odd-core lemma does not
apply and arbitrary target dimension is possible. Odd $`n`$ has no perfect
matchings in this model.

The earlier written foundations are collected in
[the higher-response directory](../computations/unaudited-codex-higher-common-power-bridge-2026-09-05/UNIFORM-THREE-ACTIVE-COLOR-HIGHER-PURE-RESPONSE-VANISHING.md),
with separate proofs and audits of reflection, even omission, and global
diagonal reduction. The new step is Section 4: finite
$`\mathrm O(2)`$ covariance and two original root identities force the
endpoint equality. Sections 2–3 are included
here so that the all-orders conclusion has no dependency on a finite
enumeration, an unproved normalization operation, or an assumed vanishing
of three-color higher responses.
