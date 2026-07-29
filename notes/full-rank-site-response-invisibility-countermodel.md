# Full-rank-site response invisibility and the two-site frontier

## 1. Result

The determinant, adjugate, and sitewise chain identities from
[`sitewise-common-power-response-filtration.md`](sitewise-common-power-response-filtration.md)
do not propagate a rank-three incident space to another site.  In fact,
this remains false after retaining independent target triples at a second
site.

Two exact rational countermodels are given below.  The first exposes the
two-vector deformation kernel of the one-site scalar response.  In it,
the projected target rank is exactly

\[
 \dim\bigl(W_0\cap\operatorname {span}\{e_0,e_1,e_2\}\bigr)=3. \tag{1}
\]

The stronger second model has independent frames at sites zero and one,
and satisfies

\[
 p_i s_jq^{[2]}=\delta_{ij}
       e_i^{(0)}e_i^{(1)}z_2z_3z_4z_5,\qquad q^{[3]}=0. \tag{2}
\]

while

\[
 W_0=\operatorname {span}\{e_0^{(0)},e_1^{(0)},e_2^{(0)}\},
 \qquad W_1=\mathbb C e_2^{(1)}.                        \tag{3}
\]

Thus even two-site target separation does not force a second rank-three
endpoint space.  The global six-site four-cover remains essential.

### The first model

Let

\[
 {\mathcal R}=({\mathbb C}\oplus V_0)\otimes
          \bigotimes_{v=1}^5({\mathbb C}\oplus {\mathbb C}z_v),
 \qquad V_0=\operatorname {span}\{e_0,e_1,e_2\}.
\]

There is a quadratic element \(q\), and six linear elements \(p_i,s_j\),
such that

\[
 q^{[3]}=0,
 \qquad
 p_i s_jq^{[2]}=\delta_{ij}e_i z_1z_2z_3z_4z_5.       \tag{4}
\]

Moreover the incident endpoint space at site zero is

\[
                         W_0=V_0,                       \tag{5}
\]

so it contains all three target axes.  For arbitrary covectors at site
zero, the scalar response is the full reduced diagonal pencil, its
adjugate has the expected three pair products, and the cofactor matrix is
generically nonsingular.  The vector chain identity is also exact.

Thus no argument using only the identities visible after fixing the other
five site covectors can prove \(\dim W_0\leq2\), or force another site to
have rank at least two.  A positive rank-propagation lemma must retain
target separation at at least one additional site (or use an equivalent
genuinely cross-site tensor identity).

This first model is not a ternary six-site GHZ system: sites
\(1,\ldots,5\) are
one-dimensional.  It is a countermodel to the proposed *local invariant*,
not to Krenn's conjecture.

## 2. A two-vector response-invisible deformation

For arbitrary \(a,b\in V_0\), put

\[
\begin{aligned}
q(a,b)={}&(2e_2+a)z_1+az_2+2e_2z_3+bz_4+bz_5\\
 &+z_1z_5-z_2z_5+z_2z_4+z_3z_4.                       \tag{6}
\end{aligned}
\]

The internal graph on \(\{1,\ldots,5\}\) has deleted-vertex four-site
matching cofactors

\[
                (c_1,c_2,c_3,c_4,c_5)=(-1,1,1,0,0).   \tag{7}
\]

Every perfect matching uses one edge incident with site zero.  Therefore

\[
\begin{aligned}
q(a,b)^{[3]}
 &=\sum_{v=1}^5c_vq_{0v}\\
 &=-(2e_2+a)+a+2e_2=0.                                \tag{8}
\end{aligned}
\]

Equation (8) also exhibits the sitewise chain relation without selecting
one term from a cancelling sum.  The deformation

\[
 (\Delta q_{01},\Delta q_{02},\Delta q_{03},
   \Delta q_{04},\Delta q_{05})=(a,a,0,b,b)             \tag{9}
\]

lies simultaneously in the cubic-chain kernel and in the kernel of all
nine response entries below.  The two free vectors in (9) are the reason
the original one-line scalar cycle can acquire a three-dimensional star.

Indeed, let \(t_v\in V_0\) be arbitrary changes to the five star blocks.
After applying a covector \(x\in V_0^*\), write the resulting scalars with
the same letters.  With the fixed rows below, the complete response change
is

\[
 \Delta M=
 \begin{pmatrix}
 0&0&0\\
 (t_4-t_5)/2&0&0\\
 (-t_1+t_2+t_3)/2&0&(t_1-t_2+t_3)/4
 \end{pmatrix}.                                        \tag{10}
\]

The cubic-chain change is \(-t_1+t_2+t_3\).  Thus (9) kills the chain
and every entry of (10) vector-valuedly, before choosing \(x\).

Take

