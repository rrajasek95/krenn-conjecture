# The square-zero one-bad packet is a uniform active clean cap

## Uniform local lemma

Let `U` have size `2h`, with `h>=3`, and work in its endpoint-coloured
site-square-zero algebra.  Suppose a selected physical pair has been put in
the exact one-bad normal form

\[
 q^{[h]}=X_0,
 \qquad p_i s_jq^{[h-1]}=\delta_{ij}X_i
 \quad(i,j\in\{1,2\}),                                \tag{1}
\]

with the colour-zero endpoint star rows zero.  Assume

\[
 p_1^{[2]}=p_2^{[2]}=s_1^{[2]}=s_2^{[2]}=0.           \tag{2}
\]

Then the pair has an active clean cap and the source descends exactly from
`2h+2` to `2h` vertices.

For literal star rows, (2) says only that each row is supported at at most
one physical residual site.  The four sites need not be distinct; collisions
kill additional products.  Thus this is slightly weaker than a four-distinct
literal-port hypothesis.

## The explicit cap

Use the cap covector

\[
 K=\begin{pmatrix}
 1&0&0\\
 0&1&1\\
 0&-1&1
 \end{pmatrix}.                                      \tag{3}
\]

The normalized one-bad direct block is `E00`, so

\[
 s(K)=1,
 \qquad (\kappa_0,\kappa_1,\kappa_2)=(1,1,1).         \tag{4}
\]

In particular, `K` is active.  Its effective residual correction is

\[
 R=p_1s_1+p_1s_2-p_2s_1+p_2s_2.                      \tag{5}
\]

The binary block of (3) has permanent `1-1=0`.  The complete repeated-sector
identity from `4df721f` is

\[
 R^{[2]}={1\over2}p_1^2(s_1+s_2)^2
 +p_1p_2(s_2^2-s_1^2)
 +{1\over2}p_2^2(s_2-s_1)^2.                         \tag{6}
\]

Equation (2) makes (6) zero source-coefficientwise.  Therefore every
`R^[k]` with `k>=2` is zero, and for every `h>=3`

\[
 \begin{aligned}
 (q+R)^{[h]}
 &=q^{[h]}+Rq^{[h-1]}\\
 &=X_0+X_1+X_2=\Delta_{2h,3}.                         \tag{7}
 \end{aligned}
\]

This is a literal finite aggregate source on the residual sites.  Equivalently,
the homogeneous cap error of the pinned exact clean-pair theorem vanishes:
every term in that error contains `R^[k]` for `k>=2`.  The theorem then gives
the same finite decorated-source descent, retaining endpoint order and
arbitrary complex weights.

## Minimal-order consequence

If a hypothetical exact ternary source of minimum even order `N=2h+2`
admits the packet (1)--(2), (7) constructs an exact source at order `N-2`.
This contradicts minimality; the bottom order six is already excluded over
arbitrary complex blocks.  Hence (1)--(2) is not merely an `N=8` obstruction:
it is a uniform theorem-completing local clean-cap lemma.

The same proof allows a nonunit direct coefficient.  If the direct block is
`lambda*E00`, replace the `(0,0)` entry of `K` by `lambda^-1`; the direct
scalar remains one and all three target coefficients remain nonzero.  A
one-site diagonal colour rescaling after descent normalizes their values.

## Exact map to `SP-CLEAN-BRIDGE`

The certified spine already supplies a source-provenant, generically active
physical curvature line.  The full-nine/shared-flag reductions supply the
one-bad row shape when their projection-degenerate branch is reached.  The
remaining extraction hypothesis is precisely:

> from the selected active physical line, either produce an active clean cap
> directly, or preserve the pair and its mutual unary anchor while reducing
> the complementary binary endpoint rows to the four self-square identities
> (2).

Once that statement is proved, (3)--(7) discharge `SP-CLEAN-BRIDGE` and the
minimal-order descent.  No further `N=8` matching-support census is needed for
the cap algebra.

What is **not** proved here is that minimum support forces (2).  The exact
response guard in `4df721f` shows why activity matters: a nonzero repeated
sector can be carried by a removable inactive arm.  A minimum-support full
packet must either retract all such sectors or upgrade a coupled survivor to
the already selected active/curved physical geometry.  That is the dashed
active-line-to-active-clean-cap arrow, not a defect in the descent lemma.

## Reproduction

```sh
uv run python computations/verify_uniform_one_bad_square_zero_clean_cap.py
PYTHONOPTIMIZE=1 uv run python computations/verify_uniform_one_bad_square_zero_clean_cap.py
```

The checker verifies the permanent, activity data, universal square-zero
quotient, and dependency hashes for the exact clean-pair descent and six-site
terminal theorem.
