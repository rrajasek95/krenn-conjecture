# Higher-cost mates reset the private-tail filtration

## Outcome

The local pattern

\[
 q_{45}\longrightarrow q_{35}\longrightarrow
 \text{inherited-only}                                  \tag{1}
\]

is not a global well-founded potential.  Exhaustively enumerate every
independent cost-at-least-two DQ/PS path that can mate the two terminal rows

\[
 R_3=(101200;00),\qquad R_5=(111112;01).                 \tag{2}
\]

There are 206 paths.  Exactly 204 create a new residual monomial containing
the active octagon edge (q_{45}) or (q_{35}); every path of cost three or
four does.  A cost-two DQ mate of (R_3) already returns to the prior row
(101222;00), closing the coarse cycle

\[
 q_{45}\longrightarrow q_{35}\longrightarrow
 \text{inherited-only}\longrightarrow q_{45}.           \tag{3}
\]

Thus tail rank and cost-plus-tail rank both fail as global termination
measures.  The smallest reset SCC is nevertheless unit-excluded by an exact
two-row polynomial identity.

The scope is all *independent one-path additions* of cost at least two over
the two normalized terminal branches.  Simultaneous unions of several such
paths can have additional cross products and remain beyond this theorem.

## Exhaustive higher-cost census

For (R_3), the complete operation-path distribution is

\[
\begin{array}{c|rrrrr}
&0&1&2&3&4\\ \hline
\mathrm{PS}&1&0&11&28&50\\
\mathrm{DQ}&0&0&1&4&10.
\end{array}                                              \tag{4}
\]

Among its cost-at-least-two paths, the reset counts are

\[
\begin{array}{c|rrr}
\text{cost}&2&3&4\\ \hline
\text{reset}&11&32&60\\
\text{no reset}&1&0&0.
\end{array}                                              \tag{5}
\]

For (R_5), the complete distribution is

\[
\begin{array}{c|rrrrr}
&0&1&2&3&4\\ \hline
\mathrm{PS}&1&1&14&34&40\\
\mathrm{DQ}&0&1&4&10&0.
\end{array}                                              \tag{6}
\]

The corresponding cost-at-least-two reset counts are

\[
\begin{array}{c|rrr}
\text{cost}&2&3&4\\ \hline
\text{reset}&17&44&40\\
\text{no reset}&1&0&0.
\end{array}                                              \tag{7}
\]

The two non-reset exceptions are pinned with their complete source keys by
the checker.  They do not rescue (1): the other 204 paths, including every
higher-cost path, explicitly regenerate an active tail face.

## Smallest recurrent reset

Start on the (X_3) terminal branch.  Its private row is

\[
 R_3=bc(S_0X_3+A_{00}L_{13}),                           \tag{8}
\]

where the cost-two DQ mate introduces

\[
 A_{00}=a_{00},\qquad L_{13}=q_{13}^{0,2}.              \tag{9}
\]

The target word is (101200); hence the DQ matching

\[
                   67\mid02\mid13\mid45                \tag{10}
\]

uses the inherited colour-zero edge (b=q_{45}^{0,0}).  The same new direct
and mixed edge reappear at word (101222), where the last edge is now the
active octagon cell (q_{45}^{2,2}).  The reset row is

\[
 R_0=c\{S_0Xq_{35}+q_{45}(S_0X_3+A_{00}L_{13})\}.       \tag{11}
\]

Equations (8) and (11) obey

\[
 \boxed{bR_0-q_{45}R_3=XS_0bcq_{35}.}                  \tag{12}
\]

The right side is a unit on the inherited active torus.  Therefore the
smallest recurrent SCC has no point: repairing (R_3) with this DQ mate
necessarily reopens (R_0), and repairing both contradicts (12).

At the normalized rational point, one may take (A_{00}=1,L_{13}=-1) to
cancel the value (+1) of (R_3).  The reset contribution at (R_0) is then
(+2), making the recurrence visible numerically as well as symbolically.

## Consequence for termination strategies

The three coarse states

\[
 T_{45},\qquad T_{35},\qquad T_0
\]

are mutually reachable via the already constructed minimum migrations and
the cost-two return (9)--(11).  They form one strongly connected component.
No ordering based only on external cost, word/head lex, or active-tail edge
can be well founded on the full external response graph.

What survives is algebraic rather than order-theoretic: the smallest reset
cycle carries the unit certificate (12).  A global proof along this lane
would need to attach compatible unit certificates to simultaneous higher-
cost SCCs, not seek a monotone tail potential.  The present checker supplies
the exact finite reset census and the first such SCC certificate.

## Verification

Run

```text
python computations/verify_n8_pure21_private_tail_higher_cost_reset_gate.py
python computations/verify_n8_pure21_private_tail_higher_cost_reset_gate.py --mode census
python computations/verify_n8_pure21_private_tail_higher_cost_reset_gate.py --mode resets
python computations/verify_n8_pure21_private_tail_higher_cost_reset_gate.py --mode cycle
python computations/verify_n8_pure21_private_tail_higher_cost_reset_gate.py --mode potential
```

The dependency-free checker enumerates both 105-path fibres, expands every
independent cost-at-least-two addition, scans every word/head residual for
(q_{45}/q_{35}) reset monomials, pins both exceptions, constructs the first
recurrent DQ square with full operation/fine data, verifies (12), and checks
the coarse SCC directly.
