# Independent audit: the \(p=28\) two-quartic \(q=5\) grid closure

## 1. Verdict and scope

The argument in the
[primary grid-closure note](live-three-zero-higher-split-p28-two-quartic-q5-grid-closure.md)
passes an independent reconstruction.  On the six equality splits

\[
 (h,k)=(22,6),(23,5),(24,4),(25,3),(26,2),(27,1),
\]

it excludes both residual \(d\leq2\) tuples

\[
                  (e,a,b,u)=(2,7,0,1),(2,7,1,-1).
\]

The proof uses the independently audited singleton-swap statement as its
input: in every fixed-triple row, each selected kernel has dimension five
or six and at most one entry has dimension six.  Everything after that
input was reconstructed here, including the selected/complementary
indexing, the exact local unit, all projection-rank cases in the
seven-plane lemma, and the final exact order-three row.

This is a genuine closure of the two displayed tuple families in the
\(p=28\), \(d\leq2\) equality frontier.  It is not a closure of the
unrestricted \(p=28\) ledger and is not a uniform all-even theorem.

## 2. Selection and grid bookkeeping

Let \(i\) be one of the seven exact-triple values.  Give \(i\) role two.
In the second tuple also give the unique exact double role two.  If

\[
                         d=1+b,
\]

then the number of selected ordinary singleton layers and the total
number \(N\) of ordinary singleton values are

\[
\begin{array}{c|c|c|c}
(e,a,b,u)&d&\text{selected singletons}&N=h+u\\ \hline
(2,7,0,1)&1&h&h+1\\
(2,7,1,-1)&2&h-2&h-1.
\end{array}
\]

Thus choosing a complementary ordinary singleton \(s\) leaves exactly

\[
                         4^2 3^6 1_i1_s.                  \tag{1}
\]

This profile has mass \(28\) and ten value classes.  If the corresponding
selected kernel has dimension \(q_{i,s}=5\), its row-relation space has
dimension

\[
                         q_{i,s}-2=3
\]

and the relation-to-polynomial map places it in degree

\[
                         10-4=6.
\]

We denote it by

\[
             \mathcal S_{i,s}\subseteq\mathbb C[z]_{\leq6},
             \qquad\dim\mathcal S_{i,s}=3.                \tag{2}
\]

The singleton-swap input permits at most one \(q=6\) entry in each of the
seven fixed-\(i\) rows.  Hence the entire \(7\)-by-\(N\) grid has at most
seven \(q=6\) entries, and at most seven columns are contaminated.  Since
\(N\geq23\) in the first tuple and \(N\geq21\) in the second, there are
at least sixteen and fourteen all-\(q=5\) columns, respectively.

## 3. Pair transport and its correct indexing

Fix \(i\), and take distinct singleton values \(s,t\) for which both grid
entries have \(q=5\).  Put

\[
                    f_x=(z-x)^2(z+x).
\]

The subscript on \(\mathcal S_{i,s}\) records the singleton left
complementary.  Therefore \(t\), not \(s\), is selected in the
\(s\)-complement selection.  Restoring both choices gives the correctly
indexed transports

\[
\begin{aligned}
 f_t\mathcal S_{i,s}&\subseteq\mathcal K_{i;s,t},\\
 f_s\mathcal S_{i,t}&\subseteq\mathcal K_{i;s,t}
                         \subseteq\mathbb C[z]_{\leq9}.    \tag{3}
\end{aligned}
\]

The common baseline is

\[
                         4^2 3^6 1_i1_s1_t.               \tag{4}
\]

If the degree-nine common kernel contained a five-space, its two
order-four, six order-three, and three order-one rows would force

\[
          2(5-4)+6(5-3)+3(5-1)=26
\]

units of Wronskian weight, while the cap is

\[
                         5(10-5)=25.
\]

This one-unit excess survives every gcd.  For a common zero of order
\(g\) at an exact order-\(m\) row, division contributes \(5g\) to the
lost degree cap and leaves the cost
\(\max(0,5-m+g)\) when \(g\leq m\); if \(g>m\), the row is automatic but
the cost \(5g\) is already larger than the original
\(\max(0,5-m)\).  Thus

