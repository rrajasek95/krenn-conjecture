# The reduced-Eq class is a Koszul face, but its physical Tate lift needs augmented descent

## Exact derived construction

Write

\[
F=H_0-u,
\qquad Q=\operatorname{Eq}.
\]

In the derived intersection of the two actual equations `F=0` and `Q=0`,
the Koszul resolution has degree-one generators
`epsilon_F,epsilon_Q` and the degree-two cell

\[
 \theta=\epsilon_F\wedge\epsilon_Q,
 \qquad d\theta=F\epsilon_Q-Q\epsilon_F.                 \tag{1}
\]

The two terms in (1) are essential: `d^2 theta=FQ-QF=0`.  After relative
base change along `Q=0`, with `epsilon_Q` represented by the physical
EqSystem output `e_Eq`, the cell `C_K=-theta` has

\[
                         dC_K=-F e_{\rm Eq}.             \tag{2}
\]

Thus the desired conormal face is canonical in the *unaugmented derived
intersection*.  It is not an arbitrary formal boundary.

Checker:
[`verify_h3_reduced_eq_koszul_tate_relative_orbit_gate.py`](../computations/verify_h3_reduced_eq_koszul_tate_relative_orbit_gate.py).

## Why the old physical source still does not contain `C`

The literal old generators in the normalized cap block are

\[
 dr_0=F e_{\rm Eq},\qquad dT=-Yw,\qquad d\varrho=w,
\]

with `target(r0)=target(T)=1` and `ores(varrho)=1`.  In coordinates

```text
(-F eEq, Yw, target, Y ores)
```

their edge-augmented columns are

```text
r0       = (-1, 0, 1, 0)
T        = ( 0,-1, 1, 0)
Y varrho = ( 0, 1, 0, 1).
```

The unique obvious target- and `W`-dark lift of (2) is therefore

\[
 C_{\rm near}=-r_0+T+Y\varrho=(1,0,0,1).               \tag{3}
\]

It has exactly the right boundary and zero target/`W`, but it carries
labelled ordinary residue `+Y`.  The desired column `(1,0,0,0)` is outside
the old span.  It enlarges the rank from three to four by a unimodular
minor and is detected by the primitive covector

\[
 \lambda_{\rm cap}=(-F e_{\rm Eq})+Yw+\operatorname{target}
                    -Y\operatorname{ores}.              \tag{4}
\]

This is the precise distinction between the Koszul identity and a physical
relative cell.  Declaring the Tate cell to have zero augmented readouts
kills (4), so it changes the augmented physical cokernel; that declaration
is exactly the missing comparison theorem.

There is a second, independently pinned obstruction in the zero-anchor
quotient.  Every old pure-Eq correction is killed by

\[
                   \lambda_{\rm a}=\operatorname{pureEq}
                                      +\operatorname{ainc}, \tag{5}
\]

whereas the required reduced-Eq face is detected.  Consequently (1)--(2)
alone assign neither the required physical anchor nor its ridge companion.

## The regular `rho` orbit and the parity trap

Duplicating the block at two `rho`-related literal labels gives two
independent primitive obstruction lines.  For the nearest representatives,

\[
 \operatorname{ores}(C_{\rm near}-\rho C_{\rm near})=(1,-1),
 \qquad
 \operatorname{ores}(C_{\rm near}+\rho C_{\rm near})=(1,1). \tag{6}
\]

The odd value in (6) has aggregate sum zero, but it is not zero in the
complete labelled-residue module.  Hence antisymmetrizing the old cap
packet does not construct Gate I's protected cell; it only passes a coarse
aggregate-residue projection.  The even and odd primitive covectors pair
independently with `C_+` and `C_-`, so neither parity follows from the
other.

This sharpens the common-orbit target.  A positive theorem must construct a
source-labelled map from the Koszul normal cell (2) to the complete physical
homotopy fibre.  Equivariance then supplies the regular two-dimensional
orbit `Q{C,rho C}`.  Before that comparison is built, the ordinary Koszul
resolution gives only the unaugmented core.

## What the existing Hasse/PP totalization contains

The checked complete squarefree Hasse totalization contains jets
`r0[U],rm[U]` together with `T,varrho`.  Its 17-term top cycle is reconstructed
from those row jets and its diagonal projection retains exactly
`F e_Eq`.  It does **not** declare an independent normal generator
`epsilon_F wedge epsilon_Q` carrying physical readouts.

A full Tate/cofibrant resolution of the derived intersection does contain
(1).  What remains unproved is the comparison from that canonical model to
the physical correction complex.  That comparison must preserve, at the
literal repeated `P3+K2` grade:

- labelled ordinary residue, not merely its aggregate;
- physical anchor incidence and the required ridge;
- source word, private boundary, and the eta/sigma terminal packet;
- the physical terminal `q=sum_6 m_i-ainc`.

The Koszul universal property assigns none of the latter rows.  In
particular, `q` extends precisely when its comparison defect vanishes in
`D^*/row(J)`.  If it does not vanish and both `q` rows are physically typed,
the protected-kernel witness is already the relative-generator branch.

## Dual consequence and sharp next lemma

The covectors (4) and (5) are primitive left separators of the *checked
underived* source inventory.  They become Fredholm/terminal annihilators
only after proving that they kill every cell of the complete augmented
Tate/relative source.  A newly admitted cell (2) is detected by them, so
old-inventory nonmembership is not by itself a terminal theorem.

The shortest remaining positive lemma is therefore:

> Construct one source-labelled comparison from the normal Koszul cell
> `-epsilon_F wedge epsilon_Q` to the complete physical homotopy fibre,
> cancelling both its forced labelled-residue class (4) and its
> `pureEq+ainc` class (5), with the literal repeated grade and terminal rows.
> Equivariance then produces `C,rho C`; physical `q` closes by the existing
> quotient-defect/generator alternative.

## Verification

```text
python3 computations/verify_h3_reduced_eq_koszul_tate_relative_orbit_gate.py
python3 -O computations/verify_h3_reduced_eq_koszul_tate_relative_orbit_gate.py
python3 -I -S computations/verify_h3_reduced_eq_koszul_tate_relative_orbit_gate.py
```

Frozen ledger SHA-256:

```text
f07e62cab3e9ba76ebb2bdb466bded141ed9bfcaae56aea5a96c336089763560
```
