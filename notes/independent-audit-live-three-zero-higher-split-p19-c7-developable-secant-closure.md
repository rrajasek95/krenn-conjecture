# Independent audit: the \(p=19,C=7\) developable-secant closure

## Verdict

**PASS.**  I reconstructed the proof in
`live-three-zero-higher-split-p19-c7-developable-secant-closure.md`
without using its geometric checker as an oracle.  The two profiles

\[
 2^9 1^{h+3},\qquad 3\,2^8 1^{h+2}
\]

are excluded.  The common-four-space saturation, the parity-quotient
degree, the developability argument, and both terminal signed-zero counts
remain valid after allowing degree drops, common Pluecker factors, and
ramification at infinity.

## 1. Saturated four-space

The two selections have

\[
 (P,N;\mathbf m)=(6,11;2^7),\qquad(5,10;3,2^6).
\]

Each moving transport is a three-space
\({\cal T}_q=(z-q)^2(z+q){\cal S}_q\) inside the common kernel
\({\cal K}\).  The inherited five-space estimate gives
\(\dim {\cal K}\leq4\).  If its dimension were three, every
\({\cal T}_q\) would equal \({\cal K}\); pairwise nonopposition makes the
\(P\) cubics coprime, so every member would be divisible by a polynomial
of degree \(3P>N\).  Thus \(\dim {\cal K}=4\).

For a primitive four-space, an exact order-\(m\) row costs at least
\(4-m\).  The two finite totals are

\[
 6\cdot3+7\cdot2=32=4(11-3),\qquad
 5\cdot3+1+6\cdot2=28=4(10-3).
\]

A common zero of order \(g<m\) changes the local lower bound to
\(4g+4-(m-g)=5g+4-m\), which is strictly larger; \(g=m\) forces another
common zero after division, and \(g>m\) costs at least \(4g\).  Hence
there is no finite base point.  A zero pool value would replace
\((0,2,3,4)\) by at least \((0,3,4,5)\), adding three units.  Equality
therefore gives sequence \((0,2,3,4)\) at every pool value and no
unaccounted ramification.

This equality also handles infinity, a point that is easy to miss.  If
the echelon degrees are \(n_0<\cdots<n_3\leq N\), then
\(\deg\operatorname{Wr}({\cal K})\leq\sum n_i-6\leq4N-12\).
The finite rows already attain \(4N-12\), so
\((n_0,n_1,n_2,n_3)=(N-3,N-2,N-1,N)\), the leading Wronskian coefficient
is nonzero, and the homogenized point map has neither a base point nor
ramification at infinity.  In particular its point line is exactly
\({\cal L}_F={\cal O}_{\mathbb P^1_z}(-N)\).

## 2. Parity quotient, including its common gcd

Writing \(F=(A_0,\ldots,A_3)\), the hyperplane
\({\cal T}_q\) is both evaluation kernels, so
\([F(q)]=[F(-q)]\).  Saturation says

\[
 F'(q)\in\langle F(q)\rangle,\qquad
 F'(-q)\notin\langle F(-q)\rangle.
\]

The parity wedge \(W(z)=F(z)\wedge F(-z)\) is divisible by
\(H_P(z)=z\prod_q(z^2-q^2)\).  Its degree is at most \(2N-1=2P+9\), so
\(W/H_P\) is an even vector polynomial of degree at most eight, hence a
six-tuple of polynomials of degree at most four in \(x=z^2\).

The pool roots are exactly simple as vector roots.  Indeed, after scaling
\(F(-q)=\mu F(q)\),

\[
 W'(q)=-F(q)\wedge F'(-q)\ne0.
\]

