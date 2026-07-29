# The sparse eight-site quadratic has no pair-cap preimage

## 1. Result

Let \(q\) be the nine-cell quadratic from the unrestricted polarized
countermodel:

\[
\begin{aligned}
\operatorname{supp}(q)=\{&23_0,45_0,67_0,
01_1,36_1,57_1,\\
&02_2,14_2,56_2\}.
\end{aligned}                                             \tag{1}
\]

Although some quadratic \(z\) satisfies
\(zq^3/3!=\Delta_{8,3}\), no quadratic of the actual pair-cap form does:

\[
 \boxed{\quad (a q+4ps){q^3\over3!}\ne\Delta_{8,3}
 \quad\text{for every }a\in\mathbb C
 \text{ and all linear }p,s.\quad}                       \tag{2}
\]

This is stronger than the rank-three minor for the particular \(z\) in the
earlier note: it excludes every other preimage of the target for this fixed
\(q\).  It is still not a uniform pair-cap theorem, because \(q\) itself is
fixed to (1).

The exact checker is
[verify_polarized_eight_site_fixed_q_pair_cap_obstruction.py](../computations/verify_polarized_eight_site_fixed_q_pair_cap_obstruction.py).

## 2. Seven forced Gram entries

Put

\[
 Q={q^4\over4!},\qquad F={q^3\over3!},\qquad
 R_{(u,c),(v,d)}=p_{u,c}s_{v,d}+s_{u,c}p_{v,d}.          \tag{3}
\]

Since \(qF=4Q\), equation (2) would give

\[
                         aQ+psF={1\over4}\Delta_{8,3}.   \tag{4}
\]

Exact enumeration finds nineteen terms in \(F\).  Filling their two missing
sites by one entry of \(R\) gives 171 incidences on 165 words: 163 words have
one contributor, and two have four.  Moreover,

\[
 Q=e_{11000000}+e_{22212111}.                            \tag{5}
\]

The following seven words are singleton incidences and are absent from
\(Q\).  Write

\[
\begin{array}{lll}
 A=(0,0),&B=(1,0),&C=(2,1),\\
 D=(4,1),&E=(3,2),&F_0=(7,2),
\end{array}
\]

where a pair denotes a site-mode.  The three pure target words force

\[
 R_{A,B}=R_{C,D}=R_{E,F_0}={1\over4},                   \tag{6}
\]

while the four uniquely supported mixed words force

\[
 R_{A,F_0}=R_{B,F_0}=R_{A,C}=R_{C,F_0}=0.               \tag{7}
\]

No cancellation, genericity, or division by a source coefficient is used:
each assertion follows from one literal top-tensor coordinate of (4), and
the direct term \(aQ\) is zero on all seven coordinates.

## 3. Two-dimensional Gram contradiction

Associate to every site-mode \(X\) the vector

\[
                         x_X=(p_X,s_X)\in\mathbb C^2
\]

and equip \(\mathbb C^2\) with the nondegenerate symmetric form

\[
             \beta((r,t),(r',t'))=rt'+tr'.              \tag{8}
\]

Then \(R_{X,Y}=\beta(x_X,x_Y)\).  From
\(\beta(x_E,x_{F_0})=1/4\), the vector \(x_{F_0}\) is nonzero.  Equations
\(\beta(x_A,x_{F_0})=\beta(x_B,x_{F_0})=0\) put both \(x_A,x_B\) in the
one-dimensional space \(x_{F_0}^{\perp}\).  Hence they are proportional.
Their nonzero product \(\beta(x_A,x_B)=1/4\) says that their common line
\(L\) is nonisotropic.

Now \(\beta(x_C,x_D)=1/4\) makes \(x_C\ne0\), while
\(\beta(x_A,x_C)=0\) puts \(x_C\) in \(L^\perp\).  The vector \(x_{F_0}\)
also lies in \(L^\perp\).  Because \(L\) is nonisotropic and the ambient
form is nondegenerate, its one-dimensional orthogonal complement is
nonisotropic.  Two nonzero vectors on that line cannot be orthogonal.  This
contradicts the last equation \(\beta(x_C,x_{F_0})=0\).

This proves (2) over \(\mathbb C\).  The checker independently reconstructs
the nineteen \(q^{[3]}\) terms, all word multiplicities, (5), and the seven
selected coordinates.  As a redundant algebraic audit, Singular reduces
the seven bilinear equations over \(\mathbb Q\) to the unit ideal.

## 4. Consequence and boundary

The unrestricted polarized countermodel cannot be repaired into the
pair-cap variety merely by adding an element of
\(\ker(z\mapsto zq^3/3!)\).  Thus a search for an eight-site pair-cap
countermodel must change the internal quadratic \(q\), not only \(z\).

This remains a fixed-\(q\) theorem.  It neither excludes (2) for arbitrary
quadratics nor supplies the missing all-even descent.  The live global
targets remain a uniform pair-cap obstruction, compatibility among two or
more shared star rows, and overlap of the identities from distinct physical
pairs.
