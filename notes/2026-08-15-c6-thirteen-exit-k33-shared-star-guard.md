# The first shared-star-valid thirteen-exit guard is a dirty `K3,3`

## Result

The thirteen exits of the degree-four parent chain have a sharp minimum
classification.

* Among all `78` unordered two-exit supports, `12` already expose a mixed
  singleton and the other `66` have an explicit active clean cap.
* There are `32` cap-`34`-avoiding, pairwise edge-disjoint three-factor
  packets.  The `24` triangular-prism packets again have an active clean
  cap.  The remaining `8` parity-labelled packets are four physical
  `K3,3` supports.  They are the first geometry on which every occupied cap
  can remain dirty.
* One `15`-cell `K3,3` packet is an exact local counterguard: its four live
  mixed rows vanish, its signed exit sum vanishes, every response slice has
  the literal shared-star form `uv^T+xy^T`, and it has no active clean cap.
* The counterguard is not a full GHZ source.  All three pure rows are absent.
  Moreover, all `15^3=3375` ways to add one pure matching witness in each
  colour create mixed singleton debt; the minimum is ten singleton rows.

Thus `9ab9b48 + 1412e4d` do not by themselves close the thirteen exits.
They reduce the first unresolved case to a concrete `K3,3` permanent-zero
packet.  The missing hypothesis is recursive completion/minimality: every
mate of the forced pure debts must yield a unit, restore a clean cap, or
strictly lower the packet.

The exact checker is
`computations/verify_c6_thirteen_exit_k33_shared_star_guard.py`.

## 1. Matching geometry of the thirteen exits

Retain

```text
M0 = 05|12|34,
M1 = 01|25|34.
```

After removing these parents, the signed fifteen-matching relation has

```text
1 cap-complement + 4 M0-tail + 4 M1-tail + 4 transverse-C6 exits.    (1)
```

Two distinct perfect matchings of `K6` either share one edge, hence differ
on a `C4`, or are disjoint, hence form an alternating `C6`.  Exact
enumeration of the thirteen exits gives

| tail-free cardinality | all families | cap-34 avoiding |
|---:|---:|---:|
| 2 | 44 | 36 |
| 3 | 48 | 32 |
| 4 | 14 | 6 |
| 5 | 2 | 0 |

For every pair, put both endpoint-coloured occurrences into the two sections
`111001` and `111221`, and choose one exclusive edge sign so that the two
occurrence values are `+1,-1` whenever both are present.  Replaying all 729
coefficient words gives

| geometry | mixed singleton | active clean cap |
|---|---:|---:|
| common tail | 4 | 30 |
| disjoint | 8 | 36 |

The clean caps are literal physical caps, not matching-graph labels.

* For a common-tail pair, cap the common edge.  Neither occurrence has a
  star leaving the cap, so `r=0`.
* For a disjoint pair avoiding `34`, cap the unique all-colour-one edge of
  either matching.  The other matching supplies response on only one
  residual edge, so `r^2=0` in the four-site residual algebra.

In either case the direct block is nonzero.  A covector `K` can be chosen
with all three diagonal readouts nonzero and `s(K) != 0`; hence this is an
active clean cap in the exact `N=6` condition.

This proves that a two-exit cancellation is never the hard case.

## 2. The first three-channel exception

Restrict to the `32` pairwise-disjoint triples which avoid cap `34`.  Their
edge union is one of the two cubic graphs on six vertices.

* `24` unions are triangular prisms.  Some occupied cap sees response edges
  with matching number one, so `r^2=0`.
* `8` parity-labelled triples have union `K3,3`.  They represent four edge
  supports, and form one orbit under the word-section stabilizer
  `S_{0,1,2,5} x S_{3,4}`.

For `K3,3`, cap any occupied edge.  Its two endpoints see the complementary
`K2,2`, so the response square is a `2x2` permanent rather than a repeated
edge.  This is the first place shared-star integrability is compatible with
an everywhere-dirty active locus.

## 3. Smallest literal guard

Take shores

```text
L = {0,1,5},       R = {2,3,4}
```

and put on their nine edges the nonzero matrix

\[
 W=\begin{pmatrix}
 1&1&1\\
 -2&1&1\\
 1&1&1
 \end{pmatrix}.                                             \tag{2}
\]

