# The fourth-high sole-plane layer: exact four-profile frontier

## 1. Status

Continue from the uniform closure of \(t=r+5\) in
[live-three-zero-sole-plane-third-high-layer-uniform-closure.md](live-three-zero-sole-plane-third-high-layer-uniform-closure.md).
The next sole-plane layer is

\[
                         r\ge7,\qquad t=r+6.                    \tag{1}
\]

This note does **not** close (1).  It gives a uniform Hermite reduction,
closes every profile containing a beta class of multiplicity at least
three, closes the all-distinct sector by full four-anchor endpoint
rigidity, closes a large sparse-double sector, and identifies the exact
first residual at \((r,t)=(7,13)\).

**Theorem 1.1 (closed sectors).**  On the sole-plane layer (1), some
noncoordinate permanent pivot is nonzero in each of the following cases:

1. an exceptional beta class has multiplicity at least three; or
2. all multiplicities are at most two, there is one double class, or there
   are at least two double classes and at least eleven value classes; or
3. all exceptional beta values are distinct.

The inherited coordinate pivot is always nonzero.  Thus the complete
shared-zero response is injective on every listed sector, with arbitrary
beta repetitions, singleton zero beta, row plane, and direct scale.

At the first point, the complete partition count is

\[
                         101=97+4.                              \tag{2}
\]

The four profiles not closed here are

\[
 2^3 1^7,\qquad 2^4 1^5,\qquad 2^5 1^3,\qquad 2^6 1.          \tag{3}
\]

The all-distinct profile reduces to a cubic Robin determinant with a
genuine identity branch; a bare degree-eight root count cannot close it.
The full DR4 theorem proves that this is the only identity branch, and
overlapping four-cores then give a quadratic-fibre contradiction.

## 2. Five-special \(P_r\) and inherited \(S_r\)

Use the normalization and notation of the preceding sole-plane notes.  The
exceptional live set has

\[
                         |E|=r+6.                               \tag{4}
\]

There are \(r-6\) common-beta live sites.  Together with the two type-
\(10\) centres put

\[
 A=(U\setminus E)\sqcup\{c,d\},\qquad |A|=r-4.                \tag{5}
\]

The active sites are \(A\sqcup\{e\}\).  The noncoordinate family is

\[
\begin{aligned}
 &m\in E,\qquad E\setminus\{m\}=L\sqcup R,
 \qquad |L|=r,\quad |R|=5,\\
 &P_{m;L\mid R}
  =\mathcal C_r\bigl(\nu_L\mid(1^{[r-5]},\nu_R)\bigr).        \tag{6}
\end{aligned}
\]

The coordinate and extra-block family is

\[
\begin{aligned}
 &B\subset E,\quad |B|=2,\qquad E\setminus B=L\sqcup R,
 \qquad |L|=r,\quad |R|=4,\\
 &S_{B;L\mid R}
  =\mathcal C_r\bigl(\nu_L\mid(1^{[r-4]},\nu_R)\bigr).        \tag{7}
\end{aligned}
\]

Omit one label \(q\in E\).  On the remaining \(r+5\) labels, (7) is
exactly a \(P_r\) pivot from the now-closed layer \(t=r+5\), with the old
marked label joined to \(q\) to form \(B\).  Hence some \(S_r\) pivot is
always nonzero.

The literal response is the same shore-count template as before.  In the
noncoordinate case, put a target \(v\in A\) with \(L\) on one shore and
\((A\setminus\{v\})\sqcup R\) on the other.  Removing the target leaves
\(r\) sites on each shore, and a nonzero (6) kills both binary target rows;
the centre third rows are literal zero-row singletons.  A nonzero (7) then
kills the extra block, and the common-live third rows follow triangularly.
For the coordinate plane, the other \(r-4\) active sites together with the
four labels of \(R\) balance \(L\), so (7) performs every binary and third-
row cleanup.  Source \(22\) removes the direct \(B_{01}\) term identically.

## 3. One-deletion Hermite degree

Fix five labels \(R\) and put

\[
                         N=E\setminus R,\qquad |N|=r+1.        \tag{8}
\]

Simultaneous row and column confluence in Borchardt's identity gives the
same \((r+1)\)-by-\(r\) squared-Cauchy numerator jet matrix as in the
preceding layer.  If every one-label deletion (6) vanished while this
matrix had rank \(r\), its one-dimensional left kernel would be supported
below the top row jets.  The associated rational function would have
numerator degree at most \(q_{\rm rep}-2\le r-1\), but the \(r\) column
jets would give \(r\) zeros counting multiplicity.  Partial-fraction
uniqueness is a contradiction.  Therefore the global matrix has rank less
than \(r\).

