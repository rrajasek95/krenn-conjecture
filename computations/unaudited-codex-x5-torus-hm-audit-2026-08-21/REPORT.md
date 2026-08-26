# Site-colour torus and Hilbert--Mumford audit

Status: **exact covariance PASS; the proposed minimal-support reduction fails**.

## 1. Source torus

Let `M=Z^24`, with basis `e_(i,a)` for site `i` and endpoint colour
`a`.  The literal action is

```text
x_ij^(ab) -> lambda_(i,a) lambda_(j,b) x_ij^(ab),
wt(x_ij^(ab)) = e_(i,a)+e_(j,b).
```

Every term in the amplitude `F_w` is indexed by a perfect matching.  It
uses every site once, with colour `w_i` at site `i`, so every term has the
same character

```text
chi_w = sum_i e_(i,w_i).
```

The checker replays this on all `6,561*105=688,905` matching terms.  The
three pure characters `p_c=sum_i e_(i,c)` are independent.  Therefore the
normalization-preserving subtorus is

```text
T0 = intersection_c ker(p_c),
N(T0) = {u in Z^24 : sum_i u_(i,c)=0 for c=0,1,2},
dim T0 = 21.
```

A cocharacter basis is `e_(i,c)-e_(7,c)`, `i=0,...,6`.  The full 24-by-252
variable weight matrix has rank 24 and image-lattice index two: every column
has even total coordinate sum, while the stored odd-unicyclic 24-column
minor has determinant `+/-2`.  Its projection to `T0` has rank 21.

## 2. The 728 carrier conditions

For carrier pair `(p,q)`, response row `(ab:alpha,beta)`, and column `ij`,
both literal response summands have weight

```text
rho_(ab:alpha,beta) + kappa_(ij),
rho = e_(a,alpha)+e_(b,beta),
kappa = e_(p,i)+e_(q,j).
```

Thus `L(lambda.A)=D_rho L(A) D_kappa`.  The checker verifies all 680,400
entries of the 168 star and 560 triangle matrices.  The three diagonal
blockers have dual characters `-kappa_dd`; the direct blocker
`<K,A_pq>` is invariant.  Rank, row-span membership, and activity are
therefore invariant for torus elements.

They are **not closed across rank drops**.  The pinned exact curve has all
three pure Hafnians equal to one, but for carrier `(67, centre 0)` its
rowspace is `span(K00)` for `t != 0` and zero at `t=0`.  Its four membership
bits change from `[1,0,0,0]` to `[0,0,0,0]`.  Consequently neither one
unstratified membership condition nor the four-way no-cap union is closed.
Ordinary Hilbert--Mumford cannot be applied to that locus.

The chartwise repair is precise: retain a nonzero rank pivot for every
carrier and require its character to have one-parameter weight zero.  Then
rank and the chosen membership persist.  This repair does not, however,
produce the desired degeneration.

## 3. Exact rank-stratified cones

On generic full support, the cone is zero.  For each colour, sum the 28
nonnegative live-cell weights `u_(i,c)+u_(j,c)`.  The result is
`7 sum_i u_(i,c)=0`.  Hence every one of the 28 weights is zero.  The
unoriented incidence matrix of `K8` has rank eight, so every `u_(i,c)=0`.
This is the frozen rational Farkas countercertificate.  Adding the 728
pivot-character equations cannot enlarge the zero cone.

For each of the 310 frozen minimal diagonal records, the four anchor edges
give

```text
u_(2k+1,c)=-u_(2k,c)=-z_(k,c).
```

On superedge `kl`, a retained diagonal pair forces `z_k+z_l=0`; a retained
antidiagonal pair forces `z_k-z_l=0`.  The signed `K4` has a one-dimensional
solution exactly for the eight balanced masks

```text
11, 12, 18, 21, 33, 38, 56, 63.
```

The exact census is:

| stabilizer dimension | 310 orbit records | 275,568 labelled records |
|---:|---:|---:|
| 0 | 187 | 176,064 |
| 1 | 91 | 79,776 |
| 2 | 26 | 17,424 |
| 3 | 6 | 2,304 |

In every nonzero case, all 48 live source cells have weight zero.  These are
support-fixing stabilizers, not contracting directions.  Every nonzero
carrier pivot on such a support is built from weight-zero live cells, so its
character is automatically zero.  Rank-stratum preservation therefore
does not change the verdict: **none of the 310 records has a smaller toric
face reachable by an admissible nontrivial one-parameter subgroup**.

## 4. Scope and counterexample to a weights-only containment claim

The twelve common-anchor cells

```text
x_01^(cc), x_23^(cc), x_45^(cc), x_67^(cc), c=0,1,2
```

form an ambient minimal normalized torus-closed support: for each colour its
four projected weights sum to zero with positive coefficients.  It is not a
48-cell frozen-antichain record.  This is not an `X5` or no-cap
counterexample—the mixed pair-constant amplitudes are nonzero—but it is an
exact counterexample to the assertion that the character lattice alone
confines closed support faces to the 310 records.

Hence the torus theory does not supply the missing promotion from the closed
310 minimal strata to the full `e=t=0` component.  The next valid target is
a non-toric support-minimal degeneration/initial-ideal lemma compatible with
all fixed-rank carrier pivots, or a direct exact exclusion of larger-support
strata.

## Replay

```sh
python3 computations/unaudited-codex-x5-torus-hm-audit-2026-08-21/audit_x5_torus_hm.py --write-results
python3 -O computations/unaudited-codex-x5-torus-hm-audit-2026-08-21/audit_x5_torus_hm.py
python3 -I -S computations/unaudited-codex-x5-torus-hm-audit-2026-08-21/audit_x5_torus_hm.py
```

All three modes return logical SHA-256
`8ddc0cead9c8ec71b6091847319a053c8f1d3b275e19fb44c8280c716832b12c`.

