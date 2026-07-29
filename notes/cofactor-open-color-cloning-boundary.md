# Cofactor-open color cloning kills every mixed-with-zero layer

## Outcome

Assume only the two complete binary restrictions on colors `0/1` and
`0/2`, as opposed to all three principal binary restrictions.  Then the
first genuinely ternary cubic layer need not contain a nonzero coefficient.
There is a uniform obstruction: **local color cloning** turns any exact
binary source into a ternary source for which

\[
 H(\widetilde A)
   =X_0+\bigotimes_{i\in B}(e_1+\lambda_i e_2).            \tag{1}
\]

If `product_i lambda_i=1`, both the `0/1` and `0/2` faces are exact, while
every coefficient containing color zero and at least one nonzero color
vanishes.  This includes every genuinely ternary coefficient of total
nonzero-color degree three, and indeed every such degree from one through
`n-1`.

The construction is compatible with the cofactor-kernel parametrization.
It keeps the scalar leading matrix `C` unchanged, scales the second first
jet rowwise from the first, and its four second-jet blocks are exactly the
unique cofactor-open quadratic lifts.  At four sites there is an explicit
rational binary seed with `haf(C)=1` and all six two-hole cofactors nonzero.
Two nonproportional active first jets obtained from it give an exact
countermodule satisfying all the stated hypotheses and all degree-three
equations.

Thus there is no theorem, from the two binary faces and cofactor openness
alone, forcing a nonzero mixed cubic.  A positive continuation for
`n>=6` must either prove that the required cofactor-open binary seed cannot
exist at those orders or use the omitted `1/2` face.  The clone fails that
third face in the sharpest possible way: its full-support `1/2` tensor is
decomposable rather than binary equality.

## 1. The local color-cloning identity

Let `A` be an arbitrary binary decorated-edge source on a vertex set `B`.
For an edge `ij`, write its aggregate matrix as

\[
                         A_{ij}(r,s),\qquad r,s\in\{0,1\}.
\]

Fix nonzero scalars `lambda_i`.  Collapse the ternary colors by

\[
 \bar0=0,\qquad \bar1=\bar2=1,
\]

and put

\[
 \mu_i(0)=\mu_i(1)=1,\qquad \mu_i(2)=\lambda_i.
\]

Define a ternary source on the same pairs by

\[
 \widetilde A_{ij}(r,s)
       =\mu_i(r)\mu_j(s)A_{ij}(\bar r,\bar s).             \tag{2}
\]

This formula retains arbitrary endpoint order and arbitrary aggregate
matrices; it is not a diagonal-edge construction.

**Lemma 1 (local color cloning).**  For every ternary word
`gamma:B -> {0,1,2}`,

\[
 [e_\gamma]H(\widetilde A)
   =\left(\prod_{i:\gamma(i)=2}\lambda_i\right)
      [e_{\bar\gamma}]H(A).                               \tag{3}
\]

Consequently, if

\[
                              H(A)=X_0+X_1,               \tag{4}
\]

then (1) holds.  If also `product_i lambda_i=1`, the two
restrictions `0/1` and `0/2` are respectively `X_0+X_1` and `X_0+X_2`.
Every word using zero and one or both of the other colors has coefficient
zero.

**Proof.**  In any perfect-matching term compatible with `gamma`, every
site occurs in exactly one selected edge.  The product of the factors
`mu_i(gamma(i))` from (2) is therefore
`product_(gamma(i)=2) lambda_i`, independently of the selected matching.
After removing it, the remaining matching term is exactly the term of `A`
compatible with the collapsed word `bar gamma`.  Summing the matching
terms proves (3).  Substitution of (4) gives (1) and all remaining claims.
`QED`

Under the uniform pure-limit torus `diag(1,t,t)`, (1) becomes

\[
 H(\widetilde A(t))
   =X_0+t^n\bigotimes_i(e_1+\lambda_i e_2).                \tag{5}
\]

Thus the clone has no intermediate output jet at any order, although both
missing colors have nonzero first-source jets whenever the seed does.

## 2. Compatibility with the cofactor-open lift

Decompose the binary source relative to its color-zero endpoint as

\[
 A=C+B+D,
\]

where `C`, `B`, and `D` have respectively zero, one, and two color-one
endpoints.  Write `b_ij` for the directed cell having color one at `i` and
zero at `j`, and write `d_ij` for the `11` cell.  If

\[
 h_{ij}=\operatorname{haf}C[B\setminus\{i,j\}],           \tag{6}
\]

then the degree-one binary equations say

\[
                         \sum_{j\ne i}b_{ij}h_{ij}=0.      \tag{7}
\]

On the locus where every `h_ij` is nonzero, the degree-two equation gives
the unique bilinear lift

