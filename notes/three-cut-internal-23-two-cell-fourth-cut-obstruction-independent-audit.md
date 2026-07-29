# Independent audit: the two-cell internal-$23$ perturbation obstruction

## 1. Verdict and exact scope

The theorem in
[the primary note](three-cut-internal-23-two-cell-fourth-cut-obstruction.md)
passes an independent endpoint-ordered reconstruction.  For

\[
 A_{23}=tE_{21}+sE_{00},\qquad t,s\in\mathbb C,
\]

with the other eight internal aggregate cells fixed, no arbitrary-complex
choice of the two boundary stars and block $67$ satisfies the complete
quotient identities on cuts $2,3,4$ together with cut $0$, $1$, or
$5$.  All diagonal targets and all ordered off-diagonal fibres were kept.

No primary project module was imported.  A fresh checker recomputed the
matching tensors, insertion cylinders, torus covariance, bilinear ideals,
minimal components, and all $12032$ component tuples.  No algebraic or
scope error was found.

This remains a controlled-family theorem.  It does **not** treat an
arbitrary $3\times3$ block at $23$, a perturbation of another internal
block, or a global Krenn realization.

## 2. Independent endpoint and cylinder reconstruction

Every aggregate cell was re-entered with literal endpoint order.  Direct
perfect-matching enumeration on $S=\{0,1,2,3,4,5\}$ gives

\[
 H_S(t,s)=t[002100]+s[000000]
          +[121200]+[111110]+[220220].                   \tag{A1}
\]

Deleting each pair and enumerating the remaining four sites gives the full
parametric cofactor table

\[
\begin{array}{c|l@{\qquad}c|l@{\qquad}c|l}
01&t[2100]+s[0000]&02&[1110]+[2200]&03&[1010]\\
04&[2020]&05&t[1211]+s[1001]&12&[2120]\\
13&[1100]+[2020]&14&[1110]&15&t[2212]+s[2002]\\
23&[0000]&24&[0010]&25&[2222]\\
34&[0000]&35&[1111]&45&[1212]+t[0021]+s[0000].
\end{array}                                               \tag{A2}
\]

Thus the four cofactors $01,05,15,45$, and only those four, change with
the new cell.

For a five-site set $U$, the audit independently formed

\[
 K_U=\operatorname{span}\left\{
 e_c^{(i)}\otimes H_{U\setminus\{i\}}:
 i\in U, 0\le c<3
 \right\}                                                \tag{A3}
\]

and lifted $K_{S\setminus\{z\}}$ to its six-site cylinder.  Exact
rational annihilator intersections, rather than imported rank tables,
then yielded

\[
\begin{aligned}
 C_2\cap C_3\cap C_4\cap C_0
  &=C_2\cap C_3\cap C_4\cap C_1
    =\langle t[002100]+s[000000],u_+\rangle,\\
 C_2\cap C_3\cap C_4\cap C_5
  &=\langle H_S(t,s)\rangle                              \tag{A4}
\end{aligned}
\]

whenever $(t,s)\ne(0,0)$, where

\[
 u_+=[121200]+[111110]+[220220].                          \tag{A5}
\]

At the origin all three intersections are the line
$\langle u_+\rangle$.  Each possible fourth cut has a nonzero pure-target
quotient defect.  In the exceptional $(0,1)$ plane normal,
$[0^6]$ belongs to the normal while $[1^6]$ and $[2^6]$ do not.

## 3. Literal shared-star expansion

The audit next assigned distinct rational values to every entry of both
boundary stars and to all nine entries of $A_{67}$, enumerated all
eight-site perfect matchings, and compared every one of the nine boundary
slices to a separately assembled cofactor formula.  The equality obtained
was

\[
\begin{aligned}
 H_{ab}={}&r_{ab}H_S(t,s)\\
 &+\sum_{i<j}\sum_{c,d}
 \left(p^a_{i,c}q^b_{j,d}+p^a_{j,d}q^b_{i,c}\right)
 e_c^{(i)}e_d^{(j)}\otimes H_{S\setminus\{i,j\}}.         \tag{A6}
\end{aligned}
\]

This check independently confirms both endpoint orientations and the reuse
of the same star variables in diagonal and cross fibres.  Since $H_S$
belongs to every normal in (A4), the $r_{ab}H_S$ term is absorbed for all
nine independently variable entries of block $67$.

Inserting all nine colour pairs in every deleted pair gives

\[
\begin{array}{c|c|c|c}
(t,s)&\text{weighted atoms}&\text{reachable words}&
\text{word multiplicities}\\ \hline
(0,0)&126&100&78,18,4\\
(1,0),(0,1)&162&126&96,25,4,1\\
(1,1)&198&152&114,32,4,2.
\end{array}                                               \tag{A7}
\]

The entries in the final column correspond respectively to multiplicities
$1,2,3,4$.

## 4. Why four parameter representatives suffice

The diagonal vertex-colour action was checked separately on each of the
four support strata.  When a coefficient is present, let

