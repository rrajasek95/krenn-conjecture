# A response two-jet leaves the terminal \(h=3\) middle class

## 1. Outcome

Fix an off-diagonal full-nine row and write

\[
 \alpha=d_{ab}\ne0,\qquad R=p_as_b,\qquad
 Q_j=R^{[j]}q^{[3-j]}\quad(0\leq j\leq3).
 \tag{1}
\]

Translate the internal quadratic in the response direction while holding
the response fixed:

\[
 q_t=q+tR,\qquad f(t)=\alpha q_t^{[3]}+R q_t^{[2]}.
 \tag{2}
\]

Then

\[
 \boxed{
 f(t)=(\alpha Q_0+Q_1)
      +t(\alpha Q_1+2Q_2)
      +t^2(\alpha Q_2+3Q_3)
      +t^3\alpha Q_3.}
 \tag{3}
\]

Consequently, if a source construction supplies the three
response-translation equations through order two, the clean tail is only
reduced to the terminal cubic class:

\[
 \boxed{
 \chi:=\alpha Q_2+Q_3=-2Q_3
       =-{2\over\alpha}[t^3]f(t).}
 \tag{4}
\]

Thus the translated two-jet equations do not by themselves yield the
triangular transgression. Their exact remaining obstruction is one
terminal coefficient. The third equation

\[
                         \alpha Q_3=0                  \tag{5}
\]

is indispensable. It is the same last equation used by the full unipotent
derivation argument, but (3)--(4) show that it is not a technical extra:
it is exactly the nonclean tail.

There is a parallel coding-theoretic location for this class. After
uniform substitution, a degree-six ternary row whose coefficients at
Hamming distance at most two from every pure word vanish is supported on
the ten-dimensional **count-type quotient**

\[
 \boxed{
 \begin{aligned}
 \mathcal C_6^{\mathrm{count}}={}&
 \langle x_i^3x_j^3:i<j\rangle\\
 &\oplus
 \langle x_i^3x_j^2x_k:\{i,j,k\}=\{0,1,2\}\rangle
 \oplus\langle x_0^2x_1^2x_2^2\rangle .
 \end{aligned}}
 \tag{6}
\]

The three summands have dimensions \(3,6,1\). This is not the literal
word space: uniform substitution sums coefficients of words having the
same colour counts. Before that summation, the central word space has

\[
 3\binom63+
 6{6!\over3!2!1!}+{6!\over2!2!2!}
 =60+360+90=510                                      \tag{7}
\]

coordinates. On one literal binary face its middle layer has
\(\binom63=20\) words; uniform substitution sends their sum to the single
count monomial \(x_i^3x_j^3\).

This identifies a short possible positive route: construct one
source-provenant, target-compatible map sending \([t^3]f\) into the
literal 510-coordinate middle space, or into (6) together with a proof
that the count projection detects the scalar. The complete all-word rows
would kill the image, and (4) would then kill the tail.

No such landing map is proved here. Nor does this abstract calculation
refute the full structured implication from all Hamming-two rows, the
other eight rows, Segre factorization, and all three anchors to
cleanliness: those nonlinear constraints could still force the terminal
class. What is ruled out is the narrower inference from the three
translated-jet equations, and any merely linear radius-two inference that
never reaches the middle sector. This note does not modify the certified
spine and does not resolve Krenn's conjecture.

## 2. Exact response-jet calculation

The divided-power binomial identities give

\[
 \begin{aligned}
 (q+tR)^{[3]}&=Q_0+tQ_1+t^2Q_2+t^3Q_3,\\
 R(q+tR)^{[2]}&=Q_1+2tQ_2+3t^2Q_3.
 \end{aligned}                                         \tag{8}
\]

Adding the two lines with coefficients \(\alpha\) and \(1\) proves (3).
If the second-order coefficient vanishes, then

\[
                 \alpha Q_2+3Q_3=0.                   \tag{9}
\]

Subtracting (9) from the tail gives (4). Neither the constant nor the
first-order equation can remove \(Q_3\); they only determine lower
response grades above it.

The independence is visible in the exact scalar jet module

\[
 \alpha=1,\qquad (Q_0,Q_1,Q_2,Q_3)=(-6,6,-3,1).       \tag{10}
\]

For (10), the four coefficients of \(f\) are

\[
                         (0,0,0,1),                    \tag{11}
\]

while

\[
                         \chi=-2.                      \tag{12}
\]

