# Independent audit of the uniform rootless-line response resultant

## Verdict

**PASS.**  The divided-power elimination, the all-degree binary-form
Macaulay criterion, and the canonical scalar-zero packet in
[the primary note](curved-rootless-line-uniform-response-resultant.md)
are correct.  The note retains endpoint order and parallel-source
aggregation, and it does not promote the cubic four-cut formula to higher
order.

The audited primary file had SHA-256 digest

    3217de977a32603f9cea691fe71f714052173c78e25cc5b76da8901d819aa098  notes/curved-rootless-line-uniform-response-resultant.md

No load-bearing repair is needed.  For a literally total statement of
Lemma 3.1, it would be helpful to declare the gcd of an identically zero
coordinate family to be zero, equivalently to regard its generated ideal
as the zero ideal.  Under the standard ideal convention this is already
implicit: the zero vector form satisfies neither item 1 nor item 2.

## 1. Divided-power normalization

Let the residual set have \(2h\) sites.  Sorting perfect matchings at the
deleted physical pair gives, with no extra scalar factor,

\[
                  s q^{[h]}+r q^{[h-1]}=T.                       \tag{A1}
\]

The direct-pair sector leaves \(h\) internal edges and hence \(q^{[h]}\).
The cross sector chooses one edge from each deleted endpoint; the ordinary
product of their star forms retains both endpoint assignments, while the
remaining \(h-1\) unordered internal edges give \(q^{[h-1]}\).  Thus (A1)
has the correct normalization even with asymmetric endpoint blocks.

Divided-power polarization gives

\[
 (sq+r)^{[h]}
   =\sum_{j=0}^{h}s^{h-j}q^{[h-j]}r^{[j]}.                       \tag{A2}
\]

Multiplying (A1) by \(s^{h-1}\) gives

\[
 s^{h-1}T=s^hq^{[h]}+s^{h-1}r q^{[h-1]},                        \tag{A3}
\]

which is exactly the \(j=0\) plus \(j=1\) part of (A2).  Therefore

\[
 {\cal E}=(sq+r)^{[h]}-s^{h-1}T
          =\sum_{j=2}^{h}s^{h-j}q^{[h-j]}r^{[j]}.                \tag{A4}
\]

No division by \(s\), factorial, or binomial coefficient is missing.  At
\(s=0\), only \(j=h\) remains, so \({\cal E}=r^{[h]}\).  At \(h=3\),

\[
 {\cal E}=sqr^{[2]}+r^{[3]}
          ={3sqr^2+r^3\over6}
          ={r^2(r+3sq)\over6},                                  \tag{A5}
\]

which verifies the displayed cubic specialization.

## 2. Macaulay/Sylvester equivalence in degree \(h\)

For a \(V\)-valued binary \(h\)-form \(E\), let

\[
 L_E=\{\lambda(E):\lambda\in V^*\}
       \subseteq\operatorname {Sym}^h\mathbb C^2.                \tag{A6}
\]

Changing a tensor-coordinate basis changes neither this subspace nor the
ideal it generates.  A projective point annihilates \(E\) exactly when it
is a common zero of \(L_E\), equivalently when the scalar forms have a
positive-degree gcd over \(\mathbb C\).

If they share a linear factor \(\ell\), then

\[
 L_E\operatorname {Sym}^{h-1}\mathbb C^2
       \subseteq\ell\operatorname {Sym}^{2h-2}\mathbb C^2,       \tag{A7}
\]

whose dimension is \(2h-1\), so multiplication cannot reach its
\(2h\)-dimensional target
\(\operatorname {Sym}^{2h-1}\mathbb C^2\).

Conversely, under gcd one choose nonzero \(f\in L_E\).  For every root of
\(f\), evaluation is a proper hyperplane in \(L_E\); choose \(g\) outside
their finite union.  Then \(\gcd(f,g)=1\).  If
\(fA=gB\), with \(A,B\in\operatorname {Sym}^{h-1}\mathbb C^2\),
coprimality gives \(f\mid B\), impossible in degree \(h-1<h\) unless
\(A=B=0\).  Hence

\[
 f\operatorname {Sym}^{h-1}\mathbb C^2
 \oplus g\operatorname {Sym}^{h-1}\mathbb C^2
      =\operatorname {Sym}^{2h-1}\mathbb C^2.                    \tag{A8}
\]

