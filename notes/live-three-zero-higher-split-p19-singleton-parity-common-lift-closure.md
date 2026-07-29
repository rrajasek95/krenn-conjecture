# Higher splits: a singleton-parity common-lift closure at (p=19)

## 1. Uniform theorem

Use a higher-split formal selection whose selected-row kernel is
five-dimensional.  Suppose that, after fixing all but one selected
singleton, the last selected singleton can range over a pool (P) of
distinct value classes.  For (q\in P), write the complementary profile
as

\[
             1^{\,P-1}m_1\cdots m_C,                         \tag{1}
\]

where the (C) displayed classes do not depend on (q).  Put

\[
                    M_5=\sum_{i=1}^C\min(m_i,5).              \tag{2}
\]

All values obey the usual structural hypotheses: distinct value classes
are distinct and nonopposite, repeated values are nonzero, and at most one
member of (P) is zero.

**Theorem 1.1 (singleton-parity common lift).**  The formal configuration
is impossible if

\[
                    (P-1)+M_5\leq28
              \qquad\hbox{and}\qquad C\leq5.                  \tag{3}
\]

The first inequality is a capped-mass condition and the second only counts
the value classes outside the moving pool.  Thus the statement is not
specific to one collision profile or even to (p=19).

At the (p=19) boundary every surviving complement has actual, hence also
five-capped, mass nineteen.  The first condition in (3) is automatic.
The theorem closes exactly fifty-seven of the ninety-four boundary families:

\[
\boxed{
\begin{array}{c|c}
\text{profile type}&\text{closed parameter range}\\ \hline
3^a2^b1^{h+21-3a-2b}
 &\begin{array}{l}
 a=0:\ 1\le b\le7,\\
 a=1:\ 0\le b\le6,\\
 a=2:\ 0\le b\le5,\\
 a=3:\ 0\le b\le4,\\
 a=4:\ 0\le b\le3,\\
 a=5:\ 0\le b\le2;
 \end{array}\\[4mm]
4\,3^a2^b1^{h+17-3a-2b}
 &\begin{array}{l}
 a=0:\ 0\le b\le6,\\
 a=1:\ 0\le b\le5,\\
 a=2:\ 0\le b\le4,\\
 a=3:\ 0\le b\le3,\\
 a=4:\ 0\le b\le2.
 \end{array}
\end{array}}                                                   \tag{4}
\]

There are thirty-two families in the first block and twenty-five in the
second.  The proof uses neither a saturated relation Wronskian nor a
profile-specific Schubert calculation.

## 2. Exact moving-singleton transport

Let the complement in (1) have

\[
                         c=P-1+C                              \tag{5}
\]

value classes.  Since the selected-row kernel has dimension five, its
row-relation space is a three-space

\[
                 {\cal S}_q\subseteq\mathbb C[z]_{\leq c-4}.
                                                                    \tag{6}
\]

Remove the moving singleton (q) from the selected normalization while
retaining every fixed selected layer.  As in the complete (p=18)
low-triple closure, the exact regular-unit quotient is

\[
                         f_q(z)=(z-q)^2(z+q).                   \tag{7}
\]

For each pool point (r) the baseline has an exact first-order row, and
for a fixed complementary class of multiplicity (m_i) it has an exact
order-(m_i) row.  At (r=q), the square in (7) kills the complete first
jet.  At every other row, (7) is a unit and the product rule transports
the selected relation equation exactly.  Therefore

\[
 {\cal T}_q:=f_q{\cal S}_q\subseteq{\cal K}
       \subseteq\mathbb C[z]_{\leq c-1},\qquad
                         \dim{\cal T}_q=3,                     \tag{8}
\]

where the common kernel ({\cal K}) is independent of (q).  No division
by (q) occurs, so (q=0), when (f_q=z^3), is included.

## 3. The common kernel has dimension at most four

Suppose that ({\cal K}) contained a five-space.  The (P) simple
baseline rows force Wronskian weight at least (4P).  A fixed exact
order-(m_i) row forces weight at least

