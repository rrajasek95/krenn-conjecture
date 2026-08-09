# N=8 balanced-anchor chart cover: finite outer layer and sharp trinomial gate

## Result

Choose one nonzero perfect-matching monomial from each of the three pure
coefficients of a hypothetical exact `N=8` source.  Their twelve
endpoint-colour cells form three labelled perfect matchings

\[
                         Q_0,Q_1,Q_2.                       \tag{1}
\]

The exact checker
[`verify_n8_balanced_anchor_chart_cover.py`](../computations/verify_n8_balanced_anchor_chart_cover.py)
establishes the following bounded outer cover.

1. Triples (1) have 86 orbits under `S8` with the colours fixed, and 31
   orbits under `S8 x S3`.  They have 18 coarse
   overlap/multiplicity/component signatures.
2. Modulo the twelve anchor characters, the target-torus character quotient
   has dimension 12.  Every one of the other 240 endpoint-colour cells lies
   in a positive anchor-relative circuit using either two or three nonanchor
   cells.  Adding all twelve anchors gives an explicitly strictly balanced
   support of size at most 15 through any prescribed cell.
3. Every anchor orbit already has a mixed singleton monomial.  Across the 31
   representatives the number of such mixed anchor monomials ranges from 2
   to 78.  Full exactness forces a supported same-colour alternating `C4` or
   `C6` cancellation pattern for each one.
4. The sharpest orbit has only two mixed anchor monomials, and their complete
   full-source coefficient equations are two explicit trinomials.  They are
   unaffected by any other endpoint matrices.

This is not yet the requested global source-chart cover.  It proves that
the moment polytope supplies a finite local outer cover, and identifies the
smallest source-ideal gate that must be closed next.  It also proves that
moment balance alone is far too permissive.

## 1. Aggregate cells and the cubic anchor multigraph

For each colour `i`, the pure coefficient is one.  At least one of its
perfect-matching monomials is therefore nonzero; call its physical matching
`Q_i`.  Its four source cells are `(uv;i,i)`.  The union of the three
matchings is a 3-edge-coloured cubic multigraph on the eight physical sites.
If two colours choose the same physical pair, their cells remain distinct
because their endpoint colours differ.  Genuine parallel graph edges with
the same endpoints and endpoint colours have already been summed into one
aggregate cell.

All cells use canonical endpoint order `u<v`.  Thus mixed cells keep the
colour at `u` in the first slot and the colour at `v` in the second slot;
none of the orbit or character calculations silently symmetrizes an
asymmetric matrix entry.

Fix

```text
Q0 = {01,23,45,67}.
```

Its vertex stabilizer has order `2^4 4! = 384`.  Exact traversal of its
action on the `105^2` choices of `(Q1,Q2)` gives 86 ordered orbits.  A second
exact quotient by colour permutations leaves 31.  Eight representatives
have twelve distinct physical edges and hence are simple cubic graphs; four
have girth three and four have girth four.  Every other representative has
a repeated physical pair.

## 2. Moment-polytope circuits

The twelve pure-anchor characters are independent in the 24-dimensional
ambient port lattice.  Their span contains the three target characters,
because

\[
                  \sum_{e\in Q_i}a_{(e;i,i)}
                    =\sum_v e_{v,i}.                        \tag{2}
\]

The relative target-character quotient consequently has dimension
`24-12=12`.

There are 240 cells outside the anchors.  For every one of the 31 anchor
orbits their quotient characters are all distinct.  The exact positive
circuit census is:

| cells requiring three nonanchors | anchor orbits | remaining cells using two |
|---:|---:|---:|
| 24 | 8 | 216 |
| 22 | 4 | 218 |
| 20 | 6 | 220 |
| 18 | 4 | 222 |
| 16 | 4 | 224 |
| 14 | 1 | 226 |
| 12 | 2 | 228 |
| 8 | 1 | 232 |
| 0 | 1 | 240 |

For a two-cell circuit the two exact quotient rays are opposite with
positive rational coefficients.  For a three-cell circuit the checker
verifies a literal unit relation `q_s+q_t+q_u=0`.  It then lifts each
relation back to the port lattice.  On each `Q_i` edge the extra incidence
at the two endpoints agrees; choosing a target degree larger than these four
edge incidences gives positive weights on all twelve anchors and constant
port degree in each colour.  Thus the asserted 14- or 15-cell support is
strictly target-torus balanced, not merely quotient-dependent.

There is also an intrinsic bound inside any hypothetical polystable support
`S` containing the anchors.  Write `q_s` for the nonanchor quotient
characters.  A positive balance on all of `S` gives

\[
                         \sum_{s\in S-Q}\alpha_s q_s=0,
                         \qquad \alpha_s>0.                 \tag{3}
\]

Fix one nonanchor `s`.  Equation (3) puts `-q_s` in the positive cone of the
other quotient characters.  Conic Caratheodory in dimension 12 uses at most
12 of them.  Lifting as above gives, **inside `S`**, a strictly balanced
sub-support containing `s`, all twelve anchors, and at most thirteen
nonanchors: at most 25 cells total.

