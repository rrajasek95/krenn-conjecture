# Vertex deletion turns the six-crossing residues into Kneser incidence

## 1. Outcome

The forced four/six-crossing residue in
[six-set-beta-overlap-jet.md](six-set-beta-overlap-jet.md) does not cancel
under the first natural overlaps of different six-sets.  At order twelve,
take a set \(Z\) of size \(6+d\), a common complement \(P\) of size
\(6-d\), and all six-sets

\[
                  S_D=Z\setminus D,qquad
                  R_D=P\cup D,qquad |D|=d.               \tag{1}
\]

Assume the blocks internal to \(Z\) are identities.  Pull the residue
equation for \(S_D\) to \(P\) by contracting every vertex of \(D\) at
color zero.  The pulled six-crossing term has the exact form

\[
 L_D^{(6)}=
   \sum_{\substack{A\subset Z,\ |A|=d\\A\cap D=\varnothing}}C_{D,A},
 \qquad C_{D,A}=C_{A,D}.                                \tag{2}
\]

Thus the top residues are the unsigned vertex sums of edge tensors on the
Kneser graph \(KG(6+d,d)\).  For \(1\le d\le5\), every component of this
graph is nonbipartite, so its unsigned incidence matrix has full row rank.
There is no nonzero scalar combination of the pulled six-set equations
which cancels the six-crossing atoms formally.

This is sharp in matching-realizable local models.  Exact finite-field
specializations give

\[
\begin{array}{c|c|c|c}
d&\text{overlapping six-sets}&\dim V_P&
       \operatorname{rank}\{L_D^{(6)}\}\ \hline
1&7&243&7\\
2&28&81&28.
\end{array}                                                \tag{3}
\]

In the same specializations, all \(7+28\) external six-site Hessians have
rank \(130=135-5\), every internal block is invertible, and every relevant
monomer map is injective by the Hessian criterion.  Hence neither deleting
one vertex, deleting two vertices, nor scalar inclusion--exclusion isolates
the four-crossing jet.  Any successful overlap proof must use the shared
permanent/recombination structure *inside* the atoms \(C_{D,A}\), together
with the mixed GHZ equations.

## 2. Pulling every residue to a common shore

For a six-set \(S\) with identity internal blocks, put

\[
 \Lambda_S=3e_{0^S}^*-
       \sum_{\substack{w\in\{0,1\}^S\\|w|_1=2}}e_w^*.     \tag{4}
\]

If \(H_B(A)=\Delta_{B,3}\), the mixed-jet identity is

\[
 3e_0^{\otimes R_S}
     =(\Lambda_S\otimes\operatorname{id}_{R_S})
          (T_2^{R_S|S}+T_4^{R_S|S}+T_6^{R_S|S}).          \tag{5}
\]

Now specialize to (1).  Since \(|S_D|=|R_D|=6\), all three displayed
sectors can occur.  Define tensors on the one common space \(V_P\) by

\[
 L_D^{(2j)}=
  (e_0^{*\otimes D}\otimes\Lambda_{S_D}
                  \otimes\operatorname{id}_P)
          T_{2j}^{R_D|S_D}.                               \tag{6}
\]

Contracting (5) gives the exact pulled equation

\[
             3e_0^{\otimes P}
                    =L_D^{(2)}+L_D^{(4)}+L_D^{(6)}
                    \qquad\left(D\in\tbinom{Z}{d}\right). \tag{7}
\]

The question is whether a linear combination of (7), as \(D\) varies,
can remove \(L_D^{(6)}\) and leave a lower-jet or diagonal identity.  The
answer is no at the level of overlap incidence.

## 3. Exact atomization of the top jet

Fix disjoint \(d\)-sets \(D,A\subset Z\), and put

\[
                          U=Z\setminus(D\cup A),
                          \qquad |U|=|P|=6-d.              \tag{8}
\]

Let \(\operatorname{Per}_{U,P}(A)\in V_U\otimes V_P\) be the sum over all
bijections from \(U\) to \(P\) of the corresponding products of cross-edge
tensors.  Define

\[
 \rho_U=3e_{0^U}^*-
       \sum_{\substack{w\in\{0,1\}^U\\|w|_1=2}}e_w^*,
 \qquad
 C_{D,A}=d!\,(\rho_U\otimes\operatorname{id}_P)
                 \operatorname{Per}_{U,P}(A).            \tag{9}
\]

**Lemma 3.1 (symmetric top atoms).**  Equations (2) and (9) hold.

**Proof.**  In the six-crossing sector, all six vertices of \(S_D\) are
matched across to all six vertices of \(R_D\).  After the \(D\)-slots are
contracted at zero, a unique \(d\)-set \(A\subset S_D\) is matched to
\(D\).  Every block between \(A\) and \(D\) is \(I_3\), so the vertices of
\(A\) are forced to color zero.  There are \(d!\) bijections between
\(A\) and \(D\), all of weight one.  Restricting \(\Lambda_{S_D}\) to
zero on \(A\) gives exactly \(\rho_U\), and the remaining vertices \(U\)
are bijected to \(P\).  This proves (9) and the sum in (2).

Interchanging \(D,A\) leaves \(U\), \(\rho_U\), the factor \(d!\), and
the permanent into \(P\) unchanged.  Hence \(C_{D,A}=C_{A,D}\).
\(\square\)

