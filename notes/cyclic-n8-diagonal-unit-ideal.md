# The cyclic eight-site chart has no diagonal three-colour point

This note gives an exact nonlinear counterguard for a natural high-symmetry
counterexample search.  It also records why a linear/Fourier attack cannot
exclude the corresponding unrestricted cyclic chart.  Neither statement is
an obstruction to arbitrary endpoint-colour matrices without vertex
symmetry.

## 1. The unrestricted cyclic chart has no linear separator

Label the sites by `Z/8`.  Choose arbitrary matrices

\[
 C_1,C_2,C_3\in\operatorname {Mat}_{3\times3}(\mathbb C)
 \quad\hbox {and}\quad C_4=C_4^T.
\]

For `u<v`, put `C_(v-u)` on `uv` when `v-u<=4`, and put
`C_(8-v+u)^T` there when `v-u>4`.  This is precisely the general
`Z/8`-translation-invariant endpoint-colour source: it has
`3*9+6=33` parameters, including every cyclic distance and all off-diagonal
endpoint-colour cells.

Rotation makes the coefficient polynomials constant on word necklaces.
Burnside gives

\[
 \frac{3^8+4\cdot3+2\cdot3^2+3^4}{8}=834                 \tag{1}
\]

necklaces.  Expanding all 105 perfect matchings produces 26,370 distinct
degree-four parameter monomials.  Sparse elimination over
`F_1000003` gives rank 834 for the 834 coefficient-polynomial rows.  Since a
nonzero minor modulo a prime is a nonzero integer minor, the rank over
`Q` is also 834.

Thus the linear span of fourth powers in the 33-parameter chart is the
entire 834-dimensional cyclic output space.  In particular no linear
functional of output coefficients, Fourier transformed or otherwise, can
separate this chart from `Delta_3`.  Any exact obstruction to the full
cyclic chart must be nonlinear.

## 2. The colour-diagonal specialization

Now specialize, without imposing nonzero, real, or sign assumptions, to

\[
 C_d=\operatorname {diag}(a_d,b_d,c_d),\qquad 1\le d\le4. \tag{2}
\]

These are twelve arbitrary complex parameters.  For a word
`w in {0,1,2}^8`, a matching contributes only if both endpoints of each edge
have the same letter.  Equivalently, if `S_r=w^{-1}(r)` and `H_r(S)` is the
hafnian of the distance-weighted cyclic graph of colour `r` induced on `S`,
then

\[
 [e_w]q^{[4]}=H_0(S_0)H_1(S_1)H_2(S_2).                \tag{3}
\]

This identity includes every cancellation among matchings.  The target
conditions are that (3) is one on the three constant words and zero on every
mixed word.  After cyclic word reduction there are 150 distinct nonzero
polynomial residuals.

Only 39 of them are needed.  Take every colour permutation of the following
eleven words and delete duplicate polynomials caused by rotations:

```text
00000000   00001111   00001221   00012012
00012021   00101101   00110011   00110022
00120012   00120021   01010202
```

The first family supplies the three equations `H_r(V)-1`; the other ten
families supply mixed coefficient equations.  Let `I` be their ideal in

\[
 \mathbb Q[a_1,a_2,a_3,a_4,b_1,b_2,b_3,b_4,c_1,c_2,c_3,c_4]. \tag{4}
\]

Exact degree-reverse-lexicographic Groebner reduction gives

```text
size(I) = 39
size(slimgb(I)) = 1
slimgb(I)[1] = 1
```

Therefore `I=(1)`.  The selected target equations have no common zero over
`C`, proving the following scoped lemma.

**Lemma.**  No colour-diagonal, `Z/8`-translation-invariant quadratic source
has fourth divided power `Delta_3`.

No normalization was used: zero entries and arbitrary complex weights are
included.  The result is genuinely nonlinear; Section 1 shows that a linear
coefficient identity cannot prove even the larger cyclic statement.

## 3. Exact audit and relation to earlier slices

Run

```sh
.venv/bin/python computations/verify_cyclic_n8_diagonal_no_go.py
```

The checker reconstructs the 105 matchings and all 834 necklaces, verifies
the unrestricted rank over the prime field, reconstructs all 150 diagonal
residuals, verifies that the displayed 39 are genuine coefficient equations,
and asks Singular to recompute the Groebner basis over `Q`.  Its terminal
line is

```text
PASS: exact linear-span audit and exact diagonal no-go
```

This does not duplicate the Fourier obstruction in
[`n8-counterexample-recon.md`](n8-counterexample-recon.md): that result
assumes every edge matrix is colour-circulant but permits arbitrary vertex
dependence, whereas (2) assumes vertex translation invariance and permits
three unrelated diagonal entries.  It also strictly goes beyond the
`{0,+1,-1}` diagonal slice in
[`diagonal-mod2-route.md`](diagonal-mod2-route.md), because the twelve
parameters here are arbitrary complex numbers.  Conversely, it says nothing
about the off-diagonal cells in the full 33-parameter cyclic chart or about
the unrestricted Krenn fibre.
