# Proof-first primary theorems

Frontier update: 2026-08-11, after commits `5a01b0a`, `ecb53c5`,
`8855f11`, `05a9d46`, `7320475`, `3836903`, `ebd1ba1`, `8fe3f8b`,
`8f58910`, `222c66d`, `b62a039`, `e35b24c`, `414f4c6`, `91041f7`, `9fd0de3`, `0373033`,
`9376a3f`, `d354257`, `44c0a37`, `2304c4a`, `7c6d431`, `8c42d66`,
`8771755`, `bd9e172`, `729eb41`, `727de71`, `65518ac`, and `43b6038`.

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
13. Every simultaneous pair of new internal cells is also an ordinary
    two-row source unit: all `57,291` records close in complete `G11`, unary,
    or `G22` coefficients (`414f4c6`).  The earliest same-chart survivor
    therefore requires at least three coordinated cells.
14. The cubic top layer is now exhausted too: all `2,126,208`
    three-new-internal-cell specializations are ordinary `G11`, unary, or
    `G22` source units (`c13911e`).  Since the equations are multiaffine of
    degree at most three, no new local monomial type appears at larger
    support.  The remaining issue is witness gluing: the winning row varies
    with the triple, while the universal target retains `24/26` private
    monomials.  The exact next lemma is a triangular/standard-basis
    reduction eliminating those private terms while retaining the target
    constant.
15. That reduction now has a precise first syzygy.  Every attempted `G11`
    leading-term order meets a two-cycle swapping the two endpoint
    orientations of one common bright tail.  Complete unary rows break all
    `228` private cycles, but the source-provenant multiplied S-pairs carry
    degree-three tails in `24` cases and degree-four tails in `204`
    (`6e5878e`).  The next lemma is reduction of these unary-times-q
    Buchberger tails; `G22` cannot remove them directly because its endpoint
    colour grade is separate.
16. That reduction now stabilizes at nine unary-word orbits and three
    factorizations.  Every return factor involves only the two missing
    chords `q04:00,q13:00`; singular factors activate a chord and route to
    the crossed-`C4` theorem, while the chordless locus leaves a private
    self-loop.  Neither its zero nor unit specialization removes the class
    (`2c981a6`).  The first missing combinatorial row is therefore a
    same-word endpoint/companion attachment.

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

The newest comparison identifies one common operation behind that missing
provenance.  The rootless companion `q_(1,23|45)` is literally the decorated
`2K2` core in one E14 S-pair orbit after a fixed site relabeling and colour
swap (`2957235`).  The surrounding source grades do not match, so it is not
an existing row.  In the minimal quotient
`(E_+,E_-,Omega,qcomp)`, the required chain has boundary
`A=(1,-1,1,-1)`.  With the existing bar `(0,0,-1,1)` and signless endpoint
sum `(1,1,0,0)`, it splits the two orientations with determinant `-2`
(`744cd9a`).  This endpoint-word-change homotopy is the strongest current
candidate for the source-connectivity theorem.

That candidate is now reduced to one coefficient-level lift.  On a literal
equal common tail, the complete marked five-lock component is an even
relative incidence path, so its alternating row sum is already
`D=E_+-E_-`; the rootless bar then gives `A`.  One unequal tail is the exact
endpoint-holonomy obstruction (`727de71`).  Independently, the mixed
bar--curvature Massey chain constructs `D` at the exact rootless word and
with zero target.  It fails only because its ordinary residue is carried by
`a24:11*a35:11`, while the rootless bar carries the aligned companion
`a24:21*a35:12`; subtraction leaves their primitive Segre-corner difference
(`43b6038`).  The reciprocal Hasse--Bianchi row cannot supply it: all its
endpoint projections are signless and common multiplication preserves this
parity (`65518ac`).

The fastest positive statement is therefore:

> **Residual-q Kodaira--Spencer relative-cell theorem.**  In word `1211222`
> and the labelled repeated `P3+K2` grade, construct one physical relative
> cell which cancels the complete private full-nine boundary, transports
> `11|11 -> 21|12` with ordinary residue `-delta`, has
> `D=W=target=ainc=0`, obeys
> `dr_v(eta_z)=1+delta_vz*u_z/t`, and carries the facewise sigma correction
> `-q_pq:22`.  If no such cell exists, prove this using the exhaustive
> physical augmented map; only then does its left kernel give the separator.
> If lifts exist but their terminal values differ, that kernel difference is
> already the normalized relative generator.

