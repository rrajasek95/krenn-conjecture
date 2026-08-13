# Interference--Cartan proof map

Audit date: 2026-08-12.

This is the current shortest proof sketch.  It replaces a large collection
of local cycle cases by one complete source-entry fork, one physical
word-changing comparison, and one transverse landing theorem.  It is not
yet a proof of the conjecture.  The six-site occurrence module is now split
exactly into a filtered-lift sector and a determinant sector, so the live
entry problem is narrower than an arbitrary marked lift: descend the lower
collision face and pair it with the physical anchor, or land the evaluated
determinant.  Construction of one protected physical comparison and final
transverse landing are the other two live structure theorems **inside this
canonical packet**.  Globally, one further coverage statement is necessary:
either uniformly enter this packet from every synchronized source, or extend
the same comparison through the exhaustive all-inactive branch, including
its diagonal Rees routing.

## 1. Global contradiction setup and scope

Assume a strict weighted advantage over the support-only construction and
choose a representative which first maximizes the protected pure anchors
and then minimizes occupied support and cancellation complexity.  The
decorated perfect-matching tensor is

\[
                         H(A)=\sum_{i=0}^2e_i^{\otimes n}.       \tag{1}
\]

Choose a nonzero unwanted mixed matching occurrence.  Exactness forces it
into a finite source-labelled cancellation component.  Same-word matching
interference changes phases and tails but never changes the local head at a
site.  Therefore the component has two fundamentally different operations:

```text
matching interference   : same word/head, controls holonomy and potentials;
physical Cartan          : changes the word/head, controls transverse escape.
```

This separation is proved by `abe582b`.

The occurrence analysis below starts once the selected cancellation data
has entered the six-site marked packet.  That entry is not automatic for an
arbitrary synchronized ternary source.  The global proof can justify it in
either of two ways: a uniform constructive entry/termination theorem, or the
proved rootless/all-inactive gcd split followed by a physical comparison on
both branches.  All statements below must be read with that coverage guard.

## 2. The rectangular interference alternative

Let `M:X->Y` be the complete protected source-incidence map in the finite
labelled packet, let `h_phys` be the physical pure/target reduction row, and
let `g` be the whole physical Cartan column.  The essential entry datum is
one kernel circuit

\[
                 Mc=0,\qquad h_{\rm phys}(c)\ne0.      \tag{K}
\]

Then the exact rectangular alternative (`a4e15ab`) is:

* `[g] != 0` in `coker M`: adjoining `g` and `h_phys` raises rank by two,
  giving the bright localized minor/source-unit branch;
* `g in im M`: solve `My=g` and adjust `y` along `c` to match the augmented
  anchor coefficient; `(-y,1)` is a unit-coordinate kernel.

No square block, component projector, left-cokernel mode, corank-one
hypothesis, or zero-holonomy classification is required.

The earlier Schur block is the useful minimal special case: take a minimal
square critical `M` in the component.

* Nontrivial/odd holonomy makes `M` invertible, hence gives a localized
  source unit.
* Zero holonomy gives `rank(M)=r-1` with full-support right and left charges
  `c` and `ell`.

For a pure anchor row `h` and a word-changing connector `g`, the complete
Schur minor is

\[
 \det\begin{pmatrix}M&g\\h^T&\alpha\end{pmatrix}
        =-\kappa(h^Tc)(\ell^Tg).                       \tag{S}
\]

The physical anchor makes `h_phys^Tc!=0`.  Thus only the Cartan charge
matters, and its two branches are exactly the two rectangular cases above.

The connector is now uniform.  The complete perfect-matching tensor is
equivariant under local colour changes, and endpoint oddization kills the
target defect.  For every marked offdiagonal occurrence at even order at
least six, `346d76a` constructs the ambient physical Cartan prism and
`6824c9e` places it with coefficient `-1` in the exact marked fine label.
Consequently

```text
ell^T g != 0  -> Schur unit -> contradiction.
```

No residue or eta/sigma terminal is needed on this bright branch
(`83151bf`).

## 3. Marked-kernel entry and optional component assembly

