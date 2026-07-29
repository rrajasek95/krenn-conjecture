# The representable even-delta-matroid transversal route

## Outcome

The proposed delta-matroid statement is exactly the characteristic-two
transverse-Pfaffian obstruction after a feasible-set twist; it is not a
formal consequence of strong symmetric exchange.  An exact source-ideal
certificate proves the statement at six sites over every field of
characteristic two.  Combined with the Pfaffian Schur reduction in
`notes/char2-schur-reduction.md`, this excludes a transverse realization at
every even order at least six in characteristic two.

Two tempting shortcuts have been audited and ruled out.

1. Pairwise feasible-set exchange does not remain inside the family of
   transversals (or inside the paired code after twisting).  It supplies
   paths through hole/double-occupancy sets, so Wenzel's strong exchange
   theorem alone does not produce the desired fourth transversal.
2. A binary paired-EQ chart is **not** necessarily locally congruent to a
   sparse Hamilton-cycle chart.  There is already a four-site chart in which
   every one of the six inter-site `2 by 2` blocks is nonzero of rank one,
   all proper paired principal Pfaffians vanish, and the full one is a unit.
   Blockwise `GL_2` congruence preserves the rank and zero/nonzero status of
   each inter-site block, so this dense chart cannot be congruent to the
   sparse four-cycle construction.

An exact degree-nine source-ideal calculation over `F_2` was carried out in
the only symmetry quotient for which Reynolds averaging is valid.  Averaging
over the odd subgroup

\[
 H=\langle(012),(345)\rangle\times\langle(012)_{\rm color}\rangle,
 \qquad |H|=27,
\]

is lossless in characteristic two.  The complete `H`-invariant Macaulay map
has 430,206 row orbits, 162,672 column orbits, and 2,436,368 nonzero entries.
Exact elimination produces an explicit 77,179-column XOR certificate that
the product of the three uniform coefficients belongs to the ideal of the
mixed coefficients.  The construction and audit are in
`computations/test_degree9_source_ideal_char2.py` and
`computations/verify_degree9_char2_certificate.py`.

## 1. Exact twist reformulation

Let the ground set be the disjoint union of triples

\[
                 \{a_i,b_i,c_i\},\qquad 1\leq i\leq n,
\]

and let an alternating matrix `C` represent the normal even delta-matroid

\[
             \mathcal F(C)=\{X:\operatorname {Pf}C[X]\ne0\}.
\]

Put

\[
 A=\{a_i:i\in[n]\},\quad B=\{b_i:i\in[n]\},\quad
 C_0=\{c_i:i\in[n]\}.
\]

Suppose `A` is feasible.  Principal pivot on `A` represents the twist
`D*A`; equivalently, after normalizing by `Pf C[A]`, its principal Pfaffians
are the old principal Pfaffians indexed by symmetric difference with `A`.
Under this twist, a transversal `T` becomes a union of the local codewords

\[
 \begin{array}{c|c}
 T\cap\{a_i,b_i,c_i\}&A\mathbin\triangle T\text{ at site }i\\ \hline
 \{a_i\}&\varnothing\\
 \{b_i\}&\{a_i,b_i\}\\
 \{c_i\}&\{a_i,c_i\}.
 \end{array}                                                \tag{1}
\]

Thus the three column transversals become

\[
 \varnothing,\qquad
 P=\bigcup_i\{a_i,b_i\},\qquad
 Q=\bigcup_i\{a_i,c_i\}.                                  \tag{2}
\]

A fourth feasible transversal is exactly a nonconstant local word in the
three-symbol paired code

\[
             \{\varnothing,\{a_i,b_i\},\{a_i,c_i\}\}.      \tag{3}
\]

Consequently, over a field of characteristic two, the assertion that (2)
cannot be the only feasible codewords is precisely the support form of the
six-site transverse Pfaffian problem.  Nonzero values of the three constant
coordinates can be normalized independently at one site, so support and the
unit-coefficient identity are equivalent here.

## 2. What strong symmetric exchange actually gives

