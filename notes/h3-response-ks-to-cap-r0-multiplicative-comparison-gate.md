# The response KS and tied cap `r0` fit algebraically, but their physical graded map is missing

## Outcome

The attempted upgrade stops at one precise source-labelled arrow.

The universal response deformation canonically constructs the relative
Kodaira--Spencer generator

\[
                       d\epsilon_s=-c_f              \tag{1}
\]

in the response occurrence/cotangent object.  Independently, the physical
cap generator `r0` is genuinely tied:

```text
literal full-nine private boundary     B
cap differential                       E=(H0-u)e_Eq
normalized target                      1.
```

Thus a column already known to be an `r0` column has `B=Eq`.

After forgetting source grades, the two complexes admit a unique normalized
chain-map shape:

\[
 \Phi_1(\epsilon_s)=r_0,
 \qquad
 \Phi_0(c_f)=-E.                                      \tag{2}
\]

There is no coefficient or sign obstruction in (2).  The obstruction is
that the fixed physical source contains no degree-zero map `Phi` between the
two literal objects:

```text
response   11:110000 / centered occurrence-PP / universal-response KS
cap        01211222 / t*q_(v,N) / P3+K2 / AugP2-K_Eq.
```

All six selected fine degrees change, the words differ at six sites, and the
cap word is not in the response `D4` cube.  The standard mapping-cylinder
construction requires `Phi` as input; it cannot manufacture a map between
these orthogonal idempotents.

Therefore the strict physical multiplicative schema is **not constructed**.
If one source-labelled normalized `Phi` is constructed naturally at the
eight marked one-root objects, then its image factors through tied `r0`, the
standard mixed products satisfy `B=Eq`, and commit `3ad761f` gives

\[
                         \lambda_i=0
 \quad\text{for all eight instances}.                \tag{3}
\]

Checker:
[`verify_h3_response_ks_to_cap_r0_multiplicative_comparison_gate.py`](../computations/verify_h3_response_ks_to_cap_r0_multiplicative_comparison_gate.py).

## 1. The literal response generator

Let the complete response be

\[
                         R=\sum_{M=1}^{90}f_M
\]

and mark one occurrence `f`.  The universal family

\[
                         R_s=R-90s f                  \tag{4}
\]

has relative derivative

\[
              -90f+R=-(90f-R)=-c_f.                 \tag{5}
\]

Its 89-dimensional augmentation-zero completion is natural for the
matching and endpoint operators.  In the orbit-relative Tate presentation,
(5) is precisely (1), with coefficient one and pinned sign.

This is real positive input.  The obstruction is no longer the existence of
the centered response KS class.  What (4)--(5) do not give is a chosen image
of `epsilon_s` in the old fixed physical AugP2/E14 complex.  Flat base change
constructs a transitivity class, not a splitting or nullhomotopy of that
class in a different source summand.

The matching numerator makes the next coefficient step exact:

\[
 (A+I)c_f=3c_{01},
 \qquad c_{01}=30b_{01}-R.                            \tag{6}
\]

In a presentation-preserving relative graph, however, this gives only

\[
 d\epsilon_{01}=b_{01}-t_B,                          \tag{7}
\]

where `t_B` is the retained carrier coordinate.  Setting `t_B=0` would turn
the centered relative comparison into an absolute selected response
equation and change `H0`.  Thus (6) does not secretly supply an absolute
fixed-fibre generator.

## 2. The cap `r0` is tied internally

The cap theorem supplies a physical generator `r0` whose cap differential
is

\[
                         dr_0=(H_0-u)e_{Eq}=E.         \tag{8}
\]

Its literal full-nine response face is the private packet `B`, and its
target is normalized to one.  In the physical output convention the same
column therefore has

\[
                         (B,Eq)=(v,v)                 \tag{9}
\]

for its occurrence vector `v`.  Equation (9) is an actual theorem about
the cap object; it is not notation inserted to make the balanced dual work.

