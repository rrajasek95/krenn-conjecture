# Complete Hasse/Cartan naturality: the first missing physical square

## Verdict

Applying the Cartan homotopy to the **complete** Hasse/cosimplicial
totalization proves a coherent source-side statement, but it does not prove
the selected Gate-I equality

\[
J_3(M_v)=A\,J_{\rm col}(u_{024}-u_{012}).
\]

The first failure is not Cartan naturality. It is the absent comparison from
the principal-parts/Hasse source resolution to the literal repeated-grade
augmented correction complex. In the first coefficient-prolongation degree,
that absent chain-map square is detected exactly by the already isolated
one-term face \(\xi\).

The executable certificate is
`computations/verify_h3_complete_hasse_cartan_naturality_square_gate.py`.

## The square that really commutes

Let \(F\) be the perfect-matching tensor polynomial map. The committed Ward
calculation proves that the coefficient-space root field and the output root
field are \(F\)-related on every complete matching row. Therefore

\[
\begin{CD}
\Omega^k(\text{output}) @>{\iota_{X_{\rm out}}}>>
\Omega^{k-1}(\text{output})\\
@V{F^*}VV @VV{F^*}V\\
\Omega^k(\text{coefficient PP source}) @>{\iota_{X_{\rm src}}}>>
\Omega^{k-1}(\text{coefficient PP source})
\end{CD}
\]

commutes. On functions this is the Ward identity. On one-forms it is
\(\iota_{X_{\rm src}}d(F^*f)=F^*(X_{\rm out}f)\), and the identity extends to
all forms because contraction is a degree-minus-one derivation. Hasse
translation is an algebra map, so this remains valid throughout the complete
principal-parts/cobar totalization. Thus the higher faces, including the face
containing \(\xi\), belong to one coherent source-side totalization rather
than being independent source equations.

## The square that is still missing

The Gate-I square has different objects:

\[
\begin{CD}
U_{15} @>{\Phi}>> L_{h=3}\\
@V{J_{\rm col}}VV @VV{J_3}V\\
E_{\rm col}^{\rm aug} @>{A}>> E_{h=3}^{\rm aug}.
\end{CD}
\]

Here \(U_{15}\) is the physical collision quotient, \(L_{h=3}\) is the
canonical repeated-grade correction domain, and the lower objects contain the
literal private features and augmented rows. The polynomial pullback \(F^*\)
has none of these source or target types. Naturality cannot create \(\Phi\),
\(J_{\rm col}\), or a chain comparison \(\Pi\) from the PP totalization to
this diagram.

The first required chain-map identity would be

\[
\Pi_1 d_{\rm PP}=d_{\rm corr}\Pi_0
\]

on the coefficient-prolongation faces. It is not defined at

\[
\xi=\frac43
q_{01}^{01}q_{27}^{21}q_{34}^{11}q_{35}^{12}q_{67}^{22}.
\]

In its exact fine degree there are only two compatible old complete full-row
columns. Both contain a forced \(q_{37}\), while \(\xi\) does not. Hence

\[
\lambda_\xi=\frac34e_\xi^*
\]

vanishes on both columns and reads one on \(\xi\). This is the first exact
failure of the proposed comparison, not a failure of the source Cartan
identity. A new chart-nondiagonal relative Spencer cell could still repair it;
the certificate is not a universal no-go.

## Augmented readouts

- Endpoint oddization kills the Weyl target defect on the polynomial/output
  word side.
- The residual value \(D_2=-\delta\) is exact after the committed
  grade-forgetting projection. This does not define a termwise private
  90/360-feature map.
- Literal private features and the \(D,W,\mathrm{ainc},\mathrm{Eq}\) rows have
  no induced value until the missing comparison is constructed.
- The order-six operator commutes formally with the terminal Kähler ridge,
  but the pinned ridge audit explicitly leaves the physical labelled
  repeated-grade tensor product unconstructed. Thus \(\eta/\sigma\) do not
  descend merely from naturality.

So the complete totalization improves the interpretation of \(\xi\): it is a
boundary **face in a source-side coherent system**, not an isolated failure of
source closure. It does not yet make \(\xi\) a boundary in the physical
correction complex. The smallest live datum remains one exact
chart-nondiagonal relative Spencer cell, with its transported mate and full
augmented readout.

## The explicit three-term bridge does not supply that cell

There is a tempting fine-homogeneous expression

\[
m\bigl(q_{35}^{12}q_{67}^{22}
       +q_{36}^{12}q_{57}^{22}
       +q_{37}^{12}q_{56}^{22}\bigr),
\qquad
m=q_{01}^{01}q_{27}^{21}q_{34}^{11}.
\]

Its first term is the monomial underlying \(\xi\), and its third term is
literally in one of the two compatible 90-term columns: it is
\(q_{37}^{12}\) times the matching
\(q_{01}^{01}q_{27}^{21}q_{34}^{11}q_{56}^{22}\). The middle term contains
the forbidden direct pair \(q_{36}\). Exact enumeration therefore gives

\[
(\text{membership in the old full-row block})=(0,0,1).
\]

This does not yet transport \(\xi\) to its third-term mate. The parenthesis
is the ordinary all-plus four-site Hafnian. In the labelled Boolean cobar, a
four-occurrence block has fourteen ordered nontrivial splits: six ordered
\(2+2\) splits (the two orders of these three commutative pairings) and eight
\(1+3/3+1\) splits. Thus the displayed parenthesis is a nonzero
\(2+2\)-sector of a Hasse face, not the complete alternating boundary of a
relative bar cell. Projecting away \(q_{36}\) deletes the middle monomial; it
does not impose

\[
q_{35}^{12}q_{67}^{22}+q_{37}^{12}q_{56}^{22}=0.
\]

The bridge is nevertheless informative: it finds exactly the complete-row
mate to which a missing PP/Weyl cell should route \(\xi\). Such a cell must
also carry the complementary Hasse sectors, the transported mate, and the
literal augmented readouts. The three-term Hafnian alone is not that cell.
