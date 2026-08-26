# Orbit-85 diagonal-to-tail extraction starts in a new quadratic channel

Status: **UNAUDITED bounded exact provenance audit**.

## Outcome

Under

```text
A_ij^(ab) = delta_(a,b) d_ij^a + epsilon T_ij^(ab),
```

the orbit-85 extended certificate has no order-one tail term.  Its only
epsilon-dependent source leaves are all-even mixed amplitudes of profiles
`6+2+0`, `4+4+0`, and `4+2+2`; each first sees general off-diagonal cells at
order two.  The resulting `Tail2` layer is therefore not any frozen
`7+1`, `6+1+1`, `3+3+2`, or carrier-response row.

The packet freezes a circuit for the order-two correction but does not yet
expand it or prove that the complete circuit is nonzero.  Thus `2` is the
first **possible** global correction order.  The individual amplitude leaves
have nonzero quadratic terms exactly as stated below.

## Antecedent-by-antecedent epsilon audit

The 13,670 antecedents split exactly as follows.

| antecedent kind | count | first positive epsilon order |
|---|---:|---:|
| mixed diagonal amplitude | 1,638 | `2` |
| Boolean axiom | 5,592 | none |
| selector zero link | 384 | none |
| selector guarded inverse | 384 | none |
| Laplace-witness definition | 5,208 | none |
| inside-free product equation `P_j=0` | 448 | none on the fixed branch |
| outside-free complement localizer | 7 | none |
| unguarded open localizer | 9 | none |

Selectors, inverses, and constructible-branch witnesses are held
epsilon-constant.  Pure same-colour Hafnians, their Laplace identities, and
all selector links therefore contain no `T` cell at any order.

There is one important source guard.  The 448 `FR` antecedents are diagonal
branch equations `P_j(d)=0`; they are not stored as full eight-site X5
amplitudes.  They consequently have no epsilon correction in this fixed
branch packet.  Replacing an `FR` leaf by its corresponding full amplitude
would produce a quadratic correction, but doing so requires a separate
localized source derivation and is not licensed by the current DAG.

At the compiled-clause level, the 502 core inputs have family counts

```text
A3g 308, FR 93, A3 59, A2 25, XF 6,
C0 5, Ch 3, A1 2, Cnz 1.
```

Only the 25 `A2` clauses, five `C0` clauses, and six `XF` clauses through
their `C0` derivations are tail-sensitive.  They reference 569 mixed-
amplitude leaves, 185 distinct.

## Literal matching expansion

For an all-even word `w`, every matching has even crossing degree at each
colour.  Hence a matching cannot contain exactly one cross-colour edge and

```text
F_w(d+epsilon T)
 = F_w(d) + epsilon^2 Tail2_w(d,T) + O(epsilon^3).
```

The exact perfect-matching census is

| profile | tail-degree census among 105 matchings | `Tail2` terms |
|---|---|---:|
| `6+2+0` | `0:15, 2:90` | 90 |
| `4+4+0` | `0:9, 2:72, 4:24` | 72 |
| `4+2+2` | `0:3, 2:30, 3:48, 4:24` | 30 |

Every `Tail2` monomial consists of two `T` cells and the two remaining
same-colour diagonal edge factors.  Its two cross-colour edges are parallel
in colour space: `(01,01)`, `(02,02)`, or `(12,12)`.

Among the 185 distinct core amplitude leaves, the profile census is

```text
6+2+0 :  22
4+4+0 :   9
4+2+2 : 154.
```

Counting repeated compiler references gives `46,9,514`, respectively.

For example, the orbit-85 A2 representative with masks `(0,252,3)` is
`F_22111111`.  Its constant term is

```text
Haf(d^1 on {2,3,4,5,6,7}) * d^2_01,
```

and its first tail term is the 90-term sum obtained by connecting sites
`0,1` to two distinct sites of `{2,...,7}` with two colour-`12` cells and
matching the remaining four colour-1 sites diagonally.

## Comparison with 611, 332, and carriers

The frozen polar packet has the incompatible census

```text
7+1      : tail degree 1:105
6+1+1    : tail degree 1:15, 2:90
3+3+2    : tail degree 1:9, 2:18, 3:42, 4:36.
```

Those words have two odd colour classes, so their cross-degree parity is odd
at two colours.  Every orbit-85 amplitude leaf has three even colour classes,
so its cross-degree parity is even at every colour.  This parity obstruction
is invariant under site and colour transport.

Even the quadratic remainder of a `6+1+1` row is different: for
`F_01222222` its two tail edges form the colour path `(02,12)`.  Orbit-85
`Tail2` uses a doubled colour pair.  The carrier matrices and the frozen
`380 x 12` matrix are first derivatives at `T=0`, hence live at order one.

Therefore the closest existing description is the all-even
second-tail/second-fundamental layer of the zero-tail `620/440/422` packet.
It is not a literal `611`, `332`, or carrier packet, and no frozen response
rank theorem applies to it without a new quadratic extraction theorem.

## Diagonal-to-tail plan and remaining check

Linearize the arithmetic proof DAG at order two:

1. replace each `mixed_diagonal_amplitude` leaf by its literal `Tail2_w`;
2. give every epsilon-constant antecedent derivative zero;
3. propagate these values through the stored product/sum gates using the
   frozen order-zero multipliers.

This produces the candidate coefficient `C2` in

```text
C(epsilon) = 1 + epsilon^2 C2 + O(epsilon^3).
```

The current high-level DAG records enough provenance to build that circuit,
but it does not store a reduced source-labelled expansion or a nonvanishing
witness for `C2`.  That bounded circuit evaluation is the next exact step.
It should retain the fixed-branch `FR` convention above; a global X5-only
claim additionally needs FR derivation and the later 87-orbit branch gluing.

## Replay

```bash
python3 computations/unaudited-codex-n8-orbit85-tail-extraction-audit-2026-08-23/audit_orbit85_tail_extraction.py --check-results
python3 -O computations/unaudited-codex-n8-orbit85-tail-extraction-audit-2026-08-23/audit_orbit85_tail_extraction.py --check-results
python3 -I -S computations/unaudited-codex-n8-orbit85-tail-extraction-audit-2026-08-23/audit_orbit85_tail_extraction.py --check-results
```

The hostile `--mutate` mode changes the frozen first possible order and is
rejected.

Frozen logical digest:
`67f2142e6687668eaad423e71061a700080f04e625923b6d2a84fb8f7127d33c`.
