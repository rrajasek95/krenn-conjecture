# Proof-first primary theorems

Frontier update: 2026-08-11, after commits `5a01b0a`, `ecb53c5`,
`8855f11`, `05a9d46`, `7320475`, `3836903`, `ebd1ba1`, `8fe3f8b`,
`8f58910`, `222c66d`, `b62a039`, `e35b24c`, `91041f7`, `9fd0de3`, `0373033`,
`9376a3f`, `d354257`, `44c0a37`, and `2304c4a`.

This note organizes the remaining proof around the statements that would
actually advance the dashed clean-point implication.  A computation is
primary only when it proves a bounded case of one of these statements,
finds its first literal obstruction, or falsifies a proposed implication.

## Theorem A: source connectivity, affine accessibility, and active landing

### Target

For a synchronized maximum-anchor, minimum-support one-bad packet satisfying
the unary equation and all four response equations, form the exhaustive
graph of literal matching bases occurring in its occupied complete endpoint
columns.  Then every component must do one of the following:

1. join another component by a certified typed matching exchange;
2. expose a nonflat source-labelled separator and hence a literal active
   carrier;
3. enter an anchor-safe star/triangle/`K2,2` Hall reduction; or
4. admit a complete-column dependence and a support-reducing affine move.

The routed carrier must then acquire distinct heads and four deleted-star
ranks three, or the same source move must strictly lower a global potential.
Iteration reaches the already proved concentrated clean-cap/source-unit
packet.

### Established structure

1. Minimum support gives independent occupied complete response columns and
   a unique full-support circuit modulo the target line.  For a
   three-column circuit a literal `2x2` quotient minor is nonzero.
2. A word-synchronized, oppositely oriented, typed single-`C4`
   common-tail minor produces a source-valid active determinant/cofactor
   carrier.
3. Every coefficientwise-flat even alternating cycle with a nonzero common
   matching tensor is a vertex-gauge/Segre transport, allowing zero
   coordinates and rectangular supports.  The vacuous identically-zero
   equality is not covered.  Thus nonempty flat `C6/C8` geometry is no
   longer an independent problem.
4. For one fixed endpoint star, if its literal base graph is connected,
   typed, and source-exhaustive, flat transport makes all of that star's
   complete columns proportional.  The
   exact one-sided finite move then deletes a component without losing the
   synchronized anchor count.  This works for arbitrary column count.
   Consequently **flat arbitrary `k` is already closed once connectivity
   and exhaustivity are known**.
5. Whole alternating components can be switched without new cells.  A
   nonflat `C_(2r)` with a synchronized distance-three chord shortens to
   `C4+C_(2r-2)`.
6. Cross-intersecting selected hole families have the exact finite normal
   forms star, triangle, and `K2,2`; many strict instances, including the
   co-located Hall-star packet and strict endpoint-complete `K2,2`, are
   closed.
7. The normalized `h=3` target-coloop label family is routed out of its own
   label residual.  Its last
   punctured-`C4` sixteen cases force an alternate bright target matching
   and an off-anchor exit.  It is not the smallest open affine case anymore.
8. The first disconnected four-base test is also sharply reduced.  The
   minimum packet is a unit unless a single silent diagonal `C6` appears.
   Zero response fibres alone admit an injective/no-wedge guard, but every
   genuine fixed-port bright completion forces a two-decoration unary mate.
   All nine fixed-port bright completions are a source unit or a nonanchor
   active carrier (`b4d8568`), hence enter the still-live active-rank/global
   affine interface.
9. On the same minimal decorated support, all nine bright charts are source
   units even with all 48 core endpoint components.  Proportional internal-
   tail contamination preserves the unit, whereas asymmetric contamination
   forces a genuine new literal source edge.
10. At the canonical first `C6` word, dense occupancy is an odd-holonomy
    unit and the `E13` degeneration is a literal typed response chord.  The
    first exact source-typing survivor is the response-silent `E14` pair:
    its common `q14:11` tail becomes an attachment only when the physical
    hole-`14` endpoint product is occupied.
11. In fact the minimal `E14` internal-tail enlargement alone is still a
    source unit in all nine bright charts with arbitrary core endpoint
    variables.  Its `q14:11` contribution contaminates the target and zero
    rows identically through a different hole.  Therefore a genuine survivor
    requires either an outside endpoint route or a second asymmetric internal
    tail (`8fe3f8b`).
12. That first asymmetric one-cell layer is now completely empty.  Complete
    unary rows turn all `1,020` extensions into ordinary source units,
    superseding the response-only reselection split.  The next local packet
    requires at least two simultaneous new internal cells or an outside-core
    endpoint component (`e35b24c`).

### The live proof lemma

The former “word-synchronized chord-or-Hall” target is now better stated as
the **source connectivity/exhaustivity-or-separator theorem**:

> In the complete unary-plus-four-response packet, the first literal base
> outside a flat component either joins it by a certified typed exchange,
> yields a nonflat/common-tail carrier, enters a Hall/lock incidence, or
> supplies an anchor-safe complete-column reduction.

