# The relative `GL3` bar times `K_Eq` is strict but remains outside `Gamma_*`

## Verdict

The normalized local-`GL3` interval can be multiplied by the strict central
cone without making either endpoint absolute.  If

\[
                  dE=L-D,qquad d\theta=F=(H_0-u)e_{Eq}, \tag{1}
\]

then the literal product is

\[
 \boxed{
 \kappa_{bar}=E\theta,qquad
 d\kappa_{bar}=(L-D)\theta-EF.}                       \tag{2}
\]

Equation (2) is a genuine relative bar--Koszul square and its differential
squares to zero.  This is the strongest positive statement supplied by the
two committed constructions.

It is not the physical `kappa_i` square at the fixed grade `Gamma_*`.  The
first mismatch occurs before the cap top: on the compatible four-site face,
the normalized bar endpoint has mixed-colour covariance/output coefficients
and horizontal bar degree, while the selected response section requires the
pure-`q:00` fibre and its six-term vertical principal-parts face `db01`.
Tensoring with `K_Eq` does not change those tags.

At the cap the mismatch remains:

| tag | relative local-`GL3` bar times `K_Eq` | required `Gamma_*` cell |
|---|---|---|
| word role | complete input `01211222`, output/covariance interval | cap output word `01211222` reached from the response word |
| fine | mixed-colour `h_vY_0` covariance coefficients | six literal `t*q_(v,N)` occurrence degrees |
| repeated | raw squarefree `2K2` | repeated `P3+K2` |
| operation | local-`GL3` output bar x objectwise `K_Eq` | response-to-`AugP2` mixed orbit/`K_Eq` |
| occurrence | four-site covariance face | selected window `2345` occurrence idempotent |

Therefore

\[
       \Pi_{C_{phys,\Gamma_*}}(E\theta)=0             \tag{3}
\]

as a literal direct-sum projection.  It is zero because it is off-grade,
not because it constructs a tied physical `B/Eq` column.

The endpoint ordinary-residue class is `Psi`-dark.  The normalized bar has

\[
        \epsilon(L)=\epsilon(D)=1,\qquad\epsilon(E)=0, \tag{4}
\]

and the physical split-cap landing reads either endpoint as `h_vY_0` in
ordinary residue.  Since `Psi=delta.(B-Eq)/4` is zero on the ordinary-residue
row, it kills this class.  Nevertheless either endpoint remains nonzero in
normalized bar `H_0`; darkness does not make it a boundary.  The relative
difference `L-D` cancels the residue, but it still does not become the
selected occurrence section.

Consequently the relative bar edge does not force any of the eight
`lambda_i`.  If one additionally grants a source-labelled comparison which
retags (2) as the selected `Gamma_*` product, then the strict mapping-cone
normalization theorem applies and gives `B=Eq`, hence `lambda_i=0`.  That
grant is exactly the missing physical multiplicative `kappa` schema, so it
cannot be inferred from the bar interval itself.

Exact checker:
[`verify_h3_relative_gl3_bar_keq_kappa_normalization_gate.py`](../computations/verify_h3_relative_gl3_bar_keq_kappa_normalization_gate.py).

## 1. The relative product is real

Both `E` and `theta` are odd in the displayed presentation.  The derivation
law gives

\[
 d(E\theta)=dE\,\theta-E\,d\theta
            =L\theta-D\theta-EF.                     \tag{5}
\]

Taking another differential gives

\[
             LF-DF-(LF-DF)=0.                         \tag{6}
\]

No endpoint is discarded in (5).  In particular, the old obstruction that
neither `L` nor `D` is individually a normalized bar boundary does not stop
the existence of the relative two-cell.  This is why the present audit is
strictly stronger than asking whether the all-`L` endpoint is absolute.

It is important, however, to identify what (5) resolves.  Its degree-zero
objects are the two presentations of local covariance:

```text
L = output colour change,
D = contragredient source derivation.
```

Thus (5) belongs to the covariance/output bicomplex.  The standard
`kappa_i` normalization instead begins with a selected response section

