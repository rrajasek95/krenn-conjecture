# Optimal W-state rates in the one-root architecture

September 26, 2026. **Written research; exact supporting checks; awaiting
independent audit.** No historical priority claim is made for W-state
preparation or for the classical hafnian inequality used below.

[Illustrated guide](../explainers/METHOD-UTILITY.md) ·
[Replay](../computations/method-utility-2026-09-26/README.md)

## 1. A sharp theorem over a whole architecture family

Let \(n=2m\ge4\), choose one root site, and write \(N=n-1\).
Every edge between the other sites emits only the local state \(aa\), with
arbitrary complex weight. Edges incident to the root may have arbitrary
endpoint colors. Thus the odd core is a complex scalar weighted graph;
it need not be complete, positive, or symmetric under site permutations.

The target is the uniform single-excitation state

\[
 W_n=\sum_{j=1}^{n}|a\cdots b_j\cdots a\rangle.
\]

For a source with exact nonzero output proportional to \(W_n\), define
\(R=\|H\|^2/S^m\), where \(S\) is the sum of squared magnitudes of
all source cells. Define

\[
 B_n=\frac{((n-1)!!)^2}{\binom{n}{2}^{m}}.
\]

**Theorem.** Over this entire class of cores and all their incident edges,

\[
 \boxed{\max R=\frac{n B_n}{(n-1)^2+1}.}                 \tag{1}
\]

A complete core with equal weights attains the bound, with suitably chosen
incident weights. At six sites the optimum is exactly \(1/65\).
This is a global optimum within the stated architecture class. It is not
an optimum over arbitrary colored cores or a Gaussian probability optimum.

## 2. Solve the incident edges for an arbitrary core and target

Let \(Q\) denote the scalar core, \(a=\sum_{i<j}|Q_{ij}|^2>0\), and

\[
 h_i=\operatorname{haf}(Q\setminus i),\qquad T=\sum_i|h_i|^2.
\]

For a weighted single-excitation target, let \(w_i\) be the desired amplitude
at core site \(i\), and \(w_0\) the desired amplitude at the root.
If \(x_i\) is the incident cell with root color \(a\) and core color \(b\),
and \(y_i\) has root color \(b\) and core color \(a\), matching expansion gives

\[
 H_i=h_i x_i,\qquad H_0=\sum_i h_i y_i.             \tag{2}
\]

The two groups of cells are disjoint. All other incident-color sectors
produce outputs outside the single-excitation target, or zero output.
They cannot reduce the norm needed for (2).

If every nonzero \(w_i\) has \(h_i\ne0\), and \(T>0\), the unique
minimum-norm choices in these two groups are

\[
 x_i=w_i/h_i,\qquad y_i=w_0\overline{h_i}/T,
\]

with zero used for \(w_i=h_i=0\). The squared minimum norm is

\[
 D_Q(w)=\sum_{i:h_i\ne0}\frac{|w_i|^2}{|h_i|^2}
                    +\frac{|w_0|^2}{T}.             \tag{3}
\]

Cauchy--Schwarz proves the minimum for the \(y_i\), including arbitrary
complex phases. A missing cofactor with a required nonzero amplitude makes
the target impossible for that core.

Scaling the root vector to squared norm \(t\) gives output norm squared
\(t\|w\|^2/D_Q(w)\). The unique optimal scale is
\(t=a/(m-1)\). Consequently

\[
 \boxed{R_Q(w)=\frac{(m-1)^{m-1}}{m^m a^{m-1}}
                     \frac{\|w\|^2}{D_Q(w)}.}        \tag{4}
\]

This solves exact weighted-W preparation for every specified scalar core.
For the equal-weight complete core, choosing the root at a largest
\(|w_j|\) minimizes (3) among root choices.

## 3. A sharp odd-core cofactor bound

