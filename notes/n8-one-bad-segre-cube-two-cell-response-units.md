# The four surviving Segre two-cell top packets fail both diagonal responses

## The exact response calculation

The critical-pair audit `af4c340` left four proper unary-top ideals.  Their
supports have the uniform source-labelled form

\[
 H+\sum d_e(00)_e+\sum a_e(11)_e+\sum b_e(22)_e
       +u(10)_{0k}+v(20)_{0k},\qquad k=2,3,4,5.       \tag{1}
\]

For each of the four cases, adjoin arbitrary endpoint-star forms

\[
 p_1,s_1,p_2,s_2\in\bigoplus_{i=0}^5\mathbb C e_i
\]

and construct the four literal response tensors

\[
 p_1s_1q^{[2]}=X_1,\quad p_1s_2q^{[2]}=0,\quad
 p_2s_1q^{[2]}=0,\quad p_2s_2q^{[2]}=X_2.            \tag{2}
\]

Exact reduced standard bases of the four top ideals contain every diagonal
carrier variable

\[
                       a_e, b_e\qquad(e\in E(K_6)). \tag{3}
\]

This immediately conflicts with either diagonal row in (2).  For example,
the pure coefficient of the first row is

\[
 D_{11}=\sum_{r\ne s}p_{1,r}s_{1,s}
       \sum_{M\in\operatorname {PM}([6]\setminus\{r,s\})}
       \prod_{e\in M}a_e.                            \tag{4}
\]

It has 90 literal ordered-hole/matching monomials.  Equation (3) puts
(D_{11}) in the top ideal, while the target response row is
(D_{11}-1=0).  Hence

\[
                         1=D_{11}-(D_{11}-1)          \tag{5}
\]

is in the combined top/response ideal.  The identical argument with the
fifteen (b_e) gives a second, independent unit certificate from the
(22) response.

## Literal source lifts

[`verify_n8_one_bad_segre_cube_two_cell_response_units.py`](../computations/verify_n8_one_bad_segre_cube_two_cell_response_units.py)
does not merely reduce (4).  It asks Singular over \(\mathbb Q\) for exact
representations of (D_{11}) and (D_{22}) by the original labelled top
coefficient rows, verifies those representations by multiplication, and
then verifies (5).  The active top-row counts are

| packet | (11) lift | (22) lift |
|---|---:|---:|
| `02:10+02:20` | 26 | 22 |
| `03:10+03:20` | 28 | 38 |
| `04:10+04:20` | 28 | 25 |
| `05:10+05:20` | 27 | 28 |

All four full response maps are built before the unit is checked.  Depending
on (k), the `11`/`22` maps have 302 or 304 nonzero word rows and 1,459
terms; each crossed map has 408 nonzero rows and 1,458 terms.  The crossed
rows are not needed in (5), because either diagonal row already contradicts
the top ideal.

## Consequence and scope

There is no response-compatible point, rational or complex, on any of the
four proper two-cell top packets from `af4c340`.  Thus the complete pinned
one-cell source-certificate critical-pair frontier closes after the genuine
one-bad responses are restored.

This is local to the fixed Segre--\(K_4\) chart (1).  It does not prove that
every one-bad source normalizes to that chart, and it does not examine a
third missing decorated cell.  Any remaining Segre escape must therefore
transgress at least two of the already-audited one-cell certificates in a
way not represented by these four minimal top packets, or deform the pinned
fourteen-cell initial form itself.
