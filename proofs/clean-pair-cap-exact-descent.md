# Exact clean-pair descent

## Theorem

Let an exact ternary aggregate source on an even site set `B`, with
`|B|>=8`, have matching tensor `Delta_B`. Choose two sites `p,q`, put
`U=B-{p,q}`, write `|U|=2h`, and let `K` be a cap covector. Define

```text
s = <K,A_pq>,
R_ab = K |-(A_pa A_qb + A_pb A_qa),
r = sum_ab R_ab,
x = sum_ab A_ab  on U.
```

If the three pure cap coefficients `kappa_c=<K,e_c e_c>` and `s` are
nonzero, and the homogeneous cap error

```text
E_pq(K) = sum_(k=2)^h s^(h-k) [r^k/k! exp(x)]_U
```

vanishes, then there is a finite endpoint-coloured ternary source on `U`
whose matching tensor is exactly `Delta_U`.

This theorem is conditional on the existence of the active clean cap. It
does not assert that every exact source has one.

## Proof

Every perfect matching of `B` lies in exactly one of two classes:

1. it contains `pq`, contributing `s[exp(x)]_U`; or
2. it sends `p,q` to two distinct sites `a,b` of `U`, contributing
   `R_ab` times a matching of `U-{a,b}`.

Therefore, with endpoint order retained,

```text
K |- H_B(A) = [(s+r)exp(x)]_U.
```

Set `y=x+r/s`. Expanding one effective edge per pair gives

```text
s^h H_U(y) = s^(h-1) K|-H_B(A) + E_pq(K).
```

The power of `s` on a matching using `k` effective `r` edges is `h-k` on
both sides: the cap term supplies `k=0,1`, and `E_pq` supplies `k>=2`.
Consequently `E_pq(K)=0` implies

```text
H_U(y) = (1/s) K|-Delta_B
       = sum_c (kappa_c/s) e_c^(tensor U).
```

At one site of `U`, multiply the colour-`c` endpoint of every incident
block by `s/kappa_c`. Every perfect matching uses exactly one such block,
so the resulting matching tensor is `Delta_U`.

Finally expand every effective block in the ordered endpoint basis. Each
nonzero coefficient becomes one decorated source. This uses at most
`9*binom(|U|,2)` sources, retains arbitrary complex coefficients and
endpoint asymmetry, and uses exactly the three colours because each pure
target coefficient is one.

## Verification

The independent checker
[`verify_clean_pair_cap_exact_descent_symbolic.py`](../computations/verify_clean_pair_cap_exact_descent_symbolic.py)
does two things not covered by the older lightweight ledger:

- it expands every one of the `3^6` boundary words at `N=8` and compares
  all `3^6 * 105 * 9 = 688,905` universal endpoint-ordered cap monomials;
- it checks the denominator-cleared canonical-error identity on every typed
  perfect matching through half-order six.

Run:

```text
python3 computations/verify_clean_pair_cap_exact_descent_symbolic.py
python3 -O computations/verify_clean_pair_cap_exact_descent_symbolic.py
python3 -I -S computations/verify_clean_pair_cap_exact_descent_symbolic.py
```

The separate checker
[`audit_clean_pair_cap_exact_descent_independent.py`](../computations/audit_clean_pair_cap_exact_descent_independent.py)
rebuilds the cap partition, factorial cancellation, endpoint ordering,
one-site normalization, and decorated lift from scratch. Its report is
[`clean-pair-cap-exact-descent-independent-audit.md`](../notes/clean-pair-cap-exact-descent-independent-audit.md).
The theorem is therefore status `[P]`.

Frozen ledger SHA-256:

```text
936d7ace3b705d088360812cc5bd30cbe85d1a0557f4a54329af0bf4042966d7
```