What remains conditional is membership of a response-side row in that cap
object.  The four tied rows used in the local rank-`126/127` supermap are the
result of choosing the missing cross-word image to be `r0`.  They do not
construct the cross-word image.

## 3. The ungraded chain map is unique

Strip away word, fine, repeated, and operation idempotents.  Retain the two
two-term complexes

\[
 C_R:\quad \mathbb Q\langle\epsilon_s\rangle
       \mathop{\longrightarrow}^{d}
       \mathbb Q\langle c_f\rangle,
 \qquad d\epsilon_s=-c_f,                            \tag{10}
\]

and

\[
 C_C:\quad \mathbb Q\langle r_0\rangle
       \mathop{\longrightarrow}^{d}
       \mathbb Q\langle E\rangle,
 \qquad dr_0=E.                                      \tag{11}
\]

Write

\[
 \Phi_1(\epsilon_s)=a r_0,
 \qquad \Phi_0(c_f)=bE.                              \tag{12}
\]

The chain-map equation gives

\[
 d\Phi_1(\epsilon_s)=aE
   =\Phi_0(-c_f)=-bE,
 \qquad a+b=0.                                       \tag{13}
\]

The solution space is one-dimensional, generated by `(a,b)=(1,-1)`.
Monicity of (5) and the normalized `r0` target select exactly this generator.
Hence the signs and scalar are already forced if the physical graded map
exists.

The standard cone of this normalized map has tied projection (9), so its
balanced charge is zero.  Adding a nonstandard closed terminal cocycle would
reopen the freedom from `3ad761f`; it is excluded precisely by requiring the
normalized standard mapping cylinder/module product.

## 4. Literal idempotents kill the map

Let `e_R` and `e_C` denote the response and cap source idempotents.  The
currently constructed fixed-grade operation algebra contains the two
diagonal matrix units

\[
                         e_R,qquad e_C,               \tag{14}
\]

but no off-diagonal unit

\[
                    w_{KS,cap}=e_Cw e_R.              \tag{15}
\]

The exact literal tags are

| axis | response KS | cap `r0` |
|---|---|---|
| word | `11:110000` | `01211222` |
| fine | centered marked response occurrence/PP | selected six `t*q_(v,N)` degrees |
| repeated | response occurrence and its PP faces | `P3+K2` |
| operation | universal response KS / endpoint-matching orbit | AugP2 cap / `K_Eq` |

Forgetting these tags changes the two diagonal operation coordinates into a
coarse coefficient space where (2) can be written.  Restoring them raises
the operation-coordinate rank from two to three when (15) is adjoined.
Neither matching centering nor the moving-target `D4` orbit supplies (15):
matching stays in the response word, while the `D4` cube runs from `110000`
to `111111`; the cap word is not one of its vertices.

A standard mapping cylinder is functorial in an already specified chain
map.  It adds the cone shift, the oriented square, and its interchange cell.
It does not add the missing degree-zero matrix unit (15).  Calling the cone
“standard” before (15) is constructed therefore assumes the desired
physical comparison.

## 5. First literal proper face and first mixed face

The obstruction has two complementary finite projections.

At first principal-parts order, differentiating (6) gives

\[
                         dc_{01}=30db_{01}-dR,         \tag{16}
\]

where

\[
\begin{aligned}
 db_{01}=p_0s_1(&dq_{23}q_{45}+q_{23}dq_{45}
                +dq_{24}q_{35}+q_{24}dq_{35}\\
               &+dq_{25}q_{34}+q_{25}dq_{34}).       \tag{17}
\end{aligned}
\]

The old complete response PP row has rank one in the thirty
fixed-endpoint-fibre quotient.  Adjoining (17) raises the rank to two.
Thus `db01` is the first literal proper face which a physical `Phi` must
carry; it is not already a boundary in the old fixed source.

The presentation-safe graph alternative

