# Independent audit: the uniform developable-secant lemma

## Verdict

**PASS, with the exact common-lift hypotheses retained.**  I reconstructed
[the uniform lemma](live-three-zero-higher-split-uniform-developable-secant-lemma.md)
without calling its checker.  The theorem is valid for positive integral
fixed multiplicities, exact baseline jet rows,

\[
 M_4=(P-1)+\sum_{i=1}^C\min(m_i,4)=19,\qquad
 4\leq C\leq7,\qquad P\geq\max(1,2C-9).
\]

The proof does not silently require the raw parity-quotient degree to be
attained.  Finite common factors, a factor at infinity, a lower actual
Plücker degree, critical edge points, and zeros of the rank-one second
fundamental form all remain covered.  The four stated \(p=20\)
one-quintuple families really do supply the common-lift setup.

This is a conditional higher-split exclusion, not a proof of the global
conjecture and not a result for \(M_4>19\), \(C\geq8\), or a pool below the
displayed threshold.

## 1. The common kernel is exactly a primitive four-space

Put

\[
 N=P+C-2,\qquad
 M_5=(P-1)+\sum_i\min(m_i,5).
\]

Since passing from cap four to cap five adds at most one unit per fixed
class,

\[
 M_5\leq19+C\leq26.
\]

If the common kernel \(\mathcal K\) contained a five-space, its \(P\)
exact simple rows and \(C\) fixed exact rows would force Wronskian weight

\[
 4P+\sum_i\max(0,5-m_i)
 =5P+5C-M_5-1.
\]

The degree-\(N\) cap is \(5(P+C-6)\), so the forced weight exceeds it by
\(29-M_5>0\).  Therefore \(\dim\mathcal K\leq4\).

Every moving transport

\[
 \mathcal T_q=(z-q)^2(z+q)\mathcal S_q
\]

is three-dimensional.  If \(\dim\mathcal K=3\), all \(\mathcal T_q\)
coincide.  Nonopposition makes their \(P\) cubic factors pairwise
coprime, so three independent members require

\[
 3P\leq N-2=P+C-4.
\]

But the theorem range gives \(2P>C-4\), hence the strict reverse
inequality.  Thus \(\dim\mathcal K=4\).

For a primitive four-space, an exact order-\(m\) row contributes at least
\(\max(0,4-m)\).  Consequently the finite forced weight is

\[
\begin{aligned}
 3P+\sum_i\max(0,4-m_i)
 &=3P+4C-\sum_i\min(m_i,4)\\
 &=4P+4C-20\\
 &=4(N+1-4),
\end{aligned}
\]

which is the full Wronskian cap.

I checked every gcd branch rather than assuming primitivity.  At an
exact order-\(m\) row, a common zero of order \(g<m\) changes the local
cost to

\[
 4g+\max(0,4-m+g)>\max(0,4-m).
\]

If \(g=m\), the exact highest-jet coefficient forces the reduced section
to vanish too, contradicting maximality of the gcd.  If \(g>m\), the
cost \(4g\) is already strictly larger.  A common root away from a
listed row adds at least four units.  Since the nominal rows already
consume the whole cap, no finite gcd is possible.

A zero moving value is also impossible.  The three members of
\(\mathcal T_0=z^3\mathcal S_0\), together with a fourth independent
member and primitivity, give vanishing sequence at least
\((0,3,4,5)\), of weight six instead of the allotted three.  Hence every
moving value is nonzero, and equality gives sequence
\((0,2,3,4)\) at every pool point.

Infinity is not an omitted base point.  If the echelon degrees are
\(n_0<\cdots<n_3\leq N\), then

\[
 \deg\operatorname{Wr}(\mathcal K)
 \leq\sum_i n_i-6\leq4N-12.
\]

The finite rows already contribute \(4N-12\).  Therefore the only
possible degrees are

\[
 (n_0,n_1,n_2,n_3)=(N-3,N-2,N-1,N),
\]

the leading Wronskian coefficient is nonzero, and the point line of the
homogenized map is exactly \(\mathcal O_{\mathbb P^1_z}(-N)\).  This
simultaneously excludes a base point and ramification at infinity.

## 2. The parity quotient survives every homogeneous degree drop

Choose a basis of \(\mathcal K\) and write its point map as \(F(z)\).
At a pool value \(q\), dimension and saturation give

