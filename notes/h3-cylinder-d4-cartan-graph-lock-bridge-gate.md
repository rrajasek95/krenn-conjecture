# D4 followed by tail Cartan reaches two graph-lock packets, but not the cap grade

## Exact coefficient bridge

Let

```text
M0=q23*q45,   M1=q24*q35.
```

The cylinder matching factor is `M0^00-M1^00`.  The four-root D4 top at
sites `2,3,4,5` and the physical Cartan/Weyl action at sites `2,5` act
literally by

```text
M0^00 -> M0^11=q23:11*q45:11 -> M0^d=q23:21*q45:12,
M1^00 -> M1^11=q24:11*q35:11 -> M1^d=q24:21*q35:12.
```

Endpoint antisymmetrization gives the required corner signs

```text
(-1,+1,+1,-1).
```

Thus the proposed `M1` term is exactly the graph-lock packet
`delta_M1=M1^11-M1^d`.  On the **full** cylinder factor, however,

\[
 (w-1)(M_0^{11}-M_1^{11})
                  =\delta_{M_1}-\delta_{M_0}.          \tag{1}
\]

The two packets have disjoint matching labels and rank two.  The composition
is not one selected `delta`; it is the difference of two covariant copies.
This causes no new coefficient conjecture: the committed Physical Cartan
Descent is matching-covariant and supplies both copies once they are in its
canonical physical grade.

Checker:

```text
computations/verify_h3_cylinder_d4_cartan_graph_lock_bridge_gate.py
```

Frozen ledger digest:

```text
91878b6d455d4db6ca5e88bc26e77589fe27105e021a7ee34d40c5a0ec6ae11c
```

## The literal cap multiplier blocks the composition

The response D4 path is exact on words

```text
110000 -> 111111 -> 112112.
```

The physical cap graph instead has word `01211222`.  At the four D4 sites
`2,3,4,5`, its letters are

```text
2,1,1,2,
```

so the `0->1` D4 operation used on the response occurrence has no literal
input on the cap multiplier.  The cap graph is flat as a spectator in the
formal tensor/orbit-relative bicomplex, but this does not give a
source-labelled fixed-fibre cross-word map.

Consequently polynomial closure from the previous audit is still
conditional in exactly one place: the cap graph must first be placed across
the response/E14 word and repeated grade.  After that placement,
`-k(T+Y rho)` cancels the target curvature and (1) is its ordinary-residue
debt.

## Endpoint polarization and repeated grade

The D4--Cartan calculation also reproduces the known associated-symbol
boundary rather than bypassing it.

- A fixed-right comparison supplies eight labelled `P`-tail Hasse pairs.
- The physical residue packet has sixteen pairs, the disjoint sum of eight
  `P`-tail and eight `S`-tail terms.
- Endpoint transpose supplies the missing `S` half at associated grade.
- That transpose sends the canonical fine degree and six private features
  to a conjugate component: `Lambda -> Lambda^T`, with zero overlap between
  the two six-feature sets.

A four-coordinate check sees the correct `(-1,1,1,-1)` shadow on either
half and therefore cannot detect this obstruction.  The endpoint and
repeated labels are load-bearing.

## Augmented rows and consequence

Once the canonical grade is genuinely reached, the committed Physical
Cartan Descent already supplies

```text
ordinary residue             = (-1,+1,+1,-1),
D,W,target,anchor,pure-Eq     = 0,
eta/sigma                     = the -dOmega ridge packet,
physical q                    = generator/Fredholm alternative.
```

Thus no new residue or terminal theorem remains after placement.  The
shortest missing theorem is the physical multiplicative cross-word
comparison which:

1. carries the cap graph over the D4 response path;
2. retains both matching packets in (1);
3. includes the endpoint-transpose half; and
4. transports the conjugate `Lambda^T` repeated component back to canonical
   `Lambda` with the augmented rows above.

With that comparison, the local cylinder residue closes by the existing
Physical Cartan Descent.  Without it, the proposed D4--Cartan composition is
exact only at coefficient/associated-symbol level and does not yet close
the physical cylinder placement.

Scope is canonical `h=3`; the formal spectator-cap tensor is not asserted
to be a fixed-fibre source map.
