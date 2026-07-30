# Independent audit: generic-hafnian apolar lift obstruction

## 1. Verdict

**PASS, with the stated narrow scope.**  The primary-source attribution,
edge-only generator list, Hilbert function, top-apolar reduction, arbitrary
base-extension claim, degree-lowering obstruction, and the exact selected-word
counterpacket in
[the primary note](shafiei-generic-hafnian-apolar-lift-obstruction.md) all
check.

The result rules out a closure obtained from Shafiei's generic-hafnian apolar
ideal, or from the complete scalarized nine-row interface at one mixed word.
It does not rule out a cross-word consequence of the shared physical blocks,
does not prove the proposed cross-word kernel-exclusion lemma, and is not a
counterexample to the global tensor system.  In particular, the words
"weakest" and "smallest" in Section 7 should be read as describing the
targeted output needed to remove the nonzero mixed-response alternative, not
as a theorem that every possible global proof must factor through (43).

No correction to the primary note was needed.  The audited version has
SHA-256

    d4316b6141346a3bc865d975686530a137b3649c24e0725cabad50fcc97cad9c  notes/shafiei-generic-hafnian-apolar-lift-obstruction.md

## 2. Primary-source theorem and conventions

The cited source is Shafiei,
[*Apolarity for determinants and permanents of generic matrices*](https://arxiv.org/abs/1212.0515v2),
arXiv:1212.0515v2.  I checked the v2 TeX source, whose downloaded e-print had
SHA-256

    186b774f52502ae1d5b62b3e9d9ebfbf053ece49ba3d5556ea38b4810e5061b7

The source begins over a field of characteristic zero or characteristic
\(p>2\), defines the apolar action by Macaulay contraction, and states that
ordinary partial differentiation may replace contraction in characteristic
zero or when the characteristic is greater than the degree of the form.
Thus the primary note's restriction to \(\mathbb C\) is safe.

Theorem 4.14 literally states that the apolar ideal of the hafnian of a
generic symmetric \(2n\times2n\) matrix is generated in degree two.  Its proof
first observes that the diagonal dual variables annihilate linearly, restricts
to the generic zero-diagonal symmetric matrix, and invokes the preceding
Pfaffian proof with Pfaffians and hafnians interchanged.  The theorem statement
does not repeat the quadratic list; that list comes from Definition 4.5 in the
Pfaffian proof after changing the four-site signs.  In the edge-only symmetric
ring it is exactly

\[
 Y_{ij}^2,\qquad Y_{ij}Y_{ik},\qquad
 Y_{ij}Y_{kl}-Y_{ik}Y_{jl},\quad
 Y_{ij}Y_{kl}-Y_{il}Y_{jk}.                    \tag{A1}
\]

The signs in the last two generators can be checked without trusting the
paper's terse transfer: all three two-edge contractions on the same four-set
leave the same complementary hafnian.  Hence differences, rather than sums,
annihilate the hafnian.  The primary note handles the diagonal-variable
qualification correctly by defining an edge-only ring before saying that the
quadrics generate \(I\).

There is also no hidden divided-power factor in the application.  Every
hafnian monomial is squarefree.  Operators containing a repeated edge
annihilate under both actions, and on every surviving squarefree operator
monomial Macaulay contraction and ordinary differentiation agree.

## 3. Independent reconstruction of the six-vertex quotient

The exact ideal needed here can be reconstructed directly, independently of
the general theorem.  There are fifteen edge variables, so

\[
                         \dim \mathcal T_2={16\choose2}=120.   \tag{A2}
\]

The degree-two generators in (A1) occupy disjoint monomial sectors:

* 15 edge squares;
* \(6{5\choose2}=60\) products of two distinct incident edges;
* on each of the \({6\choose4}=15\) four-sets, a two-dimensional difference
  space among the three two-edge matchings, for 30 dimensions.

Thus their span has dimension \(15+60+30=105\), leaving a
15-dimensional quotient.  A basis is given by the classes
\(\nu_S\), one for each four-set \(S\), where the three perfect matchings of
\(S\) have the same class.  Degree-two contraction of the six-vertex hafnian
spans the fifteen distinct complementary edge variables, so there are no
additional degree-two annihilators.

In degree three, every monomial containing a repeated edge or an incident
pair is already zero modulo (A1).  The only survivors are the fifteen perfect
matchings of the six vertices.  Four-vertex flips connect the perfect-matching
graph, and every flip is one of the balanced differences in (A1) multiplied
by the untouched third edge.  All survivors therefore have the same class

\[
                 \mu=\overline{Y_{01}Y_{23}Y_{45}}.            \tag{A3}
\]

This class is nonzero because \(\mu\circ F=1\).  Every degree-four monomial in
edge variables contains a repeated edge or two incident edges: four edges
have eight endpoint incidences but only six vertices.  Hence the quotient
vanishes from degree four onward.  First contractions of \(F\) are the
fifteen complementary four-site hafnians with disjoint monomial supports,
second contractions span the fifteen edge variables, and third contractions
span the constants.  This independently gives

\[
                       H_{\mathcal T/I}=(1,15,15,1)             \tag{A4}
\]

and proves that (A1) generates the full six-vertex apolar ideal.

## 4. Top-apolar identity and base extension

Expand \(\frac12L_Q^2L_R\).  After the preceding reduction, only a perfect
matching \(M\) can survive.  If \(e\in M\) supplies the \(R\)-coefficient,
the other two edges can occur in the two orders in \(L_Q^2\), so the factor
\(\frac12\) removes exactly that multiplicity.  Therefore

\[
\begin{aligned}
 \overline{\frac12L_Q^2L_R}
   &=\left(\sum_{M\in\operatorname{PM}(6)}
       \sum_{e\in M}R_e\prod_{f\in M\setminus\{e\}}Q_f\right)\mu\\
   &=D F_Q(R)\,\mu.                                    \tag{A5}
\end{aligned}
\]

This verifies both the normalization and the claimed equivalence

\[
             \frac12L_Q^2L_R\in I_3
                  \quad\Longleftrightarrow\quad D F_Q(R)=0.    \tag{A6}
\]

The scheme-theoretic statement also survives the strongest advertised
test.  For an arbitrary commutative \(\mathbb C\)-algebra \(B\), scalar
extension gives

\[
        (\mathcal T/I)_3\otimes_{\mathbb C}B=B\mu,              \tag{A7}
\]

a free rank-one \(B\)-module.  Thus \(b\mu=0\) implies \(b=0\), even when
\(B\) has zero divisors or nilpotents.  There is no flatness, reducedness, or
generic-point loophole: the inverse-image membership scheme is cut out by the
single polynomial \(D F_Q(R)\).

One degree lower, multiplication by \(\overline{L_Q}\) is exactly

\[
       m_Q(\nu_S)=Q_{S^c}\mu.                          \tag{A8}
\]

For \(Q\ne0\), this has rank one and a 14-dimensional kernel.  The tangent
equation places \(\overline{L_QL_R}\) in that kernel and supplies no reason
for the class itself to vanish.  This confirms that quadratic generation
cannot be run backwards to obtain \(L_QL_R\in I_2\).

The coefficient-to-algebra-map distinction in Section 4 is also exact.
An assignment \(Y_{xy}\mapsto\rho_{xy}\) factors through the quotient if and
only if the images of all generators in (A1) vanish.  With
\(\rho_{xy}=R_{xy}z_xz_y\) in the site-square-zero marker algebra, the
square and incident generators vanish automatically, while the balanced
generators are precisely the numerical equalities

\[
       R_{ij}R_{kl}=R_{ik}R_{jl}=R_{il}R_{jk}.          \tag{A9}
\]

Ideal membership of \(\frac12L_Q^2L_R\) does not assert (A9).

## 5. All-word family

The polynomial family does not restore the lost information.  Each entry of
\(P(u)^TH(Q(u))S(u)\) is multilinear in the six local probes, so equality on
the \(3^6\) coordinate probes determines the full polynomial identity.  With
\(K_*=\tau E_{ab}-\alpha I\), the coefficient pairing is

\[
       \sum_{i,j}(K_*)_{ij}a_{ij}
          =\tau a_{ab}-\alpha\operatorname{tr}a=0,     \tag{A10}
\]

and every diagonal entry of \(K_*\) is \(-\alpha\).  Contracting the nine
rows therefore gives exactly

\[
 D F_{Q(u)}(R(u))
    =-\alpha\bigl(G_0(u)+G_1(u)+G_2(u)\bigr).          \tag{A11}
\]

Combining (A5) and (A11) proves the displayed family identity in the primary
note.  Its right side is nonzero in the full probe ring, so there is no
extended apolar membership there.  Passing to the quotient by
\(G_0+G_1+G_2\) creates membership, but by (A7) it creates exactly that one
relation and nothing further.  The description as a pulled-back Jacobian
syzygy, rather than a constant-direction apolar problem, is therefore
accurate.

## 6. Exact replay of the selected-word counterpacket

For the all-one off-diagonal \(Q\), direct perfect-matching enumeration gives

\[
                         F(Q)=15,\qquad H(Q)_{xy}=3.     \tag{A12}
\]

Using the six rows in (32), exact rational matrix multiplication gives

\[
 P^TH(Q)S=
 \begin{pmatrix}3&3&-6\\3&3&-6\\3&3&-6\end{pmatrix}.
                                                               \tag{A13}
\]

Hence the displayed \(a=-M/15\) satisfies the complete nine-entry mixed
identity.  Its trace is zero, \(a_{01}=-1/5\), and the physical definition
of the contracted block gives

\[
                         K_*=\frac15I.                 \tag{A14}
\]

Both endpoint matrices have rank three.  The response calculation leaves
exactly

\[
 R_{01}=\frac15,\qquad R_{23}=\frac15,\qquad
 R_{45}=-\frac25.                                      \tag{A15}
\]

Consequently

\[
 D F_Q(R)=3\left(\frac15+\frac15-\frac25\right)=0,
 \qquad
 \operatorname{haf}(R)=-\frac2{125}\ne0.              \tag{A16}
\]

The three independent advertised witnesses also replay exactly:

\[
 [\overline{L_QL_R}]_{\nu_{0123}}=\frac25,\qquad
 \operatorname{per}(P_AK_*S_B^T)=-\frac2{125},\qquad
 (Y_{01}Y_{23}-Y_{02}Y_{13})\longmapsto
       \frac1{25}z_0z_1z_2z_3\ne0.                   \tag{A17}
\]

Thus the packet simultaneously has a zero top contraction, a nonzero
lower-degree apolar class, a nonzero Hall-certified permanent, and failure
of the coefficient-preserving balanced relation.  It really does falsify
all of the proposed fixed-word upgrades while satisfying the full nine
scalarized rows, both rank-three conditions, and the prescribed \(K_*\).

## 7. Precise no-gain conclusion

The following conclusions are justified:

1. Shafiei's theorem alone supplies no support equation, lower-degree
   annihilator, balanced response relation, or response-weighted algebra
   map beyond the scalar tangent equation.
2. Adding the complete nine scalarized equations at one mixed word, full
   scalarized star rank, invertible \(K_*\), and a nonzero response hafnian
   still does not supply such a fixed-word upgrade; Section 6 is an exact
   countermodel.
3. Treating every word as one polynomial family does not turn the family
   into a constant-coefficient annihilator, because the pure-word right side
   in (A11) remains nonzero.

The counterpacket deliberately does not satisfy the other coordinate words
of one shared global tensor identity.  It therefore does **not** falsify a
cross-word theorem.  What remains open on this route is source-relative:
one must use the shared block evaluation, star factorization, and polynomial
coefficient coupling to prove an implication such as (43), and separately
obtain the three pure response nonvanishings (44) if one wants to enter the
known ternary descent.  Those are the surviving attack angles; another
presentation of the intrinsic generic-hafnian apolar ideal is not one.
