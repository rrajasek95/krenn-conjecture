# The affine raw occurrence cut has the right residue but is not Gamma1

## Outcome

After granting the pointed primitive/common-carrier cell (p), the most
canonical shifted restriction--insertion candidate has exactly the required
coefficient normalization.  At occurrence order three,

\[
 {1\over2}\sum_e I_eD_e=1,
 \qquad
 \int_0^1t\,d\bigl(t(1-t)\bigr)=-{1\over6},
\]

so its reinserted top shadow is

\[
 \boxed{
 \Gamma_{\rm raw}^{\rm top}
   =-{1\over6}\,{1\over2}\sum_e I_eD_e
   =-{1\over6}\,1.}                                  \tag{1}
\]

Thus the affine raw cut really does produce the scalar in

\[
 d\Gamma _1(z)=-{1\over6}(r-2q)\chi(z).               \tag{2}
\]

It does **not** construct the physical source cell (Gamma _1).  Before
reinsertion, either of the two marked residual cuts has shifted component

\[
 -{1\over12}D_ec_{f,3}
   =-{5\over8}c_{f/e,2}-{13\over24}{\bf1}_2.           \tag{3}
\]

The primitive lower coordinate difference kills the constant term and reads
(-15/2) on (3).  The two marked cuts occupy separately labelled lower
occurrence summands.  Granting (p=(-Q,-\operatorname {ores})) and one
common (H_0) line cannot remove either centered component.  Consequently
the raw affine construction identifies the desired (L_1) column, but does
not prove (L_1\in\operatorname {im}D_Q).

Companion checker:
[verify_h3_gamma1_affine_raw_occurrence_cut_gate.py](../computations/verify_h3_gamma1_affine_raw_occurrence_cut_gate.py).

## 1. Exact affine normalization

Use the based loop

\[
                         \eta(t)=t(1-t).
\]

It preserves both endpoints and the unweighted carrier:

\[
 \eta(0)=\eta(1)=0,
 \qquad \int_0^1d\eta=0.
\]

Its first moment is

\[
 \int_0^1t\,d\eta
 =\int_0^1(t-2t^2)dt
 ={1\over2}-{2\over3}=-{1\over6}.                    \tag{4}
\]

For an order-three occurrence, every residual matching contains two edges.
Hence the exact restriction--insertion identity is

\[
                         \sum_eI_eD_e=2\,1.            \tag{5}
\]

Equations (4) and (5) prove (1).  This is the correct shifted calculation;
an unshifted (c_1) column is irrelevant because it lies in the (c_1)
coordinate, whereas (1) is the first affine/β face.

There is nevertheless no homological gain in (5).  The normalized raw
operator is the identity endomorphism of the coefficient module.  Multiplying
it by a path moment specifies the boundary *value* requested in (2); it does
not provide a degree-one source generator whose differential has that value.

## 2. The two lower centered debts

Let

\[
 c_{f,3}=90e_f-{\bf1}_3.
\]

For a marked residual edge (e), the exact restriction formula is

\[
 D_ec_{f,3}
 ={15\over2}c_{f/e,2}+{13\over2}{\bf1}_2,             \tag{6}
\]

while an unmarked edge gives (-{\bf1}_2).  The factor in one summand of
(1) is

\[
 {1\over2}\left(-{1\over6}\right)=-{1\over12}.
\]

This gives (3); an unmarked component becomes
(+{1\over12}{\bf1}_2).

Choose (g\ne f/e) and put

\[
                 \lambda_e=e_{f/e}^*-e_g^*.
\]

Then

\[
 \lambda_e({\bf1}_2)=0,
 \qquad
 \lambda_e\!left(-{1\over12}D_ec_{f,3}\right)
       =-{90\over12}=-{15\over2}.                    \tag{7}
\]

There are exactly two such marked (e).  Their covectors live on distinct
labelled lower-cut summands, so neither is cancelled by adding or identifying
constant carriers.  Reinsertion reconstructs the original centered class;
it does not show that the intermediate centered faces are boundaries.

## 3. What granting (p) does and does not grant

The already isolated first cell is

\[
                         p=(-Q,-\operatorname {ores})
\]

in the canonical cap grade.  Granting it supplies the primitive residue
section and allows one to compare the component constants with a common
(H_0).  As presently stated, it has no map to either twelve-coordinate
lower centered occurrence module in (6).  Therefore both covectors (7)
annihilate everything actually granted by (p).

One could strengthen the hypothesis by requiring (p)'s enriched pointed
comparison to carry the two centered values in (3).  That is not a
consequence of the existing cap theorem: it is precisely the additional
restriction-totalization theorem being sought.  In that strengthened form,
the required source statement is

\[
 \boxed{
 \text{a rho-compatible filler of the two marked }c_{f/e,2}
 \text{ faces, with zero complete augmented leakage}.}                 \tag{8}
\]

Only after (8) is supplied can the affine density (4) promote the
coefficient shadow (1) to a physical (Gamma _1).

## 4. Word, fine, and repeated-grade audit

The reinserted **top coefficient** has the desired declared labels:

~~~text
word                 01211222
fine grade           Q_(v,N)=t_v q_(v,N)
repeated-site type   P3+K2
~~~

Same-edge reinsertion restores the top occurrence and hence preserves those
labels at coefficient level.  But (D_e) factors through an order-two
occurrence module on the four undeleted occurrence sites.  The raw incidence
operator contains no physical map which:

1. decorates those lower centered coordinates with the full word/fine tail;
2. totalizes their PP/Hasse product-rule faces;
3. cancels the first known cross-word reset
   (h_v(H_0-u)e_{\rm Eq}); and
4. preserves protected, target, anchor, ordinary-residue, eta/sigma, (W),
   and physical-(q) rows.

Thus (1) is source-label preserving only after forgetting the intervening
chain faces.  It is not a proof that a source-valid chain exists in the full
`01211222`/`P3+K2` grade.

## 5. Sharp next finite theorem

Let (C_e^0) be the centered quotient of the lower occurrence module for a
marked cut.  The raw affine candidate has projection

\[
       \left(-{5\over8}c_{f/e_1,2},
             -{5\over8}c_{f/e_2,2}\right)
       \in C_{e_1}^0\oplus C_{e_2}^0.                 \tag{9}
\]

The shortest positive addition is a physical, rho-compatible mapping-cone
cell whose lower boundary is the negative of (9), whose reinserted top is
zero, and whose complete augmented boundary cancels the reduced-Eq reset.
Equivalently, append that candidate to the complete boundary (D_Q) and
test the two labelled columns by exact rank.  Failure produces a cokernel
covector extending at least one (lambda_e).  It becomes a physical
terminal only if it also annihilates all protected and physical-(q) source
columns.

This is strictly sharper than asking for another (c_1) identity.  The
moment identity and its (-1/6) normalization are already exact; what is
missing is the shifted restriction-totalization cell.

## Scope

Proved here are the affine moment, the normalized top action, the exact
marked and unmarked lower components, and the two constant-killing
detectors.  Also proved is that the presently stated (p)/common-(H_0)
grant does not by itself supply those components.

Not proved is nonexistence in the complete physical source complex.  A new
PP/Hasse lower-centered filler may exist.  Nor are the occurrence covectors
in (7) asserted to be physical terminal readouts before the complete
augmented membership problem is built.

## Verification

Run

~~~text
python3 computations/verify_h3_gamma1_affine_raw_occurrence_cut_gate.py
python3 -O computations/verify_h3_gamma1_affine_raw_occurrence_cut_gate.py
python3 -I -S computations/verify_h3_gamma1_affine_raw_occurrence_cut_gate.py
~~~
