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

## Tooling hazards
5. **pysat + cadical `get_proof()` silently truncates DRUP files**
   (mid-clause; most truncated proofs still replay, so passing
   certificates do not vindicate the method). Write solver-native
   proof files and REPLAY every stored proof. Details:
   `notes/2026-08-15-pysat-cadical-proof-truncation-hazard.md`.
6. **Singular 4.4**: `e1`, `mult`, `I` are reserved identifiers; a
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
