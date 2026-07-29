# Independent audit: the full five-cell internal-\(23\) plane locus

## 1. Verdict and scope

The theorem in
[the primary note](three-cut-internal-23-plane-support-fourth-cut-obstruction.md)
passes an independent exact reconstruction.  Retain the eight
endpoint-ordered internal cells

\[
\begin{array}{c|c@{\qquad}c|c@{\qquad}c|c}
01&E_{00}&45&E_{00}&02&E_{11}\\
14&E_{11}&04&E_{22}&13&E_{22}\\
25&E_{00}&35&E_{10},
\end{array}
\]

and allow

\[
A_{23}\in
{\cal L}=\langle E_{00},E_{01},E_{02},E_{11},E_{21}\rangle_{\mathbb C}.
\tag{A1}
\]

For every such \(A_{23}\), arbitrary complex entries in both boundary
stars and arbitrary \(A_{67}\) cannot satisfy the complete quotient
identities for cuts \(2,3,4,0\), nor for cuts \(2,3,4,1\).  The same is
therefore impossible for cuts \(2,3,4,5\).

The independent checker imports no primary project module:
[verify_three_cut_internal_23_plane_support_fourth_cut_obstruction_independent_audit.py](../computations/verify_three_cut_internal_23_plane_support_fourth_cut_obstruction_independent_audit.py).
It freshly enumerates matchings, cylinders, boundary-star terms,
coordinate quotients, and the five exact-\(\mathbb Q\) ideals.  No
algebraic, endpoint-order, or scope error was found.

This remains a local controlled-family theorem.  It does not treat a cell
outside (A1), a second perturbed internal block, an arbitrary six-site
interior, or a global Krenn realization.

## 2. Complex support orbits and cylinders

Let the five displayed coefficients be
\((x_{00},x_{01},x_{02},x_{11},x_{21})\).  The independent audit
reconstructs a fixed-cell stabilizing colour torus whose five free
parameters act with factors

\[
(r_0c_0,\ r_0^2,\ r_0c_2,\ r_0r_1,\ r_0r_2).
\tag{A2}
\]

The exponent determinant has absolute value \(2\).  Surjectivity over
\(\mathbb C\) is also explicit: for any five desired nonzero factors,
choose a square root \(r_0\) of the second factor and then solve linearly
for \(c_0,c_2,r_1,r_2\).  Thus every fixed zero/nonzero support is one
torus orbit and has a zero/one representative.  The \(32\) representatives
exhaust all of (A1), including coefficients of arbitrary magnitude and
phase.

The torus extension was checked cell by cell on all eight fixed sources.
Taking

\[
g_{6,c}=1,\qquad
g_{7,c}=\left(\prod_{i=0}^{5}g_{i,c}\right)^{-1}
\tag{A3}
\]

fixes every diagonal target coefficient.  All boundary and \(67\) entries
are merely multiplied by nonzero scalars, so their allowed parameter
spaces remain arbitrary.  As an ancillary census, exhaustive enumeration
of site permutations and global colour permutations preserving both the
fixed cells and the oriented locus found only the identity.  This discrete
stabilizer statement is not needed for exhaustiveness; the torus reduction
already supplies it.

For a support \(S\), direct matching enumeration gives

\[
H_S=h_S+u_+,\qquad
h_S=\sum_{(c,d)\in S}[00cd00],
\tag{A4}
\]

where

\[
u_+=[121200]+[111110]+[220220].
\tag{A5}
\]

The audit independently forms every five-site insertion space and lifts
its annihilator into the six-site word space.  For each of the \(32\)
supports, exact rational ranks and containment checks give

\[
\begin{aligned}
{\cal C}_2\cap{\cal C}_3\cap{\cal C}_4\cap{\cal C}_0
&={\cal C}_2\cap{\cal C}_3\cap{\cal C}_4\cap{\cal C}_1
 =\langle h_S,u_+\rangle,\\
{\cal C}_2\cap{\cal C}_3\cap{\cal C}_4\cap{\cal C}_5
&=\langle h_S+u_+\rangle .
\end{aligned}
\tag{A6}
\]

At \(S=\varnothing\), the first plane has its evident one-dimensional
specialization.  These are \(96\) separately reconstructed four-cut
intersections.  In particular, the cut-\(5\) line lies in the cut-\(0\)
and cut-\(1\) plane, so an obstruction modulo the plane also obstructs
the line.

## 3. Literal boundary fibres and the direct block

The independent audit assigns distinct rational values to all \(108\)
entries of the two boundary stars and to all nine entries of \(A_{67}\).
It then enumerates the full eight-site matching tensor and checks all nine
boundary-colour slices against the separately assembled identity

