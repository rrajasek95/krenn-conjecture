# An arbitrary internal \(A_{23}\) block still cannot activate a fourth cut

## 1. Result and exact scope

Retain the eight endpoint-ordered internal aggregate cells

\[
\begin{array}{c|c@{\qquad}c|c@{\qquad}c|c}
01&E_{00}&45&E_{00}&02&E_{11}\\
14&E_{11}&04&E_{22}&13&E_{22}\\
25&E_{00}&35&E_{10},
\end{array}
\]

and now allow

\[
                         A_{23}=X\in\operatorname{Mat}_{3\times3}(\mathbb C)
                                                               \tag{1}
\]

to be completely arbitrary.  Allow all \(108\) entries of the two
boundary stars \(i6,i7\), \(0\leq i<6\), and all nine entries of
\(A_{67}\) to be arbitrary complex numbers.

No such system satisfies the complete quotient identities on cuts
\(2,3,4\) together with cut \(0\), \(1\), or \(5\), while retaining the
three unit diagonal target fibres.

Together with the independently audited five-cell theorem, this treats
every \(3\times3\) block \(A_{23}\).  It remains a fixed-interior local
theorem: the other eight internal cells are not varied, no second internal
block is perturbed, and this is not a global Krenn obstruction.

The exact checker is
[verify_three_cut_internal_23_arbitrary_block_fourth_cut_obstruction.py](../computations/verify_three_cut_internal_23_arbitrary_block_fourth_cut_obstruction.py).
The full-support and cross-ratio helpers are
[explore_three_cut_internal_23_full_supports.py](../computations/explore_three_cut_internal_23_full_supports.py)
and
[test_three_cut_internal_23_x12_crossratio_symbolic.py](../computations/test_three_cut_internal_23_x12_crossratio_symbolic.py).
The exploratory projected-diagonal worker is
[test_three_cut_internal_23_full_diagonal_projection.py](../computations/test_three_cut_internal_23_full_diagonal_projection.py);
the theorem checker does not rely on its earlier bounded experiments.

## 2. Torus action and the one surviving invariant

The fixed-cell stabilizing colour torus acts on \(X=(x_{ab})\) by

\[
\begin{array}{c|ccc}
&b=0&b=1&b=2\\ \hline
a=0&r_0c_0&r_0^2&r_0c_2\\
a=1&r_1c_0&r_1r_0&r_1c_2\\
a=2&r_2c_0&r_2r_0&r_2c_2.
\end{array}                                               \tag{2}
\]

As before, the action extends to sites \(6,7\) so that each diagonal
target coefficient stays exactly one.  Boundary blocks remain arbitrary
because every change is invertible.

Order the four cells outside the earlier five-cell locus as

\[
                       x_{10},\quad x_{12},\quad x_{20},\quad x_{22}.
                                                               \tag{3}
\]

Every support meeting this set has a unique first nonzero cell in (3).
The \(480\) such support masks split as

\[
                         256+128+64+32.                    \tag{4}
\]

The retained nonzero coefficients in the \(x_{10}\), \(x_{20}\), and
\(x_{22}\) strata have independent exponent rows and can all be
normalized to one on each fixed support.

In the \(x_{12}\) stratum the only dependent retained support is the full
rectangle

\[
                 \{x_{11},x_{12},x_{21},x_{22}\}.          \tag{5}
\]

Its exponent relation is

\[
              \operatorname{wt}(x_{12})+\operatorname{wt}(x_{21})
             =\operatorname{wt}(x_{11})+\operatorname{wt}(x_{22}), \tag{6}
\]

so the sole invariant is

\[
                    \lambda={x_{12}x_{21}\over x_{11}x_{22}}. \tag{7}
\]

When all four entries are nonzero, normalize

\[
                   x_{12}=x_{11}=x_{22}=1,\qquad x_{21}=\lambda.
                                                               \tag{8}
\]

Every other retained support is a single complex torus orbit represented
by zero/one coefficients.  No coefficient outside the retained chart is
normalized; those coefficients disappear under the coordinate quotients
below and remain genuinely arbitrary.

## 3. Nine disjoint variable-coordinate blocks

Only deleted-pair cofactors \(01,05,15,45\) can depend on \(A_{23}\).
For each of the nine cells \(e=(a,b)\), insert every boundary endpoint
colour into the variable part of those cofactors and let \(R_e\) be the
set of reached six-word coordinates.  Exact enumeration gives

\[
 |R_e|=35,\qquad R_e\cap R_f=\varnothing\ (e\ne f),\qquad
 \left|\bigcup_eR_e\right|=315.                           \tag{9}
\]

Moreover,

