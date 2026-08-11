# All five axis-preserving mates collapse to the clean branch

## Result

The sharp five-cell boundary left by `7be34b6` is closed as one symbolic
module.  Allow arbitrary coefficients

```text
y13=x13_10, y14=x14_10, y45=x45_01,
y35=x35_01, y25=x25_01
```

simultaneously.  Also allow arbitrary coefficients `z17,z23,z24` on the
three possible star/pure carriers `x17_11,x23_00,x24_00`.  Complete physical
matching expansion gives six mixed source rows

\[
\begin{array}{rcll}
g_{13}&=&-y_{13},&11002002,\\
g_{35}&=& y_{35},&00101110,\\
g_{45}&=& y_{45},&00220110,\\
g_{25}&=& y_{25},&11012112,\\
g_{14}&=& y_{14}+z_{17}y_{45},&11220111,\\
g_c&=&t+y_{13}z_{24}+y_{14}z_{23}
 +y_{45}z_{17}z_{23}+y_{35}z_{17}z_{24}+y_{25}z_{17},&21000121.
\end{array}
\]

These are ordinary source generators with the literal eight-site word labels
shown at right.  They give the exact polynomial lifts

\[
\begin{aligned}
y_{13}&=-g_{13},&y_{35}&=g_{35},&y_{45}&=g_{45},&y_{25}&=g_{25},\\
y_{14}&=g_{14}-z_{17}g_{45},
\end{aligned}
\]

and

\[
\boxed{
t=g_c+z_{24}g_{13}-z_{23}g_{14}
      -z_{17}z_{24}g_{35}-z_{17}g_{25}.}
\]

Thus all five mate coefficients and the spread parameter `t` lie in the
ordinary affected-row source ideal.  No cancellation counterguard survives.

The exact checker is
`computations/verify_uniform_one_bad_five_axis_mate_clean_closure.py`.

## Clean-cap consequence

In the canonical one-bad chart the only spread endpoint row is

\[
                  Q_c=e_1^{(0)}+t e_1^{(1)}.
\]

Its divided square is exactly

\[
                  Q_c^{[2]}=t,e_1^{(0)}e_1^{(1)}.
\]

The other three endpoint rows are already supported at one site.  Therefore
the identity `t in I` makes all four endpoint-star self-squares zero.  The
uniform square-zero one-bad theorem then supplies the explicit active clean
cap and exact `N -> N-2` descent.

The proposed dichotomy consequently collapses to its first alternative on
this module: every source point has `R^[2]=0`; the rank-`(3,3,3,3)` OO
alternative is unnecessary.

## Completeness and scope

The checker reconstructs all `3^8=6561` physical output words.  There are 22
parameter-affected source generators, with term histogram

```text
terms per row       1   2   3   5   6
number of rows     13   6   1   1   1.
```

The six displayed rows are selected from that complete affected-grade
ledger, not guessed from the companion alone.  The identities are integral
and use no division or nonvanishing assumption on `z17,z23,z24`.

The scope is exactly the canonical chart plus the five axis-mate cells and
the three arbitrary mate carriers.  An additional physical cell capable of
adding a monomial to one of the six displayed rows is outside this theorem;
no such larger support layer is inferred here.

## Verification

Run

```text
python3 computations/verify_uniform_one_bad_five_axis_mate_clean_closure.py
python3 -O computations/verify_uniform_one_bad_five_axis_mate_clean_closure.py
python3 -I -S computations/verify_uniform_one_bad_five_axis_mate_clean_closure.py
```

The frozen ledger digest is

```text
33137440a89a759c786b785417e1a91d79e4cafea15ff2ee6b9b759e516b2751
```
