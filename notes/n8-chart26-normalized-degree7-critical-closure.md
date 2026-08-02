# Chart 26 has a 49-row normalized critical class through degree seven

## Outcome

After setting the twelve chart-26 support variables to one, the old
balanced degree-six obstruction disappears immediately.  The exact
six-column contraction of
[`n8-full-source-degree6-bockstein.md`](n8-full-source-degree6-bockstein.md)
has image

\[
                              1+R,                         \tag{1}
\]

where $R$ is supported on 564 invariant monomial orbits of normalized
degrees 2 through 7.  This note follows that residual through a finite,
global top-degree contraction.

The residual-led component closes after three exact dual-guided extensions.
Its final census is

\[
                 273{,}857\text{ row orbits},\qquad
                 3{,}721\text{ column orbits},\qquad
                 \operatorname{rank}_{\mathbb Q}=3{,}721. \tag{2}
\]

The final separating functional has only 49 rows.  It annihilates every
normalized mixed-generator column with multiplier degree at most three and
pairs to one with the constant monomial.  Thus no degree-seven homogeneous
repair turns (1) into a certificate for $1$.  This is an exact bounded
critical class, not an unrestricted localized obstruction.

## Well-founded top-degree orientation

There are 6,558 normalized mixed hafnian coefficients.  Every one has
maximum normalized degree four, and their graded-lex leading monomials are
6,558 distinct squarefree degree-four monomials.  Orienting a column by
such a top term never raises total degree.  Within a fixed degree its other
top terms are lower in the chosen global lex order.  Hence ordinary
division is well-founded.

Dividing the 2,240-term actual tail from (1) by this ordered list takes only
26 steps, but leaves a 913-term remainder with degree histogram

\[
 0:1,\quad2:2,\quad3:18,\quad4:92,\quad
 5:274,\quad6:414,\quad7:112.                              \tag{3}
\]

Because the generators are not a certified Groebner basis, this nonzero
remainder is order-dependent and is not itself an obstruction.  It is only
the seed for the source-faithful closure below.

## Residual-led closure and exact ranks

Start with the 564 invariant rows of $R$.  Whenever a degree-four
generator term divides a current row, include the corresponding normalized
column and every one of its output rows.  This keeps every row in degree at
most seven and terminates at 20,859 rows and 298 columns.  Exact elimination
shows that all 298 columns are independent and that the normal form of
$R$ is exactly $-1$, as forced by (1).

The resulting three-row dual does not annihilate all bounded columns: 13
external columns meet it.  Adjoin precisely those violating columns, close
again under top-degree incidence, and repeat.  The exact adaptive census is

| round | rows | columns | rank | dual rows | incident columns | violations |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 20,859 | 298 | 298 | 3 | 16 | 13 |
| 1 | 134,041 | 1,849 | 1,849 | 24 | 38 | 8 |
| 2 | 216,350 | 2,955 | 2,955 | 37 | 50 | 6 |
| 3 | 273,857 | 3,721 | 3,721 | 49 | 56 | 0 |

Only 27 external column orbits are forced over the three extensions.  At
every round the columns remain independent; no internal source syzygy can
alter the critical value.  In the final round exhaustive incidence from
the 49 dual rows finds 56 bounded columns, all already present and all with
zero pairing.  Every other multiplier-degree-at-most-three column misses
the dual support and therefore pairs to zero trivially.

Expanding the 56 column orbits gives 220 actual columns.  Dividing each
invariant row weight by its row-orbit size produces a full-space functional
which annihilates all 220 actual columns separately, not merely their orbit
sums.

The final dual has degree distribution

\[
                  0:1,\quad4:1,\quad5:3,\quad6:5,\quad7:39
\]

and coefficient histogram

\[
                  -2:19,\quad-1:3,\quad1:4,\quad2:23.
\]

Its exact 49-row digest is
`b0f137c8827d8da94525a53636bd30791e7c56722b09a74e8cdfd0c792e75fb3`.

## Homogenized meaning and the termination guard

Let $I^h\subseteq\mathbb Q[y,t]$ be the degree-four homogenization of the
normalized mixed ideal.  A normalized column with multiplier degree at
most three becomes a degree-seven homogeneous column after multiplying by
the appropriate power of $t$.  The final dual therefore certifies

\[
                              t^7\notin I^h.               \tag{4}
\]

Equation (4) is the precise meaning of the bounded obstruction: the first
apparent unit repair (1) does not close at homogenized degree seven.

It does **not** prove $1\notin I$.  Since the normalized ideal is
inhomogeneous, an S-pair of degree greater than seven may cancel its top
terms and leave a new consequence in degree at most seven.  In homogeneous
language this is exactly the possibility of $t$-torsion.  The exact
termination target from
[`n8-support-normalization-is-exact-localization.md`](n8-support-normalization-is-exact-localization.md)
is

\[
  F\in I
  \quad\Longleftrightarrow\quad
  t^N F^h\in I^h\text{ for some }N\geq0,                  \tag{5}
\]

where $F=\bar H_0\bar H_1\bar H_2$.  A complete chart proof must bound
the saturation exponent $N$, exhibit a finite identity, or construct an
acyclic matching across all relevant $t$-levels.  No finite degree cap by
itself supplies that conclusion.

The final 49-row functional happens to see only the constant term of $F$
and pairs to one there.  This records the provenance of the old target
class, but it is not a degree-twelve test of (5).

## Reproduction

```sh
python3 computations/verify_n8_chart26_normalized_degree7_closure.py
```

The checker reconstructs all normalized generators, the six-column seed,
the graded-lex closure, all four rational ranks and duals, and the exhaustive
bounded-column separation without cached matrices or modular arithmetic.
