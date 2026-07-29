# Independent audit of the centered rank-one overlap packet

## Verdict

The minimal three-private-coordinate overlap obstruction in
[the primary note](centered-rank-one-overlap-packet.md) is correct.  For the
sharp rank-one spoke in
[centered-low-degree-rank-tradeoff.md](centered-low-degree-rank-tradeoff.md),
the contracted 27-equation packet has a small exact common-quadratic
relaxation at eight sites.  That relaxation cannot, however, be lifted to the
four shared star forms required by an actual source.  More generally, none of
the 24 minimal private-coordinate incidence designs admits such a lift, even
when equality of quadratic representatives is weakened correctly modulo
`Ann(q)`.

One proposed intermediate assertion needs to be discarded: the direct
coefficients multiplying \(q^{[2]}\) are **not** forced to vanish.  On the
relevant four-site support their contribution lies in a one-dimensional
intersection and can cancel a coordinate component of the two product
blocks.  The corrected proof only uses the transverse components and leaves
that intersection untouched.

## 1. Reconstruction of the contracted packet

Use the rank-one sharp witness with

\[
 M=A_{x\mid y}=e_0e_0^T,
 \qquad
 (b_0,b_1,b_2)=(e_0,e_0+e_2,e_0+e_1),
\]

and

\[
 (P_0,P_1,P_2)=(0,e_0,e_0),\qquad
 (S_0,S_1,S_2)=(0,-e_0,-e_0).
\]

Here the \(P_c\)'s are the rows of \(A_{r\mid y}\), while the \(S_d\)'s
are the rows of \(A_{u\mid y}\).  Their common left kernel is

\[
 L=\langle f,h\rangle,
 \qquad f=e_0,\qquad h=e_1-e_2.                         \tag{1}
\]

The normalized data at \(x\) are therefore

\[
 p_{f,x}=s_{f,x}=f,\qquad
 p_{h,x}=h,\qquad s_{h,x}=-h.                          \tag{2}
\]

Since \(A_{y\mid x}=M^T=e_0e_0^T\), the third-star rows also satisfy

\[
 t_{0,x}=f,\qquad t_{1,x}=t_{2,x}=0.                  \tag{3}
\]

Let \(Y\) be the five-site common complement of \(r,u,y\), and let \(q\)
be its internal quadratic.  At \(N=8\), the complete three-endpoint identity
is

\[
 \begin{aligned}
 &\bigl(A_{r\mid u}(c,d)t_e+A_{r\mid y}(c,e)s_d
        +A_{u\mid y}(d,e)p_c\bigr)q^{[2]}
       +p_c s_d t_e q\\
 &\hspace{42mm}=\delta_{c=d=e}X_c^Y .                 \tag{4}
 \end{aligned}
\]

Contracting the \(c\)-index by \(l\in L\) and the \(d\)-index by
\(k\in L\) kills the two middle direct-block terms.  With

\[
 \beta_{lk}=l^TA_{r\mid u}k,
 \qquad
 F_{lk}=\beta_{lk}q^{[2]}+p_ls_kq,                    \tag{5}
\]

one obtains exactly

\[
                         t_eF_{lk}=l_ek_eX_e^Y.        \tag{6}
\]

This derivation retains endpoint order.  In particular, (2) follows from
\(s_{h,x}=b_1-b_2=e_2-e_1=-h\); there is no hidden sign or transpose change.

## 2. The exact common-\(q\) relaxation

Write \([ij]_{cc}=x_{i,c}x_{j,c}\) in the site-square-zero algebra on
\(Y=\{0,1,2,3,4\}\), and take \(x=0\).  Define

\[
\begin{aligned}
 q&=[34]_{00}+[24]_{11}+[13]_{22},\\
 C_{ff}&=[12]_{00},\\
 C_{hh}&=[03]_{11}+[04]_{22},\\
 C_{fh}&=C_{hf}=0,
\end{aligned}                                         \tag{7}
\]

and

\[
 t_0=x_{0,0},\qquad t_1=x_{1,1},\qquad t_2=x_{2,2}.   \tag{8}
\]

Direct multiplication gives

\[
\begin{aligned}
 C_{ff}q&=[12]_{00}[34]_{00},\\
 C_{hh}q&=[03]_{11}[24]_{11}+[04]_{22}[13]_{22}.
\end{aligned}                                         \tag{9}
\]

Every omitted cross-product has a repeated site and vanishes.  Consequently

\[
\begin{array}{c|cccc}
 &ff&fh&hf&hh\\ \hline
e=0&X_0^Y&0&0&0\\
e=1&0&0&0&X_1^Y\\
e=2&0&0&0&X_2^Y
\end{array}                                           \tag{10}
\]

