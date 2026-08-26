# Bosonic-Gaussian annihilator projection audit

Status: **terminal negative PASS**.  Projecting the formal Gaussian parent
equations onto the one-photon, hole, and collision sectors gives exactly the
ordinary Wick/Laplace recurrence.  Repeated commutators reproduce the frozen
site-down/carrier hierarchy and yield no new source-faithful clean-cap relation.

## 1. Exact coefficient recurrence

Let the 24 modes be `mu=(site,colour)`, let `A` be the symmetric block-off-
diagonal covariance, and put

```text
q = (1/2) sum_(mu,nu) A_mu,nu a_mu^dagger a_nu^dagger,
|A> = exp(q)|vacuum>.
```

The formal Bargmann identity is

```text
(a_mu - sum_nu A_mu,nu a_nu^dagger)|A> = 0.       (1)
```

For the derivative-normalized moment `M(m)`, the coefficient of any odd
occupation vector gives

```text
M(m+e_mu) = sum_nu m_nu A_mu,nu M(m-e_nu).        (2)
```

The factor `m_nu` is the canonical bosonic commutator multiplicity.  The
checker evaluates (2) exactly over Q for three deterministic N8 sectors:

- a seven-site one-hole state leading to a one-photon-per-site amplitude;
- a two-hole state with a distinct-colour double occupation;
- a two-hole state with a repeated-mode double occupation, where the
  multiplicity two is exercised literally.

All three identities pass.  The collision equations contain no new kind of
term: they are the same recurrence with occupation multiplicities and moments
of sectors not specified by the Krenn target.

## 2. Repeated annihilators are the site-down hierarchy

Write `L_mu=sum_nu A_mu,nu a_nu^dagger`.  Normal ordering `k` annihilators
against the Gaussian gives a sum over partial matchings of the `k` exposed
modes: every paired exposed pair contributes `A`, and every unmatched mode
contributes `L`.  The exact profiles by number of paired pairs are

| k | partial-matching counts |
|---|-------------------------|
| 1 | `1` |
| 2 | `1 + 1` |
| 3 | `1 + 3` |
| 4 | `1 + 6 + 3` |

Consequently, projection to distinct physical sites gives

```text
k=1: D_p q^[4] = l_p q^[3],

k=2: D_p D_r q^[4]
     = A_pr q^[3] + l_p l_r q^[2],

k=3: D_p D_r D_s q^[4]
     = (A_pr l_s + A_ps l_r + A_rs l_p) q^[2]
       + l_p l_r l_s q.
```

Direct enumeration of all 105 K8 perfect matchings gives exactly the frozen
source partitions:

```text
one exposed site:     105 crossing,
two exposed sites:     15 internal + 90 double-crossing,
three exposed sites:   45 internal/crossing + 60 triple-crossing.
```

Thus the two-annihilator layer is the existing full-nine/response-carrier
identity, and the third is the existing site-down `45+60` layer.  Four and
more annihilators continue the same partial-matching formula.  When exposed
colours and residual words are all retained, their coordinates simply
reindex the original 6,561 top coefficients, exactly as in the pinned zeon
module-rank theorem.

## 3. Purity adds no algebraic source equation

For every symmetric `A` in the analytic contraction ball, the normalized
state `exp(q)|0>` is already a pure Gaussian.  The covariance purity relation
is therefore an identity after substituting its rational formula in `A`; it
does not cut down the source parameter space.  Moreover it uses `A^dagger`,
positivity, inverse matrices, and normalizability, none of which are part of
the holomorphic polynomial membership problem over C.

Likewise, canonical commutators only generate the contractions already
visible in the Wick partial matchings.  A parent-Hamiltonian norm statement
would use discarded collision/hole sectors and complex conjugation; it cannot
be promoted to a holomorphic equation for the one-photon projection.

## 4. Exact controls

### N4

The exact three-matching GHZ4 witness is a bona fide Gaussian projection and
satisfies every identity above.  Hence no universal annihilator, commutator,
or covariance-purity identity can by itself contradict a GHZ target or force
a unique internal three-channel bottleneck.

### N6

The frozen unrestricted N6 theorem proves emptiness of the normalized target
coefficient fibre.  Equations (1)--(2) add no source row beyond those target
coefficients and their Wick re-expression, so they do not independently
recover the N6 unit certificate.  The coefficient cancellations, rather than
Gaussian purity, carry that theorem.

### N8 invisible chord and Laurent scope

For the colour-zero matching `01|23|45|67`, adjoining the chord `02` changes
the numbers of supported matching terms in divided powers `q^[1]` through
`q^[4]` by

```text
1, 2, 1, 0.
```

In particular the hole/collision and lower-power data change while the entire
one-photon-per-site top tensor remains fixed.  Both sources continue to obey
all annihilator identities.  This proves that introducing lower sectors does
not make them consequences of X5.

The frozen Laurent families supply the complementary analytic guard: they may
leave every fixed normalizability ball while their top projection approaches
GHZ.  Gaussian norm/purity compactness therefore cannot replace exact affine
source membership.

## Terminal verdict

The bosonic formalism is a faithful and useful repackaging, but its parent
equations are precisely Wick recurrence.  On the one-hot sector they are the
known Laplace/site-down/carrier rows; on collision sectors they introduce
unconstrained lower moments.  No canonical-commutator or Gaussian-purity term
escapes this hierarchy, so the route supplies no new global relation forcing
a clean pair.

## Replay

```sh
python3 computations/unaudited-codex-bosonic-gaussian-annihilator-2026-08-21/audit_bosonic_gaussian_annihilator.py --write-results
python3 -O computations/unaudited-codex-bosonic-gaussian-annihilator-2026-08-21/audit_bosonic_gaussian_annihilator.py
python3 -I -S computations/unaudited-codex-bosonic-gaussian-annihilator-2026-08-21/audit_bosonic_gaussian_annihilator.py
```

Frozen logical digest:
`221e1ad0eba30b5a3777fc8076fd2436351be0aef877e6c8478d0fdb6ab1b051`.
