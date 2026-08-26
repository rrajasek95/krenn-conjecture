# Feasibility — a Lean 4 proof of the eight-site diagonal obstruction

> **UNAUDITED — lane L1, 2026-08-20.** Pinned krenn-conjecture HEAD
> `f9a3bd6b93417a43d86ad782d1f76b62f14bc50a`. Not spine. Nothing has been
> submitted anywhere and nothing here proposes that it should be; opening a
> formal-conjectures PR is the user's decision.

## 1. Bottom line

**Feasible, and the part everyone assumes is the hard part is already done.**

The certificate layer — the thing that would sink the project if it were going
to sink — is finished. All 87 orbit refutations are Lean theorems with a
kernel-proved soundness chain, they build in **19 seconds**, and the embedded
certificate payload is **29 MiB**, less than half of algal's accepted-track
64 MB. The proposed registry statement **compiles clean against the real
upstream module** at the toolchain formal-conjectures pins, `--wfail`, 82
additions / 0 deletions, and three of its declarations are already sorry-free
proofs.

What remains is entirely the *mathematical bridge*: get from "a diagonal `W`
satisfies `EqSystemN 8 3`" to "the Boolean assignment satisfies orbit `k`'s
CNF". That is ordinary — if substantial — Lean work, estimated at **13–19
agent-sessions**, with two steps carrying most of the risk (§3).

The honest comparison: algal's (6,3) proof is 9,313 hand-written lines plus
343,407 generated. Ours should be *smaller* in hand-written terms, because our
Boolean variables are semantic (hafnian-vanishing predicates) rather than
per-edge, so our clause-soundness lemmas are hafnian identities rather than a
Laurent-certificate algebra layer. But it is the same order of project, and it
should be planned as one.

## 2. Measured cost of the replay layer

Everything in this table was run on this machine today; none of it is estimated.

| quantity | value |
|---|---|
| orbit refutations built as Lean theorems | **87 / 87** |
| `lake build` wall time, all 87 | **19.22 s** (18 cores; 64 s CPU) |
| per orbit | ~3.5 s; 353 MB peak RSS in isolation |
| LRAT payload | 12.65 MiB (min 41 KiB / mean 149 KiB / max 420 KiB) |
| CNF payload | 16.41 MiB, **byte-identical** to the certified package (sha256 87/87) |
| combined `include_str` payload | **29.06 MiB** |
| LRAT production time | 6.4 s for all 87 (CaDiCaL 3.0.1) |
| independent LRAT re-check | drat-trim `lrat-check` 87/87 `c VERIFIED` |
| Lean `verifyCert`, interpreted | 87/87 `true`, 59.8 s |
| axiom closure | `[propext, Classical.choice, Lean.ofReduceBool, Lean.trustCompiler, Quot.sound]`, no `sorryAx` |
| dependencies needed for this layer | **none** — `Std.Tactic.BVDecide` ships in the toolchain |

Bound for the finished project: the replay layer is ~20 s; the upstream
formal-conjectures module is 52 s once mathlib is cached; algal's comparable
complete build is 22 min. **A finished build here should be well under an hour**,
and the certificate payload is not a constraint.

### 2.1 Two findings that would have cost a later lane real time

**(i) `drat-trim -L` output is rejected by Lean's LRAT checker.** Converting our
87 stored `.drat` certificates with `drat-trim CNF DRAT -L OUT.lrat` produces
files that drat-trim reports `s VERIFIED` on and that drat-trim's own
`lrat-check` reports `c VERIFIED` on — and that Lean *parses* successfully
(`LRAT.parseLRATProof` returns `.ok`, 1,182 actions for orbit 0) — but on which
`Std.Tactic.BVDecide.LRAT.check` then returns `false`. A minimal four-clause
instance converts fine, so it is not a gross format error; it appears at scale.

Worse, in **forward** mode (`-f`) drat-trim prints "optimized proofs are not
supported for forward checking" and emits LRAT that *its own* `lrat-check`
rejects (`c NOT VERIFIED`). `-f` must never be used to produce LRAT. Since our
existing replay scripts invoke drat-trim as `drat-trim CNF DRAT -f`, this is an
easy trap to walk into.

**Fix, adopted:** produce LRAT natively with
`cadical <cnf> <lrat> --lrat=true --no-binary --checkproof=2`, which is what
algal does. Lean accepts all 87. This is not a weakening of the chain: the CNF
remains the audited artifact, and the LRAT is an independently produced
refutation of that same CNF, checked by CaDiCaL's internal LRAT checker, by
drat-trim's `lrat-check`, and by Lean. The stored DRAT files remain the audit
lane's record and are untouched.

