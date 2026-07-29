# Independent audit: the \(p=28\), \(4^3 3^6\) residual rank-one branch

## 1. Verdict and exact scope

**PASS.**  This audit independently reconstructs the generic-rank-one
exclusion in
[the primary note](live-three-zero-higher-split-p28-three-quartic-six-triple-rank-one-closure.md).
It uses only the previously audited \(q=5\) saturation normal form:

\[
 \mathcal K\subset \mathbb C[z]_{\leq9},\qquad
 \dim\mathcal K=6,
\]

the echelon degrees are \(4,5,6,7,8,9\), and the three exact quartic and
six exact triple rows exhaust the Wronskian degree \(24\).  For

\[
 F(z)=E(t)+zO(t),\qquad t=z^2,
\]

the primitive residual four-plane bundle \(W\) has annihilator

\[
 \mathcal A\simeq\mathcal O(-\alpha)\oplus\mathcal O(-\beta),
 \qquad 2\leq\alpha\leq\beta,
 \qquad d=\alpha+\beta\leq6.                 \tag{1}
\]

The independently verified conclusion is

\[
 \boxed{\operatorname{rank}_{\mathrm{gen}}\theta\ne1},
 \qquad
 \theta:W\longrightarrow\mathcal A^*\otimes\Omega_{\mathbb P^1}.
\]

Generic rank zero is also impossible: it would make the Grassmannian map
\(t\mapsto\mathcal A_t\) constant, whereas (1) has positive Pluecker
degree \(d\geq4\).  Hence the residual map has generic rank two.  Combined
with the previously audited degree-six reduction, this leaves precisely
the splittings \((2,4)\) and \((3,3)\).  Neither splitting is closed here.

## 2. Duality and the focal-line dichotomy

Work locally with a frame of the rank-two subbundle
\(\mathcal A\subset V^*\otimes\mathcal O\), where \(\dim V=6\).  The
differential of its Grassmannian map is

\[
 \phi:\mathcal A\longrightarrow
       (V^*/\mathcal A)\otimes\Omega_{\mathbb P^1}.
                                                        \tag{2}
\]

Under the natural annihilator pairing, (2) is the transpose of the second
fundamental map \(\theta\), so the two maps have the same generic rank.
If this rank is one, the saturated kernel of (2) is a line subbundle
\(M\subset\mathcal A\).  Choose a local nonzero lift \(\gamma(t)\in V^*\)
of \(M\).  The condition \(\phi(\gamma)=0\) says exactly that

\[
                         \gamma'(t)\in\mathcal A_t.       \tag{3}
\]

There are now only two cases.

* If the projective point \([\gamma(t)]\) is constant, every line
  \(\mathbb P(\mathcal A_t)\) passes through a fixed vertex.  That vertex
  gives a nowhere-zero constant section
  \(\mathcal O\hookrightarrow\mathcal A\), impossible because both
  summands in (1) have negative degree.
* Otherwise \(\gamma\) is nonconstant, and (3), together with the generic
  rank two of \(\mathcal A\), gives after saturation

  \[
                         \mathcal A_t
                         =\langle\gamma(t),\gamma'(t)\rangle. \tag{4}
  \]

Thus (4) is the tangent-line family of its focal or edge curve.  This
derivation includes planar developables and multiple covers; it does not
silently assume that the ruled surface is nonplanar or birational to its
edge.

## 3. The complete tangent-edge ledger, including infinity

Let \(U\subset V^*\) be the coefficient span of a primitive homogeneous
lift of \(\gamma\), put \(m=\dim U\), and let \(e\) be the degree of the
resulting nondegenerate \(g^{m-1}_e\) on the same, fixed \(\mathbb P^1\).
At every point \(x\), including infinity, write its vanishing sequence as

\[
 0=a_0(x)<a_1(x)<\cdots<a_{m-1}(x).
\]

