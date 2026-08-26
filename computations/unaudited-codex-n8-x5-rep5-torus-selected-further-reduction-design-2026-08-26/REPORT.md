# Selected rep5 73/6561 torus chart: further exact reduction design

Verdict: **an exact further reduction exists**. Expanding all 6,561 source-labelled equations gives 254,598 terms and an exact grading matrix of rank 72/nullity 1. Its primitive residual torus has weights `+1` on `A04[20..22]` and `-1` on `A35[21], A35[22], A37[20]`.

An exhaustive six-coordinate comparison selects `q=A37[20]` (weight `-1`). The root-free identity `D(q) union V(q)` yields two exact 72-variable sources: on `D(q)`, use `lambda=q` to gauge `q=1`; on `V(q)`, set `q=0`. Both 6,561-generator sources were canonically expanded and byte-reparsed against their specializations. The open chart has grading nullity 0; the closed chart retains nullity 1, so this is an exact smaller cover but not claimed terminal.

No coordinate is amplitude-inactive, no generator is affine-linear, no unit-coefficient graph substitution exists, and the variable interaction graph is one 73-node component. The full linear-part rank is 43. No further determinant/minor is globally invertible; a new such choice would require another exhaustive split. `dp` versus block order remains only a future performance benchmark, not an exact reduction.

No Singular process or ideal solve ran. This package establishes design equivalence only and makes no mathematical-coverage or rep5-closure claim.
