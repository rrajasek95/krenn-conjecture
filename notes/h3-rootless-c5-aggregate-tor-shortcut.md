# One aggregate Tor vector suffices modulo the clean C5 collisions

## Exact theorem

Let \(F=S^5\) be the five-face reduced-companion module on the normalized
C5 chart, and let

\[
 \epsilon(y_1,\ldots,y_5)=\sum_v y_v.
\]

The five clean collision cells have face boundaries

\[
                         dE_v=-e_v+e_{v+1}.            \tag{1}
\]

Their image is not merely rank four: it is the saturated lattice
\(\ker\epsilon\).  Consequently surjectivity of the denominator
transgression

\[
       \tau:\operatorname{Tor}_1(\operatorname{coker}b,S)\longrightarrow F
\]

is stronger than the normalized rootless construction needs.

Suppose one homogeneous \(y\in\operatorname{im}\tau\) has
\(s=\epsilon(y)\) a unit on the active localization.  Normalize
\(y'=s^{-1}y\).  For every face \(v\),

\[
                         e_v-y'\in\ker\epsilon=\operatorname{im}dE.
\]

Adding the corresponding clean collision path to the Tor cell therefore
produces the primitive face augmentation \(e_v\).  All collision cells have
zero `W`, anchor, target, and ordinary-residue readouts, so those values of
the Tor cell are preserved.

An explicit integral solver makes saturation exact.  For a zero-sum vector
\(z=(z_0,\ldots,z_4)\), put

\[
 c_i=-\sum_{j=0}^i z_j\quad(0\le i<4),\qquad c_4=0.
\]

Then \(\sum_i c_i(-e_i+e_{i+1})=z\).  No division occurs in this step.

## Fine-grade condition

The statement is homogeneous.  The Tor vector and collision paths must be
transported to one common repeated-site degree using the selected Laurent
C5 factors before they are added.  Their numerical normalization to one
does not erase physical degree.  Once that standard homogenization is made,
the result applies over the localized source ring; at a coefficient point,
`nonzero aggregate` means a unit after shrinking to its principal open.

## The old rank counterguards already hit the aggregate

The two exact packets in the denominator-Tor gate were advertised as
rank-deficient counterguards to surjectivity.  Replaying their actual
transgression rows gives:

```text
direct-free packet: rank 4, contains (1,0,0,0,0)
tilted packet:      rank 3, contains (1,0,0,0,0).
```

Thus each already has a unit aggregate hit and, conditional on the common
physical typing just stated, supplies every primitive face augmentation
after collision transport.  Neither packet is a full source point, so this
does not prove existence over the full-source ring.  It does show that
`rank(tau)<5` is not the relevant obstruction.

For the normalized rootless base-column purpose, the exact Tor obligation is

\[
                    \boxed{\epsilon(\operatorname{im}\tau)\ni1},          \tag{2}
\]

locally, not \(\operatorname{im}\tau=F\).

## What the aggregate-zero branch does and does not give

If \(\epsilon(\operatorname{im}\tau)=0\), then \(\epsilon\) descends to a
primitive covector on the reduced face quotient

\[
                    F/(\operatorname{im}\tau+\operatorname{im}dE).       \tag{3}
\]

This is not automatically the rootless terminal annihilator.  A literal
endpoint bar has typed projection

\[
                   (-\Omega_v,+e_v;\operatorname{ores}=1).               \tag{4}

\]

The face covector alone reads one on (4).  Correcting it with
`-ores*` kills (4), but then reads nonzero on the physical pure-residue
column.  If the annihilator is required to kill ordinary residue, the
unique correction on this block instead adds the aggregate endpoint-ridge
covector \(\sum_v\Omega_v^*\).

That correction becomes physical only after the still-unconstructed
multidegree-preserving comparison \(\Omega_v\mapsto r_v\), and it must also
kill every endpoint-word-change/correction row.  Therefore (3) is a sharp
reduced separator, not yet a Component-III terminal functional.  This is
the same `Omega`/rootless-ridge typing obstruction isolated by `6d6121a`.

## Relation to the C5 cross-word response row

The smallest coefficient which changes the reset value at \(v\) from zero
to \(m_v\) while retaining an off-cycle tail \(N\) is exactly the complete
six-term response coefficient of `8771755`:

\[
 (p_i@x\,s_j@v+p_i@v\,s_j@x)N
 +\text{four different-tail C4 terms}=0.               \tag{5}

\]

It has two same-tail orientations and four C4 alternatives.  Thus an active
term in (5) routes by the committed unit/deletion/Fitting/off-anchor/Hall
dichotomy.  But (5) is a bright outer-word row, disjoint in fine degree from
the five reset unary SCCs of `f3e4b01`; no coefficient identity makes one of
its endpoint products nonzero.  In the dark branch it adds no face image to
\(\tau\) and does not remove the extension obstruction above.

## Scope and verification

This theorem corrects the algebraic burden for the normalized C5 rootless
base: one unit aggregate Tor hit suffices.  It does not construct such a hit
over the full-source ring, a full-source dark-bracket point, the
`Omega`-to-ridge comparison, or the final terminal annihilator.

Run:

```text
python3 computations/verify_h3_rootless_c5_aggregate_tor_shortcut.py
python3 -O computations/verify_h3_rootless_c5_aggregate_tor_shortcut.py
python3 -I -S computations/verify_h3_rootless_c5_aggregate_tor_shortcut.py
```

Frozen ledger SHA-256:

```text
51381f29700602ccd05daede6f5ec1c6285ad508046b6daf36f5e45663579a67
```
