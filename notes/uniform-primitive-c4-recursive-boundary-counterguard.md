# Recursive primitive `C4` completion reaches a common-core recurrence, not a monotone

## Outcome

The six singleton debts exported by the primitive-`C4` wandering guard have
a **unique support-minimal simultaneous `C4` completion**.  It uses seven
new decorated cells.  After an integral four-cell completion of the reopened
pure-zero and `L/R` rows, the resulting 26-cell packet has

```text
all three pure coefficients normalized to 1,
eleven cancelling mixed rows,
thirteen primitive binomial subrows,
thirty-three remaining nonzero mixed coefficients.
```

This layer gives both a negative and a positive answer.

* Negative: recursive completion is not governed by common-window size,
  occupied support, or odd sign holonomy.  Every one of the 33 residual
  coefficients admits an anchor-contained primitive-`C4` occurrence; a
  deterministic simultaneous choice of their least cores has empty total
  window intersection; and the current signed exponent component has no odd
  dependency.
* Positive: the packet already contains two exact two-row recurrences.  In
  each recurrence the physical tail, `C4` window, bistar shores, and all four
  varying decorated cells are path-independent.  Only the pure colour on the
  retained tail changes.  This is the desired fixed-endpoint common-core
  output at the occurrence level.

What remains is not another support enumeration.  It is a complete-row
projection theorem showing that such a recurrent core remains a
source-provenant bistar carrier in the presence of arbitrary extra matching
terms—or else those extra terms give a unit, support deletion, or active
outside fan.

Exact checker:
[`verify_uniform_primitive_c4_recursive_boundary_counterguard.py`](../computations/verify_uniform_primitive_c4_recursive_boundary_counterguard.py).

## The unique seven-cell completion

Start from the 15-cell packet of
[`uniform-primitive-c4-source-label-wandering-counterguard.md`](uniform-primitive-c4-source-label-wandering-counterguard.md).
For each of its six singleton debt words there are exactly six primitive
`C4` mates.  Exhausting all

\[
                              6^6=46,656
\]

simultaneous choices gives a unique minimum union, of size seven:

```text
03:01 =  1,    25:01 =  1,
24:20 =  i,
34:00 =  1,
14:02 =  1,    35:01 =  i,
25:20 = -1.
```

This is a gauge normalization, not a claim that the seven individual
weights are unique.  Put

```text
a=03:01, b=25:01, c=24:20, d=34:00,
e=14:02, f=35:01, g=25:20.
```

The six cancellation equations force the gauge-invariant products

\[
       ab=1,\qquad ac=i,\qquad d=1,\qquad ef=i,
       \qquad eg=-1.                                  \tag{1}
\]

The checker chooses `a=e=1`, giving the displayed Gaussian values.  Every
nonzero factorization of (1) has the same two common-core relations below.

The resulting pairings are

```text
010111 : 02|14|35  <->  03|14|25,
020002 : 04|15|23  <->  02|15|34,
022102 : 04|15|23  <->  03|15|24,
101000 : 02|13|45  <->  02|15|34,
101021 : 02|13|45  <->  02|14|35,
202220 : 03|15|24  <->  03|14|25.
```

The shared cell `34:00=1` closes two debts simultaneously, but adds the
pure-zero occurrence `02|15|34` of weight `-1`.  Hence the normalized
all-zero coefficient drops from `1` to `0`.  Two of the new chains likewise
add terms of weights `i` and `-i` to the old `L/R` rows.  This is the first
literal reason that singleton completion cannot be considered independently
of the normalized and boundary rows.

One integral closure is

```text
24:00 = 1,    35:00 = 1,
35:10 = -1,   24:02 = 1.
```

It restores the all-zero coefficient to `1`, restores both complete `L/R`
rows as four-term cancellations, and also closes the new boundary rows
`000020` and `000100`.  The other two constant-colour coefficients remain
`1`.

## Full second-layer ledger

The eleven cancelling mixed rows have occurrence histogram

```text
9 rows with 2 occurrences,
2 rows with 4 occurrences.
```

They are

```text
000020, 000021, 000100, 002100, 002121,
010111, 020002, 022102, 101000, 101021, 202220.
```

The two four-term rows split exactly into two primitive signed binomials.
Thus there are thirteen primitive binomial subrows in the displayed closed
part of the ledger.

The remaining supported mixed coefficients comprise 33 debts: 28 are
singletons and five have three occurrences.  Multiterm cancellation is
therefore present already at this second layer; the audit never assumes
that future source rows remain binomial.

## Recursive least-core audit

For every residual debt, enumerate every currently dead perfect matching
which differs by one `C4` from a live occurrence.  Discard a candidate only
when one of its newly required cells is both

```text
off the union of the three selected pure anchor matchings, and
off-diagonal in colour.
```

Every one of the 33 debts still has a candidate.  The histogram

```text
(number of anchor-contained C4 choices, least new cells) : number of debts

(1,2):2, (2,1):4, (2,2):5, (3,1):6, (3,2):3,
(4,1):5, (4,2):4, (5,1):2, (8,1):2
```

is frozen by the checker.

