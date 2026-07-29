# Higher splits: the saturated Klein-plane closure at \(p=19, C=6\)

## 1. Result

Continue from the common-four-space and global parity-rank theorems in
[the \(C=6\) parity-pencil coupling](live-three-zero-higher-split-p19-c6-parity-pencil-coupling.md).
Write \(P\) for the moving pool.  The only \(C=6\) profiles not covered
there with \(P\geq2\) have \(P=6,7,8\).

**Theorem 1.1 (saturated Klein-plane closure).**  None of the residual
\(p=19\), \(C=6\) configurations in table (3), equivalently none of the
four families in (1), can exist.

Consequently the following four residual families are impossible:

\[
 \boxed{
  2^8 1^{h+5},\qquad
  3\,2^7 1^{h+4},\qquad
  3^2 2^6 1^{h+3},\qquad
  4\,2^7 1^{h+3}.}
                                                               \tag{1}
\]

Together with the preceding \(C=6\) theorem, this closes ten of the
twelve \(C=6\) families.  The complete \(p=19\) ledger becomes
\(85/94\), with nine families remaining.  The two unclosed \(C=6\)
families both have \(P=1\), so there is no second moving value to which
the present secant-line argument can be applied.

## 2. Exact saturation of the common four-space

Let

\[
        {\cal K}\subseteq\mathbb C[z]_{\leq N},\qquad
        \dim {\cal K}=4,\qquad N=P+4                         \tag{2}
\]

be the common space constructed in the preceding theorem.  At each of
the \(P\) pool values there is an exact order-one row.  The six fixed
rows have multiplicities as follows:

\[
\begin{array}{c|c|c}
P&\text{fixed multiplicities}&\text{fixed mass}\\ \hline
8&2,2,2,2,2,2&12\\
7&3,2,2,2,2,2&13\\
6&3,3,2,2,2,2&14\\
6&4,2,2,2,2,2&14.
\end{array}                                                    \tag{3}
\]

Thus the fixed mass is always \(20-P\).  An exact order-\(m\) row on a
four-space has minimal local vanishing sequence obtained by omitting
\(m\) from \(0,1,2,3,4\), and hence has Wronskian weight \(4-m\).
The forced finite weight is therefore

\[
  3P+\sum_{i=1}^6(4-m_i)
       =3P+24-(20-P)=4P+4.                                   \tag{4}
\]

This is exactly the full four-space cap

\[
             4(N+1-4)=4P+4.                                  \tag{5}
\]

No pool value can be zero.  If \(q=0\), then
\({\cal T}_0=z^3{\cal S}_0\) is a three-space of sections vanishing to
order at least three at zero.  Together with a fourth independent
section, this forces local vanishing sequence at least

\[
                            (0,3,4,5),                         \tag{5a}
\]

of Wronskian weight six.  This is three units larger than the order-one
row contribution used in (4), so the total forced weight would exceed
(5).  Hence every pool value in a hypothetical configuration is
nonzero.

There is no hidden gcd case in this equality.  Indeed, if a common gcd
has local order \(g>0\) at an exact order-\(m\) row and \(g<m\), division
by the gcd changes the minimal weight to

\[
             4g+4-(m-g)=5g+4-m>4-m.                          \tag{6}
\]

The case \(g=m\) is impossible because the exact row then kills the
leading coefficient of every reduced section, contradicting maximality
of \(g\); if \(g>m\), the local weight \(4g\) is again strictly larger.
A gcd root away from the displayed rows contributes at least four new
units.  Hence any nonconstant gcd would make (4) exceed (5).

It follows that \({\cal K}\) is base-point-free, equality holds at every
displayed row, and there is no other ramification, including at
infinity.  In particular, at every pool value \(q\) the local vanishing
sequence is exactly

\[
                         (0,2,3,4).                            \tag{7}
\]

Let \({\cal T}_q=f_q{\cal S}_q\) be the transported three-space, where
\(f_q=(z-q)^2(z+q)\).  Since \({\cal T}_q\subseteq\ker E_q\) and both
spaces have dimension three, while every member of \({\cal T}_q\) also
has zero derivative at \(q\) and zero value at \(-q\), (7) gives

\[
       {\cal T}_q=\ker E_q=\ker E_{-q},
       \qquad D_q\in\mathbb C E_q.                            \tag{8}
\]

