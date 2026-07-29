# Independent audit of the actual cofactor cap cubic and four-parameter prism barrier

## Verdict

**PASS, with the stated restricted scope.**  A clean-room derivation and a
separate exact implementation confirm

\[
 {\cal D}_{\rm src}(K)=6\bigl(s(K)^2F_U^K-H_6(A^K)\bigr),
\]

the universal two-site factorization, and every coefficient of the genuine
ten-site common-edge construction.  On the displayed four-dimensional cap
slice its coordinate ideal is

\[
 I_{\cal D}=(z_0z_1z_2),\qquad
 h=(z_0+t)z_0z_1z_2\in I_{\cal D},
\]

so \(I_{\cal D}:h^\infty=(1)\).

This construction is **not** a Krenn counterexample and does not satisfy the
global ten-site GHZ equation.  It is a barrier only to the weaker inference
from common-edge realizability, exact GHZ contraction on one cap subspace,
and independence of \(s,\kappa_0,\kappa_1,\kappa_2\).  A positive argument may
still use the omitted transverse cap equations, equivalently the global
large-source identity.

## Frozen inputs and pre-audit correction

The audit was performed against these frozen primary files:

    1d990dcba8ba4d9df23ae07fec37a59494541b969812d96a2ca0e0ca7a105e64  notes/actual-cofactor-cap-cubic-and-four-parameter-prism-barrier.md
    5e03c012921fdb5eb2221813d5c3da4f2f57e1670bf5aee4a8fddd2381d086da  computations/verify_actual_cofactor_cap_cubic_and_four_parameter_prism_barrier.py

Before that snapshot was frozen, equation (19) in the note was missing the
displayed plus sign between its pure and mixed summands.  The primary checker
already used addition and returned the intended tensor.  The typo was fixed,
and this audit applies only to the corrected note hash above.

The independent checker is
[audit_actual_cofactor_cap_cubic_and_four_parameter_prism_barrier_independent.py](../computations/audit_actual_cofactor_cap_cubic_and_four_parameter_prism_barrier_independent.py).
It does not import or reuse the primary enumerator.  Its SHA-256 digest is

    790c2a3bc4b07891cf96181eec6348e380effbd8b999e57be0a9cf0559a7f07a

and its frozen semantic-ledger digest is

    2f33bfcb5be0bab24e61fcf5aeab6e97064fcb53887fe4a48c7e709470c5bd56

## 1. Cofactor cubic

Let \(x\) be the internal boundary quadratic and let \(C_{2j}\) denote the
cut contribution with \(2j\) boundary sites joined across the cut.  Disjoint
internal boundary edges are enumerated by divided powers, so

\[
 F_U^K=C_6+C_4x+\frac12C_2x^2+\frac16sx^3.             \tag{1}
\]

For fixed \(u<v\), a matching of \(W\cup\{u,v\}\) either uses \(uv\), with
coefficient \(s\), or joins both displayed boundary endpoints across the cut.
Summing in boundary endpoint order gives

\[
 \sum_{u<v}A^K_{uv}=sx+C_2.                            \tag{2}
\]

Because this is a degree-two element on six square-free sites,

\[
 H_6(A^K)=\frac16(sx+C_2)^3.                           \tag{3}
\]

Substitution in \(6(s^2F_U^K-H_6(A^K))\) cancels the \(s^3x^3\) and
\(3s^2C_2x^2\) terms and leaves

\[
 6s^2(C_6+C_4x)-3sC_2^2x-C_2^3.                       \tag{4}
\]

Thus the intrinsic common-edge discrepancy is exactly the previously
derived denominator-cleared cap cubic.  If the large source is globally
GHZ, then \(F_U^K=\sum_i\kappa_iX_i\) for every cap \(K\), giving the claimed
source formula.  No division by \(s\) occurs in (1)--(4), so zero scalars and
complex cancellation cause no exceptional case.

## 2. Two-site factorization and endpoint order

For \(W=(p,q)\), at most two boundary sites can cross the cut.  Keeping the
ordered cap coordinates \(K(e_i^{(p)}e_j^{(q)})\), put

\[
 s=K(A_{pq}),\qquad
 r=\sum_{i,j}K(e_i^{(p)}e_j^{(q)})\,\ell_i m_j.
\]

Then

\[
 F_U^K=s\frac{x^3}{6}+r\frac{x^2}{2},\qquad
 \sum_{u<v}A^K_{uv}=sx+r,
\]

and direct expansion gives

\[
 6s^2F_U^K-(sx+r)^3=-r^2(3sx+r).                       \tag{5}
\]

The independent checker tests more than a commutative placeholder identity.
It constructs an asymmetric physical source, inserts several edges through
the reverse endpoint API, and uses the nonsymmetric cap values

\[
 K(0,2)=2,\qquad K(2,0)=-3.
\]

The \(pq\)-block contains \(3e_0^{(p)}e_2^{(q)}\) and
\(7e_2^{(p)}e_0^{(q)}\), so the ordered contraction is

