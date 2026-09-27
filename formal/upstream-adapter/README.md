# Full proof for the exact upstream conjecture

[FullProof.lean](FullProof.lean) proves the complex Krenn–Gu nonexistence
statement for every even `N ≥ 6` and every `D ≥ 3`, using the exact
`MonochromaticQuantumGraph.WeightsN` and `EqSystemN` definitions:

```lean
∀ N D : ℕ, N ≥ 6 → Even N → D ≥ 3 →
  ¬ ∃ W : MonochromaticQuantumGraph.WeightsN N D ℂ,
    MonochromaticQuantumGraph.EqSystemN N D W
```

The main declaration is
`KrennAllOrders.UpstreamFullProof.eqSystem_no_solution_ge6_ge3`.
The file also proves the exact `True ↔ ...` answer wrapper for the upstream
question. Neither theorem has an unproved source-reduction hypothesis.

[UpstreamAdapter.lean](UpstreamAdapter.lean) identifies the local and upstream
edge labels, ordered vertex lists, matching recursion, and monochromatic
predicate. The [all-orders package](../all-orders/README.md) proves the
ternary contradiction. The upstream's proved palette-restriction API then
supplies all palettes of size at least three.

The upstream revision is pinned to
`e2c4441f9545b85790aebcfaa445e194fcab9d5b` in
[the formal-conjectures fork](https://github.com/rrajasek95/formal-conjectures/tree/e2c4441f9545b85790aebcfaa445e194fcab9d5b).
The proof does not use an upstream conjecture with a placeholder proof.

## Real-weight corollaries

[RealCorollaries.lean](RealCorollaries.lean) proves that mapping weights
through a semiring homomorphism preserves every branch of the matching
recursion and the normalized equation system. The map `Complex.ofRealHom`
therefore takes any real solution to a complex solution.

The complex nonexistence theorem yields exact affirmative-answer wrappers
for the five upstream real questions: the general even `N ≥ 6, D ≥ 3`
statement; `N = 6, D = 3`; `N = 6, D ≥ 3`; `N = 8, D = 3`; and
`N = 10, D = 3`. [RealCorollariesAxioms.lean](RealCorollariesAxioms.lean)
audits all ten transfer and corollary declarations.

## Reproduce

With Lean installed through `elan`, first follow the local package's build
instructions, then run:

```sh
git clone https://github.com/rrajasek95/formal-conjectures.git /tmp/krenn-upstream
git -C /tmp/krenn-upstream checkout e2c4441f9545b85790aebcfaa445e194fcab9d5b
cd /tmp/krenn-upstream
lake exe cache get
cd /path/to/krenn-conjecture/formal/upstream-adapter
python3 verify.py --upstream /tmp/krenn-upstream
```

The script checks the exact upstream revision and source state, builds the
local package and upstream target, compiles the adapter, full proof, and real corollaries with
warnings treated as errors, and audits all final declarations. It rejects
axiom dependencies other than `propext`, `Classical.choice`, and `Quot.sound`.
Source hashes and the checked declarations are recorded in
[verification.json](verification.json); [axioms.txt](axioms.txt) contains the
Lean output.
