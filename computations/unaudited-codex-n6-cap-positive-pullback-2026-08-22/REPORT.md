# Six-site certificates, cap pullback, and Hermitian positivity

Status: **local positive identities exist, and a global Cauchy inequality
exists abstractly, but the frozen six-site proof does not yield a low-degree
common identity coupled to the attained eight-site minimum.  This archive
route is terminal without a new global polynomial certificate or a new
stationarity-to-clean-error estimate.**

## 1. What the certified six-site proof actually contains

The normalized six-site system has `135` endpoint-ordered source variables
and `729` cubic coefficient equations.  Its certified emptiness proof is not
a Macaulay/Nullstellensatz certificate.  It branches by the nineteen possible
rank-defect graphs and then uses:

- Boolean exact-support UNSAT and singleton-monomial clauses;
- free-rectangle minor identities on the saturated `C6` chart;
- primitive Laurent binomial lattices, 79 translated-fibre records, and
  signed one-class/trinomial contradictions;
- 32 exceptional-triangle rigidity/support blocks.

The branch artifacts record SAT/LRAT or semantic certificates, support
localizers, and integer exponent/sign checks.  They do not record polynomials
`Q_w` satisfying `1=sum Q_w F_w`, nor a degree ledger from which such
multipliers can be reconstructed cheaply.

## 2. Exact positive identities do exist chartwise

The simplest saturated-`C6` free rectangle has four literal mixed residuals

```text
F_ab = L X_ab + P_a Q_b,       a in {i,k}, b in {j,l},     (1)
```

where `L` is the product on the other two edges of one cycle matching and
`P_a Q_b` is the other cycle-matching monomial.  Direct fraction-free
elimination gives

```text
C := L(F_ij X_kl-F_il X_kj)
     -P_i(Q_j F_kl-Q_l F_kj)
   = L^2 det(X).                                           (2)
```

Therefore

```text
|C|^2 = |L|^4 |det(X)|^2.                                 (3)
```

This is exactly the desired local form: one Hermitian square equals a live
factor times the rank-activity measure.  It is source-faithful and requires
no positivity assumption on the complex source.

The phased six-site Fourier/anchor source gives an exact hostile replay on
the literal rectangle

```text
edge=01, rows=01, columns=01, tail colours on 2345 = 0010,
L=1, det(X)=-1+omega, C=-1+omega,
|C|^2=|det(X)|^2=3.
```

The Laurent branches also Hermitianize locally.  Two inconsistent signed
binomials have coefficient rows `(1,1)` and `(1,-1)`, whose Gram matrix is
`2I`.  The translated-trinomial conflict

```text
f=1+r+s,       g=1-r+s
```

has

```text
|f-g|^2=4|r|^2.
```

Thus complex phases are not, by themselves, the obstruction.  Fixed-chart
sign conflicts possess honest positive Gram certificates.

## 3. Why localizer-power summation is not valid

The proposed projective finite-cover maneuver is:

1. homogenize each chart identity in the cap covector `K`;
2. raise its nonzero localizer `ell_beta` to a common degree; and
3. sum `|ell_beta|^(2M)` times the identities.

The open localizers are not the main problem.  On an exact support stratum,
products of its required nonzero coordinates do cover the open part and can
be homogenized.  The problem is that the certified branches are **locally
closed**, not open: every identity also assumes that specified matching
monomials are absent because some source coordinates are exactly zero.

The smallest radical test passes exactly.  For the rectangle activity
`a=L det(X)`, the localizer ideal satisfies

```text
1 in <L> : (L det(X))^infinity.
```

Thus it covers that active locus after saturation.  The frozen artifacts do
not export one unified list of all branch localizers for a larger radical
calculation; more importantly, the mutation below shows that even the
strongest possible localizer cover would not validate the coefficient
identities away from their closed zero conditions.

Turning on an absent monomial does not make `ell_beta` vanish.  Hence the
old identity contributes with positive weight at points where it is false.
There is no polynomial support indicator that is nonzero when a coordinate
is zero and vanishes whenever that coordinate becomes nonzero.

