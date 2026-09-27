# A universal W-design guarantee at every even size

**Written proof with exact supporting checks; independent audit pending.**
The exact unrestricted optimum remains open.

[Proof](../../notes/w-state-universal-factor-two-2026-09-27.md) ·
[Illustrated guide](../../explainers/W-GLOBAL-GUARANTEE.md) ·
[W project](../../research/w-state-design/README.md)

The known construction attains more than half the optimal unrestricted
rate at every even site count. The upper bound is $2B_n/n$, giving
$1/65\le R_{\rm opt}\le1/45$ at six sites.

The new ingredient is a sharp derivative bound at a zero of a homogeneous
complex polynomial. Applied to the scalar hafnian, it controls the total
cofactor strength even when supported ground matchings cancel.
Keeping the higher circle coefficients and cofactor-row imbalance gives
further source-specific bounds.

From the repository root, using Python 3.11 or later and the standard library:

~~~sh
python3 computations/w-universal-factor-two-2026-09-27/verify.py > /tmp/w-universal-factor-two.json
diff -u computations/w-universal-factor-two-2026-09-27/results.json /tmp/w-universal-factor-two.json
python3 -O computations/w-universal-factor-two-2026-09-27/verify.py > /tmp/w-universal-factor-two-optimized.json
diff -u /tmp/w-universal-factor-two.json /tmp/w-universal-factor-two-optimized.json
~~~

The exact replay checks:

- Fourteen ground-source fixtures through twelve sites, including sharp
  complex one-root examples and dense real and nonuniform complex cancellation.
- Euler orthogonality, every coefficient of the derivative-direction
  hafnian polynomial, its first coefficient, and the refined circle bound.
- Exact cofactor efficiency, row-imbalance, and weighted-target formulas.
- The all-even constants, attained construction, and approximation factors
  through eighty sites.
- A counterexample to dropping the zero-hafnian hypothesis.

The proof is universal; the finite fixtures support it and do not replace
the circle argument. The scalar norm inequality is an external mathematical
input from [Roos](https://arxiv.org/html/1906.06176), with its normalization
explained in the proof. The replay does not independently prove that input.
All acceptance checks remain active under optimized Python.
