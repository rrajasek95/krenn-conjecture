# Independent audit: selector--Macaulay jets and cross-word Riccati leakage

## 1. Verdict and scope

This is an independent algebraic audit of

* `selector-macaulay-double-jet-and-offdiagonal-hexagon.md`, SHA-256
  `2070f6c05c12701378c8fb30e1612d337fb95a8569a79a1779fda299f48983a1`;
* `cross-word-selector-riccati-leakage-guard.md`, SHA-256
  `c5133a158c3caf75b82b536801e3119c790a9b13dd6021099bd424f89848d0fd`.

Both notes pass.  I found no sign, transpose, divided-power, rank, or
fixed-block error.  Their guards have exactly the limitations stated in
the notes: the first omits the three diagonal target rows, and the second
is a fixed-block identity only on one mixed probe line, not an all-probe
ternary source.

One scope qualification is important.  Proposition 5.3 of the first note
does **not** show that every argument using selector jets is impossible.
It shows the precise narrower statement that selector-exposure
divisibility, by itself, cannot contradict rootlessness: the nonzero
scalar-zero coefficient automatically fills the resulting jet quotient.
A selector argument coupled to a literal diagonal coefficient row remains
live and is exactly the residual isolated by the note.

## 2. Audit of the selector--Macaulay reduction

### 2.1 Normalization and fixed labels

The normalization

\[
 B_{ij}=p_i s_j+\frac{a_{ij}}h q
\]

is exact because \(q q^{[h-1]}=h q^{[h]}\).  Hence

\[
 B_{ij}q^{[h-1]}=\delta_{ij}X_i.
\]

After independent row changes \(R,S\in\mathrm{GL}_3\), direct expansion
gives

\[
 \widetilde B_{kl}=\sum_{ij}R_{ki}S_{lj}B_{ij},\qquad
 \widetilde B_{kl}q^{[h-1]}
   =\sum_iR_{ki}S_{li}X_i.
\]

The three \(X_i\) are independent, so a transformed cell is an
annihilator exactly when \(R_{ki}S_{li}=0\) for every \(i\).  No common
power was cancelled in this deduction.

### 2.2 No rectangle and uniqueness of the hexagon

If \(U\otimes V\) lies in the zero-diagonal subspace of
\(\mathbb C^3\otimes\mathbb C^3\), the coordinate supports of \(U\) and
\(V\) are disjoint.  Thus

\[
 \dim U+\dim V\leq |I(U)|+|I(V)|\leq3,
\]

which excludes a \(2\)-by-\(2\) product rectangle after any independent
selector changes.  Formula (12) in the source note correctly identifies
the missing part of an attempted oblique product as the diagonal channel.

The six off-diagonal cells form the edge set of
\(K_{3,3}\setminus\{00,11,22\}\), which is one connected six-cycle.  Its
integer incidence kernel has rank
\(6-(6-1)=1\), generated primitively by the alternating cycle vector.
Therefore its toric ideal is principal, with binomial

\[
 (p_0s_1)(p_1s_2)(p_2s_0)
 -(p_0s_2)(p_2s_1)(p_1s_0).
\]

Replacing \(p_i s_j\) by \(B_{ij}-b_{ij}q\) proves the displayed hexagon
identity exactly.  This verifies the claimed uniqueness only in the
properly stated support-free/formal Segre sense; site-incidence and
top-degree relations can add further identities, as the note explicitly
allows.

### 2.3 Exposure divisibility and rank count

For \(x\in A\), quotienting by

\[
 U_x=\operatorname{span}\{p_{0,x},p_{1,x},p_{2,x},
 s_{0,x},s_{1,x},s_{2,x}\}
\]

kills every response edge incident with \(x\).  In a nonzero top-degree
monomial of \(q^{[k]}r^{[h-k]}\), all \(t=|A|\) quotient sites must
therefore be covered by the \(k\) internal \(q\)-edges.  Since those edges
cover at most \(2k\) such sites, the term vanishes for
\(k<d=\lceil t/2\rceil\).  Reindexing the target-free clean-error formula
then gives

\[
 \Pi_A\mathcal E=\sigma^dG.
\]

This also verifies the zero conclusion when \(d>h-2\), because the clean
error contains only \(0\leq k\leq h-2\).  The use of the combined \(P,S\)
span is essential and correct.

