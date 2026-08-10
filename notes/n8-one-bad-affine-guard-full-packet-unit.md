# The frozen affine-concentration guard is killed by the unary top row

## Exact verdict

Imposing the complete one-bad packet on the fixed (q)-fibre from `c11e7b7`
gives the unit ideal for the smallest possible reason.  The five-cell
quadratic is


```text
q = 13:11 + 24:11 + 12:10 - 02:10 + 34:00.
```

Every cell avoids residual site 5, so (q^{[3]}=0) identically—not only at
the displayed coefficients, but on the entire support/coefficient fibre.
The required unary equation is (q^{[3]}=X_0).  Its pure coefficient is
therefore


\[
                      g_{000000}=0-1=-1,
\]

and the ordinary physical source certificate is simply


\[
                         \boxed{-g_{000000}=1}.          \tag{1}
\]

No Gröbner basis, saturation, localization, or finite-field calculation is
needed.

The exact checker is
`computations/verify_n8_one_bad_affine_guard_full_packet_unit.py`.

## The missing binary rows were imposed symbolically

The conclusion is not based on omitting the requested equations.  Keep the
exact first response rows


```text
p1 = e1@0 + e1@1,     s1 = e1@5,
p1*s1*q^[2] = X1,
```

and introduce arbitrary multisite rows


\[
p_2,s_2\in\bigoplus_{u=0}^5\mathbb C^3,
\]

with all 36 scalar coordinates independent.  The checker reconstructs all
729 output words in each of


\[
 p_1s_1q^{[2]}=X_1,qquad
 p_1s_2q^{[2]}=0,qquad
 p_2s_1q^{[2]}=0,qquad
 p_2s_2q^{[2]}=X_2.                                  \tag{2}
\]

After exact collection, the nonzero generator counts are


```text
unary top:       1
response 11:     0
response 12:     3
response 21:    11
response 22:    34
```

The last three families are respectively linear, linear, and bilinear in
the new star variables.  They are genuine symbolic source equations, but
they are irrelevant to ideal emptiness because (1) is already a generator.
The checker hashes their exact sparse streams so later changes cannot hide a
different response packet behind the same one-row certificate.

## What enforces concentration here

No equation enforces Hall or coordinate concentration on this fixed fibre.
The unary top row deletes the fibre before either question arises.  Thus the
right theorem-level conclusion is negative but sharp:

> The `c11e7b7` cancellation circuit is a local normal form only for the
> response map.  It is not a local normal form for a full one-bad packet with
> fixed (q).

To retain that circuit inside a full packet, one must deform (q) by adding
site-5 incidence (and generally further cells) so that (q^{[3]}=X_0).  Such
a deformation changes (q^{[2]}), hence changes the affine joint kernels
whose lack of coordinate points was proved in `c11e7b7`.  The remaining
problem is therefore a **relative deformation problem**:


\[
\begin{cases}
q(t)^{[3]}=X_0,\\
p_i(t)s_j(t)q(t)^{[2]}=\delta_{ij}X_i,
\end{cases}
\]

with the multisite cancellation circuit at a boundary value.  It cannot be
settled by solving only for a second star pair over the frozen common square.

## Scope

This closes exactly the fixed five-cell (q)-fibre, with arbitrary
multisite (p_2,s_2).  It does not address the unrestricted 135-variable
quadratic (q), whose whole-packet Macaulay frontier is recorded separately.
It also does not show that every full packet concentrates: it shows why this
particular response obstruction cannot itself be a full-packet survivor.

## Verification

Run


```bash
uv run python computations/verify_n8_one_bad_affine_guard_full_packet_unit.py
uv run python -O computations/verify_n8_one_bad_affine_guard_full_packet_unit.py
```

The frozen ledger digest is


```text
6bcfbd5dd391dabed8061702bd8143f0fa31554677bca07701d121699037c8d1
```
