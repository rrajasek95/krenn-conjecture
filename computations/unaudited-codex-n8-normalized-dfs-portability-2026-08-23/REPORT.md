# Read-only portability audit: target-rooted DFS for the normalized N8 critical tail

## Verdict

The target-rooted acyclic DFS used in the frozen `P^2` filtration has a
source-faithful N8 port, but only after **homogenizing the normalized mixed
generators**.  At the first possible total degree, seven, the port is a finite
exact test for

\[
t^7\in I^h,
\]

not an ordinary-degree truncation.  The recursive pivot logic and certificate
audit can be reused verbatim.  The N6 algebra provider must be replaced by the
N8 normalized matching provider described below.  No DFS or span solve was
run in this audit.

There is also a necessary packet guard.  The frozen `closure22` words do not
contain any of the five support-stabilizer word orbits used by the six-column
normalized contraction.  Thus `closure22` alone cannot even supply the seed
`1+Tail`; it is not a drop-in generator packet for this calculation.

## Frozen inputs

The normalized source is the one reconstructed by
[`verify_n8_normalized_critical_contraction.py`](../verify_n8_normalized_critical_contraction.py):

* 8 sites, 3 endpoint colours, 28 physical edges, and 252 edge-colour cells;
* the twelve support cells have raw coordinate IDs
  `0,22,62,89,103,125,130,135,162,233,238,243` and are set to one;
* the remaining 240 variables retain their raw one-byte IDs in `0..251`;
* the relevant symmetry is the exact order-four stabilizer of the coloured
  support product, not `S8 x S3`;
* all 6,558 mixed words form 1,672 word orbits under this stabilizer;
* a word has 105 matching terms before normalization; after deleting the
  twelve support variables, equal monomials are collected with their integer
  multiplicities.

The exact balanced dual certificate has 100 rows (`80+20`).  After
normalization they remain 100 distinct critical monomials, with degree
histogram

```text
0:1, 2:1, 3:4, 4:27, 5:47, 6:20.
```

They are provenance for the contraction, not the DFS roots.  The six frozen
invariant columns give

\[
1+Tail\in I_{\rm mixed},
\]

where `Tail` has 564 invariant monomial orbits, 2,240 actual monomials, and

```text
degree       2   3   4    5    6    7
orbit count  6  16  48  104  254  136
```

Its coefficient histogram is

```text
-1: 4,  -1/2: 512,  +1/2: 48.
```

Clearing the common denominator two therefore gives an integral seed.  A
successful coordinatewise DFS on the 564 roots is stronger than necessary,
but it is sufficient: it puts every tail monomial in the chosen homogeneous
mixed span, hence puts `Tail` there.

The authoritative file digests are

```text
normalized contraction checker
  4e2ce4b12626edaedd9a8a5a4a9635ab5c74a5f139ecf52507018ca5478acd62
balanced 100-row dual certificate
  7f5ba935e260864515833a974f26899879f7153e0ff8ee91acb41c0b4b1c15d3
closure22 word manifest
  343b5f531d6303b2d651123a8a5e4f1653b060cb6f7f66bc61cbd22b7fa4d10d
```

## Exact homogeneous formulation

For a mixed word `w`, write its normalized polynomial as

\[
g_w(x)=\sum_\tau a_{w,\tau}x^\tau,
\qquad
g_w^h(t,x)=\sum_\tau a_{w,\tau}t^{4-|\tau|}x^\tau.
\]

Each normalized term has degree `0..4`.  If a column has normalized
multiplier `m` of degree `d<=3`, its degree-seven homogenization is

\[
t^{3-d}m g_w^h.
\]

Homogenizing the six frozen contraction columns to their common degree seven
preserves every cancellation and gives

\[
t^7+\sum_{r\in Tail}c_r t^{7-|r|}r\in I^h_7.       \tag{1}
\]

Consequently an acyclic triangular certificate proving every
`t^(7-|r|) r`, `r in Tail`, lies in `I^h_7` proves `t^7 in I^h`; setting
`t=1` proves `1 in I`.  This is a genuine finite polynomial certificate.

This homogenization is load-bearing.  Reusing the N6 rule “discard outputs
above the cutoff” in the inhomogeneous normalized ring would prove only a
bounded filtration statement and would not reduce the 564-tail exactly.
For a later saturation step `t^k`, the identical construction runs in total
degree `7+k`; each such degree is finite, but no fixed-degree failure decides
the saturation.

## Mapping of the cycle DFS interface

The frozen Rust interface is
[`p2-k6-global/src/main.rs`](../unaudited-codex-p2-k6-global-2026-08-23/src/main.rs)
(SHA-256
`cbe0e5edcf0fead024159bf68b8df586fb54b547b32c053b1e331ee9fd458b5a`).
Its reusable part is `DfsState`, `prove_dfs`, the post-order triangular audit,
and the `PIVOT` ledger.  The exact mapping is:

