# Schur reduction of the tangent-plus-point GHZ boundary

## Outcome

Let `n >= 6` be even and let

\[
 W_n=\sum_{v=1}^n e_0^{\otimes(v-1)}\otimes e_1
                    \otimes e_0^{\otimes(n-v)},
 \qquad T_n=W_n+e_2^{\otimes n}.                           \tag{1}
\]

Over every infinite field of characteristic two, an arbitrary-matrix
matching realization of `T_n` implies one of `T_6`.  Separately, an exact
exhaustive SAT audit of all four relative matching orbits excludes `T_6`
over `F_2`.

These two results do **not** yet combine into an algebraic-closure theorem:
the six-site SAT calculation assigns Boolean values to the entries, whereas
the Schur reduction may pass to an arbitrary characteristic-two extension.
The zero/nonzero support relaxation is satisfiable (indeed full support is
a model), so no singleton-fiber upgrade is available.  A polynomial-ideal
certificate or a field-independent six-site argument is still required.

The reduction nevertheless isolates a genuine full-local-rank boundary
family of the ternary GHZ orbit, not merely a diagonal rank-one or rank-two
degeneration.  Indeed
`T_n` is the projective limit

\[
 t^{-1}\left((e_0+t e_1)^{\otimes n}-e_0^{\otimes n}
                         +t e_2^{\otimes n}\right)
       \longrightarrow W_n+e_2^{\otimes n}.                \tag{2}
\]

For `t != 0`, the tensor in parentheses is in the local `GL_3` orbit of
`Delta_(n,3)`: use columns `e_0+t e_1,e_0,e_2` at every site, insert the
minus sign in the second column at one site, and multiply the third column
by `t` at one site.  Thus arbitrary local normalization cannot be analyzed
only through diagonal rank-at-most-two special outputs.

## 1. Transverse Pfaffian form

Suppose, toward a contradiction, that arbitrary endpoint-ordered matrices
`A_uv in K^(3 by 3)` satisfy `H_n(A)=T_n`, where `K` is infinite of
characteristic two.  For local variables `x_v=(x_(v,0),x_(v,1),x_(v,2))`,
form the alternating scalar matrix

\[
 B(x)_{uv}=x_u^T A_{uv}x_v\quad(u<v),\qquad
 B(x)_{vu}=B(x)_{uv}.                                     \tag{3}
\]

The Pfaffian signs disappear in characteristic two, so coefficient
comparison gives the polynomial identity

\[
 \operatorname {Pf}B(x)=
 \sum_v x_{v,1}\prod_{w\ne v}x_{w,0}+\prod_vx_{v,2}.       \tag{4}
\]

The right side is nonzero.  Hence `B(x)` is nonsingular over the rational
function field.  Repeated Pfaffian expansion gives a vertex set `P` of
cardinality `n-6` for which the principal Pfaffian

\[
                         \operatorname {Pf}B(x)[P]\ne0.    \tag{5}
\]

This is the same principal-Pfaffian flag argument used in
`notes/char2-schur-reduction.md`.

## 2. All-nonzero specialization and Schur complement

The polynomial in (5) is nonzero.  The coordinate torus is Zariski dense
over an infinite field, so choose

\[
                 \xi_p\in(K^*)^3\quad(p\in P)             \tag{6}
\]

with `d=Pf B(xi)[P] != 0`.  This remains valid after replacing a finite
residue field by its infinite algebraic closure.  Nonexistence over the
algebraic closure implies nonexistence over the original field, so that
extension loses nothing.

Put `R=[n]\P`, `|R|=6`, and block the specialized alternating matrix as

\[
 B=\begin{pmatrix}M&E\\E^T&D\end{pmatrix},\qquad
 N=D+E^TM^{-1}E.                                           \tag{7}
\]

Since `M^(-1)` is alternating, every diagonal entry of `N` is zero, and
every off-diagonal entry of `N` is still bilinear in the local variables at
its two boundary vertices.  Pfaffian Schur complementation gives

\[
                         \operatorname {Pf}B=d\operatorname {Pf}N. \tag{8}
\]

Define the three specialized scalars

