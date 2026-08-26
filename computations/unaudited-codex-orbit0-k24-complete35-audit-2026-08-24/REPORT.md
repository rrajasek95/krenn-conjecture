# K24 exact 35/35 charge assembly and conservation-hypothesis audit

## Outcome

The fail-closed source-extracting assembler accepts exactly the frozen 10 scalar groups and 35 lineage IDs, with no missing, duplicate, or extra group/ID.  Every group scalar is read from its pinned raw producer result, checked against its pinned acceptance/referee, checked at `U=400591699200`, checked `full=irreducible`, and counted once irrespective of the number of IDs in its source group.

The exact assembled K24 charge is

```text
1918892561475083010048 / U
= 832852674251338112 / 173867925.
```

The pinned K14-through-K23 ledger forces the conditional compensation

```text
1910994764731277672448 / U
= 829424811081283712 / 173867925.
```

Thus the exact excess and cumulative K14-through-K24 charge are

```text
7897796743805337600 / U = 19715328.
```

## Strict source ledger

| source group | IDs | scaled charge |
|---|---:|---:|
| `source_D14_R2_2_2_4` | 1 | `645926683714155380736` |
| `source_D14_R2_4_4` | 1 | `97324923903254986752` |
| `source_D14_R3_3_4` | 1 | `104945403010833285120` |
| `source_D14_R4_2_4` | 1 | `64033288812772392960` |
| `source_D15_R2_3_4` | 3 | `232469436926413209600` |
| `source_D15_R3_2_4` | 3 | `220287135823033466880` |
| `source_D16_R2_2_4` | 6 | `107213275439239495680` |
| `source_D16_R4_4` | 6 | `150102648402491473920` |
| `source_D17_R3_4` | 7 | `233614955677836902400` |
| `source_D18_R2_4` | 6 | `62974809765052416000` |

The individual evidence paths and SHA-256 pins are embedded beside every extracted group in `results_k24_complete35_exact.json`; the frozen manifest also pins both the expected-group contract and the prior exact ledger/referee.

## Exact theorem classification

There is a valid exact conservation theorem: the frozen functional kills the original structured target and all `1162/1162` complete balanced degree-24 source-column profiles, so any genuine complete exact source-column subtraction has total charge zero.  Therefore `+19715328` is impossible **for a ledger that really is such a subtraction**.

The present arithmetic sum is nevertheless exact as a 10-group artifact sum.  Its nonzero total contradicts, rather than proves, the remaining linkage hypothesis that the assembled K14-through-K24 pages are one complete source-faithful subtraction.  The reducer also records a literal K16 critical-pair obstruction: all-dividing-pivot averaging is a specified choice, not a confluence theorem.  Consequently the residual is a valid acceptance obstruction to the purported complete filtered reduction, but it does not prove K24 nonmembership, a policy-independent normal form, or any Krenn-Gu conjecture verdict.

The fail-closed guard is: do not promote this ledger to a complete reduction, terminal-span result, relative membership result, or conjecture decision until a source-labelled K14-through-K24 replay under one specified policy has exact zero total and pins every lower transfer.

## Replay and hostile modes

Run the assembler and theorem audit from the repository root:

```text
python3 computations/unaudited-codex-orbit0-k24-complete35-audit-2026-08-24/assemble_k24_complete35_source_exact.py
python3 computations/unaudited-codex-orbit0-k24-complete35-audit-2026-08-24/audit_k24_conservation_hypotheses.py
```

The assembler rejects 12 hostile cases (missing/duplicate/extra group, group multiplication, sign, U, evidence hash, forced-target sign, full/irreducible scalar and count, and ID scope).  The theorem auditor rejects six hypothesis promotions/mutations.  Both hostile suites pass under standard Python, `-O`, and `-I -S`.

## Terminal pins

- source manifest: `09c278324ec825718e1b17bf9f1f938c1a62fa3c3fb8069adb30b3cc81aceb7b`
- source-extracting assembler: `b02e6c9259c43c2c5f4fb2697ca31c7714727cece218689224756a5be7b5aaab`
- exact 35/35 result: `c9823d5c33b7e11b0c92eb89a50b33de0223fea5fdf53b2838b1094e13b9dfe6`
- theorem-hypothesis auditor: `413cc30c0e30302f93ed726e780ea72bc5c75dc57c91608256e878bbeeb043d4`
- theorem-hypothesis result: `74ea88b19e8cc146f9eb1b0c3eda2df145a2606d9e0a5e5c820d642f2c8660eb`
- independent conservation package exact result: `7a33791664ac3b92dc6489c1a8160364a8fd3347508ff7cf760803e0b7372df8`
- independent conservation/scope referee: `582a5da53157ae475d37a8a9ee9e5233eab4dc4c71ca207ae3b47d83f323dae3`

No charge producer or other heavy computation was launched by this assembly/audit package.
