# Independent audit of the scalar common-origin countermodel

## Verdict and scope

The construction in
[`common-origin-factorization-rank-countermodel.md`](common-origin-factorization-rank-countermodel.md)
is correct.  A clean-room bit-mask expansion reproduces its six-cycle
divided powers, cofactor determinant, dual rows, and all nine response and
nine common-origin products.  No sign, edge-order, or factor-of-two error
was found.

The scope restriction is essential.  Here every local degree-one space is
the single line \(\mathbb Fz_u\), so the degree-six component is the single
line \(\mathbb Fz_{012345}\).  Thus the three diagonal responses all have
the same target.  Krenn's monochromatic tensor instead requires three
linearly independent words \(e_i^{\otimes6}\) when three colours are
present.  The construction therefore refutes only the proposed scalar
rank obstruction; it is not a graph or tensor counterexample to Krenn's
conjecture.

## 1. Divided powers in a different order

Write \(z_S=\prod_{u\in S}z_u\), with \(z_Sz_T=0\) when
\(S\cap T\ne\varnothing\).  I listed the edges in the reverse order

\[
 34,24,25,15,01,03
\]

with respective weights \(e,d,c,b,a,f\).  Directly choosing disjoint edge
subsets gives exactly two three-edge selections,

\[
 (34,25,01),\qquad (24,15,03),
\]

and hence

\[
 q^{[3]}=(ace+bdf)z_{012345}.                            \tag{1}
\]

For the cofactor pairing

\[
 C_{uv}=[z_{[6]\setminus\{u,v\}}]q^{[2]},
\]

use the reordered bipartition \((4,5,0\mid3,2,1)\), rather than the order
in the primary note.  Its off-diagonal block is

\[
 E=\begin{pmatrix}
 ac&bf&cf\\
 ad&ae&df\\
 bd&be&ce
 \end{pmatrix},
 \qquad
 C\sim\begin{pmatrix}0&E\\E^{\mathsf T}&0\end{pmatrix}. \tag{2}
\]

Expansion in this order yields

\[
 \det E=(ace-bdf)^2,
 \qquad
 \det C=-\det(E)^2=-(ace-bdf)^4.                        \tag{3}
\]

Modulo \(ace+bdf\), equation (3) becomes

\[
 \det C=-16(ace)^4.                                     \tag{4}
\]

This was checked polynomially, by taking a remainder modulo
\(ace+bdf\), without dividing by any edge parameter.  If all parameters
are nonzero and the characteristic is not two, (4) is nonzero.  The
smoothness assertion is also valid: for example
\(\partial(ace+bdf)/\partial a=ce\ne0\) on that torus.

## 2. The rational point and its cubic factors

At

\[
 (a,b,c,d,e,f)=(2,1,-1,1,1,2),
\]

the two terms in (1) are \(-2\) and \(2\).  An independent expansion gives

\[
\begin{aligned}
 q^{[2]}={}&2z_{0124}-2z_{0125}+2z_{0134}+2z_{0135}
             +2z_{0234}-2z_{0235}\\
            &+z_{1245}+z_{1345}-z_{2345}.               \tag{5}
\end{aligned}
\]

Taking the complement of each pair in (5) reproduces

\[
C=\begin{pmatrix}
0&-1&1&1&0&0\\
-1&0&0&0&-2&2\\
1&0&0&0&2&2\\
1&0&0&0&-2&2\\
0&-2&2&-2&0&0\\
0&2&2&2&0&0
\end{pmatrix},\qquad \det C=-256.                       \tag{6}
\]

The displayed linear rows in the primary note are

\[
\begin{aligned}
 &(p_0,p_1,p_2)=(z_0,z_1,z_2),\\
 &(s_0,s_1,s_2)=\left(\frac{-z_1+z_3}{2},
 -\frac{z_0}{2}+\frac{z_5}{4},
 \frac{z_4+z_5}{4}\right).
\end{aligned}                                           \tag{7}
\]

Multiplication by \(q\), performed before using the cofactor matrix,
gives the following six cubic factors:

\[
\begin{aligned}
A_0={}&z_{015}+z_{024}-z_{025}+z_{034},\\
A_1={}&2z_{013}+z_{124}-z_{125}+z_{134},\\
A_2={}&2z_{012}+2z_{023}+z_{125}+z_{234},\\[1mm]
B_0={}&\tfrac12(-z_{124}+z_{125}-z_{134}+z_{135}+z_{234}-z_{235}),\\
B_1={}&\tfrac12(-z_{024}+z_{025}-z_{034}+z_{035})
       +\tfrac14(z_{245}+z_{345}),\\
B_2={}&\tfrac12(z_{014}+z_{015}+z_{034}+z_{035})
       +\tfrac14(z_{145}+z_{345}).                      \tag{8}
\end{aligned}
\]

Complementary cubic supports in (8) give, entry by entry,

\[
 \bigl([z_{012345}]A_iB_j\bigr)_{i,j}=2I_3.             \tag{9}
\]

Since every nonzero product of two cubics on six sites is already a
multiple of \(z_{012345}\), (9) is equality of the complete products, not
only a selected coefficient.  A separate direct expansion of (5) and
(7) gives

\[
 \bigl(p_i s_j q^{[2]}\bigr)_{i,j}=I_3z_{012345}.       \tag{10}
\]

Finally, direct mask multiplication verifies
\(q^2=2q^{[2]}\).  Thus (9) and (10) agree through

\[
 (p_iq)(s_jq)=p_i s_j q^2=2p_i s_jq^{[2]}.              \tag{11}
\]

This independently discharges the possible ordering and divided-power
normalization failures.

## 3. Audit of the separate pure-target example

For distinct three-subsets \(T_i,T_j\subset[6]\), equality of cardinality
implies \(T_i\setminus T_j\ne\varnothing\).  Hence the supports of
\(A_i\) and \(B_j\) overlap when \(i\ne j\), while for \(i=j\) they are
complements.  This proves the second construction in the primary note.
The independent checker exhausts all \(20\cdot19\cdot18=6840\) ordered
choices of three distinct triples.

The standalone clean-room checker
[`audit_common_origin_factorization_rank_countermodel_independent.py`](../computations/audit_common_origin_factorization_rank_countermodel_independent.py)
uses a bit-mask algebra and a different cofactor ordering, explicitly
checks (5), every factor in (8), all eighteen products in (9)--(10), and
the polynomial remainder underlying (4).  It imports nothing from the
primary verifier.
