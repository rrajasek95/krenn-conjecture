# The filtered Macaulay obstruction is an exact Schur--Bockstein class

## 1. Two-layer criterion

Let \(k\) be a field and consider a filtered linear system

\[
 M=\begin{pmatrix}A&0\\T&B\end{pmatrix}:
 X\oplus Y\longrightarrow U\oplus V,
 \qquad M(x,y)=(b,c).
\tag{1}
\]

Here \(A\) is the already solved lower-filtration block, \(B\) is the new
leading block, and \(T\) is the tail of the old columns in the new row
degree.

Assume \(b\in\operatorname {im}A\).  Put

\[
 Z_B=\{\lambda\in V^*: \lambda B=0\}
\]

and define the source-relative connecting map

\[
 \partial:Z_B\longrightarrow X^*/\operatorname {row}A,
 \qquad \partial(\lambda)=[\lambda T].
\tag{2}
\]

> **Lemma (Schur--Bockstein criterion).**  System (1) is solvable if and
> only if, for every \(\lambda\in\ker\partial\), one (equivalently every)
> \(\mu\in U^*\) satisfying
> \[
>                         \lambda T=\mu A
> \tag{3}
> \]
> obeys
> \[
>                         \lambda c=\mu b.
> \tag{4}
> \]

**Proof.**  Choose \(x_0\) with \(Ax_0=b\).  The second row of (1) is
solvable after varying \(x=x_0+k\), \(k\in\ker A\), exactly when

\[
 c-Tx_0\in\operatorname {im}B+T(\ker A).
\tag{5}
\]

The annihilator of the right side is the set of \(\lambda\) with
\(\lambda B=0\) and \(\lambda T|_{ker A}=0\).  The latter condition is
equivalent to \(\lambda T\in\operatorname {row}A\), hence to
\(\lambda\in\ker\partial\).  For (3), evaluation of (5) gives

\[
 \lambda(c-Tx_0)=\lambda c-\mu Ax_0=\lambda c-\mu b,
\]

which vanishes exactly under (4).  If two choices of \(\mu\) satisfy (3),
their difference annihilates \(\operatorname {im}A\), so they have the same
value on \(b\).  This proves both the criterion and its independence of
choices. \(\square\)

Equivalently, the left kernel of the full block consists of pairs
\((-\mu,\lambda)\) satisfying (3), and its pairing with the target is
\(\lambda c-\mu b\).  Formula (2) explains which apparent leading
obstructions disappear: if \(\partial(\lambda)\ne0\), changing the earlier
solution along \(\ker A\) changes the new residual detected by \(\lambda\).

## 2. Exact chart-25 degree-four obstruction model

The frozen chart-25 four-row dual is now an exact instance of the criterion,
including literal source labels. In the invariant row basis it splits as

\[
             (-\mu,\lambda)=(-2,-1,-1\mid1),
 \qquad      \mu=(2,1,1),\quad\lambda=(1).               \tag{6}
\]

All nine canonical incident older source-column orbits obey
\(\lambda T=\mu A\), and no leading degree-four source column meets
\(\lambda\). After expansion, the equality holds separately on all 56
individually labelled incident columns, with both sides equal to \(1/4\).
Thus this is a literal lift through (3), not an invariant-quotient analogy.

For the raw residual coordinates,

\[
       b=(-1,0,0),\qquad c=-1,\qquad
       \mu b=-2,\qquad\lambda c=-1.                      \tag{7}
\]

Hence the source-provenant secondary pairing is

\[
                     \lambda c-\mu b=1.                 \tag{8}
\]

The chosen lower certificate \(x_0\) has
\(\mu Ax_0=\lambda Tx_0=2\), so the same value is obtained on the reduced
leading residual:

\[
                     \lambda(c+Tx_0)=1.                 \tag{9}
\]

On the five-row common-factor fibre, solving the three displayed lower
cycle rows changes the leading packet \(D\) to \(4D\), and the normalized
leading cochain has \(\lambda(D)=1/4\). Thus the previously isolated relative
\(4D\) vector is exactly this secondary Schur residual, with pairing one.
The full exact audit is
[the chart-25 lifted-cochain note](n8-chart25-schur-bockstein-dual-lift.md).

The older number three associated with this dual combined the lower raw
pairing with the already reduced leading pairing; it counted
\(\lambda Tx_0=2\) twice. The nonzero obstruction is unchanged, but (8)--(9)
are the correctly typed target values.

## 3. Exact degree-five model

For the full \(n=8\), 24-port balanced Macaulay map, take \(A\) to be the
off-support filtration block through degree four and \(B\) the
minimum-degree-five block reached by one chosen exact degree-four lift.
The fixed leading system has

\[
 49{,}688\text{ rows},\qquad153{,}422\text{ columns},
 \qquad\dim\ker B^*=234
\]

over \(\mathbf F_{1009}\), and its chosen residual is inconsistent.  This
does not obstruct the pure product because it ignores (2).

After adjoining \(T\), equivalently retaining all 14,148 earlier kernel
directions, the exact coupled block has

\[
 72{,}985\text{ rows},\qquad224{,}153\text{ columns},
 \qquad\dim\ker M^*=81.
\]

Thus 153 of the 234 leading dual classes are killed by their nonzero
source-relative connecting class.  Every one of the 81 surviving coupled
duals annihilates the target.  Rational reconstruction and exact replay
then give

\[
                    H_0H_1H_2\in I_{\rm mix}+J^6.
\]

This is the first large exact calculation in the repository where the
secondary comparison is not merely an analogy: \(A,B,T\) are literal
filtered source-incidence maps, and (2) is their canonical connecting map.

## 4. Faster higher-filtration algorithm

The criterion avoids closing the new row space under every raw old-column
tail.  At filtration degree \(d\):

1. close the chosen degree-\(d\) target residual under the leading block
   \(B_d\);
2. compute \(Z_{B_d}=\ker B_d^*\);
3. for each leading class stream the old-column tail to obtain
   \([\lambda T_d]\) modulo \(\operatorname {row}A_{<d}\);
4. discard classes with nonzero connecting image; and
5. test (4) only on \(\ker\partial_d\).

This is the dual form of carrying every lower-filtration kernel vector, but
it can be much smaller.  It also cleanly separates two outcomes: a nonzero
connecting class is a repair direction, while a zero connecting class with
nonzero target pairing is a genuine source-provenant obstruction.

## 5. Relation to the uniform proof target

The clean-pair frontier has repeatedly required a Bockstein/Yoneda-type
comparison that remembers literal source lifts.  Lemma (2)--(4) gives the
minimal linear-algebraic model of that comparison:

* \(B\)-cokernel classes are the apparent boundary or rootless residues;
* \(T|_{\ker A}\) is precisely their lift indeterminacy; and
* only \(\ker\partial\) supports a single-valued physical readout.

A uniform proof still has to identify the corresponding literal
connection/normal/curvature blocks on the selected cap family and show that
the surviving class has the required target or odd-residue value.  The
finite \(n=8\) calculation proves that this mechanism is real and can remove
false obstructions; it does not by itself construct the uniform clean-pair
complex or prove Krenn's conjecture.