\[
 \alpha=\prod_{p\in P}\xi_{p,0},\qquad
 \beta=\sum_{p\in P}\xi_{p,1}
                    \prod_{q\in P\setminus\{p\}}\xi_{q,0},\qquad
 \gamma=\prod_{p\in P}\xi_{p,2}.                         \tag{9}
\]

The all-nonzero choice makes `alpha,gamma != 0`; `beta` may vanish.  On
specializing (4) and using (8), one obtains exactly

\[
 \operatorname {Pf}N=
 c\sum_{r\in R}x_{r,1}\prod_{s\in R\setminus\{r\}}x_{s,0}
       +b\prod_{r\in R}x_{r,0}+g\prod_{r\in R}x_{r,2},    \tag{10}
\]

where `c=alpha/d`, `b=beta/d`, and `g=gamma/d`.  In particular `c,g` are
nonzero.

## 3. Exact local shear normalization

Equation (10) is locally equivalent to `T_6`.  At one boundary vertex
`r_0`, make the invertible shear

\[
                         e_1\longmapsto e_1+(b/c)e_0,      \tag{11}
\]

while fixing `e_0,e_2`.  Only the `r_0` summand of `W_6` changes, adding
`(b/c)e_0^(tensor 6)`.  Because the characteristic is two, its contribution
`b e_0^(tensor 6)` cancels the displayed vacuum term in (10).

Next scale `e_1` by `c^(-1)` at every boundary vertex.  Each `W_6` summand
contains exactly one `e_1`, so this changes its common coefficient from
`c` to one.  Finally scale `e_2` by `g^(-1)` at one vertex, changing the
coefficient of `e_2^(tensor 6)` to one.  All transformations are invertible
and can be absorbed into the six-site edge matrices.  Coefficient
comparison now gives an arbitrary-matrix realization of `T_6`.

This proves the uniform reduction over an infinite characteristic-two
field.  If the original residue field is finite, one may extend it to its
infinite algebraic closure, but then the required six-site obstruction must
also hold over that algebraic closure; the present `F_2` SAT audit does not
supply it.  Notice also that the reduction is purely
characteristic two: for an unsigned matching sum modulo four, Pfaffian
signs reappear as uncontrolled first-order terms, so (8) is not a mod-four
Schur bridge.

## 4. Exhaustive six-site audit over `F_2`

The computation directly proves nonexistence over `F_2`.  It fixes a
nonzero matching term in the W-coloring
`(1,0,0,0,0,0)` to

\[
                    01|23|45                              \tag{12}
\]

with cells `10,00,00`.  This is lossless by vertex symmetry.  A nonzero
term in the all-two coefficient supplies another perfect matching.  The
stabilizer of (12) has order eight and has four orbits on the fifteen
perfect matchings:

\[
\begin{array}{c|c|c}
0&01|23|45&1\\
1&01|24|35&2\\
2&02|13|45&4\\
3&02|14|35&8.
\end{array}                                                \tag{13}
\]

The last column is the orbit size; the sizes sum to fifteen.  For each
representative, `computations/search_char2_general.py` retains all 135
asymmetric cells and all `3^6=729` coefficient equations.  All four CNFs
are UNSAT.  The observed Kissat runtimes were respectively 73.74, 96.84,
86.72, and 83.58 seconds.

Run the complete replayable audit with

~~~text
uv run python computations/verify_w_plus_product_char2.py
~~~

The wrapper regenerates and solves all four `F_2` CNFs in parallel and
accepts only four clean `sat=False` results.  Running the same generator
with `--support-only` is SAT, with the full-support pattern as an immediate
model.  Therefore this audit must not be cited over extensions of `F_2`.

## 5. Scope

The family (1) is the generic double-point-plus-distinct-point boundary of
three GHZ summands.  Even after upgrading its six-site obstruction from
`F_2` to the algebraic closure, the argument would not handle:

* diagonal rank-one or rank-two special outputs;
* a projective source limit in the base scheme `H=0`;
* triple-collision (second-osculating) border-rank-three limits; or
* higher two-adic jets above any of those special sources.

Those are the remaining arithmetic boundary strata.  In particular this
lemma must not be presented as a characteristic-zero specialization bridge.