\[
                         \max(0,5-m_i).                         \tag{9}
\]

This estimate survives arbitrary common factors: division by a gcd root
lowers the degree cap by five times its order and changes the exact jet
order by precisely the standard nonnegative correction from the
row-relation truncated-mass bound.

The ambient degree in (8) is (c-1=P+C-2), so a five-space has Wronskian
degree at most

\[
                 5\bigl((c-1)+1-5\bigr)=5(P+C-6).              \tag{10}
\]

On the other hand the forced weight is

\[
 4P+\sum_{i=1}^C\max(0,5-m_i)
                  =4P+5C-M_5.                                 \tag{11}
\]

Equations (10)--(11) would require

\[
                         (P-1)+M_5\geq29,                       \tag{12}
\]

contrary to (3).  Hence

\[
                            3\leq\dim{\cal K}\leq4.            \tag{13}
\]

This is the useful general form of the one-unit (p=19) boundary: the
moving relation three-spaces need not coincide, but they all fit in a
four-space.

## 4. A parity lemma for cubic incidence planes

We isolate the polynomial-linear-series input.

**Lemma 4.1.**  Let ({\cal S}\subseteq\mathbb C[z]_{\leq n}) be a
three-space.  Let (T) be a set of (m) distinct, pairwise nonopposite
complex numbers, at most one of which is zero.  Put

\[
                         f_t=(z-t)^2(z+t).                       \tag{14}
\]

If

\[
            \dim\bigl({\cal S}\cap f_t\mathbb C[z]\bigr)\geq2
                         \qquad(t\in T),                       \tag{15}
\]

then

\[
                              \boxed{m\leq n-2}.                \tag{16}
\]

**Proof.**  For (A,B\in{\cal S}), form the odd parity determinant

\[
              \Delta_{A,B}(z)=A(z)B(-z)-A(-z)B(z).             \tag{17}
\]

At a nonzero (t\in T), the three restricted functionals
(E_t,D_t,E_{-t}) all annihilate the plane in (15), so they are
proportional on ({\cal S}).  Hence (Delta_{A,B}(t)=0), and oddness
also gives the root (-t).  If (0\notin T), oddness supplies one more
root at zero.  If (0\in T), the plane in (15) is divisible by (z^3),
so every parity determinant has a zero of order at least three at zero.
In both cases every parity determinant is divisible by one fixed odd
polynomial of degree (2m+1).  If (m\geq n), this degree exceeds the
(2n-1) bound in (17), so every parity determinant vanishes identically.

There is one sharp boundary to retain.  If (m=n-1), every parity
determinant is a scalar multiple of the same degree-(2n-1) polynomial.
Those scalars define an alternating bilinear form on the odd-dimensional
space ({\cal S}).  It has a nonzero radical vector (R).  Hence
(\Delta_{R,A}=0) for every (A\in{\cal S}).  All rational ratios (A/R)
are even, so (\Delta_{A,B}=0) for every pair (A,B) as well.  Thus, under
the single assumption (m\geq n-1), all parity determinants vanish
identically.

Let (G=\gcd({\cal S})) and divide it out.  For a primitive basis
(A_0,A_1,A_2), vanishing of all determinants says

\[
                  (A_0(-z),A_1(-z),A_2(-z))
                    =\gamma(z)(A_0(z),A_1(z),A_2(z)).          \tag{18}
\]

Writing (gamma) in lowest terms, its denominator divides all three
(A_i), and is therefore constant.  Applying (18) twice gives
(gamma(z)\gamma(-z)=1), so (gamma) is the constant (1) or
(-1).  The odd case would give the forbidden common factor (z).
Consequently

\[
                    {\cal S}=G(z){\cal V}(z^2)                 \tag{19}
\]

for a three-space ({\cal V}\subseteq\mathbb C[x]_{\leq M}), where

\[
              M\leq\left\lfloor{n-g\over2}\right\rfloor,
              \qquad g=\deg G.                                \tag{20}
\]