\[
                         \dim\mathcal K_{i;s,t}\leq4.      \tag{5}
\]

The two spaces in (3) have dimension three, so their intersection has
dimension at least two.

Structural distinctness and nonopposition give

\[
 \operatorname {Res}_z(f_s,f_t)=-(s-t)^5(s+t)^4\ne0.      \tag{6}
\]

This includes \(s=0\), when \(f_s=z^3\).  Hence

\[
 f_t\mathbb C[z]_{\leq6}\cap f_s\mathbb C[z]_{\leq6}
                       =f_sf_t\mathbb C[z]_{\leq3}.       \tag{7}
\]

Define

\[
 \mathcal U_{i,s}
  =\{u\in\mathbb C[z]_{\leq3}:f_su\in\mathcal S_{i,s}\}.
                                                                  \tag{8}
\]

Equations (3), (5), and (7) imply

\[
                 \dim(\mathcal U_{i,s}\cap
                      \mathcal U_{i,t})\geq2               \tag{9}
\]

for every pair of \(q=5\) singleton choices.

## 4. Independent derivation of the fixed local unit

This is the place where merely saying that all factors are local units
would be insufficient.  We retain every factor that changes with \(s\).

Let

\[
                         H_Y=\prod_{y\in Y}(z+y),\qquad
                         H_s={H_Y\over z+s}.               \tag{10}
\]

Here \(H_s\) is exactly the selected-singleton plus-pole product in the
selection whose complementary singleton is \(s\).  Near the other simple
complementary value \(i\), write the complementary polynomial as

\[
                         A_s=(z-i)(z-s)C_i,                \tag{11}
\]

where \(C_i\) is independent of \(s\) and is nonzero at \(i\).  The
repeated-root factor \(g\) is also independent of \(s\), because \(s\) is
simple.  The selected repeated plus-pole product is fixed while \(s\)
moves.  Thus the exact relation identity

\[
 {d\over dz}{(z+\mu)^{k+1}N\over A_s}
 ={(z+\mu)^kg\over A_s^2}\,Q^2H_sS
\]

has, after stripping the displayed \((z-i)^{-2}\) singularity, the
order-one row unit

\[
\begin{aligned}
 U_{i,s}
 &= {(z+\mu)^kgQ^2\over C_i^2}\,
       {H_s\over(z-s)^2}\\
 &=V_i\,{H_Y\over(z+s)(z-s)^2}
  ={V_iH_Y\over f_s},                                    \tag{12}
\end{aligned}
\]

where \(V_i\) is independent of \(s\) and
\(V_i(i)H_Y(i)\ne0\).  No factor involving \(s\) has been hidden in
\(V_i\): the factor \(z+s\) is precisely the factor omitted from \(H_s\),
and \((z-s)^2\) is precisely the contribution of \(A_s^2\).

For \(S=f_su\in\mathcal S_{i,s}\), the exact simple row is therefore

\[
             (U_{i,s}S)'(i)=(V_iH_Yu)'(i)=0.              \tag{13}
\]

It is one fixed nonzero Robin functional on
\(\mathbb C[z]_{\leq3}\), independent of \(s\).  Let its three-dimensional
kernel be \(\mathcal H_i\).  Then

\[
                         \mathcal U_{i,s}\subseteq
                         \mathcal H_i.                     \tag{14}
\]

There are many \(q=5\) choices for each \(i\), and (9) shows each
\(\mathcal U_{i,s}\) has dimension at least two.  If one is a plane,
its two-dimensional intersection with every other member makes it a
subspace of every member.  If all members are the whole three-space
\(\mathcal H_i\), choose any plane.  In either case there is a fixed
plane \(\mathcal L_i\subseteq\mathbb C[z]_{\leq3}\) such that

\[
             f_s\mathcal L_i\subseteq\mathcal S_{i,s}
             \quad\text{for every \(q_{i,s}=5\).}          \tag{15}
\]

## 5. One all-\(q=5\) column and division by \(f_s\)

