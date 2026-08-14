# The first repeated-site face has exact response cycles, not an `r0` landing

## Outcome

The first forbidden order-six coordinate

\[
            (01{:}11)\wedge(07{:}11)                 \tag{1}
\]

has an exact, source-provenant lift in each of the two response fine shifts.
Each lift uses only three quadratic-coefficient order-six operators, kills
the complete source and singleton Spencer faces, and exposes (1) with
coefficient one.  The two remaining second boundaries have `36` and `30`
literal coloured-cell-pair terms.

Neither lift is a boundary into the cap generator `r0`.  Both belong to the
response Spencer endomorphism block, with words `11111111` and `11211211`.
The cap belongs to word `01211222`, the selected `t*q_(v,N)`/`P3+K2` grade,
and operation type response-to-`AugP2`.  The first failure is therefore the
operation idempotent, before any cap `B/Eq` incidence can be tested.

Exact checker:
[`verify_h3_order6_first_forbidden_face_exact_seed_cycle_gate.py`](../computations/verify_h3_order6_first_forbidden_face_exact_seed_cycle_gate.py).

## The two exact cycles

Let `D0` denote the complete order-six source boundary, `D1` the singleton
coefficient-prolonging Spencer face, and `D2` the coloured-cell pair shadow.
Exact rational elimination gives homogeneous chains `Z_pure` and `Z_mixed`
such that

\[
 D_0Z=D_1Z=0,
 \qquad [D_2Z]_{01\wedge07}=1.                       \tag{2}
\]

Their frozen data are

| response word | raw seed columns | exact equation rank | operator terms | `D2` terms | forbidden terms | squared norm |
|---|---:|---:|---:|---:|---:|---:|
| `11111111` | 627 | 254 | 3 | 36 | 9 | 18 |
| `11211211` | 192 | 67 | 3 | 30 | 6 | 39 |

The pure weights are `-1/2, 1/2, 1`; the mixed weights are `1, 1, -1`.
Every selected operator contains both cells in (1), and all literal
quadratic-coefficient and six-direction labels are frozen in the checker.

This is stronger than knowing only that (1) occurs in the modular support:
it supplies an exact characteristic-zero preimage with all first proper
faces cancelled.

## How much the seed-containing family generates

Now retain all `819` raw homogeneous operators whose direction set literally
contains (1), not merely the six terms used in (2).  Repeating the complete
constrained-shadow calculation on this strongest literal seed-containing
family gives, at both primes `1,000,003` and `999,983`,

```text
constrained D2 dimension                         178
site-repeating coordinates hit                    84
rank of site-repeating projection                 76
direct-free intersection                         102.
```

The full `8,580`-column family has `159` site-repeating coordinates and rank
`153`.  Since the seed family is a literal subfamily, its modular quotient in
the full image has rank

\[
                           153-76=77.              \tag{3}
\]

It also misses `75` coordinate supports outright.  Thus merely closing
under all operators already containing the first face does not generate the
whole site-repeating target.  A further group/naturality orbit may enlarge
it, but that is a separate test; without such an orbit, (3) is a second
generator-type debt.

## Why the exact cycles still do not land in `r0`

The two fine shifts are the negatives of the pure and mixed response words:

```text
Z_pure   shift = -11111111
Z_mixed  shift = -11211211.
```

Their `D2` output is a codimension-two `P3/P4` coloured-cell-pair shadow.
The required cap section has instead

```text
word       01211222
fine       six t*q_(v,N) P3+K2 occurrence degrees
repeated   P3+K2
operation  response -> AugP2/K_Eq cap.
```

The current executable source-derived closure has

\[
       \operatorname {Hom}^0(\mathrm{response},\mathrm{cap})=0
\]

and no operation-changing first cell.  Differential, Hasse restriction,
and source naturality preserve the response endpoint.  Therefore the exact
cycles prove the existence of the repeated-site *response boundary*, not the
missing matrix unit `e_C A e_R` or a cap augmentation of it.

## Shortest next test

Compute the literal group/naturality orbit of both cycles in (2), retaining
word, fine, repeated and operation tags.  There are two possible outcomes:

1. its constrained site-repeating projection reaches rank `153`; then the
   coefficient support is generated from the two seeds, but a separate
   response-to-cap bimodule landing is still necessary;
2. it has smaller rank; then its quotient identifies the next independent
   collision/Tate generator type before the cap comparison.

In neither case can an internal response orbit itself change the operation
idempotent.

## Verification

```text
python3 computations/verify_h3_order6_first_forbidden_face_exact_seed_cycle_gate.py --mode all
python3 computations/verify_h3_order6_first_forbidden_face_exact_seed_cycle_gate.py --mode cycles
python3 computations/verify_h3_order6_first_forbidden_face_exact_seed_cycle_gate.py --mode span
python3 computations/verify_h3_order6_first_forbidden_face_exact_seed_cycle_gate.py --mode cap
python3 -O computations/verify_h3_order6_first_forbidden_face_exact_seed_cycle_gate.py --mode all
python3 -I -S computations/verify_h3_order6_first_forbidden_face_exact_seed_cycle_gate.py --mode all
```

The exact cycles are rational.  The `76/153` comparison is a matching
two-prime modular theorem, not a rational-rank promotion.

Frozen ledger SHA-256:

```text
534d40e41691b063fbe6cc4f9fb4ed5569b39bc3e048c90e33fb41a48de5ba94
```
