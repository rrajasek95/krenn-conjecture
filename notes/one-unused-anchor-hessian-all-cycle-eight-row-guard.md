# Anchor/Hessian boundary: one eight-row guard and one three-diagonal guard

## 1. Outcome

The seven-row guard in
[the two-anchor Hessian audit](two-anchor-hessian-all-cycle-seven-row-guard.md)
leaves both unused diagonal targets absent.  The packet below strengthens
that boundary by supplying one of them as a literal, sitewise-independent
tensor equation.

On eight sites it is an ordinary two-colour matching source whose complete
signature is

\[
                         X_a^8+X_b^8.                    \tag{1}
\]

After deleting two sites, its residual data satisfy all six off-diagonal
rows and the two diagonal rows

\[
 p_as_aq^{[2]}=X_a^6,\qquad p_bs_bq^{[2]}=X_b^6.         \tag{2}
\]

Only the third diagonal row is missing.  Nevertheless, the rank-one
direct-zero selector \(E_{aa}\) has exactly two blocked sites, a unique
complementary dark matching, and four possible literal four-cycle
covectors.  The scalar \(K_6\) Hessian has rank ten, and **all four
individual covectors fail to annihilate its kernel**.

Thus the eight literal row identities, together with the cap and dark-cut
data retained here, do not by themselves force one of these four literal
cycles to be compatible.  This statement is deliberately about the
individual choices: their linear span does contain a cap-detecting
compatible mixture, exhibited in Section 4.  The guard therefore does
**not** prove that both anchors are necessary for aggregate span
compatibility, nor does it rule out a lemma using an additional
nondegeneracy or second-chart hypothesis absent from this packet.

This is not a complete-nine counterexample.  The \(\delta\delta\) row is
zero rather than \(X_\delta^6\), the direct block is zero, and each endpoint
star family has rank two.  Those limitations are part of the exact scope.

There is a complementary exact packet.  Add one monochromatic
\(\delta\)-matching to the same graph.  Then **all three diagonal anchors**
hold as literal pure tensors and both endpoint-star triples are injective;
the same cap and the same four individual Hessian failures remain.  Four
off-diagonal cells are now nonzero.  Thus even the two unused diagonal
equations taken together do not force any one of the four displayed
literal cycles to be compatible in the absence of their companion
off-diagonal equations.  This is an exact boundary for the literal-cycle
selection route, not for signed cycle mixing.

## 2. An exact two-colour eight-site source

Let the eight sites be \(0,\ldots,7\), with \(6,7\) the two sites to be
deleted.  Give all edges weight one.  The colour-\(a\) edges are

\[
  06,\quad17,\quad03,\quad15,\quad23,\quad45,             \tag{3}
\]

and the colour-\(b\) edges are

\[
  01,\quad24,\quad36,\quad57.                             \tag{4}
\]

The union of (3)--(4) has exactly two perfect matchings:

\[
  06\mid17\mid23\mid45,
  \qquad
  01\mid24\mid36\mid57.                                  \tag{5}
\]

They are respectively all \(a\) and all \(b\), proving (1) without any
cancellation.  In particular, this packet is a fully physical two-colour
source, not merely a collection of scalar row equations.

Delete sites \(6,7\).  In the six-site site-square-zero algebra put

\[
\begin{aligned}
 q={}&x_{0,a}x_{3,a}+x_{1,a}x_{5,a}
       +x_{2,a}x_{3,a}+x_{4,a}x_{5,a}\\
    &+x_{0,b}x_{1,b}+x_{2,b}x_{4,b},                       \tag{6}\\
 p_a={}&x_{0,a},&s_a={}&x_{1,a},\\
 p_b={}&x_{3,b},&s_b={}&x_{5,b},\\
 p_\delta={}&0,&s_\delta={}&0,
 \qquad d=0.                                               \tag{7}
\end{aligned}
\]

The only matching of \(q\) on the complement of the \(p_as_a\) endpoints
is \(23\mid45\), and the only matching on the complement of the
\(p_bs_b\) endpoints is \(01\mid24\).  The two cross complements have no
matching.  Therefore the complete row ledger is

\[
 d_{ij}q^{[3]}+p_is_jq^{[2]}
 =\begin{cases}
    X_a^6,&(i,j)=(a,a),\\
    X_b^6,&(i,j)=(b,b),\\
    0,&i\ne j\text{ or }i=j=\delta.
  \end{cases}                                              \tag{8}
\]

