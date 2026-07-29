# The $k=1$ constant-core role-swap closure

## 1. Result

Put

\[
 h=t-r-1,\qquad p=h+1,\qquad k=p-h=1,\qquad h\ge8.       \tag{1}
\]

The exceptional multiset has $2h+3$ labels.  This note gives two
uniform closure criteria for legal selections of $h$ labels represented
in exactly three value classes.  Such a selection has a nonzero constant
Hermite residual, and the double common pole at $-\mu$ supplies a scalar
logarithmic-derivative equation.

**Theorem 1.1 (interchangeable role).**  Fix two distinct value classes
$A,B$, select respectively $r,s\ge1$ labels from them, and put

\[
                              j=h-r-s\ge1.                 \tag{2}
\]

Suppose there are at least three further value classes $x$ such that

1. the class at $x$ has multiplicity at least $j$; and
2. the selection $A^rB^sx^j$ leaves a singleton class in its
   complement.

Then the profile is impossible on the no-extra-singular stratum.

**Theorem 1.2 (unequal-role swap).**  Fix one value class $A$ and a
positive count $t$.  Let $x,y$ be two further distinct classes, and
let $r,s\ge1$ be unequal, with

\[
                              t+r+s=h.                     \tag{3}
\]

Suppose both selections

\[
                              A^t x^r y^s,qquad A^t x^s y^r \tag{4}
\]

are available and leave a singleton in the complement.  Then the profile
is impossible.

Neither theorem requires a nonzero selected anchor.  A possible zero
exceptional value is handled explicitly in Section 4.

At the first higher frontier $(h,p)=(8,9)$, the old H/S/C/L/Q/V census
has 35 profiles labelled R.  Theorem 1.1 applies to 13 of them, Theorem
1.2 applies to 15, and their union contains exactly 17.  Four profiles are
added only by the unequal-role clause.  The union subsumes the two earlier
single-profile common-pole notes for $(4,3^5)$ and $(3^3,2^5)$, so it
adds fifteen closures beyond those two already recorded results.

## 2. Every legal three-class selection has a constant residual

Assume for contradiction that every isolated-star pivot vanishes.  Let

\[
                           R=A^rB^sx^j,qquad r+s+j=h,       \tag{5}
\]

be any of the legal selections in the theorem.  It represents three
value classes and leaves a singleton row class, so the simultaneous
Hermite lemma gives

\[
 F_R(z)={Q_R(z)\over D_R(z)},\qquad
 D_R(z)=(z+\mu)^2(z+A)^{r+1}(z+B)^{s+1}(z+x)^{j+1}.       \tag{6}
\]

The complement has $p+2=h+3$ labels.  The exact degree bounds are

\[
 \deg D_R=2+(r+1)+(s+1)+(j+1)=h+5,
 \qquad \deg Q_R\le p+3-1=h+3.                            \tag{7}
\]

All complementary row jets divide $Q_R$, counting multiplicity.  Hence

\[
                      Q_R=q_RP_N,\qquad q_R\in\mathbb C^*. \tag{8}
\]

In particular, $F_R=O(z^{-2})$.  The selected value poles have zero
simple residue by construction.  There is no residue at infinity, so the
residue theorem forces

\[
\[
                         \operatorname {res}_{z=-\mu}F_R=0. \tag{9}
\]
\]

Every factor in the regular cofactor at $-\mu$ is nonzero.  Since the
pole is double and $q_R$ is constant, (9) says that the logarithmic
derivative of that cofactor vanishes.

## 3. The exact role function and its signs

Let the full exceptional multiplicity of a value $v$ be $m_v$.  If
that class is unselected, its complementary root factors contribute

\[
                              -{m_v\over v+\mu}             \tag{10}
\]

to the logarithmic derivative at $z=-\mu$.  If $q\ge1$ labels are
selected, the numerator retains $m_v-q$ copies of $z-v$, while the
denominator contains $(z+v)^{q+1}$.  Its direct contribution is

\[
             -{m_v-q\over v+\mu}-{q+1\over v-\mu}.        \tag{11}
\]

Subtracting (10) from (11) gives the selection-role function

\[
 \begin{split}
 \Phi_q(v)
   &={q\over v+\mu}-{q+1\over v-\mu}\\
   &=-{v+(2q+1)\mu\over v^2-\mu^2}.                       \tag{12}
 \end{split}
\]

This baseline calculation includes every unselected class, so changing
one role does not silently change a background term.

For (5), equation (9) is therefore

