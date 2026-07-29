# Two completely invertible block rows are impossible

## 1. Result

Consider the two-`K_4` chart with standard ternary equality sources on both
shores.  Suppose two cross-block rows, say `r` and `s`, are completely
invertible:

\[
                  \det B_{rj}\ne0,\qquad \det B_{sj}\ne0
                         \quad(0\le j<4).                 \tag{1}
\]

**Theorem 1.1.**  The blocks in (1) cannot satisfy the full matching-tensor
equations.

The proof uses the mixed equations omitted by the dead-slab incidence
audit.  For any internal left edge `0t`, they pull back one right-shore
pair Hessian to a table supported on only one input cell.  A four-site
six-cell erasure lemma shows that even the two zero input rows force the
effective right quadratic to vanish.  That is impossible: the standard
right `K_4` has three independent incident endpoint lines at every site,
whereas a product of two stars has endpoint span at most two.

Consequently the singular positions of any two-`K_4` solution meet at least
three block rows and, by transposition, at least three block columns.  In
particular, this closes every exact-four position orbit supported on at most
two rows or at most two columns; the full-row and full-column orbits are the
most concentrated examples.

## 2. Four-site six-cell Hessian erasure

Let

\[
             \mathcal R=\bigotimes_{i=0}^3(\mathbb C\oplus V_i),
             \qquad V_i^2=0,\qquad \dim V_i=3.           \tag{2}
\]

Let `U` be a three-space and let

\[
                 P_i,S_i:U\longrightarrow V_i           \tag{3}
\]

be isomorphisms for all four sites.  Write

\[
 p_\alpha=\sum_iP_i\alpha,\qquad
 s_\beta=\sum_iS_i\beta.                                \tag{4}
\]

For a quadratic `q in R_2`, define its pulled-back pair Hessian

\[
                  \beta_q(\alpha,\beta)=q p_\alpha s_\beta
                         \in\mathcal R_4.                 \tag{5}
\]

**Lemma 2.1 (six-cell erasure).**  Let `U_0 subset U` be a two-plane.  If

\[
                  \beta_q(\alpha,\beta)=0
                  \qquad(\alpha\in U_0,\ \beta\in U),    \tag{6}
\]

then `q=0`.

Thus a `3 by 3` pulled-back Hessian table cannot be supported in one input
row, much less in one input cell.  Notice that (6) erases only six of the
nine cells.

## 3. The two elementary multiplication kernels

We prove Lemma 2.1 without a genericity assumption.  Two small kernels are
the whole argument.

**Lemma 3.1 (common invertible-star annihilator).**  If `T in R_3` obeys

\[
                         T s_\beta=0\qquad(\beta\in U),   \tag{7}
\]

then `T` belongs to a one-dimensional space.  After identifying every
`V_i` with `U` by `S_i`, its component with hole `i` is

\[
                    T_i=\lambda(-1)^i\operatorname {Det}_3              \tag{8}
\]

on the other three sites.  If `lambda` is nonzero, every one-mode
flattening of every `T_i` has rank three.

**Proof.**  Normalize `S_i=id`.  Write `T_i` for the component missing
site `i`.  At an output word `a=(a_0,a_1,a_2,a_3)`, the coefficient of
the input coordinate `b` in (7) is

\[
                         \sum_{i:a_i=b}T_i(a_{\widehat i})=0.             \tag{9}
\]

If a triple indexing `T_i` omits a color `b`, put that color at the hole.
It then occurs exactly once in (9), forcing the coefficient to vanish.
Hence `T_i` is supported only on the six permutations of `012`.  Applying
(9) to words with one repeated color relates two such coefficients at a
time.  These relations connect all four sets of six coefficients and give
exactly the alternating signs in (8).  The determinant tensor has mode
rank three.  \(\square\)

**Lemma 3.2 (kernel of one full-support linear element).**  Let
`p=sum_i p_i`, with every `p_i` nonzero.  If `qp=0`, then

\[
                         q_{ij}=z_{ij}p_i\otimes p_j,     \tag{10}
\]

where the six scalars satisfy

