# Odd-prime inverse-hafnian reciprocity gives no GHZ obstruction

The inverse-hafnian identity is valid, in a stronger unsquared form, but
its large-diagonal expansion is tautological on the transversal sector.
Every coefficient in that expansion is one scalar, independent of the
site coloring, times the original transversal hafnian.  In particular,
the first potentially nonzero correction beyond the one-cross-per-site
term cannot distinguish a ternary GHZ tensor from any other transversal
tensor.

This note proves the identity without an external citation and gives an
exact characteristic-three four-site GHZ model in which that correction
is nonzero and harmless.

## 1. Exact reciprocity

Let `F` be a field of odd characteristic `p`, and put

\[
 m=p-1,\qquad q=\frac{p-1}{2},\qquad
 c_p=(p-2)!!=1\cdot3\cdots(p-2)\in F^\times.             \tag{1}
\]

Let `K` be an invertible symmetric `N by N` matrix.  For a vector
`alpha in {0,...,p-1}^N` of even total size, let `K^(alpha)` denote the
matrix obtained by repeating label `i` exactly `alpha_i` times, and write

\[
 H_\alpha(K)=\operatorname {haf}(K^{(\alpha)}),\qquad
 \beta=m\mathbf1-\alpha,qquad r=|\alpha|/2.             \tag{2}
\]

All factorials below are interpreted in `F`; they are units because their
arguments are less than `p`.

**Theorem 1.1 (inverse-hafnian reciprocity).**

\[
 \boxed{
 H_\alpha(K)=(-1)^r
   \frac{\prod_i\alpha_i!}{c_p^N}\,
   \det(K)^q H_\beta(K^{-1}).}                           \tag{3}
\]

In particular,

\[
 \boxed{
 H_\alpha(K)^2=(-1)^{N(q+1)}
   \left(\prod_i\alpha_i!\right)^2
   \det(K)^{p-1}H_\beta(K^{-1})^2.}                     \tag{4}
\]

Thus (4) is the proposed squared identity, including its exact factorial
and sign.

## 2. Formal truncated-Fourier proof

Work in the truncated polynomial algebra

\[
 R=F[x_1,\ldots,x_N]/(x_1^p,\ldots,x_N^p).              \tag{5}
\]

Define the truncated Gaussian vector

\[
 \Phi_K(x)=
 \sum_{0\le\gamma_i\le p-1\atop |\gamma|\ {m even}}
       \frac{H_\gamma(K)}{\prod_i\gamma_i!}x^\gamma.
                                                                  \tag{6}
\]

It obeys the exact equations

\[
 \left(\partial_i-\sum_jK_{ij}x_j\right)\Phi_K=0
 \qquad(1\le i\le N).                                  \tag{7}
\]

Away from the top boundary, comparison of the coefficient of `x^gamma`
in (7) is just the hafnian recurrence

\[
 H_{\gamma+e_i}(K)=
       \sum_j\gamma_jK_{ij}H_{\gamma-e_j}(K).            \tag{8}
\]

At the only missing boundary, `gamma_i=p-1`, the right side of (8) is the
hafnian with `p` identical copies of label `i`, and this is zero in
characteristic `p`.  Indeed, cyclically permute those `p` labeled copies.
No perfect matching is fixed: an outside partner cannot be paired to all
`p` copies, while the orbit of an internal two-subset is not a matching
when `p` is odd.  The matching monomials therefore occur in free orbits of
size `p`.  This proves (7), including its boundary equations.

The simultaneous kernel of the operators in (7) is one-dimensional.  If
`f` lies in it, the coefficient equation at `gamma=alpha-e_i`, for any
`alpha_i>0`, determines the coefficient of `x^alpha` from coefficients two
degrees lower.  Hence `f` is determined by its constant coefficient, and
`Phi_K` is the unique solution with constant coefficient one.

Define the algebraic Fourier operator `T:R -> R` in one variable by

\[
             T(x^a)=(-1)^a a!x^{p-1-a},                 \tag{9}
\]

and take its tensor product in the `N` variables.  Direct calculation,
including `a=0,p-1`, gives

\[
                    Tx_i=\partial_iT,
             \qquad T\partial_i=-x_iT.                  \tag{10}
\]

Apply `T` to (7) for `K^{-1}` and multiply the resulting operator equations
by `K`.  Equations (10) show that `T Phi_(K^{-1})` lies in the common kernel
for `-K`.  Uniqueness gives

