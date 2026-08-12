# Endpoint oddness makes the Cartan prism augmentation-safe

## Structural lemma

Let `s` interchange the two endpoint orientations and let `w` be the
simultaneous tail-colour Weyl action.  Suppose a tail complex has a Cartan
homotopy

\[
                         w-1=dH_w+H_wd .                 \tag{1}
\]

The endpoint and tail actions commute.  Therefore

\[
 K=(1-s)H_w,
 \qquad
 dK+Kd=(1-s)(w-1).                                      \tag{2}
\]

This is the required mixed covariance--curvature prism.  On the seed
`E+T0`, its boundary is

\[
 -E_+T_0+E_-T_0+E_+T_1-E_-T_1,                         \tag{3}
\]

whose four coefficients are exactly

\[
                         (-1,1,1,-1)=-\delta .           \tag{4}
\]

The key point is not merely (3).  If an augmentation `a` is endpoint-even,
then `a(1-s)=0`, and consequently

\[
                              aK=0                       \tag{5}
\]

without any assumption that `w` fixes the augmentation target.  Thus the
failure of the individual root directions to stabilize the ternary GHZ
tensor is not, after endpoint oddization, an independent obstruction.

## Application to the physical packet

The pinned four-corner cap calculation proves that, corner by corner,
`D`, `W`, physical target, anchor incidence, and the pure-Eq aggregate are
endpoint-even.  The ordinary residue coordinates remain separately
labelled.  Therefore (2)--(5) give

```text
D = W = target = anchor = pure-Eq aggregate = 0,
ordinary residue = (-1,+1,+1,-1) = -delta.
```

This conclusion is stronger than cancellation on one selected
representative.  It holds for every intermediate tail form produced by the
Cartan homotopy because endpoint oddization is applied after `H_w`.

The source side is also compatible at its principal symbol.  The complete
covariance--curvature audit proves that the signed fourth symbol has zero
top and zero codimension-one shadow on every complete source word, with
first nonzero face exactly (3).  The order-six Hasse construction supplies
the full coherent `-delta` face tower, and the ridge audit proves that this
tower commutes strictly with `-dOmega_v`.

## What has actually been removed

The augmented interchange theorem no longer needs separate constructions
to cancel target, `W`, anchor, or `D` defects of the Weyl path.  These
readouts vanish functorially from endpoint parity.  The remaining local
obligations are only:

1. descend the root contractions, equivalently `H_w`, to the complete
   physical word-labelled source complex;
2. identify the residue face of that descended prism with the pinned
   complete order-six Hasse tower; and
3. tensor the descended cell with the commuting ridge class `-dOmega_v`
   and prove the physical terminal/zero-indeterminacy alternative.

The first item is still substantial.  The standard bar/first-PP graph obeys
`R=D` and does not contain the endpoint-odd residue-only face.  Equation
(2) proves what the missing relative Spencer cell must be and shows that
its protected augmentations are automatically correct; it does not place
that cell in the literal physical source image.

## Proof-theoretic consequence

The first structural theorem can now be stated with a smaller hypothesis:

> **Physical Cartan descent.**  The endpoint-odd Cartan prism `(1-s)H_w`
> for the two complete source-word components descends through the labelled
> repeated-grade source resolution.

Once this holds, all protected coarse readouts follow from the present
lemma, the order-six tower supplies `-delta`, and the terminal ridge theorem
supplies eta/sigma.  Hence the physical comparison, rather than a list of
readout cancellations, is the only remaining local construction.

## Scope and verification

This is an exact chain-algebra and augmented-readout theorem.  It does not
construct the physical source-labelled root contractions, prove terminal
zero-indeterminacy, or perform transverse rank landing.

Run:

```text
python3 computations/verify_h3_endpoint_odd_cartan_prism_augmentation.py
python3 -O computations/verify_h3_endpoint_odd_cartan_prism_augmentation.py
python3 -I -S computations/verify_h3_endpoint_odd_cartan_prism_augmentation.py
```

Frozen ledger SHA-256:

```text
2fb16b1648b2a69e892a45387bf86430200312d8ecfe1ae8d922a5c403a63c6b
```
