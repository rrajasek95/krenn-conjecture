# The first-flat physical bridge has a canonical aggregate separator

## Exact result

Work in the canonical endpoint-recoloured order-six block and in the
repeated `P3+K2` component joining faces `(3,5)`.  Impose simultaneously

1. all three complete quadratic source equations;
2. the prescribed second shadow `-delta`;
3. zero first Spencer face; and
4. equality of the normalized `07:11` covariance/arm-contraction face with
   a boundary in the complete 288-column repeated full-nine component.

The resulting exact matrix has 8,580 order-six columns, 288 repeated
completion columns, 21,116 rows after retaining the pure aggregate, and
rank 1,620 over `Q`.

The zero-normalized system is soluble over `Q`.  A deterministic sparse
solution has 336 terms, all 336 in the order-six operator block and none in
the repeated completion block.  Its repeated pure-row aggregate is zero.

Now require the sum of the six pure-word repeated coefficients to be one.
The same exact elimination becomes inconsistent at the aggregate row
itself:

```text
(4, "pure_aggregate").
```

Consequently the pure aggregate vanishes on the homogeneous kernel of the
source/first-Spencer/bridge matrix.  Equivalently, it factors through the
old output constraints and cannot be changed by another polynomial
full-nine correction.  This is a characteristic-zero statement, not only a
finite-field rank guard.

The factorization is integral and sparse.  It uses exactly six literal
repeated-boundary matching coordinates, one from each compatible pure-word
multiplier column, all with coefficient `-1`; it uses no source, first
Spencer, or second-shadow coordinate.  If `Q` denotes the pure aggregate
row and `m_1,...,m_6` those six complete-boundary coordinates, the audited
column identity is

\[
                         Q=-m_1-\cdots-m_6.             \tag{1}
\]

Thus `Q+m_1+...+m_6` is the first literal six-term dual candidate.  It is a
valid annihilator of this complete bounded matrix.  Promotion to the proof
still requires showing that its six matching-coordinate values are the
physical terminal values on the exhaustive relative cone; otherwise a
higher relative cell may kill the bounded dual.

Unlike the earlier coarse `Omega` aggregate, this dual passes the known
physical stabilizer test.  The six monomials have one common physical fine
degree.  Each contains exactly one colour-zero incidence at every physical
site.  Consequently it has weight zero under every

```text
p:0 - z:0,     x:0 - z:0,     p:2 - x:2,     x:0 - p:0
```

field used by the marked non-Euler and full-Jacobian audits.  In particular,
the five `eta_z` columns which destroyed the old aggregate separator pair to
zero here.  This does not prove invariance under every future relative
generator, but it eliminates the first committed zero-indeterminacy
counterguard and explains the gain: the new dual is fine-grade homogeneous,
whereas `Omega_v` mixed distinct characters.

The solution digest is

```text
ce6b0ac61d5b05b67b5215a3855e8ca36ed0b6609e6c03ec38dd3a37a9aadda5.
```

## Literal bridge geometry

For the first-flat representative, the endpoint primitive outputs have
supports `18,20,3`; every fine component has site profile

```text
(2,1,2,1,2,1,1,2).
```

Only the middle source product contributes to the selected faces-`3/5`
grade.  Among its 192 normalized presentations, exactly 48 are literal and
all contract the physical direction `07:11`.  No individual transform lies
in the old repeated component; their quotient span has rank 12.  Thus the
abstract `07:01` stub of the sparse grading model is not the physical
derivative, but the first-flat affine representative does contain the
correct `07:11` Spencer face.

## Proof meaning

This closes two possible loopholes at once.

* The comparison failure is not caused by choosing a sparse representative:
  the complete first-flat affine family was used.
* The missing primitive vertex is not hidden in the complete old repeated
  full-nine source component: its pure aggregate is exactly zero on every
  allowable kernel modification.

A pure repeated row has physical target `+1` and anchor incidence `-1`.
Therefore the aggregate above is not by itself the desired target-zero
relative anchor.  The theorem proves that the next object must be a genuine
relative comparison/bar cell whose differential separates these readouts,
or the corresponding aggregate factorization must be promoted to the
physical terminal/Fredholm separator.  Adding more polynomial repeated rows
cannot do either.

This is precisely the structural boundary predicted by the exhaustive-cone
proof sketch: the universal Spencer contraction exists, its old physical
source realization has only the zero aggregate, and the remaining datum
lives in relative homology.

## Scope

The theorem is complete for the bounded first-flat order-six block, one
canonical normalized bridge presentation, and the complete old repeated
full-nine component.  It does not construct the new relative cell, prove
that the aggregate factorization is the physical terminal on the exhaustive
bar cone, or perform transverse-rank landing.

Verification:

```text
python3 computations/verify_h3_first_flat_endpoint_bridge.py
python3 -O computations/verify_h3_first_flat_endpoint_bridge.py
python3 -I -S computations/verify_h3_first_flat_endpoint_bridge.py
```

Frozen ledger SHA-256:

```text
de8151738fe609f857e4e5917c3555067b2a9681018567fd11236c706316d997
```
