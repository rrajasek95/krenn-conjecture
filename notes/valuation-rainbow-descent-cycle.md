# Valuation-minimal rainbow rewrites have an exact two-cycle

## Outcome

The negative color-balanced monomial forced by the integral degree-nine
identity does not by itself start a strictly decreasing nonarchimedean
rewrite.  There are two exact reasons.

First, at a globally minimum-valuation locally-rainbow network, every usable
mixed-fibre rewrite has an equal-valuation cancellation mate and is
reversible.  Thus the local argument necessarily enters a valuation plateau.

Second, a thirteen-cell rational model realizes this obstruction sharply at
six vertices.  Its three constant coefficients are exactly `1`, a displayed
mixed coefficient is exactly `(1/2)+(-1/2)=0`, every supported
locally-rainbow degree-nine monomial has 2-adic valuation `-1`, and the
selected mixed-fibre rewrite is an immediate two-cycle between two global
minima.

This is not a Krenn counterexample: exactly four other mixed coefficients
remain nonzero.
It is a counterexample to the proposed *local descent lemma*.  A successful
continuation must use simultaneous information from additional fibres to
orient or annihilate the minimum plateau.  Merely iterating the degree-nine
identity cannot do that either: the existing exact mod-four Bockstein
character proves that no second same-multidegree lift exists.

The finite audit is
`computations/verify_valuation_rainbow_descent_cycle.py`.

## 1. The minimum-plateau lemma

Let `K` be a nonarchimedean field and let `A` be a finite collection of
nonzero endpoint-coloured aggregate cells.  A **locally-rainbow network** is
a nine-cell monomial

\[
                         w_G=\prod_{e\in G}A_e              \tag{1}
\]

whose cells match the eighteen stubs `(v,a)`, one copy of every stub.  This
is exactly the support type of every monomial in the residual `R` of the
integral degree-nine identity.

Suppose `G` has minimum valuation among all supported locally-rainbow
networks.  Let \(M\subset G\) be a decorated perfect matching whose induced
vertex colouring `c` is mixed, and suppose the exact coefficient equation is

\[
                   F_c(A)=\sum_{N\in\mathcal F_c}z(N)=0.    \tag{2}
\]

For every nonzero term `N` in this fibre, put

\[
                  G_N=(G\setminus M)\mathbin\sqcup N.      \tag{3}
\]

The complement in (3) uses at vertex `v` the two ports other than `c(v)`,
while `N` uses port `c(v)`.  Hence every `G_N` is again locally rainbow.

**Lemma 1.1 (minimum plateau).**  There is an \(N\ne M\) in the fibre with

\[
                    \nu(w_{G_N})=\nu(w_G).                 \tag{4}
\]

Moreover, replacing `N` by `M` in `G_N` returns to `G`, so the replacement
relation contains the two-cycle \(G\leftrightarrow G_N\).

**Proof.**  Minimum of `G` in the finite set of locally-rainbow networks
gives

\[
 \nu(z(N))+\nu(w_{G\setminus M})
       =\nu(w_{G_N})\geq\nu(w_G)
       =\nu(z(M))+\nu(w_{G\setminus M})                    \tag{5}
\]

for every `N`.  Thus `z(M)` has minimum valuation in its fibre.  If every
other term had strictly larger valuation, `z(M)` would be the unique minimum
in the zero sum (2), impossible by the ultrametric inequality.  Some
\(N\ne M\) therefore has \(\nu(z(N))=\nu(z(M))\), which gives (4).
Equation (3) makes the
reverse move literal. `QED`

Starting with the negative network supplied by the degree-nine residual and
then minimizing over all supported locally-rainbow networks preserves
negativity.  Lemma 1.1 shows that, whenever this minimum contains a usable
mixed matching, the mixed equation supplies motion only *along* the minimum
face, not below it.  A well-founded descent therefore needs an additional
order which is not a function of the entry valuations.

## 2. A thirteen-cell exact countermodel

Work over `Q` with the 2-adic valuation.  The nonzero aggregate cells are
listed below.  An omitted cell is zero.

