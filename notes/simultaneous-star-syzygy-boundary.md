# Simultaneous fixed-star syzygies: exact classification and the power boundary

## Outcome

Fixing the internal quadratic does **not** make the three star rows interact
linearly.  The full star map is the tensor product of the identity at the
fixed vertex with one common cofactor map.  Its kernel and its
least-Frobenius-norm inverse therefore split row by row.  In particular,
there is no support-reducing syzygy which uses one colour row to cancel a
different colour row.

This observation gives an exact criterion for the hoped-for cubic
reduction: it is possible precisely when the common power has, for every
colour, a pure constant cofactor.  Two-centre failures have the usual
Koszul bridge normal form, and the bridge can be both irredundant and the
unique least-norm preimage.

Two exact countermodels delimit what this does and does not prove.

1. A seven-site, three-colour common-near-top tensor has an injective
   cofactor map, all three constant tensors in its image, and unique
   two-centre preimages.  Its star has six cells and no three-cell
   replacement.  Thus simultaneous one-slice equations, a common cofactor
   tensor, local irredundancy, and least-norm inversion do not imply cubic
   form.  This module is not asserted to be a power of a quadratic.
2. A genuine rational six-vertex binary matching source has exact binary
   GHZ output and actual common power `q^2`.  Every star is a least-norm
   solution for its fixed internal quadratic, but four stars spread one
   colour over two neighbours.  Hence least-star norm does not select the
   cell-minimal form even in the exact shared-power setting.

Consequently the entry-minimal ternary route has one sharply identified
remaining burden: it must use a new nonlinear identity special to
`f=q^(m-1)` to force three pure cofactors.  Neither the simultaneous linear
star equations nor their Moore--Penrose normal equations can do that.

## 1. The common-power star map

Let `B` have even cardinality `n=2m`, fix `v in B`, and put

\[
 J=B\setminus\{v\},\qquad
 \mathcal Z_J=\bigotimes_{j\in J}(\mathbb C\oplus V_j),
 \qquad V_jV_j=0.                                         \tag{1}
\]

Write the matching quadratic as

\[
 Q=q+\sum_{r=0}^2x_{v,r}L_r,                              \tag{2}
\]

where `q` contains the edges internal to `J`, and

\[
 L_r=\sum_{j\in J}\ell_{j,r},\qquad \ell_{j,r}\in V_j    \tag{3}
\]

is the colour-`r` row of the star at `v`.  Since two terms using `v`
multiply to zero,

\[
 Q^m=m\sum_rx_{v,r}L_rq^{m-1}.                            \tag{4}
\]

Put

\[
 f={q^{m-1}\over(m-1)!},\qquad
 C_j=H_{J\setminus\{j\}}(q).                              \tag{5}
\]

The multidegree-`J\setminus{j}` component of `f` is exactly `C_j`.
Restoring the missing slot defines one common linear map

\[
 F_q:\bigoplus_{j\in J}V_j\longrightarrow
 W:=\bigotimes_{j\in J}V_j,
 \qquad
 F_q((z_j)_j)=\sum_jz_j^{(j)}\otimes C_j.                 \tag{6}
\]

If `g_r=e_r^(tensor J)`, the three fixed-star equations are

\[
                         F_q((\ell_{j,r})_j)=g_r,
 \qquad r=0,1,2.                                          \tag{7}
\]

Notice that (7) is not merely a necessary local test.  Equations (4)--(7)
give `Q^m=m! Delta_(B,3)`.  Thus constructing a quadratic `q` and three
rows satisfying (7) at any even order at least six would already construct
a full counterexample to Krenn's conjecture.  Conversely every full source
gives (7).  The adjective "local" must not hide this equivalence.

## 2. Row separation is exact

Allow an arbitrary perturbation of every scalar cell incident with `v`.
After restoring the `v` slot, its exact-linear star map is

\[
 \mathcal F_v:
 V_v\otimes\left(\bigoplus_{j\in J}V_j\right)
 \longrightarrow V_v\otimes W,
 \qquad \mathcal F_v=I_{V_v}\otimes F_q.                  \tag{8}
\]

