# Ledger discipline: hash content, and always ship a positive control

**UNAUDITED proposal. Pinned HEAD `7d57c552a3ef57d3a95c3bc933af547ad55e087d`.
Written against the external audit of 2026-08-13
(`computations/unaudited-external-spine-audit-2026-08-13/REPORT.md`),
systematic issues section.**

The audit's two systematic findings are that frozen ledgers across the
foundations layer hash counts, strings and booleans instead of mathematics,
and that no audited checker ships a control. Both are cheap to fix and both
are fixed in the five repair candidates in this directory. This note states
the two rules and demonstrates the first one on the sl2 prism checker, which
the audit named as the extreme case.

---

## The demonstration

`ledger_discipline_demo.py` (this directory) reads
`computations/verify_h3_sl2_weyl_cartan_prism.py`, builds five textual
variants in memory, executes each, and reports the frozen-ledger digest.
Nothing is written and nothing in the repository is touched.

| variant | what it is | `ledger_sha256` |
| --- | --- | --- |
| **V0** | the file as committed | `bde6a55fb7061024ff741b38acd22f02d2299d7e77f704eebeb9298b7b5abbb2` |
| **V1** | V0 with `require` replaced by `return None` — every mathematical check deleted | `bde6a55fb7061024ff741b38acd22f02d2299d7e77f704eebeb9298b7b5abbb2` |
| **V2** | V1 **and** the signed Weyl action mutated, `(-1)**a` → `(-1)**b` | `bde6a55fb7061024ff741b38acd22f02d2299d7e77f704eebeb9298b7b5abbb2` |
| **V3** | V0 with a content-hashing ledger (rolling sha256 of the computed Weyl images, their expected values, and the Cartan homotopy images) | `b5efd5075b0543169ce71107e2f4be379651a4cbcec325dca8f840aa02bab5a6` |
| **V4** | V3 with the checks deleted **and** the same Weyl mutation | `bd5fdde4aebc8f3c58e38cd7b828494d26dad105c0977c9bcc04bc07f6366bea` |

Read V2. A copy of the checker that computes a **false** Weyl action and
performs **no verification at all** publishes the pinned digest of the
committed file, byte for byte. The frozen ledger of that file is

```python
{"theorem": ..., "polynomial_degrees": [0, 6], "exterior_degrees": [0, 2],
 "basis_states": 112, "weyl_factorization": "...", "homotopy": "...",
 "identities": [...], "scope": "..."}
```

— one integer that counts loop iterations, and eight strings. None of it
depends on a single coefficient the checker computed. The digest attests to
the *prose*, not to the mathematics.

V3 versus V4 is the fix: one extra rolling hash over the actual computed
vectors, and the same mutation now moves the digest even with every check
removed.

---

## Rule 1 — the frozen ledger must hash mathematical content

A ledger entry earns its place only if changing the mathematics changes it.

**Hash these.** Monomial lists and their coefficients; evaluation vectors of
a covector on a column block; rank vectors; orbit representatives together
with the invariant computed on them; solution vectors and their
denominators; the literal decorated cells a colour word assigns.

**Do not let these carry the ledger alone.** Counts (`len(...)`, loop
counters), prose fields, hardcoded booleans, and restatements of the theorem.
They are fine as *additional* entries; they must never be the only entries.

**A practical test.** Neuter `require` (replace its body with `return None`),
then mutate the geometry the file is about. If the digest survives, the
ledger is content-free. This is exactly what `ledger_discipline_demo.py`
automates, and it takes under a second.

**A cheap idiom that always works.** Where the content is large, stream it:

```python
rolling = sha256()
for index, item in enumerate(canonically_ordered_items):
    rolling.update(f"{index}|{item}\n".encode())
ledger["evaluation_stream_sha256"] = rolling.hexdigest()
```

The five repair candidates in this directory use exactly this, e.g.
`verify_activity_overlap_ranks.py` hashes all 461,700 computed
`(branch, rank_before, rank_after)` triples, and
`verify_lambda_kills_operator_block.py` hashes the per-column Lambda
evaluation vector *and* every nonzero bridge sub-column of the
8,580-column operator.

**Corollary (self-pins).** `EXPECTED_LEDGER_SHA256` living in the same file
as the ledger cannot catch intentional restatement — the author who changes
the claim also changes the pin. That remains true here. Content hashing does
not fix the self-pin problem; it fixes the *different* problem that the pin
currently protects nothing mathematical. A separate registry of digests,
outside the checkers, is the complementary repair and is not proposed in
this note.

---

## Rule 2 — every checker ships at least one positive control

A checker that has never been observed to fail has not been observed to do
anything. Each repair candidate here runs, **in the same process and before
its own audit**, at least one *fabricated-geometry* variant that must raise:

```python
def should_fail(label, thunk):
    try:
        thunk()
    except RuntimeError as failure:
        return {"control": label, "fired": True, "reason": str(failure)[:200]}
    raise ControlDidNotFail(("positive control did not fail", label))
```

Two properties matter.

1. **Fabricate the geometry, not the assertion.** A control that flips a
   comparison operator proves the comparison runs; a control that moves the
   direct-free pair from `{3,6}` to `{3,7}`, or heats the wrong site in a
   hybrid word, proves the *mathematical input* reaches the check. The
   controls in this directory are all of the second kind.
2. **The control's firing goes into the ledger.** `{"control": ...,
   "fired": true}` is recorded, so a future edit that silently disarms a
   control changes the digest.

Rule 2 is deliberately weaker than mutation testing: it is one fabricated
input per checker, always executed, costing milliseconds. Mutation testing
of the main claim is still worth doing at review time, and the results for
these five candidates are in `REPORT.md`.

---

## What this does not fix

Content hashing and controls make a checker's digest *mean* something. They
do not make a stipulated model physical. The audit's CRITICAL findings —
the operator-to-physical chain map for K, the derivation of eta/sigma, the
attainability-versus-equality of `D2 = -delta`, the source typing of `x_v` —
are theorem work, not checker work, and none of them is touched here.
