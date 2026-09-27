# Full-support GHZ jets and a W shear obstruction

**Written proofs with exact supporting checks; independent audit pending.**

[GHZ identities and onset theorem](../../notes/full-support-single-color-jets-2026-09-27.md) ·
[W shear obstruction](../../notes/w-state-shear-normalization-obstruction-2026-09-27.md)

Near a full-support single-color zero-output base, mixed-output identities
force a leading GHZ output to wait until parameter order at least five at
six sites, or at least m+2 at n=2m sites. This is not a fifth-power distance
bound or a proof of the unrestricted square-root law.

An exact W example proves that local output-preserving shears can require
strictly greater source strength to isolate a ground-color site.

Python 3.10+, standard library only, from the repository root:

~~~sh
python3 computations/full-support-jets-2026-09-27/verify.py > /tmp/full-support-jets.json
diff -u computations/full-support-jets-2026-09-27/results.json /tmp/full-support-jets.json
python3 -O computations/full-support-jets-2026-09-27/verify.py > /tmp/full-support-jets-optimized.json
diff -u /tmp/full-support-jets.json /tmp/full-support-jets-optimized.json
~~~

The jet checker verifies 128 polynomial identities per base, with all 540
entries of four source jets formally available, on two complex bases.
The shear checker verifies exact output preservation and a Hermitian norm
certificate for all complex shear parameters. Missing-denominator and
incorrect-Euler-factor negative controls are included.