\[
 [0^6]\in R_{00},\qquad [1^6]\in R_{11},\qquad
 [2^6]\in R_{22},                                        \tag{10}
\]

and no pure target word lies in any other \(R_e\).  Thus retaining an
outside block alone erases every useful target; at least two diagonal
blocks must be retained as well.

The proof uses colours \(1,2\), hence always retains \(R_{11}\) and
\(R_{22}\).  Several strata also retain a zero-coefficient outside block.
That does not add a variable term; it keeps fixed cofactor equations which
would otherwise be discarded.

## 4. Projected cylinders give a rigorous safe normal

Let \(\pi\) kill selected coordinate blocks \(R_e\).  For a cut \(z\),
write \(C_z(X)\) for its actual six-site insertion cylinder and set

\[
 \overline N_z(X)=
 \pi C_2(X)\cap\pi C_3(X)\cap\pi C_4(X)\cap\pi C_z(X).
                                                               \tag{11}
\]

For the actual common normal \(N_z(X)=C_2\cap C_3\cap C_4\cap C_z\),

\[
                         \pi N_z(X)\subseteq\overline N_z(X). \tag{12}
\]

This containment is the only inference needed.  The proof never assumes
that projection commutes with intersection.

If a cell block is killed, its contribution to every projected boundary
fibre and every projected cylinder column vanishes term by term.  Hence
the spaces in (11) are independent of all killed coefficients.  The
checker verifies this both for the boundary term lists and for all six
projected cylinder spans.  Linearity then covers arbitrary complex
coefficients, not merely zero/one samples.

The four hierarchy charts are

\[
\begin{array}{c|c|c|c|c}
\text{stratum}&\text{forced earlier zeros}&
\text{retained blocks}&\text{finite strata}&
\dim\overline N_{0,1,5}\\ \hline
x_{10}\ne0&-&10,11,21,22&8&2\\
x_{10}=0,\ x_{12}\ne0&10&12,11,21,22&7+\lambda&1\\
x_{10}=x_{12}=0,\ x_{20}\ne0&10,12&10,20,11,21,22&8&2\\
x_{10}=x_{12}=x_{20}=0,\ x_{22}\ne0&
10,12,20&10,12,20,11,21,22&4&1.
\end{array}                                               \tag{13}
\]

Here a retained forced-zero block contributes only its fixed equations.
For every finite row, exact rational reconstruction gives the same
projected normal for \(z=0,1,5\).  The direct term \(\pi H_S(X)\) belongs
to that normal, so every entry of \(A_{67}\) remains absorbed.

## 5. The cross-ratio cylinder is locked to a line

The invariant case (8) needs more than a pointwise calculation.  First
span each projected cylinder at \(\lambda=0\) and \(\lambda=1\), then
intersect the four expanded cylinders.  Since every cylinder column is
affine in \(\lambda\), this gives a parameter-independent upper bound for
every complex \(\lambda\).  For each \(z=0,1,5\), that upper bound is the
same plane

\[
\begin{aligned}
 P=\langle e,v\rangle,\qquad
 e={}&[002100],\\
 v={}&[121200]+[001100]+[001200]+[002200]+[111110].
\end{aligned}                                             \tag{14}
\]

The exact functional

\[
             \ell_\lambda=[002100]^*-\lambda[001100]^*    \tag{15}
\]

annihilates every projected column of the final cylinder \(C_z(\lambda)\)
for \(z=0,1,5\).  The checker verifies (15) coefficientwise: for every
raw column, the constant, linear, and quadratic coefficients in
\(\ell_\lambda(C_z(\lambda))\) all vanish.

If \(w=\alpha e+\beta v\) lies in a projected four-cylinder
intersection, then (15) gives

\[
                         \alpha-\lambda\beta=0.            \tag{16}
\]

Therefore

\[
                  \pi N_z(\lambda)\subseteq
                  \langle v+\lambda e\rangle,             \tag{17}
\]

which is precisely the projected direct-tensor line.  This proves the
normal used by the symbolic ideal uniformly, including all exceptional
complex values of \(\lambda\).

## 6. Literal shared-star equations

For boundary colours \(a,b\), write

\[
 p^a_{i,c}=A_{i6}[c,a],\qquad
 q^b_{i,c}=A_{i7}[c,b],\qquad
 r_{ab}=A_{67}[a,b].
\]

Endpoint-ordered matching expansion gives

\[
\begin{aligned}
 H_{ab}={}&r_{ab}H_S(X)+\beta_X(p^a,q^b),\\
 \beta_X(p,q)={}&
 \sum_{i<j}\sum_{c,d}
 \left(p_{i,c}q_{j,d}+p_{j,d}q_{i,c}\right)
 e_c^{(i)}e_d^{(j)}\otimes H_{S\setminus\{i,j\}}(X).
\end{aligned}                                             \tag{18}
\]