\[
\begin{array}{c|c|c@{\qquad}c|c|c}
uv&(a,b)&A_{uv}^{ab}&uv&(a,b)&A_{uv}^{ab}\\ \hline
04&(0,0)&1/2 &12&(0,0)&1\\
35&(0,0)&1   &13&(0,0)&1\\
25&(0,0)&1   &05&(1,1)&1\\
14&(1,1)&1   &23&(1,1)&1\\
03&(2,2)&1   &15&(2,2)&1\\
24&(2,2)&1   &12&(2,1)&-1\\
35&(1,2)&1   &&&
\end{array}                                                \tag{6}
\]

The constant-colour fibres have precisely the following terms:

\[
\begin{array}{c|c|c}
a&\text{supported perfect matchings}&F_{a^6}\\ \hline
0&04|12|35,\quad04|13|25&1/2+1/2=1\\
1&05|14|23&1\\
2&03|15|24&1.
\end{array}                                                \tag{7}
\]

Select

\[
\begin{aligned}
 P_0&=04_{00}|12_{00}|35_{00},\\
 P_1&=05_{11}|14_{11}|23_{11},\\
 P_2&=03_{22}|15_{22}|24_{22}.                             \tag{8}
\end{aligned}
\]

Their union `U` is locally rainbow and

\[
                              w_U=1/2.                      \tag{9}
\]

It contains the mixed matching

\[
 R=04_{00}|15_{22}|23_{11},\qquad c=(0,2,1,1,0,2).         \tag{10}
\]

At this colouring the complete nonzero fibre consists of exactly

\[
 R,\qquad N=04_{00}|12_{21}|35_{12},                       \tag{11}
\]

with respective weights `1/2` and `-1/2`.  Hence `F_c=0` exactly.  If
\(Q=U\setminus R\), the selected-fibre rewrite is

\[
                 w_U+w_{Q\sqcup N}=1/2-1/2=0.             \tag{12}
\]

Both networks have valuation `-1`, and applying the same binomial fibre in
reverse returns from \(Q\sqcup N\) to `U`.

This plateau is global for the displayed support, not an artefact of a poor
choice of starting state.  The cell `04_00` is the only supported cell at
stub `(0,0)`, so every locally-rainbow network contains it.  It is also the
only cell of nonzero valuation.  Therefore every such network has valuation
exactly `-1`.  Direct enumeration finds four supported networks and checks
this assertion cell by cell.

Thus all of the following can hold simultaneously:

1. the three exact target normalizations `F_(a^6)=1`;
2. a negative, color-balanced, globally valuation-minimal degree-nine
   monomial;
3. an exact mixed coefficient equation containing a perfect matching of
   that monomial; and
4. no decrease at all under the resulting exact rewrite.

Only the unused mixed equations can possibly eliminate this configuration.
Any claimed descent must exhibit how several such equations interact; the
single-fibre ultrametric argument is false.

The unused equations are unusually sparse.  Of the 726 mixed colourings,
722 already vanish.  The four nonzero coefficients, each a singleton fibre,
are

\[
\begin{array}{c|c|c}
c&\text{unique supported matching}&F_c\\ \hline
(0,0,0,1,0,2)&04_{00}|12_{00}|35_{12}&1/2\\
(0,2,1,0,0,0)&04_{00}|12_{21}|35_{00}&-1/2\\
(1,0,2,0,2,1)&05_{11}|13_{00}|24_{22}&1\\
(2,1,0,2,1,0)&03_{22}|14_{11}|25_{00}&1.
\end{array}                                                \tag{13}
\]

The verifier enumerates all 729 fibres and checks that (13) is the complete
error list.

## 3. Why the degree-nine identity itself cannot be iterated

In the fixed balanced degree-nine multigrading, multiplying a mixed
coefficient `F_c` by a complementary degree-six monomial gives one column of
the complete Macaulay map `A`.  Consequently every finite sequence of
degree-nine mixed-fibre rewrites is an integral linear combination of the
columns of `A`.

The characteristic-two certificate gives

\[
                         P-Ax_0=2R.                         \tag{14}
\]

An iteration of the same kind to a second stage would imply

