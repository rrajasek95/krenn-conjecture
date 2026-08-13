# Inverting the coloop coefficient does not select an occurrence

## Exact localized result

Work on the pure-colour coloop chart

\[
                 \alpha C_c=1,
\]

so `alpha` is a unit.  For one other response channel, the complete rows
and affine target normalization are

\[
 dC+U=1,\qquad \alpha C+V=0.                         \tag{1}
\]

Suppose the bright aggregate contains the smallest nontrivial packet of
two literal occurrences.  In the `U`-bright case write `U=f+g`; in the
`V`-bright case write `V=f+g`.  After localizing at `alpha`, the two quotient
rings are both exactly

\[
                  k[\alpha^{\pm1},d,C,f].             \tag{2}
\]

Indeed, the equations successively eliminate `alpha^{-1},C_c,U,V,g`:

```text
Cc=alpha^-1,   U=1-dC,   V=-alpha C,
g=U-f  or  g=V-f.
```

Thus the localized packet is a nonempty integral chart with `f` free.  It
does not contain a hidden source unit.

Checker:

```text
computations/verify_h3_coloop_alpha_localized_pointed_pf_ga_fitting_gate.py
```

## The tangent obstruction integrates

The earlier tangent `df=1,dg=-1` is not an artifact of linearization.  It
integrates on the entire localized chart to

\[
                     f\longmapsto f+t,\qquad
                     g\longmapsto g-t.                \tag{3}
\]

Every equation in (1), the coloop equation, and the chosen aggregate split
is fixed by (3), and `alpha` remains invertible.  Its infinitesimal generator
reads one on the affine pointed conormal

\[
                           P_f=df                    \tag{4}
\]

because `du=0`.  Equivalently, relative to all aggregate coloop data,
the cotangent module is the free rank-one module `R df`.

Even if a nonzero literal `f` is chosen and one further restricts to `D(f)`,
the logarithmic vector field

\[
                  f(\partial_f-\partial_g)
\]

preserves the aggregate and reads one on `dlog(f)`.  Hence “choose a bright
term and divide by it” still does not turn its pointed comparison into a
consequence of the complete rows.

## Exact Fitting alternative

On the two occurrence columns `(f,g)`, the complete aggregate has row
`(1,1)`.  For any additional physical row `r=(r_f,r_g)`, the transverse
minor is

\[
 \det\begin{pmatrix}1&1\\r_f&r_g\end{pmatrix}
                         =r_g-r_f.                    \tag{5}
\]

Multiplication by the unit `alpha`, or any other rescaling of the same
complete row, keeps `r_f=r_g`; its minor remains zero.  Before an
occurrence-asymmetric physical row is supplied, the relative zeroth
Fitting ideal is therefore `(0)`, not the unit ideal.  If a full-source row
has unequal occurrence coefficients, (5) is exactly the Fitting carrier;
if the difference is a unit on the chart, it is the desired localized
source/Fitting exit.  Taking the selected row `(1,0)` would give the unit
minor `-1`, but that is precisely the unproved physical `P_f` row.

## Sharpened frontier

The pure-colour coloop provides a monic aggregate pivot and permits division
by `alpha`; it does not break the occurrence-redistribution symmetry.  The
smallest remaining obstruction is the free rank-one difference module

```text
df=-dg.
```

It is killed exactly by a source-valid row whose two occurrence coefficients
differ.  In the current proof this is the same physical question as

```text
e_f^* in row(full endpoint + simultaneous-q source map),
```

with nonmembership usable only after its dual survives every augmented
source column and reaches an accepted terminal.  The result is a no-go for
the localized coloop/complete-row packet alone, not for the full physical
source complex.

## Verification

Run

```text
python3 computations/verify_h3_coloop_alpha_localized_pointed_pf_ga_fitting_gate.py
python3 -O computations/verify_h3_coloop_alpha_localized_pointed_pf_ga_fitting_gate.py
python3 -I -S computations/verify_h3_coloop_alpha_localized_pointed_pf_ga_fitting_gate.py
```

Frozen ledger SHA-256:

```text
ddb5db5296ee5fb92597ac7b33395299efd96cd8ce098d0c8c1951eb77b1e629
```