\[
                         d\epsilon_i=b_i,              \tag{7}
\]

and then forms

\[
 d(\epsilon_i\theta)=b_i\theta-\epsilon_iF.           \tag{8}
\]

Replacing (7) by `dE=L-D` changes the operation parent and replaces the one
selected lower face by two covariance endpoints.  Formula (5) therefore
does not meet the hypothesis of the strict normalization theorem merely
because both expressions obey Leibniz.

## 2. The first literal mismatch is the selected `db01` face

The closest local face is deletion `v=1`, with residual sites `2,3,4,5` and
bar face word `2112`.  After granting the bar the most favourable multiplier
`p0*s1`, its all-`D` endpoint has the three terms

```text
p0*s1*q23:21*q45:12,
p0*s1*q24:21*q35:12,
p0*s1*q25:22*q34:11.
```

The selected response fibre is

\[
 b_{01}=p_0s_1(q_{23}^{00}q_{45}^{00}
              +q_{24}^{00}q_{35}^{00}
              +q_{25}^{00}q_{34}^{00}),              \tag{9}
\]

and its first physical principal-parts face is

\[
 db_{01}=p_0s_1\sum_{ab|cd}
          (dq_{ab}^{00}q_{cd}^{00}+q_{ab}^{00}dq_{cd}^{00}). \tag{10}
\]

Erasing colours and module roles makes the three coarse matching shapes in
the all-`D` endpoint and (9) agree.  Literally their supports are disjoint.
Moreover (10) has six vertical `dq` terms, whereas the all-`D` endpoint has
three horizontal-degree-zero terms.

The horizontal/vertical bidegrees are

```text
all-D endpoint       (0,0)
bar edge on b01      (1,0)
selected db01        (0,1)
bar edge on db01     (1,1).
```

The bar edge therefore does not turn a horizontal comparison into the
missing vertical selected face.  Acting on `db01` produces another
bidegree-`(1,1)` cell with boundary `L(db01)-D(db01)`, not `db01`.

The exact rank guard makes the same point.  In coordinates

```text
(selected db01, private dz01, all-D output endpoint),
```

the available graph face and retained endpoint are

```text
(-1,+1,0), (0,0,+1).
```

They have rank two.  Adding the selected face `(1,0,0)` raises the rank to
three and is detected by the primitive covector `(1,1,0)`.  Retaining both
bar endpoints relatively changes none of these vertical PP coordinates.

Thus the first obstruction is already:

```text
fine q colour + output/response module role + vertical PP degree.
```

The later `D4`, cap, and `K_Eq` factors cannot manufacture the missing
bottom face because multiplication preserves these direct-sum labels.

## 3. The full `Gamma_*` idempotent remains different

The terminal grade is

```text
word        01211222
fine        six literal t*q_(v,N) site-colour multidegrees
repeated    P3+K2
operation   response-to-AugP2 mixed orbit/K_Eq
window      2345 with literal occurrence labels.
```

The response word is `11110000`.  It differs from the cap word at sites

```text
P, 0, 2, 3, 4, 5,
```

and all six selected response fine degrees differ from their cap fine
degrees.  A physical cross-word placement must therefore carry a real
word/fine operation map; equality of an undecorated matching monomial is
not enough.

The complete seven-site normalized bar uses the nonzero part of
`01211222`, so it has the correct coarse input word for a target-zero
covariance calculation.  This does not make its output endpoint or its
operation word the response-to-cap arrow.  On the compatible local face,
its coefficient is the raw `2K2` hafnian `h_vY_0`.  The selected cap packet
has the repeated-site profile `P3+K2` and one of six literal
`t*q_(v,N)` fine degrees.

Tensoring by the central cone appends the `K_Eq` factor.  In the free
operation grammar it does not alter:

- source/output module role;
- response versus cap word idempotent;
- site-colour fine multidegree;
- raw `2K2` versus repeated `P3+K2`;
- selected occurrence/window label; or
- the pre-existing operation word.