Wenzel proved that even delta-matroids are exactly the delta-matroids obeying
a strong symmetric exchange condition: for feasible `X,Y` and
`e in X triangle Y`, an `f in (X triangle Y)\{e}` can be chosen so that both

\[
                 X\mathbin\triangle\{e,f\},\qquad
                 Y\mathbin\triangle\{e,f\}                \tag{4}
\]

are feasible.  The theorem applies to representable even delta-matroids, but
(4) does not preserve (3).

For example, exchange between `P` and `Q` takes place in
`P triangle Q=B union C`.  Choosing `f=c_i` for `e=b_i` would indeed produce
two mixed transversals.  Strong exchange, however, is free to choose
`b_j` or `c_j` at another site.  Then (4) has a hole at one site and a
double or triple occupancy at another, and the hypothesis says nothing
about its Pfaffian.

The same phenomenon appears along a shortest feasible-set path from one
column to another.  A cardinality-preserving monotone path from `A` to `B`
can have the form

\[
 A-I_k\ \cup\ \{b_j:j\in J_k\},\qquad |I_k|=|J_k|=k.       \tag{5}
\]

It is a mixed transversal only when `I_k=J_k`.  If the successive exchanges
follow one `n`-cycle permutation, every proper prefix has `I_k != J_k`.
This is exactly the defect path visible in the Hamilton-cycle construction
of binary paired equality.  Hence an exchange proof needs a genuinely
three-column compatibility lemma; pairwise strong exchange is insufficient.

Reference: W. Wenzel, *Delta-matroids with the strong exchange conditions*,
Applied Mathematics Letters **6** (1993), 67--70.

## 3. A dense paired-EQ chart refutes sparse-cycle classification

Let there be four two-dimensional blocks `L_i=<e_0,e_1>`.  Set every
diagonal block to zero.  For each `i<j`, let the cross block be the outer
product of the following nonzero half-edge vectors (the first vector belongs
to `L_i` and the second to `L_j`):

\[
\begin{array}{c|cccccc}
ij&12&23&34&14&13&24\\ \hline
(u_{ij},u_{ji})
 &(e_0,e_0)&(e_1,e_0)&(e_1,e_0)&(e_1,e_1)
 &(e_0,e_1)&(e_1,e_1).
\end{array}                                                \tag{6}
\]

All six cross blocks are nonzero and have rank one.  Therefore every
two-block principal Pfaffian vanishes.  For three sites `i,j,k`, the only
possible block-level matching is the triangle, and its Pfaffian is, up to
sign,

\[
 \prod_{uv\in\{ij,jk,ki\}}w_{uv}
 \det(u_{ij},u_{ik})
 \det(u_{ji},u_{jk})
 \det(u_{ki},u_{kj}).                                     \tag{7}
\]

Each of the four triangles in (6) has a parallel pair at a vertex:

\[
 123@1,\qquad124@4,\qquad134@3,\qquad234@2.                \tag{8}
\]

Thus all three-block Pfaffians vanish.  At four blocks, double edges again
vanish because every cross block has rank one.  Of the three Hamilton-cycle
terms, the cycle

\[
                         12|23|34|14                       \tag{9}
\]

has distinct half-edge directions at every vertex and contributes a unit.
The cycle `12|24|34|13` vanishes at vertex 1, while
`13|23|24|14` vanishes at vertex 2.  Hence the full paired Pfaffian is
`-1` in the displayed integral ordering and is nonzero over every field.

It follows that

\[
 \operatorname {Pf}K[\bigoplus_{i\in S}L_i]
   \ne0\quad\Longleftrightarrow\quad S=\varnothing
                  \text{ or }S=[4].                       \tag{10}
\]

A block-diagonal congruence sends a cross block `K_ij` to
`T_i^T K_ij T_j`, so it preserves its rank and whether it is zero.  The
sparse Hamilton-cycle normal form has two zero cross blocks, whereas (6)
has none.  Therefore (6) is not locally congruent to that form.

The exact integer audit is
`computations/verify_dense_paired_eq_chart.py`.

