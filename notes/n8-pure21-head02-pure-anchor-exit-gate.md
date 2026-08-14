# The private head chase exits to a pure colour-one row

## Outcome

Retain the exact SCC factorization and the forced cell
(J=q_{03}^{0,1}).  The mandatory row

\[
 F_{02}=TJLb,qquad(001100;02),\quad
 \mathrm{DQ},\quad67\mid03\mid12\mid45                \tag{1}
\]

has exactly one positive minimum-cost mate:

\[
                         R=s_2(3;1).                    \tag{2}
\]

Its target contribution (P_0RLb) closes (F_{02}), but the same endpoint
creates the private pure-colour-one row

\[
 \boxed{G_{12}=P_1Rce,qquad(111111;12),\quad
        \mathrm{PS},\quad65\mid73\mid02\mid14.}         \tag{3}
\]

The two rows satisfy

\[
 \boxed{P_1ceF_{02}-P_0LbG_{12}=P_1ceTJLb.}             \tag{4}
\]

The right side is a unit on the active chart.  Hence the same-word head
sequence cannot recur: the forced chase is

\[
 (001100;01)\longrightarrow(001100;02)
 \longrightarrow(111111;12),                           \tag{5}
\]

where the last arrow is a pure-word exit.

## Exact minimum classification

For word (001100) and head (02), the current DQ path in (1) costs zero.
Exhaustive compatible-path enumeration gives

\[
\begin{array}{c|rrrrr}
&0&1&2&3&4\\ \hline
\mathrm{DQ}&1&0&6&8&0\\
\mathrm{PS}&0&1&9&30&50.
\end{array}                                              \tag{6}
\]

The unique cost-one PS path has (p)-site 0, (s)-site 3, and remaining
matching (12\mid45).  Its only missing cell is (R).  Thus (2) is the full
minimum orbit, not a selected representative.

With (R) symbolic, the complete rows are

\[
 F_{02}=Lb(TJ+P_0R),\qquad G_{12}=P_1Rce.               \tag{7}
\]

Eliminating (R) gives (4).  At the rational normalization
(T=J=-1) and all other displayed inherited factors equal one, so
(F_{02}=1+R).  Closing it forces (R=-1), and then (G_{12}=-1).

The new endpoint leaves the earlier SCC rows and (F_{01}) unchanged.  It is
therefore an exit from the exact SCC boundary, not a return edge.

## Exhaustive replay

Insert (R=-1) and replay all 6561 rows.  There are ten incremental changes
and 58 nonzero full residual rows.  The target becomes zero and the pure exit
has value (-1):

```text
001100:02  -1   final 0
111111:12  -1   final -1
```

All earlier exact rows remain zero.  The checker pins the complete ten-row
incremental ledger, including the other head-(22/02/12) response faces.

## Finite head-index escalation theorem

The two exact identities are

\[
\begin{aligned}
D F_{02}-T F_{01}&=-TP_0S_1Lb,\\
P_1ceF_{02}-P_0LbG_{12}&=P_1ceTJLb.
\end{aligned}                                            \tag{8}
\]

They prove, on this fixed word/fine chart:

1. closing the private head-(01) row forces the head-(02) DQ face;
2. closing that head-(02) face forces the pure word/head-(12) PS face; and
3. neither step returns to the exact SCC.

This is a finite escalation theorem for the current branch, not a global
ordering on all head labels.  Its terminal datum is the pure response row
(3).  A recurrent same-word head cycle does not occur.

The shortest continuation is to classify mates of the pure row
(111111;12).  Because it is supported entirely on inherited colour-one
anchors plus (R), it is a stronger candidate for an immediate normalized
unit/anchor exclusion than the preceding mixed-word rows.

## Verification

Run

```text
python computations/verify_n8_pure21_head02_pure_anchor_exit_gate.py
python computations/verify_n8_pure21_head02_pure_anchor_exit_gate.py --mode classification
python computations/verify_n8_pure21_head02_pure_anchor_exit_gate.py --mode symbolic
python computations/verify_n8_pure21_head02_pure_anchor_exit_gate.py --mode replay
python computations/verify_n8_pure21_head02_pure_anchor_exit_gate.py --mode escalation
```

The checker derives all 105 compatible paths, proves uniqueness of (R),
retains every word/head/operation/fine label, verifies (4), checks absence of
an SCC return, replays every row, and records the finite escalation schema
(5)--(8).
