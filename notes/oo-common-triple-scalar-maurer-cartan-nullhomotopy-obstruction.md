# The scalar Maurer--Cartan contraction returns the whole diagonal graph

## Outcome

The determinant-cleared connection must be tested in the scalar fixed-word
coefficient ring, not by multiplying pure target tensors.  In the physical
site-square-zero bookkeeping algebra one has

\[
                 X_0X_1=X_0X_2=X_1X_2=0,                       \tag{1}
\]

but this does **not** invalidate scalar determinant clearing.  After
coefficient extraction the three pure equations are scalar source
polynomials

\[
                         F_0-1=F_1-1=F_2-1=0,                  \tag{2}
\]

so `F0 F1 F2` is a unit in the coefficient quotient.  The computation
below uses (2) and keeps the physical matching and target provenance as
tags.

The result is negative, for a sharper reason.  Put `T` for the literal
two-term curvature target and `R` for the ten-column/six-matching Bianchi
normal packet from commit `cfb03ff`.  The two labelled diagonal anchors
give the exact graph relation

\[
 D^{pq}_{pq\mid rs}-D^{pr}_{pr\mid qs}=-(T+R).                 \tag{3}
\]

The determinant-cleared adjugate/Maurer--Cartan curvature is

\[
                         -\kappa(T+R),                         \tag{4}
\]

which equals `kappa` times the literal diagonal row in (3).  Thus it is a
boundary and kills both the target and the normal residue.  The desired
target-free class

\[
                             -\kappa R                         \tag{5}
\]

is not obtained by adding diagonal-anchor multiples.  The integral
covector has

\[
 \Lambda(T)=1,qquad \Lambda(R)=-1,qquad
 \Lambda(T+R)=0,qquad \Lambda(-\kappa R)=\kappa.              \tag{6}
\]

Since `kappa` is a unit on the curved OO chart, (6) is the smallest exact
residual.  The proposed scalar connection is valid and source-polynomial,
but it reproduces the already-known cap graph rather than the missing
connection-to-diagonal nullhomotopy.

## The determinant-cleared response frame

At the selected curvature component, embed the direct square in the full
three-colour response frame

\[
 K=\begin{pmatrix}
       A&B&0\\ F&U&0\\0&0&1
    \end{pmatrix},qquad \kappa=AU-BF.                          \tag{7}
\]

The third diagonal entry is normalized using the scalar pure equation in
(2).  The exact polynomial adjugate is

\[
 \operatorname {adj}(K)=
 \begin{pmatrix}
 U&-B&0\\-F&A&0\\0&0&\kappa
 \end{pmatrix},qquad
 K\operatorname {adj}(K)=\kappa I_3.                          \tag{8}
\]

No direct entry is divided.  With the selected columns and adjugate rows

\[
 c_1=\binom AF,quad c_2=\binom BU,quad
 \lambda=(-F,A),quad\eta=(U,-B),                              \tag{9}
\]

one has

\[
 \lambda c_1=\eta c_2=0,qquad
 \lambda c_2=\eta c_1=\kappa.                                \tag{10}
\]

These are exactly the two determinant-cleared curvature contractions.  In
the target-augmented coefficient complex, the two copies in (10) force the
complete target/residue graph (4), just as the bounded scalar filtered
calculation in
[`h3-target-augmented-filtered-d2-first-obstruction.md`](h3-target-augmented-filtered-d2-first-obstruction.md)
does.  Replacing the graph by (5) deletes its target coordinate and breaks
the connection square by `kappa T`.

The use of the selected block in (7) is not an abstract truncation.  For
the fine word

\[
                         (a,0,1,\ell,2,2,2,2),                  \tag{11}
\]

the checker begins with all 18 labelled full-nine rows.  Fine-degree
selection leaves exactly the `pq:(a,0)` and `pr:(a,1)` mixed rows and the
two labelled `22` anchors; every other response channel has a different
physical colour word.  Equation (7) is the determinant-cleared scalar
frame on precisely this projected component, with pq/pr labels retained.

## Literal matching graph

Let

\[
 L=M_{pq\mid rs}-M_{pr\mid qs}.                               \tag{12}
\]

The minimal K6 potential row gives `R=-L`.  On the other hand, the source
part of the diagonal difference in (3) is `L`, while its target part is
`-T`.  Hence

\[
 D^{pq}_{pq\mid rs}-D^{pr}_{pr\mid qs}
       =L-T=-R-T,                                             \tag{13}
\]

which proves (3) without quotienting or cancelling a matching power.
Both sides are sparse vectors in the same 108-feature source/target space.

The integral covector from the two-edge obstruction kills each of the six
labelled diagonal columns separately.  It reads `-1` on `R` and `+1` on
`T`, so it kills the complete graph in (13).  Multiplying by any scalar
coefficient polynomial, including the pure units in (2), preserves this
conclusion.  In particular,

\[
 \Lambda\bigl(-\kappa(T+R)\bigr)=0,qquad
 \Lambda(-\kappa R)=\kappa\ne0.                              \tag{14}
\]

Thus no determinant-cleared scalar combination of (4) and the literal
diagonal rows can equal (5).

## Consequence and scope

This test does not rule out every nonlinear use of all scalar coefficient
equations.  It rules out the specific flat-frame/Maurer--Cartan candidate:
after valid scalar localization, its curvature is exactly the common
diagonal cap graph and hence zero modulo that graph.  It has no target-free
normal component.

The missing operation remains precisely the one isolated in `cfb03ff`: a
source-provenant connection-to-diagonal nullhomotopy whose boundary cancels
the target part `kappa T` while retaining the normal part `-kappa R`.
Another Bianchi row, another diagonal adjugate, or another coefficient
order merely re-presents (3)--(4).

## Reproduction

Run

```text
python3 computations/verify_oo_common_triple_maurer_cartan_grade_obstruction.py
python3 -O computations/verify_oo_common_triple_maurer_cartan_grade_obstruction.py
```

The checker distinguishes tensor/Hasse and scalar coefficient
multiplication, verifies the full `3x3` adjugate (8), audits all nine colour
normalizations and their 18-row fine-degree projections, expands (3)
matching by matching, and verifies the four pairings in (6) over the exact
polynomial `kappa=AU-BF`.  The frozen ledger digest is

```text
5993f5eed23db28579d2b0bbbd57d49e35daf224432e204bd16947ff4097f540
```