\[
\begin{aligned}
H_{ab}={}&r_{ab}H_S\\
&+\sum_{i<j}\sum_{c,d}
\left(p^a_{i,c}q^b_{j,d}+p^a_{j,d}q^b_{i,c}\right)
e_c^{(i)}e_d^{(j)}\otimes H_{S\setminus\{i,j\}}.
\end{aligned}
\tag{A7}
\]

This checks literal endpoint orientation, both ways of attaching sites
\(6\) and \(7\), and reuse of the same star variables in every diagonal
and ordered off-diagonal fibre.  Since \(H_S\) lies in both normals in
(A6), every independently arbitrary \(r_{ab}H_S\) is absorbed.

The full residual condition is therefore

\[
\beta_S(p^a,q^b)-\delta_{ab}[a^6]\in N
\qquad(0\leq a,b<3).
\tag{A8}
\]

All three diagonal fibres in (A8) have coefficient-one targets; all six
ordered off-diagonal fibres have target zero.  The checker verifies that
all three pure target words occur in the unprojected cofactor system for
every support.

## 4. Five disjoint coordinate blocks and support classes

Only deleted-pair cofactors \(01,05,15,45\) depend on \(A_{23}\).  For
each allowed cell \(e\), the audit independently inserts all nine endpoint
colour pairs into the variable part of these cofactors.  The resulting
coordinate set \(R_e\) has size \(35\), and

\[
R_e\cap R_f=\varnothing\quad(e\ne f),\qquad
\left|\bigcup_eR_e\right|=175.
\tag{A9}
\]

For a maximal support \(M\) and a mandatory subset \(P\), project away
the blocks \(R_e\) for \(e\in M\setminus P\), together with the
coordinates of \(u_+\) outside the retained \(R_e\), \(e\in P\).
For every \(P\subseteq S\subseteq M\), the checker compares terms rather
than dimensions and confirms that both the projected bilinear map and the
projected normal are identical.  This is an exact coordinate relaxation,
not a specialization or semicontinuity argument.

The five tested intervals are

\[
\begin{array}{c|c|c|c|c|c|c}
\text{class}&|{\cal S}|&|\ker\pi|&
\text{words}&\text{atoms}&\dim\pi(N)&\text{colours}\\ \hline
x_{00}=0&16&141&53&54&0&0,2\\
x_{00}\ne0,\ x_{11}=x_{21}=0&4&107&66&71&0&1,2\\
x_{00}x_{21}\ne0,\ x_{11}=0&4&72&127&153&1&1,2\\
x_{00}x_{11}\ne0,\ x_{21}=0&4&71&123&156&2&1,2\\
x_{00}x_{11}x_{21}\ne0&4&71&149&192&2&1,2.
\end{array}
\tag{A10}
\]

Their sizes \(16+4+4+4+4\) partition all \(32\) masks exactly.  Every
mandatory bit is present in every member of its class, every member lies
under its stated maximal mask, and all termwise quotient equalities were
checked.

## 5. Exact unit ideals and the inference

For the selected pair of colours in each row of (A10), retain both
coefficient-one diagonal fibres and both ordered off-diagonal zero fibres.
This gives \(72\) genuinely shared star variables.  The omitted third
colour is a relaxation: any solution of the full nine-fibre system (A8)
must restrict to these four fibres.  Therefore inconsistency of the
selected system is sufficient; no extension claim for the omitted colour
is required.

A freshly generated Singular program, using a different variable order
from the primary checker, computes over characteristic zero:

\[
\begin{array}{c|c|c}
\text{class}&\text{generators}&\text{reduced standard basis}\\ \hline
x_{00}=0&216&[1]\\
x_{00}\ne0,\ x_{11}=x_{21}=0&268&[1]\\
x_{00}x_{21}\ne0,\ x_{11}=0&504&[1]\\
x_{00}x_{11}\ne0,\ x_{21}=0&484&[1]\\
x_{00}x_{11}x_{21}\ne0&588&[1].
\end{array}
\tag{A11}
\]

Each ideal is generated by necessary projected consequences of (A8).
Since it contains \(1\) over \(\mathbb Q\), it has no common zero over
\(\mathbb C\).  Hence each support class is impossible modulo the
cut-\(0/1\) plane.  The containment of the cut-\(5\) line in that plane
then excludes cut \(5\) as well.

## 6. What cannot be weakened silently

The inference depends on the complete selected four-fibre packet: the two
diagonal targets, both ordered off-diagonal fibres, and shared star
variables.  Treating bilinear monomials as independent, discarding an
ordered cross fibre, or replacing the unit calculation by a dimension
count would be a different and weaker system.

Likewise, freeing one of the eight fixed internal cells, adding a sixth
cell to \(A_{23}\), or enlarging the cylinder normal changes the cofactors
or membership equations.  The five certificates in (A11) cannot be
carried across such a change without recomputation.  Quotienting more
coordinates would also weaken the necessary subsystem and would require a
new unit certificate.  These are scope boundaries, not conclusions about
the unrestricted conjecture.