Thus the map defined by \({\cal K}\) is projectively stationary at
\(q\), and its values at \(q\) and \(-q\) agree.  At a nonzero \(-q\),
on the other hand, its projective derivative is nonzero: otherwise
\(-q\) would be an additional Wronskian root of weight at least three,
contrary to saturation.  Here the structural nonopposition hypothesis is
essential: for nonzero \(q\), the value \(-q\) is neither another pool
value nor one of the six fixed row values.

## 3. The degree-three secant-line curve

Choose a basis \(A_0,\ldots,A_3\) of \({\cal K}\), and put

\[
                   F(z)=(A_0(z),\ldots,A_3(z)).               \tag{9}
\]

The row vector \(F(z)\) represents evaluation at \(z\).  Set

\[
 C(x)=\prod_{q\text{ in the pool}}(x-q^2).                   \tag{10}
\]

The squares in (10) are distinct and nonzero.  For \(i<j\), define

\[
 Q_{ij}(x)=
 {A_i(z)A_j(-z)-A_i(-z)A_j(z)\over zC(z^2)},
 \qquad x=z^2.                                                \tag{11}
\]

The numerator is odd and the global parity divisor proves that (11) is
a polynomial.  Its degree in \(x\) is at most three, because the
numerator has \(z\)-degree at most \(2N-1=2P+7\), whereas the divisor
has degree \(2P+1\).

None of the pool squares is a common zero of the six \(Q_{ij}\).  At a
pool value \(q\), (7) makes the positive branch projectively stationary,
while the preceding paragraph makes the negative branch regular.  Their wedge
therefore has a simple zero in \(x-q^2\).  Up to a nonzero scalar, its
divided value is

