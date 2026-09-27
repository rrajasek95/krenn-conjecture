# Optimal W-state rates with two roots: connected cores at every even order, and all cores at six sites

September 26, 2026. **Written proof with exact supporting checks; awaiting
independent audit. Unrestricted colored-core optimality remains open.**

[Guide](../explainers/BOUNDARY-STRUCTURE.md) ·
[Replay](../computations/higher-order-2026-09-26/README.md) ·
[Earlier odd-cycle reduction](two-root-w-state-reduction-2026-09-26.md)

## 1. The strengthened theorem

Let \(n=2m\ge6\), with two root sites \(p,q\). Edges between the other
\(n-2\) sites form an arbitrary complex scalar \(aa\) core \(D\).
All edges incident to either root are unrestricted complex endpoint-color
blocks. Set

\[
 \tau=\operatorname{haf}(D),\qquad
 C_{ij}=\operatorname{haf}(D\setminus\{i,j\})\ (i\ne j),
 \qquad C_{ii}=0.
\]

The cofactor graph contains edge \(ij\) when \(C_{ij}\ne0\).
For an exact uniform W output \(H=\lambda W_n\), \(\lambda\ne0\),
use the normalized strength \(R=n|\lambda|^2/S^m\).

**Theorem A.** If the cofactor graph is connected, the source can be replaced
by a one-root source with the same output and no larger source norm. Its
exact optimal rate is therefore

\[
 \boxed{R_{\max}=\frac{n B_n}{(n-1)^2+1},\qquad
       B_n=\frac{((n-1)!!)^2}{\binom{n}{2}^{m}}.}           \tag{1}
\]

Connected bipartite graphs are included. The matrix \(C\) may be singular.
This removes the odd-cycle requirement from the earlier theorem.

**Theorem B.** At six sites the same optimum, **\(1/65\)**, holds over
the entire two-root architecture, including disconnected cofactor graphs.
Every feasible disconnected case has rate at most \(1/144<1/65\).

The complete-core one-root construction attains (1) and belongs to these
two-root classes. At eight or more sites, disconnected cofactor graphs still
need analysis. Neither theorem covers arbitrary colored cores.

## 2. All relevant output equations

First project every local color space onto \(a,b\). This preserves the
W output and can only decrease the source norm. For each core site \(i\),
write the two binary root blocks as

\[
 A_{pi}=\begin{pmatrix}x_i&u_i\\s_i&d_i\end{pmatrix},
 \qquad
 A_{qi}=\begin{pmatrix}y_i&v_i\\t_i&e_i\end{pmatrix}.
\]

Rows specify root colors; columns specify core colors. Let \(Z=A_{pq}\).
Two core excitations, with root colors respectively \(aa,ba,ab,bb\), give

\[
 C_{ij}(u_iv_j+u_jv_i)=0,\quad
 C_{ij}(d_iv_j+d_jv_i)=0,
\]
\[
 C_{ij}(u_ie_j+u_je_i)=0,\quad
 C_{ij}(d_ie_j+d_je_i)=0.                                 \tag{2}
\]

One core excitation gives

\[
 u_i(Cy)_i+v_i(Cx)_i=\lambda,                              \tag{3}
\]
\[
 d_i(Cy)_i+v_i(Cs)_i=0,\quad
 u_i(Ct)_i+e_i(Cx)_i=0,\quad
 d_i(Ct)_i+e_i(Cs)_i=0.                                   \tag{4}
\]

No core excitation gives

\[
 \tau Z_{aa}+x^TCy=0,\qquad
 \tau Z_{ba}+s^TCy=\lambda,
\]
\[
 \tau Z_{ab}+x^TCt=\lambda,\qquad
 \tau Z_{bb}+s^TCt=0.                                    \tag{5}
\]

These are bilinear transposes, not Hermitian inner products. Conjugates enter
only in norm estimates. Together these equations cover every output:
the scalar core permits at most two excited core sites.

Equation (3) forces \((u_i,v_i)\ne(0,0)\) and a nonzero row of \(C\)
at every core site. In particular, feasible graphs have no isolated vertices.

## 3. What connectedness forces

The first equation in (2) has two possibilities on a connected graph.

* If one pair \((u_i,v_i)\) has only one nonzero entry, that type propagates
  to every neighbor. Exchange the roots if necessary to get \(v=0\) and
  every \(u_i\ne0\).
* Otherwise every \(u_i,v_i\ne0\), and \(v_i/u_i\) changes sign across
  each edge. The graph is bipartite. For its signs \(\sigma_i\in\{1,-1\}\),
  one has \(v=rJu\), where \(r\ne0\) and
  \(J=\operatorname{diag}(\sigma_i)\).

On a bipartite graph \(CJ=-JC\), so \(JC\) is skew-symmetric and
\(z^TJCz=0\) for every complex vector \(z\). No matrix inversion is used.

### The pure-type branch reduces by deletion