Both endpoint orientations occur, and the same star variables are reused
in diagonal and ordered off-diagonal fibres.  Projecting a full solution
and allowing the larger safe normal (11) gives necessary equations

\[
 \pi\beta_X(p^a,q^b)-\delta_{ab}\pi[a^6]\in\overline N_z(X).
                                                               \tag{19}
\]

The proof retains \(a,b\in\{1,2\}\): two coefficient-one diagonal fibres
and both ordered off-diagonal zero fibres.  These use \(72\) shared star
variables.  Any solution of the full nine-fibre, \(108\)-variable system
must restrict to this four-fibre packet, so its inconsistency is
sufficient.

An exact numerical reconstruction with distinct rational values in all
nine cells of \(X\), all \(108\) star entries, and all nine direct entries
checks (18) against literal eight-site perfect-matching enumeration on
every boundary slice.

## 7. Exact characteristic-zero unit ideals

Write

\[
 d=2\,{\bf1}_{x_{11}\ne0}+4\,{\bf1}_{x_{22}\ne0},
 \qquad b={\bf1}_{x_{21}\ne0}.                            \tag{20}
\]

For every finite torus stratum, Singular computes over \(\mathbb Q\):

\[
\begin{array}{c|c|c}
\text{family}&(d,b)&\text{generator counts}\\ \hline
x_{10}&
(0,0),(0,1),(2,0),(2,1),(4,0),(4,1),(6,0),(6,1)&
328,432,412,516,440,544,524,628\\
x_{12}&
(0,0),(0,1),(2,0),(2,1),(4,0),(4,1),(6,0)&
332,436,416,520,444,548,528\\
x_{20}&
(0,0),(0,1),(2,0),(2,1),(4,0),(4,1),(6,0),(6,1)&
356,460,440,544,468,572,552,656\\
x_{22}&
(4,0),(4,1),(6,0),(6,1)&
384,488,468,572.
\end{array}                                               \tag{21}
\]

Every one of these \(27\) ideals has reduced standard basis

\[
                              [1].                         \tag{22}
\]

For the omitted \(x_{12}\) case \((d,b)=(6,1)\), \(\lambda\) is entered
as an ordinary polynomial variable, not as a generic coefficient-field
parameter.  Modulo the exact line (17), the resulting
\(628\)-generator ideal in

\[
             \mathbb Q[\lambda,p^1,p^2,q^1,q^2]           \tag{23}
\]

also has reduced standard basis \([1]\).  Thus there is no exceptional
complex cross-ratio value.

The certificates are characteristic-zero unit calculations.  Scalar
extension from \(\mathbb Q\) to \(\mathbb C\) preserves the unit ideal.
Because every generator is a necessary projected consequence of the
actual shared-star system, (22)--(23) exclude all \(480\) outside support
masks with arbitrary complex coefficients.

## 8. Reproduction log

From the repository root, run

```text
uv run python computations/verify_three_cut_internal_23_arbitrary_block_fourth_cut_obstruction.py
```

The clean locked-environment rerun on 2026-07-27 ended with

```text
arbitrary A23 outside-locus fourth-cut obstruction: PASS
480 support masks partitioned 256+128+64+32: PASS
27 finite complex torus orbits plus Q[lambda] cross ratio: PASS
projected cut-0/1/5 normals and arbitrary killed coefficients: PASS
endpoint order, 108 shared-star entries, ordered fibres, A67: PASS
...
x12_crossratio_lambda: N=1, generators=628, 32.231s: PASS
parallel exact-Q wall time: 74.336s
```

The complete process took \(75.62\) seconds of wall time.  The \(27\)
finite Singular jobs and the one symbolic job run in parallel, so their
individual timings do not sum to this wall time.  Python byte-compilation
of the checker and all three helper scripts also passed.

## 9. Consequence

The independently audited five-cell theorem covers the remaining \(32\)
support masks, for which

\[
 A_{23}\in\langle E_{00},E_{01},E_{02},E_{11},E_{21}\rangle.
\]

Combining it with the present \(480\)-mask theorem yields:

> With the other eight internal cells fixed as displayed, an arbitrary
> complex \(3\times3\) block \(A_{23}\), two arbitrary boundary stars, and
> arbitrary \(A_{67}\) cannot activate a fourth cut \(0\), \(1\), or \(5\)
> in addition to cuts \(2,3,4\).

The next escape must therefore perturb a second internal block or replace
the fixed six-site interior.  Varying \(A_{23}\) alone is now exhausted
without a bounded-weight assumption and without leaving any torus
cross-ratio untreated.
