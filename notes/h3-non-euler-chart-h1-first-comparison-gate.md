# The first filler for the non-Euler chart class is a shifted denominator-marked two-edge cell

## Outcome

For the primitive class (k_v=c_{pq}-c_{pr}) isolated in
[the 90-term separator theorem](h3-rootless-non-euler-90term-chart-h1-separator.md),
the earliest possible literal repair is now classified.

The raw marked-face map sends

\[
 k_v\longmapsto
 S_v=(h_v)_{pq,\mathrm{direct}}
           -(h_v)_{pr,\mathrm{two\ star}}.             \tag{1}
\]

Its normalized odd projection sends (S_v) to (h_vY_0), and the final
three-matching average reads one.  Hence attaching a source cell
(b_v) with (db_v=k_v) extends the marked-face map if and only if one
also supplies a chain (n_v) with

\[
                         dn_v=h_vY_0.                  \tag{2}
\]

Subtracting this homotopy gives terminal correction (-1).  Equation (2),
not a stipulated scalar, is the first physical chain-map datum.

No raw denominator source term enters its strict fine degree.  The unique
possible denominator face has coefficient/output weight (9), while the
source block has weight (12); it enters only after the unconstructed
module shift

\[
                  \sigma=e_{x,0}+e_{p,0}+e_{q,0}.      \tag{3}
\]

Moreover a chart-neutral placement has marked value zero.  With primitive
unit coefficients on both chart faces, the unique placement contributing
(-1) is (-S_v).  Therefore the minimal new source type is

\[
 \boxed{[K_v;d_{v,m_v};u_v,t;\sigma]}
\]

with source-derived chart-odd decoration, target zero, and ordinary residue
zero.  Neither the shift nor those augmented readouts have been constructed.
This is the exact first-degree obstruction.

The denominator-marked order-four cube remains useful, but it is the first
(q)-zero scalar continuation of (2), not the first candidate for killing
the chart (H_1) class.  Its eventual (kappa Yw_v) cap landing must not be
identified with the initial boundary (h_vY_0).

## 1. The chain-map extension equivalence

Let the two chart generators have the same 90-term physical boundary:

\[
 d c_{pq}=B_w=d c_{pr},\qquad k_v=c_{pq}-c_{pr}.       \tag{4}
\]

Differentiate in the two marked directions (u_v=a_{xv}^{00}) and
(t=a_{pq}^{00}).  Literal chart partition gives (1).  Define

\[
 \Omega(pq,M)=\frac12M Y_0,\qquad
 \Omega(pr,M)=-\frac12M Y_0.                           \tag{5}
\]

Then

\[
                  \Omega T(k_v)=h_vY_0.                \tag{6}

Suppose a higher source cell (b_v) is adjoined with (db_v=k_v).  A
chain map extending (Omega T) over (b_v) must send it to some (n_v)
obeying

\[
 d n_v=\Omega T(db_v)=\Omega T(k_v)=h_vY_0,            \tag{7}
\]

which proves necessity.  Conversely, a chain satisfying (7) defines the
extension on the one new generator, so it is sufficient.  This is a plain
chain-map equation; no spectral-sequence or cap interpretation is assumed.

Let (epsilon_h) assign (1/3) to each of the three matching monomials of
(h_v).  The six-entry cochain of `091edba` factors as

\[
                         \Lambda_v=\epsilon_h\Omega,   \tag{8}
\]

and (epsilon_h(h_v)=1).  Thus the corrected cochain subtracts (n_v)
and obtains the required (-1).  The raw differential in (7) has the plus
sign; these two signs should not be conflated.

## 2. Exact first fine degree

In the strict degree

\[
 \lambda_v=e_{x,0}+e_{v,0}+e_{p,0}+e_{q,0}
       +\sum_{i\in F_v}(e_{i,0}+e_{i,m_i}),\qquad
 |\lambda_v|=12,                                      \tag{9}
\]

the complete source census has 48 columns per chart.  Each one-chart block
has rank 48, while the doubled 96-column block still has rank 48.  Its
kernel consists exactly of the 48 componentwise chart comparisons.

All (15\cdot81\cdot3=3645) raw denominator monomials were checked.  None
divides (9).  The reset face (h_vY_0) has unshifted weight 9, and

\[
               \deg(h_vY_0)+\sigma=\lambda_v.          \tag{10}
\]

After declaring (3), exactly one denominator column aligns:
(d_{v,m_v}).  Thus (3) is not optional grading notation; it is the unique
degree in which the candidate (2) could occur.  But the census derives no
physical cap-row shift, so (10) is alignment, not provenance.

## 3. The chart-decoration obstruction

Write a possible two-chart denominator tail as

\[
                 a(h_v)_{pq}+b(h_v)_{pr}.              \tag{11}

The normalized marked readout is

\[
                         \Lambda_v(11)=\frac{a-b}{2}.  \tag{12}

The chart-neutral choice ((a,b)=(1,1)) has value zero.  Among placements
with both faces present and primitive unit coefficients, the unique value
(-1) is

\[
                         (a,b)=(-1,1),                 \tag{13}

which is (-S_v).  The existing raw denominator generator has no derived
chart placement at all; placing it diagonally in older leading-block models
was a modelling choice.  Therefore no committed literal cell realizes
(13), even after the degree alignment (10).

An ordinary (R)-linear mapping-cone declaration cannot bypass this.  The
exact selector obeys

\[
                         \Psi_v(1)=0,\qquad
                         \Psi_v(H_m)=1,                \tag{14}

so its terminal correction is intrinsically a principal-parts/Hasse
operation with nonzero Leibniz cross terms.

## 4. Where order four begins

Starting from the external order-two face (h_v), contracting zero, one,
or two internal matching edges gives

\[
\begin{array}{c|c|c}
 \text{total PP order}&q\text{-degree}&
       \text{stabilizer character}\\ \hline
 2&2&\ne0\\
 3&1&\ne0\\
 4&0&0.
\end{array}                                             \tag{15}
\]

At order four every internal perfect matching differentiates (h_v) to
the unit, and Reynolds averaging canonically normalizes the three choices.
This is why the committed four-cube is the first invariant scalar candidate.
It does not change the order-two extension criterion (7), and it still lacks
the physical comparison differential and ordinary-residue map.

## Verification

Run

    python3 computations/verify_h3_non_euler_chart_h1_first_comparison_gate.py
    python3 -O computations/verify_h3_non_euler_chart_h1_first_comparison_gate.py
    python3 -I -S computations/verify_h3_non_euler_chart_h1_first_comparison_gate.py

The checker pins the non-Euler separator, the complete first-degree census,
the denominator-marked four-cube, and the exact Reynolds nonlinearity
witness.  It verifies (6)--(8), all 3645 denominator terms, the 48/96 chart
ranks, the unique shift and shifted column, all primitive chart placements,
and every order-two/three/four face on the three internal matchings.  The
frozen digest is

    980a89c64009ba6eedbaa7f2c6969b8fcf7b2bfe4031983a163360bf6126c91e