This verifies eight of the literal nine equations.  Relabelling \(b\) and
\(\delta\) shows that either one of the two unused anchors can be supplied
while the other remains absent.

## 3. The cap and the unique dark matching

Take the selector \(\ell=E_{aa}\).  Since \(d=0\), it is direct-zero, and

\[
              \beta=p_as_a=x_{0,a}x_{1,a},\qquad
              \beta q^{[2]}=X_a^6.                         \tag{9}
\]

Its local cap planes are \(\mathbb Ce_a\) at sites \(0,1\) and zero at
the other four sites.  Thus its target-blocking set is exactly
\(\{0,1\}\).  Contracting the two cap sites by \(e_a^*\) gives the pure
coefficient cut

\[
 \beta_{01}(e_a^*,e_a^*)
       (q_a|_{\{2,3,4,5\}})^{[2]}
 =x_{2,a}x_{3,a}x_{4,a}x_{5,a},                            \tag{10}
\]

and the unique dark matching is

\[
                              23\mid45.                    \tag{11}
\]

At the cap edge, the \((a,a)\)-coefficient of \(q_{01}\) and the direct
block both vanish, while the endpoint-star assignment is \(E_{aa}\).
Hence the same selector detects the literal transition \(-E_{aa}\) with
value \(-1\).  The packet therefore retains both the physical coefficient
cut and nonradial transition visibility.

## 4. All four individual cycle normals fail

Probe every residual site by \(e_a^*\).  The resulting scalar array has
support

\[
                         Q_a=\{03,15,23,45\}.              \tag{12}
\]

For either dark edge \(uv\in\{23,45\}\), and either orientation of its
endpoints, use

\[
\begin{aligned}
 \kappa_{uv}^{(0)}(r)&=r_{01}r_{uv}-r_{0u}r_{1v},\\
 \kappa_{uv}^{(1)}(r)&=r_{01}r_{uv}-r_{0v}r_{1u}.          \tag{13}
\end{aligned}
\]

All four functions vanish at \(q_a\), and all four differentials evaluate
to one on the cap vector \(\mathbf e_{01}\).  Explicitly,

\[
\begin{array}{c|cccc}
 (uv,\epsilon)&(23,0)&(23,1)&(45,0)&(45,1)\\ \hline
 d\kappa_{uv}^{(\epsilon)}{}_{q_a}
   &\mathbf e_{01}&\mathbf e_{01}-\mathbf e_{12}
   &\mathbf e_{01}-\mathbf e_{04}&\mathbf e_{01}.
\end{array}                                                \tag{14}
\]

Let \(H_{q_a}\) be the fifteen-by-fifteen hafnian Hessian.  Exact
elimination gives

\[
 \operatorname{rank}H_{q_a}=10,
 \qquad
 z=\mathbf e_{01}-\mathbf e_{04}-\mathbf e_{12}
                         +\mathbf e_{24}\in\ker H_{q_a}.   \tag{15}
\]

The four pairings, in the order of (14), are

\[
                              1,\quad2,\quad2,\quad1.       \tag{16}
\]

They are all nonzero.  Symmetry of \(H_{q_a}\) therefore proves

\[
 d\kappa_{uv}^{(\epsilon)}{}_{q_a}
       \notin\operatorname{row}H_{q_a}
 \quad(uv\in\{23,45\},\ \epsilon\in\{0,1\}).             \tag{17}
\]

This exhausts the literal cycle choices furnished by the unique dark
matching.

It does **not** exhaust their linear span.  In fact the signed mixture

\[
 \lambda_{\rm mix}
   =-2d\kappa_{23}^{(0)}{}_{q_a}
       +d\kappa_{23}^{(1)}{}_{q_a}
   =-\mathbf e_{01}-\mathbf e_{12}                        \tag{17a}
\]

still detects the cap, with \(\lambda_{\rm mix}(\beta)=-1\), and has the
explicit Hessian pullback

\[
 H_{q_a}(-\mathbf e_{03}+\mathbf e_{15}-\mathbf e_{23})
                         =\lambda_{\rm mix}.              \tag{17b}
\]

Thus this guard has no aggregate cycle-*span* obstruction.  Its exact
negative conclusion is only that none of the four individual literal
choices works.  Whether the signed mixture in (17a) has the required
filtered source provenance is a separate question not tested here.

