# A balanced competing minimum in the six-site W problem

**Written proof with exact supporting checks; independent audit pending.**
The unrestricted global W optimum remains open.

[Proof](../../notes/w-state-balanced-three-plus-three-2026-09-27.md) ·
[Illustrated guide](../../explainers/W-GLOBAL-GUARANTEE.md) ·
[W project](../../research/w-state-design/README.md)

Split six sites into two triples. Give each triple one uniform complex
ground weight, and all cross edges a third weight. When the ground
hafnian vanishes, the scalar response cost is at least $117/2$.
This is exactly $81/80$ times the one-root value $520/9$.
Every colored exact-W completion therefore has rate strictly less than
$16/1053=(80/81)(1/65)$.

At the balanced representative, within-triple weights are
$+\sqrt{2/3}$ and $-\sqrt{2/3}$ and cross weights are one.
It is also a strict local minimum of the scalar objective on the
full complex zero-hafnian manifold, allowing arbitrary perturbations.
The constrained quadratic form has 21 positive directions and only
the seven null directions from scaling and site phases.
This excludes a neighborhood of another complete-support cancellation
family, and shows why a local optimizer of the scalar relaxation
need not converge to the known one-root family.

From the repository root, with Python 3.11 or later and the standard library:

~~~sh
python3 computations/w-balanced-cancellation-2026-09-27/verify.py > /tmp/w-balanced-cancellation.json
diff -u computations/w-balanced-cancellation-2026-09-27/results.json /tmp/w-balanced-cancellation.json
python3 -O computations/w-balanced-cancellation-2026-09-27/verify.py > /tmp/w-balanced-cancellation-optimized.json
diff -u /tmp/w-balanced-cancellation.json /tmp/w-balanced-cancellation-optimized.json
~~~

The replay uses exact arithmetic in $\mathbb Q(\sqrt6)$ and checks:

- Every coefficient of the three-parameter ground hafnian and all
  fifteen cofactors, plus complete and disconnected family examples.
- The sharp scalar value, its ratio to the one-root cost, and the
  resulting strict rate threshold.
- All 210 evaluations needed to determine the real and imaginary
  quadratic forms on full 14-dimensional tangent bases.
  Direct corrected-path series, the matrix formula, and the symmetry
  decomposition agree coefficient by coefficient.
- The ranks 13 and 8 of the two forms, positive two-by-two blocks,
  and the one scaling and six independent phase null directions.
- The exact derivative-circle polynomial and its nonzero
  two-excitation coefficient in the minimum-row completion.
- All 64 output words for an explicit exact W completion of the
  same ground source, proving that the family is nonvacuous.

All checks remain active under optimized Python. The general family
inequality and passage from positive curvature to a neighborhood bound
use the written proof and its pinned dependencies. No numerical search
or floating-point eigenvalue calculation is part of this replay.
The scalar minimum is not claimed to be a local optimum of the exact
colored W design problem, and the rate threshold is not claimed attained.
