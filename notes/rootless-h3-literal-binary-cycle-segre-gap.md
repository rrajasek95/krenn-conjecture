# The literal (h=3) root coefficient survives until shared-star factorization

## 1. Outcome

This note tests the sharp coefficient

\[
                         \chi=g(1,0)
\]

from the triple-root boundary in an actual six-site site-square-zero
matching algebra.  It gives the strongest near-physical boundary reached
here; it does not prove that a complete physical full-nine source has
\(\chi\ne0\), and it does not close Krenn's conjecture.

For an off-diagonal cell with direct coefficient \(\alpha\), response
quadratic \(R\), and internal quadratic \(q\), the exact physical row is

\[
                   \alpha q^{[3]}+Rq^{[2]}=0.             \tag{1}
\]

At the root direction \([1:0]\), expansion before division or
common-power cancellation gives

\[
\boxed{
 (\alpha q+R)^{[3]}
   =\alpha^2(\alpha q^{[3]}+Rq^{[2]})
      +\alpha R^{[2]}q+R^{[3]}.
}                                                          \tag{2}
\]

Consequently every selected tensor coordinate \(Y\) obeys

\[
 \boxed{
 \chi_Y=[Y](\alpha q+R)^{[3]}
        =[Y](\alpha R^{[2]}q+R^{[3]}).
 }                                                          \tag{3}
\]

Thus the top off-diagonal row kills exactly the first two matching layers.
The two nonlinear response layers in (3) are the literal coefficient that
a positive coefficient-cut lemma must control.

The packet below has:

* a genuine eight-site binary \(C_8\) aggregate whose global matching
  tensor is exactly \(X_0+X_1\);
* two overlapping physical pair charts, each with the differently
  labelled anchors \(X_0,X_1\), all target-zero off-diagonal slices, and
  a complete crossed four-index target-zero slice;
* on the first six-site chart, an exact top-level eight-row extension with
  one selected off-diagonal direct cell;
* a physical binary line with
  \[
                         f=v^3,\qquad g=u^3-u^2v,
                         \qquad \chi=g(1,0)=1;            \tag{4}
  \]
  hence the residual map \(gS_2\to Q_f\) has determinant one.

The first omitted compatibility is exact and occurs before the missing
\(X_2\) anchor: the added cap quadratics are not products \(p_i s_j\) of
literal endpoint stars.  A six-port diagonal-completion rank test proves
this, so the failure is not being hidden in a top-degree cancellation.
Accordingly the calculation does **not** decide whether all nine physical
rows together with shared-star factorization force \(\chi=0\).  It shows
that site-square-zero multiplication, two physical anchors, a literal
two-chart overlap, the crossed target-zero slice, and eight top rows still
leave \(\chi\ne0\) until the Segre/shared-star compatibility is used.

## 2. The literal binary (C_8) base

Use eight sites

\[
                     \{p,q,0,1,2,3,4,5\}
\]

and put unit diagonal colour-zero cells on

\[
                       p0\mid q1\mid23\mid45
\]

and unit diagonal colour-one cells on

\[
                       p5\mid q0\mid12\mid34.           \tag{5}
\]

Their union is the alternating cycle

\[
                       p-0-q-1-2-3-4-5-p.
\]

An even cycle has exactly its two alternating perfect matchings.  With the
decorations in (5), the complete global matching tensor is therefore

\[
                              X_0+X_1.                    \tag{6}
\]

There are no mixed supported matchings and no cancellations in (6).

Delete \(p,q\).  The residual six-site quadratic is

\[
                 q=(23)_0+(45)_0+(12)_1+(34)_1.         \tag{7}
\]

The two diagonal response edges are

\[
                         A_0=(01)_0,qquad A_1=(05)_1.   \tag{8}
\]

Site \(0\) is isolated in (7), so \(q^{[3]}=0\).  The only relevant
two-matchings give

\[
                         A_0q^{[2]}=X_0,qquad
                         A_1q^{[2]}=X_1.                 \tag{9}
\]

Every other pair slice is zero.  Deleting \(p,5\) gives a second,
overlapping six-site chart with the same two physical-label anchors and
the same eight of nine target rows, because both charts are literal slices
of (6).  In either chart the sole missing target row is

\[
                                  0=X_2.                 \tag{10}
\]

For a concrete crossed four-index coefficient, expose \(p,q,5,0\).  The
boundary assignments \((0,0,1,1)\) and \((1,1,0,0)\) have zero complete
complementary tensor: neither of the two matchings in (6) has those mixed
boundary labels.  This is a genuine source-provenant four-index
target-zero slice, not a formal matrix relation between independent chart
copies.

## 3. An exact eight-row cap extension

Retain the physical internal quadratic (7) and introduce two literal
quadratics in the same six-site algebra:

\[
\begin{aligned}
 B&=(02)_2+(13)_2+(45)_1,\\
 R&=(04)_2+(12)_2+(35)_2.                              \tag{11}
\end{aligned}
\]

Each displayed edge of \(B\) and \(R\) has zero \(q^{[2]}\)-cofactor.
For example, deleting \(0,4\) leaves \(1,2,3,5\), on which (7) has no
perfect matching; the other five checks are identical short path checks.
Hence

\[
                              Bq^{[2]}=Rq^{[2]}=0.       \tag{12}
\]

Put the cap table

\[
 z_{00}=A_0,qquad z_{11}=A_1,qquad z_{22}=B,qquad
 z_{02}=R,                                               \tag{13}
\]

with every other \(z_{ij}=0\), and take the sole direct entry

