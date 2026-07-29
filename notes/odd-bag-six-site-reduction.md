# A six-odd-bag reduction criterion

Let (B) have even order and partition it into six nonempty odd bags

\[
                         B=C_1\sqcup\cdots\sqcup C_6.      \tag{1}
\]

This note gives a coordinate-free sufficient condition under which an exact
matching tensor on (B) collapses to an ordinary matching tensor on the six
bags.  The condition is exactly a linear-span separation: in each bag, the
three constant-color tensors must survive modulo every local sector coming
from matchings with at least three crossing edges.

The final flattening rank of the GHZ tensor does not imply this separation.
It constrains the sum of all crossing sectors, while the criterion concerns
the left Schmidt spaces of the individual high-crossing matching terms.
Order-minimality likewise gives no formal implication beyond the already
known tight-cut case.

## 1. Local high-crossing sector spaces

Write

\[
                         V_C=\bigotimes_{v\in C}V_v,
 \qquad
 t_M=\bigotimes_{uv\in M}A_{uv}                           \tag{2}
\]

for a perfect matching (M) of (B).  For a bipartition (C|B\setminus C),
let

\[
 \operatorname {LS}_C(t_M)\subseteq V_C                 \tag{3}
\]

be the left Schmidt space of (t_M): equivalently, it is the image of the
flattening map obtained by contracting all (B\setminus C) slots with
arbitrary covectors.  This definition retains arbitrary ranks and
asymmetric endpoint matrices and is independent of any chosen rank
factorization.

For an odd bag (C), every perfect matching crosses its cut an odd number of
times.  Define its high-crossing space

\[
 \mathcal W_C=\sum_{\substack{M\in\operatorname {PM}(B)\\
                      |M\cap\delta(C)|\ge3}}
                         \operatorname {LS}_C(t_M).        \tag{4}
\]

Zero matching terms contribute the zero subspace.  Thus a linear map
(\Phi_C:V_C\to\mathbb C^3) with

\[
                         \mathcal W_C\subseteq\ker\Phi_C \tag{5}
\]

kills every individual perfect-matching term having at least three crossing
edges at (C), even before cancellations with other matchings.

Put

\[
 g_{C,r}=e_r^{\otimes C},\qquad
 \mathcal G_C=\operatorname {span}\{g_{C,0},g_{C,1},g_{C,2}\}.\tag{6}
\]

**Lemma 1.1 (exact local span criterion).**  There is a linear map
(\Phi_C) satisfying

\[
 \Phi_C(\mathcal W_C)=0,
 \qquad \Phi_C(g_{C,r})=e_r\quad(r=0,1,2)                 \tag{7}
\]

if and only if

\[
                         \boxed{\mathcal G_C\cap\mathcal W_C=0.}\tag{8}
\]

**Proof.**  Necessity follows because the prescription in (7) is injective
on (\mathcal G_C).  Conversely, (8) makes the three classes of the
(g_{C,r}) independent in (V_C/\mathcal W_C).  Send those classes to the
three coordinate basis vectors, extend arbitrarily to the quotient, and
compose with the quotient map.  `QED`

One may replace (4) by a larger, easier-to-check sufficient span.  For an
odd set (S\subseteq C), an internal perfect matching (N) of (C\setminus S),
and a matching (F) from (S) to distinct vertices outside (C), contract the
outside endpoints of

\[
       \left(\bigotimes_{xy\in N}A_{xy}\right)
       \left(\bigotimes_{uv\in F}A_{uv}\right)            \tag{9}
\]

by arbitrary covectors and take the resulting span in (V_C).  Summing these
spaces over all odd (|S|\ge3) contains (\mathcal W_C).  Disjointness of
(\mathcal G_C) from this larger span is therefore sufficient, although not
necessary.

## 2. Exact collapse to six aggregate vertices

Assume (8) for every bag and choose maps (\Phi_a=\Phi_{C_a}) as in (7).
For distinct bags (C_a,C_b), define an effective aggregate edge

\[
 \begin{split}
 Y_{ab}=\sum_{u\in C_a}\sum_{v\in C_b}
 (\Phi_a\otimes\Phi_b)\bigl(&H_{C_a\setminus\{u\}}(A)
              \otimes A_{uv}\\
              &\otimes H_{C_b\setminus\{v\}}(A)\bigr),  \tag{10}
 \end{split}
\]

