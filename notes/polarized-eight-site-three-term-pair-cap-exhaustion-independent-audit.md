# Independent audit: the eight-site three-term pair-cap exhaustion

## 1. Verdict

The finite theorem in
[the primary note](polarized-eight-site-three-term-pair-cap-exhaustion.md)
passes a clean-room reconstruction.  After normalizing the flagged
colour-zero matching, all \(420^2=176{,}400\) ordered choices for colours
one and two were scanned.  Exactly \(9{,}888\) supports have precisely the
three required decorated matching terms in \(zq^{[3]}\).  Every one gives a
sound two-dimensional Gram contradiction:

\[
 7{,}968\text{ by the short seven-entry pattern},\qquad
 1{,}920\text{ by the general closure only}.
\]

No flaw was found.  The independent checker is
[verify_polarized_eight_site_three_term_pair_cap_exhaustion_independent_audit.py](../computations/verify_polarized_eight_site_three_term_pair_cap_exhaustion_independent_audit.py).
It uses only the Python standard library and neither imports nor reads either
primary computational module.

The audit also proves a support-level strengthening: the exclusion remains
valid when the nine retained \(q\)-cells have arbitrary nonzero complex
weights and the three \(z\)-cells have the weights required by
\(zq^{[3]}=\Delta_{8,3}\).  Unit representatives enumerate the supports,
but the Gram obstruction is weight-uniform on each retained support.

This remains the finite same-colour, exactly-three-decorated-term class.  It
is not a Krenn counterexample or a proof of Krenn's conjecture.

## 2. Matching enumeration and normalization

Rather than use the primary recursive generator, the audit filters all
\(\binom{28}{4}=20{,}475\) four-edge subsets of \(K_8\) for disjoint
endpoint sets.  It obtains exactly \(105\) perfect matchings and therefore
\(4\cdot105=420\) flagged matchings \((P,d)\).

The normalization of the first flag loses no cases.  Applying all \(8!\)
site permutations to

\[
 P_0=01\mid23\mid45\mid67,\qquad d_0=01
\]

produces the full set of \(420\) flags.  Equivalently, the stabilizer has
size

\[
 2\cdot3!\cdot2^3=96,\qquad {8!\over96}=420.
\]

A physical-site relabelling preserves both the polarized identity and the
existence of \(z=aq+4ps\).  Thus the first colour may be fixed, while the
two remaining labelled colours contribute the ordered \(420^2\) cases.

For each case, the audit builds the nine \(q\)-cells literally.  For each
distinguished \(z\)-edge, it tests all \(\binom93=84\) triples of
\(q\)-cells and retains those whose physical endpoints are the six
complementary sites.  A support is accepted only when that list has length
one and all three cells have the distinguished edge's colour.  This yields
exactly \(9{,}888\) supports.

The clean-room ordering reproduces the primary certificate-ledger SHA-256:

    5f42b78f2f972ed25a96f6ea01a25dcaf2b1c108174ba0fe2d0804132dddb639

An independent ledger additionally records every forced-zero graph and
selected projective certificate:

    20e054d75b6dd11d1dd219fe4677242ab17f6dd1cac0860457eda6f93788b36f

## 3. Coefficient and Gram reconstruction

For each accepted support, the audit reconstructs every site-multilinear
coefficient of

\[
 F=q^{[3]},\qquad Q=q^{[4]}.
\]

A triple of pairwise-disjoint \(q\)-cells leaves two physical sites.
Assigning all nine ordered colour pairs to those sites gives the complete
ledger of possible \(psF\) contributors.  Four pairwise-disjoint
\(q\)-cells give the separate \(Q\)-ledger.

For modes \(X,Y\), write

\[
 R_{XY}=p_Xs_Y+s_Xp_Y=\beta(x_X,x_Y),\qquad
 x_X=(p_X,s_X),
\]

where

\[
 \beta((r,u),(s,v))=rv+us.
\]

If \(z=aq+4ps\), then \(qF=4Q\) gives

\[
                       aQ+psF={1\over4}\Delta_{8,3}.      \tag{1}
\]

For every accepted support and every colour \(c\), the pure word \(c^8\)
has exactly one \(F\)-contributor.  Its leftover modes are the endpoints of
\(d_c\), and \(Q\) has no such word.  Thus the three distinguished Gram
pairs are nonzero.

