# One collision family prolongs to all needed jets, but misses the aggregate

## Exact answer

The adjacent `P3 disjoint K2` S-pair and its reduced pure-Eq correction are
functorial under principal parts.  If a single polynomial family

```text
d C_v = -delta_v (H0-u) Eq
```

is constructed, its order-one, order-two, and order-three Hasse
coefficients cancel exactly the Eq convolutions in the corresponding
physical PP edge.  No new target, ordinary residue, `W`, or physical anchor
readout appears.  Normal order is an external Rees grade, so forgetting it
leaves the same physical site profile

```text
P3 disjoint K2 = sorted site degrees (2,1,1,1,1).
```

Thus higher normal order introduces no new generator **type**.  One
polynomial reduced-Eq family supplies all its jet copies.

It is nevertheless not the whole physical comparison.

## The rank-four obstruction persists in every grade

After the reduced Eq correction, the five cyclic physical edges have
boundaries

```text
-r_v+r_(v+1).
```

Their matrix is the oriented incidence matrix of `C5`.  It has saturated
rank four and primitive cokernel `Z`, detected by

```text
(1,1,1,1,1).
```

The reduced Eq face changes neither this ridge boundary nor any augmented
readout, so it cannot raise the rank.

For normal orders one through three, the associated-graded boundary is
three diagonal copies of this matrix.  The 15 normal-indexed mixed-row
classes therefore receive only rank 12, with one primitive aggregate
cokernel in each normal grade.  Lower triangular Hasse convolutions do not
remove these grade-leading covectors.

A single primitive vertex-anchor column completes one `C5` block
unimodularly.  Consequently one **polynomial primitive-anchor family**—and
therefore its three jet copies—completes all three grades to rank 15.  A
fixed zeroth-order anchor without its functorial prolongations would not.

## No new higher-order compatibility defect

On the five-cycle chart,

```text
delta=(a-b,c-d,e-a,b-c,d-e)
```

and the Tate multipliers are

```text
(ce,be,bd,ad,ac).
```

Their weighted sum is the zero polynomial.  Substituting arbitrary cubic
jets `a(tau),...,e(tau)` and expanding verifies the identity in every
coefficient through total degree nine.  Hence the degree-five `d^2`
compatibility automatically prolongs with the reduced Eq family.  Orders
two and three create neither a new multidegree nor a new residue/readout
obstruction.

## Minimal physical interface

The bounded audit therefore isolates exactly two source generator families:

1. the zero-anchor adjacent collision/reduced-Eq family, with
   `ainc=W=tgt=ores=0`;
2. the separate primitive vertex-anchor family, with physical anchor
   incidence `-1` and zero `W`, target, and residue.

These types suffice functorially through the normal orders required by
`44c0a37`, if they are constructed.  Neither family currently exists as a
physical source cell.  The source-provenant comparison carrying derived
`Yw` to physical cap `W` also remains separate.

This note is therefore an exact chain-map interface and a negative answer
to “does the adjacent edge family alone suffice?”, not a construction of
the missing physical cells.

## Verification

```text
python3 computations/verify_h3_component_iv_collision_family_normal_jet_interface.py
python3 -O computations/verify_h3_component_iv_collision_family_normal_jet_interface.py
python3 -I -S computations/verify_h3_component_iv_collision_family_normal_jet_interface.py
```

Frozen ledger SHA-256:

```text
9ed6ea59f35ab3e7abc5381c93479d1837666962b5402d240d3af0fe04eff88c
```
