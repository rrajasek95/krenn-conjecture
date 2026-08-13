# A trapped fan carrier is a complete labelled basis/circuit problem

## Scope correction from the actual endpoint expansion

The abstract linear alternative below remains valid for a supplied complete
matrix `J_T`, but its old physical interpretation was too strong.  The
actual fixed-common-`q` audit shows that unary endpoint derivatives vanish,
the four response blocks are physical, and selected-anchor borders are
protection constraints rather than automatically physical source rows.
Consequently “transverse” below means transverse in the **bordered** map,
and the final row-space selector is a complete-map dual.  It is a physical
response/Fitting dual only if the selector already lies in the row span of
the four-response submap.  Otherwise it is the sharp surviving protection
covector.  See
[`h3-trapped-carrier-actual-endpoint-map-boundary.md`](h3-trapped-carrier-actual-endpoint-map-boundary.md).

## Result

There is a direct Route-A alternative for the saturated active-fan coloop
packet which does not assume the open Gate-I comparison `Phi`.

Fix one sequential endpoint fibre and let

\[
                    J_T:X_T\longrightarrow Y_T                 \tag{1}
\]

be its **complete labelled endpoint map**.  Its domain contains every
effective literal endpoint-coordinate column in the saturated trapped
packet.  Its codomain retains the complete diagonal and crossed response
coefficient rows, unary and target rows, protected word/head/orientation
rows, and every selected physical-anchor row.  Rows which vanish on both
the packet and the right-hand side, and columns which vanish identically on
this whole map, may be removed; no other projection is allowed.

Let `b=J_T x` be the value of the current physical endpoint row.  Thus the
fibre is nonempty before any line-hitting claim.  Choose `x` of minimum
support `B`.  Then the columns indexed by `B` are independent, and exactly
one of four outcomes occurs.

1. `|B|=1`: the fibre meets a literal target-coordinate line.
2. Some effective column outside `B` is transverse to `span(J_T|B)`: this
   raises bordered complete-map rank.  It is a physical response/Fitting
   carrier only if it already raises the response-submap rank.
3. Every outside column lies in that span and at least one exists: its
   fundamental circuit is a nonzero complete-column dependence.  Because
   the selected-anchor protection rows are part of (1), the relation is
   anchor-safe.
4. `B` is the entire effective packet: `J_T` has full column rank.  Every
   occupied literal coordinate selector satisfies

   \[
                     e_j^*=\lambda_j J_T,\qquad
                     \lambda_j(b)=x_j\ne0.             \tag{2}
   \]

   This is a localized complete-map row dual.  When its multiplier uses a
   selected-anchor protection row, it is not yet a physical source pivot.

Checker:
[`verify_h3_trapped_carrier_complete_labelled_fibre_alternative.py`](../computations/verify_h3_trapped_carrier_complete_labelled_fibre_alternative.py).

## Proof

Minimum support makes `J_T|B` injective: a kernel relation supported on `B`
would translate `x` while deleting an occupied coordinate.  If the support
has one element, outcome 1 holds.

Now take another effective column `c`.  If `c` is outside the span of the
basis columns, adjoining it raises complete labelled rank, giving outcome
2.  Otherwise write

\[
                         c=\sum_{j\in B}a_jc_j .       \tag{3}
\]

Then

\[
                         e_c-\sum_{j\in B}a_je_j       \tag{4}
\]

lies in `ker J_T`.  It preserves every response, target, protected, and
anchor row retained in (1), so (4) is the required anchor-safe complete-
column dependence.

If no further effective column exists, the whole map has full column rank.
Its row space is the full coordinate dual of `X_T`, proving (2).  Since
`b=J_Tx`, equation (2) reads `x_j` on the fibre value.  This is precisely
the literal-coordinate row-space alternative for the supplied complete
map.  The later actual-map audit separates physical response rows from
protection rows; only a selector in the former row span is a physical
source pivot.

There is therefore no fifth finite-dimensional branch.

## Composition with Hall saturation

First insert every source-certified carrier reachable inside the current
`K6` Galois closure.  A physical column with a hole outside the closure is
already the strict-growth outcome of `32e07b5`.  If all holes remain
trapped, apply the theorem to (1) once.

```text
complete trapped endpoint fibre
        |
        +-- support one ------------> target-coordinate access
        +-- transverse column ------> bordered rank; test physical submap
        +-- in-span extra column ---> anchor-safe fundamental circuit
        `-- no extra column --------> localized complete-map row dual
```

The same argument is applied to the left fibre and then to the recomputed
right fibre, exactly as in the sequential joint-kernel theorem.  Anchor
safety is not inferred afterward: it is built into `J_T` by bordering the
map with all selected anchor rows before taking a basis.

This gives a direct alternative to the `0c7b112` route through a fan-grade
odd comparison.  The comparison remains useful for canonical transport and
terminal reuse, but it is not a hypothesis of the basis/circuit theorem.

## What the later actual-map audit exposes

The scalar identity from `32ce01c`,

\[
                       \alpha U_i-d_iV_i=\alpha,       \tag{5}
\]

is only one evaluated projection of (1).  It proves a physical nonzero
pure/mixed omit-coloop carrier and fixes its common `q`, endpoint,
orientation, word, and remote tail.  It did not by itself publish the
matrix entries of the unary, crossed, and protection rows.

That distinction is sharp.  The checker holds the visible scalar row fixed
and supplies complete hidden-row extensions realizing target-coordinate
access, complete-column dependence, and transverse rank.  Thus (5) cannot
choose the branch.

The later endpoint-map theorem performs that expansion.  Unary derivatives
are zero on fixed-`q` endpoint columns; all four response blocks have the
explicit common-cofactor formula; and selected marked-anchor constraints
are coordinate-selector borders.  Exact rank therefore decides the
constrained endpoint packet without Gate-I `Phi`.  The remaining caveat is
that a bordered selector need not be a physical source dual: it may require
the protection row.  That branch needs an actual source realization of the
selector or extension by simultaneous `q`-deformation columns.

There is already concrete evidence that the omitted rows close rather than
create a new branch.  The frozen two-response guard

\[
                         C_0=X_1+Y,\qquad C_1=-Y
\]

has no coordinate-line point in that projection.  Commit `5ba50c8` imposes
its actual full one-bad packet and finds

\[
                         q^{[3]}[000000]-1=-1.
\]

Hence the ordinary certificate `-(q^[3][000000]-1)=1` kills that entire
fixed `q` fibre before Hall concentration.  The standard affine guard is
therefore not a surviving full-packet obstruction; an arbitrary trapped
carrier must use a different, unary-compatible complete map.

## Scope and verification

This is an exact basis/circuit/cocircuit theorem.  The later actual-map
audit supplies the fixed-`q` matrix and corrects its physical scope.  This
note does not claim that a dual using a protection row is a terminal.

Run:

```text
python3 computations/verify_h3_trapped_carrier_complete_labelled_fibre_alternative.py
python3 -O computations/verify_h3_trapped_carrier_complete_labelled_fibre_alternative.py
python3 -I -S computations/verify_h3_trapped_carrier_complete_labelled_fibre_alternative.py
```

Frozen ledger SHA-256:

```text
72be8a2405e1ac55cb4c6d624e95d149b9699a28a72d3e517d27ab9ff7be3d14
```