For a three-site selector \(d=2\).  Multiplication of the unexposed
degree-\(h\) coordinates by degree \(h-1\) forms lands in

\[
 \sigma^2\operatorname{Sym}^{2h-3}\mathbb C^2,
\]

which has dimension \(2h-2\).  Thus every rank-\(2h\) minor needs at least
two exposed columns, and full rank forces their images to span the
two-dimensional quotient \(J_2\).  The same calculation gives dimension
\(2h-d\) and a required \(d\) exposed columns for \(J_d\).  At \(h=3\),
\(d=2>h-2\), so the unexposed clean error is indeed zero.

### 2.4 Proposition 5.3

At the scalar-zero point, divisibility gives
\(\Pi_A\mathcal E(K_*)=0\).  Since
\(\mathcal E(K_*)=r_*^{[h]}\neq0\), an adapted exposed coordinate \(f\)
has \(f(K_*)\neq0\).  Choose a linear form \(t\) independent of
\(\sigma\).  Modulo \(\sigma^d\), the \(d\) columns

\[
 f\sigma^kt^{h-1-k},\qquad 0\leq k<d,
\]

have successive \(\sigma\)-orders \(0,\ldots,d-1\), with nonzero leading
coefficients.  They are a triangular basis of \(J_d\).  This proves the
proposition for every \(d\leq h\).

The sharp model is also correct.  The unexposed image has dimension
\(2h-d\); the intersection of
\(t^h\operatorname{Sym}^{h-1}\) with it is

\[
 \sigma^dt^h\operatorname{Sym}^{h-d-1},
\]

of dimension \(h-d\).  The sum therefore has dimension \(2h\).

Finally, for \(f(K_*)\neq0\), one has \(\gcd(f,\sigma)=1\).  Hence
\(f\mid\sigma^dg\) implies \(f\mid g\), proving injectivity of (37); both
sides have dimension \(h\), proving the asserted isomorphism and the
dimension-\(h\) residual quotient.

### 2.5 Six-row guard

The local \(Z_k^*\) contractions in (28)--(29) return
\(\delta_{ik}\) and \(\delta_{jk}\), so both displayed stars really have
fixed-label three-site selectors.  On the all-\(U\) mixed coordinate, all
\(A\)-rows equal label \(0\), all \(B\)-rows equal label \(1\), and the
response cross matrix is the \(3\)-by-\(3\) all-\(u\) matrix.  Its
permanent is \(3!u^3\).  On the all-\(V\) coordinate both shores have label
\(2\), giving \(3!v^3\).  Both target coordinates vanish because the
physical words are mixed.  Thus the clean-error coordinates are coprime
and the cubic Macaulay map has rank six.

With \(q=0\), all six off-diagonal pair rows vanish identically and the
hexagon holds by commutativity.  The three diagonal equations are exactly
what fail.  The example therefore guards the stated six-row implication
and nothing stronger.

## 3. Audit of the Riccati--leakage reduction

### 3.1 Flag test and normalization

A rank-one diagonal matrix occupies one coordinate diagonal cell.  Thus

\[
 A^{-\mathsf T}\operatorname{Diag}_3B^{-1}
   =\operatorname{Diag}_3
\]

forces corresponding columns of \(A^{-\mathsf T}\) and \(B^{-\mathsf T}\)
onto the same three coordinate axes, once each.  This is equivalent to
\(A,B\) being monomial with the same permutation; the converse is direct.

At a separating coordinate selector, the normalized entry

\[
 \widehat H_{ij}=(A^{-\mathsf T}P^{\mathsf T}HSB^{-1})_{ij}
\]

is the literal physical cofactor \(H_{x_i y_j}\) at the base point.  The
normalization of the full-nine equation is therefore exact and retains
the fixed direct block through
\(C=A^{-\mathsf T}aB^{-1}\).

### 3.2 Riccati--leakage identity

At a mixed base point, \(D=0\), \(A=B=I\), and \(C=a\), so

\[
 H_{x_a y_b}=-F\alpha.
\]

An own-edge lift has \(\xi F=H_{x_a y_b}\).  The cofactor deletes its own
edge, hence \(\xi H_{x_a y_b}=0\).  Also
\(\xi\widehat D=0\): the base target is zero, so normalization derivatives
multiply zero, while \(dG_c(\xi)=0\).  Differentiating the normalized
entry gives

