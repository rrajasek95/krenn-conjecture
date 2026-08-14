# The cap tie is physical, but the cross-word tie is still the missing map

## Verdict

The statement `B=Eq` has two different meanings in the current proof, and
only one has been constructed.

The old cap generator `r_0` is genuinely tied.  Its literal full-nine
response boundary is the private packet `B`, while its cap differential is

\[
                 d r_0=(H_0-u)e_{\rm Eq}.
\]

Thus a column already known to be an `r_0` column carries both incidences.

The selected four-site response row is different.  It lives in response
word `11:110000`, whereas the cap generator lives in word `01211222` with
the repeated `P3+K2` and AugP2 operation tags.  No source-labelled map from
the former object to the latter has been constructed.  Consequently the
four tied rows inserted into the local rank-126 supermap are the result of
choosing the missing image to be `r_0`; they do not construct that image or
determine its mixed reduced-Eq incidence.

Exact checker:
[`verify_h3_uc4_beq_tie_source_provenance_audit.py`](../computations/verify_h3_uc4_beq_tie_source_provenance_audit.py).

## Exact sensitivity

Use coordinates

```text
B_0,...,B_3, Eq_0,...,Eq_3
```

and put `delta=(1,1,-1,-1)`.  The four cap rows and the four signless
square companions are

\[
 d_j=(e_j,\epsilon_j e_j),\qquad
 s_{ab}=(e_a+e_b,0),
 \quad a\in\{0,1\},\ b\in\{2,3\}.
\]

Here `epsilon_j=1` means the `j`th row is tied.

When all four rows are tied, the eight columns have rank seven and their
unique left kernel is

\[
                 \delta\cdot(B-\operatorname {Eq}).
\]

It detects the desired private balanced packet `(delta,0)`.

If exactly one row is untied, the rank is still seven.  The unique kernel,
however, is now the unused `Eq_j` coordinate at that corner.  It has value
zero on `(delta,0)`.  Thus the numerical rank survives while the claimed
terminal does not.  If two or more rows are untied, the rank drops below
seven and the cokernel is no longer one-dimensional.

This proves that all four equalities are load-bearing, not harmless
notation.

## Where the open datum lives

The canonical source-operation census leaves exactly eight mixed
cross-word/K_Eq interchange cells

```text
kappa_0012, kappa_0102, kappa_0110, kappa_0111,
kappa_0122, kappa_0212, kappa_1112, kappa_2112.
```

Their values

\[
             \lambda_i={1\over4}\delta\cdot(B-\operatorname {Eq})
                         (d\kappa_i)
\]

are explicitly recorded as undecided.  The cross-word `B=Eq` claim is
equivalent to setting the relevant values to zero.  A nonzero value is the
rank-seven to rank-eight filler branch; proving all values zero is the
terminal branch.  The old internal `r_0` tie does not choose between them.

## Correct proof status

The local rank-126 theorem remains a valid algebra theorem for the declared
tied four-site supermap.  It should be used conditionally:

```text
if the physical cross-word image factors through tied r_0 rows,
    Psi_loc is the unique local terminal;
otherwise
    its private-minus-Eq component is exactly the missing filler scalar.
```

This does not add a new obstruction.  It identifies the existing eight
mixed incidences as the sole place where the load-bearing tie must be
proved or broken.

## Verification

```text
python3 computations/verify_h3_uc4_beq_tie_source_provenance_audit.py
python3 -O computations/verify_h3_uc4_beq_tie_source_provenance_audit.py
python3 -I -S computations/verify_h3_uc4_beq_tie_source_provenance_audit.py
```

Frozen ledger SHA-256:

```text
1ba9269700cead684c84fc90642da8dab3676e3d12a93826d43dfc190542978f
```
