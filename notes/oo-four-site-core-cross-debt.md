# A four-site zero-Fitting core has an exact crossed-debt boundary

## Outcome

Fix a four-plus-four site cut `S|T`.  Let `U,V,W` be the three perfect
matching monomials on `S`, with their literal endpoint colours, and let
`H_T` be the three-term hafnian on `T`.  Every eight-site coefficient
decomposes uniquely by the number of edges crossing the cut:

\[
 P_w=(U_w+V_w+W_w)H_{T,w}+C_{2,w}+C_{4,w}.             \tag{1}
\]

Here `C_2` contains the 72 matchings with two crossing edges and `C_4`
contains the 24 matchings with four crossing edges.  More structurally,
`C_2` is the sum of 36 internal-edge factors times two-by-two cross
permanents, while `C_4` is the four-by-four cross permanent.

If the spectator-factorization theorem supplies the localized
zero-Fitting relation

\[
                         U_w+V_w=0,                    \tag{2}
\]

then the complete physical row is exactly

\[
 P_w=W_wH_{T,w}+C_{2,w}+C_{4,w}.                       \tag{3}
\]

Thus the absent third `K4` route is not an unspecified contamination.  Its
entire obstruction is the literal two-cross/four-cross debt.  For a source
row `F_w=P_w-\delta_w`, equation (3) becomes

\[
 W_wH_{T,w}=\delta_w-C_{2,w}-C_{4,w}.                  \tag{4}
\]

This is the exact interface that a complete full-output/four-cut comparison
or clean-cap theorem must control.  The top row supplies (1); additional
pair-labelled full-nine data would be needed to control its crossed debt.

This physical decomposition is not by itself a Schur-complement formula.
It has the same `0/2/4` sector grading as the four-boundary specialization
of [`product-cap-monomer-reduction.md`](product-cap-monomer-reduction.md),
but the notation must be kept straight: the boundary tensor `C_2` enters
the top coefficient as `[xC_2]_4`, where `x` is the internal quadratic on
the right shore.  The 72-term sector above is `[xC_2]_4`, not `C_2` alone.
The zero-Fitting spectator factorization supplies a canonical route into
the physical `0/2/4` boundary, but it supplies no factorization of `C_2`.

## 1. The `9+72+24` decomposition

An eight-site perfect matching crosses an equal four-site cut in an even
number of edges.

* With zero crossing edges, choose one of three matchings independently on
  each shore: `3*3=9`.
* With two crossing edges, choose the internal edge on each shore and one
  of the two bijections between the remaining vertices: `6*6*2=72`.
* With four crossing edges, choose a bijection between the shores: `4!=24`.

These sectors are disjoint and exhaust all `105` perfect matchings.  The
checker repeats the identity after decorating every edge by its endpoint
colours, for all `3^8=6561` output words.  Consequently (1) is a literal
source-coefficient identity, not an uncoloured support statement.

## 2. Relation to the zero-Fitting source switch

The spectator-factorization theorem says that a two-row zero determinant
`AD=BC` has the form

\[
 (A,B)=G(U,V),\qquad (C,D)=H(U,V).
\]

After active localization, both rows give (2).  Multiplying this physical
relation by `H_T` removes six of the nine uncrossed terms in (1).  What
remains is precisely the third core route `W H_T` and the crossed debt in
(3).  No term order or private-matching hypothesis enters this reduction.

On a mixed output word, `delta_w=0`, so the crossed ledger must cancel the
third route.  On a pure anchor, `delta_w=1`, so the same ledger is a
potential ordinary unit or clean-cap connector.  This explains why pure
anchors and crossed rows must be used together: neither the zero-Fitting
block nor the pure row alone controls (4).

In the notation of the product-cap monomer formula, write the boundary
signature as

\[
 C_0=h=U+V+W,\qquad C_2=Q,\qquad C_4.
\]

Then the physical top row is

\[
       hH_T(x)+[xQ]_T+C_4,                                \tag{5}
\]