Minimum support gives a primitive signed circuit through every occupied
optical cell in the unsigned port-incidence map.  It does **not** yet give
(K), because the complete labelled source map retains every matching
completion and contaminating term.  The exact lift gate (`03f6304`) first
uses the auxiliary occurrence-coordinate covector `e_s^*`.  It starts with
the common-tail candidate `x0`, marked value `(x0)_s!=0`, and defect `d=Mx0`:

* a correction `z` with `Mz=-d` and `z_s=0` yields a kernel with nonzero
  marked occurrence coordinate;
* otherwise `e_s^*` lies in `row(M)` and gives a separator reading
  nontrivially on `d`, already a pivot/coloop source-unit exit.

The successful coordinate lift is not yet (K): a mixed matching occurrence
is a domain coordinate, while `h_phys` is the reduced pure/target source
row.  The remaining entry theorem must both lift the marked coordinate and
prove that the resulting kernel pairs nontrivially with the actual physical
anchor row (or dualize its failure).  The no-common-tail and repeated-site
failures continue to route to Tutte/Hall and principal-parts/Cartan-Spencer
exits.

The componentwise theorem is now an optional explicit construction rather
than a necessary hypothesis.

The complete Cartan column generally cannot be projected to a physical
source chain supported on one matching component (`4f2472b`).  This is no
longer needed.  Decompose the **complete protected incidence map** into its
actual connected anchor-critical blocks and analytically project the one
whole physical Cartan column to every block:

\[
                  M=\bigoplus_\Gamma M_\Gamma,
                  \qquad g=(g_\Gamma)_\Gamma .        \tag{3}
\]

Any physical column touching two proposed blocks joins them, so the final
decomposition is genuinely block diagonal.  If some
`ell_Gamma^T g_Gamma` is nonzero, its anchor-critical Schur block is bright
and gives the source unit.

If every component is dark, each has an exact potential

\[
                    M_\Gamma y_\Gamma=g_\Gamma.       \tag{4}
\]

The component potentials now assemble without ever projecting the physical
Cartan chain (`bcc75e1`).  There are two source-level possibilities.

### 3.1 Nonexhaustive inventory

If a nonzero coordinate of the whole Cartan column remains outside the
current saturated blocks, it is a literal typed exit.  Adjoining its
incident relation strictly enlarges the finite labelled inventory.  A
global proof must show that this enlargement either joins another
anchor-critical block, reaches a bright Schur test, or lands in the
active/Hall alternatives below.  It may not silently call an omitted
internal fine label an exit.

### 3.2 Exhaustive inventory

If the blocks exhaust every protected label, their direct sum is the
complete equality `G=Cy`.  Therefore

\[
                              k=(-y,1)                 \tag{5}
\]

is a unit-coefficient kernel class of the complete augmented correction
map.  It need not be a dependence among occupied scalar cells in one
endpoint row; the smallest exact counterguard is type-split (`a60ee53`).

The correct replacement is terminal-safe cancellation (`00db7ee`).  For the
physical terminal `q`:

* `q(k)!=0`: normalize `k`; it is the relative generator;
* `q(k)=0`: quotient the augmented domain by `<k>`.  This preserves the
  image, cokernel, and the terminal image of the remaining kernel;
* if another kernel class is `q`-visible, that class is the generator;
* only when `q` kills the entire protected kernel does
  `q=lambda J_0` give the physical Fredholm separator (`941f4b6`).

Thus a dark Cartan direction never creates a third terminal outcome.  The
load-bearing hypothesis is that `q` is the physical anchor/ridge readout on
the exhaustive protected complex, not a component charge or chart tag.

## 4. What symmetry cannot do

Three tempting shortcuts are now exactly excluded.

1. A target-touching occurrence rectangle cancels after summing the complete
   matching row (`7c62988`).
2. Complete site bars and Cartan prisms remain in the trivial matching
   representation.  They leave every matching-centered cut plus one Weyl
   marginal (`4f2472b`).  Hence group averaging does not produce an
   occurrence-local component projector.
3. Ordinary matching-tail multiplication does not transport the terminal
   packet.  Residue commutes with the Cartan square only for invariant
   oriented tails, and the two halves of the Kähler ridge have permanently
   different site degrees (`83151bf`).

