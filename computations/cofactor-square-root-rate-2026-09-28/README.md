# Cofactor square-root certificates and unrestricted rate improvement

**Written proof with exact supporting checks; independent audit pending.**
The unrestricted six-site square-root law remains open.

[Proof](../../notes/cofactor-square-root-rate-2026-09-28.md) ·
[Illustrated guide](../../explainers/COFACTOR-RATE-TEST.md) ·
[GHZ project](../../research/ghz-rates/README.md)

A bound on the polynomial scaling residual also bounds the polynomial's
coefficients. This removes a signal-dependent loss in the earlier
normalization. It gives a local square-root criterion without response-rank
assumptions and improves the unrestricted six-site exponent to 1/14.

The criterion covers every balanced single-color six-site zero.
An exact polynomial certificate proves that a scalar source with a perfect
matching cannot have zero matrix–cofactor product; the balanced case with
no perfect matching is settled by the two-triangle calculation.
The explicit diagnostic can vanish at other colored limits, including
the already settled prism.

Run from the repository root with Python 3.11 or later:

~~~sh
python3 -B computations/cofactor-square-root-rate-2026-09-28/verify.py > /tmp/cofactor-square-root-rate.json
diff -u computations/cofactor-square-root-rate-2026-09-28/results.json /tmp/cofactor-square-root-rate.json
python3 -B -O computations/cofactor-square-root-rate-2026-09-28/verify.py > /tmp/cofactor-square-root-rate-optimized.json
diff -u /tmp/cofactor-square-root-rate.json /tmp/cofactor-square-root-rate-optimized.json
~~~

The standard-library checks use exact rational and Gaussian arithmetic.
They test polynomial coercivity, the fixed normalization radius, the
uncanceled high-degree residual, exact cofactor products and response ranks,
and all four constant budgets. An actual four-site source with tiny
off-color error exercises the improved response and inverse inequalities
in their small-residual regime. Four sites permit exact GHZ; this fixture
does not assert a six-site near-counterexample.

The [scalar certificate](scalar-matching-certificate.json) is a 244-node
rational polynomial derivation of the constant one from the entries of
the normalized matrix–cofactor product. The replay builds its inputs
directly, checks all arithmetic, and rejects a corrupted final multiplier.
This proves a polynomial identity for twelve arbitrary complex variables,
not just a finite collection of examples. The complex site-scaling
identity connects it to every nonzero perfect matching.

The optional discovery script requires SymPy:

~~~sh
python3 generate_scalar_certificate.py
~~~

Run it from this package directory. It instruments the installed SymPy
Buchberger routine to save ideal-membership arithmetic; search details
may change across SymPy versions. Reproducing the published certificate
requires only the standard-library replay above, not regeneration.

General inequalities and all-size claims are proved in the note.
The code imports earlier arithmetic and matching expansions and pins them;
it is an exact supporting replay, not an independent implementation or
independent audit. Old dated packages remain unchanged.
