# The physical augmented pentagon has a generator-or-annihilator alternative

## Exact theorem interface

Let \(k\) be a field of characteristic zero. In the rootless \(h=3\)
two-chart packet, suppose the following **physical** data have been
constructed in one common source complex:

* an augmented correction map
  \(\widehat J:L\to E\), including source boundary, physical target, and
  ordinary-residue rows; and
* a map \(P:C=k^5\to E\) from the five labelled pentagon ridge/polar
  classes, obtained from invisible first jets and their complete mixed
  Hessian/overlap correction.

Write

\[
 Q=E/\operatorname{im}\widehat J,\qquad
 \overline P:C\longrightarrow Q,\qquad
 \epsilon(c_0,\ldots,c_4)=\sum_i c_i .                 \tag{1}
\]

Then exactly one of the following holds.

1. **Relative generator.** There is \(c\in\ker\overline P\) with
   \(\epsilon(c)\ne0\). By definition,
   \(P(c)=\widehat J(x)\) for some \(x\in L\), so the corrected physical
   combination

   \[
                    P(c)-\widehat J(x)=0                \tag{2}
   \]

   is a relative cycle. Multiplication by
   \(\epsilon(c)^{-1}\) normalizes its pentagon aggregate to one. Because
   target and ordinary residue are rows of \(\widehat J\), (2) is exactly
   the primitive target- and residue-zero anchor face required by the
   augmented-pentagon interface of commit 5f490c6.

2. **Rootless separator.** There is a functional
   \(\lambda\in Q^*\) such that

   \[
              \lambda\overline P=\epsilon .             \tag{3}
   \]

   Its lift to \(E^*\) obeys
   \(\lambda\widehat J=0\) and \(\lambda P=\epsilon\). Thus it kills every
   admitted physical correction and reads one on the pentagon aggregate.
   When \(Q\) is the source-provenant terminal/Macaulay quotient of
   Component III, this is exactly the missing annihilator.

The proof is one line of Fredholm duality. A vector as in item 1 exists
exactly when \(\epsilon\) does not vanish on \(\ker\overline P\). If it does
vanish there, \(\epsilon\) factors through
\(\operatorname{im}\overline P\); extend the resulting functional to \(Q\)
to obtain (3). The alternatives are exclusive because applying (3) to a
vector from item 1 would give \(0=1\).

This removes a potential rank case split from the rootless proof. Once the
physical augmented overlap--jet map \(P\) is defined in the correct
terminal quotient, **every** rank outcome is useful: it supplies either the
positive relative face or the dual Macaulay obstruction. It does not,
however, define \(P\).

## The exact datum still needed to define \(P\)

The source-valid input is the augmented mixed-jet datum of
h3-augmented-hasse-schmidt-polar-membership.md. For each of the five faces
one needs two invisible first jets \(\xi_v,\eta_v\) in the same two-chart
source, together with the literal correction module \(L\), such that

\[
 \widehat J\xi_v=\widehat J\eta_v=0,\qquad
 P(e_v)=
 [\widehat H(\xi_v,\eta_v)]
       \in\operatorname{coker}\widehat J .              \tag{4}
\]

Here \(\widehat J\) includes physical target and ordinary residue before
the quotient. The two-chart comparison must identify (4), with its endpoint
and residual-word grade intact, with the five ridge classes whose aggregate
pushes to the Component-III terminal line. Finally, the landing must
annihilate \(\ker\widehat J\); otherwise (4) depends on the choice of mixed
correction and is not a source-provenant map.

Thus the missing object is not a choice of a favorable rank for five formal
symbols. It is one chain map: the complete target/residue-augmented
two-chart mixed-Hessian comparison into the physical terminal quotient.

## Audit of committed candidates

No committed polar or Schur object yet instantiates (4).

* The shifted marked principal-parts square is a genuine
  **presentation-relative** two-chart cycle and has the correct polar
  \(h_v\), but it explicitly does not construct geometric invisible first
  jets. Its reset commutator has five independent components.
* The bare Schur polar has source connecting matrix \(I_5\). Consequently
  its leading cochain does not descend through the lower source boundary;
  it is not a map \(P\) into the augmented physical cokernel.
* The squarefree fourth-Hasse cone supplies a formal relative face, but its
  selected operator sends the source equation \(H_m\) to \(1\). Its
  diagonal physical projection has defect \((H_0-u)e_{\rm Eq}\), so it
  fails source descent before (4) is defined.
* The zero-target terminal packet has a complete physical two-chart array,
  but omits the nonzero diagonal GHZ anchors. It excludes an anchor-blind
  contraction; it cannot define the anchor-relative map required here.
* Commit a2292a2 and the all-order target-lock theorem exclude ordinary
  polynomial/Tate replacements: target-zero polynomial source combinations
  have zero pure-anchor incidence. They do not construct (4).

The denominator-decoration fork is therefore no longer a rank-choice
problem. A chart-odd decoration may put the construction in item 1; a
nonrepairing decoration may put it in item 2. Either conclusion is valid
only after the same physical augmented map (4) is built. Treating the
three-term polar, its scalar fourfold coefficient, or its stipulated chart
decoration as \(P\) would discard exactly the first-jet, target, residue,
and zero-indeterminacy conditions which remain open.

## Verification and scope

Run:

    python3 computations/verify_h3_rootless_augmented_pentagon_fredholm_alternative.py
    python3 -O computations/verify_h3_rootless_augmented_pentagon_fredholm_alternative.py
    python3 -I -S computations/verify_h3_rootless_augmented_pentagon_fredholm_alternative.py

The checker exhausts every binary matrix with zero through three quotient
rows and five pentagon columns (33,825 matrices), proving the exclusive
repair/separator alternative. It separately constructs exact rational
examples with a nontrivial correction quotient and verifies both the lifted
equation (2) and the dual row-space branch.

The frozen ledger digest is

    be24a91a9d275eaa7879cdb91a057b4d4993ca8608307ee3bb03376859d23f24

This is an exact theorem interface, not the overlap--jet theorem, a physical
relative generator, or a proof of Krenn's conjecture. Its additive content
is that the rank of the eventual physical five-polar map cannot create a
third rootless branch: physical construction and zero-indeterminacy of that
map are the only remaining tasks.
