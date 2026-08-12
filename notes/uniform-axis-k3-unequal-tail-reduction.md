# Unequal k=3 tails reduce to one chord-or-Hall lemma

## Theorem

Fix one literal output word `w`.  Let `M,N` be two nonzero decorated perfect
matching monomials in the same physical coefficient row.  Their symmetric
difference is a disjoint union of even alternating cycles.

1. If there is more than one component, switch any proper collection of
   whole components.  The intermediate matching uses only decorated cells
   already present in `M` or `N`, so its monomial is nonzero and belongs to
   the same word `w`.  Repeating reduces to one alternating component.
2. Suppose the remaining component is
   `C_(2r)`, `r>=3`, with

   ```text
   M = 01 | 23 | 45 | ...,
   N = 12 | 34 | 56 | ... | (2r-1)0.
   ```

   If the one decorated chord `03` is nonzero, put

   ```text
   K = 03 | 12 | 45 | 67 | ... .
   ```

   Then `M△K` is one `C4`, while `K△N` is one `C_(2r-2)`.  Only `03` is a
   new cell; `12` already belongs to `N`.  Induction reduces the unequal tail
   to the typed common-tail theorem in `f6ce8cc`.

All switches preserve the literal word, so this is source-valid matching
exchange rather than a formal change of cofactor variables.  If the chord
endpoints carry different colours, the chord is a typed off-diagonal cell
and the target-augmented private-site identity already forces an active
determinant/cofactor carrier.  If they carry the same colour, the shortening
remains in the coordinate-diagonal cycle web.

The checker is
`computations/verify_uniform_axis_k3_unequal_tail_reduction.py`.

## Precise hypotheses for the active landing

The nonzero quotient minor of the minimum `k=3` circuit gives an active
source route under the following exact hypotheses.

1. **Word synchronization.**  One signed determinant orientation and its
   cross orientation contain nonzero matching terms which can be compared
   inside one literal output word, with all common decorations retained.
2. **Exchange accessibility.**  After whole-component switching, every
   single `C_(2r)` with `r>=3` has a nonzero distance-three shortening chord,
   until a single `C4` is reached.
3. **Typed terminal.**  The terminal `C4` has either the common decorated
   cross orientation required by the alternating determinant, or a nonzero
   off-diagonal cell to which the unary private-site identity applies.

Under these hypotheses the minor yields a literal active carrier.  If the
corresponding physical arm is outside the selected anchor union, the existing
nonanchor theorem gives the free four-good route.  If every such carrier is
anchor-contained, its hole incidence is passed to the finite Hall normal
form rather than treated as another coefficient face.

## The exact missing lemma

The remaining implication is now sharply isolated.

> **Word-synchronized chord-or-Hall lemma.**  In the full unary plus four
> response packet, every nonzero determinant contribution outside the
> common-tail class either admits a same-word distance-three shortening
> chord, or its two selected response-hole families are cross-intersecting.
> In the latter case they lie in a star, triangle, or four-site `K2,2`.

This lemma must use the second diagonal and both crossed companion rows.
The five aggregate tensor sums alone do not prove it: their exact `k=3`
typed row module allows independent mixed debt coordinates without any
matching-tail synchronization.  Nor can a component switch repair terms in
different output words, because changing decorations would cease to be a
source-labelled operation.

There are therefore only two honest residuals:

- a chordless, word-synchronized alternating `C6/C8`; or
- an unsynchronized determinant pair whose cross orientation changes the
  decorated tail.

If every potential chord in the first residual is coordinate-diagonal, it
is precisely the diagonal lock web.  The primitive three-column diagonal
web is already source-unit, but reducing arbitrary larger diagonal webs to
that chart remains separate.

## Verification

The checker verifies the component switch and the one-chord formula for
`C6,C8,...,C20`; the displayed formulas prove every even length.

```text
python3 computations/verify_uniform_axis_k3_unequal_tail_reduction.py
python3 -O computations/verify_uniform_axis_k3_unequal_tail_reduction.py
python3 -I -S computations/verify_uniform_axis_k3_unequal_tail_reduction.py
```

Frozen ledger SHA-256:

```text
65431ee6c2d09f4dee90effa31be774bd8214b35affb4d5690049702b1379ced
```
