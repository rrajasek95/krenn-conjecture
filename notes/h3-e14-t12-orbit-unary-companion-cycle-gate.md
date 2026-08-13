# T12 is the shadow of the central private placement, not a second theorem

## Result

The complete unary identity is

\[
 T_{12}=v_{24}^{11}U_{000101}+R_{E14},\qquad
 R_{E14}=g(1-v_{04}^{00}).                            \tag{1}
\]

Therefore the source-labelled placement

\[
 E=(H_0-u)e_{\rm Eq}\longmapsto R_{E14}              \tag{2}
\]

automatically supplies all twelve word-resolved tails through the old
physical unary row.  `T12` is not an additional higher-cell hypothesis once
(2) is present.

Checker:
[`verify_h3_e14_t12_orbit_unary_companion_cycle_gate.py`](../computations/verify_h3_e14_t12_orbit_unary_companion_cycle_gate.py).

## Exact first-hit rank change

Before (2), the 269 complete target-augmented first-hit columns have rank
269 and

\[
                         [T_{12}]=[R_{E14}].           \tag{3}
\]

The primitive dual has value `-1` on both sides.  Adjoining the literal
`R_E14` column raises the rank

```text
269 -> 270
```

and reduces `T12` to zero.  Hence the same dual is killed.  There is no
remaining `T12` coefficient direction and no new `T12`-specific augmented
terminal.

There is also no hidden nonzero source syzygy at this stage.  If `C` denotes
the first-hit lift characterized by `T12-C=R_E14`, then the old unary column
`U` has the same property.  The 269 first-hit columns are independent, so
their free source kernel has dimension zero and

```text
C=U,
Z=U-C=0,
support(Z)=0,
word_counts(Z)={}.
```

Thus `Z` lies in the standard Schreyer/Koszul syzygy module by the empty
zero certificate; there is no nontrivial higher cell to construct from it.

The earlier `D1`--`D3` result remains correct with narrower scope: those
old response faces do not construct `R_E14`.  Its surviving class
`[T12]=[R_E14]` is precisely the missing private placement, not evidence for
a second cross-operation cell after (2).

## What the moving-target D4 top does—and does not—supply

On the silent fibre, `v04=0`, so

\[
                              R_{E14}=g.               \tag{4}

The orbit-relative fourth-Hasse cube transports the marked centered
occurrence from `110000` to the pure-target occurrence `g` in `111111`, and
the moving target absorbs the old fixed-fibre unit defect.  Thus its
occurrence projection agrees with (2).

But the two objects have different source domains:

```text
D4 top domain : centered occurrence c_f/P_f over the moving target orbit;
required domain: E=(H0-u)e_Eq in the central K_Eq comparison.
```

In the necessary forgetful quotient

```text
(private occurrence R, central Eq-input incidence)
```

they are

```text
silent D4 occurrence top = (1,0),
required E -> R placement = (1,1).
```

The primitive covector `(0,1)` separates them.  The horizontal cap graph
`T+rho` has `(0,0)` in this quotient: it repairs affine target/scalar-residue
normalization but cannot supply the central Eq incidence.

Thus the exact remaining equality is

\[
 \boxed{\Phi_{\rm orb}((H_0-u)e_{\rm Eq})=R_{E14}}   \tag{5}
\]

as a source-labelled full-row boundary—not merely
`pi_occ(Phi_orb)=g` after setting `v04=0`.  Equivalently, one needs a
comparison from the central `K_Eq` product to the marked top of the moving
target occurrence cube.

## Reconciliation with the master local theorem

Once (5) is physical, the committed chain is:

```text
central E -> R_E14       : supplies the private occurrence;
old U[000101]*v24        : supplies all twelve T12 tails by (1);
rooted d_even            : cancels the exact word-resolved residue;
existing main reductions : close occurrence, Eq, lower, target and ores.
```

Physical `q` then follows through the existing defect/transport alternative.
The labelled shifted ridge remains a face of the overall augmented `P2`
schema, but it is not introduced by `T12`.  The apparent presentation
syzygy between two reductions of (1) is already zero because the first-hit
source columns are independent.

## Shortest construction target

Do **not** add a separate `T12` cell.  Construct the single comparison (5)
with the pointed occurrence, moving target/cap, word/fine/repeated labels,
anchor, physical-`q`, and shifted-ridge structure required by the augmented
`P2` theorem.  The old unary row then closes `T12` exactly.

## Scope

This reconciliation is exact for canonical `h=3`, chart `(1,1)`, and the
silent `v04=0` E14 packet.  It proves conditional redundancy of `T12`; it
does not construct (5).

Run normally, optimized, and isolated/no-site.  Frozen ledger SHA-256:

```text
107c6e3e10bd3dd4c9ac6bd76e27defbcd138a205e9eb9470934baacce0c9b94
```