| Cycle/N6 object | Normalized N8 object |
|---|---|
| `Packed {off, gs[3]}` | sorted raw IDs of normalized variables; the `t` exponent is implicit as `7-len(row)` |
| 90 bichromatic variables | all 240 nonsupport edge-colour cells |
| three ternary diagonal graph codes | deleted; the twelve chart cells equal one |
| word code in `0..728` | base-three 8-site word code in `0..6560` (`u16` still suffices) |
| 15 six-site matchings | 105 eight-site perfect matchings |
| `S6 x S3`, order 4,320 | frozen support stabilizer, order 4 |
| minimum off-degree cutoff | fixed homogeneous total degree seven |
| truncated column outputs | every term of `t^(3-|m|) m g_w^h`, with collected integer multiplicity |
| target rows | the 564 rows `t^(7-|r|)r`; the 100-row dual is metadata, not a root set |

Rows need no explicit `t` field at degree seven.  A normalized monomial is a
sorted byte string; its degree is its byte length and its `t` exponent is
`7-degree`.  A column is `(word_code, multiplier_bytes)`, with
`len(multiplier)<=3` and implicit multiplier `t` exponent
`3-len(multiplier)`.

For a root row `r`, incidence is inverted exactly as follows:

1. enumerate every multiset divisor `tau` of `r` of degree at most four;
2. look up every allowed mixed word having normalized term `tau`;
3. require `len(r)-len(tau)<=3` (equivalently, divisibility by the term's
   homogenizing power of `t`);
4. set `m=r/tau` and canonicalize `(w,m)` under the order-four stabilizer.

The output map is the existing invariant orbit sum
`invariant_column_image((w,m), polynomials)`.  Its coefficients, including
matching collisions, must be retained.  In the bounded root census below
they are `1,2,4`; treating a column as a set of rows would be unsound.

## Proposed byte interfaces

The smallest source-faithful seed format is

```text
KRENN_N8_NORMALIZED_TAIL_V1 7 564 2 <allowed-word-manifest-sha256>
ROW <sorted-raw-variable-ids-as-hex> <coefficient-after-times-two>
...
```

The `2` records the cleared common denominator.  Raw IDs, rather than a new
dense numbering, make every row directly comparable with the frozen Python
artifacts.

The certificate is the direct N8 analogue of the existing text ledger:

```text
KRENN_N8_HOMOGENEOUS_DFS_V1 7 564 <pivot-count> <manifest-sha256>
PIVOT <row-hex> || <word-code> <multiplier-hex> || <integer-diagonal>
...
```

The order is dependency-first.  An independent checker must reconstruct the
complete invariant homogeneous column, check its displayed diagonal, check
that every other row has appeared earlier, check that no column is reused,
and back-substitute the cleared 564-row target coefficients.  The last step
is not done by the current N6 Rust writer because that engine proves
coordinatewise surjectivity; adding it makes the final `t^7` identity
explicit rather than merely existential.

## Packet guard and bounded sizing census

The 22 literal closure words occupy 17 support-stabilizer orbits and expand
to 62 literal words.  The six contraction columns use five distinct word
orbits, represented by

```text
00000012  11000010  11010012  11012111  12012000.
```

They expand to 16 literal words and are disjoint from the closure22
stabilizer closure.  Thus the smallest invariant discovery packet containing
both frozen artifacts is

```text
closure22^H plus the five contraction orbits:
22 H-orbits, 78 literal words.
```

This is only a subideal screen.  The authoritative normalized ideal uses all
1,672 stabilizer orbits / 6,558 mixed literal words.

A read-only enumeration of only the 564 root incidences at total degree seven
gave:

| allowed packet | root columns | one-hop rows | one-hop degree counts |
|---|---:|---:|---|
| `closure22^H + C5^H` | 294 | 25,153 | `0:1,2:16,3:70,4:419,5:2330,6:7906,7:14411` |
| all mixed words | 902 | 78,081 | `0:1,2:16,3:111,4:953,5:5837,6:23922,7:47241` |

Every one of the 564 roots has at least one incident column in both packets.
These are first-shell counts only, not a closure size or a solve result.

## Smallest implementation change

For a first bounded attempt, the smallest change is a Python adapter, not a
Rust rewrite:

1. import the frozen normalized checker and reuse `canonical_monomial`,
   `canonical_column`, `normalized_generator`, `invariant_column_image`,
   `multiset_divisors`, `quotient`, and `CONTRACTION`;
2. add the four-step homogeneous incidence filter above and memoize complete
   invariant column images;
3. copy the approximately fifty-line `prove` recursion and post-order audit
   from [`dfs_power2_filtration.py`](../dfs_power2_filtration.py);
4. emit the two text formats above and replay the target coefficients.

If the first shell grows too large, the Rust port should retain
`DfsState/prove_dfs/dfs_certificate` and replace the algebra-specific
`Engine`: use `N=8`, 105 matchings, the order-four maps, raw normalized byte
monomials, and a term-to-word inverse index.  The `gs[3]` graph codes and the
off-degree cutoff disappear.  At degree seven the existing nine-byte fixed
array is already large enough; a dynamic byte vector is needed only for
testing higher `t`-saturation degrees.

## Terminal scope

This audit establishes a finite exact interface and its first-shell size.  It
does not assert that the degree-seven DFS succeeds, that `closure22+C5`
generates the tail, or that any fixed-degree failure survives
`t`-saturation.  No broad closure, DFS, rank, or Groebner computation was
launched.
