# The symmetrized permanent grading still has a four-class kernel

## Outcome

Quotienting ordered cross-pair provenance by endpoint swap removes the
two-grade ambiguity from the preceding note, but it does not make the
graded data injective.  On the anchored N=10 forced-pair model there is an
exact four-class relation

\[
 G_{27}^{22}-G_{36}^{11}+G_{57}^{11}-G_{56}^{22}=0,      \tag{1}
\]

where all new-end colours are zero and \(G_{vw}^{ab}\) denotes the
swap-symmetrized permanent grade with old endpoints \(v,w\) in colours
\(a,b\).

Equation (1) holds simultaneously in

1. the full matching tensor, and
2. every labelled quadratic cofactor column on all six adjacent cuts.

Thus it also holds on each four-cut set \(\{2,3,4,z\}\),
\(z\in\{0,1,5\}\).  No linear invariant of this combined ordinary data can
separate the four permanent grades.

This is the smallest exact combined circuit: distinct permanent grades are
not proportional, and an exhaustive exact audit finds no dependent triple
among the 55,000 possible triples in the only character groups where a
dependency could occur.

This is **not** a finite Krenn counterexample.  The permanent coefficients of
one finite cross-edge source are constrained quadratic products; the checker
does not claim that the four coefficients in (1) can occur alone without
additional off-circuit grades.  The result freezes linearized symmetrized
provenance separation and points to the nonlinear permanent-image constraint
as the remaining possible rescue.

## 1. Swap-symmetrized permanent grades

For distinct old endpoints \(v,w\), old colours \(\alpha,\gamma\), and new
colours \(\beta,\delta\), define the visible coefficient

\[
 \pi_{vw}^{\alpha\gamma;\beta\delta}
 =x_{v8;\alpha\beta}x_{w9;\gamma\delta}
  +x_{w8;\gamma\beta}x_{v9;\alpha\delta}.               \tag{2}
\]

The two summands have identical full and quadratic cofactor images, so (2)
is the correct quotient of ordered provenance.  There are 2,268 such
permanent grades at N=10.

For a grade \(p\), let

\[
 \Phi_{\cal C}(p)=
 \left(D_p,\ (C_{p,z;h,i})_{z\in\cal C,\,h,i}\right),   \tag{3}
\]

where \(D_p\) is its full quadratic matching tensor and
\(C_{p,z;h,i}\) is the literal quadratic coefficient of the labelled
cofactor column \((h,i)\) on cut \(z\).  Labels are retained: the audit does
not weaken the data by replacing the cofactor map with its span.

The strongest finite map tested is \(\Phi_{\{0,1,2,3,4,5\}}\).  A kernel for
this all-cut labelled map is automatically a kernel for every four-cut
restriction.

## 2. Character-class census

Modulo the anchored support and the three target characters, the 2,268
permanent grades form 959 exact character classes:

| class size | number of classes |
|---:|---:|
| 1 | 612 |
| 3 | 174 |
| 4 | 120 |
| 6 | 12 |
| 9 | 12 |
| 12 | 20 |
| 18 | 2 |
| 22 | 6 |
| 66 | 1 |

The full-output grades are independent in every class except the six
22-element classes and the single 66-element zero-character class.  Their
full ranks are respectively 15 and 45.  Hence any combined full-plus-cofactor
kernel must lie in these seven groups, containing only 198 grades in total.

Adding every labelled quadratic cofactor on all six cuts raises the ranks to

\[
                       21\quad\text{and}\quad63.         \tag{4}
\]

The combined all-cut kernel therefore has dimension

\[
                       6(22-21)+(66-63)=9.               \tag{5}
\]

Exactly the same rank pattern occurs for each fixed-three-plus-candidate
quartet.  In this anchored model, adding the other two cuts does not shrink
the permanent-grade kernel.

## 3. The smallest circuit

In coordinate notation, equation (1) is

\[
\begin{aligned}
 &G_{((2,8;20),(7,9;20))}
 -G_{((3,8;10),(6,9;10))}\\
 &\qquad
 +G_{((5,8;10),(7,9;10))}
 -G_{((5,8;20),(6,9;20))}=0.                            \tag{6}
\end{aligned}
\]

All four grades have zero anchored target-stabilizing quotient character.
Their full tensors telescope particularly transparently.  Put

