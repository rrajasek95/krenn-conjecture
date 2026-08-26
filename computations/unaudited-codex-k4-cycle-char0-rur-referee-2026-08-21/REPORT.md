# K4-cycle all-minor RUR referee

## Decisive correction

The modular all-minor RUR components are **not** points of the full
branch-0 source.  The determinantal export retains the four triangle rows,
`Cof(0,0)`, `Cof(0,3)`, and `Cof(e,0)` for `e=1,...,5` through its affine
packet.  It never imposes the five literal rows

```
Cof(1,3), Cof(2,3), Cof(3,3), Cof(4,3), Cof(5,3).
```

The six permanent equations are already identically solved by the block
parametrization.  Thus these eleven retained rows plus the five omitted
rows are the sixteen nontrivial members of the literal 22-row branch-0
source.

`audit_modular_rur_full_raw_rows.py` reconstructs the RUR coordinates
directly, checks all sixteen exported equations and the F4SAT live factor,
performs the unique rank-three affine source solve, and then evaluates all
sixteen nontrivial literal rows in every irreducible factor field.  At both
`p=1073741827` and `p=1073741789`, all sixteen irreducible factors (32
factor fields total) fail exactly the same five omitted cofactors and no
other literal row.  The first factor at each prime is quadratic and remains
Hafnian-live, providing the must-fire control.

Result logical SHA-256:

```
36dfe4bcee4855b546de0d837405ed0e2b239345eb0859eeacadfc9a06018188
```

This is exact finite-field arithmetic, not sampling.  It proves that every
reported modular all-minor component is a determinantal false positive for
the full source.  It makes no characteristic-zero assertion.

## Characteristic-zero parser correction

The first characteristic-zero input used a Rabinowitsch row containing
coefficient-after-symbol products such as `z*2*x`.  msolve 0.10.1 silently
changes such terms.  The two toy inputs in this directory demonstrate the
failure exactly: with `x-2`, the malformed `z*2*x-1` returns `z=1/2`, while
the canonical `2*z*x-1` returns the correct `z=1/4`.  An output of the form
`[1,n,-1,[]]:` is msolve's positive-dimensional sentinel and must never be
parsed as an RUR.

The canonical exporter now prints coefficients first.  Any canonical
characteristic-zero RUR remains only a parametrization of the necessary
all-minor locus until the five omitted literal cofactors are replayed and
shown to vanish.  In view of the two-prime referee, reduction of even one
of those cofactors is the first decisive exact test.

## Independent Cof(1,3) branch control

`export_cofactor13_cramer_obstruction.py` constructs a determinant-safe
Cramer homogenization of the omitted literal `Cof(1,3)`.  Its reduced core
has 7,264 terms and SHA-256
`058684ffb96848a3bd96de7835a986bdbcd1017b5d579f3abd6f163a23bb8cf6`;
an independent raw replay in the neighbouring exact lane agrees byte for
byte.  The three-variable generic factor system did not finish within its
bounded 60-second run, so no generic UNIT is claimed from it.

The exceptional `b1=d1` branch required a different Cramer packet because
the original obstruction vanishes identically there.  The bounded exact
packet export found two nonzero determinant-safe rows, from source triples
`(0,1,2)` and `(0,1,4)`, with 2,370 and 3,197 terms respectively.  After
specializing all fifteen packet minors and preserving every factor of the
original open-set saturator, the branch is UNIT at both large primes.  The
exact export logical digest is
`7a9eb561b533d12169e72a7c2978f8d5ebcb48e5b89a92c02b4f863c815dba83`;
the two toolkit manifests have logical digests
`8737c9a2ea0dd0d2cf16d758008edd3637fb9ecbbbe92a30eecb64a23817202e`
and
`47295861910f1e69ac9f7bb148ea58725a008b4a46a30618c2b763fad39f56e9`.

A must-fire exporter regression initially stripped the live monomial
`b0*d1*x` from the *saturator itself*, producing a false nonunit leading
shape `{b0^2,d1^2*x^3}`.  Restoring those factors changes both primes to
UNIT.  The false result is not evidence.  This two-prime branch closure is
only an independent modular control and was not lifted over `Q`, because a
separate exact `Cof(3,3)` certificate subsequently closed the whole
`Delta=0` subtree.
