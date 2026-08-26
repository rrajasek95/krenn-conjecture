# W4 — Pfaffian linearization + T.1 scouting — REPORT (UNAUDITED, 2026-08-15)

Pinned HEAD 26ba69f. Exact arithmetic (one mod-2^61-1 sweep re-run over
Q on a sample). Scripts/logs/JSON in this directory. Headlines:

1. DECOMPOSITION (A): 4-Pfaffian identity at K6 built and verified 3
   ways (symbolic over Z[w_e]; 100 random exact matrices; per colour
   word on sources). 4 is minimal (no orientation pair suffices); the
   128 clockwise-odd orientations form the predicted H^1(T^2;F_2)
   torsor; Arf signs (+1,-1,+1,+1). Descent = Pfaffian row/column
   deletion (all 15 pairs); the genus 1->0 collapse happens in the
   sum, not termwise.
2. DICTIONARY (B): R-blocks are GRAM matrices of the hyperbolic form
   B_K; every error component is a K4 Pfaffian (Klein quadric);
   span{E_w} = image of mu_pq from four <=3-planes Xi_x;
   kappa_c^2-blocking <=> delta_c^{x4} in image(mu_pq) (apolarity at a
   marked Segre-Veronese point). P2's FACT 1 and FACT 2 are now
   PROOFS (wedge-pair cancellation; the pi_Lambda computation).
   Witness condition classically: E(K)=0 <=> the 4x4 antisymmetric
   Kasteleyn matrix has rank <= 2 for EVERY lambda (a family of lines
   in P^3).
3. PAYOFF (C): the generic kappa_c^2 mode is PROVED vacuous (the
   marked point kills the Lambda^2 obstruction) — W2 confirmed twice
   over. The useful non-generic output: necessary condition (N)
   e_c in P and e_c in Q (column spans); and in R_cell the
   EQUIVALENCE (C): kappa_c^2 blocks <=> some 2+2 split of U has the
   p-cells coloured c on T and the q-cells coloured c on T^c — a
   SUPPORT condition (the J.1c rank->support bridge W2 flagged
   missing; equivalence in the free class 327/327, necessary in the
   tied class). NEW degree-3 law via Cauchy: I_3 misses
   Lambda^3 x Lambda^3 = <det K>; the mixed-determinant law follows
   representation-theoretically, and by Pieri NO such obstruction
   exists in degree >= 4 — explaining P2's degree spectrum and
   proving P1's "degree-3 only" observation.
4. ARF/HANDCUFF (C2): partial identification with an exact
   obstruction. POSITIVE: spin sectors = H_1(T^2;F_2) classes of the
   15 matchings (sizes 4,4,4,3); every two-term O1 fibre equation IS
   a spin-sector Pfaffian-vanishing statement (binomial relations get
   a classical home). NEGATIVE: epsilon does NOT factor through the
   spin grading — two committed certificates contain alpha=0 fibres
   where every character is +1; the grading is colour-blind while the
   oddness is cross-fibre. CONCLUSION: genus-1 Kasteleyn supplies the
   wrong mod-2 group; O1's classical home must be H_1 of the CELL
   graph (Zaslavsky), not the surface.
5. T.1 SCOUTING (D): full-cone singleton coverage impossible on the
   nose (18-dim gauge lineality; T.1 must be stated mod gauge).
   Generic robustness total (200/200 across all random families; all
   32 symmetry cones 800/800). THE FAILURE LOCUS IS EXPLICIT: a
   21-dim linear space = gauge(18) + edge-independent symmetric
   colour forms w[(u,v),i,j] = f(i,j) (6), meeting in 3 — i.e. mod
   gauge the no-singleton locus is essentially the colour-form
   weights, inside the S_6-invariant cone; the pure/Laurent mechanism
   leaves 162 gap points. Verdict: a separate symmetric-cone argument
   is needed and looks feasible (small, highly structured target).
6. Soft spots honestly listed (mod-p degree-3 pass; (C) sampled not
   census-exhausted; 21-dim is a lower bound; C2 trusts committed
   certificate transcriptions; no witness re-decisions).

FEEDS: criterion (C) -> W6 (J.1c bridge); the colour-form residual
cone -> W7 (symmetric-cone closure of T.1; candidate mechanism: the
initial systems at colour-form weights may reduce to the committed
diagonal-pencil insolubility).
