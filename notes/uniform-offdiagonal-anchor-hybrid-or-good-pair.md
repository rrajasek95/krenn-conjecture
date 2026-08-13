# Every off-diagonal cell gives a good pair or opens a matching exchange

## Result

Choose one nonzero pure perfect-matching monomial `Q_0,Q_1,Q_2` from the
three target coefficients of an exact ternary source.  Let

\[
                         e=A_{uv}(a,b)\ne0,
                         \qquad a\ne b.                 \tag{1}
\]

Then exactly one of two source-valid entries is available.

1. **Nonanchor pair.**  If the physical pair `uv` is absent from
   `Q_0 union Q_1 union Q_2`, deleting `uv` retains the three pure coordinate
   heads at both endpoints.  Both deleted stars have rank three, and the
   target-augmented private-site identity supplies a nonzero active
   determinant/cofactor product.
2. **Anchor hybrid.**  If `uv` belongs to `Q_i`, retain the off-diagonal
   cell (1) on that edge and the three pure-`i` cells on the other edges of
   `Q_i`.  This is a nonzero perfect-matching monomial in a mixed output
   word.  Exactness makes that coefficient zero, so a cancellation monomial
   exists on a physical perfect matching different from `Q_i`.

The conclusion is uniform in the even order, allows asymmetric endpoint
colours and aggregated parallel sources, and requires no support-minimality
hypothesis.  It closes the first source-accessibility question for every
off-diagonal cell: such a cell is never response-dark merely because it lies
on a selected anchor pair.

Checker:
[`verify_uniform_offdiagonal_anchor_hybrid_or_good_pair.py`](../computations/verify_uniform_offdiagonal_anchor_hybrid_or_good_pair.py).

## 1. The hybrid is a literal complete-row term

For the chosen colour `i`, write

\[
                    Q_i=\{uv,e_2,\ldots,e_{N/2}\}.
\]

Its selected pure monomial proves that every factor
`A_{e_r}(i,i)` is nonzero.  Replacing only `A_uv(i,i)` by (1) gives

\[
        A_{uv}(a,b)\prod_{r=2}^{N/2}A_{e_r}(i,i)\ne0. \tag{2}
\]

The output colours at `u,v` are `a,b`, while all other sites have colour
`i`.  Since `a != b`, the word is mixed.  Its target coefficient is zero.

For a fixed physical matching and fixed output word, the decorated monomial
is unique.  Hence a second term cancelling (2) cannot use the same matching
skeleton.  The symmetric difference with `Q_i` is a nonempty union of
alternating even cycles.  This is a literal typed edge into the global
matching-component/holonomy analysis, not an abstract support possibility.

## 2. The complementary branch is already rank-good

If no `Q_i` uses `uv`, each matching contributes at `u` a surviving
coordinate column labelled by its target colour.  The three colour labels
are independent even when two matchings use the same physical neighbour.
The same holds at `v`, giving deleted-star ranks `(3,3)`.

The exact private-site identity based at (1) is

\[
             \sum_s\Delta_{us}C_s=-A_{uv}(a,b)\ne0.   \tag{3}
\]

Some literal active product in (3) is therefore nonzero.  This is precisely
the already pinned nonanchor good-pair entry.  It still needs generic
active-minor-to-clean-cap landing downstream.

## 3. Effect on the interference proof

The protected-relative frame-circuit theorem remains necessary for global
phase and potential control, but not for establishing that the selected
off-diagonal amplitude occurs in a physical source row.  The entry map is
now simply

```text
off-diagonal physical cell
   |
   +-- pair outside Q0 union Q1 union Q2 --> rank-good active route
   |
   `-- pair in Qi ------------------------> mixed hybrid row, distinct mate
```

Iterating the second branch builds a finite literal matching component.  A
private term closes it immediately; odd signed holonomy gives a source unit;
coherent even holonomy is governed by the Schur anchor/Cartan amplitudes.
Thus the remaining source-exhaustivity problem is no longer occurrence of
the selected cell.  It is the treatment of contamination in the complete
row and the component-exact even potential.

This also supersedes a triangle-specific alternating-path argument: if a
selected anchor uses the carrier pair, the one-edge hybrid (2) is already
the required mixed occurrence, independently of the unused tail topology.

## Scope

The forced mate may remain inside the selected anchor web, have zero even
Fitting holonomy, or fail transverse rank.  The nonanchor branch supplies a
good active minor, not automatically an active clean cap.  The theorem does
not close same-head `(2,2,3,3)` landing, complete-row contamination, or the
component-potential/deletion implication.

Run:

```text
python3 computations/verify_uniform_offdiagonal_anchor_hybrid_or_good_pair.py
python3 -O computations/verify_uniform_offdiagonal_anchor_hybrid_or_good_pair.py
python3 -I -S computations/verify_uniform_offdiagonal_anchor_hybrid_or_good_pair.py
```

Frozen ledger SHA-256:

```text
2e06fd3c3232a210b422fed25aba0968fb5a5934af259e91415a26f39d0c1fea
```
