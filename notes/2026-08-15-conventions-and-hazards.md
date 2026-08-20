# Conventions and hazards ledger (2026-08-15)

Collected from the day's probe fleet and prior-art sweeps so future
lanes and outside readers do not trip. Update in place.

## Terminology collisions (qualify in every new note)
1. **"clean"** has three distinct meanings in the corpus:
   - *slice-clean* (W5/P1/W13/W14): the colour-c pair slice error
     E_pq(E_cc) vanishes — the operative predicate for witness
     theory; closed forms in
     `computations/unaudited-slice-dirtiness-w5-2026-08-15/slice_core.py`.
   - *word-clean* (W15): no single-cell block is active on the word.
   - *cut-clean* (W12): no supported matching uses a crossing edge
     of a given bipartition.
2. **"witness"** has two meanings:
   - current fleet: an active clean cap (p, q, K) with
     s kappa_0 kappa_1 kappa_2 != 0 and E_pq(K) = 0 (the descent
     input);
   - older N=8 notes (e.g. n8-minimal-witness-union-obstruction):
     a site u with C_{u,r} = 0. Unrelated.
3. **Two h conventions differ by one**: the old curvature-line spine
   uses N = 2h; the 2026-08-15 witness campaign uses h = N/2 - 1.
4. **"O1" collision**: `notes/route-registry.md` O1 is a legacy
   route identifier, NOT the odd-holonomy kill mechanism.
5. **"witness" has a FOURTH sense as of the N=8 diagonal theorem.**
   Item 2 lists three; `proofs/eight-site-diagonal-obstruction.md`
   adds a fourth, unrelated one:
   - *B2 witness site* (W29/A9, 2026-08-19/20): one of the three
     sites `y_0, y_1, y_2` produced by Lemma 3.4 (W29-B2) when a
     block-diagonal source is put in the free-set-triple normal form.
     `y_c` is a site of the solved-out star at which BOTH
     `x^c_{y_c} = t^c_{z y_c} != 0` and `h_c(y_c) = haf(t^c|V'-y_c) != 0`;
     the three are forced distinct. Nothing to do with cap witnesses,
     SAT template witnesses, or the legacy `C_{u,r} = 0` sites.
   The proof document writes "B2 witness site" at every occurrence and
   never plain "witness"; new notes should do the same. If a fifth
   sense ever appears, the right move is a rename, not a fifth entry.
6. **"X_k", "off-count", "level", and "diagonal" in the N=8 campaign**
   (W28/W29/A8/A9; promoted with
   `proofs/eight-site-diagonal-obstruction.md`):
   - *off-count* of a word `w` on `N` sites is
     `off(w) = N - max_c |w^{-1}(c)|`, the number of sites outside the
     largest colour class. `off(w) = 0` exactly for constant words.
   - *`X_k`* (the *level-k system*) imposes the three constant-word
     conditions plus vanishing of ONLY those mixed words with
     `off(w) <= k`. So `X_0` is contained in `X_1` is contained in ...,
     and larger `k` is a STRONGER system. `X_k`-feasible means "has a
     solution at level k".
     **NOTATION COLLISION, pre-existing**: `X_k` / `X_4` / `X_i` are
     ALSO used across the committed corpus as ordinary indeterminates
     and series symbols in TeX — e.g. `\frac18X_4` in
     `notes/collision-cofactor-bianchi.md` (21)-(22),
     `\lambda_kX_i+\lambda_iX_k` in
     `notes/invertible-monomial-nine-cap-classification.md` (12),
     `X_k^D` in `notes/full-missing-square-cap-carrier-resonance.md`
     (15), and `X_23`/`X_45` as named quantities in
     `notes/h3-direct-free-feature-selector-index-gate.md`. 33 tracked
     files under `notes/` and `proofs/` match `X_4` or `X_k` at the
     pinned HEAD; the ONLY one using the level sense is
     `notes/2026-08-15-resolution-master-plan.md` (addenda v40 onward).
     Everywhere else the symbol is an indeterminate. So the level
     reading is safe only inside the N=8 support/diagonal campaign;
     anywhere else, write "the level-k system X_k" in full on first
     use, or avoid the symbol.
   - The level at which `X_k` becomes full exactness DEPENDS ON `N`
     and is not `4`: for block-diagonal sources it is `2` at `N = 4`,
     `4` at `N = 6` and `N = 8`, **`6` at `N = 10`**, `8` at `N = 12`.
     Reading `X_4` as "exactness" is correct only at `N <= 8`; this
     exact slip is what produced, and then refuted, the "uniform in
     even N" claim of W29 (master-plan v47, withdrawn in v50).
   - *diagonal* in this campaign means **block-diagonal**:
     `A_uv = diag(t^0_uv, t^1_uv, t^2_uv)`, i.e. three independent
     symmetric edge-weight functions, one per colour. It is STRICTLY
     WEAKER than the general bicoloured model (arbitrary `3 x 3`
     `A_uv`) and STRICTLY STRONGER than the single-cell edge-coloured
     model (at most one colour supported per pair). Do not collide it
     with the *diagonal gauge group* of `draft_gauge_lemma.md` (one
     nonzero scalar per site-colour pair), which is unrelated.