\[
 \ker E_q=\mathcal T_q=\ker E_{-q},\qquad
 F'(q)\in\langle F(q)\rangle,\qquad
 F'(-q)\notin\langle F(-q)\rangle.
\]

The last assertion uses both nonopposition, which makes \(-q\) an
unlisted point, and the already proved absence of any unlisted
ramification.

The odd wedge \(W(z)=F(z)\wedge F(-z)\) has degree at most \(2N-1\) and
is divisible by

\[
 H_P(z)=z\prod_{q\in P}(z^2-q^2).
\]

Thus

\[
 \frac{W(z)}{H_P(z)}=Q(z^2),\qquad
 \deg_x Q\leq C-3.
\]

Every removed pool root is exactly simple as a **vector** root.  After
scaling \(F(-q)=\mu F(q)\),

\[
 W'(q)=-F(q)\wedge F'(-q)\ne0.
\]

Hence no common coordinate factor of \(Q\) contains a pool square, and
the divided pool fiber is the genuine line
\(\langle F(q),F'(-q)\rangle\).

Now homogenize all six coordinates, remove their complete homogeneous
gcd—including a factor supported at infinity—and lower the homogeneous
degree if the leading coefficient vector vanishes.  This produces a
base-point-free map

\[
 \ell:\mathbb P^1_x\longrightarrow\operatorname{Gr}(2,4),
 \qquad 1\leq d\leq C-3,
\]

without losing any pool incidence.

The two endpoints in this assertion are justified.  If \(Q=0\),
primitivity gives \(F(-z)=cF(z)\) with \(c=\pm1\).  The odd case gives a
common factor \(z\); the even case transfers stationarity from \(q\) to
\(-q\), contradicting saturation.  If \(\ell\) were constant, every
generic \(F(z)\) would lie in one fixed two-dimensional vector space,
forcing two linear dependencies among the four basis polynomials.

Finally, the coefficient vectors of \(Q\) span a space of dimension at
most

\[
 (C-3)+1=C-2\leq5
\]

inside the six-dimensional Plücker space.  A nonzero Klein hyperplane
therefore contains the entire curve.  Its alternating form has rank two
(decomposable) or rank four (symplectic); there is no third rank branch
in dimension four.

## 3. Stationarity forces a developable line curve

For the pulled-back tautological sequence, let

\[
 \beta:\mathcal S\longrightarrow
       \mathcal Q\otimes\Omega^1_{\mathbb P^1}
\]

be the second fundamental form.  Since
\(\det\mathcal S=\mathcal O(-d)\) and
\(\det\mathcal Q=\mathcal O(d)\),

\[
 \det\beta\in H^0(\mathcal O(2d-4)).
\]

At each nonzero moving \(q\), \(x=z^2\) is a local coordinate and
\(F(\sqrt x)\) is a stationary local section of the secant line.  Hence
all \(P\) distinct pool squares are zeros of \(\det\beta\).  Uniformly
over every actual degree drop,

\[
 P\geq2C-9>2C-10\geq2d-4.
\]

(For \(C=4\), the explicit \(P\geq1\) hypothesis is stronger than the
possibly negative first bound.)  Therefore \(\det\beta=0\).  The map
\(\ell\) is nonconstant in characteristic zero, so \(\beta\) has
generic rank one.  Its saturated kernel
\(\mathcal R=\mathcal O(-e)\) supplies the edge point curve.  A constant
edge gives a cone; a nonconstant edge gives the tangent-line curve of
the edge away from isolated critical points.  These are the complete
developable alternatives needed below.

## 4. Every terminal branch is impossible

### Cone

For a constant vertex, \(\mathcal R=\mathcal O\) and the direction
curve is a base-point-free spanning \(g^2_d\).  Otherwise all secant
lines lie in one fixed plane, contradicting independence of the four
basis polynomials.  Thus \(d\geq2\).

If \(c\) pool squares are critical for the direction curve, each costs
at least two in its degree-\(3(d-2)\) Wronskian:

\[
 2c\leq3(d-2).
\]

Projection from the vertex after the square cover is a nonzero map

\[
 \mathcal O(-N)\longrightarrow\mathcal O(-2d).
\]

It cannot vanish identically: that would make the entire point curve
equal the vertex, contradicting independence of the four coordinate
polynomials.

At every noncritical pool square, stationarity forces the point to equal
the vertex.  The two distinct signed preimages \(q,-q\) are therefore
zeros, so

\[
 2(P-c)\leq N-2d.
\]

Combining the two inequalities gives

\[
 P\leq C+d-8\leq2C-11,
\]

contrary to \(P\geq2C-9\).  Zeros at infinity can only consume more of
the available degree.

### Decomposable tangent hyperplane

A nonplanar edge has degree \(e\geq3\).  If the Klein form is
\(\omega=u\wedge v\), the tangent-line condition is

\[
 (u\circ\gamma)(v\circ\gamma)'
 -(v\circ\gamma)(u\circ\gamma)'=0.
\]

After cancelling a common factor, this is the numerator of the
derivative of the rational projection
\([u\circ\gamma:v\circ\gamma]\).  In characteristic zero the projection
is constant, so the edge lies in a plane through the fixed projection
line.  This includes the cases where the edge meets or lies in the
center.  A planar edge makes all its tangent lines, and hence the
generic \(F(z)\), planar; that contradicts the four-dimensional basis.

### Symplectic tangent hyperplane

For a symplectic form, \(\mathcal Q\simeq\mathcal S^*\) and \(\beta\)
is symmetric.  With \(k=d-e\), its rank-one quotient is a nonzero
section

\[
 \overline\beta\in H^0(\mathcal O(2k-2)).
\]

Thus \(k\geq1\), and at most \(s\leq2k-2\) pool squares can be zeros of
this quotient form.  At every remaining pool square the stationary
point is the edge point.  The nonzero signed quotient map

\[
 \mathcal O(-N)\longrightarrow
 \pi^*(\mathcal S/\mathcal R)=\mathcal O(-2k)
\]

therefore yields

\[
 2(P-s)\leq N-2k.
\]

This quotient map cannot vanish identically either.  Otherwise both
generic signed branches \(F(z),F(-z)\) would lie in the one-dimensional
edge fiber, although their nonzero wedge spans the two-dimensional
secant fiber.

The form degree and zero count are retained here; no unspoken
nowhere-vanishing assumption is used.  Since \(d\leq C-3\leq4\),
\(e\geq3\), and \(k\geq1\), the sole possible tuple is

\[
 (C,d,e,k)=(7,4,3,1).
\]

Then \(s=0\), and the sharper signed count gives

\[
 2P\leq N-2=P+C-4,\qquad P\leq C-4=3,
\]

contradicting the required \(P\geq5\).  The cone, decomposable tangent,
and symplectic tangent cases exhaust the proof.

## 5. The \(p=20\) application has the required quantifiers

For the four profiles

\[
 5\,3^a2^{7-a}1^{h+3-a},\qquad 0\leq a\leq3,\quad
 13\leq h\leq19,
\]

select two double classes and \(h-2\) singleton layers, then vary the
last selected singleton.  The exact common-lift data are

\[
\begin{array}{c|c|c|c}
a&P&N&\text{fixed multiplicities}\\ \hline
0&6&10&5,2,2,2,2,2\\
1&5&9&5,3,2,2,2,2\\
2&4&8&5,3,3,2,2,2\\
3&3&7&5,3,3,3,2,2.
\end{array}
\]

Each row has \(C=6\), \(M_5=20\), \(M_4=19\), and
\(P\geq3=2C-9\).

The relation-three-space premise is not an extra assumption.  Pair
drops give selected-kernel dimension at least four.  For \(p=20\) and
\(13\leq h\leq19\), the \(q=6\) selected-row gap is

\[
 22-h+\max(0,6-(20-h))>0,
\]

so the dimension is at most five.  The already proved low-role
incidence theorem excludes dimension four.  Thus a hypothetical
configuration is either already contradictory or has dimension exactly
five, whose row-relation space has dimension three and supplies the
setup used by the uniform lemma.

The next \(C=6\) pool has only \(P=2\), exactly enough roots for a
degree-two determinant, and the \(C=7\) pools have \(P\leq4<5\).
Those profiles are correctly left open by this lemma.

## 6. Independent executable check

[audit_live_three_zero_higher_split_uniform_developable_secant_lemma.py](../computations/audit_live_three_zero_higher_split_uniform_developable_secant_lemma.py)
imports none of the proposed checker or census modules.  It exhausts all
attainable cap-four patterns, rather than merely sampling \(P,C\);
enumerates every homogeneous Plücker degree drop, cone critical-point
budget, and symplectic edge degree; reconstructs all four \(p=20\)
selections for every \(h\); and checks the local divided-wedge and
decomposable-projection identities exactly.
