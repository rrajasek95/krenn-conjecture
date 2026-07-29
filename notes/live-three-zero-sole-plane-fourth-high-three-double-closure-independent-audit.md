# Independent audit: sole-plane \(2^3 1^7\) closure

## 1. Verdict and scope

**PASS.**  The characteristic-zero degree-78 squeeze in the
[primary closure note](live-three-zero-sole-plane-fourth-high-three-double-closure.md)
is valid.  A fresh checker reconstructs the cleared rows, first
cross-identity system, cyclic parameter obstructions, modular rank bound,
exact rational overideals, Hilbert values, and projective boundary without
importing either the primary closure checker or the three-double frontier
checker.

The result closes exactly the sole-plane profile

\[
                              2^3 1^7
\]

at \((r,t)=(7,13)\).  It does not close the remaining profiles
\(2^4 1^5,2^5 1^3,2^6 1\), nor does it by itself settle Krenn's
conjecture.

The independent executable and its normalized transcript are:

- [verify_live_three_zero_sole_plane_fourth_high_three_double_closure_independent_audit.py](../computations/verify_live_three_zero_sole_plane_fourth_high_three_double_closure_independent_audit.py)
- [verify_live_three_zero_sole_plane_fourth_high_three_double_closure_independent_audit.log](../computations/verify_live_three_zero_sole_plane_fourth_high_three_double_closure_independent_audit.log)

## 2. Rebuilt necessary obstructions

For an anchor \(a\), effective first logarithmic derivative \(P\), and
\(R=P^2+W\), the audit independently expands the cleared row

\[
\begin{aligned}
 M_a&=R(x^2-a^2)^2-2P(x^2-a^2)(x+3a)
       +4(x^2+2ax+3a^2),\\
 N_a&=2P(x^2-a^2)^2-2(x^2-a^2)(x+3a)-aM_a.
\end{aligned}
\]

It derives this row from the logarithmic first- and second-derivative
numerators, verifies the weights \(M_a\mapsto c^2M_a\) and
\(N_a\mapsto c^3N_a\), and checks the selected-partner exchange

\[
 P\mapsto P+\delta,\qquad
 R\mapsto R+2P\delta+\delta^2+\epsilon.
\]

After normalizing the three double values to \(1,v,w\), it reconstructs
the first cross polynomial

\[
 C_1=(x-v)F_{1v}-\lambda(x-w)F_{1w}
\]

and its ten confluent evaluations.  Every input denominator factors into

\[
 v,\ w,\ v\pm1,\ w\pm1,\ v\pm w.
\]

Over \(\mathbb Q(v,w)\), an independently generated \(10\times1\)
lift matrix has 34 coefficient terms and satisfies the literal matrix
identity

\[
                    \operatorname{matrix}(E)\,U
                    =\operatorname{matrix}(G).
\]

Every coefficient denominator in \(U\) is constant in \(v,w\).  The raw
constant obstruction is therefore necessary wherever the structural
product

\[
 L=vw(v-1)(v+1)(w-1)(w+1)(v-w)(v+w)
\]

is nonzero.

The audit performs all three cyclic reanchorings before removing factors.
For each resulting quotient \(h_i\), it checks exactly that the removed
factor divides \(L^{60}\), that \(\gcd(h_i,L)=1\), and that

\[
                  \deg h_i=30,\qquad |{\rm supp}(h_i)|=319.
\]

Thus no nonstructural parameter component is discarded.

## 3. Independent good-prime rank bound

Let

\[
 S=\mathbb Q[t,v,w],\qquad
 J=((h_1)^h,(h_2)^h,(h_3)^h).
\]

The audit uses the different prime \(31991\) and the permuted ring order
\(dp(w,t,v)\).  A name-marker polynomial checks the source-to-target
map, and successful reduction of all three rational generators verifies
that their coefficient denominators are invertible at this prime.  The
modular standard basis has 417 elements and gives

\[
                  \operatorname{HF}_{J_{31991}}(78)=318.
\]

There are

\[
                    \dim S_{78}=\binom{80}{2}=3160
\]

target monomials, so the modular Macaulay rank is \(2842\).
After clearing rational coefficient denominators by integers not
divisible by \(31991\), any nonzero modular minor is the reduction of a
nonzero characteristic-zero minor.  Hence

\[
 \operatorname{rank}_{\mathbb Q}M_{78}\ge2842,\qquad
 \operatorname{HF}_{J}(78)\le318.
\]

Only this one-sided rank specialization is used.  No modular membership,
unit ideal, or characteristic-zero equality is inferred.