These are not reasons to return to cycle enumeration.  The simultaneous
component theorem bypasses the second obstruction for the bright/dark
alternative.  The other two say that the physical terminal comparison must
still be relative and source-labelled.

There is nevertheless a clean representation-theoretic interference
pattern at six sites (`62054c1`):

\[
 \mathbb Q[\mathcal M_6]
      = \mathbf 1\ \oplus\ C_{\rm cut}^{0}\ \oplus\ D_{\rm alt},
             \qquad 15=1+9+5.                         \tag{I}
\]

Colour-diagonal tangent Hasse cubes generate the nine-dimensional centered
cut-permanent sector.  The five-dimensional debt is its alternating
`K3,3` determinant dual.  This is a transverse Fitting candidate, not a new
terminal: it becomes a physical carrier only when the corresponding
decorated determinant evaluates nonzero and its heads, support, and
cofactors satisfy the landing hypotheses.

### 4.1 The complete six-site entry fork

The decomposition above is now constructive on one side and physically
landed on part of the other side.  Let `v` be the complete
fifteen-occurrence profile obtained after retaining every contaminating
matching term in the balanced six-site word.

* If `v` has augmentation zero and all five determinant coordinates vanish,
  `4be703c` expands it uniquely in centered cut-permanent profiles.  The
  corresponding differences of physical tangent-Hasse cubes give the
  filtered source cycle

  \[
                         (v,-v),
  \]

  with `v` in the ordinary squarefree grade and `-v` in the repeated-site
  collision grade.  An ordinary occurrence marker can be retained, but it
  is not the physical pure/target anchor row.
* If an unbalanced decorated cross-cut determinant evaluates nonzero,
  `5a12d88` chooses a nonzero offdiagonal Laplace factor and the private-site
  identity turns it into a literal determinant--hafnian-cofactor fan.  When
  that factor lies on a simple selected edge, the result enters the existing
  coloop/C6--C8/five-lock landing alternative.
* The unbalanced cuts span only four of the five alternating directions.
  The four balanced determinants add one common quotient scalar.  The exact
  rational guard in `h3-balanced-only-determinant-debt.md` has hafnian zero,
  all unbalanced determinants zero, and all balanced determinants equal to
  three.  Nevertheless a bright balanced scalar on a zero mixed source row
  forces some offdiagonal cell elsewhere: if all offdiagonal cells vanished,
  the only diagonal matching product would equal both the balanced
  determinant and the zero mixed coefficient.  The private-site identity
  therefore returns this branch to the active-fan route after one extra
  source-equation step.
* A nonzero abstract determinant coordinate which is neither an evaluated
  physical minor nor a row-space occurrence pivot is only a correction
  debt.  It may not be called an active carrier.

Thus the old instruction “isolate the marked matching occurrence” is no
longer the right first theorem.  The exact remaining entry assertions are:

1. construct the protected comparison on the fifteen physical collision
   labels of the lower face, check its three shared-label coherence
   equations, and retain a nonzero physical anchor pairing (or dualize
   failure in the complete physical map); and
2. in the determinant branch, place an offdiagonal Laplace factor on a
   simple critical edge, or prove that failure of simplicity is already an
   effective Hall/reselection exit; and
3. for the one balanced-only scalar, use the zero mixed source equation to
   select an offdiagonal cell and enter the same active-fan landing.

Bare C4/C6 occurrence pairs never lie in the determinant-dark sector: every
one has six nonzero determinant readings.  Complete-row contamination is
therefore load-bearing data, not noise to remove term by term.

## 5. The transverse landing

The determinant-bright entry is now exhaustive (`1ec750e`).  A nonzero
unbalanced determinant supplies an offdiagonal Laplace factor; a nonzero
balanced-only determinant on the zero mixed row forces an offdiagonal cell
somewhere else in that row.  In either case the private-site identity gives
a nonzero distinct-head active fan.

For either physical edge `p` of that fan, complete pure target support gives
the exact endpoint-rank formula

\[
 \operatorname {rank}_{\rm pure}(p)
 =\#\{c:\text{some nonzero pure-}c\text{ matching avoids }p\}.
\]

