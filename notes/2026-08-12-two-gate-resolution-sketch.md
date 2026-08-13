# Two-gate resolution sketch

Audit date: 2026-08-12.

This note is the shortest route through the **canonical six-site core**
after the exact `15=1+9+5` occurrence split and the active-fan coloop
theorem.  It is a proof programme, not a claim that the two gates below are
already proved.  More importantly, these two gates do not by themselves
cover every synchronized ternary packet: a separate global-coverage theorem
is required in Section 4.

## 1. The canonical core is complete outside two gates

Assume that the global clean-point problem has already entered either a
synchronized one-bad packet or the corresponding rootless/inactive collision
chart, and choose a representative by

```text
maximum protected mutual anchors,
then minimum occupied scalar support.
```

The established circuit-cover and lift trichotomy attach every unwanted
occupied cell to the protected anchors by a primitive frame circuit.  There
are only three source types.

1. A squarefree circuit with a common tail enters one complete matching
   coefficient.
2. Failure of a tail is a Tutte/Hall accessibility barrier.
3. A repeated physical site is a Cartan--Spencer collision face.

At six residual sites the complete occurrence profile splits as

\[
              \mathbb Q[\mathcal M_6]
                =\mathbf1\oplus C_{\rm cut}^{0}\oplus D_{\rm alt},
              \qquad15=1+9+5.
\]

The centered cut sector has the constructive filtered cycle `(v,-v)`.  A
determinant-bright zero mixed row has a nonzero offdiagonal cell, hence a
source-provenant private-site fan.  Complete pure target supports make that
fan four-good unless one edge is a literal pure-colour coloop.  Therefore
this canonical core needs only the following two gates.

## 2. Gate I: one protected physical comparison

For the determinant-dark cut profile, the complete lower Hasse face has

```text
18 direction-labelled terms,
15 physical collision labels,
3 shared labels,
12 nonzero collision coefficients.
```

Their input geometry is now simpler than three independent equations
(`47582d4`).  On the fifteen-label quotient the lower face is

\[
                   (\rho-1)u_{012},\qquad \rho=(1\;4),
\]

with seven two-cycles and one fixed point.  The shared labels are one fixed
point and one two-cycle, so any genuinely `rho`-equivariant comparison
satisfies all three overlap coherences automatically.  The transposition is
not itself physical in the fixed source word: it changes `001122` to
`021102`, and every physical cut transport needs at least two local colour
repairs.  Thus Gate I has reduced from fifteen independent images to one
target-cancelled **two-local-root Cartan--Spencer attachment** and its
equivariant translates.

The output-side cell is now constructed on the normalized `Y=1` slice
(`271df91`).  With `alpha=(-1,+1,+1,-1)` and

\[
 O_\alpha=\sum_j\alpha_j(-r_{0,j}+T_j+\rho_j),
\]

the complete old cap gives the forced 360-term private/Eq image and residue
`-alpha` after negation.  The physical endpoint-odd Cartan/HPL cell `K` has
zero literal source and first-Spencer output, residue `+alpha`, zero
protected rows, and precisely the eta/sigma ridge.  Hence

\[
                         M_v=-O_\alpha+K                \tag{1}
\]

is exactly the formerly missing literal mapping-cone image.  Gate I is no
longer an output-membership problem.

The external unaudited probe in
`computations/unaudited-gate1-phi-probe-2026-08-12/` correctly predicted
this decomposition in a coarse 32-row signature model, but it is not part
of the proof spine: it assumed the Cartan private rows and terminal packet.
The literal theorem `271df91` independently supplies both.  The probe is
therefore evidence that the compression was natural, not evidence for the
remaining input comparison.

Construct the remaining input-side source-valid comparison

\[
             \Phi:U_{15}\longrightarrow L_{h=3},
             \qquad J_3\Phi=A J_{\rm col},             \tag{2}
\]

whose one-face image is (1).  Equality on the three shared labels is exactly
the descent condition from the two cut charts to the physical collision
quotient.  The remaining obstruction is the source-labelled two-local-root
word change (or absorption of its forced complementary-word copy), not
private-boundary, Eq, residue, or terminal construction.

