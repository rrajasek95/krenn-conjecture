# The centered square exits the physical operation fan at its first mandatory face

## Verdict

The centered balanced `K2,2` of `ff4b719` does **not** survive as a closed
internal component after the actual Gate-II port, site, operation, word and
reinsertion labels are restored.

On the fixed residual window

```text
W = 2345,
H_W = q23*q45 + q24*q35 + q25*q34,
```

put

\[
 A=Dq_{01}H_W,\qquad B=p_0s_1H_W,\qquad C=p_1s_0H_W. \tag{1}
\]

The formal square has ordered direct vertices
`A_[a|b],A_[b|a]` and endpoint vertices `B,C`.  All four of its mate
edges change the physical operation profile

```text
DQ = (1,0,0,1)   <->   PS = (0,1,1,0).
```

Literal site-root, restriction and reinsertion faces preserve that profile.
Consequently none of the four formal `K2,2` edges is an internal physical
face.  Under the projection identifying the two ordered direct copies, the
four edges become exactly two missing switch row types:

\[
                              A+B,\qquad A+C.          \tag{2}
\]

Mandatory product-rule differentiation makes the failure sharper rather
than repairing it.  Its six literal direction labels carry primitive
charge

\[
 (dD,dq_{01},dp_0,ds_1,dp_1,ds_0)
                  =(2,2,-1,-1,-1,-1).                \tag{3}
\]

Reinserting the two arrows of each operation block gives

\[
 (2+2,-1-1,-1-1)=(4,-2,-2)=2(2,-1,-1).             \tag{4}
\]

After the shore gauge, (4) is `(4,2,2)`, of augmentation `8`.  Thus the
first mandatory face routes the centered coefficient square to a
**noncentered physical cone debt**.  The presentation-safe relative graph
`dU=H_W-r` transports the same debt from `H_W` to the retained `r`; it does
not close it.

Exact checker:
[`verify_h3_fixed_window_centered_k22_physical_routing_gate.py`](../computations/verify_h3_fixed_window_centered_k22_physical_routing_gate.py).

## 1. The smallest canonical fully labelled packet

Retain exactly the labels needed by the known physical faces:

```text
four words       0112, 1112, 0102, 1102
three charts     A=D*q01, B=p0*s1, C=p1*s0
three C4 tails   23|45, 24|35, 25|34
one r carrier    for every word/chart
```

This gives `4*3*3=36` occurrence coordinates and `4*3=12` retained
coordinates.  The checker includes all of the following complete families:

1. every edge of the literal two-root word square, at each fixed chart and
   matching occurrence;
2. both primitive matching differences on `2345`, at every word and chart;
3. the complete response row `A+B+C`, at every word and matching;
4. every monic relative graph `dU_(w,j)=H_(w,j)-r_(w,j)`;
5. every induced word face and complete-response face of the retained
   carriers.

There are 100 displayed boundary columns in 48 output coordinates.  Their
rank is 46.  A two-dimensional chart quotient remains: the endpoint-odd
line and the Gate-II line

\[
                              L=(2,-1,-1).             \tag{5}
\]

The exact `L` detector is constant on the word square.  On each of the
three matching coordinates it has value `L/3`; on the retained carrier it
has value `L`.  It therefore kills every listed boundary, including

\[
                         H_{w,j}-r_{w,j},              \tag{6}
\]

and reads `6` on both `L H_W` and `L r`.  In particular,

\[
                         L H_W-Lr                     \tag{7}
\]

is an internal graph boundary, but neither term of (7) is internal by
itself.  This is the exact sense in which the relative construction moves
the obstruction without erasing it.

The packet is minimal in the canonical Cartesian face category: four word
vertices are forced by the two-root square, three chart tags by (1), three
matching occurrences by the literal `C4`, and one retained coordinate per
word/chart by presentation safety.  This is not a claim of absolute
minimality among arbitrary untyped complexes.

## 2. Why the direction face is noncentered

The six physical arrows in (3) map to charts as

```text
(dD)*q01      -> A
D*(dq01)      -> A
(dp0)*s1      -> B
p0*(ds1)      -> B
(dp1)*s0      -> C
p1*(ds0)      -> C.
```

Equation (4) follows termwise.  With all three residual matchings retained,
the eighteen direction terms are `2 L H_W`.  The detector reads `12` on
this packet.  Totalizing the two Leibniz arrows in each block cancels the
mixed `x'y'U` faces exactly and replaces `2 L H_W` by `2 L r`; the detector
still reads `12`.

Thus no combination of the known tag-preserving word faces, matching
faces, complete response rows or relative reinsertion faces can close the
direction packet.  In a full source it must acquire a column with nonzero
image in this quotient, or it remains a normalized terminal class.

## 3. The first missing full-source rows

Coefficientwise, both switch types in (2) are necessary.  With the internal
packet of Section 1, adjoining only `(A+B)H_W` gives ranks

```text
46 -> 47 -> 48 after adjoining L*H_W;
```

and the same holds with only `(A+C)H_W`.  Adjoining both switches gives

```text
46 -> 48 -> 48 after adjoining L*H_W.
```

The literal projection is

\[
        L=-4(A+B+C)+3(A+B)+3(A+C).                   \tag{8}
\]

Therefore the first missing full-source datum is a pair of same-word,
same-fine, same-repeated-grade, same-window chart-switch families with
faces

\[
 (Dq_{01}+p_0s_1)H_{2345},\qquad
 (Dq_{01}+p_1s_0)H_{2345},                           \tag{9}
\]

together with their `dU=H-r` restriction/reinsertion companions and the
`q`, pointed-anchor, `W` and ridge readouts of those **same** source cells.
They are outside the existing tag-preserving operation fan.  A different
source column is equally sufficient only if its projection has the same
nonzero quotient image.

This locates the first missing row more sharply than “some companion term.”
It is not another pure normalization, scalar localization, ordinary
`q`-Jacobian column, or tag-preserving root face.

## 4. Uniform finite-family consequence

Complete word/window/tail labels define independent coefficient rows until
a physical cross-label reinsertion column is supplied.  Hence a finite
family of internal packets is a block sum of the local 48-coordinate
complex.  The checker freezes one, two and three components: their
cokernel dimensions are respectively `2,4,6`.  Global signed sums cannot
cancel a charge living in a distinct labelled summand.

Together with `ff4b719`, this gives the sharp boundary:

```text
normalization alone       -> centered K2,2 guards are compatible;
full operation labels     -> their mate edges leave the internal fan;
mandatory PP/reinsertion  -> a nonzero-augmentation L debt is exported;
both chart switches       -> coefficient projection succeeds by (8);
no chart switches         -> the augmented terminal branch remains.
```

## Scope and terminal alternative

This is an exact physical-label/rank theorem for canonical `h=3` and the
fixed-window face category currently constructed in the proof.  It proves
that the abstract centered guard cannot be promoted to a closed
tag-preserving physical component.  It does not construct the two
profile-changing source families in (9), and it does not yet prove that the
displayed detector annihilates every additional, as-yet-unlisted full-source
column.

Accordingly the final local fork is exact:

```text
physical chart-switch/cone column exists
    -> it lands the noncentered charge and starts the committed descent;
no such column in the exhaustive same-grade map
    -> extend the L detector to the normalized augmented terminal.
```

Run

```text
python3 computations/verify_h3_fixed_window_centered_k22_physical_routing_gate.py
python3 -O computations/verify_h3_fixed_window_centered_k22_physical_routing_gate.py
python3 -I -S computations/verify_h3_fixed_window_centered_k22_physical_routing_gate.py
```
