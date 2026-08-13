# The full eight-site groupoid contracts the last H2 tag

## Exact coefficient theorem

The fixed-response second-Hasse audit distinguishes six residual sites and
two response endpoints.  This distinction hides one symmetry.  Encode the
source variables as ordinary edges of the eight physical sites:

```text
q_ij = ij,     p_i = iP,     s_i = iS,     d = PS.
```

Under this dictionary the complete inventory of 210 compatible direction
pairs and seventy `K3,3` tail components is stable under all of `S8`, not
only under permutations of the six residual sites and `P <-> S`.

Checker:
[`verify_h3_h2_full_site_groupoid_tag_contraction.py`](../computations/verify_h3_h2_full_site_groupoid_tag_contraction.py).

The centered direction-tag module has dimension 140.  Exact modular ranks
at `1000003` and `1000033` are

```text
residual S6 action                    139
residual S6 + the transposition 5,P  140
full S8 action                        140.
```

Since 140 is the full dimension, the rational coinvariant space for the
full eight-site action is zero.  In particular, the fixed-endpoint survivor

\[
                    2e_{DQ}-e_{PS,1}-e_{PS,2}
\]

is not a physical-site invariant.  A single adjacent transposition which
exchanges a residual site with the selected response endpoint connects it
to the already contractible tag module.

## Why this was invisible in the fixed-response quotient

The previous rank-139 theorem used

\[
                     S_6\times\langle P\leftrightarrow S\rangle.
\]

That subgroup preserves the operation types `D,Q` and `P,S`, so their
orbit-count difference leaves one trivial representation.  In the original
eight-site tensor, however, the choice of which two sites are exposed as
the response endpoints is auxiliary.  Swapping an exposed endpoint with a
residual site sends the direct/endpoint distinction into a different
response chart and removes the orbit-count imbalance.

This is an exact action calculation, not an appeal to transitivity.  Every
generator maps the literal pair inventory and each three-pair `K3,3`
component bijectively, and the checker constructs all action-relation rows
on the integral centered basis.

## Physical meaning and remaining hypothesis

Suppose the lower principal-parts comparison is defined termwise on every
literal direction pair and is natural under changing the two selected
response endpoints.  Its action-groupoid bar then contracts every
direction-tag class over characteristic zero.  The formerly separate
generic symmetric C4 column is no longer an independent homogeneous face.

This does **not** construct the termwise physical comparison.  Coefficient
covariance under `S8` is automatic, while a physical bar must preserve the
source boundary, word/fine/repeated grade, protected rows, and augmented
readouts in every response chart.  A retained-label fold without the
source-labelled endpoint-change map would again be circular.

The downstream endpoint-even `P2` carrier in word `0102` is also outside
the original 140-dimensional tag module.  Its detectors `-13/6` and
`35/72` after `dq23` reinsertion remain the first explicit landing test.

Thus the lower frontier sharpens to one statement:

> Construct a termwise, source-valid, endpoint-choice-natural PP comparison
> for the complete H2 restriction.  Full-site equivariance removes every
> direction tag; the resulting word-`0102` carrier then enters the already
> proved augmented filler-or-terminal alternative.

The checker runs normally, optimized, and isolated/no-site.  Its frozen
ledger digest is
`32598f0d35eb7b57b5885481d9d7590bb85a9f27a0f4de8078a9955b46c51ffe`.
