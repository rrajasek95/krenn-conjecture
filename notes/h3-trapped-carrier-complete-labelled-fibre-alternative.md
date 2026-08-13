# A trapped fan carrier is a complete labelled basis/circuit problem

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
   is a typed complete-rank/Fitting carrier.
3. Every outside column lies in that span and at least one exists: its
   fundamental circuit is a nonzero complete-column dependence.  Because
   the physical anchor rows are part of (1), the relation is anchor-safe.
4. `B` is the entire effective packet: `J_T` has full column rank.  Every
   occupied literal coordinate selector satisfies

   \[
                     e_j^*=\lambda_j J_T,\qquad
                     \lambda_j(b)=x_j\ne0.             \tag{2}
   \]

   This is a localized physical row dual/source pivot, not an occurrence
   covector.

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
the literal-coordinate row-space alternative isolated in the complete-
source lift theorem: on an exhaustive physical packet it is a source
pivot, not merely a quotient diagnostic.

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
        +-- transverse column ------> typed rank/Fitting exit
        +-- in-span extra column ---> anchor-safe fundamental circuit
        `-- no extra column --------> localized physical row dual
```

The same argument is applied to the left fibre and then to the recomputed
right fibre, exactly as in the sequential joint-kernel theorem.  Anchor
safety is not inferred afterward: it is built into `J_T` by bordering the
map with all selected anchor rows before taking a basis.

This gives a direct alternative to the `0c7b112` route through a fan-grade
odd comparison.  The comparison remains useful for canonical transport and
terminal reuse, but it is not a hypothesis of the basis/circuit theorem.

## What is still not exposed

The scalar identity from `32ce01c`,

\[
                       \alpha U_i-d_iV_i=\alpha,       \tag{5}
\]

is only one evaluated projection of (1).  It proves a physical nonzero
pure/mixed omit-coloop carrier and fixes its common `q`, endpoint,
orientation, word, and remote tail.  It does not publish the matrix entries
of the unary, second-colour crossed, and physical-anchor rows.

That distinction is sharp.  The checker holds the visible scalar row fixed
and supplies complete hidden-row extensions realizing target-coordinate
access, complete-column dependence, and transverse rank.  Thus (5) cannot
choose the branch.

The smallest remaining physical audit is now:

> Expand the actual unary plus four-response endpoint columns of the
> saturated carrier packet in their common labelled `q` grade, border them
> with the selected physical-anchor rows, and verify that this is the
> exhaustive allowed endpoint-perturbation map `J_T`.

Once those entries are exposed, the theorem above decides the trapped
packet by exact rank; no protected map to the Gate-I collision packet is
needed.  If only the selected `U/V` projection is retained, a row-space
dual is not physical and the conclusion cannot be invoked.

## Scope and verification

This is an exact basis/circuit/cocircuit theorem and a strict reduction of
the missing physical data.  It does not claim that the existing scalar
pivot audit has already constructed `J_T`, nor that a dual of an incomplete
response projection is a terminal.

Run:

```text
python3 computations/verify_h3_trapped_carrier_complete_labelled_fibre_alternative.py
python3 -O computations/verify_h3_trapped_carrier_complete_labelled_fibre_alternative.py
python3 -I -S computations/verify_h3_trapped_carrier_complete_labelled_fibre_alternative.py
```

Frozen ledger SHA-256:

```text
4dd3b55f1fd5ffbfd8649be7fe706451db2e259a091b40f9af62b22e6d421615
```
