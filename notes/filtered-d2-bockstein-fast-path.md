# The shortest live overlap target is a filtered \(d_2\), not a raw landing row

Research target only.  Krenn's conjecture remains open,
`SP-CLEAN-BRIDGE` is untouched, and no certified dependency changes.

## 1. Outcome

The raw fixed-block coefficient cut is not the only possible organization
of the complete two-chart program.  A more economical proof experiment is
to construct one target-augmented, three-step filtered source complex and
compute a single second differential.  For that experiment to feed the
unified theorem, its \(d_2\)-class must additionally have the typed,
zero-indeterminacy, and homological-faithfulness properties stated below.

This distinction matters because the current and forthcoming source-grade
guards test a statement of the form

\[
 \operatorname {pr}_{\rm bad}{\mathscr X}=dB,
 \qquad \operatorname {tar}{\mathscr X}=0,
 \qquad \operatorname {pr}_{\rm low}{\mathscr X}={\cal N}.
\tag{1}
\]

A guard in which the proposed landing row raises the literal row rank
disproves (1).  It does **not** disprove the weaker filtered statement: the
bad component may be nonzero as a chain, become a boundary on the first
page, and leave a nonzero \(d_2\)-class in the low quotient.  Such a class
is only a candidate for the target-zero, curvature-weighted odd residue
required by the inactive ledger.  It becomes a single physical value only
after the target/residue readout is proved to descend through the
first-page indeterminacy.

The elementary lemma below makes this precise.  Its application does not
construct the physical complex.  The live theorem is to build that complex
from the literal all-label two-chart rows, including target augmentation,
construct a physical readout \(\rho_c\) on the relevant \(E_2\)-quotient,
and prove

\[
             \rho_c\bigl(d_2[\mathscr X]\bigr)
                    =(0,-\kappa\overline Y_c)
\tag{2}
\]

for one surviving label \(c\).  The first coordinate in (2) is the
physical target and the second is the odd residue.  Equation (2) is not an
equality in the raw low chain group.  On the rootless ledger the same
filtered class must instead be sent by a separately constructed nonzero
readout to the residual Macaulay quotient.  A uniform theorem needs both
typed readouts and the relevant homological faithfulness; (2) is only the
already reduced inactive value.

## 2. The three-step lemma

Let \(C^\bullet=G_0^\bullet\oplus G_1^\bullet\oplus G_2^\bullet\) be a
cochain complex over a field.  Suppose its differential decomposes by
filtration drop as

\[
                  d=d_0+d_{-1}+d_{-2},
 \qquad d_{-j}(G_r)\subseteq G_{r-j},
\tag{3}
\]

where a summand with a negative index is zero.  The equations in \(d^2=0\)
at filtration drops zero, one, and two are

\[
 d_0^2=0,\qquad
 d_0d_{-1}+d_{-1}d_0=0,\qquad
 d_0d_{-2}+d_{-1}^2+d_{-2}d_0=0.
\tag{4}
\]

Use the increasing filtration
\(F_rC=\bigoplus_{i\le r}G_i\), and number the spectral sequence so that
\(E_1=H(G,d_0)\).  Thus \(d_1\) is induced by \(d_{-1}\) and lowers the
displayed grade by one.  All page and sign statements below use this
convention.

> **Lemma 2.1 (explicit filtered \(d_2\)).**  Let \(x\in G_2^n\) satisfy
> \(d_0x=0\), and suppose the first-page obstruction vanishes:
> \([d_{-1}x]=0\) in \(H^{n+1}(G_1,d_0)\).  Choose
> \(y\in G_1^n\) with
> \[
>                         d_0y=-d_{-1}x.                 \tag{5}
> \]
> Then
> \[
>                  \beta_2(x,y)=d_{-2}x+d_{-1}y\in G_0^{n+1}
> \tag{6}
> \]
> is a \(d_0\)-cycle.  With
> \[
> d_1[z]=[d_{-1}z],\qquad
> E_2^{0,n+1}=
> {H^{n+1}(G_0,d_0)\over d_1H^n(G_1,d_0)},                \tag{6a}
> \]
> its class in \(E_2^{0,n+1}\) is independent of the choice of \(y\)
> and is the second differential
> \(d_2[x]\in E_2^{0,n+1}\), for
> \([x]\in E_2^{2,n-2}\), of the filtration spectral sequence.

**Proof.**  Equations (4), \(d_0x=0\), and (5) give

