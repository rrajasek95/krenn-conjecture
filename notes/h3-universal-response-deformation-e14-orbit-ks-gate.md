# Universal response deformation and the E14 orbit KS gate

## Result

The universal response deformation gives the marked centered-occurrence
Kodaira--Spencer class canonically, and its centered completion is natural for
the matching and endpoint operators.  It also combines flatly with the
four-root moving-target orbit.  This is a positive construction in the
orbit-relative presentation, but it does **not** yet give the required chain
in the fixed physical AugP2/E14 complex.

The first missing datum is now precise: compare the relative Tate/connection
generator whose boundary is the centered occurrence class with a
source-labelled physical AugP2/E14 chain, including its word, fine,
repeated-edge, ridge, and `q` readouts.

The exact certificate is

```text
computations/verify_h3_universal_response_deformation_e14_orbit_ks_gate.py
```

with frozen ledger digest

```text
769845c7dc831d448d582f8108ea4fc71782c1df8e7e08d742a5dda378660d85
```

## 1. The relative KS class

Let the complete response row be

\[
 R=\sum_{M=1}^{90} f_M
\]

and mark one occurrence `f`.  The one-parameter presentation

\[
 R_s=R-s\,90f
\]

has derivative `-90f`.  Modulo the original response direction,

\[
 -90f+R=-(90f-R)=-c_f.
\]

Thus the family constructs exactly the centered class, with coefficient one
and the correct sign.  Equivalently, for

\[
 h_f=e_f-\frac1{90}{\bf 1},
\qquad -90h_f=-c_f.
\]

The selected one-parameter family is not endpoint-equivariant because an
endpoint path moves the marked occurrence.  Its minimal equivariant
completion is the 89-dimensional centered family

\[
 R_z=R-90\sum_M z_Mf_M,
\qquad \sum_M z_M=0.
\]

The KS map is `-90` times the identity on this centered module, hence an
isomorphism over the characteristic-zero theorem field.

## 2. Matching and endpoint naturality

On the literal 90-occurrence module, the centering operator is

\[
 C=90I-J.
\]

The checker verifies on all 90 basis occurrences that

\[
 [C,A+I]=0,
 \qquad [C,B]=0.
\]

The matching graph has degree 3 and the endpoint graph degree 8.  Therefore
the already isolated private curvatures

\[
 C_2=(B+4/7)v_0,
 \qquad
 C_3=(B^2-6B-52/7)v_0
\]

are induced coefficientwise by this single `B`-natural response schema.  No
additional coefficient generator is needed.  This statement does not itself
construct the augmented physical second-Hasse faces.

## 3. Product with the moving-target orbit

The formal two-parameter family is

\[
 R_{z,t}=g_tR-90\sum_M z_Mg_tf_M-\Delta(t).
\]

Occurrence parameters act on tags; the four roots act on colours.  The
certificate checks all 32 root edges and 24 mixed squares.  Their mixed
curvature is zero.  The orbit-relative D4 result transports

```text
bottom: -c_f in word 11:110000
top:    -c_g in pure G11[111111]
```

and removes the affine target unit in the moving-target cone.  No pullback to
a fixed labelled fibre is required for this formal orbit-relative statement.

## 4. What the family does not supply

Evaluation at `s=0` is a genuine pointed augmentation, and the response
family is flat (one can solve for an unmarked occurrence).  The obstruction
is therefore **not** absence of an augmentation or a Tor defect.

In a Tate presentation, differentiating the response generator and applying
the old-row gauge produces a relative connection generator
`epsilon_s` with

\[
 d\epsilon_s=-c_f.
\]

Flat base change constructs this nonzero transitivity/KS class; it does not
provide a splitting or nullhomotopy of it in the old fixed physical fibre.
The first physical theorem needed is a source-labelled comparison

\[
 \epsilon_s\longmapsto
 \operatorname{AugP2/E14}_{\rm phys}
\]

carrying the known occurrence, target, residue, and protected rows.

This is exactly where the formal response family stops.  Calling the family
itself a fixed-fibre physical boundary would be circular.

## 5. Cap, ridge, and physical `q`

The normalized cap graph is formally constant in the response parameter and
flat over the D4 cube.  The shifted ridge has the known root connection face

\[
 -d(q_{xv}^{01})
\]

at the matching root site, with zero mixed root curvature.  That face is
eta/sigma dark in the fixed frame, and transported contractions preserve the
terminal laws.

This still lacks literal physical placement: the cap word `01211222` is not
an object of the `110000 -> 111111` D4 cube and has a distinct eight-site
fine/repeated grade.  Thus the formal horizontal local system does not prove
the physical ridge comparison.

Likewise, physical

\[
 q=\sum 6m-a_{\rm inc}
\]

is a cochain on the complete physical relative domain.  It has no value on
`epsilon_s` before the comparison above is constructed.  After a protected
physical comparison exists, no separate exact terminal equality is needed:
the committed `q`-defect alternative gives either transport/Fredholm or the
physical relative generator, provided both endpoint readouts are physically
typed.

## Shortest remaining lemma

Construct one endpoint- and D4-equivariant, pointed map from the universal
relative KS generator into the complete physical AugP2/E14 complex, preserving
the flat cap graph and shifted ridge.  Matching/endpoint polynomial faces and
the D4 target correction then come for free from the construction above; the
physical `q` branch closes by the existing defect alternative.

Scope is canonical `h=3` over a characteristic-zero field.  No uniform-in-`h`
comparison, fixed physical grading map, `q` extension, or terminal promotion
is claimed here.