\[
 g_{5,0}=a,\quad g_{4,0}=g_{2,0}=g_{3,1}=a^{-1},\quad
 g_{2,2}=a/t,\quad g_{3,0}=a/s,                           \tag{A8}
\]

omitting the last two assignments when the corresponding coefficient is
zero.  Direct multiplication confirms that all eight fixed cells retain
coefficient one, while every present cell of $A_{23}$ is normalized to
one.  Taking

\[
 g_{6,c}=1,\qquad
 g_{7,c}=\left(\prod_{i=0}^5g_{i,c}\right)^{-1}           \tag{A9}
\]

fixes every coefficient of the diagonal target tensor.  All factors are
nonzero, so arbitrary boundary blocks remain arbitrary under the change of
coordinates.

For every even internal subset, the checker also verified term by term

\[
 H'_U=\left(\bigotimes_{i\in U}G_i\right)H_U.             \tag{A10}
\]

Consequently insertion spaces, their lifted cylinders, targets, and full
quotient feasibility transform covariantly.  The four rational
representatives

\[
                         (0,0),(1,0),(0,1),(1,1)           \tag{A11}
\]

therefore exhaust all complex $(t,s)$.

As a supplemental check on the continuation stated in the primary note,
the five allowed cells of the plane-normal locus have exponent matrix

\[
\begin{pmatrix}
1&1&0&0&0\\2&0&0&0&0\\1&0&1&0&0\\
1&0&0&1&0\\1&0&0&0&1
\end{pmatrix},qquad |\det|=2.                            \tag{A12}
\]

The audit explicitly extended these five row/column factors to a
stabilizer of all eight fixed cells and then to one fixing the diagonal
target.  Over $\mathbb C$, the finite-index monomial map is surjective on
the torus, so every fixed support in that five-cell locus is a single
orbit.

## 5. The $(0,1)$ two-colour reduction is an equivalence

For $(t,s)=(0,1)$ and the plane normal,

\[
 N=\langle[000000],u_+\rangle.                            \tag{A13}
\]

Any full solution restricts to the four fibres indexed by colours
${1,2}$.  Conversely, given a solution of those four fibres, set
$p^0=q^0=0$.  Every ordered fibre involving colour zero then has zero
bilinear term.  Its only possible nonzero target is $[0^6]$ on fibre
$(0,0)$, and (A13) absorbs that target exactly.  Hence the extension
satisfies all nine fibres.  The checker verifies this by applying every
annihilator row of $N$ to $[0^6]$.

Thus omitting colour zero in this one component calculation neither relaxes
nor strengthens feasibility.

## 6. Independent characteristic-zero certificates

For each retained diagonal colour $c$, let $I_c(N)$ denote its exact
bilinear fibre ideal, including the coefficient-one target.  Let $X(N)$
contain every ordered off-diagonal fibre among the retained colours.  A
freshly generated Singular program over $\mathbb Q$, with a different
variable naming and ordering from the primary checker, obtained

\[
\begin{array}{c|c|c|c|c|c}
(t,s)&N&\text{colours}&\text{equations/fibre}&
\text{minimal components}&\text{tuples}\\ \hline
(0,0)&\text{line}&0,1,2&99&9,12,9&972\\
(1,0)&\text{plane}&0,1,2&124&15,13,14&2730\\
(1,0)&\text{line}&0,1,2&125&9,11,9&891\\
(0,1)&\text{plane}&1,2&124&13,10&130\\
(0,1)&\text{line}&0,1,2&125&31,11,9&3069\\
(1,1)&\text{plane}&0,1,2&150&25,13,10&3250\\
(1,1)&\text{line}&0,1,2&151&10,11,9&990.
\end{array}                                               \tag{A14}
\]

For each tuple of minimal components, the audit formed their sum with
$X(N)$, computed an exact standard basis, and reduced $1$.  All

\[
 972+2730+891+130+3069+3250+990=12032                  \tag{A15}
\]

tuples reduced $1$ to zero; no nonunit tuple survived.  Minimal-component
exhaustion covers every complex point of the diagonal ideals, and a unit
certificate over $\mathbb Q$ remains a unit certificate over
$\mathbb C$.

The plane certificate applies identically to cuts $0$ and $1$ by
(A4); the line certificate applies to cut $5$.  This establishes the
claimed obstruction on all three candidate fourth cuts.

## 7. Executable audit

[verify_three_cut_internal_23_two_cell_fourth_cut_obstruction_independent_audit.py](../computations/verify_three_cut_internal_23_two_cell_fourth_cut_obstruction_independent_audit.py)
imports none of the primary checker or its helper modules.  It rebuilds
(A1)--(A14), directly checks a numerical instance of the literal
eight-site identity (A6) on all boundary slices, and verifies every unit
certificate counted in (A15).

The primary checker
[verify_three_cut_internal_23_two_cell_family_fourth_cut_obstruction.py](../computations/verify_three_cut_internal_23_two_cell_family_fourth_cut_obstruction.py)
uses shared earlier graph helpers, but its asserted cylinder spaces,
component counts, and scope all agree with the independent reconstruction.