Once this theorem connects the flat inventory, `8855f11` and `05a9d46`
dispose of every flat component, independent of `k`.  For a nonflat long
separator, chord shortening and the typed `C4` theorem finish the
coefficient geometry.  The remaining content is source provenance: the
complete rows must select the typed edge or route the changed tail.

The first bounded endpoint beyond the fixed-port silent-`C6` theorem is now
also reduced on its nine selected private coefficients (`f5af6fd`).  Each
such core-port coefficient has only the fixed and endpoint-swapped
orientations on one identical `q` tail.
Proportional complete columns absorb anchor-safely into the fixed-port
closure.  A diagonal swapped lock removes the selected bright hole and
forces a Hall-colliding reselection.  The sharp survivor is a
nonproportional reciprocal hole-`04` Fitting carrier trapped in the existing
core Hall-accessibility interface.  Surplus nonproportional columns can
enlarge this module and remain part of the global Hall/affine theorem; the
nine-coefficient reduction does not classify arbitrary core-port mass.

### Second live lemma: active landing and termination

Connectivity does not by itself finish Theorem A.  A nonzero carrier can
still have deleted-star profile `(2,2,3,3)`.  The remaining rank theorem
must use a source-labelled companion, pure-anchor reselection, or
anchor-safe simultaneous endpoint move to create a transverse head and
four ranks three.

The termination potential should be defined on

```text
(number of unresolved base components,
 minimum intercomponent alternating distance,
 unresolved lock rank,
 endpoint support).
```

Flat arbitrary-`k` contraction is no longer a separate coordinate.  What is
unproved is that every nonflat/Hall/endpoint return decreases this potential
or lands at the active clean-cap interface.

## Theorem B: one physically typed augmented comparison

### Target

Construct one derived-to-physical augmented comparison in a fixed pentagon
fine grade.  It must preserve source boundary, physical `W`, target,
ordinary residue, and endpoint/output word grade.  Its source part must lift
the five adjacent pentagon differences by zero-anchor collision cells, and
its target part must identify

```text
derived Yw             -> physical cap coordinate W.
```

The chart value `-S_v` is a diagnostic of the derived correction, not
physical anchor incidence.  Once the physical polar map exists, Fredholm
either constructs the separate primitive anchor combination or supplies the
rootless annihilator.

After this comparison is constructed, the five physical polar columns

```text
P : k^5 -> coker(Jhat)
```

are defined in the correct physical quotient.  The established Fredholm
alternative then supplies either the relative generator or the rootless
Component-III annihilator.

### Established structure

1. The five-column augmented pentagon has an exact
   generator-or-annihilator alternative once physical `P` exists.
2. A non-Euler colour-diagonal GHZ-stabilizer pair gives genuine physical
   first jets modulo site-Euler gauge.  It has zero source, target, and all
   fifteen selected ordinary residues; its marked Hessian sector is exactly
   `h_v` with coefficient one.
3. The complete corrected mixed Hasse row has two identical physical chart
   lifts.  Their primitive difference `k_v` is correction homology, and the
   marked chart cochain reads one on it.
4. Because `k_v` is a genuine presentation syzygy, a free resolution may
   adjoin `b_v` with `d b_v=k_v`.  The shifted indexed Hasse/Koszul
   construction supplies

   ```text
   (d,tgt,ores)(n_v)=(h_v Yw,0,0)
   ```

   with the required chart correction `-S_v`.  This is a valid derived
   chain-map extension.  The failed underived diagonal projection and its
   monic `(H_0-u)e_Eq` commutator rule out only that particular comparison;
   underived polynomial descent is sufficient, not necessary.
5. Zero indeterminacy is no longer an independent hard theorem after the
   physical typing exists.  If the physical anchor readout kills
   `ker(Jhat)`, `P` is well defined.  If it does not, a detected kernel
   element normalizes directly to signature `(-1,0,0,0)` and is already the
   relative generator (`0373033`).
6. A single-face physical comparison is impossible in the complete first
   collision degree.  One multiplied route has a private ordinary-residue
   unit.  The first residue-zero source boundary is the adjacent two-face
   `P3 disjoint-union K2` S-pair; it has physical anchor incidence zero and
   requires a new higher collision cell.  The primitive anchor is a separate
   mapping-cone datum (`255eb8a`).
7. The formal adjacent collision edge already exists as a denominator/PP
   S-pair with the correct ridge boundary and zero coarse readouts.  Physical
   descent adds exactly `delta_v*(H_0-u)*e_Eq`.  A primitive
   `pure-Eq+ainc` covector excludes every bounded polynomial/cap correction.
   Thus the first missing physical cell is a zero-anchor reduced Eq face
   cancelling this term; the degree-five compatibility is already exact
   (`9fd0de3`).

### Missing lemma

The load-bearing task is the **physically typed comparison theorem**.  The
pair `(b_v,-n_v)` is presently only a cone homotopy.  Its chart scalar cannot
be renamed as physical anchor incidence, and its derived terminal is not yet
the physical `W` readout.

Thus the missing proof is no longer “construct first jets, then separately
solve marked descent, then separately prove zero indeterminacy.”  The first
jets and derived filler exist, and zero-indeterminacy failure is useful.  We
must construct or separate one augmented comparison with the physical
source and target typings above.

