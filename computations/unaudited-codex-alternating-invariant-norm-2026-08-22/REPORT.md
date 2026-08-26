# Three-copy alternating invariant versus minimum norm

Status: **terminal equality no-go.**  The vertex-determinant expansion gives
clean source-relative norm bounds, but even the exact `n=4` global GHZ-fibre
minimum is strictly inside them.  Minimum norm on the fibre therefore cannot
force their equality case.

## 1. Source-relative bounds

Write `n=2m`, `r_e=||A_e||_F`, `nu_e=||A_e||_*`, and

```text
haf(q)=sum_(M perfect matching) prod_(e in M) q_e.
```

Choose an SVD rank factorization in the exact vertex-determinant expansion.
Hadamard at every vertex, followed by the triangle inequality over factor
labels, gives for each ordered matching triple

```text
|Phi_A(M1,M2,M3)|
  <= prod_(k=1)^3 prod_(e in Mk) nu_e.
```

Consequently the strongest simple block-weighted bound coming directly from
that expansion is

```text
|I_n(H(A))| <= haf(nu)^3.                                 (1)
```

Fixed-triple equality requires every contributing triple of incident
half-edge vectors to be orthogonal at every vertex and all determinant
products to have one phase.  Equality in (1) additionally requires these
conditions and phase alignment for every live ordered matching triple; a
triple whose nuclear-norm product is positive but determinant contraction is
zero already makes (1) strict.

There is also a stronger Frobenius bound when the summed output is retained.
Let

```text
K_n x = epsilon^(tensor n)(x,-,-).
```

The literal local contraction has `K_1^*K_1=2I`, hence
`K_n^*K_n=2^n I` and its exact flattening norm is `2^(n/2)=2^m`.  Cauchy and
the matching triangle inequality give

```text
|I_n(T)| <= 2^m ||T||^3,
|I_n(H(A))| <= 2^m haf(r)^3.                              (2)
```

Equality in the first inequality requires `K_nT` to be proportional to the
conjugate of `T tensor T`; equality in the second also requires all live
matching tensors to lie on one complex ray.

For `S=sum_e r_e^2` and `d=(n-3)!!`, AM--GM on each matching and incidence
counting give, for `m>=2`,

```text
haf(r) <= d m^(-m/2) S^(m/2),
|I_n(H(A))|
  <= 2^m d^3 m^(-3m/2) ||A||^(3m).                       (3)
```

The conversion (3) is deliberately labeled a corollary, not a sharp global
polynomial norm.

## 2. Sharp equality on the one-matching stratum

If only one perfect matching is live, the exact repeated-matching formula is

```text
I_n(H(A))=6^m prod_(e in M) det A_e.
```

Determinant Hadamard and energy AM--GM yield the sharp stratum bound

```text
|I_n(H(A))|
 <= (2/sqrt(3))^m (S/m)^(3m/2).                           (4)
```

Equality holds exactly when all live blocks are scaled unitaries and have
equal Frobenius energy.  At `n=4`, (4) is

```text
|I_4(H(A))| <= S^3/6.                                    (5)
```

Thus the sharp global source ratio is at least `1/6`, whether or not some
more complicated source makes it larger.

## 3. Exact controls

### Exact `n=4` GHZ global minimum

For a fixed pure colour, its coefficient is the sum of the three disjoint
matching products.  Cauchy gives

```text
1 <= (diagonal-cell energy for that colour)/2.
```

The three colours therefore force `S>=6`, and the standard three-matching
source attains `S=6`.  It is a genuine global minimum of the full GHZ fibre.
Exact replay gives

```text
I_4=6,       ||H||^2=3,       |I_4|/||A||^6=1/36.
```

This is six times below the one-matching value `1/6`.  It is also strict in
the flattening inequality: `36 < 2^4*3^3`.  In the vertex-determinant bound,
only six rainbow ordered triples contribute; the other positive-norm triples
have zero local determinants.

### Phased `n=6` block-injective local minimum

Exact Eisenstein replay gives

```text
S=63,       ||H||^2=1529,
I_6=24264+53604 omega,
|I_6|^2=2161483056.
```

Here `haf(r)=103` and `haf(nu)=85+180 sqrt(3)`.  Both (1) and (2) are strict;
in particular

```text
2161483056 < 2^6*1529^3.
```

### `n=8` Laurent border control

At `t=2`, the frozen source has

```text
S=57/4,       ||H||^2=11,       haf(r)=7,       I_8=6.
```

The support replay shows that no mixed output triple contributes to `I_8`,
so `I_8=6` along the whole Laurent arc.  Its source energy is

```text
S(t)=10+t^2+t^(-2).
```

Therefore `|I|/||A||^12 -> 0` as `t->0`, even though `H(A(t))->GHZ`.  The
border control is very far from equality, with `36 < 2^8*11^3` already at
`t=2`.

## 4. The logical gap is exact

On every exact normalized GHZ fibre point,

```text
I_n(H(A))=6.
```

Minimizing `||A||` therefore maximizes the invariant ratio **within that
fibre**.  It does not maximize the ratio over all sources, which is the
equality problem for (1)--(4).  The exact `n=4` global minimum is already a
counterexample to that inference: its ratio is `1/36`, while the elementary
scaled-unitary one-matching stratum reaches `1/6` and has non-GHZ output.

Hence no Hadamard/Cauchy equality theorem from this invariant can force a
clean or rank-one matching triple at a GHZ-fibre minimum.  A useful norm
argument would need a new *fibre-relative* inequality, not the global
operator norm of the alternating invariant.

## Replay

```sh
python3 computations/unaudited-codex-alternating-invariant-norm-2026-08-22/audit_alternating_invariant_norm.py --write-results
python3 -O computations/unaudited-codex-alternating-invariant-norm-2026-08-22/audit_alternating_invariant_norm.py
python3 -I -S computations/unaudited-codex-alternating-invariant-norm-2026-08-22/audit_alternating_invariant_norm.py
```

All modes return logical SHA-256
`3aeb5dbea0c2744aca10b893fc841a69e6501134110437aba07062a434b4bc7c`.
The hostile `--mutate-n4-minimum` run exits nonzero.
