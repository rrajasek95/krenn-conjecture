# Exact nine reduces to the three-by-three singular square

## 1. Outcome

Continue from
[`two-k4-exact-eight-checkerboard-hessian-obstruction.md`](two-k4-exact-eight-checkerboard-hessian-obstruction.md),
including its proved overlap-one common-site incidence lemma.  Let
\(B_{ij}\) be the sixteen cross blocks between the two standard
\(K_4\) shores, and suppose exactly nine of them are singular.

After all pre-seven position rules and the separated one-plus-two erasure,
there are nine row/column/transpose orbits.  Seven are excluded directly
by the overlap-one lemma, allowing an invertible component to pad an
exception set of size one.  An eighth, the disjoint-pair orbit

\[
       012\mid 01\mid 23\mid 23,                       \tag{1}
\]

is excluded for every literal-zero degeneration by a two-block polynomial
certificate.  The sole position orbit not closed by these local inputs is

\[
       \boxed{012\mid012\mid012\mid\varnothing}.        \tag{2}
\]

Thus an exact-nine solution, if one exists, has (up to row and column
permutations and transposition) precisely the top-left \(K_{3,3}\) as its
singular support.  All seven blocks in row or column \(3\) are invertible.
The residual is subsequently excluded, for arbitrary ranks and unrelated
erased planes, in
[`two-k4-k33-nonzero-star-erasure.md`](two-k4-k33-nonzero-star-erasure.md),
with an independent two-zero audit in
[`two-k4-k33-two-zero-independent-closure.md`](two-k4-k33-two-zero-independent-closure.md).
Consequently exact nine is impossible and every two-\(K_4\) solution has at
least ten singular cross blocks.

## 2. The unconditional nine-orbit census

Of the \({16\choose9}=11440\) position supports, \(2752\) survive the
pre-seven and separated one-plus-two rules.  Their complete orbit census
is as follows.  The fourth column counts perfect matchings in the
*nonsingular complement* only as a diagnostic.

\[
\begin{array}{c|r|c|c|l}
 &\text{orbit size}&\text{singular rows}&\#\mathrm{PM}&\text{local conclusion}\\ \hline
H_0&288&0123\mid01\mid02\mid0&0&\text{overlap }01,02\\
H_1&16&012\mid012\mid012\mid\varnothing&0&K_{3,3}\text{ residual}\\
H_2&288&012\mid012\mid03\mid3&0&\text{padded overlap }03,13\\
H_3&192&012\mid013\mid023\mid\varnothing&1&\text{transpose overlap}\\
H_4&576&012\mid013\mid02\mid2&1&\text{padded overlap }02,12\\
H_5&576&012\mid01\mid03\mid23&1&\text{overlap }01,03\\
H_6&576&012\mid013\mid23\mid2&2&\text{padded overlap }23,02\\
H_7&144&012\mid01\mid23\mid23&2&\text{disjoint, then (7)}\\
H_8&96&012\mid03\mid13\mid23&2&\text{overlap }03,13.
\end{array}                                             \tag{3}
\]

It would be invalid to discard the first six rows of (3) using the
low-matching or unique-perfect-matching theorems.  Those theorems concern
the graph of nonzero cross blocks.  A singular block need not be zero, so
the matching count of the nonsingular complement does not define that
graph.  This is exactly the distinction emphasized in
[`two-k4-rank2-support-nondegeneration.md`](two-k4-rank2-support-nondegeneration.md).

## 3. Seven overlap-one closures

The overlap-one lemma has the following invariant hypothesis.  Each of two
stars has a selected two-element exception set; the maps at selected sites
are arbitrary, while the maps at the other two sites are invertible.  The
selected maps are not required to be singular.  Consequently a star with
only one singular component may be **padded** by selecting one additional
invertible component as arbitrary.

If the selected exception pairs meet only at \(h\), the eight erased cells
force the three blocks of \(q_{\rm eff}\) incident with \(h\) to vanish.
For complementary left row pairs \(\{a,b\}\), \(\{r,s\}\), and
\(c=\kappa(ab)=\kappa(rs)\), the actual two-/four-cross pullback is

\[
 q_{\rm eff}=\lambda_{ab}q_R+p_{a,c}p_{b,c},
 \qquad
 q_{\rm eff}p_{r,x}p_{s,y}=0\quad((x,y)\ne(c,c)).       \tag{4}
\]

At endpoint \(h\), the three incident blocks of \(q_R\) have endpoint
lines \(\mathbb Fe_0,\mathbb Fe_1,\mathbb Fe_2\).  Every endpoint image
of the product term in (4) lies in the fixed plane spanned by the two
components of \(p_{a,c},p_{b,c}\) at \(h\).  Three vanished incident
blocks would put all three coordinate lines in that plane, a contradiction.

The seven applications are recorded in the last column of (3).  More
explicitly, \(H_3\) is first transposed; in \(H_2,H_4,H_6\), the
degree-one row is padded to the displayed two-set.  All actual singular
components lie in the selected pairs, so every unselected component is
indeed invertible.  This excludes
\(H_0,H_2,H_3,H_4,H_5,H_6,H_8\) without any rank or nonzero assumption on
their singular blocks.

## 4. Every literal-zero branch of the disjoint orbit

