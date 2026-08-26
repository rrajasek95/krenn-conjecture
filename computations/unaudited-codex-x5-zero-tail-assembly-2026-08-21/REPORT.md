# X5 zero-tail extended diagonal packet and support shadow

The exact packet in the normalized `e=t=0` quotient is now complete.  It is

| sector | literal rows |
|---|---:|
| frozen master | 270 |
| full `440/2110` orbit | 144 |
| new `422/01010202` orbit | 288 |
| new `422/00010212` orbit | 576 |
| new `422/00010122` orbit | 288 |
| explicit packet | **1,566** |

The remaining `422/00001212` orbit has 72 rows.  Every row is replayed
literally as `e_c[ab]*X_d[T]*X_e[U]`, so it vanishes in the declared quotient.
The disjoint union `1566 + 72` is exactly the complete 1,638-row nontrivial
zero-tail packet.  This part is an exact source-label/orbit statement.

## Support-only census

The Boolean shadow retains one diagonal/antidiagonal entry pair in each of
the six permanent blocks of every colour and one complementary transversal
`Q` pair per colour, as forced minimally by the exact polarized `H` identity.
The transverse `440` rows make the three `Q` pairs distinct.  The new
`422/01010202` orbit cuts the resulting 88,080,384 labelled models to 275,568.
The other new rows have nontransversal majority `Q` factors and therefore do
not fire after those optional support bits are deleted.

Exact quotienting by `B4 x S3` leaves **310** minimal support/signature
orbits.  Their `Q` data have only two geometries:

- `0,7,25`: 224 `X`-relation refinements;
- `0,30,45`: 86 `X`-relation refinements.

The full 310-record antichain is stored in
`results_extended_diagonal_packet_support_shadow.json`.

## Frozen no-goods and remaining obligation

The support6, support8, TP, cycle-boundary, and `A=B` mate-closure artifacts
are hash-pinned in the result.  None soundly deletes a minimal record: the
support6/support8/cycle/`A=B` antecedents force larger exact `Q` signatures,
while TP is a coefficient chart rather than a Boolean support mask.  Replacing
those exact antecedents by support containment would be unsound.

Thus the smallest next coefficient target is the 86-refinement `0,30,45`
geometry.  One needs an exact identity showing its shadows unrealizable under
`e=t=0`, or a source-faithful routing of every realization to a transported
frozen component.  The `0,7,25` geometry is the second target.  The SAT/support
census is discovery only and is not a closure theorem.

## Replay

```text
PYTHONHASHSEED=17 python3 -O audit_extended_diagonal_packet_and_support_shadow.py --check-results
```

Current SHA-256 digests:

- script: `6087c51946b1d7c3d8a25a8c33c0aac8ccb9ebbd4ab36315c4d42e61bb5060a3`
- packet: `7a7ce9a77b57fc7c64d0f34aefffe233baf5850fe869ada2d85caa44ce691432`
- support result: `498b55eb7ad89c0a3b7596cc8583e9bccd6663adcca1109fe10f3d71c8d8af53`
- packet logical: `aeb45a4da9a575e29a2f9707c8d7abc17ad66b7d1eb8d95b894756c4251543b1`
- result logical: `9324dae6c55780dc17bbc2f5235dfb04ecbb4aa821676615caebcf53e6de871f`

## Exact closure of the `0,7,25` geometry

`audit_q_geometry_0_7_25_laurent_closure.py` restores the coefficient data
discarded by the Boolean shadow.  Of the 224 support refinements, 220 have a
supervertex triple with no live cubic term.  Their corresponding reduced
triangle row is literally `1-1-1-1=-2`, so they are impossible in
characteristic zero.

Only four relation-mask triples survive:

```text
(38,56,56)  (38,63,56)  (63,38,63)  (63,63,63).
```

Each admits a unimodular three-entry Laurent gauge.  The four triangle
equations leave exactly six roots per colour in `Q(sqrt(2))`, hence 216
three-colour branches.  Their exact stabilizer quotients have respectively
56, 56, 56, and 34 branch orbits.  Every branch has `(H0,H1,H2)=(4,4,4)`.
The audit then replays all 1,566 literal rows, including all three new `422`
orbits and full `440`.  A single source row is nonzero on every branch:

```text
(38,56,56)  00110110 = Q0[0147] Q1[2356]
(38,63,56)  00110110 = Q0[0147] Q1[2356]
(63,38,63)  00021021 = Q0[0125] X1[47] X2[36]
(63,63,63)  00011011 = Q0[0125] Q1[3467].
```

