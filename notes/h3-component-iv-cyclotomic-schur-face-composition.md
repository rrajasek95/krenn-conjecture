# On the cyclotomic face-zero stratum the Schur obstruction vanishes, but so does the attaching tail

This composes the positive word-change relation of `7ee2f87` with the five
literal marked Schur faces.  It resolves the fate of the old chart-odd and
ordinary-residue obstructions after imposing (h_1=\cdots=h_5=0).  It does
not yet close Component IV.

## Exact five-face composition

Start at the endpoint-changed complete word

\[
                         W=01211200.                     \tag{1}
\]

For every (v\in D=\{1,\ldots,5\}), apply the local source covariance
derivation changing the letter (m_v\in\{1,2\}) to zero.  Term by term on
the 105 K8 matchings this gives the certified Schur word (c_v):

\[
\begin{array}{c|ccccc}
v&1&2&3&4&5\\\hline
c_v&00211200&01011200&01201200&01210200&01211000.
\end{array}                                              \tag{2}
\]

Differentiate the row (H_{c_v}) by the two literal cells

\[
                         a_{xv}^{00},\qquad a_{pq}^{00}. \tag{3}
\]

Exactly three of the 105 matchings contain both marked cells.  Removing
them leaves the three perfect matchings of (D\setminus\{v\}), hence

\[
 {\partial^2H_{c_v}\over
  \partial a_{xv}^{00}\partial a_{pq}^{00}}=h_v.        \tag{4}
\]

All three terms lie in the (pq)-direct sector and, simultaneously, in the
(pr)-response sector.  Thus the two chart copies carry

\[
                         (h_v,-h_v).                     \tag{5}
\]

The checker verifies (2)--(5) literally for all five faces.

## What changes after imposing the cyclotomic equations

Before specialization, the normalized chart-odd cochain gives weight
(+1/6) to each of the three (pq)-terms and (-1/6) to each of the three
(pr)-terms.  It therefore reads one on every chart difference, giving the
generic connecting matrix (I_5).

On the cyclotomic component,

\[
 q_m^{[2]}=0
 \quad\Longleftrightarrow\quad
 h_1=\cdots=h_5=0.                                     \tag{6}
\]

Consequently both tagged copies in (5) vanish separately.  The specialized
chart-odd tail has rank zero.  In the old split-cap landing, q-augmentation
and ordinary residue both read the same scalar (h_v), so the specialized
ordinary-residue block also has rank zero.

This does not contradict the generic (I_5) calculation.  Its cochain
(\Lambda_v) does **not descend** through (6): already on one sector,

\[
                         \Lambda_v(h_v)=\tfrac12\ne0.   \tag{7}
\]

Thus the relation being imposed is not in the kernel of the old cochain.
After base change, the old separator is simply not a functional on the new
quotient.

## Exact verdict

The covariance word change and all five face deletions are now constructed
with their original source labels.  On (V(h_1,\ldots,h_5)), the generic
Schur connecting class and the old ordinary-residue obstruction disappear.

However, the actual composed tail is also zero.  The calculation does not
produce the required nonzero invisible curvature/cap boundary; it removes
an obstruction rather than supplies the attaching row.  Therefore it is not
yet a route to an active clean cap, a source unit, or the final Component-IV
membership.

The next exact datum is a **normal/Rees correction transverse to** (V(h)):
one must decide whether the first divided change of the vanishing face,
after multiplication by the localized curvature scalar, produces a nonzero
boundary while target and ordinary residue remain zero.  Another
set-theoretic evaluation on (h=0) cannot answer that lifting question.

## Verification

Run

```text
.venv/bin/python computations/verify_h3_component_iv_cyclotomic_schur_face_composition.py
.venv/bin/python -O computations/verify_h3_component_iv_cyclotomic_schur_face_composition.py
```

The checker reconstructs every covariance row and marked polar, verifies the
two chart placements, evaluates all five (h_v) over both cyclotomic
conjugates, and records the generic versus specialized chart-odd and old
ordinary-residue ranks.
