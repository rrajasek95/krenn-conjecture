# Transverse Cartan landing is a two-root test with a concrete coloop/Hall residual

## Result

Let `e=uv` occur in exactly one of three selected pure anchor matchings,
say the colour-`c` matching.  Deleting `e` leaves rank two at both endpoint
stars.  The two deficient quotient lines are not unrelated: both select the
same missing local head `c`.

Consequently a Cartan connector with endpoint heads `(i,j)` is visible in
both quotient lines exactly when

\[
                             i=j=c.                   \tag{1}
\]

This makes the word-change requirement sharper.

* Every row in a fixed double-dark word is invisible in both quotients,
  independently of its matching skeleton, tail, or interference phase.
* A one-site root move can repair only one quotient.  It is necessarily a
  split-visible column.
* The first single double-visible object is the commuting two-root corner
  which changes both endpoint heads to `c`.  Equivalently, two separately
  sourced one-root exits can repair the two sides together.

The checker is
[`verify_h3_transverse_double_quotient_cartan_landing.py`](../computations/verify_h3_transverse_double_quotient_cartan_landing.py).
It audits this classification on every simple selected edge in all 31
`S8 x S3` anchor types.

## 1. Why both quotient lines have the same colour

For a selected pure matching `Q_k`, the endpoint-star column of its edge is
the coordinate head `e_k`.  If `e` belongs only to `Q_c`, deleting `e`
leaves precisely `e_d,e_f` at **each** endpoint, where
`{c,d,f}={0,1,2}`.  Thus

\[
 Q_u\simeq k^3/\langle e_d,e_f\rangle,
 \qquad
 Q_v\simeq k^3/\langle e_d,e_f\rangle,               \tag{2}
\]

and both cokernel covectors are the `c`-coordinate covector.

Across the 31 normalized anchor types there are 249 such simple selected
edges.  They give the exact head census

```text
double-dark same-word head pairs       996
one-site root exits                  1,992  (all split-visible)
two-site root corners                  996  (all double-visible).
```

Equation (2) also explains why bidirectional private-site identities alone
do not prove the quotient landing.  They produce two exact active fans from
one off-diagonal cell, but further tails of that fixed cell retain its two
endpoint labels.  They cannot manufacture the missing `c` head on a side
where the decoration is not `c`.

## 2. Avoiding pure matching gives the positive landing

Expand the pure-`c` target coefficient and inspect its literal nonzero
matching monomials.  There is an exhaustive dichotomy.

1. Some nonzero pure-`c` matching `M` avoids `e`.
2. Every nonzero pure-`c` matching contains `e`; then `e` is a literal
   pure-target coloop.

In the first branch replace the selected `Q_c` by `M`.  Since `e` belonged
to neither of the other two selected matchings, it is now absent from the
entire three-colour anchor union.  The three surviving pure-coordinate
columns have rank three at both endpoints of `e`.

Now use the exact target-augmented private-site identity on the nonzero
off-diagonal carrier at `e`, and its transposed copy.  Each supplies a
nonzero determinant/cofactor fan.  If one active fan mate is also outside
the reselected anchor union, both physical edges are absent from all three
anchors.  All four deleted-star ranks are three, while the fan determinant
has distinct centre heads.  This is the desired distinct-head four-good
active overlap.

The finite geometry has substantial slack.  The checker tries all 90
perfect matchings avoiding each of the 249 simple edges:

```text
pure-anchor reselections                         22,410
minimum off-anchor fan-mate choices per endpoint      3
total off-anchor fan-mate choices                155,700.
```

Nonvanishing—not incidence—is the remaining issue.  The source identities
decide which of those candidate mates actually carries a nonzero cofactor.

## 3. The exact failure branches

If the positive landing does not fire, there are two source-level residuals.

### A. Pure-target coloop

If no nonzero pure-`c` matching avoids `e`, then `e` is a literal coloop,
not merely a rank-two aggregate port.  Given a nonzero common-`q` outside
column with four distinct endpoint holes, the physical matching-base `E2`
identity gives an exact alternative:

* an alternate pure target matching, which breaks the coloop; or
* a nonzero target/outside exchange minor.

At `h=3`, the nine four-hole tail pairs have cycle types

```text
C4 + C4 : 2
C6      : 1
C8      : 6.
```

The two `C4+C4` cases have crossed recombined matchings and land whenever a
new edge escapes the anchor union.  The seven single-cycle cases have no
third perfect matching on the same edge union.  The sharp coloop residual is
therefore a source-typed, anchor-contained `C6/C8` exchange carrier.

The four-distinct-hole hypothesis is explicit.  Hole collisions belong to
the already separated lower Hall/reselection strata.

### B. Anchor-contained bidirectional Hall web

Suppose an avoiding pure reselection exists, but every nonzero mate in both
private-site fans stays in the reselected anchor union.  The same-star
five-lock theorem gives the exact trichotomy:

1. a lock-kernel vector is an anchor-safe support deletion;
2. complementary crossed off-anchor components give the four-good wedge;
3. the lock map is injective and has no complementary crossed wedge.

Only the third case remains.  Complete same-cell companion rows cannot
repair it: all 216 audited avoiding companions preserve the two original
endpoint labels.  The sharp Hall residual is therefore

\[
 \boxed{\text{injective five-lock, no complementary off-anchor wedge, and
 all active mates anchor-contained}.}                \tag{3}
\]

The `C6/C8` coloop carrier and (3) are two exact surviving alternatives.
They should not be identified without an additional theorem typing the
physical `E2` carrier as a column of the bidirectional lock complex.

## 4. Frontier consequence

The requested double-quotient theorem is no longer an unspecified rank
implication.  Its shortest form is:

> Attach both endpoint roots of the physical Cartan comparison.  If the
> double-root corner has a nonzero avoiding pure-target realization, reselect
> the pure anchor and use any escaping private-site mate to obtain the
> four-good active overlap.  Otherwise route the explicit pure-coloop
> `C6/C8` carrier or the injective no-wedge Hall lock.

This also retires two unproductive shortcuts: more matching interference
inside one word cannot change a quotient head, and more tails of one fixed
decorated cell cannot fill the opposite missing-colour line.

## Verification

Run

```text
python3 computations/verify_h3_transverse_double_quotient_cartan_landing.py
python3 -O computations/verify_h3_transverse_double_quotient_cartan_landing.py
python3 -I -S computations/verify_h3_transverse_double_quotient_cartan_landing.py
```

The frozen ledger SHA-256 is

```text
0e34137efe92c16ebba1b37202ebc446e1a30ee8bb3d81ef1ebcda9e28b103c9
```
