# Three selected constant monomials force an external cancellation cycle

This is a uniform occurrence-level consequence of exact monochromaticity.
It applies to arbitrary aggregate endpoint matrices, not only diagonal or
rank-one edges.

Let `B` have even cardinality `n>=6`, and suppose

\[
 H_B(A)=\sum_{r=0}^2 e_r^{\otimes B}.                       \tag{1}
\]

For each `r`, choose a perfect matching `M_r` whose color-`r` diagonal
monomial

\[
                         \mu_r=\prod_{uv\in M_r}A_{uv}(r,r) \tag{2}
\]

is nonzero.  Such a matching exists because the constant coefficient in
(1) is one.

It is useful to regard (2) as a *decorated* matching: its edge `uv` joins
the endpoint-color ports `(u,r)` and `(v,r)`.  Even if two underlying
matchings use the same pair `uv`, their differently colored decorated
occurrences are distinct parallel edges.

## Theorem (selected-factor cancellation cycle)

The decorated union `M_0 union M_1 union M_2` contains a fourth perfect
matching `M`.  Its induced vertex coloring `c` is mixed, and `M` is the
unique compatible perfect matching contained in that decorated union.
Consequently the full support of `A` contains a different nonzero matching
monomial `M'` with the same coloring.  The symmetric difference
`M triangle M'` is a nonempty union of alternating even cycles.  Every
`M'`-edge on those cycles is an endpoint-color occurrence outside the three
selected matchings.

## Proof

The three decorated `M_r` are pairwise edge-disjoint one-factors of a
cubic multigraph.  The standard three-one-factors lemma says that their
union has a fourth perfect matching whenever `n>=6`.  A self-contained
proof is given in
[`odd-near-perfect-gadget-obstruction.md`](odd-near-perfect-gadget-obstruction.md):
switch a proper alternating-cycle component if one exists; otherwise use
one opposite-parity chord, or two interlacing same-parity chords, relative
to an alternating Hamilton cycle.

*Attribution.*  The three-one-factors lemma is **Bogdanov's observation**
(Bogdanov 2017); the occurrence-multigraph form used here is Thm 1.7 of
Chandran-Gajjala-Illickan, arXiv:2407.00303 (the simple-graph form is
Thm 1 of Chandran-Gajjala, arXiv:2202.05562).  See
[`references/REFERENCES.md`](../references/REFERENCES.md).  No priority is
claimed for it here.

Color each vertex by the decoration of its incident edge in `M`.  This
coloring is mixed, since a monochromatic matching in the selected union is
necessarily the corresponding `M_r`.

Now fix this coloring `c`.  At the selected port `(v,c(v))`, exactly one
edge of the decorated union is incident: the edge of `M_(c(v))` at `v`.
Thus any compatible perfect matching contained in the selected union is
forced edge by edge and equals `M`.

The monomial of `M` is nonzero, being a product of selected nonzero cells.
But its mixed coefficient in (1) is zero.  A sum over a field cannot cancel
one nonzero summand by itself, so there is a distinct compatible perfect
matching `M'` with nonzero monomial.  Two distinct perfect matchings have
symmetric difference a nonempty disjoint union of alternating even cycles.
More strongly, if `M'` uses a selected-union edge at a vertex of color `s`,
that edge is the unique selected edge at port `(v,s)` and hence is the
`M`-edge there.  It is shared and does not lie in the symmetric difference.
Consequently every `M' setminus M` edge on every alternating cycle is
outside the selected union.  This proves the theorem.

## Consequences and the inverse-expansion boundary

1. Any support consisting of only three selected constant matching
   monomials is impossible uniformly for `n>=6`.  This includes the
   one-factor and disjoint near-one-factor diagonal gadgets.
2. More generally, every choice of one nonzero constant monomial per color
   forces an additional same-fiber occurrence and an alternating
   cancellation cycle.  This is the arbitrary-local-map bridge: the extra
   occurrence may be off-diagonal and need not lie on a selected underlying
   edge.
3. If a proposed vertex substitution has a *clean outer cofactor*--the
   outside restriction of the induced coloring has a unique nonzero
   matching--and its odd gadget has the singleton near-perfect fiber from
   the preceding note, their product is a globally singleton mixed fiber
   and is impossible.  In particular this rules out substituting such a
   finite gadget into a unique-monomial outer one-factor construction.

There is a stronger localization when the interface is tight.  Let `L` be
an odd gadget shore and suppose its cut is tight, so every perfect matching
uses exactly one boundary edge.  Assume the three boundary states are
coordinate-separated: state `r` uses one nonzero boundary occurrence
`b_r`, and the selected constant matching factors as

\[
                    P_r\;b_r\;R_r,                         \tag{3}
\]

where `P_r` is internal and exposes the state-`r` terminal and `R_r` is an
outside near-perfect matching.  In the constant color-`r` coefficient,
tightness and coordinate separation give a product of the total internal
near-perfect amplitude, `b_r`, and the total outside cofactor.  Since that
coefficient is one, the outside cofactor is nonzero.

Now use the odd-gadget theorem to obtain a mixed selected near-perfect
matching `Q` exposing state `r`, and fix its internal vertex coloring `d`.
Let `g_d` be the *total* internal amplitude of that near-perfect fiber,
including all extra gadget entries.  Extend `d` by constant color `r` on
the outside.  Tightness again factors the resulting global mixed
coefficient as

\[
              g_d\,b_r\,(
                  \text{nonzero outside color-`r` cofactor}). \tag{4}
\]

It must vanish, so `g_d=0`.  Thus the selected monomial `Q` has a
cancellation mate **inside the gadget**.  In particular a selected-only
tight gadget is impossible even when the outer constant fiber has many
terms; uniqueness of the outer monomial is unnecessary.  More generally,
a tight arbitrary-matrix gadget must already contain the extra occurrence
cycle locally.  If all its mixed internal amplitudes vanish and its three
pure amplitudes are nonzero, its boundary signature is precisely a scaled
three-state equality signature and it can be collapsed to one vertex.  This
is the occurrence-level version of the tight-cut collapse.

The theorem alone does not give an unconditional inverse vertex expansion.
For a non-tight cut the cancellation mate `M'` may use extra entries in the
outer piece or may cross the gadget boundary three times, so (4) no longer
factorizes.  Thus the exact dichotomy is: a tight coordinate interface
localizes the mate and reduces to an equality-signature collapse, whereas
every surviving non-tight expansion must exploit a three-crossing term or
an extra same-coloring cancellation cycle across its interface.