Choose an all-\(q=5\) column \(s\).  For a triple value \(i\), restoring
the selected triple uses

\[
                  B_i=(z-i)^2(z+i)^2=(z^2-i^2)^2
\]

and gives

\[
 B_i\mathcal S_{i,s}\subseteq\mathcal K_s
                         \subseteq\mathbb C[z]_{\leq10},  \tag{16}
\]

where the baseline is \(4^2 3^7 1_s\).  By (15),
\(f_sB_i\mathcal L_i\subseteq\mathcal K_s\).

It is legitimate to divide this particular span by \(f_s\).  At \(s\),
\(f_s\) has a double zero, so every exact first-order row is automatic.
At a repeated value \(a\), structural separation gives \(f_s(a)\ne0\);
if the old row is \((U_a f_sP)^{(m)}(a)=0\), then the divided row is

\[
                         (G_aP)^{(m)}(a)=0,\qquad
                         G_a=U_af_s,\quad G_a(a)\ne0.      \tag{17}
\]

Therefore

\[
 \mathcal M:=\operatorname {span}_{i=1}^7B_i\mathcal L_i
       \subseteq\mathcal J_s\subseteq\mathbb C[z]_{\leq7},\tag{18}
\]

where \(\mathcal J_s\) has two exact order-four and seven exact
order-three rows.

A five-space in degree seven would force

\[
                  2(5-4)+7(5-3)=16
\]

against the cap \(5(8-5)=15\).  The same local gcd calculation used in
Section 3 proves

\[
                         \dim\mathcal J_s\leq4.            \tag{19}
\]

For \(i\ne j\), the coprime factors \(B_i,B_j\) have product degree
eight, so

\[
 B_i\mathbb C[z]_{\leq3}\cap
 B_j\mathbb C[z]_{\leq3}=0.                               \tag{20}
\]

Two of the planes \(B_i\mathcal L_i\) consequently already span a
four-space.  Equations (18)--(20) force

\[
 \dim\mathcal M=4,\qquad
 \dim\bigl(\mathcal M\cap B_i\mathbb C[z]_{\leq3}\bigr)
 \geq2\quad(1\leq i\leq7).                               \tag{21}
\]

## 6. Independent audit of the seven-plane classification

Put \(t=z^2\), \(R=\mathbb C[t]_{\leq3}\), and

\[
                 E_a=(t-a)^2\mathbb C[t]_{\leq1}\subset R.
\]

The parity decomposition identifies
\(\mathbb C[z]_{\leq7}=R\oplus zR\), and
\(B_i\mathbb C[z]_{\leq3}=E_{a_i}\oplus zE_{a_i}\), where
\(a_i=i^2\).  The \(a_i\) are distinct.

Let \(F\) be the image of \(\mathcal M\) under even projection, put
\(r=\dim F\), and let

\[
              K=\{q\in R:zq\in\mathcal M\},\qquad
              \dim K=4-r.
\]

Projecting the intersection in (21), and retaining its kernel, gives the
essential inequality

\[
 \dim(F\cap E_a)+\dim(K\cap E_a)
 \ \geq\
 \dim\bigl(\mathcal M\cap(E_a\oplus zE_a)\bigr)
 \ \geq2.                                                  \tag{22}
\]

All five possible ranks are as follows.

- If \(r=3\), the first term in (22) is one or two and the second is zero
  or one.  Hence either \(E_a\subset F\) or \(K\subset E_a\).
  Two distinct \(E_a\)'s are complementary in \(R\), since their
  intersection would require a degree-at-most-three polynomial with two
  distinct double roots.  Thus the first event occurs at most once.
  The same degree argument shows that the fixed line \(K\) lies in at
  most one \(E_a\).  Seven values are impossible.

- If \(r=1\), the symmetric alternatives are \(F\subset E_a\) or
  \(E_a\subset K\), and again each can occur at most once.  This rank is
  impossible.

