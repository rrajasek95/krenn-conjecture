# Every repeated C5 component has a homogeneous six-term dual

## Result

For each of the five repeated `P3+K2` components in cyclic face order

```text
(1,3), (3,5), (5,2), (2,4), (4,1),
```

the complete full-nine boundary has 288 columns and exactly six pure-word
columns.  Every pure column has at least one literal matching coordinate
owned by no other column.  Choose one such coordinate `m_i` from each pure
column.  With the repeated boundary written with the mapping-cone sign, the
integral identity is

\[
                  Q+m_1+\cdots+m_6=0,                 \tag{1}
\]

where `Q` is the pure coefficient aggregate.  Thus each component has a
six-term integral dual.  The five components occupy five distinct physical
fine grades, so after primitive normalization their formal face-pairing
matrix is `I_5`.

For faces `(3,5)`, equation (1) is not merely a repeated-source identity.
The exact first-Spencer-flat order-six calculation proves that the same dual
annihilates the combined 8,580-column order-six and 288-column repeated
bridge matrix, while the desired primitive aggregate pairs to one.

## Why this is better than the old aggregate separator

All six coordinates in each (1) have one common physical fine degree.  They
have weight zero under the five `eta_z=p:0-z:0` fields, the five left
non-Euler fields `x:0-z:0`, and the two additional full-Jacobian guards
`p:2-x:2` and `x:0-p:0`.  The `eta_z` family was exactly what destroyed the
earlier coarse `Omega` separator.

The gain is structural: (1) is homogeneous, whereas `Omega` subtracted edge
coordinates of different characters.  The first committed
zero-indeterminacy obstruction therefore does not recur for the six-term
dual.

## Remaining step

The other four componentwise duals are exact old-source candidates, but the
physical order-six comparison has only been checked in the canonical
faces-`(3,5)` grade.  The symbolic cyclic bridge has rank four and transports
the grading to all faces; what remains is to prove that physical cyclic
transport in the augmented relative cone, or to construct the relative
comparison cell directly.

Consequently the comparison frontier is now a sharp alternative:

1. a new relative cell supplies the primitive aggregate and hence the
   physical comparison; or
2. the homogeneous six-term duals survive the exhaustive relative cone and
   give the five facewise separator columns.

No additional polynomial full-nine row can change this alternative.

## Scope

The theorem covers the complete old repeated boundary in all five grades and
the known diagonal stabilizer families.  It does not prove invariance under
an arbitrary future relative generator, physical cyclic propagation of the
order-six chain, or transverse-rank landing.

Verification:

```text
python3 computations/verify_h3_repeated_component_six_term_separators.py
python3 -O computations/verify_h3_repeated_component_six_term_separators.py
python3 -I -S computations/verify_h3_repeated_component_six_term_separators.py
```

Frozen ledger SHA-256:

```text
6063daed9a1759d2051996230a6b6906a9c7136380593476f7fd6e8c352e6497
```
