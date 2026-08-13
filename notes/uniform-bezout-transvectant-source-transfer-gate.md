# The uniform Hankel transfer is a simultaneous Bezout-kernel theorem

## Outcome

Let $h\geq3$, let $U$ be the binary clean-line parameter space, and let

\[
             \mathcal E_h\subseteq\operatorname {Sym}^hU^*
\]

be the clean error space. The desired uniform transfer must construct a
nonzero

\[
 \Theta_h\in\ker\!\left(
   \mu_{\mathcal E_h}^*:
   (\operatorname {Sym}^{2h-1}U^*)^*
   \longrightarrow
   (\mathcal E_h\otimes\operatorname {Sym}^{h-1}U^*)^*
                         \right).                         \tag{1}
\]

A classical Bezoutian gives an exact finite reformulation of (1), but not
an automatic construction. Choose $0\ne f\in\mathcal E_h$, dehomogenize on
a chart where $f$ is monic, and put

\[
                       A_f=\Bbbk[t]/(f).
\]

Then (1) is equivalent to the existence of

\[
 \boxed{
  0\ne a_h\in A_f,\qquad
  \bar e\,a_h=0\quad\text{for every }e\in\mathcal E_h.}  \tag{2}
\]

Equivalently,

\[
                 z_h=B(f,1)^{-1}a_h                     \tag{3}
\]

is a simultaneous kernel vector for

\[
                   B(f,e),\qquad e\in\mathcal E_h.       \tag{4}
\]

This identifies the shortest possible positive theorem for the proposed
transfer $\operatorname {Tr}_h$: the complete source equations must
produce the **same nonzero Bezout-kernel section for every clean
coordinate**, with a physical source boundary and terminal normalization.

The existing grade-split sum-channel row does not imply (2). Neither does
the $(h-1)$-st transvectant. Indeed,

\[
       (u^h,v^h)_{h-1}=(h!)^2uv\ne0,                     \tag{5}
\]

while $u^h,v^h$ are coprime and their Bezout matrix is invertible. Thus a
nonzero selector quadratic obtained by transvection is compatible with the
rootless branch.

There is also a uniform typing gap which is invisible at $h=3$. The
transvectant (5) lies in $\operatorname {Sym}^2U$, of dimension three,
whereas $A_f$, the residual quotient, and its dual have dimension $h$.
These dimensions agree only when $h=3$. If the transfer is to be a
Cartan-product prolongation of the selector quadratic, it needs an
additional source-derived degree-$(h-3)$ covariant, followed by the
$f$-dependent residual/Bezout identification. A direct construction of
(2) would be equivalent and need not factor this way.

Finally, singularity of one selected Bezout matrix is insufficient. The
selected pair can share one root and a second pair can share a different
root, while the simultaneous kernel in (4) is zero. A uniform adjugate
also works only on the corank-one stratum; it vanishes identically at
corank at least two. A source-faithful construction must therefore include
a first-nonzero-subresultant/Fitting normalization and prove that its local
kernel sections glue and remain nonzero.

Under the currently committed inputs, no such relation is available. The
ordinary Yoneda/cup route does not add it: the relevant cup of a comparison
boundary with the augmented cap cycle is again a boundary, and the split
cap connecting class is a relative lifting obstruction rather than an
absolute terminal. Hence the present result is a sharp gate, not a proof
of $\operatorname {Tr}_h$ or of Krenn's conjecture.

## 1. The residual quotient is a Frobenius algebra

Choose coordinates $[t:1]$ so that $f(t)$ is monic of degree $h$. The
degree-$(2h-1)$ residual quotient

\[
 Q_f=\operatorname {Sym}^{2h-1}U^*/
             f\operatorname {Sym}^{h-1}U^*               \tag{6}
\]

is identified, by polynomial division, with $A_f=\Bbbk[t]/(f)$. Under this
identification the residual Macaulay map is

\[
 \bar\mu:\mathcal E_h\otimes A_f\longrightarrow A_f,
                      \qquad e\otimes b\longmapsto\bar e b. \tag{7}
\]

Let

\[
 \epsilon:A_f\longrightarrow\Bbbk,\qquad
 \epsilon(b)=[t^{h-1}]b                                  \tag{8}
\]

for the unique representative of degree below $h$. The pairing

\[
                         (b,c)_f=\epsilon(bc)             \tag{9}
\]

is nondegenerate. If $b\ne0$ has leading term $b_dt^d$, multiplication by
$t^{h-1-d}$ reads $b_d$ in (8), with no reduction term of degree $h$.
Thus $A_f\simeq A_f^*$ as $A_f$-modules.

For $w\in A_f$, let $\lambda_w(b)=\epsilon(wb)$. Nondegeneracy gives

\[
\begin{aligned}
 \lambda_w(\bar e b)=0\quad\text{for all }b\in A_f
  &\Longleftrightarrow \bar e w=0,\\
 \lambda_w\circ\bar\mu=0
  &\Longleftrightarrow
  w\in\operatorname {Ann}_{A_f}(\bar{\mathcal E}_h).     \tag{10}
\end{aligned}
\]

