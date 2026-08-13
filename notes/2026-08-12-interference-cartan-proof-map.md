# Interference--Cartan proof map

Audit date: 2026-08-12.

This is the current shortest proof sketch.  It replaces a large collection
of local cycle cases by one marked complete-source kernel lift, one complete
word-changing Cartan column, and one physical terminal alternative.  It is
not yet a proof of the conjecture: the marked lift, construction of one
protected physical comparison, and final transverse landing are the three
live structure theorems.

## 1. Global contradiction setup

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

## 2. The rectangular interference alternative

Let `M:X->Y` be the complete protected source-incidence map in the finite
labelled packet, let `h` be the marked anchor row, and let `g` be the whole
physical Cartan column.  The essential entry datum is one kernel circuit

\[
                         Mc=0,\qquad h(c)\ne0.         \tag{K}
\]

Then the exact rectangular alternative (`a4e15ab`) is:

* `[g] != 0` in `coker M`: adjoining `g` and `h` raises rank by two, giving
  the bright localized minor/source-unit branch;
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

The marked anchor makes `h^Tc!=0`.  Thus only the Cartan charge matters, and
its two branches are exactly the two rectangular cases above.

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
(2), because the complete labelled source map retains every matching
completion and contaminating term.  The exact lift gate (`03f6304`) starts
with the common-tail candidate `x0`, marked value `h(x0)!=0`, and defect
`d=Mx0`:

* a correction `z` with `Mz=-d` and `h(z)=0` yields the required marked
  kernel `x0+z`;
* otherwise `h` lies in `row(M)` and gives a separator reading nontrivially
  on `d`; if `h` is the literal marked-coordinate row, this is already a
  pivot/coloop source-unit exit.

Thus the remaining entry theorem is a marked-coordinate-preserving
chain/nullhomotopy lift from the optical circuit to the complete source
presentation.  The no-common-tail and repeated-site failures continue to
route to Tutte/Hall and principal-parts/Cartan-Spencer exits.

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

## 5. The transverse landing

Deleting a simple selected edge leaves one deficient line at each endpoint.
Both quotient lines miss the same pure colour `c` (`ea8c864`).  Therefore:

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

## 7. Shortest remaining route

The proof should now be attacked in this order.

1. **Prove the marked complete-source kernel lift.**  Lift the
   protected-relative optical frame circuit through the common-tail source
   map while retaining its marked coordinate.  A successful nullhomotopy
   feeds the rectangular alternative; a literal-coordinate separator is
   already the pivot/source-unit branch.
2. **Construct one protected physical comparison.**  Build a source-valid
   `Phi` from each remaining exhaustive grade to the canonical
   rootless/inactive grade.  Exact terminal equality need not be imposed:
   mismatch gives the generator and agreement gives Fredholm.  Do not
   demand false arbitrary-tail naturality.
3. **Land scalar exits.**  Convert one double-visible or two split-visible
   occupied columns to a four-good pair, or route the explicit coloop
   `C6/C8` and injective five-lock residuals.
4. **Use a finite relation potential.**  Each nonzero complete residual
   enlarges the saturated relation component; each unit cancellation lowers
   the relative-domain rank; a Schur unit, physical generator, separator, or
   four-good pair terminates.  Prove that Hall/reselection moves cannot
   increase the leading pair

   \[
       (\text{unjoined saturated labels},\ \text{relative-domain rank}).
   \]

5. **Finish by clean descent.**  A four-good active pair enters the proved
   clean-cap descent, lowers the even order by two, and repeated descent
   reaches the exact six-site contradiction.  The generator/separator
   outcomes close the exhaustive no-active-clean branch directly.

The central statement is therefore no longer “classify every interference
cycle,” “construct a physical projector onto each cycle,” or even
“manufacture a square anchor-critical cover.”  It is:

> **Marked-lift, protected-comparison, and landing theorem.**  A nonzero
> marked matching occurrence either lifts to an anchor-visible kernel of the
> complete labelled source map or exposes a typed pivot/active/Hall carrier;
> every exhaustive kernel branch admits one physical protected comparison;
> and every surviving visible scalar lands in a four-good pair or one of the
> two explicit finite residuals.

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
* canonical residual-q Cartan/KS comparison.

Open load-bearing parts:

* marked-coordinate-preserving lift from an optical frame circuit to the
  complete labelled source kernel;
* one common rootless/inactive protected physical comparison (terminal
  mismatch/agreement is already closed once this exists);
* scalar-exit transverse landing for the two explicit residual types;
* global monotonicity through Hall/reselection moves.

No further flat-cycle or bounded support census is presently justified
unless it tests one of these four statements.