If \(m_R\) exceptional value classes occur in \(R\), a nonzero column
dependence is

\[
 F_R(z)={Q_R(z)\over D_R(z)},\qquad
 D_R(z)=(z+1)^{r-4}\prod_y(z+y)^{r_y+1}.                       \tag{9}
\]

The degree calculation is again

\[
 \deg D_R=r+m_R+1,\qquad \deg Q_R\le r+m_R-1.                 \tag{10}
\]

The \(r+1\) row jets divide \(Q_R\), so the residual degree is at most
\(m_R-2\):

\[
\begin{array}{c|ccccc}
m_R&1&2&3&4&5\\ \hline
\deg(Q_R/P_N)&\text{impossible}&0&1&2&3.
\end{array}                                                     \tag{11}
\]

This unchanged \(m_R-2\) rule is the reusable part of the next-layer
attack.

## 4. Multiplicity at least five

If \(a\) occurs at least five times, choose five copies for \(R\).  With

\[
                         h_i={\nu_i+a\over\nu_i+1}\ne0,
 \qquad j=r-5,                                                 \tag{12}
\]

the pivot is a nonzero structural factor times

\[
                         5!j!\,e_j(h_i:i\in L).                \tag{13}
\]

If all \(r+1\) one-deletion values vanished, summing them would give

\[
 \sum_{m\in N}e_j(N\setminus\{m\})=(|N|-j)e_j(N)=6e_j(N)=0. \tag{14}
\]

The identity
\(e_j(N)=e_j(N\setminus\{m\})+h_me_{j-1}(N\setminus\{m\})\)
then descends to \(e_0=0\), a contradiction.  This closes every class of
multiplicity at least five.

## 5. Multiplicity three or four

Let a value \(u\) occur at least three times and select

\[
                         R=\{u,u,u,b,c\}.                      \tag{15}
\]

There are three selected value classes, so (11) supplies a nonzero affine
residual \(\ell_{bc}\).  At the two simple selected poles its undivided
Robin equations have the form

\[
 \ell_{bc}'(-b)=Y_b(c)\ell_{bc}(-b),\qquad
 Y_b(c)=A_b+{c+3b\over c^2-b^2}.                              \tag{16}
\]

The pair compatibility, triangle resultant, and four-anchor contradiction
of the preceding layer apply verbatim: if four distinct value classes are
available besides \(u\), two candidate triangles force an opposite pair.
Thus every such profile with at least five value classes is closed.

It remains to inspect four-class profiles.  With four values \(a,b,c,d\),
selecting \(j=3\) copies of a moving class \(u\) changes the fixed-anchor
constant by

\[
                         {j+1\over u-b}-{j\over u+b}.          \tag{17}
\]

Comparing the choices \(u=a,c\) and \(u=a,d\) gives, respectively,

\[
 jab+ac+b^2+jbc=0,\qquad jab+ad+b^2+jbd=0.                   \tag{18}
\]

Their difference forces \(a=-jb\), and the first equation becomes
\((1-j^2)b^2=0\).  For \(j=3\), this contradicts \(b\ne0\).
This closes \(4,4,3,2\), \(4,3,3,3\), and all later four-repeated-class
boundaries.

At \(r=7\), the remaining four-class profile is \(4^3 1\).  If the
singleton value \(b\ne0\), the same exchange uses it as anchor and again
forces \(b=0\).  On the boundary \(b=0\), choose
\(R=\{b,u,u,u,u\}\) as \(u\) ranges over the three four-class values.
Here \(m_R=2\), the residual is constant, and the simple-pole equation at
zero contains the moving term

\[
 \chi_4(0,u)={4\over u}-{5\over u}=-{1\over u}.               \tag{19}
\]

Three distinct nonzero values cannot have the same reciprocal.  Hence no
profile containing a class of multiplicity three or four remains.

## 6. Two degree-eight sparse-double lemmas

Assume all parts are one or two.  Two exact determinants close the sparse
sector.

**Lemma 6.1 (one selected double).**  Fix a double value \(u\), two other
classes \(a,b\), and let \(x\) vary in

\[
                         R_x=\{u,u,a,b,x\}.                    \tag{20}
\]

The residual \(H_x\) is quadratic.  At the simple anchors \(a,b\), use the
two first-order Robin equations.  At the selected double pole \(-u\), put

\[
\begin{aligned}
 U_x&=U-{x+3u\over x^2-u^2},\\
 W_x&=W+{1\over(u+x)^2}+{2\over(x-u)^2}.
\end{aligned}                                                  \tag{21}
\]

