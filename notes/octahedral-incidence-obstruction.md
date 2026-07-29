# The octahedral perfect-matching tensor has subrank at most two

This note tests the first perfect-matching incidence support that escapes the
cubic-vertex lemma.  Let

\[
 O=K_6\setminus\{01,23,45\}.
\]

It is four-regular and has eight perfect matchings.  Even though a general
tight/free tensor with only five or nine support terms can have ordinary
subrank three and monomial subrank two, the endpoint-consistency pattern of
`O` prevents this: its perfect-matching incidence tensor has ordinary
subrank at most two.

The proof works over `C` (more generally, in characteristic different from
`2` and `3`) and allows arbitrary local images of every edge occurrence.
In particular, it is not a positivity or monomial argument.

## 1. Incidence tensor and a locally independent triple

For each vertex `v`, let `W_v` have a basis vector `f_{v,e}` for every edge
`e` of `O` incident with `v`.  Its perfect-matching incidence tensor is

\[
 \mathcal T_O=\sum_{M\in\operatorname{PM}(O)}
                   \bigotimes_{v=0}^5 f_{v,e_v(M)}.
\tag{1}
\]

Suppose, toward a contradiction, that local maps
`L_v:W_v -> K^3` send (1) to a tensor in the `GL(3)^6` orbit of
`Delta_(6,3)`.  The three-copy alternating invariant of that image is
nonzero.  Expanding the invariant in the eight matching terms shows that
there are three perfect matchings `M_0,M_1,M_2` such that, at every vertex,

\[
 L_v f_{v,e_v(M_0)},\quad L_v f_{v,e_v(M_1)},\quad
 L_v f_{v,e_v(M_2)}
\tag{2}
\]

are linearly independent.  Consequently the three matchings are
edge-disjoint.  Apply an invertible map at every output site so that the
three vectors in (2) become `e_0,e_1,e_2`, respectively.  This operation
does not preserve the literal coordinates of `Delta_(6,3)`, but it does
preserve every flattening rank.  The transformed target has rank three
across every grouping of the six sites.

Every three edge-disjoint perfect matchings of `O` extend to a
one-factorization of `O`; the unused edges form a fourth perfect matching.
Up to an automorphism and a permutation of `M_0,M_1,M_2`, take

\[
\begin{aligned}
 M_0&=02|14|35,\\
 M_1&=03|15|24,\\
 M_2&=04|13|25,\\
 M_3&=05|12|34.
\end{aligned}
\tag{3}
\]

The other four perfect matchings are

\[
 02|15|34,\quad 03|14|25,\quad 04|12|35,
 \quad 05|13|24.
\tag{4}
\]

## 2. Grouped form of all eight matching terms

Group the output sites as

\[
 X=V_0\otimes V_5,\qquad
 Y=V_1\otimes V_2,\qquad
 Z=V_3\otimes V_4,
\tag{5}
\]

and write `E_ab=e_a tensor e_b` in each grouped space.  Let

\[
 x=L_0(f_{0,05})\otimes L_5(f_{5,05})\in X,
\]

and define `y in Y` and `z in Z` analogously from the edges `12` and
`34`.  These vectors may be arbitrary decomposable tensors, including
zero.

Using (3)--(4), the transformed image of (1) is exactly

\[
\begin{aligned}
 T={}&\sum_{a=0}^2 E_{aa}^X\otimes E_{aa}^Y\otimes E_{aa}^Z\\
 &+E_{12}^X\otimes E_{02}^Y\otimes E_{10}^Z\\
 &+E_{01}^X\otimes E_{10}^Y\otimes z\\
 &+E_{20}^X\otimes y\otimes E_{02}^Z\\
 &+x\otimes E_{21}^Y\otimes E_{21}^Z
   +x\otimes y\otimes z.
\end{aligned}
\tag{6}
\]

The first line consists of `M_0,M_1,M_2`; the second line is the matching
`03|14|25`, which uses only their edges.  The last four terms are the
remaining matchings and use, respectively, the edges `34`, `12`, `05`, and
all three of them.

## 3. A rank-four flattening

Flatten (6) across `X | (Y tensor Z)`.  First omit the two terms containing
`x`, and call the resulting matrix `B`.  Its first four nonzero `X`-rows
have the following four distinct coordinate vectors on the right:

\[
 E_{00}^Y E_{00}^Z,\quad E_{11}^Y E_{11}^Z,\quad
 E_{22}^Y E_{22}^Z,\quad E_{02}^Y E_{10}^Z.
\tag{7}
\]

They are linearly independent.  If `y` is nonzero, the `E_20^X` row is
`y tensor E_02^Z`; its `Z` coordinate does not occur in (7), so it is
independent of (7).  If `z` is nonzero, the `E_01^X` row is
`E_10^Y tensor z`; its `Y` coordinate does not occur in (7), so it too is
independent of (7).  Therefore

\[
 \operatorname{rank} B\geq5
 \quad\hbox{if at least one of }y,z\hbox{ is nonzero}.
\tag{8}
\]

The omitted pair of terms combines into the single rank-one matrix

\[
 x\otimes\bigl(E_{21}^Y\otimes E_{21}^Z+y\otimes z\bigr).
\tag{9}
\]

A rank-one update lowers matrix rank by at most one, so (8) gives

\[
 \operatorname{rank}T_{X|YZ}\geq4.
\tag{10}
\]

It remains to consider `y=z=0`.  Then `B` has rank four by (7), while the
right factor in (9) is the coordinate vector
`E_21^Y tensor E_21^Z`, which is outside the row space in (7).  Adding a
rank-one matrix whose right factor is outside the old row space cannot
lower rank.  Hence (10) holds in this case as well.

The tensor in the `GL(3)^6` orbit of `Delta_(6,3)` has rank exactly three
across the grouping (5), contradicting (10).  Thus

\[
                         Q(\mathcal T_O)\leq2.
\tag{11}
\]

## 4. Relevance to symbol cloning

The interpolation counterexample in
`notes/tight-free-lagrange-counterexample.md` relies on a dense column
whose image has three nonzero output coordinates.  Cloning such a symbol
at two endpoints replaces that column by a decomposable matrix
`u tensor v`; it cannot reproduce the required diagonal matrix of rank
greater than one.  The octahedral graph is the smallest degree-four support
where extra perfect matchings might conceivably repair this defect.  Formula
(6) shows exactly why they do not: rectangle completion supplies one fixed
fourth anchor, while all remaining freedom enters one flattening through
only a rank-one update after two visibly independent rows.  The resulting
rank-four obstruction is the incidence-specific information absent from
tightness and freeness.
