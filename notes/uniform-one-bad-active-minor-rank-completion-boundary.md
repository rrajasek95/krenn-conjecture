# The flat-Hessian active minor still needs a one-arm rank completion

## Outcome

The active product from `d79340a` does not itself produce the clean/curved
landing.  In the canonical physical `h=3` chart it is literally

\[
                         \Delta_{20}K_0=1.
\]

The two physical arms appearing in that determinant are

```text
10:E00,  12:-E10.
```

They are both active, and their centre heads are independent, but their
outer heads are the same target line `e0`.  Their four deleted-star ranks are

```text
2,2,3,3.
```

Thus an active determinant/cofactor product is strictly weaker than a
curved doubly-good OO pair.

The exact checker is
`computations/verify_uniform_one_bad_active_minor_rank_completion_boundary.py`.

## Exact private-site source identity

Use pure colour `a=0`, change site `v=1` to colour `b=1`, and take reference
site `u=2`.  On the frozen packet

```text
p_u=A12[0,0]=0,       q_u=A12[1,0]=-1.
```

Among all alternate sites, only `s=0` contributes.  There

```text
p_s=A10[0,0]=1,       q_s=A10[1,0]=0,
Delta_20=1,
K_0=(27:00)(34:00)(56:00)=1.
```

The pure row `00000000` has coefficient one and the private mixed row
`01000000` has coefficient zero.  The target-augmented identity is therefore

\[
 q_u+\sum_s\Delta_{2s}K_s=-1+1=0.
\]

This pins the downstream input to ordinary physical source rows; it is not
a declared minor or a support-only witness.

## The one-arm exchange which works in the canonical chart

Retain the good active arm `12:-E10` and replace the deficient arm `10:E00`
by the already present endpoint arm

```text
16:-E11.
```

The exchanged arms have distinct outer lines `e0,e1`.  Their deleted-star
ranks are exactly `(3,3,3,3)`.  Their cofactor coefficients have witnesses

```text
arm 12: (06:11)(34:00)(57:11) = 1,
arm 16: (02:10)(34:00)(57:11) = -1,
```

and the literal transition minor with indices `(1,0,1; site0, colour1)` is
`-2`.  Hence this exchanged pair is genuinely shared, active, nonflat, and
four-good.  The canonical chart therefore reaches the curved OO side by a
one-arm exchange, not by upgrading the original active pair in place.

This is the useful structural refinement: the missing operation is not an
unspecified increase of four ranks.  It is transport of the active cofactor
from the same-head arm to one distinct-head endpoint arm while retaining
activity, all four rank-three star minors, and one nonzero transition minor.

## Exact companion boundary

If the sparse companion word `21000121` has no cancellation mate, its row
forces the multisite parameter `t=0`; the only spread endpoint row then
concentrates and all four endpoint-star divided squares vanish.  This is the
clean alternative.

For an arbitrary source the companion has 105 possible matchings.  Besides
the pivot, five preserve both outer axes and expose exactly

```text
13:10, 14:10, 45:01, 35:01, 25:01.
```

The other 99 expose an off-diagonal outer arm.  No source identity presently
shows that cancellation through the five internal cells preserves the
displayed one-arm exchange or produces another one.  This five-cell internal
mate class is the sharp downstream obstruction; combinations of larger
supports need not be enumerated before this structural transfer is proved.

## Scope guard

The checker expands all `3^8=6561` output words of the sparse calibration.
It has the three correct pure rows, but it also has six nonzero mixed rows:

```text
00222002, 11012002, 12222212,
21000121, 21111121, 22000220.
```

Accordingly it is not a source and not a counterexample to the desired
global dichotomy.  It proves the exact information boundary:

> `Delta*K != 0` supplies a same-head `(2,2,3,3)` landing.  To finish the
> `k=2` branch uniformly, the complete one-bad rows must either concentrate
> an effective response to `R^[2]=0`, or justify the distinct-head one-arm
> exchange which yields an active nonflat `(3,3,3,3)` OO pair.

## Verification

Run

```text
python3 computations/verify_uniform_one_bad_active_minor_rank_completion_boundary.py
python3 -O computations/verify_uniform_one_bad_active_minor_rank_completion_boundary.py
python3 -I -S computations/verify_uniform_one_bad_active_minor_rank_completion_boundary.py
```

The frozen ledger digest is

```text
88ff86b4914b8d03779cdaac4c64a3544384d5852082814bf9ab1cb796c19751
```