\[
                         P\in A\mathbb Z^{\mathcal C}
                                  +4\mathbb Z^{\mathcal R}. \tag{15}
\]

But the exact support-2,179 character from
`notes/degree9-bockstein-mod4.md` satisfies

\[
                    \lambda^TA=0\pmod4,\qquad
                    \lambda^TP=2\pmod4.                   \tag{16}
\]

It is therefore a finite certificate that (15) is impossible, independent
of the chosen first-stage characteristic-two lift.  The primitive integral
left-kernel functional in the same note further shows that the class of `P`
has a nonzero free component in the rational cokernel, so no unlimited
same-degree rewrite can remove it after changing coefficients.

The valuation plateau and the mod-four character close the two literal
versions of the proposed descent.  They do not rule out a higher-degree
radical identity or a new invariant of the simultaneous minimum-state
network.  Either of those would be genuinely additional input.

## 4. Repairing all four singletons does not lower the minimum

The four errors in (13) are not the global input needed by the proposed
descent.  They can all be repaired exactly without either changing a
constant coefficient or creating a locally-rainbow monomial below valuation
`-1`.

There is a particularly sharp completion.  Add eighteen cells to (6):

\[
\begin{array}{c|c@{\quad}c|c@{\quad}c|c}
01&(1,1)&(2,1)&02&(1,2)&(2,2)\\
03&(1,2)&&05&(2,1)&\\
13&(0,1)&&14&(1,2)&\\
15&(2,0)&&23&(1,0)&\\
24&(2,1)&&25&(0,2)&\\
34&(2,1)&(2,2)&35&(0,2)&(1,0)\\
45&(1,1)&(2,1)&&&
\end{array}                                                \tag{17}
\]

An exact MaxSAT optimization shows that eighteen is the minimum number of
added cells among supports containing the fixed thirteen cells of (6) and
having no mixed singleton.  More importantly, direct enumeration of the
displayed 31-cell support gives the complete fibre-size distribution

\[
                665\text{ empty fibres},\qquad
                 64\text{ two-term fibres}.                \tag{18}
\]

Thus every one of the 726 mixed fibres is either empty or binomial.

Here are exact weights which repair the four errors while retaining the old
cycle.  Put

\[
                         \epsilon=16,\qquad D=1+\epsilon^2=257. \tag{19}
\]

Initially give every new cell in (17) weight `epsilon`.  Make the following
changes:

\[
\begin{array}{c|c@{\qquad}c|c}
\text{cell}&\text{weight}&\text{cell}&\text{weight}\\ \hline
23_{11}&1/D&15_{22}&1/D\\
12_{21}&-1/D^2&13_{01}&-1\\
15_{20}&1/D^2&02_{12}&-1\\
01_{21}&-1&25_{02}&1\\
23_{10}&1&45_{21}&1\\
34_{21}&1&&
\end{array}                                                \tag{20}
\]

The first three entries in (20) replace their old weights from (6); the
others replace the default weight `epsilon` in (17).  Exact enumeration now
gives

\[
 F_{0^6}=F_{1^6}=F_{2^6}=1,                               \tag{21}
\]

and five exact mixed cancellations: the selected colouring (10) and all
four colourings in (13).  For example, their two-term values are

\[
\begin{array}{c|c}
(0,2,1,1,0,2)&-1/(2D^2)+1/(2D^2)\\
(0,0,0,1,0,2)&1/2-1/2\\
(0,2,1,0,0,0)&-1/(2D^2)+1/(2D^2)\\
(1,0,2,0,2,1)&-1+1\\
(2,1,0,2,1,0)&-1+1.
\end{array}                                                \tag{22}
\]

Only `04_00=1/2` has negative valuation.  Of the other thirty entries,
twenty are units and ten have valuation four.  Consequently no
locally-rainbow stub matching can have valuation below `-1`.  Complete
enumeration finds 336 locally-rainbow networks, of which 36 attain `-1`.
The selected state and its cancellation mate still have weights
`1/(2D^2)` and `-1/(2D^2)` and hence remain an exact two-cycle on that
minimum face.

