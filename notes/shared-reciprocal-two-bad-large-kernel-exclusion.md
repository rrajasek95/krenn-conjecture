# Large diagonal kernel circuits cannot carry the two bright images

## 1. Result

Continue in the five-site cofactor quotient of
[`the two-bad theorem`](shared-reciprocal-two-bad-cofactor-quotient.md).
Assume that every internal cell has the same colour at its two endpoints.
Write `a,c` for the two bright colours and `t` for the missing target.

> **Large-kernel exclusion.**  If `X_a,X_c` belong to the common-cofactor
> image, then the target-axis part of a cofactor-kernel row cannot have
> support on three or more centres.

This is coefficient-independent over an integral domain.  Combined with
the already checked one- and two-centre packets, it removes the last
coordinate-diagonal kernel geometry from the two-bad branch.  A remaining
two-bad source must use a mixed-colour internal cell.

## 2. The one-target projection

Let `K_x` be the four-site cofactor at hole `x`, and let `K_x^B` be its
projection to words using only `a,c`.  Colour parity splits a kernel row.
Its target-axis part is

\[
             \sum_x u_x e_t^{(x)}K_x=0.                 \tag{1}
\]

Fix `x` with `u_x != 0` and retain output words whose unique `t` occurs at
`x`.  A colour-diagonal four-site matching uses every colour an even number
of times.  Therefore no summand of (1) inserted at another hole contributes
to this projection, and

\[
                         u_x K_x^B=0.                    \tag{2}
\]

Thus, over an integral domain,

\[
               K_x^B=0\quad\hbox{for every }x\in S,
               \qquad S=\operatorname{supp}(u).         \tag{3}
\]

The checker exhausts all `5*2^4=80` one-target/binary words.  The 40 words
with even binary parity receive exactly the contribution inserted at the
target hole; the other 40 vanish structurally.

## 3. Two pure images through at most two holes

Project a preimage of `X_a` to the parity-`a`, target-free sector.  It has
the form

\[
       \sum_{x\notin S}\alpha_x e_a^{(x)}K_x^B=X_a.     \tag{4}
\]

The analogous equation holds for `X_c`.  If `|S|=5`, (4) has no column.
If `|S|=4`, both equations would use the same nonzero cofactor.  The first
would make it a pure `a` tensor and the second a pure `c` tensor, impossible.

It remains to take `|S|=3`, with complementary holes `h,k`.  In the
`a` equation, a nonzero coefficient at `h` forces `K_h^B` to have factor
`e_a` at `k`: a word with another colour at `k` cannot be cancelled by the
term inserted at `k`, whose `k` coordinate is fixed to `a`.  The same
argument applies at every used hole and to the `c` equation.  Since a
nonzero tensor cannot have both factors `e_a,e_c` at one site, the two
targets allocate the two holes bijectively.  After exchanging them,

\[
                         K_h^B=\lambda e_a^{\otimes4},
       \qquad K_k^B=\mu e_c^{\otimes4},                 \tag{5}
\]

with `lambda*mu != 0`.  This is the complete two-hole factor allocation;
there is no hidden cancellation or division by an unspecified sum.

## 4. The unique mixed coefficient

Choose a nonzero matching monomial `M_a` in the first coefficient of (5)
and `M_c` in the second.  They are perfect matchings of the two distinct
four-subsets `C\{h}` and `C\{k}`.

Some edge of `M_a` is disjoint from some edge of `M_c`.  Indeed, otherwise
each `M_c` edge would have to meet both disjoint edges of `M_a`.  But the
`M_c` edge incident with `h` has only one endpoint in `C\{h}`, so it can
meet at most one of them.

Let the disjoint edges leave hole `x`.  Colour their endpoints `a,a` and
`c,c`.  In a colour-diagonal matching there is exactly one compatible
perfect matching of `C\{x}`: the two displayed same-colour edges.  Its
coefficient is the product of two named nonzero factors, hence is nonzero.
It is a mixed coefficient of `K_x^B`.

This contradicts every possibility:

- if `x in S`, equation (3) says `K_x^B=0`;
- if `x=h`, equation (5) says `K_h^B` is pure `a`;
- if `x=k`, equation (5) says `K_k^B` is pure `c`.

The checker audits all ten pairs of holes and all `3*3` pairs of matching
monomials, reconstructing the unique mixed word in all 90 cases.

## 5. Scope and consequence

The proof allows arbitrary multi-centre preimages of the two bright
tensors and arbitrary additional diagonal cells.  It uses only parity,
factor separation, and a coefficient with a unique compatible matching.
It does not apply to mixed-colour internal cells.  In that case colour
parity no longer makes the target-coordinate part of a kernel row a kernel
row by itself: a non-`t` component inserted at another hole can multiply a
cofactor word containing a single `t` and enter the same projection as
(2).  The displayed isolation remains valid for a genuinely target-axis
row, but it cannot be extracted from an arbitrary kernel row.

Together with the atomic and two-centre bridge exclusions, this completes
the colour-diagonal part of the pure kernel-product question.  The next
theorem-level packet is the mixed-colour internal branch, not a larger
diagonal support search.

## 6. Reproduction

```sh
python3 computations/verify_shared_reciprocal_two_bad_large_kernel_exclusion.py
python3 -O computations/verify_shared_reciprocal_two_bad_large_kernel_exclusion.py
```

The checker uses only the Python standard library.
