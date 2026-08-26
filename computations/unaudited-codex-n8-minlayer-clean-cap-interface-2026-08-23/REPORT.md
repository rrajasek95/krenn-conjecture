# Minimum-layer contamination is the clean-cap response

Status: **UNAUDITED exact source/combinatorial PASS**. No solve was run.

## Literal identity

Fix a physical pair `p,q` and the six residual sites `U`. The 105 perfect
matchings split source-faithfully as

```text
15 using pq     = [s(K) exp(x)]_U,
90 avoiding pq  = [r(K) exp(x)]_U.
```

The second count is literal: choose the unordered neighbours of `p,q` in
`C(6,2)=15` ways, choose their endpoint orientation in two ways, and match
the remaining four sites in three ways. Thus the 90 fixed-edge terms in the
minimum-layer audit are the **linear response**, not the clean error.

Put `y=x+r/s`. At six residual sites the exact expansion is

```text
s H6(y)
 = [(s+r) exp(x)]_U + s^-1 r^2 x/2 + s^-2 r^3/6.
```

After multiplying the difference by `s^2`, the correction is precisely the
certified eight-to-six error

```text
E_pq(K)=s r^2 x/2+r^3/6.
```

So demanding cancellation of all 90 terms was too strong. Clean descent
retains them as the effective six-site edge correction `r/s`; only their
quadratic and cubic reinsertions must vanish.

## Exact triangle landing

For a residual triangle `T`, let `L_T` be the `108 x 9` matrix of all nine
cells of the 12 response edges outside `T`, and put `V_T=ker L_T`. For
`K in V_T`, `r(K)` is supported on the three edges of `T`. Those edges have
matching number one, hence

```text
r(K)^2=r(K)^3=0,
E_pq(K)=0.
```

At the raw matching level, `K in V_T` kills 72 of the 90 avoiding terms and
retains the 18 terms on the triangle (`3 edges * 2 orientations * 3
four-site matchings`). Retaining those 18 terms is correct: they are absorbed
into `y`.

The four activity forms on `V_T` are

```text
K00, K11, K22, <K,A_pq>.
```

Over `C`, a vector space is not a finite union of proper hyperplanes. Thus
there is a common `K in V_T` on which all four forms are nonzero iff none of
the forms vanishes identically on `V_T`, equivalently iff none belongs to
`rowspan L_T`. Therefore failure of the min-layer-to-clean landing is
**exactly** one of

```text
K00 in rowspan L_T,  K11 in rowspan L_T,
K22 in rowspan L_T,  or <K,A_pq> in rowspan L_T.
```

These are the four blocker branches for one of the `28*C(6,3)=560`
triangle carriers. The first three mean that one endpoint colour channel is
absent from every common triangle-kernel cap; the fourth means every such cap
has zero direct scalar. No star blocker remains: normalized `X5` already
forces all 168 stars blocked tautologically.

## Why three colour-fixed closures do not glue

The three fixed-colour packets correspond to coordinate contractions
`E00,E11,E22`. Each coordinate cap is inactive because two `Kcc` coordinates
vanish, and the packets do not prove that the three coordinate matrices lie
in one `V_T`. More importantly, cleanliness is cubic in `K`, so individual
coordinate cleanliness does not survive addition.

A literal aggregate guard makes this sharp. Set

```text
A_60[0,0]=A_71[0,0]=1,    r(E00)=R_01[0,0],
A_62[1,1]=A_73[1,1]=1,    r(E11)=R_23[1,1],
A_64[2,2]=A_75[2,2]=1,    r(E22)=R_45[2,2],
A_67[0,0]=A_67[1,1]=A_67[2,2]=1,   x=0.
```

Each coordinate response is one edge, so each coordinate error is zero.
But for `K=E00+E11+E22`, the three response edges are disjoint and

```text
E_67(K)=r^3/6=R_01[0,0] R_23[1,1] R_45[2,2] !=0.
```

Here the `R` cells are effective response cells produced by the displayed
spokes; the internal source blocks `A_01,A_23,A_45` are zero as part of
`x=0`.

This is a source-labelled aggregate guard, not an `X5` point. It proves that
coordinate closure alone cannot manufacture the required common clean cap.

## Consequence for the global spine

The minimum-layer failure has now been translated without another raw `X5`
solve:

```text
three colour-fixed pages
  --do not glue automatically-->
choose pair pq and triangle T
  --> active common K gives certified clean descent
  --> otherwise one of the four triangle memberships holds.
```

The exact remaining conjecture-level target is still
`normalized X5 + all 560 triangle carriers blocked => contradiction` (or a
wider cancellation-clean cap). The min-layer recursion supplies the literal
cap-response interpretation, but it does not select which of the four
blockers occurs.

## Replay

```sh
python3 computations/unaudited-codex-n8-minlayer-clean-cap-interface-2026-08-23/audit_minlayer_clean_cap_interface.py --write-results
python3 computations/unaudited-codex-n8-minlayer-clean-cap-interface-2026-08-23/audit_minlayer_clean_cap_interface.py --check-results
python3 -O computations/unaudited-codex-n8-minlayer-clean-cap-interface-2026-08-23/audit_minlayer_clean_cap_interface.py --check-results
python3 -I -S computations/unaudited-codex-n8-minlayer-clean-cap-interface-2026-08-23/audit_minlayer_clean_cap_interface.py --check-results
```

Hostile `--mutate` must fail. The logical digest is recorded in the result.
