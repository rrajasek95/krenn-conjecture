# A Hall star forces two active crossed debts or an anchor triangle

## Result

Consider the arbitrary-multisite one-bad packet

\[
 q^{[h]}=X_0,\qquad
 p_i s_jq^{[h-1]}=\delta_{ij}X_i
 \quad(i,j\in\{1,2\}).
\]

Assume the two pure diagonal hole families are in the strict Hall-star
normal form: every live pure target monomial has a hole edge through one
common residual centre `c`.  Split each pure diagonal coefficient according
to whether `P` or `S` occupies `c`.

There is an exact dichotomy.

1. If the two colours have a common nonzero centre side, both crossed zero
   rows force nonempty sets of off-centre, off-diagonal, cofactor-active
   endpoint cells.  If the two ordered active sets use different physical
   sites, they are the distinct-head four-good wedge already closed by the
   five-lock theorem.
2. If the effective centre-side sets are disjoint, each is a singleton and
   they are opposite.  The selected unary and diagonal matchings then
   contain the literal three-colour triangle

   ```text
   P-S : colour 0,    P-c : colour 1,    S-c : colour 2
   ```

Thus the star family is reduced, without a support census, to two sharp
normal forms:

\[
 \boxed{\text{one co-located bidirectional off-diagonal lock}}
 \quad\text{or}\quad
 \boxed{\text{the outer-centre three-colour anchor triangle}.}
\]

The checker is
`computations/verify_uniform_multisite_hall_star_source_reduction.py`.

## The aggregate crossed identities

Suppose first that `P` is an effective centre side for both colours.  Write

```text
a_i = p_i(c,i),
U_i = the complete pure-i coefficient of s_i q^[h-1] after fixing c.
```

The `P`-oriented contribution to the diagonal target is `a_i U_i`.
**Effectiveness means that this aggregate contribution is nonzero**, not
merely that one of its matching terms is supported.  Since the coefficient
domain is integral, both `a_i` and `U_i` are then nonzero.  In the crossed word which is
colour `i` at `c` and colour `j` everywhere else, expansion by the site of
the `p_i` cell is exactly

\[
 0=a_iU_j+\sum_{u\ne c}p_i(u,j)C^{ij}_u.              \tag{1}
\]

Here `C^{ij}_u` is the **complete** remaining `s_j q^[h-1]` cofactor in
that word.  It includes arbitrary multisite support and every internal
matching; no termwise uniqueness is assumed.  Since `a_iU_j` is nonzero,
(1) proves that some literal product

\[
                 p_i(u,j)C^{ij}_u\ne0.                \tag{2}

Applying (1) for `(i,j)=(1,2)` and `(2,1)` gives two nonempty active-site
sets.  The same proof holds with `P` and `S` interchanged.

On the pure-side chart, the statement has the ordinary source-polynomial
form

\[
\begin{aligned}
 a_2g_{12}-a_1g_{22}
   &=a_1+a_2\sum_up_1(u,2)C^{12}_u,\\
 a_1g_{21}-a_2g_{11}
   &=a_2+a_1\sum_up_2(u,1)C^{21}_u.                   \tag{3}
\end{aligned}
\]

The checker expands (3) over `Z`; localization is used only to infer
nonvanishing from the already selected target contributions.

## Why distinct carrier sites are four-good

The normalized unary target matching uses the direct edge `P-S`.  On the
common-`P` star chart, the selected colour-one and colour-two matchings both
use `P-c`.  Therefore every off-centre pair `P-u` in (2) is absent from all
three selected pure matchings.

Reselecting `P-u` as a physical pair leaves one coordinate column from each
pure matching at each endpoint.  More explicitly, at either endpoint the
three undeleted columns have labels

\[
 (\operatorname{neighbour}_0,0),\quad
 (\operatorname{neighbour}_1,1),\quad
 (\operatorname{neighbour}_2,2).
\]

They are independent because their colour labels are distinct, even if
some physical neighbours coincide.  Thus both deleted stars have rank
three for **every** off-anchor `P-u`, not only for the checker normalization.
If (2) for `12` occurs at `u` and (2) for
`21` occurs at `v!=u`, the two good pairs `P-u,P-v` share `P`, have heads
`e_1,e_2`, and retain their nonzero cofactors.  This is precisely the
source-valid distinct-head four-good wedge: no coefficient is changed, so
the landing is automatically anchor-safe.

For two nonempty active-site sets `A12,A21`, either they admit representatives
`u!=v`, or every cross-pair is equal; the latter immediately forces both
sets to be the same singleton.  Hence the only way this argument misses the wedge is

```text
supp(active 12 debt) = supp(active 21 debt) = {u}.
```

Then one off-anchor block `P-u` carries both ordered off-diagonal debts.
The crossed identities genuinely permit this: the checker gives the exact
scalar solution `a1=a2=U1=U2=1`, with both active products `-1` at the same
site.  The residual is therefore a co-located alternating-C4 lock, not a
missing Hall selection.

## The opposite-side residual

For each colour the nonzero effective side set is a nonempty subset of
`{P,S}`.  If the two sets do not meet, they must be the opposite singletons
`{P},{S}`.  Choose a nonzero monomial from each effective diagonal
contribution.  Together with the unary direct anchor, their physical edges
at the common centre are

```text
P-S, P-c, S-c.
```

The corresponding colours are `0,1,2`.  In this orientation the obvious
crossed product at `c` is site-square-zero, so neither crossed row has the
nonzero centre pivot from (1).  This explains exactly why the source-row
argument stops: the residual is a selected-anchor triangle, and closing it
requires a triangle exchange/line-hitting identity rather than another
star-family selection.

## Scope

This result uses the genuine unary selected matching, both diagonal target
rows, both crossed zero rows, and arbitrary complete cofactors.  It is not a
full one-bad counterexample and it does not claim affine line-hitting in the
two displayed residual normal forms.  It closes every strict Hall-star
packet with two distinct active debt sites by the existing four-good
theorem; the co-located lock and outer-centre triangle are the exact next
source obligations.  Triangle and `K2,2` hole-family types remain separate.

Run

```text
python3 computations/verify_uniform_multisite_hall_star_source_reduction.py
python3 -O computations/verify_uniform_multisite_hall_star_source_reduction.py
python3 -I -S computations/verify_uniform_multisite_hall_star_source_reduction.py
```

Frozen ledger SHA-256:

```text
bc484624f80803e7df024c0a727128d79c8516aebde56fec8eca5ae3e802b4f7
```
