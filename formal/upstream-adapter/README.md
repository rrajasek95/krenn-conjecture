# Exact upstream adapter

[UpstreamAdapter.lean](UpstreamAdapter.lean) proves that the local
`MatchingModel.EqSystemN` and upstream `MonochromaticQuantumGraph.EqSystemN`
have exactly the same solutions. The proof compares edge labels, ordered
vertex lists, the matching recursion, and the monochromatic predicate.
It does not assume a correspondence or prove nonexistence of solutions.

The upstream revision is pinned to
`e2c4441f9545b85790aebcfaa445e194fcab9d5b` in
[the formal-conjectures fork](https://github.com/rrajasek95/formal-conjectures/tree/e2c4441f9545b85790aebcfaa445e194fcab9d5b).
To reproduce with Lean installed through `elan`:

```sh
git clone https://github.com/rrajasek95/formal-conjectures.git /tmp/krenn-upstream
git -C /tmp/krenn-upstream checkout e2c4441f9545b85790aebcfaa445e194fcab9d5b
cd /tmp/krenn-upstream
lake exe cache get
cd /path/to/krenn-conjecture/formal/upstream-adapter
python3 verify.py --upstream /tmp/krenn-upstream
```

The script verifies the upstream revision and source state, builds the local
package and upstream target, and compiles the adapter with warnings treated
as errors. It rejects axiom dependencies other than `propext`,
`Classical.choice`, and `Quot.sound`, then writes source hashes and the
checked declarations to [verification.json](verification.json).