## 4. Characteristic-two degree-nine audit

Let `F_c` be the six-site coefficient cubic in the 135 edge entries, let
`I` be generated by the 726 mixed `F_c`, and put

\[
                         P=F_{0^6}F_{1^6}F_{2^6}.           \tag{11}
\]

The characteristic-zero calculation in `notes/ideal-membership-route.md`
uses `S_6 x S_3` Reynolds averages.  Reducing that 3,102-by-1,314 matrix
modulo two is unsound: the averaging denominator is even.  Replacing
normalized averages by integral full-group orbit sums is sound, but the
resulting invariant map does **not** contain `P` modulo two.

For a lossless test, use the odd group `H` displayed in the Outcome.  Its
order is one in `F_2`, so any hypothetical certificate can be averaged over
`H`.  Enumerating every `H`-orbit of the complete multigraded Macaulay map
gives

\[
 \begin{array}{c|c}
 \text{mixed-coloring orbits}&42\\
 \text{domain-column orbits}&162,672\\
 \text{occurring row orbits}&430,206\\
 \text{nonzero matrix entries}&2,436,368\\
 \text{target row orbits}&139.
 \end{array}                                               \tag{12}
\]

Every column and every target coordinate is constructed from the original
stub matchings before quotienting.  Since all `H`-orbit sizes are odd,
coefficient reduction modulo two loses no normalization factor.  Exact
singleton-row elimination makes 36 assignments and leaves

\[
 430,170\text{ rows},\qquad162,636\text{ columns},
 \qquad\text{nonzero residual target}.                     \tag{13}
\]

Minimum-variable-degree elimination of the dual system

\[
                     A^Ty=0,\qquad b^Ty=1                  \tag{14}
\]

is exact sparse Gaussian elimination over `F_2`.  It produces the
inconsistent row `0=1` after 150,143 pivot eliminations.  Tracking the XOR
provenance of that row gives 77,179 domain-column orbits whose images XOR to
the target vector `b`.  The independently reloadable certificate is

`computations/certificates/degree9_char2_h27_membership.pkl.gz`

with SHA-256

`8e8c90cf84f8c651b74fd0b575a973ab4ca56ca249b57fec696e78b814b8419f`.

The verifier reconstructs the target and checks the 77,179-column XOR
directly, without rerunning elimination.  Therefore the following identity
holds in the full polynomial ring over `F_2`:

\[
       F_{0^6}F_{1^6}F_{2^6}
          =\sum_{c\ {\rm mixed}}Q_cF_c.                    \tag{15}
\]

Every `Q_c` has exactly the complementary vertex/color multidegree described
in `notes/ideal-membership-route.md`.  If all mixed coefficients vanish at
a point over any extension field of `F_2`, (15) makes the product of the
three uniform coefficients zero.  Hence those three coefficients cannot all
be nonzero, and in particular no six-site ternary equality realization
exists.  The Schur reduction makes the same conclusion uniform for every
even order `n>=6` over every infinite characteristic-two field (and hence
over every algebraic closure of `F_2`).

## 5. The integral lift does not bridge to characteristic zero

Lifting the selected GF(2) columns integrally gives

\[
                     P-\sum_j C_j=2R,
\]

where every monomial of \(R\) still has degree one at all 18 vertex/color
ports. The first residual for this lift is already outside the mod-two
source image. More strongly, an exact support-2,179 character modulo four
annihilates the complete integral Macaulay map and pairs with \(P\) to
\(2\bmod4\). Therefore no choice of the mod-two certificate lifts to
modulo four.

This is lossless under the same odd group \(H\), because \(27\) is a unit
modulo every power of two. It shows that the characteristic-two identity
cannot be iterated into a fixed-degree two-adic descent. An exact integral
left-kernel functional also gives a saturated obstruction with target
pairing of two-adic valuation 12. The full arithmetic statement,
certificates, and independent verifiers are in
`notes/degree9-bockstein-mod4.md`.

These facts do not address higher powers of \(P\): radical membership moves
to larger ordinary degree and remains a separate characteristic-zero
question.
