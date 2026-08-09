# Reciprocal coordinate pairs do not admit a universal 3x3 port completion

## Outcome

The adjacent-cubic descent cannot be extended verbatim to the reciprocal
coordinate-block branch.  For a reciprocal pair, all three target colours
must be manufactured by endpoint-port responses.  The natural completion is
therefore governed by a `3x3` coefficient matrix with all three diagonal
entries nonzero.  Universal cancellation of the second insertion requires
all its `2x2` permanents to vanish.  Over characteristic zero this system has
no solution.

The obstruction is already an integral three-equation certificate and a
single mixed permanent equal to `2`.  It applies to diagonal and
off-diagonal reciprocal matrix units after scalar normalization.

This retires the simplest “one permanent-null cap theorem covers curved
overlap, adjacent cubic, and reciprocal block” strategy.  It does not exclude
a descent using source-specific annihilation of the surviving quadratic
cofactor, a staged completion, or non-port quadratic cells.

## Pair packet and the completion matrix

Delete a reciprocal pair `p,r` from an exact source and write `q` for the
residual quadratic form.  Put

```text
r_ij = p_i s_j
```

for the source-labelled quadratic port insertion.  The full nine pair rows
are

```text
r_ij q^[h-1] = delta_ij X_i - d_ij q^[h],                 (1)
```

where the reciprocal direct block is the literal coordinate cell

```text
d = lambda E_ba.
```

Try

```text
z(C) = sum_ij c_ij r_ij,
q'   = q + z(C).                                          (2)
```

For the linear part of `q'^[h]` to be the ternary GHZ tensor, (1) forces

```text
c_00=c_11=c_22=1,
lambda c_ba=1.                                            (3)
```

The remaining off-diagonal entries multiply zero-response rows and are free
at first order.  Because

```text
r_ij r_kl = r_il r_kj = p_i p_k s_j s_l,
```

the coefficient of a quadratic port insertion is the `2x2` permanent

```text
c_ij c_kl + c_il c_kj.                                   (4)
```

A completion that is clean for arbitrary source ports must kill every
expression (4).  Once the quadratic term vanishes universally, all higher
port insertions vanish as well; the obstruction already occurs at degree
two.

## Integral no-go certificate

Write the three relevant permanent equations as

```text
f01 = 1 + c01 c10,
g1  = c12 + c02 c10,
g2  = c01 c12 + c02.
```

They obey the literal identity

```text
g2 - c01 g1 + c02 f01 = 2 c02.                            (5)
```

Another principal permanent gives `1+c02 c20=0`, so `c02` is a unit on the
candidate chart.  Equations `f01=g1=g2=0`, saturated by `c02`, therefore
force `2=0`.  In characteristic zero the permanent-null ideal is the unit
ideal.

The smallest numerical witness is

```text
C = [ 1  1  1
     -1  1  1
     -1 -1  1 ].                                         (6)
```

All three principal `2x2` permanents of (6) vanish, while the minor on rows
`0,1` and columns `1,2` is

```text
1*1 + 1*1 = 2.                                           (7)
```

For an off-diagonal reciprocal cell take `d=-E_10`; then
`lambda*c10=1`.  For a diagonal reciprocal cell take `d=E_00`.  Thus (6)
satisfies the first-order `q^[h]` cancellation in both representative
branches, but (7) leaves a nonzero quadratic six-port cofactor.

## Why adjacent cubic is different

In the adjacent-cubic branch, the residual `q^[h]` already supplies one pure
target colour.  Only the other two colours need port completion.  The
coefficient problem is `2x2`, and

```text
[ 1  1
 -1  1 ]
```

has permanent zero.  This is exactly the crossed-cell cancellation used in
the committed adjacent-cubic descent.

A reciprocal coordinate block does not make `q^[h]` a pure target tensor;
equation (1) only expresses it through another port response.  All three
diagonal entries in (3) remain necessary, triggering the `3x3` obstruction.

## Consequence for the uniform dichotomy

The current structural theorem gives

```text
reciprocal coordinate block
or
curved overlap on two active rank-one good pairs.
```

The no-go above says these branches cannot be merged merely by declaring a
universal permanent-null port completion.  To close the reciprocal branch,
one must prove at least one of the following additional facts from the exact
source equations:

1. the surviving mixed permanent (7) annihilates the relevant
   `q^[h-2]` cofactor;
2. one target colour is already carried purely by `q^[h]`, reducing to the
   two-colour completion;
3. a staged descent makes one port response exact before adding the other
   two; or
4. the reciprocal incidence structure forces an adjacent cubic pair, where
   the existing descent applies.

The first option is the closest analogue of the decorated OO correction:
it is source-specific and cannot be inferred from the coordinate direct
block alone.

## Reproduction

```text
python3 computations/verify_reciprocal_port_permanent_null_no_go.py
python3 -O computations/verify_reciprocal_port_permanent_null_no_go.py
```
