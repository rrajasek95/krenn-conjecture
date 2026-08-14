# Independent audit of exact clean-pair descent

## Verdict

**PASS**, for the intended induction scope `|B| >= 8`, with
`U=B-{p,q}` and `|U|=2h`.  The proof in
[`clean-pair-cap-exact-descent.md`](../proofs/clean-pair-cap-exact-descent.md)
is mathematically sound.  The cap partition, powers of `s`, divided-power
factorials, endpoint order, one-site normalization, and finite decorated
lift all check independently.

Independent checker:
[`audit_clean_pair_cap_exact_descent_independent.py`](../computations/audit_clean_pair_cap_exact_descent_independent.py).
It pins but does not import the submitted checker.

## 1. Cap partition

For a matching `M` on `B`, let `mate_M(v)` denote the partner of `v`.
Exactly one of the following holds:

```text
mate_M(p)=q;
mate_M(p)=a and mate_M(q)=b for distinct a,b in U.
```

In the second case the ordered pair `(a,b)` retains which boundary endpoint
is attached to the `p` slot and which is attached to the `q` slot.  Removing
the displayed cap edges leaves a unique perfect matching of the remaining
sites.  Conversely, the tail matching and this ordered attachment reconstruct
`M`.  Thus the partition is bijective.

For `|U|=2h`, its counts are

\[
 (2h-1)!!
 \quad\text{and}\quad
 \binom{2h}{2}\,2\,(2h-3)!!,
\]

whose sum is `(2h+1)!!`, the number of matchings on `B`.  The audit checks
the bijection at orders `4,6,8,10,12` in both a monotone and non-monotone
ordering of `(p,q)`.

The coefficient-level test is stronger.  It reconstructs universal
endpoint-ordered edge variables and the ordered cap variables from scratch,
then compares

\[
 K\mathbin{\lrcorner}H_B(A)
     =[(s+r)\exp(x)]_U                                  \tag{1}
\]

for every ternary boundary word:

- every one of the `30` ordered cap pairs at six sites; and
- the non-monotone cap `(p,q)=(6,1)` at eight sites.

This explicitly catches a row/column transpose: the `K` slots remain
`p` then `q` even when the canonical storage order of an edge is reversed.

## 2. Factorials and powers of `s`

Fix a perfect matching of `U` and mark `k` of its `h` edges as effective
`r` edges.  On the left of

\[
 s^hH_U(x+r/s)
 =s^{h-1}K\mathbin{\lrcorner}H_B(A)+{\cal E}_{p,q}(K), \tag{2}
\]

the fixed typed matching has `h!` orderings in the exponential numerator
and denominator `h!`, hence coefficient one and scalar power `s^(h-k)`.

On the right:

- `k=0` comes from `s^(h-1) s exp(x)`;
- `k=1` comes from `s^(h-1) r exp(x)`; and
- `k>=2` comes from
  `s^(h-k) r^k x^(h-k)/(k!(h-k)!)`.

For the last case a fixed typed matching occurs

\[
                  k!\,(h-k)!
\]

times in the two powers, so both factorials cancel exactly.  Its coefficient
is one and its scalar power is again `s^(h-k)`.  The checker verifies every
`k` through `h=9`, including

\[
 {cal E}_{p,q}={s r^2x\over2}+{r^3\over6},
 \qquad 6{cal E}_{p,q}=3sr^2x+r^3
\]

at the eight-to-six boundary.

This closes a real coverage weakness in the submitted checker: its uniform
loop checked the `s` exponents and typed-term counts, but did not itself
compute the factorial multiplicities asserted in its docstring.  The
theorem's factorials are correct; the independent checker supplies the
missing verification.

## 3. One-site normalization

From cleanliness and the exact target,

\[
 H_U(y)=\sum_{c=0}^2{\kappa_c\over s}X_c^U.
\]

Choose `u0 in U` and act on its colour-`c` endpoint by `s/kappa_c` in every
incident block.  Every perfect matching has exactly one edge incident with
`u0`, so every word coefficient is multiplied exactly once, by the factor
belonging to its colour at `u0`.  Pure coefficients become one and mixed
coefficients remain zero.

The independent checker constructs arbitrary asymmetric rational blocks on
six sites and checks all `3^6` words before and after the endpoint action.
It covers both cases in which `u0` is the first stored endpoint and those in
which it is the second.  It then checks the symbolic pure/mixed normalization
on all `3^6` words for nonzero rational `s,kappa_0,kappa_1,kappa_2`.

## 4. Decorated lift

For each ordered endpoint coefficient of a transformed aggregate block,
introduce one decorated source with that endpoint-colour pair and weight.
Aggregation then recovers the block entry by entry.  The independent checker
performs this construction for asymmetric rational `3 x 3` blocks, omits
actual zero coefficients, and compares the aggregate and decorated matching
tensors on every word.

There are at most

\[
                         9\binom{|U|}{2}
\]

sources.  No endpoint symmetry is imposed.  Every introduced colour is one
of `0,1,2`; conversely, the nonzero coefficient of each pure target word
implies that at least one nonzero matching term, and hence at least one
nonzero source, uses that colour.  The palette is therefore exactly ternary.

## 5. Scope and minor presentation issue

The theorem proves only

```text
active clean cap  ->  exact ternary source on B-{p,q}.
```

It does not prove existence of the active clean cap.  No positivity,
genericity, symmetry of endpoint colours, or termwise inference from a
cancelling sum is used.

The standalone proof page uses `h` without locally writing `|U|=2h`, and
its theorem paragraph does not repeat the inherited `|B|>=8` induction
hypothesis.  Read in the repository's stated descent scope these are
editorial omissions, not mathematical defects.  Defining `h=|U|/2` in the
standalone statement would make it self-contained.

## Verification

```text
python3 computations/audit_clean_pair_cap_exact_descent_independent.py
python3 computations/audit_clean_pair_cap_exact_descent_independent.py --mode partition
python3 computations/audit_clean_pair_cap_exact_descent_independent.py --mode factorials
python3 computations/audit_clean_pair_cap_exact_descent_independent.py --mode normalization
python3 computations/audit_clean_pair_cap_exact_descent_independent.py --mode lift
python3 -O computations/audit_clean_pair_cap_exact_descent_independent.py
python3 -I -S computations/audit_clean_pair_cap_exact_descent_independent.py
```

Frozen ledger SHA-256:

```text
8dc02500a03a1c317fae9aeb81e0f4487719ceda412ae11e1654a0d6600e5d2f
```
