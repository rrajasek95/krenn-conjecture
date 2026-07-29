# Independent audit of the degenerate three-line-field response normal form

## 1. Verdict and certification boundary

Sections 1--6 of
[the primary normal-form note](degenerate-three-line-field-response-normal-form.md)
are correct.  The incidence boundary, five-good-site axial/bridge dichotomy,
boundary-pair forcing, singleton collisions, local separability table,
layer-Hall classifications, and the 141/110 bridge censuses survive an
independent reconstruction.

The
[clean-room checker](../computations/audit_degenerate_three_line_field_response_normal_form_independent.py)
imports no project code.  It certifies the finite combinatorics and symbolic
rank identity.  The arbitrary-vector quotient, response-module split, and
singleton response-tensor arguments are mathematical proofs, not facts
established merely by the finite census.  This distinction is important:
the computation does not sample arbitrary rows or infer that aggregate
cancellation vanishes termwise.

This audit was made against these frozen SHA-256 identities:

~~~text
8cacf2696b109f800143c269738bbfb8290393efbe044783e9d315a395d3eec4  notes/degenerate-three-line-field-response-normal-form.md
4be9cff9b9a2812ba5410e5427bdc93dfdd7a0ad54f8f83b405d58900c312c0a  computations/verify_degenerate_three_line_field_response_normal_form.py
68217adfaa39f7638c9403ac285d4b02d34bd3cd774ae442ed2a530cf283bd3d  computations/audit_degenerate_three_line_field_response_normal_form_independent.py
~~~

## 2. Four-cover, site cover, and the all-deficient boundary

Two response rows can change factors at only the two missing sites of a
four-site field lift.  Quotienting by \(W_u\) at any three sites therefore
kills every response summand.  A pure target survives exactly when it lies
outside all three local spaces, proving that each target axis belongs to at
least four \(W_u\)'s.

For the site cover, contraction at a fixed site by
\(\eta\in W_u^\perp\) kills every term not missing that site.  Retaining both
endpoint orders gives

\[
 M=xR^{\mathsf T}+Cy^{\mathsf T},
\]

so \(\operatorname{rank}M\le2\) with all aggregate sums still present.  If
all three target axes were outside \(W_u\), choose \(\eta\) nonzero on their
three quotient classes and choose the other contractions nonzero on every
target factor.  The literal response would then make \(M\) an invertible
diagonal matrix, a contradiction.  The independent checker verifies the
determinant identity symbolically in twelve variables, rather than by random
trials.

If every \(\dim W_u\le2\), the three four-covers give at least 12 target-axis
incidences, while the six local spaces allow at most 12.  Equality forces six
coordinate planes, each target omitted twice.  Exhaustive enumeration gives
90 labelled omission assignments.  Projecting \(q\), but not the response
rows or targets, to these fixed planes preserves \(F\) and both power
equations; the already audited coordinate-plane mixed-packet theorem then
closes this branch.

## 3. Five-site box theorem

At the five good sites the three field axes are independent.  Their
radius-two Hamming balls are pairwise disjoint because their centres have
distance five.  The good-coordinate support of a pure target is a Cartesian
box contained in the union of these balls.

The independent checker enumerates all \(15^5=759{,}375\) **ordered** boxes on
three field symbols plus one collapsed transverse symbol.  For each box it
literally searches for a word in which no field occurs three times; such a
word lies outside all three balls.  Collapsing all transverse basis symbols
to one is exact here because every transverse choice is a deviation from all
three field centres, and a word chooses only one coordinate per site.

Exactly 6,516 boxes are contained in the union: 6,093 are axial and 423 are
binary bridges.  The alternatives are disjoint and their field or field pair
is unique.  In an axial box, three singleton field coordinates force every
word into that one ball.  In a bridge box all factors use one field pair and
each singleton class has size at most two.

## 4. Boundary words and bridge census

An axial target with exactly three good agreements has two remaining sites.
Choosing a nonaxial coordinate at each produces a word on the boundary of
only its assigned field ball.  Its two deviations force the missing pair to
be exactly those sites, leaving the bad-site field vector proportional to the
bad-site target.  This supplies the fourth axial agreement.

For a bridge between fields \(r,s\), choose an \(r\)-centred boundary word
with \(s\) at exactly two sites.  The supported pairs are precisely

