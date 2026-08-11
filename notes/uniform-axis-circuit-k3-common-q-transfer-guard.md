# A genuine common-q deformation can contract a three-column axis circuit

## Result

The obstruction in `e4962e1` is specific to coefficientwise deletion.  At
the level of the genuine common quadratic and its entire cofactor tower, a
simultaneous carrier deformation can transfer the omitted response residue
and reach the proved two-column normal form.

There is an exact coordinate-diagonal family at every `h >= 4` with three
minimum response columns

\[
 C_0=X+Y,\qquad C_1=-Y+tZ,\qquad C_2=-tZ.                \tag{1}
\]

For `t != 0` the columns are independent.  At `t=0`,

\[
 C_2(0)=0,\qquad C_1(0)=C_1(1)+C_2(1),\qquad
 C_0(0)+C_1(0)=X.                                      \tag{2}
\]

Thus the common-`q` deformation absorbs the omitted coordinate residue into
the retained column and reduces the response to `k=2`.  It never creates an
off-diagonal internal cell or a transverse local port.

This is a sharp physical counterguard, not a full one-bad packet.  Its first
failed source equation is exactly the unary top: the opposite-star site is
isolated in `q`, so `q^[h]=0` rather than `X0`.  Consequently Hessian and
third-cofactor provenance alone cannot prove that simultaneous transfer is
impossible or that it forces clean/OO.  A positive arbitrary-`k` theorem
must use the unary top attachment (and then the other-colour companion rows)
to obstruct or reroute the family (1).

The nonanchor off-diagonal reselection theorem `336492c` does not touch this
guard: every displayed cell is coordinate-diagonal.  The family therefore
lies exactly in that theorem's remaining decorated diagonal-cycle branch,
not in the already-routed off-diagonal complement.

Checker:
`computations/verify_uniform_axis_circuit_k3_common_q_transfer_guard.py`.

## The literal quadratic

On core sites `0,...,7`, take the occupied axis star and its opposite row

```text
p = e1@0 + e1@1 + e1@2,       s = e1@7.
```

The common quadratic has only coordinate-diagonal cells:

```text
12:11 =  1       02:11 = -1       34:00 = 1
56:11 =  1       04:00 =  t       25:11 = 1
36:11 =  1       13:11 = -1       14:11 = 1.
```

Perfect-matching expansion after deleting the star sites gives precisely

```text
hole 0,7:  14|25|36  + 12|34|56       = X + Y,
hole 1,7: -02|34|56  + 04|25|36       = -Y + t Z,
hole 2,7: -04|13|56                   = -t Z.
```

Here `X` is the all-`1` word,

```text
Y = X with sites 3,4 changed to 0,
Z = X with sites 0,4 changed to 0.
```

The coefficient matrix on `X,Y,Z` has determinant `t`; hence the three
occupied columns are a minimum-support circuit away from `t=0`.  Scaling
the one physical coefficient `q04:00=t` is the simultaneous source
deformation in (2), rather than the forbidden operation of merely setting
the third star coefficient to zero while holding all columns fixed.

For larger `h`, tensor the construction with the disjoint cells
`89:11, 10,11:11, ...`.  Equations (1)-(2) acquire the same pure-`1`
factors and remain literal.

## Genuine cofactor provenance

Nothing in (1) declares formal Hessian data.  The checker constructs every
hafnian cofactor of the displayed `q`.  On the eight-site core it verifies
the complete Euler tower

\[
 m H_R=\sum_{e\cap R=\varnothing}q_eH_{R\cup e}
 \qquad (|R|=0,2,4,6),                                  \tag{3}
\]

coefficientwise over `Z[t]`.  There are 128 cofactor tensors and 127 exact
recurrence checks.  In particular the second- and third-cofactor carriers
are genuine consequences of the same varying `q`; the word-carrier theorem
from the prior third-cofactor audit is automatically satisfied throughout
the deformation.

The construction also explains why the linear-algebra guard `6999cbc` is
sharp.  Complete response-tail independence can be carried entirely by
coordinate-diagonal matching tails.  It need not create a transverse outer
head or improve a `(2,2,3,3)` port profile.

## Exact missing hypothesis

Site `7` carries no `q` cell.  Therefore every perfect matching of the full
site set is absent and

\[
                          q^{[h]}=0.                    \tag{4}
\]

The unary pure-zero source generator is consequently `-1`.  This is the
first source row outside the verified packet; no higher cofactor recurrence
detects the failure because all those recurrences are identities for the
genuine `q` in (1).

So the remaining theorem is now source-specific:

> In a genuine one-bad packet with `q^[h]=X0`, show that a residue-transfer
> deformation such as (2) either violates a mixed unary coefficient, creates
> an off-diagonal active determinant/cofactor carrier, or lands in the
> already-closed clean/curved packet.

The second diagonal and crossed-zero responses are also absent here and may
be needed after the unary attachment.  The result does not claim that the
unary row alone closes every `k>=3` circuit, nor that every larger circuit
contracts.

## Verification

Run

```text
python3 computations/verify_uniform_axis_circuit_k3_common_q_transfer_guard.py
python3 -O computations/verify_uniform_axis_circuit_k3_common_q_transfer_guard.py
python3 -I -S computations/verify_uniform_axis_circuit_k3_common_q_transfer_guard.py
```

The checker pins the `k>=3` coefficient-deletion and rank guards, the
Hessian carrier theorem, and the third-cofactor carrier theorem.  It audits
the uniform response family for `h=4,...,8`, the `t=1` minimum rank, the
exact residue transfer at `t=0`, coordinate diagonality, and the complete
core cofactor tower.

Frozen ledger SHA-256:

```text
24578960f6c78c54fb0b160b5e02b1c36b18eff6c1a95216f18e5e3997583460
```
