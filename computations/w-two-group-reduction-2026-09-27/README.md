# Two-group W designs: exact reduction and bounds

**Written proof with exact supporting checks; independent audit pending.**
The unrestricted W optimum remains open.

[Proof](../../notes/w-state-two-group-reduction-2026-09-27.md) ·
[Illustrated guide](../../explainers/W-GLOBAL-GUARANTEE.md) ·
[W project](../../research/w-state-design/README.md)

The ground source has two groups, one uniform complex weight within each
group, and one across the groups. All other colored source entries are free.

- At **every even size from six onward**, a two-site group versus the rest
  gives rate strictly below $(5/6)R_*$.
- At **every even size from six through forty**, the exact optimum across
  all two-group ground sources is the known attained rate $R_*$.
  Every split with at least two sites in each group has a strict
  $(80/81)R_*$ upper bound.
- For **arbitrary specified group sizes**, Gegenbauer roots list all
  cancellation branches. Each branch's scalar response minimum can be
  found among the positive roots of a polynomial of degree six.

The finite-range result uses exact certificates for **171 unequal splits
and 615 branches**, plus the earlier all-even equal-split theorem.
The one-site split attains $R_*$. The forty-site endpoint is a finite
verification boundary; no extrapolation to all unequal splits is claimed.
The sextic reduction optimizes the scalar relaxation, not the actual
colored completion problem.

From the repository root, with Python 3.11 or later and the standard library:

~~~sh
python3 computations/w-two-group-reduction-2026-09-27/verify.py > /tmp/w-two-group.json
diff -u computations/w-two-group-reduction-2026-09-27/results.json /tmp/w-two-group.json
python3 -O computations/w-two-group-reduction-2026-09-27/verify.py > /tmp/w-two-group-optimized.json
diff -u /tmp/w-two-group.json /tmp/w-two-group-optimized.json
~~~

The replay independently counts matching and cofactor polynomials through
24 sites, checks the Gegenbauer identity using its recurrence, and verifies
the scalar-cost and sextic formulas. The all-even two-site proof has three
finite polynomial certificates and a positive polynomial establishing its
infinite tail.

For the full finite catalog, rational Sturm sequences isolate every
cancellation root. Interval bounds give a lower polynomial for the scalar
gap. Exact Bernstein subdivision proves that polynomial positive on the
entire positive half-line. These are checks over every source parameter
in each stated branch, not numerical sampling.

[certificates.json](certificates.json) records all rational root intervals
and the dyadic subdivision cells; a cell $[j,d]$ denotes
$[j/2^d,(j+1)/2^d]$ after $t=x/(1+x)$.
The verifier reconstructs and checks the entire catalog. The saved receipt
pins this file, the proof, the programs, and the earlier dependencies.
Every check remains active under optimized Python.

To attempt a larger finite range:

~~~sh
python3 computations/w-two-group-reduction-2026-09-27/two_group.py --max-sites 42 > /tmp/w-two-group-42.json
~~~

This optional command does not change the published certificate or its
scope. It is not needed for replay. Failure to find a positive certificate
is inconclusive; it would not itself demonstrate a better W design.
