# Source-labelled exchange cycles need a global boundary potential

## Outcome

The sharp one-bad repair process has no cycle through its first two direct
matching-exchange arrows.  The exact 168-chart theorem leaves a new private
mixed top word in every case.  At the first possible later return, cycle
parity gives a sharp but incomplete dichotomy:

1. an odd closed exponent circuit is an ordinary Laurent unit; but
2. an even matching-exchange square can close consistently and need not
   decrease the original fibre.

The second alternative is real, not a formal caveat.  The existing exact
rank-one feedback model has all three normalized pure coefficients, eleven
cancelling mixed binomials with one common nonzero Laurent row, and no odd
dependency.  It closes its local feedback while exporting one hundred
mixed singleton fibres.

Therefore there is no sound well-founded potential depending only on the
currently repaired fibre, its matching count, or its local alternating
cycle.  A global proof must order the complete boundary-fibre ledger (or
use a source identity coupling those fibres).

The exact audit is
`computations/verify_n8_one_bad_exchange_cycle_gate.py`.

## Primitive exchanges on the six-site residual

There are fifteen physical perfect matchings of six sites.  Among their
105 unordered pairs, 45 share one edge and differ on an alternating `C4`,
while 60 are disjoint and differ on an alternating `C6`.  From any fixed
matching there are six `C4` mates and eight `C6` mates.  This exactly
explains the second-arrow split:

```text
12 private words * 6 C4 mates = 72 two-new-cell charts,
12 private words * 8 C6 mates = 96 three-new-cell charts.
```

More generally, if two matchings differ on two disjoint alternating
components, their union contains the four independent component switches.
Such a fibre is not binomial.  Thus a genuine direct binomial repair is a
primitive single-component switch.

## Cycle parity

Orient a plus-binomial cancellation as

\[
                         x^{u_i}/x^{v_i}=-1,
 \qquad d_i=u_i-v_i.                                  \tag{1}
\]

For a closed exponent circuit `sum d_i=0`, multiplication of (1) gives

\[
                              1=(-1)^k.                \tag{2}
\]

Odd `k` is therefore an exact Laurent unit over characteristic zero.  Even
`k` has trivial sign holonomy and needs additional information.

The first independent physical diamond uses two disjoint alternating
`C4`s and hence eight vertices.  With

```text
M00 = 01|23|45|67,   M10 = 03|12|45|67,
M01 = 01|23|47|56,   M11 = 03|12|47|56,
```

one has the literal occurrence identity

\[
                 \chi_{00}+\chi_{11}=\chi_{10}+\chi_{01}. \tag{3}
\]

This is the commuting square: its four exponent rows telescope, but its
holonomy is `(-1)^4=1`.  It is a valid local diamond, not a contradiction.

## Why local maximality is not a potential

The pinned twelve-site feedback counterguard makes the even escape exact.
Its three pure fibres have `(size,coefficient)`

\[
                         (1,1),\quad(5,1),\quad(1,1),  \tag{4}
\]

and its mixed-fibre histogram is

\[
                       100\text{ singletons}+11\text{ binomials}. \tag{5}
\]

All eleven binomials cancel, and their signed exponent differences are the
same nonzero four-cycle circulation.  Any integer dependency among identical
nonzero rows has coefficient sum zero, so odd holonomy is impossible.  The
feedback can return without enlarging its tracked fibre; the obstruction has
simply moved into the one hundred other boundary words.

This model is not a Krenn counterexample.  It is a counterguard to promoting
the first- and second-arrow propagation into a global theorem using only
local fibre size or cycle parity.

## Precise next theorem

The viable global statement must use one of the following genuinely stronger
objects:

- a lexicographically ordered vector of singleton debts over **all** mixed
  words, proving every even commuting square lowers the first changed entry;
- the augmented signed exponent group of all currently binomial fibres,
  followed by one-class residual rows; or
- a full-nine/source-provenance identity transporting a local even square
  to a nonzero boundary coefficient.

The current checker does not enumerate a third one-bad support layer.  It
certifies the two-arrow no-return, identifies the first even physical
diamond, and freezes the exact obstruction that any proposed global
potential must defeat.

## Reproduction

```sh
uv run python computations/verify_n8_one_bad_exchange_cycle_gate.py
PYTHONOPTIMIZE=1 uv run python computations/verify_n8_one_bad_exchange_cycle_gate.py
```

Both modes freeze the ledger hash printed by the checker.
