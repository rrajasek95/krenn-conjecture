# Complementary rows kill the unary guard's concentrated shore but leave a deconcentrated packet

## 1. Outcome

Work at the first \(8\to6\) pair-cap boundary.  Suppose a canonical
diagonal line has a clean unary coordinate point \(K_0=E_{00}\), and
also retain the complete physical equation at its scalar-zero point.  If
the scalar-zero point is the binary boundary

\[
                         K_1=E_{00}-I,                         \tag{1}
\]

then the additional row makes genuine progress, but does not by itself
finish the curved branch.

There are three exact conclusions.

1. A scalar-zero response supported on one residual physical pair cannot
   produce a binary or ternary target.  This is a one-line Schmidt-rank
   obstruction.  It excludes the padding mechanism of
   [the two-chart unary guard](curved-n8-two-chart-unary-root-guard.md)
   even if arbitrary cells are added strictly inside its four-site
   transverse core.
2. A full scalar-zero binary row is nevertheless compatible with
   injective three-row endpoint stars and with cleanliness.  Section 5
   gives a six-site packet with
   \(Rq^{[2]}=-(X_1+X_2)\) and \(R^{[3]}=0\).  Thus the extra row forces
   the response to spread across more than one residual pair; it does not
   force an active clean point by rank alone.
3. Joining the clean unary point to a clean scalar-zero binary point
   leaves exactly two tensors
   \(\Omega_0,\Omega_1\).  An active point exists unless these tensors are
   independent or exactly one vanishes.  Across two curved charts, the
   remaining theorem is therefore to exclude those two residual patterns
   simultaneously using the shared colour-zero curvature data.

So the audited guard cannot be extended without changing its sparse star
shore, but no contradiction has yet been proved for the deconcentrated
case.  The complementary row converts the problem from “more Bianchi
algebra” into one precise incidence question: can the two scalar-zero
responses spread to different residual pairs while remaining compatible
with the two clean unary quadratics and \(AU-BF\ne0\)?

## 2. Exact interpolation from the unary root to scalar zero

Let \(q\) be the internal quadratic on the six residual sites.  For a
pair covector \(K\), write

\[
 s=s(K),\qquad r=r(K),\qquad F=sq+r,
\]

and let \(T(K)\) be its target row.  The complete physical and clean
equations are

\[
 sq^{[3]}+rq^{[2]}=T,
 \qquad
 \mathcal E(K)=F^{[3]}-s^2T.                           \tag{2}
\]

Take a clean unary point \(K_0\) with data

\[
 s_0=\sigma\ne0,\qquad F_0=\sigma q+r_0,\qquad
 F_0^{[3]}=\sigma^2T_0,                                \tag{3}
\]

and a scalar-zero point \(K_1\) with

\[
 s_1=0,\qquad F_1=R,\qquad Rq^{[2]}=T_1.             \tag{4}
\]

On the homogeneous joining pencil \(tK_0+uK_1\), divided-power
polarization gives the unconditional identity

\[
\boxed{
 \mathcal E(tK_0+uK_1)
   =t^2u\,\Omega_0+tu^2\,\Omega_1+u^3\,\Omega_2,}       \tag{5}
\]

where

\[
\begin{aligned}
 \Omega_0&=R F_0^{[2]}-\sigma^2T_1
           =R\bigl(\sigma q r_0+r_0^{[2]}\bigr),\\
 \Omega_1&=R^{[2]}F_0,\\
 \Omega_2&=R^{[3]}.
\end{aligned}                                                   \tag{6}
\]

The second expression for \(\Omega_0\) uses the complete scalar-zero row
in (4), not a formal target substitution:

\[
 F_0^{[2]}-\sigma^2q^{[2]}
     =\sigma q r_0+r_0^{[2]}.
\]

Formula (5) is also the polarization of

\[
                         6\mathcal E=r^2(r+3sq),         \tag{7}
\]

so it retains the actual common internal quadratic.

If the scalar-zero point is clean, then \(\Omega_2=R^{[3]}=0\), and

\[
 \boxed{
 \mathcal E(tK_0+uK_1)=tu(t\Omega_0+u\Omega_1).}         \tag{8}
\]

For the special boundary (1), the target coordinates of the joining
covector are

\[
                         (\kappa_0,\kappa_1,\kappa_2)
                              =(t,-u,-u),               \tag{9}
\]

and its direct scalar is \(t\sigma\).  Thus every point with \(tu\ne0\)
is active.  Equation (8) yields an exact classification:

* if \(\Omega_0,\Omega_1\) are nonzero and dependent, their unique
  residual kernel has \(tu\ne0\), and it is an active clean cap;
