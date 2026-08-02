# The denominator Tor transgression misses at least one of the five face classes

Research reduction only.  This note does not compute the full source
syzygy complex, prove that the active full-nine ring is nonzero, construct
the five relative cap homotopies, prove the unified overlap theorem, or prove
Krenn's conjecture.

## 1. Outcome

The specialization alternative left open by the corrected derived-base-change
framework has a smallest exact finite-free test.  Let

\[
 R_0=\mathbb Q[q_{ij}^{ab}:1\leq i<j\leq5,\ 0\leq a,b\leq2]
\]

and let

\[
 b:C^1=R_0^{15}\longrightarrow V=R_0^{243},\qquad
 d_{v,a}\longmapsto e_a^{(v)}q^{[2]}.                 \tag{1}
\]

Thus (1) is the complete five-site odd denominator presentation, not only
its selected coefficient.  For

\[
                         m=12112,
\]

put (W=R_0\langle\omega_1,\ldots,\omega_5\rangle), where
\(\omega_v\) labels the fine-degree class \([h_vY_0]\) from commit
`f09cbfb`, and define the normalized cap-coordinate map

\[
 a(d_{v,m_v})=\omega_v,\qquad
 a(d_{v,c})=0\quad(c\ne m_v).                          \tag{2}
\]

The terminology is literal: projection of (1) to the output word (m)
satisfies

\[
 [e_m]b(d_{v,m_v})=h_v,
 \qquad [e_m]b(d_{v,c})=0\ (c\ne m_v).                \tag{3}
\]

Hence (2) retains the five labelled mixed-to-pure defects before the map
\(\omega_v\mapsto h_vY_0\) forgets their deletion-face labels.

The universal map (b) is injective.  Consequently, after any base change
\(R_0\to S\),

\[
 \operatorname {Tor}_1^{R_0}(\operatorname {coker}b,S)
       \cong\ker(b_S),\qquad
 \tau_S=a_S|_{\ker b_S}:\ker b_S\longrightarrow W_S.  \tag{4}
\]

Thus positive Tor can indeed create denominator-invisible chains.  The
relevant question is not whether Tor is nonzero, but whether (4) is onto the
five-dimensional face obstruction.

On the two exact rational packets the answer is **no**:

\[
\begin{array}{c|c|c|c|c}
 &\operatorname {rank}b_S&\dim\operatorname {Tor}_1&
 \operatorname {rank}\tau_S&\dim\operatorname {coker}\tau_S\\ \hline
 \text{direct-free}&7&8&4&1\\
 \text{tilted}&8&7&3&2.
\end{array}                                             \tag{5}
\]

Both packets have nonzero curvature
\(\kappa=-1/4,-5/2\), respectively, and both specialize all five
\(h_v\) for the word `12112` to zero.  Therefore curvature localization and
the five scalar vanishings do not force the five transgression classes.
The direct-free packet still misses one normalized face direction; the
tilted packet misses two.

This does not rule out a larger full-source Tor class.  It proves that such a
class cannot be inferred from the old fifteen denominator columns and the
five equations (h_v=0).  Any successful specialization-created proof must
add source-provenant columns whose cap projections fill the missing
directions.

## 2. Universal injectivity

Write (Q_0=\operatorname {coker}b\).  The exact checker evaluates the
universal variables at the integral point

\[
 q_{ij}^{ab}=((((i-1)5+j)3+a)3+b)+1.                  \tag{6}
\]

At (6), a displayed (15\times15) row minor of (1), using the words

\[
\begin{gathered}
00000,00001,00002,00010,00011,00020,00100,00101,00110,00111,\\
00200,01000,02000,10000,20000,
\end{gathered}
\]

has determinant

\[
 -32451587105484628367742562673068054425600000\ne0.   \tag{7}
\]

Therefore the corresponding universal minor is a nonzero polynomial.
Since (R_0) is a domain, (b) has rank fifteen over its fraction field;
as its source has rank fifteen, its kernel is a torsion submodule of the
free module (C^1), hence is zero.  We have the free resolution

\[
 0\longrightarrow C^1\mathop{\longrightarrow}^{b}V
 \longrightarrow Q_0\longrightarrow0.                 \tag{8}
\]

Tensoring (8) with (S) proves the first isomorphism in (4).  Since the
universal kernel is zero, the quotient by (a(\ker b)\) required in the
general corrected framework is just (W), and (2) gives the transgression.

The ten unselected columns are also universally independent.  At (6), the
minor on columns