This immediately gives the complete simultaneous linear classification.

**Proposition 2.1 (row-separation theorem).**

\[
 \ker\mathcal F_v=V_v\otimes\ker F_q.                     \tag{9}
\]

For the standard Hermitian structures, the least-Frobenius-norm star with
fixed `q` and output `Delta_(B,3)` is

\[
 \sum_{r=0}^2e_r^{(v)}\otimes F_q^+g_r,                   \tag{10}
\]

where `F_q^+` is the Moore--Penrose inverse.  Thus both exact star
perturbations and least-norm inversion split into three independent row
problems.

**Proof.**  Tensoring the exact sequence
`0 -> ker F_q -> direct-sum V_j -> W` by the vector space `V_v` remains
exact, proving (9).  The three spaces `e_r tensor W` are mutually
orthogonal and (8) acts by the same map `F_q` on each.  Minimizing the sum
of the three squared row norms therefore gives (10). `QED`

At an entry-minimal full source, the derivative atoms used in each row are
linearly independent.  Proposition 2.1 shows why the word "simultaneous"
does not strengthen this through an exact-linear variation: a dependence
between different rows is impossible because their `v`-slot factors are
independent.  Any further coupling has to change `q`, or use a nonlinear
identity satisfied by its power.

## 3. Exact criterion for a cubic replacement

The desired one-centre rows can be characterized without approximation.

**Proposition 3.1 (pure-cofactor criterion).**  The equation

\[
                         F_q(z)=g_r                       \tag{11}
\]

has a preimage supported at one centre `j` if and only if, for a nonzero
scalar `gamma`,

\[
 C_j=\gamma e_r^{\otimes(J\setminus\{j\})}.               \tag{12}
\]

The preimage is then `z_j=gamma^(-1)e_r`.  Consequently the entire star can
be replaced, with `q` fixed, by exactly three rank-one same-colour cells if
and only if (12) holds for every `r=0,1,2`.  The three centres are
automatically distinct.

**Proof.**  A one-centre equation is
`z_j tensor C_j=g_r`.  Uniqueness of the factors of a nonzero decomposable
tensor gives (12) and the stated value of `z_j`; the converse is immediate.
A nonzero tensor `C_j` cannot be proportional to two distinct constant
colour tensors, so one centre cannot serve two colours. `QED`

Thus slice covering does not yet give the needed conclusion.  It produces
an incident matrix whose *opposite endpoint image* is `C e_r`; Proposition
3.1 additionally requires its entire complementary hafnian to be the pure
constant tensor of colour `r`.

The smallest obstruction is completely classifiable.

**Proposition 3.2 (one-colour two-centre Koszul bridge).**  Let `j != k`,
let `R=J\setminus{j,k}`, and suppose `x in V_j` and `y in V_k` are
nonzero.  Then

\[
 x^{(j)}\otimes C_j+y^{(k)}\otimes C_k=g_r               \tag{13}
\]

forces at least one of `x,y` to be proportional to `e_r`.  After possibly
interchanging `j,k`, there are `alpha != 0` and a tensor `Z` on `R` such
that

\[
 x=\alpha e_r,\qquad
 C_k=e_r^{(j)}\otimes Z,\qquad
 \alpha C_j=e_r^{(k)}\otimes e_r^{\otimes R}
                         -y^{(k)}\otimes Z.                \tag{14}
\]

For a zero right side, every nonzero two-centre syzygy similarly has the
pure Koszul form

\[
 C_j=y^{(k)}\otimes Z,\qquad C_k=-x^{(j)}\otimes Z        \tag{15}
\]

after rescaling the displayed factors.

**Proof.**  Apply the quotient maps
`V_j -> V_j/Cx` and `V_k -> V_k/Cy` to (13).  Both left summands vanish.
The image of the right side can vanish only if `e_r` belongs to at least one
of the two killed lines.  Suppose `x=alpha e_r`.  Quotienting only at `j`
then forces `C_k` to have the factor `e_r` at `j`; substitution and
cancellation of that factor give (14).  The same two quotient operations
with zero right side give (15). `QED`

