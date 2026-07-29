# Pairwise transverse Pfaffians and matchgate compatibility

## Outcome

A two-color transversal of the characteristic-two Krenn matrix is not, in
general, a standard matchgate signature on `n` external bits.  Relative to a
nonzero reference amplitude it is exactly a **paired restriction** of a
standard even Pfaffian signature on `2n` external nodes.  The paired chart
has one additional condition: its principal block on the `n` hole nodes is
nonsingular.

This distinction is decisive.  Binary equality is not a standard normalized
matchgate signature for even `n>=4`, but it has a transverse paired-Pfaffian
representation for every even `n`.  Moreover, the three pairwise binary
equalities for colors `0,1,2` are mutually compatible over every field,
including the algebraic closure of `F_2`.  An explicit six-vertex example
has a nonzero genuinely ternary coefficient.  Consequently no identity
using only the three principal two-color restrictions can prove the desired
three-color obstruction.

All matrices below are alternating: `K^T=-K` and the diagonal is zero.  In
characteristic two the first condition reads `K^T=K`, while the zero-diagonal
condition is retained.  Pfaffians are defined by their usual signed matching
polynomial; all displayed identities are polynomial identities over the
integers and hence remain valid after reduction modulo two.

## 1. The transverse Pfaffian chart

Let `n` be even.  At each vertex choose a reference variable `x_i` and an
alternative variable `y_i`.  In the order

\[
                 x_1,\ldots,x_n,y_1,\ldots,y_n,
\]

write the alternating covariance as

\[
 K=\begin{pmatrix}A&B\\-B^T&D\end{pmatrix}.                 \tag{1}
\]

Suppose the reference amplitude is nonzero.  After a harmless scalar
normalization,

\[
                           \operatorname {Pf}A=1.            \tag{2}
\]

Thus `A` is nonsingular because `det A=(Pf A)^2`.  Put

\[
 H=A^{-1},\qquad M=A^{-1}B,
 \qquad Q=D+B^TA^{-1}B,                                    \tag{3}
\]

and form the alternating matrix

\[
 G=\begin{pmatrix}H&M\\-M^T&Q\end{pmatrix}                 \tag{4}
\]

on formal nodes `h_1,...,h_n,p_1,...,p_n`.  When taking a principal
Pfaffian, order a selected pair as

\[
                         h_i,p_i                             \tag{5}
\]

and order these pairs by increasing `i`.

**Lemma 1.1 (paired Pfaffian replacement identity).**  For every
`S subseteq [n]`, let `T_S` select `y_i` at vertices in `S` and `x_i`
elsewhere, in vertex order.  Then

\[
 {\operatorname {Pf}K[T_S]\over\operatorname {Pf}A}
   =\operatorname {Pf}G[(h_i,p_i)_{i\in S}].                \tag{6}
\]

If the selected nodes of `G` are instead ordered with all holes before all
particles, the right side acquires the factor
`(-1)^(|S|(|S|-1)/2)`.

**Proof.**  This is the Pfaffian replacement, or generalized Wick,
identity.  For completeness, introduce anticommuting variables `x,y`.  The
coefficient of an ordered squarefree monomial `z_I` in

\[
                 \exp\!\left({1\over2}z^TKz\right)          \tag{7}
\]

is `Pf K[I]`.  Complete the alternating square:

\[
 {1\over2}x^TAx+x^TBy+{1\over2}y^TDy
 = {1\over2}(x+A^{-1}By)^TA(x+A^{-1}By)
     +{1\over2}y^TQy.                                      \tag{8}
\]

Extract the reference coefficient `x_1...x_n`.  Replacing `x_i` by `y_i`
introduces one hole and one particle.  Wick expansion of the resulting
`2|S|` insertions has contractions

\[
 \langle h_i h_j\rangle=H_{ij},\quad
 \langle h_i p_j\rangle=M_{ij},\quad
 \langle p_i p_j\rangle=Q_{ij},                            \tag{9}
\]