For a mixed word, the audit marks a Gram edge zero only if the word has
exactly one \(F\)-contributor and its \(Q\)-coefficient is
support-theoretically absent.  It does not use any word having two possible
contributors, infer that an unmarked edge is nonzero, or assume
cancellation.

The six-vertex zero graphs have the exact distribution

\[
\begin{array}{c|rrrrr}
\#\text{ zero edges}&6&7&8&9&10\\ \hline
\#\text{ supports}&96&288&3456&4896&1152.
\end{array}
\]

## 4. A distinct exact closure test

For a nonzero vector \(x\), let \(L_x\) be its projective line and put

\[
                         \tau(L)=L^\perp.
\]

Nondegeneracy and symmetry of \(\beta\) imply \(\tau^2=1\).  A zero edge
\(XY\) says \(L_Y=\tau(L_X)\).  Consequently:

1. an odd zero path joins orthogonal endpoint lines;
2. an odd zero cycle forces \(L=\tau(L)\), hence an isotropic line;
3. every vertex in that cycle's connected component then lies on the same
   isotropic line.

The checker decomposes each zero graph into connected components and tests
bipartiteness.  It returns one of two literal certificates.

- An odd-path certificate joins a required-nonzero pair by an odd zero
  path.
- An isotropic-component certificate records a simple odd cycle and zero
  paths from it to both endpoints of a required-nonzero pair.

Every path and cycle is replayed edge by edge.  These rules cannot create a
false contradiction: they use only forced zero edges, their vertices are
known nonzero, and the final conflicting pair is independently required
nonzero.  No inference is made between disconnected components.

The short certificate searches the labelled pattern with required pairs
\(AB,CD,EF\) and zeros

\[
                         AF=BF=AC=CF=0.
\]

It occurs in \(7{,}968\) supports.  The remaining \(1{,}920\) supports all
close under the projective test: \(96\) have an odd-path certificate and
\(1{,}824\) have an isotropic-component certificate.  There are no
survivors.

## 5. Why arbitrary nonzero weights are covered

Assign a nonzero formal weight \(t_e\) to each retained \(q\)-cell.  Every
coefficient equation used above has exactly one \(F\)-contributor, whose
coefficient is

\[
                         \mu=t_{e_1}t_{e_2}t_{e_3}\ne0.
\]

For a pure word, (1) gives

\[
                         \mu R_{d_c}={1\over4},
\]

so \(R_{d_c}\ne0\).  For a selected mixed word, \(Q\) is absent and (1)
gives \(\mu R_{XY}=0\), so \(R_{XY}=0\).  The unit and weighted models
therefore have exactly the same nonzero pairs and forced-zero graph.

Given arbitrary nonzero \(q\)-weights, the three pure decorated terms are
normalized by choosing each \(z\)-weight as the inverse of the corresponding
triple product.

This strengthening does not allow a retained weight to vanish without
changing the support.  It also does not cover additional decorated terms
whose coefficients cancel, extra or endpoint-asymmetric cells, or a
quadratic outside the enumerated same-colour form.

## 6. Reproduction

Run

    .venv/bin/python computations/verify_polarized_eight_site_three_term_pair_cap_exhaustion_independent_audit.py

The checker reports:

    independent eight-site three-term pair-cap audit: PASS
    C(28,4) gives 105 matchings and 420 flagged matchings: PASS
    S_8 orbit of the normalized first flag has size 420: PASS
    all 176400 normalized flagged pairs scanned: PASS
    9888 exact three-decorated-term supports: PASS
    7968 short-pattern + 1920 closure-only contradictions: PASS
    closure-only certificate kinds: {'isotropic_component': 1824, 'odd_zero_path': 96}
    zero-edge histogram: {6: 96, 7: 288, 8: 3456, 9: 4896, 10: 1152}
    published ledger SHA-256: 5f42b78f2f972ed25a96f6ea01a25dcaf2b1c108174ba0fe2d0804132dddb639
    independent ledger SHA-256: 20e054d75b6dd11d1dd219fe4677242ab17f6dd1cac0860457eda6f93788b36f
    all closure certificates replay as literal odd paths/cycles: PASS
    arbitrary nonzero weights on the same exact supports: PASS