Hence the fan is four-good unless one of its edges is a literal coloop of a
complete pure-colour matching family.  Simplicity relative to one selected
anchor triple and escape from that particular anchor union are unnecessary.

The earlier selected-edge quotient description remains useful after a
coloop is normalized.  Deleting a simple selected edge leaves one deficient
line at each endpoint.  Both quotient lines miss the same pure colour `c`
(`ea8c864`).  Therefore:

* same-word interference is dark in both quotients;
* a one-root Cartan exit is visible on only one side;
* the first single double-visible head is the two-root `(c,c)` corner.

If a nonzero pure-`c` matching avoids the selected edge, reselect it.  The
old edge leaves the three-anchor union, and any active escaping mate from
the two transposed fans gives a distinct-head four-good pair.  If no such
landing occurs, the exact survivors are

```text
pure-c coloop -> anchor-contained C6/C8 E2 carrier;
avoiding pure matching -> injective five-lock with no complementary wedge.
```

The arbitrary active-fan coloop is now the exact normalization gate.  The
full later target-coloop chain through `5a01b0a`, together with the
punctured-C4 and conjugate double-coloop theorems, consumes every coloop
already placed in the normalized packet.  Although the earlier intermediate
theorem `0556512` handed one case back to a multisite affine/Hall interface,
the later specialized chain closes that case.  Thus the remaining theorem is
only: normalize an arbitrary active-fan coloop into one of those packets, or
obtain a complete-row relation/free carrier before normalization.  `C6/C8`,
injective five-lock, and a post-normalization affine gate are not independent
residual theorem families.

If a complete dark equality expresses a double-visible Cartan image through
occupied scalar columns, elementary quotient linear algebra supplies either
one double-visible scalar column or two split-visible scalar columns
(`00db7ee`).  But visibility alone is not enough (`32f3bdc`): the unique
double-visible scalar may be diagonal on the selected edge, and two
split-visible scalars may remain anchor-contained or decorate the same
pair.  Positive landing is presently exact only when an active fan mate
escapes the anchor union, or the split labels form a distinct-pair,
distinct-head, nonzero-cofactor crossed wedge.

## 6. The common rootless/inactive comparison

The non-Euler physical first jets and their complete mixed Hasse correction
exist.  Their marked sector is the desired polar `h_v`, but the other
matching completions cancel it.  The five physical polars would define

\[
             \overline P:k^5\longrightarrow\operatorname{coker}\widehat J.
                                                               \tag{6}
\]

Once (6) is source-provenantly defined, Fredholm is final:

* a kernel vector of nonzero pentagon aggregate is the relative generator;
* otherwise the aggregate factors through `P` and gives the annihilator.

The canonical residual-q Cartan/Kodaira--Spencer lift is already physical,
with the correct residue and eta/sigma ridge (`367e068`).  What is not yet
proved is the protected comparison selecting the marked polar from its
complete Hasse row and transporting `Yw` to physical `W` in the common
rootless/inactive grade.  In particular, Cartan placement does not transport
the physical terminal `q=sum6m-ainc`.  The weakest law for a protected
comparison `Phi` is equality of the matching-aggregate and anchor-incidence
defect classes modulo `row(J)`, equivalently `q-q_3 Phi=lambda J`
(`8b43f2a`).  Once `Phi` maps the complete physical relative domains, the
terminal decision is closed (`7efd10d`): a nonzero defect gives a kernel
witness on which `q` or `q_3 Phi` is nonzero, hence a relative generator; a
zero defect transports `q` and feeds Fredholm.

The determinant-dark source-entry nullhomotopy and this downstream
comparison are now the same construction problem, not two unrelated maps.
For the explicit cut profile, `4647afe` retains eighteen directional lower
terms and quotients them to fifteen physical collision labels; the quotient
has exactly three shared-label coherence equations.  Commit `e8838b7` joins
that finite input packet to the literal one-face mapping-cone output isolated
by `7c6a87c`: a `360`-term endpoint-odd full-nine aggregate, Eq signature
`-delta`, zero protected target rows, and the prescribed eta/sigma packet.
On the oriented physical relabeling orbit, `Phi=rho_*` is already a protected
comparison.  Off orbit, membership of this one equivariant mapping-cone
family and the three coherence equations are the complete finite gate.

