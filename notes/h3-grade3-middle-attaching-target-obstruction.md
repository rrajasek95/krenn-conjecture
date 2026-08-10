# The first source-labelled grade-three attaching map is target-compatible but not normalized

> **Scope correction (commit `9dac232`).**  The defect
> `sum_S D_S` below is the normalization defect of the separately internal
> diagonal source used by this guard.  It is **not** the genuine common
> full-nine attaching class.  In one common selected row, every midpoint
> coefficient also contains its response companion `M_S`; the literal
> aggregate is `alpha(C+D)+M=0`, not `C+D=0`.  Consequently `D=0` is
> insufficient.  The corrected source-relative target is
> `K=sum_S(M_S+alpha D_S)=0`.  See
> [`h3-full-nine-middle-companion-normalization-guard.md`](h3-full-nine-middle-companion-normalization-guard.md).
> The checker and the separate-source obstruction recorded here remain
> valid within their stated scope.

## Outcome

For a selected off-diagonal $h=3$ row, put

\[
 \alpha=d_{ab},\qquad R=p_as_b,\qquad
 \chi=\alpha R^{[2]}q+R^{[3]}.                         \tag{1}
\]

There is a canonical, literal response-grade-three map

\[
 \mathfrak A_{q,R,\alpha}:\langle\chi\rangle
        \longrightarrow \mathbb C^{\binom63}           \tag{2}
\]

whose twenty coordinates are indexed by the binary midpoint words
$1^S0^{S^c}$, $|S|=3$. Its augmentation is

\[
                 \boxed{\sum_{|S|=3}\mathfrak A_S=8\chi.} \tag{3}
\]

Every midpoint word is mixed, so (2) is target-compatible: every diagonal
GHZ target has coefficient zero there. If the canonical attaching cells
were identified with the actual two-chart first and second cells, the
complete all-word equations would kill every coordinate in (2), and (3)
would kill the terminal class.

That normalization is not supplied by the complete binary diagonal face or
by the already closed static two-chart transport. An exact binary diagonal
source with matching tensor $X_0+X_1$, together with a literal shared-star
response satisfying the selected top row, has

\[
 (Q_0,Q_1,Q_2,Q_3)=(1,-1,-10,-18),\qquad \chi=-28.     \tag{4}
\]

All twenty actual midpoint coefficients vanish, while the canonical vector
has sum $-224=8\chi$. The attaching defect therefore has sum $224$. Thus
the first grade-three map exists and has the correct target, but the current
named two-chart presentation does not prove that the physical source lands
through it. The terminal class is not killed at this interface.

The third diagonal target grade is retained in the static label block, but
the checker does not claim a common physical ternary packet. That simultaneous
coupling remains a possible source of the missing normalization. Accordingly
this is a sharp source-provenance obstruction, not a Krenn counterexample.

## 1. The twenty literal Bianchi coordinates

Fix a three-set $S=\{i,k,p\}$ and put $T=S^c$. Define

\[
\begin{aligned}
 \Theta_S={}&2\alpha\sum_{\{i,k\}\subset S}
      R_{ik}\sum_{j\in T}R_{pj}q_{T\setminus\{j\}}\\
 &+\operatorname {per}(R_{S,T}),                       \tag{5}
\end{aligned}
\]

where $p$ is the member of $S\setminus\{i,k\}$ and
$q_{T\setminus\{j\}}$ is the edge on the remaining two sites. This is
identity (18) of
[`h3-nonclean-twojet-middle-core.md`](h3-nonclean-twojet-middle-core.md)
with $(A,B,Q)=(2\alpha R,R,q)$.

Formula (5) is already a literal source coefficient. Introduce an auxiliary
binary edge array by

\[
 \widehat q_{xy}^{00}=q_{xy},\qquad
 \widehat q_{xy}^{10}=\widehat q_{xy}^{01}=R_{xy},\qquad
 \widehat q_{xy}^{11}=2\alpha R_{xy}.                  \tag{6}
\]

Direct matching expansion gives

\[
              [1^S0^T]\widehat q^{[3]}=\Theta_S.        \tag{7}
\]

The terms using one $11$-edge, one crossing edge, and one $00$-edge give
the first line of (5); the three crossing edges give its permanent. Summing
(7) over the twenty three-sets marks each $R^{[2]}q$ matching eight times
after the factor $2\alpha$, and each $R^{[3]}$ matching once for each of
its eight endpoint transversals. This proves (3).

