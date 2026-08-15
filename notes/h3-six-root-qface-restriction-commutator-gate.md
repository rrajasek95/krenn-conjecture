# Six-root restriction at the two physical cap edges

## Result

The six-root word section has a canonical restriction to both cap edges,
but the correct restriction operator is the multiplicity-adapted divided
Hasse action, not the same six ordinary roots on every face.

Let

```text
response word  11110000
cap word       01211222
```

and let (R) be the product of the roots at sites
`0,2,4,5,6,7`.  On squarefree perfect matchings, direct calculation gives

\[
 D_eR_S=R_{S\setminus(e\cap S)}D_e.                  \tag{1}
\]

If one wrongly keeps a root at an endpoint removed by (D_e), it acts on
no coefficient factor and annihilates the cofactor.  The resulting naive
commutator has direct-free ranks

```text
q23:21   15
q45:12   12.
```

After omitting those endpoint roots, both commutators have rank zero.  The
checker verifies (1) on all 105 perfect matchings and all 90 direct-free
parents.  The surviving six-site words are respectively

```text
110000 -> 011222,
111100 -> 012122,
```

and both restrictions remain target-safe.

## The repeated branch forces divided order

The relevant collision monomials are not squarefree in their site
incidence.  For the selected branch

```text
parent  01|23|45|67
branch  07|23|45|67
missing site 1, doubled site 7,
```

ordinary order-one roots give two partially recoloured terms because site
7 occurs twice.  They do not contain the fully recoloured cap branch.
Instead use

\[
 \mathcal R_F=
 \prod_{i\in\{0,2,4,5,6,7\}}
 E_i^{[m_i(F)]},                                     \tag{2}
\]

where (m_i(F)in\{0,1,2}) is the incidence multiplicity of site (i)
in the retained face (F).  This is source-valid in the filtered setting:
it is the coefficient of the literal endpoint Hasse/substitution coaction
in the fixed multiplicity grade.  The factorial in divided order two
normalizes the doubled-site coefficient to one.  Missing and deleted sites
automatically use order zero.

The checker independently enumerates all 540 marked branches.  It verifies
all 90 branch deletions containing `q23`, all 72 containing `q45`, including
the 60 and 48 `P3+K2` faces, and the selected first-principal-parts squares.
Every divided-root Beck--Chevalley commutator is zero.

For the selected branch the two target faces are

```text
delete q23: 07:02 | 45:12 | 67:22,
delete q45: 07:02 | 23:21 | 67:22.
```

Together with the retained missing-site mark these compress to the literal
lower words

```text
0112/q23:21,
0121/q45:12.
```

Thus the two marked-derived coefficient/word/fine/repeated rows are now
constructed with rank two.  Parent matching, missing site, doubled site,
deleted edge, and the `P3+K2` type are all preserved termwise.

## Exact remaining operation boundary

This calculation does not silently identify a decorated marked-derived cap
face with the underived physical `P2/B1` or `P2/B4` object.  The pinned E14
calculation already supplies the coefficient label association

```text
q23 response face -> B1,
q45 response face -> B4,
```

but explicitly does not supply the word/fine/**operation** transport.  The
divided endpoint action acts on coefficient and differential factors and
preserves the marked-derived operation idempotent.  In the four-coordinate
quotient

```text
(marked Dq23, marked Dq45, physical P2/B1, physical P2/B4)
```

its image is the first two axes, while the required physical rows are the
last two.  The two physical-coordinate covectors give an exact residual of
rank two.

The protected accounting is therefore:

- the parent augmentation is one, both (q)-faces are present, and the
  six-site target value is zero;
- the formal target/root-Eq cone has zero residual;
- the divided-root map does not supply complete Eq;
- aggregate `dq` ordinary residue is zero, but the labelled class
  (v=(B1+B4)/2) and its word-resolved face are not evaluated;
- the nearest physical dressing has (W=0), while no physical P2 ridge
  value is constructed.

The smallest full pointed section still has boundary

\[
 (\text{private }R,\text{root lower},\text{root Eq},
   \text{root ores})=(1,-1,0,1).                      \tag{3}
\]

The coefficient calculation proves the top entry in (3).  It does not yet
prove the hidden lower (-E), word-resolved ordinary-residue (+E), or the
underived operation landing.  Once that operation-labelled section is
constructed, the pinned simultaneous D4/P2/K_Eq/(d_{\rm even}) system is
nonsingular and closes the remaining target, Eq, residue, and anchor rows.

So the previous word obstruction has genuinely moved: the derived
`0112/0121` word/fine faces exist.  The next exact map is the underived
marked-derived-to-physical P2 operation comparison with boundary (3), not
another coefficient root identity.

## Scope and verification

Run:

```text
python3 computations/verify_h3_six_root_qface_restriction_commutator_gate.py --mode all
python3 computations/verify_h3_six_root_qface_restriction_commutator_gate.py --mode squarefree
python3 computations/verify_h3_six_root_qface_restriction_commutator_gate.py --mode branch
python3 computations/verify_h3_six_root_qface_restriction_commutator_gate.py --mode protected
```

The result is exact over the rationals.  It constructs a marked-derived
coefficient/word/fine Beck--Chevalley map, not an underived AugP2 comparison,
an absolute Eq filler, or a terminal separator.

Frozen ledger digest:

```text
e476c8a59693a496fa0ba81a4954b8e9d7ac973d3c2be3dca9c6a901e615945b
```