More precisely, put `W=001122`, `W'=021102`, let `rho=(1 4)`, and let `w`
be the signed two-root Weyl operation.  Then `wW=-W'`, `rho W=W'`, and the
target-safe odd prism `K=(1-rho)H_w` has the desired anti-pair in both word
grades.  If `u=u_012`, the Cartan homotopy identity is

\[
        dK+Kd=(1-\rho)(w-1).
\]

The `rho`-transported filtered cube cancels the complementary `W'` copy,
but it does not automatically cancel `K d(u)`.  Nor can `K d(u)` yet be
compared labelwise with (1): the former is defined on the fifteen
six-site `(matching,repeated-edge)` collision labels, whereas the literal
boundary of (1) is a 360-feature decorated eight-site packet.  Identifying
those two ambient modules is already the missing comparison and must not be
assumed in order to prove it.

Thus the sharpest Gate-I statement is a **shifted source-label theorem**:
construct the fine-grade/tail map from the fifteen collision labels to the
literal 360-feature repeated packet, intertwine its `rho`-odd Cartan
residual `K d(u_012)` with the image (1), and preserve all protected rows.
This is smaller and more concrete than an arbitrary map on fifteen labels,
but it is not merely an equality inside an already common vector space.
The residual is `rho`-odd; consequently it cannot be supplied by the
`rho`-even target-bearing adjacent-power cell required in the inactive
branch.

The moving support of this theorem is now constructible.  In the canonical
faces-`(3,5)` repeated component, the unique nontrivial physical involution
acts on the six pure multipliers by `(0 5)(2 3)(1)(4)`.  Exactly four
equivariant one-double-fibre site collapses lift all twelve nonzero lower
labels, and after dividing by two their signed pushforward is precisely one
required 360-feature `alpha` aggregate.  The only obstruction to extending
the map over all `U_15` is the three-label shared packet: every working
collapse identifies source sites `0,2`, while each shared label repeats the
edge `02`, hence maps it to a forbidden loop.  These labels have nonzero
occurrence boundary and cannot simply be killed.  Since they form one
fixed orbit and one rho-pair, Gate I has reduced further to **two equivariant
shared-loop repair images**; the other twelve labels are done.

The shared repairs are now exhausted combinatorially (`f59bbc6`).  Every
single-C4 bypass lands, up to the physical involution, in one paired target
orbit `{B0,B5}` or `{B2,B3}` and one fixed target `B1` or `B4`; there are
four equivariant orbit assignments.  The existing `M_v`, clean-collision,
and projected reduced-Eq families span exactly the augmentation-zero
hyperplane of the six pure multipliers.  A shared-label image has
augmentation one.  Adding an ordinary `r0` unit restores augmentation but
leaves protected `(target,ainc)=(1,-1)`.  Consequently the exact remaining
Gate-I objects are two source-provenant relative C4 cells—one fixed and one
paired representative—with

```text
pure-multiplier augmentation = 1,
protected target = 0,
physical ainc = 0.
```

This is a genuine relative target/anchor-cone requirement, not another
choice of site-collapse map.

Equation (2) does two jobs at once.

* It nullhomotopes the lower collision face of the determinant-dark filtered
  cycle, producing the complete marked kernel.
* It is the protected rootless/inactive comparison needed to define the
  physical polar map.

Exact terminal equality is unnecessary.  The proved quotient alternative
states:

```text
q-Phi defect nonzero on protected kernel -> physical relative generator;
q-Phi defect zero                       -> q transports -> Fredholm.
```

For the constructive Route A, one independent row law remains: the physical
pure/target anchor must see the corrected kernel.  It is enough to prove one
of:

1. `ainc` transports separately modulo the protected rows;
2. fine grading makes `ainc` kill the collision correction; or
3. direct evaluation gives a nonzero anchor value.

Then the rectangular interference theorem gives either a rank-two localized
source unit or a unit-coordinate kernel absorbed by the same physical
terminal alternative.

This separate anchor law is **not** a prerequisite for the rootless
generator/Fredholm dichotomy in Route B.  Once `Phi` is physical on the
complete protected domains, `7efd10d` already resolves either value of the
physical terminal defect.  The inactive extension must still identify the
physical cap/anchor coordinate on its own normal faces, but the rootless
branch should not be delayed by the constructive anchor pairing.

This is the highest-leverage construction because it closes the rootless
comparison immediately, supplies the common input for the inactive
extension, and leaves only the separate anchor law when one also wants the
constructive determinant-dark entry.

