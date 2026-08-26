# Fixed one-hot K8 quantum max-flow/min-cut audit

Status: **terminal negative result**.  Quantum cut ranks do not supply an
equality-case rigidity principle capable of forcing a three-channel internal
bottleneck or a clean pair in the fixed one-hot K8 network.

## Exact network and cut formula

Each site tensor has one physical leg of dimension 3 and seven virtual legs of
dimension 4.  For a physical terminal set `S` and a choice `U` of site tensors
placed on the `S` side, the nominal cut capacity is

```text
3^|S symmetric_difference U| * 4^(|U|(8-|U|)).
```

Exhausting the 256 choices of `U` gives the following minima, where `k=|S|`
and `1 <= k <= 4`:

| k | nominal min cut | GHZ flattening rank | deficit factor |
|---|----------------:|---------------------:|---------------:|
| 1 | 3  | 3 | 1  |
| 2 | 9  | 3 | 3  |
| 3 | 27 | 3 | 9  |
| 4 | 81 | 3 | 27 |

For `k=1,2,3` the unique minimizer is `U=empty`; for `k=4`, both
`U=empty` and `U={0,...,7}` minimize.  Thus every minimum can be obtained by
cutting physical legs only.  The one-site equality is tautological, while all
larger cuts have a strict rank deficit.  There is no saturated internal cut to
which an equality-case QMF/QMC theorem could apply.

The GHZ rank computation is literal: across every nontrivial bipartition its
flattening has precisely three nonzero entries, one for each constant-colour
row/column pair, so its rank is 3.

## Source-aware necessary inequality

For a bond block `A_uv`, the state

```text
|00> + sum_ab A_uv[a,b] |a,b>
```

has Schmidt rank `r_uv=1+rank(A_uv)`.  Any realized rank-three output therefore
obeys the weak necessary cut inequality

```text
product_(uv crossing U) r_uv >= 3
```

for every nontrivial site cut `U`.  It only says that the cut has either one
block of rank at least 2 or at least two nonzero rank-one blocks.  It does not
select a three-colour edge, a matching decomposition, or a clean pair.

## Two exact countercontrols

### K4 exact GHZ witness

Put one colour on each of the three perfect matchings of K4.  Direct enumeration
of all 81 output words gives exactly

```text
F_0000=F_1111=F_2222=1,
```

with every other output zero.  All six edge blocks have rank 1, hence all six
bond states have Schmidt rank 2.  The source-aware min cuts are 3 and 9, while
every GHZ flattening rank is 3.  This disproves the inference that a rank-three
output must come from a single internal bond carrying three colour channels.
The witness does have clean caps, so it is deliberately only a bottleneck
rigidity countercontrol, not a counterexample to clean-cap existence.

### K8 invisible chord

Start with the colour-zero matching `01|23|45|67` and add the colour-zero chord
`02`.  The chord cannot occur in a supported perfect matching: after using it,
sites 1 and 3 cannot be paired.  Exact enumeration of all 6561 words therefore
gives the same sole output `F_00000000=1` before and after adding the chord.
Nevertheless the `02` bond Schmidt rank changes from 1 to 2.  Thus the complete
top tensor, and consequently every flattening rank, fails to recover internal
bond support or capacity for this projector.

## Scope of X5 and theorem applicability

For N=8,d=3 the X5 equations are precisely the full mixed-output equations.
Together with pure normalization they assert that the realized top tensor is
GHZ.  Hence the flattening ranks above are consequences of that same output
equality, not additional source-coordinate constraints.

Generic quantum max-flow/min-cut results concern maximum or generic achievable
rank.  They do not classify low-rank equality for this fixed, highly
noninjective one-hot projector.  The physical-cut census, K4 bottleneck witness,
and K8 invisible chord jointly rule out using rank plus X5 alone to force a
literal internal three-channel bottleneck or clean pair.  Any clean-cap proof
must use finer coefficient/source equations than top flattening ranks.

## Reproduction

```sh
python3 computations/unaudited-codex-onehot-qmfmc-2026-08-21/audit_onehot_qmfmc.py --write-results
python3 -O computations/unaudited-codex-onehot-qmfmc-2026-08-21/audit_onehot_qmfmc.py
python3 -I -S computations/unaudited-codex-onehot-qmfmc-2026-08-21/audit_onehot_qmfmc.py
```

Frozen logical result digest:
`9504647717a08fa2e7cc34d38c7b0313e6ead296e7ccd1ebecf0207eb095f5f3`.

Pinned inputs:

- one-hot PEPS/Holant result:
  `d5029396bbe6347808d5e7c5cab4baf5bebcacc9eaba9d7f97405649d3d02221`
- zeon contraction result:
  `0861f75b1cb729d1550673a8ff9252c0fb756ef455e8a1f4c218bb7dc9aa3cc7`
