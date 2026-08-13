# The even trace site-collapse comparison has one two-label repair

## Result

The missing shifted map `iota=tau_plus` from the identity-cap Cartan orbit
to the diagonal fifteen-label packet is now explicit on thirteen labels,
including its mixed Cartan target and coefficientwise Rees extension.  In the
canonical faces-((3,5)) complete component, every maximal equivariant site
collapse has pushforward

\[
       3B_0+2B_1+3B_2+3B_3+2B_4+3B_5.                \tag{1}
\]

The two omitted labels are one \(\rho\)-pair and acquire a forbidden loop.
The unique equivariant linear repair completing the uniform trace target is

\[
  \text{each omitted label}\longmapsto {B_1+B_4\over2}. \tag{2}
\]

Each retained label lands in a literal decorated complete pure multiplier
column.  Tensoring that column with the physical Cartan root orbit gives its
mixed-word image; coefficientwise extension gives the same map at each Rees
order.  Thus this is a construction of `iota` on thirteen labels, not merely
visibility of their targets.

This reduces the generic `iota=tau_plus` problem to one relative orbit image.
A literal physical source cell realizing (2) is not present in the
construction yet.  Moreover, an explicit integral separator proves that no
rational combination of all natural equivariant site collapses can synthesize
it.

Checker:
[`verify_h3_trace_cartan_tau_plus_site_collapse_gate.py`](../computations/verify_h3_trace_cartan_tau_plus_site_collapse_gate.py).

## The even fifteen-label source packet

After forgetting the Cartan root decoration, the trace cap \(P(I)\) gives the
unsigned `012` collision packet and its exact \(\rho\)-translate `024`.
Their even sum has fifteen collision labels.  Twelve occur once; the three
shared repeated-`02` labels occur twice.  Thus the packet has total occurrence
weight eighteen and is \(\rho\)-even.

The canonical complete target has 288 columns and six pure diagonal columns
\(B_0,\ldots,B_5\).  The physical involution acts by

\[
                 (B_0\ B_5)(B_2\ B_3)
\]

and fixes \(B_1,B_4\).  The identity cap supplies the equal-weight trace
landing

\[
                 3\sum_{i=0}^5 B_i,                  \tag{3}
\]

whose total coefficient is again eighteen.  The six physical boundary rows
are pairwise disjoint 90-feature rows, so (3) is a literal 540-feature
decorated packet with coefficient three on each feature.

## Exhaustive equivariant collapse calculation

Enumerate all maps from the six collision sites to the five canonical odd
target sites satisfying \(\phi\rho=s\phi\).  A source label is counted as valid
only when its entire matching maps to one of the six physical loop-free pure
graphs.  Among the 405 equivariant maps, the valid-label histogram is

```text
0 labels:   381 maps
10 labels:    4 maps
12 labels:    4 maps
13 labels:   16 maps
```

There is no fifteen-label map.  Each of the sixteen maximal maps has exactly
one double fibre, retains all three shared labels, omits one nonshared
\(\rho\)-pair, and gives exactly (1).  The four possible omitted pairs are

```text
(0,01)  <-> (11,04)
(2,01)  <-> (10,04)
(6,12)  <-> (8,24)
(12,12) <-> (13,24).
```

For the lexicographically first maximal map

```text
phi = (1,2,4,3,5,4),
```

source sites 2 and 5 both map to target site 4.  The omitted matchings
`(2,01)` and `(10,04)` both contain edge `25`, which becomes the forbidden
loop `44`.  Their deficit from (3) is precisely (B_1+B_4).

Because the omitted labels are exchanged by \(\rho\), equivariance requires
them to have the same target image.  Because \(s\) fixes both deficient target
columns, (2) is the unique image completing (3).  Over the physical rational
coefficient field this is one new equivariant orbit image, rather than two
independent generators.

## Why averaging the partial maps cannot close the gap

Order the fifteen labels as in the checker and consider the integral
\(\rho\)-even covector

```text
(1,-4,0,1,-4,10,-4,1,1,-4,0,1,1,1,1).
```

It evaluates to zero on the coverage vector of every one of the 24 nonzero
partial equivariant site-collapse maps.  It evaluates to `2` on the all-ones
fifteen-label coverage vector.  Hence that vector is not in the rational
span of the complete partial-collapse family.  Averaging maps, changing the
double fibre, or combining all four possible missing pairs cannot define a
full label map.

This separator is deliberately scoped.  It obstructs maps induced by an
equivariant collapse of sites into the five canonical odd sites.  It does not
obstruct a new diagonal/loop-resolution relative cell with the image (2).

## Relation to the two proof routes

For the odd `tau_minus` packet, the successful collapse lives on the twelve
nonshared labels and all three shared labels form the loop obstruction.  For
the even `tau_plus` packet the multiplicity-two shared labels all survive;
the best collapse instead loses one nonshared \(\rho\)-pair.  The common pattern
is sharper than a generic fifteen-label comparison:

```text
tau_minus: 12-label signed landing + two shared-orbit repairs,
tau_plus:  13-label even landing   + one nonshared-pair repair.
```

Thus the even route asks for the smaller relative interface.

## The `beta=0` branch remains separate

At `beta=0`, \(J_*=0\) and the intrinsic selected block is literally
`alpha*E_00`.  In the typed `(D0,D2)` basis the cap rows have selected `D0`
coefficient zero and see only the `D2` root defect.  The
missing `D0` selected-colour order-three unary/complement branch is a target
root-coordinate problem, not one of the omitted collision labels above.
The repair (2) therefore does not supply it.  Any final inactive theorem must
state the generic trace repair and the `D0` alternative as two obligations.

## Exact frontier

The generic trace comparison is reduced to constructing one source-valid,
\(\rho\)-even diagonal/loop-resolution orbit cell whose two boundary labels
both read `(B1+B4)/2`, with the already required target augmentation and Rees
typing.  If no such cell exists, the coverage covector above is the first
literal site-collapse separator.  The `beta=0` `D0` unary/complement remains
independent.

## Verification

Run:

```text
python3 computations/verify_h3_trace_cartan_tau_plus_site_collapse_gate.py
python3 -O computations/verify_h3_trace_cartan_tau_plus_site_collapse_gate.py
python3 -I -S computations/verify_h3_trace_cartan_tau_plus_site_collapse_gate.py
```

Frozen ledger SHA-256:

```text
e66354d199f39b5f350cb808f351ce94819a9af9b6e4a87402c5b57ede50f7f0
```
