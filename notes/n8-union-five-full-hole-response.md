# The full row at the unique nonwitness site

## 1. Exact decomposition

Fix an invertible pair `p,q` in the eight-site problem and suppose that the
zero-cross witness union is a five-set `U`.  Write `k` for the remaining
outside site.  Work at a generic point of

\[
 g=\alpha^T A_{pq}\beta=0
\]

and put, at every outside site,

\[
 x_i=A_{pi}^T\alpha,\qquad y_i=A_{qi}^T\beta.
\]

Do **not** contract `k` only by its common annihilator.  For an arbitrary
covector `z` at `k`, set

\[
 d_i(z)=A_{ki}^Tz\quad(i\in U),\qquad
 s_p(z)=x_k^Tz,\qquad s_q(z)=y_k^Tz.                 \tag{1}
\]

For `i in U`, let `H_(U-i)` be the four-site matching tensor on
`U minus {i}` and define the two one-cross responses

\[
 X=\sum_{i\in U}x_i^{(i)}\otimes H_{U-i},\qquad
 Y=\sum_{i\in U}y_i^{(i)}\otimes H_{U-i}.             \tag{2}
\]

Finally, for an internal edge `ab subset U`, let `C=U minus {a,b}` and
write

\[
 \operatorname{Per}_C(x,y,d(z))
 =\sum_{\sigma:\{p,q,k\}\mathbin\simto C}
     x_{\sigma(p)}\otimes y_{\sigma(q)}
                         \otimes d_{\sigma(k)}(z),       \tag{3}
\]

with the factors restored to the site order of `C`.  Put

\[
 F(z)=\sum_{\{a,b\}\subset U} A_{ab}\otimes
                  \operatorname{Per}_{U-\{a,b\}}(x,y,d(z)). \tag{4}
\]

**Proposition 1 (arbitrary nonwitness row).**  On `g=0`, contraction of
the full matching tensor at `p,q,k` by `alpha,beta,z` is

\[
 \boxed{\quad s_p(z)Y+s_q(z)X+F(z).\quad}              \tag{5}
\]

Consequently, in a realization of the ternary diagonal,

\[
 \boxed{
 \sum_{r=0}^2\alpha_r\beta_rz_r e_r^{\otimes U}
       =s_p(z)Y+s_q(z)X+F(z)\qquad(z\text{ arbitrary}).} \tag{6}
\]

**Proof.**  Split a perfect matching by its number of edges crossing the
odd cut `{p,q,k}|U`.  It has either one or three crossing edges.  In the
one-cross sector, the internal edge on the three-set is `pk`, `qk`, or
`pq`.  The first two choices give `s_p(z)Y` and `s_q(z)X`; the last is
multiplied by `g` and vanishes.  In the three-cross sector, the two unused
vertices of `U` form the internal edge `ab`, while `p,q,k` are bijected to
its three-site complement.  This is exactly (3)--(4).  The target
contraction is the left side of (6). `QED`

## 2. The common-annihilator specialization and the missing compatibility

At the nonwitness site put

\[
 \gamma_k=x_k\mathbin\times y_k.
\]

Its three coordinates are nonzero in the incidence function field.
Since `s_p(gamma_k)=s_q(gamma_k)=0`, equation (6) becomes the familiar
five-hole identity

\[
 \sum_r\alpha_r\beta_r\gamma_{k,r}e_r^{\otimes U}
                         =F(\gamma_k).                  \tag{7}
\]

Formula (4) is the important strengthening of the arbitrary symmetric
two-slice relaxation.  If

\[
 R_{uv}=x_u y_v^T+y_u x_v^T,
\]

then (7) can also be written

