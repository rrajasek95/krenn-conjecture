# Exact fourth-cut intersections for the repaired six-site interior

## 1. Result and scope

Fix the nine aggregate cells internal to
\(S=\{0,1,2,3,4,5\}\) from the repaired three-cut construction:

\[
\begin{array}{c|c@{\qquad}c|c@{\qquad}c|c}
01&E_{00}&45&E_{00}&02&E_{11}\\
14&E_{11}&04&E_{22}&13&E_{22}\\
25&E_{00}&35&E_{10}&23&E_{21}.
\end{array}                                               \tag{1}
\]

For \(z\in S\), put \(U_z=S\setminus\{z\}\) and define the internal
five-site insertion cylinder

\[
 \mathcal C_z
   :=V_z\otimes\mathcal S_{U_z}\subseteq V_S,
 \qquad
 \mathcal S_{U_z}
   =\sum_{u\in U_z}V_u\otimes H_{U_z\setminus\{u\}}.     \tag{2}
\]

Exact rational row reduction gives

\[
\begin{aligned}
 \dim(\mathcal C_2\cap\mathcal C_3\cap\mathcal C_4)&=8,\\
 \dim(\mathcal C_2\cap\mathcal C_3\cap\mathcal C_4
                         \cap\mathcal C_0)&=2,\\
 \dim(\mathcal C_2\cap\mathcal C_3\cap\mathcal C_4
                         \cap\mathcal C_1)&=2,\\
 \dim(\mathcal C_2\cap\mathcal C_3\cap\mathcal C_4
                         \cap\mathcal C_5)&=1.            \tag{3}
\end{aligned}
\]

The last line is unchanged if all six cylinders are intersected.  More
importantly, every space in (3) has an explicit basis below.  This is an
arbitrary-complex linear theorem for the fixed interior, not a bounded
weight search.

For an eight-site tensor \(H_B\), let
\(D=H_B-\Delta_{8,3}\), and slice it by the boundary word
\((a,b)\) at sites \((6,7)\):

\[
                         D=\sum_{a,b}D_{ab}\otimes e_a^{(6)}e_b^{(7)}.
                                                                    \tag{4}
\]

If the complete quotient identities hold on a set of cuts \(Z\), then

\[
                         D_{ab}\in\bigcap_{z\in Z}\mathcal C_z
                         \qquad\text{for every }a,b.       \tag{5}
\]

Thus (3) is the exact formal residual left by a fourth cut.  It does not by
itself decide endpoint-factor realizability when both boundary stars are
free.  The formal relaxation with independent bilinear monomials is
feasible, whereas actual star cells share cross products.  That distinction
is made explicit in Section 5.

The standalone exact audit is
[`verify_three_cut_fourth_cut_fixed_interior_intersection.py`](../computations/verify_three_cut_fourth_cut_fixed_interior_intersection.py).

## 2. The internal tensor

Write \([w]\) for the coordinate tensor with six-site word \(w\).  Direct
perfect-matching expansion of (1) gives

\[
 H_S=[002100]+[121200]+[111110]+[220220].                 \tag{6}
\]

Put

\[
 u_0=[002100],\qquad
 u_+= [121200]+[111110]+[220220],                         \tag{7}
\]

so that \(H_S=u_0+u_+\).

The constant-word intersections and target-defect dimensions of the six
five-sets are

\[
\begin{array}{c|c|c}
z&\mathcal G_{U_z}\cap\mathcal S_{U_z}&\dim W_{U_z}\\ \hline
0&0&3\\
1&0&3\\
2&\langle0^{U_2},2^{U_2}\rangle&1\\
3&\langle0^{U_3},1^{U_3}\rangle&1\\
4&\langle0^{U_4}\rangle&2\\
5&\langle1^{U_5},2^{U_5}\rangle&1.
\end{array}                                               \tag{8}
\]

In particular, every candidate fourth cut in (3) is target-active before
the quotient equations are imposed.

## 3. Explicit intersection bases

For the original three cuts, an exact basis is

\[
\begin{aligned}
 \mathcal C_2\cap\mathcal C_3\cap\mathcal C_4
  =\operatorname{span}\{&[000000],[000100],[000110],[000120],\\
                         &[000200],[001100],u_0,u_+\}.    \tag{9}
\end{aligned}
\]

Either fourth cut \(z=0\) or \(z=1\) removes the first six coordinate
directions:

\[
 \mathcal C_2\cap\mathcal C_3\cap\mathcal C_4\cap\mathcal C_z
                 =\operatorname{span}\{u_0,u_+\}
                 \qquad(z=0,1).                          \tag{10}
\]

The fourth cut \(z=5\) also ties the two remaining coefficients:

\[
 \mathcal C_2\cap\mathcal C_3\cap\mathcal C_4\cap\mathcal C_5
                 =\operatorname{span}\{H_S\}.            \tag{11}
\]

Finally,

\[
                         \bigcap_{z=0}^5\mathcal C_z
                           =\operatorname{span}\{H_S\}.   \tag{12}
\]

Consequently, four complete cuts \(2,3,4,5\) force the particularly rigid
normal form