\[
\begin{aligned}
 d_0\beta_2(x,y)
 &=d_0d_{-2}x+d_0d_{-1}y\\
 &=-d_{-1}^2x-d_{-1}d_0y=0.
\end{aligned}
\]

If \(y'\) is another choice, then \(z=y'-y\) is a \(d_0\)-cycle and

\[
                  \beta_2(x,y')-\beta_2(x,y)=d_{-1}z,
\]

which is precisely a first differential from \(H(G_1,d_0)\).  The usual
change of the representative can be checked explicitly.  If
\(x'=x+d_0w\), take \(y'=y+d_{-1}w\).  Then (4) gives

\[
 \beta_2(x',y')-\beta_2(x,y)
   =d_{-2}d_0w+d_{-1}^2w=-d_0d_{-2}w.                    \tag{6b}
\]

There is no incoming first differential at the top filtration grade
\(G_2\).  Thus (6a) is exactly the \(E_2\)-class represented by (6).
\(\square\)

The signs in (5)--(6) are forced by the corrected lift \(x+y\):
\(d_0y=-d_{-1}x\) cancels its grade-one differential, and the remaining
grade-zero term is \(d_{-2}x+d_{-1}y\).  Reversing the orientation of the
two-chart comparison cell reverses \(x,y\), and hence the physical value.
Lemma 2.1 therefore fixes the relative plus sign in (6), but it does not
by itself prove the normalization
\(-\kappa\overline Y_c\) in (2); that sign must be inherited from the
oriented five-site and scalar-zero cap rows.

The lemma is deliberately smaller than a homological-perturbation theorem.
No inverse series and no acyclicity of the whole middle grade are required.
The price is visible: the output lives modulo the first-differential image.
A chain-level target/residue map first has to kill \(d_0\)-boundaries so
that it descends to \(H(G_0,d_0)\).  Its value is then single-valued on
(6a) exactly when it also kills

\[
 d_1H^n(G_1,d_0)\subseteq H^{n+1}(G_0,d_0).               \tag{6c}
\]

This is the precise zero-indeterminacy condition for this three-step
model.  Contractibility of the complete-anchor relative kernel would be a
strong sufficient mechanism for (6c), but neither Lemma 2.1 nor the
existing physical rows prove it.

## 3. Physical dictionary

The proposed source complex should use the following grades.

| Filtered piece | Physical content |
|---|---|
| \(G_2\) | the source-faithful five-exposed-site comparison cell, with its crossed four-index coefficient and curvature orientation |
| \(G_1\) | the connection, normal, direct/internal companions and the target-augmented scalar-zero cap lifts |
| \(G_0\) | the proposed low response carrier; its homology must admit the physical target and odd-residue readout (and, separately, the rootless divisor/Macaulay readout) |
| \(d_0\) | literal same-grade source identities before cancelling a matching power |
| \(d_{-1}\) | coefficient exposure and the cap-multiplication section defect |
| \(d_{-2}\) | the direct low-grade landing correction |

The formal site-occupancy note already constructs a coefficient-one
exposure section and proves that it commutes with the chart-symbol
differential.  It also computes the failure of that section to commute
with evaluated cap multiplication: on the scalar-zero cap, the resulting
one-chart class is \(-\overline Y_c\).  These are source data from which
one hopes to define \(d_{-1}\); a section and its defect are not
themselves a differential component.  The formal split supplies neither
the grading decomposition above nor the equations \(d^2=0\) for the
evaluated target-augmented complex.

What is absent is the **single total differential** containing both chart
comparison and target-augmented cap multiplication.  Without it, equations
(4) are not available and calling the section defect a Bockstein is only an
analogy.  Constructing the total differential is the substantive source
problem.

If it is constructed with the selected physical orientation, the desired
second composition must retain the curvature determinant

\[
                         \kappa=AU-BF\ne0.               \tag{7}
\]

The desired computation is then (2), interpreted through the quotient
(6a).  The five-site ledger fixes the requested normalization, but does
not prove that this coefficient is the second composition.  This route is
weaker than (1): neither the raw bad-grade projection nor the raw low-grade
projection has to equal its final value separately.

## 4. Why this is the faster proof experiment

There are three coarse diagnostic outcomes of the proposed bounded
\(h=3\) construction.

1. The target-augmented rows do not form a filtered complex: one component
   of \(d^2\) is a new, explicitly named physical obstruction.  Realizing
   or cancelling that component is the next exact target for this route.
2. They form a complex, but the middle common mode survives and the readout
   does not kill its first-differential image.  This gives a sharp
   zero-indeterminacy counterguard and rules out this proposed
   single-valued secondary operation.  A deliberately quotient-valued
   operation would have to state its larger indeterminacy instead.
3. They form a complex and the readout is well defined.  Computing (6) then
   either gives (2) or gives an exact different residue.  In the former
   case, the certificate--bracket theorem handles every higher coefficient
   uniformly in \(h\) only after the quotient class is lifted to the typed
   source-filtered normal value
   \(\tau_c(\gamma z)=\gamma\widehat\zeta_c\).  Excluding the routed
   inactive branch still requires the existing comparison-chain and
   restricted homology-injectivity hypotheses.

Thus the first experiment is finite and diagnostic.  Outcome 3 would
close neither **SP-CLEAN-BRIDGE** nor even the routed inactive branch
without those additional typing and faithfulness results.  The experiment
does not attempt a 252-variable, 6561-equation elimination for the full
\((8,3)\) system, and it does not reopen the branch-by-branch level-two
census.

## 5. Relation to the unified theorem

The
[unified full-nine two-chart saturation theorem](unified-full-nine-two-chart-overlap-jet-saturation-target.md)
still has four logical components: tilted/direct-free overlap;
anchor/selector or maximal-shore conversion; the rootless residual
Macaulay annihilator; and inactive/mixed boundary exactness.  Lemma 2.1
does not prove any of them.

Its role is architectural.  A single physical filtered complex could package
the last two components without demanding a false raw landing identity:

* the inactive readout of its \(d_2\), after (6c), is proposed to be (2);
* the rootless readout is a separately constructed nonzero element of
  \((S_{2h-1}/fS_{h-1})^*\), extracted from the same filtered class and
  required to annihilate the residual clean-coordinate shifts; and
* a mixed assignment uses the two readouts on the two ends of the same
  comparison cell, rather than manufacturing an identification between
  unrelated branch certificates.

The same complete anchors and crossed row which enter Component II are the
natural candidates for killing the relative middle kernel and making
(6c) hold.  Their existence does not imply that kernel is contractible;
this is precisely the zero-indeterminacy problem.

At \(N=8\), proving the resulting clean bridge is equivalent to proving the
open \((8,3)\) case.  This is therefore a more economical organization of
the final proof, not a logically easier intermediate statement.  A
standalone inactive \(d_2\)-value is not the clean bridge.

## 6. Nonclaims

1. No target-augmented physical filtered complex is constructed here.
2. The formal occupancy splitting alone is not such a complex.
3. The physical readout \(\rho_c\), the value (2), zero indeterminacy, and
   the nonzero rootless Macaulay readout are unproved.  Even (2) would not
   by itself give the typed radial-to-response transgression, the
   comparison-chain injection, an active clean point, or the mixed-ledger
   theorem.  At trace zero the existing cap rows have zero radial symbol,
   so a relation-level \(d_2\) would still need a separate source-filtered
   normal value.  An \(h=3\) complex also does not automatically prolong to
   all \(h\); only the coefficient correction after a typed radial
   transgression is already uniform.
4. A raw-row counterguard does not prove or disprove the filtered \(d_2\).
5. Nothing here changes `SP-CLEAN-BRIDGE`, the certified spine, or the
   status of Krenn's conjecture.

## 7. Inputs

* [`site-occupancy-bockstein-partial-matching-flatness.md`](site-occupancy-bockstein-partial-matching-flatness.md)
  supplies the split formal occupancy module and computes its cap section
  defect.
* [`five-exposed-site-yoneda-cup-obstruction.md`](five-exposed-site-yoneda-cup-obstruction.md)
  identifies one natural five-site restriction--insertion degree and the
  target/residue lock; it does not prove that factorization is necessary.
* [`residue-chain-map-radial-transgression.md`](residue-chain-map-radial-transgression.md)
  proves that the certificate--bracket coefficient correction is formal
  after one typed radial-to-response transgression; it does not construct
  that transgression or the comparison exactness.
* [`uniform_adjacent_cycle_filtered_prolongation.md`](uniform_adjacent_cycle_filtered_prolongation.md)
  separates the raw landing identity from the zero-indeterminacy route and
  records the additional comparison-chain/injectivity hypotheses needed
  after an inactive readout.
* [The unified full-nine two-chart saturation target](unified-full-nine-two-chart-overlap-jet-saturation-target.md)
  places this construction inside Components III--IV and keeps the
  complete-anchor relative kernel as an explicit unproved interface.
* [`clean-bridge-at-eight-is-the-open-case.md`](clean-bridge-at-eight-is-the-open-case.md)
  records the exact complexity status of the final implication.
