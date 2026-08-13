# Every lower second-Hasse face has the same `K3,3` tag obstruction

## Result

The literal `C2+`, `C4`, `P2`, and reversed-`P2` faces are governed by one
uniform incidence geometry.  There are

```text
210 nonzero response direction pairs,
210 distinct complementary lower tails,
630 literal pair-tail incidences.
```

Joining a direction pair to a complementary tail when together they form a
response occurrence gives exactly

\[
                         70K_{3,3}.                  \tag{1}
\]

The component types are

| lower type | `K3,3` components |
|---|---:|
| `C2+` | 15 |
| `C4` (`DQ` plus the two `PS` orientations) | 15 |
| `P2` | 20 |
| reversed `P2` | 20 |

Hence the ordinary untagged pair-to-tail Hasse incidence has rank `70`, not
`210`.  Its direction-pair kernel and tail cokernel both have dimension
`140`.  On each component the decomposition is

\[
              \mathbf Q^3=\mathbf Q(1,1,1)
                    \oplus\{x_1+x_2+x_3=0\}.         \tag{2}
\]

The aggregate line is the familiar three-term lower polynomial.  The
two-dimensional standard summand is the missing direction-pair label.

Checker:

```text
computations/verify_h3_h2_second_hasse_k33_tagged_landing_gate.py
```

Frozen ledger SHA-256:

```text
4199398ce09747e2179e9b256cb14242a2aa92e451b86058b8a9f32a227f62a9
```

## What is uniform—and what is not

The ordinary Hasse coproduct is already one natural restriction formula for
all types.  It sends each tagged direction pair to the sum of its three
complementary tails.  Equation (1) shows why this is insufficient for the
physical theorem: all three direction vertices in one component have the
same untagged image.

For example a `C4` component has direction tags

```text
(d,q04), (p4,s0), (p0,s4)
```

and the same three `q*q` tails.  A `P2` component has

```text
(p0,q12), (p1,q02), (p2,q01)
```

and the same three `s*q` tails.  Forgetting the pair tag therefore destroys
exactly the fine/source datum that distinguishes the physical Hessian face.

A single fixed untagged column cannot repair all four types: their
direction-pair labels and target/repeated readouts remain distinct.  A single
**natural family schema** can do so only if it stays indexed by the direction
pair and carries the centered summand in (2) objectwise.

## Strongest `h=2` placement results

The source side is already highly organized:

- the labelled two-root Hasse/cobar square is explicit;
- the universal relative occurrence graph constructs
  `d Gamma_i=t_i-(Cu)_i` and is presentation-safe while `t` is retained;
- the `B-4/C2+` coefficient landing agrees exactly with `delta_plus`; and
- the formal divided-power `C4` Hasse face exists.

What none of these constructs is the physical centered carrier:

- the endpoint-even private `P2` carrier has rank `5`;
- the `C2+` restriction/reinsertion to its target-bearing orbit is open; and
- the old literal `C4` inventory is site-squarefree and contains no
  source-loop-labelled relative diagonal cell.

Thus setting the relative carrier `t=0` is not a construction.  It changes
the classical fibre from `A` to `A/(Cu)`.

## The smallest actual unfilled coordinate

The first completely explicit instance is the `P2` packet

```text
base word       0112
intermediate    0102
residual        q45:12
reinsertion     q23:21
top grade       01211222 / labelled P3+K2.
```

Modulo the complete response line, its endpoint-even private face is
detected by

\[
                    \ell=e_0+e_3-e_1-e_6,
 \qquad \ell(r_{0102})=-{13\over6}.                  \tag{3}
\]

The target/reduced-Eq cone has zero projection to this coordinate.  After
reinsertion, the forced labelled `dq23` preimage is still detected:

\[
                       \ell(z_{dq23})={35\over72},    \tag{4}
\]

while its scalar ordinary residue is zero.  Therefore (3) is the first
missing occurrence-private placement, and (4) is its first proper labelled
face.  They are actual coordinates, not an abstract cokernel dimension.

## Shortest construction theorem

Construct one centered direction-pair-tagged carrier family, natural under
restriction, labelled root principal parts, and matching-tail reinsertion.
Its `P2` instance must land (3)--(4); its `C2+` and `C4` instances retain
their distinct target and repeated-grade rows.  This is one equivariant
schema, not one ungraded column.

Once that carrier lands in the exhaustive augmented cap complex, the
cap--Cartan extension theorem applies: every local obstruction dual extends
through physical `q/ainc/target/W/ores/ridge`, and exact duality yields a
protected filler or an augmented terminal.  Thus the `K3,3` centered tag is
the common first pre-terminal obstruction.

## Scope

The incidence theorem is exact for the full uncoloured site/head response
census; literal colours refine, rather than merge, its components.  The
`h=2` coordinate statements retain the exact word, fine, and reinsertion
grades.  No physical tagged carrier is constructed here.