for \(t_eC_{lk}q\).  This is precisely (6), because the coordinatewise
products of \(f=(1,0,0)\) and \(h=(0,1,-1)\) give the same table.  Equation
(8) also has exactly the local data (3).

Thus (7)--(8) is a genuine countermodel to an argument which treats the four
quartics \(F_{lk}\) as independent multiples of one \(q\).  It is not yet a
countermodel to the shared-star equations (5).

## 3. The quotient condition that a lift must satisfy

For five sites,

\[
                         q q=2q^{[2]}.                 \tag{11}
\]

Hence a proposed lift of \(F_{lk}=C_{lk}q\) need not satisfy equality of the
quadratic representatives.  Its exact condition is

\[
 C_{lk}-\frac{\beta_{lk}}2q-p_ls_k\in\operatorname{Ann}(q).
                                                               \tag{12}
\]

This distinction is essential: comparing the quadratic blocks in (12)
before multiplication by \(q\) would be invalid.

For distinct sites \(i,j\), orient the block with \(i\) first and put

\[
 K^{lk}_{i\mid j}
   =p_{l,i}\otimes s_{k,j}+s_{k,i}\otimes p_{l,j}.    \tag{13}
\]

Reversing the endpoints transposes this matrix.  In particular, with \(x\)
first, (2) gives

\[
\begin{aligned}
 K^{fh}_{x\mid j}&=f\otimes s_{h,j}-h\otimes p_{f,j},\\
 K^{hf}_{x\mid j}&=h\otimes s_{f,j}+f\otimes p_{h,j},\\
 K^{hh}_{x\mid j}&=h\otimes(s_{h,j}-p_{h,j}).         \tag{14}
\end{aligned}
\]

All three matrices have their \(x\)-factor in \(L\).  If \(x\) is the
second endpoint, the same statement holds for the right factor instead.

## 4. Minimal private-coordinate packets

Let \(v_0=x,v_1,v_2\) be distinct ports in a five-set \(Y\).  For each
colour \(c\), let \(D_c,T_c\) be two edges which partition
\(Y\setminus\{v_c\}\).  Choose nonzero scalars \(\mu_c,\nu_c\), and set

\[
 Q_c=\mu_c E^c_{T_c},\qquad Z_c=\nu_c E^c_{D_c},
 \qquad q=Q_0+Q_1+Q_2,                                \tag{15}
\]

where \(E^c_{\{i,j\}}=[ij]_{cc}\).  Impose the cross-privacy condition

\[
                         D_c\cap T_d\ne\varnothing
                         \quad(c\ne d).                \tag{16}
\]

Then the minimal response representatives are

\[
 C_{ff}=Z_0,\qquad C_{fh}=C_{hf}=0,
 \qquad C_{hh}=Z_1+Z_2.                               \tag{17}
\]

Condition (16) kills every wrong \(Z_cQ_d\), while
\(D_c\sqcup T_c=Y\setminus\{v_c\}\) retains \(Z_cQ_c\).  Suitable nonzero
scalar multiples of the coordinate forms \(x_{v_c,c}\) therefore give the
same response table (10).

There are six ordered edge partitions of each four-set
\(Y\setminus\{v_c\}\), hence \(6^3=216\) raw support triples.  An independent
enumeration chose each \(D_c\) from the six two-subsets, set \(T_c\) to its
complement, and tested all six ordered cross-intersections in (16).  It gives

\[
\begin{array}{c|c|r}
x\in D_1&x\in D_2&\text{designs}\\ \hline
\text{yes}&\text{yes}&2\\
\text{yes}&\text{no}&10\\
\text{no}&\text{yes}&10\\
\text{no}&\text{no}&2
\end{array}                                           \tag{18}
\]

Thus there are 24 private designs in total.  The next two sections cover all
22 designs in the first three rows and both designs in the last row.

## 5. A distinguished \(h\)-cap through \(x\) cannot lift

Suppose \(x\in D_c\) for \(c=1\) or \(2\), and write
\(D_c=\{x,j\}\).  In the four-site component on
\(Y\setminus\{v_c\}\), compare these two words:

1. the all-\(c\) word;
2. the word obtained by changing only the colour at \(x\) to the other
   member of \(\{1,2\}\).

The first word has the prescribed nonzero coefficient from \(Z_cQ_c\), and
the second has prescribed coefficient zero.  The only channel that can
produce either word on the lift side is

\[
                         K^{hh}_{x\mid j}Q_c.           \tag{19}
\]

Indeed, a cell \(Q_d\) with \(d\ne c\) places colour \(d\) at two sites, so
it cannot produce a word whose only non-\(c\) site is \(x\).  A direct term
from \(q^{[2]}\) uses two distinct \(Q\)-cells and has the same obstruction;
the square of \(Q_c\) vanishes by repeated sites.

