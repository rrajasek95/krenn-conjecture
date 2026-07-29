# Independent audit of the centered low-degree rank tradeoff

## Verdict

The local theorem in
[centered-low-degree-rank-tradeoff.md](centered-low-degree-rank-tradeoff.md)
is correct.  After normalizing the invertible \(r\)-to-\(x\) block, the
six mixed equations

\[
 e_c\otimes S_d+b_d\otimes P_c=\lambda_{cd}M,\qquad c\ne d,
 \tag{1}
\]

have only \(P_0=P_1=P_2=S_0=S_1=S_2=0\) when
\(\operatorname{rank}M=2\) and
\(\dim\langle b_0,b_1,b_2\rangle\ge2\).  I reconstructed this directly
from (1), without using the support-case proof in the primary note.

Both threshold witnesses are also exact.  Rank one for the \(b\)-star
allows a rank-two \(M\) with exactly two zero endpoint rows, while rank
one for \(M\) allows an invertible \(b\)-star with exactly two zero
endpoint rows.  Thus neither rank hypothesis can be weakened using the
six off-diagonal equations alone.

## Clean-room reduction

Let \(M_e\) be row \(e\) of \(M\), let

\[
 \alpha_0M_0+\alpha_1M_1+\alpha_2M_2=0
 \tag{2}
\]

span the left-kernel relation, and put
\(\beta_d=\alpha(b_d)\).  Contracting (1) on the left gives

\[
 \alpha_cS_d+\beta_dP_c=0,\qquad c\ne d.                \tag{3}
\]

If \(\alpha_c\ne0\), the two rows \(M_e\), \(e\ne c\), are independent.
Taking those two rows in (1) proves the useful implication

\[
 P_c\ne0\quad\Longrightarrow\quad
 b_d\in\mathbb C e_c\quad\hbox{for both }d\ne c.        \tag{4}
\]

Indeed a nonzero \(\lambda_{cd}\) would make two independent rows of
\(M\) proportional to the one vector \(P_c\); hence
\(\lambda_{cd}=0\), and the two off-\(c\) coordinates of \(b_d\) vanish.
This is the only rank comparison needed below.

## Exhaustion by the support of the kernel relation

### Three-coordinate relation

Assume every \(\alpha_c\ne0\), and let
\(J=\{c:P_c\ne0\}\).

If \(J\) is empty, (3) immediately kills every \(S_d\).  If
\(|J|=1\), for every \(d\) there is a zero \(P_k\) with \(k\ne d\), so
(3) again kills every \(S_d\).  The two equations incident with the
unique nonzero \(P_c\) then compare a rank-one matrix with the rank-two
matrix \(M\), forcing \(b_d=0\) for \(d\ne c\).  The \(b\)-star has rank
at most one, a contradiction.

If \(|J|=2\), say \(P_c,P_e\ne0\) and \(P_k=0\), (4) puts the shared
column \(b_k\) in both \(\mathbb Ce_c\) and \(\mathbb Ce_e\), so
\(b_k=0\).  Equation (3) then kills \(S_k\), while the equations using
the zero row \(P_k\) kill the other two \(S\)'s.  Rank-one versus
rank-two in (1) now makes the two nonzero \(P\)'s kill all three
\(b\)-columns.  Finally, if \(|J|=3\), every \(b_d\) belongs by (4) to
the two distinct coordinate lines indexed by \(c\ne d\), so \(b_d=0\).
Both cases contradict the assumed \(b\)-rank.  Thus \(J\) is empty and
all six endpoint rows vanish.

### Two-coordinate relation

Relabel so that \(\alpha_0\alpha_1\ne0\) and \(\alpha_2=0\).
If both \(P_0,P_1\) are nonzero, (4) gives

\[
 b_0\in\mathbb Ce_1,\qquad b_1\in\mathbb Ce_0,\qquad b_2=0.
\]

Rank at least two makes \(b_0,b_1\) nonzero.  Equation (3) then makes
\(S_0,S_1\) nonzero and \(P_2=0\), but the \((2,0)\) equation is the
nonzero rank-one tensor \(e_2\otimes S_0\) equal to a multiple of
rank-two \(M\), a contradiction.

