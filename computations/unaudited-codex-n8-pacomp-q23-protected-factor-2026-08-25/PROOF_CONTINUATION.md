# `Q23-PROTECTED-FACTOR`: first unmatched term

Status: **COUNTER-OBLIGATION ISOLATED; FACTORIZATION NOT PROVED**  
Parent package manifest: `e580fd316a4aa3a52b50e66b5173d7c3372a39d2da721848a21be8295aeb0a6e`

## Result

The source-side `q=23` square closes term by term, including all source
labels available before protected cap projection.  The first unmatched term
is not a coefficient, divided-root, restriction, reinsertion, word, fine,
repeated-site, target, or ordinary-residue term.  After the strongest pinned
endpoint correction is cancelled, it is the clean Eq-only coordinate

\[
 C_{Eq,23}=(0,E_{23},0),\qquad
 E_{23}=D_{\rm root}\otimes B_1,qquad
 D_{\rm root}=(-1,1,-1,1),                         \tag{1}
\]

in `(lower, Eq, ores)` order.  Lexicographically, the first unmatched term is

```text
operation: response -> cap (e_C A e_R)
cut/face:  q23 / 0112:q23:21
root word: 0
pure label: B1
row:        Eq
coefficient: -1
lower=0, ores=0.
```

The primitive covector
`lower_(root0,B1)-Eq_(root0,B1)` kills the complete strong endpoint grant
and reads `+1` on this term.  Thus the present pinned definitions do not
prove `Q23-PROTECTED-FACTOR`.

## 1. Literal selected source object

The canonical parent and marked branch are

```text
parent = 01|23|45|67,
branch = 07|23|45|67,
missing site = 1,
doubled site = 7.
```

At response word `11110000`, the branch is

```text
07:10, 23:11, 45:00, 67:00.
```

At cap word `01211222`, it is

```text
07:02, 23:21, 45:12, 67:22.
```

Deleting `q23` leaves

```text
response lower = (07:10,45:00,67:00),
cap lower      = (07:02,45:12,67:22).
```

The remaining divided-root orders at changed sites
`(0,2,4,5,6,7)` are `(1,0,1,1,1,2)`.  The zero at missing site 2 and order
two at doubled site 7 are essential: replacing them with ordinary order-one
roots does not define the marked branch map.

## 2. The two intrinsic composites

Let `m` be the response decorated branch monomial.  The first path is

\[
 m\xrightarrow{\Phi}
 (07{:}02)(23{:}21)(45{:}12)(67{:}22)
 \xrightarrow{D_c}\
 (07{:}02)(45{:}12)(67{:}22)
 \xrightarrow{I_c}\
 (07{:}02)(23{:}21)(45{:}12)(67{:}22).
\]

Every arrow has coefficient `+1`.  The second path is

\[
 m\xrightarrow{D_r}
 (07{:}10)(45{:}00)(67{:}00)
 \xrightarrow{\Phi_{\widehat{23}}}
 (07{:}02)(45{:}12)(67{:}22)
 \xrightarrow{I_c}\
 (07{:}02)(23{:}21)(45{:}12)(67{:}22),
\]

again with coefficient `+1`.  The checker repeats this equality on all 90
marked branches containing `q23`.  Hence

\[
 I_cD_c\Phi d(m)=dI_c\Phi_{\widehat{23}}D_r(m)        \tag{2}
\]

term by term.  There is no unmatched sign on the intrinsic square.

## 3. Marked coefficient augmentation

The missing-site mark plus the cofactor recovers the deleted edge.  The
pinned lower quotient therefore names the cap lower face canonically:

```text
0112/q23:21 -> B1.
```

The endpoint-even normalized image is

\[
 {c_1^+\over8}={1\over8}(-1,5,-1,-1,-1,-1).        \tag{3}
\]

This is source-provenant in the marked-derived category.  It does not choose
between the protected `B` and `Eq` copies.  The actual cap top is tied, so

```text
actual    = (c1+/8,c1+/8),
required  = (c1+/8,0),
residual  = (0,-c1+/8).
```

