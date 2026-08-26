# Cross-agent referee: `D14:222|R:3-2-2`

Status: `PASS_TERMINAL_CROSS_AGENT_REFEREE_D14_222_R_3_2_2_K21_SINGLETON`.

The sealed producer manifest and every upstream binary/source hash replay.
The exact result is

```text
-832152508704647184384 / 400591699200
= -32834300375025536 / 15806175.
```

The referee independently parsed all 485 R8 records and recovered 838,080
heads, source mass `-40310784`, and L1 mass `385689600`.  All recurrence
identities and denominator histograms replay: 6,619,280 first pivots;
211,816,960 K17 candidates; 197,414,400 pivotable K17 children; 815,482,880
second pivots; 9,785,794,560 K19 candidates; 2,969,658,880 pivotable K19
children; 5,075,412,480 third pivots; and 60,904,949,760 K21 children.

The direct coefficient is `-M`; three normalized responses produce
`+M/(m1*m2*m3)`, and every observed product divides U.  Signature mass follows
`10 -> 7 -> 5 -> 3`, while every pivot has mass four, so all K21 children are
terminal and full equals irreducible.

Without rerunning the aggregate, the Rust referee rebuilt all 257 distributed
nonzero-charge source heads and the recorded row17/row19 provenance.  It
literally evaluated 3,084 recorded terminal-K2 children and independently
searched a nonzero terminal continuation for each head, evaluating another
3,084 children.  All were terminal; all 257 recorded terminal charges matched.

Cross-agent logical SHA-256:
`c6a04781dc56763c28a9ae164aab5138e381e255d4830ad73e05fd89f185c5dc`.
Scope is this singleton K21 scalar only: no full rerun, K22, or other lineage.
