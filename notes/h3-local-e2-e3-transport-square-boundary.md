# The local transport square needs the full Hamming cube

## Result

At the final `00112200` affine return, remove the already routed `04|15`
term and compare the two remaining four-hole matching monomials

\[
 A(w)=x_{01}(w_0,w_1)x_{45}(w_4,w_5),\qquad
 B(w)=x_{05}(w_0,w_5)x_{14}(w_1,w_4).
\]

At the base word `d=(0,0,2,2)`, the zero-face equation is

\[
                         A(d)+B(d)=0.                 \tag{1}
\]

The matching-base `E2/E3` complex is the correct source-labelled transport
square, but one square does not prove the hoped-for deletion dichotomy.
The exact replacement is a Hamming-cube descent followed by a
source-saturation theorem.

Checker:
`computations/verify_h3_local_e2_e3_transport_square_boundary.py`.

## Curvature gives the desired carrier

Change site `0` from colour `0` to `i` and call the new word `f`.  The exact
matching-base minor is

\[
\begin{aligned}
 \Delta^{BA}_{df}
 &=B(d)A(f)-B(f)A(d)\\
 &=x_{14}^{02}x_{45}^{22}
   \bigl(x_{05}^{02}x_{01}^{i0}
        -x_{05}^{i2}x_{01}^{00}\bigr).                \tag{2}
\end{aligned}
\]

The analogous formulas hold at sites `1,4,5`.  Thus nonzero curvature is
already the required physical object: a localized common tail times a
same-star Pluecker minor.  The matching-base `E2` identity is source-valid
before any division, and the selected tail factors are units on the chart.

This proves the curved half of the proposed local principle:

```text
nonzero transport curvature => literal active common-q carrier.
```

## First-square flatness does not give deletion

There is a literal edge-monomial counterexample.  Set

```text
x05=x14=x45=1,
x01(a,b)=-1 except x01(1,1)=0.
```

Then `A+B` vanishes at `d` and at every Hamming-one neighbour of `d`.
Every corresponding `E2` minor and every `E3` face made from the base and
two such neighbours also vanishes.  Nevertheless

\[
                  (A+B)(1,1,2,2)=1.                  \tag{3}
\]

This is not an abstract vector guard: both `A` and `B` are products of
literal physical edge matrices.  Consequently the implication

```text
one flat transport square => complete-column dependence => deletion
```

is false.  The first hidden obstruction may live on a two-coordinate face
(`11112211` after restoring the endpoint word), exactly where primitive
factor cancellation becomes a colon/source-saturation issue.

## Corrected local theorem to prove

The useful replacement has two layers.

> **Hamming-cube curvature descent.** Starting from (1), choose a
> minimum-Hamming-weight word on which `A+B` is nonzero.  The boundary of
> its first nonflat face, together with the third matching base and the
> complete response row, produces either a localized same-star carrier, an
> already routed external term, or a strictly lower face.

> **Primitive saturation.** If every face is flat, the global equality of
> the two matching-evaluation tensors must lift through the labelled source
> module to a finite one-star joint-kernel relation.  That relation deletes
> the affine-return component without losing the synchronized anchor.

The first statement is a finite cubical induction.  The second is the
load-bearing algebra: it asserts that cancelling the selected common tail
does not leave a primitive colon class.  General `C4` exchange complexes do
have such colon classes, so this must use the special target, unary, and
localized-tail hypotheses of the one-bad packet.

## Consequence for the larger proof pattern

The coherence-versus-curvature pattern survives, but the cells must include
all Hamming faces rather than only elementary squares:

```text
first nonflat face  -> carrier;
all faces flat      -> global dependence, conditional on saturation;
unfillable face     -> relative critical class.
```

This is also the form needed later for marked-sector descent: local
nullhomotopies are insufficient until their overlap faces and lift
indeterminacy are controlled.

## Scope

The checker proves all eight Hamming-one factorizations and the literal
Hamming-two counterexample.  It does not prove Hamming-cube descent or
primitive saturation.

Frozen ledger SHA-256:

```text
9417e879bd19e1cd282e670f0d77c747a0014c02ecddf6df52a656aab86efa87
```
