# The permanent image meets the nine-dimensional all-cut kernel only at zero

## Outcome

The nonlinear rank-one constraint rescues the swap-symmetrized permanent
grading from the linear kernel found in the preceding note.  On the anchored
N=10 forced-pair model,

\[
 \operatorname{PermImage}(X,Y)\cap
 \ker\Phi_{\{0,1,2,3,4,5\}}=\{0\}.                     \tag{1}
\]

Here \(X\) and \(Y\) are the actual cross-edge weights incident to new
vertices 8 and 9, the permanent image consists of their symmetrized
quadratic products, and \(\Phi\) retains the full quadratic tensor plus every
labelled quadratic cofactor column on all six cuts.

The nine-dimensional linear kernel has an especially rigid form: it is the
direct sum of one four-grade circuit for each ordered pair of new-end
colours.  None of those circuits, nor any linear combination of them, is the
permanent vector of actual cross weights unless all nine circuit
coefficients vanish.

This eliminates exact invisible **quadratic-grade** cancellation.  It does
not yet prove Krenn's conjecture or the full ungraded four-cylinder
implication.  Ordinary cylinder membership permits lower-degree one-cross
columns and parameter-dependent column-span coefficients; cancellations
through those mechanisms remain open.

## 1. The nine kernel generators

For new-end colours \((\beta,\delta)\in\{0,1,2\}^2\), let

\[
\begin{aligned}
 K_{\beta\delta}={}&
 G_{((2,8;2\beta),(7,9;2\delta))}
 -G_{((3,8;1\beta),(6,9;1\delta))}\\
 &+G_{((5,8;1\beta),(7,9;1\delta))}
 -G_{((5,8;2\beta),(6,9;2\delta))}.                    \tag{2}
\end{aligned}
\]

The exact combined full-plus-all-cofactor ranks from the preceding checker
give total kernel dimension

\[
                       6(22-21)+(66-63)=9.               \tag{3}
\]

The nine vectors (2) have disjoint permanent-coordinate supports, so they
are independent.  Literal perfect-matching expansion verifies that every
one lies in the all-six-cut kernel.  Therefore they form a basis of the
entire kernel, not merely a collection of examples.

Any kernel point has the form

\[
                         \sum_{\beta,\delta}
                              k_{\beta\delta}K_{\beta\delta}.          \tag{4}
\]

## 2. Rank-one permanent parametrization

Fix one ordered new-colour pair \((\beta,\delta)\).  Index an old
endpoint-colour choice by \(i=(v,\alpha)\), and put

\[
 u_i=\left(X_{v,\alpha;\beta},Y_{v,\alpha;\delta}\right)\in\mathbb C^2.
                                                                    \tag{5}
\]

The visible permanent coefficient for two different old vertices is

\[
 \pi_{ij}=B(u_i,u_j),
 \qquad
 B((x,y),(x',y'))=xy'+x'y.                              \tag{6}
\]

The form \(B\) is nondegenerate.  For every nonzero vector \(u\), its
orthogonal complement \(u^\perp\) is a one-dimensional projective line.
Thus the realizability of a kernel vector is a rank-two symmetric-bilinear
incidence problem, not a free choice of its 2,268 permanent coordinates.

## 3. Exact orthogonality contradiction

Suppose \(k_{\beta\delta}\ne0\) in (4).  Denote the endpoint-colour nodes of
the first three supported grades in (2) by

\[
\begin{aligned}
 A&=(a,b)=((2,2),(7,2)),\\
 B&=(c,d)=((3,1),(6,1)),\\
 C&=(e,f)=((5,1),(7,1)).                                \tag{7}
\end{aligned}
\]

The kernel support requires

\[
 \pi_{ab}\ne0,\qquad \pi_{cd}\ne0,\qquad \pi_{ef}\ne0,             \tag{8}
\]

and, because the following pairs are distinct old vertices but absent from
the kernel support,

\[
 \pi_{ac}=\pi_{ad}=\pi_{ae}=\pi_{ce}=0.                 \tag{9}
\]