\[
                         z_{ij}+z_{ik}+z_{jk}=0           \tag{11}

for every three-site subset `{i,j,k}`.  This kernel has dimension two.

**Proof.**  Choose local bases with `p_i=e_0`.  In a three-site component
of `qp`, a coefficient having two nonzero colors comes from only one block
and kills every entry `q_ij(a,b)` with `a,b!=0`.  For an entry with just
one nonzero endpoint color, the three choices of the third site give
`u_ij+u_ik=0`, `u_ij+u_iell=0`, and `u_ik+u_iell=0`.
Characteristic zero gives `u=0`.  Only the `00` entries remain, and the
all-zero three-site coefficients are exactly (11).  The four triangle
equations on six edges have rank four.  \(\square\)

## 4. Proof of the erasure lemma

For `alpha in U_0`, equation (6) says that the cubic

\[
                              T_\alpha=qp_\alpha          \tag{12}
\]

is annihilated by the whole invertible star `S`.  Lemma 3.1 puts every
`T_alpha` on one fixed line.  The map

\[
                         U_0\longrightarrow\mathcal R_3,
                         \qquad\alpha\longmapsto T_\alpha              \tag{13}
\]

therefore has a nonzero kernel.  Choose independent `alpha,alpha' in U_0`
with

\[
                         qp_\alpha=0.                    \tag{14}

Lemma 3.2 writes `q` as in (10), with `p_i=P_i alpha`.  Since every `P_i`
is invertible, `p_i` and `p'_i=P_i alpha'` are independent at every site.

The cubic `qp_(alpha')` is again on the determinant line (8).  On the
other hand, every factor in each of its hole components belongs to the
two-plane `span(p_i,p'_i)`.  Its one-mode ranks are therefore at most two.
The nonzero tensor in (8) has rank three at every mode, so necessarily

\[
                         qp_{\alpha'}=0.                 \tag{15}

In a three-site component of (15), the three terms have `p'` at three
different sites and `p` at the other two.  They are linearly independent,
so all three corresponding scalars `z_ij,z_ik,z_jk` vanish.  Varying the
three-site subset kills all six scalars.  Hence `q=0`, proving Lemma 2.1.

## 5. Pullback of the two-`K_4` sectors

Relabel the two invertible rows as `r,s`, let the other two rows be `0,t`,
and put

\[
 c=\kappa(0t),\qquad \{r,s\}=\{1,2,3\}\setminus\{t\}.   \tag{16}
\]

On the four right sites define the color-row stars

\[
                         p_{i,x}=\sum_{j=0}^3
                              \operatorname {row}_x(B_{ij})^{(j)}.       \tag{17}

\]

Let `q_R` be the standard right `K_4` quadratic and put

\[
                         q_{\rm eff}=q_R+p_{0,c}p_{t,c}. \tag{18}

If the left word has color `c` at `0,t` and colors `x,y` at `r,s`, then
the complete two-/four-cross contribution is exactly

\[
                         \boxed{\ \beta_{q_{\rm eff}}
                                (p_{r,x},p_{s,y}).\ }     \tag{19}

\]

Indeed, the `q_R` part chooses one right internal edge and gives the
two-cross permanent; the product in (18) assigns the other two left stars
and gives the four-cross permanent.  If `(x,y)!=(c,c)`, the left word is
nonconstant and has exactly the one compatible internal edge `0t`.
There is no zero-cross term, and the full target coefficient is zero.
Therefore

\[
                \beta_{q_{\rm eff}}(p_{r,x},p_{s,y})=0
                            \qquad((x,y)\ne(c,c)).        \tag{20}


Every component map `x mapsto row_x(B_rj)` and
`y mapsto row_y(B_sj)` is invertible by (1).  In particular the two rows
`x!=c` in (20), with all three values of `y`, satisfy Lemma 2.1.  Hence

\[
                              q_{\rm eff}=0.              \tag{21}

## 6. The effective quadratic cannot vanish

Put

\[
                 u_j=\operatorname {row}_c(B_{0j}),\qquad
                 v_j=\operatorname {row}_c(B_{tj}).      \tag{22}

The `ij` block of their square-free product is

\[
                         u_i\otimes v_j+v_i\otimes u_j.  \tag{23}

At endpoint `i`, its image lies in the fixed plane
`span(u_i,v_i)`, of dimension at most two.  But the three blocks of the
standard `q_R` incident with `i` have endpoint factors

\[
                         e_{\kappa(ij)}\qquad(j\ne i).    \tag{24}

The three colors in (24) are distinct, so these factors span `V_i`.
Consequently `q_R` cannot equal `-p_(0,c)p_(t,c)`, contradicting (21).
This proves Theorem 1.1.

## 7. Exact audit

Run

```text
python computations/verify_two_k4_four_singular_row_obstruction.py
```

The checker verifies the two kernel dimensions `1` and `2`, their explicit
generators, full `54/54` six-cell-erasure rank in canonical and nontrivial
invertible charts, all `729` coefficients of the effective-Hessian sector
identity, and the final three-line versus two-plane contradiction.
