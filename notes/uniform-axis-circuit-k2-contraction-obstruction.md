# A minimum axis circuit does not contract coefficientwise to two columns

## Result

The proved `k=2` clean closure does not extend to `k>=3` by deleting the
other occupied star components while keeping the common cofactor data fixed.
This failure is exact linear algebra, not a missing support case.

Let the occupied complete response columns be

\[
                         C_1,\ldots,C_k
\]

and let minimum support give their linear independence.  The target row is

\[
                         T=\sum_{i=1}^k\lambda_i C_i,
                         \qquad \lambda_i\ne0.             \tag{1}
\]

Because the columns are independent, `(1)` is the unique expression of
`T`.  For any selected self-square pair `u,v`, and any omitted index
`w`, the dual coordinate `ell_w` satisfies

\[
 \ell_w(C_u)=\ell_w(C_v)=0,
 \qquad \ell_w(T)=\lambda_w\ne0.                           \tag{2}
\]

Therefore

\[
                         T\notin\langle C_u,C_v\rangle.     \tag{3}
\]

The image of `T` in the pair quotient has `k-2` nonzero coordinate
residues.  A nonzero self-square `lambda_u lambda_v` merely selects the
pair; it does not remove any of those residues.

The exact checker is
`computations/verify_uniform_axis_circuit_k2_contraction_obstruction.py`.

## Relation to the unique quotient circuit

Modulo the target line, the `k` column images have rank `k-1` and the unique
relation

\[
                         \sum_i\lambda_i\overline C_i=0.
\]

Every coefficient is nonzero.  This is precisely why the quotient circuit
cannot be restricted to the chosen pair: a two-term relation landing on the
target line would lift to a second relation among the independent `C_i`.
For `k>=3` that is impossible.

The checker audits the all-ones normal form at every `k=3,...,10` and all
164 selected pairs.  This is representative of the general theorem after
rescaling the independent columns by the nonzero `lambda_i`; the displayed
basis proof applies at arbitrary `k`.

## Why the current source rows do not supply the contraction

The common Hessian recurrence constructs the physical cofactor content of
each fixed column `C_i`.  At one source point it does not provide a
deformation `delta C_i`.  Likewise, the unary private-site identity

\[
                  \sum_s\Delta_{us}K_s=-q_u
\]

routes a nonzero off-diagonal cell to an active minor, but it does not change
the unique coefficients in `(1)`.

Consequently a coefficient-only specialization

```text
lambda_w -> 0 for w outside {u,v}
```

cannot preserve the target tensor.  The primitive separator `(2)` detects
the lost coefficient immediately.

The first possible positive operation must instead deform the columns
themselves: it must vary the common `q` or the opposite endpoint stars so
that the resulting `delta C_i` transfer all `k-2` omitted target residues
into the retained pair, while preserving every source response row and all
localized units.  No such source-labelled operation is supplied by the
Hessian or private-site identities currently in the packet.

## Scope

This is a sharp obstruction to the proposed direct induction, not a physical
one-bad source or a counterexample to a more general contraction that changes
the common cofactor data.  It performs no `k=3` support enumeration.  The
proved all-five `k=2` closure remains valid; reaching it from `k>=3` requires
the named simultaneous column-deformation theorem.

## Verification

Run

```text
python3 computations/verify_uniform_axis_circuit_k2_contraction_obstruction.py
python3 -O computations/verify_uniform_axis_circuit_k2_contraction_obstruction.py
python3 -I -S computations/verify_uniform_axis_circuit_k2_contraction_obstruction.py
```

The frozen ledger digest is

```text
a3ad54e1ddc2a88c092e73757816942b5bf28de524f3d516f0d25cda2839cb06
```