The two summands and target have dimensions \(h,h,2h\).  The matrix of
(A8) is the \(2h\)-by-\(2h\) Sylvester matrix, so it is invertible exactly
when \(\operatorname {Res}(f,g)\ne0\).  Concatenating the
\(2h\)-by-\(h\) Toeplitz blocks of a spanning coordinate list gives the
same image.  Rank \(2h\) therefore gives a nonzero \(2h\)-column minor.
Those columns may be different shifts of fewer than \(2h\) distinct tensor
coordinates; the primary note does not claim otherwise.

This verifies all four clauses of Lemma 3.1 and every dimension in its
proof.

## 3. Canonical scalar-zero cases

On \(K(u,v)=uE_{ab}+vI\), direct contraction is

\[
 s(K(u,v))=\alpha u+\tau v,\qquad
 \alpha=A_{pq}(a,b)\ne0,\quad
 \tau=\operatorname {tr}A_{pq}.                                \tag{A9}
\]

Its unique projective scalar-zero point is represented by

\[
                            K_*=\tau E_{ab}-\alpha I.             \tag{A10}
\]

The physical row and (A4) give

\[
             r_*q^{[h-1]}=T(K_*),\qquad
             {\cal E}(K_*)=r_*^{[h]}.                            \tag{A11}
\]

If the whole line is rootless, the second tensor is nonzero.

For \(a\ne b\), \(E_{ab}\) has zero diagonal and square zero.  Therefore

\[
 T(K_*)=-\alpha\sum_{c=0}^2X_c,\qquad
 \det K_*=(-\alpha)^3\ne0,                                     \tag{A12}
\]

which verifies the full ternary packet and its sign.

For \(a=b\), the diagonal entries of \(K_*\) are

\[
                 \tau-\alpha\quad\hbox{at }a,\qquad
                 -\alpha\quad\hbox{at the other two colours}.   \tag{A13}
\]

Thus \(\det K_*=\alpha^2(\tau-\alpha)\).  When
\(\tau\ne\alpha\), all three target coefficients are nonzero and the cap
matrix is invertible; when \(\tau=\alpha\), exactly the \(a\)-target is
lost and the remaining packet is binary.  Since \(\alpha\ne0\), there is
no further exceptional value.

## 4. Endpoint order, aggregation, and higher-order scope

Write the deleted endpoint stars as

\[
 p_i=\sum_{x\in W}p_{i,x},\qquad
 s_j=\sum_{y\in W}s_{j,y}.                                     \tag{A14}
\]

Then

\[
 r(K)=\sum_{ij}K_{ij}p_i s_j                                  \tag{A15}
\]

contains both assignments \(p\to x,q\to y\) and
\(p\to y,q\to x\).  Same-site terms vanish in the site-square-zero
algebra.  Endpoint order is therefore retained, rather than identified.
Aggregate blocks may be sums of parallel decorated sources; expanding
(A14)--(A15) retains every parallel choice and arbitrary complex
cancellation.  No step assumes a simple graph, a nonzero individual
summand, or a rank-one physical block.

The final injective-star formulation is correctly labelled as a proposed
remaining theorem.  Injectivity comes from a good physical pair; it is not
inferred merely from invertibility of the \(3\)-by-\(3\) cap matrix \(K_*\).

Finally, the primary note never claims that a two-site cut at \(h>3\)
leaves a four-site tensor or that the cubic rows persist unchanged.  Its
all-order certificate uses scalar coordinates of the **full**
\(2h\)-site clean tensor.  Literal four-cut formulas and selector
alternatives are routed only to the linked first-boundary \(h=3\) theorem.

## 5. Exact repair list

1. **No mathematical repair required.**  Equations (1)--(19) and Lemma
   3.1 pass.
2. **Optional convention:** declare the gcd of an empty coordinate list
   to be \(0\), or begin Lemma 3.1 with \(E\ne0\).
3. **Cosmetic only:** replace plain parenthesized TeX in the primary prose
   with rendered math delimiters.

No executable is needed: the audit consists of the displayed
divided-power expansion, the coprime Sylvester degree count, and the direct
\(3\)-by-\(3\) determinant calculation.

The optional zero-family gcd convention and the prose math delimiters were
then repaired.  These changes do not alter any audited equation.  The
repaired primary has SHA-256

    36d0c291156328afedbd71486998b5f7dbcc8444431d3cf7a94aaf3185da8cd7  notes/curved-rootless-line-uniform-response-resultant.md
