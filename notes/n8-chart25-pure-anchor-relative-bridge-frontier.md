# Pure anchors construct the projected chart-25 relative edge

This is an exact source-labelled result in the canonical chart-25 fibre.
It constructs the missing relative edge after projection, but it does not
yet lift that edge through the full source complex and does not prove
`SP-CLEAN-BRIDGE` or Krenn's conjecture.

## The literal bridge

Let \(A_1,\ldots,A_4,D\) be the five rows over the canonical positive
centre.  Their source incidence is

\[
                         d e_i=A_i+D .                   \tag{1}
\]

All five rows contain the same pure-zero perfect matching

\[
                         M_0=01\mid24\mid35\mid67 .      \tag{2}
\]

Put \(m_i=A_i/M_0\).  The four \(m_i\) have the same literal fine degree:
at every site their colour degree is \((0,1,1)\).  Hence both \(e_i\) and
the pure-anchor column

\[
                         a_i=m_i(H_{0^8}-1)              \tag{3}
\]

have balanced site-colour degree \((1,1,1)\) at all eight sites.  For any
choice of one of the \(3,4,4,3\) actual labelled columns in (1),

\[
                         r=\sum_{i=1}^4(e_i-a_i)         \tag{4}
\]

is a literal source-labelled chain.  Projection to the complete 20-row
dual support cancels the four \(A_i\)'s and gives

\[
                         p\,dr=4D-\tau,
                 \qquad \tau=-\sum_{i=1}^4m_i .         \tag{5}
\]

Thus the formal \(D\)--\(\tau\) edge isolated previously is not merely an
abstract mapping-cylinder declaration: the mixed rows together with the
ordinary pure anchor construct it exactly after the chart-25 projection.
This is not an ordinary label-diagonal Koszul operation.

## Exact target extension

Across all 20 dual-support rows there are 44 pure-anchor factorizations,
forming 32 distinct pure columns.  Their target multipliers have
multiplicity histogram

\[
                       20\cdot1+12\cdot2=44 .            \tag{6}
\]

The chart-25 cochain extends consistently to every one of these target
multipliers.  On the 44 row factorizations its source-pairing histogram is

\[
 -\tfrac14:16,\qquad 0:16,\qquad-\tfrac12:8,
 \qquad+\tfrac14:4 .                                    \tag{7}
\]

Each of the four multipliers in (5) has target weight \(-1/4\).  Therefore
the source part \(4D\) has pairing \(+1\), while the displayed target part
has pairing \(-1\).  Equation (5) is a genuine relative boundary and does
not kill the obstruction by itself: \(\tau\) is a nonzero target class.

## The first coherence obstruction

The full boundary of (4) is not confined to the five-row fibre.  There are
\(3\cdot4\cdot4\cdot3=144\) labelled choices.  Every choice has the same
projected boundary (5), but every choice has a nonzero off-fibre tail.  Its
signed coefficient norm is always 828.  The minimum support is 774 rows,
attained by two choices; the complete support-size histogram is frozen by
the checker.

This failure persists after admitting the entire first source
neighbourhood of the 20-row dual support:

* all 56 incident mixed physical columns;
* all 32 distinct incident pure-anchor columns;
* all their 7,536 source and target feature rows.

The 88 source columns are integrally independent.  A deterministic
\(88\times88\) minor has determinant \(-1\).  Appending the desired exact
\(4D-\tau\) vector gives an \(89\times89\) minor of determinant \(-4\).
Consequently

\[
         4D-\tau\notin\operatorname {im}(d_{\rm first\ neighbour})
                                                               \tag{8}
\]

over \(\mathbb Q\), and indeed over every characteristic except possibly
two.  This is an ordinary integer-minor certificate, not a heuristic rank
or finite-field verdict.

## Relation to the unified two-chart inventory

The committed full-nine and two-chart calculations are compatible with
this result but do not finish it.  The exact two-edge reinsertion identity
does put curvature times a diagonal anchor in its target-side image, and
the power-free Bianchi rows transport chart labels.  However, the
source-resolution audit still has no descended coefficient/reinsertion
column, while the signed-circuit and monic-anchor audits prove that ordinary
chart transport preserves total pure-anchor incidence unless the localized
source ideal is already a unit.

The first missing object is therefore sharper than an abstract
\(D\)--\(\tau\) half-edge: (4) already supplies that half-edge after
projection.  What remains is a balanced-fine-degree, target- and
ordinary-residue-zero chain \(c\) in the kernel of the chart-25 projection
whose boundary cancels the off-fibre tail of (4).  For either minimum
choice this means a source-labelled nullhomotopy of the frozen 774-row
tail.  Then, and only then, \(r+c\) is the required full relative edge.

The determinant theorem is exact for the complete first-neighbour
inventory and the currently certified anchor/Bianchi operations.  It does
not exclude a deeper correction built entirely from source columns which
miss the chart-25 dual support; that dual-invisible contraction is now the
precise remaining gate.

## Verification

Run

```text
.venv/bin/python computations/verify_n8_chart25_pure_anchor_relative_bridge_frontier.py
.venv/bin/python -O computations/verify_n8_chart25_pure_anchor_relative_bridge_frontier.py
```

The checker reconstructs the split \(\mathbb Z^4\) cokernel, all pure-anchor
target weights, all 144 literal bridges, and the two exact determinant
minors.  It also replays the certified full-nine, two-edge anchor, Bianchi,
signed-circuit, and monic-anchor dependencies.

Frozen ledger SHA-256:
0de355496d404d578c4762403690dae387eeb627760558376c53ada57caf4d2e.