This disproves the stronger repair dichotomy: even repairing **all four**
singleton errors need neither break a target normalization nor produce a
strictly lower balanced monomial.  Simultaneous equations enlarge the
minimum plateau; they do not orient it.

The completion is still not a Krenn counterexample.  Of its 61 supported
mixed binomials, 23 cancel under (19)--(20) and 38 do not.  Section 6 gives a
three-fibre certificate showing that no nonzero choice of weights on this
support can cancel all 61.

## 5. The degree-nine residual gives no four-state parity contradiction

The four locally-rainbow networks in the original thirteen-cell model are

\[
 U_R=P_0\sqcup P_1\sqcup P_2,\quad
 U_N=(U_R\setminus R)\sqcup N,\quad
 U'_R=S_0\sqcup P_1\sqcup P_2,\quad
 U'_N=(U'_R\setminus R)\sqcup N.                            \tag{23}
\]

Their weights are `(1/2,-1/2,1/2,-1/2)`.  The
\(R\leftrightarrow N\) rewrites give two
disjoint edges; the leading 2-adic relation between the two colour-zero
terms gives the other two edges of a square.  Hence the minimum graph is
bipartite before any coefficient calculation.

Mapping (23) into the saved first integral residual in (14) gives the four
exact row indices

\[
                 (430202,118509,430205,430203)              \tag{24}
\]

and residual coefficients

\[
                              (0,-1,-1,-1).                 \tag{25}
\]

This is consistent, not obstructive:

\[
 0(1/2)+(-1)(-1/2)+(-1)(1/2)+(-1)(-1/2)=1/2.              \tag{26}
\]

Modulo two, the three odd coefficients in (25) simply account for the odd
leading residue forced by `R(A)=1/2`.  They do not contradict a replacement
relation.  The coefficients also depend on the chosen first lift `x_0`, so
their restriction is not a certificate-independent graph invariant.

The no-singleton completion makes this diagnosis stronger.  Its complete
binomial replacement graph has 336 vertices and 736 edges, and exhaustive
breadth-first colouring proves it is bipartite.  Thus the degree-nine
identity supplies no odd replacement-cycle obstruction on either the
four-node minimum graph or its completed state space.  The mod-four
Bockstein character remains a valid obstruction to a second *polynomial
Macaulay lift*, but it does not localize to an odd cycle on these four
evaluated monomials.

## 6. A different three-fibre parity obstruction appears globally

Although the replacement graph is bipartite, the 31-cell support has a
three-fibre Laurent sign obstruction.  Consider the binomial fibres

\[
\begin{array}{c|l}
(1,0,0,2,1,1)&
03_{12}12_{00}45_{11}+05_{11}12_{00}34_{21}\\
(1,1,0,2,1,0)&
01_{11}25_{00}34_{21}+03_{12}14_{11}25_{00}\\
(1,1,1,0,1,1)&
01_{11}23_{10}45_{11}+05_{11}14_{11}23_{10}.
\end{array}                                                \tag{27}
\]

All displayed cells are nonzero.  Cancelling the common monomial in each
row would respectively force

\[
\begin{aligned}
 {03_{12}45_{11}\over05_{11}34_{21}}&=-1,\\
 {01_{11}34_{21}\over03_{12}14_{11}}&=-1,\\
 {01_{11}45_{11}\over05_{11}14_{11}}&=-1.                 \tag{28}
\end{aligned}
\]

But the left side of the third equation is the product of the first two
left sides.  The first two equations therefore make it `+1`, contradicting
the third.  In exponent notation, this is the exact dependency

\[
                              d_3=d_1+d_2                  \tag{29}
\]

with an odd sign requirement.

This certificate clarifies the boundary precisely.  Global collections of
mixed fibres can give a parity contradiction, but it need not be an odd
cycle in the locally-rainbow replacement graph and it is not supplied by
the four-node restriction of the degree-nine residual.  The obstruction in
(27)--(29) is a Laurent exponent dependency using three different fibres.

The exact audit of (17)--(29) is
`computations/verify_valuation_rainbow_plateau_completion.py`.
