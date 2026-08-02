# The repaired full-\(K_4\) binary-pair coupled census has no modular survivor

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome

Start with the repaired packet \(M^\dagger\), keep

\[
                         M_{04}=M_{15}=E_{10},
\]

and independently vary \(M_{05}\) and \(M_{14}\) over all sixteen binary
\(2\times2\) matrices. Of the resulting \(16^2=256\) ordered pairs, exactly
172 retain differential rank \(55\). Every one of those 172 gives the unit
ideal over \(\mathbb F_{101}\) for the actual vertex-sum-coupled four-slice
factor system on the full \(K_4=\{0,1,4,5\}\).

Thus this finite grid contains no **modular** rank-\(55\) escape. There are
no \(\mathbb F_{101}\)-nonunit survivors to rerun over \(\mathbb Q\) and
\(\mathbb F_{32003}\), so those exact survivor ledgers are empty. A unit
ideal after reduction modulo one prime does not by itself prove that the
corresponding rational ideal is a unit ideal. The result is therefore a
discovery-field exhaustion of this binary grid, not an exact obstruction
over \(\mathbb Q\) for all 172 cases.

## Exact rank and incidence census

Encode a binary block by

\[
 m=M(0,0)+2M(0,1)+4M(1,0)+8M(1,1),\qquad0\leq m<16.
\]

The checker visits the ordered pairs \((m_{05},m_{14})\) lexicographically.
Its exact rank census is

\[
\begin{array}{c|rrrrrrr}
\operatorname{rank}d\Psi_M&48&50&51&52&53&54&55\\ \hline
\#\text{ pairs}&1&3&12&20&8&40&172.
\end{array}
\]

The mixed-output rank is always two less. Indeed, throughout the grid the
literal tangent cell \(01(0,0)\) is the column \(e_{0^6}\), while
\(45(1,1)\) is the column \(e_{1^6}\). These are private pivots for the two
pure rows. For every rank below 55 the checker computes rational rank and
requires agreement with ranks modulo 101 and 32003. At rank 55, the five
independent vertex gauges give the rational upper bound 55, while a
nonzero minor modulo 101 gives the matching lower bound.

Both localized pure tangent columns consequently survive all 256 changes.
The fixed physical R2 witnesses also survive:

\[
\begin{array}{c|cc}
\text{root}&\text{output }0&\text{output }1\\ \hline
0&03&02\\
1&12&13\\
2&23&20\\
3&32&31\\
4&45&40\\
5&54&51.
\end{array}
\]

Every displayed complementary cofactor is nonzero in every case; the
minimum number of nonzero cofactor words is four for all 256 pairs.

## The coupled full-\(K_4\) census

For each endpoint slice \(st\in\{0,1\}^2\), introduce the star variables
\(U_r^s(a),V_r^t(a)\) and one gauge variable \(\alpha_r^{st}\) at each
vertex \(r\in\{0,1,4,5\}\). On all six edges \(ru\) of this \(K_4\), impose

\[
 U_r^s(a)V_u^t(b)+V_r^t(a)U_u^s(b)
 =R_{ru}^{st}(a,b)
  +(\alpha_r^{st}+\alpha_u^{st})M_{ru}(a,b).                 \tag{1}
\]

Here \(R^{00}\) is supported at \(01(0,0)\), \(R^{11}\) is supported at
\(45(1,1)\), and \(R^{01}=R^{10}=0\). Equation (1) uses the actual coupled
vertex sums, not independent scalars on the 24 edge-slices. Each case has
48 variables and 96 quadrics.

The resulting classification is

\[
\begin{array}{l|r}
\text{class}&\#\text{ pairs}\\ \hline
\text{exact differential rank below }55&84\\
\text{rank }55\text{ and unit ideal over }\mathbb F_{101}&172\\
\text{rank }55\text{ and nonunit over }\mathbb F_{101}&0.
\end{array}
\]

The SHA-256 ledger of the 172 rank-\(55\) mask pairs is

```text
ce4d50c94e3ee71ca79da513234d214894705835ac72afad45426b60bc4315de
```

The combined ledger of the eight deterministic Singular programs over
\(\mathbb F_{101}\) is

```text
fc43415ba36a41f1af993b3f66d4cb8b9d6df496f07b44b7ce593795e54a10a3
```

The checker
[verify_level_two_repaired_full_k4_binary_pair_coupled_census.py](../computations/verify_level_two_repaired_full_k4_binary_pair_coupled_census.py)
regenerates all ranks, pure columns, R2 cofactors, equations, reduced bases,
and ledgers. Python uses only the standard library; Singular is the sole
external executable. The conclusion concerns this finite binary
\((M_{05},M_{14})\) grid with the rest of \(M^\dagger\) fixed, not the full
\(6R\) stratum.
