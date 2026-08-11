# A literal covariance row changes `11211200` to `01211200`, but only transports the cyclotomic kernel

This is a positive source-provenance result at the exact pair of word grades
left by `4c4d9bf`.  It is not yet the Component-IV attaching theorem.

## Exact fixed-pair relation

Let

\[
 W_2=11211200,\qquad W_3=01211200.                       \tag{1}
\]

The residual parts are the Hamming-two word `112112` and its
endpoint-changed word `012112`; the last two zeros retain the labelled chart
endpoints.  Both complete words are mixed, hence both full-nine target
coordinates are zero.

On the universal source coordinate ring, take the site-(x) covariance
derivation

\[
 \delta_x(q_{xv}^{,1,c})=q_{xv}^{,0,c},                \tag{2}
\]

and the analogous rule on every endpoint-star/direct cell incident with
(x).  Every K8 perfect matching contains exactly one such cell.  Literal
matching expansion therefore gives the termwise identity

\[
                  \boxed{\delta_xH_{W_2}=H_{W_3}.}       \tag{3}
\]

The checker verifies all 105 monomials.  More strongly, (3) preserves each
physical chart sector separately:

\[
\begin{array}{c|cc}
 &\text{direct}&\text{response}\\\hline
 pq&15&90\\
 pr&15&90.
\end{array}                                              \tag{4}
\]

Thus (3) is not a declared cross-word column and does not erase the two-chart
provenance.  It remains exact in the direct-free (A_{pr}=0) specialization,
where the same 15 (pr)-direct monomials are removed on both sides.

Equivalently, the normalized one-site covariance bar has boundary (L-D),
augmentation zero, and zero target at both endpoints.  At this fixed pair,
the missing word change itself is therefore available from the original
source action.

## What happens on the cyclotomic face-zero slice

The derivation maps the five Hamming-two carriers to the endpoint-changed
carriers:

\[
 r_v=q_{xv}^{,1,m_v}
       \longmapsto
 \rho_v=q_{xv}^{,0,m_v}.                               \tag{5}
\]

It leaves the other five colours (m=12112) fixed.  Consequently the
cofactor matrix in the changed row is the same (K_\zeta) as in `4c4d9bf`.
On the localized carrier (r_1=1),

\[
 \operatorname {rank}K_\zeta=3,
 \qquad
 \ker K_\zeta=
 \left\langle e_1,(0,1,\zeta,\zeta,1)\right\rangle.    \tag{6}
\]

Equation (3) transports (6) isomorphically from \(r\) to \(\rho\); it does
not annihilate it.  Thus the Hamming-two zero coefficient becomes an
endpoint-changed zero coefficient, but no scalar unit or clean-cap value is
created.

## Exact remaining datum

The bare two-chart Schur polar at `01211200` has the certified chart-odd
connecting matrix (I_5).  The site-(x) derivation is diagonal on the
(pq/pr) chart labels, so it cannot cancel that class.  The positive
relation (3) resolves only the complete-word provenance gap; it leaves the
five (v)-labelled face deletion/residue corrections untouched.

The next bounded calculation is consequently forced: compose (3) with the
five marked Schur face deletions and decide whether specializing

\[
                         h_1=\cdots=h_5=0               \tag{7}
\]

removes their chart-odd connecting/ordinary-residue class in the physical
quotient.  The normalized local-GL3 audit says that class is (h_vY_0), so
(7) is exactly the place where its old obstruction can disappear; this has
not yet been promoted to a source-labelled attaching chain.

## Verification

Run

```text
.venv/bin/python computations/verify_h3_component_iv_cyclotomic_word_change_relation.py
.venv/bin/python -O computations/verify_h3_component_iv_cyclotomic_word_change_relation.py
```

The checker reconstructs both complete K8 word rows, verifies the derivation
term by term and within both chart sectors, transports the exact cyclotomic
kernel over both conjugate roots, and pins the Hamming-two, Schur-polar,
normalized-bar, and reduced-word-companion boundaries.
