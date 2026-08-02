# The second-lift tangent cone has five linear branches

## Exact outcome

At the rational point on the five-parameter \(n=8\) mixed torus, let
\(T\) be the 56-dimensional mixed tangent space.  The exact second Hasse
obstruction

\[
  \operatorname {Sym}^2(T)\longrightarrow
  \operatorname {coker}J_{\rm mix}
\]

has rank 39.  Its image coordinates generate a quadratic ideal \(I_2\) in
56 tangent parameters.  Exact rational Gröbner reduction now proves that
the reduced second-liftable tangent cone is the union of exactly five
linear spaces:

\[
  \boxed{\sqrt{I_2}=P_1\cap P_2\cap P_3\cap P_4\cap P_5.}
\]

Their affine dimensions are respectively

\[
                         51,quad47,quad46,quad45,quad45.
\]

Thus the nonlinear-looking rank-39 compatibility system has a finite,
completely linear reduced branch geometry.  The obstruction scheme itself
is slightly nonreduced; six generators of its radical require squaring.

## Ferrers form of the radical

Use the free-coordinate labels from the exact tangent echelon basis and put

\[
\begin{array}{lll}
 a=z_{3712},&b=z_{3710}+z_{3711},&c=z_{1321},\\
 d=z_{1311}-z_{3711},&e=z_{1301},
\end{array}
\]

and

\[
\begin{array}{llll}
q_0=z_{0400},&q_1=z_{0401},&q_2=z_{0402},
  &q_3=z_{0410}-z_{0411},\\
q_4=z_{0412},&q_5=z_{0420},&q_6=z_{0421},&q_7=z_{0422},\\
q_8=z_{0601},&q_9=z_{0611},&q_{10}=z_{0621}.
\end{array}
\]

Then \(\sqrt{I_2}\) is the squarefree Ferrers edge ideal whose five left
neighbourhoods are

\[
\begin{aligned}
N(a)&=\{q_0,\ldots,q_9\},\\
N(b)&=\{q_0,\ldots,q_{10}\},\\
N(c)&=\{q_0,q_1,q_3,q_5,q_6\},\\
N(d)&=N(e)=\{q_0,\ldots,q_7\}.
\end{aligned}
\]

It has 42 quadratic generators.  Its five minimal vertex covers give the
linear primes

\[
\begin{aligned}
P_1={}&(a,b,c,d,e),\\
P_2={}&(a,b,d,e,q_0,q_1,q_3,q_5,q_6),\\
P_3={}&(a,b,q_0,q_1,q_2,q_3,q_4,q_5,q_6,q_7),\\
P_4={}&(b,q_0,q_1,q_2,q_3,q_4,q_5,q_6,q_7,q_8,q_9),\\
P_5={}&(q_0,q_1,q_2,q_3,q_4,q_5,q_6,q_7,q_8,q_9,q_{10}).
\end{aligned}
\]

The decomposition is irredundant: the five primes are pairwise
incomparable.

## Exact certificate

The 39 obstruction quadrics have only 68 monomial terms.  Their reduced
Gröbner basis has 48 elements.  The nine additional elements are especially
simple.  With

\[
 a=z_{3712},\qquad (r,s,t)=(z_{0420},z_{0421},z_{0422}),
\]

they are exactly

\[
 a^2r,a^2s,a^2t,
 \quad ar^2,ars,art,as^2,ast,at^2
 =a(r,s,t)(a,r,s,t).
\]

There are no higher-degree Gröbner generators.  Thus a literal local
standard-basis lift requires only nine new cubic leading forms beyond the
39 quadratic obstruction lifts.  The checker also verifies directly that:

1. every obstruction quadric belongs to the 42-generator Ferrers ideal;
2. the Ferrers ideal equals the intersection of the five displayed linear
   primes;
3. 36 Ferrers generators already reduce to zero modulo \(I_2\); and
4. the squares of the other six reduce to zero modulo \(I_2\).

These inclusions prove the radical identity without trusting a reported
primary decomposition: \(I_2\subseteq J\), \(J\) is radical, and
\(J\subseteq\sqrt{I_2}\).

## Meaning and scope

This explains why arbitrary tangent tests were misleading.  A tangent
vector can extend to second order only on one of five sharply constrained
linear branches (up to the nilpotent structure of \(I_2\)).  The quartic
pure-output factorizations found earlier vanish because they lie in this
obstruction ideal.

The theorem concerns only the reduced second-lift tangent cone.  Third and
higher Hasse equations may cut these five spaces further, and the result
does not by itself prove formal-local membership of either missing pure
coefficient.  Its value is that the next all-orders test can now be split
into five explicit linear branches rather than the full 56-variable
quadratic cone.

## Reproduction

```sh
python3 computations/verify_n8_second_lift_obstruction_radical.py
python3 -O computations/verify_n8_second_lift_obstruction_radical.py
python3 -I computations/verify_n8_second_lift_obstruction_radical.py
python3 -S computations/verify_n8_second_lift_obstruction_radical.py
```

The checker reconstructs the obstruction forms from the frozen mixed-jet
data and uses exact rational Gröbner reductions in Singular.  It records
the obstruction support, Gröbner size, radical size, six square witnesses,
five component dimensions, and Ferrers neighbourhood sizes.