This does not let us delete the rest of `S`.  Full matching coefficients do
not pass from a source to a balanced sub-support.  The result is a finite
moment-chart cover, not a source-ideal descent.  The stronger ambient
15-cell census makes the adversarial point especially clear: almost any
coordinate can be embedded in a tiny balanced anchor chart.

## 3. The mixed-fibre condition that balance omits

A perfect matching assembled from coloured anchor edges determines its
output colouring.  For that fixed colouring it is the **unique** matching
using only anchor cells: within colour `i`, every vertex can only use its
`Q_i` partner.  Hence every mixed anchor matching contributes a nonzero
singleton monomial before other source cells are admitted.

The 31 orbit representatives contain 404 such mixed anchor matchings, with
colour-class profiles

| profile | occurrences among representatives |
|---|---:|
| `(6,2,0)` | 162 |
| `(4,4,0)` | 110 |
| `(4,2,2)` | 132 |

These are representative counts, not orbit-size-weighted counts.

If the full source were exact, the corresponding mixed coefficient would
be zero.  Since its anchor monomial is nonzero, at least one other supported
perfect matching with the same colouring must occur.  The symmetric
difference of the two matchings is a disjoint union of alternating even
cycles, and every cycle is contained in a single colour class.  At `N=8` a
mixed colour class has size at most six.  Therefore at least one supported
alternating cycle is a `C4` or `C6`, using respectively two or three
nonanchor same-colour cells.

This implication is source-faithful and allows arbitrary complex
cancellation: it only uses that a nonzero monomial cannot sum to zero with
no other monomial.  It does not assume positivity or that the eventual
coefficient is binomial.  The multi-mate fibres are exactly where a Laurent
or Koszul identity is still needed.

## 4. The sharp two-trinomial orbit

Two anchor orbits have only two mixed anchor matchings.  The sharper one is

```text
Q0 = {01,23,45,67}
Q1 = {02,14,36,57}
Q2 = {03,15,27,46}.
```

Its two mixed colourings have profile `(4,2,2)`.  For each colouring there
are exactly three compatible physical perfect matchings in the complete
graph: the anchor matching and two possible cancellation mates.  Write
`x_uv^i=A_uv(i,i)`.  Cancelling the nonzero common anchor factors gives the
literal full-source equations

\[
 x_{01}^0x_{23}^0+x_{02}^0x_{13}^0+x_{03}^0x_{12}^0=0,     \tag{4}
\]

\[
 x_{01}^0x_{45}^0+x_{04}^0x_{15}^0+x_{05}^0x_{14}^0=0.     \tag{5}
\]

No other source coordinate can enter these two output words.  The first
terms in (4)--(5) are nonzero anchor products.  Thus (4) forces at least one
of the two replacement pairs `{02,13}`, `{03,12}`, and (5) forces at least
one of `{04,15}`, `{05,14}`.  In particular every exact source in this
anchor chart has at least four specified additional colour-zero cells,
arranged as two overlapping four-site hafnian gates.

Equations (4)--(5) are consistent by themselves, so they are a gate rather
than a contradiction.  The next bounded source-ideal task is now precise:
branch over their four pair choices, retain every newly created mixed
coefficient, and seek a Laurent unit or a small Koszul circuit.  This is a
four-branch calculation on a full-source consequence, not an unrestricted
support enumeration.  The other two-mixed-fibre orbit has profile `(4,4,0)`
and eight possible mates per fibre, so (4)--(5) is the preferred first chart.

## 5. Uniform high-girth counterguard

The small `N=8` overlap census cannot be promoted to all even orders using
pure cubic-graph combinatorics.  The checker contains two exact guards.

First, the Heawood incidence graph on 14 vertices is the union of three
disjoint perfect matchings, has girth six, and every two-colour union is one
14-cycle.

More decisively, an explicit 11-fold cyclic voltage cover of that graph has
154 vertices.  Its frozen 21 voltages give three disjoint perfect matchings
whose union is connected, simple, cubic, and has girth ten.  Every two-colour
union is one Hamilton 154-cycle.  Hence it has no common anchor pair and no
anchor cycle of length 4, 6, or 8.  It nevertheless has an explicit mixed
anchor matching obtained by flipping a ten-cycle, with colour profile
`(144,8,2)`.  Thus the mixed source equations are nonvacuous, but pure
anchor combinatorics cannot bound the cancellation cycle.

This is a support countermodel, not an exact GHZ source.  It establishes the
correct uniform stopping rule: any all-even chart-cover theorem must use the
mixed-fibre coefficient ideal (or a non-torus source operation), not only a
short cycle in the three-coloured cubic anchor graph.

## Scope and next decision

The result gives a complete finite outer layer for `N=8` and a universal
25-cell moment witness bound through every cell of a polystable anchored
support.  It does not yet show that these witness sub-supports inherit
exactness, map automatically into D1/D2/P5, or admit a non-torus reduction
to the GHZ-empty `ece62cf` germ.

The next admissible bounded test is the four-branch closure of (4)--(5).
Stop that branch if a completion introduces an unbounded multiterm fibre
without a reusable Laurent/Koszul circuit; otherwise promote the resulting
finite certificate as the first genuine source-ideal member of the global
balanced chart cover.