\[
 S\subseteq P\subseteq S\cup M, |P|=2,
\]

and the symmetric formula holds around \(s\).  Since the target coefficient
of every such word is nonzero and no other field ball contains it, the
corresponding aggregate lift coefficient is nonzero.  This uses uniqueness
of the field module, not termwise cancellation inside a response tensor.

For a fixed field pair, the independent checker examines all \(3^5\) patterns
of \(r\)-singleton, \(s\)-singleton, and mixed sites.  The singleton bounds
leave 141 patterns.  It reconstructs both forced pair families by literal
boundary-word support and verifies they have distinct representatives.  A
three-family Hall failure can remain only when a forced family is a singleton
or their union has at most two elements, equivalently
\(|R|=2\) or \(|S|=2\).  Exactly 110 patterns survive, with profile census

\[
10(2,0,3)+30(2,1,2)+30(2,2,1)
+10(0,2,3)+30(1,2,2).
\]

## 5. Singleton collisions and local selectors

After restriction to good coordinates, the three radius-two field modules
are disjoint.  Every field has a nonzero diagonal target component: in the
all-axial case this is its assigned target; in the bridge normal form fields
zero and one have axial targets and field two has a nonzero bridge boundary
component.  For every two fields there is a target component nonzero in one
module and zero in the other.

If \(H_r=H_s=\{P\}\), the nonzero singleton module forces the common ordered
endpoint tensor \(B_{tt}(P)\) to be nonzero, while the zero singleton module
forces that same tensor to vanish.  Aggregate lift coefficients and outside
field factors are nonzero and may be cancelled; no individual summand inside
\(B_{tt}(P)\) is separated.  More generally, if an axial \(s\)-target deviates
from \(L_s\) exactly on \(P\), quotienting its \(s\)-module at those two sites
kills every missing pair other than \(P\) and forces \(B_{tt}(P)\ne0\), while
a singleton \(r\)-module on \(P\) forces \(B_{tt}(P)=0\).

The three bad-site matroids have exactly the nonseparable killed-field sets

\[
\begin{array}{c|c}
\text{circuit}&|K|=2\\
L_0=L_2\ne L_1&\{0\},\{2\},\{0,1\},\{1,2\}\\
\text{rank one}&\varnothing\ne K\ne\{0,1,2\}.
\end{array}
\]

The checker independently tests all locally separable selector triples:
2,130 circuit, 1,430 coincident, and 780 rank-one labelled choices.  The
good selectors plus the bad quotient retain exactly the chosen lift in every
field.  A killed good-site field axis is likewise omitted by its selected lift
and may be restored to its original independent axis.  When a selected
incident field is killed at the bad site, its chosen lift omits that site;
replacing the unused zero image by a nonzero dummy is therefore required and
harmless before applying the distinct-lift theorem.

## 6. Layer-Hall audit and scope

The checker exhausts all \(63^3=250{,}047\) triples of nonempty families on a
six-element model split into three good-layer and three bad-star elements.
Three representatives can detect only equality and unions of size at most
three, so this model realizes every Hall pattern relevant to the physical
10+5 split.  For each triple it lists the star-field set \(K\) of every SDR
and verifies:

* the circuit residual forbids the all-good, all-star, and one-star triples,
  leaving only \(|K|=2\);
* the coincident residual forbids both equal fields being in the same layer,
  giving the two displayed failures in equation (30) of the primary note;
* the rank-one residual forbids the all-good and all-star triples, leaving
  only nonempty proper \(K\);
* under the bridge hypotheses, the dimension-two conditions imply
  \(I_1=\varnothing\), the exact alternative (32), and the Hall alternatives
  (33); the rank-one conditions imply both failures in (36).

The finite checks reproduce 90 plane assignments, the 6,093/423 box split,
the 141/110 bridge split, and all layer classifications.  They do not extend
the theorem to two deficient sites: with only four or fewer good sites the
radius-two balls need not be disjoint.  They also do not turn a response
normal form into the missing arbitrary-\(n\) descent for Krenn's conjecture.

Run

    uv run python computations/audit_degenerate_three_line_field_response_normal_form_independent.py

for the full finite and symbolic replay.