The source side must genuinely change physical degree.  The first pentagon
syzygies have repeated-site degree `P3 disjoint-union K2`, whereas the known
normal/chart Hasse fillers are site-squarefree.  The minimal positive datum
is a five-cell cyclic family

```text
d E_v = -r_v+r_w,
(W,tgt,ores,ainc)(E_v)=(0,0,0,0),
```

with the known degree-five compatibility.  After these zero-anchor edges
make the physical pentagon map well typed, the separate primitive anchor is
obtained—or replaced by the annihilator—by the established Fredholm
alternative.  A positive comparison therefore cannot merely rename the
existing derived filler.

More precisely, the strict PP edge is already constructed.  It becomes
physical as soon as one builds

```text
d C_v = -delta_v*(H_0-u)*e_Eq,
(W,tgt,ores,ainc)(C_v)=(0,0,0,0).
```

This reduced Eq face is now the earliest rootless construction target.
One such polynomial collision/reduced-Eq family automatically prolongs
through normal orders one to three.  It leaves one primitive aggregate
cokernel in each grade, all filled by the jet copies of a single polynomial
primitive-anchor family.  No third physical generator type appears at
higher normal order (`2304c4a`); the derived `Yw -> W` comparison remains a
separate map.

## Theorem C: use the same comparison on the inactive side

### Face-open candidate

On `D(h_v)`, the derived filler has the normalized scaling

```text
(kappa/h_v)n_v,
```

whose derived boundary is `(kappa Yw,0,0)`.  Therefore the first hard
rootless cell and the first inactive cap cell have one common candidate.
If the comparison of Theorem B identifies derived `Yw` with physical `W`,
this scaled chain is exactly the missing target/residue-invisible
Component-IV cap direction.

This is a conditional consolidation on the target side, not an assertion
that the repeated-site rootless source cell and the inactive normal face are
literally the same.  It is not a physical generator: the
primitive physical separator `E+W+T-O` still reads one on the desired cap
column and zero on every old physical lower face.

### Face-zero locus

The simultaneous locus `V(h_1,...,h_5)` remains separate.  On its dense
cyclotomic `C5` torus stratum, the normal/Rees comparison is full rank and
lifts to all orders in the chart module, with target and old residue zero.
There the naked regularized difference has boundary
`Yw+(H_0-u)e_Eq`; the single complete normal Hasse face
`s_ut(q_0)[nu]` cancels the Eq term in all four indexed grades.  After the
exact normal inverse, this is an all-order derived filler with boundary
`Yw` and chart correction `-S_v` (`827e329`).

The nondense support is now classified.  Every feasible exact support is
either intersecting (star/triangle type) or has one isolated vertex and an
induced `C4`, `K4-e`, or `K4`.  The first two and generic `K4` have normal
rank five and inherit the relative-derived repair.  The exact singular
first-order strata do not survive to all orders: the cyclotomic isolated
`K4` missing covector is hit by an explicit second Hasse coefficient, and
every intersecting support has a full weighted-normal system of degree at
most three (`d354257`).  The remaining theorem is not another support
classification.  Complete derived companions through orders one, two, and
three now assemble those systems with zero target and old residue
(`44c0a37`).  Their exact first defect is physical: the normal-indexed mixed
row has no homogeneous site-squarefree image.  This is precisely the same
collision/reduced-Eq family, primitive-anchor family, and `Yw -> W`
comparison already isolated in Theorem B; the two generator families
prolong through all required orders (`2304c4a`).

Physical promotion on the dense stratum needs more than the face-open
identifications: the comparison must also carry the complete indexed normal
face `s_ut(q_0)[nu]` and glue it to the physical correction module.  It is a
goal to extend the comparison of Theorem B with this normal-face
compatibility, not an automatic consequence of `derived Yw -> physical W`.

### Final coupling

Even after the first physical cap direction is constructed, the final
horizontal rootless/inactive comparison must preserve both readouts and the
common fine grade.  The inactive Omega/Bezout and certificate-bracket
prolongations are already proved after this input.  The diagonal inactive
branch retains its separate source-level Rees membership/routing condition.

## Proof allocation

1. Prove the source connectivity/exhaustivity-or-separator theorem first in
   the `h=3` two-component and arbitrary-core-port packets.
2. Prove active carrier rank landing and a strict component/endpoint
   potential.  This finishes Theorem A.
3. Construct one physical adjacent-face collision edge in its repeated-site
   grade, extend it cyclically with the degree-five compatibility, and land
   derived `Yw` in physical `W`.  Do not require an underived diagonal
   representative or identify chart `-S_v` with anchor incidence.
4. Extend that comparison over the dense and normal-rank-five face-zero
   strata, carrying the complete normal Hasse face and identifying derived
   `Yw` with physical `W`.  The explicit order-two and order-three derived
   companions on every singular stratum are already assembled; carry them
   through that one physical comparison.
5. Apply the indeterminacy-or-generator and Fredholm alternatives, then
   complete the common horizontal/inactive routing.

Every new finite audit must name which one of these proof steps it proves,
routes, or falsifies.
