# Complete anchors leave one uniform Fitting identity unproved

## Outcome

The complete diagonal anchors and crossed target-zero row do not, by
themselves, force a common clean factor. Their strongest committed effect is
to make the static label-transport block invertible. After that elimination,
the all-order divided-power expansion leaves an independent nonlinear tail.

Write

\[
                         F=\alpha q+R.
\]

In the source grades \(R^{[j]}q^{[h-j]}\),

\[
 F^{[h]}=\sum_{j=0}^h
              \alpha^{h-j}R^{[j]}q^{[h-j]}.             \tag{1}
\]

The crossed physical row is

\[
                     \alpha q^{[h]}+Rq^{[h-1]}=0.        \tag{2}
\]

Subtracting \(\alpha^{h-1}\) times (2) from (1) leaves

\[
 \boxed{
 G_h=\sum_{j=2}^h
       \alpha^{h-j}R^{[j]}q^{[h-j]}.}                    \tag{3}
\]

At \(h=3\), this is the previously isolated
\(\alpha R^{[2]}q+R^{[3]}\). The complete anchor/crossed packet controls
the \(j=0,1\) grades and imposes no equation on (3).

This yields a sharp uniform Fitting guard. Normalize one exposed clean form
to \(f=v^h\), and write every other clean form as

\[
 g_i=\chi_i u^h+c_{i,1}u^{h-1}v+\cdots+c_{i,h}v^h,
 \qquad
 \chi_i=[u^h]G_{h,i}.                                    \tag{4}
\]

On

\[
 Q_f=S_{2h-1}/v^hS_{h-1}
  =\langle u^{2h-1},u^{2h-2}v,\ldots,u^hv^{h-1}\rangle,
\]

multiplication by \(g_i\) is the lower-triangular Toeplitz matrix

\[
 M_i=
 \begin{pmatrix}
 \chi_i&0&\cdots&0\\
 c_{i,1}&\chi_i&\ddots&\vdots\\
 \vdots&\ddots&\ddots&0\\
 c_{i,h-1}&\cdots&c_{i,1}&\chi_i
 \end{pmatrix},
 \qquad \det M_i=\chi_i^h.                               \tag{5}
\]

Hence the combined residual map

\[
 \mathcal M_f=[M_1\ M_2\ \cdots\ M_m]:
                         A_f^{\oplus m}\longrightarrow A_f \tag{6}
\]

has rank below \(h\), over the physical coefficient field, exactly when

\[
                         \chi_1=\cdots=\chi_m=0.          \tag{7}
\]

If one \(\chi_i\ne0\), its block \(M_i\) is invertible and the top Fitting
ideal specializes to the unit ideal. If all \(\chi_i=0\), the first row of
(6) is zero and coefficient extraction at \(u^{2h-1}\) is a nonzero common
dual. Scheme-theoretically, the radical of the maximal-minor ideal of the
universal Toeplitz family is

\[
                 \sqrt{I_h(\mathcal M_f)}
                      =(\chi_1,\ldots,\chi_m).            \tag{8}
\]

Thus the exact positive source identity is

\[
 \boxed{\bigwedge^h\mathcal M_f=0}                       \tag{9}
\]

in the complete physical source quotient. On the chart \(f=v^h\), (9)
reduces set-theoretically to (7), with each \(\chi_i\) the literal leading
coefficient of (3). No committed anchor, crossed-row, or uniform
grade-split identity proves (9).

There is a second, genuinely constructive route through syzygies.
Let \(\mathbf g=(g_1,\ldots,g_m)^{\mathsf T}\), with all \(g_i\) homogeneous
of degree \(h\). If the source constructs a homogeneous
\(m\times(m-1)\) matrix \(H\) such that

\[
 H^{\mathsf T}\mathbf g=0,\qquad
 \operatorname {rank}_{\Bbbk(u/v)}H=m-1,\qquad
 \sum_{j=1}^{m-1}b_j<h,                                 \tag{10}
\]

where \(b_j\) is the degree of column \(j\), then all \(g_i\) have a common
factor of degree at least

\[
                         h-\sum_jb_j>0.                  \tag{11}
\]

This is the sharp Hilbert--Burch alternative. The strict degree inequality
is essential: there are full-rank syzygy matrices with
\(\sum b_j=h\) whose maximal minors are

\[
                         v^h,\quad -uv^{h-1},\quad u^h,  \tag{12}
\]

and these forms are coprime.

