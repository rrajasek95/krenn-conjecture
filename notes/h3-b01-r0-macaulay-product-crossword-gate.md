# The product `b01*r0` is cap-internal, not the missing cross-word map

## Outcome

There is a tempting Leibniz identity

\[
d(b_{01}r_0)=db_{01}\,r_0+b_{01}(H_0-u)e_{Eq}.
\]

At the undecorated polynomial level, these are exactly the selected six-term
`db01` shape and the central reduced-`Eq` shape needed by the proposed
response-KS to cap-`r0` comparison.  The identity is correct but does not
construct that comparison.

The reason is the full source grading.  The selected response face has tag

```text
word       11:110000
repeated   squarefree vertical PP
operation  selected response / endpoint-matching PP,
```

whereas `r0`, and therefore every Macaulay multiple of `r0`, has tag

```text
word       01211222
repeated   P3+K2
operation  AugP2 cap / K_Eq.
```

Macaulay multiplication changes polynomial multidegree.  It preserves the
word, operation parent, source idempotent, repeated parent, and occurrence
labels.  Consequently `db01*r0` is the cap-parent copy of the six polynomial
derivatives, not the selected response vertical face.

The checker
[`verify_h3_b01_r0_macaulay_product_crossword_gate.py`](../computations/verify_h3_b01_r0_macaulay_product_crossword_gate.py)
keeps three direct-sum coordinates:

```text
selected response db01,
cap-parent db01*r0 PP face,
cap-parent b01*(H0-u)eEq face.
```

The two cap faces have rank two.  Adjoining the selected response face raises
the rank to three.  Thus equality of the six displayed polynomials does not
identify the typed cells.

## Private/reduced-Eq charge

The cap generator `r0` is internally tied: its private and reduced-`Eq`
corner vectors agree.  With

\[
\delta=(1,1,-1,-1),\qquad \chi=\delta\mathbin{\cdot}(B-Eq),
\]

the product `b01*r0` therefore has `chi=0`.  It is a legitimate dark
cap-internal Macaulay column.  It neither fills the balanced quotient nor
creates the missing operation-changing generator.

## Positive conditional use

If one supplies the degree-zero source-labelled matrix unit

```text
Phi_KS,r0 : response KS -> cap AugP2/K_Eq r0,
```

then the same Leibniz calculation becomes exactly the desired first-face
formula.  The normalized chain-map signs are uniquely

```text
Phi_1(epsilon_s)=r0,    Phi_0(c_f)=-E.
```

Strict multiplicativity then retains `B=Eq`, so all eight standard mixed
`kappa` charges vanish.  The logical direction is therefore sharp:

> the cross-word comparison makes `b01*r0` useful; `b01*r0` does not
> manufacture the cross-word comparison.

This closes a plausible shortcut while leaving the frontier unchanged: the
first new physical datum is still the response-to-cap matrix unit with its
selected `db01`, central `Eq`, and augmented proper faces.