## Tooling hazards
5. **pysat + cadical `get_proof()` silently truncates DRUP files**
   (mid-clause; most truncated proofs still replay, so passing
   certificates do not vindicate the method). Write solver-native
   proof files and REPLAY every stored proof. Details:
   `notes/2026-08-15-pysat-cadical-proof-truncation-hazard.md`.
6. **Singular 4.4**: reserved-identifier collisions error with
   RETURN CODE 0 (parse stdout for `?`). Build-calibrated on
   4.4.1p05 by H1: only `mult` of the originally listed names is
   actually reserved there (`e1` and `I` are usable); treat the
   reserved set as build-specific and probe it per environment. A
   leading unary `+` is a parse error.

## Record corrections adopted this cycle (see master-plan addenda)
7. "Blocking degrees 2..5" is not reproducible from stored data
   (every P2 runner used max_degree=4); treat degree-5 blocking as
   unestablished until a certificate is produced (v22).
8. W6's Sigma_min tables and W6 Result 1/Result 3 are superseded
   (v11); the admissible zero-singleton threshold is 16 (v15).
9. The phase-only reduction (v5) is withdrawn (v12); balance
   survives audit.
10. The fourth-matching theorem (A3.4) is Bogdanov restricted to
    properly 3-edge-coloured cubic graphs — cite Bogdanov and
    Chandran–Gajjala ("crossing pairs", "drums"); no novelty claim
    (v21).
11. **Singular traps (audit A4, D6)**: Singular reports many errors
    on stdout with RETURN CODE 0 — parse output for `?` lines; and
    `ideal S = sat(I,J)[1];` coerces the list and takes the first
    GENERATOR of the saturation — use
    `list L = sat(I,J); ideal S = L[1];`.
12. **Audit-method lesson (A5)**: "NEVER"-type claims must be tested
    by exhaustive sweeps over small structured strata (0/1 matrices;
    {-1,0,1} up to the symmetry of the question), not only random
    batteries — random draws systematically miss measure-zero
    failure regimes (T2's 17% of the 0/1 stratum was invisible to
    hundreds of random draws).
13. **SEVERE — Singular identifier shadowing manufactures FALSE
    KILLS (W16 §7)**: `poly g11 = ...;` in a ring that has a
    variable named `g11` silently REBINDS the identifier — no
    warning, no `?` line, return code 0; the stdout-`?` guard does
    NOT catch it. In W16 it turned a feasible Branch-B system into
    a reported unit ideal (a false kill), detected only by an
    explicit exact point contradicting the verdict. REQUIRED
    PRACTICE, every lane: (a) never name generators after ring
    variables — use a reserved prefix (`zzg*`) and run a
    no-shadowing guard over every emitted script (see
    computations/unaudited-residual2-w16-2026-08-15/w16_sing.py);
    (b) add the EXPLICIT-POINT CONTROL to the standard set: for
    every infeasibility verdict, construct one explicit rational
    point of a known-feasible relaxation and test the verdict
    against it — it is the only control that caught this.
