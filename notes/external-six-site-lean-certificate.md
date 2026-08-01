# An external machine-checked proof of the six-site obstruction

Reference note.  Krenn's conjecture remains open, `SP-CLEAN-BRIDGE` is
untouched, and no certified dependency changes.  This records external work
that **independently corroborates** `SP-K6`; it supersedes nothing and is not a
supersession candidate.

## 1. What was found

A public repository contains a Lean 4 proof of

\[
 \neg\exists\,W:\ \texttt{MonochromaticQuantumGraph.WeightsN 6 3}\ \mathbb C,\quad
 \texttt{MonochromaticQuantumGraph.EqSystemN 6 3}\ W .
\]

* Repository: `algal/krenn-gu-6x3-certificate`, commit
  `c04696e515e0c02be140353fb52ea60c62e827b1`.
* Theorem: `KrennGuCertificate.eqSystem6_no_solution_d3`.
* Release run recorded 2026-07-24: Lean 4.27.0, 8421 build jobs, 22m18s,
  50 artifact checksums.

It uses the **official** definitions from Google DeepMind's
`formal-conjectures` (`FormalConjectures/Paper/MonochromaticQuantumGraph.lean`),
not a bespoke restatement.

## 2. The statement is exactly Theorem 1.1

Read from the official source:

* `EdgeN N D` is `⟨u, v, i, j⟩` and `WeightsN N D α := EdgeN N D → α`, so a
  weight is attached to each (edge, colour at `u`, colour at `v`) — an arbitrary
  \(3\times3\) complex matrix per edge, \(15\times9=135\) entries for
  \(N=6,\ D=3\).  Nothing is assumed symmetric, nonzero, real or monochromatic.
* `pmSumListAux` pairs the head vertex with each later vertex, weighting by
  `W (mkEdge v u (ι v) (ι u))` and recursing on the rest — the perfect-matching
  sum, read at the colouring `ι`.
* `EqSystemN N D W := ∀ ι, pmSumN N D W ι = if allEqual ι then 1 else 0`, and
  `allEqual` means all \(N\) vertices carry the same colour.

That is \(H_6(A)=\Delta_{6,3}=\sum_ce_c^{\otimes6}\) over arbitrary complex
matrices — hypothesis for hypothesis, the statement of Theorem 1.1 of
[`six-site-arbitrary-complex-obstruction.md`](../proofs/six-site-arbitrary-complex-obstruction.md),
which is `SP-K6` in [`BASELINE.md`](../certification/BASELINE.md).

The definitional comparison above was made by reading the Lean source.  It is a
human reading, not a machine-checked equivalence.

Two independent counts corroborate it.  The external repository describes its
system as **135 coloured edge types** and **729 inherited-colouring equations**;
those are exactly \(15\times9\) and \(3^6\), the counts reconstructed here
from the matching definition for the six-vertex general model.  A third party
working in Lean from the official definitions arrives at the same system.  At
eight vertices the correspondence is checked mechanically rather than read:
[`verify_chart_model_is_official_eqsystem.py`](../computations/verify_chart_model_is_official_eqsystem.py)
transcribes the official recursion and confirms it agrees with this project's
chart decomposition on all \(6561\) coefficients.

## 3. Method, and its trust boundary

A hybrid: Lean rechecks finite data and algebraic identities, over SAT
certificates in LRAT format across eight branches, with an
\(S_6\times S_3\) orbit analysis and a verified LRAT-checker soundness theorem.
Python and CaDiCaL produced candidate data and are stated to be outside the
trusted base.

The axiom closure is `propext`, `Classical.choice`, `Lean.ofReduceBool`,
`Lean.trustCompiler`, `Quot.sound`, with `sorryAx` **absent**.

The caveat worth stating plainly: `Lean.ofReduceBool` and `Lean.trustCompiler`
are the axioms characteristic of `native_decide`, and extend the trusted base
beyond the Lean kernel to the compiler and native runtime.  That is a weaker guarantee than a
kernel-only proof, and stronger than an unchecked hand argument.  Its release
notes also record that publication was still gated at that commit.

## 4. What this changes here, and what it does not

**Changes.**  `SP-K6` now has independent corroboration by a different method —
Lean plus LRAT certificates and orbit analysis, against this repository's hand
lemmas, rank strata and DRUP supplement.  Two independent proofs of the same
statement, by different routes, is materially stronger evidence than either
alone.  Neither proof is audited in this note; what is checked here is that the
statements coincide.  Any note here that describes the six-site obstruction as
externally unverified should be corrected to cite this instead.

**Does not change.**  It settles \((6,3)\).  It says nothing about \((8,3)\),
which is the case this project's descent actually targets, and nothing about the
uniform conjecture.  The spine is unaffected: `SP-K6` was already certified
here, and this is corroboration, not supersession.  No entry in
[`SUPERSESSIONS.md`](../certification/SUPERSESSIONS.md) is warranted, since
nothing is replaced or narrowed.

**Worth noting for planning.**  The release is dated a week before this note
and was not announced.  A search of the published literature would not have
found it, so absence from such a search is not evidence that a case is open.

## 5. The release run was reproduced here

Run on 2026-08-01 against the same commit, following `scripts/verify_release.sh`:

* all **50** committed artifact checksums verify;
* `lake build KrennGuCertificate` completes, **8421** jobs, matching the
  recorded count;
* `lake env lean LeanCheck.lean` reports

  ```
  KrennGuCertificate.eqSystem6_no_solution_d3 : ¬∃ W, EqSystemN 6 3 W
  depends on axioms: [propext, Classical.choice, Lean.ofReduceBool,
                      Lean.trustCompiler, Quot.sound]
  ```

  which is exactly the closure the release script requires, with `sorryAx`
  absent.

So the corroboration of `SP-K6` is now by **execution**, not only by reading the
statement.  The trust boundary of section 3 is unchanged: the closure still
contains the two axioms that carry the Lean compiler and native runtime.

## 6. Still unchecked

The proof itself was not audited — neither the Lean development, the eight
LRAT branches, nor the orbit analysis.  Reproducing a build establishes that
the stated theorem is derived from the stated axioms in that development; it
does not review the mathematics.  What is checked in section 2 is only that the
*statement* proved is the statement of Theorem 1.1, by reading the official
definitions.
