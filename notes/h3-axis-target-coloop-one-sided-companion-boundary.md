# One-sided companion proportionality is an exact finite reduction

## Result

Continue with one of the seven single-`C6/C8` target-coloop records at
`h=3`.  On a selected mixed zero word, the active outside matching `N` and
its forced target-port companion `M` have the same endpoint output labels.
Thus their two `P`-port cells are components of one literal row `p_i`, and
their two `S`-port cells are components of one literal row `s_j`.  They need
not use the same physical ports.

Fix `q` and the entire opposite star.  For a `P` component `z`, let

\[
 {\mathcal L}_s(z)=\bigl(zs_1q^{[2]},zs_2q^{[2]}\bigr)       \tag{1}
\]

with **every** fine output coefficient retained.  If the outside and
companion columns satisfy

\[
              {\mathcal L}_s(z_{\rm out})=\lambda
              {\mathcal L}_s(z_{\rm cmp}),                  \tag{2}
\]

and their scalar coefficients in `p_i` are `x_out,x_cmp`, then

\[
 x_{\rm out}\mapsto0,\qquad
 x_{\rm cmp}\mapsto x_{\rm cmp}+\lambda x_{\rm out}    \tag{3}
\]

preserves all four response tensors exactly.  The unary top and the other
endpoint rows do not involve `p_i`, so they are unchanged as well.  This is
a finite `P`-only joint-kernel modification; changing both endpoint stars
and accounting for a bistar Hessian is unnecessary.  The transposed
statement holds for `S`.

Checker:
[`verify_h3_axis_target_coloop_one_sided_companion_boundary.py`](../computations/verify_h3_axis_target_coloop_one_sided_companion_boundary.py).

## Exact anchor-safety scope

The outside component is, by hypothesis, off the selected anchor union.
Equation (3) therefore strictly reduces support provided the companion
coefficient remains nonzero, or provided its decoration is not protected by
a selected anchor.  Changing the numerical coefficient of a protected cell
while it remains nonzero does not lose that literal anchor.

There is one sharp exception:

```text
z_cmp is a protected anchor decoration
and x_cmp + lambda*x_out = 0.
```

Then (3) zeros the protected companion together with the outside component.
It is still an exact source modification, but it is not a contradiction to
the maximum-anchor-then-minimum-support choice because it can lose an
anchor.  This is an anchor-contained Hall/lock stratum.  It must not be
reported as a free deletion.  In particular, proportionality of one chosen
coefficient is insufficient throughout: (2) must hold for the complete
labelled tensor columns.

If the two complete columns are not proportional, their rank is two, hence
some pair of fine output coefficients has a nonzero `2 x 2` minor.  This is
the exact one-sided alternative on both endpoint stars.

## The symmetric nonproportional branch

Normalize the target ports to `P-0,S-1` and the outside ports to
`P-2,S-3`.  On the selected word form the physical four-corner cofactor
matrix

\[
 K_d=
 \begin{pmatrix}
 H_{01}(d)&H_{03}(d)\\
 H_{21}(d)&H_{23}(d)
 \end{pmatrix}.                                        \tag{4}
\]

The checker audits all three tails on each corner for every one of the
seven single-cycle records.  Its contained-support matrix is always

\[
 \#\{\hbox{matchings contained in }M\cup N\}
             =\begin{pmatrix}1&0\\0&1\end{pmatrix}.    \tag{5}
\]

The two diagonal entries are exactly the selected tails `T_M,T_N`.
Every other diagonal or crossed-corner matching contains a residual `q`
edge outside `M union N`.  There are `70` such matchings across the seven
records.  Consequently the branch where both endpoint pairs are
nonproportional has the exact physical split:

1. an additional supported corner term is a literal external `q` mate and
   opens the single alternating cycle; or
2. no such term occurs, and

   \[
                K_d=\operatorname{diag}(T_M,T_N),qquad
                \det K_d=T_MT_N\ne0.                  \tag{6}
   \]

   This is the selected-word bistar/Fitting carrier.

The external edge in the first branch is external to `M union N`; it can
still be anchor-contained, in which case the Hall/lock routing is required.

## Sharp remaining boundary

This result deliberately does **not** identify (6) with a determinant of
the two complete tensor columns.  Such a promotion requires the `P` and `S`
minors to be detected in a common fine-word pair.  Without that synchrony,
the honest survivors are:

```text
protected companion-decoration lock,
or selected-word bistar carrier awaiting a compatible full-row landing.
```

The forced unary/direct third base from the physical `E3` theorem supplies
a third matching outside `M union N`, but if it is the already selected
unary anchor it does not itself repair the lost bright deleted-star colour.
This is not just a rank warning.  The checker superposes each of the `15`
possible unary bases on each of the seven single-cycle records.  Among the
`105` physical three-base unions, `55` contain a matching with crossed ports
`(P-2,S-1)` or `(P-0,S-3)`, while `50` contain no crossed response matching
at all (`10` over the `C6`, `40` over the six `C8` records).  Therefore the
unary base plus (6) does not automatically enter the strict Hall or
five-lock theorem.  Even in the `55` topological hits, the crossed matching
still needs its actual response decoration and nonzero coefficient.

The smallest new physical input is consequently precise: a complete
response companion selecting one of the crossed matchings, or an alternate
bright matching avoiding the target-coloop arm.  Either repairs the rank or
opens the anchor web; absent it, the `50` no-cross unions are a genuine
full-row provenance residual rather than a missing graph enumeration.

## Verification

Run

```text
python3 computations/verify_h3_axis_target_coloop_one_sided_companion_boundary.py
python3 -O computations/verify_h3_axis_target_coloop_one_sided_companion_boundary.py
python3 -I -S computations/verify_h3_axis_target_coloop_one_sided_companion_boundary.py
```

Frozen ledger SHA-256:

```text
d9ab3e869fac17f1adf932e3a7aebcc66ac6b62f424c12cfc41aacb69f4b10b4
```
