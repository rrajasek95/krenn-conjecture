# Independent audit: fourth-cut intersections for the fixed interior

## 1. Verdict and scope

The fixed-interior theorem in
[the primary note](three-cut-fourth-cut-fixed-interior-intersection.md)
passes an independent reconstruction over \(\mathbb Q\).  Direct primal
intersection of the six insertion cylinders gives

\[
\begin{aligned}
\dim({\cal C}_2\cap{\cal C}_3\cap{\cal C}_4)&=8,\\
\dim({\cal C}_2\cap{\cal C}_3\cap{\cal C}_4\cap{\cal C}_0)&=2,\\
\dim({\cal C}_2\cap{\cal C}_3\cap{\cal C}_4\cap{\cal C}_1)&=2,\\
\dim({\cal C}_2\cap{\cal C}_3\cap{\cal C}_4\cap{\cal C}_5)&=1,
                                                               \tag{A1}
\end{aligned}
\]

and intersecting all six still gives dimension one.  Every displayed
basis in the primary note is exact.

The result is an arbitrary-complex linear theorem for the nine fixed
interior cells.  It does not settle factorized realizability when the
two boundary stars vary.  The three-atom construction is a valid
counterexample only to the relaxation in which cross monomials are
independent.

## 2. Interior tensor and five-site defects

Endpoint-ordered expansion of the nine internal cells leaves exactly
four supported matchings:

\[
                 H_S=[002100]+[121200]+[111110]+[220220].
                                                               \tag{A2}
\]

Write

\[
 u_0=[002100],\qquad
 u_+=[121200]+[111110]+[220220].                            \tag{A3}
\]

For each \(z\), the audit independently formed all five-site insertion
columns

\[
 {\cal S}_{U_z}=\sum_{u\in U_z}
          V_u\otimes H_{U_z\setminus\{u\}}
\]

from the three perfect matchings of each four-site cofactor.  Exact
column reduction gives

\[
\begin{array}{c|c|c}
z&{\cal G}_{U_z}\cap{\cal S}_{U_z}&\dim W_{U_z}\\ \hline
0&0&3\\
1&0&3\\
2&\langle0^{U_2},2^{U_2}\rangle&1\\
3&\langle0^{U_3},1^{U_3}\rangle&1\\
4&\langle0^{U_4}\rangle&2\\
5&\langle1^{U_5},2^{U_5}\rangle&1.
\end{array}                                                \tag{A4}
\]

The defect was computed as the rank increase after adjoining all three
constant words, not inferred merely by checking them one at a time.
Thus possible linear combinations inside
\({\cal G}_{U_z}\cap{\cal S}_{U_z}\) are included.

## 3. Direct primal intersections and bases

The primary proof stacks bases of the dual annihilators.  As an
independent method, the audit lifted a basis of every
\({\cal S}_{U_z}\) directly into the \(3^6\)-coordinate primal space,
forming a basis of

\[
                         {\cal C}_z=V_z\otimes{\cal S}_{U_z}.
\]

For two current subspaces with column matrices \(A,B\), it solved

\[
                          Ax-By=0                            \tag{A5}
\]

over \(\mathbb Q\), mapped the kernel through \(A\), and iterated this
operation across the desired cuts.  This yields the dimensions in
(A1), independently of the primary annihilator implementation.

The resulting eight-space is exactly

\[
\begin{aligned}
{\cal C}_2\cap{\cal C}_3\cap{\cal C}_4
=\operatorname {span}\{&
[000000],[000100],[000110],[000120],\\
&[000200],[001100],u_0,u_+\}.                              \tag{A6}
\end{aligned}
\]

Adjoining cut zero or one gives, in either case,

\[
             \operatorname {span}\{u_0,u_+\}.              \tag{A7}
\]

Adjoining cut five instead gives

\[
             \operatorname {span}\{u_0+u_+\}
                         =\operatorname {span}\{H_S\}.       \tag{A8}
\]

The all-six intersection is the same line.  The complementary dual
ranks are consequently

\[
                         721,\ 727,\ 727,\ 728,\ 728,
\]

matching the primary rank table.

There is also an atomwise inclusion check for the surviving line.
In each perfect matching of \(S\), site \(z\) is paired to one
\(u\in U_z\); deleting that edge leaves a term of
\(H_{U_z\setminus\{u\}}\).  Hence every matching atom of \(H_S\) lies
in \({\cal C}_z\), for every \(z\).  The rank calculation proves that no
second direction survives cut five.

## 4. Boundary slicing and the fourth-cut normal forms

For an eight-site residual, slice at the ordered boundary sites:

\[
                   D=\sum_{a,b}D_{ab}\otimes
                     e_a^{(6)}e_b^{(7)}.                    \tag{A9}
\]

The complete quotient condition on \(z\) is

\[
 D\in V_{(z,6,7)}\otimes{\cal S}_{U_z}.
\]

Taking a boundary coordinate of this inclusion gives
\(D_{ab}\in{\cal C}_z\).  Therefore four complete cuts
\(2,3,4,5\) and (A8) force

\[
                         D=H_S\otimes R_{67}                \tag{A10}
\]

for an arbitrary two-site tensor \(R_{67}\).  Cuts \(2,3,4,0\), or
\(2,3,4,1\), and (A7) similarly force

\[
                         D=u_0\otimes R_0+u_+\otimes R_+.    \tag{A11}
\]

These are linear consequences of the quotient conditions.  They do not
assert that arbitrary \(R_{67}\), \(R_0\), or \(R_+\) comes from two
shared endpoint stars.

## 5. Formal three-atom relaxation

The three relevant internal cofactors are exactly

\[
 H_{0145}=e_{0000},\qquad
 H_{0124}=e_{1111},\qquad
 H_{0134}=e_{2222}.                                       \tag{A12}
\]

If the bilinear product of one site-\(6\) star cell and one site-\(7\)
star cell is treated as an independent variable for each pair, choose

\[
\begin{array}{c|c}
(i,j)&\text{colours at }i,6,j,7\\ \hline
(2,3)&0,0,0,0\\
(3,5)&1,1,1,1\\
(2,5)&2,2,2,2.
\end{array}
\]

Multiplication by the three cofactors in (A12) gives respectively

\[
                         e_0^{\otimes8},\quad
                         e_1^{\otimes8},\quad
                         e_2^{\otimes8}.                    \tag{A13}
\]

Their formal sum is \(\Delta_{8,3}\), so \(D=0\) and (A10) holds with
\(R_{67}=0\).

Actual star cells do not make these three bilinear products independent.
Each selected cell multiplies every compatible cell on the opposite
star, generating shared cross terms.  Thus (A13) is not an
endpoint-factorized decorated-source family and cannot refute a Segre
obstruction.  Conversely, any argument that proves impossibility only
after freeing all cross monomials is invalid for exactly this reason.

## 6. Independent executable audit

[verify_three_cut_fourth_cut_fixed_interior_intersection_independent_audit.py](../computations/verify_three_cut_fourth_cut_fixed_interior_intersection_independent_audit.py)
imports none of the primary checker.  It reconstructs every internal
matching and defect, intersects the primal cylinders by (A5), verifies
both inclusions for all explicit bases, and rebuilds each of the three
formal atoms.