Every edge incident with sites `3` or `4` receives both endpoint-colour
versions from `111001` and `111221`; the other three edges retain colour
`11`.  Hence the decorated support has

```text
6 doubled boundary edges + 3 fixed all-1 edges = 15 cells.             (3)
```

The six fine matchings of `K3,3` are all thirteen-exit matchings: none uses
`01` or `34`.  In each of the four live word sections

```text
111001, 111021, 111201, 111221
```

their values are

```text
1, 1, -2, 1, -2, 1,                                      (4)
```

whose sum is zero.  Since all six exits have positive sign in the deleted
`a01` relation, the signed exit sum is the same zero.

Equivalently,

\[
                       \operatorname{perm}(W)=0.           \tag{5}
\]

All nine `2x2` permanental cofactors of `W` are nonzero:

```text
2, -1, -1,  2, 2, 2,  2, -1, -1.                         (6)
```

This gives the exact cap classification.  A pair outside `K3,3` has zero
direct block and is inactive.  At an occupied edge `(i,j)`, the common-edge
formula factors the response through the complementary `K2,2`; its top
square is a nonzero multiple of

\[
             \operatorname{perm}(W_{\widehat i,\widehat j})s(K)^2.       \tag{7}
\]

By (6), every active covector has nonzero clean error.  Therefore the guard
has no active clean cap.

The checker also evaluates all

```text
15 caps x 6 residual edges x 9 decorated cells = 810
```

response slices.  Every determinant is zero, exactly as required by the
physical shared-star identity of `1412e4d`.  This is an actual aggregate
edge assignment, not a formal response tensor.

## 4. Why the permanent-triangle unit does not fire yet

The three factors used to describe the `K3,3` are one parity class of its
six permutations.  Their edge union automatically supports the other
parity class.  Thus the four source rows in (4) have six occurrences each.

The permanent-triangle lemma `90e5faf` requires three private binomial rows,
each isolating one `2x2` permanent with a unit cofactor tail.  Those private
rows are absent here.  Applying the identity directly would discard the
other four occurrences in each contaminated row.  The guard is therefore
also the sharp counterguard to a graph-only invocation of the permanent
triangle.

## 5. Pure normalization forces the first debt

The bare guard has no occurrence in `000000`, `111111`, or `222222`, so it
has three literal pure failures.  To test the smallest possible repair,
choose an arbitrary perfect matching witness in each colour and adjoin its
three cells.  There are `15^3=3375` labelled choices.

The complete 729-row replay gives

```text
support size 23: 2025 completions,
support size 24: 1350 completions,
singleton-free:       0 completions,
minimum mixed singleton rows: 10.                         (8)
```

This is stronger than checking four disjoint third fines: it allows every
pure matching independently in each colour.  Coefficients cannot remove a
singleton because every occupied cell is nonzero.

Equation (8) is a forced *debt* for a larger source, not yet a global unit.
An exact source could add further endpoint-coloured cells which mate the
singleton.  The next finite problem is to classify cardinality-minimum
simultaneous mates of the ten-debt completions.

## Scope

This result is exact for the thirteen `K6` exits, both displayed word
sections, all literal endpoint-coloured shared stars, all 729 coefficient
words, every two-channel support, every cap-avoiding tail-free triple, and
all minimum pure-witness completions of the first hard orbit.

It does not prove that arbitrary larger mate packets preserve the singleton
or clean cap.  In particular, it does not promote the partial support debt
in (8) to a unit in an unknown full source.  The sharp terminal alternative
is now:

> every simultaneous mate of a minimum `K3,3` pure-completion debt yields a
> permanent-triangle unit, restores an active clean cap, or decreases a
> source-minimal potential.

Run:

```text
python3 computations/verify_c6_thirteen_exit_k33_shared_star_guard.py --mode structural
python3 -O computations/verify_c6_thirteen_exit_k33_shared_star_guard.py --mode full
python3 -I -S computations/verify_c6_thirteen_exit_k33_shared_star_guard.py --mode exhaustive
```

All modes have frozen ledger SHA-256
`d20758f5c1b8a571f523e074f88f0b6037d29389e86fd6a89d3bb57c1f7b0d03`.
