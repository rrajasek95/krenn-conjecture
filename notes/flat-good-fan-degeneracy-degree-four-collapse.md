# Overlapping flat good fans collapse to degree four

## 1. Outcome

Let \(B\) have even size \(N\ge8\), and let arbitrary endpoint-ordered
aggregate blocks satisfy

\[
                         H_B(A)=\Delta_{B,3}.                    \tag{1}
\]

Call a pair **good** when both of its deleted endpoint-star maps are
injective, as in
[the target-flattening essential-star theorem](target-flattening-essential-star-pair-bound.md).
Then one has the following uniform alternative.

**Theorem 1 (curvature or a degree-four foothold).** At least one of the
following holds.

1. Some canonical transition on a good fan is nonzero. Hence there is a
   literal nonzero \(2\times2\) source-block minor, an inverse two-flag
   selector, and a generically active affine cap line.
2. Some site \(p\) has only three or four nonzero incident aggregate
   blocks.

In the second alternative the local geometry is already known exactly.
If the degree is three, cubic-vertex rigidity gives three same-colour
coordinate blocks and pure complementary cofactors. If the degree is
four, choose the three forced colour anchors and call the remaining
neighbour \(r\). Its complementary matching tensor lies in the
three-anchor partition kernel.

Thus, after flatness is imposed on all overlapping good fans, the
degree-five common-line and degree-six common-plane alternatives from
[the low-degree residual theorem](flat-fan-low-degree-residual-transversal.md)
are not terminal cases. They can occur at a particular centre, but the
same source always has another centre at which only the cubic or
partition-kernel case remains.

This improves the one-fan bound of six exceptional blocks to four. The
proof is just the missing composition of two coordinate-free results: bad
pairs are \(4\)-degenerate, and a flat good fan is centre-dark. It uses no
Hessian classification and no graph subcase enumeration.

## 2. Proof of the global reduction

Let \({\cal B}\) be the graph of pairs which are not good. The
target-flattening essential-star theorem proves that \({\cal B}\) is
\(4\)-degenerate. In particular, on the full vertex set there is a site
\(p\) with

\[
                         \deg_{\cal B}(p)\le4.                    \tag{2}
\]

Let \(F\) be the set of good neighbours of \(p\). Then

\[
                         |F|=N-1-\deg_{\cal B}(p)
                              \ge N-5\ge3.                       \tag{3}
\]

For \(q,r\in F\), centre colour \(a\), and endpoint colours
\(b,c\), let

\[
 D_{qr}^a(b,c)
   =A_{pq}(a,b)S_{r,c}|_{B\setminus\{p,q,r\}}
    -A_{pr}(a,c)S_{q,b}|_{B\setminus\{p,q,r\}}             \tag{4}
\]

be the physical canonical transition. If one of (4) is nonzero, the
curvature-minor and cap-line conclusions are exactly Sections 6--7 of
[the canonical transition theorem](canonical-transition-pencil-fan-dichotomy.md).

Suppose instead that every transition (4) vanishes. Every pair
\(\{p,q\}\), \(q\in F\), is good and \(|F|\ge3\), so the flat exact-fan
theorem applies and gives

\[
                              A_{pq}=0\qquad(q\in F).              \tag{5}
\]

All nonzero blocks at \(p\) therefore go to bad neighbours. By (2),

\[
                d_A(p):=|\{j\ne p:A_{pj}\ne0\}|\le4.             \tag{6}
\]

The forced incident-edge theorem supplies, for each \(c=0,1,2\), a
distinct neighbour \(a_c\), a nonzero vector \(u_c\in V_p\), and a
nonzero complementary cofactor such that

\[
 A_{p a_c}=u_c^{(p)}\otimes e_c^{(a_c)},\qquad
 H_{B\setminus\{p,a_c\}}(A)\ne0.                          \tag{7}
\]

The neighbours are distinct because a nonzero rank-one block cannot have
its opposite image in two different coordinate lines. Hence
\(d_A(p)\ge3\). Together with (6), this proves Theorem 1.

Notice that the threshold \(N=8\) is exact for this composition: it is
precisely what makes the fan in (3) have at least three members.

There is also a short ordered version. Choose a \(4\)-degeneracy ordering
\(p_1,\ldots,p_N\) of the bad graph, so that \(p_i\) has at most four bad
neighbours among \(p_i,\ldots,p_N\). Its total bad degree is at most
\[
                              \deg_{\cal B}(p_i)\le i+3.          \tag{7a}
\]
Whenever \(i\le N-7\), the complementary good fan has at least three
members. Thus, in the absence of every canonical curvature,
\[
                              d_A(p_i)\le i+3
                              \qquad(i\le N-7).                  \tag{7b}
\]
In particular, for every \(N\ge10\) there are three distinct ordered
centres of block degrees at most \(4,5,6\). The low-degree transversal
theorem applies to this whole packet: the first centre is already
cubic/partition-kernel, the second can additionally have a common-line
residue, and the third can additionally have a common-plane residue.
This is the natural setting in which the edge-overlap rules below can be
used; the alternatives are attached to three sites of one source, not to
independently chosen abstract stars.

