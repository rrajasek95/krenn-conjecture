# One marked exceptional site closes the axial extra-plane boundary

## 1. Outcome

Continue from
[live-three-zero-extra-plane-two-marked-transverse.md](live-three-zero-extra-plane-two-marked-transverse.md).
There are \(2r\) live sites, exactly \(t\) of them have beta value
different from the common centre value, and the sole extra singular site
\(e\) satisfies

\[
                  \operatorname {im}P_e=\langle e_0,e_1\rangle . \tag{1}
\]

Normalize the third output row of \(P_e\) to zero and put
\(R=\operatorname {row}P_e\).  This note treats the two axial families
left by the transverse argument.

**Theorem 1.1 (axial extra-plane injectivity).**  Suppose

\[
 r\ge2,\qquad 1\le t\le\min(2r,r+2),\qquad
 R\cap\langle e_0,e_1\rangle=\mathbb C e_0
 \quad\hbox{or}\quad
 R\cap\langle e_0,e_1\rangle=\mathbb C e_1.                     \tag{2}
\]

Then the complete residual star at the shared zero \(z_0\) vanishes.
Consequently \(z_0\) has no rank-three neighbour.

Together with the transverse theorem, this closes every row plane in the
range \(2\le t\le\min(2r,r+2)\).  The case \(t=1\) was already covered
for \(r\ge3\) by the minority-exceptional theorem; the proof here also
covers the endpoint \((r,t)=(2,1)\).  The all-common case \(t=0\) is the
all-order common-beta theorem.

The new point is that one exceptional site and \(e\), rather than two
exceptional sites, can be made the unique marked pair.  This removes the
kernel parameter from every pivot.  At the last endpoint \(t=r+2\), the
possible Cauchy cancellation is killed by the invertible one-point
deletion transform \(J-I\).  No exceptional beta values are assumed
distinct.

## 2. Axial normal form and the forced pair

It is enough to treat the first family in (2); the other follows by
interchanging \(0\) and \(1\).  The standard normalization is

\[
 P_i=I\quad(i\text{ live}),\qquad
 P_c=P_d=D=\operatorname {diag}(1,1,0),\qquad
 H=\begin{pmatrix}0&1&1\\1&0&1\\1&1&0\end{pmatrix},\qquad \mu=1.
                                                                    \tag{3}
\]

The axial intersection permits an output change at \(e\) after which

\[
 P_e=\begin{pmatrix}1&0&0\\0&u&1\\0&0&0\end{pmatrix}             \tag{4}
\]

for an arbitrary \(u\in\mathbb C\).  Notice that \(u=0\) is allowed.
Write

\[
 E=\{y_1,\ldots,y_t\},\qquad
 A=(U\setminus E)\sqcup\{c,d\},\qquad
 n=|A|=2r+2-t.                                                     \tag{5}
\]

The exceptional blocks at \(z_0\) vanish structurally.  Fix one output
coordinate at \(z_0\), and write \(Z_{i,a}\) for the corresponding entry
in row \(a\) of the block at \(i\in A\sqcup\{e\}\).

Choose one exceptional label \(m\in E\).  Give \(m\) output colour \(2\),
contract \(e\) by its second output row

\[
                              p=(0,u,1),                            \tag{6}
\]

give every other site a binary output colour, and read source \(22\).
The only two rows with a nonzero source-\(2\) entry are \(m\) and \(e\).
Thus they are the unique marked pair, with marked coefficient \(2\).
The direct coordinate-factor term is zero because its \(22\) coefficient
is zero.  In particular, every response coefficient constructed this way
is independent of \(u\).

Put

\[
 \kappa={1\over2},\qquad
 \lambda_j={1\over1+\nu_j}\ne0.                                  \tag{7}
\]

All denominators \(\nu_j+1\) and \(\nu_j+\nu_k\) used below are nonzero
by the structural live--centre and live--live equations.

## 3. Cancellation-free range \(1\le t\le r+1\)

Give every site of \(E\setminus\{m\}\) colour \(0\).  For

\[
                  S\subset A,\qquad |S|=r+2-t,                    \tag{8}
\]

give \(S\) colour \(0\) and \(A\setminus S\) colour \(1\).  If the star
uses \(i\in S\), removal of \(m,e,i\) leaves \(r\) zero sites and \(r\)
one sites.  If the star lies in \(A\setminus S\), the two shore sizes are
\(r+1\) and \(r-1\), so its cofactor is zero.

Every exceptional zero must pair with a common-beta one.  All surviving
perfect matchings therefore have the same nonzero weight, and the exact
response is

\[
 C_m\sum_{i\in S}Z_{i,0}=0,
 \qquad
 C_m=2r!\left(\prod_{j\ne m}\lambda_j\right)
                    \kappa^{\,r-t+1}\ne0.                        \tag{9}
\]

Here the exponent is nonnegative exactly in the stated range.  Moreover,

\[
       1\le r+2-t<n,\qquad n-(r+2-t)=r.                            \tag{10}
\]

The fixed-cardinality subset incidence matrix has full column rank in
characteristic zero.  Hence \(Z_{i,0}=0\) for all \(i\in A\).  Swapping
the binary colours gives the identical coefficient \(C_m\) and proves

\[
                   Z_{i,0}=Z_{i,1}=0\qquad(i\in A).               \tag{11}
\]

