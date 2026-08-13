# Complete rows do not manufacture the Gate-II pointed scalar

## Exact `h=3` answer

The three normalized pure targets and all complete five-tensor coefficient
rows do **not** by themselves force

\[
                         [H]=[P_f]
\]

and do not construct the missing fan-grade source comparison `Phi`.

In the direct-free part of the physical response coefficient

```text
head/word 11:110000
```

there are exactly

\[
                    6\cdot5\cdot3=90
\]

labelled `p*s*q*q` occurrences.  On their occurrence-expanded module
`Q^90`, the restriction of the complete inventory

```text
729 unary rows + 4*729 response rows = 3645 rows
```

has rank one.  The selected response row is

\[
                         \epsilon=(1,\ldots,1),       \tag{1}
\]

and every other output-labelled coefficient row restricts to zero.  The
normalized pure-target constants have zero differential on this mixed
response idempotent, and the fifteen direct `D*q^[3]` terms have no column
in the direct-free occurrence block.

For distinct occurrences `f,g`, put

\[
              \xi=e_f-e_g,\qquad P_f=e_f^*.
\]

Then

\[
              \epsilon(\xi)=0,\qquad P_f(\xi)=1,     \tag{2}
\]

so adjoining `P_f` raises the restriction rank from one to two.  Thus no
same-grade linear combination of the complete coefficient rows is the
pointed scalar.

Checker:
[`verify_h3_gate_ii_complete_rows_pointed_scalar_boundary.py`](../computations/verify_h3_gate_ii_complete_rows_pointed_scalar_boundary.py).

## Why `q=M-a` does not fix this

The formal projection

\[
            \Phi_{\rm occ}(v)=v-(e_f-e_g)P_f(v)      \tag{3}
\]

fixes (1) and kills `P_f`.  If `M` and `a` are aggregate-symmetric on this
two-occurrence quotient, then it fixes

\[
                            q=M-a                    \tag{4}
\]

literally as well.  Hence exact transport of an already typed symmetric
`q` readout does not logically imply anchor faithfulness.

Equation (3) is **not** the desired physical `Phi`.  It acts on formal
occurrence-presentation columns.  A physical comparison has to lift it
through the scalar-cell monomial Jacobian and preserve the fan word,
fine/repeated grade, common decorated `q` tail, endpoint head, protection,
ridge/`W`, `eta/sigma`, and terminal rows.  This is precisely the missing
source statement, not something supplied by the coefficient equations.

## The two-occurrence guard is not a full-source counterexample

The strongest complete-row result cuts the other way.  For the literal
special two-occurrence active-coloop packet, the three mixed unary rows have
`2744` simultaneous mate choices.  Only `148` initially remain in a closed
Hall shore.  Completing their three private response rows gives

```text
148 * 2 * 8 * 2 = 4736
```

labelled response seeds, and exactly zero remain trapped.

Therefore (2)--(3) are a sharp **no-implication guard**, not a complete GHZ
source point or a counterexample to Gate II.  The complete rows eliminate
the smallest special packet by strict Hall growth; they do not turn the
selected occurrence covector into a source chain.

This also prevents an overclaim in the opposite direction: the complete-row
census does not close an arbitrary active-fan coloop.  The special packet
has a one-term residual cofactor, whereas an arbitrary normalized coloop can
have several cancelling residual matching terms.  Relabelling and torus
scaling do not reduce that support.

## First additional row/cell

On the two occurrence columns `(f,g)`, any additional physical row
`r=(r_f,r_g)` has transverse Fitting minor

\[
 \det\begin{pmatrix}1&1\\r_f&r_g\end{pmatrix}
                         =r_g-r_f.                   \tag{5}
\]

Thus the exact zeroth-order exit is an occurrence-asymmetric physical row;
on a localized coloop chart, a unit `r_g-r_f` supplies the pointed
direction.  Chain-theoretically, the first new object is an
occurrence-labelled relative principal-parts/Spencer (equivalently suitable
Tate) cell whose boundary lifts `e_f-e_g` through the scalar monomial
Jacobian in the required fan grade.

If such a first-order lift exists, the next exact obstruction is not another
aggregate row but

\[
              o_2=[F_{[2]}(\xi)]\in\operatorname{coker}(J_xF), \tag{6}
\]

followed by the augmented anchor, literal `q=M-a`, ridge/`W`, `eta/sigma`,
and terminal compatibility.  If (6) survives as a physically typed dual,
it must be promoted by the existing generator/separator alternative; it
cannot be called terminal merely because it is nonzero in an occurrence
presentation.

The shortest honest Gate-II theorem is therefore:

> On every arbitrary trapped active-fan coloop packet, construct one
> occurrence-asymmetric scalar-source PP comparison with unit minor (5),
> kill or terminalize its Hasse obstruction (6), and extend the literal
> augmented row `q=M-a`.  The already committed Gate-II assembly then closes
> all downstream branches.

## Scope

This result is exact at canonical `h=3` for the selected `11:110000`
direct-free occurrence grade and for the pinned complete-row census of the
special packet.  It does not assert an all-order trapped-coloop theorem.
For general `h`, a coefficient with at least two terms still has an
aggregate-versus-pointed incidence quotient, but the all-`h` physical lift,
completion census, and literal `q=M-a` comparison remain separate theorems.

Run:

```text
python3 computations/verify_h3_gate_ii_complete_rows_pointed_scalar_boundary.py
python3 -O computations/verify_h3_gate_ii_complete_rows_pointed_scalar_boundary.py
python3 -I -S computations/verify_h3_gate_ii_complete_rows_pointed_scalar_boundary.py
```

Frozen ledger SHA-256:

```text
e1582198c5c22571f9df873b419dd8e92afbd61dc04eddde07292f7cc61b23c4
```
