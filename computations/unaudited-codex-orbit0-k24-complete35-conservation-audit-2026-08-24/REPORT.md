# Complete K24 charge assembly and conservation audit

## Outcome

The authoritative accepted K24 fragments assemble exactly once into all **10 frozen scalar groups and all 35 frozen lineage IDs**.  There are no missing, duplicate, extra, or regrouped IDs.  All 35 terminal K4 responses have anchor mass zero, so there is no K25 continuation in this recurrence.

The exact K24 charge is

```text
832852674251338112 / 173867925
```

or, at `U = 400591699200`,

```text
1918892561475083010048 / U.
```

The sealed K14--K23 ledger requires K24 compensation

```text
829424811081283712 / 173867925
= 1910994764731277672448 / U.
```

The difference is therefore exactly

```text
+19715328
= +7897796743805337600 / U.
```

Thus `sum(K14..K24) = 19715328`, not zero.

## Strict group ledger

| group | IDs | charge scaled by U | terminal occurrences |
|---|---:|---:|---:|
| `source_D14_R2_2_2_4` | 1 | `645926683714155380736` | `34216879080` |
| `source_D14_R2_4_4` | 1 | `97324923903254986752` | `60681898800` |
| `source_D14_R3_3_4` | 1 | `104945403010833285120` | `161268940800` |
| `source_D14_R4_2_4` | 1 | `64033288812772392960` | `82522944000` |
| `source_D15_R2_3_4` | 3 | `232469436926413209600` | `358355558400` |
| `source_D15_R3_2_4` | 3 | `220287135823033466880` | `193212825600` |
| `source_D16_R2_2_4` | 6 | `107213275439239495680` | `164736458640` |
| `source_D16_R4_4` | 6 | `150102648402491473920` | `71208252000` |
| `source_D17_R3_4` | 7 | `233614955677836902400` | `50538086400` |
| `source_D18_R2_4` | 6 | `62974809765052416000` | `13856256000` |

Grouped scalars are counted once, never once per lineage ID.  The assembler pins every raw result and its acceptance/referee evidence.  It rejects omitted or duplicated groups, duplicate or regrouped IDs, a sign change, a wrong `U`, and multiplication of a grouped scalar by its ID count.  The independent audit adds wrong-target-sign and false promotion to ideal nonmembership or a conjecture verdict.  Standard Python, `-O`, and `-I -S` give identical independent-audit output SHA-256 `582a5da53157ae475d37a8a9ee9e5233eab4dc4c71ca207ae3b47d83f323dae3`.

## What conservation proves—and does not prove

The 77-functional annihilates all 1,162 abstract balanced source-column profiles, and the original structured `a*T` has functional value zero.  Therefore any complete exact subtraction of complete balanced source columns from `a*T` must retain total value zero.  Since the assembled terminal ledger has value `19715328`, the following conjunction cannot be accepted:

1. every K14--K24 fragment is linked occurrencewise to the same source-faithful reduction;
2. the frozen 35-ID DAG is complete for that reduction;
3. all signs, normalizing pivot divisors, and charges use one convention; and
4. the assembled pages are the complete terminal normal.

This is a genuine **filtered acceptance obstruction**: it rejects the present 35-ID ledger as a conservation-valid completion and blocks relative K24 production.  It is not an ideal-nonmembership certificate.  The same functional pairs with `a*T` as zero, so it cannot separate `a*T` from the mixed source ideal.  The mismatch diagnoses an inconsistency among the recurrence premises; it cannot be reinterpreted as a proof merely by calling the nonzero terminal normal an obstruction.

Terminality rules out a future K25 repair.  The repair must instead locate a missing/duplicated lineage, a sign or `U` normalization error, or a source-provenance mismatch somewhere in K14--K24 (or revise the claimed conservation interface).  Exact 35-ID equality only excludes those errors relative to the frozen DAG; it does not prove that the DAG itself retained every source occurrence correctly.

## Relation to the Krenn--Gu conjecture

This computation is on the single orbit-zero, anchors-one chart and the localized/powered multiplier target `a*T`.  It does not cover the other 30 charts and does not establish the global implication from a hypothetical general bicoloured source to this chart calculation.  Consequently it proves neither the general bicoloured `n=8,d=3` case nor the all-even-order Krenn--Gu conjecture.  The repository's independently proved `(6,3)` theorem and the `n=8` block-diagonal stratum remain the strongest completed conjecture cases; the general bicoloured `n=8,d=3` case remains open.

After the conservation defect is repaired, a local terminal certificate still requires the full relative operator

```text
B = (L,T),     A24_rel = T restricted to ker(L),
```

and either an exact solve `B*x=(0,0,0,R24)` or a complete exact rank/dual certificate deciding whether `R24` lies in `T(ker L)`.  Charge-only group scalars do not retain the K20/K22/K23 lower projections or the K24 row-orbit residual needed for that test.  A genuine charge separator would instead have to annihilate the source columns and pair **nonzero** with `a*T`; the present 77-functional does not.

The separate global proof gap is still the branch

```text
X5 + all 560 triangle carriers blocked  ==>  contradiction
```

or an equivalent same-source clean-cap/descent theorem, together with provenance-preserving transport across the remaining charts.  The orbit-zero result advances none of those global arrows until its own conservation failure is reconciled.

## Authoritative files

- Frozen K24 partition: `computations/unaudited-codex-orbit0-k24-availability-schedule-2026-08-24/results_k24_availability_schedule.json` (`ec91fa81...`).
- Complete K14--K23 ledger: `computations/unaudited-codex-orbit0-filtered-charge-ledger-through-k23-2026-08-24/results_charge_ledger_through_k23.json` (`45c94294...`).
- Strict assembly: `results_k24_complete35_conservation.json` (`7a337916...`).
- Independent audit: `results_k24_complete35_independent_audit.json` (`582a5da5...`).
- Independent cross-check assembly: `../unaudited-codex-orbit0-k24-complete35-audit-2026-08-24/results_k24_complete35_exact.json` (`c9823d5c...`).
- Second conservation/scope audit: `results_k24_complete35_conservation_audit.json` (`d4eac8af...`).
- Exact 77-functional premise: `computations/unaudited-codex-orbit0-k16-weighted-dafsa-2026-08-23/results_k16_cycle_partition_quotient.json` (`d4cbc735...`).
- Relative terminal interface: `computations/unaudited-codex-orbit0-k24-relative-column-interface-gate-2026-08-24/REPORT.md` (`947d8b63...`).
- Current global missing-arrow audit: `computations/unaudited-codex-current-route-archive-audit-2026-08-22/REPORT.md` (`2c22b369...`).

All paths in the machine-readable assembly carry full SHA-256 values.  This directory is unaudited working evidence, not a promoted proof-spine certificate, and no heavy computation was launched by the assembly/audit.