Thus the protected split, not (2) or (3), is the first failing interface.

## 4. Hidden `-E/+E` faces and exact cancellation

Split the pinned combined coefficient

\[
 E=2D_{\rm root}\otimes{B_1+B_4\over2}
   =E_{23}+E_{45}
\]

as

\[
 E_{23}=D_{\rm root}\otimes B_1,qquad
 E_{45}=D_{\rm root}\otimes B_4.                    \tag{4}
\]

For `q23`, the required hidden boundary is

\[
 H_{23}=(-E_{23},0,+E_{23}).                         \tag{5}
\]

The strongest pinned endpoint grant allows arbitrary tied endpoints
`M_u=(u,u,0)`, arbitrary ordinary-residue endpoints `K_u=(0,0,u)`, and all
root/cut bars between them.  With

\[
 M_{E23}=(E_{23},E_{23},0),\qquad
 K_{E23}=(0,0,E_{23}),
\]

the termwise decomposition is

\[
 \boxed{H_{23}=-M_{E23}+K_{E23}+C_{Eq,23}}.          \tag{6}
\]

The first two summands cancel every lower and ordinary-residue term, but
also introduce `-E23` in the Eq row.  The unique correction is (1).  In root
order `0,1,2,3`, its four nonzero Eq coefficients are

```text
-1, +1, -1, +1
```

at pure label `B1`, with lower and ores zero.  The strong endpoint/bar span
has rank 48; adjoining `C_Eq,23` raises it to 49.  This proves that (1) is
the first unmatched protected object in the pinned inventory.

Equivalently, restoring the polynomial label suppressed in (1), the missing
face is

\[
 D_{\rm root}\otimes B_1\otimes(H_0-u)e_{Eq},        \tag{7}
\]

with no lower/private, ores, `W`, target, or anchor component.

## 5. Covariance and sign provenance

The site involution `sigma=(2 5)(3 4)` sends the decorated `q23` lower word
to the `q45` lower word with coefficient `+1`.  On root/pure labels, the
pinned transition is

```text
root: (0 1)(2 3),
pure: (B0 B5 B3 B2)(B1 B4).
```

The root permutation sends `D_root` to `-D_root`, while the pure transition
sends `B1` to `B4`.  Therefore

\[
                  \sigma(E_{23})=-E_{45}.             \tag{8}
\]

A covariant missing cell must consequently satisfy
`d(sigma X23 + X45)=0`; after a normalized choice with no extra closed
summand, `sigma X23=-X45`.  The plus sign in the decorated monomial square
and the minus sign in (8) concern different label layers and are both pinned.
No existing `e_C A e_R` operation supplies the latter orientation: the
generated off-diagonal operation space has dimension zero.

Root naturality is a separate obligation.  The `AB` and `AC` receiving
sections form a two-dimensional labelled quotient; neither a single section
nor a root-forgetting sum suffices.  The four `D_root` word coordinates in
(4) must not be confused with those two operation-root labels.

## Minimal counter-obligation

Construct a source-labelled cell `X23` in the response-to-cap corner
`e_C A e_R` whose selected-grade augmented boundary contains exactly (7) in
the protected Eq row and zero in lower/private, ores, `W`, target, and anchor
rows after the known `-M_E23+K_E23` cancellation.  Prove the cut covariance
`sigma X23=-X45` up to a source-provenant closed nullhomotopy, and construct
the two separate natural `AB` and `AC` instances.

This is smaller than a full comparison: all terms before (7) have been
identified and cancelled.  It is also not a theorem that such a cell does
not exist; it is the first exact term not supplied by the current pinned
operation inventory.

## Scope guard

This note proves an `h=3`, canonical-`q23`, first-unmatched-term statement.
It does not prove `Q23-PROTECTED-FACTOR`, `PAComp(3)`, uniform `PAComp(h)`,
source-terminal essential surjectivity, or the Krenn–Gu conjecture.  Nothing
here is promoted to the certified spine.

