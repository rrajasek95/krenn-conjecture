# The canonical principal-parts collision map does not define GammaJetEnrichment

## Exact conclusion

The proposed construction has a canonical, useful response-valued core, but
it does **not** construct the required physical map

\[
J_{\mathrm{phys},\Gamma}:P_{\mathrm{official}}\longrightarrow Y_\Gamma.
\]

The official order-six principal-parts block has 8,580 columns.  Its only two
fine words are

\[
11111111\quad(6381\text{ columns}),\qquad
11211211\quad(2199\text{ columns}),
\]

whereas the cap landing has word `01211222`.  Its site-repeating projection
has 159 coordinates and rank 153 over each pinned large prime.  Those 159
coordinates have an exact source-topological decomposition:

* 148 are pairs of distinct decorated edges sharing one site, hence P3
  collision coordinates;
* 11 use one underlying edge: four are off-diagonal same-edge recolourings
  and seven are diagonal Euler/divided-power faces.

The last 11 are not primitive classes.  In the augmented
trigger/triangle/Euler simplex they are proper faces: the seven diagonal
directions are absorbed by the divided-power Euler completion and the four
same-edge recolourings by its off-diagonal trigger completion.  After
minimalizing this exact sector, the surviving 148 shared-P3 coordinate map
has rank 146.  This is the canonical principal-parts core.  It remains in
the response object and in the two response fine summands.

## What the \(1/6\) average proves

For the 21 unordered pairs in the site-0 star, the collision outputs have
rank 7.  Every one of the 90 retained matching parents occurs six times, so

\[
\frac16\sum_{1\le i<j\le7}\Phi(dC_{ij})=H
\]

is an exact coefficient identity.  Formally adjoining AB and AC labels gives
a direct-sum rank 14 calculation, but the official EqSystem does not contain
those root-path labels.  The termwise trigger construction has 540 branches
per formal root and 1,620 remote commuting product faces.

The full augmented trigger simplex supplies the additional homogenizer and
has exact response boundary `dG0=H-u`.  The *collision average by itself*
is not yet a chain functor on the full Taylor/Hasse cube.  The
parent-labelled deletion calculation has 1,152 commuting kept-factor flags,
but 1,020 noncommuting deleted-factor flags and nine collected-lcm
ambiguities.  Each deleted flag needs a mapping cylinder.  Moreover the star
average has boundary `H`, not the needed homogenized `H-u`; its first missing
face is `-u*e_Eq`.

The first literal collision Tate cell confirms the categorical issue.  Its
official primitive second Hasse face vanishes; its source-valid relative Tate
replacement has a 30-term boundary and operation endpoint
`response -> response`.  It supplies no `response -> AugP2 cap` matrix unit.

## Why B/Eq is not a canonical cotangent decoration

This is not repaired by declaring B/Eq tags on the native conormal module.
In one native relation slot write its degree-one generator as `e`.  Stabilize
the first Tate presentation by the contractible pair

\[
d h=k,\qquad d k=0,
\]

and put

\[
B=e+\tfrac12k,\qquad Eq=e-\tfrac12k.
\]

Both forget to the same native generator `e`, while

\[
B-Eq=k=dh.
\]

A separator with values \(\omega(B)=1\), \(\omega(Eq)=-1\) evaluates to 2
on the boundary `dh`, so it does not descend to conormal/cotangent homology.
Tensoring this stabilization with the six fine monomials and eight Boolean
divisor masks gives 48 contractible copies.  All 72 Hasse and 72 reverse
Macaulay edges act diagonally and commute with `dh=k`.  Consequently
differential and Macaulay functoriality alone cannot select the B/Eq split.
The two stabilized lifts do **not** survive minimalization—their difference
is contractible by construction.  This is a non-descent certificate for the
B/Eq readout, not a claimed primitive homology class.  Quotienting it leaves
the rank-146 shared-P3 response map and still supplies no cap operation.

The canonical native data are the EqSystem relation word, its 252-variable
torus multidegree, principal-parts order, and literal cell support.  The B/Eq
anti-diagonal, response/cap idempotent, AB/AC root path, normalized target,
and protected cap rows are additional physical structure.

## Minimum missing theorem

A literal terminal matrix requires a stabilization-invariant decorated
principal-parts/cotangent lift with all of the following:

1. physical response and AugP2-cap idempotents and AB/AC root paths;
2. a noncontractible B/Eq filtration, normalized target, and protected rows;
3. the 1,020 deletion cylinders making the collision map a chain map;
4. a proof that the associated `Gamma*` grade exhausts physical primitive
   columns.

Without that lift, a semi-free tagged registry is discretionary: two
quasi-isomorphic source presentations have the same official jets but may
give opposite B/Eq readouts.  Therefore the previously constructed
`omega_Eq` terminal remains conditional on this precise decorated
principal-parts/completeness theorem.

## Reproduction

```bash
python3 computations/verify_h3_canonical_principal_parts_gammajet_enrichment_gate.py --mode structural
python3 computations/verify_h3_canonical_principal_parts_gammajet_enrichment_gate.py --mode full
python3 computations/verify_h3_canonical_principal_parts_gammajet_enrichment_gate.py --mode exhaustive
```

The frozen full ledger digest is
`bde9561f4f4ade5d6f9efba100bb53aa1ea7007fbea5ca1b713ef348a91ffac4`.
