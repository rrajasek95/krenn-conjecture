# The six-term physical alternative is stable under every relative extension

## Theorem

Fix one common physical repeated grade.  Let

\[
 J_0:L_{\rm rel}\longrightarrow E_0
\]

be the **complete** protected map on the canonical relative source complex:
literal boundary, `W`, target, ordinary residue, and every other row required
to vanish on a relative anchor.  Let

\[
 q:L_{\rm rel}\longrightarrow k
\]

be the physically typed six-term readout

\[
 q=\sum_{i=1}^{6}m_i-\operatorname {ainc}
\]

from the first-flat theorem.  Then exactly one of the following holds.

1. There is `x in ker J_0` with `q(x)!=0`.  Dividing by `q(x)` gives a
   protected-zero relative anchor with physical anchor value one.
2. The readout kills `ker J_0`.  Therefore it factors through `J_0`:

   \[
                         q=\lambda J_0.
   \]

   The row `(-lambda,1)` annihilates the complete augmented map
   `(J_0,q)`.  It is the physical left-separator branch.

This is elementary row-space duality, but its consequence is substantial:
**arbitrary future relative generators do not need a separate census.**
Adding every normalized-bar, principal-parts, Cartan, or mapping-cone cell
merely enlarges the column set of the same dichotomy.  A new cell with
nonzero readout is useful—it is the relative generator.  If no such cell
exists, the corrected six-term covector is automatically the separator of
the entire enlarged image.

## Cyclic assembly

The five facewise readouts kill the oriented `C5` edge lattice

\[
 e_3-e_1, e_5-e_3, e_2-e_5, e_4-e_2, e_1-e_4,
\]

which has saturated rank four.  Their sum pairs to `5` with the only
primitive aggregate `(1,1,1,1,1)`.  Hence the same alternative survives
cyclic propagation: a nonzero aggregate relative class normalizes after
division by five, while the zero branch is the summed physical separator.

## What remains genuinely open

The theorem does not manufacture the physical map.  The protected rows and
six-term/pentagon readout must still be defined in one common labelled
repeated grade on the canonical exhaustive relative complex.  That is the
physical Cartan/order-six comparison problem.  Once that typing exists,
however, neither relative-cell enumeration nor a separate
zero-indeterminacy proof remains.

This is stronger than checking the currently known relative cells one by
one and sharper than assuming they all vanish: both possible ranks advance
the proof.

Verification:

```text
python3 computations/verify_h3_six_term_exhaustive_relative_extension_alternative.py
python3 -O computations/verify_h3_six_term_exhaustive_relative_extension_alternative.py
python3 -I -S computations/verify_h3_six_term_exhaustive_relative_extension_alternative.py
```

Frozen ledger SHA-256:

```text
7efd330f4d1b4bf4d7d6fc60e71c33df798896eb11c556b1122dc990636fd579
```