## 5. Exact implication for the remaining proof

The guard satisfies more than a scalar replacement for one missing row:
equation (2) is the full pure tensor \(X_b^6\), with its six independent
site factors, and (1) verifies every mixed word on the original eight
sites.  Yet every individual literal-cycle conclusion still fails.

Consequently, a positive lemma based only on the row identities and the
cap/dark-cut facts shared with this packet cannot select one individual
literal cycle by the decoupled recipe

1. use the \(b\)-anchor alone to obtain a compatible cycle;
2. repeat with the \(\delta\)-anchor; and
3. combine the two conclusions afterward.

Within that restricted route, a still-unruled positive step would have to
couple the two unused diagonal rows through their common decorated
quadratic and endpoint stars.  Possible mechanisms include a genuinely
mixed \(b/\delta\) coefficient, a two-by-two diagonal-row syzygy, or a
second-chart identity retaining both labels; the guard does not prove
that this list is exhaustive.  Signed cycle mixing is a different route
and already repairs the aggregate Hessian equation in this guard; it
still faces the separate filtered-provenance problem.

## 6. Both unused anchors without the off-diagonal cancellations

The preceding claim that diagonal anchors alone do not force an individual
literal choice also has an exact physical certificate.  Add the four
colour-\(\delta\) edges

\[
                         04,\quad13,\quad27,\quad56        \tag{18}
\]

to the eight-site graph (3)--(4), again with unit weights and the same
colour at both endpoints.  The enlarged union has nine perfect matchings.
Exactly three have the same colour at deleted sites \(6,7\): they are the
three displayed monochromatic matchings.  Every other matching has
different colours at sites \(6,7\).  Hence, after deletion, the three
diagonal rows are exactly

\[
                         X_a^6,\qquad X_b^6,\qquad
                         X_\delta^6.                       \tag{19}
\]

More explicitly, add

\[
 q_\delta=x_{0,\delta}x_{4,\delta}
              +x_{1,\delta}x_{3,\delta},qquad
 p_\delta=x_{5,\delta},qquad
 s_\delta=x_{2,\delta}.                                  \tag{20}
\]

The three cap complements are respectively

\[
  23_a\mid45_a,\qquad
  01_b\mid24_b,\qquad
  04_\delta\mid13_\delta,                                \tag{21}
\]

which proves (19) directly.  The triples

\[
 (p_a,p_b,p_\delta)=(x_{0,a},x_{3,b},x_{5,\delta}),
 \qquad
 (s_a,s_b,s_\delta)=(x_{1,a},x_{5,b},x_{2,\delta})        \tag{22}
\]

are injective.  The four nonzero off-diagonal response cells are

\[
 (a,b),\qquad(a,\delta),\qquad(b,\delta),\qquad(\delta,a), \tag{23}
\]

with one matching in each of the first two cells and two matchings in each
of the last two.  The other two off-diagonal cells vanish.  Their decorated
words are pairwise audited by the checker, so none is being hidden by a
scalar projection.

The \(a\)-scalar residual quadratic, the selector \(E_{aa}\), the cap cut,
and the Hessian are unchanged by (18).  Equations (12)--(17) therefore
continue to hold verbatim, including the span repair (17a)--(17b).  This
second guard proves the sharper, literal-selection boundary

\[
 \boxed{\begin{gathered}
 \text{both unused diagonal anchors alone do not force any one of the}\\
 \text{four literal cycles; their off-diagonal companions are omitted.}
 \end{gathered}}                                           \tag{24}
\]

It still is not a complete-nine source: the four cells in (23) must be
zero in one.  Together, the eight-row guard and the three-diagonal guard
rule out two decoupled *individual-cycle* strategies: adding just one
missing diagonal row, and using all three diagonal rows without their
off-diagonal companions.  A genuinely coupled diagonal/off-diagonal
full-nine identity is one remaining positive input, but these packets do
not prove that every one of the nine rows is separately necessary.  They
make no necessity claim at all for a mixed-cycle theorem.

The dependency-free checker
[`verify_one_unused_anchor_hessian_all_cycle_eight_row_guard.py`](../computations/verify_one_unused_anchor_hessian_all_cycle_eight_row_guard.py)
enumerates both eight-site matching packets, rebuilds their residual rows
as decorated tensors, checks the cap quotient, and verifies the Hessian
kernel and all four augmented-rank failures.
