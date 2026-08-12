# The regularized shifted filler needs one normal Hasse face on `V(h)`

## Exact outcome

The literal first normal difference of the shifted filler from `91041f7`
does **not** itself extend the shared comparison candidate of `0828a2f`
across the cyclotomic face-zero locus.

Write the complete two-direction source cycle of `91041f7` as

\[
\begin{aligned}
s_{ut}(q)={}&H_m(q)r_0[ut]+(\partial_uH_m(q))r_0[t]
 +(\partial_tH_m(q))r_0[u]\\
 &+h_v(q)r_0[\varnothing]-F_0r_m[ut],\\
n_v(q)={}&s_{ut}(q)-h_v(q)T,\qquad dn_v(q)=h_v(q)Yw.
\end{aligned}                                           \tag{1}
\]

For the five exact normal arcs at the cyclotomic point,

\[
 h(q(\tau))=\tau B(\tau),\qquad B(\tau)=I_5+\tau R.   \tag{2}
\]

The polynomial numerator is coefficientwise divisible by `tau`, but its
q-independent mixed-row companion cancels in the subtraction.  Project to
the zero `u/t` Hasse grade, equivalently the empty-Eq output coordinate.
For the five-by-five family this gives

\[
 \pi_0\frac{n(q(\tau))-n(q_0)}{\tau}
       =B(\tau)(r_0[\varnothing]-T).                    \tag{3}
\]

Consequently, after applying the exact completed inverse from `c9ae815`,

\[
 \pi_0d\bigl(B(\tau)^{-1}(3)\bigr)
      =Yw+F_0e_{\rm Eq}[\varnothing].                  \tag{4}
\]

Target and ordinary residue are zero, and the chart-odd correction is the
required `-S_v`.  The failure is solely the source boundary in (4).
It is primitive: `F_0` has 91 labelled terms and contains the monic term
`-u_hom`, while the five residual columns have matrix `I5`.  No further
normal division or `B`-linear combination removes it.

Checker:
`computations/verify_h3_cyclotomic_regularized_shifted_filler_normal_face.py`.

## The exact missing normal face

The subtraction in (3) discarded the entire base source cycle which must
live on the new normal Hasse index.  The required first face is therefore

\[
                         s_{ut}(q_0)[\nu].              \tag{5}
\]

Its distinguished mixed-row component is

\[
                         -F_0r_m[ut,\nu].               \tag{6}
\]

At `h(q0)=0`, the normal derivative of the mixed row reads one in the
normalized face coordinate.  Consequently (6) has the empty-Eq boundary

\[
             \pi_0d(-F_0r_m[ut,\nu])
                    =-F_0e_{\rm Eq}[\varnothing].       \tag{7}
\]

This cancels (4) in the decisive projection.  The other terms of (5) are
not optional: they occupy the remaining `u/t` Hasse grades and are required
for a full indexed source chain.

The checker also verifies the complete relative differential.  If
`G_A=(H_A(q(tau))-H_A(q0))/tau` for the four `u/t` Hasse coefficients, the
naked quotient has boundary

\[
 F_0\sum_{A\subseteq\{u,t\}}G_A
       e_{\rm Eq}[\{u,t\}\setminus A]+G_{ut}Yw.        \tag{8}
\]

The one normal face (5) has exactly the negative of the Eq sum in (8).
Hence their sum is an exact relative derived chain with

\[
 d\left(\frac{n(q(\tau))-n(q_0)}{\tau}
             +s_{ut}(q_0)[\nu]\right)=G_{ut}Yw,        \tag{9}
\]

zero target and ordinary residue, and chart correction `-G_ut S_v`.
Multiplying the five columns by `B(tau)^(-1)` turns (9) into `Yw` with
chart correction `-S_v` to all orders.

Thus there is no coefficient-divisibility obstruction and no obstruction
from the invertibility of `B`.  There is one indispensable source-connection
face.  The naked regularized difference is not a chain, but adjoining the
complete face (5) repairs it exactly in the relative derived presentation.

## Relation to the face-open candidate

On `D(h_v)`, `0828a2f` uses `(kappa/h_v)n_v`.  On `V(h)`, the naked
regularization cannot be declared to be its extension, but the repaired
chain (9) is the exact derived comparison candidate.  Thus the same derived
mechanism now covers the face-open and face-zero loci, with different
normalizations.

Physical promotion remains conditional.  A comparison must carry the
complete normal-indexed source face (5), preserve target and the correctly
defined ordinary residue, send chart correction `-S_v` to the physical
chart incidence, and identify derived `Yw` with the physical cap coordinate.

Declaring only the quotient (3) to be the extension drops (5) and leaves
the monic error (4).  The relative derived repair is exact; whether it admits
the required physical comparison remains conditional.

## Scope and verification

This is an exact relative derived calculation over
`Q[zeta]/(zeta^2+zeta+1)`.  It pins the cyclotomic normal matrix, its
all-order inverse, the complete shifted filler, and the shared comparison
interface.  It verifies the naked obstruction in the empty-Eq projection
and the one-face repair in all four `u/t` Hasse grades.  It does not claim
that the displayed mixed-row component alone is a full filler, construct an
underived physical source chain, or construct the physical cap comparison.

Run

```text
python3 computations/verify_h3_cyclotomic_regularized_shifted_filler_normal_face.py
python3 -O computations/verify_h3_cyclotomic_regularized_shifted_filler_normal_face.py
python3 -I -S computations/verify_h3_cyclotomic_regularized_shifted_filler_normal_face.py
```

Frozen ledger SHA-256:

```text
d44bb7419baae7c0aae7c3b7b74ee2ceffe5ebb714e58a1b2a16fa4058341742
```
