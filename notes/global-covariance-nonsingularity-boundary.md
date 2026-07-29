# Global covariance nonsingularity is a genuinely ternary question

## Outcome

Let `Z(A)` be the symmetric global port matrix with off-diagonal blocks
`A_uv` and reverse blocks `A_uv^T`.  The palette-uniform implication

\[
                 H_{n,q}(A)=\Delta_{n,q}\quad\Longrightarrow\quad
                 \det Z(A)\ne0                              \tag{1}
\]

is false.  There is an exact rational binary counterexample already at
`n=4`, the smallest nontrivial order.  Its global `8 by 8` covariance has
nullity two.  After embedding it in three colors it is a singular point
over the rank-two GHZ boundary.

Singularity also survives substantially stronger ternary boundary data:

* a cofactor-open four-site source with the exact `01` and `02` faces and
  every mixed-with-zero equation has covariance rank `8/12`; and
* a rational six-site source with all three binary faces exact has
  covariance rank `12/18`.

Neither is full ternary equality.  Conversely, the standard exact ternary
`K_4`, the all-exceptional one-error model, and every finite member of the
prism border family have nonsingular covariance (determinant `1,-1,-1`,
respectively, in the normalizations below).  Thus the precise ternary claim

\[
                 H_{n,3}(A)=\Delta_{n,3}
                 \quad\Longrightarrow\quad\det Z(A)\ne0   \tag{2}
\]

remains plausible, but none of constant fibers, all binary faces, cofactor
openness, mixed cubic contact, Gaussian physicality, or closeness to the
target proves it.  Any proof of (2) must use a genuinely ternary full-target
equation.

## 1. Smallest exact countermodel to the uniform statement

On vertices `0,1,2,3`, use only same-color cells.  For color zero put

\[
 A_{01}^{00}=A_{02}^{00}=1,
 \qquad A_{23}^{00}=A_{13}^{00}=\frac12,                  \tag{3}
\]

and for color one put

\[
                         A_{03}^{11}=A_{12}^{11}=1.        \tag{4}
\]

The three supported perfect matchings are `01|23`, `02|13`, and `03|12`.
The first two are all zero and have weights `1/2,1/2`; the last is all one
and has weight one.  Hence exactly

\[
                         H_{4,2}(A)=X_0+X_1.               \tag{5}
\]

Ordering the four color-zero ports as the bipartition `{0,3}|{1,2}`, their
covariance is

\[
 \begin{pmatrix}0&B\\B^T&0\end{pmatrix},\qquad
 B=\begin{pmatrix}1&1\\[1mm]1/2&1/2\end{pmatrix}.        \tag{6}
\]

Thus this block has rank two and nullity two.  The color-one block is the
adjacency of a perfect matching and has rank four.  Therefore

\[
                         \operatorname {rank}Z(A)=6<8.    \tag{7}
\]

More generally, in the norm-flat family with the two color-zero matching
products `c^2,s^2`, the determinant of (6) is `(c^2-s^2)^2`, whereas the
required unsigned matching coefficient is `c^2+s^2`.  Equality of the two
products cancels the determinant without cancelling the hafnian.  This is
the basic mechanism a ternary proof must exclude.

At `n=2`, binary equality is one invertible `2 by 2` endpoint block and its
global covariance is nonsingular, so (3)--(7) are order-minimal.

## 2. Strong ternary boundary countermodels

The cofactor-open clone in
[`cofactor-open-color-cloning-boundary.md`](cofactor-open-color-cloning-boundary.md)
is the pullback of an invertible binary covariance by rank-two local maps

\[
             (x_0,x_1,x_2)\longmapsto(x_0,x_1+\lambda_i x_2). \tag{8}
\]

Consequently its global matrix factors through an eight-dimensional port
space.  The exact rational instance has rank exactly eight.  Nevertheless
its `01` and `02` faces are both binary equality, it is cofactor-open, and
every coefficient containing color zero together with another color
vanishes.  Only the omitted full-support `12` face detects the failure.

There is an even stronger six-site warning.  Rationally reweight the three
five-edge families in Proposition 3.1 of
[`binary-norm-equality-counterfamily.md`](binary-norm-equality-counterfamily.md)
so that each of the two monochromatic matching products in a four-cycle is
`1/2`.  Every pair of colors still gives exact binary equality.  For each
color, however, the port covariance is an isolated matching edge plus a
four-cycle whose two signed matching products cancel.  It has rank four of
six.  The complete global matrix therefore has