This binary face embeds in the 510-dimensional literal ternary middle-word
sector by setting the third colour count to zero. Thus one 20-dimensional
face already detects $\chi$ once (6) is physically normalized.

## 2. Exact target compatibility and the attaching defect

For every $|S|=3$, the word $1^S0^{S^c}$ contains three zeros and three
ones. Hence

\[
 [1^S0^{S^c}](X_0+X_1+X_2)=0.                         \tag{8}
\]

Suppose a physical two-chart construction supplies oriented first cells
$b^{10},b^{01}$ and second cells $A^{11}$. Its actual midpoint vector is

\[
       \Theta^{\rm src}_S=\Theta_S(A,b^{10},b^{01};q).  \tag{9}
\]

Complete target rows give $\Theta^{\rm src}_S=0$. Write

\[
 D_S=\Theta^{\rm src}_S-
          \Theta_S(2\alpha R,R,R;q).                    \tag{10}
\]

Equations (3), (9), and (10) give the exact obstruction identity

\[
                         \boxed{8\chi=-\sum_SD_S.}      \tag{11}
\]

Target compatibility is therefore automatic; attaching normalization is
the only issue. It is enough to prove $\sum_SD_S=0$, which is weaker than
the coefficientwise equalities in (6). No current diagonal or static
two-chart identity proves this aggregate equality.

Under uniform binary specialization, put

\[
 B=b^{10}+b^{01},\qquad A=A^{11}.                       \tag{12}
\]

The augmentation of (10) is the normalization defect

\[
 \mathfrak D(A,B)=ABq+B^{[3]}
              -8(\alpha R^{[2]}q+R^{[3]}).             \tag{13}
\]

The source-labelled vector (10) is stronger than (13).

## 3. A complete binary diagonal target with nonzero defect

On sites $0,\ldots,5$, take

\[
 M_0=01\mid23\mid45,\qquad M_1=05\mid12\mid34.         \tag{14}
\]

Give every edge of $M_c$ diagonal endpoint colour $(c,c)$. Their union is
one alternating six-cycle and has exactly its two factor matchings. Thus

\[
                         H_6=X_0+X_1                    \tag{15}
\]

on all $2^6$ binary words. Its first cells vanish, and all twenty midpoint
coefficients vanish exactly.

Retain the pure-zero quadratic $q=M_0$ and use the literal shared-star
response

\[
 p=z_0+z_2+z_4,\qquad s=z_1+z_3-3z_5,\qquad R=ps,       \tag{16}
\]

with $\alpha=1$. The four response layers are (4), so the selected top row
is admitted:

\[
                         \alpha Q_0+Q_1=1-1=0.          \tag{17}
\]

The canonical array (6) has midpoint sum $-224$, while (15) has the zero
vector. Hence (10) has sum $224$. This proves that a complete binary
diagonal target alone does not normalize the attaching map.

The completed static two-chart label block has determinant $-3$. Padding it
by the independent third diagonal target grade leaves that determinant
unchanged. After this block is split off, the only aggregate attaching
equation is

\[
                         C+D=0,                          \tag{18}
\]

where $C=8\chi$ and $D=\sum_SD_S$. This row has rank one in the
two-dimensional $(C,D)$ plane. Adjoining cleanliness $C=0$ raises the
combined presentation rank from six to seven; the determinant is $3$. The
exact separator is $(C,D)=(1,-1)$.

## 4. Verdict and next required identity

The first response-grade-three attaching map is explicit, source-labelled,
and target-compatible. It would kill $Q_3$, hence the terminal class, if the
two-chart overlap supplied

\[
                         \boxed{\sum_SD_S=0.}            \tag{19}
\]

The complete binary diagonal target does not supply (19), and the static
crossed/anchor transport lives in a different endpoint fine degree. The
third diagonal row could matter only through a genuinely common physical
ternary comparison, not through its static target grade.

The remaining proof task is therefore no longer to find the middle-word
map. It is to construct a Bianchi/attaching comparison identifying the
actual physical first/second cells with (6) modulo an augmentation-zero
defect.

The dependency-free checker
[`verify_h3_grade3_middle_attaching_target_obstruction.py`](../computations/verify_h3_grade3_middle_attaching_target_obstruction.py)
enumerates all $2^6$ coefficients of (15), all twenty literal coordinates
in (7), the response layers (4), both augmentation sums, and the final rank
obstruction. It uses explicit runtime failures and runs unchanged under
optimized and isolated Python.