## 3. Gate II: trapped-carrier affine accessibility for a fan coloop

Let one edge of a source-provenant active fan be a pure-colour coloop.  The
complete later target-coloop chain, punctured-C4 theorem, and conjugate
double-coloop theorem fully consume a coloop once it has the normalized
common-`q`, endpoint-port, and response-head typing.  The earlier multisite
affine handoff in `0556512` is superseded inside that normalized chain.
Accordingly the live gate is normalization of an arbitrary fan coloop, not a
new branch after normalization.

The source-provenance half of this gate is now proved.  Let `e=uv` be the
pure-`c` coloop edge, with nonzero cell `alpha`, and compare a pure target
row in channel `i` with the row obtained by changing only `u,v` from `i` to
`c`.  Splitting both complete rows according to whether they retain `e`
gives (`32ce01c`)

\[
 d_iC_i+U_i=1,\qquad \alpha C_i+V_i=0,
 \qquad \alpha U_i-d_iV_i=\alpha.                     \tag{2}
\]

Thus a literal pure-target or fine-typed mixed matching omitting `e` always
exists.  Termwise, the pure and mixed carriers retain the same matching
skeleton, common residual `q`, endpoint partners and orientation, response
heads, remote decorated tail, and fine word.  The same pivot works for all
six saturated concepts; no orbit-specific response identity remains to be
found.

What is still missing is the final affine/dependence landing when every
carrier furnished by (2) stays trapped in the saturated shores.  Here the
parity pattern further unifies the gates (`e6b390a`).  The physical complete
row supplies the signless packet

\[
 S=\alpha(U_++U_-)-d(V_++V_-)-\alpha,
\]

while a target-safe odd two-root comparison would supply

\[
 D=\alpha(U_+-U_-)-d(V_+-V_-).
\]

Then `(S+D)/2` and `(S-D)/2` are the two oriented target-bearing affine
rows.  No target-unsafe signless Cartan homotopy is needed.  The remaining
pre-anchor obstruction is exactly agreement of the complete protected odd
Cartan packet with `D`; after agreement, the independent condition is
`h_phys(k)!=0` on the minimum target circuit (or the physically typed dual
of its failure).  Thus Gate II is another instance of the same protected
two-root comparison/anchor schema as Gate I, not a six-case Hall proof.

The packet-disagreement alternative is now exact (`7a3ad78`).  Its class is

\[
 [\mathfrak o]=[(M-M_0\Phi)-(a-a_0\Phi)]
              =[q-q_0\Phi]\quad\text{in }L^*/\operatorname{row}J.
\]

If this class is nonzero, a protected-kernel witness is either the physical
relative generator or a literal saturated typed exit.  If it vanishes, a
row correction makes the odd packet physical and `(S+D)/2`, `(S-D)/2`
perform the oriented affine split.  Hence Gate II no longer needs separate matching-
aggregate and anchor-incidence comparison maps.  The physical circuit row
`h_phys` remains independent and must still see the resulting minimum
target circuit (or produce its own physically typed dual).

Fix `q` and the two opposite endpoint rows and form

\[
             L_s(v)=(vs_1q^{[h-1]},vs_2q^{[h-1]}).
\]

Take all literal source-certified common-tail, Cartan, and response
exchanges at once.  They form a finite directed graph on complete endpoint
columns.  Saturate the component reachable from the coloop fan.

* If the reachable component meets the required target-coordinate lines in
  both sequential affine fibres, perform the joint-kernel concentration.
* If it reaches a free active fan, complete pure supports give four-good or
  another named coloop already inside the same saturated component.
* If neither happens, the reachable set is tight for the two endpoint
  quotient matroids.  The matroid-intersection covector must be lifted
  through the complete source rows.  A proportional lift is the proved
  same-row support deletion; a nonproportional lift is another typed
  exchange, contradicting saturation; the remaining cross-intersecting
  shadows are precisely star, triangle, or `K2,2` Hall relations.

The purely combinatorial termination statement is now exact (`32e07b5`).
The `5,141` cross-intersecting six-site inputs have `446` saturated closed
concepts and only six types modulo site symmetry and shore swap; every new
typed hole strictly enlarges the closure.  Thus there is no iterative Hall
cycle once the physical rows realize the saturation.  The intended output
is immediately one of