The standard two-tail transport cannot supply this cell because its residue
and main boundary satisfy `R=D` (`c66e393`).  The additive eta primitive
cannot be multiplied into the residue in the fixed grade (`c6f39eb`).  The
coarse cap identity factors the desired residue through a reduced-Eq face,
but a literal private matching pivot of the pure row obstructs the lift
(`e6deb15`).  The complete doubled chart has `576` columns of rank `288`,
and its kernel is exactly the `288` pairwise `pq-pr` presentation
differences.  Each cancels the entire physical column and every
chart-neutral terminal; the chart-odd Hasse value is not a physical residue
or stabilizer readout (`4291ccc`).  Thus the open statement is genuine
relative-source image membership, not another scalar, quotient, or chart-
kernel identity.

The literal target is one aggregate mapping-cone cell `M_v`: its boundary
must cancel the four selected complete matching columns (360 literal terms),
its Eq corners are fixed by `alpha=-delta`, its protected readouts vanish,
and its eta/sigma values are the ones displayed above (`45ed42d`).  This is
the smallest sufficient source direction; current rank does not require four
independent cells.

There is now a canonical principal symbol for `M_v`.  Literal two-site
colour covariance transports the complete `11|11` tail row to the
`21|12` tail row term by term.  Commuting this transport with the
endpoint-odd curvature gives coefficients `alpha=(-1,1,1,-1)`: its scalar
fourth-Hasse top and codimension-one shadow vanish source-word by source-
word, and its first nonzero face is exactly
`(E_- - E_+)(T_0-T_1)=-delta` (`52d5baa`).  Therefore the remaining first
theorem is a relative Spencer nullhomotopy of this one explicit commutator,
with the full `B_j`/Eq/eta/sigma image.  Bare covariance does not prove it,
because the existing physical transport remains locked by `R=D`.

The source side of this nullhomotopy is now proved.  An exact 248-term
linear-coefficient order-five correction completes the lower faces and
annihilates the three pair generators literally (`6bed6ae`).  It remains in
the two required commutator fine shifts, with no leakage (`591187c`).  Its
natural eta/sigma response is zero, so the first theorem has narrowed again:
construct the physical relative fiber-product map gluing this source
homotopy to the formal `t-u_v` eta and `-q_pq:22` sigma terminal corrections.
Do not repeat the source-row rank calculation.

The ordinary linear-coefficient order-five enlargement is also exhausted
(`3152336`, `636f9f7`, `463b0b9`).
Among all 252 decorated coefficient cells, only the direct-free cell
`36:11` enters the required fine shifts.  Its 180 operator columns have a
152-dimensional source kernel and even contain a two-term integral cycle
detected by the scalar `-delta` pairing.  But the complete sixteen-coordinate
shadow raises rank `135 -> 136`; an exact 14-source/12-shadow left separator
certifies non-membership.  This is a bounded dual, not yet a physical
terminal functional.  Indeed the shadow-only projection misses the singleton
face `07:11 wedge 24:11`.  It proves that another linear/order-five
coefficient or kernel search cannot supply `M_v`: the missing map is
genuinely relative.  Higher coefficient/order towers are not covered by this
audit, but would have to supply that same face with the relative terminals.

The first such higher layer succeeds on the entire source shadow
(`1e923cc`).  Among 8,580 correctly graded quadratic-coefficient order-six
operators containing the missing face, an exact 188-term rational chain has
zero literal boundary on all three pair generators and complete
codimension-two shadow `-delta`.  Every term factors through
`d_07:11 d_24:11`, leaving a quadratic-coefficient order-four operator.  Its
coefficient cells still have zero natural eta/sigma character.  Therefore
the local source-and-residue construction is complete through order six;
only physical repeated-grade typing, alternating Spencer totalization, and
terminal gluing remain.  The unsigned higher-face tower is already complete:
`L_0=L_1=0`, `L_2=-delta`, and
`down(L_(k+1))=(6-k)L_k` through the top layer (`9bd3533`).