so its first two terms are precisely the 9- and 72-term sectors.  On an
active `h != 0` chart, pair conversion replaces `x` by `x+Q/h`; the
effective pair update is `L_2=Q/h`, and its first non-pairwise cumulant is

\[
 L_4={C_4\over h}-{1\over2}\left({Q\over h}\right)^2,
 \qquad
 h^2L_4=hC_4-Q^{[2]}.                                  \tag{6}
\]

Thus the obstruction to reconstructing the `72+24` debt from its pairwise
sector is the fourth cumulant (6).  The physical top debt itself remains
`[xQ]_T+C_4`; equation (6) is its canonical non-pairwise residue, not an
identification of those expressions.

The following compact eighteen-term expansion requires an additional
factorized four-star signature.  Namely, assume that for four boundary
forms `L_0,...,L_3` the six entries of `Q` are

\[
 a_{23}L_0L_1,\ a_{13}L_0L_2,\ a_{12}L_0L_3,\
 a_{03}L_1L_2,\ a_{02}L_1L_3,\ a_{01}L_2L_3,
                                                               \tag{7}
\]

and `C_4=L_0L_1L_2L_3`.  Under (7), all four-cross factors use the same
four boundary forms.  This hypothesis is valid in the formal permanent-null
one-bad specialization below.  It is **not** implied by the arbitrary
physical cut decomposition (1), by the zero-Fitting relation (2), or by
the spectator-factorization theorem.

Expanding (6) under (7) gives an especially small exact ledger.  The three
complementary products are exactly `h C_4` and cancel.  The
remaining divided square has eighteen terms, all with coefficient `-2` in
`hC_4-Q^[2]`: six contain two factors `L_i^[2]L_j^[2]`, and twelve contain
one repeated-endpoint factor `L_i^[2]`.  Therefore

\[
 h^2L_4\in (L_0^{[2]},L_1^{[2]},L_2^{[2]},L_3^{[2]}).  \tag{8}
\]

Conditional equation (8) is the precise interface with the square-zero one-bad
landing theorem: that theorem kills all four generators of this ideal,
whereas an arbitrary multisite packet may cancel their eighteen-term sum
without killing the generators separately.

There is a sharper relationship with the exact binary one-bad cap.  Put

\[
 (L_0,L_1,L_2,L_3)=(p_0,p_1,s_0,s_1)
\]

and specialize the six internal coefficients in (7) to

\[
 a_{23}=a_{01}=0,\quad a_{13}=a_{12}=a_{02}=1,
 \quad a_{03}=-1.                                         \tag{9}
\]

Then

\[
 Q=p_0s_0+p_0s_1-p_1s_0+p_1s_1,
 \qquad
 h=a_{01}a_{23}+a_{02}a_{13}+a_{03}a_{12}=0.      \tag{10}
\]

Thus the matrix of `Q` is exactly the permanent-null one-bad matrix
`[[1,1],[-1,1]]`, and (6) specializes without division to

\[
        (hC_4-Q^{[2]})\big|_{(9)}=-Q^{[2]}.          \tag{11}
\]

The eighteen generic repeated-endpoint terms collapse under (9) to the eight
already-audited one-bad defect sectors: four same-entry sectors, two
repeated-row sectors, and two repeated-column sectors.  In particular, the
multisite one-bad defect is not merely analogous to the four-core debt; it
is its exact permanent-zero boundary.

The checker establishes this twice.  Besides specializing the eighteen-term
formula, it imports the independently committed raw row/column-provenance
census in
[`verify_n8_multisite_permanent_null_repeated_defect.py`](../computations/verify_n8_multisite_permanent_null_repeated_defect.py),
pins that file by SHA-256, converts its raw products into divided-power
normalization, and obtains the same eight coefficients.  This guards both
the signs and the factors of two in (8).

Within the factorized subclass (7), this marks a necessary distinction.
The `h!=0` route uses the normalized cumulant `L_4`; the permanent-null
one-bad route lies on `h=0`, where `L_4` itself is unavailable and only its
polynomial numerator survives.  The two strata share the polynomial (6)
inside that subclass, but they are not the same open packet.