## 4. Exact rational overideals

Put

\[
 L^h=vw(v-t)(v+t)(w-t)(w+t)(v-w)(v+w),
\]

so the projective structural discriminant is \(\Delta=tL^h\), and define
\[
                        Q=t^{46}(L^h)^4\in S_{78}.
\]

The checker directly verifies

\[
                    \deg Q=78,\qquad Q|_{t=1}=L^4.
\]

### 4.1 Affine overideal

The audit reconstructs the affine candidate in the reversed order
\(dp(w,v)\), normalizes it over \(\mathbb Q\), and then homogenizes it in
the order \(dp(w,t,v)\).  All facts used later are fresh exact reductions:

\[
 J\subseteq A,\qquad Q\in A,\qquad
 \operatorname{HF}_A(78)=192,\qquad
 \operatorname{HF}_{A+(t^{16})}(78)=0.
\]

The reversed-order homogeneous basis has 60 elements (rather than the
primary transcript's 55), while its Hilbert numerator is again

\[
             1-4z^{18}-8z^{19}+8z^{20}+3z^{21}-z^{22}+z^{23}.
\]

This order-dependent basis-size difference is useful independent evidence:
the Hilbert invariant and all exact containments agree without replaying
the same standard basis.

### 4.2 Infinity overideal

The second reconstruction uses \(dp(w,v,t)\).  A marker verifies that the
map from source order \((t,v,w)\) sends the three source names to the
same-named target variables despite the reordered ring.  Exact rational
normalization then verifies

\[
 J+(t^{16})\subseteq B,\qquad Q\in B,\qquad
 \operatorname{HF}_B(78)=126.
\]

The homogeneous basis has 73 elements, with Hilbert numerator

\[
 1-z^{16}-3z^{30}+3z^{46}+14z^{48}+4z^{49}-18z^{50}.
\]

Probabilistic modular reconstruction is used only to propose \(A\) and
\(B\).  The proof consumes only the subsequently checked exact rational
containments, homogeneity, target reductions, and Hilbert numerators.
Consequently an incorrect proposal cannot create a false positive.

## 5. Degreewise squeeze

Let \(C=A\cap B\).  Exact reductions give \(J\subseteq C\) and
\(Q\in C\).  Since \(t^{16}\in B\),

\[
                         A+(t^{16})\subseteq A+B.
\]

The degree-78 quotient of the left side is zero, so the degree-78
quotient of the right side is also zero.  Applying the homogeneous
degree-78 part of

\[
0\longrightarrow S/(A\cap B)\longrightarrow
S/A\oplus S/B\longrightarrow S/(A+B)\longrightarrow0
\]

gives

\[
             \operatorname{HF}_{C}(78)=192+126-0=318.
\]

Because \(J\subseteq C\), one has
\(\operatorname{HF}_{J}(78)\ge318\).  Together with the alternate-prime
upper bound, this yields equality of both quotient dimensions and then,
degreewise,

\[
                             J_{78}=C_{78}.
\]

Thus \(Q\in J_{78}\).  Evaluation at \(t=1\) is a ring homomorphism,
each \((h_i)^h\) maps to \(h_i\), and \(Q\) maps to \(L^4\).  Therefore

\[
                             L^4\in(h_1,h_2,h_3).
\]

At any putative counterexample the three necessary obstructions vanish,
forcing \(L=0\), contrary to structural admissibility.

## 6. Projective boundary and wording caveat

The independent checker computes the exact gcd of the three leading
binary forms:

\[
                              v^6w^6.
\]

Hence their only common directions on \(t=0\) are
\([0:1:0]\) and \([0:0:1]\), both on the structural discriminant
\(\Delta=tL^h=0\).  This is a consistency check, not a discarded-boundary
step: the homogeneous Hilbert squeeze retains the complete degree-78
contribution.

One wording refinement is appropriate.  Since \(B\) is proved to be an
overideal rather than identified as a primary component ideal, its
126-dimensional value should be called the exact \(B\)-term in the
Hilbert squeeze, not by itself a proved scheme-theoretic primary
“infinity component.”  This does not affect any equation or the closure.

## 7. Recorded transcript

The fail-closed run produced

~~~text
audit prime / ambient / modular rank: 31991 3160 2842
HF(Jmod), HF(A), HF(A+t^16), HF(B), HF(A intersect B):
318 192 0 126 318
SOLE-PLANE 2^3 1^7 INDEPENDENT CLOSURE AUDIT PASS
~~~

No logical, algebraic, characteristic, variable-map, dehomogenization, or
projective-boundary gap was found.