The exact one-corner mutation is the smallest counterguard.  Start from (1),
turn on a third matching monomial `Z` only in the `ij` corner, and take

```text
L=1, P=(1,1), Q=(1,1), Z=1,
X=[[-2,-1],[-1,-1]].
```

All four mutated residuals vanish, while

```text
det(X)=1,       ell=L=1.
```

The old chart square is zero and its claimed right side is one.  Thus even
a unit localizer does not let that support-conditional SOS extend to the
neighboring support.  Multiplying it by higher powers of `ell` cannot help.

A full algebraic case-split compilation is still possible in principle.
One combines a zero branch with a localized-open certificate, clears a
power of its localizer, and recursively repeats through the finite tree.
But this is different from summing the existing identities.  Each case
combination raises degrees; repeated coordinate, minor, rank, and support
splits cause uncontrolled growth.  The frozen SAT/semantic artifacts contain
no compiled multiplier data.

## 4. The global Nullstellensatz certificate does exist

The branch incompatibility must not be overstated.  Since the normalized
six-site ideal has empty complex zero set, Hilbert's Nullstellensatz
guarantees a branch-independent identity

```text
1 = sum_w Q_w(y) F_w(y).                                  (4)
```

Consequently Cauchy gives the common positive inequality

```text
1 <= (sum_w |Q_w(y)|^2)(sum_w |F_w(y)|^2).                (5)
```

So commonization exists abstractly.  Generic effective bounds are only on
the singly-exponential scale `3^135` (up to the convention used in the
effective Nullstellensatz).  This number is a complexity scale, not a claim
that the minimal certificate has that degree.  Nothing in the archived
branch proof improves it to a usable degree.

## 5. Why (5) does not couple to minimum norm

For an eight-to-six cap, the effective source is

```text
y=x+r/s,
```

and pure normalization uses the factors `s/kappa_c`.  Pulling (4) back
therefore introduces high powers and inverse powers of

```text
s*kappa_0*kappa_1*kappa_2.
```

Near the inactive divisor, `Q_w(y)` can grow without bound and the residual
lower bound from (5) degenerates.  Normalizing projective `K` does not make
the active locus compact; it is the complement of those divisors.

More fundamentally, the block-normal/minimum-norm equations constrain the
original eight-site source.  They do not make the effective six-site GHZ
residual `sum|F_w(y)|^2` small for any cap.  The phased six-site source is a
smooth local norm minimum for its own output but has exact mixed residual
norm squared `1526`, while its local rectangle SOS is fully live.  This is
the required stationarity guard.

The remaining controls agree with the scope:

- exact `n=4` GHZ has all mixed amplitudes zero, a basic positive sanity
  check;
- W40 has six active star carriers but is only `X4`, so its missing higher
  equations carry the residual rather than force the N6 contradiction;
- W25 has no passing star or triangle carrier and is only `X3`, so every
  activity-weighted identity is vacuous there.

## Terminal verdict

There is a useful low-degree **chartwise** Hermitian identity, and global N6
emptiness guarantees an abstract global Nullstellensatz/Cauchy inequality.
But the certified branch proof cannot be combined by positive localizer
weights, does not furnish low-degree global multipliers, and supplies no
estimate connecting its effective N6 residual to the attained N8
minimum-norm equations.  Pullback of the existing N6 certificates therefore
does not close the proof spine.

## Replay

```sh
python3 computations/unaudited-codex-n6-cap-positive-pullback-2026-08-22/audit_n6_cap_positive_pullback.py --write-results
python3 -O computations/unaudited-codex-n6-cap-positive-pullback-2026-08-22/audit_n6_cap_positive_pullback.py
python3 -I -S computations/unaudited-codex-n6-cap-positive-pullback-2026-08-22/audit_n6_cap_positive_pullback.py
```

All modes return logical SHA-256
`26438fd7ee895dbfe227c03eac873518fa8c09113b4c657e93dee68d3dc21b3c`.
The hostile `--mutate-local-identity` run exits nonzero.
