# Independent audit: the rootless curved-line Macaulay packet

## 1. Verdict

**PASS, with three prose/scope repairs and no displayed-equation repair.**  The
divided-power elimination, scalar-zero specialization, binary-cubic
Macaulay criterion, fixed-cut regrouping, Hall--Rado selector dichotomy,
and final source-realization scope claim in
[the primary note](curved-no-root-macaulay-and-scalar-zero-packet.md) are
correct over \(\mathbb C\).  At audit time the primary file had SHA-256

```text
286da1c0be65d9bbb3349719278346d78b4cb78411632e5ab61e49a79f9ea1b8  notes/curved-no-root-macaulay-and-scalar-zero-packet.md
```

The three repairs are matters of exact logic, terminology, and scope.

1. Under the gcd-one hypothesis, the scalar-zero packet **and** the
   rank-six Macaulay certificate both occur.  Independently, each endpoint
   has a selector **or** a sparse shore.  Thus the box in (3) should read
   “packet and minor, together with selector or sparse concentration,”
   rather than presenting the three objects as one disjunction.  Theorem
   7.1 already states the stronger logic correctly.
2. The Macaulay matrix has six target rows.  A witnessing \(6\times6\)
   minor chooses six shifted **columns**, drawn from at most six scalar
   coordinate cubics.  Phrases such as “six shifted rows” should be
   changed to “six shifted columns from at most six coefficient rows.”
   This does not change the bounded certificate.
3. The outcome's assertion that the cubic packet and rank-six certificate
   are “stable ... under embedding the six-site packet as a transverse
   boundary of a higher-order cap” is not established by the note and
   should be deleted or qualified as a proposed continuation.  At general
   order the clean error has degree \(h\) and its Macaulay/Sylvester rank
   is \(2h\), not six.  Contracting extra residual sites does not, without
   an additional coefficient-factorization lemma, preserve gcd one or
   produce the literal cubic four-cut ledger.  Section 8 below records the
   valid uniform statement.

It would also be useful to say explicitly in Theorem 7.1(1) that the
diagonal case uses the modified right side displayed after (16), not the
off-diagonal right side in (15).  The surrounding text already makes this
unambiguous.

## 2. Pair equation and divided-power normalization

Let \(W\) have six sites.  In the site-square-zero commutative algebra,
\(q\) and \(r=\sum K_{ij}p_i s_j\) have degree two.  Sorting a full
matching according to whether it uses the deleted physical pair gives,
with no multiplicity loss,

\[
 a_{ij}q^{[3]}+p_i s_jq^{[2]}=\delta_{ij}X_i.
\]

The product \(p_i s_j\) retains the two endpoint roles: an edge from the
first endpoint and an edge from the second endpoint are ordered by their
physical endpoints, even though the residual algebra is commutative.
Collisions at one residual site vanish in the site-square-zero algebra.
Thus there is no missing factor of two.

After contraction by \(K\), put \(s=s(K)\), \(r=r(K)\), and \(F=sq+r\).
The physical equation is

\[
                         sq^{[3]}+rq^{[2]}=T.
\]

Divided-power polarization gives

\[
 (sq+r)^{[3]}
 =s^3q^{[3]}+s^2rq^{[2]}+sqr^{[2]}+r^{[3]}.
\]

Subtracting \(s^2T\) cancels the first two terms exactly.  Hence

\[
 \mathcal E=sqr^{[2]}+r^{[3]}
          ={r^2(r+3sq)\over6}.
\]

The ordinary-power display is legitimate because \(q,r\) have even
degree and \(r^{[j]}=r^j/j!\) in characteristic zero.  It is not an
identity in an unrestricted polynomial algebra; it is the compact form of
the preceding divided-power identity in the square-zero site algebra.
At \(s=0\), it gives \({\cal E}=r^{[3]}\) with no division by \(s\).

An equivalent normalization check uses

\[
 Fq^{[2]}-2sq^{[3]}=T,
\]

