# The interference alternative is rectangular

## Result

The Schur interference argument does not intrinsically require a square
corank-one cancellation block.  Let

\[
                         M:X\longrightarrow Y
\]

be the **complete protected** source-incidence map in one finite labelled
packet.  Let `h in X*` be the distinguished pure-anchor row and let `g in Y`
be the whole physical Cartan column.  Assume that the anchor sees some
protected kernel circuit:

\[
                 h|_{\ker M}\ne0.                     \tag{1}
\]

For any bottom-right coefficient `alpha`, exactly one of the following holds.

1. If `[g] != 0` in `coker M`, then

   \[
   \operatorname {rank}
   \begin{pmatrix}M&g\\h&\alpha\end{pmatrix}
             =\operatorname {rank}M+2.                \tag{2}
   \]

   This is the rectangular form of the bright Schur branch.
2. If `g in im M`, there is a potential `y` with

   \[
                         My=g,\qquad h(y)=\alpha.       \tag{3}
   \]

   Consequently `(-y,1)` is a unit-coefficient kernel vector of the complete
   augmented map.

Checker:
[`verify_rectangular_interference_anchor_cartan_alternative.py`](../computations/verify_rectangular_interference_anchor_cartan_alternative.py).

## Proof

Condition (1) says that appending `h` as a row raises rank by one.  If `g` is
nonzero in the cokernel, appending it as a column also raises rank by one.
The last column of the fully augmented matrix cannot lie in the span of the
old columns, since its projection to `Y/im M` is `[g]`.  This proves (2).

Now suppose `g=My_0`.  Choose `c in ker M` with `h(c) != 0`.  Then

\[
              y=y_0+\frac{\alpha-h(y_0)}{h(c)}c       \tag{4}
\]

satisfies (3), and direct multiplication gives

\[
       \begin{pmatrix}M&g\\h&\alpha\end{pmatrix}
                    \binom{-y}{1}=0.                  \tag{5}
\]

No component projector, left-cokernel generator, square block, or
corank-one hypothesis is used.

## Consequence for the proof map

The new global dark-component theorem still gives a useful explicit
blockwise construction.  This rectangular lemma shows that even that
decomposition is optional once the actual complete source packet supplies
one kernel circuit through the marked occurrence which is visible to the
protected anchor row.

The shortest possible entry theorem is therefore:

> **Anchor-visible circuit entry.**  Every marked unwanted occurrence in a
> maximum-anchor/minimum-support source lies in a complete protected kernel
> circuit `c` with nonzero marked anchor coordinate, or the first failure is
> already a typed active/Hall exit.

If that theorem holds, apply the rectangular alternative directly:

```text
Cartan outside im(M)  -> two-rank bright minor -> source unit;
Cartan inside im(M)   -> unit kernel -> physical terminal Fredholm branch.
```

The protected-relative frame-circuit theorem is strong evidence for the
existence of `c`: every occupied unprotected optical cell lies in a primitive
signed circuit whose negative part is protected.  What remains to be proved
has **two** typings.  First lift that optical circuit to a kernel circuit of
the complete matching-occurrence incidence map while preserving its marked
domain coordinate.  Then prove that this kernel pairs nontrivially with the
physical pure/target reduction row `h`.  The auxiliary coordinate covector
`e_s^*` used to preserve a marked occurrence is not automatically the
physical row `h`; confusing them would turn the rank-two branch into an
unphysical bordered minor.

## Scope

This is exact linear algebra over the localized characteristic-zero field.
It does not construct the physical map `M`, prove the anchor-visible kernel
circuit for an arbitrary source, transport the physical terminal
`q=sum6m-ainc`, or by itself turn a nonzero rank jump into the final
four-good pair.  Those are source typing and landing statements, not missing
linear algebra.

## Verification

```text
python3 computations/verify_rectangular_interference_anchor_cartan_alternative.py
python3 -O computations/verify_rectangular_interference_anchor_cartan_alternative.py
python3 -I -S computations/verify_rectangular_interference_anchor_cartan_alternative.py
```

Frozen ledger SHA-256:

```text
fb39d34a7a7a98d11901a867bdd495cc197c5722cf257a6e5efdbfb15c0b1bd5
```