The required canonical output cell is now physical (`271df91`).  On the
normalized `Y=1` slice, the negative old cap aggregate supplies the exact
360-term private boundary and Eq signature, while the source-provenant
endpoint-odd Cartan/HPL cell cancels its residue and contributes the full
eta/sigma ridge.  Their sum is the literal `M_v` image with all protected
rows zero.  The comparison gate is therefore input-side only.

The input coherences have now collapsed to a single symmetry statement
(`47582d4`).  The cut transposition `rho=(1 4)` acts on the fifteen labels as
seven two-cycles and one fixed point, and the full lower face is
`(rho-1)u_012`; the shared labels form one fixed orbit and one paired orbit.
Equivariance therefore enforces all three equalities.  This is not yet a
physical relabeling: `rho` changes `001122` to `021102`, and the full GHZ
word stabilizer contains no cut transport.  The first physical source type
is one target-cancelled two-local-root Cartan--Spencer attachment realizing
the six moving pairs and the `M_v` image.  Gate I is now a one-operation
construction, not a fifteen-column interpolation.

There is an important typing boundary.  The Cartan homotopy leaves the
residual `K d(u_012)` in the fifteen-label six-site collision module, while
the constructed `M_v` boundary is a 360-feature decorated eight-site
packet.  Declaring those expressions equal would already assume `Phi`.
The remaining theorem is therefore the shifted fine-label/tail map between
these modules, intertwining the rho-odd residual with `M_v` and preserving
the complete protected rows.  The rho-even adjacent-power cell needed on
the inactive diagonal cannot supply this odd residual.

Constructing `Phi` settles the terminal `q` decision and is sufficient for
the rootless generator/Fredholm alternative.  It does not by itself prove
the physical pure/target anchor sees the determinant-dark kernel.  That
anchor law remains an independent row comparison only when this filtered
kernel is also used in the constructive rectangular route: transport
`ainc` separately, prove it kills the collision correction by fine grade,
or compute it directly on the corrected kernel.

## 7. Shortest remaining route

The proof should now be attacked in this order.

1. **Construct the one protected physical comparison.**
   Build the input-side equivariant two-local-root `Phi`; its cut-swap
   symmetry handles the three shared labels automatically, and its output
   is the now constructed literal `M_v` image.  This simultaneously
   nullhomotopes the determinant-dark
   lower face and defines the rootless/inactive comparison.  Exact terminal
   equality is unnecessary: mismatch gives the generator and agreement
   gives Fredholm.  If pursuing constructive Route A as well, separately
   prove that the physical pure/target anchor sees the corrected kernel, or
   use its physically typed row-space dual; this extra pairing does not
   block the rootless terminal alternative.
2. **In parallel, normalize and land the active-fan coloop.**  Every determinant-bright
   zero mixed row now yields an active fan, and complete pure supports make
   that fan four-good unless one edge is a literal pure-colour coloop
   (`1ec750e`).  Use the complete mixed/response rows to place an arbitrary
   such coloop in the normalized target-coloop or conjugate double-coloop
   packet, or directly obtain an anchor-safe relation/free carrier.  The
   normalized packets are already completely consumed by the later
   target-coloop chain.  The first complete-row normalization step is now
   uniform (`32ce01c`): eliminating the retained coloop cofactor between a
   pure target row and its two-site-mixed companion forces a literal
   omit-coloop pure or mixed carrier, with common `q`, endpoint
   orientation/head, fine word, and remote decorated tail all preserved.
   The remaining source theorem is only the landing of a carrier trapped in
   the saturated Hall shores.  The complete row already supplies its
   signless orientation sum, while the target-safe odd Cartan comparison
   would supply the difference (`e6b390a`); their half-sum/half-difference
   gives oriented affine rows.  Thus the live inputs are protected-packet
   agreement for that odd comparison and the separate physical-anchor
   visibility of the resulting circuit, not a signless homotopy or a new
   Hall census.
