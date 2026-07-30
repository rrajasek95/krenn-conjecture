# A rank-two shore has a two-label kernel

## 1. Outcome

Let \(h\ge1\), let \(|W|=2h\), and work in the site-square-zero algebra
\(\bigotimes_{y\in W}(\mathbb C\oplus V_y)\), where \(V_yV_y=0\) and
each \(V_y\) has the fixed basis \(e_0^{(y)},e_1^{(y)},e_2^{(y)}\).
Suppose the complete fixed-label pair equations are

\[
 a_{ij}q^{[h]}+p_i s_jq^{[h-1]}=\delta_{ij}X_i,
 \qquad 0\le i,j\le2.
\tag{1}
\]

Write \(P:\mathbb C^3\to\bigoplus_{y\in W}V_y\) for
\(P(e_i)=p_i\), and assume \(P\) is injective.  The audited exceptional
shore theorem excludes
\(\operatorname {rank}P_{\bar x}\le1\).  This note records the fixed-label
structure at the next boundary.

**Theorem 1.1 (rank-two shore coordinate support).**  If

\[
 \operatorname {rank}P_{\bar x}=2
\tag{2}
\]

and \(0\ne c\in\ker P_{\bar x}\), then \(c\) has at most two nonzero
coordinates in the fixed row basis.  If it has exactly two, the nonzero
local vector \(P_x(c)\) is proportional to one of the corresponding two
physical coordinate axes at \(x\).

The assertion is uniform in \(h\) and has a transposed version for the
second endpoint star.

If both endpoint stars have rank two away from the same site \(x\), let
\(c,d\) span the two kernel lines.  Then either

\[
 q^{[h]}\in\operatorname {span}\{X_r,X_s\}
\quad\text{for at most two labels }r,s,
\tag{3}
\]

or

\[
 c_i d_i=0\qquad(i=0,1,2).
\tag{4}
\]

Thus the common-coloop obstruction to disjoint selector packing is not
generic: it routes to a zero, unary, or binary internal matching power, or
to two disjoint fixed-coordinate kernel supports.  These alternatives are
inclusive rather than mutually exclusive.

## 2. A one-row tensor lemma

Let \(V\) have fixed basis \(e_0,e_1,e_2\), let \(Z\) contain independent
nonzero vectors \(Y_0,Y_1,Y_2\), and suppose

\[
 b_jQ+u\otimes h_j=c_j e_j\otimes Y_j
 \qquad(j=0,1,2)
\tag{5}
\]

for \(0\ne u\in V\), \(Q\in V\otimes Z\), \(h_j\in Z\), and scalars
\(b_j,c_j\).

**Lemma 2.1.**  The support of \((c_0,c_1,c_2)\) has size at most two.  If
it has size two, \(u\) is proportional to one of the two corresponding
basis vectors.

**Proof.**  Let \(\pi:V\to V/\mathbb Cu\), and put
\(\bar Q=(\pi\otimes1)Q\).  Projecting (5) gives

\[
 b_j\bar Q=c_j\pi(e_j)\otimes Y_j.
\tag{6}
\]

First suppose \(\bar Q=0\).  For every \(j\) with \(c_j\ne0\), equation
(6) forces \(\pi(e_j)=0\), so \(u\parallel e_j\).  This can occur for at
most one fixed basis vector.

Now suppose \(\bar Q\ne0\).  Among the active indices \(j\) for which
\(c_j\ne0\), at most one can have \(\pi(e_j)\ne0\).  Indeed, for every
such index (6) forces \(b_j\ne0\) and makes the same nonzero tensor
\(\bar Q\) proportional to
\(\pi(e_j)\otimes Y_j\).  Two different active indices would make
\(\bar Q\) proportional to pure tensors with independent \(Z\)-factors
\(Y_j,Y_k\), which is impossible.

There is also at most one active index with \(\pi(e_j)=0\), because
\(\pi(e_j)=0\) means \(u\parallel e_j\).  Hence there are at most two
active indices in total.  If there are two, exactly one has zero
projection, so \(u\) is proportional to its coordinate axis.  \(\square\)

## 3. Application to a full-nine shore

Fix \(x\) satisfying (2).  Its kernel is a line.  Choose
\(0\ne c\in\ker P_{\bar x}\) and put

\[
 u=P_x(c).
\tag{7}
\]

Injectivity of \(P\) gives \(u\ne0\).  Set

\[
 Q=q^{[h]},\qquad
 q_0=q|_{W\setminus\{x\}},\qquad
 h_j=(s_j|_{W\setminus\{x\}})q_0^{[h-1]},\qquad
 Y_j=\bigotimes_{y\ne x}e_j^{(y)}.
\tag{8}
\]

Every term of \(s_jq^{[h-1]}\) which uses site \(x\) collides with
\(P(c)=u\), while restriction to the other sites gives

\[
 P(c)s_jq^{[h-1]}=u\otimes h_j.
\tag{9}
\]

Taking the \(c\)-linear combination of the three rows in column \(j\) of
(1) therefore gives

\[
 (c^{\mathsf T}a)_jQ+u\otimes h_j
       =c_j e_j^{(x)}\otimes Y_j.
\tag{10}
\]

Lemma 2.1 applies verbatim and proves Theorem 1.1.  Transposing the pair
rectangle proves the statement for the second endpoint.

## 4. A common exceptional site

Suppose now that both endpoint stars have rank two away from \(x\).
Choose kernel vectors \(c,d\) and put

\[
 P(c)=u\in V_x,\qquad S(d)=v\in V_x.
\tag{11}
\]

Their product vanishes in the site-square-zero algebra because both
factors occupy \(x\).  Taking the \(c,d\) bilinear combination of all nine
equations (1) gives

\[
 (c^{\mathsf T}ad)\,q^{[h]}
       =\sum_{i=0}^2c_id_iX_i.
\tag{12}
\]

By Theorem 1.1, each of \(c,d\) has fixed-coordinate support at most two.
If \(c^{\mathsf T}ad\ne0\), equation (12) proves (3).  If
\(c^{\mathsf T}ad=0\), independence of \(X_0,X_1,X_2\) gives (4).

Equation (12) does not by itself exclude the common-coloop chart.  Unary
and binary matching powers remain possible, while (4) is a coordinate
kernel alternative.  Its value is to replace the abstract matroid-union
failure by two explicit fixed-label branches which can be coupled to the
scalar-zero response, the diagonal anchors, or an overlapping chart.