Suppose \(P_0\ne0\) and \(P_1=0\).  Equation (3) gives
\(S_0=S_2=0\), while (4) gives \(b_1,b_2\in\mathbb Ce_0\).
The \((0,2)\) equation forces \(b_2=0\).  Rank at least two then makes
\(b_0\) nonzero and outside \(\mathbb Ce_0\); the \((2,0)\) equation
forces \(P_2=0\), the \((2,1)\) equation forces \(S_1=0\), and the
\((0,1)\) equation finally forces \(b_1=0\).  Only \(b_0\) remains,
again a contradiction.  The case \(P_1\ne0,P_0=0\) is symmetric.

Consequently \(P_0=P_1=0\).  Equations (3) kill all \(S_d\).  If
\(P_2\ne0\), the \((2,0)\) and \((2,1)\) equations force
\(b_0=b_1=0\), leaving \(b\)-rank at most one.  Hence \(P_2=0\).

### One-coordinate relation

Relabel so that \(\alpha_2\ne0\) and
\(\alpha_0=\alpha_1=0\).  Then \(M_2=0\) and \(M_0,M_1\) are
independent.

If \(P_2\ne0\), (4) gives \(b_0,b_1\in\mathbb Ce_2\).  The
\((1,0)\) equation has left image in
\(\langle e_1,e_2\rangle\), whereas \(M\) has left image
\(\langle e_0,e_1\rangle\); it therefore forces \(b_0=0\).
The \((0,1)\) equation similarly forces \(b_1=0\), leaving \(b\)-rank
at most one.  Thus \(P_2=0\), and the \(c=2\) equations give
\(S_0=S_1=0\).

The \((0,1)\) and \((1,0)\) equations now give
\(b_1P_0=b_0P_1=0\).  Both \(P_0,P_1\) cannot be nonzero, since then
only \(b_2\) could survive.  If only \(P_0\) is nonzero, the
\((1,2)\) equation kills \(S_2\), and the \((0,2)\) equation kills
\(b_2\); together with \(b_1=0\), this again leaves rank at most one.
The case with only \(P_1\) nonzero is symmetric.  Therefore all
\(P\)'s and all \(S\)'s vanish.

This proves the uniform implication over characteristic zero.

## Independent exact census

I also reused the equation-matrix machinery of the earlier independent
one-invertible audit, not the new primary checker.  For each finite field,
I normalized the first star to \(e_0,e_1,e_2\), enumerated the zero vector
and every projective vector for each \(b_d\), retained exactly the
\(b\)-matrices of rank at least two, and used one right-equivalence
representative for every rank-two left image of \(M\).

For each homogeneous solution space, every one of the eighteen endpoint
coordinates was tested for a nonzero projection.  The results were:

* over \(\mathbb F_2\), all \(3234\) normalized classes had zero endpoint
  projection;
* over \(\mathbb F_3\), all \(34476\) normalized classes had zero endpoint
  projection.

This is stronger than finding no all-row-nonzero solution: every solution
in every enumerated class has all six endpoint vectors zero.  The census
is an exact finite-field falsification audit, while the preceding
support proof supplies the characteristic-zero theorem.

## Sharp witnesses

The first witness has

\[
\begin{aligned}
 &(b_0,b_1,b_2)=(0,0,(1,1,0)),\\
 &M=\begin{pmatrix}-1&-1&0\\-1&0&0\\0&0&0\end{pmatrix},\\
 &(P_0,P_1,P_2)=((1,0,0),(-1,-1,0),(1,1,1)),\\
 &(S_0,S_1,S_2)=(0,0,(0,1,0)),
\end{aligned}
\]

with multipliers
\((0,-1,0,1,0,0)\) in order
\((01),(02),(10),(12),(20),(21)\).
Direct multiplication verifies (1).  Here
\(\operatorname{rank}M=2\), the \(b\)-rank is one, the \(P\)-matrix is
invertible, and exactly \(S_0,S_1\) vanish.

For the second witness take

\[
\begin{aligned}
 &(b_0,b_1,b_2)=(e_0,e_0+e_2,e_0+e_1),\qquad M=e_0e_0^T,\\
 &(P_0,P_1,P_2)=(0,e_0,e_0),\qquad
 (S_0,S_1,S_2)=(0,-e_0,-e_0),
\end{aligned}
\]

with multipliers \((-1,-1,1,1,1,1)\).  The \(b\)-matrix is invertible,
\(M\) has rank one, and exactly \(P_0,S_0\) vanish.  These computations
confirm the precise scope stated in the primary note: diagonal target
equations or overlapping-chart compatibility are genuinely needed
beyond the local mixed system.

