# Active-leader quotient counterguard on the 114 compound regressions

The private Hall audit leaves 114 doubly-active four-cell parents for which
no minimal Hall pair occupies a `2x2` compound position in either OO chart.
This note tests the stronger proposal: localize a leading coefficient of
each active arm cofactor and inspect the corresponding full-nine packet.

## Coefficient packet at an active leader

For one pair chart, let `d` be its direct `3x3` block and let

\[
Q(\omega)=[q^{[3]}]_{\omega}\ne0                         \tag{1}


be a chosen residual-word coefficient.  Evaluating the nine exact target
rows at `omega` would give the endpoint-response matrix

\[
T(\omega)=\Delta(\omega)-Q(\omega)d,                     \tag{2}


where `Delta(omega)=0` for a mixed residual word and
`Delta(omega)=E_cc` for the pure word `c^6`.  After localizing `Q(omega)`,
(2) has rank two precisely when the pure coordinate line `e_c` is
transverse to both the row and column lines of the rank-one direct block.
That rank-two case supplies a nonzero `2x2` compound minor.

In the alternating-C8 packet the two direct arms are

\[
                         d_{02}=E_{10},\qquad d_{04}=E_{11}. \tag{3}


## Exact 114-profile census

For every regression parent, the selected coefficient in each cofactor is
a single Laurent monomial, so localization is honest and needs no
cancellation assumption.  Nevertheless:

* every `02` leader word is mixed;
* 91 `04` leader words are mixed;
* the remaining 23 `04` leaders are pure `1^6`, whose coordinate line
  collides with both lines of `E_11`.

Consequently the formal target-response rank bounds are `(<=1,<=1)` in all
114 profiles.  (A pure-normalization equation can lower one of these ranks
to zero.)  No transverse rank-two/diagonal compound minor appears.

On the common five sites of the two charts, the two leader words agree in
exactly one profile.  That is the literal proportional-word branch.  The
other 113 have distinct common words (Hamming distances one through five)
and remain rank-one annihilated branches.  Thus the requested dichotomy is

\[
  0\text{ nonzero compound},\qquad
  1\text{ proportional common word},\qquad
  113\text{ distinct-word rank-one branches}.            \tag{4}


## Scope and stopping decision

This is a counterguard to the **one chosen cofactor leader** version of the
weighted Lefschetz argument.  Activity makes the coefficient invertible,
but it does not make its residual word a transverse pure word.  Hence
localization alone does not create the diagonal minor needed to contradict
rank-one alignment.

The 114 parents are support relaxations already killed by private target
rows; they are not exact Krenn sources.  Therefore (4) does not disprove a
theorem that uses exactness to combine several cofactor coefficients or
changes leaders after higher-cell mates are added.  It does show that the
next lemma must use at least one of:

1. a linear combination of two or more active cofactor words;
2. transport between distinct common-five words via a head-column row; or
3. a genuine Hessian/second-polar minor, rather than the first coefficient
   packet (2).

Further raw support layers are not indicated by this test.

## Reproduction

```text
python computations/verify_oo_c8_active_leader_quotient.py
python -O computations/verify_oo_c8_active_leader_quotient.py
```

The checker reconstructs the 114 regression supports, both active
cofactors, their exact leading monomials, common-five restrictions, and the
formal target-response rank criterion.
