# The eighth split: common-pole closure of \((4,3,3,3,3,3)\)

## 1. Result

Consider the first residual profile in the higher-split collision census,

\[
                    (h,k;\lambda)=(8,1;(4,3,3,3,3,3)).     \tag{1}
\]

Thus \(p=h+k=9\), there are nineteen exceptional labels, one value class
\(A\) has multiplicity four, and five distinct values

\[
                         T=\{b_1,\ldots,b_5\}               \tag{2}
\]

have multiplicity three.  All six values are nonzero, pairwise distinct,
and pairwise nonopposite.  The common value \(\mu\) is distinct from them
and every required sum with \(\mu\) is structurally nonzero.

**Theorem 1.1.**  Profile (1) is impossible on the no-extra-singular
stratum.

The proof uses the common pole \(-\mu\), not a moving-anchor root count.
Every legal three-class selection leaves a constant Hermite residual.  The
residue theorem gives one logarithmic-derivative equation at \(-\mu\).
Changing which triple class is fully selected forces four distinct triple
values into one fibre of a nonconstant degree-two rational function.

## 2. The legal \(3+3+2\) selections

Assume for contradiction that every isolated-star pivot vanishes.  Fix a
partial triple value \(c\in T\).  For each \(b\in T\setminus\{c\}\), select

\[
                         R_{b,c}=A^3b^3c^2.                 \tag{3}
\]

The four-class and the partial triple each leave one label in the
complement.  Hence the simultaneous-Hermite singleton-row lemma applies.
The complement has \(p+2=11\) labels, while (3) represents three value
classes.  The Hermite numerator has degree at most

\[
                         p+3-1=11.                          \tag{4}
\]

After the complementary root polynomial of degree eleven is divided out,
the residual is a nonzero constant:

\[
                         Q_{b,c}=q_{b,c}P_{N_{b,c}},
                         \qquad q_{b,c}\ne0.                \tag{5}
\]

The rational dependence is

\[
 F_{b,c}(z)=
 {q_{b,c}P_{N_{b,c}}(z)\over
  (z+\mu)^2(z+A)^4(z+b)^4(z+c)^3}.                         \tag{6}
\]

Its numerator has degree eleven and its denominator degree thirteen, so

\[
                              F_{b,c}(z)=O(z^{-2}).          \tag{7}
\]

At each of the three selected value poles, the confluent squared-kernel
column span contains pole orders at least two but no simple pole.  Thus all
three finite residues away from \(-\mu\) vanish.  There is no residue at
infinity by (7), so the residue theorem gives

\[
                         \operatorname {res}_{z=-\mu}F_{b,c}=0. \tag{8}
\]

All factors in the regular cofactor at \(-\mu\) are nonzero.  Since the
pole in (6) is double and the residual (5) is constant, (8) is exactly the
vanishing of its logarithmic derivative.

## 3. The full-triple role function

It is cleanest to write the logarithmic derivative relative to the full
unselected exceptional multiset.  At \(z=-\mu\), an unselected class of
multiplicity \(m\) contributes

\[
                              -{m\over x+\mu}.               \tag{9}
\]

If \(r\ge1\) labels of that class are selected, \(r\) numerator roots are
removed and a denominator pole of order \(r+1\) is introduced.  Its change
from (9) is therefore

\[
 \Delta_r(x)={r\over x+\mu}-{r+1\over x-\mu}.              \tag{10}
\]

All terms in (8) other than the fully selected triple \(b\) are fixed once
\(A\) and \(c\) are fixed.  Hence (8) has the form

\[
                         C_{A,c}+\Phi(b)=0,                 \tag{11}
\]

where

\[
 \Phi(x)=\Delta_3(x)
        ={3\over x+\mu}-{4\over x-\mu}
        =-{x+7\mu\over x^2-\mu^2}.                        \tag{12}
\]

This calculation includes all unmatched labels.  Explicitly, the
four-class contributes

\[
 -{1\over A+\mu}-{4\over A-\mu},                           \tag{13}
\]

the full triple \(b\) contributes \(-4/(b-\mu)\), the partial triple
\(c\) contributes

\[
 -{1\over c+\mu}-{3\over c-\mu},                           \tag{14}
\]

and every other triple \(x\) contributes \(-3/(x+\mu)\).
Equations (13)--(14) agree term by term with the baseline formula
(9)--(10), fixing the signs in (12).

## 4. The fibre contradiction

For the fixed \(c\), all four values \(b\in T\setminus\{c\}\) satisfy
(11).  Thus they lie in one fibre of \(\Phi\).  But for any scalar
\(\lambda\), the equation \(\Phi(x)=\lambda\), after multiplication by
the structurally nonzero denominator \(x^2-\mu^2\), is

\[
                     \lambda(x^2-\mu^2)+x+7\mu=0.          \tag{15}
\]

This is a nonzero polynomial of degree at most two: its coefficient of
\(x\) is one, even if its quadratic coefficient vanishes.  Consequently a
fibre of \(\Phi\) contains at most two admissible distinct values.  The four
distinct values forced by (11) are impossible.  This contradiction proves
Theorem 1.1.

## 5. Exact audit

[verify_live_three_zero_eighth_split_433333_common_pole_closure.py](../computations/verify_live_three_zero_eighth_split_433333_common_pole_closure.py)
checks all twenty ordered choices in (3), the complementary multiplicities,
the constant-residual and infinity degrees, reconstructs the common-pole
logarithmic derivative both directly and from the full-multiset baseline,
verifies the signs and factorization in (12), and checks the strict
four-versus-two fibre count.