By (14), the \(x\)-factor in (19) is \(h=e_1-e_2\).  Its coefficients at
the two compared words are exact negatives.  The all-\(c\) coefficient
cannot therefore be nonzero while the colour-swapped coefficient is zero.
This proves the obstruction in all 22 cases where at least one distinguished
\(h\)-cap uses \(x\).  The argument is unchanged after transposing an ordered
block.

## 6. The two remaining incidence designs

Assume now that \(x\notin D_1\cup D_2\).  Then \(x\in T_1\cap T_2\).
Let \(a,b\) be the two non-port sites.  Cross-privacy forces, up to swapping
\(a,b\), the unique pattern

\[
\begin{array}{c|cc}
c&T_c&D_c\\ \hline
0&\{v_1,v_2\}&\{a,b\}\\
1&\{x,a\}&\{v_2,b\}\\
2&\{x,b\}&\{v_1,a\}.
\end{array}                                           \tag{20}
\]

For completeness, since \(D_1\cap T_2\ne\varnothing\) and
\(D_2\cap T_1\ne\varnothing\), the non-\(x\) endpoints of \(T_1,T_2\)
must be the two distinct non-port sites \(a,b\).  Then
\(D_0\cap T_1\ne\varnothing\) and
\(D_0\cap T_2\ne\varnothing\) force \(D_0=\{a,b\}\), giving (20).

Consider a mixed congruence in (12) on the four-site support
\(Y\setminus\{b\}\).  Its only channels are

\[
 K^{lk}_{x\mid a}Q_0,qquad
 K^{lk}_{v_1\mid v_2}Q_1,qquad
 \beta_{lk}Q_0Q_1,                                   \tag{21}
\]

where the last term has coefficient one because \(q^{[2]}\) counts each
unordered disjoint pair once.  The first two channel spaces intersect in
exactly

\[
 \mathbb C\bigl(E_{11}^{x\mid a}
                 \otimes E_{00}^{v_1\mid v_2}\bigr). \tag{22}
\]

It follows that

\[
 K^{fh}_{x\mid a},K^{hf}_{x\mid a}\in
                         \mathbb C E_{11}^{x\mid a}.  \tag{23}
\]

On the other hand, (14) puts their \(x\)-factors in
\(L=\langle e_0,e_1-e_2\rangle\), and \(e_1\notin L\).  Therefore both
blocks in (23) vanish.  Independence of \(f,h\) in (14) gives

\[
 s_{h,a}=p_{f,a}=s_{f,a}=p_{h,a}=0.                   \tag{24}
\]

Repeating the argument on \(Y\setminus\{a\}\), with the coordinate line
\(\mathbb C E_{22}^{x\mid b}\), gives

\[
 s_{h,b}=p_{f,b}=s_{f,b}=p_{h,b}=0.                   \tag{25}
\]

Finally inspect the support \(Y\setminus\{x\}\) in the \(ff\) equation.
The prescribed nonzero word \(Z_0Q_0\) has only one possible lift channel,

\[
                         K^{ff}_{a\mid b}Q_0.          \tag{26}
\]

But (24)--(25) give \(K^{ff}_{a\mid b}=0\), contradicting the nonzero
coefficient \(\mu_0\nu_0\).  This closes the last two designs.

The role of `Ann(q)` is explicit in (21)--(23): the proof does not compare
quadratic representatives.  It compares their products with \(q\) on one
four-site support at a time.

## 7. The direct coefficients are not forced to vanish

Equation (21) also identifies the correction to the preliminary proof.
The direct term \(\beta_{lk}Q_0Q_1\) lies in the intersection (22).  Its
coefficient may be absorbed by the \(E_{11}\) component of
\(K^{lk}_{x\mid a}\), the \(E_{00}\) component of
\(K^{lk}_{v_1\mid v_2}\), or both.  Thus the support equation does not imply
\(\beta_{lk}=0\).

Only the mixed blocks' components transverse to (22) are forced to vanish.
Their prescribed \(x\)-factor then makes even the possible intersection
component zero, which is all the no-lift proof requires.  No cancellation of
a nonzero scalar, tensor, or star form occurs.

## 8. Exact scope

The result excludes every minimal three-private-coordinate realization of
the sharp rank-one spoke packet at \(N=8\), with arbitrary nonzero cell
weights and with the correct quotient by `Ann(q)`.  In particular, the
explicit relaxation (7)--(8) cannot be promoted to shared physical star
forms.

It does not eliminate the rank-one E2 branch.  A general solution may use
additional cells in \(q\), non-coordinate or multi-site third-star forms,
extra diagonal representatives killed after multiplication by the relevant
\(t_e\), or nonzero mixed quartics annihilated by all three \(t_e\).  Nor does
this five-site argument by itself control the higher common powers occurring
above \(N=8\).  Those are the remaining overlap/diagonal residuals after this
minimal packet is removed.
