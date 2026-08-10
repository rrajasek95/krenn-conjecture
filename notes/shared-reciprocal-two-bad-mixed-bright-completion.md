# The first mixed transgression has one direct bright completion

## 1. Exact bounded verdict

Start from the first mixed-parity kernel circuit on five common sites,
with `{a,c,t}={0,1,2}`:

```text
12:aa,  34:cc,  02:ta,
U=e_t@0-e_a@1 in ker(Phi).
```

Among the nine ways to complete the displayed `12:aa` and `34:cc`
matching leaders by one further pure edge each, exactly two preserve the
tilted bridge.  They are exchanged by `3<->4`; a representative is

```text
12:aa, 34:cc, 02:ta, 01:cc, 03:aa.                 (1)
```

For (1), `X_a,X_c` lie in `im(Phi)`, `X_t` does not, and

```text
rank(Phi)=11,  dim ker(Phi)=4.
```

Thus the bright equations do not kill the incoming mixed differential.
But the completion forces `K_3=0`: after deleting site `3`, site `4` is
isolated.  The first mixed correction therefore lands on a smaller
one-centre cofactor-kernel boundary, rather than producing the nonlinear
missing pure class.

## 2. Complete kernel-product check

The checker adjoins every column

```text
P*U'*V'*q,  P in direct_sum_x V_x,  U',V' in ker(Phi),
```

to the literal common-cofactor image.  This raises the rank from `11` to
`13`, but its intersection with the three-dimensional pure target space is
still exactly

```text
span{X_a,X_c}.
```

In particular `X_t` is absent even from the stronger linear span of all
kernel products.  This is stronger than checking one chosen nonlinear
product, although it is still only a theorem on the displayed chart.

## 3. The first activation of the dead cofactor

There are `85` possible new endpoint-coloured coordinates outside (1).
Requiring simultaneously

1. the same tilted bridge,
2. both bright pure classes,
3. `X_t` outside `im(Phi)`, and
4. all five cofactors nonzero

leaves exactly the nine coordinates

```text
04:rs,  0<=r,s<=2.                                  (2)
```

Every other physical activation either breaks the bridge, contaminates a
bright lift, or loses the required image pattern.  The nine six-cell
families have exact rank data

```text
(rank Phi, nullity Phi, augmented rank)
  (12,3,23) x1
  (13,2,17) x2
  (13,2,22) x2
  (14,1,16) x4.
```

In all nine cases the augmented pure intersection remains
`span{X_a,X_c}`.  This includes `04:tt`, the first coordinate which could
itself serve as the residual `tt` edge of a pure kernel-product monomial.
For `04:tt`, the only cofactor-kernel direction is still the tilted bridge,
so its square retains an `a` endpoint and cannot make `X_t`.

The six cell characters are independent in the site-colour torus for every
choice in (2).  Hence arbitrary nonzero weights can be normalized to the
unit calculation; the rank and membership verdict is not a coefficient
grid.

## 4. Scope and next boundary

This does **not** prove the arbitrary mixed-colour kernel-product theorem
and is not a Krenn counterexample.  It proves that the minimal incoming
mixed differential, its unique direct bright completion, and its first
cofactor activation do not create the missing pure class.  Any escape from
this chart needs at least one of:

* a second independent off-diagonal transition (the first colour cycle);
* a non-direct or multi-centre bright lift outside the selected leader
  chart; or
* at least two further internal coordinates.

The complementary general target-axis analysis identifies the same next
boundary from the opposite direction: an arbitrary mixed escape from the
large target-axis kernel argument must contain a paired off-diagonal colour
transition.

## 5. Reproduction

```sh
uv run python computations/verify_shared_reciprocal_two_bad_mixed_bright_completion.py
uv run python -O computations/verify_shared_reciprocal_two_bad_mixed_bright_completion.py
```

Both modes reproduce

```text
da4ce8fc3b4f8f167fe6dd11e108a2219889071d95cbbbb1463e2facb34867d8
```
