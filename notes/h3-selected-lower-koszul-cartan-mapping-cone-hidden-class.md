# Gate I's output is physical; its input mapping cone has one occurrence-local class

## The selected square after the Koszul/Cartan completion

The signed lower vector

\[
                         \ell=u_{024}-u_{012}
\]

has twelve nonzero coordinates among the fifteen physical collision labels.
The exact support collapse sends it, after normalization by `1/2`, to

\[
                  \alpha=B_0+B_2-B_3-B_5.               \tag{1}
\]

The literal boundary of (1) has 360 seven-edge features.  On the canonical
normalized `Y=1` output side, the physical cap/Cartan theorem gives

\[
                         O_\alpha-K_\alpha=-M_v,         \tag{2}
\]

so the full alpha augmentation is already physical.  Reversing the mapping-
cone orientation gives the equivalent `M_v=-O_alpha+K_alpha` form used in
the one-chain equation

\[
                         J_3(M_v)=A J_{\rm col}(\ell).   \tag{3}
\]

Thus Gate I no longer lacks an output Eq/residue/eta-sigma cell.  It lacks
the source-labelled input arrow in (3).

This also answers the residual in the cut-swap odd prism.  With the pinned
orientation,

\[
 F_W-\rho F_W-K(u_{012})
\]

has residual `+K d(u012)`.  Its disclosed projections split into the monic
normal Eq face and the twelve-label alpha collapse (1).  The question is
whether this is the complete decomposition.  It is not for the closest
committed source constructor: the additional hidden row is (4).

Checker:
[`verify_h3_selected_lower_koszul_cartan_mapping_cone_hidden_class.py`](../computations/verify_h3_selected_lower_koszul_cartan_mapping_cone_hidden_class.py).

## The exact hidden class

The closest source-provenant Cartan--Spencer constructor has the correct
grade-forgotten secondary class `-delta`.  In four exact fine degrees its
first private face is the endpoint-odd packet

\[
 \boxed{\Xi^-={4\over3}(\xi-\bar\xi-s\xi+s\bar\xi)},    \tag{4}
\]

with

\[
 \xi=q_{01}^{01}q_{27}^{21}q_{34}^{11}q_{35}^{12}q_{67}^{22}.
\]

All four terms have repeated-site profile

```text
(1,1,1,2,1,1,1,2).
```

The formal 341-edge Weyl bar cancels (4) exactly, and endpoint oddization
kills its GHZ target defect.  The failure is physical occurrence descent:
every compatible complete-row endpoint and normalized bar contains a forced
`q37` edge, while the private terms in (4) do not.

The exhaustive finite quotient is

```text
rank(complete endpoints + every normalized/odd bar)        8
rank(after the four physical Hasse faces)                  12
rank(after adjoining Xi^-)                                13.
```

An extended primitive odd dual vanishes on every complete endpoint, bar,
and Hasse face, and reads one on (4).  Relative to this tested physical
constructor there is therefore exactly one new selected class, not an
unspecified collection of hidden rows.

## Why the Koszul cell does not automatically fill it

The normal Koszul generator

\[
 C_K=-\epsilon_F\wedge\epsilon_{\rm Eq},
 \qquad dC_K=-(H_0-u)e_{\rm Eq}
\]

has only its unaugmented Eq face before comparison with the physical
source.  It has no occurrence-local private coordinate, so the odd dual
above reads zero on the bare `C_K`.  Equations (1)--(2) show what its physical
dressing must become, but they do not define the source map that carries
`C_K` or the selected collision chain to the 360 literal features of `M_v`.

Equivalently, adjoining `C_K` closes the normal two-equation Koszul square;
it does not close the occurrence-local naturality square

```text
formal 341-edge Weyl bar  --->  source occurrence resolution
          |                              |
          v                              v
  normal Koszul core       --->    physical +/- M_v.
```

The missing diagonal of this square is exactly (4).

Consequently one cannot use the physically dressed Koszul output (2) to
declare `K d(u012)=M_v`: that would erase (4) by assigning the missing
occurrence-local comparison, which is precisely equation (3).  The new
Koszul/Cartan theorem closes every exposed augmented output row, but does
not silently close this last private input row.

## Sharp remaining lemma

Construct one occurrence-local principal-parts/Weyl-bar lift of the formal
341-edge bar in the four displayed fine degrees.  Its differential must
contain `-Xi^-`, and its augmented image must be the already fixed
`+/-M_v`, including the eta/sigma terminal.  This one cell establishes (3)
for the selected lower vector; a full map on all fifteen labels is not
needed for this branch.

The class (4) is not yet a physical terminal.  The physical `q` row is not
defined on the formal occurrence bar.  Once the lift is physical, `q` is
handled by the existing quotient-defect alternative: zero defect transports
`q`, while nonzero defect gives a protected-kernel relative generator.

## Verification

```text
python3 computations/verify_h3_selected_lower_koszul_cartan_mapping_cone_hidden_class.py
python3 -O computations/verify_h3_selected_lower_koszul_cartan_mapping_cone_hidden_class.py
python3 -I -S computations/verify_h3_selected_lower_koszul_cartan_mapping_cone_hidden_class.py
```

Frozen ledger SHA-256:

```text
c9af24b12ae1829348f6aed4e93a944b24fa418b6255c7372ec028eed4570903
```
