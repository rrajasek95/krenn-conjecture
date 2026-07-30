# Certified-spine supersession ledger

This ledger is append-only.  It is initially empty because
`certified-spine-2026-07-30` is the certification baseline.

A research result, computation, or author self-check does not modify the
certified spine.  A supersession is accepted only when all of the following
are recorded:

1. the stable dependency ID from [`BASELINE.md`](BASELINE.md), or from an
   earlier accepted supersession;
2. the exact old file and certified commit being replaced or narrowed;
3. the new theorem or guard, with its exact hypotheses and scope delta;
4. the new proof artifact and exact checker, when computation is used;
5. an independent audit performed by an agent other than the author;
6. the audit outcome and every correction it required; and
7. the commit that contains the audited replacement.

Use this record format:

```text
## SUPERSESSION-YYYY-MM-DD-NN

- Dependency ID:
- Replaces:
- Replacement:
- Scope delta:
- Proof artifact:
- Checker:
- Independent auditor:
- Audit outcome/corrections:
- Certified commit:
```

After appending an accepted record, update the current consolidated spine in
the same commit or in a directly linked follow-up commit.  Claims not covered
by the named scope delta retain their prior certified status.  Negative
guards may narrow a dependency or invalidate a proposed implication, but
must not be described as positive closure.
