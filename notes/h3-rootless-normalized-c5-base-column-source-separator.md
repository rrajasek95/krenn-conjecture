# The normalized C5 base column is absent from the complete first physical inventory

## Exact bounded theorem

Work on the exact target-preserving normalized specialization of `7c6d431`,
with all \(R_v=0\). Fix one repeated-site \(P_3\sqcup K_2\) fine degree.
The clean collision edges are

\[
 dE_v=-r_v+r_{v+1},\qquad
 (W,\operatorname{ainc},\operatorname{tgt},
       \operatorname{ores})(E_v)=(0,0,0,0).            \tag{1}
\]

They span the saturated rank-four incidence lattice of \(C_5\). The
smallest physical base requested by `8c42d66` is

\[
 P_v=(-r_v,\operatorname{Eq}=0,W=1,
       \operatorname{ainc}=-1,operatorname{tgt}=0,
       \operatorname{ores}=0).                         \tag{2}
\]

After multiplying by the selected face/incident-cycle factors (all equal to
one on this slice), the closest existing cap/source combination is the
diagonal coefficient

\[
                    r_0-T=(\operatorname{Eq}=1,W=1,
                     \operatorname{ainc}=-1,0,0).      \tag{3}
\]

Thus (3) already has the correct cap, anchor, target, and residue values.
It fails in two independent physical coordinates:

1. it retains one pure-Eq conormal component;
2. it has no primitive ridge-vertex boundary.

Here `Eq` denotes the normalized conormal coordinate
\((H_0-u)e_{\rm Eq}\), not its numerical value at a solution. The required
correction is exactly

\[
                P_v-(r_0-T)=-r_v-e_{\rm Eq}.           \tag{4}
\]

## Two primitive separators

Put the five ridge coordinates first, followed by
\((\operatorname{Eq},W,\operatorname{tgt},
\operatorname{ores},\operatorname{ainc})\). The complete existing coarse
image consists of the five edges (1) and

\[
 r_0=(1_{\rm Eq},0,1,0,-1),\qquad
 T=(0,-1,1,0,0),\qquad
 \rho=(0,1,0,1,0).                                    \tag{5}
\]

After imposing every other literal source-boundary coefficient, its
admissible coarse image has rank seven. Two primitive integral covectors
annihilate every column in (1), (5):

\[
 \epsilon=\sum_v r_v^*,\qquad
 \lambda=e_{\rm Eq}^*+\operatorname{ainc}^*.          \tag{6}
\]

On the desired column (2),

\[
                         \epsilon(P_v)=\lambda(P_v)=-1. \tag{7}
\]

Hence adjoining (2) raises rank. This conclusion survives the selected-cell
Laurent normalization: both covectors concern source/readout labels, not
the numerical values of \(a,b,c,d,e\).

The pins make the inventory statement coefficient-complete in the first
repeated-site layer:

* all 288 polynomial full-nine row/multiplier columns in each of the five
  \(P_3\sqcup K_2\) degrees and both chart copies;
* the literal denominator/PP collision routes and their ordinary-residue
  companions;
* the complete old cap block (5); and
* the squarefree Hasse/normal faces that could be proposed before the site
  degree is shifted.

The complete multidegree theorem shows that the full-nine/Tate-compatible
kernel has zero physical anchor and cap readout. The single-face collision
theorem shows that changing to the repeated-site degree creates a private
residue and forces the adjacent two-face S-pair (1), whose anchor is zero.
Therefore no omitted column of this existing inventory escapes (6).

## Why the normal face does not repair (3)

In the indexed derived presentation the completed normal Hasse face cancels
the Eq term in (3). But it is squarefree, its terminal value is the chart
label \(-S_v\), and it has no defined physical ridge or anchor incidence.
Multiplying it by the incident selected cycle edge to enter the repeated
degree triggers the private-residue calculation just described; cancellation
then forces the adjacent edge (1), not a vertex.

Equivalently, the two formal repairs in (4) are

\[
 C_v^{\rm Eq}=-e_{\rm Eq},\qquad A_v=-r_v.             \tag{8}
\]

The first is detected by \(\lambda\); the second by \(\epsilon\). Neither
is an existing physical cell. They may ultimately be supplied by one
combined higher relative generator, but normal-face relabelling or old cap
correction does not construct it.

The pointwise equality \(H_0-u=0\) on a source solution does not remove
this source-level obstruction: (2) must be a chain in the augmented source
complex, and the conormal coefficient in (3) is precisely the failure of
that chain identity. The result is therefore stronger than a numerical
Jacobian coincidence at the normalized point.

## Consequence and scope

Fredholm remains unavailable on this specialization because the physical
five-column polar map still lacks one base image. The earliest exact new
datum is a source-valid cell with the combined boundary/readout (2), or
separate cells (8) whose sum corrects (3). After one such column exists,
the clean edge propagation and the `0373033` dichotomy apply.

This is a complete theorem for the currently audited first repeated-site
source/PP/cap inventory. It does not rule out a genuinely new higher
relative generator.

Run:

```text
python3 computations/verify_h3_rootless_normalized_c5_base_column_source_separator.py
python3 -O computations/verify_h3_rootless_normalized_c5_base_column_source_separator.py
python3 -I -S computations/verify_h3_rootless_normalized_c5_base_column_source_separator.py
```

Frozen ledger SHA-256:

```text
e90edede01f8008725630a630c2a8ec1ac54eff68fecbaa12b97664a5198766c
```