**(ii) A kernel-only replay does not exist at this scale.** The brief assumed
"algal used `native_decide`; a kernel LRAT replay would be strictly stronger".
Both halves need correcting. algal's LRAT step already goes through
`Reflect.verifyCert_correct`, a **kernel-proved** soundness theorem;
`native_decide` only executes the verified checker. And replacing that
`native_decide` with `decide` on one of our orbits **stack-overflows the kernel
in 1.2 seconds** (`skeleton/lrat-probe/LratProbe/Kernel.lean`, `rc=134`, even
with `maxRecDepth 100000`). So the trust story available to us is exactly PR
#4610's, and exactly `bv_decide`'s: two extra axioms, `Lean.ofReduceBool` and
`Lean.trustCompiler`. There is no stronger option to hold out for, and a PR
should say so plainly rather than frame it as future work.

### 2.2 The 87-vs-4096 question, settled by measurement

The brief asked whether 4096 tiny CNFs might be cheaper than formalizing the
group action. All 4096 cases were encoded and solved to settle it:

| route | CNF | LRAT | **total embedded** |
|---|---|---|---|
| 87 orbit representatives | 16.41 MiB | 12.65 MiB | **29.06 MiB** |
| all 4096 cases | 772.6 MiB | 547.0 MiB | **1,319.6 MiB** |

The hypothesis fails on both factors: the CNFs are not tiny (197 KiB each,
because the case-independent A2/A3/A3g bulk is 97.7% of every formula) and there
are 47× more of them. 1.3 GiB of `include_str` data is not a build.

The deeper reason to take the orbits, developed in `architecture.md` §5.2: the
**normal form (Theorem 3.5) already forces us to formalise a relabelling action
on weightings and prove `EqSystemN` invariant under it**. The 4096 → 87
reduction reuses that same machinery with different group elements, so its
marginal cost is a 4096-row coverage table plus one chunked `native_decide` —
roughly 300 lines — against a measured saving of 1,290 MiB. There is no version
of this project that avoids the symmetry layer and also avoids the certificate
explosion.

Side benefit: the run is a fresh, independent re-confirmation of Theorem 6.1 on
the **full** 4096-case ledger (4096/4096 UNSAT, CaDiCaL exit 20 every time),
rather than on the 87 representatives.

## 3. The three riskiest steps

**Risk 1 — the product formula, `pmSumList_diagonal` — RETIRED.** Built and
sorry-free in `lean/Product.lean` (`REHEARSAL.md` §3.1); it cost about a
quarter of a session against a 2–4 session estimate, because every arm of the
fuelled recursion reduces definitionally and `List.erase_filter` removed the
budgeted `Nodup` hypothesis. The statement and the reasons it was hard are kept
below for the record.

```lean
theorem pmSumList_diagonal {α : Type} [CommSemiring α] {N D : Nat}
    {W : WeightsN N D α} (hW : IsDiagonal W)
    (ι : V N → Fin D) (L : List (V N)) (hL : L.Nodup) :
    pmSumList W ι L = ∏ c : Fin D, haf W c (L.filter (fun v => ι v = c))
```

Everything downstream rests on it — it *is* equation (2) of the proof document,
"the entire structural content of diagonality". Three specific hazards: (a)
`pmSumListAux`'s fuel parameter is a four-way match with two unreachable arms,
and the induction must be set up so those do not have to be discharged
repeatedly; (b) the step needs `List.filter`/`List.erase` commutation with a
`Nodup` side condition; (c) it is stated over a general `CommSemiring`, so no
`decide` and no `native_decide` can help anywhere.

*Mitigation:* prove it at `N = 6` first (13 orbits, known answer) before
committing at `N = 8`. *Fallback:* mirror algal's `pmSumN_six_explicit` at
`N = 8` — a 105-term explicit expansion by `simp; ring` — and derive each of the
1,638 A2 rows as a concrete polynomial identity. Strictly worse (1,638 `ring`
calls versus one induction) but it is a known-working tactic at 15 terms.

**Risk 2 — `eqSystemNZ_pullWeights`, the equivariance theorem
(architecture.md §5.3).** Estimated 2–3 sessions.

The registry's `EdgeN` carries no `u < v` constraint while `pmSumListAux` only
ever queries labels with `e.u < e.v`, so the relabelling action has to
canonicalise orientation, and the invariance proof has to reindex the
matching sum by an induced permutation of matchings. algal's report is explicit
that this — not the group theory — was the fiddly part of his symmetry layer,
showing up as repeated `by_cases`/`canonicalEdgeKey` splits. We inherit the
hazard exactly.

