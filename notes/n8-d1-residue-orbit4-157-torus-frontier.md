# First torus-consistent O4 frontier

After promoting the first 157-cell holonomy repair chart, the exact O4
support CEGAR still has a 157-cell maximum.  The new canonical support passes
all 8,100 support fibres and has 4,321 exact coefficient generators under
SHA-256
`00839fab040697522574a57f3529eb2968247eaa0b2ab49d2eadaf4795cf17d4`.

This is the sharp stopping case for the Laurent character oracle.  The 72
initial plus binomials have exponent rank 25 and 47 consistent dependencies.
Reducing every generator adds 19 distinct two-class equations.  The full
91-row system has exponent rank 36 and 55 integral dependencies, all with
the correct character.  There is no one-class equation.  Thus neither a
Laurent monomial nor any signed/SNF holonomy closes this face.

All 36 lattice pivots are units.  The checker triangularly solves them and
freezes an explicit Laurent parametrization in 121 independent nonzero
parameters.  It substitutes that parametrization back into every character
equation, so the torus-consistency claim is constructive and includes the
nonprimitive-lattice guard rather than relying on a numerical solver.

Higher-class equations remain.  The first selected three-class residual is
record 343; after the torus parametrization it is an exact Laurent trinomial
with coefficient pattern `+,-,+`.  The next legitimate attack is therefore
resultant/ideal reduction on these residual trinomials and larger fibres.
This artifact is not a coefficient point and does not claim that the full
4,321-generator ideal is nonempty.

Reproduce with:

```bash
python3 computations/verify_n8_d1_residue_orbit4_157_torus_frontier.py
python3 -O computations/verify_n8_d1_residue_orbit4_157_torus_frontier.py
```

Frozen ledger SHA-256:
`55572b97ff5a8bb421d81a9c8e32e1a29f2308e19602ea217ff48d56ccf77360`.
