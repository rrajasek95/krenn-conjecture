# First atlas boundary: chart 1 with `A_02[0,0]=0`

## Terminal status

**Unresolved after the bounded gate; an exact D12 root core is frozen.**

The branch is source-faithful:

```text
chart support     three colours on 01|23|45|67
normalization     all twelve selected cells equal 1
boundary          A_02[0,0] = 0
source variables  239
mixed rows         6,558
live-target rows   s_c H_c - 1, c=0,1,2
```

A characteristic-zero unit for this extended ideal would close the first of
the 31 singleton branches in the minimum chart-atlas propagation tree.

## Literal source census

Every mixed word row survives the boundary specialization.  The collected
source packet has 677,670 terms and 596,816 global monomial keys:

```text
row term count      728 rows with 90; 5,830 rows with 105
minimum y-degree    d0:78, d1:648, d2:1944, d3:2592, d4:1296
constant rows       78
pure H term counts  90, 105, 105; each has constant coefficient 1
```

The strict msolve input has 242 variables after adjoining the three inverse
variables, 6,561 equations, and no invalid row.

## Bounded gate

The large-prime ordinary Gröbner gate over `p=1073741827` ran with eight
threads, DRL, and a full-basis request.  It hit the hard cap at 300.461
seconds, was terminated with return code `-15`, and left a zero-byte basis.
Its only engine output was the parser banner.

This is a timeout, not a unit, nonunit, dimension, or nonmembership result.
The one-shot gate should not be repeated without a structural compression.

## Exact homogeneous D12 root interface

The boundary stabilizer has order 32.  The 78 constant mixed words form 18
orbits.  Their complete root interface is

```text
rows / columns / exact rank   250 / 18 / 18
row degrees                   d0:1, d2:16, d3:46, d4:187
Fh rows on the interface      22
```

The finite target restriction is not in this 18-column span.  Its exact
five-row dual is

```text
row hex   weight
empty       -1
0a49         4
0d4c         2
0e4d         2
123f         1
```

and pairs with the restricted `Fh` target by `2`.  It is not a full D12
separator: the complete incident scan finds 148 column orbits, of which 130
kill the dual.  The lex-first killer is source word `00000011` (code 4),
multiplier `0a49`, with pairing `8`.

Thus the exact result is a small unresolved core, not nonmembership.

## Smallest next computation

Adjoin those 130 literal D12 column orbits, close their row incidence under
the order-32 boundary stabilizer, and rerun exact/modular span.  This is the
correct target-rooted continuation and retains every homogeneous multiplier
degree through eight.  It is materially smaller and more source-structured
than the timed-out 242-variable one-shot solve.

## Scope

Everything here concerns only chart 1, the all-twelve-anchor normalization,
and `A_02[0,0]=0`.  The modular timeout and finite root projection make no
claim about full D12 membership, saturation, radical membership, branch
emptiness, or any other chart boundary.

## Lazy D12 continuation

The exact root core was continued by dual-guided CEGAR in the order-32
boundary-stabilizer quotient.  Unlike the one-shot gate, this calculation
contains the complete homogeneous target: 992,250 actual `Fh` monomials,
forming 32,965 invariant rows.  Every selected column retains all of its
literal outputs, and every round agrees between exact rational and
`p=1073741827` rank/remainder status.

Seven rounds were accepted:

```text
round   rows    cols=rank   dual   incident   new crossings
  0    33,193       18        5       148          130
  1    35,086      148        6       247          229
  2    40,911      377        5       148          130
  3    44,368      507        9       603          585
  4    65,146    1,092       11       600          582
  5    83,847    1,674       13       915          897
  6   122,553    2,571        1        42           42
```

Every finite dual was killed.  The last one-row dual pairs the target by one
and has exactly 42 incident column orbits, all 42 of which cross it.  Those
repairs have been adjoined in the resumable state, giving 2,613 selected
column orbits.

The next scan stopped at `round_7_scan_512`.  Peak recorded RSS was
8,795,160,576 bytes.  Since the cap was checked between 512-column scan
blocks, terminalization occurred at 308.918 seconds, 8.918 seconds after the
nominal 300-second wall.  No round-seven result was accepted.

This remains unresolved: there is neither an exact D12 member nor an exact
D12 separator.  `resume_d12_lazy_cegar.json` is the exact restart packet;
it instructs the next pass to rebuild the full invariant target and all
outputs of the 2,613 selected columns, then begin with the round-seven span.