\[
 T\Phi_{K^{-1}}=S(K)\Phi_{-K},qquad
 S(K)=H_{m\mathbf1}(K^{-1}),                             \tag{11}
\]

where the scalar is obtained by taking the constant coefficient.

It remains only to evaluate the top moment.  For every symmetric matrix
`L`,

\[
                  H_{m\mathbf1}(L)=c_p^N\det(L)^q.       \tag{12}
\]

Here is a self-contained proof.  Linear substitution in (6), followed by
the uniqueness just proved, gives

\[
             \Phi_{GLG^{\mathsf T}}(x)=\Phi_L(G^{\mathsf T}x).
                                                                  \tag{13}
\]

The top socle line `F x_1^m...x_N^m` in `R` transforms by
`det(G)^m`: this is immediate for diagonal matrices and permutations, and
for a transvection every other binomial term has some exponent at least
`p` and vanishes.  Over an algebraic closure every invertible symmetric
matrix is diagonalizable by congruence.  On a diagonal matrix the top
hafnian is

\[
       \prod_i (m-1)!!\,L_{ii}^{m/2}=c_p^N\det(L)^q.
\]

This proves (12) on the dense invertible locus, hence as a polynomial
identity.

Now compare the coefficient of `x^alpha` in (11).  The complementary term
on the left is exactly `H_beta(K^{-1})`; on the right it is

\[
 c_p^N\det(K)^{-q}
       \frac{(-1)^rH_\alpha(K)}{\prod_i\alpha_i!}.
\]

Rearranging proves (3).  Pairing the nonzero residues with their inverses
(only `1` and `-1` remain unpaired) gives `(p-1)!=-1`.  Replacing each
even residue by the negative of its complementary odd residue then gives

\[
 (p-1)!=(-1)^q c_p^2=-1,qquad
                    c_p^2=(-1)^{q+1}.                   \tag{14}
\]

Squaring (3) and using (14) proves (4).

## 3. Applying the identity to transversal hafnians

Let the Krenn matrix have `n` sites and three modes per site, so its scalar
dimension is `N=3n`.  We may take its within-site blocks to be zero because
they never occur in a transversal hafnian.  Denote the resulting symmetric
matrix by `A`.

For a site coloring `c`, let `alpha(c)` have one at the selected mode of
each site and zero at the other two modes.  Then

\[
 H_{\alpha(c)}(A)=H_A(c),\qquad |\alpha(c)|/2=n/2=:r.     \tag{15}
\]

Choose arbitrary invertible symmetric `3 by 3` matrices `D_v`, put
`D=directsum_v D_v`, and introduce

\[
                         L(z)=D+zA.                      \tag{16}
\]

The added within-site blocks still cannot occur in the selected principal
hafnian, while every matching has `r` cross-site edges.  Therefore

\[
                  H_{\alpha(c)}(L(z))=z^rH_A(c).         \tag{17}
\]

Every coordinate of `alpha(c)` is zero or one, so its factorial product is
one and does not depend on `c`.  Solving (3) for the inverse hafnian gives
the exact identity

\[
 \boxed{
 H_{m\mathbf1-\alpha(c)}(L(z)^{-1})
   =(-1)^r c_p^{3n}z^r\det(D+zA)^{-q}H_A(c).}            \tag{18}
\]

If `A` has ternary GHZ transversal tensor, the left side of (18) is zero
for every mixed coloring and is the same Laurent series for all three
constant colorings.  This holds coefficient by coefficient to every order,
not merely at the leading term.

For the formulation in the question, take `K=tD+A` and `z=t^{-1}`.  The
degree of the complementary hafnian is

\[
 s=\frac{|m\mathbf1-\alpha(c)|}{2}=3nq-r.
\]

Homogeneity and (18) give

\[
 H_{m\mathbf1-\alpha(c)}(K^{-1})
 =(-1)^r c_p^{3n}t^{-3nq}
   \det(D+t^{-1}A)^{-q}H_A(c).                           \tag{19}
\]

Thus adjoining the arbitrary blocks `D_v` has produced an exact scalar
multiple of the original system, not a new family of GHZ equations.

## 4. The first two corrections

Put `B=D^{-1}` and `X=BA`.  To second order,

\[
\begin{aligned}
 \det(D+zA)^{-q}
  =\det(D)^{-q}\bigg[1-q\operatorname {tr}(X)z
   +\frac{q^2\operatorname {tr}(X)^2
           +q\operatorname {tr}(X^2)}2z^2+O(z^3)\bigg]. \tag{20}
\end{aligned}
\]