14. Singular build calibration (W16): on this build `sat(I,J)`
    returns an ideal (the A4/A6 `[1]` trap does not fire here, but
    keep the `list` form for portability); `LIB "elim.lib";` is
    required or `sat` is undefined — which the `?`-guard does catch.
15. Minimality statements for ideal-membership certificates must be
    QUANTIFIED RELATIVE TO THE MULTIPLIER/normal form: W15's
    "leave-one-out 6/6" (its multiplier), A6's five-mixed-word
    certificate (different multiplier), and W16's degree-6 minimal
    multiplier are all consistent — each is minimal in its own
    frame. State the frame.
16. **Proof-system mismatch (W18)**: a solver-native proof file is
    necessary but not sufficient — the checker's proof system must
    match the solver's. RUP-only checkers (rup18, W11's rupcheck)
    reject legitimate DRAT proofs containing RAT steps from
    lingeling inprocessing. Pair lingeling with a DRAT-capable
    checker, disable inprocessing, or re-emit via a solver whose
    output the available checker fully covers. One 1.06M-lemma
    proof (class 7847550) is in this state — treat the class as
    unverified until re-proved.
17. **Vacuous-by-specialisation tests (W20)**: deciding "does the
    mixed system force the pure coefficient to vanish?" by
    specialising the other blocks to random rationals is VACUOUS —
    at any non-solution point the mixed matrix has full column
    rank, so the pure row is trivially in its row space and the
    test reports a kill for EVERY template (verified: proved-dead
    m=24 shows 24/24 false "kills"). Such tests have content only
    at points of the solution variety: do the elimination (maximal
    minors) or evaluate at constructed exact solution points, never
    at random specialisations.
18. **Explicit-point controls for FORCING verdicts must live OUTSIDE
    the asserted locus (A7)**: a control point at which the forced
    conclusion already holds (e.g. all sites factoring) can never
    falsify the forcing claim — it only shows the ideal is not
    unit. Construct the control at a point where the target does
    NOT vanish; if no such point can be constructed, say so — that
    absence is itself unverified territory. Companion rule: "an
    exact search never reaches X" is NOT evidence that X is
    unreachable (demonstrated at m=25: the descent never reaches
    zero factoring sites while an exact zero-factoring point
    exists). Search minima may guide effort, never support claims.
19. **Characteristic caveats for exhaustive sweeps (W21; refines
    item 12)**: a complete single-small-field classification can
    produce FALSE KILLS of statements over Q — an exhaustive F_5
    sweep "proved" a permanent-vanishing impossibility whose Q
    counterexamples need a primitive cube root of unity (absent in
    F_5); it passed mutation and positive controls in two
    independent pipelines. Characteristic 3 is degenerate for 4x4
    permanents (4! = 0 there). For NEVER claims over Q, use at
    least two primes with the relevant residues (p = 1 mod 3 for
    cube roots, p = 1 mod 4 for i), or eliminate over Q directly.
20. **The adversarial-builder control (W21)**: for any new
    NEVER/impossibility lemma, spawn an independent lane whose sole
    task is to BUILD the forbidden object (over extensions of Q,
    not just samples). Cross-lane contradiction caught a false kill
    that every within-lane control missed.
21. **Control files must fail loudly if a control never runs
    (W18)**: a `__main__` block placed above a control function's
    definition silently skipped that control (EPC2b) while the file
    exited 0. Require every control script to end by asserting a
    manifest of executed control names against its declared list;
    check other lanes' control files for the same ordering pattern.