since \(q q^{[2]}=3q^{[3]}\).  This is exactly the physical row used in
the later four-cut formula.

## 3. Scalar-zero cap and all matrix edge cases

On the canonical line \(K(u,v)=uE_{ab}+vI\),

\[
 s(K(u,v))=\alpha u+\tau v,
 \qquad \alpha=a_{ab}\ne0,
 \qquad \tau=\operatorname{tr}a.
\]

Thus \(s\) is not the zero polynomial, even when \(\tau=0\), and its
unique projective zero is

\[
                  [u:v]=[\tau:-\alpha],\qquad
                  K_*=\tau E_{ab}-\alpha I.
\]

This cap covector is never zero because \(\alpha\ne0\).

If \(a\ne b\), \(E_{ab}^2=0\), every diagonal entry of \(K_*\) is
\(-\alpha\), and the matrix-determinant lemma (or a triangular basis)
gives

\[
             \det K_*=(-\alpha)^3,
             \qquad T(K_*)=-\alpha\Delta_{6,3}.
\]

The physical and clean equations at this point are therefore

\[
 r_*q^{[2]}=-\alpha\Delta_{6,3},
 \qquad \mathcal E(K_*)=r_*^{[3]}.
\]

Gcd one means that the vector cubic has no projective zero, so the second
tensor is nonzero.  This proves (15), including the trace-zero case
\(K_*=-\alpha I\).

If \(a=b\), the three diagonal entries are \(\tau-\alpha,-\alpha,-\alpha\).
Thus

\[
 \det K_*=(\tau-\alpha)(-\alpha)^2,
 \qquad
 T(K_*)=(\tau-\alpha)X_a-\alpha\sum_{c\ne a}X_c.
\]

There is exactly one degeneracy equation, \(\tau=\alpha\).  Off that
hyperplane the cap and target are ternary and the cap matrix is invertible;
on it the cap has rank two and the target is exactly binary.  In both
cases gcd one still gives \(r_*^{[3]}\ne0\).

No symmetry of the endpoint-ordered block \(a\) was used.  Transposing the
physical pair changes which coordinate is called \(a_{ab}\) and transposes
the cap covector, but preserves the scalar contraction, determinant, and
target-diagonal calculation.  Parallel decorated sources have already
been summed into the aggregate entries and therefore cause no additional
terms.

Invertibility of \(K_*\) has only the factor-level meaning asserted in the
note: it gives a nondegenerate coefficient pairing between the two
independent star triples.  It does **not** imply that an arbitrary choice
of disjoint selector bases has a nonzero commutative permanent.  The
nonnilpotence \(r_*^{[3]}\ne0\) comes from gcd one, not from
\(\det K_*\ne0\).  No later proof step makes the forbidden
determinant-to-permanent inference.

## 4. Gcd, Macaulay rank, and resultant

Let \(L\) be the span of the scalar coordinate cubics.  A common
projective zero on \(\mathbb P^1_\mathbb C\) is equivalent to a common
linear factor, hence to a positive-degree gcd.  This proves the first
equivalence in Lemma 4.1.

If a common factor \(\ell\) exists, then

\[
 L\operatorname{Sym}^2\mathbb C^2
      \subseteq \ell\operatorname{Sym}^4\mathbb C^2,
\]

whose dimension is five, so the multiplication map cannot have rank six.
Conversely, take nonzero \(f\in L\).  At each of its at most three
distinct projective roots, gcd one supplies a member of \(L\) which does
not vanish.  A linear combination outside the finite union of the
corresponding hyperplanes gives \(g\in L\) with \(\gcd(f,g)=1\).

If \(fh=gk\) with \(h,k\) quadratic, coprimality implies \(f\mid k\).
Since \(\deg k<\deg f\), both sides vanish.  Therefore

\[
 f\operatorname{Sym}^2\mathbb C^2
 \oplus g\operatorname{Sym}^2\mathbb C^2
       =\operatorname{Sym}^5\mathbb C^2.
\]

