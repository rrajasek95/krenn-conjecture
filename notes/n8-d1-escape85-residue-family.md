# N=8 D1: escape 85 residue family and exact full frontier

The residue subsystem of arbitrary-support CEGAR escape `85` is not empty.
It has a ten-parameter torus family after two edge gauges, including an
explicit rational point.  Therefore no residue-only rank, quotient, or
Koszul lemma can close this support: the next obstruction must couple the
residue to a six-site or full eight-site equation.

Write

```text
A=A45, B=A46, C=A47, D=A56, E=A57, F=A67.
```

The support is

```text
A: {12,22}                  D: {20,21,22}
B: all except 10            E: {22}
C: {02,10,11,20,21,22}      F: all except 02.       (1)
```

Every one of the three matching products contains `e2` at vertex `5`.
After the independent edge gauges `A12=1` and `E22=1`, put

```text
A=(0,1,r) tensor e2,        D=e2 tensor d,
B1=(0,b1,b2),               C1=(c10,c11,0),
C0=c0*e2.
```

The three vertex-`4` row slices classify the ideal successively:

```text
B0=-c0*d,
F=-(B1 tensor e2+d tensor C1),
C2=(r*c10,r*c11,c22),
B2=r*B1-c22*d+e2.                                      (2)
```

Conversely, direct substitution of (2) makes the first two slices zero and
the target slice exactly `E22`.  Thus (2), subject only to nonvanishing of
the displayed supported cells, is the complete localized residue family.

One rational point is

```text
A rows: (0,0,0), (0,0,1), (0,0,1)
B rows: (-1,-1,-1), (0,1,1), (-3,-2,-1)
C rows: (0,0,1), (1,1,0), (1,1,3)
D rows: (0,0,0), (0,0,0), (1,1,1)
E rows: (0,0,0), (0,0,0), (0,0,1)
F rows: (-1,-1,0), (-1,-1,-1), (-1,-1,-1).
```

All 28 supported entries are nonzero, and its 81 residue coefficients are
`80` zeros and the required single `1` at colour word `2222`.

## What remains

Taking every E1-admissible cell outside the 26 holes in (1) gives a maximal
support with `191` localized variables.  It passes all `8,100` exact support
fibres.  Direct reconstruction gives `7,029` distinct coefficient
generators, no monomial generator, `288` plus-binomials, and `289` total
binomials.  The checker freezes their complete digest without trusting the
CEGAR process.

This is not a point of the full ideal.  It is an exact proof that the
residue projection of that ideal is nonempty, together with a reproducible
full-ideal input.  The unresolved task is to combine (2) with the two
six-site purity tensors and full output exactness, or to lift (2) to all
`191` variables and verify all full equations.

The checker
[`verify_n8_d1_escape85_residue_family.py`](../computations/verify_n8_d1_escape85_residue_family.py)
reconstructs the support and all full generators, symbolically verifies the
family, and evaluates the rational point coefficient by coefficient.  Its
frozen ledger SHA-256 is
`6ca2649ae88ab8394755fc4ad4f2025c7b4c0a9db8151a5ecd2961ab56bb0c41`.
