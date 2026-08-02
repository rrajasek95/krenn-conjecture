# Independent audit of the repaired \(6R\) factor obstruction

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome

The repaired common-isotropic packet \(M^\dagger\) has two separate
factored pure L0 faces but no shared endpoint-star assignment realizing
both pure targets and both mixed zeros. This note independently audits that
obstruction in two ways:

1. it checks the Euler/gauge reduction from the complete four-slice
   equations to the weakened edge-scalar equations; and
2. it uses the alternate four-edge core
   \[
                              01,05,15,45,                     \tag{1}
   \]
   rather than the primary certificate's core \(01,04,05,45\).

The alternate core sees the second repaired block \(M_{15}=E_{10}\), while
the primary core sees \(M_{04}=E_{10}\). Its independently ordered exact
ideals are the unit ideal over both \(\mathbb Q\) and
\(\mathbb F_{32003}\).

## Why the original all-rank-one guard must be replaced

The earlier exact rank-\(55\), all-six-rank-one/R2 packet from the
[one-sided guard](level-two-one-sided-rank55-guard.md) does not admit either
pure target even linearly. If \(D=d\Psi_M\), exact rational and three-prime
row reduction gives

\[
\begin{array}{c|cccc}
 &D&[D\mid e_{0^6}]&[D\mid e_{1^6}]&
       [D\mid e_{0^6}\mid e_{1^6}]\\ \hline
\operatorname{rank}&55&56&56&57.
\end{array}                                                     \tag{2}
\]

Thus endpoint-star factorization cannot work on that fixed packet. A
rank-preserving replacement or deformation is logically necessary. The
two-block repair of the sharp packet supplies exactly that replacement.

## Exact Euler/gauge reduction

For one endpoint-colour slice \(st\), write \(N^{st}\) for the factored
star tangent and \(w_{st}\) for the direct endpoint cell. Let \(R^{00}\)
be the single tangent cell \(01(0,0)\), let \(R^{11}\) be \(45(1,1)\), and
put \(R^{01}=R^{10}=0\). The four desired slice equations are

\[
 w_{st}\Psi(M^\dagger)+d\Psi_{M^\dagger}(N^{st})
                     =d\Psi_{M^\dagger}(R^{st}).              \tag{3}
\]

The repaired differential has rank \(55\). Its five universal vertex
gauges are independent, so they are its entire kernel. Euler's identity

\[
                       d\Psi_{M^\dagger}(M^\dagger)
                              =3\Psi(M^\dagger)                \tag{4}
\]

turns (3) into

\[
 N^{st}_{ru}=R^{st}_{ru}
   +\left(\mu_r^{st}+\mu_u^{st}-\frac{w_{st}}3\right)
                                      M^\dagger_{ru}.          \tag{5}
\]

There is no missing trace condition here. Starting with
\(\sum_r\mu_r^{st}=0\), set

\[
                 \alpha_r^{st}=\mu_r^{st}-\frac{w_{st}}6.     \tag{6}
\]

Then the coefficient in (5) is precisely
\(\alpha_r^{st}+\alpha_u^{st}\). Allowing a completely independent scalar
\(\lambda_{ru}^{st}\) on every retained edge is a further relaxation.
Therefore a unit ideal for the relaxed system is a valid obstruction to
every global shared-star completion.

The audit verifies (4) directly on all \(64\) outputs and checks (6) on all
fifteen residual edges with exact rational arithmetic.

## An alternate four-edge unit ideal

On vertices \(\{0,1,4,5\}\), retain the blocks

\[
\begin{aligned}
M_{01}&=\begin{pmatrix}2&3\\4&6\end{pmatrix},&
M_{05}&=\begin{pmatrix}6&7\\13&9\end{pmatrix},\\
M_{15}&=\begin{pmatrix}0&0\\1&0\end{pmatrix},&
M_{45}&=\begin{pmatrix}1&0\\0&0\end{pmatrix}.
\end{aligned}                                                   \tag{7}
\]

For every \(st\in\{0,1\}^2\), every retained edge \(ru\), and every binary
cell \(ab\), impose the weakened equations