The direct-sum multiplication matrix is the ordinary cubic Sylvester
matrix, so its determinant is the classical resultant.  This proves all
four equivalences without a genericity hypothesis.

Multiplication of
\(c_0u^3+c_1u^2v+c_2uv^2+c_3v^3\) by \(u^2,uv,v^2\) gives exactly the
three columns in (22).  Hence the displayed Toeplitz normalization is
correct.  A nonzero maximal minor selects six of these shifted columns.
Those columns can originate in at most six coordinate cubics; applying
the same lemma to their span shows that two linear combinations of that
bounded subset already have nonzero resultant.

## 5. Literal four-cut regrouping

Fix residual sites \(x,y\), endpoint colours \(c,d\), and put
\(D=W\setminus\{x,y\}\).  Suppress all rows other than the selected
\((c,d)\)-coefficient and write

\[
 \begin{aligned}
 q&=z+e_xt+e_yv+e_xe_yU+\cdots,\\
 F&=f+e_xL+e_yH+e_xe_yM+\cdots.
 \end{aligned}
\]

In the two site markers, direct expansion gives

\[
 \begin{aligned}
 [e_xe_y]q^{[2]}&=Uz+tv,\\
 [e_xe_y]q^{[3]}&=Uz^{[2]}+tvz,\\
 [e_xe_y](Fq^{[2]})
   &=Mz^{[2]}+(Lv+Ht+fU)z+ftv,\\
 [e_xe_y]F^{[3]}&=Mf^{[2]}+LHf.
 \end{aligned}
\]

Combining the middle two identities with
\(Fq^{[2]}-2sq^{[3]}=T\) gives (24) exactly, including the coefficient
\(-2s\).  The last identity gives (25).  Thus the selected coefficient of
the unconditional clean error is

\[
 \epsilon_{cd}=C_{cd}-s^2P_{cd}.
\]

Here \(P_{cd}\) is the *complete physical row*, equal to the selected
target coefficient by (4); it is not one chosen matching monomial.
Therefore the target cancels without discarding cancellation terms.

For a fixed cut, every word on \(W\) has a unique decomposition into its
colour \(c\) at \(x\), colour \(d\) at \(y\), and word \(\omega\) on
the four sites of \(D\).  Conversely every triple \((c,d,\omega)\) is one
word on \(W\).  The 729 scalar cubics are consequently only permuted by
this regrouping.  Their span, gcd, and Macaulay rank are unchanged.  This
proves the “for every fixed cut” quantifier in Corollary 5.1, including
off-diagonal \(c\ne d\) rows whose physical target is zero.

## 6. Hall--Rado selector dichotomy

For the component \(\Psi_x:\mathbb C^3\to V_x\), let

\[
 L_x=\operatorname{im}(\Psi_x^*:V_x^*\to(\mathbb C^3)^*).
\]

Injectivity of \(\Psi\) is equivalent to
\(\sum_xL_x=(\mathbb C^3)^*\).  The rank form of Rado's theorem says that
the maximum size of an independent partial transversal from the six
subspaces is

\[
 \min_{J\subseteq W}
      \left(\dim\sum_{x\in J}L_x+|W\setminus J|\right).
\]

Thus a three-site independent transversal fails exactly when this number
is at most two for some \(J\).  If the complement of \(J\) has at least
three sites, the cardinality term alone is at least three.  If \(J=W\),
the dimension term is three.  The only possibilities are therefore

\[
 \begin{array}{c|c|c}
 |J|&|W\setminus J|&\dim\sum_{x\in J}L_x\\ \hline
 4&2&0,\\
 5&1&\le1.
 \end{array}
\]

The first says all components on four sites vanish, so \(\Psi\) is
supported on at most two sites.  The second says that away from the one
exceptional site, the restricted map has rank at most one.  Conversely,
either condition allows at most two independent representatives from
distinct sites.  Lemma 6.1 is therefore exact.

If selector sites \(x,y,z\) exist, the dual row space on \(x,y\) has rank
at least two, and adding the four-site complement containing \(z\) raises
the combined row space to rank three.  This only chooses a useful cut.
It does not force the six columns of a nonzero Macaulay minor to use any
of these selector coordinate rows, exactly as the primary note warns.