In a local parameter at \(x\), the common order removed from
\(\gamma\wedge\gamma'\) is exactly \(a_1(x)-1\).  Therefore, with

\[
 R_1=\sum_{x\in\mathbb P^1}(a_1(x)-1),
\]

the primitive tangent-line Pluecker degree is

\[
                         d=2e-2-R_1.                       \tag{5}
\]

The Wronskian of the \(g^{m-1}_e\) has total weight

\[
                         m(e-m+1).                         \tag{6}
\]

If \(s=a_1(x)-1\), strict increase gives \(a_j(x)\geq j+s\) for every
\(j\geq1\).  Hence that point spends at least \((m-1)s\) units of (6),
and globally

\[
                  (m-1)R_1\leq m(e-m+1).                  \tag{7}
\]

For \(m\geq4\), combining (5)--(7), \(4\leq d\leq6\), and
\(e\geq m-1\) gives the finite bound

\[
 (m-2)e\leq(m-1)(d+2-m).
\]

The complete integer ledger is

\[
\begin{array}{c|c|c|c}
m&e&d&R_1\\ \hline
4&3&4&0\\
4&4&5&1\\
4&4&6&0\\
4&5&6&2\\
4&6&6&4\\
5&4&6&0.
\end{array}                                               \tag{8}
\]

There is no \(m=6\) case.  If \(m\leq2\), the tangent line in (4) is
constant.  The remaining \(m=3\) case is disposed of in the next section.

## 4. Why \(E,O\) lie in the second-osculating kernel

Every member of \(\mathcal A_t\) annihilates
\(E,O,E',O'\).  In particular, using (4),

\[
 \gamma E=\gamma'E=\gamma E'=\gamma'E'=0.
\]

Differentiating \(\gamma'E=0\) and using \(\gamma'E'=0\) gives
\(\gamma''E=0\).  The same argument applies to \(O\).  Thus, as a generic
identity and hence after saturation everywhere,

\[
 E(t),O(t)\in
 D_t:=\ker\langle\gamma,\gamma',\gamma''\rangle.          \tag{9}
\]

For \(m=3\), the three covectors in (9) generically span all of \(U\), so
\(D_t=U^\perp\), a fixed three-space in \(V\).  Then
\(E,O,E',O'\) all lie in that three-space, contradicting the nonzero
residual four-wedge.  This also explains why (8) begins with \(m=4\).

## 5. Four-dimensional edge span

Assume \(m=4\) and set \(C=U^\perp\), so \(\dim C=2\).  Modulo \(C\),
the saturated kernel in (9) is the osculating-dual line
\(\langle\nu(t)\rangle\), and

\[
                         D_t=C\oplus\langle\nu(t)\rangle. \tag{10}
\]

The osculating-dual curve \(\nu\) spans \(\mathbb P^3\).  Indeed, a
constant hyperplane relation on \(\nu\) would, after a constant change of
basis in \(U\), say

\[
 \det(\gamma,\gamma',\gamma'',e_4)=0.
\]

This determinant is the ordinary Wronskian of three transformed coordinate
functions of \(\gamma\).  In characteristic zero those three functions
would be linearly dependent over the constants; adding the fourth
coordinate would make the coefficient span of \(\gamma\) at most three,
contrary to \(m=4\).

Let \(e^*\) be the degree of the primitive curve \(\nu\).  Homogenizing
the degree-at-most-four vector polynomials \(E,O\), their projections in
(10) factor as bundle maps

\[
                 \mathcal O(-4)\longrightarrow\mathcal O(-e^*). \tag{11}
\]

At least one is nonzero; otherwise \(E,O\), and therefore their
derivatives, lie in the fixed two-space \(C\).  Thus (11) implies
\(e^*\leq4\).  On the affine chart there are polynomials \(p,q\) and
\(C\)-valued terms such that

\[
 E=p\nu+c_E,\qquad O=q\nu+c_O.
\]

Consequently the four quotient coordinates of \(F\) form the series

\[
             A(z)\mathcal V(z^2),\qquad
             A(z)=p(z^2)+zq(z^2)\ne0,                    \tag{12}
\]

where \(\mathcal V\) is a four-dimensional nondegenerate coordinate
series.  At \(t=0\), three jet conditions impose at most three independent
conditions on this four-series.  Hence it has a nonzero member of order at
least three.  Pullback by \(t=z^2\) and multiplication by the regular
nonzero polynomial \(A\) turn it into a nonzero member of \(\mathcal K\)
of order at least six at \(z=0\).

## 6. Five-dimensional edge span

The final row of (8) has \(m=5,e=4,R_1=0\).  A five-dimensional degree-four
series on \(\mathbb P^1\) is the complete \(H^0(\mathcal O(4))\).  Thus a
constant target change, with no reparameterization of the fixed domain
coordinate \(t\), gives

\[
                         \gamma=(1,t,t^2,t^3,t^4).         \tag{13}
\]

Inside \(U^*\), the kernel of \(\gamma,\gamma',\gamma''\) has the exact
polynomial frame

\[
\begin{aligned}
u&=(-t^3,3t^2,-3t,1,0),\\
v&=(0,-t^3,3t^2,-3t,1).
\end{aligned}                                             \tag{14}
\]

The minor in the last two coordinates is one, so any polynomial section
of this kernel has a unique polynomial expression \(au+bv\).  If all five
coordinates have degree at most four, the first coordinate forces
\(\deg a\leq1\); the second then forces \(\deg b\leq1\).  Applying this to
both \(E\) and \(O\), and separating the fixed line \(C=U^\perp\), gives

\[
 E=au+bv+c_E,\qquad O=ru+sv+c_O,
 \qquad \deg a,\deg b,\deg r,\deg s\leq1.                 \tag{15}
\]

The first coordinate of \(F\) is therefore

\[
                         -z^6(a(z^2)+zr(z^2)).             \tag{16}
\]

It is not identically zero.  If it were, parity would give \(a=r=0\),
and the first coordinate of the complete evaluation vector would vanish,
which is a constant relation among the chosen basis of \(\mathcal K\).
Thus (16) is again a nonzero section of order at least six at zero.

## 7. The terminal Wronskian contradiction

For a six-dimensional polynomial series, a nonzero section of order at
least six forces the last term of the vanishing sequence at zero to be at
least six.  The smallest possible sequence is

\[
                         (0,1,2,3,4,6),
\]

of Wronskian weight one.  Both surviving rows of (8) therefore make
\(z=0\) a Wronskian root.

All nine prescribed quartic and triple values are nonzero, so zero is not
one of them.  Their exact weights already sum to

\[
                         3(6-4)+6(6-3)=24,
\]

the complete degree \(6(10-6)=24\) of the Wronskian of \(\mathcal K\).
The extra root is impossible.  This proves the generic-rank-one exclusion.

## 8. Independent executable check

[The standalone verifier](../computations/verify_live_three_zero_higher_split_p28_three_quartic_six_triple_rank_one_closure_independent_audit.py)
imports no primary checker.  It independently checks the complete integer
ledger, the cofactor determinant identity behind osculating-dual
nondegeneracy, the bundle-degree alternatives, the full degree-four
polynomial solution module for (13)--(15), and the final square-cover and
Wronskian-order calculation.
