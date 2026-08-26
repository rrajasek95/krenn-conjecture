# The frozen 62-word packet does not force triangle-carrier rank drop

Status: **UNAUDITED exact counterguard; full normalized `X5` remains open**.

## Sparse structural minor

Fix the canonical carrier with cap pair `67` and residual triangle `012`.
The edge `03` is not internal to the triangle, so its nine output-cell rows
are rows of `L_(67,012)`.  With

```text
P_r=A_6r,  Q_r=A_7r,
R_03(K)=P_0^T K Q_3 + Q_0^T K^T P_3,
```

define the degree-18 minor

```text
Delta_03 = det(Mat_3 -> Mat_3, K |-> R_03(K)).
```

At the source-faithful specialization

```text
P_0=I, Q_3=I, P_3=Q_0=0
```

the response is literally `R_03(K)=K`; hence `Delta_03=1` and
`rank L_(67,012)=9`.  This supplies a fixed, sparse structural rank-nine
minor rather than a generic/random determinant.

## Exact literal counterguard to the frozen packet

Keep `A_60=A_73=I` and activate only diagonal colour cells on the following
three perfect matchings:

```text
colour 0: 01,23,45,67
colour 1: 01,23,46,57
colour 2: 02,13,45,67.
```

Exact perfect-matching enumeration gives

```text
F_(0^8)=F_(1^8)=F_(2^8)=1,
F_w=0 for every one of the 62 closure22 + full-profile71 words,
Delta_03=1.
```

Therefore evaluation at this literal source annihilates the ideal generated
by the 62 amplitude rows and the three pure normalization rows but sends
`Delta_03` to one.  In particular `Delta_03` is in neither that ideal nor
its radical.  All of the frozen degree-13 closure22 translations vanish
there as well, so the abstract joint-semigroup packet cannot prove this
rank drop.  There is also a degree guard: the frozen translations live in
degree 13, whereas this determinant has degree 18.

## Precise remaining scope

This is not a normalized full-`X5` point.  Exactly 22 other mixed amplitudes
are nonzero: eight have profile `6+2`, six have profile `4+4`, and eight
have profile `4+2+2`.  Thus full `X5` could still force `Delta_03=0`, but
every proof excluding this guard must use at least one of those unlisted
rows (or a consequence that genuinely contains one).  None of the frozen
62-word/closure22 identities does.

The smallest honest next target is therefore the full-chart statement

```text
<all normalized X5 rows> : Delta_03^infinity = <1>,
```

or, before that broad test, a source-labelled reduction using the 22-row
guard packet.  Rank drop is not currently a consequence of the strongest
tractable frozen packet.

## Replay

```bash
python3 computations/unaudited-codex-triangle-rankdrop-prerequisite-2026-08-23/audit_triangle_rankdrop_prerequisite.py --check-results
python3 -O computations/unaudited-codex-triangle-rankdrop-prerequisite-2026-08-23/audit_triangle_rankdrop_prerequisite.py --check-results
python3 -I -S computations/unaudited-codex-triangle-rankdrop-prerequisite-2026-08-23/audit_triangle_rankdrop_prerequisite.py --check-results
```

Frozen logical digest:
`ea57f5fb8c98f6994af409090e349093797d13d5a8853ee94bdfa417886887ca`.