## 3. The two surviving local forms

If \(d_A(p)=3\), the cubic-vertex lemma gives, after indexing the three
neighbours by colour,

\[
                A_{p a_c}=w_c e_c^{(p)}\otimes e_c^{(a_c)},
                \qquad w_c\ne0.                                \tag{8}
\]

Contracting the star expansion at \(p\) by \(e_c^*\) leaves only this
term, so it also gives the useful cofactor identity

\[
       H_{B\setminus\{p,a_c\}}(A)
          =w_c^{-1}e_c^{\otimes(B\setminus\{p,a_c\})}.            \tag{9}
\]

If \(d_A(p)=4\), retain the three anchors (7) and denote the fourth
neighbour by \(r\). Let

\[
 C_r=H_{B\setminus\{p,r\}}(A),\qquad
 \pi_c:V_{a_c}\longrightarrow V_{a_c}/\mathbb Ce_c.       \tag{10}
\]

Apply the three quotient maps to the star expansion at \(p\). Every
constant target term dies at its same-colour anchor, and every anchor term
dies at its own centre. Consequently

\[
 A_{pr}\otimes
   (\pi_0\otimes\pi_1\otimes\pi_2\otimes\operatorname{id})C_r=0.
                                                                    \tag{11}
\]

Since \(A_{pr}\ne0\),

\[
 \boxed{
 C_r\in\sum_{c=0}^2 e_c^{(a_c)}\otimes
       \bigotimes_{v\in B\setminus\{p,r,a_c\}}V_v .}             \tag{12}
\]

This includes the case in which the fourth block is tensor-inactive and
\(C_r=0\). No entry-minimality assumption is needed.

Equations (8)--(12) are the exact flat endpoint left by the global
argument. In particular, a continuation does not have to classify a
three-port common centre plane before obtaining a uniformly bounded
foothold.

## 4. The degree-four port either becomes pure or exports deficiency

The remaining port has a useful opposite-centre interpretation which is
not visible in the quotient (12).

**Lemma 2 (pure cofactor or essential-direction export).** In the
degree-four case, put

\[
                         U=\operatorname{span}(u_0,u_1,u_2)
                                  \subseteq V_p.                  \tag{13}
\]

Exactly one of the following holds.

1. The anchor factors are dependent. Then \(U\) is a coordinate
   two-plane: for a unique \(k\),

   \[
             U=\ker e_k^*,\qquad
             (e_k^*\otimes\operatorname{id})A_{pr}
                    =\gamma e_k^{(r)},\qquad
             C_r=\gamma^{-1}
                    e_k^{\otimes(B\setminus\{p,r\})}              \tag{14}
   \]

   for some \(\gamma\ne0\).
2. The anchor factors are a basis of \(V_p\). Then the deleted
   endpoint-star map at \(p\) for the pair \(\{p,r\}\) is injective.
   Since \(pr\) is a bad pair, the opposite deleted star is noninjective:

   \[
      W_r^{(p)}:=
        \sum_{x\notin\{p,r\}}\operatorname{im}_{V_r}A_{rx}
                \subsetneq V_r.                                \tag{15}
   \]

   Moreover

   \[
          W_r^{(p)}+\operatorname{im}_{V_r}A_{rp}=V_r,
          \qquad
          \operatorname{im}_{V_r}A_{rp}\not\subset W_r^{(p)}.    \tag{16}
   \]

Thus dependence produces a literal pure complementary matching tensor,
while independence propagates the obstruction across the fourth edge as
an essential direction transverse to a proper opposite star flag.

**Proof.** Suppose first that \(U\ne V_p\), and take nonzero
\(\lambda\in\operatorname{Ann}U\). Contracting the star expansion at
\(p\) kills all three anchors and gives

\[
 \sum_{i=0}^2\lambda(e_i)e_i^{\otimes(B\setminus\{p\})}
   =
 ((\lambda\otimes\operatorname{id})A_{pr})^{(r)}
       \otimes C_r.                                           \tag{17}
\]

The left side is nonzero. Across the flattening
\(V_r\mid\bigotimes_{x\notin\{p,r\}}V_x\), its rank is the number of
nonzero coordinates \(\lambda(e_i)\), since the corresponding constant
tensors on the other \(N-2\) sites are independent. The right side has
rank one. Hence every nonzero element of \(\operatorname{Ann}U\) is
supported on one coordinate covector.

The annihilator cannot have dimension at least two: two independent
coordinate covectors in it would have a sum supported on two coordinates.
Therefore \(U\) is a plane and its annihilator is one coordinate line,
say \(\mathbb Ce_k^*\). Unique factorization of the nonzero decomposable
equality (17) gives (14).

