# Independent audit of the single-Koszul five-face star

Audit target: corrected commit `c32f529`.  The full-image coordinate
subpresentation, (u)-leading identity map, corrected fixed-chart symmetry,
relabelled-chart scope, and packet Tor comparisons are sound.

This audit does not construct a cap homotopy, prove compatibility between
relabelled (r)-charts, give packet Tor classes full-source provenance,
establish zero indeterminacy, or prove Krenn's conjecture.

## 1. Audited outcome

For the selected odd word

\[
                         \bar m=12112,
\]

the five reset-active denominator columns have complete coordinate support
on exactly 211 of the 243 five-site words.  This is the smallest coordinate
subpresentation containing their **entire** images.  The remaining 32 words
disagree with (\bar m) at every site.  The single coordinate
(e_{12112}) already detects the five defects, so the corrected note is
right not to claim 211 is minimal among quotients or readouts.

For the degree-four cell

\[
 K_m=H_mr_0+(u-H_0)r_m,
 \qquad m=01211222,
\tag{A1}
\]

the literal reset defect on column (d_{v,\bar m_v}) is

\[
                     (u-H_0)h_vY_0.
\tag{A2}
\]

The (u)-coefficient of (A2), after labelling the five independent classes
(h_vY_0) by (\omega_v), is exactly

\[
                        I_5:D_{\bar m}\longrightarrow W.
\tag{A3}
\]

Thus the fact that (A1) is one Koszul cell does not turn its five incident
denominator relations into one face sum.  This statement is conditional on
the literal representative-independent reset architecture; it is not a
necessity theorem for every possible source complex.

The earlier symmetry objection is fully corrected.  The word stabilizer is

\[
 S_{\{1,3,4\}}\times S_{\{2,5\}}\cong S_3\times S_2,
\tag{A4}
\]

with two face orbits, but it moves the distinguished site (r=3).  It gives
two templates only over a family of relabelled (r)-charts, and only after
one proves compatibility of that transport.  In the fixed direct-free
overlap, the available subgroup is

\[
 S_{\{1,4\}}\times S_{\{2,5\}}\cong S_2\times S_2,
\tag{A5}
\]

with three orbits

\[
                       \{1,4\},\qquad\{3\},\qquad\{2,5\}.
\tag{A6}
\]

Exactly three seed types are necessary and sufficient inside this fixed
chart.  The corrected shortest-attack recommendation therefore has the
right scope.

Finally, independently rebuilding the two packet denominator matrices gives
face-image ranks four and three, Tor dimensions eight and seven, and
four-dimensional cap-invisible kernels in both packets.  These remain
specialization counterguards, not physical source constructions.

## 2. The exact 211-coordinate subpresentation

The universal denominator entry is reconstructed directly as

\[
 [e_w]\delta(d_{v,a})=
 \begin{cases}
 \displaystyle
 \sum_{M\in\operatorname {Match}(D\setminus\{v\})}
       \prod_{ij\in M}q_{ij}^{w_iw_j},&w_v=a,\\[5pt]
 0,&w_v\ne a.
 \end{cases}
\tag{A7}
\]

For each selected column (d_{v,\bar m_v}), (A7) is nonzero on the 81
words satisfying (w_v=\bar m_v).  The union of the five supports consists
of the words agreeing with (\bar m) at least once.  Its complement has two
wrong-colour choices independently at every site, hence

\[
                   3^5-2^5=243-32=211
\tag{A8}
\]

active coordinate words.

Every active coordinate contains a nonzero universal three-term quadratic
in at least one selected column.  Therefore a coordinate subpresentation
which retains every column image must retain all 211 coordinates.  The five
columns themselves are independent: for each (v), choose the word equal
to (\bar m_v) at (v) and zero elsewhere.  It occurs only in selected
column (v), giving a diagonal five-column nonzero-polynomial witness.

This verifies the exact qualification introduced by `c32f529`.  A smaller
coordinate quotient may detect (or forget) selected features, but it is no
longer the subpresentation containing the full five column images.

## 3. Why the (u)-leading map is (I_5)

The literal reset kills the pure row (r_0).  On (r_m), its failure to
descend is the five-column map

\[
 d_{v,\bar m_v}\longmapsto h_vY_0,
 \qquad v=1,\ldots,5.
\tag{A9}
\]

Multiplying (r_m) by its Koszul coefficient (u-H_0) multiplies (A9)
column by column.  Since (u) is an independent homogenizing variable and
(H_0) contains no (u), coefficient extraction at (u) gives

\[
 d_{v,\bar m_v}\longmapsto h_vY_0.
\tag{A10}
\]