This proof uses neither a generic beta value nor a nonzero value of the
axial parameter \(u\).

## 4. The endpoint \(t=r+2\)

Now \(n=r\), so (8) has size zero.  Fix distinct labels \(m,o\in E\),
put

\[
                         L=E\setminus\{m,o\},\qquad |L|=r,       \tag{12}
\]

give \(m\) colour \(2\), give \(L\) colour \(0\), give \(o\) colour
\(1\), and retain the row (6) at \(e\).  For a chosen \(i\in A\), give
\(i\) colour \(0\) and every site of \(A\setminus\{i\}\) colour \(1\).
Source \(22\) again forces the marked pair \(\{m,e\}\).  After removing
the target star, the cofactor is the permanent between the \(r\) rows
indexed by \(L\) and the columns indexed by
\(\{o\}\sqcup(A\setminus\{i\})\).  Consequently the response is the
singleton

\[
 C_{m,o}Z_{i,0}=0,                                                \tag{13}
\]

where

\[
 C_{m,o}
 =2(r-1)!\left(\prod_{\ell\in L}{1\over\nu_\ell+1}\right)
       \sum_{\ell\in L}{\nu_\ell+1\over\nu_\ell+\nu_o}.          \tag{14}
\]

Fix \(o\) and put \(N=E\setminus\{o\}\), so \(|N|=r+1\).  Define the
nonzero numbers

\[
                         h_\ell={\nu_\ell+1\over\nu_\ell+\nu_o}
                         \qquad(\ell\in N).                       \tag{15}
\]

If (14) vanished for every \(m\in N\), then

\[
                         \sum_{\ell\in N\setminus\{m\}}h_\ell=0
                         \qquad(m\in N).                          \tag{16}
\]

The coefficient matrix in (16) is \(J-I\), with eigenvalues \(r\) and
\(-1\).  It is invertible in characteristic zero, so every \(h_\ell\)
would vanish, contradicting (15).  Therefore some choice of \(m\) makes
\(C_{m,o}\ne0\).  Keep this choice for every \(i\in A\) in (13), and
then swap the binary colours.  This proves (11) also at \(t=r+2\).

The argument remains valid when beta values repeat: (14) is the original
permanent expansion, and (15)--(16) use only structurally nonzero
denominators.

## 5. The extra block and all third rows

First kill the full block at \(e\).  When \(t\ge2\), choose two
exceptional sites \(B\subset E\), give them colour \(2\), give the other
\(t-2\) exceptional sites colour \(0\), give \(r+2-t\) active sites
colour \(0\), and give the remaining \(r\) active sites colour \(1\).
Use source \(22\), and contract the output at \(e\) by an arbitrary
covector \(\eta\).  In the star-at-\(e\) term, \(B\) is the unique marked
pair and the remaining binary cofactor is a nonzero monomial.  Every
other active star contains a variable from (11), and every exceptional
star is structurally zero.  Hence

\[
                              \eta^{\mathsf T}q_{ez_0}=0           \tag{17}
\]

for every \(\eta\).  This count is valid through \(t=r+2\), where there
are no active zeros.  For \(t=1\), instead give the exceptional site
colour \(0\), give \(r-1\) active sites colour \(0\), give the other
\(r+2\) active sites colour \(1\), and use source \(11\).  The extra-star
coefficient is

\[
 2{r+2\choose2}r!\lambda_1\kappa^{\,r-1}\ne0,                    \tag{18}
\]

so (17) follows in that case as well.

It remains to kill \(Z_{i,2}\) for \(i\in A\).  In Section 3 choose an
\(S\) containing \(i\), replace the output row at \(i\) by row \(2\), and
keep source \(22\).  In Section 4 make the same replacement in the
singleton word (13).  The marked pair \(\{m,e\}\) gives respectively the
pivot \(C_m\) or \(C_{m,o}\).  If \(i\) is live, the two other possible
marked pairs contain \(i\); their star is then either \(e\), an
exceptional site, or an active site in a binary row.  Those terms vanish
by (11), (17), or structural zero.  If \(i\) is a type-\(10\) centre,
its third row in \(P_i\) is zero and no additional marked pair occurs.
Thus every \(Z_{i,2}\) vanishes.

Repeating Sections 3--5 for all three coordinates at \(z_0\) kills the
complete residual star.  The removed type-\(22\) ports are singular and
the zero--zero blocks vanish by beta parity, so \(z_0\) has no rank-three
neighbour.  This proves Theorem 1.1.

## 6. Exact audit and the next split

[verify_live_three_zero_extra_plane_axial.py](../computations/verify_live_three_zero_extra_plane_axial.py)
constructs the complete marked response, retaining the arbitrary axial
parameter.  It checks the subset rows, the endpoint singleton pivots, the
extra-star cleanup, and the triangular third-row cleanup.  It also checks
the \(J-I\) deletion identity through \(r=10\), including exact repeated-
beta stress cases.

The same unique-pair construction continues beyond \(t=r+2\).  If
\(s=t-r-1\ge2\), its isolated-star pivot is a permanent with \(s\)
exceptional columns and \(r-s\) repeated common columns.  The elementary
one-point deletion transform used in (16) is no longer injective on all
\(s\)-subset data.  Thus the present lemma closes exactly the axial
geometry left by the two-marked transverse theorem; higher split layers
require the corresponding constrained Cauchy-permanent argument rather
than an unsupported noncancellation claim.
