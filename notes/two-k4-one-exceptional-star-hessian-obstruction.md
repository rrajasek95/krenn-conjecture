# One exceptional component still cannot evade Hessian erasure

## 1. Result

Consider the two-`K_4` chart with the standard unit ternary equality source
on each shore.  Suppose one cross-block row is completely invertible and a
second row has at least three invertible blocks.  After relabelling, write

\[
 \det B_{sj}\ne0\quad(0\leq j<4),\qquad
 \det B_{rj}\ne0\quad(j\ne h),                          \tag{1}
\]

with no assumption on `B_rh`.

**Theorem 1.1.**  The blocks in (1) cannot satisfy the full matching-tensor
equations.

This strengthens
[`two-k4-four-singular-row-obstruction.md`](two-k4-four-singular-row-obstruction.md),
where both displayed block rows were assumed completely invertible.  The
new ingredient is a one-exceptional-component version of the six-cell
Hessian erasure lemma.  Instead of forcing the entire effective quadratic
to vanish, it forces its three blocks incident with the exceptional site
to vanish; that is already incompatible with the right `K_4`.

As a finite consequence, an exactly-four-singular two-`K_4` array must have
one singular block in every block row and every block column.  Hence, up to
row and column permutations, its only remaining position support is the
transversal matching

\[
                       (0,0),(1,1),(2,2),(3,3).         \tag{2}
\]

In particular the `3`-row/`4`-column orbit

\[
                       (0,0),(0,1),(1,2),(2,3)          \tag{3}
\]

and its transpose are impossible for arbitrary ranks of the four singular
blocks.  The exact audit is

```text
computations/verify_two_k4_one_exceptional_star_hessian.py
```

## 2. Square-free notation

Let

\[
             \mathcal R=\bigotimes_{i=0}^3(\mathbb C\oplus V_i),
             \qquad V_i^2=0,\qquad \dim V_i=3.          \tag{4}
\]

For a three-space `U`, maps `P_i,S_i:U -> V_i`, and `alpha,beta in U`,
put

\[
 p_\alpha=\sum_iP_i\alpha,\qquad
 s_\beta=\sum_iS_i\beta.                               \tag{5}
\]

If `q in R_2`, its pulled-back pair Hessian is

\[
                 \beta_q(\alpha,\beta)=q p_\alpha s_\beta
                           \in\mathcal R_4.              \tag{6}
\]

We use two kernels proved in Sections 3--4 of the preceding note.

* If every `S_i` is an isomorphism and a cubic `T` satisfies
  `T s_beta=0` for every `beta`, then `T` is on the alternating
  four-vector line `Omega_S`.  Every hole component of a nonzero
  `Omega_S` is a determinant tensor and has all three mode ranks equal to
  three.
* If a linear element `p=sum_i p_i` has every `p_i` nonzero and `qp=0`,
  then

  \[
       q_{ij}=z_{ij}p_i\otimes p_j,\qquad
       z_{ij}+z_{ik}+z_{jk}=0                            \tag{7}
  \]

  on every three-site subset.

Both statements are elementary coefficient comparisons over
characteristic zero.

## 3. One-exceptional-component erasure

**Lemma 3.1.**  Let every `S_i` be an isomorphism.  Fix a site `h`, assume
`P_i` is an isomorphism for `i != h`, and allow `P_h` to be arbitrary.
Let `U_0 subset U` be a two-plane.  If

\[
              \beta_q(\alpha,\beta)=0
              \qquad(\alpha\in U_0,\ \beta\in U),       \tag{8}
\]

then

\[
                         q_{hi}=0\qquad(i\ne h).         \tag{9}
\]

**Proof.**  For every `alpha in U_0`, condition (8) and the first kernel
above give

\[
                         q p_\alpha=\ell(\alpha)\Omega_S \tag{10}
\]

for one linear functional `ell` on `U_0`.  Choose nonzero
`alpha in ker ell`, so that

\[
                              q p_\alpha=0,              \tag{11}
\]

and choose `alpha' in U_0` independent of `alpha`.  Write
`p_i=P_i alpha` and `p'_i=P_i alpha'`.  For `i != h`, the pairs
`p_i,p'_i` are independent.

Suppose first that `p_h` is nonzero.  The second kernel above gives (7).
The hole-`h` component of `q p_(alpha')` is supported, at each of its
three sites, on `span(p_i,p'_i)`.  Its mode ranks are therefore at most
two.  Equation (10) for `alpha'` cannot make this a nonzero determinant
tensor, so `ell(alpha')=0` and

