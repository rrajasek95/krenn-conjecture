# Careful global proof sketch

Audit date: 2026-08-11.

This is a conditional proof skeleton.  Every arrow is labelled `PROVED`,
`FORMAL AFTER INPUT`, or `OPEN`.  The point is to show exactly how the local
matching-base work would imply Krenn's conjecture without silently assuming a
support-skeleton extraction theorem.

## 1. Extremal statement and tensor model

After aggregating parallel sources with the same physical edge and ordered
endpoint colours, write their total cell as `A_uv(i,j)`.  The perfect-matching
sum is the tensor

\[
 H_B(A)=\sum_M\prod_{uv\in M}A_{uv}
       \in (\mathbb C^D)^{\otimes B}.                      \tag{1}
\]

Monochromaticity is exactly

\[
                       H_B(A)=\Delta_{B,D}
                         :=\sum_{i=1}^{D}e_i^{\otimes B}.  \tag{2}
\]

Endpoint order, offdiagonal colours, and complex cancellation are retained in
(1).  Projecting a palette of size at least three onto any three colours gives
the ternary equation

\[
                         H_B(A)=\Delta_{B,3}.              \tag{3}
\]

Thus the upper bound for even `n>=6` follows once (3) is impossible.  The
support-only lower bounds are the parallel edges at `n=2`, a one-factorization
of `K4`, and the two alternating matchings of `C_n`.

Status: the reformulation, palette projection, lower bounds, `n=4` upper
bound, and terminal six-site ternary obstruction are `PROVED` in the proof
spine.

## 2. Outer induction: clean-pair descent

Assume a ternary solution of minimum even order `n>=8`.  Within that order,
choose a maximum-anchor and then minimum-support representative.  The proved
curvature-line and anchor-synchronization theorems select a physical pair
`p,q` and a projective cap line on which the deletion is generically active.
Let

\[
                         {\cal E}_{p,q}                    \tag{4}
\]

be the clean error restricted to that line.

If (4) has an **active zero**, exact clean-pair descent constructs

