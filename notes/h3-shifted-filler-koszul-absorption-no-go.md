# The physical Koszul cell cannot absorb the shifted filler's Eq defect

## Result

The monic commutator left by `91041f7` is not removable by the existing
physical Koszul cell, even after allowing an arbitrary polynomial multiple
or passing formally to its mapping cone.

Work over

\[
R=\mathbb Q[u,H_0,H_m],\qquad F_0=H_0-u
\]

with the underived physical differential

\[
dr_0=F_0e_{\rm Eq},\qquad dr_m=H_me_{\rm Eq},
\qquad dT=-Yw.                                           \tag{1}
\]

The physical degree-four Koszul cell is

\[
K_m=H_mr_0-F_0r_m.                                      \tag{2}
\]

Commutativity gives `dK_m=0`.  Therefore, for every polynomial
`c in R`,

\[
\boxed{d\big((r_0-T)+cK_m\big)=Yw+F_0e_{\rm Eq}.}       \tag{3}
\]

Thus adjoining a mapping-cone cell for `K_m`, or merely changing the
representative by a multiple of it, cannot alter the Eq component.  The
first underived residual remains exactly the one found by `91041f7`.

Checker:
`computations/verify_h3_shifted_filler_koszul_absorption_no_go.py`.

## General polynomial correction also fails

Allow the more general correction `b r_m`, with arbitrary `b in R`.
Its Eq boundary is `bH_m e_Eq`, so cancellation of (3) requires

\[
                         bH_m=-F_0=u-H_0.                \tag{4}
\]

Equation (4) has no polynomial solution.  Indeed, specialize
`H_m=H_0=0`.  Its left side becomes zero and its right side becomes the
independent monic variable `u`.  Equivalently,

\[
                  F_0\notin (H_m)\subset R.             \tag{5}
\]

This is stronger than failure of one guessed coefficient.  No polynomial
combination of the existing `r_m` route can cancel `F_0e_Eq` without
localizing `H_m` or imposing a new source relation that makes (5) false.

## Exact remaining input

At the `q=0` top, `H_0=H_m=0`, so the residual is the primitive class

\[
                         -u e_{\rm Eq}.                  \tag{6}
\]

A successful physical descent therefore needs a genuinely new
target/residue-zero lower face whose Eq boundary has unit coefficient, or a
separate source-valid localization/divisibility theorem.  The closed cell
`K_m` itself supplies neither.  This pins the earliest obstruction before
any curvature or cap normalization.

## Scope

- The statement is in the underived polynomial source.  It does not forbid
  a new Hasse lower face or an explicitly justified localization.
- Treating `K_m` as a mapping-cone generator does not help unless the cone
  differential introduces a new physical Eq boundary; declaring such a
  boundary would be exactly the missing generator, not absorption by the
  old closed Koszul relation.
- The five-face rank obstruction in `c32f529` is pinned independently; the
  present no-go concerns the single monic Eq coefficient already after the
  derived filler has cancelled all indexed Hasse faces.

## Verification

```text
python3 computations/verify_h3_shifted_filler_koszul_absorption_no_go.py
python3 -O computations/verify_h3_shifted_filler_koszul_absorption_no_go.py
python3 -I -S computations/verify_h3_shifted_filler_koszul_absorption_no_go.py
```

Frozen ledger SHA-256:

```text
9b63dd33425b1086103ee324a8dd5fa41ee7a219fc9b43b406342c8581155dc7
```