Consequently the divided Pluecker vector is nonzero at \(x=q^2\) and
represents the line
\(\langle F(q),F'(-q)\rangle\).  Thus its common gcd has no pool-square
factor.  Remove its full homogeneous gcd, including any factor at
infinity, and lower the chosen homogeneous degree if all leading
coefficients vanish.  The result is a base-point-free morphism

\[
 \ell:\mathbb P^1_x\longrightarrow\operatorname{Gr}(2,4),
 \qquad d=\deg\ell\leq4,
\]

and every pool fiber still contains \([F(q)]\).  This proves the exact
claim needed later even when the quotient has a degree drop or a
nontrivial common factor away from the pool.

The rank-zero parity case is also genuinely excluded.  If every minor
vanished, primitivity would give \(F(-z)=cF(z)\) with constant
\(c=\pm1\).  The odd case has common factor \(z\); in the even case
stationarity at \(q\) forces stationarity at \(-q\), contradicting the
regular unlisted negative point.  Thus \(\ell\) exists.  It is not
constant: a constant secant line would contain every generic \(F(z)\),
forcing the four coordinate polynomials to be linearly dependent.

## 3. Developability

For the pulled-back tautological sequence, \(\deg\det{\cal S}=-d\) and
\(\deg\det{\cal Q}=d\).  Therefore

\[
 \det\beta\in
 H^0\!\left((\det{\cal S})^*\otimes\det{\cal Q}
                 \otimes(\Omega^1)^2\right)
 =H^0({\cal O}(2d-4)).
\]

At a nonzero pool value, \(x=z^2\) is a valid local coordinate and the
stationary section \(F(\sqrt x)\) lies in \(\ker\beta\).  Five distinct
pool squares exceed \(2d-4\leq4\), so \(\det\beta=0\).  Since \(\ell\)
is nonconstant, \(\beta\) has generic rank one.  Its saturated kernel
line \({\cal R}\) gives an edge point curve \(\gamma\).  Differentiating
a section of \({\cal R}\) shows that either \(\gamma\) is constant and
\(\ell\) is a cone, or \(\ell\) is generically the tangent-line curve of
\(\gamma\).  This remains true if \(\gamma\) or \(\ell\) has isolated
critical points.

## 4. Cone branch

For a cone, \({\cal R}={\cal O}\) and
\({\cal S}/{\cal R}={\cal O}(-d)\).  A direction image contained in a
line sweeps a fixed plane and contradicts independence, so the direction
coordinates form a base-point-free spanning \(g^2_d\); in particular
\(d\geq2\).  If \(c\) pool squares are critical, their weight at least
two in its degree-\(3(d-2)\) Wronskian gives

\[
 2c\leq3(d-2).
\]

After the square cover, projection away from the vertex is the nonzero
bundle map

\[
 {\cal O}(-N)\longrightarrow{\cal O}(-2d).
\]

At every noncritical pool square, \(\ker\beta\) is precisely the vertex,
so both distinct points \(z=q\) and \(z=-q\) are zeros.  Hence
\(2(P-c)\leq N-2d\).  Combining the inequalities yields
\(P\leq d-1\leq3\), contrary to \(P\geq5\).  Ignoring zeros at critical
pool squares only weakens the contradiction, so no multiplicity
assumption is hidden here.

## 5. Tangent-edge branches

A planar edge again makes the four coordinates dependent; a nonplanar
edge has \({\cal R}={\cal O}(-e)\) with \(e\geq3\).

For a decomposable Klein hyperplane, every tangent line meets one fixed
line \(L_0\).  If \(u,v\) cut out \(L_0\), this condition is

\[
 (u\circ\gamma)(v\circ\gamma)'-(v\circ\gamma)(u\circ\gamma)'=0.
\]

Thus the rational projection \([u\circ\gamma:v\circ\gamma]\) is
constant in characteristic zero, including all degree-drop cases.  The
edge lies in a plane through \(L_0\), a contradiction.

For a symplectic Klein hyperplane, \({\cal Q}\simeq{\cal S}^*\) and
\(\beta\) is symmetric.  Since

\[
 \deg({\cal S}/{\cal R})=(-d)-(-e)=e-d,
\]

the induced nonzero rank-one quotient form is a section of

\[
 (({\cal S}/{\cal R})^*)^{\otimes2}\otimes\Omega^1
       ={\cal O}(2(d-e)-2).
\]

Nonnegativity, \(d\leq4\), and \(e\geq3\) leave only
\((d,e)=(4,3)\).  The quotient form then has degree zero and never
vanishes, so every pool stationary point equals the edge point.  Here
\({\cal S}/{\cal R}={\cal O}(-1)\); after the square cover the nonzero
quotient map is

\[
 {\cal O}(-N)\longrightarrow{\cal O}(-2).
\]

Both \(q\) and \(-q\) map to the same edge fiber and are distinct zeros.
The map cannot vanish identically, because then the two generic branches
would span only the one-dimensional edge point rather than \(\ell(x)\).
Its zero divisor has degree \(N-2\), forcing
\(2P\leq N-2=P+3\), false for \(P=5,6\).

## 6. Independent executable check

`audit_live_three_zero_higher_split_p19_c7_developable_secant_closure.py`
recomputes the profile numbers, all Wronskian and bundle degrees, the
homogeneous degree-drop bounds, the exact local divided wedge at a pool
square, and every terminal inequality.  It does not import or call the
original C7 checker.