For \(H_7\), use rows \(r=1,s=2\), whose exception pairs are
\(\{0,1\}\) and \(\{2,3\}\).  The disjoint lemma and the endpoint-plane
argument exclude the branch unless

\[
                 B_{10}=B_{11}=B_{22}=B_{23}=0.        \tag{5}
\]

Repeating with rows \(1,3\) forces \(B_{32}=B_{33}=0\).  After
transposition, use columns \(0,3\) and then \(1,3\).  The same argument
forces

\[
                            B_{00}=B_{01}=0.             \tag{6}
\]

An exhaustive zero/nonzero audit of all \(2^9=512\) branches therefore
leaves only the empty set and \(\{B_{02}\}\) as possible nonzero singular
sets.

Return to \(r=1,s=2,a=0,b=3\).  Their common internal colour is
\(c=2\).  Since both disjoint exception pairs are now literal zero, the
disjoint lemma says that \(q_{\rm eff}\) is supported only on right edges
\(01\) and \(23\).  In particular its \(02\) and \(12\) blocks vanish.
Write

\[
       \alpha=\lambda_{03}\rho_{02},\qquad
       \beta =\lambda_{03}\rho_{12}.                  \tag{7a}
\]

Both scalars are nonzero.  Indeed, each of the three constant-word
coefficients of either standard \(K_4\) factor is nonzero; every internal
edge occurs in one of those perfect matchings, so every left weight
\(\lambda_{ij}\) and right weight \(\rho_{uv}\) is nonzero.  No equality
between \(\alpha\) and \(\beta\), and no unit-weight normalization, is
being assumed.

Put

\[
 v=\operatorname {row}_2(B_{02})^{\mathsf T},\qquad
 u_0=\operatorname {row}_2(B_{30})^{\mathsf T},\qquad
 u_1=\operatorname {row}_2(B_{31})^{\mathsf T}.
\]

Because right edges \(02\) and \(12\) have colours \(1\) and \(2\),
respectively, their exact equations are

\[
       0=(q_{\rm eff})_{02}=\alpha E_{11}+u_0v^{\mathsf T},
 \qquad
       0=(q_{\rm eff})_{12}=\beta E_{22}+u_1v^{\mathsf T},
 \qquad \alpha\beta\ne0.                               \tag{7}
\]

If \(v\ne0\), these equations would put the same vector \(v\) on both
\(\mathbb Fe_1\) and \(\mathbb Fe_2\).  The following division-free
certificate also handles \(v=0\).  If

\[
 f_{11}=\alpha+u_{0,1}v_1,\qquad
 f_{12}=u_{0,1}v_2,\qquad
 g_{22}=\beta+u_{1,2}v_2,
\]

then

\[
 \beta f_{11}
 -v_1\bigl(u_{0,1}g_{22}-u_{1,2}f_{12}\bigr)=\alpha\beta. \tag{8}
\]

Vanishing in (7) contradicts \(\alpha\beta\ne0\), including the case
\(B_{02}=0\).  This closes \(H_7\).

## 5. Why the three-by-three square is a genuine local residual

In (2), three rows have three singular components and the fourth has none;
the same is true after transposition.  Hence no two distinct stars have
all their singular components inside two-element exception sets, even
after padding.  Neither exact-eight local lemma applies.

A direct rank-one specialization shows that simply extending the
common-site incidence conclusion would be false.  In the four-site
erased-Hessian notation, take

\[
 P_0=P_1=P_2=S_0=S_1=S_2=\operatorname {diag}(1,0,0),
 \qquad P_3=S_3=I.                                    \tag{9}
\]

For every \((x,y)\ne(0,0)\), every quadratic block on one of the edges
\(03,13,23\) is annihilated in

\[
                         q p_xs_y=0.                   \tag{10}
\]

Indeed, one of the two stars is then supported only at site \(3\), and the
square-free product repeats that site.  Thus all \(27\) coordinates on the
three edges incident with the common regular site lie literally in the
kernel.  The exact erased-Hessian matrix in this specialization has rank
\(19\).  This is a countermodel to the missing *local* incidence lemma,
not a solution of the complete two-\(K_4\) tensor equations.

Closing (2) therefore requires either a coupled use of several row-pair
sectors or a new argument forcing literal zeros or stronger rank incidence
inside the singular \(K_{3,3}\).

## 6. Exact audit

Run

```text
python computations/verify_two_k4_exact_nine_frontier.py
```

The checker verifies the complete census, all padded exception
containments, all \(8\cdot729=5832\) coefficients of the selected actual
sector identities with an algebraically independent selected left weight
and six algebraically independent right weights, every literal-zero branch
of \(H_7\), certificate (8), and the rank-one local barrier (9)--(10).  Its
output is

```text
exact-nine census: 2752 supports in 9 position orbits
nonsingular-complement PM histogram: 592 / 1344 / 816 (diagnostic only)
seven overlap-one orbits: common-site endpoint contradiction
disjoint orbit B: 512 literal-zero branches -> {zero, B_02}
sharp B residual: weighted alpha*beta polynomial certificate
K3,3 residual: rank-one local kernel has 27 invisible incident columns
two-K4 exact-nine frontier reduction: PASS
```