\[
                         d\epsilon_g=z_{01}-b_{01}     \tag{18}
\]

does not solve this.  Its Koszul product has the unwanted face
`z01*theta`.  Killing `z01` makes `b01=0` in the classical fibre and changes
`H0`.  The primitive graph dual `(1,-1,1)` detects the missing selected
section exactly.

After granting the selected PP face and the endpoint target normal, retain

```text
(P_f, primitive cap, R_E14, central E, ridge).
```

The first three existing directions have rank three.  The required
source-labelled placement

\[
                     \Phi_{orb}(E)=R_{E14}             \tag{19}
\]

raises the rank to four and is read by the central-incidence covector
`(0,0,0,1,0)`.  Hence (17) is the first response proper face and (19) is the
first cross-summand face of the same missing map.  They are not independent
proof branches.

## 6. Smallest source-labelled counterguard

Take the direct sum of the two committed literal presentations:

```text
response object    d epsilon_s=-c_f, word 11:110000
cap object         d r0=E, tied B=Eq, normalized target 1.
```

Retain every internal response identity, every internal cap identity, and
the formally flat cap graph and `D4` transport.  Set

\[
                         \operatorname{Hom}^0(e_R,e_C)=0. \tag{20}
\]

This is exactly the present fixed-grade grammar.  It satisfies all pinned
internal equations but has no mixed mapping cylinder and therefore no
physical reason to assign the eight `lambda_i` the standard-product value.
It is a source-labelled counterguard, not merely an abstract filtered DGM.

Adjoining one matrix unit (15), together with its boundary map in (2), is
the smallest rank-raising change.  The chain-map equation then forces the
same normalization on both faces.

## 7. Minimal positive schema

The exact missing theorem can now be stated without a free scalar:

> **Response-KS/cap-`r0` comparison.**  Construct a protected,
> source-labelled degree-zero chain map `Phi_KS,r0`, natural in the marked
> endpoint/matching and one-root object, from the universal response KS
> family to the physical AugP2/`K_Eq` cap complex.  Require
> `Phi_1(epsilon_s)=r0` modulo typed dark cap normalizers and
> `Phi_0(c_f)=-E`, with monic normalization.  Its proper faces are the
> selected `db01` family, the central placement (19), the primitive cap and
> closed `T+rho` normalizer, physical `ainc/q`, `W`, labelled residue, and
> shifted ridge/eta/sigma.

One schema must be instantiated separately at the eight labelled lower
words

```text
0012, 0102, 0110, 0111, 0122, 0212, 1112, 2112.
```

No coarse symmetry transport is used.  Once the schema is natural on those
objects, its standard mapping cylinder exists, the `r0` image is tied, and
(3) follows.  Conversely, without (15)/(19), the internal `r0` tie cannot be
exported to the response row.

## Scope and verification

This is an exact canonical `h=3` rational obstruction and construction
interface.  It proves that the response KS generator and cap `r0` have
compatible unique ungraded normalization, and identifies the first literal
graded obstruction.  It does not prove nonexistence of the physical map,
construct a full finite GHZ packet, settle all target/output words, or give
uniform spectator-tail transport.

Run:

```text
python3 computations/verify_h3_response_ks_to_cap_r0_multiplicative_comparison_gate.py
python3 computations/verify_h3_response_ks_to_cap_r0_multiplicative_comparison_gate.py --mode counterguard
python3 computations/verify_h3_response_ks_to_cap_r0_multiplicative_comparison_gate.py --mode positive-schema
python3 -O computations/verify_h3_response_ks_to_cap_r0_multiplicative_comparison_gate.py
python3 -I -S computations/verify_h3_response_ks_to_cap_r0_multiplicative_comparison_gate.py
```

Frozen ledger SHA-256:

```text
61eb76cf31690a4aea7981a872a43b0b740d98193b2a08526d63f232d2f4c7f2
```
