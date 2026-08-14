# Adversarial readout of external spine audit 2

## Verdict

The external report identifies one still load-bearing defect correctly:
the local `B=Eq` response/`Eq` tie is a constructor assumption, not a
source-labelled theorem.  It also correctly prompted the later repairs to
Proposition 5.2 and Theorem B.  Its attack on the literal `db01/dL01`
zero projection is not valid: that result is explicitly a strict typed
direct-sum projection, where zero-extension is definitional and the
cross-grade comparison is declared missing.

The package is not replayable as delivered.  Its only file is `REPORT.md`;
none of the promised transcripts, task files, run logs, roughly forty
mutation scripts, or independent derivations is present.  Exact numbers
which occur only in that missing evidence are not adopted here.

Checker:
[`audit_external_spine2_claims.py`](../computations/audit_external_spine2_claims.py).

## Exact new findings

Two claims were reconstructed independently.

First, aggregate the four operation corners to coordinates

```text
(B0,B1,B2,B3, Eq0,Eq1,Eq2,Eq3).
```

The four tied response rows `(e_i,e_i)` and the four private signless
`K2,2` rows have rank seven, with annihilator

\[
                 \chi=\delta\cdot(B-Eq),\qquad
                 \delta=(1,1,-1,-1).
\]

Replace any one tied response row `(e_i,e_i)` by `(e_i,0)`.  In every one
of the four mutations the rank remains seven, but the old `chi` reads
`+1` or `-1`.  Thus the `126/127` or aggregated `7/8` rank statement does
not determine the advertised dual.  The literal tie is load-bearing.  In
the committed local checker it is inserted directly at
`top_projection_columns()` as identical `B` and `Eq` entries; the later
word census and product-rule tests only propagate that starting choice.

Second, the external report is right that the committed endpoint checker's
`full_coefficient_projector_audit()` records denominators and then asserts
the composite output without applying the two operators.  A fresh direct
application repairs the bounded evidence gap:

```text
h=3: 7560 on every one of 840 occurrences
h=4: 25088 on every one of 9450 occurrences.
```

In both cases `(A_h-lambda_h I)` applied to the actual Gram row first agrees
with the closed matching-flat input used by the endpoint checker, and the
cubic endpoint polynomial then gives the displayed nonzero constant.
There is no arithmetic counterexample at these orders.  Also, as the
matching checker's own docstring says, `Pi_match` is a projector only on
`1+E1`; the new checker confirms it is not idempotent on a general matching
basis vector.  The current frontier sentence “the all-order coefficient
problem is completely solved” is therefore stronger than the committed
end-to-end test, although its intended coefficient identity survives the
first two literal composite checks.

## Claim-by-claim classification at current `HEAD` (`9ad603f`)

