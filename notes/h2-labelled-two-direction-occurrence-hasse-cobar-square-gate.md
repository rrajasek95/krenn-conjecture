# One occurrence has a finite labelled Hasse square; its pointed cap is the first physical face

## Verdict

For the literal lower occurrence

\[
 f=(p_0^0,s_1^1,q_{45}^{12})
\]

in word `0112`, the two ordered site-root directions

\[
 a=E_{10}^{(0)},\qquad b=E_{01}^{(4)}
\]

give an explicit labelled square

```text
              A0
       0112 ------> 1112
        |             |
     B0 |             | B1
        v             v
       0102 ------> 1102.
              A1
```

The roots act on different literal factors and therefore commute.  They
recolour the fine grade but preserve the structural occurrence tag
`(p_site=0,s_site=1,residual_sites=(4,5))`.  With the ordered-bar signs

\[
 [a|b]\longmapsto A_0+B_1,
 \qquad
 [b|a]\longmapsto -(B_0+A_1),
\]

the unsigned Boolean-cobar face `[a|b]+[b|a]` realizes

\[
                  dQ=A_0+B_1-A_1-B_0,
                  \qquad d^2Q=0.                 \tag{1}
\]

Thus the finite two-direction totalization is not the problem.  One
**pointed, source-valid occurrence section**, stable under these two root
principal-parts operators and under `q23` reinsertion, would functorially
generate this whole square.  The currently committed complete-response
source row does not provide that marked section.  Its first absent physical
face is the pointed occurrence/global cap.  Conditional on this cap, the
square's target commutator cancels; reinsertion then exposes the nonzero
labelled `dq23` conormal.

Checker:
[`verify_h2_labelled_two_direction_occurrence_hasse_cobar_square_gate.py`](../computations/verify_h2_labelled_two_direction_occurrence_hasse_cobar_square_gate.py).

## 1. Bar signs and the occurrence tag

Write `00`, `10`, `01`, `11` for applying neither root, only `a`, only
`b`, or both.  Give every edge the boundary `target-source`.  Then

\[
\begin{aligned}
 dA_0&=10-00, & dA_1&=11-01,\\
 dB_0&=01-00, & dB_1&=11-10.
\end{aligned}
\]

The two ordered paths are `A0+B1` and `B0+A1`.  The Koszul/desuspension
sign on the reversed path gives (1), since

\[
 (10-00)+(11-10)-(11-01)-(01-00)=0.
\]

This is the cubical realization of the pinned reduced Boolean cobar

\[
 \Delta'\{a,b\}=\{a\}|\{b\}+\{b\}|\{a\}.
\]

The plus sign in the coalgebra and the minus sign on the reversed geometric
path are compatible: the latter is the totalization/Koszul sign.  Discarding
the labels erases precisely this cancellation and produces the previously
observed nonnilpotent recursive `(B-4)^{-1}` repair.

The occurrence tag is structural, not a word label.  At the four vertices
the factors are

```text
00: p0^0 s1^1 q45^12     word 0112
10: p0^1 s1^1 q45^12     word 1112
01: p0^0 s1^1 q45^02     word 0102
11: p0^1 s1^1 q45^02     word 1102.
```

Only colours change; the marked endpoint, spectator endpoint, and residual
edge remain the same literal occurrence.

## 2. What is source-provenant

The committed physical Cartan theorem proves that the local root vector
fields act termwise on **complete matching rows**, and the complete
Hasse/principal-parts theorem totalizes their product-rule faces.  Therefore
the square above exists canonically in the ambient complete PP source
resolution.

That statement does not split a complete response row into its twelve
occurrences.  If `e_f` is the marked coordinate and `1` is the complete row,
then the covector `e_f^*-e_g^*` kills `1` and reads one on `e_f`.  Hence root
naturality cannot by itself turn `e_f` into a physical relative source
column.  The missing datum is exactly a pointed occurrence/global section,
equivalently the first conormal comparing the marked occurrence value with
the common response value.

This gives the sharp conditional theorem:

> If one occurrence section is physical, pointed, and functorial for the two
> displayed root PP operators and `q23` multiplication, then its four root
> translates and the two ordered paths form (1).  No recursively generated
> unlabelled cells are needed for this occurrence.

This is a theorem for one occurrence.  It does not say that an untyped seed
spans the other marked-site orbits.

## 3. Augmented faces

The word/fine objects at the four corners are distinct, as they must be in
the physical grade quiver.  The repeated `P3+K2` reinsertion label is held
fixed.  On the target, `a` and `b` act at distinct sites, so the two ordered
paths end at the same word `1102`; their commutator target face is zero.
Individual edges may still have mixed-target normals—the cancellation is a
four-face statement, not a claim that each edge is target-zero.

The first physical failure occurs before this target cancellation can be
used: there is no source-valid marked occurrence section with its pointed
cap.  If that cap is granted, the product rule for the literal reinsertion
is

\[
                 d(q_{23}S)=q_{23}\,dS+dq_{23}\,S.       \tag{2}
\]

For the exact private `(B-4)` preimage `z_private`,

\[
 \sum_i(z_{\rm private})_i=0,
 \qquad
 (e_0+e_3-e_1-e_6)(z_{\rm private})={35\over72}.       \tag{3}
\]

Thus scalar ordinary residue sees zero, while the occurrence-labelled
`dq23` cap/conormal is nonzero.  Aggregate residue or the target/Eq cone
cannot remove it.  A positive physical construction must attach the
pointed occurrence section with this labelled face; a bare complete-row
Cartan square is insufficient.

## Scope

The result is exact for one literal `0112/q23:21` occurrence and its two
ordered roots.  It constructs the source-side labelled square and locates
the first physical comparison face.  It does not construct the pointed
section, extend the labelled detector over physical `q` and terminal rows,
or prove that one seed covers the other occurrence/site orbits.

Run:

```text
python3 computations/verify_h2_labelled_two_direction_occurrence_hasse_cobar_square_gate.py
python3 -O computations/verify_h2_labelled_two_direction_occurrence_hasse_cobar_square_gate.py
python3 -I -S computations/verify_h2_labelled_two_direction_occurrence_hasse_cobar_square_gate.py
```

Frozen ledger SHA-256:

```text
6006cc5db1e07d60cd2dc724ba5c6c0b7335a2afb64e294bdebb9332736dd490
```