\[
 d_{10},d_{12},d_{20},d_{21},d_{30},d_{32},d_{40},d_{42},d_{50},d_{51}
\]

and rows

\[
 00000,00001,00002,00010,00011,00020,00100,00200,01000,20000
\]

has determinant

\[
 8906634052942223094145500014691840000\ne0.            \tag{9}
\]

Thus the generic situation is exactly (10+5=15): every selected face
column supplies a new direction until specialization creates relations.

## 3. Exact transgression and the sharp membership criterion

Split the source according to (2):

\[
 C^1=C_{\rm sel}\oplus C_{\rm oth},\qquad
 b=[\,b_{\rm sel}\ b_{\rm oth}\,],                    \tag{10}
\]

where (C_{\rm sel}\cong R_0^5), (C_{\rm oth}\cong R_0^{10}), and
\(a\) is projection to (C_{\rm sel}\cong W\).  For an (S)-algebra,
the image of (4) consists exactly of those (y\in S^5) for which there is
some (z\in S^{10}) satisfying

\[
                    b_{\rm sel}y+b_{\rm oth}z=0.        \tag{11}
\]

It follows that

\[
 \boxed{\quad
 \tau_S\text{ is onto}
 \iff
 b_{\rm sel}(S^5)\subseteq b_{\rm oth}(S^{10}).
 \quad}                                                 \tag{12}
\]

Equivalently, the induced map

\[
 S^5\mathop{\longrightarrow}^{\bar b_{\rm sel}}
                    \operatorname {coker}(b_{\rm oth}) \tag{13}
\]

must be zero.  Formula (13), rather than the mere nonvanishing of Tor, is the
smallest exact full-ring condition.

There is a useful sharp determinantal version.  Over a field (k),

\[
 \operatorname {rank}\tau_k
   =5-\bigl(\operatorname {rank}b_k-
                  \operatorname {rank}(b_{\rm oth})_k\bigr),       \tag{14}
\]

and surjectivity is equivalent to equality of the two ranks on the right.
Over a local ring, suppose an (r\times r) minor
\(\Delta\) of (b_{\rm oth}\) is a unit and (b_{\rm oth}) has constant
rank (r) on that open set, equivalently
\(I_{r+1}(b_{\rm oth})=0\) there.  Then (12) is equivalent to the
vanishing of every ((r+1)\times(r+1)) minor obtained by adjoining one
selected column to (b_{\rm oth}).  This is Cramer's rule after pivoting on
\(\Delta\), so it is a membership criterion, not only a set-theoretic rank
bound.  In particular one may take (r=10) wherever a full ten-column minor
of (b_{\rm oth}) is a unit.  A unit minor of nonmaximal size, with no
constant-rank hypothesis, is not enough.

Globally, (12) has the necessary Fitting condition

\[
                         I_{11}(b)S=0,                  \tag{15}
\]

because the image of (b) would then be generated by the ten unselected
columns.  Condition (15) alone is not sufficient, even over a field on a
lower-rank stratum: both packets in Section 5 have
\(\operatorname {rank}b<11\), so (15) holds while the transgression is not
onto.  The exact condition is the vanishing of (13), or the constant-rank
local augmented-minor criterion above.

## 4. The full-nine quotient and curvature localization

Let \(\mathscr R\) be the full polynomial ring in all labelled cells of the
eight-site problem, containing (R_0), and let (J_{pq,pr}) be the ideal of
the complete simultaneous `pq`/`pr` full-nine coefficient relations.  On
the selected active overlap set put

\[
 S=\bigl(\mathscr R/J_{pq,pr}\bigr)[\kappa^{-1}].       \tag{16}
\]

Polynomial extension from (R_0) to \(\mathscr R\) preserves the
injectivity proved above.  Therefore the exact answer over the intended
ring (16) is the symbolic formula

\[
 \operatorname {Tor}_1^{\mathscr R}(Q_0\otimes\mathscr R,S)
       =\ker(b\otimes S),\qquad
 \operatorname {im}\tau_S
       =\ker\!\left(S^5\mathop{\longrightarrow}^{\bar b_{\rm sel}}
                    \operatorname {coker}(b_{\rm oth}\otimes S)\right).
                                                               \tag{17}
\]

The five classes enter the image exactly when (13) vanishes after imposing
the full-nine ideal and localizing at \(\kappa\).  In particular, a proof by
this route may target the concrete module membership

