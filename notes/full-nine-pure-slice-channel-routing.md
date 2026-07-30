# A pure full-nine row forbids the mislabelled unary-channel guard

## 1. Outcome

Work on the six residual sites with the complete pair equations

\[
 a_{ij}q^{[3]}+p_i s_jq^{[2]}=\delta_{ij}X_i,
 \qquad 0\leq i,j\leq2.                                  \tag{1}
\]

Fix an off-diagonal direct entry

\[
                         \alpha=a_{ab}\ne0,
                         \qquad a\ne b.                 \tag{2}
\]

At a constant physical colour \(d\), let \(I_d\) and \(J_d\) be the
fixed-label row channels which actually occur in the two endpoint-star
scalarizations.  Put \(F_d=\operatorname {haf}(Q_d)\).  The full pure
row gives the following exact routing dichotomy:

\[
 \boxed{\begin{array}{ll}
 F_d\ne0:
   &(P_d^{\mathsf T}H(Q_d)S_d)_{ab}=-\alpha F_d\ne0,
     \quad a\in I_d,\ b\in J_d;\\[1mm]
 F_d=0:
   &P_d^{\mathsf T}H(Q_d)S_d=E_{dd},
     \quad d\in I_d\cap J_d.
 \end{array}}                                           \tag{3}
\]

Thus a missing colour cannot be confined at both endpoints to one
*wrong* latent channel.  More precisely, if

\[
                         I_d=J_d=\{k\},
                         \qquad k\ne d,                 \tag{4}
\]

then (1) is impossible for every \(q\) and every direct matrix having a
nonzero off-diagonal entry.

This excludes the exact simultaneous unary/common-cofactor-hole guard of
Section 7 of
[the common-power audit](curved-pure-binary-three-channel-common-power-independent-audit.md)
with its displayed endpoint factorization.  On physical colour \(1\),
that guard has \(I_1=J_1=\{0\}\); on physical colour \(2\), it has
\(I_2=J_2=\{1\}\).  Either pure row already contradicts (3).  The
conclusion is stronger than the recorded failure of the guard's displayed
common quadratic: **no replacement \(q\), and no replacement direct block
\(a\) with off-diagonal curvature, can complete those same stars to the
full nine rows.**

The scope is deliberately narrow.  It does not exclude a correctly
labelled singleton channel with a hafnian-zero pure \(q\)-slice, a singleton
cross-channel carrying the distinguished curvature cell itself, or a
deconcentrated missing-colour packet.  Hence it does not prove the general
missing-colour full-nine response/cohafnian lemma and is not an
eight-site obstruction.

## 2. Fixed-label channel supports

For the constant word \(d^6\), let \(Q_d\) be the scalar internal edge
matrix and let \(P_d,S_d\in\operatorname {Mat}_{6\times3}(\mathbb C)\)
be the endpoint-star scalarizations.  Define

\[
 I_d=\{i:(P_d)_{*,i}\ne0\},
 \qquad
 J_d=\{j:(S_d)_{*,j}\ne0\}.                            \tag{5}
\]

Put

\[
 F_d=\operatorname {haf}(Q_d),
 \qquad
 M_d=P_d^{\mathsf T}H(Q_d)S_d.                         \tag{6}
\]

The constant-word member of the full-nine cohafnian identity is

\[
                         M_d=E_{dd}-F_da.               \tag{7}
\]

By definition of \(I_d,J_d\), the left side has the fixed-label support
restriction

\[
                         \operatorname {supp}M_d
                              \subseteq I_d\times J_d.  \tag{8}
\]

No change of endpoint-row basis is made in (5)--(8).  This is important:
the target cell \(E_{dd}\) and the curvature cell \(a_{ab}\) use the same
global labels at every word.

## 3. Pure-slice curvature routing lemma

**Lemma 3.1.**  Under (1)--(2), the alternative (3) holds for every
physical colour \(d\).

**Proof.**  If \(F_d\ne0\), the off-diagonal \((a,b)\)-entry of (7) is
\[
                  (M_d)_{ab}=-F_da_{ab}=-F_d\alpha\ne0.
\]
The support restriction (8) then forces \(a\in I_d\) and \(b\in J_d\).

If \(F_d=0\), equation (7) becomes

\[
                         M_d=E_{dd}.                    \tag{9}
\]