This proves the equivalence of (1) and (2). It also shows why the desired
object is not merely a scalar determinant: it is a nonzero element in the
annihilator of the entire clean ideal.

The previously proved residual-Macaulay theorem gives

\[
 \dim\operatorname {Ann}_{A_f}(\bar{\mathcal E}_h)
       =\deg\gcd(\mathcal E_h).                           \tag{11}
\]

Consequently (2) is already equivalent to the common-root conclusion. A
positive source theorem must construct $a_h$; it cannot assume rank loss
and then advertise the Bezoutian as an independent reason for it.

## 2. Exact Bezout form of the missing relation

For dehomogenized forms of degree at most $h$, use the convention

\[
 \frac{f(x)e(y)-f(y)e(x)}{x-y}
       =\sum_{0\leq i,j<h}B(f,e)_{ij}x^iy^j.             \tag{12}
\]

Let $M_{\bar e}$ denote multiplication by $\bar e$ on $A_f$ in the
monomial basis. Barnett's identity in this convention is

\[
                  B(f,e)=M_{\bar e}B(f,1).               \tag{13}
\]

The matrix $B(f,1)$ is invertible for monic $f$. Therefore

\[
 \bigcap_{e\in\mathcal E_h}\ker B(f,e)
   =B(f,1)^{-1}
       \operatorname {Ann}_{A_f}(\bar{\mathcal E}_h).    \tag{14}
\]

Equations (10) and (14) give a completely finite interface for
$\operatorname {Tr}_h$. The exact extra source relation beyond the
grade-split identity is a chain $Z_h$ and a Bezout-coordinate readout
$z_h$ such that

\[
\begin{array}{ll}
 dZ_h=0 & \text{in the complete source/relative totalization},\\
 B(f,e)z_h=0 & \text{for every literal clean coordinate }e,\\
 z_h\ne0 & \text{under the physical terminal normalization},\\
 z_h & \text{has the word, fine, and repeated grades of }Q_f.
\end{array}                                                \tag{15}
\]

If (15) is proved, putting $a_h=B(f,1)z_h$ and applying the Frobenius
pairing constructs $\Theta_h$ in (1). The residual gcd theorem then closes
the rootless branch immediately.

This formulation is stronger than asking for

\[
                         \det B(f,g)=0                    \tag{16}
\]

for one chosen $g$. For example, take

\[
 f=t^{h-1}(t-1),\qquad e_0=t^h,\qquad e_1=(t-1)^h.        \tag{17}
\]

Both $B(f,e_0)$ and $B(f,e_1)$ are singular. Their kernels encode the roots
$0$ and $1$, respectively, and

\[
              \ker B(f,e_0)\cap\ker B(f,e_1)=0.          \tag{18}
\]

Thus pairwise resultant vanishing must be supplemented by common-kernel
compatibility for all clean coordinates.

## 3. Why the transvectant does not produce the kernel

For $f,g\in\operatorname {Sym}^hU^*$, the $(h-1)$-st transvectant has type

\[
          (f,g)_{h-1}\in\operatorname {Sym}^2U^*         \tag{19}
\]

up to the conventional determinant twist. With

\[
 (f,g)_r=\sum_{k=0}^r(-1)^k{r\choose k}
  (\partial_u^{r-k}\partial_v^kf)
  (\partial_u^k\partial_v^{r-k}g),                       \tag{20}
\]

putting $f=u^h$, $g=v^h$, and $r=h-1$ leaves only $k=0$ and proves
(5). On the affine chart $v=1$, however,

\[
 \frac{x^h-y^h}{x-y}
       =x^{h-1}+x^{h-2}y+\cdots+y^{h-1},                 \tag{21}
\]

so $B(u^h,v^h)$ is the anti-identity and

\[
                   \det B(u^h,v^h)\in\{1,-1\}.           \tag{22}
\]

The clean Macaulay map is consequently an isomorphism and its dual kernel
is zero. This exact algebraic guard rules out the inference

\[
     (f,g)_{h-1}\ne0\quad\Longrightarrow\quad
                     \ker\mu_{\langle f,g\rangle}^*\ne0. \tag{23}
\]

It also clarifies the accidental $h=3$ match. At that order the selector
cycle $\Psi_C$ and a residual representative both have three coefficients.
For $h>3$, their dimensions are $3$ and $h$. There is no canonical
identification supplied by the grade-split equation.

If one insists on a polynomial covariant route, a top Cartan lift would
have schematic form

\[
  \Psi_C\in\operatorname {Sym}^2U,\qquad
  b_{h-3}\in\operatorname {Sym}^{h-3}U,\qquad
  \Psi_C b_{h-3}\in\operatorname {Sym}^{h-1}U.           \tag{24}
\]