* if both vanish, the whole pencil is clean and has active points;
* absence of an active clean point forces either
  \(\Omega_0\wedge\Omega_1\ne0\), or exactly one of
  \(\Omega_0,\Omega_1\) to vanish.

This is the precise residual left by adding a *clean* complementary row.
If the scalar-zero row is only physical and \(R^{[3]}\ne0\), the quadratic
packet in (5) remains; the physical equation alone does not create a
second clean root.

There is a parallel distinction when the binary boundary \(E_{00}-I\)
is not scalar-zero.  Its complete physical equation alone supplies no
second factor of the clean error.  If that binary point is additionally
clean, the general two-root polarization theorem applies, but a residual
kernel may still lie on the separate direct-scalar zero.  Consequently
“one more physical row” and “one more clean root” must not be conflated.

## 3. Scalar-zero shore-rank lemma

The full complementary row immediately removes the sharp concentration
used by the unary guard.

**Lemma 3.1 (one-pair response cannot carry two target colours).**  Let
\(W\) have \(2h\) sites with \(h\geq2\), let \(x,y\in W\), and suppose a
scalar-zero cap
satisfies

\[
                         Rq^{[h-1]}=T,
 \qquad
 T=\sum_{c\in C}\kappa_cX_c,\qquad\kappa_c\ne0.       \tag{10}
\]

If \(|C|\ge2\), then \(R\) is not supported entirely in
\(V_x\otimes V_y\) for one residual pair \(xy\).

**Proof.**  If \(R\in V_x\otimes V_y\), every term of \(q^{[h-1]}\)
using \(x\) or \(y\) collides with \(R\).  Hence

\[
 Rq^{[h-1]}
   =R\otimes
      \left(q|_{W\setminus\{x,y\}}\right)^{[h-1]}.      \tag{11}
\]

Across the flattening

\[
 (V_x\otimes V_y)\ \bigm|\
       \bigotimes_{z\in W\setminus\{x,y\}}V_z,
\]

the tensor in (11) has rank at most one.  The target in (10) has rank
\(|C|\): its left factors
\(e_c^{(x)}e_c^{(y)}\) and right factors
\(e_c^{\otimes(W\setminus\{x,y\})}\) are separately independent.  This
is impossible when \(|C|\ge2\).  \(\square\)

The lemma allows arbitrary cancellation inside \(R\), arbitrary block
rank in \(q\), and endpoint asymmetry.  It concerns the complete aggregate
response, not one selected product of star entries.

A useful star-map corollary is immediate.  Suppose the rows of the first
endpoint selected by a rank-two diagonal covector are all supported at one
residual site \(x\), while the corresponding rows of the second endpoint
are all supported at one residual site \(y\).  Then their contracted
response lies in \(V_x\otimes V_y\), so they cannot satisfy a binary
scalar-zero target.  Therefore the complementary row forces at least one
of those endpoint-row packets to propagate to another residual site.

## 4. Why the audited unary guard cannot be repaired internally

Use the cells and labels of the audited guard.  In the \(pq\)-chart, the
binary boundary is also scalar-zero because the only direct diagonal cell
is \(A_{pq}(0,0)=1\).  Its response is

\[
 R_{pq}
   =-e_1^{(r)}e_1^{(s)}-e_2^{(r)}e_2^{(s)}.             \tag{12}
\]

After \(r,s\) are occupied, the internal quadratic has only the matching
\(uv\mid wx\), of weight \(1/2\).  Thus the actual physical left side is

\[
 R_{pq}q_{pq}^{[2]}
  =-{1\over2}
   \left(e_1^{(r)}e_1^{(s)}+e_2^{(r)}e_2^{(s)}\right)
      e_0^{(u)}e_0^{(v)}e_0^{(w)}e_0^{(x)},             \tag{13}
\]

not \(-X_1-X_2\).  The \(pr\)-chart gives the same formula with the
left pair \(q,s\).

More strongly, no change confined to blocks on
\(D=\{u,v,w,x\}\) can repair either equation while the padding star rows
are retained.  Such a change merely replaces the common four-site factor
in (13) by another tensor \(Q_D\), leaving

\[
 R_{pq}\otimes Q_D.
\]

This has rank one across \(rs\mid D\), whereas the desired binary target
has rank two.  Hence the extra complementary row necessarily changes an
incident colour-1 or colour-2 block and destroys the guard's concentrated
padding shore.  Adding more transverse matching cells alone is futile.