with tensor slots restored to their natural bag order before applying the
maps.  This is an arbitrary element of (\mathbb C^3\otimes\mathbb C^3), so
it is a legitimate aggregate edge matrix.

**Theorem 2.1 (six-odd-bag reduction).**  If

\[
                         H_B(A)=\Delta_{B,3}               \tag{11}
\]

and every bag satisfies (8), then the effective edges (10) obey

\[
                         H_{\{1,\ldots,6\}}(Y)=\Delta_{6,3}.\tag{12}
\]

**Proof.**  For a perfect matching (M), let (d_a) be the number of its
edges crossing (\delta(C_a)).  Since every bag is odd, every (d_a) is odd.
If some (d_a\ge3), equations (4)--(5) make

\[
                 (\Phi_1\otimes\cdots\otimes\Phi_6)t_M=0.\tag{13}
\]

The only surviving matchings therefore have (d_a=1) at all six bags.  Their
crossing edges induce a perfect matching of the six bags.  After that
supermatching is fixed, choosing its original crossing edge (uv) and the
internal perfect matchings of (C_a\setminus\{u\}) and
(C_b\setminus\{v\}) is independent for every superedge.  The sum of those
choices is exactly (Y_{ab}) in (10).  Hence the sum of all surviving terms
is (H_6(Y)).

On the other hand, (7) sends the target to

\[
 (\Phi_1\otimes\cdots\otimes\Phi_6)\Delta_{B,3}
 =\sum_{r=0}^2e_r^{\otimes6}=\Delta_{6,3}.                 \tag{14}
\]

Applying the six maps to (11) and combining (13)--(14) proves (12).
`QED`

The tight-cut collapse is the special case in which one relevant odd bag
has no high-crossing sector at all.  Theorem 2.1 permits such sectors, but
requires their local Schmidt spaces to miss the three diagonal directions.

## 3. What a hypothetical minimal counterexample must do

The established six-site obstruction immediately gives the contrapositive.

**Corollary 3.1 (diagonal contamination certificate).**  In any
hypothetical exact realization on more than six vertices, every partition
into six nonempty odd bags has a bag (C_a) for which

\[
 \mathcal G_{C_a}\cap\mathcal W_{C_a}\ne0.                \tag{15}
\]

Equivalently, for that bag there are scalars not all zero such that

\[
 \lambda_0e_0^{\otimes C_a}+lambda_1e_1^{\otimes C_a}
      +\lambda_2e_2^{\otimes C_a}\in\mathcal W_{C_a}.    \tag{16}
\]

This conclusion does not require support minimality.  If one additionally
chooses an order-minimal realization, tight-cut freeness says that every
nontrivial odd shore participates in some matching with at least three
crossing edges; it only proves (\mathcal W_C\ne0), not the intersection
(15).

## 4. Flattening rank three does not imply the span separation

Across (C|B\setminus C), the target has left Schmidt space exactly
(\mathcal G_C) and flattening rank three.  That statement concerns the
*sum* of the one-crossing and high-crossing sectors.  It gives no
disjointness information about either sector separately.

The failure is already exact linear algebra.  Let (r_0,r_1,r_2) be
independent right-side vectors and decompose

\[
 \sum_{i=0}^2g_{C,i}\otimes r_i
 =\underbrace{g_{C,1}\otimes r_1+g_{C,2}\otimes r_2}_{T_1}
  +\underbrace{g_{C,0}\otimes r_0}_{T_{\ge3}}.            \tag{17}
\]

The total tensor has flattening rank three, while the left Schmidt space of
(T_{\ge3}) contains (g_{C,0}); hence
(\mathcal G_C\cap\operatorname {LS}(T_{\ge3})\ne0).
Arbitrary cancellation terms can be added to both summands without changing
the total.  Therefore no argument using only the final flattening rank can
prove (8).

There is also no support-only substitute.  A tight-cut-free graph can have
matchings with three or more crossing edges across every nontrivial odd cut,
and full-rank crossing matrices can make the local spaces in (4) very large.
What remains open is whether the *simultaneous exact GHZ cancellation
equations*, together with order minimality, force one six-bag partition to
escape the contamination certificate (16).  Theorem 2.1 isolates that as a
precise linear-span problem; rank three by itself does not solve it.
