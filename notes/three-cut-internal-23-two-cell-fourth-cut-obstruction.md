# A two-cell internal perturbation still cannot activate a fourth cut

## 1. Result and scope

Retain the eight fixed aggregate cells

\[
\begin{array}{c|c@{\qquad}c|c@{\qquad}c|c}
01&E_{00}&45&E_{00}&02&E_{11}\\
14&E_{11}&04&E_{22}&13&E_{22}\\
25&E_{00}&35&E_{10},
\end{array}
\]

and replace the ninth internal block by

\[
                         A_{23}=tE_{21}+sE_{00},
                         \qquad t,s\in\mathbb C.             \tag{1}
\]

Allow every entry on both boundary stars \(i6,i7\), \(0\leq i<6\), and
on \(67\) to be an arbitrary complex number.  No member of (1) satisfies
the complete quotient identities on cuts \(2,3,4\) and on any one of
\(0,1,5\), with all three unit diagonal target fibres retained.

This is an arbitrary-complex theorem for a genuine two-dimensional
internal-block family.  It strictly extends the fixed-interior Segre
obstruction, but it is not a theorem for an arbitrary \(3\times3\) block
at \(23\), and it is not a global Krenn obstruction.

The exact checker is
[verify_three_cut_internal_23_two_cell_family_fourth_cut_obstruction.py](../computations/verify_three_cut_internal_23_two_cell_family_fourth_cut_obstruction.py).
The equation generator and specialization explorer are
[explore_three_cut_internal_23_perturbation.py](../computations/explore_three_cut_internal_23_perturbation.py).

## 2. Parametric cylinder normal forms

Write

\[
\begin{aligned}
 v_{t,s}&=t[002100]+s[000000],\\
 u_+&=[121200]+[111110]+[220220].
\end{aligned}                                               \tag{2}
\]

Direct endpoint-ordered matching expansion gives

\[
                         H_S(t,s)=v_{t,s}+u_+.              \tag{3}
\]

Exact cylinder intersections give, when \((t,s)\ne(0,0)\),

\[
\begin{aligned}
 {\cal C}_2\cap{\cal C}_3\cap{\cal C}_4\cap{\cal C}_0
    &=\langle v_{t,s},u_+\rangle,\\
 {\cal C}_2\cap{\cal C}_3\cap{\cal C}_4\cap{\cal C}_1
    &=\langle v_{t,s},u_+\rangle,\\
 {\cal C}_2\cap{\cal C}_3\cap{\cal C}_4\cap{\cal C}_5
    &=\langle H_S(t,s)\rangle.                              \tag{4}
\end{aligned}
\]

At \((t,s)=(0,0)\), all three spaces in (4) are the common line
\(\langle u_+\rangle\).  Every possible fourth cut remains target-active.
In the exceptional \(t=0,\ s\ne0\) plane, the colour-zero target
\([0^6]\) itself lies in the residual plane; the other two target
directions remain active.  Thus this is the most permissive stratum for a
fourth cut, not a vacuous target-free quotient.

For arbitrary \(A_{23}=X\), let

\[
 h_X=\sum_{c,d}X_{cd}[00cd00].
\]

There is a useful structural reason for the two-plane in (4).  The
\(h_X\) slice belongs automatically to \({\cal C}_2\) and
\({\cal C}_3\).  On cut \(4\), the two literal insertion families

\[
 e_c^{(2)}\otimes H_{0135},\qquad
 e_d^{(3)}\otimes H_{0125}
\]

cover respectively column \(1\) and row \(0\) of \(X\), because

\[
 H_{0135}=[0010],\qquad H_{0125}=[0000].                  \tag{5}
\]

Consequently the linear matrix space

\[
 {\cal L}=
 \left\{
 \begin{pmatrix}
 *&*&*\\
 0&*&0\\
 0&*&0
 \end{pmatrix}
 \right\}                                                  \tag{6}
\]