The new factor $b_{h-3}$ must come from the complete source equations, and
one must still pass through the $f$-dependent quotient and prove all of
(15). The spectator matching tail has parameter degree zero and does not
supply (24). The activity covariant has a different degree and its unique
Cartan product was already shown to fail the pure-axis Hankel guard.

## 4. Subresultants are local formulas, not the source theorem

On the open part of the resultant divisor where $B(f,g)$ has corank one,

\[
                      \operatorname {adj}B(f,g)\ne0       \tag{25}
\]

and any nonzero column gives the kernel line. This is a useful local
formula for $z_h$. It is not uniform on the full rank-defect locus. If the
corank is at least two, every $(h-1)\times(h-1)$ minor vanishes and

\[
                      \operatorname {adj}B(f,g)=0.        \tag{26}
\]

A uniform construction must choose the first nonzero subresultant on each
Fitting stratum, prove that the resulting local kernel sections agree up to
the permitted unit, and extend the section from the selected $g$ to every
$e\in\mathcal E_h$. It must also prove nonvanishing after the physical
terminal/readout map. None of these statements follows from the two-chart
selector determinant or from the isolated sum-channel row.

There is an even more basic algebraic obstruction to a universal formula
under the current inputs. The coprime locus is Zariski open, and on that
locus $B(f,g)$ is invertible. A polynomial natural section which is
required to lie in its kernel vanishes on this dense open set, hence
vanishes identically unless the source equations first force the relevant
resultant/Fitting ideal to vanish. The source provenance must therefore
enter before, not after, the Bezout construction.

## 5. The Yoneda product does not supply the missing incidence

The tempting homological version is to regard the transvectant or
Bezoutian as a Yoneda product of the selector cycle with the cap/Macaulay
resolution. The committed complexes do not support that conclusion.

First, in any enhancement where the already displayed comparison is a
boundary and the product obeys Leibniz, its cup with the augmented cap
cycle is again a boundary. It cannot be the nonzero absolute class (1).
Second, the universal cap block splits into a free cycle plus a contractible
identity block. Its connecting class is the obstruction to lifting a
relative response, not an absolute Tor class. Third, ordinary
multiplication has the wrong site support; the previously isolated
restriction-insertion/Rees datum is still required to move between the
relevant exposed-site sets.

Thus an actual Yoneda realization of $\operatorname {Tr}_h$ would have to
be secondary and filtered. In addition to (15), it would need:

1. a source-provenant extension class rather than the split cap block;
2. a proof that its indeterminacy has zero $z_h$/terminal readout; and
3. compatibility with the common clean ideal, not merely one selected
   binary pair.

These are precisely new hypotheses, not consequences of the ordinary cup
calculation.

## 6. Shortest positive theorem and proof impact

The remaining uniform rootless lemma can now be stated without reference
to a guessed formula.

> **Simultaneous Bezout transfer theorem.** For every physical clean error
> packet $\mathcal E_h$ produced by an exhaustive source component,
> $h\geq3$, the complete source totalization constructs, functorially in
> the two selector charts, a chain $Z_h$ satisfying (15). Its kernel
> section is compatible with the first-nonzero-subresultant transitions and
> has nonzero physical terminal.

The proof after this theorem is short:

\[
 Z_h\longmapsto z_h
 \overset{(13)}\longmapsto
 a_h=B(f,1)z_h\in
 \operatorname {Ann}_{A_f}(\bar{\mathcal E}_h)\setminus0
 \overset{(10)}\longmapsto
 \Theta_h\in\ker\mu_{\mathcal E_h}^*\setminus0
 \overset{(11)}\Longrightarrow
 \deg\gcd(\mathcal E_h)>0.                               \tag{27}
\]

This closes the rootless branch. Conversely, a physically typed dual
separating the proposed $Z_h$ from the complete source image would be the
sharp obstruction to this route and should be tested for terminal/Fredholm
promotion.

The theorem is strictly stronger than the current grade-split target. The
grade-split row supplies a selector/filtration equation; it does not impose
the multiplication equations $\bar e a_h=0$, construct the missing
degree-$(h-3)$ typed lift, or provide subresultant gluing. Those three
requirements are the exact additional source relation isolated here.

## 7. Exact checker and scope

The dependency-pinned checker
[verify_uniform_bezout_transvectant_source_transfer_gate.py](../computations/verify_uniform_bezout_transvectant_source_transfer_gate.py)
audits over exact rationals for $3\leq h\leq9$:

* the nonzero pure-axis transvectant coefficient $(h!)^2$;
* the invertible pure-axis Bezout anti-identity;
* Barnett's identity $B(f,e)=M_{\bar e}B(f,1)$;
* nullity equal to the monomial gcd degree;
* a literal shared-root evaluation kernel;
* two singular selected pairs with zero simultaneous kernel;
* the $3$-versus-$h$ type mismatch; and
* nonzero adjugate at corank one but zero adjugate at corank two.

The checker does not model a full Krenn source, construct a physical
$Z_h$, or assert resultant vanishing. It verifies the algebraic interface
and the counterguards used to isolate the missing theorem.
