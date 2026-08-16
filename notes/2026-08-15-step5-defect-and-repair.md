# Correction: the Step-5 paragraph of the odd-near-perfect gadget proof (2026-08-15)

**Affected file (byte-frozen canonical, not edited):**
`proofs/odd-near-perfect-gadget-obstruction.md`, lines 56-58.

**Defect (found by hygiene audit H1,
`computations/unaudited-hygiene-h1-2026-08-15/`).** The paragraph
"Restricting to either parity class repeats the argument and forces
the endpoints to be congruent modulo every power of two" is a
non-sequitur: restricting to one parity class discards the
interleaved partner class, so the crossing hypothesis does not
survive and the argument cannot be repeated. Explicit checkable
counterexamples to the claimed descent step (matchings satisfying
the level-1 conclusion and violating the level-2 conclusion) are in
`h1_b1_step5_stepcheck.py`: at N = 8 the matching {(0,4),(2,6)} is
congruent mod 4 and violates mod 8; at N = 16 eight of the nine
mod-4 matchings violate mod 8; at N = 24 all 225 do.

**The theorem is TRUE and independently proved twice in committed
material; the conclusion of every downstream use is unaffected:**
1. `notes/finite-obstruction.md` §7 restricts to each pair of
   ADJACENT residue classes (one even, one odd), which preserves
   the interleaving and genuinely descends — H1 verified the
   restricted alternation and sub-class closure at N = 8, 12, 16,
   20.
2. `notes/termwise-rank3-cubic-uniqueness.md` §3.5 (B3) proves the
   same statement by a minimal-arc argument with no descent at all
   (H1 re-derived the same argument independently before locating
   it).
Additionally H1 supplies a one-line third proof (contract the M_0
edges; the quotient's edges all join same-parity indices of
Z_{N/2}, so the union is disconnected, contradicting Step 1's
failure) and an exhaustive verification of the residual-case
emptiness to twice the original range (N = 8, 12, 16, 20:
9 / 225 / 11,025 / 893,025 parity-preserving configurations, zero
survivors, matching the §3.6 census row exactly).

**Disposition.** The canonical file stays byte-frozen (pin-target
discipline). Readers and future auditors must take Step 5 from
source 1 or 2 above. Recorded as SUPERSESSION-2026-08-15-01 in
`certification/SUPERSESSIONS.md`; permanent audit record at
`certification/audits/SUPERSESSION-2026-08-15-01.md`.