Its \((d,d)\)-entry is nonzero.  The product description (6) consequently
forces both column \(d\) of \(P_d\) and column \(d\) of \(S_d\) to be
nonzero.  Thus \(d\in I_d\cap J_d\), proving (3).  \(\square\)

One useful singleton refinement records all escapes rather than only the
contradiction used here.

**Corollary 3.2 (singleton classification).**  Suppose

\[
                         I_d=\{i\},\qquad J_d=\{j\}.
\]

Then \(M_d=\lambda E_{ij}\) for some scalar \(\lambda\), and exactly one
of the following is possible.

1. \(F_d=0\), \(i=j=d\), and \(\lambda=1\).
2. \(F_d\ne0\) and
   \[
                     a=F_d^{-1}(E_{dd}-\lambda E_{ij}). \tag{10}
   \]
   If \(a\) has a nonzero off-diagonal entry, then necessarily
   \(i\ne j\), \(\lambda\ne0\), and that sole off-diagonal cell is
   \((i,j)\).

In particular \(i=j\ne d\) is impossible in an off-diagonal packet.

**Proof.**  The support inclusion (8) gives
\(M_d=\lambda E_{ij}\).  If \(F_d=0\), equation (7) reads
\(\lambda E_{ij}=E_{dd}\), which is precisely the first case.  If
\(F_d\ne0\), rearranging (7) gives (10).  Its asserted support is
immediate.  \(\square\)

The first case is a real boundary of this argument, not a removable
technicality.  At one scalar word, take \(Q_{01}=Q_{23}=1\) and all other
edges zero.  Then \(F_d=0\) while \(H(Q_d)_{45}=1\).  Taking only the
target-labelled endpoint rows \(p_d\) at site \(4\) and \(s_d\) at site
\(5\) gives \(M_d=E_{dd}\).  This is only a one-word scalar packet, but it
shows why the conclusion of Lemma 3.1 must retain the aligned hafnian-zero
escape.

## 4. Application to the exact unary/common-hole guard

Use the stars displayed in equations (A16)--(A17) of the independent
common-power audit.  In the present notation the first endpoint rows are

\[
\begin{aligned}
 p_0&=(x_{0,0}+x_{4,0})+i(x_{0,1}+x_{1,1}),\\
 p_1&=(x_{1,0}+x_{3,0})+i(x_{0,2}+x_{2,2}),\\
 p_2&=x_{2,0},
\end{aligned}                                             \tag{11}
\]

and the second endpoint has the same decorated supports (with the
nonzero scalar changes recorded there).  Consequently

\[
                         I_1=J_1=\{0\},
                         \qquad I_2=J_2=\{1\}.          \tag{12}
\]

For \(d=1\), (12) is the forbidden singleton pattern \(k=0\ne1\).
Equivalently, the pure sandwich is supported only at \((0,0)\), whereas
the full row is

\[
       \lambda E_{00}=E_{11}-F_1a.                    \tag{13}
\]

If \(F_1=0\), (13) equates two distinct matrix units.  If \(F_1\ne0\),
(13) makes \(a\) diagonal, contrary to (2).  The colour-two row gives the
same contradiction with \(E_{11}\) and \(E_{22}\).

This proof uses neither the six-edge common quadratic of the guard nor its
enumeration of 729 words.  It uses the fixed endpoint labels and one of the
three omitted diagonal anchors.  In particular, changing the common
quadratic cannot repair the guard while retaining its displayed stars.

## 5. Exact remaining gate

Lemma 3.1 routes, but does not close, a general missing colour \(d\).
Every full-nine counterguard must lie on exactly one of the following
pure-slice ledgers:

* \(F_d\ne0\), in which case the distinguished off-diagonal endpoint
  channels \(p_a\) and \(s_b\) both occur and have the nonzero cohafnian
  pairing
  \[
       (P_d^{\mathsf T}H(Q_d)S_d)_{ab}
                         =-\alpha\operatorname {haf}(Q_d)\ne0;
  \]
* \(F_d=0\), in which case the complete sandwich is the
  exact fixed-label biorthogonality \(E_{dd}\).

Thus the common-hole mechanism cannot remain a mislabelled unary latent
channel.  It must either carry the curvature channel itself or pay an
aligned hafnian-zero-\(q\) boundary.  Excluding those two source-provenant
possibilities, especially when \(I_d,J_d\) are not singletons, is the
remaining full-nine cohafnian problem.
