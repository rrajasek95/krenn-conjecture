# Divided-root naturality constructs the marked-derived P2 faces

## Result

The six-root response-to-cap section has a canonical extension from perfect
matchings to every marked collision branch.  At a changed site, use divided
root order equal to the site's occurrence multiplicity: order zero at a
missing site, order one at an ordinary site, and order two at a doubled site.
This is not a collection of unrelated recolourings.  The checker verifies
all 540 parent-to-branch squares

\[
 \Phi_{\rm branch} I_{0j}^{r}D_{0i}^{r}
 =I_{0j}^{c}D_{0i}^{c}\Phi_{\rm parent},
\]

and all 1,080 marked `P3+K2` deletion faces, coefficient one termwise.  The
branch total orders are `5:126`, `6:279`, and `7:135`; the changing order is
exactly what makes the trigger square commute when a changed site is missing
or doubled.

Consequently this construction genuinely fills the rank-`0 -> 2`
word/fine defect in the **marked-derived** cap.  It is more than an
undecorated response shadow, but it is not an underived projection to `r0`.

The exact checker is
[`verify_h3_six_root_marked_collision_p2_restriction_reinsertion.py`](../computations/verify_h3_six_root_marked_collision_p2_restriction_reinsertion.py).

## The two cuts

Put

```text
r = 11110000,
c = 01211222,
changed sites = {0,2,4,5,6,7}.
```

For every perfect matching containing `23`, delete its decorated `23` cell
and omit the root at changed endpoint 2.  For every matching containing
`45`, omit the roots at endpoints 4 and 5.  Direct calculation gives

\[
R_{23}^{21}\Phi_6=\Phi_{\widehat 2}R_{23}^{11},
\qquad
\Phi_6 I_{23}^{11}=I_{23}^{21}\Phi_{\widehat 2},
\]

and

\[
R_{45}^{12}\Phi_6=\Phi_{\widehat4,\widehat5}R_{45}^{00},
\qquad
\Phi_6 I_{45}^{00}=I_{45}^{12}\Phi_{\widehat4,\widehat5}.
\]

The remaining cap words are

```text
delete 23: core 0112, spectator 22, reinsertion q23:21;
delete 45: core 0121, spectator 22, reinsertion q45:12.
```

They occupy independent word/fine/operation summands, so their image has
rank two.  This is exactly the rank which was absent from the diagonal
marked cap.

All 64 vertices of the top root cube, all 32 vertices of the `q23` lower
cube, and all 16 vertices of the `q45` lower cube are mixed GHZ-zero words.
Thus the restriction has zero target commutator; no target filler is being
hidden in the construction.

## Pointed occurrence and first PP face

The marked Beck--Chevalley section is monic on each parent and retains its
missing-site/fine/reinsertion label.  The omitted-root restriction is also
monic and preserves the ordered lower occurrence.  It therefore supplies,
in the marked-derived category, the pointed occurrence section which the
existing two-direction Hasse/cobar square used as its sole conditional
input.  All 12 ordered `h=2` occurrences are obtained termwise.

Linearity now permits the exact private combination

\[
z_{\rm private}=(101/432,-1/108,-1/27,101/432,-1/27,-1/108,
 -1/108,-1/27,-61/432,-1/27,-1/108,-61/432).
\]

It has augmentation zero.  Reinsertion is governed by the literal first-PP
identity

\[
d(q_{23}S)=q_{23}dS+dq_{23}S.
\]

Hence its `dq23` coefficient is again `z_private`; the primitive detector
`+e0+e3-e1-e6` reads `35/72`, while ordinary residue reads zero.  The
symmetry `sigma=(2 5)(3 4)` gives the `q45/dq45` mate with the same value.
The divided-root map commutes with the universal first-PP differential, so
this `dq` face is part of the marked-derived map, not merely a predicted
coefficient.

## First remaining protected failure

The result does not identify the marked totalization with the underived
physical `r0` packet.  At the first complete protected landing, the marked
map remains tied:

```text
derived readout     (delta_plus, delta_plus),
required output     (delta_plus, 0).
```

The integral `B-Eq` covector kills the former and reads `3` on the latter.
Equivalently the map still needs the hidden proper faces

```text
lower/private        -E,
word-resolved ores   +E.
```

Thus the proof frontier moves again.  The Hom/word section, both marked P2
restrictions, and the first `dq` reinsertion are now constructed in the
derived marked complex.  The shortest remaining datum is their protected
`B/Eq/ores` totalization (or an exhaustive dual proving it cannot exist),
not another word or occurrence selector.