\[
                  \boxed{D=H_S\otimes R_{67}}             \tag{13}
\]

for one arbitrary two-site boundary tensor \(R_{67}\).  Four complete cuts
\(2,3,4,0\) or \(2,3,4,1\) instead force

\[
                 D=u_0\otimes R_0+u_+\otimes R_+          \tag{14}
\]

for two boundary tensors \(R_0,R_+\).

## 4. Exact rank proof

Let \(K_{U_z}=\mathcal S_{U_z}^{\perp}\).  Algebraic annihilator duality
gives

\[
                  \mathcal C_z^{\perp}=V_z^*\otimes K_{U_z}.         \tag{15}
\]

Therefore

\[
 \left(\bigcap_{z\in Z}\mathcal C_z\right)^{\perp}
                   =\sum_{z\in Z}V_z^*\otimes K_{U_z}.   \tag{16}
\]

The checker independently enumerates every four-site internal matching,
constructs the insertion columns in each \(3^5\)-dimensional word basis,
constructs exact bases of the annihilators, lifts them into the
\(3^6=729\)-dimensional six-site dual, and row-reduces over \(\mathbb Q\).
The dual ranks are

\[
\begin{array}{c|c|c}
Z&\operatorname{rank}\sum_{z\in Z}V_z^*\otimes K_{U_z}
  &\dim\bigcap_{z\in Z}\mathcal C_z\\ \hline
\{2,3,4\}&721&8\\
\{2,3,4,0\}&727&2\\
\{2,3,4,1\}&727&2\\
\{2,3,4,5\}&728&1\\
\{0,1,2,3,4,5\}&728&1.
\end{array}                                               \tag{17}
\]

It then verifies both inclusions between each computed nullspace and the
explicit spans (9)--(12).  Thus the dimensions in (17) and the displayed
basis vectors together certify all equalities, without numerical rank or a
genericity assumption.

There is also a conceptual reason that \(H_S\) survives every cylinder.
In each internal perfect matching, site \(z\) is paired with one exposed
site \(u\in U_z\), and the remaining four sites contribute the cofactor
\(H_{U_z\setminus\{u\}}\).  Hence
\(H_S\in V_z\otimes\mathcal S_{U_z}\) atom by atom for every \(z\).
The exact rank calculation proves that cut \(5\) leaves no other common
direction.

## 5. Formal bilinear feasibility is not a star realization

With both boundary stars free, a matching which pairs site \(6\) to
\(i\in S\) and site \(7\) to \(j\in S\) contributes a bilinear product of
two star cells times \(H_{S\setminus\{i,j\}}\).  If each such product is
incorrectly treated as an independent variable, three atoms already give
the target:

\[
\begin{array}{c|c|c}
(i,j)&\text{star endpoint colours}&\text{full atom}\\ \hline
(2,3)&(0,0)\text{ on both stars}&e_0^{\otimes8}\\
(3,5)&(1,1)\text{ on both stars}&e_1^{\otimes8}\\
(2,5)&(2,2)\text{ on both stars}&e_2^{\otimes8}.
\end{array}                                               \tag{18}
\]

The relevant cofactors are respectively
\(H_{0145}=e_{0000}\), \(H_{0124}=e_{1111}\), and
\(H_{0134}=e_{2222}\).  Their formal sum is exactly \(\Delta_{8,3}\), so
it satisfies every cut and (13) with \(R_{67}=0\).

Actual endpoint blocks cannot activate only those three products.  A star
cell used in one diagonal atom also multiplies every compatible cell on the
opposite star, producing shared cross terms.  The exact two-star model in
[the cumulative-repair countermodel](three-cut-two-boundary-star-cumulative-repair-countermodel.md)
is one such factorized example: its cross term transports the debt but no
fourth cut becomes complete.

Thus (11)--(14) narrow the live question to a genuine Segre/factorization
problem.  They are not a proof that the factorized problem has no solution.

## 6. Route consequence

For this fixed interior, a fourth-cut attack no longer needs to manipulate
hundreds of quotient rows.  It must decide whether the two shared boundary
stars can realize (13), or one of the two-plane forms (14), while retaining
the exact diagonal target coefficients.  Any claimed obstruction proved
only after freeing the bilinear monomials independently is invalid, because
(18) is an exact formal counterexample to that relaxation.

That residual shared-star problem is now resolved exactly in
[the two-star Segre obstruction](three-cut-two-boundary-star-fourth-cut-segre-obstruction.md).
The line normal has \(9\cdot11\cdot9=891\) diagonal component triples and
the plane normal has \(15\cdot13\cdot14=2730\); after the six off-diagonal
factorization equations are imposed, every component triple has unit ideal
over \(\mathbb Q\), hence no complex point.  Thus arbitrary changes on both
boundary stars cannot create a fourth cut for this fixed interior.

The
[independent intersection audit](three-cut-fourth-cut-fixed-interior-intersection-independent-audit.md)
reconstructs the fixed interior and obtains (9)--(12) by direct primal
cylinder intersections rather than the primary annihilator calculation.