This is an abstract response-grade counterpacket, not a decorated graph
source and not a full-nine/Segre counterpacket. Its force is narrow and
exact: the three lower translated coefficients do not imply a clean tail
unless some additional hypothesis kills (5).

## 3. The literal and count-type middle sectors

Uniformly substitute \(x_0,x_1,x_2\) for the three physical labels on
the six residual sites of one fixed endpoint row. This forgets site
positions and retains only the \(S_6\)-symmetrized colour count. A word
with counts \((n_0,n_1,n_2)\) contributes to
\(x_0^{n_0}x_1^{n_1}x_2^{n_2}\), where

\[
                         n_0+n_1+n_2=6.                \tag{13}
\]

Its Hamming distance from the pure \(c\)-word is \(6-n_c\). Vanishing
at distance at most two from all three pure words removes precisely the
count monomials with some \(n_c\geq4\). The survivors satisfy

\[
                         0\leq n_c\leq3
                         \quad(c=0,1,2).               \tag{14}
\]

The solutions of (13)--(14) are the permutations of

\[
                         (3,3,0),\qquad(3,2,1),
                         \qquad(2,2,2),                \tag{15}
\]

giving \(3+6+1=10\) count types and proving (6). Restoring site
positions gives the multiplicities in (7), hence 510 literal central
words.

On a binary face, the missing colour has exponent zero, so (13)--(14)
force the other exponents to be \(3,3\). The radius-two equations at the
two ends kill degrees \(0,1,2,4,5,6\), while the 20-word degree-three
layer survives. The all-word row kills it too.

The independently proved
[colour-torus two-jet boundary](color-torus-pure-limit-two-jet-boundary.md)
fits this calculation exactly: its first and second colour-torus jets are
freely solvable, and its first genuine compatibility occurs in degree
three, with an explicit \((3,2,1)\) word. Equation (4) newly identifies
the clean defect with the terminal class of the response-translation
filtration. The two filtrations therefore meet in the same degree, but no
existing theorem constructs the chain map between them.

## 4. The minimal new source statement

Let \(\mathcal J_{ab;c}\) be the one-dimensional terminal quotient of
(3), generated by \([t^3]f\). Let
\(\mathcal K_6^{\mathrm{mid}}\) be the 510-dimensional literal middle word
space, and let \(\mathcal C_6^{\mathrm{count}}\) be its ten-dimensional
uniform count quotient (6). A sufficient new statement is a
source-derived map

\[
 \Theta_{ab;c}:\mathcal J_{ab;c}
               \longrightarrow\mathcal K_6^{\mathrm{mid}}
 \tag{16}
\]

with the following properties:

1. it is computed from the same adjacent full-nine block array, rather
   than chosen after evaluating a row;
2. it respects response grade and the selected direct scalar \(\alpha\);
3. it sends target-zero rows to target-zero middle coefficients; and
4. it detects \([t^3]f\), either before count projection or after a
   separately proved injective count readout.

The most economical count-level version lands in one binary midpoint
line \(\langle x_c^3x_e^3\rangle\). That version must prove that uniform
summation detects the response class rather than cancelling it. If no
single binary face is canonical, the honest target is
\(\mathcal K_6^{\mathrm{mid}}\), whose count quotient also retains the
six oriented \((3,2,1)\) types and the \((2,2,2)\) centre.

There is an exact formula for the candidate readout. For a three-set
\(S=\{i,k,p\}\) with complement \(T\), and symmetric edge arrays
\(A,B,Q\), define

\[
 \begin{aligned}
 \Theta_S(A,B,Q)={}&
 \sum_{\{i,k\}\subset S}
 A_{ik}\sum_{j\in T}B_{pj}Q_{T\setminus\{j\}}\\
 &+\operatorname{per}(B_{S,T}),
 \end{aligned}                                         \tag{17}
\]

where \(p\) is the member of \(S\setminus\{i,k\}\), and
\(Q_{T\setminus\{j\}}\) is the edge on the remaining two members of
\(T\). Then the following marking identity holds for arbitrary \(Q,R\):

\[
 \boxed{
 \alpha R^{[2]}Q+R^{[3]}
 ={1\over8}\sum_{\substack{S\subset\{0,\ldots,5\}\\|S|=3}}
       \Theta_S(2\alpha R,R,Q).}                       \tag{18}
\]

