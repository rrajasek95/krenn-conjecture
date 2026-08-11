# The selected denominator memberships are confined to the five-face zero locus

Research boundary only.  This is an exact source-module separator, not a
construction of the five Component-IV augmentations, a proof that their
remaining scalar-zero locus is empty, or a proof of Krenn's conjecture.

## Outcome

Let

\[
 b:R^{15}\longrightarrow R^{243},\qquad
 d_{v,a}\longmapsto e_a^{(v)}q^{[2]},
\]

and take the selected word \(m=12112\).  Split the fifteen columns into the
five \(d_{v,m_v}\) and the ten columns \(d_{v,a}\), \(a\ne m_v\).  The
single literal word-coordinate functional \(\epsilon_m\) satisfies

\[
 \epsilon_m b(d_{v,m_v})=h_v,
 \qquad
 \epsilon_m b(d_{u,a})=0\quad(a\ne m_u),                 \tag{1}
\]

where

\[
 h_v=\operatorname {Haf}
       (q_m|_{\{1,\ldots,5\}\setminus\{v\}})
\]

is the sum of the three perfect-matching monomials on the deleted four-site
face.  Equation (1) is an identity over the universal polynomial ring; it
does not use a rational calibration or a support specialization.

Therefore, after *every* base change to a ring \(S\),

\[
 b(d_{v,m_v})\in\operatorname {im}(b_{\rm oth})
       \quad\Longrightarrow\quad h_v=0\text{ in }S.     \tag{2}
\]

On the open chart \(S[h_v^{-1}]\), that membership is impossible unless the
chart quotient is already the zero ring.  In particular, surjectivity of the
five-face transgression from the reduced-companion/Tor gate forces

\[
                         h_1=\cdots=h_5=0.              \tag{3}
\]

This is the requested primitive separator.  It decides the membership
negatively on every nonzero deleted-face chart and reduces the unresolved
physical calculation to

\[
 \left((\mathscr R/J_{\rm full\ nine})[\kappa^{-1}]
 \right)/(h_1,\ldots,h_5).                              \tag{4}
\]

It does **not** decide the memberships in (4).

## Why the converse is false

The two previously frozen exact rational packets make all five \(h_v\)
zero, but still fail the desired conclusion:

\[
\begin{array}{c|c|c|c}
 &\operatorname {rank}\tau&
 \text{individually hit faces}&\text{primitive cokernel}\ \\ \hline
 \text{direct-free}&4&1,3&(0,1,0,1,2)\\
 \text{tilted}&3&1,3&(0,1,0,1,0),(0,0,0,0,1).
\end{array}
\]

Those packets are not points of the complete full-source scheme, so they do
not prove nonmembership over (4).  They do prove that scalar vanishing alone
cannot replace the remaining whole-column calculation.  Thus (3) is a sharp
necessary branch reduction, not a sufficient criterion.

## Symmetry and chart scope

The identity is equivariant under all \(120\) permutations of the five
sites when the selected word is transported with the sites.  For the fixed
word `12112`, its stabilizer is \(S_3\times S_2\), with face orbits

\[
                         \{1,3,4\},\qquad\{2,5\}.
\]

Hence a fixed-word computation cannot honestly be reduced to one face by
\(S_5\); it has two stabilizer orbits.  No such reduction is needed for
(1), since the same coordinate calculation applies literally to all five
faces.

The known fixed-port one-bad packets are source-empty, but that fact does not
normalize arbitrary multisite stars into (4).  This note therefore does not
promote their unit/descent certificates to a decision of the remaining
full-nine quotient.

## Verification

Run

```text
.venv/bin/python computations/verify_h3_component_iv_selected_denominator_membership_separator.py
.venv/bin/python -O computations/verify_h3_component_iv_selected_denominator_membership_separator.py
```

The checker constructs the three monomials in every \(h_v\), verifies that
all ten unselected columns have zero `12112` coordinate, checks pairwise
face-support separation and all \(600\) site/face transports, reconstructs
the fixed-word stabilizer orbits, and reruns the exact rank-four/rank-three
converse counterguards.  It pins the reduced-companion and denominator-Tor
dependencies.
