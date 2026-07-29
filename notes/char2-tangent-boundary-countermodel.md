# The tangent GHZ boundary is uniformly realizable in characteristic two

## Outcome

For every even `n >= 4` and every field of characteristic two, the tangent
tensor

\[
 W_n=\sum_{r=0}^{n-1}e_0^{\otimes r}\otimes e_1
                         \otimes e_0^{\otimes(n-1-r)}       \tag{1}
\]

is an arbitrary-matrix matching tensor.  The construction is explicit and
uses only the two colors `0,1`; all cells involving color two vanish.

This is a uniform countermodel to any proposed arithmetic bridge that tries
to exclude every non-diagonal boundary of ternary GHZ after reduction.  The
tensor (1) is itself a projective GHZ boundary:

\[
 t^{-1}\left((e_0+t e_1)^{\otimes n}-e_0^{\otimes n}
                              +t^2e_2^{\otimes n}\right)
                       \longrightarrow W_n.                \tag{2}
\]

For `t != 0`, the tensor in parentheses is in the local `GL_3` orbit of
`Delta_(n,3)`.  Thus arbitrary local normalization can land on a genuine
characteristic-two matching tensor of border rank two and tensor rank much
larger than two.

## 1. The odd-cycle reference form

Use vertices `0,1,...,n-1`.  Let `C` be the alternating `n by n` matrix over
`F_2` whose only nonzero upper-triangular entries are the edges of the odd
cycle on `1,...,n-1`:

\[
 12,23,\ldots,(n-2)(n-1),(n-1)1.                           \tag{3}
\]

Vertex zero is isolated.  Put

\[
                         v=e_0+e_1,\qquad
                         t=(t_0,\ldots,t_{n-1})^T           \tag{4}
\]

and define the alternating matrix

\[
                         B(t)=C+vt^T+tv^T.                 \tag{5}
\]

The last two terms form a decomposable alternating rank-two update in
characteristic two.

## 2. Exact Pfaffian calculation

For an alternating matrix `C` and a decomposable two-form `v wedge t`, the
Pfaffian rank-two update identity is

\[
 \operatorname {Pf}(C+vt^T+tv^T)
 =\operatorname {Pf}C+
   \sum_{i<j}(v_it_j+v_jt_i)\operatorname {Pf}C[\widehat{i,j}]. \tag{6}
\]

There are no higher update terms because `(v wedge t)^2=0`.  The identity
may also be checked directly by grouping matching terms according to the
unique chosen update edge.

Here `Pf C=0` because vertex zero is isolated.  If neither deleted vertex
is zero, the complementary matrix still has that isolated vertex, so its
Pfaffian vanishes.  If the deleted pair is `{0,j}` with `j>=1`, deleting
`j` from the odd cycle leaves an even path.  That path has a unique perfect
matching, hence

\[
                         \operatorname {Pf}C[\widehat{0,j}]=1. \tag{7}
\]

Equations (4), (6), and (7) give

\[
 \operatorname {Pf}B(t)
   =\sum_{j=1}^{n-1}(v_0t_j+v_jt_0)
   =t_0+t_1+\cdots+t_{n-1}.                                \tag{8}
\]

## 3. Conversion to endpoint-local matching cells

Introduce local binary variables `x_(i,0),x_(i,1)` and set
`t_i=x_(i,1)/x_(i,0)`.  Multiplying the `(i,j)` entry of (5) by
`x_(i,0)x_(j,0)` gives the endpoint-local bilinear form

\[
 C_{ij}x_{i,0}x_{j,0}
   +v_i x_{i,0}x_{j,1}
   +v_j x_{i,1}x_{j,0}.                                   \tag{9}
\]

Thus put

\[
 A_{ij}^{00}=C_{ij},\qquad
 A_{ij}^{01}=v_i,\qquad
 A_{ij}^{10}=v_j,\qquad
 A_{ij}^{11}=0,                                           \tag{10}
\]

and set all color-two cells to zero.  Restoring the factored local
`x_(i,0)` variables in (8) yields

\[
 \operatorname {Pf}B(x)=
       \sum_i x_{i,1}\prod_{j\ne i}x_{j,0}.               \tag{11}
\]

In characteristic two the Pfaffian signs equal the unsigned matching signs.
Coefficient comparison in (11) proves `H_n(A)=W_n` over every
characteristic-two field.

The exact audit
`computations/verify_char2_tangent_boundary_countermodel.py` constructs
(10), enumerates all matching coefficients for `n=4,6,8,10`, and checks
(11) directly over `F_2`.  Since the polynomial identity has coefficients
zero and one, that audit represents the same identity over every extension
field of characteristic two.

## 4. Consequence for the arithmetic route

The following zeroth-order boundary outputs are all genuine
characteristic-two matching tensors:

* rank one `e_0^(tensor n)`, from a single perfect matching;
* diagonal rank two `e_0^(tensor n)+e_1^(tensor n)`, from the two alternating
  perfect matchings of a Hamilton cycle; and
* the non-diagonal tangent tensor `W_n`, by (10).

Therefore target geometry, determinant valuations, and the
characteristic-two matching equations cannot force a hypothetical
normalization away from the rank-one, rank-two, or tangent strata.  Any
successful bridge must use higher-jet information tied to the original
characteristic-zero constant coefficients.