Each chosen symmetric-difference core is literally a four-cycle: it is
connected, degree two, matching-covered, and has exactly the two displayed
perfect matchings.  This is precisely the single-even-cycle branch of the
read-only U7H least-core theorem.  The imported theorem is useful here as a
canonical **within-fibre** classifier, but it supplies no relation between
the least cores of distinct colouring fibres.  The checker consequently
verifies the `C4` property directly and does not depend on unaudited code.

Taking, for every debt, the lexicographically first candidate using the
fewest new cells produces windows with empty total intersection.  This does
not claim that all 33 choices have simultaneously solvable scalar weights.
It proves the exact local negative statement: recursive least-core
classification alone does not force a common physical endpoint.

## Why the three proposed monotones stop

### Window intersection

The original three boundary windows already have empty intersection.  The
deterministic least-core choices for all 33 residual debts again have empty
intersection.  Intersection size therefore stays at its minimum rather
than improving toward a common star.

### Occupied-cell support

Every repair adds support or reuses an existing cell.  This is monotone in
the wrong direction: it is not a well-founded descent, and shared cells can
close several rows while reopening normalized or boundary rows.  The cell
`34:00` is the smallest exact example.

### Odd signed character

Form the decorated exponent-difference matrix of the thirteen primitive
binomial subrows.  Over `F_2` it has rank `10`.  Appending the all-ones row
still gives rank `10`.  Hence every integral exponent dependency has even
coefficient sum: an odd `(-1)` holonomy is impossible in this component.

This is stronger than finding no odd cycle in one chosen graph.  If an
integer dependency had odd signed length, its reduction modulo two would
contradict the all-ones row-space test.

## The two smallest recurrent components

Despite the absence of odd holonomy, the kernel has two literal length-two
recurrences.

### Tail `02`, bistar endpoints `15`

Rows `000021` and `101021` both contain the same core relation on window
`1345`:

\[
 (13{:}00)(45{:}21)+(14{:}02)(35{:}01)=0.             \tag{2}
\]

The `C4` shores are `{1,5}` and `{3,4}`.  Thus one may choose ordered
bistar endpoints `1,5`, with fixed port sites `3,4`.  The two complete
occurrence pairs differ only in the retained tail:

```text
row 000021 uses 02:00,
row 101021 uses 02:11.
```

Both exponent rows are identical and both cancellation characters are
`-1`, so their closed holonomy is `+1`.

### Tail `15`, bistar endpoints `02`

Rows `002100` and `022102` both contain the same core relation on window
`0234`:

\[
 (03{:}01)(24{:}20)+(04{:}00)(23{:}21)=0.             \tag{3}
\]

The shores are `{0,2}` and `{3,4}`.  Choose ordered bistar endpoints `0,2`
and fixed port sites `3,4`.  The retained tails are

```text
row 002100 uses 15:00,
row 022102 uses 15:22.
```

Again the decorated exponent rows agree literally and the length-two
holonomy is `+1`.

These are not merely matching-isomorphic flips.  Equations (2) and (3)
reuse the exact same four decorated cells along both paths.  Endpoint,
port, tail, and cofactor transport are therefore path-independent inside
each component.

Consequently there is a genuine restricted routing theorem:

> If all six debts of the 15-cell wandering packet are completed by one
> primitive `C4` occurrence each and the union of new decorated cells is
> support-minimal, then the completion necessarily contains both recurrent
> common-bistar cores (2) and (3), independently of the two scalar gauges.

This theorem allows the other complete rows to be multiterm.  What it does
not yet supply is a source-provenant operation which projects those complete
rows onto their already cancelling common-core subrows.

## The exact theorem still needed

The occurrence-level placement output is now concrete, but a future full
source may add arbitrary further terms to both rows.  One may not simply
discard those terms and call (2) or (3) a source identity.  The remaining
uniform statement is:

> **Complete-row recurrent-core projection theorem.**  Suppose two or more
> complete vanishing source rows contain a common primitive decorated `C4`
> exponent difference, with fixed bistar endpoints and path-independent
> tail/cofactor transport.  Then either a source-provenant linear
> combination projects the complete rows onto that common core, or the
> unprojected companion terms force an odd Laurent unit, an anchor-safe
> support deletion, or an active outside private-site fan.

The two length-two recurrences above are the smallest exact test cases for
this theorem.  U7H cannot prove it, because U7H is fibrewise and the load-
bearing assertion compares complete rows across two different colour
words.

## Scope

The 26-cell packet is not a Krenn source: its 33 residual mixed coefficients
are nonzero.  It is a finite exact boundary counterguard and a positive
placement certificate.  It rules out the three naive recursive monotones,
freezes every next least-core choice, and identifies the shortest remaining
route: prove the complete-row recurrent-core projection theorem at either
of the two displayed common bistars.

Run

```text
python3 computations/verify_uniform_primitive_c4_recursive_boundary_counterguard.py
python3 -O computations/verify_uniform_primitive_c4_recursive_boundary_counterguard.py
python3 -I -S computations/verify_uniform_primitive_c4_recursive_boundary_counterguard.py
```

The checker uses exact Gaussian-integer arithmetic, exhausts the `6^6`
first completion choices, expands all `3^6` word fibres, audits all residual
primitive completions, and freezes the signed exponent rank test.
