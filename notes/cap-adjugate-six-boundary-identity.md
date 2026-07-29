# The cap-adjugate identity: exact alternating cancellation of all pair defects

## 1. Outcome

For an arbitrary eight-site ternary aggregate edge family, delete a pair
`p,q` and retain six boundary sites `U`.  The nine matrix-unit caps at
`p,q` give nine denominator-cleared boundary edge families `B_ij`.  Although
their individual six-site hafnians have nonlinear repeated-star defects,
the determinant of the `3 by 3` matrix `(B_ij)` cancels every such defect:

\[
 \boxed{
 \det(B_{ij})=2\sum_{i,j=0}^2
       \operatorname {Cof}_{ij}(A_{pq})
       \bigl((e_i^*\otimes e_j^*)\mathbin{\lrcorner}H_8(A)\bigr).}
                                                                  \tag{1}
\]

The determinant and products on the left are taken in the commutative
square-free boundary algebra.  Equation (1) is universal: it assumes no
target equation, nonvanishing, rank, symmetry, or genericity.

Consequently, if `H_8(A)=Delta_(8,3)`, then

\[
 \boxed{
 \det(B_{ij})=2\sum_{i=0}^2
       \operatorname {Cof}_{ii}(A_{pq})e_i^{\otimes6}.} \tag{2}
\]

Thus every pair whose three principal cofactors are nonzero gives an exact
nondegenerate diagonal six-boundary tensor.  This is the first reconstruction
which uses the omitted common-edge compatibility and removes the full
nonlinear cap contamination, rather than merely testing whether it vanishes.

There remains one precise gap to an ordinary six-site descent: the left side
of (2) is an alternating sum of six mixed products of edge families, not one
hafnian `H_6(C)`.  In the language of `global-cap-span-descent.md`, (2)
places a non-decomposable alternating cubic in the mixed kernel; one still
has to force a decomposable cube on the Veronese variety.  If that conversion
can be made, every pair with three nonzero principal cofactors is closed;
otherwise every pair must enter an explicit cofactor-degenerate branch.

The exact audit is
`computations/verify_cap_adjugate_identity.py`.

## 2. Pair slices in the square-free algebra

Let

\[
                         B=\{p,q\}\mathbin{\dot\cup}U,
                         \qquad |U|=6.                    \tag{3}
\]

Work in the square-free site algebra `R_U` and put

\[
 x=\sum_{u<v\in U}A_{uv},\qquad
 H={x^3\over3!},\qquad Q={x^2\over2!}.                  \tag{4}
\]

Orient the two deleted stars toward `p,q`.  For colors `i,j`, define their
row elements

\[
 \ell_i=\sum_{u\in U}(e_i^*\otimes\operatorname{id})A_{p\mid u},
 \qquad
 m_j=\sum_{u\in U}(e_j^*\otimes\operatorname{id})A_{q\mid u},             \tag{5}
\]

and write `a_ij=A_(p|q)(i,j)`.  The response to the matrix-unit cap is

\[
                         r_{ij}=\ell_i m_j.               \tag{6}
\]

Its component on a boundary pair `uv` is exactly the sum of the two ways
to send `p,q` to `u,v`, with endpoint order retained.  Hence the full
eight-site slice and the denominator-cleared boundary pair family are

\[
 D_{ij}:=(e_i^*\otimes e_j^*)\mathbin{\lrcorner}H_8(A)
          =a_{ij}H+r_{ij}Q,
 \qquad
 B_{ij}=a_{ij}x+r_{ij}.                                  \tag{7}
\]

These are identities of tensors, including every parallel source and every
complex cancellation.

## 3. The adjugate cancellation

Let `a=(a_ij)`, let `C_ij=Cof_ij(a)`, and regard
`ell=(ell_i)` and `m=(m_j)` as a column and row over `R_U`.  Equation (7)
packages the nine edge families as

\[
                         (B_{ij})=xa+\ell m^{\mathsf T}.  \tag{8}
\]

The rank-one determinant lemma is a polynomial identity over every
commutative ring, so it remains valid in the nilpotent square-free algebra:

\[
 \det(xa+\ell m^{\mathsf T})
   =x^3\det a+x^2\sum_{i,j}C_{ij}\ell_i m_j.             \tag{9}
\]

No inverse of `a` is used.  Substitute `x^3=6H`, `x^2=2Q`, and (7):

\[
\begin{aligned}
 \det(B_{ij})
 &=6(\det a)H+2\sum_{i,j}C_{ij}(D_{ij}-a_{ij}H)\\
 &=2\sum_{i,j}C_{ij}D_{ij}
   +2\left(3\det a-\sum_{i,j}C_{ij}a_{ij}\right)H.
                                                               \tag{10}
\end{aligned}
\]

