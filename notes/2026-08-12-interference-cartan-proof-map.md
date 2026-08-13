# Interference--Cartan proof map

Audit date: 2026-08-12.

This is the current shortest proof sketch.  It replaces a large collection
of local cycle cases by one interference block, one word-changing Cartan
test, and one physical terminal alternative.  It is not yet a proof of the
conjecture: the occurrence-local/terminal comparison and final landing are
the two live structure theorems.

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

## 2. The interference block

Take a minimal square critical block `M` in the component.

* Nontrivial/odd holonomy makes `M` invertible, hence gives a localized
  source unit.
* Zero holonomy gives `rank(M)=r-1` with full-support right and left charges
  `c` and `ell`.

For a pure anchor row `h` and a word-changing connector `g`, the complete
Schur minor is

\[
 \det\begin{pmatrix}M&g\\h^T&\alpha\end{pmatrix}
        =-\kappa(h^Tc)(\ell^Tg).                       \tag{2}
\]

The marked anchor makes `h^Tc!=0`.  Thus only the Cartan charge matters.

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

## 3. The dark branch

If `ell^Tg=0`, there is an exact component potential

\[
                              My=g.                    \tag{3}
\]

For complete lifts `C,G`, form

\[
                              R=G-Cy.                  \tag{4}
\]

There are two source-level possibilities.

### 3.1 Nonzero complete residual

If the component projection is saturated by word, matching, tail,
orientation, and fine-grade labels, every nonzero coordinate of `R` is a
literal typed exit from the current component.  Adjoining its incident
relation strictly enlarges the finite relation component.  A global proof
must show that this enlargement either reaches a bright Schur test or lands
in the active/Hall alternatives below.  It may not silently call an omitted
internal fine label an exit.

### 3.2 Zero complete residual

If `R=0`, then

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

These are not reasons to return to cycle enumeration.  They say precisely
that the remaining comparison must be relative and source-labelled.

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
(`00db7ee`).  Activity and anchor-safe landing of those columns remain a
physical theorem; visibility alone is not enough.

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
proved is the occurrence-local comparison selecting the marked polar from
its complete Hasse row and transporting `Yw` to physical `W` in the common
rootless/inactive grade.  The component-splitter cokernel above shows why a
complete group bar alone cannot perform this selection.

## 7. Shortest remaining route

The proof should now be attacked in this order.

1. **Occurrence-local augmented alternative.**  Construct a relative
   source operator with nonzero matching-centered boundary, or prove that
   its first failure is a physically typed kernel/separator.  The natural
   candidate is a tangent-corrected logarithmic Euler/Hasse cube through one
   nonzero marked matching; arbitrary differentiation of a point equation
   is invalid and must not be used.
2. **Define the physical terminal once.**  Build the labelled shifted
   Kähler comparison in the canonical rootless/inactive grade.  On all
   other fine grades, prove either a covariant transported copy or a
   terminal-zero direct summand; do not demand false arbitrary-tail
   naturality.
3. **Land scalar exits.**  Convert one double-visible or two split-visible
   occupied columns to a four-good pair, or route the explicit coloop
   `C6/C8` and injective five-lock residuals.
4. **Use a finite relation potential.**  Each nonzero complete residual
   enlarges the saturated relation component; each unit cancellation lowers
   the relative-domain rank; a Schur unit, physical generator, separator, or
   four-good pair terminates.  Prove that Hall/reselection moves cannot
   increase the leading pair

   \[
       (\text{unjoined saturated labels},\ 	ext{relative-domain rank}).
   \]

5. **Finish by clean descent.**  A four-good active pair enters the proved
   clean-cap descent, lowers the even order by two, and repeated descent
   reaches the exact six-site contradiction.  The generator/separator
   outcomes close the exhaustive no-active-clean branch directly.

The central conjectural statement is therefore no longer “classify every
interference cycle.”  It is:

> **Augmented occurrence-localization theorem.**  A nonzero marked matching
> occurrence in the complete source fibre either admits a tangent-corrected
> relative projector, exposes a physical active/Fitting carrier at its first
> uncorrectable face, or is detected by the physical terminal kernel/dual.

That theorem is the common source of the combinatorial contraction, the
rootless polar, and the inactive cap.  Proving it would turn the remaining
maps into formal or already-audited landing steps.

## 8. Honest status

Completed structural parts:

* separation of same-word interference and word-changing Cartan;
* zero-holonomy Schur factorization;
* uniform physical Cartan source provenance and marked placement;
* terminal-safe treatment of complete dark kernels;
* exact classification of the first transverse quotient residuals;
* canonical residual-q Cartan/KS comparison.

Open load-bearing parts:

* occurrence-local augmented localization or its physical dual;
* common rootless/inactive terminal comparison;
* scalar-exit transverse landing for the two explicit residual types;
* global monotonicity through Hall/reselection moves.

No further flat-cycle or bounded support census is presently justified
unless it tests one of these four statements.
