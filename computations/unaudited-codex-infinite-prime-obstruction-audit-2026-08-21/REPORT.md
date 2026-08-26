# Infinite-prime obstruction audit

## Outcome

The arithmetic reduction is exact and potentially decisive, but none of the
existing odd-characteristic mechanisms supplies it.  For the normalized
integral source scheme, geometric emptiness over
`algebraic_closure(F_p)` for infinitely many primes would prove emptiness in
characteristic zero.  However, any certificate using one fixed Macaulay
degree and support at infinitely many primes already lifts to a rational
certificate.  The audited odd-prime identities are either local
counterguards, source gauges, finite-field rational-point searches, or a
`p`-dependent tautological rewriting of the original amplitudes.

Thus there is no new infinite congruence-class obstruction in the frozen
machinery.  The only genuinely different version of this route would be a
uniform family of `p`-dependent Nullstellensatz certificates proving
**geometric** emptiness over infinitely many `algebraic_closure(F_p)`.

## 1. Exact spreading-out theorem

Let

```text
I_Z = (all mixed amplitudes,
       F_00000000 - 1,
       F_11111111 - 1,
       F_22222222 - 1)
      subset Z[x_1,...,x_252].
```

Declared nonvanishing conditions may be included source-faithfully by
adjoining inverse variables.  This still gives a finite-type affine scheme
over `Z`.

**Proposition 1 (good-reduction direction).**  If the normalized scheme has a
point over `Qbar`, then it has a point over `algebraic_closure(F_p)` for every
rational prime outside a finite set.

Indeed, put the finitely many algebraic coordinates and declared inverses in
a number field `K`.  After inverting the finitely many primes supporting their
denominators, they define a point over an `S`-integer ring.  Reduction at any
prime of that ring gives a point over a finite residue extension, hence over
`algebraic_closure(F_p)`.  Every rational prime outside the finite set has a
prime above it.

**Proposition 2 (certificate direction).**  If the normalized scheme is empty
over `Qbar`, then it is empty over `algebraic_closure(F_p)` for every
sufficiently large prime.

By the weak Nullstellensatz and faithful scalar extension, `1` belongs to
`I_Z tensor Q`.  Clear the finitely many coefficient denominators in one
certificate to obtain a nonzero integer `N` in `I_Z`.  For every `p` not
dividing `N`, the reduction of `N` is a unit, so the reduced ideal is the unit
ideal.

Consequently

```text
empty over Qbar
  <=> empty over algebraic_closure(F_p) for all sufficiently large p,
```

and emptiness for merely infinitely many primes already implies the
characteristic-zero conclusion.

The word **geometric** is essential.  An exhaustive search over `F_p` rules
out only `F_p`-rational points.  It does not rule out points over finite
extensions or over `algebraic_closure(F_p)`.

## 2. Fixed-degree Macaulay torsion principle

Fix a Macaulay degree, a finite multiplier list, and a monomial basis.  Let
`M` be the resulting integer column matrix and `t` the integer target column.

**Proposition 3.**  If `t` belongs to the column span of `M mod p` for
infinitely many primes `p`, then `t` belongs to the column span of `M` over
`Q`.  Conversely, rational membership reduces to modular membership outside
a finite set of denominator primes.

For the nontrivial direction, if `t` is not in the rational span, linear
duality gives `y in Q^rows` with

```text
y M = 0,       c = y t != 0.
```

Clear denominators so `y` is integral and `c` is a nonzero integer.  Modular
membership forces `c=0 mod p`, so it can occur only at prime divisors of
`c`.  Equivalently, one may use a nonzero augmented rank minor or Smith
normal form.  The checker includes the exact model

```text
M = (1,1)^T,   t = (0,1155)^T,
```

whose rational membership fails and whose modular membership primes are
exactly `3,5,7,11`.

This also rules out a fixed bounded integer identity that holds only on an
infinite congruence class of odd primes: infinitely many reductions force the
same characteristic-zero identity.  A modular calculation at several primes
can still be extremely useful, but its role is rational reconstruction and
exact replay, not a logically separate infinite-prime theorem.

## 3. Audit of the existing odd-characteristic lanes

### 3.1 Six-boundary cap identity

The all-covector binary source in
`notes/odd-characteristic-six-boundary-barrier.md` is defined over `Z[1/2]`.
For pair `13`, exact source enumeration gives the unique cleared defect