\[
                              a_{02}=1.                  \tag{14}
\]

Equations (7), (9), and (12) give, coefficientwise in the full top tensor,

\[
 a_{ij}q^{[3]}+z_{ij}q^{[2]}
 =\begin{cases}
 X_0,&(i,j)=(0,0),\\
 X_1,&(i,j)=(1,1),\\
 0,&\text{otherwise}.
 \end{cases}                                             \tag{15}
\]

Thus (15) has both differently labelled anchors and every off-diagonal
row, including the selected \(02\) row.  Relative to the ternary target,
its unique failed row is still (10).

This is already stronger than an associated-graded cap-symbol packet:
every object in (7), (11), and (13) is a decorated quadratic in the actual
six-site square-zero algebra, and all bracket powers in (12)--(15) are
literal matching products.

## 4. The triple-root line has (chi=1)

On the canonical line

\[
                          K(u,v)=uE_{02}+vI,
\]

the direct scalar is \(\sigma=u\).  Put

\[
             D=A_0+A_1+B,qquad
             F(u,v)=u(q+R)+vD.                            \tag{16}
\]

Against the ternary target define the usual clean error

\[
             {\cal E}(u,v)=F(u,v)^{[3]}
                    -u^2v(X_0+X_1+X_2).                  \tag{17}
\]

Let

\[
              Y=e_2^{(0)}e_2^{(1)}e_2^{(2)}e_2^{(3)}
                    e_1^{(4)}e_1^{(5)}.                 \tag{18}
\]

The unique \(Y\)-matching is the three-edge matching \(B\), and none of
the edges in \(q+R\) is compatible with a complete \(Y\)-matching.
Therefore

\[
                          f(u,v):=[Y]{\cal E}(u,v)=v^3.  \tag{19}
\]

For the pure colour-two word, the unique source matching is the three-edge
matching \(R\), all with coefficient \(u\).  The target contributes the
only other term, so

\[
                         g(u,v):=[X_2]{\cal E}(u,v)
                                  =u^3-u^2v.             \tag{20}
\]

In particular

\[
                              \chi=g(1,0)=1.             \tag{21}
\]

At the root itself, (12) and \(q^{[3]}=0\) put (2) in the especially
transparent form

\[
                  (q+R)^{[3]}=R^{[2]}q+R^{[3]},
                  \qquad [X_2](q+R)^{[3]}=1.            \tag{22}
\]

No common power was cancelled to obtain (22).

Modulo \(fS_2=v^3S_2\), multiplication by (20), on the bases
\((u^2,uv,v^2)\) and
\((\overline{u^5},\overline{u^4v},\overline{u^3v^2})\), has matrix

\[
                         \begin{pmatrix}
                         1&0&0\\
                        -1&1&0\\
                         0&-1&1
                         \end{pmatrix}.                  \tag{23}
\]

Its determinant is \(1=\chi^3\).  Deleting any one edge of the matching
\(R\) kills the \(u^3X_2\) coefficient, while moving its edge \(04\) to
\(03\) makes \(Rq^{[2]}\ne0\) and immediately violates the selected
off-diagonal row.  These two mutations separately test the root
coefficient and the physical top row.

## 5. The first omitted compatibility is the Segre product

The table (13) is not yet a physical endpoint-star table.  In a genuine
chart one must have

\[
                              z_{ij}=p_i s_j              \tag{24}
\]

for two common triples of linear stars.  Here the failure is visible even
before testing the common triples: neither \(B\) nor \(R\) is one product
of two linear forms.

For \(R\), restrict at each site to the colour-two port.  Its off-diagonal
coefficient graph is the perfect matching

\[
                              04\mid12\mid35.            \tag{25}
\]

For \(B\), use the six ports prescribed by the word (18).  Its graph is

\[
                              02\mid13\mid45.            \tag{26}
\]

In either case, an arbitrary diagonal completion of the symmetric
six-by-six coefficient matrix is block diagonal on three nonzero
two-by-two blocks.  Each block has rank at least one, so every completion
has rank at least three.  If a quadratic were \(ps\), its completed
symmetric coefficient matrix would be

\[
                              ps^{\mathsf T}+sp^{\mathsf T},
\]

which has rank at most two.  This contradiction proves the claimed
individual nonfactorization.

The hierarchy of what is and is not realized is therefore exact.

1. The binary \(C_8\), its two overlapping charts, two physical anchors,
   and the crossed four-index zero slice are genuine aggregate-block data.
2. The extension (11)--(15), the line (16), and the cubics (19)--(20) are
   genuine six-site matching-algebra identities.
3. The first absent physical compatibility is (24).  After it, the next
   absent full-nine datum is the \(X_2\) diagonal row (10).

Hence this guard cannot show that a complete physical full-nine overlap
permits \(\chi\ne0\).  Conversely, any proof that complete physical rows
force \(\chi=0\) must use the shared-star Segre rectangles, the missing
\(X_2\) anchor, or their transported two-chart coefficient cuts; equation
(1), the two existing anchors, and the crossed source slice alone do not
remove the nonlinear residue in (3).

## 6. Audit

The dependency-free checker
[`verify_rootless_h3_literal_binary_cycle_segre_gap.py`](../computations/verify_rootless_h3_literal_binary_cycle_segre_gap.py)
enumerates the global eight-site matching tensor and both chart slices,
checks the two crossed four-index slices, expands every six-site bracket
power in (12)--(22), verifies the residual determinant (23), and audits
the diagonal-completion obstruction and the two sharp mutations.  It uses
explicit failures and runs unchanged under optimization.
