# Independent audit of the sole-defect two-pair obstruction

## 1. Verdict

[The primary two-pair theorem](sole-defect-two-pair-common-power-obstruction.md)
is correct.  The simultaneous coefficient normalization works for every one
of the 105 unordered choices of distinct physical pairs.  A separate orbit
construction gives \(17+31+17=65\) cases, and a clean-room reconstruction of
every unsaturated common-power ideal gives the unit ideal over \(\mathbb Q\).

Consequently the no-ordinary-SDR branch at one deficient site is empty.  In
any surviving sole-defect three-field response configuration, ordinary
distinct active-pair representatives exist, but every such choice is locally
nonseparable at the bad site.

This audit was made against these frozen SHA-256 identities:

~~~text
68ffa028dad871d1121f9ca8ca005f874609c3ad33f2833f1797d8a3068b6e20  notes/sole-defect-two-pair-common-power-obstruction.md
d93a9e182dac1cb369e56377e50712d03bdeee4f15ba5448d065d510e10756b7  computations/verify_sole_defect_two_pair_common_power.py
de6c829bde59674bea4691cff26075e0faea0f92a98da99fc25aed781362e6e5  computations/audit_sole_defect_two_pair_common_power_independent.py
~~~

## 2. Coefficient normalization

For a field active on distinct pairs \(P,Q\), its two coefficients transform
by the good-site characters

\[
 (t_u)_{u\ne o}\longmapsto
 \left(\prod_{u\notin P}t_u,\prod_{u\notin Q}t_u\right).
\]

The independent checker forms the corresponding \(2\times5\) zero-one
exponent matrix and searches all \(2\times2\) minors.  Every one of the 105
pair choices has a determinant-\(\pm1\) good-site minor.  The numbers of
choices having respectively 3, 5, 7, or 8 such minors are 20, 30, 10, and
45.  Hence the character map is surjective on \((\mathbb C^*)^2\) without
root extraction.

Equivalently, choose a good \(x\in P\mathbin\triangle Q\), orient \(P,Q\)
so that \(x\in P\setminus Q\), and choose a good
\(y\notin P\cup Q\).  Scaling the field axis at \(x,y\) supplies the ratio
and common-factor adjustments.  Such \(x,y\) always exist even when one
direction of the symmetric difference is the bad site.  Singleton fields
need only one occupied good site.  Since the three field axes are independent
at every good site, all field normalizations are simultaneous and independent.

## 3. Family and orbit census

On a fixed unordered pair set \(\{P,Q\}\), each nonempty family is
\(\{P\},\{Q\}\), or \(\{P,Q\}\).  Requiring total union
\(\{P,Q\}\) and excluding two equal singleton families leaves exactly
13 labelled systems:

\[
 1\text{ of profile }(2,2,2),\qquad
 6\text{ of }(2,2,1),\qquad
 6\text{ of }(2,1,1).
\]

Across the 105 pair sets this is 1,365 systems.  The independent checker uses
maximal representatives under the good-site \(S_5\) action.  Quotienting by
all field permutations gives 17 circuit and 17 rank-one orbits; quotienting
only by the equal-field swap gives 31 coincident-pair orbits.

## 4. Independent ideals

The
[independent checker](../computations/audit_sole_defect_two_pair_common_power_independent.py)
imports only the companion clean-room algebra builder, never a primary
checker or ledger.  It uses the same alternative deficient-matroid
coordinates, reversed endpoint/cell/equation streams, rightmost-pivot RREF,
sparse monomial dictionaries, reversed variables, and Singular `Dp` order
described in the
[distinct-lift audit](sole-defect-distinct-lift-common-power-obstruction-independent-audit.md).

For every orbit it literally multiplies every \(q\)-coordinate by every
active lift, collects equal degree-six words, solves \(qF=0\), and substitutes
the complete kernel into all coefficients of \(q^{[2]}-F\).  The resulting
affine ideals are unsaturated and retain every coordinate of (q).  Their
rank ranges agree with the primary statement:

\[
\begin{array}{c|c|c}
\text{matroid}&\operatorname{rank}(qF)&\dim\ker(qF)\\ \hline
\text{circuit/coincident}&12,15,18&108,105,102\\
\text{rank one}&6,12,18&99,93,87.
\end{array}
\]

All 65 independent Singular calculations returned the unit ideal.  The
frozen clean-room combined ledger hashes are

| bad-site matroid | independent combined SHA-256 |
|---|---|
| circuit | `7b55e9a776e9cda65ba0921b9deb97bfee6f6c2ec60c7832d2cc0444e01cae39` |
| coincident pair | `4d1670d84f3875602ec140cf6e7b9245f79ed76ec799894a1d6bc5855640bc33` |
| rank one | `b512dc69f4514173f6c77528e2ecf295d626b68be051be6065cadeae98c361e0` |

Run

    uv run python computations/audit_sole_defect_two_pair_common_power_independent.py

for the full replay, or add `--ledger-only` for the exact construction without
the 65 Singular calls.

## 5. Logical scope

For three nonempty active families, Hall failure is witnessed either by two
equal singleton families or by total union of size at most two.  The response
singleton-collision lemma excludes the first.  A one-pair union would again
make equal singleton families, so a no-SDR system has exactly two physical
pairs and one of the three profiles above.  The audited theorem rules all of
them out.

This closes the no-ordinary-SDR branch only at one deficient site.  It does
not eliminate ordinary SDRs with nonseparable bad-site incidence, and it does
not address configurations with two or more deficient sites.
