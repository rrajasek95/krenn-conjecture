# Two marked exceptional sites close every transverse extra plane

## 1. Outcome

Continue from
[live-three-zero-extra-plane-minority-exceptional.md](live-three-zero-extra-plane-minority-exceptional.md).
There are \(2r\) live sites, exactly \(t\) of them have exceptional beta
value, and the sole extra singular site satisfies

\[
                  \operatorname {im}P_e=\langle e_0,e_1\rangle .
                                                                    \tag{1}
\]

Normalize the third output row of \(P_e\) to zero and put
\(R=\operatorname {row}P_e\).

**Theorem 1.1 (two-marked transverse injectivity).**  Suppose

\[
 r\ge2,\qquad 2\le t\le\min(2r,r+2),\qquad
 R\cap\langle e_0,e_1\rangle
       \text{ contains }p=(p_0,p_1,0)\text{ with }p_0p_1\ne0.     \tag{2}
\]

Then the complete residual star at the shared zero \(z_0\) vanishes.
Consequently \(z_0\) has no rank-three neighbour.

Condition (2) includes the coordinate plane
\(R=\langle e_0,e_1\rangle\) and every noncoordinate plane whose
intersection line with the binary source plane is not a coordinate axis.
Thus, in the range of the theorem, only the two axial families

\[
 R\cap\langle e_0,e_1\rangle=\mathbb C e_0
 \quad\text{or}\quad
 R\cap\langle e_0,e_1\rangle=\mathbb C e_1                  \tag{3}
\]

remain outside this argument.

## 2. The forced marked pair

Use the normalization of the preceding notes:

\[
 P_i=I\quad(i\text{ live}),\qquad
 P_c=P_d=D=\operatorname {diag}(1,1,0),\qquad
 H=\begin{pmatrix}0&1&1\\1&0&1\\1&1&0\end{pmatrix},\qquad\mu=1.
                                                                    \tag{4}
\]

Let \(E\) be the exceptional set and choose two labels
\(B=\{y_1,y_2\}\subset E\).  Give precisely these two sites output colour
\(2\) and read source \(22\).  Contract \(e\) to the vector \(p\) in
(2).  Since \(p_2=0\), the marked pair is forced to be \(B\).

Put

\[
 A=(U\setminus E)\sqcup\{c,d\},\qquad |A|=n=2r+2-t,
                                                                    \tag{5}
\]

\[
 \kappa={1\over2},\qquad
 \lambda_j={1\over1+\nu_j},\qquad
 C_{r,t,B}
   =2r!\left(\prod_{j\in E\setminus B}\lambda_j\right)
              \kappa^{\,r-t+2}\ne0.                              \tag{6}
\]

The two marked exceptional beta values do not occur in (6), because those
sites are removed before the binary cofactor is formed.  Every unmarked
exceptional site lies on one binary shore and contributes its single
factor \(\lambda_j\).  Hence (6) is a nonzero monomial even when beta
values repeat.

## 3. Binary subset equations

Give all sites of \(E\setminus B\) colour \(0\).  For

\[
                         S\subset A,\qquad |S|=r+3-t,              \tag{7}
\]

give \(S\) colour \(0\) and \(A\setminus S\) colour \(1\).  If the star
uses \(i\in S\), then after removing \(B\) and \(i\), the extra site must
pair with a zero.  Whether that zero is common or exceptional, every
complete matching has the same weight in (6).  Every other active star,
and the star at \(e\), leaves unbalanced binary shores.  The exact response
is therefore

\[
                    C_{r,t,B}p_1\sum_{i\in S}Z_{i,0}=0.           \tag{8}
\]

The subset size in (7) is nonempty because \(t\le r+2\), and it is proper
because \(r\ge2\).  Fixed-size
subset incidence and \(p_1\ne0\) give

\[
                              Z_{i,0}=0\qquad(i\in A).             \tag{9}
\]

Colour swapping, with every unmarked exceptional site now colour \(1\),
gives

\[
                    C_{r,t,B}p_0\sum_{i\in S}Z_{i,1}=0,
 \qquad                        Z_{i,1}=0\quad(i\in A).             \tag{10}
\]

## 4. Remaining star rows

Contract \(e\) by an arbitrary output covector.  Keep \(B\) as the marked
pair, give the unmarked exceptional sites colour \(0\), give \(r+2-t\)
active sites colour \(0\), and give the remaining \(r\) active sites
colour \(1\).  After removing \(B\) and the star at \(e\), the two binary
shores both have size \(r\).  All off-star terms vanish by (9)--(10) or
by the structural zero of an exceptional star.  Thus

\[
                         C_{r,t,B}\eta^{\mathsf T}q_{ez_0}=0      \tag{11}
\]

for every \(\eta\), killing the full extra block.

Give \(c\) its zero third row, keep the unmarked exceptional sites at
colour \(0\), give \(r+2-t\) of the other active sites colour \(0\), and
give the remaining \(r-1\) active sites colour \(1\).  The marked pair is
still \(B\), \(e\) is forced to a zero, and the singleton coefficient is

\[
                              C_{r,t,B}p_1Z_{c,2}=0.               \tag{12}
\]

This kills row \(2\) at both \(c\) and \(d\).

Finally choose any common-beta live site \(i\), give it colour \(2\), and
use the same binary counts on \(A\setminus\{i\}\).  For the star at \(i\),
the marked pair is again exactly \(B\), so its coefficient is
\(C_{r,t,B}p_1\).  Every off-star variable has already vanished.
Therefore \(Z_{i,2}=0\).  Exceptional live stars were zero from the start.

Repeat for the three coordinates at \(z_0\).  The removed type-\(22\)
ports are singular and the zero--zero blocks vanish by beta parity, so
the full rank-three star at \(z_0\) is empty.  This proves Theorem 1.1.

## 5. Exact audit

[verify_live_three_zero_extra_plane_two_marked_transverse.py](../computations/verify_live_three_zero_extra_plane_two_marked_transverse.py)
constructs the complete marked response and verifies (8)--(12) symbolically
at \((r,t)=(2,2),(3,3)\).  It also audits the endpoint counts
\((2,4),(3,5)\), where the subset in (7) has size one.  The proof above is
the uniform factorial calculation.