Hence the strict product (2) is a physical relative cell in its own
bicomplex but has literal projection zero to `C_phys,Gamma_*`.

## 4. Ordinary residue is dark but protected

On every four-site face, the local covariance identity gives the same
polynomial value `h_vY_0` at every `L/D` corner.  Under the committed
split-cap landing, normalized augmentation is ordinary residue.  Therefore

```text
ores(L)=h_vY0,
ores(D)=h_vY0,
ores(E)=0,
ores(L-D)=0.
```

The balanced terminal covector is supported on the eight private/reduced-Eq
coordinates:

\[
             \Psi={1\over4}(\delta,-\delta,0_{ores}). \tag{11}
\]

It follows immediately that

\[
              \Psi(h_vY_0\,e_{ores})=0.               \tag{12}
\]

Thus the answer to the endpoint-residue question is **yes**: it is
`Psi`-dark.  But the normalized bar augmentation gives one on either
endpoint, so neither endpoint is a boundary.  The ordinary-residue row is
also one of the protected rows retained in `Y_phys,Gamma_*`; it may not be
deleted merely because the particular balanced covector ignores it.

This distinction explains why the relative construction is simultaneously
target-safe and insufficient.  The complete seven-site word makes the
target zero, and the endpoint difference cancels ordinary residue, yet the
relative edge still has the wrong physical source parent and fine grade.

## 5. Consequence for `lambda_i`

The strict normalization theorem says that an already physical selected
product has

\[
        \Pi_{B/Eq}(d\kappa_i)=(v,v),
        \qquad\lambda_i=\Psi(d\kappa_i)=0.             \tag{13}
\]

For the bar product, the actual statement is instead

\[
 \Pi_{B/Eq,\Gamma_*}(d(E\theta))=0
       \quad\hbox{because every face is off-grade}.   \tag{14}

Equation (14) does not evaluate a `kappa_i` column; it says that the column
is absent from the selected domain.  One cannot infer `lambda_i=0` for a
different, unconstructed operation merely because the bar product has zero
projection.

If one grants a comparison

\[
 E\longmapsto\epsilon_i
\]

which carries the local bar interval into the six selected response/cap
occurrence fibres and makes multiplication by `theta` a normalized
module/DGA map, then (13) follows immediately.  But that comparison must
itself supply `db01`, the word/fine placement, repeated `P3+K2`, the
`AugP2/K_Eq` operation parent, and the protected augmented rows.  It is
precisely the physical multiplicative `kappa` schema whose existence was
open in the first place.

## Shortest next datum

The shortest positive lemma is a source-labelled comparison from the
normalized covariance interval to the selected response-to-cap occurrence
interval, not another bar or cone identity.  It must:

1. send the compatible local face to the literal pure-`q:00` selected
   `db01`/graph packet;
2. carry all six `t*q_(v,N)` occurrence idempotents in repeated `P3+K2`;
3. land in the response-to-`AugP2` mixed operation parent at word
   `01211222`; and
4. preserve target, ordinary residue, `q`/anchor, `W`, ridge, eta, and sigma.

If that comparison is strict and normalized over `K_Eq`, the already
committed calculation forces all its `lambda_i` values to zero.  The local
bar interval alone neither constructs that comparison nor contradicts it.

## Reproduction

```bash
python3 computations/verify_h3_relative_gl3_bar_keq_kappa_normalization_gate.py
python3 computations/verify_h3_relative_gl3_bar_keq_kappa_normalization_gate.py --mode grade
python3 computations/verify_h3_relative_gl3_bar_keq_kappa_normalization_gate.py --mode residue
python3 computations/verify_h3_relative_gl3_bar_keq_kappa_normalization_gate.py --mode lambda
python3 -O computations/verify_h3_relative_gl3_bar_keq_kappa_normalization_gate.py
python3 -I -S computations/verify_h3_relative_gl3_bar_keq_kappa_normalization_gate.py
```

All modes print the same frozen ledger digest.