3. **Saturate before applying Hall duality.**  Build the finite directed
   graph of all source-certified exchanges reachable from the coloop fan.
   A target-line or free-fan vertex terminates positively.  If neither is
   reachable, apply matroid-intersection duality once to the saturated set
   and lift its tight-set covector through the complete source rows.  A
   dependence lowers support; a new typed exchange contradicts saturation.
   The combinatorial part is now finite and exact (`32e07b5`): `5,141`
   inputs yield `446` closed concepts and six symmetry types, and every new
   typed hole strictly enlarges closure.  The next exchange already has its
   complete-row physical provenance by the pivot above.  The sole remaining
   Hall datum is the simultaneous affine/dependence landing when all such
   carriers remain trapped; no separate move-by-move potential or six-case
   source census is required.

4. **Close global coverage.**  Either prove uniform entry of every
   synchronized packet into the source fork above, with a strict decrease
   through long-cycle and Hall returns, or extend `Phi` over all inactive
   normal faces and finish the horizontal and diagonal inactive routing.
   The latter is currently the shorter exhaustive route: all derived normal
   systems through order three are already built, so its remaining defect is
   physical typing and diagonal Rees membership.  A Hasse/Rees-linear `Phi`
   propagates the same finite label quotient to all jet orders (`981f1b0`),
   so no new matching census is needed.  The generic asymmetric diagonal
   route still needs one target-bearing adjacent-power cone cell and
   vanishing of the truncated class in `ker(epsilon)/N_lit`; at trace
   collision it needs the order-`h` unary jet or complementary survival.
5. **Finish by clean descent.**  A four-good active pair enters the proved
   clean-cap descent, lowers the even order by two, and repeated descent
   reaches the exact six-site contradiction.  The generator/separator
   outcomes close the exhaustive no-active-clean branch directly.

The central statement is therefore no longer “classify every interference
cycle,” “construct a physical projector onto each cycle,” or even
“manufacture a square anchor-critical cover.”  It is:

> **Source-entry, protected-comparison, and landing theorem.**  A complete
> marked occurrence profile either descends from its filtered
> Cartan--Spencer lift to an anchor-visible kernel, or exposes a physically
> evaluated determinant/pivot/Hall carrier; every exhaustive kernel branch
> admits one physical protected comparison; and every surviving carrier
> lands in a four-good pair or a support-reducing tight-set dependence.

The rectangular theorem performs the interference decision as soon as the
marked kernel exists; the simultaneous component theorem remains an
explicit way to assemble many dark potentials at once.  The rootless polar
and inactive cap still need the protected comparison, while the
combinatorial descent still needs transverse rank landing.

## 8. Honest status

Completed structural parts:

* separation of same-word interference and word-changing Cartan;
* zero-holonomy Schur factorization;
* rectangular anchor--Cartan rank/unit-kernel alternative;
* uniform physical Cartan source provenance and marked placement;
* simultaneous bright/typed-exit/global-kernel absorption over an exhaustive
  anchor-critical cover;
* terminal-safe treatment of complete dark kernels;
* exact classification of the first transverse quotient residuals;
* canonical residual-q Cartan/KS comparison;
* the exact `15=1+9+5` occurrence decomposition;
* a constructive determinant-dark filtered cycle for every complete
  augmentation-zero profile in the nine-dimensional sector;
* physical landing of every determinant-bright zero mixed row on an
  offdiagonal private-site fan;
* the complete-pure-support fan alternative: four-good or a literal
  pure-colour coloop, with no simple-edge or anchor-escape hypothesis.

Open load-bearing parts:

* the input side of the one fifteen-label protected physical comparison:
  the literal equivariant `M_v` output image is constructed, while the
  two-local-root word-changing map on the collision quotient remains;
* nonzero pairing of the resulting kernel with the physical pure/target
  reduction row, or a physically typed dual of its failure;
* protected odd-Cartan packet agreement and physical-anchor visibility for
  the trapped omit-coloop carrier; the complete-row signless packet and all
  carrier word/tail/orientation data are constructed;
* on the logically shortest exhaustive route, one rho-even target-bearing
  adjacent-power companion, literal truncated-Rees membership, and the
  final horizontal/diagonal inactive routing;
* alternatively, uniform constructive entry plus the active-fan coloop
  landing above and a well-founded inner decrease.

No further flat-cycle or bounded support census is presently justified
unless it tests one of these statements.