This also simplifies the fiber target (`cc2d607`).  Conditional on physical
typing of the order-six chain, subtracting it from the former combined
residual/eta/sigma target leaves a terminal-only relative direction: zero
source boundary, residue, `D`, `W`, target, and anchor, with only
`eta_z=1+delta_(vz)u_z/t` and `sigma=-q_pq:22`.  No vector in the entire
8,580-column ordinary order-six block can carry those terminals.  The
remaining construction is therefore a shifted Cartan/Spencer comparison,
not another private-boundary or residue calculation.

More precisely, the remaining terminal class is uniquely
`gamma_v=-dOmega_v` (`202d79e`).  This one relative Kähler class has exactly
the required eta and sigma contractions and zero ordinary/protected faces.
Its `pq` and `xv` halves have different site degrees; their ordinary lcm
completion is `t*b-u*a`, whose terminal law is wrong.  Thus the remaining
source theorem is a chart-nondiagonal, labelled shifted first-jet lift.

Moreover the common primitive face `07:11 wedge 24:11` is an endpoint arm
with a disjoint cofactor tail.  Under the same physical typing, choosing its
internal endpoint target-full and its colour visible in the outer quotient
changes the overlap profile `(2,3)` to `(3,3)`.  This conditionally merges
the residual comparison theorem with the first one-sided rank landing.

Conditional on the cell, the E14 self-loop and unequal-tail five-lock
holonomy close and the typed-component potential decreases (`2593831`).
This does not restore transverse physical rank.  The dual/generator claims
remain conditional on exhaustive source typing of the repeated grade; the
current bounded parity/Segre covectors are not global Macaulay functionals.

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
still have deleted-star profile `(2,2,3,3)`.  A dependence among occupied
complete columns in one fixed endpoint row gives an explicit anchor-safe
support deletion (`0a965e7`).  After excluding that kernel, full-nine
incidence guarantees at least two internal target-full sites; attaching one
endpoint arm to such a site restores rank three there (`70eb104`).  The
remaining defect is therefore one-sided: visibility in the deficient
quotient at the opposite endpoint.  A smallest target-coloop counterguard
shows that endpoint-orientation rank two alone does not provide this
visibility.

The remaining rank theorem must therefore make a literal common-`q`
exchange produce either such a same-row dependence, or an overlap through a
target-full site followed by a column visible in the remaining deficient
quotient.  Only the second alternative creates the transverse head data
needed for four ranks three; Hall and termination remain separate.

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

On the selected nonzero `C5` torus, a target-preserving degree-two etale
gauge kills the five pure-Eq defects and descends literally.  It proves the
exact `C5` specialization clean.  A general selected-cycle chart retains
only `R_v-R_w`, the difference of off-cycle companion tails (`7c6d431`).
Those tails do not yet have a synchronized endpoint-star/common-tail lift,
so this does not reduce Theorem B to Theorem A without a new attachment
statement.

The ten off-cycle tail monomials are pairwise distinct.  Conditional on an
active forced response hole, its complete six-term row proves the desired
attachment trichotomy: unit, same-tail deletion/Fitting, or different-tail
`C4` off-anchor/Hall.  The exact remaining input is response-hole
accessibility; normalized internal `C5` data alone do not force that endpoint
product (`8771755`).

The response-dark version of this obstruction is now eliminated.  Every
nonzero residual `R_v-R_w` contains an off-cycle chord whose complete
five-tensor column is either zero—hence exactly deletable, contradicting
minimum support—or exports a literal unary/response carrier.  The audit is
uniform over all ten tails and fifteen chord occurrences (`d5b8ebc`).  Thus
the residual-tail branch now lands directly in Theorem A's already named
affine/Fitting/Hall promotion problem; there is no additional C5 attachment
theorem before that interface.

Universally, the bare ten-tail quotient has rank four because all `21`
relevant complete coefficients have positive endpoint-use grade.  The
missing typed inputs are exactly ten unary spokes and forty response
brackets/eighty orientations (`bd9e172`).  Thus accessibility is a genuine
source attachment theorem, not a hidden row-span consequence.

On the exact `R_v=0` specialization, the five clean physical edges leave one
aggregate comparison class.  One physical base column with the prescribed
`Yw -> W`, boundary, anchor, target, residue, and fine-grade signature would
be sufficient: edge propagation defines the other four and then Fredholm is
immediately available (`8c42d66`).  The new source audit shows, however, that
this column cannot be obtained by the two tempting short routes.

