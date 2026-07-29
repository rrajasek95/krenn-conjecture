# Higher splits: a moving-triple common-lift closure at (p=19)

## 1. Uniform theorem

Let ({\mathscr X}) be a set of (a) exact triple value classes.  Keep the
same singleton layers and any same additional repeated layers selected,
but let one member (x\in{\mathscr X}) supply a role-two layer.  Its third
label remains complementary at (x).  Assume every such formal selection
has a five-dimensional selected-row kernel and a relation three-space.
Let its complement have (c) value classes and six-capped mass (M_6).

**Theorem 1.1 (moving-triple common lift).**  If (M_6\leq27), the
configuration is impossible when

\[
 \boxed{
 \begin{array}{c|c}
 c\leq7&a\geq2,\\
 c=8&a\geq6.
 \end{array}}                                                  \tag{1}
\]

At (p=19), this closes four further boundary families:

\[
 \boxed{
 3^6 2^2 1^{h-1},\qquad
 3^7 1^h,\qquad
 3^7 2\,1^{h-2},\qquad
 4\,3^5 2^2 1^{h-2}.}                                         \tag{2}
\]

They are disjoint from both preceding (p=19) common-lift closures.
The combined new ledger is therefore seventy-five of ninety-four families.

## 2. The exact quartic transport

For the selection using the triple value (x), let

\[
              {\cal S}_x\subseteq\mathbb C[z]_{\leq c-4},
              \qquad\dim{\cal S}_x=3.                         \tag{3}
\]

In the exact rational derivative, the selected profile has a simple
complementary root at (x), hence denominator ((z-x)^2), and the
selected role-two layer contributes ((z+x)^2).  The baseline in which
that layer is not selected has the exact-triple denominator
((z-x)^4).  Their exact quotient is the even quartic

\[
                         B_x(z)=(z-x)^2(z+x)^2.                 \tag{4}
\]