\[
\begin{array}{lll}
p_0=e_0,&p_1=(-z_1+z_3)/2,&p_2=z_4,\\[1mm]
s_0=(-z_1+z_3)/2,&s_1=e_1,&s_2=-(z_1+z_3)/4.
\end{array}                                            \tag{11}
\]

The rows (11) do not depend on \(a,b\).  Direct multiplication in the
site-square-zero algebra gives, for every \(a,b\),

\[
 p_i s_jq(a,b)^{[2]}
       =\delta_{ij}e_i z_1z_2z_3z_4z_5.               \tag{12}
\]

In particular, choose \(a=e_0\) and \(b=e_1\).  The five incident blocks
then contain \(e_0,e_1,e_2\), proving (5), while (8) and (12) remain
unchanged.

## 3. Exact cofactor and determinant audit

Normalize the five line covectors by \(\ell_v(z_v)=1\), and set

\[
 x_i=\ell_0(e_i),\qquad A=\ell_0(a),\qquad B=\ell_0(b).
\]

In site order \(0,1,2,3,4,5\), the deleted-pair cofactor matrix is

\[
C(A,B)=
\begin{pmatrix}
0&-1&1&1&0&0\\
-1&0&B&0&-2x_2&A+2x_2\\
1&B&0&B&2x_2&A+2x_2\\
1&0&B&0&-2x_2&A+2x_2\\
0&-2x_2&2x_2&-2x_2&0&0\\
0&A+2x_2&A+2x_2&A+2x_2&0&0
\end{pmatrix}.                                        \tag{13}
\]

The response-row matrices are

\[
P=\begin{pmatrix}
x_0&0&0&0&0&0\\
0&-1/2&0&1/2&0&0\\
0&0&0&0&1&0
\end{pmatrix},\qquad
S=\begin{pmatrix}
0&-1/2&0&1/2&0&0\\
x_1&0&0&0&0&0\\
0&-1/4&0&-1/4&0&0
\end{pmatrix}.                                        \tag{14}
\]

Multiplication, with both endpoint orders retained, yields the polynomial
identity

\[
       PC(A,B)S^{\mathsf T}=\operatorname {diag}(x_0,x_1,x_2), \tag{15}
\]

independently of \(A,B\).  Hence

\[
 \det(PCS^{\mathsf T})=x_0x_1x_2,
 \quad
 \operatorname {adj}(PCS^{\mathsf T})
       =\operatorname {diag}(x_1x_2,x_0x_2,x_0x_1).   \tag{16}
\]

Even singularity of the full cofactor form supplies no hidden defect:

\[
                         \det C=-64x_2^2(A+2x_2)^2.   \tag{17}
\]

which is nonzero on a dense open set.  For \(a=e_0,b=e_1\), equations
(13)--(17) are identities in the three independent variables
\(x_0,x_1,x_2\).

## 4. Two separated target sites still do not propagate rank

Let \(V_0,V_1\) have independent bases

\[
 (e_0,e_1,e_2),\qquad(f_0,f_1,f_2),
\]

and let sites \(2,3,4,5\) be the lines \(\mathbb Cz_2,\ldots,
\mathbb Cz_5\).  Put

\[
\begin{aligned}
q={}&(2e_2+e_1)f_2+e_1z_2+2e_2z_3+e_0z_5+f_2z_5\\
   &-z_2z_5+z_2z_4+z_3z_4.                              \tag{18}
\end{aligned}
\]

where juxtaposition between two different sites denotes their tensor
product.  There are three perfect matchings.  Grouping at site zero
gives the tensor identity

\[
 -(2e_2+e_1)f_2+e_1f_2+2e_2f_2=0,                     \tag{19}
\]

so \(q^{[3]}=0\).

Take

\[
\begin{array}{lll}
p_0=e_0,&p_1=f_1,&p_2=z_2-z_3,\\[1mm]
s_0=-f_0,&s_1=-e_1,&s_2=(e_1+z_4+z_5)/4.
\end{array}                                            \tag{20}
\]

Exact multiplication gives (2).  Every block incident with site one has
endpoint factor \(f_2\), whereas the site-zero star contains
\(e_0,e_1,e_2\).  This proves (3), including target-space projected rank
three at site zero and rank one at site one.

For a scalar audit set

\[
x_i=\ell_0(e_i),\qquad y_i=\ell_1(f_i).
\]

The same deleted-pair construction gives a generically invertible
cofactor matrix with

\[
                     \det C=-64x_2^2y_2^4(x_1+2x_2)^2. \tag{21}
\]

and the rows (20) satisfy

\[
              PCS^{\mathsf T}
       =\operatorname {diag}(x_0y_0,x_1y_1,x_2y_2).    \tag{22}
\]

Consequently the two-site determinant and every adjugate entry have
exactly the target bidegrees.  Neither the cofactor rank nor the two local
chain identities expose the hidden rank-one second star.

