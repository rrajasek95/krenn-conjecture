# A typed common-tail C4 routes the first k=3 minor to an active carrier

## Result

Let `C0,C1,C2` be the three occupied complete columns of a minimum-support
axis response, where a complete column retains both the diagonal and crossed
response tensors.  If

\[
                 \lambda_0C_0+\lambda_1C_1+\lambda_2C_2=(X_i,0),
                 \qquad \lambda_0\lambda_1\lambda_2\ne0,                 \tag{1}
\]

then their images modulo the target line have rank two.  Consequently two
literal mixed output-word coordinates have a nonzero `2x2` minor.  No
occupied column can itself lie on the target line: that would reduce the
quotient rank to at most one.  Coordinate-line hitting, if it occurs, must
therefore use another coordinate column and an actual affine joint-kernel
translation; it is not hidden among the three occupied components.

Expand the nonzero minor using the genuine common-`q` matching tails.  A
selected product of two nonzero literal terms gives two perfect matchings on
the augmented eight-site set.  If their physical symmetric difference is a
single `C4`, their two other edges have the same decorations, **and the
opposite determinant orientation contains the switched `C4` pairing with
that same decorated tail**, the two signed products factor as

\[
                 C\,(x_{ab}x_{cd}-x_{ac}x_{bd}).       \tag{2}
\]

This is the literal common-cofactor alternating-cycle carrier.  Separately,
when one of the displayed cells is a typed off-diagonal reference cell, the
unary target rows give the ordinary source identity

\[
 p_uG_{\rm mixed}-q_uG_{\rm pure}
 =q_u+(p_uq_s-q_up_s)C_s.                              \tag{3}
\]

Thus `q_u!=0` forces the literal active product

\[
                         (p_uq_s-q_up_s)C_s\ne0.        \tag{4}
\]

This is the requested physical promotion of the first minor on the complete
typed `C4` branch.  It is not an abstract determinant implication: (3) uses
the constant `-1` in the genuine pure target coefficient and has the exact
common hafnian cofactor `C_s`.  The cross-orientation hypothesis above is
essential; a lone physical `C4` pair does not assert that the second signed
determinant product has the same decorated tail.

Checker:
`computations/verify_uniform_axis_k3_minor_common_tail_boundary.py`.

## Complete first topology split

There are `105` perfect matchings on the augmented eight sites and `5,460`
unordered distinct pairs.  Their alternating-component types are exactly

```text
single C4       630
single C6      1680
single C8      2520
C4 + C4         630
```

The single-`C4` pairs are precisely the physical common-tail pairs: they
share two edges.  The other `4,830` pairs do not have a four-site common
tail on which (2) can be read without another matching exchange.  Even in
the single-`C4` class, the ternary label split has six off-diagonal
pure/mixed types and three coordinate-diagonal types.  The former enter
(2); the latter remain a diagonal cycle web.

Accordingly the first exact obstruction after selecting a nonzero product
in the common-`q` expansion is now only

1. **unequal tails:** a `C6`, `C8`, two independent `C4` components, or a
   single physical `C4` whose opposite determinant orientation does not
   retain the same decorated tail; or
2. **diagonal cycle web:** a single physical `C4` whose labels do not give
   an off-diagonal private-site comparison.

The unequal-tail alternative is the point where the selected hole incidence
must be fed to the already proved star/triangle/`K2,2` Hall classification,
or shortened by a source-valid matching switch.  The diagonal alternative
is the primitive lock-web branch; its first carrier topology is already
empty by the unary source unit and coefficient-torus theorem, but arbitrary
larger diagonal webs are not reduced to that primitive chart.

## Scope

This is a positive source route for every complete typed single-`C4` pair of
opposite determinant orientations.  It does **not** claim that an arbitrary
minor has such a pair: coefficient cancellation may leave only unequal
matching tails, the cross orientation may change the decorated tail, and
coordinate-diagonal tails do not enter the off-diagonal private-site
identity.  It therefore does not close the global affine-accessibility gate
or construct a full-row counterexample.

Run

```text
python3 computations/verify_uniform_axis_k3_minor_common_tail_boundary.py
python3 -O computations/verify_uniform_axis_k3_minor_common_tail_boundary.py
python3 -I -S computations/verify_uniform_axis_k3_minor_common_tail_boundary.py
```

Frozen ledger SHA-256:

```text
b946af6d2769f985fe04926039399e61f3a692f12fc923824df0b4f2c9ef2cb9
```
