# The closure22 first-exchange dual is a cut–colour correlation cocycle

## Exact scope and verdict

In the joint semigroup quotient, a decorated monomial is recorded by

\[
 k=(m_{uv})_{0\leq u<v<8}\oplus(h_{ab})_{0\leq a,b<3}\in\mathbb N^{37},
 \tag{1}
\]

where \(m_{uv}\) is its multiplicity on physical edge \(uv\), and \(h_{ab}\)
is its global ordered endpoint-colour-pair histogram. The integer dual in
results_closure22_joint_semigroup.json has support 16, annihilates the
**128,516 target-touching translations used in that replay**, and pairs the
holonomy target to \(1\) over \(\mathbb Z\).

This is a finite first-exchange-layer separator only. It does **not**
annihilate all degree-13 translates of the 22 closure words and therefore
does not prove degree-13 or full-ideal nonmembership. The exact scope guard
is given below.

Combinatorially, its support carries a recognizable two-vertex-cut versus
ordered-colour correlation. The complete coefficient vector is nevertheless
not one signed graph cycle, cut, determinant minor, or toric circuit. It is
a rank-four functional supported on four correlated
physical-graph/colour-histogram fibres. One two-term fibre is an ordinary
four-cycle minor, but that minor does not account for the remaining fourteen
terms.

## The 13 physical graphs and four colour histograms

Write repeated edges with exponents. In order of first appearance, the 13
physical multigraphs are

~~~text
G1  07^2 16 17 25 27 34 36^3 45^3
G2  07^2 16 17 25 27 34^2 36^2 45^2 56
G3  07^2 16 17 25 26 34^2 36 37 45^2 56
G4  07^2 16 17 23 27 34 36^2 45^3 56
G5  07^2 16 17 23^2 36^2 45^4 67
G6  07^2 14 17 23^2 36^2 45^3 56 67
G7  01 07 17 27^2 36^4 45^4
G8  01 07 17 27^2 34 36^3 45^3 56
G9  01 07 17 26 27 36^3 37 45^4
G10 01 07 17 26 27 34 36^2 37 45^3 56
G11 01 07 17 23 27 36^3 45^4 67
G12 01 07 17 23 27 34 36^2 45^3 56 67
G13 01 07 17 23 26 34 36 37 45^3 56 67
~~~

Every graph has 13 edges with multiplicity and the same labelled degree
sequence

\[
                    (2,2,2,4,4,4,4,4).                 \tag{2}
\]

The four ordered histograms, with row index the colour at the smaller site,
are

\[
H_1=\begin{pmatrix}6&1&0\\1&1&1\\0&3&0\end{pmatrix},\quad
H_2=\begin{pmatrix}6&1&0\\1&2&0\\0&2&1\end{pmatrix},\quad
H_3=\begin{pmatrix}6&0&0\\2&2&2\\0&0&1\end{pmatrix},\quad
H_4=\begin{pmatrix}6&1&0\\1&2&2\\0&0&1\end{pmatrix}.
\tag{3}
\]

Rows \(G_i\), columns \(H_j\), and zero for absent support give the complete
dual coefficient matrix

\[
\begin{pmatrix}
-1&-1&0&0\\
 1& 1&0&0\\
-1&-1&0&0\\
 0&-1&0&0\\
 0& 0&1&0\\
 0& 0&-1&0\\
 0& 0&0&-4\\
 0& 0&0& 2\\
 0& 0&0& 1\\
 0& 0&0&-1\\
 0& 0&0& 1\\
 0& 0&0&-1\\
 0& 0&0& 1
\end{pmatrix}.
\tag{4}
\]

It has rank four. Its support incidence is a \(K_{3,2}\), one extra
\(H_2\)-leaf, an \(H_3\)-pair, and seven \(H_4\)-leaves. Thus the 16 columns
are not a Cartesian product of a graph orbit and a colour orbit.

Each \(H_j\) has trivial stabilizer and orbit size six under simultaneous
global \(S_3\) colour relabelling. Only \(H_2^{\mathsf T}=H_4\) remains in
the displayed support; the transposes of \(H_1,H_3\) are absent. Hence this
sparse dual is not itself an \(S_3\)-orbit sum. This is consistent with its
construction by a lexicographically chosen free column and echelon
back-substitution: the separator is exact, but not canonical.

## The unique linear edge–colour correlation on its support

The physical graphs have affine rank six, the four histograms have affine
rank three, but the 16 joint columns have affine rank eight rather than nine.
Their marginal spans therefore meet in one nonconstant direction. A
primitive formula for it is

\[
 \boxed{2m_{01}=2h_{01}+h_{11}+h_{12}-4}
 \qquad\text{on these sixteen columns}.                 \tag{5}
\]

Indeed \(m_{01}=0\) on \(G_1,\ldots,G_6\) and \(m_{01}=1\) on
\(G_7,\ldots,G_{13}\); the right side makes the same \(0/2\) split between
\(H_1,H_2,H_3\) and \(H_4\). Equation (5) is the recognizable part of the
edge–colour correlation: an asymmetric ordered-colour count detects whether
the physical graph contains the distinguished edge \(01\). It is a relation
on the dual's support, not an identity in the ambient semigroup.

Because every graph has \(d_0=d_1=2\), the same direction is literally the
two-vertex cut statistic

\[
 \boxed{
 |\delta_{\{0,1\}}|
 =4-2m_{01}
 =8-2h_{01}-h_{11}-h_{12}.}
 \tag{5a}
\]

It has value \(4\) on the first nine dual columns and \(2\) on the last
seven. Thus “cut–colour correlation cocycle” accurately describes the
support geometry. It does not mean that the sixteen dual coefficients
themselves are evaluations of this cut.

The graph fibres themselves are connected by ordinary alternating
four-cycle moves. For example

