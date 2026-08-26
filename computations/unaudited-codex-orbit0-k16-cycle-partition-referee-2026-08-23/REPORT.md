# Exact referee: balanced-port cycle quotient at K16

## Terminal result

`PASS_EXACT_Q_ABSTRACT_SEPARATOR_WITH_CONSERVATION_GUARD`.

The independent checker enumerates all `320` partitions of `24` with parts at
least two and all `1,162` abstract four-path-plus-closed-cycle profiles.  The
corresponding `105`-term perfect-matching completion vectors have exact rank
`271` over `Q`, hence a `49`-dimensional cokernel.  The connected-block weights
are exactly `w_1=1, w_2=2, w_3=8, w_4=48` (total `105`).

Streaming the frozen `1,848,174` weighted K16 target rows, without traversing
the `98,609,090`-column language, gives `118` nonzero cycle coordinates and
raises the exact rank to `272`.  The replayed primitive integer dual has
support `77`, maximum absolute coefficient `2,956,800`, annihilates all `1,162`
abstract completion profiles, and pairs the K16 target by `-311,258,112`.

## Exact scope guard

This proves a leading-filtration cycle charge: every *complete* balanced
degree-24 source column is killed by the functional, while the frozen K16
residual carries nonzero charge.  It is not a full ideal or localized
nonmembership certificate.  Independently reconstructing the original
structured `a*H0*H1*H2` vector gives support `30`, mass `105^3=1,157,625`, and
dual pairing `0`; omitted filtration layers/corrections must carry the
compensating charge.  Thus the theorem is conservation/migration across K
layers, not a terminal obstruction to the original target.

## Replay

Run:

```text
python3 computations/unaudited-codex-orbit0-k16-cycle-partition-referee-2026-08-23/audit_balanced_cycle_partition_referee.py
```

Artifacts:

- `results_balanced_cycle_partition_referee.json`, logical digest
  `ed18303a4bb5f211d4b6313330c028ae2354957e3ce8b89e615eeb29954f6c1e`;
- `replayed_cycle_partition_dual.tsv`, SHA-256
  `fea91d03250128fa6ea99252659ddd2b46329a9318916a19d6dae0ecfb69dd84`;
- `replayed_target_cycle_vector.tsv`, SHA-256
  `b4964cbc96fb217fa84fb6cd62942ee0738f0feafe421137e28ade82644035dd`.

The two replayed ledgers are byte-identical to the independently produced
Tail ledgers.  The literal target is decoded afresh into its 24-port
2-regular multigraph before projection.