\[
 \Lambda_{ab}=-(\xi F)\alpha-F\xi C_{ab}
   =F(\alpha^2-\xi C_{ab}).
\]

The signs, endpoint order, and absence of a factor two are correct.  At
the coordinate flag,

\[
 \xi C=-(\xi A)^{\mathsf T}a-a(\xi B),
\]

as stated.  If shore separation persists, normalized and physical
cofactors agree, so \(\Lambda_{ab}=0\) and
\(\xi C_{ab}=C_{ab}^2\) at the base point.  If the flag is horizontal,
\(\xi C_{ab}=0\), the leakage is \(F\alpha^2\).  Saturating by
\(F\alpha\) therefore makes the simultaneous equations
\(\Lambda_{ab}=\xi C_{ab}=0\) inconsistent; (38) follows.

The Hall calculation is literal.  The cross-shore response matrix is
\(K_*=\operatorname{tr}(a)E_{ab}-\alpha I\).  A permutation using its
sole off-diagonal cell cannot fill column \(a\), so only the diagonal
permutation survives and its permanent is \((-\alpha)^3\).

### 3.3 Fixed-block guard

Every object in Section 5 comes from a fixed local block.  Varying only
\(u_{x_0}=e_0+te_1\) evaluates the fixed block

\[
 q_{x_0y_1}=(\gamma e_0^*+e_1^*)\otimes e_0^*
\]

as \(\gamma+t\); the other two fixed matching blocks remain \(1\).  No
scalar edge is assigned independently of the probe map.  The three pure
target products vanish identically on the line.

The selector matrices are
\(A=\operatorname{diag}((\gamma+t)/\gamma,1,1)\), \(B=I\).  The internal
hafnian and its only nonzero cofactors are

\[
 F=\gamma+t,\qquad H_{x_0y_1}=1,\quad
 H_{x_1y_0}=H_{x_2y_2}=F.
\]

Direct multiplication gives exactly

\[
 P^{\mathsf T}HS=
 \begin{pmatrix}0&F/\gamma&0\\F&0&0\\0&0&F\end{pmatrix}
 =-Fa,
\]

so all nine mixed entries hold along the line.  With
\(K_*=-E_{01}+\gamma^{-1}I\), the oriented response matrix is \(AK_*\),
whose permanent is \((\gamma+t)/\gamma^4\).  Its tangent contraction is
\(-d+F/\gamma=0\), where \(d=F/\gamma\).

Separation persists, so leakage is zero, while

\[
 C_{01}=-\frac1{\gamma+t},\qquad
 \frac{dC_{01}}{dQ_{x_0y_1}}=\frac1{(\gamma+t)^2}=C_{01}^2.
\]

Thus the guard genuinely realizes flag drift with fixed source blocks,
rank-three endpoint stars, all nine mixed identities, and nonzero Hall
response on \(F\neq0\).  It correctly does not claim the constant-word
anchors or the all-probe identity.

## 4. Common next theorem

The reductions support one common mechanism, but do not yet prove it.
The six off-diagonal labels form a single cycle, so their only
source-index syzygy is the unanchored hexagon.  On a moving mixed selector
chart the same freedom appears geometrically as a one-scalar connection:
the flag can drift according to the Riccati equation and absorb the
would-be cofactor contradiction.  Both guards survive precisely because
the three fixed diagonal target charts are absent.

A natural common target is therefore an **anchored selector-overlap
exactness lemma**: for an actual fixed-block all-probe source, transport a
mixed selector chart to the three constant-word target charts and prove
that one literal diagonal coefficient cut makes the six-cycle cocycle
Koszul-exact.  In the cross-word language this should force both a
horizontal anchored flag \(\xi C_{ab}=0\) and zero cofactor leakage
\(\Lambda_{ab}=0\), contradicting the audited identity on
\(F\alpha\neq0\).  In the Macaulay language the same anchored relation
should lower the image in

\[
 \operatorname{Sym}^{2h-1}\mathbb C^2/
 f\operatorname{Sym}^{h-1}\mathbb C^2
\]

from dimension \(h\) to at most \(h-1\).

This is a genuinely smaller theorem than the conjecture only if it is
formulated with the actual overlap map: fixed source blocks, at least one
literal diagonal target coefficient, and the selector/own-edge chart.
Neither “six off-diagonal rows plus selectors” nor “all nine identities on
one mixed line” is sufficient, by the two exact guards above.
