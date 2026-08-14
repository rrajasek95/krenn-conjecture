# The site-repeating enrichment leaves one diagonal seven-dimensional root residual

## Outcome

The `159` site-repeating second-jet coordinates solve a real support problem,
but they do not construct either root-labelled receiving section.  They are
new target rows, not degree-zero operation arrows.  Consequently the
source-derived graph still has

\[
 \operatorname {Hom}^0(\mathrm{response\ jet},\mathrm{AugP2}/K_{Eq})=0.
\]

The exact remaining carrier ambiguity can nevertheless be sharpened jointly
for the `A/B` and `A/C` roots.  For either root, the physical two-word lift
fibre has dimension `21`; all committed parity, Weyl, corner, aggregate,
single-cell and coarse readouts have rank `14`.  The residual is therefore
seven-dimensional.  Every residual vector has zero pair shadow, zero four-
corner value, and is endpoint-odd and Weyl-odd.

Exact checker:
[`verify_h3_site_repeating_two_root_augp2_naturality_residual_gate.py`](../computations/verify_h3_site_repeating_two_root_augp2_naturality_residual_gate.py).

## The joint root calculation

With the two root labels retained independently, the lift space has
dimension `42`.  The two copies of the current rank-`14` readout have rank
`28`, leaving residual dimension `14`.

Now grant the strongest possible response-side naturality: identify every
one of the `21` `A/B` coordinates with its transported `A/C` coordinate.
Only seven of those relations are new after the current readouts, so

```text
two labelled lift fibres                         42
current rootwise readout rank                    28
+ full AB<->AC covariance                        35
remaining diagonal residual                       7.
```

Thus root covariance does not remove the ambiguity; it identifies the two
seven-dimensional copies.  An ad hoc termwise landing on `A/B` without
covariance leaves the entire `A/C` residual.  Conversely, once full
naturality is genuinely part of the map, an injective termwise readout on
one root representative determines both roots.

This is distinct from the two-dimensional operation-Hom quotient.  The
site-repeating rows do not touch that quotient at all: before a physical
augmentation is supplied, neither `A/B` nor `A/C` has an `e_C A e_R`
matrix unit.

## What the termwise `H_w` readout would do

The physical two-word carrier is supported on `180` perfect-matching
coordinates.  The seven residual vectors are honest nonzero vectors in
that coordinate space, so the literal coordinate identity has rank seven
on the residual.  A termwise `H_w`/private-full-nine cap readout would
therefore kill the last diagonal ambiguity.

That is a conditional statement.  The current `r0` packet does not define
those `180` source-term values in the response jet grade.  The `159` new
pair rows likewise have no differential or cap augmentation.  Coordinate
injectivity becomes useful only after a natural dg map into `AugP2` has
been constructed.

The nearest existing polynomial pattern does not provide the map.  The
complete source has the exact Koszul relation

\[
                  H_w r_0-(H_0-u)r_w.
\]

Its complete component has `181` columns, rank `180`, and one kernel
generator.  But it is cap-internal, its Hamming-one word is `01000000`
rather than the receiving-section words, and its typed readout is

```text
(ainc, word, target, ores)=(-H_w,0,H_w,0).
```

Physical target zero therefore kills `H_w` and the anchor incidence
together.  This S-pair cannot be relabelled as a response-to-cap section.

## Exact stopping datum

The shortest positive object is one natural transformation

\[
 A_{\Gamma,\mathrm{root}}:
 J^{\mathrm{red,rep}}_{PS/q}(\mathrm{EqSystem})
 \longrightarrow C_{\mathrm{AugP2},\Gamma}
\]

with two literal instances, `A/B` and `A/C`.  It must:

1. be a genuine degree-zero `e_C A e_R` operation;
2. contain the full `A/B <-> A/C` covariance graph;
3. send `epsilon_s` to `r0` and `c_f` to `-E` with monic normalization;
4. retain all `159` site-repeating rows;
5. define the `180`-coordinate termwise `H_w`/private-full-nine readout and
   have rank seven on the diagonal residual; and
6. preserve the literal word, head, fine, repeated and operation tags of
   both receiving sections.

Under these hypotheses the termwise readout removes the residual seven and
naturality supplies both root-labelled sections.  None of these conclusions
follows from adding the `159` coordinates alone.

This result uses the two-prime `159/153` support replay only at its stated
modular scope.  The `21/14/7` carrier calculation and the joint covariance
ranks are exact over the rationals.

## Verification

```text
python3 computations/verify_h3_site_repeating_two_root_augp2_naturality_residual_gate.py --mode all
python3 computations/verify_h3_site_repeating_two_root_augp2_naturality_residual_gate.py --mode residual
python3 computations/verify_h3_site_repeating_two_root_augp2_naturality_residual_gate.py --mode termwise
python3 computations/verify_h3_site_repeating_two_root_augp2_naturality_residual_gate.py --mode schema
python3 -O computations/verify_h3_site_repeating_two_root_augp2_naturality_residual_gate.py --mode all
python3 -I -S computations/verify_h3_site_repeating_two_root_augp2_naturality_residual_gate.py --mode all
```

Frozen ledger SHA-256:

```text
39aef26317c181880c098a929ec8716ef19d3afaa1bafd222b93cc77edf6236e
```