| External claim | Classification | Current evidence |
|---|---|---|
| The external package contains replayable transcripts and mutation scripts | **False as delivered** | The directory contains only `REPORT.md`. |
| The word-changing `11:110000 -> 01211222` comparison is missing | **Sound; load-bearing** | The current degree-one census still does not construct any `kappa_i`; it leaves all eight `lambda_i` unevaluated. |
| The physical four-site `B=Eq` tie is unproved | **Sound; load-bearing** | The local checker writes the tie into its four response columns.  The exact rank-preserving mutations above destroy `chi`. |
| `c24b09c` proves conservation only by hardcoded zero vectors | **Factually true, but the alleged circularity is false** | The code uses six and eighteen zero vectors, after separately proving the response and cap live in distinct word/fine/repeated summands.  It explicitly says the projection is zero-extension and the comparison map is absent.  It proves strict projection darkness, not physical cross-grade conservation. |
| The 121/24/24/30/6/18 dark-family entries are zero by definition | **Sound description, false as a defect** | The current gluing note labels off-grade families “zero in the current direct sum” and explicitly refuses to infer darkness after a comparison is added. |
| There are exactly two deciding scalars | **Superseded** | `fb45b07` had two root-labelled scalars at one lower sector.  Current `9ad603f` refines the fixed grade to eight one-root neighbours of `0112`; all eight `lambda_i` remain.  The symmetry audit supplies no sign-negating stabilizer or equality reducing them. |
| An uncovered `A+B` / `A+C` chart-switch family remains | **Superseded as a separate family, still missing physically** | The current grammar includes the four shore edges, the two root sections, and their mixed `K_Eq` interchange type.  Those are precisely the eight unconstructed `kappa` instances after lower-word refinement. |
| A higher multi-parent generator gives a third branch | **Superseded inside the declared grammar; still a scope guard globally** | `9ad603f` declares a free cellular/bar grammar and enumerates its degree-one operation types.  Its checker implements that enumeration as a literal 17-record tuple and explicitly does not prove equivalence with a completed full decorated physical source. |
| The source-grade census is open | **Partly superseded** | It is closed by definition for the declared canonical grammar, but essential surjectivity from the actual full physical presentation into that grammar is still not proved.  Therefore the full-source version remains load-bearing. |
| Proposition 5.2 depends only on Conjecture 6.2 | **Sound at the audited snapshot; repaired** | Current Proposition 5.2 explicitly assumes A2, A3, A4, and A11 and states that they are independent open hypotheses. |
| Theorem B has no adequate checker | **Sound; disclosure repaired** | Current Theorem 3.2 is labelled `[P-prose]` and says its machine verification and independent audit remain outstanding. |
| The `psi_z` probe was silently/selectively adopted | **Partly superseded procedurally** | Current proof prose downgrades the two affected claims to `[G]`; later owned work pins the external `psiz` report and removes the superseded coincidence sentence.  There is still no corresponding entry in `certification/SUPERSESSIONS.md`, and the proof sketch says repository re-audit is pending. |
| The all-order projector composite was never computed | **Sound evidence defect; boundedly repaired here** | The old function only checked denominator arithmetic.  Direct composite checks now pass at `h=3,4`; uniform physical lifting remains open. |
| E14 rank-three, dq-conormal, and packaging ranks were manufactured | **Unsupported by the delivered external package** | No referenced mutation script or derivation is present.  The current artifacts correctly treat those rows as conditional packaging coordinates; no stronger adverse conclusion is adopted without the missing evidence. |
| The first campaign's criticized checkers remained unrepaired | **Not auditable from this package** | The report supplies neither the first campaign's exact defect ledger nor its replay scripts.  Each claimed carry-over needs its own current-HEAD audit. |

## Reproduced positive claims

Current committed checkers rerun cleanly for the following central values:

- `7/8` private/`Eq` quotient and unique `delta.(B-Eq)` under the tied-row
  hypothesis;
- local rank `126/127`, with all 18 direction and 24 tail flags included;
- uniform spectator rank `8k-1` in dimension `8k`;
- the exact Hilbert--Cauchy/Rodrigues moment tower through the committed
  range, including its mutation guards;
- the `Gamma_*` eight-instance ledger for the declared grammar; and
- the new literal projector-composite values `7560` and `25088` above.

These reruns validate arithmetic within the stated models.  They do not
repair the missing physical `B=Eq` construction, build the eight mixed
word/`K_Eq` cells, evaluate their `lambda_i`, or prove that the declared
grammar is the entire full-source presentation.

## Shortest current repair order

1. Construct or refute the physical same-grade `B=Eq` incidence.  The
   rank-preserving mutation proves this cannot be inferred from corank one.
2. Construct one literal mixed word/`K_Eq` mapping cylinder.  Equivariance
   reduces its direction faces to `DQ` and `PS` seeds, but does not determine
   its `B/Eq` value.
3. Evaluate all eight `lambda_i=Psi(d kappa_i)`.  A nonzero value is the
   filler exit; eight zeros give the terminal only inside the declared
   grammar.
4. Prove the comparison from the full decorated physical source category to
   that grammar, or explicitly retain the noncellular-generator scope guard.
5. Add the bounded composite computation to the canonical projector audit
   and weaken the frontier's all-order wording until the uniform composite
   and its physical totalization are both proved.

The external recommendation to retitle or revert `c24b09c` is not on this
list: its current theorem and disclosures are already correctly scoped.

## Reproduction

```text
python3 computations/audit_external_spine2_claims.py
python3 -O computations/audit_external_spine2_claims.py
python3 -I -S computations/audit_external_spine2_claims.py
```

Frozen ledger SHA-256:

```text
ae9bbadee72382167942a17db44741d7f558eb89c3e4f545eee24dee6014e352
```
