# The terminal-only packet is the relative first jet of the ridge

## Exact identification

For one face write

\[
 a=q_{pq}^{22},\quad t=q_{pq}^{00},\quad
 b=q_{xv}^{0m_v},\quad u=q_{xv}^{00},
 \qquad \Omega_v=(a-t)-(b-u).
\]

The class left after the order-six residual lift is not an arbitrary new
terminal character.  It is exactly

\[
                         \gamma_v=-d\Omega_v
\]

in the relative first-principal-parts/Kähler module.  Indeed

\[
 \iota_{\eta_z}\gamma_v=1+\delta_{vz}u_z/t,
 \qquad
 \iota_\sigma\gamma_v=-q_{pq}^{22}.
\]

Its ordinary multiplication boundary is zero.  Hence its source boundary,
residue, `D`, `W`, target, and anchor projections are all zero—the exact
terminal-only packet isolated by `cc2d607`.

This identification is unique at the ridge level.  For a linear
combination `c_a a+c_t t+c_b b+c_u u`, impose the eta constant, eta
`u_z/t`, sigma `q_pq:22`, and zero coefficient-augmentation equations.  The
four-by-four system has rank four and unique solution

```text
(c_a,c_t,c_b,c_u)=(-1,1,1,-1).
```

Checker:
`computations/verify_h3_residual_q_terminal_ridge_kahler_identification.py`.

## What this removes from the frontier

We no longer need to guess a terminal correction or prove separately that
the affine eta primitive and the sigma face are compatible.  They are the
two contractions of one canonical relative differential.  The formula
`t-u_v` is simply the eta contraction of `-Omega_v`; it is not the source
coefficient of the missing cell.

This also explains why the order-six chain can be terminal-dark without
causing a contradiction.  It supplies the ordinary residual direction;
`-dOmega_v` supplies the relative terminal direction.  Their sum is the
old one-cell fiber target.

## The remaining physical gate

The raw Kähler identity is not yet a cell in the fixed physical fine grade.
The two halves have different site multidegrees:

\[
 \deg(a)=\deg(t)=e_p+e_q,
 \qquad
 \deg(b)=\deg(u)=e_x+e_v.
\]

A common tail preserves this mismatch.  The smallest ordinary polynomial
completion is

\[
 u(-a+t)+t(b-u)=tb-ua.
\]

Unlike the old `t-u` completion, this is a genuine determinant, not zero.
But it changes the terminal laws:

\[
 \eta_z(tb-ua)=b+\delta_{vz}(u_z/t)a,
 \qquad
 \sigma(tb-ua)=-ua,
\]

which are not the required identities over the full coefficient ring.
Thus ordinary homogenization is not the answer.

The exact next theorem is a **labelled shifted Kähler lift**:

> Retain the `pq` and `xv` halves of `-dOmega_v` as distinct relative
> principal-parts labels, shift them into the repeated `P3+K2` grade, and
> construct a physical higher differential whose image is their sum while
> preserving zero source/residue/protected rows.

The existing chart difference does not do this: it cancels the entire
physical column and every descended terminal.  The desired lift must be
chart-nondiagonal.  The order-six primitive face `07:11 wedge 24:11` is the
natural common attachment through which to type it.

## Consequence for the shortest proof

The local end game now has two concrete source constructions rather than an
opaque fiber-product problem:

1. physically type the explicit order-six residual chain;
2. lift the canonical relative class `-dOmega_v` through the same repeated
   grade.

The first already contains the conditional one-sided `(2,3)->(3,3)` rank
arm.  The second has completely fixed terminal data.  Once both are built,
their sum supplies the residual comparison, closes the unequal-tail
holonomy, and feeds the physical B/C comparison.

## Scope

This is an exact ridge/Kähler and grading theorem.  It does not assert that
the current physical relative source inventory contains the shifted class,
nor that the ordinary determinant completion has the correct terminal
readout.

Verification:

```text
python3 computations/verify_h3_residual_q_terminal_ridge_kahler_identification.py
python3 -O computations/verify_h3_residual_q_terminal_ridge_kahler_identification.py
python3 -I -S computations/verify_h3_residual_q_terminal_ridge_kahler_identification.py
```

Frozen ledger SHA-256:

```text
eee80a364e67043f2ebaae1f65461908b4943ee82dddbfd03a63dee8b69dad71
```