\[
\begin{aligned}
 M  &=e_{00210012}\otimes e_{00},\\
 P_1&=e_{11111111}\otimes e_{00},\\
 P_2&=e_{22222222}\otimes e_{00}.
\end{aligned}
\]

Then the four full grades, in the order shown in (6), are

\[
                   M+P_2,\quad M+P_1,\quad P_1,\quad P_2,             \tag{7}
\]

which proves the full part of (6).  The checker independently constructs
every quadratic cofactor from literal perfect matchings and verifies the
same signed relation column by column on cuts 0 through 5.

There is no two-class circuit because the 2,268 swap classes were chosen to
have distinct projective full outputs.  Any three-class combined circuit
would first be a full-output circuit, so the checker exhausts all triples in
the seven full-dependent character classes.  All 55,000 triples have exact
rank three.  Equation (6) has rank three on four columns, making support four
minimal.

## 4. Consequence for four-cut separation

Let \({\cal C}_z=\{2,3,4,z\}\) for \(z=0,1,5\).  The exact ranks on each
quartet are

| character group | number of groups | domain dimension | rank of \(\Phi_{{\cal C}_z}\) |
|---|---:|---:|---:|
| large nonzero classes | 6 | 22 | 21 |
| zero class | 1 | 66 | 63 |

In particular,

\[
       \text{four simultaneous labelled cofactor data}
       \not\Longrightarrow
       \text{individual permanent-grade separation}     \tag{8}

as a linear statement.  Since (6) already cancels before passing to
cofactor spans or quotient cylinders, no choice of row functional on the
same full/cofactor data can restore injectivity.

The source-graded counterguard from the earlier note remains valid for a
single explicit grade.  What fails is the inference that a general source's
permanent grades can be tested independently: four or more grades can hide
in the kernel (5).

## 5. Honest realizability scope

The vector space in (3) treats permanent-grade coefficients as independent
scalars.  A finite source does not.  Its coefficients have the special form
(2), simultaneously for every endpoint and colour choice.  Choosing cells
to make the four displayed permanents nonzero also creates products with
other old-endpoint pairs.  Those off-circuit grades are not included in
(6), and the checker does not solve the nonlinear equations required to
cancel them.

Therefore (6) is:

* an exact obstruction to a **linearized provenance-separation lemma**;
* an exact kernel vector of the strongest labelled all-cut quadratic data;
* not an actual finite source;
* not evidence that four complete cylinders exist; and
* not a Krenn counterexample.

The conjecture route can still be rescued if the permanent image of actual
cross weights meets the nine-dimensional kernel (5) only at zero, or if any
nonzero intersection necessarily destroys one of the lower-sector cylinder
conditions.

## 6. Forced-pair stability

Adjoin another isolated diagonal old pair and move the two new cross
vertices to 10,11.  The checker verifies (6) again in the N=12 full tensor
and in every labelled quadratic cofactor column on all six inherited cuts.
Thus the four-class kernel persists exactly on the forced-pair tower.

This stability is base-specific: (7) uses the matching cofactors of the
anchored source.  It is not claimed for arbitrary old sources or arbitrary
new edges incident to the intervening matched pair.

## 7. Sharp next test

The next bounded problem is nonlinear but finite.  Let \(X\) and \(Y\) be
the two collections of cross weights incident to the two new vertices.  Map
their rank-one products through the symmetrized permanent map (2), then
through \(\Phi_{{\cal C}_z}\).  Test exactly whether

\[
       \Phi_{{\cal C}_z}(\operatorname{Perm}(X,Y))=0     \tag{9}

has a nonzero solution compatible with the three pure anchors and the
linear one-cross cofactor directions.

An empty intersection gives the desired bounded nonlinear provenance lemma.
A smallest nonzero solution is the next genuine cancellation source to test
against the full four-cylinder equations.

## Reproduction

    python3 computations/verify_n10_permanent_grade_four_cut_kernel.py
    python3 -O computations/verify_n10_permanent_grade_four_cut_kernel.py
    python3 -I computations/verify_n10_permanent_grade_four_cut_kernel.py
    python3 -S computations/verify_n10_permanent_grade_four_cut_kernel.py

The checker uses exact rational matching tensors, labelled cofactor columns,
character quotients, and sparse ranks throughout.