## 3. Zero Fitting does not imply the factorized signature

The checker freezes a dense scalar physical counterguard.  On the four
core sites take

\[
 a_{01}=a_{23}=a_{02}=1,\quad a_{13}=-1,\quad
 a_{03}=2,\quad a_{12}=3.
\]

The three core matching products are `(U,V,W)=(1,-1,6)`, so the exact
zero-Fitting relation `U+V=0` holds and `h=6`.  Take the ordinary cross-edge
matrix

\[
 B=\begin{pmatrix}
 1&2&1&3\\2&1&3&1\\1&3&2&4\\3&1&4&2
 \end{pmatrix}.
\]

Literal matching expansion gives

\[
 (Q_{01},Q_{02},Q_{03},Q_{12},Q_{13},Q_{23})
       =(50,64,72,70,36,100),\qquad C_4=496,
\]

and therefore

\[
                     hC_4-Q^{[2]}=-9368.                 \tag{12}
\]

If (7) held with these same core coefficients, the three quantities

\[
 {Q_{01}Q_{23}\over a_{23}a_{01}},\qquad
 {Q_{02}Q_{13}\over a_{13}a_{02}},\qquad
 {Q_{03}Q_{12}\over a_{12}a_{03}}
\]

would all equal `L_0L_1L_2L_3`.  All three pairwise equalities fail by
cross multiplication.  Hence a literal zero-Fitting four-core does not
land in the four-star ansatz, even with every cross entry nonzero.

This counterguard does not invalidate the general cumulant identity (6):
`Q` and `C_4` are always the genuine boundary tensors.  It invalidates the
unconditional use of the eighteen-term self-square expansion and the claim
that spectator factorization alone identifies the OO crossed debt with the
formal permanent-null one-bad packet.

## 4. What is still missing

Equation (4) does not prove that the crossed debt vanishes, factors through
a lower source, or supplies an active clean cap.  In particular, the known
equal-word `C4 x C4` square may close with even holonomy before the complete
crossed ledger is imposed.

The remaining theorem is therefore not another expansion identity.  It
must either derive the factorized signature (7) from additional physical
rank-one/full-nine hypotheses, or work directly with the general boundary
tensors `Q,C_4`.  Only after that step is it meaningful to compare a
terminal crossed-debt charge with the numerator (6).  Neither the
zero-Fitting relation nor cumulant algebra supplies the source-labelled
comparison.

This does **not** also solve the rootless `n_A` attaching problem.  Every
monomial in (6) is made solely from physical cell coefficients; it has
zero incidence under the conormal functional that extracts the homogenizing
target variable `u`.  The missing `n_A` chain must cancel a nonzero
`kappa[F_0]` class in that conormal degree.  Thus the fourth-cumulant theorem
can feed the clean-cap/one-bad route, but a separate word-changing source
comparison is still required in the rootless two-chart route.

The proof-completing next lemma can now be stated finitely and
source-provenantly:

> For every active curved doubly-good overlap whose critical zero-Fitting
> block has a four-site core, the literal `[xQ]_T+C_4` ledger in (4) either
> supplies the missing two core-pair routes (hence the determinant-two
> hafnian triangle), produces an ordinary unit/active clean cap through a
> pure anchor, or descends to a strictly smaller exact source packet.

Six- and eight-site alternating cores remain separate residual cases, but
the smallest zero-Fitting SCC is no longer a global 105-matching problem:
it is the explicit 72-plus-24 crossed-debt module.

## Verification

Run

```text
.venv/bin/python computations/verify_oo_four_site_core_cross_debt.py
.venv/bin/python -O computations/verify_oo_four_site_core_cross_debt.py
```

The checker enumerates all 105 `K8` perfect matchings, reconstructs the
`9/72/24` sectors from the cut formula, retains literal endpoint colours,
and verifies (1)--(3) for all 6,561 words.  It separately audits the
conditional factorized four-star formula and the permanent-null
specialization, then reconstructs the dense physical counterguard (12) and
checks all three failed factorization equalities.
