# The physical unary word excludes the target-coloop E3-flat plane

## Result

Continue from the single-`C6/C8` target-coloop exchange at `h=3`.  The
five source values used in an E3 comparison can be taken on the literal
full-`H8` words

```text
22222222,  one active mixed word,  one further mixed word,
00000000,  11111111,
```

with target vector

\[
                             h=(1,0,0,1,1).            \tag{1}
\]

Let `M` be the bright target response matching and `N` the outside response
matching.  They are fixed physical matching bases throughout these five
words.  In the normalized one-bad packet the colour-zero endpoint rows
vanish away from the direct `E_00` pair.  Since both `M,N` avoid that direct
pair,

\[
                  \mu_M(0^8)=\mu_N(0^8)=0.            \tag{2}

If `t` is the bright target word and `d` the selected outside mixed word,
the target-coloop E2 pivot is

\[
 \Delta_{td}=\mu_M(t)\mu_N(d)\ne0.
\]

Equations (1)--(2) give the literal E3 identity

\[
 \boxed{
 \det(\mu_M,\mu_N,h)_{t,d,0^8}=\Delta_{td}}
                                                               \tag{3}
\]

up to the harmless global sign from the ordering of the three columns.
Thus the E3-flat two-base plane is impossible on the physical one-bad
packet.

Checker:
[`verify_h3_axis_target_coloop_unary_e3_flat_exclusion.py`](../computations/verify_h3_axis_target_coloop_unary_e3_flat_exclusion.py).

## Scope correction to the row-level flat guard

The rational vectors

\[
 a=(1,1,2,3,4),\qquad b=(0,-1,-2,-2,-3),\qquad h=a+b
\]

do make every E3 determinant vanish abstractly.  But their unary entries
are `3` and `-2`; they violate (2).  They are therefore a valid arbitrary
five-row module and **not** a full-source one-bad boundary.

The source typing in (3) is literal.  All five rows are coefficients of one
full eight-site matching tensor, and `M,N` are the same physical bases in
every word.  The vanishing (2) comes from actual zero outer star cells, not
from assigning formal evaluation coordinates.

## The selected third base

The E3 matching-base identity cancels the `M,N` terms before division by any
common factor.  Since (3) is nonzero, a third literal full-source matching
survives.  In the unary word every nonzero matching must use the direct
`P-S:00` cell: all colour-zero endpoint-star cells are zero.  Hence the
third bases are exactly

```text
P-S together with one of the 15 pure-zero matchings on the six residual sites.
```

Each uses a physical edge outside `M union N`, for both the `C6` and `C8`
topologies.  This is a source-valid cycle opening.

It is not yet a free-edge theorem.  The direct `P-S` edge is already the
selected unary anchor, and the residual pure-zero matching may be chosen as
the existing unary witness.  Therefore the E3 output can remain wholly in
the selected three-anchor web.  Moreover, it does not supply an alternate
bright response matching avoiding the target-coloop arm.  The exact
remaining branch is

```text
bright target coloop + outside active response base + unary direct-anchor base.
```

Routing that three-base anchor web to a four-good/Hall landing needs one
more response companion or an anchor-safe matching exchange; the abstract
E3-flat obstruction itself is gone.

## Verification

Run

```text
python3 computations/verify_h3_axis_target_coloop_unary_e3_flat_exclusion.py
python3 -O computations/verify_h3_axis_target_coloop_unary_e3_flat_exclusion.py
python3 -I -S computations/verify_h3_axis_target_coloop_unary_e3_flat_exclusion.py
```

Frozen ledger SHA-256:

```text
1e572c10454eaf99a0737d07a3a0efd6df1cb01c4d85c22359444f893de3f20e
```