\[
                              q p_{\alpha'}=0.            \tag{12}
\]

In the hole-`h` component of (12), the three terms have `p'_i` at three
different sites and `p_i` at the other two.  They are linearly independent,
so all three `z_ij` with `i,j != h` vanish.  The three remaining triangle
relations in (7) are

\[
 z_{hi}+z_{hj}=0\qquad(i\ne j,\ i,j\ne h).              \tag{13}
\]

Their only characteristic-zero solution is zero.  Thus `q=0`, which is
stronger than (9).

It remains to suppose `p_h=0`.  Let `i,j,k` be the other three sites and
take the component of (11) on `{h,i,j}`, whose hole is `k`.  It reads

\[
                    q_{hi}p_j+q_{hj}p_i=0.              \tag{14}
\]

Two-term pure-factor cancellation says that

\[
             q_{hi}=x_i\otimes p_i,\qquad
             q_{hj}=x_j\otimes p_j,\qquad x_i+x_j=0,    \tag{15}
\]

where `x_i,x_j in V_h`.  Running (14) over the three pairs makes (15)
hold simultaneously for vectors `x_i,x_j,x_k`.  Hence

\[
                     x_i+x_j=x_i+x_k=x_j+x_k=0.
\]

Characteristic zero gives all three vectors zero, proving (9). `QED`

The proof allows `P_h=0`, rank one, rank two, or rank three.  What matters
is that the other three components of `P` and all four components of `S`
are isomorphisms.

## 4. Pullback of the two-`K_4` sectors

Let `{a,b}` be the two left rows complementary to `{r,s}`, and put

\[
                         c=\kappa(ab)=\kappa(rs).        \tag{16}
\]

On the four right sites define the colour-row stars

\[
             p_{i,x}=\sum_{j=0}^3
                     \operatorname{row}_x(B_{ij})^{(j)}. \tag{17}
\]

Let `q_R` be the standard right-`K_4` quadratic and define

\[
                         q_{\rm eff}=q_R+p_{a,c}p_{b,c}. \tag{18}
\]

Fix colours `c,c` at left sites `a,b`, and colours `x,y` at `r,s`.
Exactly as in the full-erasure identity, the complete two-/four-cross
sector is

\[
                    \beta_{q_{\rm eff}}(p_{r,x},p_{s,y}). \tag{19}
\]

When `(x,y)!=(c,c)`, the left word is nonconstant and its only compatible
internal edge is `ab`.  There is no zero-cross term and the target
coefficient is zero.  Thus

\[
        \beta_{q_{\rm eff}}(p_{r,x},p_{s,y})=0
                         \qquad((x,y)\ne(c,c)).          \tag{20}
\]

Use only the six equations with `x != c` and arbitrary `y`.  For row `r`,
the maps

\[
               x\longmapsto\operatorname{row}_x(B_{rj}) \tag{21}
\]

are isomorphisms at the three sites `j != h`, while the map at `h` is
arbitrary.  All four analogous maps for row `s` are isomorphisms.  Lemma
3.1 therefore gives

\[
                    (q_{\rm eff})_{hi}=0\qquad(i\ne h). \tag{22}
\]

## 5. The right `K_4` cannot lose an incident star

Write

\[
             u_j=\operatorname{row}_c(B_{aj}),\qquad
             v_j=\operatorname{row}_c(B_{bj]).          \tag{23}
\]

For every `i != h`, equation (22) is

\[
 e_{\kappa(hi)}\otimes e_{\kappa(hi)}
       +u_h\otimes v_i+v_h\otimes u_i=0.                \tag{24}
\]

Looking only at the endpoint space `V_h`, (24) puts

\[
                         e_{\kappa(hi)}
                              \in\operatorname{span}(u_h,v_h).          \tag{25}
\]

As `i` ranges over the other three right sites, `kappa(hi)` ranges over
all three colours.  The left side of (25) therefore spans `V_h`, while the
right side has dimension at most two.  This contradiction proves Theorem
1.1.

## 6. Exactly four singular positions

Suppose an exactly-four-singular support omits a block row.  That row is
completely invertible.  Among the other three rows, at least one contains
at most one of the four singular positions.  Theorem 1.1 excludes the
array.  Transposition similarly shows that the support omits no block
column.  Four positions meeting all four rows and all four columns form a
transversal matching, proving the reduction to (2).

This is a position reduction only.  It does not yet exclude the matching
orbit itself, nor any stratum with five or more singular blocks.