```text
[101111] defect = -k10^2 k11.
```

Its coefficient is `-1`, so it survives every odd characteristic and every
extension field.  This is a genuine infinite-prime statement, but it points
in the wrong direction: it refutes a local rule asserting that every active
pair admits a clean nondegenerate cap.  The binary source has other clean
pairs, so the identity is not a global pair-selection obstruction and is not
a ternary `n=8` nonexistence theorem.

The independent checker here replays all `3^8=6561` ternary words for the
embedded binary source and derives the general-covector defect using sparse
polynomials over `Q`.

### 3.2 Odd-prime inverse hafnian

The reciprocity identity has complementary multiplicity `p-1`, so it does
escape the fixed-degree ceiling.  But equation (18) of
`notes/odd-prime-inverse-hafnian-tautology.md` is exact:

```text
complementary inverse hafnian for word c
  = one colour-independent scalar * original amplitude F_c.
```

This holds coefficient-by-coefficient to every order.  It reproduces the
original GHZ system and imposes no new constraint.

There is also a uniform source-faithful counterguard.  The integral `K4`
one-factorization realizes ternary GHZ over every field.  For every odd prime
`p != 3`, choosing the within-site diagonal `D=I` makes the first determinant
correction

```text
((p-1)/2)/2 * tr(A^2) = -3 mod p,
```

which is nonzero.  At `p=3`, negating one diagonal mode gives correction
`1`.  Thus no odd-prime argument may infer that this correction vanishes on
GHZ.  It is common to all three pure words and harmless.  This legal `n=4`
source is a method counterexample, not an `n=8` conjecture counterexample.

### 3.3 The characteristic-three slices

The joint-`C3` source reduction to `84` variables and `2187` equations is
exact inside that slice, and the seven supported-matching branches are
exhaustive for **`F3` assignments in that slice**.  The frozen log has not
terminalized the full search.  Even a terminal `F3`-UNSAT result would not
prove geometric emptiness over `algebraic_closure(F_3)`.

The twisted pure orbit work reduces `36` branches to `11` exactly, but again
only within its finite-field slice.  The character-twist construction is
exactly a site-colour diagonal gauge of the untwisted translation-invariant
slice, so its `512` character triples do not provide independent arithmetic
evidence.

### 3.4 Pfaffian and Frobenius ceilings

The transverse hafnian becomes the transverse Pfaffian at characteristic
two because signs disappear.  This does not extend to any odd congruence
class.  A fixed integral Pfaffian-derived relation valid modulo infinitely
many odd primes would already be a characteristic-zero relation by
Proposition 3 (or simply coefficientwise divisibility).

Frobenius can evade fixed degree only through exponents growing with `p`.
But equations such as `x^p-x=0` characterize `F_p`-rational coordinates, not
all points over `algebraic_closure(F_p)`.  A valid infinite-prime proof must
produce geometric ideal membership `1 in I_(F_p)`, not merely exclude points
over one finite base field.

## 4. Ranked verdict

1. **Exact positive reduction:** geometric emptiness for infinitely many
   primes proves characteristic-zero emptiness.
2. **Terminal result for current machinery:** no audited odd-prime identity
   supplies such emptiness.  Fixed-degree repetition would already be an
   exact rational certificate; the one `p`-dependent identity is tautological.
3. **Best operational use:** if a fixed Macaulay interface is tractable
   modulo several large primes, reconstruct its certificate over `Q` and
   replay it exactly.  This is stronger and finite.
4. **Only genuinely new arithmetic route:** construct a uniform,
   `p`-dependent family of Nullstellensatz certificates over infinitely many
   odd primes, with source-faithful proof that each certifies emptiness over
   the algebraic closure.  No such family is present in the current ledger.

## Replay

```sh
python3 computations/unaudited-codex-infinite-prime-obstruction-audit-2026-08-21/audit_infinite_prime_obstruction.py
python3 -O computations/unaudited-codex-infinite-prime-obstruction-audit-2026-08-21/audit_infinite_prime_obstruction.py
python3 -I -S computations/unaudited-codex-infinite-prime-obstruction-audit-2026-08-21/audit_infinite_prime_obstruction.py
```

All modes return logical SHA-256
`c7781ba342afbf441edf4f89b4ad8f280505c5d3b1deba4b0c4c16df335425b8`.
