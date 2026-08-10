# The Segre Rees response keeps the full cofactors

## Exact associated-graded system

Use the off-`01` cocharacter from `a17e42b`.  Give a residual cell the weight

\[
 \operatorname{wt}(q_{rs}^{ab})=u_{ra}+u_{sb},
\]

and give the pure-colour star entries `p_c@r,s_c@r` weight `u_rc` for
`c=1,2`.  Every matching monomial in the top coefficient of word `w` then
has the same grade

\[
                         \sum_r u_{r,w_r}.
\]

The identical formula holds for every monomial in all four response rows.
Consequently these equations are already Rees-homogeneous.  Their leading
system retains all 135 residual cells and all 24 star entries; it is not the
affine 24-cell face.

The exact weight census is

```text
q cells:       59 in grade 0, 62 in grade 1, 14 in grade 2
star entries:  12 in grade 0, 12 in grade 1
target grades: X0=0, X1=3, X2=3.
```

With the fourteen coefficients of `H` pinned, the Rees leading system still
has 145 free source coefficients.  The 729 top rows are homogeneous; the
four response blocks have respectively `473,602,602,473` nonempty word
rows.

## What survives of the odd triangle

In the restricted support of `4a213d8`, a selected diagonal response row is

\[
                         g_e=Q_e f_e,
 \qquad f_{rs}=p_rs_s+p_ss_r,
\]

with a single two-cell matching monomial `Q_e`.  In the full Rees source the
same row is instead

\[
                         g_e=F_e f_e,
\]

where `F_e` is the full three-term two-edge cofactor on the four remaining
sites.  The ordinary polynomial identity does lift:

\[
 2ABCabc F_{01}F_{02}F_{12}\in
 (F_{01}f_{01},F_{02}f_{02},F_{12}f_{12}).
\]

Thus the valid condition is nonvanishing of all three **cofactor sums**.
Nonvanishing of one physical monomial in each cofactor is insufficient.

## A literal one-cell counterguard

Take colour `1`, star triangle `{0,1,2}`, and the three actual response words

```text
110022, 101022, 011022.
```

The selected restricted-face factors are

```text
Q01 = (23:00)(45:22)
Q02 = (13:00)(45:22)
Q12 = (03:00)(45:22).
```

Set these factors to `1` and all six star entries on the triangle to `1`.
Add the single positive-weight cell `35:02`, with value `1`.  The fixed
Segre cell `24:02` already has value `-1`; set the face cells `14:02` and
`04:02` to `-1`.  Set the unused third matching factors to zero.  Then the
three full cofactors are literally

```text
F01 = (23:00)(45:22) + (24:02)(35:02) + 0 = 1-1,
F02 = (13:00)(45:22) + (14:02)(35:02) + 0 = 1-1,
F12 = (03:00)(45:22) + (04:02)(35:02) + 0 = 1-1.
```

All three full response rows vanish, while all six stars and all three
`Q_e` from the `4a` odd-clause antecedent remain nonzero.  This is a
source-labelled one-cell counterguard to lifting that Boolean clause.

It is not a full one-bad packet: the other top and response rows are not
asserted.  Its consequence is narrower and decisive.  The all-subsets
theorem remains exact on its fixed support, but its monomial odd clauses do
not promote through the off-`01` Rees filtration.  A further theorem would
need to force nonzero full cofactors or control their cancellations using
the remaining source rows.

## Reproduction

```sh
.venv/bin/python computations/verify_n8_one_bad_segre_rees_response_triangle_counterguard.py
.venv/bin/python -O computations/verify_n8_one_bad_segre_rees_response_triangle_counterguard.py
```
