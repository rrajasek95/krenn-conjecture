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

This decomposition is not a new Schur-complement formula.  It is the
four-boundary specialization of
[`product-cap-monomer-reduction.md`](product-cap-monomer-reduction.md).  The
new point here is that the zero-Fitting spectator factorization supplies a
canonical route into that already-audited cap boundary.

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

In the notation of the product-cap monomer formula, write

\[
 C_0=h=U+V+W,qquad C_2=Q,qquad C_4=L_1L_2L_3L_4.
\]

The effective pair update is `L_2=Q/h`, and its first non-pairwise
cumulant is

\[
 L_4={C_4\over h}-{1\over2}\left({Q\over h}\right)^2,
 \qquad
 h^2L_4=hC_4-Q^{[2]}.                                  \tag{5}
\]

Thus the obstruction to reconstructing the `72+24` debt from its pairwise
sector is precisely the repeated-endpoint/fourth-cumulant defect already
known to obstruct arbitrary multisite hafnian Schur descent.  The physical
debt itself remains `C_2+C_4`; equation (5) is its canonical non-pairwise
residue, not an identification of those two expressions.  When all four
cross-star linear forms are square-zero, the repeated-endpoint terms vanish
and (5) is zero; without that hypothesis the product-cap counterguards show
that no local Schur argument can eliminate it.

Expanding (5) gives an especially small exact ledger.  Write the six terms
of `Q` as

\[
 a_{23}L_0L_1, a_{13}L_0L_2, a_{12}L_0L_3,
 a_{03}L_1L_2, a_{02}L_1L_3, a_{01}L_2L_3.
\]

The three complementary products are exactly `h C_4` and cancel.  The
remaining divided square has eighteen terms, all with coefficient `-2` in
`hC_4-Q^[2]`: six contain two factors `L_i^[2]L_j^[2]`, and twelve contain
one repeated-endpoint factor `L_i^[2]`.  Therefore

\[
 h^2L_4\in (L_0^{[2]},L_1^{[2]},L_2^{[2]},L_3^{[2]}).  \tag{6}
\]

Equation (6) is the precise common interface with the square-zero one-bad
landing theorem: that theorem kills all four generators of this ideal,
whereas an arbitrary multisite packet may cancel their eighteen-term sum
without killing the generators separately.

There is a sharper relationship with the exact binary one-bad cap.  Put

\[
 (L_0,L_1,L_2,L_3)=(p_0,p_1,s_0,s_1)
\]

and specialize the six internal coefficients to

\[
 a_{23}=a_{01}=0,\quad a_{13}=a_{12}=a_{02}=1,
 \quad a_{03}=-1.
\]

Then

\[
 Q=p_0s_0+p_0s_1-p_1s_0+p_1s_1,
 \qquad
 h=a_{01}a_{23}+a_{02}a_{13}+a_{03}a_{12}=0.       \tag{7}
\]

Thus the matrix of `Q` is exactly the permanent-null one-bad matrix
`[[1,1],[-1,1]]`, and (5) specializes without division to

\[
        (hC_4-Q^{[2]})\big|_{(7)}=-Q^{[2]}.           \tag{8}
\]

The eighteen generic repeated-endpoint terms collapse in (8) to the eight
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

This also marks a necessary distinction.  The curved-OO route uses the
normalized cumulant `L_4` on an active `h != 0` chart.  The permanent-null
one-bad route lies on `h=0`, where `L_4` itself is unavailable and only its
polynomial numerator survives.  The two proof gates therefore share one
source polynomial, but they are not the same open stratum.  A closing
argument must either keep `h != 0` and control `L_4`, or remain on `h=0`
and force the eight sectors in `Q^[2]` to vanish or descend.

## 3. What is still missing

Equation (4) does not prove that the crossed debt vanishes, factors through
a lower source, or supplies an active clean cap.  In particular, the known
equal-word `C4 x C4` square may close with even holonomy before the complete
crossed ledger is imposed.

The remaining theorem is therefore not another expansion identity: it must
first compare the terminal physical crossed-debt class with the polynomial
numerator in (5), using common-source/full-nine provenance, and then
annihilate or transport the resulting class.  The curved-OO and arbitrary
multisite one-bad frontiers share that numerator, respectively on its
`h != 0` and `h=0` strata; the source-labelled comparison is not supplied by
the cumulant algebra alone.

This does **not** also solve the rootless `n_A` attaching problem.  Every
monomial in (5)--(6) is made solely from physical cell coefficients; it has
zero incidence under the conormal functional that extracts the homogenizing
target variable `u`.  The missing `n_A` chain must cancel a nonzero
`kappa[F_0]` class in that conormal degree.  Thus the fourth-cumulant theorem
can feed the clean-cap/one-bad route, but a separate word-changing source
comparison is still required in the rootless two-chart route.

The proof-completing next lemma can now be stated finitely and
source-provenantly:

> For every active curved doubly-good overlap whose critical zero-Fitting
> block has a four-site core, the literal `C_2+C_4` ledger in (4) either
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
and verifies (1)--(3) for all 6,561 words.