Euler's identity for the cubic determinant is

\[
                         \sum_{i,j}C_{ij}a_{ij}=3\det a. \tag{11}
\]

The last term in (10) therefore vanishes, proving (1).  Under the ternary
GHZ equation, `D_ij=delta_ij e_i^(tensor 6)`, which gives (2). `QED`

The elementary common-edge relations responsible for (9) can also be
seen directly:

\[
 r_{ij}r_{k\ell}=r_{i\ell}r_{kj},                        \tag{12}
\]

and, for every permutation `sigma in S_3`,

\[
 r_{0,sigma(0)}r_{1,sigma(1)}r_{2,sigma(2)}
       =\ell_0\ell_1\ell_2m_0m_1m_2.                    \tag{13}
\]

Thus all six alternating-cycle products are literally the same boundary
tensor.  Their signed sum is zero.  Equations (12)--(13) are precisely the
nonlinear shared-star information absent from a formal assignment of cap
outputs.

## 4. Relation to ordinary six-site hafnians

Expanding the determinant gives

\[
 \det(B_{ij})=\sum_{\sigma\in S_3}\operatorname {sgn}(\sigma)
          B_{0,\sigma(0)}B_{1,\sigma(1)}B_{2,\sigma(2)}. \tag{14}
\]

Each product is a genuine trilinear polarization of the six-site hafnian.
For arbitrary pair families `Y_1,Y_2,Y_3`,

\[
 Y_1Y_2Y_3
 ={1\over24}\bigl((Y_1+Y_2+Y_3)^3
 -(Y_1+Y_2-Y_3)^3-(Y_1-Y_2+Y_3)^3
 -(-Y_1+Y_2+Y_3)^3\bigr).                               \tag{15}
\]

Since `H_6(Y)=Y^3/3!`, equation (2) puts the normalized ternary target in
the linear span of at most twenty-four ordinary six-site hafnians whenever
the three principal cofactors are nonzero.  What (15) does not supply is a
single member of that span whose mixed coefficients vanish.  The binary
cross-pair pencil shows that such a decomposable member can occur; the
ternary prism shows that it need not follow from a generic polarization
argument.

## 5. The six formal correction rows detected exactly

The formal cap-family countermodel in `global-cap-span-descent.md` can be
made to fail (1) in exactly the six rows which distinguish block GHZ from
global GHZ.  Use the two disjoint canonical `K_4` sources on
`{p,x_0,x_1,x_2}` and `{q,y_0,y_1,y_2}`, and take the otherwise inactive
direct block

\[
 a=\begin{pmatrix}1&2&3\\4&5&7\\8&11&13\end{pmatrix},
 \qquad
 (C_{ij})=
 \begin{pmatrix}-12&4&4\\7&-11&5\\-1&5&-3\end{pmatrix}.             \tag{16}
\]

All nine cofactors are nonzero.  The actual eight-site tensor is

\[
 H_8^{\rm act}=\sum_{i,j}e_i^{\otimes\{p,x_0,x_1,x_2\}}
                         e_j^{\otimes\{q,y_0,y_1,y_2\}}, \tag{17}
\]

independently of `a`, because using `pq` strands two odd triangles.  The
genuine lower cofactors therefore obey

\[
 \det(B_{ij})=2\sum_{i,j}C_{ij}
     e_i^{\otimes\{x_0,x_1,x_2\}}
     e_j^{\otimes\{y_0,y_1,y_2\}}.                       \tag{18}
\]

If one formally replaces (17) by `Delta_(8,3)` while retaining those lower
cofactors, the right side of (1) would instead be

\[
                         2\sum_iC_{ii}e_i^{\otimes6}.    \tag{19}
\]

The discrepancy is exactly

\[
 2\sum_{i\ne j}C_{ij}
     e_i^{\otimes\{x_0,x_1,x_2\}}
     e_j^{\otimes\{y_0,y_1,y_2\}},                      \tag{20}
\]

with all six coefficients nonzero.  Thus (1) detects, in one alternating
identity, every cross-row correction which the formal model changed.  Any
genuine shared-edge repair must modify the lower cofactor determinant by
exactly (20); it cannot cancel the six top rows independently.

For a diagonal cap `K=diag(z_0,z_1,z_2)` the same lower family remains the
root-covered prism

\[
 H_6(A^K)=s^2\sum_i z_i e_i^{\otimes6}
       +z_0z_1z_2e_{012012},
 \qquad s=z_0+5z_1+13z_2.                               \tag{21}
\]

So the adjugate identity is strictly stronger than all individual cap-top
contractions: it couples the six repaired global rows to the alternating
cubic of the common lower edge factors.