For (t\in T), if (G(t)\ne0), the plane in (15) gives two sections of
({\cal V}) vanishing to order at least two at (x=t^2).  Thus its
Wronskian has weight at least two there.  The values (t^2) are distinct.
At most (g) members of (T) can instead be roots of (G).  Hence

\[
              2(m-g)\leq3(M-2).                               \tag{21}
\]

Since a three-space requires (M\geq2), one has (g\leq n-4).  Using
(20) in (21) gives

\[
 m\leq g+{3\over2}(M-2)
    \leq {3n+g\over4}-3\leq n-4.                              \tag{22}
\]

Equations (19)--(22) now give (m\leq n-4), contradicting the temporary
assumption (m\geq n-1).  Therefore (m\leq n-2), which proves the lemma.
\(\square\)

## 5. Completion of the uniform theorem

Fix (q\in P).  For every (t\in P\setminus\{q\}), the two
three-spaces ({\cal T}_q,{\cal T}_t\subseteq{\cal K}) have intersection
dimension at least two by (13).  The cubic factors are coprime, so after
division by (f_q),

\[
 \dim\bigl({\cal S}_q\cap f_t\mathbb C[z]\bigr)\geq2.          \tag{23}
\]

Apply Lemma 4.1 to

\[
                       m=P-1,qquad n=c-4=P+C-5.               \tag{24}
\]

The hypothesis (C\leq5) gives (m\geq n-1), whereas the lemma gives
(m\leq n-2).  This contradiction proves Theorem 1.1.

## 6. Exact (p=19) census

The ninety-four survivors of the truncated-mass census split into

\[
 \begin{aligned}
  &3^a2^b1^{h+u},&&3a+2b+u=21 &&\quad(55\text{ families}),\\
  &4\,3^a2^b1^{h+u},&&3a+2b+u=17 &&\quad(39\text{ families}).
 \end{aligned}                                                \tag{25}
\]

This is also the exact classification under the previously available
routes.  The `H/S/C/L/Q/V` frontier and the selected-lift incidence
argument are already incorporated in the baseline residual set.  The
truncated-mass theorem closes every applicable profile of high excess at
least two and leaves exactly the ninety-four profiles in (25).  The
general-collision fixed-numerator theorem has eighth-split hypothesis

\[
                              h=8,                              \tag{26}
\]

so it closes none of these (13\leq h\leq18) families as presently
stated.  Finally, the (p=18) overlap and cofactor theorems use a fully
saturated relation Wronskian; at (p=19) that Wronskian has one unit of
slack, so none of those profile-specific conclusions can be imported
without a new argument.  The common-lift parity theorem above is precisely
such an argument.

For either type, select

\[
                          d=\min(b,2)                           \tag{27}
\]

exact double classes and (h+2-2d) singleton layers.  Fix all but one
selected singleton.  The moving pool has

\[
                          P=u-1+2d,                             \tag{28}
\]

and the number of fixed complementary classes is

\[
                          C=a+(b-d)+e,                          \tag{29}
\]

where (e=0) for the first line of (25) and (e=1) for the second.
The formal complement has mass nineteen, so (3) reduces exactly to
(C\leq5).  Equations (27)--(29) give precisely the ranges in (4).

For completeness, the selected-row kernel really is five-dimensional in
every case used here.  Pair drops give dimension at least four.  The
(q=6) selected Wronskian gap is

\[
                     22-h+\max(0,6-k)>0                         \tag{30}
\]

for (p=h+k=19), (13\leq h\leq18), so its dimension is at most five.
If it were four, it would equal the four-dimensional pair-drop span and
Sections 4--5 of the low-role selected-lift incidence theorem give a
contradiction.  Thus the relation three-spaces used in (6) exist exactly
as asserted.

## 7. Exact audit

[verify_live_three_zero_higher_split_p19_singleton_parity_common_lift_closure.py](../computations/verify_live_three_zero_higher_split_p19_singleton_parity_common_lift_closure.py)
reconstructs the (55+39=94) symbolic census, every selection and pool
count, the fifty-seven-family closed set, the common-kernel Wronskian
inequality, the parity degree threshold, and the gcd/square-space
Wronskian bound.
