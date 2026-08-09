# Hall certificates versus a two-by-two full-nine minor

The seven-cell private-row audit supplies a finite place to test the
proposed compound-map proof.  Regard each private output word as a row of
the two pair charts by recording its endpoint colours

\[
(w_p,w_q)\quad\text{and}\quad(w_p,w_r).                   \tag{1}


A pair of words occupies a genuine `2x2` compound position in a chart when
both its row labels and its column labels differ.  If the Hall obstruction
could always be selected in such a position, it would be evidence for a
minor of the weighted map

\[
                         t\longmapsto t q^{[2]}           \tag{2}


on the six-site residual complement.

## Exact active census

Among the 7,200 four-cell parents, 5,110 make both OO arm cofactors
support-nonempty.  Their minimal Hall certificate sizes are

\[
4940\text{ of size }2,qquad170\text{ of size }3.          \tag{3}


The two size-four Hall certificates in the unrestricted census are **not**
doubly active: both activate only arm `04`.  They are therefore not
alignment degeneracies of the selected curved two-arm stratum.

For the 4,940 size-two active parents, allowing every minimal Hall pair
gives

\[
\begin{array}{c|rrr}
\text{compound availability}&\text{neither chart}&
\text{some chart, not both}&\text{both charts}\\ \hline
\text{parents}&114&720&4106.
\end{array}                                                \tag{4}


For all 170 size-three active parents, some minimal certificate contains a
compound pair: eight do so in only one chart and 162 in both.

Thus 4,996 of 5,110 active parents admit a compound Hall certificate, but
114 do not.  The failure is not one isolated overlap type.  The 114
parents occur in every leading-cofactor union type

\[
P_2+C_2+C_2,\qquad P_4+C_2,\qquad P_6,                    \tag{5}


and across all six shore patterns present in the four-cell census.  In
112 cases the support consists of a pure-1 completion plus one non-anchor
cell; two cases have four pure-1 cells.  Hence the two exceptional
size-four Hall cores are not the source of the compound failure.

## Verdict and exact next target

The Hall theorem does **not** by itself promote to a universal literal
`2x2` minor of the endpoint row labels.  This is a counterguard to reading
the private-row transversal as the determinant

\[
                         T_{aa}T_{bb}.                    \tag{6}


It does not refute a weighted Lefschetz/disjointness-map theorem.  Such a
theorem may select a non-private row combination or take a minor only after
quotienting by the two active cofactor leaders.  The honest remaining
lemma is therefore:

1. localize one nonzero coefficient in each arm cofactor;
2. form the coefficient matrix of (2) on the resulting two leader
   quotients;
3. prove that some `2x2` minor carrying two diagonal target anchors is
   nonzero; and
4. use curved rank-one full-nine alignment to force that same minor to
   rank at most one.

The 114 profiles are the finite regression set for step 3.  A proof which
selects only two private output fibres is already false on them.

## Reproduction

```text
python computations/verify_oo_c8_seven_cell_activity_frontier.py
python -O computations/verify_oo_c8_seven_cell_activity_frontier.py
```

The checker reconstructs all Hall repair families, arm activity, pair-row
labels, and every minimal-certificate compound choice exactly.