The complete anchor/crossed label block is not a matrix \(H\) of the type
(10). It is an invertible scalar transport matrix in a separate label
module. The uniform grade-split carrier likewise relates selector and
curvature filtration classes, not the clean forms \(g_i\) by a homogeneous
syzygy. Therefore neither currently supplies the degree deficit in (10).

The proof frontier is now an exact fork:

1. prove the literal maximal-minor identity (9) for the complete source
   equations; or
2. construct a source-provenant Hilbert--Burch matrix satisfying (10).

Either closes the rootless branch. The existing inputs establish neither.
This is a source-presentation counterguard, not a global Krenn
counterexample.

## 1. What the complete anchors actually prove

On two selected labels \(r,s\), retain the two diagonal-anchor columns, the
common direct table, and the crossed target-zero row. In the ordered
entry basis \(rr,rs,sr,ss\), the committed static block is

\[
 S=
 \begin{pmatrix}
 1&0&1&0\\
 0&0&1&1\\
 0&0&1&-2\\
 0&1&2&0
 \end{pmatrix},
 \qquad \det S=-3.                                      \tag{13}
\]

Thus the diagonal anchors plus crossed row reconstruct the entire static
normal square. There is no static cokernel from which a clean divisor
functional could be extracted. This is useful progress: it moves the
problem completely into the nonlinear repeated-insertion grades. It does
not impose an equation there.

The complete all-colour diagonal-anchor theorem gives, at each physical
colour \(c\),

\[
 P_c^{\mathsf T}H(Q_c)S_c=E_{cc}-F_cd.                  \tag{14}
\]

This controls rank and flag alignment of endpoint factors. It is still an
identity in the target-label sandwich. It neither contains (3) nor gives a
homogeneous syzygy among the binary clean forms. In particular, (14) cannot
be read as a Hilbert--Burch column without an additional source map from the
endpoint-label module to \(\mathcal E_h\).

The all-order tail calculation is division-free. In the free source-grade
basis

\[
       q^{[h]},Rq^{[h-1]},R^{[2]}q^{[h-2]},\ldots,R^{[h]},
\]

the coefficient vector of \(F^{[h]}\) is

\[
                    (\alpha^h,\alpha^{h-1},\ldots,1),
\]

while \(\alpha^{h-1}\) times the crossed row has vector

\[
                    (\alpha^h,\alpha^{h-1},0,\ldots,0).
\]

Their difference is exactly (3). Since these are distinct repeated
physical insertion grades, static label reconstruction cannot cancel their
coefficients.

## 2. The top Fitting ideal on the pure divisor chart

Let \(A_f=\Bbbk[t]/(t^h)\), using the affine coordinate
\(t=v/u\). The class of (4) is

\[
              \bar g_i=\chi_i+c_{i,1}t+\cdots+c_{i,h-1}t^{h-1}.
\]

Matrix (5) is multiplication by \(\bar g_i\) in
\(1,t,\ldots,t^{h-1}\). It immediately proves:

> **Lemma 2.1 (pure-divisor Fitting criterion).**
> The following are equivalent over a coefficient field:
>
> 1. \(\operatorname {rank}\mathcal M_f<h\);
> 2. \(I_h(\mathcal M_f)=0\);
> 3. every \(\chi_i\) is zero;
> 4. \(1\in A_f\) is not contained in the ideal
>    \((\bar g_1,\ldots,\bar g_m)\);
> 5. coefficient extraction at \(u^{2h-1}\) annihilates the image.

Indeed, if some \(\chi_i\ne0\), then \(\bar g_i\) is a unit in the local
Artin ring \(A_f\), so \(M_i\) is invertible. If all \(\chi_i=0\), every
\(\bar g_i\) lies in the maximal ideal \((t)\), so the combined image lies
there and the first quotient coordinate survives.

The universal variety of rank defect is therefore the coordinate plane
\(\chi_1=\cdots=\chi_m=0\), proving (8) by the Nullstellensatz in
characteristic zero. The actual maximal-minor ideal can have nonreduced
subresultant structure; for example, one individual block contributes
\(\chi_i^h\). That scheme structure matters for a canonical section across
corank strata, but not for the pointwise rank criterion.

Coordinate-free, the same condition is the vanishing of every
\(h\times h\) minor in (9), or equivalently a nonzero common Bezout kernel
after the fixed Barnett/Frobenius transformations. This is exactly the
simultaneous-kernel theorem isolated previously.