Absence of the simple term at the order-three pole is

\[
 H_x''(-u)+2U_xH_x'(-u)+(U_x^2+W_x)H_x(-u)=0.                 \tag{22}
\]

After multiplying the two simple rows by \(x^2-a^2,x^2-b^2\) and the
row (22) by \((x^2-u^2)^2\), their determinant has degree at most eight in
\(x\).  It is never identically zero on the structural locus.  Its nine
coefficients generate the unit ideal after adjoining the localizer

\[
 u(a^2-1)(b^2-1)(u^2-1)
 (a-b)(a+b)(a-u)(a+u)(b-u)(b+u).                              \tag{23}
\]

Therefore at most eight distinct moving values are possible.  A one-double
profile has \(r+5\ge12\) value classes, hence at least nine choices after
fixing \(u,a,b\), and is closed.

**Lemma 6.2 (two selected doubles).**  Fix two double values \(u,v\) and
let

\[
                         R_x=\{u,u,v,v,x\}.                    \tag{24}
\]

The residual is affine.  Apply the order-three condition (22) at both
\(-u\) and \(-v\), omitting the \(H''\) term.  After clearing
\((x^2-u^2)^2(x^2-v^2)^2\), the determinant of the two coefficient rows has
degree at most eight.  Its coefficient ideal is a unit after localizing at

\[
 uv(u^2-1)(v^2-1)(u-v)(u+v).                                 \tag{25}
\]

Thus, if there are at least eleven value classes, the \(q-2\ge9\) moving
choices contradict the degree bound.  This proves Theorem 1.1.

For a singleton/double profile with \(d\) doubles, the number of value
classes is \(q=r+6-d\).  Lemmas 6.1--6.2 close \(d=1\) and every
\(2\le d\le r-5\).  The possible dense tail is

\[
                         d\ge r-4,qquad
                         d\le\left\lfloor{r+6\over2}\right\rfloor. \tag{26}
\]

It is finite in \(r\): (26) is empty for \(r\ge15\).  At \(r=7\), it is
exactly \(d=3,4,5,6\), the first four profiles in (3).

## 7. The all-distinct cubic DR4 closure

Suppose all exceptional values are distinct.  Fix four nonzero anchors
\(C=\{a,b,c,d\}\), let \(x\) range over \(E\setminus C\), and put

\[
                         R_x=C\sqcup\{x\}.                     \tag{27}
\]

The last line of (11) gives a nonzero cubic \(H_x\).  At an anchor \(y\),
write

\[
 Y_y(x)=U_y(C)+\psi(y,x),\qquad
 \psi(y,x)={1\over y+x}-{2\over x-y}
           =-{x+3y\over x^2-y^2}.                             \tag{28}
\]

The Robin row on the coefficients of a cubic is

\[
 \bigl(3y^2-y^3Y_y,\ -2y+y^2Y_y,\ 1-yY_y,\ Y_y\bigr).        \tag{29}
\]

Clearing the four quadratic denominators gives a determinant polynomial of
degree at most eight in \(x\).  It has \(|E|-4=r+2\ge9\) distinct roots,
so it is identically zero.

This identity is not itself a contradiction.  The branch

\[
                         U_a(C)=U_b(C)=U_c(C)=U_d(C)=0         \tag{30}
\]

is genuine: the explicit cubic

\[
                         H_x(z)=(z-x)(z+x)^2                  \tag{31}
\]

satisfies every row because

