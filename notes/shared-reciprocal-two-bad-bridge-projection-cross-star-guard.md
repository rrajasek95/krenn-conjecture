# The target-line quotient retains crossed-star bright responses

## 1. Verdict

The simplest proposed extension of the target-line bridge theorem to
multi-centre bright lifts is false.  Projecting the two bridge sites
`0,1` modulo `e_t` does kill the two bridge columns, but it does **not**
kill the crossed matchings through their two stars.  Consequently a bright
response need not factor through the direct block `q_01`.

The checker gives an exact colour-diagonal packet with

```text
K_0 = e_t^(1) tensor Z,
K_1 = e_t^(0) tensor Z,
e_t^(0)-e_t^(1) in ker(Phi),
q_01 = 0,
K_2 = -2 X_a on C\{2}.
```

It also retains a nonzero all-`t` coefficient in `P U U q`.  Thus the
guard includes the target-line bridge, the active quadratic channel, and
an honest bright lift from the same internal quadratic.  It omits the
second bright colour and is not a two-bad source counterexample.

## 2. Exact packet

Let `C={0,1,2,3,4}`, `a=0`, and `t=2`.  The nonzero diagonal cells are

```text
02:tt =  1       12:tt =  1       34:tt = 1
03:aa =  1       04:aa = -1
13:aa =  1       14:aa = -1
23:aa =  1       24:aa =  1       34:aa = 1.
```

On deleting site `0`, the two all-`a` matchings cancel:

```text
(13)(24) + (14)(23) = 1-1=0.
```

The same cancellation holds after deleting site `1`.  The remaining
terms are therefore

```text
K_0 = e_t^(1) tensor (e_t e_a e_a + e_t e_t e_t),
K_1 = e_t^(0) tensor (e_t e_a e_a + e_t e_t e_t).
```

Their difference gives the literal target-line kernel.  With `P=e_t` at
site `2`, the cell `34:tt` makes the all-`t` coefficient of `P U U q`
equal to `-2`, so the pure channel is active.

## 3. The surviving cross-star term

Delete site `2`.  Since `q_01=0`, the direct matching is absent, but the
two crossed matchings give

```text
[K_2]_{aaaa}
 = q_03(a,a) q_14(a,a) + q_04(a,a) q_13(a,a)
 = -1-1 = -2.                                           (1)
```

There are no other terms in `K_2`, so
`(-1/2)e_a^(2) K_2=X_a`.  In particular, quotienting sites `0,1` by
`e_t` leaves (1) unchanged.  The hoped-for implication

```text
projected bright response != 0  =>  projected q_01 != 0
```

is therefore false even with common cofactor provenance and an active
pure-`t` channel.

## 4. What remains viable

This guard does not refute a coupled two-bright theorem.  Rather, it shows
what that theorem must use: the `X_a` and `X_c` equations have to be
combined before projection, so that the crossed permanents for the two
colours compete for the same three residual edges.  Treating either bright
equation separately cannot work.

A plausible next finite lemma is to write, for each non-target colour `d`,

```text
g_d = q_01(d,d) r_d + perm_cross(u_d,v_d),
u_d dot r_d = v_d dot r_d = 0,
```

where `r_d` is the three-edge residual vector.  The mixed bridge rows give
the coordinatewise exclusions
`u_{d,i} r_{e,i}=v_{d,i} r_{e,i}=0` for `d!=e`.  The open question is
whether these two coupled systems can support both pure response vectors
after the complete mixed bright equations are imposed.

## 5. Reproduction

```sh
python3 computations/verify_shared_reciprocal_two_bad_bridge_projection_cross_star_guard.py
python3 -O computations/verify_shared_reciprocal_two_bad_bridge_projection_cross_star_guard.py
```

The checker uses only exact rational arithmetic from the Python standard
library and reconstructs every displayed cofactor from literal matchings.