\[
                  H_{B\setminus\{p,q\}}(A')
                       =\Delta_{B\setminus\{p,q\},3}.     \tag{5}
\]

This contradicts minimum order, with the six-site theorem as the terminal
case.  Therefore the one remaining conjecture-level statement is:

> **Clean-point theorem (`OPEN`).**  Every synchronized ternary packet of
> even order at least eight has an active zero of its selected clean error.

Everything below is an attack on this one theorem.  There is one exhaustive
dual route, from the rootless/all-inactive split, and a potentially shorter
constructive route through the synchronized one-bad/affine packet.  The latter
becomes a complete alternative only after a uniform source-entry theorem;
that entry is not currently proved.

## 3. Constructive subroute: interference straightening (Theorem A)

The exact scope starts **after** a synchronized maximum-anchor,
minimum-support one-bad packet has been obtained.  A general synchronized
source is not yet known to reselect into this normal form.  Accordingly,
Theorem A can presently close that packet and inform the global mechanism,
but it does not by itself cover the entire clean-point theorem.  A uniform
entry theorem would promote the following subroute to an independent global
proof.

### 3.1 Literal presentation

At fixed order, preserve the complete tensor (3).  Generate the presentation
by literal occurrences

```text
(coefficient word, endpoint ports, physical perfect matching, decorated tail).
```

Two occurrences have a certified exchange edge only when a physical `C4`
switch retains the same decorated complementary tail and supplies the
opposite determinant orientation.  A coefficient equation is an attaching
relation, not automatically an exchange edge or a filled higher cell.

This distinction is load-bearing: physical matching adjacency alone loses
the source typing needed for a finite support move.

### 3.2 Local trichotomy

For one endpoint star, fix the opposite star and its common `q` tail.  The
complete response-column map has the following linear alternatives:

1. an affine fibre meets a physical coordinate target line;
2. two complete columns are proportional;
3. a quotient `2x2`/Fitting minor is nonzero.

Alternative 1 supplies the desired concentrated endpoint coordinate.
Alternative 2 gives an exact one-sided kernel move and contradicts
minimum support.  Alternative 3 is not yet geometric: a source-labelled
pure/mixed companion with the same tail must turn the minor into a literal
determinant/cofactor carrier.

Status: the linear trichotomy and proportional-column move are `PROVED`.
The same-tail promotion is `PROVED` on typed `C4` packets and important fixed
port/private-row charts, but is `OPEN` uniformly.

### 3.3 First-separator reduction

Choose an occurrence outside the joined typed component at minimum flip
distance

\[
 \delta(M,N)=\sum_{C\subset M\triangle N}(|C|/2-1).       \tag{6}
\]

Whole-component switching proves that a minimum separator is a single even
alternating cycle.  A supported typed distance-three chord shortens it.  Thus
the first genuine defects are:

```text
delta=1: a physical C4 lacking its source-labelled opposite orientation;
delta=2: a chordless C6 whose first transgression has unmatched endpoint words.
```

Flat nonempty cycle geometry is already solved by vertex-gauge transport; a
connected, typed, source-exhaustive star is proportional and reducible.  The
missing issue is source connectivity/exhaustivity, not cycle geometry.

### 3.4 Earliest open incidence theorem

In the canonical `C6`, the first residual word is invisible to every selected
response port.  Unary exactness forces six anchor-contained cancellation
matchings, but their `q` tails alone are not Hall holes and do not define
endpoint columns.  The required statement is:

> **Spoke-to-hole synchronization (`OPEN`).**  Unary top plus all complete
> response rows either synchronize endpoint line sites into an ordered
> response hole with the required colours and a nonzero common cofactor, or
> produce a target-line joint-kernel move, a source unit, or a free carrier.

After such a column exists, **endpoint-word completeness modulo Hall** must
give a same-tail opposite orientation, an outside carrier, or a literal
star/triangle/`K2,2` Hall/Fitting attachment.  Separate translated-face line
sites do not prove this pairing.

There is now one exact base case.  In the minimal rational silent-`C6`
packet, after the bright pure tails are added, arbitrary endpoint mass on
all four core ports is impossible: a complete diagonal target coefficient
`aP-1` and a complete mixed zero coefficient `bP` share the same bilinear
endpoint polynomial.  Their source-row combination is a unit in all nine
bright charts.  Hence this first `C6` obstruction cannot survive by
core-port reselection alone.  A surviving packet must add internal
decorated `q` tails which contaminate the paired rows, or leave the core
envelope and enter an already named outside route.

There is also a complementary dense result at the earlier invisible word.
When all eight canonical `z=012111` matching monomials are nonzero, three
shifted response binomials plus the unary row have an odd-holonomy
certificate equal to twice a localized unit.  Thus the dense packet must
produce an external offdiagonal `q` mate or an actual extra endpoint-hole
column.  The remaining spoke-to-hole theorem is confined to support
degenerations; after a column is produced, its rank/support landing is still
the separate open step.

The support-degenerate word is now classified more precisely.  If the
optional `E13` pair survives, its common `q13:11` cell occurs in a literal
shifted response coefficient and supplies the typed chord.  If only `E14`
survives, its common `q14:11` cell is response-silent until the corresponding
physical hole-`14` endpoint product is nonzero.  This is the smallest exact
spoke-to-hole attachment gate; it replaces a vague search over all six
competitors.

Even that minimal `E14` enlargement is not a full survivor.  Across all nine
bright completions, its new term enters one target and one zero coefficient
with the same complete endpoint polynomial, so their combination is a source
unit.  A surviving support degeneration must therefore add a second
asymmetric internal tail (or leave through an outside endpoint).  The next
finite A-test is now a two-tail source-exhaustivity problem, not the bare
spoke-to-hole product.

The entire first one-cell two-tail layer is now exhausted as well.  Across
the `1,020` possible chart/cell extensions, complete response rows first
reduce the apparent defects, and complete unary rows then make every one of
them an ordinary source unit.  Thus no first extra internal cell—diagonal or
offdiagonal—survives as a new `C6` topology.  The earliest local survivor
must contain at least two simultaneously new internal cells which
cross-contaminate the paired unary/response collisions, or an outside-core
endpoint component.  This does not settle arbitrary multisite components,
active-rank landing, or termination.

The complete two-cell layer is empty too.  All `57,291` unordered pairs of
new internal cells retain a literal two-row unit: `51,615` in the base
`G11` comparison, `2,850` in an alternate `G11` word, `2,818` in the unary
row, and the final eight `K4,2` records in `G22`.  Therefore the earliest
same-chart local survivor requires at least three simultaneous new internal
cells.  This is strong evidence for a module-level exhaustivity theorem, but
does not replace global multisite connectivity or rank/termination.

The three-cell top degree is now empty too.  All `2,126,208` simultaneous
three-new-internal-cell specializations are literal source units
(`c13911e`).  Because the physical equations are multiaffine cubic, this
exhausts the local monomial types.  It does not by itself prove the
arbitrary-support statement: the witnessing zero row varies with the
triple, and the universal target has `24/26` private degree-one/two
monomials.  What remains is a triangular/Rees or standard-basis gluing
lemma, not a four-cell census.

The first gluing syzygy is explicit.  Response-row leading terms form
endpoint-orientation two-cycles in every chart.  Unary rows break all `228`
cycles, but the honest multiplied S-pairs introduce nonprivate tails of
degree three (`24` cases) or four (`204` cases); `G22` lies in a different
endpoint grade (`6e5878e`).  The next finite proof object is precisely the
reduction of these unary-times-q Buchberger tails.

The complete first reduction shows that these tails form nine word orbits
and return only to themselves through the missing chords
`q04:00,q13:00`.  A singular return activates a chord and exits through the
crossed-`C4` theorem; on the chordless locus the private endpoint-orientation
class remains for both zero and unit specializations (`2c981a6`).  The
missing row is exactly a same-word endpoint/companion attachment.

This attachment has a minimal algebraic form.  The rootless residual
companion is literally the decorated `2K2` core of one E14 S-pair under a
site/colour relabeling, although their full source grades differ
(`2957235`).  With coordinates `(E_+,E_-,Omega,qcomp)`, one new chain
`A=(1,-1,1,-1)` combines with the existing bar and signless endpoint sum to
split the two orientations (determinant `-2`, `744cd9a`).  Its degree-zero
shadow is the missing A-side word change; its degree-one boundary is the
B-side `Omega/qcomp` cancellation.

The construction problem for `A` is now much sharper.  On an equal literal
common tail, the complete five-lock rows form an even relative incidence
path, and their alternating sum already gives `E_+-E_-`.  A single unequal
tail is the exact endpoint-holonomy obstruction (`727de71`).  The physical
mixed bar--curvature chain nearly fills it: in the exact rootless word it has
zero target and the correct oriented endpoint boundary, but subtracting the
aligned rootless bar leaves the primitive residue

```text
(E_+-E_-)*(a24:11*a35:11-a24:21*a35:12).
```

Reciprocal Hasse--Bianchi cannot repair this defect: it is endpoint-even in
every canonical projection, and common multiplication preserves that parity
(`43b6038`, `65518ac`).  Standard bar, first-PP, Hasse--Bianchi, and matching-
square transport is even more rigid: in the endpoint-odd two-tail square its
main boundary and residue obey the graph law `R=D`, whereas the desired class
has `D=0` and residue `-delta` (`c66e393`).

The leading local theorem is therefore one **source-provenant residual-q
Kodaira--Spencer relative cell** in word `1211222` and the labelled repeated
`P3+K2` grade.  Its complete signature must simultaneously

```text
cancel the literal private full-nine boundary,
carry ordinary residue -delta and D=W=target=ainc=0,
have dr_v(eta_z)=1+delta_vz*u_z/t,
and have sigma response -q_pq:22.
```

These projections are formally compatible and one relative cell suffices,
but ordinary multiplication by the eta primitive `t-u_v` is inhomogeneous
and gives only a tautology after homogenization (`c6f39eb`).  A tempting cap
identity `K=-r0+T+rho-C` is exact only in a five-row quotient: restoring one
of `r0`'s literal private matching pivots separates `K`, so the quotient
cannot be reversed into a source chain (`e6deb15`).  Doubling the complete
full-nine chart gives `576` columns of rank `288`, but its `288`-dimensional
kernel consists exactly of pairwise `pq-pr` presentation differences.  They
cancel the whole physical column and every chart-neutral physical terminal;
the chart-odd Hasse value is presentation homology, not the missing residue
or stabilizer packet (`4291ccc`, `45ed42d`).

The literal mapping-cone target is now pinned without quotient ambiguity.
For `alpha=-delta`, one new aggregate cell `M_v` must land on the positive
sum of the four selected complete matching boundaries, carry the four Eq
coefficients `alpha`, have zero `D/W/target/ores/ainc`, and carry the eta and
sigma terminal values above.  Composing it with the existing cap aggregate
then cancels all `360` literal matching terms and leaves exactly residue
`-delta`.  This is a single image-membership question in the physical
relative Spencer/mapping-cone complex—not a search through the old chart
kernel.

The principal symbol of `M_v` is now constructed and factors cleanly.  The
two-site covariance `delta_2(1->2) delta_5(1->2)` carries the complete pure
tail row to the mixed tail row term by term.  Taking its commutator with the
endpoint-odd curvature, with coefficients `alpha=(-1,1,1,-1)`, kills the
fourth-Hasse scalar top and the entire codimension-one face on every source
word.  The first surviving face is precisely

```text
(E_- - E_+)*(T_0-T_1) = -delta.
```

This is an exact literal reduction (`52d5baa`), but covariance supplies
horizontal equality rather than its nullhomotopy.  The remaining local
statement is therefore the existence of one *mixed covariance--curvature
Spencer homotopy* whose lower image is the pinned `B_j`/Eq/eta/sigma packet.
It is narrower than an arbitrary 360-term membership search, while still
being genuinely new physical source data because the old image remains
graph-locked by `R=D`.

The generator-level lower faces are now constructed.  The complete
linear-coefficient order-five system has 1,080 literal coordinates and
exact rank 706; a deterministic 248-term rational correction makes the
signed operator annihilate `A_0^2`, `A_0A_1`, and `A_1^2` exactly, with no
source-ideal quotient remainder (`6bed6ae`).  Its 111 pure-shift and 137
mixed-shift terms have no other fine-grade component (`591187c`).  Thus the
private matching boundaries and Hasse lower faces are no longer the open
part of the first theorem.

The repair is naturally invisible to both terminal families: it uses no
colour-zero cell and no marked `p/x` colour-2 cell.  The local frontier is
therefore the relative fiber-product gluing of this constructed source
homotopy to the already-known `t-u_v` eta primitive and `-q_pq:22` sigma
correction in the physical repeated grade.  This is a comparison/typing
problem, not another source-row or support calculation.

There is now an exhaustive guard against solving that typing problem by a
larger linear-coefficient order-five ansatz (`3152336`, `636f9f7`,
`463b0b9`).  Of all ambient
decorated coefficient cells, only `36:11` newly enters the two permitted
fine shifts.  It creates a large source kernel and a two-term cycle detected
by the scalar residual, but the full `-delta` shadow is outside the
source-plus-shadow image by the exact rank jump `135 -> 136`.  A sparse
rational left separator certifies the jump inside this bounded block; more
sharply, the shadow projection never reaches the single face
`07:11 wedge 24:11`.  Since
that separator is not typed on the complete physical relative complex, it
is not the terminal Fredholm dual; it is the certificate that the next
construction must be a shifted relative/Spencer cell rather than another
linear/order-five correction.  A higher coefficient/order tower is not
excluded, but it must enter through this same missing relative face.

The first quadratic/order-six layer does exactly that (`1e923cc`).  The
8,580 correctly graded operators containing `07:11 wedge 24:11` have
source-plus-shadow rank 783, and adjoining `-delta` does not raise it.  Exact
elimination gives a 188-term chain with zero literal pair-generator boundary
and exactly the sixteen required shadow coordinates.  All terms contain the
two missing-face derivatives, so the chain is
`d_07:11 d_24:11` times a quadratic-coefficient order-four operator.  Its
natural eta/sigma character is still zero.  Thus the local algebraic source
and residue problem is solved; the remaining issue is physical relative
typing and terminal gluing, not another lower-face search.

The complete unsigned Hasse tower of this same chain is also coherent
(`9bd3533`).  Its empty and singleton layers vanish, its pair layer is
`-delta`, and all higher layers obey
`down(L_(k+1))=(6-k)L_k`.  In particular the 401 nonzero triple faces are
forced by `down(L_3)=4L_2`; they are not independent errors to cancel.  What
remains is physical repeated-grade typing and the alternating Spencer
realization of this already coherent tower.

At the augmented-row level the terminal gluing is now isolated (`cc2d607`).
After the typed order-six chain is subtracted, the remaining class has zero
source/residue/protected rows and only the eta law plus the `-q_pq:22` sigma
face.  Since the entire ordinary order-six block is terminal-dark, this is a
pure shifted-relative comparison problem.  It no longer has to cancel the
literal private full-nine boundary or create `-delta`; those jobs are carried
by the explicit order-six chain.

The terminal-only packet is itself canonical (`202d79e`): it is the
relative first-principal-parts class `-dOmega_v`.  Its eta contraction is
`1+delta_(vz)u_z/t` and its sigma contraction is `-q_pq:22`, while its
ordinary boundary and protected readouts vanish.  Ordinary polynomial
homogenization gives the determinant `t*b-u*a` and changes these terminal
laws.  The exact missing object is therefore a labelled shifted Kähler
lift of `-dOmega_v`, not an unknown terminal character.

There is no further mixed coefficient-ring obstruction between these two
pieces (`10ab27f`).  Every coefficient and derivative cell in all 8,580
eligible order-six operators is disjoint from all four coordinates of each
terminal ridge, simultaneously for all five faces.  Hence
`[Theta_6,-dOmega_v]=0` in the polynomial/Kähler bicomplex.  Only the
physical chart-nondiagonal grade comparison remains.

The primitive order-six face also has the exact one-sided landing topology
(`07:11 wedge 24:11`).  Once physically typed with site `0` target-full and
colour `1` visible in the deficient endpoint quotient, it upgrades the
overlap profile `(2,3)` to `(3,3)`.  Thus the comparison construction and
the first transverse-rank repair are no longer independent proof targets;
their remaining hypotheses are the same label/totalization gate.

If this cell exists, the conditional landing theorem closes the E14
orientation loop and the **unequal-tail** five-lock holonomy and strictly
decreases the number of unresolved typed components (`2593831`).  It does
not create a transverse head or four-good ranks.  If it does not exist, only
an exhaustive *physically typed augmented map* can promote failure to a
terminal separator; nonunique lifts with nonzero terminal difference give
the relative generator.  The bounded parity/Segre covectors alone are not
global dual certificates (`0e4d7f8`, `c2eaa4d`).

### 3.5 Landing and termination

A typed carrier may still have deleted-star ranks `(2,2,3,3)`.  Any
dependence among the occupied complete columns of one fixed endpoint row
gives an explicit anchor-safe support deletion (`0a965e7`).  At minimum
support those columns are therefore independent.  Full-nine incidence then
supplies at least two internal target-full sites, and an overlap at either
one repairs that side to rank three (`70eb104`).  The residual problem is
one-sided: make the carrier visible in the deficient quotient at the other
endpoint.  Endpoint orientation rank two does not imply even this; the
kernel-free target-coloop counterguard remains quotient-dark.

The second uniform theorem must consequently turn a literal common-`q`
exchange into either (i) a same-row dependence touching the carrier, hence
support descent, or (ii) a target-full overlap and a column visible in the
remaining one-dimensional deficient quotient, hence restoration of all four
ranks.  Hall landing starts only after this dichotomy; it is not a substitute
for quotient visibility.

The inner iteration needs a well-founded potential.  Current evidence points
to a lexicographic refinement of

```text
(unresolved affine fibres,
 endpoint support,
 typed components,
 minimum flip distance,
 source-typing debt,
 unresolved Hall/Fitting rank,
 deleted-star rank deficit).
```

Coordinate-line hits, kernel contractions, typed joins, and chord shortening
have proved local decreases.  A global decrease for Hall returns and rank
repairs is `OPEN`; it must not be inferred from finite chart closure.

If source entry, synchronization, landing, and this decrease theorem hold,
the inner iteration yields an active clean point and the outer descent (5)
finishes the proof.  Without source entry, the result closes the one-bad
subbranch but must still be consumed inside the exhaustive B/C architecture.

## 4. Exhaustive dual route: no active clean point (Theorems B/C)

Instead suppose the selected line has no active clean zero.  The exact
two-chart gcd split is:

1. the clean-error coordinates are rootless on a chart; or
2. roots exist, but every root is inactive.

There is no third case.

### 4.1 Rootless chart (Theorem B)

Rootlessness makes the residual Macaulay map surjective.  An abstract
functional is insufficient; it must have literal source provenance.  The
physical non-Euler jets, marked Hessian `h_v`, presentation syzygy `k_v`, and
derived filler

```text
d b_v = k_v,
d n_v = h_v Yw,
(tgt,ores)(n_v)=0,
chart(n_v)=-S_v
```

are `PROVED` in the indexed presentation.

The missing comparison must physically lift the adjacent repeated-site
pentagon differences and identify

```text
derived Yw -> physical W,
```

while preserving boundary, target, ordinary residue, and fine grade.  Once
this physical typing exists, correction indeterminacy is a useful dichotomy:

- a kernel class detected by anchor incidence normalizes to the required
  relative generator;
- otherwise the five polar columns are well defined in the physical cokernel,
  and the proved Fredholm alternative gives the terminal annihilator or the
  same relative-generator output.

The physically typed comparison is `OPEN`; the derived inputs and the linear
generator-or-annihilator alternative are `PROVED`.

The comparison must genuinely change source type.  Rootless pentagon
syzygies first occur in repeated-site degree `P3 disjoint-union K2`, while
the constructed chart and normal Hasse fillers are site-squarefree.  A
single-face collision has a private ordinary residue; only an adjacent
two-face S-pair cancels it, and that pair has physical anchor incidence zero.
Thus the first new cells are zero-anchor collision edges with the known
degree-five compatibility.  Chart `-S_v` is not physical anchor incidence;
the separate primitive anchor combination or dual annihilator is supplied
only after the physical polar map exists and Fredholm is applied.

The collision edge itself is now nearly explicit: the denominator/PP S-pair
has the correct repeated-site ridge boundary, but physical descent contributes
`delta_v*(H_0-u)*e_Eq`.  The exact first new source datum is a zero-anchor
reduced Eq face cancelling that term.  Its five cyclic defects already obey
the required degree-five compatibility.

This source type is sufficient at every normal order needed below.  A single
polynomial collision/reduced-Eq family prolongs functorially through orders
one, two, and three without new multidegrees or readout defects.  Its cyclic
edge matrix still has rank four in each grade, so one separate polynomial
primitive-anchor family is necessary and sufficient to fill the aggregate
cokernel.  The remaining `Yw -> W` identification is independent.  Thus the
full B/C comparison needs exactly these two physical generator families plus
the terminal readout map, not a new family for each singular normal stratum.

On the selected nonzero `C5` torus there is a further simplification.  A
target-preserving degree-two etale site-colour gauge normalizes all five
cycle cells to one, fixes the marked colour-zero cells and non-Euler jets,
preserves every augmented readout, and descends under its deck involution.
It kills the five selected pure-Eq defects.  Hence the exact `C5`
specialization already has clean physical collision edges.  On the general
selected-cycle chart the only remaining edge boundary is the off-cycle tail
difference `R_v-R_w`.  These tails are not yet Theorem A objects: no common
endpoint-star column or identical decorated complement tail has been
supplied.  A source-labelled tail-to-endpoint attachment theorem is required
before the A connectivity mechanism can replace the B comparison.

The tail attachment itself is now exact once a forced response hole is
active.  With off-cycle chords `A,...,E`, the five residuals are

```text
R1=CE+D, R2=A+BE, R3=BD+C, R4=E+AD, R5=AC+B.
```

All ten monomials are distinct.  The complete six-term response coefficient
of any active forced hole routes exhaustively to a source unit, a same-tail
proportional deletion/Fitting carrier, or a different-tail `C4` off-anchor
or Hall/lock case.  The sharp preceding obstruction is that internal `C5`
data do not force the endpoint product at that hole to be nonzero.  Thus #2
has reduced to the same response-hole accessibility/affine line-hitting
lemma as Theorem A; rank landing remains downstream.

The alleged response-dark subcase is now gone.  A nonzero `R_v-R_w`
contains an off-cycle chord whose complete physical column is zero and
minimum-support deletable, or nonzero and source-forces a unary/response
carrier (`d5b8ebc`).  Hence the general residual-tail branch has already
reached the common affine/Fitting/Hall rank-landing gate.

On the exact normalized `R_v=0` specialization, path #1 is sharper than a
missing-column formulation suggests.  The clean collision lattice is
saturated rank four, so one physical augmented base column carrying derived
`Yw` to physical `W` would propagate to the other four faces and make
Fredholm available.  But the marked unary row cannot construct it: after
the direct-zero normalization its mates remain in five reset-word
components (`467d545`, `f3e4b01`).  Nor can a positive aggregate Tor class
construct it.  The literal clean denominator identity forces every such
image to have coordinate sum zero (`ba52560`).

Consequently the clean branch is now a dual problem.  Cyclic gluing reduces
the first endpoint/Bianchi cokernel from five face classes to one primitive
aggregate class.  An explicit candidate separator reads one on the endpoint
ridge, q-companion, and rootless ridge classes and zero on Eq, W, target,
residue, and anchor incidence (`a4c687c`).  The full physical-kernel audit
shows that this coarse covector does not descend: five target stabilizers
pair with it as `-5-u_z/t`, and they kill the entire nonzero covector space
on the old endpoint/companion/rootless inventory (`586f885`, `d7ff17d`).
The formally unique scalar correction on those five directions is itself
detected by two other physical stabilizers and is not source-typed
(`a9f64aa`).

The remaining theorem must therefore construct genuinely new physical
comparison data in repeated-site `P3 disjoint-union K2` degree: a
source-valid `Omega_v <-> r_v` map whose stabilizer variation supplies
`5+u_z/t`, together with derived `Yw -> W` and the reduced-Eq correction.
If its indeterminacy has nonzero anchor readout, `0373033` turns that failure
directly into the required relative generator; otherwise the comparison
defines the polar map and Fredholm finishes the rank alternative.

The smallest source type is now explicit.  It is a same-labelled-companion
lift `(-r_v,+Q_(v,N);ores=1)` in repeated `P3 disjoint-union K2` degree;
subtracting the endpoint bar gives exactly `-t_v Omega_v+r_v`.  No existing
source family contains it (`947ce8e`, `3e64181`).  Cyclic homogenization
first occurs in degree `abcde`, but its aggregate has lower boundary
`5abcde`, so ordinary matching, Pluecker, and incidence cells cannot fill
it.  The positive object is a relative augmentation `U` with
`d_0U=abcde`, after which the corrected package `A-5U` is a cycle
(`252bdc8`).  This is a single named cell, not an indefinite higher-order
search.

Nor is `U` hidden in the existing top degree: `abcde` occurs only as a pure
unary multiplier with anchor `-1` and target `+1`.  A primitive augmented
functional separates it from the target/anchor-zero `U`, and the complete
top source map is injective (`6c76d22`).

This does not add a third independent theorem.  The old target/cap rows
already form `x=(1,-1,0,0,0)`.  If anchor incidence is nonzero on the
kernel preserving lower boundary, W, target, and residue, that kernel
element is the primitive relative generator.  If a physical cyclic
comparison `A=(5,0,0,0,0)` is built, then `A-5x` is exactly such an element
(`c094bbb`).  Hence the construction-or-generator dichotomy absorbs `U`;
the single real construction remains `A`, equivalently the physical
`Omega <-> r` comparison.

The formal third-cofactor cell confirms the source type.  After the
target-normalized correction it has the perfect coarse relative-generator
signature, but it leaves one scalar unit, one `Omega_v` ridge, and the
literal companion `q_(v,N)`; a C5 edge transfers rather than kills the
defect, while the full bar retains the same companion (`66af3a5`).  Hence
the combinatorial and rootless attacks meet at one same-word
endpoint/companion attachment theorem.

The same operation is exactly what rank landing asks for.  Every
offdiagonal carrier produces transposed private-site fans with distinct
centre heads.  Off-anchor fans are already four-good; two anchor-contained
fans are precisely the injective/no-wedge five-lock Hall residual, and an
ordinary same-cell row cannot change the heads (`44dbdfd`).

The universal typed quotient confirms that no polynomial bookkeeping can
skip the accessibility step.  Before localization, the five cyclic tail
differences span a four-dimensional quotient: every complete unary or
response occurrence has positive endpoint-use grade and projects to zero in
the bare-tail summand.  The exact missing inventory is ten unary spokes and
forty response brackets (eighty orientations).  On path #1, the nearest
existing base column `r_0-T` already has the correct `W`, anchor, target, and
residue but is separated from the desired column by two primitive defects:
one reduced pure-Eq face and one ridge vertex.  No audited cap/PP/normal
column supplies them.  Hence the remaining physical theorem must construct
these attachments on the residual-tail branch, while the exact clean branch
must promote its forced aggregate separator rather than merely combine
existing coarse rows.

### 4.2 All roots inactive (Theorem C)

The face-open derived candidate is `(kappa/h_v)n_v`.  On the dense
cyclotomic stratum of the simultaneous face-zero locus, the normal/Rees lift
is all-order after adding the complete normal Hasse face.  These are derived
chart statements, not physical cap columns.

The comparison from Theorem B must extend to this normal face and identify
the candidate with the physical inactive cap coordinate.  The nondense
face-zero locus is now finite: regular isolated-vertex `C4`, `K4-e`, and
generic `K4` inherit the derived normal repair.  Every singular first-order
stratum also has a literal weighted-normal escape by order at most three:
the cyclotomic rank-four `K4` missing covector is hit at order two, while the
intersecting supports have explicit degree profiles using only orders two
and three beyond their first-normal span.  Hence there is no remaining
set-theoretic singular-support separator.  What remains is chain-level:
the complete derived second-normal companions (and the third-normal
triangular companions for the one-edge/three-star strata) now exist, have
zero target/old residue, and assemble rank-five boundary systems on every
stratum.  Their first failure is exactly the same physical comparison as in
Theorem B: the normal-indexed mixed row has no homogeneous site-squarefree
physical image.  Thus only the site-collision/primitive-anchor cells and the
physical `Yw -> W` comparison remain.  The horizontal
rootless/inactive comparison and diagonal inactive routing remain `OPEN`.
Once a physical cap exists, the Omega/Bezout and certificate-bracket
prolongations are `PROVED`.

If B/C close every rootless/inactive chart pairing, the assumption of no
active clean zero is contradictory.  The outer descent then applies.

## 5. Relation to support-skeleton extraction

It would be sufficient to select one nonzero monochromatic perfect matching
per colour whose union contains no further perfect matching.  That union,
with unit weights, is an unweighted witness with the same palette.  This is
the most transparent extremal interpretation of the conjecture.

The proposed proof does **not** assume that stronger extraction theorem.
Theorem A tries to realize it locally by deleting cancellation complexity,
but it may instead produce an active pair and descend in order.  Theorems B/C
are the dual fallback for cancellation homology that cannot be eliminated.
Thus the actual proof target is weaker and more robust:

```text
support straightening OR order descent OR a terminal contradiction.
```

## 6. Exact remaining load-bearing theorems

The proof closes if either the exhaustive B/C route is completed, or A is
completed together with uniform source entry.  The current load-bearing
theorems are:

1. uniform entry into the synchronized one-bad packet, if A is to be a
   standalone global route;
2. membership of the pinned aggregate mapping-cone cell `M_v` in the
   physical relative Spencer complex, or an exhaustive physical separator;
3. globalization of that attachment to spoke-to-hole synchronization and
   endpoint-word completeness modulo Hall;
4. double-quotient transverse visibility plus a well-founded inner decrease
   theorem;
5. physical terminal typing of that same repeated-grade comparison for
   Theorem B;
6. its compatible extension over inactive face-zero strata and the final
   horizontal/diagonal routing for Theorem C.

The first four complete the constructive route.  The last two complete the
exhaustive dual route.  Some overlap is expected: a terminal Hall/Fitting
class from A may be exactly the physical correction class evaluated by B/C.
Establishing that comparison would reduce the number of independent hard
theorems, but it must be proved rather than imposed as a unification
principle.