The published scalar hafnian inequality is
\(|\operatorname{haf}(A)|^2\le B_n S(A)^m\).
It follows from [Roos, Theorem 2.3 and equation (42)](https://arxiv.org/html/1906.06176).
Its equality case includes equal off-diagonal entries.

Attach scalar root edges \(z_i=\sqrt t\,\overline{h_i}/\sqrt T\) to
\(Q\). Then \(|\operatorname{haf}(A)|^2=tT\) and \(S(A)=a+t\).
Using \(t=a/(m-1)\) in the published inequality gives

\[
 \boxed{T\le B_n\frac{m^m}{(m-1)^{m-1}}a^{m-1}.}     \tag{5}
\]

The bound is sharp: a complete equal-weight odd core has
\(h_i=(n-3)!!\), \(a=N(m-1)\), and equality in (5).
This is a derived application of the known hafnian norm bound.

For uniform \(w\), Cauchy--Schwarz gives

\[
 D_Q(W_n)=\sum_i\frac1{|h_i|^2}+\frac1T
       \ge\frac{N^2+1}{T}.                           \tag{6}
\]

Insert (5)--(6) into (4). The prefactors cancel to give (1).
The complete core has equal cofactor magnitudes, so all these inequalities
are simultaneously attained. This proves the optimization over the core,
not just the optimization with a preselected core.

## 4. The six-site optimum and a design diagnostic

Set all ten core \(aa\) weights to one. Set each of the five root-\(a\),
core-\(b\) weights to \(5/\sqrt{26}\), and each root-\(b\), core-\(a\)
weight to \(1/\sqrt{26}\). All six target amplitudes are
\(15/\sqrt{26}\), and every other output is zero. Thus

\[
 S=15,\qquad \|H\|^2=675/13,\qquad R=1/65.
\]

The replay checks all 729 ternary output coefficients using rational
directions, and verifies a minimum-norm preimage certificate.

| Sites | Optimal rate in this architecture class |
|---|---|
| 4 | \(1/10\) |
| 6 | \(1/65\) |
| 8 | \(9/3136\) |
| 10 | \(49/83025\) |
| 12 | \(3675/28579232\) |

There is also a stability diagnostic. Write \(x_i=|h_i|^2>0\). If a core
can attain at least \((1-\delta)\) times (1), where \(0\le\delta<1\), then

\[
 \boxed{\sum_{i<j}\frac{(x_i-x_j)^2}{x_i x_j}
        \le\frac{(N^2+1)\delta}{1-\delta}.}           \tag{7}
\]

Indeed,
\(T\sum_i1/x_i-N^2=\sum_{i<j}(x_i-x_j)^2/(x_ix_j)\), and the ratio
of (4) to (1) factors into two numbers at most one: the cofactor efficiency
in (5), and \((N^2+1)/(T\sum_i1/x_i+1)\). Each factor must be at least
\(1-\delta\). The cofactor bound (5) must therefore also be nearly saturated.
This diagnoses nearly optimal designs without claiming a full classification
of their edge weights.

### Weighted targets also have an architecture-wide upper bound

Weighted Cauchy--Schwarz in (3) gives

\[
 D_Q(w)\ge\frac{(\sum_{i=1}^N|w_i|)^2+|w_0|^2}{T}.
\]

Consequently every core in the class satisfies

\[
 R_Q(w)\le B_n\,
 \frac{\sum_{i=0}^{N}|w_i|^2}{(\sum_{i=1}^N|w_i|)^2+|w_0|^2}. \tag{8}
\]

If all core-site target magnitudes equal \(a_1\), and the root target
magnitude is \(b_1\), the complete core attains this bound exactly:

\[
 \max R=B_n\frac{N a_1^2+b_1^2}{N^2a_1^2+b_1^2}.     \tag{9}
\]

Arbitrary target phases can be compensated by the incident cells. This
includes the uniform W target and targets with a different excitation weight
at one distinguished site. For a general unequal weighted target, (8) is an
upper bound; simultaneous equality in its two ingredients is not asserted.

## 5. What has and has not been extended

W states are established targets; see, for context,
[Dür--Vidal--Cirac](https://arxiv.org/abs/quant-ph/0005115).
The contribution here is the explicit optimal normalized-rate calculation
for this architecture family, the weighted-target formula, and their exact
connection to the response and cofactor machinery already used in the workspace.
Whether these application formulas have appeared elsewhere has not been
exhaustively checked. The analytic proofs require independent audit.
