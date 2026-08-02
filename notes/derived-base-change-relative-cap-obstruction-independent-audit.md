# Independent audit of the derived cap/base-change obstruction

This note audits commit `0c21ae3` without importing its checker.  It confirms
the cap-complex calculation, relative sign, formal occupancy splitting, and
hypothetical-lift test.  It also corrects one categorical overclaim in the
original classification.  The invisible cross-word lift lemma, unified
overlap theorem, SP-CLEAN-BRIDGE, and Krenn's conjecture remain open.

## Confirmed cap calculation

For

\[
 G=(R\langle T,\rho\rangle\mathop{\longrightarrow}^{[-Y\;1]}
       R\langle w\rangle),
\]

the columns \(g=T+Y\rho\) and \(\rho\) give the unimodular basis matrix

\[
 \begin{pmatrix}1&0\\Y&1\end{pmatrix}.
\]

Thus \(G=Rg\oplus(R\rho\xrightarrow{1}Rw)\) as a complex, over the
universal ring itself.  The target map sends \(g\) to one, so no nonzero
target-zero class exists in \(H^1(G)\) after any base change.  This is
stronger than a generic-rank argument and is unaffected by non-flatness.

With the standard cochain connecting convention, the relative element
\(p_c=-\kappa Y\rho\) has

\[
 \partial[p_c]=d(-\kappa Y\rho)=-\kappa Yw.
\]

The sign in `0c21ae3` is correct.  The selected representative
\(-\kappa(T+Y\rho)\) is instead a graph cycle.  If an invisible generator
\(n\) with \(dn=\kappa Yw\) is adjoined, then
\(n-\kappa Y\rho\) is the unique target-zero kernel line and has ordinary
response \(-\kappa Y\).  These statements were independently replayed on
four exact rational active packets, including the direct-free boundary.

## Formal occupancy and the section defect

The coefficient-one exposure map is a literal section of the matching-state
projection.  The independent checker enumerates every partial matching on
one through six sites, forms the basis

\[
 \{\text{states covering }x\}\ \cup\ \{s_x(N)},
\]

and obtains full rank over \(\mathbb Q\) and after reduction modulo
\(2,3,5,7\).  More importantly, the coefficient identity
\(\pi_xs_x=1\) holds state by state over \(\mathbb Z\), hence after tensoring
with every ring.  The formal occupancy extension and its connecting map are
therefore zero under arbitrary base change.

For a relation submodule \(E\subset P=K\oplus s(Q)\), the proposed defect

\[
 \omega_s(e')=[e-s(e')]
       \in K/(E\cap K),\qquad \pi(e)=e',
\]

is well defined: changing \(e\) changes the numerator by an element of
\(E\cap K\).  It vanishes exactly when \(s(\pi(E))\subset E\), which is the
condition for the fixed section to descend.  A four-dimensional exact
model in the checker exhibits both a coupled relation with nonzero defect
and a blockwise relation with zero defect.  Therefore an evaluated
cap/exposure relation can obstruct descent, while a relation of the form
\(JP\) coming only from a base ideal cannot.

## Tor, Yoneda, and Atiyah scope

The relative triangle gives a genuine connecting/Yoneda operation, but its
value is the nonzero obstruction above; it does not construct an absolute
target-zero class.  Since \(G\) is chain-isomorphic to a free cycle plus a
contractible summand, its positive Tor and Atiyah class vanish in the stated
module-theoretic setting.  No multiplication and nullhomotopy data defining
a Massey product have been supplied.  Finally, \(\kappa=AU-BF\) enters as
the external determinant of an overlap contraction, not as curvature of a
connection on \(G\).  The original Tor/Yoneda/Massey/Atiyah nonclaims are
therefore sound for the cap and formal occupancy objects.

They did not justify the original if-and-only-if assertion for the **full
source complex**.  Let

\[
 b:C^1\to V
\]

collect target, ordinary residue, and every boundary component other than
the cap row, let \(a:C^1\to Rw\) be that cap coordinate, and set
\(K=\ker b\), \(Q=\operatorname {coker}b\),
\(I=a(K)\), \(O=Rw/I\).  For finite free \(C^1,V\), non-flat base change
gives

\[
 0\to\operatorname {im}(K\otimes S)
   \to\ker(b\otimes S)
   \to\operatorname {Tor}_1^R(Q,S)\to0.
\]

Consequently \([w]=0\) in \(O\otimes S\) classifies exactly the lifts
descending from universal invisible chains.  New post-specialization
invisible chains are measured by \(\operatorname {Tor}_1^R(Q,S)\), and
their cap coordinate gives a transgression

\[
 \tau_S:\operatorname {Tor}_1^R(Q,S)\to O\otimes S.
\]

The full lift exists precisely when \([\kappa Yw]\) lies in the image of
this map.  Positive Tor can therefore contribute existence, not merely
indeterminacy.  The primary note has been corrected accordingly.

The checker includes the sharp model \(R=\mathbb Q[t]\),
\(b=t:R\to R\), \(a=1\), and \(S=R/(t)\).  Universally \(K=0\) and
\([w]\ne0\) in \(O\otimes S\), but \(b\otimes S=0\); its new one-dimensional
invisible kernel is \(\operatorname {Tor}_1^R(R/(t),R/(t))\), and \(a\)
sends it to \(w\).  This directly refutes the
unqualified degree-zero-only classification while leaving the split-cap
no-go untouched.

## Compatibility with the mixed-word reset audit

Commit `befda3f` proves that three strict coefficient resets descend to the
odd quotient and normalize a **guard EqSystem defect** to the desired pure
word.  On a genuine source that defect is zero, so the strict reset has zero
boundary.  This neither produces a universal invisible chain nor computes
the transgression above.  The two notes are compatible after correction:
the missing one-higher source syzygy may be a universal lift, or it may be a
controlled Tor class becoming invisible only after the full-nine
specialization.  Arbitrary descended resets still fail zero indeterminacy.

## Executable audit

The dependency-free checker is
[audit_derived_base_change_relative_cap_obstruction_independent.py](../computations/audit_derived_base_change_relative_cap_obstruction_independent.py).
It uses `require`/`RuntimeError`, supports `all`, `cap`, `occupancy`,
`defect`, and `tor` modes, and freezes the combined exact ledger by SHA-256.

```text
223e8f5530585c2ff92b3d74f4fc80afe3a2c513244b353fdf2a648b0a8e9f06
```
