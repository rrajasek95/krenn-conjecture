# Cubic transition invariants and the Petersen replacement

This note tests whether the selected-triple rewrite can be closed by a
standard invariant of its locally-rainbow cubic occurrence networks.  The
answer is negative for three natural and fairly broad candidates:

1. the Penrose epsilon contraction / proper 3-edge-colouring count;
2. the perfect-matching two-factor transition polynomial; and
3. every nontrivial multiplicative character of the endpoint-colour
   transitions.

The obstruction is exact and occurs on the prism-to-Petersen binomial
replacement from `notes/triple-matching-rewrite.md`.  The last class admits
a complete classification: universal replacement-neutrality forces the
character to have rank one, after which it is constant on *all*
locally-rainbow networks.

## 1. What compatibility with a binomial rewrite requires

Use the ten-vertex construction of the earlier note.  Write `U` for its
selected pentagonal prism and `U'` for the Petersen network obtained by
removing the mixed matching `R` and inserting its unique cancellation mate
`N`.  Their occurrence products are

\[
                         W(U)=1,\qquad W(U')=-1,           \tag{1}
\]

and the complete mixed fibre equation is simply

\[
                         W(U)+W(U')=0.                    \tag{2}
\]

Let `I` be a scalar state invariant intended to multiply every term in a
replacement relation.  On (2), the weighted relation is

\[
 I(U)W(U)+I(U')W(U')=I(U)-I(U').                         \tag{3}
\]

Consequently this one legal binomial rewrite forces

\[
                              I(U)=I(U').                 \tag{4}
\]

This is stronger than asking for a known nonzero covariance factor: an
invariant which vanishes on `U'` but not on `U` cannot cross this relation
at all.

Both networks carry more structure than an ordinary cubic graph.  Every
half-edge has its local occurrence colour in `{0,1,2}`, and the three
labels at every vertex are distinct.  On `U`, every edge joins equal
labels.  On `U'`, the new matching has three mismatched edges, of types
`01`, `12`, and `20`, as well as two equal-label edges.

## 2. The oriented Penrose contraction jumps from 30 to zero

Order the incident half-edges at each vertex by their local labels
`0,1,2`.  The natural Penrose tensor contraction is

\[
 \mathcal P(G)=
 \sum_{\phi:E(G)\to\{0,1,2\}}
 \prod_{v}\epsilon\bigl(
   \phi(e_{v,0}),\phi(e_{v,1}),\phi(e_{v,2})
 \bigr).                                                  \tag{5}
\]

Only proper 3-edge-colourings contribute.  Direct enumeration gives

\[
                         \mathcal P(U)=30,
             \qquad      \mathcal P(U')=0.                \tag{6}
\]

For completeness, the eleven perfect matchings of the prism split by the
cycle lengths of their complementary two-factors as

\[
\begin{array}{c|ccc}
\text{cycle lengths}&(10)&(4,6)&(5,5)\\ \hline
\text{number}&5&5&1.
\end{array}                                               \tag{7}
\]

The first two types have respectively two and four alternating
2-colourings of their complements, while the odd type has none.  This
gives `5*2+5*4=30` ordered proper edge-colourings.  With the displayed
local port orders every contribution has sign `+1`.  Each of the six
perfect matchings of Petersen instead has complementary cycle type
`(5,5)`, so Petersen has no proper 3-edge-colouring.

Thus the Penrose-weighted version of (2) is `30`, not zero.  In particular,
neither 3-edge-colourability, its signed Penrose refinement, nor any
invertible multiplicative normalization of it supplies a functional that
survives the selected rewrite through snarks.

## 3. The entire one-variable two-factor transition polynomial fails

Consider the perfect-matching transition polynomial

\[
              \Theta_G(x)=\sum_{M\in\operatorname{PM}(G)}
                                  x^{\kappa(G-M)},        \tag{8}
\]

where `kappa` is the number of cycles in the complementary two-factor.
The table above and the Petersen matching enumeration give

\[
              \Theta_U(x)=6x^2+5x,
       \qquad \Theta_{U'}(x)=6x^2.                       \tag{9}
\]

Their difference is `5x`.  Hence no nonzero specialization of (8) over
the complex numbers is replacement-neutral even on this single binomial
fibre.  The zero specialization also vanishes on the selected state and
cannot yield a contradiction.

The length-refined version

\[
 \Theta_G({\bf t})=
 \sum_M\prod_{C\text{ a cycle of }G-M}t_{|C|}             \tag{10}
\]

has the exact values

\[
\begin{aligned}
 \Theta_U({\bf t})  &=5t_4t_6+5t_{10}+t_5^2,\\
 \Theta_{U'}({\bf t})&=6t_5^2.
\end{aligned}                                             \tag{11}
\]

Thus this pair imposes the necessary equation

\[
                         t_{10}+t_4t_6=t_5^2.             \tag{12}
\]

The usual 3-edge-colouring specialization, `t_even=2` and `t_odd=0`,
violates (12) and recovers the jump `30 -> 0`.  The ordinary matching-count
specialization `t_l=1` also violates it (`11 -> 6`).  Equation (12) does
not by itself exclude specially tuned length-dependent loop weights, but
it rules out the standard one-parameter transition polynomial completely.

## 4. Edge-transition characters: an exact classification

Let `B=(B_ij)` be a symmetric `3 by 3` complex matrix.  For a locally
rainbow port-labelled network define

\[
             \chi_B(G)=\prod_{uv\in E(G)}
                    B_{\ell_u(uv),\ell_v(uv)}.            \tag{13}
\]

This contains all multiplicative signs depending only on the endpoint
colour type of an occurrence edge.  In particular, characters of the
mod-2 vector of transition-edge counts are obtained by taking
`B_ij` in `{+1,-1}`.

Call `B` **replacement-neutral** if, whenever a same-colour perfect
matching is removed, the product contributed by a new matching on those
fixed ports is independent of how the ports are paired.  The number of
ports of each colour is even in every such move.  We require the diagonal
entries to be nonzero, since otherwise (13) vanishes on the original
selected union of three constant matchings.

**Proposition 4.1.**  A symmetric edge-transition character with nonzero
diagonal is replacement-neutral for every selected-triple move if and only
if

\[
                              B_{ij}=a_i a_j               \tag{14}
\]

for three nonzero scalars `a_0,a_1,a_2`.  In that case

\[
                       \chi_B(G)=(a_0a_1a_2)^n             \tag{15}
\]

on every locally-rainbow network on `n` vertices, so the character is
completely graph-independent.

**Proof.**  Take four selected ports with colour multiset `(i,i,j,j)`.
Comparing the pairing within equal colours with either cross pairing gives

\[
                         B_{ii}B_{jj}=B_{ij}^2.            \tag{16}
\]

Next take the six-port multiset `(0,0,1,1,2,2)`.  Compare the three
equal-colour pairs with the matching having one edge of each cross type
`01,12,20`.  Neutrality gives

\[
                 B_{00}B_{11}B_{22}=B_{01}B_{12}B_{20}.  \tag{17}
\]

Choose square roots `d_i^2=B_ii`.  By (16), write
`B_ij=s_ij d_i d_j` with `s_ij` in `{+1,-1}`.  Equation (17) says
`s_01 s_12 s_20=1`.  Hence these signs are a vertex coboundary: after
putting `epsilon_0=1`, `epsilon_1=s_01`, and `epsilon_2=s_02`, one has
`s_ij=epsilon_i epsilon_j`.  Taking `a_i=epsilon_i d_i` proves (14).

Conversely, (14) makes the matching contribution on a fixed port set
equal to `product_v a_{c(v)}`, independently of its pairing.  Finally,
every locally-rainbow vertex has one endpoint of each label, so multiplying
over all edge endpoints gives (15). `QED`

The tempting mismatch-parity character illustrates the triangle condition
exactly:

\[
 B_{ii}=1,\qquad B_{ij}=-1\quad(i\ne j).                  \tag{18}
\]

It assigns `+1` to the selected prism and `-1` to its Petersen mate,
because the mate contains the cross-transition triangle `01,12,20`.
Consequently the character-weighted binomial relation is `1+1=2`, not
zero.  Proposition 4.1 says that every transition-count sign which avoids
this problem is a trivial port gauge and has the same value on every
locally-rainbow cubic graph.

## 5. A pinned vertex-model extension

There is a related no-go for the usual tensor-contraction construction of
graph polynomials.  Let a real tensor \(T\in
\mathbb R^q\otimes\mathbb R^q\otimes\mathbb R^q\) define

\[
 Z_T(G)=\sum_{\sigma:E(G)\to[q]}
        \prod_v T_{\sigma(e_{v,0}),\sigma(e_{v,1}),
                         \sigma(e_{v,2})},                \tag{19}
\]

with the positive-definite delta contraction along each edge.  Penrose is
the special alternating tensor.  Say that this model is **open-boundary
pinned replacement-neutral** if, after cutting the unchanged connections,
reconnection gives the same tensor even when arbitrary states are fixed
independently on all exposed unchanged half-edges.  This is the local form
of neutrality normally needed for a tensor-network skein rule; it is
stronger than equality of the unpinned closed partition functions.

**Proposition 5.1.**  Every nonzero open-boundary pinned
replacement-neutral real vertex model has a decomposable local tensor.  If
neutrality is required when the selected port may have any of the three
local labels, its three factor vectors are collinear and the closed
partition function is graph-independent at fixed order.

**Proof.**  Select the first port at four vertices and pin the other two
states.  A pin \((b,c)\) exposes the slice vector

\[
                     x_{bc}=(T_{abc})_{a=1}^q.            \tag{20}
\]

For four choices \(x_1,x_2,x_3,x_4\), the three possible reconnections of
the selected ports have contraction factors

\[
\begin{split}
 \langle x_1,x_2\rangle\langle x_3,x_4\rangle,\qquad
 \langle x_1,x_3\rangle\langle x_2,x_4\rangle,\qquad
 \langle x_1,x_4\rangle\langle x_2,x_3\rangle.            \tag{21}
\end{split}
\]

Neutrality makes them equal for every four slices.  These are precisely
the vanishing \(2\) by \(2\) minors of the Gram matrix of all mode-one
slices.  It therefore has rank at most one.  Positive definiteness says
that the slices themselves span a space of dimension at most one, so the
mode-one flattening of \(T\) has rank one.  Applying the same argument to
the other two ports shows that \(T=a\otimes b\otimes c\).

If selected ports of different local labels may be paired, the same
four-port test applies to the Gram matrix of the three factor vectors
\(a,b,c\); it too has rank one.  Positive definiteness makes them
collinear.  Write them as \(a=\lambda_0h\),
\(b=\lambda_1h\), and \(c=\lambda_2h\).  On an \(n\)-vertex
locally-rainbow network the closed contraction is then

\[
       Z_T(G)=
       \langle h,h\rangle^{3n/2}
       (\lambda_0\lambda_1\lambda_2)^n,                  \tag{22}
\]

independent of the graph, proving the last assertion. QED

The open-boundary qualification is essential: Proposition 5.1 does not
claim that accidental equalities of two closed partition functions force
a local tensor to decompose.  It does show why the standard local
tensor/skein upgrade of the Penrose scalar cannot work.  The epsilon tensor
has mode rank three, while open-boundary local reconnection-neutrality
forces mode rank one.  Explicitly, its slices
\(x_{12}=e_0\) and \(x_{20}=e_1\) give the four-port contractions
\(\langle e_0,e_0\rangle\langle e_1,e_1\rangle=1\) and
\(\langle e_0,e_1\rangle^2=0\) for two reconnections.

The exact scope of Proposition 5.1 is worth keeping explicit.  It covers
scalar finite-state vertex models with

1. one real local tensor and the Euclidean delta edge contraction;
2. equality as an **open-boundary tensor identity**, not merely after
   closing or summing the unchanged legs; and
3. termwise neutrality under every pairing of the selected ports, for all
   three local port labels.

It therefore applies to a proposed local Penrose/transition skein
multiplier.  It does **not** cover a complex bilinear contraction with
isotropic slice spaces, an identity which appears only after the entire
matching fibre is summed, a vector-valued or homological invariant, or a
closed state sum whose equality is accidental and graph-global.  Over a
complex bilinear form the proof stops at “the slice Gram matrix has rank at
most one”: a higher-dimensional totally isotropic part can remain, so
positive definiteness cannot simply be omitted.

## 6. Consequence for the selected-triple route

The locally-rainbow port labels do let one extend a nonzero scalar to
Petersen and other snarks—for instance the constant character.  What they
do not provide is a discriminating scalar compatible with all matching
replacements.  Penrose and two-factor state sums distinguish the selected
source from Petersen but therefore fail to multiply the exact binomial
relation.  Multiplicative transition characters can multiply every
relation only when they are rank-one gauges, in which case they distinguish
nothing.

Accordingly a successful cubic-network continuation cannot be a scalar
Penrose evaluation, a one-variable circuit-count transition polynomial, or
a cycle-space sign built from endpoint transition counts.  It would need a
higher object whose *sum over an entire replacement fibre* obeys a new
identity, rather than a state-by-state scalar multiplier.

The dependency-free audit is
`computations/verify_cubic_transition_invariant_obstruction.py`.