so its sum is the Pfaffian in (6).  Division by the extracted reference
coefficient gives the left side.  Moving all particles past later holes
uses `|S|(|S|-1)/2` swaps and gives the alternative sign convention.
This proves (6) over the rational function ring in the entries of `A,B,D`.
Clearing the power of `Pf A` in the denominators gives an identity over the
integers.  It therefore specializes to every field whenever `Pf A` is
nonzero, including characteristic two. `QED`

The chart is also reversible.

**Proposition 1.2 (classification of transverse charts).**  The change of
variables (3) is a bijection between alternating block matrices (1) with
`A` nonsingular and alternating matrices (4) with `H` nonsingular.  Under
this change of variables, the normalized transversal coordinates are the
paired restriction (6) of the standard principal-Pfaffian signature of
`G`.

**Proof.**  Lemma 1.1 gives the forward map.  Conversely, given (4) with
`H` nonsingular, set

\[
 A=H^{-1},\qquad B=AM,\qquad D=Q-B^THB.                    \tag{10}
\]

These matrices are alternating in the required blocks, and substitution in
(3) recovers `H,M,Q`.  If an unnormalized amplitude rather than its ratios
is required, scale both local variables `x_i,y_i` at one site by
`(Pf A)^(-1)`; every transversal amplitude is scaled by the same factor,
while the normalized signature is unchanged. `QED`

Thus a transverse bit is encoded by the two-node codeword
`{h_i,p_i}`.  It is not an ordinary deletion bit on one external node.

There is also a compact polynomial form of the classification.  Let `J_i`
be the alternating `2 by 2` matrix with entry `1` in position `(h_i,p_i)`,
and put

\[
                         Z(z)=\bigoplus_{i=1}^n z_iJ_i.       \tag{10a}
\]

Expanding a Pfaffian according to the local `Z`-edges gives

\[
 \operatorname {Pf}(G+Z(z))
   =\sum_{S\subseteq[n]}
       \operatorname {Pf}G[(h_i,p_i)_{i\in S}]
       \prod_{i\notin S}z_i.                               \tag{10b}
\]

Consequently a transverse chart with nonzero reference coordinate is
binary equality exactly when its hole block is nonsingular and

\[
                         \operatorname {Pf}(G+Z(z))
                              =1+z_1z_2\cdots z_n.           \tag{10c}
\]

This is often a more convenient formulation than the individual
coordinates.  Squaring gives the necessary determinant identity

\[
                         \det(G+Z(z))=(1+z_1\cdots z_n)^2,  \tag{10d}
\]

including in characteristic two.  The Hamilton-cycle construction below
shows that neither (10c) nor the nonsingular-hole condition is an
obstruction.

## 2. It is not a standard `n`-bit matchgate signature

Let

\[
 \mathrm{EQ}_n(S)=\begin{cases}1,&S=\varnothing\text{ or }S=[n],\\
                                0,&\text{otherwise.}
                 \end{cases}                               \tag{11}
\]

For even `n>=4`, this is not a standard normalized matchgate signature on
`n` external nodes.  Indeed, a standard even Pfaffian chart with nonzero
empty coordinate has

\[
                         F(S)=\operatorname {Pf}W[S]         \tag{12}
\]

for one alternating `n by n` matrix `W`.  Equation (11) on two-element sets
gives `W_ij=0` for every `i<j`, hence `W=0`, while (12) then gives
`F([n])=0`, contrary to (11).  This argument is field-uniform.

On the other hand, (11) is a paired transverse signature.  Let `P_0,P_1`
be perfect matchings whose union is one alternating Hamilton cycle.  Put a
nonsingular alternating matrix `A_0` on `P_0` and an alternating matrix
`A_1` on `P_1`, scaling one edge in each so that

\[
                         \operatorname {Pf}A_0
                         =\operatorname {Pf}A_1=1.           \tag{13}
\]

Take `B=0`, `A=A_0`, and `D=A_1` in (1).  For a replacement set `S`,

\[
 \operatorname {Pf}K[T_S]
   =\epsilon(S)\operatorname {Pf}A_0[[n]\setminus S]
      \operatorname {Pf}A_1[S].                             \tag{14}
\]