Now suppose \(U=V_p\). Deleting \(r\) leaves the three maps
\(\lambda\mapsto\lambda(u_c)e_c\), whose direct sum is injective because
the \(u_c\)'s are a basis. Thus the \(p\)-endpoint star of the deleted pair
is injective. The edge \(pr\) goes to a bad neighbour of \(p\), so the
pair is not good and its \(r\)-endpoint star must be noninjective. This is
exactly the proper containment (15). The complete mode-\(r\) support
spans \(V_r\) by the target-flattening theorem. Splitting that support into
the \(p\)-block and all other blocks proves both assertions in (16).
\(\square\)

The two conclusions suggest distinct continuations. In the pure branch,
one can overlap (14) with the other two pure cofactors at a nearby cubic
port. In the export branch, essential-subspace counting allows at most
three such incoming directions at any opposite centre. This is a bounded
incidence problem attached to actual deficient endpoint flags, not to
arbitrary line/plane residual labels.

## 5. What the discarded line and plane cases do on overlaps

For later use, their genuine overlap content can also be recorded without
coordinates beyond the three target axes. Suppose centres have chosen
anchor/residual decompositions from the low-degree transversal theorem.

**Lemma 3 (edge-status propagation).** Let \(uv\) be nonzero.

1. If \(uv\) is a colour-\(c\) anchor at \(u\) and a common-line residual
   at \(v\), then the residual line at \(v\) is
   \(\mathbb Ce_c\). Hence all anchor-to-residual edges entering the same
   common-line centre carry one and the same colour.
2. If \(uv\) is a colour-\(c\) anchor at \(u\) and a common-plane residual
   at \(v\), then \(e_c\) lies in the residual plane at \(v\). Hence at
   most two distinct anchor colours can enter residual ports of that
   centre.
3. If \(uv\) is residual at both endpoints, then

   \[
          A_{uv}\in L_u\otimes L_v
          \quad\hbox{or}\quad
          A_{uv}\in P_u\otimes P_v,                         \tag{18}
   \]

   in the common-line or common-plane cases, respectively.
4. If \(uv\) is an anchor at both endpoints, of colours \(c\) at \(u\)
   and \(d\) at \(v\), then

   \[
                        A_{uv}\in
                   \mathbb C^*e_d^{(u)}\otimes e_c^{(v)}.    \tag{19}
   \]

**Proof.** An anchor of colour \(c\) at \(u\) has the form
\(x^{(u)}\otimes e_c^{(v)}\). A residual condition at \(v\) says that
the \(v\)-side image of the same nonzero tensor is contained in \(L_v\)
or \(P_v\), proving the first two assertions. Applying the residual image
condition at both endpoints gives (18). Two nonzero rank-one
factorizations of the anchor-anchor block have the same two factor lines,
which gives (19). \(\square\)

There is a similarly exact propagation statement for two degree-four
partition kernels. Suppose \(uv\) is the fourth port at both endpoints,
the two anchor triples \((a_0,a_1,a_2)\) and \((b_0,b_1,b_2)\) are
disjoint, and their killed lines are \(L_i\subset V_{a_i}\) and
\(M_j\subset V_{b_j}\). Applying (12) at both endpoints and using
exactness of tensor products over a field gives

\[
 \boxed{
 C_{uv}\in
   \sum_{i=0}^2\sum_{j=0}^2
       L_i^{(a_i)}\otimes M_j^{(b_j)}\otimes
       \bigotimes_{x\notin\{u,v,a_i,b_j\}}V_x .}                 \tag{20}
\]

Indeed, after grouping the two disjoint triples, the two kernels are
\(K_a\otimes V_b\otimes W\) and
\(V_a\otimes K_b\otimes W\); their intersection is
\(K_a\otimes K_b\otimes W\). Expanding the two one-site kernel sums
gives (20).

These rules are sharp as statements about local tensor geometry. A pure
tensor containing one prescribed line from each anchor triple lies in
(20), and choosing all residual lines equal to one coordinate axis, or all
residual planes equal to one coordinate two-plane, realizes every allowed
incidence in Lemma 3. Thus edge-status propagation alone cannot kill the
residues. The content of Theorem 1 is that the global good-fan overlap
avoids that dead end: it finds a degree-three/four centre before such a
line/plane classification is needed.

## 6. Sharp graph boundary

The number four cannot be improved using only bad-graph degeneracy and
flatness. On eight cyclically labelled vertices, the square \(C_8^2\) is
four-regular (join vertices at cyclic distance one or two), hence
\(4\)-degenerate. Declare these pairs bad and the three remaining
neighbours at each vertex good. A support contained in the bad graph is
compatible with the degeneracy and fan-size inequalities used in Theorem 1
and has degree four everywhere.

This is only a sharp graph guard, not an exact source. To finish the flat
branch one must use (12), its opposite-centre refinements such as (20), or
the unquotiented target rows. Further bad-pair counting by itself cannot
force a cubic vertex.

No executable is needed: the only inputs to Theorem 1 are the already
audited \(4\)-degeneracy and flat-fan theorems, and Lemmas 2--3 and (20) are
elementary factor-line and tensor-kernel identities.
