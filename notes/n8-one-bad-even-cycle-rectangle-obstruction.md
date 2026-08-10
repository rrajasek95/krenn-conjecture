# The first one-bad exchange closure is an even cycle, then a tensor unit

## Outcome

For the reduced six-site one-bad packet

\[
 q^{[3]}=X_a,
 \qquad p_i s_jq^{[2]}=\delta_{ij}X_i
       \quad(i,j\in\{b,c\}),                            \tag{1}
\]

the private-word exchange cannot be oriented globally by “choose the unique
matching.”  Above the first sharp source orbit there is a 19-cell support
with

```text
one live singleton fibre:       the desired aaaaaa top word,
twenty-four live double fibres: every other top/response word.
```

Thus every forbidden live monomial has a matching mate.  The support is a
literal even-cycle counterguard to the matching-potential route.

It is not a coefficient point.  The 24 double fibres are six `2x2` tensors,
and a two-zero fan among them is already the unit ideal over `Q`.  This gives
a small support-independent obstruction to the entire rectangle.

## The 19 cells

Retain the top matching

\[
                         01|23|45:a a
\]

and split the other sites into left shore `{0,1}`, `b`-right shore `{2,4}`,
and `c`-right shore `{3,5}`.  On every left-to-right physical edge retain
both possible left colours and the fixed right colour:

```text
left {0,1} -> right {2,4}:  bb and cb,
left {0,1} -> right {3,5}:  bc and cc.
```

There are 16 rectangle cells, four of which coincide with the sharp binary
near-matchings, so the union has `3+16=19` cells.  Direct expansion gives
one singleton top fibre and 24 double fibres.  Eight doubles are the two
mixed top slices left by the top edges `23` and `45`; sixteen are the four
binary response tensors.

This is the promised genuine even cycle: response-mate insertion can return
through the opposite side of the rectangle rather than strictly increasing
or decreasing a private-word potential.

## A shared two-zero fan is impossible

For each right vertex `r in {2,4,3,5}`, collect its two left-colour columns
at sites 0 and 1 as vectors `u_r` and `v_r` in the binary target planes.
Every live double fibre is a coefficient of

\[
                  T_{rs}=u_r\otimes v_s+u_s\otimes v_r. \tag{2}
\]

The diagonal responses require, up to nonzero scalar normalization,

\[
                  T_{24}=e_b\otimes e_b,
        \qquad   T_{35}=e_c\otimes e_c.                 \tag{3}
\]

The two cross responses give `T25=T34=0`.  The two mixed top slices, after
division by the localized `aa` top edges, give `T23=T45=0`.

Only two zero tensors sharing a vertex are needed.  For example assume

\[
                         T_{23}=T_{25}=0.                \tag{4}
\]

If `u_2=0`, nonzero `T24` makes `v_2` nonzero, and (4) forces
`u_3=u_5=0`, contradicting nonzero `T35`.  The case `v_2=0` is symmetric.
Hence both are nonzero.  Each equality in (4) is an equality of two nonzero
simple tensors (otherwise `T35=0`), so

\[
 u_3,u_5\in\mathbb C u_2,
 \qquad v_3,v_5\in\mathbb C v_2.                        \tag{5}
\]

Consequently `T35` is a nonzero multiple of `u_2 tensor v_2`, and (3)
puts `u_2,v_2` on the `c` target lines.  But

\[
 T_{24}\in u_2\otimes V+U\otimes v_2,
\]

whose image in `(U/<e_c>) tensor (V/<e_c>)` is zero.  The image of
`e_b tensor e_b` is nonzero, contradicting (3).

The same proof applies to the other three shared fans

```text
{T23,T43}, {T25,T45}, {T43,T45}.
```

The checker independently reconstructs all 24 source fibres and verifies
that each 16-variable fan ideal has Groebner basis `[1]` over `QQ`.  Removing
either zero tensor from any fan makes the ideal proper, so the theorem is
not silently using a one-zero shortcut.

## Scope and next gate

This closes the first complete even-cycle repair of a sharp support orbit.
It does not prove (1) impossible for arbitrary larger support.  The reusable
theorem is the shared two-zero fan: any quotient of the general packet that
produces two independent pure pair tensors and two zero pair tensors sharing
one carrier is empty.

A support-independent completion must now prove that every one-bad source
admits such a four-right-vertex quotient (or another finite tensor unit).
Continuing to orient individual private matchings cannot suffice, because
the 19-cell shadow already has no forbidden singleton.

## Reproduction

```sh
uv run python computations/verify_n8_one_bad_even_cycle_rectangle_obstruction.py
PYTHONOPTIMIZE=1 uv run python computations/verify_n8_one_bad_even_cycle_rectangle_obstruction.py
```

Both modes must print the frozen ledger digest recorded by the checker.

```text
18bc30b370f3bff59d5eb97428dae7d7358ae0202599a606cf6f93aec93faf5e
```