If `y tensor C_k` is not proportional to `g_r`, the two atoms on the left
of (13) are linearly independent: they are `g_r-z` and `z` for a nonzero
`z notin Cg_r`.  Hence entry-minimality alone permits an irredundant bridge.

## 4. A three-colour irredundant common-cofactor module

The following exact module shows that sharing one near-top tensor does not
remove the bridges.  Let

\[
 J=\{0,1,2,3,4,5,6\},\qquad
 (a_0,b_0)=(0,1),\ (a_1,b_1)=(2,3),\ (a_2,b_2)=(4,5),      \tag{16}
\]

and put `y_r=r+1 mod 3`.  On
`R_r=J\setminus{a_r,b_r}`, define the three basis tensors `z_r` by the
following colour table:

\[
\begin{array}{c|ccccc}
r&\multicolumn{5}{c}{\text{colours on }R_r\text{ in increasing order}}\\ \hline
0&1&2&0&1&2\\
1&2&0&1&2&0\\
2&0&1&2&0&1
\end{array}                                                \tag{17}
\]

Define tensors on the indicated missing-site products by

\[
\begin{aligned}
 C_{a_r}&=e_r^{(b_r)}\otimes e_r^{\otimes R_r}
              -e_{y_r}^{(b_r)}\otimes z_r,\\
 C_{b_r}&=e_r^{(a_r)}\otimes z_r,\\
 C_6&=e_0^{(0)}e_0^{(1)}e_0^{(2)}e_0^{(3)}e_0^{(4)}e_1^{(5)}.
                                                               \tag{18}
\end{aligned}
\]

They are the multidegree components of the single near-top element
`f=sum_j C_j`.  Let `F` be its cofactor map (6).  For every colour `r`,

\[
 F\bigl(e_r\text{ at }a_r, e_{y_r}\text{ at }b_r\bigr)
 =e_r^{\otimes J}.                                        \tag{19}
\]

The transfer terms in (18) cancel exactly.

**Proposition 4.1.**  The full twenty-one-column map `F` is injective.
Hence the three preimages (19) are unique
and are in particular the unique least-norm preimages.  Every one uses two
centres, all six used derivative atoms are independent, and no constant
tensor has a one-centre preimage.

**Proof.**  Insert each of the three possible colours in the missing slot
of (18).  For the nine columns centred at an `a_r`, the first summand gives
the nine basis colourings

\[
 (l,0,0,0,0,0,0),\quad
 (1,1,l,1,1,1,1),\quad
 (2,2,2,2,l,2,2)\qquad(l=0,1,2).                           \tag{20}
\]

By inspection of (17), none of these nine colourings occurs in any other
column.  They are pivots, so every coefficient of an `a_r`-column in a
linear dependence is zero.  The remaining nine `b_r`-columns and the three
columns obtained from `C_6` are nonzero, pairwise distinct standard-basis
vectors, and are therefore independent.
This proves injectivity.

Equation (19) gives the preimages, so injectivity gives uniqueness and
least norm.  Finally, every `C_(a_r)` is the sum of two distinct basis
tensors, every `C_(b_r)` has a nonconstant colour pattern by (17), and
`C_6` is also nonconstant.
None satisfies the pure-cofactor criterion (12). `QED`

This example satisfies a stronger local condition than star
entry-irredundancy: the complete active cofactor map is injective.  It also
retains all endpoint asymmetry.  Its precise limitation matters: (18) is a
common near-top element, but it has **not** been represented as
`q^(m-1)/(m-1)!`.  Producing such a `q` together with (19) would already be
an eight-vertex counterexample by Section 1.  The example therefore isolates
the power condition, rather than evading it.

## 5. A genuine shared-power least-star counterexample in two colours

Least-star norm itself already fails to select the sparse form in an actual
matching source.  On vertices `0,...,5`, put same-colour diagonal cells

\[
\begin{array}{c|c|c}
\text{colour}&\text{edges}&\text{weights}\\ \hline
0&01,23&c,c\\
0&02,13&s,s\\
0&45&1\\
1&12,34,05&1
\end{array},
\qquad c={3\over5},\quad s={4\over5}.                     \tag{21}
\]

The support graph has exactly three perfect matchings,

