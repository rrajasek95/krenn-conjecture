# The full five-cell internal-\(23\) plane locus cannot activate a fourth cut

## 1. Result and exact scope

Retain the eight fixed internal aggregate cells

\[
\begin{array}{c|c@{\qquad}c|c@{\qquad}c|c}
01&E_{00}&45&E_{00}&02&E_{11}\\
14&E_{11}&04&E_{22}&13&E_{22}\\
25&E_{00}&35&E_{10},
\end{array}
\]

and let the ninth block be an arbitrary complex point of

\[
 {\cal L}=
 \left\{
 \begin{pmatrix}
 x_{00}&x_{01}&x_{02}\\
 0&x_{11}&0\\
 0&x_{21}&0
 \end{pmatrix}:x_{cd}\in\mathbb C
 \right\}.                                                \tag{1}
\]

Allow all \(108\) entries of the two boundary stars \(i6,i7\),
\(0\leq i<6\), and all nine entries of \(A_{67}\) to be arbitrary
complex numbers.  No such system satisfies the complete quotient
identities on cuts \(2,3,4\) and either cut \(0\) or cut \(1\).  It
therefore cannot satisfy cuts \(2,3,4,5\) either.

This closes all \(32\) support orbits in the natural plane-normal locus,
including the \(28\) not covered by the earlier two-cell theorem.  It is
not a theorem for a general \(3\times3\) block outside (1), for two
simultaneously changed internal blocks, or for a global Krenn
realization.

The exact checker is
[verify_three_cut_internal_23_plane_support_fourth_cut_obstruction.py](../computations/verify_three_cut_internal_23_plane_support_fourth_cut_obstruction.py).
The support census and quotient discovery drivers are
[explore_three_cut_internal_23_plane_supports.py](../computations/explore_three_cut_internal_23_plane_supports.py)
and
[explore_three_cut_internal_23_universal_projection.py](../computations/explore_three_cut_internal_23_universal_projection.py).

## 2. Thirty-two complex support orbits

Put

\[
 L=\{x_{00},x_{01},x_{02},x_{11},x_{21}\}.
\]

The fixed-cell-preserving diagonal colour action has five free factors
\(r_0,c_0,c_2,r_1,r_2\), and the entries in \(L\) scale by

\[
\begin{array}{c|ccccc}
&x_{00}&x_{01}&x_{02}&x_{11}&x_{21}\\ \hline
\text{factor}&r_0c_0&r_0^2&r_0c_2&r_1r_0&r_2r_0.
\end{array}                                               \tag{2}
\]

Its exponent matrix is

\[
 E=\begin{pmatrix}
 1&1&0&0&0\\
 2&0&0&0&0\\
 1&0&1&0&0\\
 1&0&0&1&0\\
 1&0&0&0&1
 \end{pmatrix},
 \qquad |\det E|=2.                                      \tag{3}
\]

Thus the monomial map \((\mathbb C^\times)^5\to
(\mathbb C^\times)^5\) is surjective.  Every nonzero entry on a fixed
support can be normalized to one, while zero entries stay zero.

For completeness, one extension to the six internal sites is

\[
\begin{gathered}
 g_{2,0}=g_{3,1}=g_{4,0}=r_0,\qquad g_{5,0}=r_0^{-1},\\
 g_{3,0}=c_0,\quad g_{3,2}=c_2,\quad
 g_{2,1}=r_1,\quad g_{2,2}=r_2,\\
 g_{0,1}=r_1^{-1},\qquad g_{1,2}=c_2^{-1},
\end{gathered}                                            \tag{4}
\]

with every unlisted internal factor equal to one.  Direct multiplication
fixes all eight displayed internal cells.  Taking

\[
 g_{6,c}=1,\qquad
 g_{7,c}=\left(\prod_{i=0}^{5}g_{i,c}\right)^{-1}          \tag{5}
\]

fixes each coefficient of the diagonal target.  Boundary blocks remain
arbitrary under this invertible change.

