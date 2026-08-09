# A diagonal target bridge cannot carry both bright images

## 1. Result

The product-incidence split after
[`the three-coordinate bright theorem`](shared-reciprocal-two-bad-three-coordinate-bright-coupling.md)
is unnecessary in the colour-diagonal chart.

> **Diagonal bridge support theorem.**  Let `q` be a colour-diagonal
> quadratic on five sites, and let a minimal target-line kernel bridge use
> sites `0,1`:
>
> ```text
> K_0=e_t^(1) tensor Z,       K_1=e_t^(0) tensor Z.
> ```
>
> If `X_t` is outside `im(Phi)`, then `im(Phi)` cannot contain both other
> pure tensors `X_a,X_c`.

This is an exact support theorem over every integral domain.  It does not
assume which two entries of the bridge occur in the nonlinear kernel
product, and it does not use the second kernel row at all.  Consequently it
closes the remaining one-bridge-site incidence as well as the same-pair
incidence in the diagonal chart.

Mixed-colour internal cells and kernel circuits on at least three sites
which do not contain a two-centre subbridge remain separate.

## 2. Why a non-target residual edge is mandatory

Minimality makes `Z` nonzero.  If `Z` were a scalar multiple of the pure
three-site target tensor, then inserting `e_t` at site `0` into `K_0`
would put `X_t` in `im(Phi)`.  Hence `Z` has a non-pure word.

Every word of a diagonal four-site matching has even colour multiplicity.
Since site `1` in `K_0` has colour `t`, a non-pure word has pattern

```text
t,t,d,d,       d in {a,c}.
```

Its unique matching uses a target-coloured `1-i` edge and a non-target
residual edge on the other two sites.  In particular, at least one
non-target residual cell is nonzero.

## 3. The exact support relaxation

Project sites `0,1` modulo `e_t` and retain only output words containing no
target colour.  The bridge-centred columns die, and target-coloured cells
cannot occur in any retained word.  Parity purification lets a preimage of
`X_d` be replaced by its `d`-coordinate part.  Thus the complete retained
problem depends only on, for `d=a,c`,

```text
s_d       = q_01(d,d),
u_d,i     = q_0i(d,d),       v_d,i = q_1i(d,d),
r_d,i     = q_jk(d,d),       {i,j,k}={2,3,4}.
```

The off-target rows of the bridge factorization give

```text
sum_i u_d,i r_d,i = 0,       sum_i v_d,i r_d,i = 0,     (1)
u_d,i r_e,i = v_d,i r_e,i = 0       for d!=e.           (2)
```

At support level, (1) forbids exactly one nonzero monomial in either sum;
zero or at least two terms are retained as potentially cancellable.
Equation (2) is a unique mixed matching and is imposed literally.

There are `2^10` raw supports per colour and exactly 370 survive these
one-colour tests.  Among their `370^2` pairs, 12,540 satisfy (2) and contain
the mandatory non-target residual edge.

For each pair, the checker enumerates the seven nonempty supports of the
projected bright preimage on sites `2,3,4` and reconstructs every literal
matching term.  A candidate is rejected only when

- its pure coefficient has no matching term; or
- some required mixed-zero coefficient has exactly one matching term.

A row with two or more terms is accepted without checking whether its
coefficients can actually cancel.  Therefore every genuine coefficient
solution maps into the accepted semantic relaxation; the relaxation never
discards a solution merely because a cancellation ratio was not sampled.

The exact census is

| semantic bright support | pairs |
|---|---:|
| neither colour | 10,018 |
| only `a` | 1,261 |
| only `c` | 1,261 |
| both | **0** |

This proves the theorem.

## 4. Load-bearing boundary

If the mandatory residual edge is deleted, the semantic statement is
false.  The checker freezes the four-cell support

```text
04:aa, 13:aa, 03:cc, 12:cc,
```

which supports `X_a` through the cofactor centred at site `2` and `X_c`
through the cofactor centred at site `4`.  Here `K_0=K_1=0`, so it is not a
minimal two-centre bridge.  This mutation shows exactly where minimality
and `X_t notin im(Phi)` enter the proof.

## 5. Consequence for the N=8 route

Together with colour-parity straightening, the theorem removes every
minimal two-centre kernel bridge from the diagonal five-site quotient,
with arbitrary multi-centre bright lifts and without a product-incidence
case split.  The next diagonal kernel can therefore be assumed to have
minimal support at least three.  Its target-axis scalar relation is the
next finite object to classify.

## 6. Reproduction

```sh
python3 computations/verify_shared_reciprocal_two_bad_diagonal_bridge_bright_support_exclusion.py
python3 -O computations/verify_shared_reciprocal_two_bad_diagonal_bridge_bright_support_exclusion.py
```

The checker uses only the Python standard library and runs a
solver-independent finite support audit; it does not enumerate coefficient
values.
