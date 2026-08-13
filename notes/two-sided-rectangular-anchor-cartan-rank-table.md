# The beautiful interference table has two visibility bits

## Result

Let `M:X->Y` be the complete protected interference map, `h in X*` the
physical pure/target row, `g in Y` the physical Cartan column, and `alpha`
the corner coefficient.  Put

\[
                    A=\begin{pmatrix}M&g\\h&\alpha\end{pmatrix}. \tag{1}
\]

There are two independent visibility questions:

\[
 a=[h|_{\ker M}\ne0],\qquad
 b=[[g]\ne0\text{ in }\operatorname {coker}M].        \tag{2}
\]

The complete rank table is

\[
\begin{array}{c|cc}
 &b=0&b=1\\\hline
a=0&\operatorname {rank}M+[\beta\ne0]
   &\operatorname {rank}M+1\\
a=1&\operatorname {rank}M+1
   &\operatorname {rank}M+2,
\end{array}                                             \tag{3}
\]

where in the double-dark corner one may write `g=My` and `h=lambda M`, and

\[
                \beta=\alpha-h(y)=\alpha-\lambda(g).  \tag{4}
\]

Checker:
[`verify_two_sided_rectangular_anchor_cartan_rank_table.py`](../computations/verify_two_sided_rectangular_anchor_cartan_rank_table.py).

## Proof

Appending `h` raises row rank exactly when `a=1`; appending `g` raises
column rank exactly when `b=1`.  When both are visible, their quotient
classes live on opposite sides and give two independent rank jumps.  When
only one is visible, there is only one jump.

If both are dark, row and column operations replace (1) by the direct sum of
`M` and the scalar (4).  This proves the upper-left entry of (3).

The checker exhausts all `19,683` two-by-two packets over `{-1,0,1}` and
freezes rectangular and triangular guards.

## Why a bare column alternative does not close the proof

For `M=0`, `h=0`, `g=1`, and `alpha=0`, the Cartan column is outside the
image and a left separator detects it.  But the rank rises only once.  The
separator merely says that the newly adjoined column is independent; it
does not isolate an old nonzero optical monomial or the normalized target
constant.  It is therefore not automatically a source unit.

The same issue occurs in the literal pure triangular block: adjoining the
pure/target row or an uncoupled target column can raise rank once while the
old mixed block remains singular.  The load-bearing source unit is the
bottom-right entry of (3), where the physical anchor sees an old kernel mode
and the physical Cartan column sees an old cokernel mode simultaneously.

Thus the shortest entry theorem really needs both:

1. a complete source kernel which is visible to the physical pure/target
   row; and
2. a complete Cartan column nonzero in the corresponding source cokernel.

The first is the marked-lift/anchor-pairing problem.  The second is the
placed Cartan/Fitting or typed-exit problem.  Once both hold, no square or
cycle classification remains.

## Scope

Equation (3) is exact over the localized characteristic-zero field.  A
rank-two jump becomes a physical source unit only after the displayed minor
is source-provenant in one complete augmented grade.  A one-rank separator
can still be useful if independently identified with the physical terminal,
an evaluated Fitting carrier, or a normalized target pivot; the rank table
does not supply that typing.

## Verification

```text
python3 computations/verify_two_sided_rectangular_anchor_cartan_rank_table.py
python3 -O computations/verify_two_sided_rectangular_anchor_cartan_rank_table.py
python3 -I -S computations/verify_two_sided_rectangular_anchor_cartan_rank_table.py
```

Frozen ledger SHA-256:

```text
27545ee1fac34b93d3e43b2c8d20828515254aaa7b43c4b71b382f19560735a2
```