Consequently the \(2^5=32\) zero/one representatives exhaust (1) over
\(\mathbb C\); this is not a finite-field or bounded-weight inference.
An exhaustive check of all site permutations and global colour
permutations preserving the eight fixed cells and the oriented locus
\(L\) finds only the identity.  There is no additional honest discrete
orbit collapse.

## 3. Cylinder normal form for every support

For

\[
 X=\sum_{(c,d)\in L}x_{cd}E_{cd},
\]

write

\[
 h_X=\sum_{(c,d)\in L}x_{cd}[00cd00],
 \qquad
 u_+=[121200]+[111110]+[220220].                          \tag{6}
\]

Literal endpoint-ordered matching expansion gives

\[
                         H_S(X)=h_X+u_+.                  \tag{7}
\]

The checker reconstructs every five-site insertion space and every
six-site cylinder over \(\mathbb Q\).  On all \(32\) representatives it
finds

\[
\begin{aligned}
 {\cal C}_2\cap{\cal C}_3\cap{\cal C}_4\cap{\cal C}_0
  &={\cal C}_2\cap{\cal C}_3\cap{\cal C}_4\cap{\cal C}_1\\
  &=\langle h_X,u_+\rangle,\\
 {\cal C}_2\cap{\cal C}_3\cap{\cal C}_4\cap{\cal C}_5
  &=\langle h_X+u_+\rangle,                              \tag{8}
\end{aligned}
\]

with the evident one-dimensional interpretation at \(X=0\).
Torus covariance promotes (8) from the representatives to every complex
point of (1).

In particular the cut-\(5\) normal is contained in the cut-\(0/1\)
normal.  It is enough to obstruct the latter: any solution modulo the
smaller line would also be a solution modulo the larger plane.

## 4. Literal shared-star system

For boundary colours \(a,b\), put

\[
 p^a_{i,c}=A_{i6}[c,a],\qquad
 q^b_{i,c}=A_{i7}[c,b],\qquad
 r_{ab}=A_{67}[a,b].
\]

If \(T_{ij}(X)=H_{S\setminus\{i,j\}}\), direct matching expansion is

\[
\begin{aligned}
 H_{ab}={}&r_{ab}H_S(X)+\beta_X(p^a,q^b),\\
 \beta_X(p,q)={}&
 \sum_{i<j}\sum_{c,d}
 \left(p_{i,c}q_{j,d}+p_{j,d}q_{i,c}\right)
 e_c^{(i)}e_d^{(j)}\otimes T_{ij}(X).                    \tag{9}
\end{aligned}
\]

Both endpoint orientations occur, and the same star variables are reused
in diagonal and ordered off-diagonal fibres.  Since \(H_S(X)\) belongs
to every normal in (8), all nine arbitrary entries \(r_{ab}\) are
absorbed exactly.  The residual equations are

\[
 \beta_X(p^a,q^b)-\delta_{ab}[a^6]\in N.                 \tag{10}
\]

## 5. Five disjoint variable-coordinate blocks

Changing \(A_{23}\) can change only the four deleted-pair cofactors

\[
                         01,\quad05,\quad15,\quad45.      \tag{11}
\]

For a cell \(e\in L\), let \(R_e\subset\{0,1,2\}^6\) be the set of
six-word coordinates reached by inserting all nine boundary endpoint
colours into the variable part of those four cofactors.  Exact
enumeration gives

\[
                |R_e|=35,\qquad R_e\cap R_f=\varnothing
                \quad(e\ne f).                           \tag{12}
\]

The union therefore has \(175\) coordinates.  This disjointness permits
a stronger reduction than testing the \(32\) orbits separately.

Fix a maximal support \(M\subseteq L\) and a mandatory retained subset
\(P\subseteq M\).  Define a coordinate quotient \(\pi_{M,P}\) by killing

\[
 \bigcup_{e\in M\setminus P}R_e
 \quad\text{and every coordinate of \(u_+\) not lying in }
 \bigcup_{e\in P}R_e.                                    \tag{13}
\]

For every support \(S\) with

\[
                         P\subseteq S\subseteq M,         \tag{14}
\]

