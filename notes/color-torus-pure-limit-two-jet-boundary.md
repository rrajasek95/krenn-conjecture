# A pure color-torus limit has simultaneous two-jets

## Outcome

Apply the same local one-parameter subgroup

\[
                         \lambda(t)=\operatorname{diag}(1,t,t)       \tag{1}
\]

at every target site.  If `H(A)=Delta`, the transformed source has the
finite form

\[
                         q(t)=c+t b+t^2a                              \tag{2}
\]

and would satisfy

\[
 H(q(t))=X_0+t^n(X_1+X_2).                              \tag{3}
\]

There are three exact conclusions.

1. The finite leading source is not a selected matching.  It is an
   arbitrary scalar matrix `C` with `haf(C)=1`.
2. At every such leading point the two other colors have independent
   first-source-jet spaces of total dimension `2n(n-2)`.  On the open
   locus where every two-hole cofactor is nonzero, every such simultaneous
   first jet lifts uniquely through the second output equation.
3. This freedom is active, not merely formal dimension.  An exact rational
   six-site module below has a dense leading matrix, nonzero first jets in
   both other colors, vanishing output coefficients in degrees one and two,
   and nonzero terminal pure coefficients for both colors.  After two
   independent algebraic rescalings those two terminal coefficients are
   both one.  Its first failure is a genuinely ternary degree-three fibre.

Thus a uniform color-torus **first-jet** or **second-jet** theorem cannot
exclude simultaneous emergence of the two missing pure colors.  The first
possible generic compatibility is the third jet.  This is complementary
to `torus-osculation-top-half-countermodel.md`, whose sparse uniform family
survives through the middle, and to the balanced twelve-site module in
`torus-osculation-bottom-top-collision.md`, which survives seven reversed
orders before its first ternary layer.

## 1. A local color torus only regrades coefficient equations

More generally, let the diagonal one-parameter subgroup at site `v` have
weights `w_(v,0),w_(v,1),w_(v,2)`.  A source cell on `uv` with endpoint
colors `r,s` acquires weight

\[
                             w_{u,r}+w_{v,s}.             \tag{4}
\]

Every perfect matching compatible with one fixed coloring
`gamma:B -> {0,1,2}` therefore acquires the same total weight

\[
                             W(\gamma)=\sum_vw_{v,\gamma(v)}.          \tag{5}
\]

Consequently, coefficient by coefficient,

\[
        [e_\gamma]H(\lambda(t)A)
              =t^{W(\gamma)}[e_\gamma]H(A).             \tag{6}
\]

This identity retains arbitrary parallel-cell aggregation, asymmetric
endpoint colors, and complex cancellation.  In particular different
matching terms of one coloring can never be separated by a local target
torus: they always remain in the same jet.

For (1), `c` consists exactly of the `00` cells, `b` of cells with one
endpoint in `{1,2}`, and `a` of cells with both endpoints in `{1,2}`.
The order-zero equation in (3) is simply

\[
                         c=\sum_{i<j}c_{ij}x_ix_j,
              \qquad \operatorname{haf}C=1.             \tag{7}
\]

There is no further leading-source classification.  In particular (7)
does not imply unique matching support or even sparse support.

## 2. Complete first- and second-jet classification

Let

\[
 h_{i_1\cdots i_k}
   =\operatorname{haf}C[B\setminus\{i_1,\ldots,i_k\}].   \tag{8}
\]

Write `b^r_ij` for the directed cell with color `r in {1,2}` at `i` and
color zero at `j`.  Write `a_ik^(rs)` for the cell with colors `r,s` at
`i,k`.  Expanding (2) gives exactly

\[
             \sum_{j\ne i}b^r_{ij}h_{ij}=0
                  \qquad(i\in B,\ r\in\{1,2\}),         \tag{9}
\]

and

\[
 a_{ik}^{rs}h_{ik}
 +\sum_{\substack{j,\ell\notin\{i,k\}\\j\ne\ell}}
       b^r_{ij}b^s_{k\ell}h_{ikj\ell}=0.                \tag{10}
\]