*Update after the rehearsal (`REHEARSAL.md` §3.2–3.3): the hard half is now
built and sorry-free.* The hazard is real but it is not where this section said
it was: it bites at the **A3 clause family**, which expands a hafnian at every
site and therefore needs `haf` to be permutation-invariant — measured
load-bearing at `N = 8` (head-only A3 leaves 0/87 refuted) and, notably, **not**
at `N = 6` (13/13 survive), so a naive `N = 6` rehearsal would have missed it
entirely. `lean/Symm.lean` supplies `haf_swap`, `haf_move_head`, `haf_expand`
and `haf_eq_zero_of_expand`; roughly 0.5–1 session remains for the WLOG step and
the normal-form transport.

*Mitigation:* copy his design decision to **refuse group theory**. His
`Symmetry6x3` is a proof-carrying record of permutations with no `Group`
instance, no `MulAction`, no orbit–stabiliser, no quotient; `Equiv.Perm` appears
only for `injective`/`symm` and `Fintype.sum_equiv`, and the whole layer is
1,132 hand-written lines. We also get a simplification he did not: because our
Boolean variables are indexed by `(colour, subset)` rather than by edges, the
transport we consume downstream is `haf (pullWeights σ π W) c L = haf W (π c) (L.map σ)`,
so we never need an induced permutation of edge labels as a first-class object.

**Risk 3 — variable-numbering drift between the encoder and the Lean ledger
(architecture.md §6.3).** Estimated 0.5 sessions to *prevent*, unbounded to
recover from if discovered late.

The audit encoder `a9_enc.py` allocates variables lazily and interleaved: the
first gate variable is index 8 while the last base variable is index 5,506. The
ledger design that makes clause soundness tractable (algal's
`LedgerWellFormedFrom`) requires each gate's output to be the next fresh index
with strictly earlier inputs — which our CNFs do not satisfy. The Lean side
would otherwise have to replay the encoder's allocation order exactly, which is
a silent-corruption hazard of the worst kind: a mismatch produces a *different*
theorem, not an error.

*Mitigation, and it must happen before any Lean bridge code is written:*
re-emit the 87 CNFs with canonical base-variables-first numbering
(`p(c,S) → 1 + 128c + rank(S)`, then gates in ledger order) and regenerate the
LRAT. Cost is minutes — the full 4096-case encode-and-solve ran in 464 s.
Doing it afterwards means regenerating every certificate and re-verifying
everything downstream.

*Honourable mention.* The nine clause families are individually easy, but `XF`
is the one that closes the problem (proof doc §6.4: `CASE + FR` leaves 54/87
satisfiable; adding `XF` gives 0/87) and is the only family whose `←` direction
needs a nonvanishing hypothesis, `x^c_{y_c} ≠ 0`, drawn from B2 at the true
point rather than from the abstraction. It deserves the care its ablation row
implies.

*What is **not** a risk:* abstraction soundness in the dangerous direction.
The Boolean encoding is a **relaxation** — we only ever have to show a real
solution *satisfies* the CNF, never that a satisfying assignment comes from a
solution. So "cancellation is free" (proof doc §5.2) needs nothing proved in
Lean at all. This removes what would otherwise be the hardest part of the
project.

## 4. What this upgrades to when Route A/B closes the general case

The registry has **four** open `n = 8, d = 3` variants:
`eqSystem8_no_solution_d3` (ℂ), `_real` (ℝ), `_int` (ℤ), and `_trinary_int`
(weights in `{-1,0,1} ⊆ ℤ`).

**One lemma collapses all four, and it is worth building now.** `pmSumN` is a
polynomial in the weights with integer coefficients and `EqSystemN`'s
right-hand side is `0` or `1`, so a ring homomorphism carries solutions to
solutions:

```lean
theorem eqSystemN_map {α β : Type} [Semiring α] [Semiring β] (f : α →+* β)
    {N D : Nat} {W : WeightsN N D α} (h : EqSystemN N D W) :
    EqSystemN N D (fun e => f (W e))
```

Hence non-existence over ℂ implies non-existence over ℝ and over ℤ (via the
inclusions), and non-existence over ℤ implies it for the trinary restriction
immediately. `IsDiagonal` is preserved too, since `f 0 = 0`. So whichever route
closes the general statement, the other three variants are corollaries rather
than separate projects — provided the closure is stated over a coefficient
domain that admits the maps.

