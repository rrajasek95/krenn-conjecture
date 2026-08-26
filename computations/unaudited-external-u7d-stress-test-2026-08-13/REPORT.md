# UNAUDITED EXTERNAL STRESS TEST — U7D witness vs our obstruction machinery (2026-08-13)

**External repo YesterdaysLemon/krenn-gu-research pinned at commit
f17afa1c8e72aeba51dafdf1e38afeb903591750; file sha256 table in run-log.
Exact rational arithmetic except one labelled 80-digit exhibit, backed by
an exact existence proof. Our code imports nothing of theirs (witness
hand-transcribed, everything recomputed). UNAUDITED one-pass cross-check.**

## Verdicts

1. **Their witness is VALID on every claimed property (22/22 checks).**
   Eight vertices, complete r=1 support (28 matrix-unit cells, amplitudes
   ±1), three pure coefficients = 1 each via a unique diagonal matching,
   an odd three-fibre binomial cycle with gauge-invariant holonomy H = −1,
   strict positive integral endpoint balance (all 24 loads = 7), and a
   moment-balanced representative over C — which is in fact REAL, and for
   which this probe supplies an exact existence proof (convex F(x) with
   their balance certificate giving coercivity: sum_e p_e A_e = 7·1),
   replacing their unaudited convexity import. Two nits: their
   "nonrigidity" definition exists only in code; moment existence was
   deferred to an import (now closed independently).
2. **Same invariant.** Their diagonal gauge is the codimension-3 GHZ
   subtorus of our vertex-colour torus (their lattice rank 10 = our L_S
   rank 7 + the three pure indicators). But their z passes the STRONGER
   test: z ∈ ker(unsigned incidence) exactly. Their H is precisely our
   exponent-local-system holonomy of the flip loop restricted to their
   support. Zaslavsky shape: the carrier is a single even 12-cycle —
   NOT an odd handcuff (handcuffs exist on the support; the binomial
   relations never reach one), matching the programme note's claim that
   handcuffs carry every 1=−1 certificate.
3. **No bug in our machinery.** On the subsystem they satisfy (3 pure
   nonzero + 3 cycle fibres zero): O2 does not fire; the three binomial
   rows are linearly independent (relation lattice rank 0) so O1 does not
   fire — LIVE, correctly. Their H=−1 is a VALUE lambda^z=−1, not a
   collision 1=−1. On the FULL Krenn–Gu target restricted to their
   support: DEAD by O2 (94 one-term mixed fibres), which their own U7D
   exclusion theorem independently confirms (their Laurent unit
   certificate on omega=00011011 IS an O2 singleton kill; they found 10
   inside (4,4,0), the full count is 94). No conflict anywhere.
4. **Boundary sharpening for O1 (the valuable import).** U7D is a
   strictly stronger companion to our own
   notes/binomial-incidence-odd-dependence-countermodel.md: it meets that
   note's corrected hypothesis (all three constant fibre sums nonzero)
   AND adds complete support, strict balance, an actual moment normal
   form — while still carrying an odd 3-fibre cycle with H=−1 and NO odd
   exponent dependency. Consequence, FALSE with U7D as counterexample:
   "an odd-length binomial active cycle with invariant holonomy −1, on a
   complete support with all three pure coefficients nonzero, is a 1=−1
   certificate." Our O1 as written (trivial exponent dependency +
   epsilon=−1) is untouched; the trivial-dependency clause cannot be
   dropped or weakened to odd cycle length. Our note's strengthened
   statement (all mixed coefficients vanish) is NOT refuted — U7D has
   c_eta = 1 ≠ 0; that case remains open.
5. **Convergence worth exploiting:** their open "complete
   same-multidegree unit-or-syzygy lemma" is our Problem 1 (O1/O2
   propagation) restricted to a multidegree block; their 57/10/3 census
   is a one-support instance of the O2 side. Progress transfers in both
   directions.

## Controls

20/20 mutation controls behaved, including: O1 fires on a planted odd
3-row relation and when the odd cycle genuinely closes (replace r_2 by
−(r_0+r_1)), stays silent when a fourth fibre closes it evenly; O2 fires
on the full target only; nine killed witness mutations (flipped signs,
relabelled cells, broken balance, corrupted census) all detected.