\[
 G_2-G_1=E_{34}+E_{56}-E_{36}-E_{45}.                  \tag{6}
\]

The \(H_3\)-fibre is literally the signed minor

\[
 x^{\gcd(G_5,G_6)}(x_{16}x_{45}-x_{14}x_{56}).         \tag{7}
\]

But the whole dual is not a toric circuit: its coefficient sum is \(-4\),
and its first semigroup moment

\[
                         \sum_{r=1}^{16}\lambda_r k_r
\]

has 21 nonzero coordinates. A signed binomial/minor/cycle circuit would
have zero affine and first moments. Hence the complete rank-four dual is not
the single cut functional (5a), even though (5a) explains its only shared
marginal direction.

## Full-translation counterguard

Enumerating every nonnegative translation that can touch one of the 16
supported columns finds 23 nonzero pairings across seven existing closure22
words:

~~~text
01000000: 5    10000000: 5    11110101: 5
11111010: 2    21112111: 1    22111111: 2    22211111: 3
~~~

The maximum absolute pairing is \(3\). The lexicographically first guard
uses word 01000000, pairing \(-1\), and translation

~~~text
physical: 07 17 27 36^3 45^3
colours:  [[3,1,0],[0,1,1],[0,3,0]].
~~~

The same translation also pairs nontrivially with 10000000. These rows
were absent only because they do not touch the original target support.
They decisively block promotion of (4) from a first-exchange cocycle to a
full degree-13 dual.

## Terminal 100-column CEGAR dual

The later CEGAR closure in results_closure22_joint_cegar.json adds 533
independent translations over 24 rounds. Its terminal primitive integer
dual has support 100, maximum coefficient magnitude four, zero pairing with
**every abstract degree-13 joint-semigroup translate** of all 22 words, and
target pairing one. This is a genuine characteristic-zero nonmembership
certificate in that fixed-degree abstract semigroup module.

It is still not a literal decorated-ring or all-degree ideal certificate:
the semigroup allows abstract edge/histogram multipliers without proving
that each is the projection of a decorated monomial, and no higher degree
is tested.

The terminal support contains 28 physical graphs and 14 ordered-colour
histograms. All physical graphs still have degree sequence
\((2,2,2,4,4,4,4,4)\), but their
affine rank is now nine; the colour affine rank is five and the joint affine
rank is the full sum fourteen. Consequently

\[
 \dim\bigl(
 \operatorname{Aff}_{0}(\text{physical})
 \cap
 \operatorname{Aff}_{0}(\text{colour})
 \bigr)=9+5-14=0.                                    \tag{8}
\]

Thus the simple cut–colour relation (5a) is a transient feature of the
first separator, not the terminal invariant: it fails on 62 of the 100
terminal columns.

The terminal coefficient matrix has rank seven and exactly two support
components:

\[
       (21\text{ graphs},13\text{ histograms},93\text{ columns})
       \;\sqcup\;
       (7\text{ graphs},1\text{ histogram},7\text{ columns}). \tag{9}
\]

The 93-term component has rank six and zero coefficient sum separately
over every one of its thirteen colour histograms. It is therefore a pure
relative edge–colour correction invisible to the colour marginal. The
seven-term component lies over

\[
 H_{14}=
 \begin{pmatrix}6&1&0\\1&2&2\\0&0&1\end{pmatrix}=H_4
\]

and has coefficients

\[
                         (-4,2,1,-1,1,-1,1),           \tag{10}
\]

whose sum is \(-1\). Only its final three columns meet the target, with
\((\lambda,t)=(1,1),(-1,2),(1,2)\), giving total pairing one.

This gives the terminal recognition:

> The full dual is a 93-term relative correlation correction attached to a
> seven-term one-histogram graph residue. It is not a single signed minor,
> cycle, or cut functional.

Indeed its total coefficient sum is \(-1\), and its first semigroup moment
has 22 nonzero coordinates. All fourteen histograms have trivial global
\(S_3\) stabilizer; only one transpose pair occurs. Hence the sparse
terminal dual is not an orbit sum either. Its exact significance is
module-theoretic: it is a bounded correlation cocycle annihilating all
degree-13 abstract closure22 exchanges.

## New-word counterguard and smallest repair

The terminal statement is specific to the current 22-word module. An exact
scan of all 6,558 mixed eight-site words finds

\[
 4,294\ \text{new crossing words},\qquad
 44,127\ \text{distinct crossing translations}.       \tag{11}
\]

No existing closure22 word crosses, agreeing with the terminal CEGAR replay.
But the new rows show that the 100-column dual is not an invariant of the
full mixed-\(X_5\) packet.

The smallest source-symmetry shape is \(7+1\). Its full
\(S_8\times S_3\) word orbit has size 48; eight words are already in
closure22, so source-symmetric completion adds 40. Seven words in this orbit
cross the separator, through 87 translated rows. The cheapest new generator
is

\[
                    w=00000200,
\]

with four crossings, all pairing \(-1\). Thus the concrete next packet is
not another determinant identity: it is the missing \(7+1\) word orbit.

For a sparse literal guard, word \(00001000\) has a degree-nine decorated
multiplier on only five physical edges and four ordered colour pairs which
pairs the terminal dual to \(-2\). Hence this failure already occurs in a
literal source row; it is not an artefact of a non-liftable abstract
semigroup multiplier.

The exact first-layer decoder and counterguard replay is
[audit_closure22_integer_dual_shape.py](../computations/unaudited-codex-rootless-fine-macaulay-2026-08-22/audit_closure22_integer_dual_shape.py).
The terminal profile replay is
[audit_closure22_terminal_dual_shape.py](../computations/unaudited-codex-rootless-fine-macaulay-2026-08-22/audit_closure22_terminal_dual_shape.py).