\[
 F(\gamma_k)=\sum_{\{u,v\}\subset U}R_{uv}\otimes
 \left(\sum_{w\in U-\{u,v\}}
       d_w(\gamma_k)\otimes A_{U-\{u,v,w\}}\right).    \tag{8}

The two orders of the `p,q` partners share the same residual tensor, the
three possible `k` partners share the same internal matrices, and all five
vectors `d_w(z)` are columns of the same five edge maps applied to the
single row `z`.  Replacing the parenthesized tensors in (8) by arbitrary
three-tensors loses exactly this compatibility.

Equation (6) retains still more.  In the quotient by the fixed two-plane
`span{X,Y}`, all three coordinate rows satisfy

\[
 [F(e_r)]=\alpha_r\beta_r[e_r^{\otimes U}]\qquad(r=0,1,2). \tag{9}
\]

Thus a proof on the five-site witness boundary must either use the common
internal edge family in (4), or use the fact that the two discarded
responses in (9) are the actual one-cross cofactors (2).  A pointwise
argument based only on arbitrary residual tensors does not test the full
identity.

## 3. Relation to the exact thirteen-row boundary

The two-hole and hard-capacity reductions in
[`n8-witness-union-five-stages.md`](n8-witness-union-five-stages.md) leave
thirteen incidence orbits and thirty-six hard assignments.  In every one,
all five sites of `U` are hard for at least one color, so contracting any
one of them deletes a target color.  This is why (6), with the unique
nonwitness row arbitrary, is the first higher-hole identity which retains
the whole ternary target without making an invalid partial-diagonal slice
cover argument.

No exclusion of the thirteen rows is claimed here.  The exact unresolved
system is (6), together with the local witness and row-lock normal forms in
the cited note.

Subsequent work separates two sharp facts.  The exceptional `011166` row is
excluded only after adjoining its scalar two-hole cofactors
([`n8-011166-full-row-square-obstruction.md`](n8-011166-full-row-square-obstruction.md)).
On the other hand, the common-annihilator specialization (7) by itself does
have an exact rational mixed-basis solution with those same masks
([`five-hole-factorization-counterexample.md`](five-hole-factorization-counterexample.md)).
Thus the arbitrary-row or simultaneous-cofactor compatibility is essential.

## 4. An exact three-hole triangle response

There is one useful higher-hole consequence which does not use a covering
lemma for a partial diagonal.  Let three nontriple holes `1,2,3` be hard
for a color `r`, and suppose every other target color is killed by a
contracted hard site.  Over the incidence field, write

\[
 R_{ij}=x_i y_j^T+y_i x_j^T.
\]

The exact three-hole equation has the form

\[
 \lambda e_r^{\otimes3}
     =R_{12}\otimes v_3+R_{13}\otimes v_2
                         +R_{23}\otimes v_1,\qquad\lambda\ne0. \tag{10}
\]

Each `x_i,y_i` is independent.  Since `i` is hard for `r`, write

\[
 e_r=a_i x_i+b_i y_i.                                  \tag{11}
\]

**Lemma 2 (triangle-response normal form).**  Equation (10) implies that
every `v_i` lies in `span{x_i,y_i}`.  It also implies

\[
             \prod_i a_i=\prod_i b_i=0.                \tag{12}
\]

Thus one of the three holes is a `q`-side `r`-anchor and one is a distinct
`p`-side `r`-anchor.  After relabeling and rescaling the two anchor lines,
write

\[
 e_r=A_1x_1=B_2y_2=A_3x_3+B_3y_3.                     \tag{13}
\]

Then the three residual vectors are uniquely forced:

\[
\begin{aligned}
 v_1&={L_X\over2}x_1-{L_Y\over2}y_1,\\
 v_2&=-{L_X\over2}x_2+{L_Y\over2}y_2,\\
 v_3&={L_X\over2}x_3+{L_Y\over2}y_3,                  \tag{14}\\
 L_X&=\lambda A_1B_2A_3,\qquad
 L_Y=\lambda A_1B_2B_3.
\end{aligned}
\]

**Proof.**  Extend `x_i,y_i` to a basis at each hole.  The component of
(10) having the third basis vector at site `i` can only come from the
summand `R_jk tensor v_i`; the rank-two tensor `R_jk` is nonzero, so that
component of `v_i` vanishes.

Now use `X_i=x_i,Y_i=y_i` as the two local symbols.  The right side of
(10) has zero coefficients at `XXX` and `YYY`, proving (12).  Choose the
anchors as in (13).  The only target words are `XYX` and `XYY`, with
coefficients `L_X,L_Y`.  If `v_i=s_iX_i+t_iY_i`, direct comparison gives

\[
\begin{array}{lll}
 s_1+s_2=0,&s_1+s_3=L_X,&s_2+s_3=0,\\
 t_2+t_3=L_Y,&t_1+t_3=0,&t_1+t_2=0.
\end{array}
\]

The two coefficient matrices have determinant `2`, so (14) is their
unique solution. `QED`

The no-triple residual row `(0,1,3,5,6,6)` has three hard sets of size
three, and hence three overlapping copies of (14).  The remaining gap is
to impose that their nine displayed residual vectors are contractions of
one common family of internal matrices.  Treating them as independent
vectors discards the same shared-edge compatibility as replacing (4) by
arbitrary three-tensors.

## 5. The three triangle responses are jointly compatible

The common-origin condition just identified is real, but it still does not
exclude the balanced no-triple row.  Here is an exact rational local model.
It uses one common family of edge matrices for all fifteen two-hole rows
and all three triangle responses.

Delete the empty site from `(0,1,3,5,6,6)`, label the remaining sites
`0,1,2,3,4`, and call the nonwitness `k`.  At one point of the incidence
quadric choose the following star rows and common annihilators:

\[
\begin{array}{c|c|c|c}
i&x_i&y_i&n_i\\ \hline
0&e_0&e_1+e_2&(0,-1,1)\\
1&e_0&e_1&e_2\\
2&e_2&e_0&e_1\\
3&e_1&e_2&e_0\\
4&e_2&e_1&e_0\\
k&(1,1,1)&(1,2,3)&(1,-2,1).
\end{array}                                             \tag{15}
\]

The cross-product zero masks are exactly `1,3,5,6,6,0`.  This point comes
from honest fixed-pair blocks: take

\[
 \alpha=(1,1,1),\qquad \beta=(1,\tfrac12,1),\qquad
 A_{pq}=\operatorname {diag}(1,2,-2),                   \tag{16}
\]

and set `A_pi=e_0x_i^T`, `A_qi=e_0y_i^T`.  Then `A_pq` is invertible,
`alpha^T A_pq beta=0`, the selected star rows are (15), and the block
cross matrices have the declared masks.

For an outside edge define

\[
 L_{i\to j}=A_{ij}^Tn_i,\qquad
 a_{ij}=n_j^TL_{i\to j}.                               \tag{17}
\]

Choose the scalar graph to be the pure star centered at `k`:

\[
             a_{ik}=1\ (0\le i\le4),\qquad
             a_{ij}=0\ (0\le i<j\le4).                \tag{18}
\]

Every four-site hafnian of (18) is zero.  Choose dual vectors

\[
 (u_0,u_1,u_2,u_3,u_4,u_k)
       =(e_2,e_2,e_1,e_0,e_0,e_0),\qquad n_i^Tu_i=1.    \tag{19}
\]

On every `ik` set \(L_{i\to k}=u_k\) and \(L_{k\to i}=u_i\).  The nonzero directed
witness-edge rows are

\[
\begin{array}{c|c@{\qquad}c|c@{\qquad}c|c}
3\to0&\tfrac12e_0&3\to1&\tfrac12e_0&3\to2&-\tfrac12e_2\\
0\to1&\tfrac12e_1&0\to3&-\tfrac12e_2&0\to4&\tfrac12e_1\\
0\to2&\tfrac12e_2&1\to3&\tfrac12(e_2-e_1)&1\to4&\tfrac12(e_2-e_1).
\end{array}                                             \tag{20}
\]

All other directed witness rows are zero.  These declarations really do
come from common matrices, not separately selected half-edge data.  For
each `i<j`, the compatibility

\[
 n_j^TL_{i\to j}=n_i^TL_{j\to i}=a_{ij}
\]

holds, and the single formula

\[
 A_{ij}=u_iL_{i\to j}^T+L_{j\to i}u_j^T
                         -a_{ij}u_iu_j^T                \tag{21}
\]

realizes both endpoint contractions.

For a hard triple of holes and its contracted complement `C`, the actual
residual vector at a hole `h` is

\[
 v_h^C=\sum_{c\in C}L_{c\to h}\,a_{C\setminus\{c\}},   \tag{22}
\]

where the last factor is the scalar edge on the other two sites of `C`.
Equations (18)--(20) give

\[
\begin{array}{c|c|ccc}
r&\text{holes}&v_{h_1}&v_{h_2}&v_{h_3}\\ \hline
0&(0,1,2)&\tfrac12e_0&\tfrac12e_0&-\tfrac12e_2\\
1&(1,3,4)&\tfrac12e_1&-\tfrac12e_2&\tfrac12e_1\\
2&(2,3,4)&\tfrac12e_2&-\tfrac12e_1&\tfrac12e_2.
\end{array}                                             \tag{23}
\]

Direct substitution into (10) gives respectively
\(e_0^{\otimes3}\), \(e_1^{\otimes3}\), and \(e_2^{\otimes3}\).  The target coefficients
are consistent with the single choice (16): contraction at the three
complements multiplies `(alpha_r beta_r)` by respectively `1,2,1`, giving
unit coefficients in all three rows.

Thus no eliminant can follow from only the fifteen scalar four-hafnian
equations and the three shared-edge triangle normal forms.  The model is
not a five-hole realization: its uncontracted six-site row has, for
example, coefficient `1` at the off-diagonal word `(0,0,1,0,1,0)`.
Eliminating this row must use the remaining coefficients of (6), including
the common arbitrary-row maps `d_i(z)` and the fixed one-cross responses
`X,Y`.

## 6. Exact audit

Run

```text
.venv/bin/python computations/verify_n8_union_five_full_hole_response.py
```

The checker uses rational matrices, enumerates all 105 perfect matchings,
and verifies (5) coefficient by coefficient for a basis of arbitrary rows
`z`.  It independently regroups the three-cross sector in both forms
(4) and (8), and verifies that `z=gamma_k` kills precisely the two
one-cross responses.  It also verifies the six coefficient equations and
the unique solution (14) symbolically.

Run additionally

```text
.venv/bin/python computations/verify_n8_union_five_triangle_compatibility.py
```

This second checker constructs (15)--(21), verifies the exact block masks,
enumerates all 105 perfect matchings of the common eight-site edge family,
checks all fifteen zero two-hole contractions and the three pure triangle
responses, and audits the displayed off-diagonal failure of the full row.
