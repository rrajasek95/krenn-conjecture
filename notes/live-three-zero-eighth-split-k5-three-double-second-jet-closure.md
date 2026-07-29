# The eighth split at \(k=5\): the three-double second-jet closure

## 1. Result

The no-extra-singular collision profile

\[
                              3^3 2^3 1^8                 \tag{1}
\]

is impossible.  Select one of the three double classes at formal role two
and all eight singleton classes at formal role one.  The complementary
signature is \(3^3 2^2\).  The
[unified pair-drop theorem](live-three-zero-eighth-split-k5-unified-pair-drop-linear-plane-closure.md)
makes the two dual relations the full space of linear polynomials.

The earlier complementary-double swap used only the first logarithmic jet
and put the other two double values in one quadratic fibre, which is not by
itself contradictory.  The unused constant member of the linear relation
space forces the second logarithmic jet to vanish as well.  Equality of the
two jets makes the three distinct double values pairwise isotropic for one
fixed nondegenerate binary quadratic, an impossibility.

## 2. Both complementary-double jets vanish

Let the three double values be \(u,v,x\), with \(x\) selected and
\(\{u,v\}\) complementary.  Let \({\cal A}\) be the three triple values
and \({\cal R}\) the eight singleton values.  The exact differentiated
relation at the complementary double \(u\) has the local form

\[
                         {B_{x;u,v}(z)S(z)\over(z-u)^3},
                         \qquad S\in\mathbb C[z]_{\le1},  \tag{2}
\]

where

\[
 B_{x;u,v}(z)=
 { (z+\mu)^5(z+x)^2
       \displaystyle\prod_{r\in{\cal R}}(z+r)\over
   (z-v)^3\displaystyle\prod_{a\in{\cal A}}(z-a)^4}.     \tag{3}
\]

Every factor in (3) is a unit at \(u\).  The zero residue in (2) is

\[
                         (B_{x;u,v}S)''(u)=0
                         \qquad(S\in\mathbb C[z]_{\le1}). \tag{4}
\]

Taking \(S=z-u\) and \(S=1\), respectively, gives

\[
             B_{x;u,v}'(u)=0,\qquad B_{x;u,v}''(u)=0.     \tag{5}
\]

Put \(X_{x;u,v}=(\log B_{x;u,v})'\).  Since \(B_{x;u,v}(u)\ne0\),
equation (5) is equivalent to

\[
                         X_{x;u,v}(u)=X_{x;u,v}'(u)=0.    \tag{6}
\]

## 3. Swap the selected and outside double

Keep \(u\) fixed and exchange \(x\) with \(v\).  Every singleton, triple,
and common-pole term cancels when the two instances of (6) are subtracted.
The first jet gives

\[
 \Phi_u(x)=\Phi_u(v),\qquad
 \Phi_u(t)={2\over u+t}+{3\over u-t}
           ={5u+t\over u^2-t^2},                         \tag{7}
\]

and the second jet gives

\[
 \Psi_u(x)=\Psi_u(v),\qquad
 \Psi_u(t)={2\over(u+t)^2}+{3\over(u-t)^2}.               \tag{8}
\]

All denominators in (7)--(8) are structurally nonzero.  Since \(x\ne v\),
equation (7) reduces to

\[
                         u^2+5u(x+v)+xv=0.                \tag{9}
\]

The coefficient \(5u+x\) cannot vanish in (9): substituting
\(x=-5u\) would give \(-24u^2=0\), while a repeated value \(u\) is
nonzero.  Hence

\[
                         v=-{u^2+5ux\over5u+x}.           \tag{10}
\]

Direct substitution into (8) gives the exact factorization

\[
 \Psi_u(x)-\Psi_u(v)=
 -{(u^2+10ux+x^2)(5u^2+2ux+5x^2)\over
       24u^2(u-x)^2(u+x)^2}.                              \tag{11}
\]

The first factor in (11) is nonzero, because (10) also gives

\[
                         v-x=-{u^2+10ux+x^2\over5u+x},    \tag{12}
\]

and \(v\ne x\).  Thus

\[
                         5u^2+2ux+5x^2=0.                 \tag{13}
\]

The same reasoning holds for every choice of the anchor and for either of
the other two double values.  Consequently all three unordered pairs among
\(\{u,v,x\}\) satisfy the symmetric equation

\[
                         Q(a,b):=5a^2+2ab+5b^2=0.         \tag{14}
\]

Subtract \(Q(u,x)=Q(u,v)=0\).  Since \(x\ne v\),

\[
                         2u+5x+5v=0.                     \tag{15}
\]

Similarly, the anchor \(x\) gives

\[
                         5u+2x+5v=0.                     \tag{16}
\]

Subtracting (16) from (15) yields \(3(x-u)=0\), contradicting
the distinctness of the double classes over characteristic zero.  This
proves (1).

## 4. Exact audit

[verify_live_three_zero_eighth_split_k5_three_double_second_jet_closure.py](../computations/verify_live_three_zero_eighth_split_k5_three_double_second_jet_closure.py)
checks the formal selection and complement, both local residue jets, both
swap signs, factorizations (9)--(12), and the final cyclic contradiction.