- If \(r=2\), both \(F\) and \(K\) are planes.  Apart from at most one
  value with \(F=E_a\) and at most one with \(K=E_a\), equation (22)
  forces both planes to meet \(E_a\) nontrivially.  In particular \(F\)
  would meet at least five of the seven \(E_a\)'s.

  Write the Pluecker coordinates of \(F\), in coefficient order
  \(1,t,t^2,t^3\), as \(p_{uv}\).  The incidence determinant is

  \[
  \Delta_F(a)=p_{01}+2p_{02}a+(3p_{03}+p_{12})a^2
                   +2p_{13}a^3+p_{23}a^4.                \tag{23}
  \]

  This quartic is not identically zero.  If all its coefficients
  vanished, the Pluecker relation would reduce to
  \(-3p_{03}^2=0\), and characteristic zero would force every
  \(p_{uv}=0\), impossible for a plane.  Thus \(F\) meets at most four
  members of the family, contradicting the required five.

- If \(r=0\), the four-space is \(zR\), already of the required form
  \(\ell R\) with \(\ell=z\).

- If \(r=4\), even projection is an isomorphism and

  \[
          \mathcal M=\{e+zT(e):e\in R\}
  \]

  for an endomorphism \(T\) of \(R\).  A two-dimensional intersection
  with \(E_a\oplus zE_a\) means exactly that
  \(T(E_a)\subseteq E_a\).

  With

  \[
  v_0(a)=(a^2,-2a,1,0)^T,\quad
  v_1(a)=(0,a^2,-2a,1)^T
  \]

  and

  \[
  J(a)=
  \begin{pmatrix}1&a&a^2&a^3\\0&1&2a&3a^2\end{pmatrix},
  \]

  preservation says \(J(a)Tv_0(a)=J(a)Tv_1(a)=0\).  Their four entries
  have degree at most five.  Seven distinct roots make them polynomial
  identities.  Coefficient comparison for \(v_0\) gives

  \[
  T=
  \begin{pmatrix}
  \lambda&0&0&A\\
  c&\lambda&0&B\\
  0&c&\lambda&C\\
  0&0&c&D
  \end{pmatrix}.
  \]

  The \(v_1\) identities then give
  \(A=B=C=c=0\) and \(D=\lambda\).  Thus \(T=\lambda I\), and
  \(\mathcal M=(1+\lambda z)R\).

Combining the five ranks proves

\[
                         \mathcal M=\ell(z)
                         \mathbb C[z^2]_{\leq3}            \tag{24}
\]

for a nonzero affine polynomial \(\ell\).

## 7. The surviving exact triple row

Division by \(f_s\) did not lower or erase any triple row.  At a triple
value \(i\), equation (17) with \(m=3\) gives

\[
                         (G_iP)^{(3)}(i)=0,\qquad
 G_i(i)=U_i(i)(i-s)^2(i+s)\ne0.                            \tag{25}
\]

In particular the coefficient of \(P^{(3)}(i)\) is still the nonzero
number \(G_i(i)\).

A nonzero affine polynomial has at most one root, so among the seven
distinct nonzero triple values choose \(i\) with \(\ell(i)\ne0\).  The
member

\[
                  P_i=\ell(z)(z^2-i^2)^3\in\mathcal M
\]

has exact order three at \(i\).  Its lower three jets vanish, and hence

\[
 (G_iP_i)^{(3)}(i)
   =3!\,G_i(i)\ell(i)(2i)^3\ne0,
\]

contradicting (25).  This completes the independent proof.

## 8. Standalone executable audit

[verify_live_three_zero_higher_split_p28_two_quartic_q5_grid_closure_independent_audit.py](../computations/verify_live_three_zero_higher_split_p28_two_quartic_q5_grid_closure_independent_audit.py)
does not import the primary checker.  It reconstructs the two selections
at every equality split, the grid pigeonhole count, both Wronskian gaps
and every local gcd branch, the singleton resultant, the full
\(g/A_s^2\) and \(H_s\) cancellation including a zero singleton,
division by \(f_s\), the projection-dimension alternatives at
\(r=1,2,3\), the Pluecker quartic, the fifteen independent graph
constraints, and the nonzero exact order-three coefficient.
