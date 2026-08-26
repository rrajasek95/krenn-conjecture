# Inactive response kernels force an overlap dichotomy

Status: **UNAUDITED exact linear-algebra theorem plus two-prime source
replay**. This identifies why a fixed-pair full-nine attack stalls and gives
the first adjacent-chart invariant that sees the hostile kernel. It does not
finish either branch of the dichotomy.

## Fixed-pair invisibility

For a deleted pair `pq`, let `P,S:k^3 -> R_1(W)` be its two endpoint-star
maps and

```text
mu(K)=sum_ij K_ij P_i S_j in R_2(W).
```

On the five-set/pure-cofactor open of the preceding quotient-collapse
theorem, a corank-one blocked triangle yields a nonzero `K` with

```text
mu(K)=0,  K_00=K_11=K_22=0,  <K,A_pq>=0.              (1)
```

Contracting the nine full-pair equations by such a `K` gives `0=0`: the
response term, the direct term, and the three target terms all vanish.
Therefore no fixed-pair scalar elimination, regardless of Gröbner speed,
can detect this kernel. A different word or adjacent deleted pair is
mathematically necessary.

## The first adjacent coefficient

At a residual site `r`, write `P_r,S_r:k^3 -> V_r` for the incident blocks
and `P_hat,S_hat` for the stars with that site removed. Taking the
`V_r tensor R_1(W-r)` coefficient of `mu(K)=0` gives the literal overlap law

```text
sum_j (P_r K)_j tensor S_hat,j
 + sum_i (K S_r^T)_i tensor P_hat,i = 0.                (2)
```

If either incident block is invertible and the six projected star forms
`P_hat, S_hat` are independent, (2) forces `K=0`. Thus a nonzero inactive
kernel implies

```text
rank(P_hat + S_hat) <= 5                                (3)
```

at every residual site with an invertible incident block. The Rust checker
constructs `K`, verifies all 135 response equations and every coefficient
of (2), and records these ranks directly.

## Common subspace versus six-line split

Assume both incident blocks are invertible at all six residual sites, so
(3) holds everywhere. Put `P0=im(P)`, `S0=im(S)` in
`V=direct_sum_r V_r`.

For every `r`, the projected spaces intersect. If `P0 intersect S0=0`,
lifting a nonzero projected intersection gives a nonzero vector of
`(P0+S0) intersect V_r`. The six such vectors have disjoint support and
are independent. Since `dim(P0+S0)=6`, they form a basis and

```text
P0 + S0 = L_1 direct_sum ... direct_sum L_6,
L_r subset V_r a line.                                  (4)
```

Otherwise `P0` and `S0` have a genuine common subspace. This proves the
exact dichotomy

```text
common endpoint-star factor  OR  six physical port lines.         (5)
```

It is the recurring theorem shape behind the old common-factor/overlap and
six-port/reciprocal-cap routes; those are not unrelated ideas.

If the common intersection has dimension two and `mu` has corank one, its
kernel is exactly the alternating tensor of that common plane. Writing the
common-plane isomorphism as `phi`, the three equations `K_cc=0` force, **when
the common plane is not contained in a coordinate hyperplane**,

```text
phi = diag(lambda_0,lambda_1,lambda_2) on the plane.     (6)
```

Indeed, in a basis `x,y`, each equation
`x_c phi(y)_c-y_c phi(x)_c=0` says the two coordinate pairs are
proportional provided `(x_c,y_c) != (0,0)`.  If the common plane is the
coordinate plane `x_c=0`, the `c`-th equation is vacuous and the `c`-th
output coordinate of `phi` can be nondiagonal.  This exceptional stratum
was omitted in the first version of this report.  The direct equation in
(1) additionally says, on the generic-coordinate stratum, that
`A_pq diag(lambda)` restricts symmetrically to the plane. Thus the hostile
common plane is already target-label compatible; arbitrary `GL_3` alignment
is neither needed nor allowed.  The coordinate-plane stratum must be kept
as a separate boundary branch.

## Exact controls

At both primes 1009 and 1013:

- the good-star E1 control has one corank-one response kernel, it is
  inactive, the six adjacent block pairs all have ranks `(3,3)`, every
  punctured joint-star rank is four, the global joint rank is four, and the
  computed kernel is exactly the common-plane wedge;
- the dense-support E1 control lies on the omitted coordinate-plane
  exception: it has the same common-plane wedge, four invertible and two
  zero adjacent block pairs, but **no diagonal lift** of its common-plane
  isomorphism;
- W40/X4 has five inactive corank-one kernels, all on the six-line side
  (`global joint rank 6`), showing why support/rank boundary work is still
  needed;
- W25/X3 has six inactive corank-one kernels, split across global joint
  ranks five and six.

The good-star control is not an exact X5 source. Its role is to pin the hard
generic overlap geometry. The next valid lemma is now sharply localized:
use a second, source-labelled full-nine chart to exclude the
diagonal-compatible common plane (6), separately route the coordinate-plane
exception and (4) through the existing boundary machinery. A one-chart
Gröbner basis cannot supply that comparison.

## Replay

```sh
python3 computations/unaudited-codex-inactive-response-overlap-dichotomy-2026-08-22/check_results.py
```