Here `epsilon(S)` is the sign of the shuffle from vertex order to the two
color blocks (and is one in characteristic two).  The right side is nonzero
exactly when `S` is simultaneously a union of
edges of `P_0` and a union of edges of `P_1`.  Since `P_0 union P_1` is
connected, this happens only for `S=empty` and `S=[n]`.  Equations
(13)--(14) give `EQ_n` exactly.  In the paired chart this example has

\[
                         H=A_0^{-1},\qquad M=0,qquad Q=A_1. \tag{15}
\]

This explicitly verifies that the transversal restriction is a pair-code
restriction of a standard `2n`-node matchgate, but not a standard `n`-node
matchgate.

## 3. Three pairwise restrictions are compatible

The preceding construction can be made simultaneously for all three color
pairs and all even `n>=4`.  Write `N=n-1`, use vertices
`infinity union Z_N`, and define the cyclic one-factors

\[
 P_a=\{\{\infty,a\}\}\ \cup\
       \{\{a+j,a-j\}:1\le j\le (N-1)/2\},
       \qquad a=0,1,2.                                     \tag{16}
\]

The union `P_a union P_b` is Hamilton whenever `a-b` is a unit modulo `N`.
Indeed, after translating `a` to zero, its alternating walk visits

\[
 \infty,0,2(b-a),-2(b-a),4(b-a),-4(b-a),\ldots             \tag{17}
\]

before returning to infinity.  For `a,b in {0,1,2}`, every nonzero
difference is `1` or `2`, hence is a unit because `N` is odd.  Thus the
three factors in (16) are pairwise Hamiltonian.

For each `r=0,1,2`, let `A_r` be an alternating matrix supported on `P_r`
and normalized by `Pf A_r=1`.  On the `3n` vertex-color modes take the block
diagonal alternating matrix

\[
                             K=A_0\oplus A_1\oplus A_2.     \tag{18}
\]

For a coloring using only colors `r,s`, with color-`s` set `S`, its
coefficient is

\[
                 \epsilon_{r,s}(S)
                 \operatorname {Pf}A_r[[n]\setminus S]
                 \operatorname {Pf}A_s[S].                 \tag{19}
\]

The Hamilton-cycle argument following (14) makes (19) exactly
`EQ_n`.  Hence:

**Theorem 3.1 (field-uniform pairwise compatibility).**  Over every field
and for every even `n>=4`, there is one alternating covariance whose three
principal two-color transversal restrictions are all exactly binary
equality.  This remains true over the algebraic closure of `F_2`.

At six vertices the compatibility does not extend to ternary equality.
Take

\[
 \begin{aligned}
 P_0&=01|23|45,\\
 P_1&=05|12|34,\\
 P_2&=03|15|24.
 \end{aligned}                                              \tag{20}
\]

Every pairwise union is a Hamilton cycle.  Nevertheless the genuinely
ternary coloring

\[
                              (2,1,1,2,0,0)                  \tag{21}
\]

has the unique supported matching

\[
                              03|12|45,                      \tag{22}
\]

one edge from each factor, and therefore has a nonzero unit coefficient over
every field (it is one in characteristic two, and the remaining edge signs
can make it one over any field).  It is invisible in every two-color
restriction.

## 4. Precise surviving gap

Pure-spinor identities do apply after choosing a nonzero reference
amplitude, but they apply to the `2n` hole-particle matrix (4), not directly
to an `n`-bit equality signature.  The nonsingular hole condition in
Proposition 1.2 does not obstruct equality, by (15).  Chart transitions to
a different nonzero constant color merely give another paired Pfaffian
chart of the same covariance.

Theorem 3.1 rules out a contradiction based only on compatibility of the
three pairwise restrictions, in characteristic two or otherwise.  Any
successful Pfaffian argument must retain a principal coordinate involving
all three particle types—or an identity coupling such a ternary coordinate
to the pairwise charts.  Equation (21) is the minimal explicit witness to
the information lost by all pairwise restrictions.

The accompanying exact audit is
`computations/verify_pairwise_matchgate_compatibility.py`.
