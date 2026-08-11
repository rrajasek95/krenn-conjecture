# Pairwise circuits do not generate the mixed leading-support cone

Date: 2026-08-11

Checker:
`computations/verify_n8_one_bad_axis_pure_mixed_weight_hilbert_circuits.py`

## Exact cone verdict

Restrict the pure-chart cocharacter quotient to all `90` off-diagonal
residual q cells.  Their rational quotient characters span rank `11` and no
column is zero.  A mixed support cannot be made strictly positive by a
chart-preserving cocharacter exactly when its columns admit a nonzero
nonnegative dependence.

The `22` opposing pairs from `9913c00` are not the whole story.  Exact
oriented-matroid enumeration finds

```text
58 pair-free positive circuits of support size three.
```

Every circuit has primitive coefficient vector `(1,1,1)` on the **raw**
quotient characters.  Since it contains neither a zero ray nor an opposing
pair, its incidence vector cannot decompose into smaller nonnegative kernel
elements.  Each is therefore a genuine Hilbert-basis element, not merely a
rational dependence.

The order-four chart stabilizer splits the `58` triples into `18` orbits:
eleven of size four and seven of size two.

## Smallest higher primitive obstruction

The first canonical circuit is

```text
01:02,   24:12,   34:01.
```

It obeys the literal port-character identity

```text
chi(01:02) + chi(24:12) + chi(34:01)
  = chi(03:00) + chi(24:11) + chi(14:22).
```

The three cells on the right are retained chart anchors, so the relative
weights of the three mixed cells satisfy

```text
ell(01:02) + ell(24:12) + ell(34:01) = 0.
```

If all three cells are supported, finiteness makes their weights
nonnegative and hence forces all three to remain at weight zero.  No pair
among them is opposing.  This is the smallest higher primitive obstruction
to toric normalization.

## Three-edge recombination structure

All `58` circuits have the same combinatorial origin.  Their six coloured
ports are a re-pairing of a **unique** triple of retained anchors, one anchor
in each colour.  Only the three residual zero anchors and the two residual
anchors in each of colours one and two can occur, giving `3*2*2=12` anchor
triples.  The numbers of mixed recombinations per anchor triple have
histogram

```text
2 -> 2 anchor triples,
4 -> 2 anchor triples,
5 -> 2 anchor triples,
6 -> 6 anchor triples.
```

Thus the obstruction is a finite signed-matroid phenomenon, not an
arbitrary three-cell source-support search.

## Proof consequence and scope

The proposed normalization theorem cannot stop after eliminating the 22
opposing pairs: a nonseparable leading support may be pair-free and contain
one of these primitive triples.  The next coefficient-level obligation is
to eliminate or reroute these three-edge recombinations uniformly.

This checker determines the nonnegative integer kernel only through degree
three.  It does not enumerate coefficient source packets and does not claim
a complete Hilbert basis in degrees four and above.  That larger computation
is intentionally deferred unless the degree-three source equations reveal
a uniform elimination mechanism.