\[
            F(q)\wedge\bigl(F'(-q)\bmod F(q)\bigr),           \tag{11a}
\]

so the extended line \(\ell(q^2)\) contains \(F(q)\).

After removing any common factor away from the pool, the six coordinates
in (11) define a morphism

\[
 \ell:\mathbb P^1_x\longrightarrow
       \operatorname{Gr}(2,{\cal K}^*)\subseteq
       \mathbb P(\wedge^2{\cal K}^*).                         \tag{14}
\]

For generic \(x=z^2\), \(\ell(x)\) is precisely the projective line
spanned by \(F(z)\) and \(F(-z)\); (11a) gives its extension at every
pool square.  The degree of (14) with respect to the Pluecker hyperplane
bundle is at most three.

The six coordinate polynomials in (11) are the coordinate images of the
global parity map \(\Phi_{\cal K}\).  The preceding parity-rank theorem
therefore says that the linear span of \(\ell(\mathbb P^1)\) has
projective dimension at most two.

## 4. Klein lines and beta planes are impossible

First, \(\operatorname{rank}\Phi_{\cal K}=0\) is impossible.  If all the
parity minors vanished identically, the standard primitive parity
argument would give

\[
                         {\cal K}={\cal V}(z^2)               \tag{14a}
\]

after removal of the gcd; the gcd is constant by Section 2.  Indeed,
proportionality of the primitive vectors \(F(z)\) and \(F(-z)\) has a
scalar ratio with constant denominator, and applying the involution
twice makes that scalar \(1\) or \(-1\); the odd case would give the
forbidden common factor \(z\).  The projective map would consequently be
even.  At any nonzero pool value, stationarity at \(q\) would then imply
stationarity at \(-q\), contradicting the last paragraph of Section 2.
Every pool value is nonzero by Section 2.  Equivalently, the exact
pool-square quotients in Section 3 already show directly that not all
\(Q_{ij}\) vanish.

If the span of (14) is a point or a line in the Klein quadric, the flag
classification of Klein lines puts every \(\ell(x)\) inside one fixed
projective plane \(\mathbb P(W)\subseteq\mathbb P({\cal K}^*)\), with
\(\dim W=3\).  The same conclusion holds if the span is a beta plane in
the Klein quadric.

But \(F(z)\in\ell(z^2)\subseteq\mathbb P(W)\) for generic \(z\).  A
nonzero vector in the annihilator of \(W\) would then give a constant
linear combination of \(A_0,\ldots,A_3\) vanishing identically.  This
contradicts the choice of a basis.  Hence the span is neither a point, a
Klein line, nor a beta plane.

## 5. Alpha planes are impossible

Suppose the span is an alpha plane.  All lines \(\ell(x)\) then pass
through one fixed point \([w]\in\mathbb P({\cal K}^*)\).  The curve must
span that plane: if it were contained in a line, all its lines would also
lie in a fixed projective plane, the case just excluded.

Let \(d\leq3\) be the degree of the resulting nondegenerate morphism
\(\mathbb P^1\to\mathbb P^2\).  Necessarily \(d=2\) or \(3\).  Its
three-section Wronskian has total weight

\[
                              3(d-2).                          \tag{15}
\]

A point at which \(d\ell=0\) has vanishing sequence at least
\((0,2,3)\), hence costs at least two units in (15).  Consequently
\(d\ell\) can vanish at at most one point.

Now let \(q\ne0\) be a pool value for which \(d\ell_{q^2}\ne0\).  Locally
write

\[
              \ell(x)=\mathbb P\langle w,v(x)\rangle,
 \qquad F(\sqrt{x})=a(x)w+b(x)v(x).                           \tag{16}
\]

Nonvanishing of \(d\ell\) says that \(v'(q^2)\) is nonzero modulo
\(\langle w,v(q^2)\rangle\).  Projective stationarity of \(F\) at \(q\)
says that the derivative of the second expression in (16) is a multiple
of its value.  Reducing that derivative modulo
\(\langle w,v(q^2)\rangle\) gives

\[
                         b(q^2)v'(q^2)=0.                     \tag{17}
\]

Thus \(b(q^2)=0\), so \(F(q)=[w]\).

There is no zero pool value and at most one critical pool square.  Hence
a set \(S\) of at least \(P-1\) pool values has
\(F(q)=[w]\).  By (8), all \({\cal T}_q\), \(q\in S\), are then the same
three-dimensional hyperplane.  Every member of that hyperplane is
divisible by the pairwise coprime cubics \(f_q\), \(q\in S\).  A
three-space of degree-\(N\) multiples of their product can exist only if

\[
                         3|S|\leq N-2=P+2.                    \tag{18}
\]

But \(|S|\geq P-1\), and \(3(P-1)>P+2\) for \(P>5/2\).  This excludes
the alpha-plane case.

## 6. A genuine conic is impossible

It remains to consider a plane span not contained in the Klein quadric.
Its intersection with the quadric is a plane conic.  Because the image
of \(\mathbb P^1\) is irreducible and spans the plane, this conic cannot
be a pair of lines or a doubled line; it is smooth.

A smooth plane conic in \(\operatorname{Gr}(2,4)\) whose span is not a
Klein plane is one ruling of a smooth quadric surface.  To see the
relevant classification directly, pull the tautological two-bundle back
to the normalized conic \(\mathbb P^1\).  Its determinant is
\({\cal O}(-2)\), so it splits either as
\({\cal O}\oplus{\cal O}(-2)\) or as
\({\cal O}(-1)\oplus{\cal O}(-1)\).  The first splitting supplies a
fixed vector in every line and puts the conic in an alpha plane, already
excluded.  In the second splitting, the fact that the lines span
\({\cal K}^*\) makes the induced map between the two four-spaces an
isomorphism.  Thus there are two-spaces \(A,B\), an identification
\({\cal K}^*=A\otimes B\), and a morphism \([a(x)]\in\mathbb P(A)\)
such that, after possibly exchanging the factors,

\[
                         \ell(x)=\mathbb P(a(x)\otimes B).    \tag{19}
\]

The Pluecker bundle restricts to \({\cal O}_{\mathbb P^1}(2)\) on this
conic.  Since (14) has degree at most three and is nonconstant, its map
to the conic has degree one.  In particular \([a(x)]\) is an
isomorphism and has nonzero derivative everywhere.

Any local point section of (19) has the form

\[
                            p(x)=a(x)\otimes b(x).             \tag{20}
\]

Modulo the line generated by \(p(x)\), its derivative has the nonzero
component

\[
       \overline{a'(x)}\otimes b(x)
           \in (A/\langle a(x)\rangle)\otimes B.             \tag{21}
\]

Thus no point section of this ruling family is projectively stationary.
Choose any pool value \(q\), which is nonzero by Section 2.  The local section
\(p(x)=F(\sqrt{x})\) is projectively stationary at \(x=q^2\) by (7),
contradicting (21).  This excludes the conic case and completes the
proof of Theorem 1.1.

## 7. Exact audit

[verify_live_three_zero_higher_split_p19_c6_saturated_klein_plane_closure.py](../computations/verify_live_three_zero_higher_split_p19_c6_saturated_klein_plane_closure.py)
reconstructs the four-profile census and the \(85/94\) ledger, checks the
four-space saturation, the zero-pool exclusion, and all local vanishing
sequences, audits the degree-three parity quotient, verifies the
standard alpha, beta, and conic Pluecker models, and checks both terminal
degree inequalities.
