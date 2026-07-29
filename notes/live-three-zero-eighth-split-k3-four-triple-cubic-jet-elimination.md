# The eighth split: four-triple cubic-jet elimination

## 1. Result

Work at \(h=8,k=3\).  Suppose that the exceptional multiset contains four
value classes of multiplicity exactly three.

**Theorem 1.1 (four exact triples).**  This configuration is impossible on
the no-extra-singular stratum.

For each three of the four triple values, the three legal \((3,3,2)\)
roles determine the second and third all-role logarithmic jets in terms of
the first.  Applied to the four overlapping triples, those identities put
the four values among the common roots of one quartic \(R\) and one sextic
\(S\).  An exact pseudo-remainder certificate says that a genuine quartic
\(R\) cannot divide \(S\).  If its leading coefficient vanishes, \(R\) is
a nonzero cubic and cannot have four distinct roots either.

Together with the simpler five-triple overlap theorem, this closes every
updated third-order residual having at least four exact triple classes.

## 2. The two all-role identities

Let \(X=\{x_1,x_2,x_3,x_4\}\) be four exact triple values.  Fix any
three-set \(Y\subset X\) and distinguish \(a\in Y\).  The core

\[
                         a^2\prod_{y\in Y\setminus\{a\}}y^3 \tag{1}
\]

selects eight labels in three classes and leaves the singleton mate at
\(a\).  Its Hermite residual is a nonzero constant.  As in
[the five-triple theorem](live-three-zero-eighth-split-k3-seven-triple-common-pole-closure.md),
the order-three common-pole equation, for the three choices of \(a\), is
affine in

\[
                         d(a)=-{2\mu\over a^2-\mu^2}.     \tag{2}
\]

The three \(d\)-values are distinct.  If \(T_Y,V_Y,W_Y\) denote the first
three logarithmic jets with every member of \(Y\) formally assigned role
three, the affine equation therefore vanishes identically and gives

\[
                 V_Y={T_Y\over\mu}-T_Y^2,qquad
                 W_Y=2T_Y^3-{3T_Y^2\over\mu}.            \tag{3}
\]

These are exact Bell-polynomial identities, not truncated
approximations.

Let \(T_0,V_0,W_0\) be the corresponding jets with all four members of
\(X\) formally assigned role three.  Put

\[
 u_i={x_i\over\mu},\qquad
 \tau=\mu T_0,\qquad v=\mu^2V_0,\qquad \omega=\mu^3W_0. \tag{4}
\]

The dimensionless role-three jets are

\[
\begin{aligned}
 A(u)&=\mu\phi_3(\mu u)=-{u+7\over u^2-1},\\
 B(u)&=\mu^2\psi_3(\mu u)
      ={3\over(u+1)^2}+{4\over(u-1)^2},\\
 C(u)&=\mu^3\chi_3(\mu u)
      ={6\over(u+1)^3}-{8\over(u-1)^3}.                 \tag{5}
\end{aligned}
\]

Apply (3) to \(Y=X\setminus\{x_i\}\) and put
\(q_i=\tau-A(u_i)\).  For every \(i\),

\[
                         B(u_i)+q_i-q_i^2-v=0,qquad
                         C(u_i)+2q_i^3-3q_i^2-\omega=0.  \tag{6}
\]

## 3. The quartic and sextic

Write \(D=u^2-1\), \(q=\tau-A(u)\), and clear the structurally nonzero
denominators in (6):

\[
\begin{aligned}
 R(u)&=D^2\bigl(B(u)+q-q^2-v\bigr),\\
 S(u)&=D^3\bigl(C(u)+2q^3-3q^2-\omega\bigr).            \tag{7}
\end{aligned}
\]

Put

\[
                         L=-\tau^2+\tau-v.               \tag{8}
\]

Direct expansion gives

\[
\begin{split}
R(u)={}&Lu^4+(1-2\tau)u^3+(-2L-14\tau+13)u^2\\
      &+(2\tau-13)u+L+14\tau-49,                        \tag{9}
\end{split}
\]

and

\[
\begin{split}
S(u)={}&(2\tau^3-3\tau^2-\omega)u^6
 +(6\tau^2-6\tau)u^5\\
&+(-6\tau^3+51\tau^2-36\tau+3\omega-3)u^4\\
&+(-12\tau^2+96\tau-42)u^3\\
&+(6\tau^3-93\tau^2+372\tau-3\omega-144)u^2\\
&+(6\tau^2-90\tau+330)u
 -2\tau^3+45\tau^2-336\tau+\omega+819.                 \tag{10}
\end{split}
\]

The four distinct admissible numbers \(u_i\) are common roots of (9) and
(10).

## 4. Exact pseudo-remainder certificate

Let

\[
                 \operatorname {prem}_u(S,R)
                    =c_3u^3+c_2u^2+c_1u+c_0.            \tag{11}
\]

Here `prem` is the ordinary pseudo-remainder: there is a polynomial
\(Q(u)\) such that

\[
                         L^3S(u)=Q(u)R(u)+\sum_{j=0}^3c_ju^j. \tag{12}
\]

Define

\[
\begin{aligned}
P_3={}&-56L^2-32L\tau^2-320L\tau+101L
       -224\tau^3+896\tau^2-357\tau-1432,\\
P_2={}&24L^2+128L\tau+5L+128\tau^2-421\tau+810,\\
P_1={}&-56L^2-32L\tau^2-155L
       -224\tau^3+448\tau^2+155\tau-544,\\
P_0={}&3(8L^2+23L-87\tau+110).                           \tag{13}
\end{aligned}
\]

A direct coefficient expansion of (9)--(11) gives the Bézout certificate

\[
                         P_3c_3+P_2c_2+P_1c_1+P_0c_0
                              =26784L^3.                 \tag{14}
\]

This one displayed identity is the entire elimination step.  It is valid
over \(\mathbb Z[L,\tau,\omega]\), so it loses no exceptional complex
parameters.

If \(L\ne0\), then \(R\) is a quartic.  Its four distinct roots are
exactly the \(u_i\), and since they also annihilate \(S\), one has
\(R\mid S\).  Thus all four pseudo-remainder coefficients in (11) vanish.
Equation (14) would give \(L^3=0\), a contradiction.

It remains to take \(L=0\).  Equation (9) then has degree at most three
and still vanishes at the four distinct \(u_i\), so it would have to be
the zero polynomial.  Its cubic coefficient gives \(\tau=1/2\), but its
quadratic coefficient is then \(-14\tau+13=6\ne0\).  This final
contradiction proves Theorem 1.1.

## 5. Census consequence and audit

The four residual profiles with exactly four triple classes are

\[
                 3^4 2^4 1,\qquad 3^4 2^3 1^3,
                 \qquad 3^4 2^2 1^5,\qquad 3^4 2\,1^7. \tag{15}
\]

All four are closed by Theorem 1.1.

[verify_live_three_zero_eighth_split_k3_four_triple_cubic_jet_elimination.py](../computations/verify_live_three_zero_eighth_split_k3_four_triple_cubic_jet_elimination.py)
checks the scaled jets, equations (6), the full expansions (9)--(10),
pseudo-division (12), the integral certificate (14), every legal core in
the four profiles (15), and their exact positions in the old residual
census.