## 3. The uniform source counterguard

Combine (13) with one residual form \(g\) whose leading tail coefficient is
\(\chi=1\). After static elimination the presentation contains the block

\[
                         S\oplus M_g.                    \tag{15}
\]

Equations (5) and (13) give

\[
                  \det(S\oplus M_g)=-3.                 \tag{16}
\]

Thus the completed anchors, direct table, crossed row, all their static
transport, and a literal tail (3) can coexist with a full residual
Macaulay block at every \(h\ge3\). This specializes the top Fitting ideal
to the unit ideal and leaves no simultaneous Bezout kernel.

The construction is source-faithful only at the presentation interface:
the columns have the committed source grades and exact divided-power
coefficients. It does not assert that an arbitrary choice \(\chi=1\)
extends to a global Krenn source satisfying every full-nine, word, target,
and protected row. Consequently it proves the precise logical statement

\[
 \{\text{complete static anchors/crossed row and (1)--(2)}\}
       \not\Longrightarrow \bigwedge^h\mathcal M_f=0.    \tag{17}
\]

The full source equations may contain an additional cross-word or
higher-Bianchi relation which kills every \(\chi_i\). Formula (3) says
exactly where that relation must land.

The uniform grade-split sum-channel equation does not change (17). Its
isolated class lies in the selector quotient tensored with the
low/internal filtration pair. It contains no multiplication-by-\(\bar g_i\)
column and no coefficient of \(R^{[j]}q^{[h-j]}\) for \(j\ge2\). Turning it
into (9) would require precisely the missing filtered transfer
\(\operatorname {Tr}_h\); using it as though it already supplied (9) would
be circular.

## 4. The sharp Hilbert--Burch criterion

The Fitting identity can be forced indirectly if the source supplies
enough low-degree syzygies. Let

\[
 H=(H_1|\cdots|H_{m-1})
\]

be an \(m\times(m-1)\) homogeneous matrix, with every entry of column \(j\)
of degree \(b_j\). Assume \(H\) has rank \(m-1\) over the fraction field
and \(H^{\mathsf T}\mathbf g=0\).

Let \(\Delta_i\) be the signed maximal minor obtained by deleting row \(i\).
Every \(\Delta_i\) has degree

\[
                              B=\sum_jb_j.               \tag{18}
\]

The cofactor vector \(\Delta\) spans the one-dimensional kernel of
\(H^{\mathsf T}\) over the fraction field. Hence

\[
                         \mathbf g=a\,\Delta             \tag{19}
\]

there. Divide the common gcd from the \(\Delta_i\). The resulting primitive
vector still spans the kernel, and Gauss's lemma makes the corresponding
scalar \(a\) a homogeneous polynomial. Its degree is at least \(h-B\).
Therefore \(B<h\) forces a nonconstant common factor, proving (11).

The threshold is exact. For three generators, take

\[
 H=
 \begin{pmatrix}
 u&0\\
 v&u^{h-1}\\
 0&v^{h-1}
 \end{pmatrix}.                                         \tag{20}
\]

Its column degrees sum to \(h\), and its signed maximal minors are (12).
The first and third are \(v^h\) and \(u^h\), so their gcd is one.

At the first forcing degree, replace \(h-1\) in the second column of (20)
by \(h-2\). The minors then have degree \(h-1\):

\[
                 v^{h-1},\quad-uv^{h-2},\quad u^{h-1}.
\]

Multiplying all three by any nonzero linear form produces degree-\(h\)
clean forms satisfying the same two syzygies and sharing that linear
factor. This realizes equality in the lower bound (11).

Accordingly, the sharp source-level Hilbert--Burch target is not “find a
syzygy.” It is:

\[
 \boxed{
 \text{construct }m-1\text{ source syzygies of generic rank }m-1
 \text{ whose column-degree sum is at most }h-1.}        \tag{21}
\]

Neither the invertible static matrix (13) nor the grade-split carrier is
such a system.

## 5. The association-projector cubic is an independent input

The centered occurrence programme supplies exact coefficient-level
projectors. The matching two-switch operator has denominator \(2h-1\), and
the proposed endpoint association polynomial

\[
 P_h(B_h)=(B_h+2I)(B_h-(2h-2)I)(B_h-2hI)                \tag{22}
\]

has constant eigenvalue

\[
                         P_h(4h)=8h(h+1)(2h+1).          \tag{23}
\]