The five (h_v) have disjoint labelled deletion-face monomial supports.
Passing from their actual polynomials to the labelled face space
(W=\langle\omega_1,\ldots,\omega_5\rangle) turns (A10) into (A3), not
the vector ((1,1,1,1,1)) and not an alternating boundary.

The rest of (A1) cannot cancel this coefficient.  The (H_mr_0) term is
killed by the reset, and (-H_0r_m) has (u)-degree zero.  After setting
(u=1), the same separation appears in edge degree: (h_v) has degree two,
whereas (H_0h_v) begins in degree six.

The resulting rank-five obligation is representative-independent only in
the stated literal sense: a chain map on the selected presentation must
handle all five relation generators.  A larger source syzygy, a non-flat
full-source kernel, or a different corrected reset with a proved chain
identity can change the presentation and is not excluded.

## 4. Full word symmetry versus fixed-chart symmetry

The independent checker enumerates all permutations of the five odd sites.
Twelve preserve (12112), yielding the two orbits

\[
                     \{1,3,4\},\qquad\{2,5\}.
\tag{A11}
\]

The full permutation module has a two-dimensional invariant plane.  A
cyclic submodule has at most one invariant direction; exact orbit reduction
gives sharp generic cyclic rank four.  The orbits of (\omega_1) and
(\omega_2) span dimensions three and two and together span (W).  Hence
two templates are minimal at the word-stabilizer level.

That group is not a symmetry of the fixed overlap.  The condition
(A_{p3}=0) and the chosen `pr` chart distinguish site 3.  Requiring the
permutation to fix site 3 leaves the order-four subgroup (A5) and the three
orbits (A6).  Its invariant subspace has dimension three, one line for each
orbit.  Since the group is abelian and the remaining two isotypic lines are
the two sign characters, a cyclic submodule has dimension at most three.
The checker obtains this sharp rank for a generic vector.

Every module generator contributes at most one invariant direction, so
fewer than three generators cannot span the fixed-chart invariant
three-plane.  Conversely, the three orbit seeds

\[
                        \omega_1,\qquad\omega_3,\qquad\omega_2
\tag{A12}
\]

have orbit spans of dimensions two, one, and two and together span (W).
This proves the exact three-seed statement.

Applying a permutation in (A4) which moves site 3 changes the zero block and
the second chart.  It therefore transports a construction to a different
(r)-chart rather than producing another cell inside the original chart.
The two-template statement is sound precisely as phrased after correction:
one must construct a natural family and separately prove its compatibility
under those chart changes.

## 5. Packet Tor and indeterminacy comparison

The audit reconstructs both 243-by-15 denominator matrices from their raw
internal (q)-cells.  Exact rational reduction gives

\[
\begin{array}{c|c|c|c|c}
 &\operatorname {rank}b&\dim\ker b&
 \operatorname {rank}\tau&\dim\ker\tau\\ \hline
\text{direct-free}&7&8&4&4\\
\text{tilted}&8&7&3&4.
\end{array}
\tag{A13}
\]

The tilted image is contained in the direct-free image.  Both contain the
individual directions (\omega_1,\omega_3) and not
(\omega_2,\omega_4,\omega_5).  Adjoining
(\omega_2,\omega_5) completes both images; the tilted image needs both,
so one common additional direction cannot suffice.

The four-dimensional kernels in (A13) are cap-invisible for this diagnostic
map.  They do not prove downstream readout ambiguity, because a later
physical residue may annihilate them.  They do prove that this denominator
calculation alone does not establish zero indeterminacy or select a
canonical lift.  The corrected primary note states this distinction
accurately.

Neither rational packet lies on the full source scheme, and neither packet
preserves the word-stabilizer symmetry used in Section 4.  Their ranks do
not lower the universal five-component requirement or provide physical
source rows.

## 6. Verification and scope

The independent checker
[`audit_h3_single_koszul_cell_face_star_no_go_independent.py`](../computations/audit_h3_single_koszul_cell_face_star_no_go_independent.py)
imports nothing from the primary executable.  It reconstructs the universal
selected columns and face polynomials, enumerates both permutation groups,
computes orbit and invariant ranks, and rebuilds both packet Tor maps.

The audited theorem is conditional on retaining the literal associated-grade
reset ( -\kappa\iota_{00000}\epsilon_{12112}) as a
representative-independent chain map on the selected presentation.  It does
not state that five independent physical cells are necessary in every proof
architecture.  In the fixed overlap it reduces construction templates from
five to three; reducing from three to two requires an additional relabelled-
(r)-chart compatibility theorem.