\[
 01|23|45,\qquad02|13|45,\qquad05|12|34.                  \tag{22}
\]

Their tensors have coefficients `c^2`, `s^2`, and `1`, respectively.
Since `c^2+s^2=1`, this is the exact identity

\[
                         H_6=e_0^{\otimes6}+e_1^{\otimes6}.\tag{23}
\]

Fix vertex zero and let `q` be the actual internal quadratic on
`J={1,2,3,4,5}`.  Its four-site hafnian cofactors are

\[
\begin{aligned}
 C_1&=c e_0^{\otimes\{2,3,4,5\}},&
 C_2&=s e_0^{\otimes\{1,3,4,5\}},\\
 C_3&=e_1^{(1)}e_1^{(2)}e_0^{(4)}e_0^{(5)},&
 C_4&=0,\\
 C_5&=e_1^{\otimes\{1,2,3,4\}}.                          \tag{24}
\end{aligned}
\]

These are the components of the genuine common power `q^2/2`.  The two
star rows are

\[
 c\,e_0^{(1)}C_1+s\,e_0^{(2)}C_2=e_0^{\otimes J},
 \qquad e_1^{(5)}C_5=e_1^{\otimes J}.                     \tag{25}
\]

In the cofactor map, the only columns on the `e_0^(tensor J)` line are
`c e_0^(tensor J)` and `s e_0^(tensor J)`.  Its kernel on those columns is
spanned by `(s,-c)`.  All other nonzero columns in (24) are distinct
standard-basis tensors outside that line, while the two columns from `C_4`
are zero.  The coefficient vector `(c,s)` in (25) is orthogonal to
`(s,-c)` and to the zero-column directions.  It is therefore the exact
least-norm solution of the colour-zero row.  The colour-one row is visibly
least norm as well.

Thus the least star at vertex zero has the three cells

\[
 cE_{00}\text{ on }01,\qquad sE_{00}\text{ on }02,
 \qquad E_{11}\text{ on }05,                              \tag{26}
\]

where the binary cubic normal form would use only one edge per colour.
Replacing the first two cells by a single cell is possible but increases
the row norm: using `01` alone requires weight `1/c` and using `02` alone
requires weight `1/s`.  The least solution spreads the coefficient over
both copies.  The same calculation holds at every vertex; four vertices
have a duplicated colour-zero row.

This counterexample is diagonal and rational, so it does not depend on
endpoint symmetry, positivity in a cancellation argument, or numerical
approximation.  It proves that the least-star-normal-equation route cannot
by itself establish a cell-minimal star.  A ternary proof must use the
third target row through a genuinely nonlinear shared-power consequence,
not merely minimize the three row norms in (10).

## 6. Consequence for the fixed-star route

The proposed ternary cubic reduction can now be stated without ambiguity.
At an entry-minimal hypothetical source, it is enough to prove that for one
vertex (or for every vertex) the power `q^(m-1)` has the three pure
cofactors (12).  Proposition 3.1 would then give a three-cell replacement;
entry-minimality would make that star already cubic, and the existing cubic
rigidity/global matching argument would finish.

What is not available is a linear or variational shortcut to those pure
cofactors:

* simultaneous star kernels split rowwise by Proposition 2.1;
* irredundant two-centre Koszul bridges exist by Proposition 3.2;
* even an injective common-cofactor map can realize all three bridges at
  once by Proposition 4.1; and
* an actual common matching power can have a nonsparse least star by
  (21)--(26).

Therefore any continuation of this route must exhibit an identity that
uses the fact that all `C_j` are hafnian cofactors of the **same quadratic
q**, and must use all three nonzero target rows.  Proving merely another
property of the common linear map `F_q` which is compatible with the
injective module of Section 4 will not close the argument.

The exact audit
[`computations/verify_simultaneous_star_syzygy_boundary.py`](../computations/verify_simultaneous_star_syzygy_boundary.py)
checks the twenty-one-column rank and the three unique preimages in Section 4,
enumerates every matching coefficient in (23), constructs all actual
cofactors, and verifies the least-star orthogonality equations at all six
vertices over the rationals.
