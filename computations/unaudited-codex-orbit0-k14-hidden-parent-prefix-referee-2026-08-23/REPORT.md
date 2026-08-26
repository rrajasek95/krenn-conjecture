# Independent hidden K14→K16 parent-prefix referee

## Verdict

`PASS_PREFIX_OCCURRENCE_REPLAY_WITH_FULL_COUNT_SCOPE_GUARD`.  Cycle's bounded
31/485-slice prefix is source-faithful: it emits 4,837,984 pivotable K16 parent
occurrences, and a deterministic 257-record source replay independently checks
the literal row, anchor signature, valid first pivot/count, available second
pivots/count, exact coefficient, and sign.

It is not a full recovery.  The value 75,691,040 is pinned from the old full
collector and copied into the prefix result; the prefix itself does not
reconstruct that full count.

## Sign and provenance

For `P=-R8′E0E1E2`, cancellation of the K14 head gives the stored parent weight

```text
+mass*U/m1,  U=400591699200.
```

A second pivot emits `-mass*U/(m1*m2)`, so Cycle's length-one positive and
length-two negative conventions are correct.  Each 64-byte occurrence retains
the literal K16 row, U-scaled coefficient, signature, R8 slice, the three
factor-tail indices, first pivot/tail index, and both denominators.  From the
row and signature one recovers every second pivot and its 12/32/60 K2/K3/K4
tails.  This is sufficient provenance for `[2,2]`, `[2,3]`, `[2,4]`, and the
next `[2,2,2]` page.

## Aggregation and replay scope

The 1,394,334-record profile file is correctly tagged with wildcard degree
zero after Cycle's patch.  It is an exact **labelled** profile aggregation, not
an H-canonical quotient.  The occurrence stream, paired with the pinned all-78
tail tables, is the load-bearing continuation interface.

Cycle's exhaustive format replay reconstructs all prefix rows and coefficients.
It does not recompute the semantic pivot sets for every record; this referee
does so on 257 evenly spread records.  Standard, `-O`, and `-I -S` modes agree.
No child-tail stream or full 485-slice recovery was launched here.
