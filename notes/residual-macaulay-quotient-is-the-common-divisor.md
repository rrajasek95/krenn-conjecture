# The residual Macaulay quotient is exactly the common-divisor detector

## 1. Outcome

Let \(S=\mathbb C[u,v]\), let \(h\ge1\), let \(f\in S_h\) be nonzero, and let
\(L'\subseteq S_h\) be a linear space.  The selector--Macaulay reduction
leaves the map

\[
 \mu_{f,L'}:L'\otimes S_{h-1}\longrightarrow
 Q_f:=S_{2h-1}/fS_{h-1}.
\tag{1}
\]

The target has dimension \(h\).  This note records that its rank defect is
not a weaker surrogate for the clean-root problem: it measures the common
divisor exactly.

**Proposition 1.1 (residual rank equals gcd degree).**  Put

\[
 d=\deg\gcd(f,L'),
\tag{2}
\]

where the gcd is taken over \(f\) and every member of \(L'\), and put
\(d=h\) when \(L'=0\).  Then

\[
 \boxed{\operatorname {rank}\mu_{f,L'}=h-d.}
\tag{3}
\]

Consequently, at the first boundary \(h=3\), the proposed bound

\[
 \operatorname {rank}\mu_{f,L'}\le2
\tag{4}
\]

is equivalent to the existence of a projective point at which \(f\) and
every form in \(L'\) vanish.  It becomes a genuine intermediate lemma only
when a literal diagonal/four-cut equation constructs that point (or its
dual evaluation functional) from source data.

## 2. Proof

Let \(I=(f,L')\subseteq S\).  The cokernel of (1) is exactly

\[
 \operatorname {coker}\mu_{f,L'}=(S/I)_{2h-1}.
\tag{5}
\]

Write \(g=\gcd(f,L')\), with \(\deg g=d\), and write

\[
 f=g\bar f,\qquad L'=g\bar L'.
\tag{6}
\]

If \(L'=0\), then \(d=h\) by convention and the map has rank zero.  If
\(L'\ne0\) and \(d=h\), every member of \(L'\) is a scalar multiple of
\(f\), so the map again has rank zero.  We may therefore assume
\(d<h\).  The forms \(\bar f\) and \(\bar L'\) then have positive degree
and gcd one.  A generic \(\bar e\in\bar L'\) is coprime to
\(\bar f\): at each of the finitely many projective roots of \(\bar f\),
nonvanishing excludes one proper hyperplane of \(\bar L'\).  The two
degree-\((h-d)\) forms \(\bar f,\bar e\) therefore form a complete
intersection.  Its quotient vanishes in degrees at least

\[
 (h-d)+(h-d)-1=2h-2d-1.
\tag{7}
\]

It follows that, in degree \(2h-1-d\), the ideal
\((\bar f,\bar L')\) is all of \(S_{2h-1-d}\).  Multiplication by \(g\)
therefore gives

\[
 I_{2h-1}=gS_{2h-1-d}.
\tag{8}
\]

Hence

\[
 \dim(S/I)_{2h-1}
 =\dim S_{2h-1}-\dim S_{2h-1-d}=d.
\tag{9}
\]

Since \(\dim Q_f=h\), equations (5) and (9) prove (3).

## 3. Dual form at \(h=3\)

For \(h=3\), \(Q_f\) is the length-three divisor-evaluation module of
\(V(f)\subset\mathbb P^1\).  If \(f\) is squarefree with roots
\(\lambda_1,\lambda_2,\lambda_3\), then after choosing harmless fibre
trivializations,

\[
 Q_f\simeq\mathbb C_{\lambda_1}\oplus
             \mathbb C_{\lambda_2}\oplus
             \mathbb C_{\lambda_3}.
\tag{10}
\]

The image of (1) has rank at most two exactly when evaluation at one root
\(\lambda_i\) annihilates every \(e\in L'\).  For a nonreduced \(f\), the
dual decomposes into the corresponding evaluation-and-derivative principal
parts, but any positive rank defect still means that \(f\) and \(L'\) have
a common linear factor over \(\mathbb C\).

Thus a successful anchored argument must construct a nonzero covector on
\(Q_f\) that annihilates the image of (1).  Proposition 1.1 then already
forces a common linear factor; the particular covector need not separately
be shown to be evaluation at one reduced point.  The hard step is producing
that annihilator from differently labelled diagonal target coefficients
and the literal overlap equations.

## 4. Two transported anchors are the partial flag-alignment threshold

The need for differently labelled anchors has an elementary flag form.

**Lemma 4.1 (two-anchor partial flag rigidity).**  Let
\(A,B\in\operatorname {GL}_3(\mathbb C)\), and let \(r\ne s\).  If

\[
 A^{-\mathsf T}E_{rr}B^{-1},\qquad
 A^{-\mathsf T}E_{ss}B^{-1}
\tag{11}
\]

are nonzero diagonal matrices, then there are distinct coordinate labels
\(k,\ell\) such that

\[
\begin{aligned}
 A^{-\mathsf T}e_r&\parallel e_k,&
 B^{-\mathsf T}e_r&\parallel e_k,\\
 A^{-\mathsf T}e_s&\parallel e_\ell,&
 B^{-\mathsf T}e_s&\parallel e_\ell.
\end{aligned}
\tag{12}
\]

Thus the two transported target anchors recover the literal
fixed-coordinate two-label flag needed for a \(2\times2\) row/column
rectangle on their two label planes.

**Proof.**  A nonzero rank-one diagonal matrix is supported on exactly one
diagonal cell.  Since

\[
 A^{-\mathsf T}E_{cc}B^{-1}
 =(A^{-\mathsf T}e_c)(B^{-\mathsf T}e_c)^{\mathsf T},
\tag{13}
\]

the two factors for \(c=r\) lie on the same coordinate axis \(e_k\), and
the two factors for \(c=s\) lie on the same coordinate axis \(e_\ell\).
The \(r\)- and \(s\)-columns of each invertible matrix are independent, so
\(k\ne\ell\).  This proves (12).  \(\square\)

One anchor fixes only one common axis and leaves an arbitrary oblique
two-plane.  That is exactly the freedom used by the one-anchor guards.
Lemma 4.1 shows that no further local *flag-alignment* theorem is needed
after two anchors have been transported into one selector chart.  One
must still obtain the corresponding coefficient-factorization equations;
the hard step is their source-provenant transport.

## 5. Consequence for the active attacks

The quotient \(Q_f\) remains the right finite ledger: it removes the one
Macaulay block automatically filled by scalar-zero nonnilpotence.  But the
desired one-rank loss in \(Q_f\) is logically equivalent to a common root.
The actual smaller target is therefore the following source-provenant
statement.

> **Multi-anchor diagonal evaluation target.**  Use a
> selector-compatible four-cut, at least two differently labelled diagonal
> target coefficients, and their crossed target-zero row to construct
> \([u:v]\in V(f)\) such that every remaining clean coordinate vanishes at
> \([u:v]\).

The number of anchors here is substantive.  The exact two-chart guard in
[the diagonal/off-diagonal complementarity note](curved-two-chart-offdiagonal-anchor-complementarity.md)
retains curvature, clean endpoints, injective stars, all six off-diagonal
rows, \(q^{[2]}\ne0\), and the complete \(X_0\) physical row, while its
clean coordinates remain coprime.  It fails only the \(X_1,X_2\) anchors.
Thus one diagonal row cannot supply the required evaluation functional.
The three-row pattern in
[the two-dark-colour theorem](uncontracted-four-cut-two-dark-colour-obstruction.md)
shows the minimal plausible interaction: two differently labelled
diagonal anchors plus one crossed zero row.

The cross-word Riccati leakage and the two-chart \(\Omega\)-wedge are two
possible ways for such an evaluation functional to fail to glue.  The
proposed anchored overlap theorem must eliminate those failures; an
unqualified residual-rank assertion only restates the desired clean root.