To prove (18), fix a perfect matching with two \(R\)-edges and one
\(Q\)-edge. A contributing three-set contains neither endpoint of the
\(Q\)-edge, both endpoints of one \(R\)-edge, and one endpoint of the
other. There are \(2\cdot2=4\) choices. The internal edge has weight
\(2\alpha R\), so the total multiplicity is \(8\alpha\). A perfect
matching with three \(R\)-edges crosses precisely the eight cuts obtained
by choosing one endpoint of each edge; the permanent counts it once on
each cut. Division by eight gives (18).

Once (16) exists, the actual all-word full-nine identity makes its image
zero. Detection gives \([t^3]f=0\), and (4) gives \(\chi=0\). This uses
exactly one more response grade than a two-jet and is strictly weaker than
constructing a global site derivation.

Identity (18) is exactly the formal local formula suggested by the
[three-face cubic Bianchi equation](all-three-binary-cofactor-plane-boundary.md).
Its equations (18) and (21) split the first genuine third-jet coefficient
into three connection-times-cofactor terms plus one \(3\times3\)
permanent. The equality here is a formal polynomial identity after the
substitution

\[
                         (A,B,Q)=(2\alpha R,R,q).       \tag{19}
\]

There is an equivalent one-parameter form which makes the meeting with
the colour-torus filtration literal. Uniformly mark both ends of every
edge in the auxiliary binary packet. Its scalar quadratic is

\[
 \widehat q(t)=q+2tR+2\alpha t^2R,
 \qquad
 \boxed{[t^3]\widehat q(t)^{[3]}=8\chi.}               \tag{20}
\]

Indeed, the degree-three terms are
\((2tR)^{[3]}=8t^3R^{[3]}\) and
\(q(2tR)(2\alpha t^2R)=8\alpha t^3R^{[2]}q\).
Thus (18) is exactly the third uniform torus coefficient of the canonical
response two-jet, not merely an analogy between two degree filtrations.

This also isolates the physical normalization defect. Let a candidate
binary landing packet have directed first cells \(b^L,b^R\), second cells
\(A\), and leading cells \(q\), and put \(B=b^L+b^R\) after uniform
specialization. Its twenty midpoint coefficients sum to

\[
 [t^3](q+tB+t^2A)^{[3]}=ABq+B^{[3]}.                  \tag{21}
\]

Hence the exact discrepancy from the desired landing is

\[
 \boxed{
 \mathfrak D(A,B)
 :=ABq+B^{[3]}-8\bigl(\alpha R^{[2]}q+R^{[3]}\bigr).}  \tag{22}
\]

If \(B=2R+\beta\) and \(A=2\alpha R+\gamma\), direct divided-power
expansion gives the denominator-free formula

\[
\begin{aligned}
 \mathfrak D(A,B)={}&
 (2\alpha R\beta+2R\gamma+\gamma\beta)q\\
 &+4R^{[2]}\beta+2R\beta^{[2]}+\beta^{[3]}.           \tag{23}
\end{aligned}
\]

Literal normalization

\[
                         B=2R,\qquad A=2\alpha R       \tag{24}
\]

is sufficient, but stronger than necessary: an adjacent construction only
has to make \(\mathfrak D(A,B)\) vanish in the target-zero middle quotient.
Moreover, (18) needs cutwise three-site representatives, not one globally
integrable site derivation. When (24) is demanded tensorially from
sitewise first deformations, its first equation becomes the scaled tangent
equation; the audited Hamming-two packet shows that such a global tangent
need not exist, but that packet is already clean. Thus (22)--(23) give the
exact smaller target for a tangent-or-clean proof: route the aggregate
cubic defect, or prove that failure to route it kills \(\chi\) directly.

It does **not** assert that the physical first and second colour-torus
jets supplied by an adjacent chart already equal the three entries in
(19). Establishing precisely that landing modulo the killed companion
grades, equivalently killing (22), together with target compatibility, is
the remaining chain-map problem.

The existing seven-row physical guard explains why (16) must use the
complete diagonal sector. Its selected off-diagonal row is zero on every
word while its clean tail is nonzero; two complementary diagonal targets
are missing. Thus neither the selected binary midpoint alone nor its
ordinary all-word vanishing defines \(\Theta\). The map must import the
simultaneous diagonal target provenance, most naturally from an adjacent
chart.

## 5. Audit

The dependency-free
[checker](../computations/verify_h3_nonclean_twojet_middle_core.py)
verifies (3)--(4) over exact rational packets, checks (10)--(12),
enumerates the ten count types and 510 literal words in (15), and verifies
the 20-word binary midpoint layer. It also verifies (18) on exact signed
rational edge arrays, checks (20)--(23), and detects the factor-two
normalization in (19).
It remains live under optimized and isolated Python.