First, the marked unary row has `105` terms, of which `90` die under
`p_0=s_0=0`; the surviving terms are the marked base, two same-reset face
changes, four translated `C4` mates, and eight translated `C6` mates
(`467d545`).  The complete q-only transition graph has five disjoint
15-vertex components indexed by the reset word, so the desired full-colour
spoke is not reached by iterating these rows (`f3e4b01`).  Second, although a
unit-valued aggregate image would be enough in a general cyclic attachment
module (`0e117b8`), the literal clean denominator identity gives

```text
sum_v h_v y_v = 0.
```

Here `h_v=1`, so every physical denominator-kernel image has aggregate zero
(`ba52560`).  The positive Tor-filler branch is therefore absent on the clean
cycle.

What remains is sharper: the clean branch forces a primitive aggregate
**separator**.  The first endpoint/Bianchi degree has cokernel `Z^5`; after
cyclic edge gluing and the still-conditional `Omega_v -> r_v` comparison it
reduces to one aggregate `Z`.  No audited first-degree cell supplies either
that comparison or the required `(-Q,ores=-1)` transgression.  The first
common physical grade is the repeated-site `P3 disjoint-union K2` grade.  A
candidate separator is now explicit—value one on the endpoint ridge,
q-companion, and rootless ridge classes, and zero on Eq, W, target, residue,
and anchor incidence—but it does not descend through the complete physical
kernel.  The five colour-diagonal target stabilizers give pairings
`-5-u_z/t`; including them reduces the old `(Omega,Q,r)` covector space from
dimension one to zero (`586f885`, `d7ff17d`).  The formally unique correction
on that five-direction slice is

```text
sum_v Omega_v + 5t - sum_v u_v
  = 5 q_pq^22 - sum_v q_xv^(0,m_v),
```

but two further physical stabilizers show that this scalar is not invariant,
and it has no source-typed augmented readouts (`a9f64aa`).  Thus the clean
theorem is no longer merely separator promotion.  It must construct a new
physical `Omega <-> r` comparison carrying the compensating stabilizer law
`5+u_z/t`, or turn the failure of that comparison into the relative
generator.  Unary-only, positive aggregate-Tor, and old-coordinate covector
repairs are all excluded.

This comparison now has an exact minimal presentation.  In one labelled
repeated degree it is the same-companion lift

```text
P_tilde_(v,N)=(-r_v,+Q_(v,N); ores=1),
```

whose difference from the endpoint bar has boundary
`-t_v Omega_v+r_v` and zero augmented readouts (`947ce8e`, `3e64181`).
No committed Hasse, PP, full-nine, cap, normal, or Tate cell supplies it.
The five cyclic copies first share degree `abcde`; their weighted aggregate
`A` has lower boundary `d_0 A=5abcde`, so it is not an absolute
matching/Pluecker cycle.  A positive construction must contain a genuinely
relative augmentation `U` with `d_0 U=abcde`, making `A-5U` a cycle
(`252bdc8`).  This is the current smallest construction target.

The ordinary source inventory does not already contain that `U`.  The sole
`abcde` occurrence is a multiplier of the pure unary row and has augmented
column `(lower,ainc,W,tgt,ores)=(1,-1,0,1,0)`, whereas `U` must have
`(1,0,0,0,0)`.  The primitive functional `lower+ainc` separates them, and
the complete top-degree source map is injective (`6c76d22`).  Consequently
neither Laurent normalization nor an omitted full-nine top correction
constructs the relative augmentation.

The relative augmentation is nevertheless not a third independent proof
input.  Existing target/cap rows give the exact normalized lift
`x=(lower,ainc,W,tgt,ores)=(1,-1,0,0,0)`.  For the preserved map omitting
anchor incidence, either anchor is nonzero on its kernel—in which case the
normalized kernel element is already the primitive relative generator—or
anchor kills the kernel.  In particular, any physically typed cyclic
comparison `A=(5,0,0,0,0)` makes `A-5x` a kernel element of anchor value
five and immediately yields the generator (`c094bbb`).  Thus the clean
branch still needs only one new construction, the physical cyclic
`Omega <-> r` comparison; `U` is its dichotomic consequence, not another
cell to construct separately.