\[
 b(d_{v,m_v})\in\operatorname {im}(b_{\rm oth})
                 \pmod {J_{pq,pr}},\qquad v=1,\ldots,5. \tag{18}
\]

Computing (18) in the entire ring is not a smaller black-box calculation:
the full (3^8=6561)-coefficient ideal in (16) is the open eight-site source
locus.  Proving that (16) is the zero ring would already settle the case;
proving (18) nontrivially would supply precisely the missing five
homotopies.  Thus (17)--(18) are the exact symbolic characterization, while
the Fitting gate (15) is the tractable necessary condition.

Localization at \(\kappa\) is flat.  It cannot create the Tor in (17); any
new kernel comes from the quotient by (J_{pq,pr}).  Localization merely
removes inactive components and allows unit-minor tests on the active open.

## 5. Exact packet calculation

The two rational packets are not points of the full source scheme: their
complete `pq` EqSystem has six and seven failures, respectively.  They are
therefore counterguards for implications from the retained packet data, not
evaluations of (16).  Nevertheless, they give a stringent test because
\(\kappa\ne0\) and all five scalar defects (3) vanish.

For the direct-free packet, a reduced exact kernel basis of (b_k) is

\[
\begin{gathered}
 d_{10},d_{11},d_{12},d_{30},d_{31},d_{32},\\
 -d_{22}+d_{41},\qquad -2d_{22}+d_{52}.                \tag{19}
\end{gathered}
\]

Applying (2), the nonzero transgression vectors are

\[
 \omega_1,\quad\omega_3,\quad-\omega_2+\omega_4,
              \quad-2\omega_2+\omega_5.                \tag{20}
\]

They have rank four.  The cokernel is detected by the covector

\[
                         (0,1,0,1,2),                   \tag{21}
\]

and only the individual classes \(\omega_1,\omega_3\) lie in the image.
The ten unselected columns have rank six, while all fifteen columns have
rank seven.  More concretely, the columns

\[
 d_{20},d_{21},d_{40},d_{42},d_{50},d_{51},d_{22}
\]

on rows

\[
10012,11012,12002,12010,12011,12012,12022
\]

have determinant (-4).  This is a literal augmented-minor witness that
the selected column (d_{22}) does not enter the unselected image.

For the tilted packet, the kernel basis is

\[
 d_{10},d_{11},d_{12},d_{30},d_{31},d_{32},
                     -d_{22}+d_{41}.                    \tag{22}
\]

The transgression image is

\[
 \langle\omega_1,\omega_3,-\omega_2+\omega_4\rangle,   \tag{23}
\]

of rank three.  Its cokernel has dual basis

\[
                 (0,1,0,1,0),\qquad(0,0,0,0,1).        \tag{24}
\]

Again only \(\omega_1,\omega_3\) are hit individually.  The same six
unselected columns have rank six, while adding (d_{22},d_{52}) produces
an eight-by-eight minor of determinant (8) on the preceding seven rows
plus `22012`.  Hence two independent selected directions survive in
\(\operatorname {coker}b_{\rm oth}\).

Equations (19)--(24) explain why (h_1=\cdots=h_5=0) is too weak.  Those
five equalities inspect a single word row in each selected column.  A Tor
class must cancel all 243 forbidden word coordinates simultaneously.

## 6. Consequence for the proof search

The denominator specialization mechanism is real but incomplete.  It
creates eight new invisible relations on the direct-free guard, more than
the five desired labels, yet their cap projections span only four
dimensions.  Counting Tor generators is therefore misleading; the decisive
invariant is the transgression rank (14).

For a full-source construction, the next exact target is now either:

1. prove the five memberships (18) over the active full-nine quotient; or
2. enlarge (1) by genuine cross-word/full-source columns and show that their
   specialized kernel makes the analogue of (13) zero.

The old denominator block, scalar equations (h_v=0), and curvature
localization do not accomplish either task on the exact packets.

## 7. Executable verification

The dependency-free checker
[`verify_h3_denominator_tor_transgression_fitting_gate.py`](../computations/verify_h3_denominator_tor_transgression_fitting_gate.py)
reconstructs (1), certifies the universal minors (7) and (9), independently
builds both sparse rational packets, verifies all five (h_v) evaluations,
computes exact kernels and cap projections, freezes (19)--(24), and checks
the nonmembership minors.  It supports `all`, `universal`, `direct_free`,
and `tilted` modes.  The combined exact ledger digest is

```text
268c982050599af3358acb2c6b3dabc5eca0e95c994f75e50d560c41f132152a
```
