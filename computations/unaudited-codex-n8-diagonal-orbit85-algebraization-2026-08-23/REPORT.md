# Orbit-85 DRAT algebraization feasibility audit

## Verdict

The shortest certified `N8-DIAGONAL` proof, orbit 85, **can be converted
mechanically and without re-solving into a characteristic-free polynomial-
calculus refutation of its Boolean clause polynomials**.  The load-bearing
fact is stronger than mere DRAT validity: `drat-trim -U` verifies the core with
zero RAT lemmas.  Its core LRAT has 41 additions, 1,731 ordered RUP hints, and
ends in the empty clause.  Reversing unit propagation gives 1,652 ordinary
resolution steps, five weakenings, and maximum intermediate width 45; the
standard clause-polynomial conversion therefore has a constructive PC degree
bound of 46.

This is **not** yet a Nullstellensatz certificate in the original diagonal
source rows.  It is a compact extended-ring proof that the support abstraction
is inconsistent.  The missing source interface is exactly the compilation of
the sound support clauses from literal amplitude/hafnian equations and the
subsequent elimination of selector and inverse variables.

## Selected case

Orbit 85 is smallest under both frozen measures:

```text
DRAT nonempty lines  1,076
DRAT bytes           11,291
case                  ((3,4,5),(3,4,5,6),(3,4,5,6))
case-orbit size       12
```

The checker rebuilds its CNF byte-for-byte from the certified encoder.  It has
5,592 Boolean variables (384 hafnian nonzero predicates `p`, 5,208 Laplace
witnesses `g`) and 13,905 clauses.

## Characteristic-free clause algebraization

For a Boolean variable `x`, define the falsity factor

```text
f(x)  = 1-x,       f(not x) = x.
```

A clause `C` becomes the polynomial

```text
M_C = product_(literal l in C) f(l) = 0.
```

This encoding and the proof conversion are sound over every field, including
characteristic two.  For a resolution pair `A or x`, `B or not x`, multiply
each clause polynomial only by the falsity factors missing from its side.  The
two products have the common factor `M_(A union B)` and their sum is

```text
M_(A union B) * ((1-x)+x) = M_(A union B).
```

All coefficients are `0,1,-1`; the identity remains valid in every
characteristic.  Weakening is multiplication by the newly added falsity
factors.  This also shows that Boolean axioms are not needed for the
resolution-derived unit identity itself, although they are included below in
the semantic selector interface.

The orbit-85 input counts are exact:

| quantity | value |
|---|---:|
| clause width histogram | `1:47, 2:11230, 3:1260, 4:840, 6:504, 8:24` |
| positive-literal histogram | `0:2093, 1:10444, 3:840, 5:504, 7:24` |
| maximum clause-polynomial degree | 8 |
| expanded clause-polynomial monomial occurrences | 48,901 |

For a clause with `r` positive literals the expansion has exactly `2^r`
distinct monomials.  The largest input clause polynomial therefore has 128
terms.

## Source-faithful selector/Rabinowitsch interface

Let `h` be the literal diagonal hafnian represented by a `p` atom, let `b=p`,
and introduce one inverse `u_h`.  Exact equivalence between `b=1` and `h!=0`
over a field is encoded by

```text
b^2-b = 0,
(1-b)h = 0,
b(h*u_h-1) = 0.
```

The first equation is part of the Boolean-axiom packet; the other two are the
hafnian link.  All `g` variables receive only their Boolean axioms and the
certified CNF constraints.  The resulting exact extended ring has:

| quantity | value |
|---|---:|
| diagonal source variables | 84 |
| Boolean selectors/witnesses | 5,592 |
| hafnian inverses | 384 |
| total variables | 6,060 |
| clause equations | 13,905 |
| Boolean axioms | 5,592 |
| hafnian-link equations | 768 |
| total equations | 20,265 |
| maximum input degree | 8 |
| total expanded monomial occurrences | 67,345 |

The 384 `p` atoms split by hafnian vertex-set size as
`0:3, 2:84, 4:210, 6:84, 8:3`.  Their hafnians contain 2,292 matching-monomial
occurrences.  The two link equations contribute 7,260 expanded monomial
occurrences; the Boolean axioms contribute 11,184.

## What the RUP conversion does and does not provide

The raw DRAT has 1,010 additions and 66 deletions.  Backward trimming leaves
41 core RUP lemmas.  The checker reconstructs every ordered unit-propagation
conflict and reverses it into a resolution chain; this is a proof conversion,
not a search.  A straight-line PC transcript, or a DAG-valued identity
tracking each input clause multiplier, is therefore routine to emit from the
frozen LRAT.

Expanding that DAG into one static sum could be much larger, so no compact
static support count is claimed.  More importantly, even the expanded result
would have the form

```text
1 = sum_C Q_C(b,g) M_C(b,g)
```

in clause selectors.  It would not have the desired form in the original
amplitude rows.  The SAT proof treats the clauses as axioms after proving them
semantically.  It does not provide polynomial multipliers showing, for
example, that every `A2`, Laplace, free-set, and case clause lies in the
appropriate localized source ideal.  Compiling those implications introduces
the `h` links and local inverses; eliminating them and gluing the support case
back into the direct diagonal quotient is the same extraction barrier found
in the package-wide audit.

Thus the bounded answer is:

- **yes** for a characteristic-free Boolean/selector PC certificate without
  re-solving;
- **no** for a literal source-row Nullstellensatz certificate without a new
  clause-provenance and elimination stage.

## Replay

```sh
python3 computations/unaudited-codex-n8-diagonal-orbit85-algebraization-2026-08-23/audit_orbit85.py
python3 -O computations/unaudited-codex-n8-diagonal-orbit85-algebraization-2026-08-23/audit_orbit85.py
python3 -I -S computations/unaudited-codex-n8-diagonal-orbit85-algebraization-2026-08-23/audit_orbit85.py
```

The checker uses the frozen repository `drat-trim`, requires `-U`, rejects any
negative/RAT LRAT hint, and writes its temporary LRAT outside the repository.
