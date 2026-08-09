# D1 O4 incidence frontier: exact odd-circuit closure

The exact maximum-support frontier left by the one-site target-incidence
clauses has 159 localized cells and 4,318 nonzero coefficient generators.
It passes the complete 8,100-fibre support shadow, so support combinatorics
alone does not close it.

Three full eight-site output equations (artifact records 3738, 3648, and
2471) are plus binomials.  After reversing the middle orientation, write
them as `g_i=a_i+b_i`.  Their exponent vectors satisfy

```
a1*a2*a3 = b1*b2*b3,
```

and the checker verifies the ordinary polynomial identity

```
g1*a2*a3 - b1*g2*a3 + b1*b2*g3 = 2*a1*a2*a3.
```

All ten variables in the right-hand monomial are localized.  If `U` is the
product of all 159 localized variables, exact monomial division turns this
into a division-free certificate `U^3` in the three-generator ideal.  Thus
the localized ideal is the unit ideal over every field of characteristic
different from two, in particular over the complex numbers relevant to the
conjecture.

The certificate is support-faithful on the whole downward face: it only
assumes that the 34 frozen omitted cells remain absent and that its ten
named monomial witnesses remain present.  The emitted CNF clause is the
disjunction of restoring one omitted cell or deleting one witness.  The
witnesses are not confined to the three mutual target-incidence edge cells,
so this is not by itself a mutual-arc-only theorem.

Reproduce with:

```
python3 computations/verify_n8_d1_residue_orbit4_incidence_frontier_odd_circuit.py
python3 -O computations/verify_n8_d1_residue_orbit4_incidence_frontier_odd_circuit.py
```