\[
 -\sum_v{m_v\over v+\mu}
       +\Phi_r(A)+\Phi_s(B)+\Phi_j(x)=0.                  \tag{13}
\]

Once the two fixed roles are chosen, every term in (13) except the last is
independent of $x$.

## 4. Proof of the interchangeable-role theorem and zero safety

All candidate values in Theorem 1.1 lie in one fibre of

\[
                    \Phi_j(x)=-{x+(2j+1)\mu\over x^2-\mu^2}. \tag{14}
\]

For any scalar $\lambda$, the fibre equation is

\[
                  \lambda(x^2-\mu^2)+x+(2j+1)\mu=0.       \tag{15}
\]

It is a nonzero polynomial of degree at most two, because its coefficient
of $x$ is one even when $\lambda=0$.  Thus a fibre contains at most
two distinct admissible values, contradicting the three candidates.

The denominator in (14) never vanishes.  Structural admissibility gives
$x\ne\mu$ and $x+\mu\ne0$.  If $x=0$, these conditions force
$\mu\ne0$, and the denominator is $-\mu^2\ne0$.  Conversely, if
$\mu=0$, then $x\ne0$.  In the present cyclic three-zero residual one
in fact has $\mu\ne0$, but the fibre proof does not need that stronger
fact.  A zero class is necessarily a singleton, so it can occur in the
moving role only when $j=1$; equations (12)--(15) remain valid.

The same argument applies if one of the two fixed roles is the possible
zero singleton: every factor at $-\mu$ remains nonzero, and the fixed
term is simply absorbed in the constant in (13).

## 5. Proof of the unequal-role theorem

Apply (13) to the two selections (4).  Their common baseline and fixed
role cancel.  Subtraction gives

\[
 \begin{split}
 0={}&\Phi_r(x)+\Phi_s(y)-\Phi_s(x)-\Phi_r(y)\\
  ={}&(r-s)\left(
 {1\over x+\mu}-{1\over x-\mu}
 -{1\over y+\mu}+{1\over y-\mu}\right).                 \tag{16}
 \end{split}
\]

The standing cyclic residual has $\mu\ne0$, and $r-s\ne0$ by
hypothesis.  Clearing the structurally nonzero denominators in (16) gives

\[
 {2\mu(r-s)(x-y)(x+y)\over
       (x^2-\mu^2)(y^2-\mu^2)}=0.                         \tag{17}
\]

Thus $x^2=y^2$.  Equality $x=y$ is excluded because the roles use
distinct value classes, while $x=-y$ is excluded by the no-opposite
condition.  This proves Theorem 1.2.

A zero value causes no omitted edge here.  The pair $x,y$ must support
both positive counts $r,s$, so if one were zero its class would have to
be a singleton and hence could not support \(\max(r,s)\ge2\), because
unequal positive integers have maximum at least two.  The fixed class may
still be zero, but it cancels from (16).

## 6. Exact $(h,p)=(8,9)$ census

The thirteen R profiles satisfying Theorem 1.1 are

\[
\begin{gathered}
4^2 3 2^4,\quad 4 3^5,\quad 4 3^2 2^4 1,\quad
4 3^2 2^2 1^5,\\
3^6 1,\quad 3^5 2^2,\quad 3^5 2 1^2,\quad 3^5 1^4,\\
3^4 2^3 1,\quad 3^4 2 1^5,\quad 3^3 2^2 1^6,\quad
3^2 2^4 1^5,\quad 3^2 2^3 1^7.
\end{gathered}                                             \tag{18}
\]

The unequal-role theorem adds exactly four more profiles not in (18):

\[
 3^4 1^7,qquad 3^3 2^5,qquad
 3^3 2 1^8,qquad 3^3 1^{10}.                             \tag{19}
\]

Every profile in (18)--(19) has total size nineteen.  The literal checker
chooses actual class indices and actual positive selection counts; it does
not infer a witness merely from a multiplicity pattern.  It also verifies
that every member of each moving family leaves a singleton complement and
that both sides of every unequal swap are legal.

## 7. Audit

[verify_live_three_zero_higher_split_k1_constant_core_role_swap.py](../computations/verify_live_three_zero_higher_split_k1_constant_core_role_swap.py)
checks the Hermite and infinity degrees, reconstructs (10)--(13) directly,
verifies both signs in (12), proves the degree-two fibre and the exact
factorization (17), audits both zero-value cases, and independently
searches the 35 old R profiles.  It finds counts $13$, $15$, and
$17$ for Theorem 1.1, Theorem 1.2, and their union, with exactly the four
incremental profiles in (19).
