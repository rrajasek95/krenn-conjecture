# The `15=1+9+5` interference pattern separates `C4` from `C6`

## Result

At six sites, tangent Euler/Hasse cubes give the exact matching-module
decomposition

\[
 \mathbb Q[\mathcal M_6]
       =\mathbf 1\oplus C_{\rm cut}^{0}\oplus D_{\rm alt},
                   \qquad 15=1+9+5.                  \tag{1}
\]

The five-dimensional quotient is spanned by the ten alternating `K3,3`
cut determinants.  Classifying all `105` unordered matching pairs gives an
unexpectedly rigid split.

* Every one of the `45` common-edge/`C4` pairs occurs with **opposite signs**
  in exactly two alternating determinants.  Four other determinants contain
  exactly one term and four contain neither.
* Every one of the `60` edge-disjoint/`C6` pairs occurs together in exactly
  one determinant, but with the **same sign**.  Six determinants contain
  exactly one term and three contain neither.  No determinant contains the
  pair with opposite signs.

Checker:
[`verify_h3_common_tail_pair_cut_determinant_split.py`](../computations/verify_h3_common_tail_pair_cut_determinant_split.py).

## Meaning for the source proof

For a common-tail `C4`, the alternating determinant is precisely the two
opposite matching orientations required by the pinned physical
common-tail/Fitting identity.  Hence the five-dimensional tangent-Euler debt
does not create a new kind of `C4` obstruction:

```text
evaluated determinant nonzero -> typed C4/Fitting carrier;
all determinants zero         -> centered tangent-Hasse sector.
```

The second line is still filtered rather than degree-zero: its physical
Hasse cube has a lower repeated-site collision face.  That face must be
landed by the Cartan--Spencer comparison before it becomes the marked kernel
lift of the complete source presentation.

For a `C6`, the absence of an opposite-sign determinant is exactly the old
first-transgression obstruction.  The two selected matchings cannot be the
two orientations of one common-tail determinant.  One needs a same-word
distance-three chord, an endpoint word-change column, or a Hall/lock bridge.
This is structural, not an artifact of incomplete case enumeration.

## Proof

Fix a `3|3` cut.  A perfect matching contributes to its determinant exactly
when every edge crosses the cut; its sign is the parity of the induced
bijection.  Enumerating the ten unoriented cuts and the fifteen matchings
gives the signatures

\[
\begin{array}{c|rrrr|r}
 &\text{opposite}&\text{same}&\text{one term}&\text{neither}&\text{pairs}\\\hline
C_4&2&0&4&4&45\\
C_6&0&1&6&3&60.
\end{array}                                             \tag{2}
\]

The checker proves (2) exactly.  It also verifies that every pair difference
is seen by some determinant, so no bare two-occurrence difference lies in
the nine-dimensional tangent cut sector.

For a full physical matching-value vector `v`, however, all determinants
may cancel after including the other thirteen matchings.  The tangent-Euler
theorem then gives `v in C_cut^0` whenever the source row also has zero total
sum.  This is the precise positive filtered lift, and explains why complete
source rows—not isolated pairs—are load-bearing.

## Scope

This is a theorem about the six-site matching representation.  A formal
determinant which detects a pair need not evaluate nonzero at the physical
source.  Even an evaluated nonzero determinant still needs decorated minor,
head, support, and cofactor typing to land at four-good rank.  The theorem
does not close the lower Hasse collision face or the `C6` chord/Hall branch.

## Verification

```text
python3 computations/verify_h3_common_tail_pair_cut_determinant_split.py
python3 -O computations/verify_h3_common_tail_pair_cut_determinant_split.py
python3 -I -S computations/verify_h3_common_tail_pair_cut_determinant_split.py
```

Frozen ledger SHA-256:

```text
08aabf4f37dbe1117e0bdc8fa3b203546afabc869beefa490ff267e57c74121a
```
