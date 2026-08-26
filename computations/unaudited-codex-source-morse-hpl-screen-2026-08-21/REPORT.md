# Source-constrained Morse/HPL screen

Status: **exact bounded no-go for ordinary Morse cancellation; no new class**.

The smallest chart-25 source fibre is the chain complex

```text
C1 = <u1,u2,u3,u4>  -->  C0 = <A1,A2,A3,A4,D>,
d(ui)=Ai+D.
```

Its boundary has rank four. Reversing `ui -> Ai` is acyclic and leaves one
critical cell `D`, detected by `(-1,-1,-1,-1,1)`. The ordinary quotient
packet `-A1-A2-A3+D` reduces to `4[D]`, whereas the literal source packet
`-A1-A2-A3-3D=d(-u1-u2-u3)` reduces to zero. Forgetting source provenance
therefore changes the class by exactly `4[D]` and raises augmented rank from
four to five.

This is byte/representation-identical to the frozen chart-25 relative
Schur--Bockstein obstruction: the relative row list equals the Schur local
row list, and the final `D` row equals the signed-lattice canonical missing
class. It is not the degree-nine `H27` mod-four Bockstein. The complete first
neighbour packet has rank 88; adjoining `4D-tau` raises it to 89, with exact
base and augmented minors `-1` and `-4`.

No arithmetic escape occurs. The complete signed source cokernel is the
torsion-free lattice `Z^4`. Under the order-eight chart stabilizer the four
`D` images have Reynolds coefficients `(1,1,1,1)` and remain nonboundary.
Summing the four charts does not cancel them; dividing by four exposes the
primitive nonzero generator `D`. Reduction mod four merely erases the
coefficient and loses source provenance.

The surviving critical cell is a degree-four parallel-pair row, not a clean
pair. The frozen path-forest computation has no source-labelled chain map
from any of its four translates to the cap-error module: it repairs one
degree-six lead, while 72 top terms remain nonforest. The positive chart-26
control does cancel four cap errors with one source scalar, but only on one
normalized coordinate face and one spoke.

Thus ordinary discrete Morse cancellation is source-unsound here. The
source-relative HPL route becomes useful only after constructing the missing
dual-invisible relative edge `d r=4D-tau`; the present archive does not
construct it or control the remote idempotent.

Standard, optimized, and isolated/no-site modes agree at logical SHA
`204275e9269413d195ef8d5df4e84ac8a4b3331b11da1cea25c25410e3036bc3`.