This follows directly by expanding `tr log(I+zX)`; only division by two is
used, so (20) is valid for every odd `p`.

Since `B` is block diagonal and `A` has zero within-site blocks,
`tr(X)=0`.  Consequently the order immediately after the leading term in
(18) vanishes.  The first potentially nonzero correction is

\[
       \frac q2\operatorname {tr}((D^{-1}A)^2)           \tag{21}
\]

times the leading term.  Even if one retains arbitrary within-site blocks
in `A`, the preceding correction is merely `-q tr(D^{-1}A)` times the same
transversal tensor.  Neither coefficient can contradict GHZ.

The matching interpretation agrees with this calculation.  In

\[
 L(z)^{-1}=B-zBAB+z^2BABAB-\cdots,                       \tag{22}
\]

the total complementary multiplicity at every site is `3(p-1)-1`, which
is odd.  A term using only the within-site matrix `B` cannot match a site.
At least one cross correction must touch every site, so the minimum is
`r=n/2` first-order cross terms: the one-cross-per-site contribution.
All configurations one and two orders beyond it, including higher Neumann
terms and higher odd cross-degree site graphs, sum to the scalar
coefficients in (20).  Treating any one of those subfamilies separately
would discard cancellations required by the exact identity.

## 5. Exact `p=3`, four-site countermodel to the proposed obstruction

Use the standard three one-factors of `K_4`:

\[
 M_0=01|23,\qquad M_1=02|13,\qquad M_2=03|12,            \tag{23}
\]

and put a unit same-color covariance edge on `M_a` in color `a`.  Its
four-site transversal tensor is exactly ternary GHZ.

In characteristic three, take `D` diagonal on the twelve modes, with every
diagonal entry one except the mode `(site 0,color 0)`, whose entry is
`-1`.  The matrix `D+zA` is the direct sum of six two-mode blocks

\[
 \begin{pmatrix}d_u&z\\z&d_v\end{pmatrix},
       \qquad Q_{uv}=d_ud_v-z^2.                         \tag{24}
\]

Exactly one block has `d_ud_v=-1` and the other five have product one.  For
a constant site coloring, the two blocks of its selected color have
complementary multiplicities `(1,1)`, while the other four have `(2,2)`.
The inverse of (24) gives, modulo three,

\[
 H_{(1,1)}=-\frac z{Q_{uv}},\qquad
 H_{(2,2)}=\frac{d_ud_v+2z^2}{Q_{uv}^2}
           =\frac1{Q_{uv}}.                             \tag{25}
\]

Hence all three pure inverse hafnians are exactly

\[
 \frac{z^2}{\det(D+zA)}=2z^2+2z^4+O(z^6)\quad\text{in }F_3[[z]]. \tag{26}
\]

Every mixed coloring leaves some two-mode block with odd total
multiplicity.  Indeed, if site `0` has color `a`, parity on its `M_a` edge
forces its mate to have color `a`.  If the other `M_a` pair is not also
color `a`, choose its first site's color `b`; parity on its `M_b` edge
forces the other site to be `b`, making that pair an edge of both `M_a`
and `M_b`, impossible in a one-factorization.  Thus only constant
colorings have even totals in all six blocks.  A mixed inverse repeated
hafnian is consequently zero.  The `z^3` term
after the one-cross-per-site leading term vanishes, while the first
potentially nonzero correction, at `z^4`, is indeed nonzero and remains
the same on all three GHZ terms.  This is an exact countermodel to any
claim that the first nontrivial correction uniformly contradicts ternary
GHZ.  It is, of course, the allowed `n=4` GHZ construction and not a
counterexample to Krenn's conjecture itself.

## 6. Exact audit

Run

```text
uv run python computations/verify_odd_prime_inverse_hafnian.py
```

The checker:

1. verifies the Fourier constants and (14) for five odd primes;
2. clears denominators and proves every generic symmetric `2 by 2`
   instance of (3) symbolically for `p=3,5,7`;
3. exhausts all `468` invertible symmetric `3 by 3` matrices over `F_3`
   and all `100` invertible symmetric `2 by 2` matrices over `F_5`, checking
   `6552+1300` identities; and
4. checks all `81` site colorings and the nonzero correction (26) in the
   four-site GHZ model.

The conclusion does not depend on whether a hypothetical complex Krenn
solution admits good reduction at a particular prime: at every odd-prime
reduction where the construction is defined, inverse-hafnian reciprocity
repackages the original transversal equations exactly and supplies no new
constraint.