The first one-face construction identifies that same attachment.  The
formal third-cofactor tail combined with the normalized target/cap lift has
the desired coarse generator signature, but physical descent leaves a
scalar unit, the ridge `Omega_v`, and the explicit matching companion
`q_(v,N)`.  Adjacent C5 transfer merely moves the ridge; the full endpoint
bar cancels it only while retaining that companion (`66af3a5`).  Thus the
rootless construction and Theorem A's private S-pair stop at the same source
datum: a same-word endpoint/companion attachment.

The rank consequence is exact.  Any nonzero offdiagonal carrier gives two
transposed private-site fans with distinct centre heads.  An off-anchor fan
is already four-good; if both are anchor-contained, the packet lies in the
injective/no-complementary-wedge five-lock Hall residual.  Same-cell
companions cannot change endpoint heads (`44dbdfd`).  Thus the same chain-
level endpoint-word-change homotopy resolves the endpoint provenance needed
on both sides.  It does **not** itself supply the missing transverse head
(`2593831`); rank restoration remains a separate landing theorem.

The marked five-lock module now sharpens this statement.  Equal literal
tails give the endpoint difference by an alternating relative-path sum;
unequal tails give the same residual holonomy detected on the rootless side
(`727de71`).  The physical mixed bar--curvature construction supplies the
correct oriented endpoint shadow but leaves the pure/mixed tail residue
(`43b6038`), while reciprocal Bianchi is parity-even (`65518ac`).  Hence the
rootless comparison target is the same residual-q Kodaira--Spencer relative
cell, followed by the already proved correction-indeterminacy-or-generator
and Fredholm alternatives.  The cell must carry the complete private
boundary, eta, and sigma data above; the five-row cap factorization is not a
physical substitute and a primitive chart difference is presentation-only
(`e6deb15`, `4291ccc`, `45ed42d`).

The closest audited physical candidate is `r_0-T`.  It has the correct
`W`, anchor, target, and residue, but retains one pure-Eq conormal and lacks
the primitive ridge vertex.  The ridge aggregate and `Eq+ainc` are primitive
dual separators, so no existing first repeated-site cap/PP/normal column
repairs it (`729eb41`).

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

1. Promote the constructed order-four/five/six covariance--curvature source
   homotopy to the physical relative fiber product in word `1211222` and
   the labelled repeated `P3 disjoint-union K2` grade.  Only the terminal
   gluing remains: attach the `t-u_v` eta primitive and `-q_pq:22` sigma
   face without changing the proved source image and exact `-delta` shadow.
   If this is
   impossible, compute the obstruction in the exhaustive physical relative
   map; old chart differences and standard `R=D` transport are exhausted.
2. Apply `2593831` to remove endpoint holonomy, then globalize this attachment
   into the source connectivity/exhaustivity-or-separator theorem in the
   `h=3` two-component and arbitrary-core-port packets.
3. Prove the literal-exchange dichotomy from `0a965e7` and `70eb104`:
   same-row dependence gives support descent; otherwise attach through a
   target-full internal site and force visibility in the one remaining
   deficient endpoint quotient.  Combine it with Hall landing and a strict
   component/endpoint potential.  This finishes Theorem A.
4. Split the rootless comparison at the normalized cycle.  If `R_v-R_w` is
   nonzero, prove response-hole accessibility and apply the established
   unit/deletion/Fitting/Hall tail trichotomy.  If `R_v=0`, promote the
   `M_v` comparison into `Omega_v -> r_v`, identify derived `Yw` with
   physical `W`, and use its already prescribed stabilizer variation.  Do not
   search further for a unary-only, positive aggregate-Tor, or old
   `(Omega,Q,r)` covector, quotient-cap, or primitive chart-copy construction;
   all are now excluded on this slice.
5. Extend that comparison over the dense and normal-rank-five face-zero
   strata, carrying the complete normal Hasse face and identifying derived
   `Yw` with physical `W`.  The explicit order-two and order-three derived
   companions on every singular stratum are already assembled; carry them
   through that one physical comparison.
6. Apply the indeterminacy-or-generator and Fredholm alternatives, then
   complete the common horizontal/inactive routing.

Every new finite audit must name which one of these proof steps it proves,
routes, or falsifies.
