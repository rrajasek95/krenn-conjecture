# Target normalization turns the (abcde) gate into a generator dichotomy

## A clean lower lift already exists

In the common degree-(abcde) source grade, use the row order

\[
 (\operatorname{low},\operatorname{ainc},W,
    \operatorname{tgt},\operatorname{ores}).
\]

The pure unary multiplier and the old cap/residue columns are

\[
\begin{aligned}
 R&=(1,-1,0,1,0),\\
 T&=(0,0,-Y,1,0),\\
 \rho&=(0,0,1,0,1),\\
 d_{\rm ores}&=(0,0,0,0,1).
\end{aligned}
\]

With all four columns multiplied into the same source grade,

\[
       \boxed{x=R-T-Y\rho+Yd_{\rm ores}
                    =(1,-1,0,0,0).}                   \tag{1}
\]

Thus target normalization does not construct the zero-anchor augmentation
(U=(1,0,0,0,0)), but it does construct a physically clean lower lift
whose only wrong readout is anchor incidence (-1).  The checker verifies
(1) at four nonzero values of (Y).  Localization of (Y) or (abcde)
does not change the signs or source grade.

## Exact use of the `0373033` alternative

Let (J_0) retain lower boundary, (W), target, and ordinary residue in
this fixed fine grade, and let (q) be **physical** anchor incidence.
Every other clean lift is (x+k), with (k\in\ker J_0).

Over characteristic zero,

\[
 \boxed{ U\text{ exists}
    \quad\Longleftrightarrow\quad q(\ker J_0)\ne0. }  \tag{2}
\]

Indeed, if (q(k)\ne0), then

\[
 -{k\over q(k)}
\]

is already the primitive relative anchor generator of `0373033`, while
(x+k/q(k)) is (U).  Conversely, (U-x\in\ker J_0) has anchor value
one.  Therefore explicit construction of (U) is never a separate
proof-completing obligation: its existence is equivalent to the positive
indeterminacy/generator branch.

## A physical cyclic package would finish immediately

Let (A) denote a **physically typed correction chain** realizing the
cyclic comparison package, with

\[
                         J_0(A)=(5,0,0,0),qquad q(A)=0. \tag{3}
\]

Then (1) gives

\[
                         A-5x\in\ker J_0,qquad
                         q(A-5x)=5.                    \tag{4}
\]

Consequently

\[
                         -{A-5x\over5}                 \tag{5}
\]

is the primitive relative anchor generator.  Thus once (A) is physical,
one does not need to attach a separate zero-anchor (U) or a higher cell
bounding (A-5U); target normalization plus `0373033` closes the positive
branch directly.  Equivalently, over the characteristic-zero coefficient
field, (A/5) itself has the complete (U)-signature.  The kernel expression
(4) records at the same time why this is the positive-indeterminacy branch,
rather than an independent relative attachment.

The hypothesis in (3) is load-bearing.  The current weighted expression
(aceC_1+\cdots+acdC_4) is only a formal comparison package: its five
comparison vertices have not been promoted to one source-labelled physical
correction chain.  Calling that formal expression (A) would assume the
same endpoint/rootless comparison being sought.

## The zero-indeterminate branch is not yet Fredholm

If (q(\ker J_0)=0), every clean lower lift has anchor value (-1), so
(U) is impossible.  Equation (4) also shows that no physical (A) with
(3) can exist on this branch.  The descended (q) is a separator on the
lower-lift fibre, but it is not automatically the rootless Macaulay
annihilator: the physical five-polar/comparison map and its (W), pentagon,
and terminal grading have still not been constructed.  Hence Fredholm
cannot be invoked merely from this fibrewise separator.

## Scope

This is an exact conditional reduction using the complete old cap/residue
readouts and the typed indeterminacy-or-generator theorem.  It eliminates
explicit (U) as an independent goal.  The remaining construction is the
same source-valid physical cyclic comparison (A) (or one comparison
vertex from which it propagates); formal chart anchor values do not satisfy
the hypothesis.

Run:

```text
python3 computations/verify_h3_rootless_abcde_target_normalization_generator_dichotomy.py
python3 -O computations/verify_h3_rootless_abcde_target_normalization_generator_dichotomy.py
python3 -I -S computations/verify_h3_rootless_abcde_target_normalization_generator_dichotomy.py
```

Frozen ledger SHA-256:

```text
dbe3f110b5d7667d68f17cb5ea422efa6d9e45b8bf13062bc6ffc4bd36524c64
```