Suppose \(v=0\). Then (3) implies every \((Cy)_i\ne0\), so (4) gives
\(d=0\). On an odd-cycle graph, (2) forces \(e=0\), and then \(Ct=0\).
On a bipartite graph, it instead gives \(e=\beta Ju\) and
\(Ct=-\beta JCx\). In either case

\[
                            x^TCt=0.
\]

Equation (5) therefore yields \(\tau Z_{ab}=\lambda\), in particular
\(\tau\ne0\). Delete \(t,e,Z_{bb}\). Outputs with root \(q\) excited
and a core excitation disappear; the root-only excitation at \(q\) remains
\(\tau Z_{ab}=\lambda\); both roots excited now have zero output.
Every other output is unchanged. The resulting source has only \(aa\)
edges away from \(p\), and deletion cannot increase its norm.

### The mixed branch reduces by balancing two vectors

Now let \(v=rJu\), with all entries of \(u\) nonzero. The second and third
equations of (2) give \(d=\alpha u\), \(e=\beta Ju\), for scalars
\(\alpha,\beta\). The first two equations of (4) imply

\[
 Cs=-\frac{\alpha}{r}JCy,\qquad Ct=-\beta JCx.
\]

Skew-symmetry gives

\[
 s^TCy=-\frac{\alpha}{r}y^T JCy=0,\qquad
 x^TCt=-\beta x^T JCx=0.
\]

Thus (5) forces \(\tau\ne0\) and
\(Z_{ba}=Z_{ab}=\lambda/\tau\).

Set
\[
 z=y-rJx,\qquad k=1+|r|^2,\qquad
 u'=\sqrt{k}\,u,\qquad y'=z/\sqrt{k}.
\]
Using \(CJ=-JC\), equation (3) becomes
\(u'_i(Cy')_i=\lambda\). Build a new source retaining \(D\), using
only \(u'\) from root \(p\) to core color \(b\), only \(y'\) from root
\(q\) to core color \(a\), and the direct cells
\(Z'_{ba}=Z'_{ab}=\lambda/\tau\). Set all other root cells to zero.
Its output is exactly \(\lambda W_n\), and it is a one-root source.

Its source norm cannot exceed the original, because

\[
 \|u'\|^2=\|u\|^2+\|v\|^2,
\]
\[
 \boxed{\|x\|^2+\|y\|^2-\frac{\|y-rJx\|^2}{k}
      =\frac{\|x+\overline r Jy\|^2}{k}\ge0.}             \tag{6}
\]

The two retained direct cells are unchanged, and all remaining source
energy is discarded. This proves the reduction in the mixed branch.
Applying the earlier [one-root optimum](w-state-optimal-design-2026-09-26.md)
and its complete-core attaining construction proves Theorem A.

## 4. The disconnected six-site cases have a strict rate gap

There are four core vertices. A disconnected graph without isolated
vertices consists of two disjoint edges. At four sites a cofactor entry is
the scalar source entry on the complementary pair. Thus \(C\), and also
\(D\), has precisely two disjoint supported edges. Write the magnitudes of
the two cofactor weights as \(c,d>0\); the scalar core energy is
\(a=c^2+d^2\).

For a pair \(i,j\) with cofactor weight of magnitude \(c\), equation (3)
and \(2|zw|\le|z|^2+|w|^2\) give

\[
 2|\lambda|\le\frac c2
   \sum_{v\in\{i,j\}}(|u_v|^2+|v_v|^2+|x_v|^2+|y_v|^2).
\]

Summing the two components, and discarding other nonnegative source energy,

\[
              S\ge a+b|\lambda|,\qquad
              b=4(1/c+1/d).
\]

Optimizing the resulting upper bound over \(|\lambda|\ge0\) gives

\[
 R=\frac{6|\lambda|^2}{S^3}
     \le\frac8{9ab^2}\le\frac1{144}.                     \tag{7}
\]

The first maximum is at \(|\lambda|=2a/b\).
For the second inequality,
\((c^2+d^2)(1/c+1/d)^2\ge8\), with equality at \(c=d\).
Both follow from the exact factorizations

\[
 (1+t)^3-\tfrac{27}{4}t^2=\tfrac14(t-2)^2(4t+1),
\]
\[
 (c^2+d^2)(c+d)^2-8c^2d^2
       =(c-d)^2(c^2+4cd+d^2).
\]

The estimate (7) need not be attained: root-only target constraints were
discarded when obtaining it. Its strict separation from \(1/65\) suffices.
Together with Theorem A and the known attaining source, it proves Theorem B.

## 5. Evidence and remaining scope

The exact replay includes complex bipartite examples in both mixed branches
and the pure-type branch. It checks every ternary output coefficient before
and after reduction, the strict source-energy decrease, and the norm
factorization. It enumerates all 64 labeled four-vertex support graphs,
confirming the three disconnected possibilities without isolated vertices.
These checks support the written universal argument; they are not themselves
an exhaustive search over complex weights or a Lean proof.

The next W-state questions are disconnected cofactor graphs for \(n\ge8\),
and designs whose core itself has non-ground colored entries. The six-site
result is complete for the two-root architecture, not for all six-site sources.