22. **Rational coefficients into Singular (W23)**: sympy's default
    printing emits `k^2/9`-style rationals that Singular's parser
    rejects with RETURN CODE 0 (`? poly ^ number failed`) — only
    the stdout-`?` guard stands between this and a silent wrong
    answer. Clear denominators before emission; for cap-error
    systems this is sound because every term of E_pq has the same
    total degree 2h in the blocks (global rescaling changes no
    verdict).
23. **Three-way proof-check outcomes (W18; refines items 5/16/21)**:
    a checker result must be `verified` / `unchecked` / `refuted`,
    never Boolean. Two real incidents: a drat-trim TIMEOUT and a
    forward-RUP checker's failure on a (possibly-RAT) cadical DRAT
    proof were both treated as refutations — false escalation; the
    RUP-only checker can only ever CONFIRM a DRAT proof, never
    refute one (it cannot decide RAT lemmas). Refutation authority
    belongs only to a checker whose proof system COVERS the
    emitter's (drat-trim or a full-DRAT checker for DRAT; rup18
    only for DRUP emitters). Timeouts and out-of-system failures
    are `unchecked` and go to a re-check queue that must be drained
    before any completeness claim.
24. **An F_p counterexample kills a characteristic-free route, not
    a C-statement (A10; mirror of item 19)**: constructing a
    co-failure/escape point over F_p refutes any IDEAL-THEORETIC
    (all-characteristic) proof strategy for the statement, but the
    statement over Q/C may still be true. State the characteristic
    of every refutation object in headlines, not just soft-spots
    ((L2,R5) at m=28: refuted over F_31; F_13 refutes (R5,R6);
    over Q/C both remain open).
25. **Sampled disjunctive predicates are one-sided (A10, from
    W26/W30)**: sampling index choices of DELIVERS (a disjunction)
    can only miss deliveries, so sampled failure tables are UPPER
    BOUNDS on failure; any "never co-occur" claim read off one
    must be re-derived exhaustively. Compute and report effective
    coverage (W26's was ~9-21 admissible choices of 243-823 per
    vertex, not its nominal 40-60 draws). Three stored W26
    verdicts were spurious for exactly this reason.
26. **Progress tallies must reconcile two independent views (from
    the manager's own m19 miscount)**: counting records in
    checkpoint files is NOT counting verdicts — worker jsonl
    streams contain progress/attempt rows, and a naive
    index-keyed count over them reported 310/310 when the true
    state was 267/310 with 43 classes bearing NO verdict. The
    only valid tally reconciles closing rows against certificate
    files (two independent views that must agree, as W18's does).
    Applies to every lane's "N/M complete" claim — and to the
    manager.
27. **Pre-launch controls must test the exact target, not a
    relaxation (W30 round 8)**: testing a NECESSARY consequence
    of the target against stored objects can pass/fail
    spuriously — W30's (CELL)-only control reported a false alarm
    because (CELL) is satisfied identically on rank-one strata
    while the true target (the full Q = 0 system) never is. State
    the target verbatim, then control against that.
28. **Over-strong pre-filters make exhaustive sweeps vacuously
    strong (W31's ff5/ff7 trace)**: a filter justified by an
    OVER-STRONG "necessary condition" (here: demanding
    colspace(A) ⊆ Ann(V_0) where the true condition constrains A
    only on V_1) silently rejects every candidate — the sweep
    then reports zero survivors over its whole domain and reads
    as a completed classification while checking NOTHING
    (`filtered: 0, full_checks: 0` was the tell). Every
    exhaustive-sweep pre-filter must ship with a witness that
    PASSES it (a known-good object reaching the full check), or
    the sweep's zero is meaningless.
    **Correction to item 19**: the W21 false kill's stated cause
    ("F_5 lacks cube roots of unity") is WRONG — the stored
    counterexample has integer entries and its permanent vanishes
    over Q, F_5, F_7, F_13, F_31 alike; the sweep missed it
    because of exactly this item's unsound pre-filter. Item 19's
    multi-characteristic PRACTICE stands (cheap, catches other
    failure modes); its diagnosis of that incident does not.
