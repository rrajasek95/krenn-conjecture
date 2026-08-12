# The residual-q cokernel is not yet a physical rootless dual

## Exact local class

The mixed curvature/rootless-bar near-hit has now reduced the shared
attachment problem to one literal word and one repeated fine grade.  After
deleting the exposed `x=0`, the word is

```text
1211222,
```

the coarse response degree is `(p,s,q)=(1,1,2)`, and the first common cell
degree is the labelled repeated `P3+K2` degree.  In the ordered residue
basis

\[
 (P_+q_{00},P_-q_{00},P_+q_{11},P_-q_{11}),
\]

where

\[
 q_{00}=a_{24}^{11}a_{35}^{11},\qquad
 q_{11}=a_{24}^{21}a_{35}^{12},
\]

curvature minus the determinant-multiplied rootless bar leaves

\[
 \delta=(1,-1,-1,1)
       =(P_+-P_-)(q_{00}-q_{11}).                     \tag{1}
\]

Thus the missing Kodaira--Spencer correction has the pinned sign

\[
                         -\delta=(-1,1,1,-1),          \tag{2}
\]

with `W=target=ainc=0`.  This is the only correction sign which cancels the
ordinary residue of the existing near-hit.

The committed reciprocal/old-residue block is endpoint-even on each tail.
Its two coarse columns are

\[
 e_{00}=(1,1,0,0),\qquad e_{11}=(0,0,1,1).           \tag{3}
\]

The covector

\[
 \ell_{\rm res}=(1,-1,-1,1)                          \tag{4}
\]

kills both columns in (3) and reads `4` on (1).  Consequently (1) is a
genuine cokernel class of the **committed endpoint-even residue block**.
This is sharper than the earlier two-coordinate parity statement, but it
is still not a physical Fredholm annihilator.

## Why the promotion fails

The physical rootless presentation has rows

\[
 (\Omega_v,Q_{v,N},r_v,\mathrm{ores})
\]

and includes the five target-stabilizer relations `eta_z`.  Before those
relations, endpoint routes, hypothetical same-labelled PP lifts, clean C5
edges, and the pure-residue column leave one dual line: the exact constraint
matrix has `26` covector variables and rank `25`.  After the five physical
`eta_z` families are inserted, its rank is `26`.  There is no nonzero
same-labelled-`Q` dual left.

The signs are facewise exact.  On `t=q_pq^00 != 0`,

\[
 d\Omega_v(\eta_z)=
 \begin{cases}
 -1,&v\ne z,\\
 -1-u_z/t,&v=z,
 \end{cases}                                         \tag{5}
\]

whereas every selected `Q_(v,N)`, every currently defined rootless `r_v`,
and all four selected-colour residue corners in (1) have `eta_z` readout
zero.  Hence the old aggregate rootless covector reads

\[
                         -5-u_z/t.                    \tag{6}
\]

The local residue dual (4) survives (5) trivially because it sees none of
the `Omega` rows.  That is exactly the problem: no committed physical chain
map identifies (4) with a covector on the `Omega/Q/r` presentation.  The
known physical relations kill the latter presentation's proposed dual.
Calling (4) a rootless Macaulay annihilator would silently assume the
missing comparison theorem.

## The complete augmented-map interface

Let

\[
 J_{\rm phys}:C_{\rm phys}\longrightarrow Y_{\rm aug}
\]

be the matrix in this one word and fine grade.  To be complete and
physically typed, its domain must contain every source-provenant correction
generator and relation which can land in the grade, and its rows must retain

```text
literal E+/E-/Omega/qcomp boundary,
the four separate residue corners in (1),
physical W, target, and anchor incidence,
source word and chart labels.
```

It must also contain the `eta_z` relations, the endpoint/bar and PP
common-companion relations, and any higher collision or mapping-cone cells
capable of the grade.  Finally one needs a physical terminal row `tau`; the
derived chart scalar is not a substitute.

Once this finite matrix exists, ordinary exact linear algebra is decisive.

1. If `-delta` is outside `im(J_phys)`, a left-kernel covector detecting it
   is a genuine physical separator because the source census is exhaustive.
2. If `-delta` lies in the image and `tau(ker J_phys)` is nonzero, a kernel
   element normalizes to terminal value `-1` and is the relative generator.
3. If `-delta` lies in the image and `tau(ker J_phys)=0`, the terminal value
   of the lift is well-defined; this is the zero-indeterminate attachment
   branch.

The checker exhibits three extensions of the same committed even submatrix
(3): no new column gives branch 1, one `-delta` column gives branch 3, and
two `-delta` columns with different terminal values give branch 2.  Thus
failure in the bounded block logically determines none of the three
physical outcomes.

## Sharp verdict and next theorem

At present we have a nonzero **local residual Ext/cokernel class**, not a
physical left separator and not a kernel-relative generator.  The missing
physical map is not bookkeeping.  It must either

* construct a source-provenant `-delta` correction in word `1211222` and
  the labelled repeated `P3+K2` grade, with the protected readouts zero and
  with a terminal comparison satisfying

  \[
                         d r_v(\eta_z)=d\Omega_v(\eta_z),              \tag{7}
  \]

  equivalently aggregate compensating readout `5+u_z/t`; or
* prove an exhaustive physical source census in that grade which excludes
  such a correction.  Only that exhaustive failure promotes the local
  covector to the physical separator.

This removes a misleading branch from the frontier: more endpoint-parity
or common-multiplier searches cannot decide the conjecture.  The next
load-bearing object is the residue-to-rootless comparison with the eta law
(7), together with its physical terminal row.

Verification:

```text
python3 computations/verify_h3_residual_q_physical_duality_interface_counterguard.py
python3 -O computations/verify_h3_residual_q_physical_duality_interface_counterguard.py
python3 -I -S computations/verify_h3_residual_q_physical_duality_interface_counterguard.py
```

Frozen ledger SHA-256:

```text
4d6bd576c9adff697dcc9c5dfe3ea68c60d90f7a301fd0c555d4de46492fbdbe
```
