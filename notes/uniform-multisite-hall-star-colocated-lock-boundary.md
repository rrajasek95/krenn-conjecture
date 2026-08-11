# The co-located Hall-star debt reduces to a two-neighbour lock

## Result

The common-side Hall-star theorem leaves one case after the distinct-site
four-good landing: both ordered crossed debts occur on one off-centre site
`u`.  Thus the same off-anchor physical block `P-u` contains nonzero cells

```text
p_1(u,2),   p_2(u,1),
```

with nonzero complete cofactors.  This block is good at both endpoints, but
it is only one physical pair and therefore is not yet the required
two-pair overlap.

Apply the target-augmented private-site identity separately to the two
cells.  Since the selected unary matching uses the outer edge `P-S` and
both selected diagonal matchings use `P-c`, the only selected anchor
neighbours of `P` are `S,c`.  The exact dichotomy is

\[
 \boxed{\text{a free active companion, hence the four-good wedge}}
 \quad\text{or}\quad
 \boxed{\text{both transition sums are supported on }\{S,c\}.}
\]

The second box is the sharp co-located residual.  The checker is
`computations/verify_uniform_multisite_hall_star_colocated_lock_boundary.py`.

## Two exact private-site rows

Write `x_12,x_21` for the two nonzero direct cells on `P-u`.  The ordinary
source identities are

\[
\begin{aligned}
 x_{12}+\sum_{s\ne P,u}\Delta^{12}_{us}C^{12}_s&=0,\\
 x_{21}+\sum_{s\ne P,u}\Delta^{21}_{us}C^{21}_s&=0.   \tag{1}
\end{aligned}
\]

Because `x_12,x_21` are nonzero, each active-product set in (1) is nonempty.
If one contains `s` outside `{S,c}`, then both `P-u` and `P-s` avoid all
three selected pure matchings.  At either endpoint of either pair, matching
`Q_k` contributes the undeleted column

\[
                 (\operatorname{neighbour}_k,k),
                 \qquad k=0,1,2.
\]

The colour labels make these columns independent even when physical
neighbours repeat.  All four deleted-star ranks are therefore three, and
the nonzero `Delta*C` is exactly the active distinct-head transition.  This
is the already-certified four-good wedge, with no source modification.

If there is no such `s`, (1) becomes the bounded aggregate packet

\[
\begin{aligned}
 x_{12}+A^{12}_S+A^{12}_c&=0,\\
 x_{21}+A^{21}_S+A^{21}_c&=0.                           \tag{2}
\end{aligned}

There is no scalar contradiction: for example

```text
x12=2,  (A12_S,A12_c)=(-1,-1),
x21=3,  (A21_S,A21_c)=(-3,0).
```

Thus the next source theorem must couple the two rows of (2), rather than
invoke another Hall selection.

## Why one good reciprocal block is insufficient

The checker replays the pinned rational physical guard whose direct block is

\[
                    E_{01}+E_{10}.
\]

It has rank two and satisfies two complete pure response tensors and both
complete crossed zero tensors.  Its selected response compound has
determinant one, yet the source is coefficient-feasible.  The six-site top
is zero, not the required unary target.  Consequently:

> a co-located reciprocal two-cycle plus the four response rows does not by
> itself give affine line-hitting, a determinant unit, or a clean cap.

This physical guard is not a one-bad source.  It identifies the genuinely
load-bearing next row: the common unary top must straighten (2), or it must
create a source-valid free companion/clean cap.

## Exact residual and scope

The strict Hall-star family is now closed whenever its same-side crossed
debts have distinct representatives, and the co-located branch is closed
whenever either private-site active set leaves `{S,c}`.  What remains is
precisely

```text
one off-anchor good block P-u carrying 12 and 21,
both private-site transition sums trapped on P-S and P-c.
```

This is a source-labelled family reduction, not a support census.  It does
not claim that the response-only guard satisfies `q^[h]=X0`, and hence does
not refute the desired full-packet theorem.

Run

```text
python3 computations/verify_uniform_multisite_hall_star_colocated_lock_boundary.py
python3 -O computations/verify_uniform_multisite_hall_star_colocated_lock_boundary.py
python3 -I -S computations/verify_uniform_multisite_hall_star_colocated_lock_boundary.py
```

Frozen ledger SHA-256:

```text
dbece81cbbb7f24ef1360311a3da92db4269b1d2f0936cf2902abadcc6aeb04c
```