The selected simple-root row supplies the one derivative not killed
automatically by the square.  Explicitly, if (R) is the selected local
regular product, its row is (R'(x)=0), while the baseline triple row on
the transported polynomial is

\[
                     \bigl((z-x)^2R(z)\bigr)'''\big|_{z=x}
                              =6R'(x)=0.                        \tag{5}
\]

At every other row (B_x) is a structural unit and ordinary product-rule
transport applies.  Hence all moving choices lie in one kernel:

\[
 {\cal T}_x:=B_x{\cal S}_x\subseteq{\cal K}
       \subseteq\mathbb C[z]_{\leq N},\qquad
                  \dim{\cal T}_x=3,qquad N=c.                 \tag{6}
\]

## 3. Dimension and the subcritical range

The baseline changes the complementary multiplicity at (x) from one to
three.  Thus a hypothetical six-space in ({\cal K}) has forced
Wronskian weight

\[
                         6c-(M_6+2),                            \tag{7}
\]

whereas its degree-(N=c) cap is

\[
                         6(N+1-6)=6c-30.                       \tag{8}
\]

It would require (M_6\geq28).  The usual exact-row gcd correction is
nonnegative, so

\[
                             \dim{\cal K}\leq5.                 \tag{9}

For distinct nonopposite (x,y), the quartics (B_x,B_y) are coprime,
and

\[
 B_x\mathbb C[z]_{\leq N-4}\cap
 B_y\mathbb C[z]_{\leq N-4}
      =B_xB_y\mathbb C[z]_{\leq N-8}.                          \tag{10}
\]

If (N=c\leq7), this intersection is zero, while two three-spaces in
the at-most-five-space (9) must meet nontrivially.  Two moving triples
suffice, proving the first line of (1).

## 4. The degree-eight third-jet complete graph

Let (N=8).  Equation (10) is a line, so (9) gives

\[
                           B_xB_y\in{\cal K}                    \tag{11}

for every distinct pair (x,y\in{\mathscr X}).  Fix a tested triple
value (v), and write (Omega={\mathscr X}\setminus\{v\}).  Its common
baseline row is

\[
                         (U B_xB_y)'''(v)=0,                    \tag{12}

where one regular unit (U), independent of (x,y), satisfies
(U(v)\ne0).

Put

\[
 A_x={B_x'(v)\over B_x(v)}={4v\over v^2-x^2}.                  \tag{13}

The next two normalized jets are polynomial functions of (A_x):

\[
 {B_x''(v)\over B_x(v)}={A_x^2\over2}+{A_x\over v},
 \qquad
 {B_x'''(v)\over B_x(v)}={3A_x^2\over2v}.                     \tag{14}

Expanding (12) and absorbing all terms depending on only one index into a
function (F) gives

\[
 C+F(A_x)+F(A_y)
 +A_xA_y\left(L+{3\over2}(A_x+A_y)\right)=0,                  \tag{15}

where (C,L) depend only on (U) and (v).  Taking the alternating
difference of (15) over four distinct indices gives

\[
 (A_i-A_j)(A_k-A_\ell)
 \left(L+{3\over2}(A_i+A_j+A_k+A_\ell)\right)=0.              \tag{16}

The values (A_x), (x\in\Omega), are pairwise distinct: equality in
(13) gives (x^2=y^2), and distinct classes are neither equal nor
opposite.  Thus every four-element subset of the (A)-values has the same
sum (-2L/3).  Five distinct values are impossible, because two
four-subsets differing in one element would make those two elements
equal.  Consequently (|\Omega|\leq4), or (a\leq5).  This proves the
second line of (1).

## 5. Exact (p=19) specialization

If at least one exact double is available, select it together with the
moving triple and select (h-2) singleton layers.  If no double is
available, select only the moving triple and (h) singleton layers.  Let
(e\in\{0,1\}) record the quartic class.  The exact common degree is

\[
 N=c=
 \begin{cases}
 21-2a,&e=0,\ b=0,\\
 22-2a-b,&e=0,\ b\geq1,\\
 18-2a,&e=1,\ b=0,\\
 19-2a-b,&e=1,\ b\geq1.
 \end{cases}                                                  \tag{17}

The four profiles in (2) give respectively
((a,N)=(6,8),(7,7),(7,7),(5,7)), and their leftover singleton counts
are nonnegative.  Conversely, applying (1) to the exact ninety-four-family
census produces no other profiles beyond those already closed by the two
earlier common-lift routes.

Every selection used here has a five-dimensional selected-row kernel:
the (q=6) gap is strict at (p=19), and a dimension-four kernel would
equal the pair-drop span and is excluded by the low-role incidence
argument, including the possible triple--zero missing edge.

## 6. Exact residual frontier after all three routes

Nineteen (p=19) families remain.  In parameter form they are

\[
\begin{array}{c|l}
3^a2^b1^{h+u}
 &(0,8,5),(0,9,3),(0,10,1),(0,11,-1),\\
 & (1,7,4),(1,8,2),(1,9,0),\\
 & (2,6,3),(2,7,1),(3,5,2),(4,4,1),(6,0,3),(6,1,1);\\[1mm]
4\,3^a2^b1^{h+u}
 &(0,7,3),(0,8,1),(1,6,2),(2,5,1),(5,0,2),(5,1,0).
\end{array}                                                   \tag{18}
\]

Here each tuple is ((a,b,u)).  Their most useful exact stratification is
by the number (C) of complementary value classes outside a moving
singleton pool:

\[
             C=6:\ 12,\qquad C=7:\ 4,\qquad
             C=8:\ 2,\qquad C=9:\ 1.                         \tag{19}
\]

The (C=6) block is the next uniform boundary.  In the parity proof its
odd minors have a two-dimensional, rather than one-dimensional, fixed
numerator space.  Their exterior-map kernel gives a square pencil, and the
square-pencil Wronskian bound is exactly saturated.  A useful next step is
therefore to compare those equality pencils for two different fixed
moving singletons; another isolated one-pool count will not improve the
bound.

Six residual profiles also sit on the dense-double degree-eleven equality
surface:

\[
 (0,11,-1),(1,9,0),(2,7,1),(3,5,2);qquad
 (0,8,1),(1,6,2),                                             \tag{20}
\]

where the first four tuples are no-quartic and the last two are
one-quartic.  There each pair of quintic-multiple ambient spaces meets in
a pencil.  Compatibility of those pair pencils across three moving double
partners is the second concrete next target.  The remaining small equality
graphs (3^4 2^4 1^{h+1}), (4\,3^2 2^5 1^{h+1}), and the two
one-quartic five-triple profiles require simultaneous tested baselines,
because a single complete graph has too few vertices for the fibre
arguments above.

## 7. Exact audit

[verify_live_three_zero_higher_split_p19_triple_common_lift_closure.py](../computations/verify_live_three_zero_higher_split_p19_triple_common_lift_closure.py)
checks the four formal selections, the degree and capped-mass identities,
the quartic transport jets, all coprime-intersection dimensions, the
third-derivative normalization and four-index alternating difference, the
injectivity of (13), and the combined (75/94) ledger.