**This already applies to the diagonal result, and changed the statement.**
Remark 1.5 of the proof document says the argument uses only that the
coefficients have no zero divisors and that `1 ≠ 0`, so it holds over any
integral domain — not just any field. Stating the strengthened theorems over
`[CommRing α] [IsDomain α]` rather than `[Field α]` therefore covers **ℂ, ℝ and
ℤ at once**, with ℤ in turn covering the trinary restriction. `statement.lean`
was changed to do this (`eqSystem8_no_solution_d3_diagonal_domain`,
`..._nz_domain`) after checking it elaborates. Cost: zero. The diagonal
addition, once proved, therefore lands the diagonal reading of all four
registry coefficient domains in one theorem.

**What it does not do.** Nothing here bears on the general bicoloured system.
Per proof doc §9.1, the product structure (2) is exactly what diagonality buys
and exactly what a general `A_uv` destroys, and per §9.2 the Boolean
abstraction of §5 is demonstrably *not* strong enough at `N ≥ 10`. The
infrastructure that *would* survive a Route A/B closure is the reusable half:
`haf`, `pullWeights` and its equivariance, the semantic-ledger machinery, the
LRAT harness, and `eqSystemN_map`. The clause families would not.

## 5. Will a PR be accepted? The honest risks

Not a technical question, but it determines whether the work lands.

**In favour.** The diagonal restriction is not an invented variant. `EdgeN`'s
two independent endpoint indices make `WeightsN` the *bicoloured* model; the
original question of [Krenn2017] and the MathOverflow posting [MO2018] is about
graphs whose edges each carry one colour inherited by both endpoints, which is
exactly `IsDiagonal`. The proposed addition is the registry's own model
specialised back to the shape the conjecture was originally posed in, and
[Chandran2022] is where the bicoloured relaxation is studied. That framing
should lead any PR description.

**Against, and worth stating rather than hiding.**

1. *It is a new statement, not the resolution of a listed one.* PR #4610 is a
   status change on an existing entry (8 additions, 3 deletions). Ours adds
   declarations. formal-conjectures does accept variants — "keep closely related
   variants in the same file" — but a reviewer may reasonably ask why this
   variant belongs in a conjecture registry. The [Krenn2017]/[MO2018] framing is
   the answer.
2. *PR #4610 is still open.* It is on the accepted track, not merged. Its
   `native_decide` trust story is the same one we would bring, so a decision
   there sets the precedent for us — **waiting for #4610 to resolve before
   opening ours is the low-risk order of operations.**
3. *Three new declarations plus two new definitions* (`IsDiagonal`,
   `EqSystemNZ`) is more surface than a status PR. A minimal version drops
   `EqSystemNZ` and the `_nz_domain` theorem and keeps `IsDiagonal` plus the ℂ
   and domain statements — smaller, at the cost of not stating what we actually
   prove.
4. *Placeholder URLs.* The `formal_proof using lean4 at "..."` links must point
   at a published, commit-pinned certificate repository. That repository does
   not exist yet, so a PR cannot be opened before the proof is finished — which
   is the right ordering anyway.

**Drive-by finding, reportable separately.** The upstream module docstring
credits [Chandran2022] to "N. Chandran, S. Gajjala" and [Chandran2024] to
"N. Chandran, S. Gajjala, S. Illickan, M. Krenn". The authors are **L. Sunil
Chandran** and **Rishikesh Gajjala** (with Illickan and Krenn). Our own
`references/REFERENCES.md` has it right. Out of scope for an additive PR;
worth an issue.

## 6. What remains before a PR could be drafted

In order.

1. ~~**Re-emit the 87 CNFs with canonical variable numbering**~~ — **DONE**,
   `canonical/n8z0/` and `canonical/n6z0/`, clause sets verified equal to the
   audit encoder's under the variable bijection.
2. ~~**Rehearse the whole pipeline at `N = 6`**~~ — **substantially done**; see
   `REHEARSAL.md`. Note its own finding that `N = 6` alone is **not** a
   sufficient rehearsal: the A3 family is not load-bearing there, so the
   rehearsal must be run with full A3 to exercise the symmetry layer.
3. **Build the mathematical bridge** (architecture.md §3–§6), 13–19
   agent-sessions, product formula first.
4. **Assemble, and gate on `#print axioms`** showing no `sorryAx`, in a
   release script modelled on algal's `verify_release.sh`.
5. **Publish the certificate repository** and pin a commit.
6. **Then** substitute the real URLs into `statement.lean` and draft the PR —
   ideally after PR #4610 resolves.

Steps 1 and 2 are cheap and de-risk everything after them. Nothing in steps 3–6
should start before step 1, because step 1 changes the artifacts everything else
is written against.
