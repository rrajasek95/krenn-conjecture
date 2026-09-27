# W-rate bounds for cancelling ground cores

**Written proof with exact supporting checks; independent audit pending.**

[All-even theorem](../../notes/w-state-coherent-odd-core-2026-09-27.md) ·
[Six-site octahedral gap](../../notes/w-state-octahedral-ground-gap-2026-09-27.md) ·
[W research project](../../research/w-state-design/README.md)

At every even count at least six, arbitrary complex ground couplings from
the remaining site cannot improve the known W rate when the odd ground core
has a common nonzero edge weight. This permits arbitrary other colored
entries. Nonzero root ground strength gives an explicit strict rate loss.
The ground support may be complete and cancel its perfect matchings.

This is not a proof for nonuniform ground cores or unrestricted W designs.

A second theorem covers the six-site octahedral ground family with arbitrary
complex cycle and root weights. It gives the strict bound $R<2/135<1/65$,
including for every colored completion. An exact example in this family
also refutes a proposed degree-weighted polynomial shortcut to the open
harmonic inequality.

From the repository root, with Python 3.11 or later and the standard library:

~~~sh
python3 computations/w-ground-cancellation-2026-09-27/verify.py > /tmp/coherent-w-core.json
diff -u computations/w-ground-cancellation-2026-09-27/results.json /tmp/coherent-w-core.json
python3 -O computations/w-ground-cancellation-2026-09-27/verify.py > /tmp/coherent-w-core-optimized.json
diff -u /tmp/coherent-w-core.json /tmp/coherent-w-core-optimized.json
~~~

The checker enumerates matchings by a cached subset recurrence over
$\mathbb Q(\omega)$, independently of the closed formulas. It verifies:

- Ground output, every cofactor, and every response-row norm on two complex
  fixtures at each of 4, 6, 8, 10, and 12 sites.
- The response lower bound and the all-even rate formula, with exact
  positive derivative coefficients through 80 sites.
- The one-root W output, its complete-ground-support cancellation completion,
  and the equality rate.
- A four-site cancellation source where the response relaxation gives
  $1/8$ and leaves unwanted outputs.
- Rejection of a violated zero-sum condition and a wrong cofactor sign.
- The octahedral cofactor and response formulas, both Bernstein positivity
  certificates, and the exact polynomial-shortcut counterexample.

The finite checks do not replace the written proof for every even count.
All acceptance checks use explicit exceptions and remain active under
Python optimization. Dependencies and proof/code hashes are recorded in
the JSON files beside this README.
