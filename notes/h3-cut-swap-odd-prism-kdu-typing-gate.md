# The cut-swap odd prism fixes every sign; its `K d(u)` comparison still needs the shifted label map

## Exact corner calculation

Let

```text
W  = 001122,
W' = 021102,
rho = (1 4),
```

and let `w` be the signed simultaneous local `0 <-> 2` Weyl action at
sites `1,4`.  Then

```text
w W  = -W',       w W' = -W,
rho W = W',       rho W' = W.
```

If `u=u_012` is the unsigned nine-label collision packet and
`l=(rho-1)u`, direct expansion gives

\[
              (1-\rho)(w-1)u_W=l_W+l_{W'}.            \tag{1}
\]

The packet `l` has twelve nonzero coefficients on the fifteen physical
collision labels.  Its three zero coordinates are exactly the shared-label
identifications.  In particular the odd prism gives the required
anti-pair, not a sum-type corner, in both word grades.

The `rho`-transported filtered cube has the opposite orientation because
`rho(v)=-v` and `rho(l)=-l`.  Therefore the correctly oriented auxiliary is

\[
                         F_{W'}=-\rho F_W.              \tag{2}
\]

For `K=(1-rho)H_w`, equations (1)--(2) and

\[
                         dK+Kd=(1-\rho)(w-1)
\]

show that

\[
                    F_W-\rho F_W-K(u)                 \tag{3}
\]

has residual `+K d(u)`.  Reversing the global convention for `K` reverses
both displayed `K` signs; it does not change the remaining class.  Thus the
complementary word is absorbed, but only after retaining `K d(u)`.

Checker:
[`verify_h3_cut_swap_odd_prism_kdu_typing_gate.py`](../computations/verify_h3_cut_swap_odd_prism_kdu_typing_gate.py).

## Why `K d(u)=M_v` cannot yet be tested labelwise

The two sides currently live in different explicitly constructed modules.

The input checker constructs

```text
U_15 basis     = (six-site perfect matching, repeated collision edge)
direction data = 18 labels -> 15 physical labels
lower packet   = 12 nonzero coordinates
known boundary = only its occurrence-forgetful 15-matching shadow.
```

It does not construct the complete protected columns of
`J_col:U_15 -> E`.  In particular, no committed object assigns to every
collision label its physical eight-site word, shifted tail, multiplier,
and repeated `P3+K2` image.

By contrast, the normalized output theorem `271df91` constructs

```text
J(M_v) basis   = eight-site decorated seven-edge monomial features
literal support = 360
grade          = one labelled repeated P3+K2 component
augmented rows = Eq alpha, residue/protected zero, eta/sigma ridge.
```

Consequently a direct equality between `K d(u)` and `J(M_v)` is not false;
it is presently **ill-typed**.  Comparing the twelve-coordinate corner
shadow to the 360 literal features would silently insert the desired map.
The smallest missing datum is precisely a source-provenant shifted
tail/label map

\[
                 \tau:U_{15}\longrightarrow L_{h=3}                 \tag{4}
\]

which agrees on the three shared labels and carries each collision word,
repeated edge, fine grade, and tail into the complete physical correction
module.  Only after (4) is given does the equality

```text
complete protected boundary of tau(u_012) = J(M_v)
```

have a common codomain.  Constructing (4) is the input comparison `Phi`, so
using it tacitly to verify the equality would be circular.

## Parity excludes the adjacent-power companion

The unresolved `K d(u)` lies in the image of `1-rho`, hence is `rho`-odd.
The adjacent-power companion isolated by `3b8bcfc` is `rho`-even and carries
upper target `-2(w-1)Delta`.  It therefore cannot be the present residual,
even before the shifted label map is constructed.

The proposed `(D+S)/2` split has the same issue.  The formal `S` that
isolates one of the two word corners is exactly the `rho`-even corner.  A
physical `S` needs the independent target-bearing `C_plus` cell from the
adjacent-power gate.  Thus the split does not bypass either the `K d(u)`
comparison or the even-companion construction.

## Sharp frontier

All signs, collision orbits, overlap coherences, and complementary-word
absorption are now fixed.  The remaining Route-B datum is no longer an
unstructured map on fifteen labels; it is the single shifted physical label
map (4), followed by the now well-typed check against the already
constructed `M_v=-O_alpha+K` output.

This theorem neither asserts inequality with `M_v` nor promotes the
occurrence shadow to a protected source boundary.

## Verification

Run:

```text
python3 computations/verify_h3_cut_swap_odd_prism_kdu_typing_gate.py
python3 -O computations/verify_h3_cut_swap_odd_prism_kdu_typing_gate.py
python3 -I -S computations/verify_h3_cut_swap_odd_prism_kdu_typing_gate.py
```

```text
86c90e8001f6a7bb7153602183813759cdccb362040eb88567727bd8e6b84982
```