The symmetry is important: deletion does cancel the *one shared atom*
\(C_{D,A}\) when the equations indexed by \(D\) and \(A\) are subtracted.
It does not cancel their other incident atoms.

## 4. The Kneser incidence obstruction to cancellation

Let \(G_d=KG(6+d,d)\).  Its vertices are the \(d\)-subsets of \(Z\), and
two are adjacent precisely when they are disjoint.  Lemma 3.1 says that
\(D\mapsto L_D^{(6)}\) is the unsigned incidence map of \(G_d\), with a
tensor \(C_{D,A}\) on each edge.

For scalars \(\alpha_D\),

\[
 \sum_D\alpha_D L_D^{(6)}
   =\sum_{\{D,A\}\in E(G_d)}
                       (\alpha_D+\alpha_A)C_{D,A}.        \tag{10}
\]

Consequently a universal incidence cancellation requires

\[
                         \alpha_D+\alpha_A=0
                         \qquad(DA\in E(G_d)).            \tag{11}
\]

For \(d\le5\), the inequality \(2d+1\le6+d\) lets us embed
\(KG(2d+1,d)\) in \(G_d\).  On the cyclic group
\(\mathbb Z/(2d+1)\), the sets

\[
 D_i=\{id,id+1,\ldots,id+d-1\},
                   \qquad i=0,\ldots,2d,                 \tag{12}
\]

form an odd cycle: consecutive sets, including the last and first, are
disjoint.  The symmetric group on \(Z\) is transitive on the vertices of
\(G_d\), so every vertex lies on an automorphic image of such an odd cycle.
Alternating (11) around that cycle gives \(\alpha_D=-\alpha_D\), hence
\(\alpha_D=0\) in characteristic zero.  This holds at every vertex.

Thus the unsigned incidence matrix has full row rank and no nontrivial
linear combination of (7) eliminates its top atoms on incidence grounds.
For \(d=6\), the Kneser graph is a union of complementary pairs and does
have alternating kernels, but then \(P\) is empty; this terminal scalar
case does not produce the desired positive-order diagonal contraction.

## 5. One deletion produces vertex gauges, not a cancellation

The case \(d=1\) makes the obstruction especially transparent.  Write
\(S_y=Z\setminus\{y\}\) and extend (4) to seven slots by

\[
                       F_y=e_0^{*(y)}\otimes\Lambda_{S_y}. \tag{13}
\]

If \(\sum_y\alpha_y=0\), a coefficient check gives

\[
 \boxed{\quad
   \sum_y\alpha_yF_y
      =\sum_{\{i,j\}\subset Z}(\alpha_i+\alpha_j)
          e_{1_i1_j0_{Z\setminus\{i,j\}}}^*.
 \quad}                                                   \tag{14}
\]

The overlap differences therefore reproduce the familiar vertex-gauge
pattern \(\alpha_i+\alpha_j\) on the complete graph.  The target contraction
of (14) is zero because every displayed word is mixed.  On the top atoms,
the same coefficients become (10) for \(K_7\).  Its odd triangles force
the putative alternating cancellation to vanish.  Deleting one vertex
does not isolate \(\mathcal J_2\); it converts the comparison into another
nonbipartite gauge-incidence system.

## 6. Exact local countermodels to a stronger overlap claim

The full-row-rank phenomenon is not merely formal independence of named
atoms.  The audit constructs two twelve-site integer sources modulo
\(1{,}000{,}003\):

1. \(|Z|=7,|P|=5\), with all seven six-sets \(S_y\);
2. \(|Z|=8,|P|=4\), with all twenty-eight six-sets \(S_D\).

All blocks within \(Z\) are \(I_3\).  The blocks within \(P\) and from
\(Z\) to \(P\) are deterministic dense integer matrices.  For every
\(D\), the six-site quadratic internal to \(R_D=P\cup D\) has only its five
vertex gauges: its Hessian rank is exactly \(130\).  Its rank-three graph is
complete, and every row from every \(x\in S_D\) reaches all six sites of
\(R_D\).  Hence every odd-shore monomer map in the boundary factorization is
injective.

Simultaneously, the actual pulled top tensors have the ranks in (3).  In
particular, no nonzero scalar combination cancels them even after their
shared cross matrices and permanent recombinations are imposed.  These
sources are deliberately not GHZ; they show that Hessian rigidity, all
termwise boundary witnesses, and one- or two-deletion overlap do not alone
contradict one another.

## 7. Remaining global mechanism

Equation (2) does expose the remaining structure more sharply.  An atom is
not an arbitrary edge label: \(C_{D,A}\) is the contracted permanent of the
same cross blocks on \(U=Z\setminus(D\cup A)\), and those blocks recombine
in many other atoms and in lower crossing sectors.  A viable proof must use
mixed GHZ coefficients to constrain this shared permanent system.  Scalar
sums of the residue equations, deletion incidence, and Hessian-kernel
rigidity cannot remove the top jet.

## 8. Exact audit

Run

```text
python3.13 computations/verify_six_set_residue_overlap_incidence.py
```

The checker verifies the atom expansion directly, certifies the incidence
and actual tensor ranks in (3), checks all \(35\) Hessian ranks, and audits
the row-support hypotheses which imply all associated monomer maps are
injective.
