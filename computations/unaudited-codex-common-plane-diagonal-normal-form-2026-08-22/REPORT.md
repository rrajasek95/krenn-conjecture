# Common-plane diagonal normal form: exact generic/boundary split

Status: **UNAUDITED exact linear algebra plus two-prime source replay**.
This corrects an overstatement in the preceding inactive-overlap report.
It does not prove that an exact `X5` point enters the response-corank-one
branch.

## Result

For a cap pair `pq`, write its endpoint-star maps as

```text
P,S : k^3 -> direct_sum_(r notin {p,q}) V_r.
```

Suppose `im(P)` and `im(S)` meet in a plane, the response multiplication
has the corresponding one-dimensional alternating kernel `K`, and the
three diagonal blockers vanish on `K`.  Choose a basis `x,y` of the source
plane `U` and write the common-plane isomorphism as `phi`.  Then

```text
x_c phi(y)_c - y_c phi(x)_c = 0,  c=0,1,2.             (1)
```

If `U` is not a coordinate plane, every coordinate functional is nonzero
on `U`, so (1) gives a unique diagonal matrix

```text
D=diag(lambda_0,lambda_1,lambda_2),  phi=D|U.           (2)
```

Since `U` is a plane, it is the kernel of one covector `n`.  The literal
endpoint stars consequently satisfy the rank-one normal form

```text
P_i - lambda_i S_i = n_i L                            (3)
```

for one physical star form `L`.  Site by site this is

```text
A_pr[i,*] - lambda_i A_qr[i,*] = n_i l_r[*].           (4)
```

The direct-pair inactivity equation is exactly the assertion that
`A_pq D` restricts symmetrically to `U`.  The Rust checker extracts `D,n,L`
and verifies (3), every physical coordinate of (4), and the direct symmetry
at primes 1009 and 1013.

## Load-bearing exception

If `U` is the coordinate plane `x_c=0`, the `c`-th equation in (1) is
identically zero.  The `c`-th output coordinate of `phi` can then be
nondiagonal, so a diagonal lift need not exist.  The exact abstract guard

```text
U=<e0,e1>,  phi(e0)=e0+e2,  phi(e1)=e1
```

has a zero-diagonal alternating kernel and no diagonal `D` restricting to
`phi`.  This is a genuine boundary stratum, not a proof artifact.

The two source controls separate the cases exactly at both audit primes:

- `good_star_E1_block`: one generic-coordinate case, one diagonal lift,
  one verified rank-one defect and direct symmetry;
- `dense_support_E1_block`: one coordinate-plane case and no diagonal lift.

Thus the correct adjacent-chart attack has two inputs, not one:

```text
generic common plane: P-SD=n tensor L;
coordinate exception: separate support/rank boundary.
```

The next genuinely new equation must compare (4) for two adjacent cap
pairs.  Reapplying the fixed-pair full-nine rows cannot help: contraction by
the inactive kernel is identically zero.

## Replay

```sh
python3 computations/unaudited-codex-common-plane-diagonal-normal-form-2026-08-22/check_results.py
python3 -O computations/unaudited-codex-common-plane-diagonal-normal-form-2026-08-22/check_results.py
python3 -I -S computations/unaudited-codex-common-plane-diagonal-normal-form-2026-08-22/check_results.py
```
