# D0 exhaustiveness: bounded alternative-resultant audit

Status: **UNAUDITED**. This lane tests only whether one second raw
compatibility-pair resultant can remove the complementary quotient in the
frozen exact relation `R12 = E*Q`. It uses no new primes and no RUR.

## Alternative-pair result

After exactly the same pivot-gcd stripping as the frozen `R12` computation
(including only the certified `d4^2` content of compatibility 2), the proposed
pair `(1,3)` has zero `b0`-resultant at both existing primes
`1073741827` and `536870909`. Consequently `gcd(Q,R13)=Q`, all 14,350 terms.

The remaining raw pairs `(0,1),(0,2),(0,3),(2,3)` were screened at the first
prime only, as requested. Every resultant is zero. There is therefore no
second genuinely independent raw pair to cross-check at the second prime.

## Exact explanation of every zero resultant

Exact gcds over `Z[b0,d1,d4]` give two coprime irreducible 10-term factors
`A,B`, each of total degree 5 and multidegree `(3,2,2)`:

- compatibility 0 is `A*B*U0`;
- compatibility 1 is `A*U1`;
- compatibility 2 is `B*U2`;
- compatibility 3 is `A*B*U3`.

The exact ledgers are frozen in
`results_d0_alternative_resultant_gcd.json`. The reduced rows have respectively
200, 471, 471, and 491 terms. Both `gcd(A,pivot)` and `gcd(B,pivot)` are 1,
and `gcd(A,B)=1`. The gcd of all four primitive compatibilities has `b0` degree
zero exactly and at both primes, so there is no hidden all-row common factor.

Although `A` and `B` are individually nonlive, their intersection is entirely
on the pivot boundary. Exact characteristic-zero msolve on
`<A,B,z*pivot-1>` returned literal `[-1]:` in 0.01 seconds.

## Remaining exhaustiveness gap

On the pivot-open chart the exact factor pattern reduces the source scheme to
three cases:

1. `A=0, U2=0`;
2. `B=0, U1=0`;
3. `A,B != 0` and `U0=U1=U2=U3=0`.

These are a smaller, exact residual decomposition; this lane does not close
them. Hence the earlier exact characteristic-zero closures of the two
degree-21 factors remain valid, but `E=F0F1` is still only a proven divisor of
one resultant—not the full saturated D0/C0-open projection.

The finite-field/exact-factor artifact has logical digest
`78fe44e449579283ff65a25dcc04ae3a1c6a923dad7250154412c6591431ee3a`.
The exact audit is stable under `std`, `-O`, and `-I -S`, with digest
`78d0f68127380ad28ea5f762b7828ed003d37c6b6457672dd35b8a958ed116a3`.
