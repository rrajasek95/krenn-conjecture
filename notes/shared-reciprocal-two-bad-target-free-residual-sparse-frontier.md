# The residual-pure branch starts on the singular hidden-colour cofactor locus

## 1. Source-level reduction

Keep the common five-site quadratic `q`, write the missing colour as `t`,
and put

\[
 k_x=[e_t^{\otimes(C\setminus x)}]H_{C\setminus x}(q).
 \tag{1}
\]

Thus `k_x` is the all-`t` coefficient of the four-site cofactor at the
hole `x`.  The raw `X_t` coefficient of a cofactor-image column is zero
unless the inserted colour is `t`, in which case it is `k_x`.  Every
literal product in

\[
 {\cal R}_{nt}=\operatorname {im}\bigl(A_1\otimes(NK)
             \xrightarrow{\mathcal T}\operatorname {coker}\Phi\bigr)
 \tag{2}
\]

has a target-free factor, so its raw `X_t` coefficient is always zero.
Consequently

\[
                     k=0\quad\Longrightarrow\quad
                     [X_t]\notin{\cal R}_{nt}.           \tag{3}
\]

There is a second exact restriction.  Let `N in ker(Phi)` have zero
`t`-projection.  In `Phi(N)`, the coefficient of the word which is `t`
at four sites and `b!=t` at `x` has only one possible insertion site:
`x`.  It is

\[
                              N_{x,b}k_x.                 \tag{4}
\]

Hence

\[
                  N_x\ne0\quad\Longrightarrow\quad k_x=0,
                  \qquad \operatorname {supp}N\subseteq Z(k). \tag{5}
\]

Any residual-pure packet must therefore lie on the **singular hidden-colour
cofactor locus**: `k` is nonzero, but has a zero set large enough to carry
a target-free cofactor-kernel row.  This is support-independent.  It is the
next theorem target, not a claim that the whole locus is empty.

More precisely, put `Z=Z(k)` and restrict the cofactor insertion map to

\[
 \Psi_Z:\bigoplus_{x\in Z}\langle e_a,e_c\rangle_x
        \longrightarrow V_C,
 \qquad (n_x)\longmapsto\sum_{x\in Z}n_x^{(x)}H_{C\setminus x}(q). \tag{6}
\]

Then the target-free kernel is exactly `ker(Psi_Z)`.  For `|Z|=1`, a
nonzero kernel forces the entire four-site cofactor at that hole to vanish.
For `Z={x,y}`, the two nonzero summands have the exact zero-Koszul form

\[
 H_{C\setminus x}=n_y^{(y)}Z_0,
 \qquad H_{C\setminus y}=-n_x^{(x)}Z_0                 \tag{7}
\]

after rescaling, for one common three-site tensor `Z_0`.  At larger `Z`,
the load-bearing invariant is still `rank(Psi_Z)<2|Z|`; cardinality of the
zero set alone is not enough.

## 2. Exact sparse frontier at the Pythagorean packet

Start with the pinned five-cell Pythagorean common power

```text
12:00=3/5, 02:00=4/5, 34:00=1, 01:11=1, 23:11=1.
```

Adjoin between two and four nonzero endpoint-coloured cells.  A nonzero
`k` requires two disjoint `tt` cells.  Restrict to supports for which the
combined old and new site-colour character vectors are independent.  Over
the algebraically closed field, the sitewise diagonal torus then normalizes
all added coefficients to one while preserving pure-image membership,
kernel dimension, target-freeness, and residual-pure membership.

Exact rational enumeration gives

| new cells | supports with a `tt` matching | torus-independent | retain `X_0,X_1 in im Phi` | retained `rank Phi` |
|---:|---:|---:|---:|---:|
| 2 | 15 | 15 | 0 | -- |
| 3 | 1,215 | 1,215 | 4 | 15 |
| 4 | 48,580 | 48,055 | 46 | 15 |

Thus every retained chart in this exact frontier has

\[
                    \ker\Phi=N={\cal R}_{nt}=0.          \tag{8}
\]

The branch does not begin on any torus-independent deformation of this
component with at most four new cells.  This is substantially stronger
than the old Pythagorean point guard, where `R_nt` was nonzero but missed
`X_t`.

The singular locus itself is real.  The six unit cells

```text
12:00, 34:00, 01:11, 23:11, 04:22, 13:22
```

give `X_0,X_1 in im(Phi)`, `X_2 notin im(Phi)`, and
`k=(0,0,1,0,0)`.  Nevertheless `rank(Phi)=15`.  Even though `|Z(k)|=4`,
the eight columns of `Psi_Z` have rank eight.  This exact common-provenance
guard disproves any attempted conclusion from `k!=0`, singularity of `k`,
or the size of `Z(k)` alone.  A genuine branch-(i) packet additionally
needs the restricted cofactor-syzygy rank defect.

## 3. Scope guard and next calculation

This is not the universal exclusion of `[X_t] in R_nt`.  It deliberately
does not decide:

* the 525 character-dependent four-cell supports, whose coefficient
  invariant cannot be normalized away;
* five-or-more-cell deformations of the Pythagorean packet; or
* other binary common-power components.

The load-bearing continuation is now structural.  Combine
`X_a,X_c in im(Phi)`, `X_t notin im(Phi)`, and (5) to constrain the support
and rank of `k`; equivalently, classify binary six-site matching sources
whose common five-site power has a target-free star syzygy supported on
`Z(k)`.  A theorem forcing `k=0` (or forcing `Phi` injective when `k!=0`)
would close the residual-pure branch.  A rational point with `k!=0`,
`N!=0`, and `[X_t] in R_nt` would instead be the first honest seed.

## 4. Reproduction

```sh
.venv/bin/python computations/verify_shared_reciprocal_two_bad_target_free_residual_sparse_frontier.py
.venv/bin/python -O computations/verify_shared_reciprocal_two_bad_target_free_residual_sparse_frontier.py
```

The exact ledger SHA-256 is

```text
969f695da1d0bb7baeca303f425594050e6b38186b13d2f32bc5ded456f6054b
```