\[
 Q_C(b,b')_{ik}=-{1\over h_{ik}}
 \sum_{\substack{j,\ell\notin\{i,k\}\\j\ne\ell}}
 b_{ij}b'_{k\ell}h_{ikj\ell}.                            \tag{8}
\]

For the cloned source, the two first jets and four second blocks are

\[
\begin{array}{c|c}
 b^1_{ij}=b_{ij}&b^2_{ij}=\lambda_i b_{ij}\\ \hline
 a^{11}_{ik}=d_{ik}&a^{12}_{ik}=\lambda_kd_{ik}\\
 a^{21}_{ik}=\lambda_id_{ik}&
 a^{22}_{ik}=\lambda_i\lambda_kd_{ik}.
\end{array}                                               \tag{9}
\]

Row scaling preserves (7).  More strongly, (8) is local in its two exposed
rows, so

\[
\begin{aligned}
 Q_C(b^1,b^1)_{ik}&=d_{ik},&
 Q_C(b^1,b^2)_{ik}&=\lambda_kd_{ik},\\
 Q_C(b^2,b^1)_{ik}&=\lambda_id_{ik},&
 Q_C(b^2,b^2)_{ik}&=\lambda_i\lambda_kd_{ik}.
\end{aligned}                                             \tag{10}
\]

Hence (9) is precisely the simultaneous unique second lift.  Formula (3)
then says that every third and higher mixed-with-zero obstruction also
vanishes, without relying on a polarization sum over vertex placements.
This last point matters: ordinary cubic polarization alone would only
annihilate sums of differently placed `112` words, whereas (3) annihilates
each word separately.

## 3. An exact cofactor-open four-site seed

On vertices `0,1,2,3`, use the following scalar leading weights, directed
first cells, and `11` cells.  Unlisted directed first cells are zero.

\[
\begin{array}{c|r|rr|r}
ij&C_{ij}&b_{ij}&b_{ji}&d_{ij}\\ \hline
01&-1& 1& 0&-1\\
02& 1&-1& 1&-1\\
03& 1& 0& 1&-1\\
12& 1& 1& 0& 1\\
13& 1&-1&-1&-1\\
23& 1& 1& 0&-1
\end{array}                                               \tag{11}
\]

The leading hafnian and two-hole cofactors are

\[
 \operatorname{haf}C=(-1)(1)+(1)(1)+(1)(1)=1,
\]

\[
 (h_{01},h_{02},h_{03},h_{12},h_{13},h_{23})
                         =(1,1,1,1,1,-1).                 \tag{12}
\]

Thus the leading point is cofactor-open.  The four row equations (7) are
respectively `1-1`, `1-1`, `1-1`, and `1-1`.  Formula (8) gives exactly
the last column of (11).

For completeness, the remaining binary equations can be checked without
any geometry.  At degree three, according to which unique zero site
remains, the four coefficients are

\[
\begin{array}{c|c}
0&b_{20}d_{13}+b_{30}d_{12}=-1+1\\
1&b_{01}d_{23}+b_{31}d_{02}=-1+1\\
2&b_{02}d_{13}+b_{12}d_{03}= 1-1\\
3&b_{13}d_{02}+b_{23}d_{01}= 1-1.
\end{array}                                               \tag{13}
\]

The terminal coefficient is

\[
 \operatorname{haf}D=d_{01}d_{23}+d_{02}d_{13}+d_{03}d_{12}
                     =1+1-1=1.                           \tag{14}
\]

Together with (7)--(8), equations (12)--(14) prove exactly that the binary
source (11) has output `X_0+X_1`.

## 4. Two nonproportional jets with every cubic zero

Apply Lemma 1 to (11) with

\[
                         (\lambda_0,\lambda_1,
                           \lambda_2,\lambda_3)=(1,1,-1,-1).          \tag{15}
\]

Their product is one.  The resulting rational ternary source has

\[
 H(\widetilde A)=X_0+
 (e_1+e_2)\otimes(e_1+e_2)\otimes
 (e_1-e_2)\otimes(e_1-e_2).                              \tag{16}
\]

Its color-one first jet is `b`, while its color-two first jet is obtained
by multiplying rows zero and one by `1` and rows two and three by `-1`.
Both jets are active in every row, and the two full directed vectors are
not proportional.  Nevertheless:

* the complete `0/1` and `0/2` restrictions are exact binary equality;
* every output coefficient of total nonzero-color degree one, two, or
  three is zero;
* in particular all 24 degree-three words that use both colors one and two
  vanish individually; and
* both pure terminal coefficients are one.

The omitted `1/2` face of (16) has all sixteen coefficients nonzero.  Its
fourteen mixed words are precisely where the construction violates ternary
equality.  In flattening language it is one decomposable tensor, whereas
`X_1+X_2` has rank two.

The dependency-free exact audit
`computations/verify_cofactor_open_color_cloning.py` enumerates the original
sixteen binary coefficients and all 81 cloned ternary coefficients, checks
(7)--(10), verifies cofactor openness and nonproportionality, and counts the
24 vanishing mixed cubics and fourteen errors on the third face.

## 5. Consequence for the cubic route

The two complete binary faces do not couple the two missing colors.  Local
cloning exhibits the precise freedom: the second color can be a different
sitewise representative of the same binary line.  Cofactor openness makes
the second lift unique but does not remove this freedom, because the lift
is equivariant under independent row scalings.

Therefore a proposed implication

\[
 \text{cofactor-open `C' + exact faces `01,02'}
   \quad\Longrightarrow\quad
 \text{some mixed cubic is nonzero}                      \tag{17}
\]

is false as stated.  The four-site module is an exact rational witness,
and Lemma 1 makes the obstruction uniform in the order conditional on any
cofactor-open exact binary seed.  For the conjectural range `n>=6`, there
are only two logically stronger continuations:

1. prove a one-binary theorem excluding cofactor-open exact binary seeds
   at those orders; or
2. impose the third `1/2` binary face and show that it is incompatible with
   the cloned (or more generally common-line) branch.

Merely proceeding to degree four or higher while still requiring a zero
site cannot detect the clone, by (3).  The next information must instead
come from the full-support `1/2` sector or from an independent order-six
binary rigidity theorem.