\[
 U_r^s(a)V_u^t(b)+V_r^t(a)U_u^s(b)
     =R_{ru}^{st}(a,b)+\lambda_{ru}^{st}M_{ru}^\dagger(a,b).   \tag{8}
\]

There are \(32\) star coordinates, \(16\) independent edge scalars, and
\(64\) quadrics. Exact degree-reverse-lexicographic elimination gives

\[
                              \operatorname{std}(I)=(1)       \tag{9}
\]

over both fields. This audit reverses the star-variable, edge, slice,
cell, and generator orders relative to the primary calculation. Its frozen
equation-ledger SHA-256 is

```text
eb77bc41b671a8ba571109996d1a70294dd98d6933421e38b739849043def077
```

The two generated program hashes are

```text
Q       c7cae01515c6efa6e99cad9fb1cfc20f97c32dfcc2761a86b9b80c3b7f40e40c
F32003  b16653b278bce9b12edbddecbb15ab8a9357625443c012d512fea05e5c7c8956
```

Thus the simultaneous obstruction is not an artifact of the first repaired
block or of the primary elimination order.

## The first two-edge escape still fails after gauge coupling

There is a real limitation to independent edge scalars. Starting from
\(M^\dagger\), additionally replace

\[
                         M_{05}=M_{14}=E_{01}.                 \tag{10}
\]

Call this packet \(M^\ddagger\). It remains on the full boundary:

\[
 \operatorname{rank}d\Psi_{M^\ddagger}=55,
 \qquad
 \operatorname{rank}(d\Psi_{M^\ddagger})_{\rm mixed}=53,      \tag{11}
\]

over the rationals and three prime fields. Both localized pure tangent
columns remain exact, and the same two physical R2 witnesses at all six
roots retain nonzero complementary cofactors.

The full \(K_4\) on \(\{0,1,4,5\}\), with an independent scalar on every
edge and slice, is now genuinely nonempty: its reduced Gröbner basis has
size \(99\). Thus (10) escapes both four-edge independent-scalar
certificates; adding the remaining \(K_4\) edges does not restore them.

However, the actual kernel coefficients are coupled vertex sums. Replace
the \(24\) independent edge scalars on this full \(K_4\) by the \(16\)
vertex variables \(\alpha_r^{st}\) from (6). The resulting exact system has

\[
                 48\text{ variables},\qquad96\text{ quadrics}. \tag{12}
\]

Its reduced basis is again \((1)\) over both \(\mathbb Q\) and
\(\mathbb F_{32003}\). Consequently this first local escape fails: a
surviving deformation must evade the vertex-sum coupling itself, not merely
the earlier independent-edge cores.

The program hashes for the independent and coupled systems are

```text
independent Q       d37e6c21521709bda0a519e520e44894698fd053789c4ba862d7f5976a369d0e
coupled Q           b3458dd34149dfbd6178edf2236c3a82014872823b1e7072ddac283d4526189e
coupled F32003      99bb60737139882ec8a8e050a5294e0169519571b458954c20db42ef9df64d8a
```

## Exact audit

The checker
[audit_level_two_six_rank_one_repaired_factor_obstruction_independent.py](../computations/audit_level_two_six_rank_one_repaired_factor_obstruction_independent.py)

- reconstructs the old guard's rank signature (2);
- independently verifies rank \(55\), the five-dimensional gauge kernel,
  Euler's identity, direct-cell absorption, and the two localized pure
  tangent columns on \(M^\dagger\);
- pins the alternate blocks (7) and regenerates all \(64\) equations (8);
- constructs the two-edge escape (10), rechecks its complete rank,
  incidence, gauge-kernel, and R2 signatures, then distinguishes its
  nonunit \(56\)-variable independent-edge system from its unit
  \(48\)-variable vertex-coupled system; and
- requires the reduced basis \((1)\) over \(\mathbb Q\) and
  \(\mathbb F_{32003}\) using reversed orderings.

Python uses only the standard library; Singular is the sole external
executable. The conclusion concerns this fixed repaired packet, not the
full \(6R\) stratum.