## 5. What the global four-cover still forces

The countermodels above deliberately collapse at least four target
triples.  In an actual six-site response, let

\[
 r_u=\#\{i:e_i^{(u)}\in W_u\}.
\]

The four-cover theorem gives

\[
 \sum_ur_u=\sum_i|D_i|\geq12,
 \qquad r_u\leq\dim W_u,                              \tag{23}
\]

and therefore

\[
                         \sum_u\dim W_u\geq12.        \tag{24}
\]

In particular, if exactly one site has dimension three and all others
have dimension at most two, at least four of the remaining five sites
have dimension two.  The two-site model has total endpoint dimension
only eight and deliberately lies outside the six-site target hypothesis
used to derive (24); this precisely locates its scope.

There is a rigid equality case.

**Proposition 5.1 (rank-budget equality normal form).**  If

\[
                         \sum_u\dim W_u=12,            \tag{25}
\]

then every \(W_u\) is exactly the span of the target axes it contains,
every colour occurs in four endpoint spaces, and its omission set

\[
                         B_i=\{u:e_i^{(u)}\notin W_u\} \tag{26}
\]

is a pair.  If at least one site has rank three, the numbers of rank
three, rank two, and rank one sites are respectively

\[
                    (1,4,1),\qquad(2,2,2),\qquad(3,0,3). \tag{27}
\]

Equivalently, a site belongs to \(3-\dim W_u\) omission pairs.  Up to
relabeling, the pair-overlap types are:

1. \((1,4,1)\): two omission pairs meet once and the third is disjoint;
2. \((2,2,2)\): either two pairs coincide and the third is disjoint, or
   one pair meets each of the other two and those two are disjoint;
3. \((3,0,3)\): the three pairs form a triangle, with three distinct
   intersection sites.

**Proof.**  Equality in (23)--(25) forces equality term by term:
\(r_u=\dim W_u\) at every site and \(|D_i|=4\) for every colour.  Since
the contained target axes are independent, they span \(W_u\).  The site
cover makes every rank positive.  If \(n_j\) denotes the number of
rank-\(j\) sites, then

\[
 n_1+n_2+n_3=6,\qquad n_1+2n_2+3n_3=12,
\]

so \(n_1=n_3\), which gives (27).  Counting omission-pair memberships at
each rank gives the three listed overlap types.  \(\square\)

The equality case also admits a support-independent quotient refinement.
Decompose \(F=q^{[2]}\) by its missing pair,

\[
                         F=\sum_{P\in\binom U2}F_P.
\]

Quotient the two sites of a pair \(P=\{a,b\}\) by \(W_a,W_b\), retaining
all response indices.  Only \(F_P\) survives.  Define the matrix-valued
quotient tensor

\[
 (N_P)_{rs}=\bar p_{r,a}\otimes\bar s_{s,b}
             +\bar s_{s,a}\otimes\bar p_{r,b}
 \quad\in(V_a/W_a)\otimes(V_b/W_b).                    \tag{28}
\]

The nine quotient equations give

\[
 N_P\otimes F_P=
 \sum_{i:B_i=P}E_{ii}\otimes
   \bar e_i^{(a)}\otimes\bar e_i^{(b)}\otimes E_i(P). \tag{29}
\]

Flatten (29) as

\[
 \left(\operatorname {Mat}_3\otimes V_a/W_a\otimes V_b/W_b\right)
 \ \big|\ \left(\bigotimes_{u\notin P}W_u\right).      \tag{30}
\]

If two colours had the same omission pair, their left and right factors
in this flattening would each be independent, so the right side of (29)
would have rank at least two, while the left side has rank at most one.
Hence the \(B_i\) are pairwise distinct.  For \(P=B_i\), uniqueness
of a nonzero simple tensor gives a scalar \(\theta_i\ne0\) with

\[
 N_{B_i}=\theta_iE_{ii}\otimes
       \bar e_i^{(a)}\otimes\bar e_i^{(b)},\qquad
 F_{B_i}=\theta_i^{-1}E_i(B_i).                         \tag{31}
\]

Thus the coincident-pair subtype in (27) is impossible, and the *entire*
four-site slice on each omission pair is pure even though all other
missing-pair slices may remain mixed.  This is the concrete cross-site
frontier left by the failure of one- and two-site determinant propagation.

The standalone checker
[`verify_full_rank_site_response_invisibility_countermodel.py`](../computations/verify_full_rank_site_response_invisibility_countermodel.py)
reconstructs every matching power in the square-zero tensor algebra,
checks both sets of nine tensor responses over \(\mathbb Q\), derives the
cofactor matrices independently from deleted-pair matchings, verifies the
two deformation kernels and determinant identities symbolically, and
exhausts the finite incidence and omission-pair classification in
Proposition 5.1.