```text
target-line concentration,
four-good active pair,
anchor-safe support deletion,
anchor-preserving star/triangle/rectangle relation.
```

The load-bearing missing statement has consequently narrowed to the
**trapped-carrier affine/dependence lift**: the already physical carriers in
(2) must either meet the sequential target fibre, leave the saturated
shore, or make the typed Hall covector act nontrivially on a protected
complete-column circuit, producing anchor-safe dependence.  Word,
common-`q` tail, endpoint orientation/head, fine grade, and remote-tail
provenance are no longer missing.  The target-augmented circuit theorem
(`b6775b0`) then turns an internal placed Cartan direction into a normalized
affine exchange or homogeneous connector, while an external direction gives
a target-dark separator.  Its remaining independent condition is visibility
of the target circuit under the physical anchor row.

## 4. Global coverage: one of two routes must still be completed

The two local gates become a proof of the conjecture only after one of the
following exhaustive coverage routes is proved.

### Route A: uniform constructive entry

Starting from an arbitrary synchronized maximum-anchor/minimum-support
packet, prove that complete source rows either produce an active clean pair
directly or enter the canonical six-site fork above.  This includes the
uniform source-connectivity/endpoint-word theorem for long alternating
components and a well-founded decrease for affine/Hall returns.  Gate II is
the normalized coloop endpoint of this route; it is not a substitute for the
entry theorem.

### Route B: exhaustive rootless/inactive comparison

Use the proved gcd split: every line with no active clean zero is either
rootless on one chart or has roots which are all inactive.  Gate I supplies
the finite protected comparison required by the rootless branch; its
physical terminal-defect alternative does not require the separate
constructive anchor law.  The same comparison must then:

1. extend over every normal face of the inactive zero locus, including the
   complete order-two/order-three Hasse companions;
2. identify derived `Yw` with physical `W` and the normalized chain with the
   physical inactive cap coordinate; and
3. support the final horizontal rootless/inactive comparison and the still
   open diagonal inactive Rees routing.

The derived normal systems are already complete.  What remains is physical
comparison and diagonal routing, not another support-stratum census.
The diagonal label propagation is now also formalized (`981f1b0`): if
`Phi` is source-labelled and Hasse/Rees-linear, tensoring the fifteen-label
quotient with `k[ell]/ell^r` propagates the seed coherences to every jet
order.  The first genuinely new diagonal data are instead:

* one target-bearing adjacent-power cone direction on the asymmetric
  generic route (two on the symmetric route), since the two diagonal jet
  targets have rank two while `M_v` is target-zero;
* vanishing of the actual truncated principal-parts class in
  `(ker epsilon/N_lit) tensor k[ell]/ell^r`; and
* at the trace collision, the order-`h` unary target jet or a proof that a
  complementary residue survives.

On the generic `beta!=0` stratum, the first bullet is now constructible at
the upper-target level.  The combination

\[
 J_*=(\beta-2\alpha)J_1+(\beta+\alpha)J_2
\]

satisfies `T(J_*)=-3 alpha beta Delta`, hence
`hT(J_*)=-9 alpha beta Delta`.  After the physical two-root orbit and
localization at `alpha beta`, this gives exactly the required rho-even
upper target `-2(w-1)Delta`.  The remaining generic obstruction is only the
lower face: the explicit even Cartan remainder
`(1+rho)H_w d(P(J_*))` must equal the desired adjacent response face modulo
the literal Rees boundary module.  The old fourth-Hasse filler still leaves
its `(H_0-u)e_Eq` conormal defect.  The `beta=0` trace collision remains a
separate order-three unary/complementary-survival case.

The lower class is in fact parameter-free (`d84c6a8`).  The complete matrix
identity is

\[
                  J_*=-h\alpha\beta I,
\]

so after the same normalization the entire generic remainder is

\[
              -{1\over h}(1+\rho)H_w\,dP(I).
\]

Its truncated-Rees value is presently ill-typed for exactly the same reason
as the odd Gate-I residual: one still needs a shifted physical label map
`tau_+` from the trace-Cartan principal-parts orbit into the literal
diagonal `N_lit` module.  Target cancellation, order-zero agreement, and
formal Rees-linearity do not determine that membership; a two-map guard has
the same visible data but classes `0` and `[z]`.  Thus the two critical
lanes have converged on a parity pair of source-label theorems:

```text
tau_- : odd collision packet -> literal M_v packet,
tau_+ : even trace PP packet  -> literal diagonal Rees packet.
```

The first is down to two shared-loop orbit repairs.  The second is down to
one parameter-free trace jet.  Neither can substitute for the other.

A same-power target companion cannot replace the adjacent-power cell: it
cancels the ordinary residue together with the target.

Route B is presently the logically shortest global path because it is
already exhaustive and does not require proving uniform entry into the
one-bad normal form.  Route A remains valuable because its accessibility
theorem also supplies the source provenance and rank landing used inside
the comparison.

## 5. Conditional assembly

The two global routes have different minimal hypotheses.

### Route A assembly

Assume Gate I, Gate II, the independent physical-anchor law, and the uniform
constructive-entry theorem.

1. Enter the canonical collision or active-fan packet.
2. Gate I closes the determinant-dark collision packet.
3. The determinant-bright packet gives four-good or a coloop; Gate II closes
   the coloop.
4. Support deletion contradicts minimality; otherwise clean-cap descent
   lowers the even order by two and induction reaches the six-site
   contradiction.

### Route B assembly (shortest current path)

Assume Gate I and the physical inactive comparison, including its root-even
adjacent-power target cell and literal Rees membership.

1. The proved gcd split makes the rootless/all-inactive fork exhaustive.
2. Gate I and the terminal-defect alternative close the rootless side.
3. Hasse/Rees-linearity propagates the same fifteen-label comparison through
   the inactive normal jets; the root-even companion cancels the nonzero
   diagonal target direction.
4. Literal truncated-Rees membership and the physical `Yw -> W`/cap law
   close the diagonal residue.  The horizontal comparison then closes the
   remaining inactive faces.

Gate II and its anchor law are therefore a high-value parallel route, not a
logical prerequisite for Route B.

Accordingly the conjecture is not “a few finite cases” from completion.  Its
canonical core is two structural comparison/landing theorems from
completion: Gate I is one input-side equivariant two-root comparison on a
fifteen-label quotient (its output cell is constructed), and Gate II is the
same odd-comparison/anchor schema applied after a proved uniform complete-row
pivot.  Globally, one
additional coverage theorem remains: uniform constructive entry, or the
inactive extension and diagonal routing of the exhaustive dual route.

The shortest exhaustive dependency map is therefore

```text
arbitrary counterexample
        |
        v
proved clean-line gcd split
        |
        +-- rootless, normalized tail ------> two-root Phi
        |                                      |
        |                                      +-- q defect != 0 -> generator
        |                                      `-- q defect  = 0 -> Fredholm
        |
        +-- rootless, residual tail --------> complete-row tight-set lift
        |                                      -> unit/deletion/four-good/Hall
        |
        `-- all roots inactive -------------> Rees-linear Phi
                                               + adjacent-power target cone
                                               + literal Rees membership
                                               + collision/horizontal routing
                                                       |
                                                       v
                                          inactive contradiction or cap

four-good/cap output -> proved clean-pair descent -> n-2 -> ... -> n=6 contradiction
```

This diagram also records what is not shared.  `Phi` settles rootless
terminal indeterminacy but does not manufacture the diagonal target cone;
Hall saturation settles finite termination but does not supply complete-row
provenance; and the constructive physical-anchor law is unnecessary on the
rootless Fredholm branch but remains necessary if the determinant-dark
filtered kernel is used to create a rank-two active minor.

## 6. Parallel attack

The work can proceed independently.

* **Comparison lane:** construct (1) and its literal mapping-cone image
  first.  Treat the separate anchor law as a constructive-Route-A add-on,
  not as a blocker for rootless Fredholm.
* **Accessibility lane:** prove coloop normalization and the saturated
  source-typed tight-set alternative.
* **Coverage lane:** first try to extend Gate I over all inactive normal
  faces and finish the diagonal Rees route.  In parallel, record exactly what
  would be required for uniform constructive entry, but do not silently use
  it.
* **Adversarial lane:** attempt the smallest complete-source counterguards to
  the gates and their global promotion; projected matrices, bare matching
  supports, or chart-only terminals do not count.

No further extra-cell census or flat-cycle classification should be started
unless it directly tests one of these gates or their global-coverage
promotion.