These are respectively the complete coefficients of `t` and `t^2`.
Expansion of the full hafnian at `i` says

\[
                         \sum_{j\ne i}c_{ij}h_{ij}=1.    \tag{11}
\]

Thus every row in (9) is a nonzero functional on `n-1` variables.  Its
kernel has dimension `n-2`, independently for two colors and `n` sites,
giving total dimension

\[
                              2n(n-2).                   \tag{12}
\]

If every `h_ik` is nonzero, (10) independently and uniquely defines all
four cells `a_ik^(rs)` on every pair.  There is therefore no first- or
second-order cross-pair obstruction on this open leading stratum.

## 3. A dense rational simultaneous module

Take six sites modulo six.  Put

\[
                         c_{01}=-\frac{11}{3},
               \qquad c_{ij}=1\quad(ij\ne01).            \tag{13}
\]

Of the fifteen perfect matchings, three contain `01` and twelve do not,
so

\[
                         \operatorname{haf}C
                           =3(-11/3)+12=1.               \tag{14}
\]

Every two-hole cofactor is nonzero:

\[
 h_{ij}=\begin{cases}
 3,&\{i,j\}\cap\{0,1\}\ne\varnothing,\\
 -5/3,&\{i,j\}\cap\{0,1\}=\varnothing.
 \end{cases}                                             \tag{15}
\]

For color one use offsets `(p_1,q_1)=(1,2)`, and for color two use
`(p_2,q_2)=(1,3)`.  Define, with indices modulo six,

\[
 b^r_{i,i+p_r}=h_{i,i+q_r},\qquad
 b^r_{i,i+q_r}=-h_{i,i+p_r},                             \tag{16}
\]

and put every other `b` entry equal to zero.  Each row of (16) visibly
satisfies (9), and both color jets are nonzero.  Define `a` by solving
(10):

\[
 a_{ik}^{rs}=-{1\over h_{ik}}
 \sum_{\substack{j,\ell\notin\{i,k\}\\j\ne\ell}}
       b^r_{ij}b^s_{k\ell}h_{ikj\ell}.                  \tag{17}
\]

Exact enumeration gives

\[
                 \operatorname{haf}(a^{11})=-\frac{190}{3},
       \qquad   \operatorname{haf}(a^{22})= \frac{250}{3}.            \tag{18}
\]

Hence both missing pure words occur nontrivially in terminal degree six.
Choose nonzero complex numbers

\[
                  \lambda_1^6=-\frac3{190},
             \qquad\lambda_2^6= \frac3{250}.             \tag{19}
\]

The homogeneous replacement

\[
 b^r\mapsto\lambda_rb^r,qquad
 a^{rs}\mapsto\lambda_r\lambda_sa^{rs}                 \tag{20}
\]

preserves (9)--(10) and normalizes both values in (18) to one.

This is not an equality source.  Before the harmless scaling (20), the
degree-three coloring

\[
                              (0,0,0,2,1,1)              \tag{21}
\]

has coefficient `-10`.  Thus the third osculating identity detects the
module exactly where the generic classification first predicts genuine
compatibility.

## 4. Consequence for the proposed degeneration

The nonzero leading output avoids the base-locus phenomenon in
`base-locus-ghz-first-jet.md`, but it does not produce rigidity: the dense
point (13) is cofactor-open and still has the full tangent freedom (12).
Nor does Fourier root comparison help, because (6) is an exact torus
regrading rather than a lift of a discrete symmetry between fiber
components.  Finally, the exact annihilator used on the two-edge star face
depends on a shared cofactor pencil absent at a general scalar leading
point.

Accordingly, the statement

> a finite pure leading source cannot support simultaneous first nonzero
> directions toward the other two pure colors

is false through second order, even on the dense cofactor-open stratum and
with both terminal pure coefficients already nonzero and normalizable.
Any positive theorem must use the third and higher genuinely ternary
equations.  Requiring every intermediate torus layer to vanish through the
last pure output jet is, by (6), exactly the original mixed-coefficient
problem rather than a smaller degeneration theorem.

The dependency-free audit is
`computations/verify_color_torus_pure_limit_two_jet.py`.
