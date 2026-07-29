# Independent audit: the \(p=28\) cubic-pair intersection frontier

## Verdict and scope

**PASS, as a frontier and falsification result.**  I reconstructed the
[primary cubic-pair note](live-three-zero-higher-split-p28-three-quartic-cubic-pair-intersection-frontier.md)
without importing its verifier.  Both advertised phenomena are real:

1. the elementary shift has two cubic presentations but primitive splitting
   \((2,2)\), with an even scalar square in the derivative wedge;
2. the displayed transverse pair is genuinely primitive of splitting
   \((3,3)\), has the saturated echelon data and a squarefree residual sextic,
   yet its ordinary Wronskian is squarefree rather than \(T^3R^2\).

Consequently, cubic-pair intersection dimension and echelon data alone do not
close the surviving \(4^3 3^6\) profile.  The transverse model is not a
profile realization and is not a counterexample to Krenn's conjecture.

## Reconstructing \({\cal U}(C,D)\)

Write a cubic covector row as

\[
                  \lambda(s)=\lambda_0+s\lambda_1+s^2\lambda_2+s^3\lambda_3
\]

and impose \(\lambda(t)F=\lambda'(t)F=0\), where \(t=z^2\).  Direct division
by \((s-t)^2\), with no geometric input, gives

\[
 \lambda(s)F=(s-t)^2(Cs+D)
\]

and hence

\[
 (\lambda_3F,\lambda_2F,\lambda_1F,\lambda_0F)
   =(C,D-2tC,t^2C-2tD,t^2D).
\]

For the two displayed rows \(\lambda,\mu\), their coefficient-covector
matrices have ranks four and four, while their joint rank is six.  Solving

\[
             \lambda E=\mu E=\lambda'E=\mu'E=0
\]

and the identical equations for \(O\), among vector polynomials of degree at
most four, produces a \(32\times30\) rational linear system of rank \(28\).
Its nullspace is exactly two-dimensional.  Reconstructing \(C,D,P,Q\) from
that fresh basis gives

\[
 \dim{\cal U}(C,D)=\dim{\cal U}(P,Q)=4,
 \qquad
 \dim({\cal U}(C,D)+{\cal U}(P,Q))=6,
\]

so their intersection has dimension exactly two.

## Why the shift is \((2,2)\), not \((3,3)\)

Use the abstract separated basis

\[
                    C,tC,t^2C,D,tD,t^2D.
\]

For every \(c\ne0\), coefficient reduction shows

\[
 {\cal U}(C,D)\cap{\cal U}(C,D+cC)
       =\langle C,D-2tC\rangle,
\]

and the sum is the full separated six-space.  If

\[
 C=p(t)+zq(t),\qquad D=r(t)+zs(t),\qquad
 u=(1,t,t^2),
\]

then

\[
 E=(pu,ru),\qquad O=(qu,su).
\]

Modulo \(\langle E,O\rangle\), derivatives depend only on the two copies of
\(u'\).  Thus the primitive four-plane is annihilated by the two row-reduced
quadratics

\[
 (t^2,-2t,1,0,0,0),\qquad(0,0,0,t^2,-2t,1),
\]

which proves splitting \((2,2)\).  With \(\Delta=ps-qr\), I also calculated
all Pluecker coordinates formally and obtained the exact identity

\[
 E\wedge O\wedge E'\wedge O'
       =\Delta^2\,(u\otimes e_1)\wedge(u\otimes e_2)
                    \wedge(u'\otimes e_1)\wedge(u'\otimes e_2).
\]

The primitive wedge has no common scalar zero, while every scalar zero from
\(\Delta^2\) is even.  This shift cannot supply six distinct simple moving
roots.

The separated Wronskian formula was also reconstructed.  With
\({\cal D}=(2z)^{-1}d/dz\), \(\rho=D/C\), and

\[
 {\cal I}(\rho)=
 -12\rho'\rho'''\rho'''''
 +15\rho'(\rho'''')^2+18(\rho'')^2\rho'''''
 -60\rho''\rho'''\rho''''+40(\rho''')^3,
\]

differential-algebra expansion of the Crum transform gives exactly

\[
 \operatorname{Wr}(C,tC,t^2C,D,tD,t^2D)
                  =2^{17}z^{15}C^6{\cal I}(\rho).
\]

In particular the apparent \(z^{15}\) is not a forced zero: the
\({\cal D}\)-derivatives can have compensating poles.

## The transverse \((3,3)\) example

The two original cubic rows pass both independent bundle checks:

* the gcd of their nonzero \(2\times2\) minors is one, so the frame is
  primitive at every finite \(t\);
* their degree-three leading coefficient rows are independent, so the frame
  is row-reduced with splitting \((3,3)\).

The fresh degree-four syzygy basis \(E,O\) is primitive as well: the gcd of
the \(2\times2\) minors of \([E\ O]\) is one, and its two leading
coefficient columns are independent.  For this basis the two endpoint
projection determinants are

\[
 \det(E_0,O_0,E_1,O_1,E_2,O_2)
   ={3458307951792909\over119149790175232}\ne0,
\]

\[
 \det(O_4,E_4,O_3,E_3,O_2,E_2)
   =-{384256439088101\over29787447543808}\ne0.
\]

The first gives vanishing orders \(0,1,2,3,4,5\) at \(z=0\); the second
gives echelon degrees \(4,5,6,7,8,9\), hence no defect at infinity.

Put

\[
 tC+D=a(t)+zb(t),\qquad tP+Q=c(t)+zd(t).
\]

There is a useful exact orientation check behind the determinant formula.
Because \(\lambda'E=\lambda'O=0\), differentiation gives

\[
 [\lambda'E'\ \lambda'O']=-[\lambda''E\ \lambda''O]
                          =-2[a\ b],
\]

and similarly for \(\mu\).  Therefore the derivative-map determinant is
\(4\kappa\), where

\[
 \kappa=ad-bc.
\]

For the reconstructed basis,

\[
 \kappa(t)=-{72701\over78112}
 \left(2t^6+6t^5-249t^4-56t^3+81t^2+15t+3\right).
\]

The sextic in parentheses is squarefree.  Independently computing all
fifteen derivative-wedge minors gives the same monic polynomial as their
gcd.  Thus this is the primitive residual determinant, not a basis artifact.

Finally, the ordinary Wronskian of the six coordinate polynomials has degree
exactly \(24\), nonzero constant and leading coefficients, and

\[
                 \gcd(\operatorname{Wr}(F),\operatorname{Wr}(F)')=1.
\]

It is therefore squarefree and cannot realize threefold triple roots and
twofold quartic roots.

## Audit of the norm and jet-minor test

Let

\[
 T(z)=\prod_{j=1}^6(z-i_j),\qquad
 R(z)=\prod_{\nu=1}^3(z-r_\nu),\qquad
 K(t)=\prod_{j=1}^6(t-i_j^2).
\]

The structural assumptions make \(K\) squarefree.  Since the residual
determinant has exactly the six moving square roots, the required identity is
\(\kappa(z^2)=c_1T(z)T(-z)\).  Also
\(R(z)R(-z)=H(z^2)\) for a cubic \(H\).  Taking the involutive norm of

\[
                    \operatorname{Wr}(F)=cT^3R^2
\]

then gives, with the exponents unchanged,

\[
 \operatorname{Wr}(F)(z)\operatorname{Wr}(F)(-z)
          =c_2\kappa(z^2)^3H(z^2)^2.
\]

So the proposed norm comparison is a correct necessary sign-free screen.
It is not sufficient, exactly as the primary note states.

The jet-minor sizes also match the desired Schubert partitions.  At a triple
root, divisibility of every \(4\times4\) minor of \(J_3\), together with the
open rank conditions, gives pivot orders

\[
                         (0,1,2,4,5,6)
\]

and weight three.  At a quartic root, divisibility of every \(5\times5\)
minor of \(J_4\) gives

\[
                         (0,1,2,3,5,6)
\]

and weight two.  The checker reconstructs both canonical local models and
their Wronskian valuations.  Multiplication by a regular unit does not change
these ranks because it acts on initial jets by an invertible lower-triangular
matrix.

There is one scope qualification worth making explicit: the word "sharp"
means a finite necessary-and-sufficient target **inside the already fixed
transverse cubic-pair branch**, after imposing primitivity, echelon degree,
squarefreeness, nonzero/disjoint roots, the lower-jet open conditions, and
the Wronskian and residual-determinant factorizations.  Equations involving
the norm or jet minors in isolation neither close the profile nor realize it.
With that interpretation, I found no overclaim in the primary note.

The standalone checker
[verify_live_three_zero_higher_split_p28_three_quartic_cubic_pair_intersection_frontier_independent_audit.py](../computations/verify_live_three_zero_higher_split_p28_three_quartic_cubic_pair_intersection_frontier_independent_audit.py)
performs all rank, gcd, splitting, determinant, Wronskian, norm, and local-jet
calculations over \(\mathbb Q\), without importing the primary verifier.