is the natural plane-normal stratum.  Family (1) lies in \({\cal L}\).
Outside it, exact representative calculations collapse the cut-\(0/1\)
normal to the same line as cut \(5\); a uniform arbitrary-\(X\)
rank-stratification theorem is not claimed here.

## 3. The actual shared-star equations

For a boundary colour pair \((a,b)\), put

\[
 p^a_{i,c}=A_{i6}[c,a],\qquad
 q^b_{i,c}=A_{i7}[c,b],\qquad
 r_{ab}=A_{67}[a,b].
\]

If \(T_{ij}(t,s)=H_{S\setminus\{i,j\}}\), literal matching expansion is

\[
\begin{aligned}
 H_{ab}
  ={}&r_{ab}H_S(t,s)+\beta_{t,s}(p^a,q^b),\\
 \beta_{t,s}(p,q)
  ={}&\sum_{i<j}\sum_{c,d}
       \bigl(p_{i,c}q_{j,d}+p_{j,d}q_{i,c}\bigr)
       e_c^{(i)}e_d^{(j)}\otimes T_{ij}(t,s).              \tag{7}
\end{aligned}
\]

Both endpoint orientations occur and all cross products share the same
star variables.  No bilinear monomial is freed independently.

The \(r_{ab}H_S\) term already belongs to every normal in (4), so all nine
entries of \(A_{67}\) are absorbed exactly.  With \(N\) equal to the
appropriate plane or line, the residual problem is precisely

\[
 \beta_{t,s}(p^a,q^b)-\delta_{ab}[a^6]\in N,
                         \qquad 0\leq a,b<3.               \tag{8}
\]

Thus (8) retains three coefficient-one diagonal fibres and all six
ordered off-diagonal fibres.

Only four deleted-pair cofactors change when the second cell is added:

\[
\begin{array}{c|l}
01&t[2100]+s[0000]\\
05&t[1211]+s[1001]\\
15&t[2212]+s[2002]\\
45&[1212]+t[0021]+s[0000].
\end{array}                                                \tag{9}
\]

All eleven other cofactors are the fixed table from the original Segre
obstruction.  This gives \(126\) weighted atoms when \(t=s=0\), \(162\)
on either one-cell axis, and \(198\) when \(ts\ne0\).  After coordinate
collisions the corresponding reachable-word counts are \(100,126,152\).

## 4. Four torus strata exhaust all complex parameters

The equations need only be checked at

\[
                  (t,s)=(0,0),(1,0),(0,1),(1,1).          \tag{10}
\]

This is not a finite-scan inference.  It follows from an invertible
diagonal vertex-colour action.  For nonzero parameters choose
\(a\in\mathbb C^\times\) and set

\[
\begin{gathered}
 g_{5,0}=a,\qquad
 g_{4,0}=g_{2,0}=g_{3,1}=a^{-1},\\
 g_{2,2}=a/t\quad(t\ne0),\qquad
 g_{3,0}=a/s\quad(s\ne0),                                 \tag{11}
\end{gathered}
\]

with every other internal \(g_{i,c}=1\).  Multiplying an aggregate cell
\((c,d)\) on \(ij\) by \(g_{i,c}g_{j,d}\) leaves all eight fixed cells
equal to one.  It sends every nonzero coefficient in (1) to one and
preserves zero coefficients.

For each colour \(c\), take

\[
 g_{6,c}=1,\qquad
 g_{7,c}=\left(\prod_{i=0}^{5}g_{i,c}\right)^{-1}.         \tag{12}
\]

Then \(\prod_{i=0}^{7}g_{i,c}=1\), so the full diagonal target is fixed
coefficient by coefficient.  Boundary-star and \(67\) blocks remain
arbitrary under this invertible change.

For every even vertex set \(U\), matching expansion gives

\[
 H'_U=\left(\bigotimes_{i\in U}G_i\right)H_U.
\]