\[
                         {H_x'(-y)\over H_x(-y)}
                          ={x+3y\over x^2-y^2}.               \tag{32}
\]

Thus a proof which merely counts the nine roots of the degree-eight
determinant is invalid.

The identity does, however, satisfy the hypotheses of the full
four-anchor endpoint-rigidity theorem in
[dr4-full-endpoint-rigidity.md](dr4-full-endpoint-rigidity.md).  Indeed,
after clearing (28), the row at \(y\) is

\[
 \mathcal R_y(x)q=(x^2-y^2)\bigl(q'(-y)+U_y(C)q(-y)\bigr)
                         -(x+3y)q(-y).                       \tag{33}
\]

Putting \(t_y=-y\) turns (33) exactly into the DR4 row

\[
 (x^2-t_y^2)\bigl(q'(t_y)+U_y(C)q(t_y)\bigr)
                         -(x-3t_y)q(t_y).                    \tag{34}
\]

The anchors \(t_y\) are distinct, nonzero, and have no opposite pair.
DR4 therefore says that the genuine branch is the only branch:

\[
                         U_y(C)=0\qquad(y\in C).              \tag{35}
\]

The proof of DR4 is uniform on the full structural locus.  Its generic
endpoint matrix has rank fifteen; the three possible rank-drop divisors
are product-pairing charts, closed by localized homogeneous cofactor and
toric certificates.  The saturation and isolated-point audit in
[dr4-full-endpoint-rigidity-independent-audit.md](dr4-full-endpoint-rigidity-independent-audit.md)
checks that no nonstructural point is omitted.

It remains to compare overlapping four-cores.  Write

\[
 U_i(C)=A_i+\sum_{j\in C\setminus\{i\}}\psi(a_i,a_j).         \tag{36}
\]

Fix three nonzero values \(a,b,c\).  For every other eligible nonzero value
\(y\), apply (35) to \(C_y=\{a,b,c,y\}\).  The equation at \(a\) is

\[
 A_a+\psi(a,b)+\psi(a,c)+\psi(a,y)=0,                       \tag{37}
\]

so \(\psi(a,y)\) is constant as \(y\) varies.  There are at least
\((r+6)-1-3=r+2\ge9\) eligible values, since an all-distinct structural
set contains at most one zero.  On the other hand every fibre has size at
most two, because

\[
 \psi(a,y)=\lambda
 \quad\Longleftrightarrow\quad
 \lambda(y^2-a^2)+y+3a=0,                                  \tag{38}
\]

and the polynomial in (38) is never zero identically.  This contradiction
closes the all-distinct sector uniformly for every \(r\ge7\).

For completeness, the earlier quartet certificate remains an independent
linear consequence.  It implies

\[
 \sum_{i\in C}U_i(C)\prod_{j\in C\setminus\{i\}}(a_i+a_j)=0. \tag{39}
\]

Write

\[
 U_i(C)=A_i+\sum_{j\in C\setminus\{i\}}\psi(a_i,a_j).         \tag{40}
\]

The fixed pair contribution simplifies exactly to

\[
 \sum_{i\in C}\left(\prod_{j\ne i}(a_i+a_j)\right)
       \sum_{j\ne i}\psi(a_i,a_j)
                         =9\left(\sum_{i\in C}a_i\right)^2.  \tag{41}
\]

Hence every four-subset of an all-distinct exceptional set must satisfy
the explicit linear equation

\[
 \sum_{i\in C}A_i\prod_{j\in C\setminus\{i\}}(a_i+a_j)
                  +9\left(\sum_{i\in C}a_i\right)^2=0.       \tag{42}
\]

For six sample rational structural anchors, the fifteen equations (42)
have coefficient rank six and augmented rank seven.  This is only a
diagnostic cross-check; the uniform proof is the DR4 and fibre argument
above.

## 8. Exact audit and concrete next steps

[verify_live_three_zero_sole_plane_fourth_high_frontier.py](../computations/verify_live_three_zero_sole_plane_fourth_high_frontier.py)
checks the 101-profile census and the four profiles (3), the five-equal
permanent expansion and deletion descent, and the full residual-degree
table (11).  It reruns the affine Robin triangle resultant, proves the
\(j=3\) four-class exchange and zero-singleton reciprocal boundary, and
reconstructs both degree-eight determinants in Section 6.  Their
coefficient ideals are rerun exactly over \(\mathbb Q\) with the displayed
structural localizers.  The checker verifies the canonical cubic (31), the
quartet simplification (41), and the stated six-core diagnostic.  It also
evaluates the literal \(r=7\) response with repeated beta, singleton zero
beta, inherited \(S_7\), nonzero \(P_7\), and direct scale \(17\).

[verify_live_three_zero_sole_plane_fourth_high_all_distinct_dr4_closure.py](../computations/verify_live_three_zero_sole_plane_fourth_high_all_distinct_dr4_closure.py)
independently constructs the universal cleared determinant, verifies its
sharp degree eight, identifies (33) with the DR4 row under \(t_y=-y\), and
checks both strict cardinality bounds and the quadratic fibre (38).  The
generic, exceptional, and independent full-DR4 checkers all pass.

The next exact attacks are now narrow:

1. couple the degree-eight two-double determinants across the three
   overlapping pairs of double values, beginning with \(2^3 1^7\);
2. compute the leading and endpoint coefficient constraints in the sharp
   cases \(q-2\le8\), looking for an effective degree drop after one pair
   identity is imposed; and
3. saturate the simultaneous pair systems before specializing the
   singleton anchors, so that zero-singleton and vanishing-pivot boundaries
   remain covered.

These are reusable algebraic mechanisms.  Merely checking the four
\((7,13)\) profiles after specializing their beta values would not advance
the prompt's uniform all-even requirement.
