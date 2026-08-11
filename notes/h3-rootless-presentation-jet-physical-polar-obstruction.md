# The committed presentation jets do not yet define one physical rootless polar column

Exact type obstruction. This note audits the smallest proposed physical
construction of one column \(P(e_v)\) in the rootless augmented-pentagon
Fredholm alternative. It proves that the shifted principal-parts candidates
have two possible readings, neither of which supplies the required physical
invisible first jets. It does not rule out other source constructions.

## Outcome

For each deleted odd site \(v\), the committed shifted comparison uses the
mixed word \(c_v\), the marked cells

\[
 u_v=a_{xv}^{00},\qquad t=a_{pq}^{00},
\]

and two chart-tagged copies of one direct-free physical hafnian row. The
literal derivatives have

\[
 \#\partial_{u_v}H_{c_v}=
 \begin{cases}15,&v=r,\\12,&v\ne r,\end{cases}
 \qquad
 \#\partial_tH_{c_v}=15,
 \qquad
 \#\partial_t\partial_{u_v}H_{c_v}=3.                 \tag{1}
\]

There are then exactly two readings.

1. If \(u_v,t\) are read as physical coordinate tangent vectors, their
   first derivatives in (1) are nonzero. Hence they fail

   \[
      \widehat J\xi_v=\widehat J\eta_v=0               \tag{2}
   \]

   already on this one literal mixed source row. Adding target and ordinary
   residue rows cannot repair failure of the source-boundary component.

2. If the candidates are read as the committed pq-copy minus pr-copy
   presentation jets, their boundaries cancel. But forgetting the chart
   tag maps each difference to zero in the single physical source module.
   Thus their physical images are \(0,0\), whose mixed Hessian is

   \[
                        \widehat H(0,0)=0,              \tag{3}
   \]

   not the nonzero three-term sector symbol in (1).

Consequently the chart-filtered three-term polar is a genuine second
difference in the presentation/Rees filtration, but it is not yet a
physical mixed-Hessian correction column. In particular, none of the five
formal symbols currently defines even one source-valid \(P(e_v)\) for the
Fredholm alternative of h3-rootless-augmented-pentagon-fredholm-alternative.

## Exact scope of the augmented correction

The complete physical construction would have to start with vectors in the
physical source-coordinate module, not in a duplicated row presentation:

\[
 \xi_v,\eta_v\in V_{\rm src},\qquad
 \widehat J\xi_v=\widehat J\eta_v=0.                  \tag{4}
\]

Only after (4) exists is the mixed correction question defined:

\[
 \widehat J\zeta_v=-\widehat H(\xi_v,\eta_v).          \tag{5}
\]

Here \(\widehat J\) must include the source boundary, physical target, and
ordinary-residue rows. The mixed word in (1) has target zero, and the
three-term symbol has the expected fine degree. Those two facts do not
supply (4), an ordinary-residue-compatible \(\zeta_v\), or the source grade
map into the response-grade terminal face.

Likewise, zero indeterminacy cannot yet be tested. Once one solution of
(5) and a terminal landing \(q\) have been constructed, its value is
independent of the correction precisely when

\[
                        q(\ker\widehat J)=0.            \tag{6}
\]

Before (4)--(5), there is no physical correction torsor on which (6) could
be evaluated.

## The minimal missing datum

To construct one \(P(e_v)\), it is enough—and necessary for this route—to
provide all of the following source-labelled data:

1. physical invisible lifts \(\xi_v,\eta_v\) with the marked leading
   components \(u_v,t\);
2. a literal augmented correction \(\zeta_v\) satisfying (5);
3. a grade-preserving source map carrying the corrected class to the chosen
   terminal pentagon face; and
4. the kernel annihilation (6).

Symmetry could then generate the other four columns. The present audit
stops at the earliest obstruction: the committed first-jet candidates do
not supply item 1. The endpoint shift and the target-zero sector grade are
formally compatible, but compatible grade is not physical provenance.

## Reproducibility

Run

    python3 computations/verify_h3_rootless_presentation_jet_physical_polar_obstruction.py
    python3 -O computations/verify_h3_rootless_presentation_jet_physical_polar_obstruction.py
    python3 -I -S computations/verify_h3_rootless_presentation_jet_physical_polar_obstruction.py

The checker enumerates the 90 terms of each direct-free row, verifies all
five derivative counts in (1), checks that every tagged presentation
difference forgets to zero, and separately retains the nonzero three-term
sector symbol and its fine degree. Thus it records a source-type
obstruction, not a support specialization or a formal polar/Tate no-go.