\[
 s=3\cdot2+7\cdot(-3)=-15.
\]

Two independently selected star products have boundary coefficients \(12\)
and \(-105\), respectively; both would change under an accidental cap-index
transpose.  Subset-DP enumeration of the full eight-site tensor, all fifteen
pair cofactors, and their six-site hafnian agrees coefficientwise with both
identities above and with (5).  This also checks collisions at a shared
boundary endpoint in the square-free algebra.

## 3. Exact ten-site source and its cap slice

Use cap order \((p,q,r,s)\).  The two and only two internal capped matchings
give

\[
 pq\mid rs\mapsto(0,0,0,0),\qquad
 pr\mid qs\mapsto(1,2,1,2).
\]

Hence the stated cap evaluates the internal tensor as

\[
 s=z_0+t.
\]

Every supported ten-site matching uses \(rs\), one star edge \(px_i\), one
star edge \(qy_j\), and the two opposite triangle edges.  The independent
subset recurrence therefore obtains exactly the nine ordered words

\[
 (i,j,0,0,i,i,i,j,j,j),\qquad 0\le i,j\le2,            \tag{6}
\]

each with coefficient one.  On (6), the cap vanishes for \(i\ne j\) and is
\(z_i\) for \(i=j\).  Thus, throughout the whole four-parameter cap slice,

\[
 K_{z,t}\mathbin{\lrcorner}H_{10}(A)=\sum_i z_iX_i.    \tag{7}
\]

The cap map has rank four.  In coordinates \((z_0,z_1,z_2,t)\), the active
forms have matrix

\[
 \begin{pmatrix}
 1&0&0&1\\
 1&0&0&0\\
 0&1&0&0\\
 0&0&1&0
 \end{pmatrix},
\]

whose determinant is \(-1\).  Consequently
\(s,\kappa_0,\kappa_1,\kappa_2\) are independent.

The same enumeration is an exact scope check.  Of the nine words in (6),
eight are globally mixed and only the all-zero word is globally pure.  The
global \(X_1\) and \(X_2\) words are absent.  Therefore

\[
 H_{10}(A)\ne\Delta_{10,3},                             \tag{8}
\]

even though every contraction in (7) has the desired GHZ form.

## 4. Cofactors, mixed ideal, and saturation

Computing every \(H_{W\cup\{u,v\}}(A)\) from the same physical edge table and
then applying the cap produces exactly nine nonzero cofactor blocks:

* the six shore-triangle blocks, each multiplied by \(s=z_0+t\); and
* the three spokes \(x_iy_i=z_i e_ie_i\).

There are no other cofactor cells.  In boundary order
\((x_0,x_1,x_2,y_0,y_1,y_2)\), subset-DP hafnian evaluation of this prism gives

\[
 H_6(A^{K_{z,t}})
 =s^2\sum_i z_iX_i+z_0z_1z_2e_{012012}.                \tag{9}
\]

Combining (7) and (9) yields the one nonzero discrepancy coordinate

\[
 {\cal D}_{012012}=-6z_0z_1z_2.                       \tag{10}
\]

All pure coordinates cancel and every other mixed coordinate is zero.
Since \(6\) is a unit over \(\mathbb C\), the full coordinate ideal is

\[
 I_{\cal D}=(z_0z_1z_2).
\]

With \(h=(z_0+t)z_0z_1z_2\), one already has \(h\in I_{\cal D}\), and hence
\(1\in I_{\cal D}:h\).  The checker independently obtains the unit Groebner
basis from the Rabinowitsch ideal

\[
 (z_0z_1z_2,\ 1-u(z_0+t)z_0z_1z_2)=(1).
\]

The active locus is nonempty: at \((z_0,z_1,z_2,t)=(1,1,1,0)\), both \(h\)
and the mixed generator equal one.  Thus the failure is a genuine root cover,
not emptiness of the active open set.

Finally, the universal six-site radical pullback in the primary note is
algebraically consistent.  Modulo the discrepancy ideal it gives

\[
 (s^6\kappa_0\kappa_1\kappa_2)^N\in I_{\cal D}.
\]

Multiplication by
\((\kappa_0\kappa_1\kappa_2)^{5N}\) gives

\[
 (s\kappa_0\kappa_1\kappa_2)^{6N}\in I_{\cal D},
\]

so the saturation is universally the unit ideal for any actual six-site
cofactor family.  A useful contradiction route must therefore show that the
additional *global* large-source GHZ equations force the opposite conclusion.

## Reproduction

From the project root, run

    uv run python computations/audit_actual_cofactor_cap_cubic_and_four_parameter_prism_barrier_independent.py

The frozen output ends with

    independent semantic ledger SHA-256: 2f33bfcb5be0bab24e61fcf5aeab6e97064fcb53887fe4a48c7e709470c5bd56
    two-cap ordered scalar: -15
    ten-site supported/mixed words: 9 8
    active-form determinant: -1
    cap cubic: [['012012', '-6:z0*z1*z2']]
    PASS: independent actual-cofactor prism-barrier audit
