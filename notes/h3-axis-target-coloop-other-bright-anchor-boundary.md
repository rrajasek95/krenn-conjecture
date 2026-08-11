# The other bright anchor does not repair the target-coloop carrier

## Result

Let `M` be the selected pure matching of target colour `t`, let `K` be the
forced unary/direct matching, and let `L` be the mandatory pure matching in
the other bright colour `m`.  Suppose an arm of `M` is a physical
target-family coloop.

Deleting that arm removes the selected colour-`t` matching column at both
of its endpoints.  The two remaining mandatory anchors contribute only
coordinate rows `0` and `m`.  Consequently their selected-anchor
deleted-star ranks are exactly

\[
                              (2,2),                    \tag{1}
\]

not `(3,3)`.  The other-bright matching cannot supply the missing target
row `t`, so it does not upgrade the common-covector carrier of `2ad730f` to
a four-good pair or a distinct-head curved overlap.

Checker:
[`verify_h3_axis_target_coloop_other_bright_anchor_boundary.py`](../computations/verify_h3_axis_target_coloop_other_bright_anchor_boundary.py).

## The pure other-bright word is not a forced common covector

The label obstruction is equally direct.  The diagonal matching `L` lies
in row `(m,m)`.  A crossed response row is `(m,t)` or `(t,m)`, so its full
matching differs from `L` at exactly one outer endpoint head.  Hence the
nonzero literal monomial of `L` does not occur in the crossed tensor.

The checker freezes a common-source support on sites
`0,1,2,3,4,5,P,S`:

```text
K = PS | 01 | 23 | 45       on 0^8,
L = P4 | S5 | 01 | 23       on 1^8,
M = P0 | S1 | 23 | 45       on 2^8,
N = P2 | S3 | 01 | 45       on mixed word 22122212,
M companion                 on the same mixed word.
```

Here `M triangle N` is a single `C6`.  Every `s_2` component in the literal
support has tail colour `2`.  Therefore the crossed tensor `p_1s_2q^[2]`
has no term on the decomposable residual word `1^6`, although `L` is a
nonzero diagonal pure-`1` matching.  The transposed orientation has the
same one-head mismatch.

This is a source-labelled support boundary, not a formal independent
cofactor packet.  It is deliberately not claimed to satisfy every full
GHZ coefficient equation.  It proves that the existence of `L` and common
`q` support alone does not normalize the covector from `2ad730f` to a pure
coordinate word.

## Smallest remaining physical input

The mandatory anchors do not close the bistar/Fitting residual.  One of two
genuinely new pieces of source provenance is required:

1. an alternate pure matching in the selected target colour, avoiding the
   coloop arm; or
2. a literal crossed response base carrying the mismatched endpoint head.

The first breaks coloopness and restores rank three directly.  The second
opens the response/Hall web and can be tested by the existing complete-row
routing.  Neither follows from the unary and other-bright anchors alone.

## Verification

Run

```text
python3 computations/verify_h3_axis_target_coloop_other_bright_anchor_boundary.py
python3 -O computations/verify_h3_axis_target_coloop_other_bright_anchor_boundary.py
python3 -I -S computations/verify_h3_axis_target_coloop_other_bright_anchor_boundary.py
```

Frozen ledger SHA-256:

```text
26b700e22938d7f48a633636339b982e1c61a2b06e4c61f46da3b291e58287e6
```
