# Two cross edges break the one-controller contraction

## Outcome

The one-cross-edge theorem is sharp.  For the forced-pair lift from N=8 to
N=10, two cross coordinates already produce a symbolic term which no
single old-vertex controller can absorb on a candidate fourth cut.  The
smallest explicit witness is

\[
       A_{10}(t,s)=A_8\otimes g_{89}
              +tE_{08;00}+sE_{19;00}.                 \tag{1}
\]

For each of the candidate cuts \(z=0,1,5\), and for every possible old
controller on that cut, the mixed \(ts\) full-residual coefficient has a
nonzero exact normal form modulo the old N=8 cofactor cylinder.  This is a
counterexample to extending the controlled contraction theorem across two
arbitrary cross edges.  It is **not** a counterexample to Krenn's
conjecture, and it does not assert that (1) has four complete N=10 cuts.

The correct stopping decision is therefore structural: do not enumerate
two-cross coefficient values.  Any N-to-N+2 induction must add an invariant
which controls the quadratic matching of both new vertices outward, rather
than relying on one local colour trace.

## 1. Finite topology and colour census

There are 144 cross coordinates

\[
       (v,n;\alpha,\beta),\qquad
       v\in\{0,\ldots,7\},\ n\in\{8,9\},\
       \alpha,\beta\in\{0,1,2\}.
\]

Their unordered pairs have the following exact topology census.

| new endpoints | old endpoints | pairs | quadratic full term possible? |
|---|---|---:|---|
| same | shared | 576 | no |
| same | distinct | 4,536 | no |
| opposite | shared | 648 | no |
| opposite | distinct | 4,536 | **yes** |
| **total** |  | **10,296** | **4,536** |

The criterion in the last column is forced by matching incidence.  If the
new endpoint is shared, the two sources cannot both occur.  If an old
endpoint is shared, that old vertex cannot be matched twice.  With opposite
new endpoints and distinct old endpoints, both cross sources can occur and
the two new vertices match outward.

The endpoint-colour refinement is also finite:

| colour relation | pairs |
|---|---:|
| new-end colours distinct | 6,912 |
| new-end colours equal and match neither old-end colour | 1,488 |
| new-end colours equal and match exactly one old-end colour | 1,536 |
| new-end colours equal and match both old-end colours | 360 |

Inside the quadratic-capable topology, 3,024 pairs have unequal new-end
colours.  The controlled diagonal trace kills their quadratic term
immediately.  There are 168 fully compatible pairs in which both old-end
colours and both new-end colours agree.  Equation (1) is the lexicographically
first such pair.  These colour relations are a census, not claimed orbit
equivalences: the anchored N=8 source breaks most vertex and colour
symmetries.

## 2. Exact symbolic calculation

The matching and cofactor polynomials are multiaffine in \(t,s\).  The
checker reconstructs their four coefficients from

\[
                (t,s)=(0,0),(1,0),(0,1),(1,1),          \tag{2}
\]

using exact rational arithmetic.  These are coefficient corners, not a
search grid.  The linear full-tensor coefficients vanish, just as in the
one-cross theorem, while the mixed coefficient is nonzero and has support
three.  Every supported word has colours zero at vertices 0, 1, 8, and 9,
as dictated by the two cross sources.

For a cut \(C_z=\{z,6,7\}\), write

\[
 U_8=\{0,\ldots,5\}\setminus\{z\},\qquad
 U_{10}=U_8\cup\{8,9\}.
\]

For every controller \(a\in U_8\), the checker applies the same controlled
trace \(P_a\) as the forced-pair and one-cross notes.  It reduces every
contracted coefficient modulo the exact row-echelon basis of the old N=8
insertion columns.  The resulting controller census is:

| cut \(z\) | controllers containing all nonconstant cofactor coefficients | controllers also containing all nonconstant residual coefficients |
|---:|---|---|
| 0 | 1, 4, 5 | none |
| 1 | 0, 4, 5 | none |
| 2 | 0, 1, 3, 5 | 0, 1, 3, 5 |
| 3 | 0, 1, 5 | 0, 1, 5 |
| 4 | 5 | 5 |
| 5 | none | none |

Thus each of the old active cuts \(z=2,3,4\) still admits a controller under
which all symbolic directions descend.  No candidate fourth cut does.  On
cuts 0 and 1 there are controllers for which all new-hole cofactor
directions do lie in the old cylinder, but the quadratic full-residual term
does not.  Cut 5 is sharper: no controller simultaneously absorbs the two
linear new-hole cofactor families, and the quadratic residual obstruction
also survives.

For every controller on \(z=0,1,5\), the checker records a boundary row whose
mixed \(ts\) contraction has nonzero quotient remainder.  This is an exact
coefficientwise certificate over \(\mathbb Q[t,s]\): rescaling two nonzero
weights cannot make the \(ts\) coefficient itself vanish.  The checker does
not exclude a special-value cancellation between that coefficient and the
constant old residual; that is the separate actual-cylinder problem which
would have to be solved before claiming an N=10 counterexample.

## 3. What the failed theorem teaches us

The forced-pair contraction worked because both appended colours could be
tied to one old controller.  One cross edge could be tied to its own old
endpoint, and parity removed it from the full tensor.  With two outward
edges at different old endpoints, these two simplifications fail together:

1. the two new vertices now participate in a full perfect matching;
2. their quadratic coefficient correlates two distinct old endpoints; and
3. one controller cannot, in general, impose both endpoint-colour
   conditions while preserving the old cylinder.

Consequently, a viable induction needs at least a two-controller or
four-point identity which retains the correlation of the two old endpoints.
Equivalently, it needs an invariant of the quadratic outward-matching
coefficient before taking the local trace.  Further enumeration of the 168
fully compatible pairs, or sampling their weights, would not repair the
failed one-controller statement.

This negative result is still useful for the finite-versus-border program.
It is source-faithful and is expressed in literal cofactor maps, not in the
output tensor alone.  It says exactly where the finite N-to-N+2 contraction
loses information.  It does not produce a border-only obstruction and does
not settle whether a different four-cylinder identity survives uniformly in
N.

## Reproduction

    python3 computations/verify_n10_two_cross_edge_contraction_frontier.py
    python3 -O computations/verify_n10_two_cross_edge_contraction_frontier.py
    python3 -I computations/verify_n10_two_cross_edge_contraction_frontier.py
    python3 -S computations/verify_n10_two_cross_edge_contraction_frontier.py

The checker performs exact perfect-matching expansions and exact rational
span reduction throughout.
