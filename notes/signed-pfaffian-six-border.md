# The ternary six-site target is a signed Pfaffian border point

## Outcome

The six-site ternary equality tensor is in the Zariski closure of the
transverse outputs of alternating matrices of arbitrary inter-site bilinear
forms.  An exact nine-cell Laurent family has output

\[
 \Delta_{6,3}-t\,e_0\otimes e_0\otimes e_2\otimes
                       e_1\otimes e_2\otimes e_1.          \tag{1}
\]

The sign in (1) is the canonical Pfaffian sign, not a hafnian convention.
Consequently no polynomial identity in the 729 transverse output
coordinates alone can separate `Delta_(6,3)` from transverse Pfaffian
outputs.  Any characteristic-zero obstruction must use source coordinates,
denominators/localization, or nontransversal Pfaffians.  The family does not
decide whether the target itself has a finite preimage.

## 1. The exact family

Order the sites as `0,1,2,3,4,5` and the colors as `0,1,2`.  For `t != 0`,
let `K(t)` be the alternating matrix on the 18 site-color modes whose only
nonzero upper-triangular inter-site cells are

\[
\begin{array}{c|c|c}
\text{edge}&\text{endpoint colors}&\text{entry}\\ \hline
01&(0,0)&t\\
23&(0,0)&t^{-1}\\
45&(0,0)&1\\ \hline
02&(1,1)&1\\
14&(1,1)&1\\
35&(1,1)&1\\ \hline
03&(2,2)&1\\
15&(2,2)&1\\
24&(2,2)&1.
\end{array}                                                \tag{2}
\]

The lower-triangular entries are fixed by alternation.  For a coloring
`c in {0,1,2}^6`, let `K(t)[c]` be the `6 by 6` principal transversal in
site order.  Its Pfaffian is expanded with the canonical sign

\[
 \operatorname {sgn}_{\rm Pf}(M)
   =(-1)^{\#\{\{ab,cd\}\subset M:a<c<b<d\text{ or }c<a<d<b\}}. \tag{3}
\]

There are only four supported colored perfect matchings:

\[
\begin{array}{c|c|c|c}
c&M&\operatorname {sgn}_{\rm Pf}(M)&\text{entry product}\\ \hline
000000&01|23|45&+1&1\\
111111&02|14|35&+1&1\\
222222&03|15|24&+1&1\\
002121&01|24|35&-1&t.
\end{array}                                                \tag{4}
\]

Indeed, a supported matching must use only the nine underlying decorated
edges in (2).  Their uncolored union is the triangular prism, which has
exactly the four perfect matchings displayed in (4).  The endpoint colors
then force the displayed coloring.  Multiplying the audited signs and
entries proves (1).

Equivalently, if `Phi` denotes the cubic map from the 135 upper-triangular
inter-site cells to the 729 transverse Pfaffian coefficients, then

\[
                    \Phi(K(t))=\Delta_{6,3}-t e_{002121}. \tag{5}
\]

Thus `Phi(K(t))` tends coefficientwise to `Delta_(6,3)` as `t -> 0`, even
though the cell on `23;(0,0)` escapes to infinity.

## 2. Output-only identities cannot prove the missing no-go

Let `P` be any polynomial over a characteristic-zero field in the 729
transverse coefficient variables, and suppose

\[
                         P(\Phi(K))=0                     \tag{6}
\]

for every finite alternating source matrix `K`.  Substitute the Laurent
family (2).  Equation (6) holds for every `t != 0`, while
`P(Phi(K(t)))` is an ordinary polynomial in `t` by (5).  It therefore also
vanishes at `t=0`, giving

\[
                         P(\Delta_{6,3})=0.                \tag{7}
\]

This includes every consequence of the Grassmann--Pluecker/matchgate
identities after all nontransversal coordinates have been eliminated and
only polynomial transverse-output coordinates remain.  Hence such an
identity cannot contradict the target.  A useful matchgate proof must keep
some nontransversal Pfaffians, or produce a source identity valid after
localizing at the three nonzero uniform coefficients.  The pole `t^{-1}`
in (2) is exactly what such a localized argument has to control.

This does not turn (5) into a counterexample: every finite `t` retains the
nonzero mixed coefficient `-t`, and `t=0` is not a finite source point.
It distinguishes closure from membership, which is essential because the
conjecture asks for exact finite weights.

## 3. Exact audit

Run

```text
python computations/verify_signed_pfaffian_six_border.py
```

The dependency-free checker recursively enumerates all 15 perfect matchings,
computes every sign by crossing parity, and evaluates all 729 colorings as
integer Laurent polynomials.  It verifies that (4) is the complete list of
nonzero coefficients and checks the sign of each displayed matching
separately.