Thus all 224 `0,7,25` orbits are unrealizable.  Standard, optimized, and
isolated/no-site replays agree at logical SHA
`dbaed76c449aa872227e0e8f67ed311fb3ebc87723f082197c229e4f5cb0271d`.

```text
python3 audit_q_geometry_0_7_25_laurent_closure.py --check-results
python3 -O audit_q_geometry_0_7_25_laurent_closure.py --check-results
python3 -I -S audit_q_geometry_0_7_25_laurent_closure.py --check-results
```

## Independent conditional exhaustion ledger

`audit_zero_tail_exhaustion_ledger.py` independently reconstructs the entire
literal and Boolean inventory.  It verifies all ten source-label orbits under
the order-2,304 `B4 x S3` action, the disjoint identity
`1,638=1,566+72`, and the exact union of all 310 stored support orbits.  The
reconstructed orbit union equals all 275,568 Boolean survivors and splits as
224 records of type `0,7,25` plus 86 of type `0,30,45`.  It also checks that
the `0,7,25` closure loses none of its 864 root triples or 202 stabilizer
orbits.

The terminal `0,30,45` result, logical SHA
`6bdee0c2a402e1d30dae17ef2f769e7bfac6685883cc48bb157962b310454327`,
passes the frozen 86-orbit/84+2/216-branch acceptance contract.  Therefore
both geometries exhaust the **310 minimal-support strata**.  This does not alone
close every larger-support point of the full `e=t=0`, `H`-live component.
That promotion still needs a support-minimal degeneration/initial-ideal lemma
or an independent exclusion of all larger-support strata.  The ledger has a
must-fire mutation guard against silently making that promotion.

Standard, optimized, and isolated/no-site modes agree at logical SHA
`1a281967346bae06de96b7298c8fd340f8f5a17712880c508f8485d04729f728`.

## Site-colour torus obstruction to the proposed degeneration

`audit_site_colour_torus_faces.py` computes in the character lattice
`Z^(8*3)/<s_0,s_1,s_2>`, where `s_c=sum_i e_(i,c)`.  The normalization
sublattice is saturated with Smith diagonal `(1,1,1)`, so the quotient has
rank 21.  Every frozen minimal support has 16 live edges in each colour and
is four-regular.  Giving all 48 weights coefficient `1/48` therefore has sum
`4(s_0+s_1+s_2)` and projected barycentre zero with every coefficient
positive.  Hence all 310 support orbits (all 275,568 labelled supports) are
torus-closed/polystable and have empty destabilizing Hilbert--Mumford cone.

None of the 310 supports is a strict coordinate 1PS face.  In any cross
`2 x 2` block the four additive weights obey

```text
w00 + w11 = w01 + w10.
```

If the diagonal pair were the exposed live face, `w00=w11=m` and both omitted
weights would be strictly above `m`, contradicting the identity; the same
argument applies to the antidiagonal pair.  This is an exact two-inequality
Farkas certificate, already in one block.  The projected-rank census of the
310 records is `(18,19,20,21)` on respectively `(6,26,91,187)` support
orbits; the corresponding rank-21 HM lineality dimensions are `(3,2,1,0)`.

The pure matching rows alone have 64 inclusion-minimal balanced supports per
colour.  They form three `B4` orbits of sizes `8,48,8`; their three-colour
products form 363 `B4 x S3` orbits.  The frozen 310 `(Q,X)` records project to
only 175 of these `X`-orbits, leaving 188 balanced pure-row orbits absent.
The exact 363-record orbit ledger is included in the result.

There is also a one-orbit larger balanced support: keep all 28 edges per
colour (four anchors and all four entries in each cross block).  It is
seven-regular, so its projected barycentre is again zero, and the same
`2 x 2` identity prevents a strict 1PS limit to any frozen complementary-pair
support.  This is a support-level counterexample only, not an asserted
solution of the mixed source equations or an `H`-live/no-cap coefficient
point.  Consequently the site-colour torus cannot prove the missing
larger-support reduction; one still needs a mixed-row initial-ideal theorem or
direct exclusion of larger balanced strata.

Standard, optimized, and isolated/no-site modes agree at logical SHA
`f0aa090e32c2ed75125bb14164c14db621bc0ecfdab816b55cf331cf23a3374b`.