all contributions from \(S\setminus P\) vanish under \(\pi_{M,P}\).
The surviving bilinear map depends only on the fixed eight cells and the
mandatory cells \(P\).  Likewise,

\[
 \pi_{M,P}\langle h_S,u_+\rangle
\]

is independent of \(S\).  Thus one unit-ideal calculation applies
uniformly to the entire interval (14).

The checker verifies these equalities term by term for every one of the
\(32\) representatives; no semicontinuity or generic-specialization
claim is being used.

## 6. Five quotient classes exhaust all supports

The following five classes partition the support lattice.  A displayed
colour pair means that only its two diagonal fibres and its two ordered
off-diagonal fibres are retained.  Any full solution of (10) restricts
to this necessary subsystem.

\[
\begin{array}{c|c|c|c|c|c|c|c}
\text{class}&M&P&\text{colours}&
|\ker\pi|&\text{words}&\text{atoms}&\dim\pi(N)\\ \hline
x_{00}=0&
\{01,02,11,21\}&\varnothing&0,2&141&53&54&0\\
x_{00}\ne0,\ x_{11}=x_{21}=0&
\{00,01,02\}&\varnothing&1,2&107&66&71&0\\
x_{00}x_{21}\ne0,\ x_{11}=0&
\{00,01,02,21\}&\{00,21\}&1,2&72&127&153&1\\
x_{00}x_{11}\ne0,\ x_{21}=0&
\{00,01,02,11\}&\{00,11\}&1,2&71&123&156&2\\
x_{00}x_{11}x_{21}\ne0&
L&\{00,11,21\}&1,2&71&149&192&2.
\end{array}                                               \tag{15}
\]

Here \(00,01,\ldots\) abbreviate the corresponding cells of \(L\).
The class sizes are respectively

\[
                         16,\quad4,\quad4,\quad4,\quad4.  \tag{16}
\]

They total \(32\), including the zero support and the four supports from
the earlier two-cell theorem.

## 7. Exact characteristic-zero unit certificates

For each row of (15), form the selected two-colour ideal over
\(\mathbb Q\) from

- both coefficient-one diagonal target fibres;
- both ordered off-diagonal zero fibres;
- the actual shared \(p\)- and \(q\)-variables;
- membership modulo the projected plane normal.

There are \(72\) selected star variables in each calculation.  The other
\(36\) of the full \(108\) variables are unrestricted and irrelevant:
a full solution would still restrict to the selected \(72\).

Singular computes the following exact standard bases:

\[
\begin{array}{c|c|c}
\text{class}&\text{generators}&\text{reduced standard basis}\\ \hline
x_{00}=0&216&[1]\\
x_{00}\ne0,\ x_{11}=x_{21}=0&268&[1]\\
x_{00}x_{21}\ne0,\ x_{11}=0&504&[1]\\
x_{00}x_{11}\ne0,\ x_{21}=0&484&[1]\\
x_{00}x_{11}x_{21}\ne0&588&[1].
\end{array}                                               \tag{17}
\]

Every calculation is performed directly in characteristic zero.  A unit
ideal over \(\mathbb Q\) stays unit after scalar extension to
\(\mathbb C\).  Since the projected systems are necessary consequences
of (10), (17) excludes every complex support orbit.

## 8. Consequence and next boundary

Allowing the full natural plane-normal support (1) does not provide the
missing fourth cut.  The obstruction survives arbitrary coefficients,
all shared-star cross terms, endpoint order, all off-diagonal fibres,
and arbitrary block \(67\).

The next internal escape must therefore leave this five-cell locus.  The
smallest concrete continuations are:

1. add a cell outside \({\cal L}\), where the cut-\(0/1\) cylinder normal
   must be recomputed rather than assumed to remain a plane;
2. perturb a second internal block, which changes the fixed pure
   cofactors used by the target atoms;
3. replace the fixed six-site interior entirely and seek a
   parameter-uniform invariant rather than another local support chart.

Only the first item is the immediate one-block continuation of this
theorem.