From \(\pi_{ab}\ne0\), \(u_a\ne0\).  The first three equations in (9) put

\[
                       u_c,u_d,u_e\in u_a^\perp.         \tag{10}
\]

Since this is one-dimensional, \(u_c,u_d,u_e\) lie on the same projective
line.  The condition \(\pi_{cd}\ne0\) says this line is non-isotropic.  The
condition \(\pi_{ef}\ne0\) ensures \(u_e\ne0\), while \(\pi_{ce}=0\) says
the same line is isotropic.  This is impossible.

Therefore

\[
                              k_{\beta\delta}=0.          \tag{11}
\]

The argument applies independently to every ordered new-colour pair.  All
nine coefficients in (4) vanish, proving (1).

This is an exact projective elimination certificate over \(\mathbb C\); it
does not sample cross weights or assume they are nonzero generically.

## 4. Anchors and forced-lift constraints

The contradiction was obtained before imposing pure-anchor equations or
any further restrictions on cross weights.  Such constraints only shrink
the parameter space, so they cannot create a nonzero intersection with the
kernel.  In particular, the minimal four-grade circuit from the preceding
note is not realizable in isolation, even though its formal full and cofactor
data cancel and its formal relation would preserve the anchors.

The origin in (1) has a nontrivial preimage.  The permanent-zero four-cell
block

\[
 E_{08;00}+E_{19;00}+E_{18;00}-E_{09;00}                \tag{12}
\]

has nonzero cross weights but zero symmetrized permanent vector.  Its full
tensor is exactly the forced-pair lift, so it preserves the three pure
anchors.  It still contributes linear one-cross cofactor directions, and the
earlier exact audit found no complete cut.  Thus (12) is the smallest
surviving preimage of the zero quadratic grade, not a nonzero kernel point
and not a conjecture counterexample.

## 5. What implication is now usable

The exact statement proved is

\[
 \left.
 \begin{array}{c}
 \text{quadratic cross data come from actual weights }(X,Y),\\
 \text{their full and every labelled quadratic cofactor image vanish}
 \end{array}
 \right\}
 \quad\Longrightarrow\quad
 \pi(X,Y)=0.                                             \tag{13}

Equivalently, exact invisibility in the combined all-cut data cannot hide a
nonzero permanent grade.  The same conclusion holds for each
fixed-three-plus-candidate quartet because its combined kernel is the same
nine-dimensional space.

What is not yet proved is

\[
 \text{ordinary four complete cylinders}
 \quad\Longrightarrow\quad
 \text{quadratic combined data vanish}.                 \tag{14}

The premise in (14) is a span-membership statement for the full residual at
one evaluated source.  Constant old columns, linear one-cross columns, and
quadratic columns can be combined with parameter-dependent coefficients.
The next proof step needs a filtration or minor showing that these lower
degrees cannot cancel the nonzero permanent quotient detected by (13).

## 6. Stability

After adjoining another isolated old diagonal pair and moving the new cross
vertices to 10,11, the checker verifies all nine full-tensor circuit
identities at N=12.  The orthogonality contradiction uses only the unchanged
old endpoint-colour incidence in (7)--(9), so the rank-one intersection
no-go persists for the inherited kernel on the forced-pair tower.

This does not classify new kernel directions which might appear for a
general N=12 source or under arbitrary edges incident to the intervening
pair.  The stability claim is limited to the inherited anchored family.

## Reproduction

    python3 computations/verify_n10_permanent_kernel_rank_one_intersection.py
    python3 -O computations/verify_n10_permanent_kernel_rank_one_intersection.py
    python3 -I computations/verify_n10_permanent_kernel_rank_one_intersection.py
    python3 -S computations/verify_n10_permanent_kernel_rank_one_intersection.py

The checker rebuilds the exact nine-dimensional kernel, verifies its nine
channel generators, audits the finite incidence certificate, and rechecks
the nontrivial zero-grade survivor over the rationals.