Notice also that \(R_{pq}^{[2]}=0\), because both displayed summands use
the same physical sites \(r,s\).  The formal scalar-zero clean error of
the old packet therefore vanishes.  Its failure is exactly the missing
physical target row, not cleanliness.  This separates the two notions
which the guard was designed to distinguish.

## 5. A sharp deconcentrated scalar-zero packet

Lemma 3.1 is sharp: spreading the two colours over two different residual
pairs is enough to realize the complete binary row with injective ternary
stars.

Let the six residual sites be \(a,b,c,d,e,f\).  Use only the following
internal quadratic cells:

\[
 q=e_1^{(b)}e_1^{(c)}+e_1^{(e)}e_1^{(f)}
   +e_2^{(a)}e_2^{(b)}+e_2^{(d)}e_2^{(e)}.              \tag{14}
\]

Choose endpoint-star rows

\[
\begin{array}{c|ccc}
 &0&1&2\\ \hline
 p&e_0^{(b)}&e_1^{(a)}&e_2^{(c)}\\
 q&e_0^{(e)}&e_1^{(d)}&e_2^{(f)}.
\end{array}                                                   \tag{15}
\]

Both three-row maps are injective.  At \(K_1=E_{00}-I\), the direct
scalar can be set to zero and the response is

\[
 R=-e_1^{(a)}e_1^{(d)}-e_2^{(c)}e_2^{(f)}.              \tag{16}
\]

There are four disjoint-edge products in \(q^{[2]}\).  The two pure ones
are

\[
 (bc)_1(ef)_1,\qquad (ab)_2(de)_2.                    \tag{17}
\]

The mixed products are \((bc)_1(de)_2\) and
\((ef)_1(ab)_2\).  The first meets the colour-1 response edge at \(d\)
and the colour-2 response edge at \(c\); the second meets them at \(a\)
and \(f\), respectively.  All mixed products therefore vanish after
multiplication by \(R\), while the two pure products give

\[
                         Rq^{[2]}=-X_1-X_2.              \tag{18}
\]

The two response edges in (16) are disjoint, so \(R^{[2]}\ne0\), but
there are only two of them and

\[
                              R^{[3]}=0.                 \tag{19}
\]

Thus this scalar-zero point is clean.  The example retains literal
endpoint-star factorization and full rank three at both endpoints.  It is
not a full pair system: it does not supply the clean unary row or all nine
target equations.  Its purpose is exact—it proves that the complementary
row plus star injectivity cannot by itself yield a contradiction or force
the scalar-zero point dirty.

There is also no contradiction in overlapping scalar-zero packets alone.
An eight-cycle whose alternating one-factors carry colours 1 and 2 has
exact output \(X_1+X_2\).  Choose one site \(p\) and two non-neighbours
\(q,r\).  At both pairs \(pq,pr\), the covector \(-I\) has zero direct
scalar, the complete binary physical row, two independent endpoint-star
rows, and a response consisting of two edges, hence cube zero.  What is
missing from this binary model is precisely the colour-zero unary root and
the nonzero colour-zero curvature minor.

## 6. The remaining two-chart lemma

The complementary row therefore removes the old guard but leaves a
smaller, genuinely ternary coupling problem.  For each of the two
overlapping diagonal charts one has:

\[
\begin{array}{c}
 \text{a clean unary quadratic }F_0,\\
 \text{a deconcentrated scalar-zero response }R
       \text{ with }Rq^{[2]}=T_1,\\
 \text{and the residual tensors }\Omega_0,\Omega_1
       \text{ of (6).}
\end{array}                                                    \tag{20}
\]

The colour-zero charts still share the literal four-cut \((L,M)\) packet
and satisfy \(AU-BF\ne0\).  The scalar-zero shore lemma guarantees that
the two complementary star rows cannot remain on the one physical pair
used by the old padding.  It does not say where the new support goes, and
the deconcentrated packet shows that propagation by itself is consistent.

A sufficient next theorem is now sharply stated:

> For two overlapping source-provenant charts with \(AU-BF\ne0\), the
> deconcentrated responses forced by their complete scalar-zero rows cannot
> make both pairs \((\Omega_0,\Omega_1)\) independent or endpoint-degenerate.

If this holds, (8)--(9) give an active clean point on at least one line.
An alternative closure may prove that the forced propagation creates a
literal two-site star support or a rank-one five-site restriction at a
neighbour, feeding the already isolated sparse-star branch.

This note does not prove that final coupling theorem.  It does prove that
interior repairs of the known guard are impossible, exhibits the smallest
surviving scalar-zero response geometry, and reduces the next step to two
explicit polarization tensors rather than an arbitrary vector cubic.
