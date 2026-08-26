# Filtered tail lifting: exact local lemma and global obstruction

Status: **UNAUDITED exact structural PASS**.  The initial-rank theorem gives
formal/local implicit solvability, not global tail elimination.  The failure
is already visible in a one-variable quadratic.

## Literal filtered equations

Let `D` be the diagonal coefficient ring, localized at the chosen chart
factors, and let

```text
R=D[T],  J=(T),
```

where `T` consists of the 168 cross-colour endpoint cells.  Filter `R` by
powers of `J`.  Direct enumeration of all 105 perfect matchings gives:

```text
profile       tail degree : matching count
7+1                     1 : 105
6+1+1                   1 : 15,  2 : 90
3+3+2                   1 :  9,  2 : 18, 3 : 42, 4 : 36
```

Thus the tail degree is bounded by four, but the rows are not linear.  For
the canonical `6+1+1` word one has the literal form

```text
F_01222222 = h^2_01 t^01_01 + Q_01,
```

where `h^2_01` is the six-site Hafnian coefficient and `Q_01` is the sum of
the 90 degree-two matchings.  Each term of `Q_01` uses one `02` tail cell,
one `12` tail cell, and a four-site `G2` Hafnian.  Hence on `h^2_01!=0` the
exact conclusion is

```text
t^01_01 = -(h^2_01)^(-1) Q_01,
```

not `t^01_01=0`.

The 380-by-12 theorem first deletes the other tail columns.  In the full
filtered module its invertible selected block solves those twelve variables
as power series/polynomials in the undeleted columns; it does not place the
twelve variables individually in the source ideal.

## The rigorous lifting lemma that is available

Let `I` be the localized source ideal.  Suppose a batch of equations has

```text
f = M T_selected + terms in (T_other) + J^2,
```

with `M` invertible.  If `T_other` is already in `I`, then

```text
T_selected is contained in I+J^2.
```

If a well-founded triangular sequence covers every tail generator, then in
`A=R/I` its tail ideal satisfies `J_A=J_A^2`.  At any local ring `A_m` with
`J_A` contained in `m`, Nakayama gives `J_A,m=0`.  Thus a full triangular
rank theorem isolates the zero-tail component formally and locally.

This is the strongest unconditional lifting statement justified by initial
rank.  It requires all deleted equal/lower columns to have been eliminated;
the current carrier ledger does not supply that ordering.

## Smallest global obstruction

The one-variable equation

```text
t-t^2=0
```

has initial matrix `[1]`, yet has the remote solution `t=1`.  Its homogenized
family `t-s t^2=0` has special fibre `t=0` and a generic remote branch
`t=1/s`.  Indeed

```text
Q[s,t]/(t(1-st)) = Q[s] x Q[s,s^-1],
```

because `(t)` and `(1-st)` are comaximal.  It is flat over `Q[s]`.  Therefore
even flat Rees degeneration plus full initial rank does not exclude a branch
escaping the zero-tail chart.

A source-shaped three-channel version is

```text
x-yz=0,  y-xz=0,  z-xy=0.
```

Its linear initial matrix is `I_3`, but besides the origin it contains

```text
(1,1,1), (-1,-1,1), (1,-1,-1), (-1,1,-1).
```

The quotient is finite: for example

```text
x^3-x=(x^2-1)(x-yz)-z(y-xz)-xz(z-xy),
```

and cyclic identities hold for `y,z`.  Nevertheless the tail ideal is not
nilpotent, as evaluation at `(1,1,1)` shows.  Finiteness therefore does not
make Nakayama global.  A nilpotence certificate, a global Jacobson-radical
hypothesis, or an exact saturation excluding every remote component would
be sufficient, but none is frozen for the source quotient.

## Terminal zero-tail scheme and cap open

On `T=0`, a mixed row is automatic if any colour class has odd size.  If all
three classes `S_c` have even size, it becomes

```text
F_w(T=0) = product_c Haf(G_c[S_c]).
```

Among the 6,558 mixed rows, 4,920 are automatic and 1,638 form the actual
diagonal packet:

```text
6+2+0 : 168 rows
4+4+0 : 210 rows
4+2+2 : 1260 rows.
```

Let

```text
U_cap = union over 728 carriers C of
        intersection i=0..3 {rank([L_C;ell_i])=rank(L_C)+1}.
```

The exact terminal obligation is the set-theoretic containment of the
normalized diagonal packet scheme—three pure Hafnians equal one plus the
1,638 displayed rows—in `U_cap`, or a proof that this scheme is empty.  The
tail theorem and its four support-boundary orbits do not prove this
containment.  Existing diagonal mate/chart certificates cover proper
subcharts only.

## Consequence for the global bridge

The quotient-to-full arrow is therefore rigorously conditional:

```text
prior-column triangularity
 + full coverage of all 168 tail generators
 + nilpotence/remote-component saturation
 => actual zero-tail elimination.
```

After that, a separate diagonal-packet-to-`U_cap` theorem is still required.
The four support-factor orbits are neither of these two global obligations.

## Replay

```sh
python3 computations/unaudited-codex-tail-filtered-lift-obstruction-2026-08-21/audit_tail_filtered_lift_obstruction.py --write-results
python3 -O computations/unaudited-codex-tail-filtered-lift-obstruction-2026-08-21/audit_tail_filtered_lift_obstruction.py
python3 -I -S computations/unaudited-codex-tail-filtered-lift-obstruction-2026-08-21/audit_tail_filtered_lift_obstruction.py
```

All modes have byte-identical stdout/result SHA-256
`51a282ba6e866693cc12c5fafc73d77e12f3a437823cae4e54d6b85fa041604c`;
the logical digest is
`a8adc8602554c08cecf0a5a056d2dc62a77c6c5ad97766381ed25cf923346c11`.