## 7. Incidence and final scope

The full nine equations, including the direct term \(a_{ij}q^{[3]}\), do
indeed imply the cited six-site four-cover and site-cover.  This is the
\(m=3\) case of the audited full-nine target-incidence theorem, whose proof
retains the common direct term rather than applying the direct-free
response theorem incorrectly.  This incidence statement is contextual
and is not needed to prove Theorem 7.1.

The last source-realization paragraph is also exact.  Given a physical
quadratic \(q\), linear star rows \(p_i,s_j\), and direct entries
\(a_{ij}\), add two named sites and use those data as their internal,
incident, and direct aggregate blocks.  For a fixed colour pair \((i,j)\)
at the two new sites, every perfect matching either uses their direct edge,
giving \(a_{ij}q^{[3]}\), or uses one star edge from each, giving
\(p_i s_jq^{[2]}\).  These two cases are disjoint and exhaustive.
Therefore all nine equations (4) are exactly all colour coefficients of
the resulting eight-site tensor.  A physical solution of the complete
six-site transverse system would already be an eight-site Krenn
counterexample.  Formal guards which omit a row or source provenance do
not contradict this scope statement.

The correct logical package under the hypotheses of Theorem 7.1 is

\[
 \boxed{
 \begin{gathered}
 \text{nonnilpotent scalar-zero packet}\quad\mathbf{and}\quad
 \text{rank-six Macaulay certificate on every cut},\\
 \text{together with, at each endpoint,}\quad
 \text{selector}\quad\mathbf{or}\quad\text{sparse shore}.
 \end{gathered}}
\]

No positivity, symmetry, termwise noncancellation, or generic-rank
assumption is hidden in this package.

## 8. Uniform extension

The apparent all-order extension is valid.  On \(2h\) residual sites the
physical and clean equations are

\[
 sq^{[h]}+rq^{[h-1]}=T,
 \qquad
 \mathcal E=(sq+r)^{[h]}-s^{h-1}T.
\]

Divided-power expansion cancels the \(j=0,1\) terms and gives

\[
 \boxed{{\cal E}
   =\sum_{j=2}^{h}s^{h-j}q^{[h-j]}r^{[j]}.}
\]

On a physical projective line this is a vector-valued binary form of
degree \(h\).  If \(L\subseteq\operatorname{Sym}^h\mathbb C^2\) is the
span of its scalar coordinates, the same proof as in Section 4 gives

\[
 \text{gcd one}
 \Longleftrightarrow
 L\operatorname{Sym}^{h-1}\mathbb C^2
       =\operatorname{Sym}^{2h-1}\mathbb C^2
 \Longleftrightarrow
 \operatorname{rank}\mu=2h.
\]

Indeed, two coprime degree-\(h\) combinations have two
\(h\)-dimensional multiplication images with zero intersection, while a
common linear factor confines the image to dimension \(2h-1\).  The same
two combinations have nonzero degree-\(h\) resultant.  At the canonical
scalar-zero cap, rootlessness likewise forces \(r_*^{[h]}\ne0\), with
\(r_*q^{[h-1]}=T(K_*)\).  What does not extend automatically is the
specific six-row/four-site ledger: at general \(h\) its Macaulay matrix
has \(2h\) rows and the transverse coefficient bookkeeping must be stated
at the corresponding order.

## 9. Repair disposition

The primary note was repaired after this audit: (3) now has the required
packet-and-minor/selector-or-sparse logic, maximal minors are described by
their shifted columns, the diagonal target qualification is explicit, and
the unsupported higher-order contraction claim was replaced by a link to
the uniform rank-\(2h\) theorem.  The repaired primary has SHA-256

    2edbdae83d1c1b3f80184d37dbb2052a4079dae3376f21f8cf426edbe4e50f26  notes/curved-no-root-macaulay-and-scalar-zero-packet.md
