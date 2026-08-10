# The exact anchor-preserving initial frontier of the Segre--K4 chart

## Result

Let (H) be the fixed fourteen-cell Segre--K4 quadratic and let the
forty-five diagonal cells `00`, `11`, `22` remain arbitrary.  Consider a
literal word-diagonal one-parameter change

\[
                         x_i^a\longmapsto t^{u_{ia}}x_i^a .
\]

Require the fourteen cells of (H) and one supported pure-`00` perfect
matching to have weight zero.  This is the necessary affine initial-form
condition for retaining both (H) and a monomial of the unary anchor
(q^{[3]}=X_0).

The exact site/colour incidence quotient has two sharply different cases.

1. If the retained pure matching contains the distinguished physical edge
   `01`, exactly four outside mixed directions have forced weight zero:

   ```text
   23:21  25:21  34:12  45:21.
   ```

   Every one of the sixteen subsets of this four-cell face gives a unit
   top ideal over (mathbb Q), with the full forty-five diagonal variables
   still arbitrary.  Exact source lifts verify all sixteen cases.

2. If the retained pure matching avoids `01`, exactly twenty-four outside
   mixed directions have forced weight zero:

   ```text
   02:02 02:10 02:12 02:20  03:01 03:10 03:20 03:21
   04:02 04:10 04:12 04:20  05:01 05:10 05:20 05:21
   12:02 13:01 14:02 15:01  23:21 25:21 34:12 45:21.
   ```

   This is the first exact simultaneous-deformation guard.  Mere
   common-(q) provenance does not make these directions higher order, so
   the existing 45-variable and one-cell units do not imply a chart cover.

The checker is
`computations/verify_n8_one_bad_segre_cube_anchor_initial_cover.py`.

## Complete incidence criterion in the through-`01` chart

For the canonical retained anchor `01|23|45`, the nonzero quotient classes
have one exceptional opposite pair.  Write

```text
A = {
  02:02,02:10,02:12,02:20, 03:01,03:10,03:20,03:21,
  04:02,04:10,04:12,04:20, 05:01,05:10,05:20,05:21
}
B = {12:02,13:01,14:02,15:01}.
```

Two explicit integral cocharacters prove the full alternative.  Listed as
the three colour weights at sites (0,ldots,5), they are

\[
\begin{aligned}
u_A={}&(-1,-1,-1),(1,2,2),(0,2,0),(0,0,2),(0,2,0),(0,0,2),\\
u_B={}&(1,1,1),(-1,1,1),(0,2,0),(0,0,2),(0,2,0),(0,0,2).
\end{aligned}
\]

Both vanish on (H), on `01|23|45` in colour zero, and on the four forced
zero directions.  The first is strictly positive on every other outside
mixed cell except (A), where it is (-1); the second has the analogous
property with (B).  Conversely, for every (ain A,bin B),

\[
             \operatorname{inc}(a)+\operatorname{inc}(b)
       \in \langle\operatorname{inc}(H),
                 \operatorname{inc}(01{:}00),
                 \operatorname{inc}(23{:}00),
                 \operatorname{inc}(45{:}00)\rangle .
\]

Hence no cocharacter fixing the retained face can make both (a) and
(b) strictly positive.  This proves, without a cardinality search:

\[
\boxed{
\begin{gathered}
\text{through-`01` anchor and no simultaneous }A/B\text{ support}\\
\Longrightarrow \text{degeneration to one of the sixteen unit faces}.
\end{gathered}}
\]

Thus a hypothetical packet in this anchor chart must carry at least one
cell from each of (A) and (B).  Those are genuine simultaneous
directions; the thirty-two two-cell (A/B) charts happen to be unit, but
arbitrary further mixed cells can contaminate their source lifts, so that
observation is not promoted here as an all-support descent.

## What this says about the proposed chart cover

The new 45-variable and all one-cell units are mathematically sound, but
full common-(q) one-bad provenance does **not yet** force their hypotheses
as an initial form.  One still needs either

- a provenance theorem selecting a unary anchor matching through the
  repeated carrier edge and excluding simultaneous (A/B) support; or
- a coefficient theorem closing the twenty-four-cell zero face when the
  unary anchor avoids that edge.

The second item is the precise anchor-preserving simultaneous-deformation
counterguard.  It is an exact incidence face, not a claimed coefficient
point or a Krenn counterexample.  The checker deliberately does not infer
emptiness from the unsuccessful exploratory standard-basis attempt on the
whole face.

## Reproduction

```sh
.venv/bin/python computations/verify_n8_one_bad_segre_cube_anchor_initial_cover.py
.venv/bin/python -O computations/verify_n8_one_bad_segre_cube_anchor_initial_cover.py
```