This is a useful uniform occurrence projector. It does not yet supply
\(\operatorname {Tr}_h\). The operator \(B_h\) acts on ordered endpoint and
matching occurrences; its polynomial degree three is a composition/Hasse
filtration degree. It is not degree three in the binary clean parameter.
In particular, it does not define the missing

\[
                   b_{h-3}\in\operatorname {Sym}^{h-3}U \tag{24}
\]

needed to type a selector quadratic as a residual vector. The numerical
equality \(3=h-3\) at \(h=6\) has no invariant meaning.

There is a decisive independence counterguard. The occurrence association
scheme and both denominators in (22)--(23) are defined without the clean
forms. Therefore the same coefficient projector exists for

\[
                         \mathcal E_h=\langle u^h,v^h\rangle. \tag{25}
\]

But the \(2h\) Macaulay shifts of (25) are the full monomial basis of
\(S_{2h-1}\), so

\[
                    \ker\mu_{\mathcal E_h}^*=0.          \tag{26}
\]

Thus no identity internal to the coefficient association algebra can imply
the Fitting wedge (9). This does not rule out using the projector as an
input to the missing construction. A positive route would:

1. lift (22) and the matching projector to the complete augmented
   Cartan/Hasse bicomplex;
2. fill their one-, two-, mixed-, and three-fold product-rule faces;
3. construct a source comparison sending the corrected face to a
   degree-\((h-3)\) clean covariant or directly to \(z_h\); and
4. prove \(B(f,e)z_h=0\) for every clean \(e\), with nonzero physical
   terminal.

Steps 3--4 are precisely new \(\operatorname {Tr}_h\)/Fitting data. Even
step 1 is currently conditional: coefficient graph commutation does not
fill the nonzero physical Leibniz commutators. The association projector is
therefore complementary to the Bezout route, not yet its construction.

## 6. Positive proof paths

There are now two equivalent proof endpoints but different construction
problems.

### Fitting/subresultant path

Construct in the complete source quotient the identity

\[
             I_h(\mathcal M_f)=0.                        \tag{27}
\]

At a physical point, ordinary linear algebra supplies a nonzero dual
\(\Theta_h\), and the residual gcd theorem forces a common factor. To make
the construction functorial as a physical chain, choose the first nonzero
subresultant on each corank stratum, prove overlap compatibility, and show
its terminal normalization is nonzero.

On the pure-divisor chart the first source calculation is simply

\[
 [u^h]\!\left(
   \sum_{j=2}^h\alpha_i^{h-j}
       R_i^{[j]}q_i^{[h-j]}
 \right)=0
 \qquad\text{for every clean coordinate }i.              \tag{28}
\]

A complete higher-Bianchi/cross-word identity proving (23) would finish
this path locally; equivariance would then cover arbitrary divisor charts.

### Hilbert--Burch path

Construct \(H\) in (21) directly from physical source rows. This has the
advantage that its maximal-minor vector produces the common factor without
choosing an adjugate stratum. The hard requirements are literal:

* all columns must be syzygies of the **same** clean family;
* their word, fine, and repeated grades must be compatible;
* the matrix must have generic rank \(m-1\); and
* its total coefficient degree must be below \(h\).

A scalar transport identity, separately labelled syzygies, or a degree-\(h\)
Koszul/Hilbert--Burch matrix does not suffice.

## 7. Exact checker and scope

The dependency-pinned checker
[verify_uniform_anchor_crossed_bezout_fitting_hilbert_burch_gate.py](../computations/verify_uniform_anchor_crossed_bezout_fitting_hilbert_burch_gate.py)
audits over exact rationals for \(3\le h\le10\):

* determinant \(-3\) of the completed static label block;
* the all-order tail subtraction (3) in every repeated-insertion grade;
* \(\det M_i=\chi_i^h\) and exact multi-form rank behavior;
* the unit-Fitting specialization \(\chi=1\);
* the common-factor Hilbert--Burch example with column-degree sum \(h-1\);
* the coprime sharp-boundary example with degree sum \(h\); and
* coexistence of the coefficient association projector with the
  full-rank pure-axis Macaulay guard; and
* the current dependency scope.

The finite presentation does not model every global Krenn source row and
does not prove that the physical full source admits \(\chi\ne0\). It proves
that the currently named complete anchors, crossed row, and grade-split
carrier do not themselves imply the missing Fitting identity. The next
proof-advancing computation should target (23) in the full higher-Bianchi
and cross-word inventory.
