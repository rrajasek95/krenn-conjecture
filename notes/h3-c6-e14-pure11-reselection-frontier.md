# Exact frontier after the first E14 internal extension

## Result

The entire one-extra-internal-cell layer after the minimal E14 chart is now
reduced exactly.  Among the 1,020 chart/cell records there are

```text
ordinary source units                         996
Hall-intersecting alternate-X1 reselections    18
fixed-hole diagonal-C4 reselections              6
                                               ----
                                              1020.
```

Thus the layer is exhausted as a source reduction, but not all of it is an
emptiness theorem: 24 records reselect the pure `X1` target.  The rank and
termination consequences of those reselections remain separate.

Checker:
`computations/verify_h3_c6_e14_pure11_reselection_frontier.py`.

## Sharpening the 36 pure-11 records

The first second-tail census `8f58910` found 36 pure-`11` records for which
the frozen target/zero collision acquires a nonzero unordered-hole bracket.
The bracket is an effective alternate pure-`X1` matching.  Expanding every
complete `G11` word gives the stronger split

```text
literal companion-row unit                    12
alternate X1 hole meets selected X2 hole 34    18
alternate X1 hole remains 01                    6.
```

For the 12 unit records, a literal mixed zero word has complete coefficient
the negative of `G11[111111]`.  With `F_target=T-1` and
`F_companion=-T`, the ordinary identity is

```text
-F_companion-F_target=1.
```

This uses the whole endpoint polynomial and requires no localization.

## The 18 Hall landings

The alternate `X1` endpoint hole is one of `03`, `04`, or `14`.  Each meets
the selected `X2` endpoint hole `34`.  Therefore these records enter the
existing star/triangle/`K2,2` Hall-accessibility interface immediately after
reselection.

This is an incidence landing, not a deleted-star rank theorem.  In
particular, the checker does not claim that the resulting pair already has
four ranks three or reaches the clean cap.

## The six earliest source-connectivity records

Exactly six records avoid that Hall intersection.  They are

```text
old X1 tail:       1 or 3
selected X2 tail:  1, 2, or 3
new cell:          q24:11
fixed X1 hole:     01
alternate X1 tail: 24|35 (tail 2).
```

For old tail 1, the two pure target tails differ by the diagonal cycle

```text
23 - 35 - 54 - 42 - 23,
```

and for old tail 3 by

```text
25 - 53 - 34 - 42 - 25.
```

These are affine pure-target `C4` switches: the target equation only says
that the two matching contributions participate in the same nonzero target
coefficient.  It does not provide the coefficientwise Segre equality needed
for the existing flat-cycle gauge theorem.  The missing input is therefore
source exhaustivity for the complete companion rows: they must provide a
typed attachment, a flat complete-column dependence, or a Hall/off-anchor
exit.  This six-record family is the earliest actual local
source-connectivity packet after `222c66d`.

## Dependency consequence

Combining the old census with the mixed-10 companion theorem gives the 996
units:

```text
969  unchanged original units
 15  formerly defective mixed-10 companion units
 12  pure-11 companion units.
```

Every first off-diagonal/asymmetric extension is therefore an ordinary
source unit.  The only first-layer non-units are pure-target reselections:
18 enter Hall/active-rank accessibility, and six enter the affine diagonal
`C4` source-exhaustivity gate.  No larger one-cell census is needed.

This result neither enumerates simultaneous two-cell additions beyond the
forced alternate matching already present nor proves the global termination
potential.

## Verification

```text
python3 computations/verify_h3_c6_e14_pure11_reselection_frontier.py
python3 -O computations/verify_h3_c6_e14_pure11_reselection_frontier.py
python3 -I -S computations/verify_h3_c6_e14_pure11_reselection_frontier.py
```

Frozen ledger SHA-256:

```text
1e53202218683be805c5069846190068a5d9adb0d166aaf14d703e6fbc55c343
```
