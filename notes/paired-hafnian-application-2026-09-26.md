# Paired hafnians: a known inequality and an explicit stability consequence

September 26, 2026. **Research follow-up; not independently audited.**
The qualitative inequality below already follows from prior work. The
quantitative consequence is recorded here with a proof and exact examples;
no priority claim is made for it.

[Explainer](../explainers/RATE-FOLLOWUPS.md) ·
[Exact replay](../computations/rate-sharpness-followup-2026-09-26/README.md)

## The external question and its existing answer

A [2022 MathOverflow question](https://mathoverflow.net/questions/421553/a-question-about-an-inequality-for-hafnians-of-some-special-matrices)
asks whether a complex symmetric matrix \(S\), with \(SJ\) Hermitian
positive semidefinite and \(J\) swapping adjacent pairs, satisfies
\(\operatorname{Re}\operatorname{haf}S\ge\prod_i S_{2i-1,2i}\).

Reorder the first member of each pair before the second members. Symmetry
of \(S\) and Hermiticity of \(SJ\) give

\[
 S=\begin{pmatrix}Y&B\\B^T&\overline Y\end{pmatrix},\qquad
 Y=Y^T,\quad B=B^*\succeq0.
\]

For this block matrix, the expansion in
[Brádler–Friedland–Israel, Section 2, equation (2.1)](https://arxiv.org/html/1811.10342)
groups matchings by their numbers of pairs inside each half:

\[
 \operatorname{haf}S=\sum_{k=0}^{\lfloor r/2\rfloor}
 \sum_{|I|=|J|=2k}
 \operatorname{haf}Y[I]\,
 \operatorname{per}B[I^c,J^c]\,
 \overline{\operatorname{haf}Y[J]} .                 \tag{1}
\]

Here \(B,Y\) have size \(r\), and empty hafnians and permanents are one.
Every sector is nonnegative, by positivity of the corresponding permanental
compound. The \(k=0\) sector is \(\operatorname{per}B\). The classical
permanent analogue of Hadamard's inequality for positive semidefinite
matrices ([Marcus's inequality, recalled in Frenkel, equation (2)](https://arxiv.org/pdf/0704.0028)) therefore gives

\[
 \operatorname{haf}S\ge\operatorname{per}B\ge\prod_i B_{ii}.
                                                               \tag{2}
\]

This answers the posted question using existing mathematics. The full
assumption \(SJ\succeq0\) is stronger than needed: \(B\succeq0\) suffices.
Finding the connection is useful, but is not a new resolution of an open
conjecture attributable to this workspace.

## A quantitative consequence

Suppose \(r\ge2\) and \(B\succeq bI\), where \(b>0\). Then

\[
 \boxed{\operatorname{haf}S-\operatorname{per}B
 \ge\sum_{k=1}^{\lfloor r/2\rfloor}b^{r-2k}
       \sum_{|I|=2k}|\operatorname{haf}Y[I]|^2
 \ge b^{r-2}\sum_{i<j}|Y_{ij}|^2.}                 \tag{3}
\]

For completeness, diagonalize \(B\) with a unitary matrix. On the symmetric
\(s\)-fold tensor space the induced operator has eigenvalues given by
products of \(s\) eigenvalues of \(B\), hence is at least \(b^s I\).
The normalized basis vectors with no repeated index are orthonormal, and
the corresponding matrix entries are \(\operatorname{per}B[U,V]\).
Thus its principal submatrix on these vectors is also at least \(b^s I\).
Apply this to each sector of (1), with \(s=r-2k\). Keeping \(k=1\)
gives the last inequality because a two-site hafnian is its single edge.

The coefficient one in the final inequality is sharp: take \(B=bI\)
and let \(Y\) have only one nonzero off-diagonal pair. There are no higher
nonzero sectors, and equality holds. Choose that entry of modulus at most
\(b\) if the additional condition \(SJ\succeq0\) is desired.

## What this lets us infer

If the excess hafnian is at most \(\varepsilon\), then

\[
 \sum_{i<j}|Y_{ij}|^2\le\varepsilon/b^{r-2}.
\]

Thus near equality controls the off-diagonal within-half correlations when
the cross block has a positive spectral floor. The diagonal entries of
\(Y\) never enter a hafnian and cannot be controlled by this estimate.
As \(b\) approaches zero, the conclusion loses strength: degeneracy matters
here too. The replay includes complex examples, equality cases, and a
diagonal-entry counterguard.

The reusable idea is to group a matching sum into positive quadratic forms
before estimating its size. This connects the workspace's two-copy viewpoint
to an established matrix-inequality framework; it does not require or extend
the Krenn–Gu impossibility theorem itself.