Hence every insertion space and every cylinder transforms covariantly.
Complete quotient feasibility is therefore identical along each of the
four zero/nonzero strata in (10).

## 5. Exact component certificates

For each representative and normal \(N\), let \(I_c(N)\) be the exact
rational ideal of the diagonal fibre in (8), and let \(X(N)\) contain
all ordered off-diagonal fibres.  Singular computes the minimal
components of the \(I_c\)'s and then adjoins \(X(N)\) to every component
tuple.

\[
\begin{array}{c|c|c|c|c|c}
(t,s)&N&\text{active colours}&
\text{equations/fibre}&\text{components}&\text{tuples}\\ \hline
(0,0)&\text{line}&0,1,2&99&9,12,9&972\\
(1,0)&\text{plane}&0,1,2&124&15,13,14&2730\\
(1,0)&\text{line}&0,1,2&125&9,11,9&891\\
(0,1)&\text{plane}&1,2&124&13,10&130\\
(0,1)&\text{line}&0,1,2&125&31,11,9&3069\\
(1,1)&\text{plane}&0,1,2&150&25,13,10&3250\\
(1,1)&\text{line}&0,1,2&151&10,11,9&990.
\end{array}                                                \tag{13}
\]

Every one of the \(12032\) displayed component tuples has unit standard
basis after the off-diagonal equations are adjoined.

For the \((0,1)\) plane, omitting colour zero in (13) is an exact
equivalence, not a relaxation.  Since \([0^6]\in N\), any colours-\(1,2\)
solution extends to all nine fibres by setting \(p^0=q^0=0\).
Conversely, a full solution restricts to the two retained colours.

Minimal-component exhaustion is complete over \(\mathbb C\): any complex
point of all diagonal ideals lies on one selected minimal component of
each, while the unit bases in (13) show that no selected tuple survives
the shared off-diagonal equations.  The certificates are over
\(\mathbb Q\), so they remain unit certificates after scalar extension.

## 6. Route consequence

The first internal escape from the fixed-interior theorem fails even when
the coefficient of \(E_{21}\) is allowed to vanish and the missing pure
zero internal direction is added with an arbitrary complex coefficient.
The obstruction is not merely that colour zero was absent: on the
\((0,1)\) plane that target is absorbed completely, yet the two remaining
diagonal fibres and their shared cross fibres already have unit ideal.

The smallest genuinely new continuation inside one block is now finite.
On the five-cell plane locus (6), write the row/column scaling factors as

\[
 r_0=g_{2,0}=g_{3,1},\quad c_0=g_{3,0},\quad c_2=g_{3,2},
 \quad r_1=g_{2,1},\quad r_2=g_{2,2}.
\]

The five allowed entries scale as

\[
\begin{array}{c|ccccc}
&X_{00}&X_{01}&X_{02}&X_{11}&X_{21}\\ \hline
\text{factor}&r_0c_0&r_0^2&r_0c_2&r_1r_0&r_2r_0.
\end{array}                                                \tag{14}
\]

The exponent matrix in (14) has determinant \(2\).  Over
\(\mathbb C\), every fixed zero/nonzero support is therefore one torus
orbit.  The complete plane-locus problem reduces exactly to the
\(2^5=32\) zero/one support representatives; the present theorem closes
the four representatives supported inside
\(\{X_{00},X_{21}\}\), leaving 28 exact component eliminations.  This is
an algebraic orbit reduction, not a bounded-weight scan.

The other structurally stronger continuation is to perturb a second
internal block, changing the pure cofactors
\(H_{0135},H_{0125},H_{0145}\) used by all three formal diagonal atoms.

The second option is structurally stronger: changing only \(A_{23}\)
does not alter \(H_{0145}=[0000]\), \(H_{0124}=[1111]\), or
\(H_{0134}=[2222]\), so the same three formal target atoms and the same
shared-star cross mechanism remain in force.
