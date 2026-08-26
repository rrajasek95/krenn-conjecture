# D0=0, C0!=0 pivot-chart eliminant audit

Status: **UNAUDITED**.  This lane independently rebuilds the four Cramer
compatibilities from the six literal residual rows and works only on the open
chart where the selected rows `(1,4)` coefficient minor is nonzero.  It does
not cover the pivot-zero complement.

## Exact interface audit

The upstream exact interface was rebuilt with the venv Python/SymPy stack.
After the four upper cofactors, `D0=0`, and the two endpoint cofactor solves,
the remaining literal rows

`t_012,t_013,t_023,t_123,cofactor_0_3,cofactor_5_3`

are linear in `(a0,a5)`.  Rows `(1,4)` give a 320-term nonzero coefficient
minor.  The other four augmented minors have respectively
`2572,2217,2217,4473` terms.  Every msolve input in this lane contains these
four fully expanded minors followed by the fully expanded 320-term pivot as
the final native `-S` row.  There are no parentheses or Rabinowitsch parsing
shortcuts.

## Modular elimination and exact factor reconstruction

At primes `1073741827` and `536870909`, staged native saturation followed by
one-variable block elimination gives the same structural result:

- saturated DRL basis: 37 elements;
- elimination basis: 29 elements;
- unique `b0`-free row: 450 terms, total degree 42, multidegree
  `(d1,d4)=(34,14)`;
- factorization: two distinct multiplicity-one factors, each irreducible at
  both primes, with 126 terms, degree 21 and multidegree `(17,7)`.

The two factor supports agree coefficient-for-coefficient across the primes.
Height-bounded CRT/rational reconstruction gives primitive integral factors
`4 F1` and `8 F2`, with maximum reconstructed numerator 2655, and the exact
involution

`8 F2(d1,d4) = -d4^7 (4 F1)(-d1,1/d4)`.

The standard, optimized, and isolated exact reconstruction runs have the
stable logical digest
`b2c190b9dd80d9290d79c419b1034a3a02cc3b995064e2c3fe7f644fe82375a9`.
Irreducibility of each primitive factor over Q follows from either good
irreducible modular reduction.

## Exact resultant evidence and scope

After removing the exact visible pivot gcds from the two only compatibilities
whose pair resultant is nonzero, the integer resultant in `b0` has 19,969
terms, degree 538 and `(d1,d4)` multidegree `(324,222)`.  The reconstructed
450-term product divides it exactly over Z: the quotient has 14,350 terms,
degree 496 and multidegree `(290,208)`, with zero remainder.
The exact checker also verifies that the `E+1` mutation has nonzero remainder;
its logical digest is
`a799429876d35b0ba68342d438f7e38183a9adf1c8f8b28681d67052c26fd2dc`.

This exact divisibility identifies the reconstructed product as a genuine
characteristic-zero resultant factor.  It does **not** by itself prove that
all source solutions lie on that factor: a common root may instead lie on the
large quotient factor.  An exact saturated elimination certificate or a
direct source replay on the two factors is still required for that stronger
statement.

## Multi-prime/source-replay status

An unfactored third-prime staged elimination at `536870879` completed
saturation but timed out after 1800 seconds in block elimination without
serializing a basis.  Its valid full saturated basis was retained.  Adding one
reconstructed factor at a time to a full saturated basis and eliminating is
cheap (about half a second); repeating the pivot saturation after restriction
is also cheap and produces a stable 22-row component normal form.

This componentwise calculation was repeated at five primes
`1073741827,536870909,536870879,536870869,536870849`.  On the two factors the
reduced linear relations have stable `(A,B)` supports `(271,417)` and
`(271,432)`.  Nevertheless rational reconstruction at the five-prime unique
height bound still fails on `(115,161)` coefficients for the first branch and
`(110,160)` for the second.
Since `A(0,0)=1` is the fixed normalization, these entries are already ratios
to a stable nonzero coefficient.  A deterministic simultaneous-LLL/common-
denominator scan (subset dimensions 4/6/8/10/12, four offsets, numerator
weights through `2^160`, with every candidate tested on the full 688/703-entry
vector) finds no globally unique common denominator.  The three-mode-stable
height audit digest is
`d8eaa4bb4d35c1d3b907e73ee58f18fb628274186f47accaba2ebdfff9afd542`.
This is a coefficient-height/compression blocker only; it is not evidence
against characteristic-zero lifting.  `audit_d0_branch_relations.py` remains
a staged exact source checker, but no exact source-component theorem is claimed
until all of its coefficients reconstruct and its four determinant replays
vanish exactly.

## Toolkit referee notes

The shared runner correctly rejects parentheses, stages native `-S` before
`-e`, records source/input hashes and proof scope, and passes the required
`<x,z*x-1> -> [1]` regression.  Two defects found here were repaired:

- resource telemetry now tolerates sandbox denial of nested `ps`;
- input and basis characteristics now pass a deterministic 64-bit primality
  test, with a composite-modulus must-fire regression.
- standalone basis/saturation runs have an explicit `--full-basis` option;
  this is needed to reuse a saturated basis for later exact component
  restrictions without relaunching full elimination.

Both the system-Python and venv toolkit self-tests pass after these guards.
