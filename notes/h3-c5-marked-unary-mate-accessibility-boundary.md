# The marked unary row reaches translated faces, not the bright C5 bracket

## Exact boundary

Work on the target-preserving normalized C5 chart of `7c6d431`, with
internal word

\[
                         m=12112
\]

on odd sites \(D=\{1,2,3,4,5\}\).  Fix a deleted face \(v\) and one of
the two nonzero off-cycle tail occurrences \(N\subset D\setminus\{v\}\)
from `bd9e172`.  Mark the two selected colour-zero edges

\[
                 u_v=q_{xv}^{00},\qquad t=q_{pq}^{00}.
\]

The tempting accessibility monomial is \(t u_vN\).  Its complete H8
coefficient has 105 perfect-matching terms.  Exactly 90 avoid \(t\).
Because this coefficient has colour zero at both outer sites \(p,q\),
every one of those 90 terms uses a normalized-zero outer-star entry
\(p_0\) or \(s_0\), and hence vanishes in the one-bad packet.

The remaining 15 terms retain \(t\) and form the complete six-site unary
face on \(\{x\}\cup D\).  Relative to the chosen base \(u_vN\), they split
exactly as

```text
1  chosen base
2  retain u_v and replace N by another matching of D\{v}
4  move u_v through an alternating C4
8  move u_v through an alternating C6.
```

This is checked for both off-cycle tails in every one of the five faces.
With multiplicity over the ten chosen bases, the fourteen mates have
counts

```text
same-reset changed tail   20
translated C4             40
translated C6             80.
```

Checker:
`computations/verify_h3_c5_marked_unary_mate_accessibility_boundary.py`.

## Why this does not activate the conditional attachment theorem

The literal spoke used by the conditional theorem `8771755` is

\[
                        q_{xv}^{0m_v}N,                \tag{1}
\]

in the full internal word \(m\).  The marked row above has reset the
deleted site to zero, so its base edge is instead

\[
                         q_{xv}^{00}N.                 \tag{2}
\]

The mismatch is a physical fine-word mismatch, not a scalar normalization.
Nor do the two same-tail rematchings repair it.  They avoid the direct edge
\(t\), use outer word `00`, and belong to the 90 terms killed by
\(p_0=s_0=0\).  The four bright response brackets in `8771755` have outer
labels `11,12,21,22`; none occurs in this marked coefficient.

Each of the twelve reset-moving mates does contain two translated edges:
one edge \(q_{xr}^{0m_r}\) and one edge incident to \(v\) with decoration
\(0m_s\).  But after removing the first spoke, the residual face still has
colour zero at \(v\), rather than \(m_v\).  It is therefore not one of the
normalized C5 tails to which `8771755` applies.  The four C4 and eight C6
mates land exactly in the translated-face/line-to-hole synchronization
gate isolated by the Lemma-E translated-face and channel-synchronization
theorems.

## Consequence and next propagation target

The marked row cannot prove spoke-to-hole accessibility in one step.  It
does prove that any cancellation of \(t u_vN\), after the two same-reset
face changes are separated, must pass through a source-labelled translated
C4 or C6 carrying two `0m` edges.

The next source-valid lemma is consequently precise:

> **Translated-word propagation.**  Starting from one such reset-moving
> mate, use the complete unary plus four bright response rows to either
> restore the missing label \(m_v\) and produce (1) or a bright bracket
> \(B_{ij}^{xv}N\), or route an alternative term to one-star joint-kernel
> deletion, off-anchor activity, or an anchor Hall/lock.

A well-founded proof needs a progress measure on reset sites or matching
distance.  Merely observing the nonzero translated spoke does not identify
its hole with the normalized tail.

## Scope

This is a coefficient-complete theorem for the one marked unary row, all
ten normalized C5 off-cycle tail occurrences, and their literal fine
labels.  It is not a full-source counterexample, does not assert that all
accessibility brackets can be dark in a genuine one-bad source, and does
not close the translated C4/C6 propagation gate.

Run:

```text
python3 computations/verify_h3_c5_marked_unary_mate_accessibility_boundary.py
python3 -O computations/verify_h3_c5_marked_unary_mate_accessibility_boundary.py
python3 -I -S computations/verify_h3_c5_marked_unary_mate_accessibility_boundary.py
```

Frozen ledger SHA-256:

```text
23e0508b58f1340a5f743ca406815f1e613159864ebedd369ac6dc72b152f8f4
```