\[
                         \operatorname {rank}Z=12<18.     \tag{9}
\]

The nine remaining full-tensor coefficients use all three colors and are
nonzero singletons.  Thus all three binary faces still do not imply (2).

## 3. Positive audits and the exact remaining claim

For the standard ternary `K_4`, every one of the twelve ports has exactly
one unit covariance neighbor.  The global matrix is six disjoint `2 by 2`
exchange blocks, so `det Z=1`.

The three pairwise-Hamilton factors of the all-exceptional rainbow model
likewise pair all eighteen ports and give `det Z=-1`, despite their one
rainbow target error.  The prism Laurent family also pairs all ports.  The
product of its nine edge weights is the product of its three normalized
constant matching products, namely one, so

\[
                         \det Z(t)=-1\qquad(t\ne0).        \tag{10}
\]

Thus its approach to ternary GHZ is not accompanied by a covariance
determinant degeneration; instead reciprocal singular values diverge and
vanish while their product remains fixed.  The saved numerical prism
candidate reflects exactly this behavior (`det Z` is approximately `-1`).

These checks leave (2), not (1), as the usable conjectural lemma.  They also
show that a continuity, binary-restriction, or cofactor-contact proof of it
cannot work.

## 4. What a covariance kernel gives the pair Hessian

There is a precise source-relative identity, but it is not by itself an
extra-kernel theorem.  Delete sites `p,q`, put `W=B\setminus\{p,q\}`, and
write

\[
 Q=q+\sum_cx_{p,c}p_c+\sum_dx_{q,d}s_d
          +\sum_{c,d}a_{cd}x_{p,c}x_{q,d}.                \tag{11}
\]

Let `xi=(xi_v)` lie in `ker Z(A)`, and put

\[
 \alpha=\xi_p,\quad\beta=\xi_q,\quad
 p_\alpha=\sum_c\alpha_cp_c,\quad
 s_\beta=\sum_d\beta_ds_d.                               \tag{12}
\]

Contracting the quadratic source by `xi` and separating site supports gives
the exact kernel-star identity

\[
                    \iota_{\xi_W}q+p_\alpha+s_\beta=0.    \tag{13}
\]

The components on the two deleted sites give the two companion identities
`A_(p|q) beta+p(xi_W)=0` and
`A_(q|p) alpha+s(xi_W)=0`.  These use the actual source blocks; they are not
derivatives of the target tensor.

Let `r=n/2-1` and

\[
                 \mathcal H_q(R)=Rq^{r-1}.                \tag{14}
\]

Contracting the nine exact pair equations by `alpha_c beta_d` gives

\[
 \mathcal H_q\!\left(
       a(\alpha,\beta)q+r p_\alpha s_\beta\right)
   =r!\sum_c\alpha_c\beta_cX_c.                           \tag{15}
\]

Using (13), the quadratic on the left can equivalently be written

\[
 a(\alpha,\beta)q-rp_\alpha^2
                    -rp_\alpha\iota_{\xi_W}q.             \tag{16}
\]

Subtracting the three diagonal pair equations yields the explicit Hessian
kernel element

\[
\begin{aligned}
 K_{pq}(\xi)={}&
 \left(a(\alpha,\beta)-\sum_c\alpha_c\beta_ca_{cc}\right)q\\
 &+r\left(p_\alpha s_\beta
             -\sum_c\alpha_c\beta_cp_cs_c\right),
 \qquad \mathcal H_q(K_{pq}(\xi))=0.                      \tag{17}
\end{aligned}
\]

Equation (17) supplies a finite test: if for some pair it cannot be written
as a vertex gauge

\[
                 (K_{pq})_{ij}=(\gamma_i+\gamma_j)q_{ij},
                 \qquad\sum_i\gamma_i=0,                 \tag{18}
\]

then the pair Hessian has an extra kernel.  If every pair Hessian is
gauge-rigid, a hypothetical covariance kernel must instead satisfy (18) for
every pair simultaneously, together with (13).  This is the usable
kernel-to-Hessian reduction.  The binary countermodel shows why one cannot
skip the gauge-membership alternative and claim that singular covariance
automatically creates an extra Hessian kernel in every palette/order.

## 5. Exact audit

Run

```text
python computations/verify_global_covariance_boundary.py
```

The checker enumerates every matching coefficient in all five displayed
models and computes all ranks and determinants exactly over the rationals.
It verifies the binary counterexample, both singular ternary boundary
models, the nonsingular standard `K_4`, and the two determinant-`-1`
near-target six-site models.
