# Orbit-zero signed-`Counter` dependency/supersession audit

## Terminal verdict

The archived **301-row cutoff-8 leading residual and every artifact that uses
it as `R8` are invalid**.  The line `residual += Counter()` is not zero
cleanup: Python `Counter.__iadd__` deletes every nonpositive entry.  Before
that line, exact replay gives 651 nonzero quotient rows: 301 positive and 350
negative, total mass 3600, with deleted negative mass -110736 and coefficient
range [-1152,1152].  The frozen 301 rows are exactly the positive part.  The
same bug is repeated by `rebuild_r8()` in the archived T2 setup.

This does **not** invalidate the current load-bearing route.  Its `R8'` is the
independently reconstructed cutoff-9 120-orbit residual: 63 positive and 57
negative rows, total mass -23328.  Its reconstruction uses a signed dictionary
update that removes exact zeros only, replays a two-prime core and 71,492
reverse singleton pivots against the literal source ledger, and never calls
the buggy `rebuild_r8()`.  Importing the old T2 module is limited to
`row_k_degree`/orbit helper functions.

## Exact dependency graph

```text
exact 236-term cutoff-8 source certificate (VALID raw-105 replay)
  -> cutoff-8 K8 projection + Counter positive-part bug
     -> 301-row R8 (INVALID)
        -> old orbit expansion / double cosets / unary-square / partial301
        -> old radical seed
        -> old T2 pivot setup (INVALID)

cutoff-9 p1009+p1013 core + literal source-support ledger
  -> signed 120-orbit R8' (VALID; independent of 301-row R8)
     -> chart telescoping a*T (VALID)
        -> K14 interface (VALID)
           -> literal coefficient-collected K16 residual (VALID)
```

The exact cutoff-8 certificate remains valid: byte SHA
`62c33fbc985b94b3d688645bbc494c29566ecca3dc3de8c52b859915ce980c2c`;
its independent raw-105 audit is
`0f514d5d41e2dff9d44a2b357699dbf879f74f826f8e7cfbcf77bc1424cdce58`.
Only the subsequent associated-graded extraction is retracted.

## Load-bearing byte hashes

| object | byte SHA-256 | signed-arithmetic guard |
|---|---|---|
| signed cutoff-9 `R8'` | `62013c8a8453ffe68e6ef08740859db6efecaf825f121c19dc885b6afa7feb4b` | 120 rows, both signs, mass -23328; exact core/reverse replay |
| chart telescoping | `419e1ddda08c7a8141a886973ae76b441b613b988f9e8c94b33e907e626330b5` | pins the preceding `R8'` byte hash |
| K14 interface | `a67a08fd97c5cd10cfb5e7dd72db2502971c16408bd058dce4d12cbbb2f0adb3` | pins the preceding `R8'` byte hash |
| literal K16 collection | `28a648a2625d208cc86948b27a06f52f38245fe2ebe130c583e619d1d24b9189` | pins `R8'`; collects in `defaultdict(Fraction)` and drops exact zeros only |

The chart telescoping source contains unary `+Counter` at multiplication/formal
normalization points, but its inputs there are positive matching packets or a
formally checked final identity; it does not apply positive-part normalization
to `R8'`.  The K14 and literal-K16 collectors contain no
`counter += Counter()` cleanup on the signed residual.

## Retracted artifacts

| archived object | byte SHA-256 | reason |
|---|---|---|
| cutoff-8 positive residual | `98203f265402e1be81ec0916cd4204ab7e6c90b59f45cdeb848c6ee93000b000` | exact positive part of a 651-row signed residual |
| T2 pivot setup | `036018897a1fe5b4f45d65af4e0e2d0cb3ea73336dc947ef6d7d2272ce2a6af7` | rebuilds and positive-parts the same residual |
| old R8 orbit expansion | `3d2184f12618a3f6e5df4df5be45a70de2864b00ede1e2b124b035d32d9d6a13` | pins invalid 301-row input |
| old R8 double-coset census | `5d9a7f31ec43b949210effae316eeddfbe73367fa7f3b087d6d5f789e7b602c8` | pins invalid 301-row input |
| old unary-square result | `70e0d5d9c3af3f0841c6afd21a8f0abde251987db62f722d3870f92ca0a73624` | pins invalid 301-row input |
| old radical seed | `c854b6e86cfedbf8fa61b403719656f13bd5f573af1af309d0e3b18de10a548b` | pins invalid logical hash `25d4acd...` |
| old `partial301` packet | `9a195ac57f8a38b01957ecf987be4e9c111a361525917cbe3c21db58005d7478` | generated from invalid 301-row input |

Any theorem-shaped statement in the old dangerous-chart or old T2 reports
whose antecedent is “the 301-orbit `R8` represents `T` modulo `I_mix+K^9`” is
superseded by the signed cutoff-9 `R8'` statement.  `R8'`-labelled descendants
pinning `62013c...` are not in the retraction set.

## Complete occurrence audit in this dependency slice

There are five Python sources with `+= Counter()` in the slice.  The two
cutoff-7 occurrences are context-safe here: replaying the raw signed sums
without `Counter` normalization gives exactly the target, with zero negative
rows (chart26: 239 rows, coefficients 1..16; orbit0: 10 rows, 1..288).  The
dangerous-chart degree-two square system includes every supported degree-0/2
row, so its final replay cannot hide an unmodelled row; its use is likewise
context-safe.  The cutoff-8 residual and T2 rebuild occurrences are the two
unsound ones.

## Replay

Run:

```sh
python3 computations/unaudited-codex-orbit0-signed-counter-dependency-audit-2026-08-23/audit_signed_counter_dependency.py
python3 -O computations/unaudited-codex-orbit0-signed-counter-dependency-audit-2026-08-23/audit_signed_counter_dependency.py
python3 -I -S computations/unaudited-codex-orbit0-signed-counter-dependency-audit-2026-08-23/audit_signed_counter_dependency.py
```

The result logical SHA-256 is
`10a891ff4277cb47cc3b4e732b3f943c3116c44a47fdae577ca13ccf648fad58`.
