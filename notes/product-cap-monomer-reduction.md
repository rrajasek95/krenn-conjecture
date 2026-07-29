# Product caps give an exact monomer signature, not a Schur complement

This note specializes the six-boundary formalism to the most natural cap:
a product of the all-colors covectors.  It proves two useful facts.

1. Any hypothetical \(q=3\) source at even order \(n\ge8\) has a choice of
   six surviving sites for which this product cap has nonzero scalar term
   and contracts the target exactly to \(\Delta_{6,3}\).
2. Product structure does not make the capped gadget pairwise.  A six-edge
   integer example has a nonzero four-boundary cumulant, so no universal
   hafnian Schur complement can replace it by effective pair edges.

The first fact removes the nonvanishing problem for this particular cap.
The second identifies the remaining obstruction exactly: higher boundary
cumulants, rather than a bad choice of entangled covector.

## 1. Exact monomer formula for a product cap

Let \(B=U\mathbin{\dot\cup}W\), with \(|U|=6\) and \(|W|\) even.  Put a
covector \(\ell_w\in V_w^*\) at each \(w\in W\), and write

\[
                         K=\bigotimes_{w\in W}\ell_w.       \tag{1}
\]

After retaining the natural endpoint slots, define

\[
 a_{xy}=(\ell_x\otimes\ell_y)(A_{xy})\in\mathbb C,
 \qquad
 b_{ux}=(\operatorname{id}_{V_u}\otimes\ell_x)(A_{ux})
       \in V_u                                               \tag{2}
\]

for \(x,y\in W\) and \(u\in U,x\in W\).  For even
\(T\subseteq W\), let

\[
 h(T)=\sum_{M\in\operatorname{PM}(T)}\prod_{xy\in M}a_{xy},
 \qquad h(\varnothing)=1.                                  \tag{3}
\]

For every even \(S\subseteq U\), define the boundary monomer tensor

\[
 C_S=
 \sum_{\iota:S\hookrightarrow W}
      h(W\setminus\iota(S))
      \bigotimes_{u\in S} b_{u,\iota(u)},                   \tag{4}
\]

where the sum is over injections and the tensor factors are ordered by the
named sites of \(S\).  Then

\[
 \boxed{
 K\mathbin{\lrcorner}H_B(A)
   =\sum_{\substack{S\subseteq U\\|S|\text{ even}}}
       C_S\,H_{U\setminus S}(A).}                           \tag{5}
\]

**Proof.**  In a perfect matching of \(B\), let \(S\) be the surviving
vertices whose partners lie in \(W\).  Their cross edges determine an
injection \(\iota:S\hookrightarrow W\).  The vertices
\(W\setminus\iota(S)\) are matched internally and contribute the scalar
in (3), while \(U\setminus S\) is matched internally and contributes the
last factor in (5).  Conversely, these data combine uniquely to a perfect
matching of \(B\).  Product contraction turns every cross edge into (2),
so summing proves (5). \(\square\)

Thus the cap is a finite even-monomer or loop signature.  The terms
\(C_4\) and \(C_6\) are genuine four- and six-boundary interactions; they
are not encoded by the two-boundary terms \(C_2\) in general.

## 2. A nonzero all-colors product cap always exists

Let

\[
                 \epsilon= e_0^*+e_1^*+e_2^*.             \tag{6}
\]

Suppose, hypothetically, that \(H_B(A)=\Delta_{B,3}\).  Scalarize every
edge by

\[
                 \alpha_{uv}=(\epsilon\otimes\epsilon)(A_{uv}). \tag{7}
\]

Then

\[
 \operatorname{haf}\alpha[B]
 =\epsilon^{\otimes B}H_B(A)=3.                            \tag{8}
\]

**Lemma 2.1 (three-step hafnian flag).**  There is a six-set
\(U\subseteq B\) such that, for \(W=B\setminus U\),

\[
                         \operatorname{haf}\alpha[W]\ne0. \tag{9}
\]

**Proof.**  Start with \(R_0=B\).  If
\(\operatorname{haf}\alpha[R_j]\ne0\), expand at any fixed
\(u\in R_j\):

\[
 \operatorname{haf}\alpha[R_j]
  =\sum_{v\in R_j\setminus\{u\}}
       \alpha_{uv}\operatorname{haf}
          \alpha[R_j\setminus\{u,v\}].                   \tag{10}
\]

Some summand is nonzero.  Choose its pair and call the residual set
\(R_{j+1}\).  Starting from (8), three iterations leave a set
\(R_3=W\) of size \(n-6\) satisfying (9); the six deleted endpoints form
\(U\). \(\square\)

Now cap \(W\) by the product covector

\[
                         K=\epsilon^{\otimes W}.           \tag{11}
\]

Its scalar boundary component is

\[
                         s=C_\varnothing
                          =\operatorname{haf}\alpha[W]\ne0,\tag{12}
\]

and, since \(\epsilon(e_r)=1\) for all three colors,

\[
                         K\mathbin{\lrcorner}\Delta_{B,3}
                           =\Delta_{U,3}.                  \tag{13}
\]

This is a genuine all-even-to-six contraction with all three diagonal
coefficients nonzero and with a nonzero scalar sector.  What it does not do
is eliminate the higher monomer terms in (5).

## 3. Exact cumulant and pair-conversion criterion

Work in the square-free commutative tensor algebra on \(U\).  Put

\[
 x=\sum_{u<v\in U}A_{uv},\qquad C=C_0+C_2+C_4+C_6.         \tag{14}
\]

Formula (5) is

\[
                 K\mathbin{\lrcorner}H_B(A)=[C\exp(x)]_U. \tag{15}
\]

When \(s=C_0\ne0\), write \(c_j=C_j/s\).  The finite nilpotent logarithm
is

\[
 \log(C/s)=L_2+L_4+L_6,                                   \tag{16}
\]

with

\[
 \begin{aligned}
 L_2&=c_2,\\
 L_4&=c_4-\tfrac12c_2^2,\\
 L_6&=c_6-c_2c_4+\tfrac13c_2^3.
 \end{aligned}                                             \tag{17}
\]

Consequently

\[
 \boxed{
 K\mathbin{\lrcorner}H_B(A)
  =sH_U(A+L_2)+s\{L_6+L_4(A+L_2)\}.}                       \tag{18}
\]

Here the expression in braces is already supported on all six vertices.
Thus replacing the capped region by its effective pair edges \(L_2\) is
valid at the desired top boundary exactly when

\[
                         L_6+L_4(A+L_2)=0.                 \tag{19}
\]

Replacing the gadget as a **full boundary signature**, independently of
the graph attached outside, is stricter: it is possible by pair edges
exactly when \(L_4=L_6=0\).  This follows by taking the unique nilpotent
logarithm of \(C/s\).

For the cap selected in Lemma 2.1, (13) makes the left side of (18)
\(\Delta_{6,3}\).  Since the exact six-vertex obstruction rules out an
ordinary pair realization of \(\Delta_{6,3}\), the correction in (19) is
necessarily nonzero.  Thus every hypothetical larger counterexample would
force a genuinely non-pairwise all-colors product cap; product structure
alone cannot close the induction.

## 4. A five-edge product-cap counterexample to Schur closure

The failure is already visible with four named boundary sites
\(0,1,2,3\) and two capped sites \(x,y\).  Embed the following scalar
construction in the \(e_0\) coordinate of every \(\mathbb C^3\):

\[
 xy,\quad 0x,\quad2x,\quad1y,\quad3y                       \tag{20}
\]

all have weight one, and every other edge of the gadget is zero.  Cap
\(x,y\) by the product \(\epsilon_x\otimes\epsilon_y\).  The boundary
signature has

\[
 C_\varnothing=1,qquad
 C_{01}=C_{03}=C_{12}=C_{23}=e_0e_0,                       \tag{21}
\]

with \(C_{02}=C_{13}=0\).  But

\[
                         C_{0123}=0,                       \tag{22}
\]

because the two capped vertices cannot absorb four boundary vertices.

Any pair-only replacement preserving the scalar and every two-boundary
response is forced to use the six pair tensors in (21).  Its four-boundary
response would be their hafnian:

\[
 C_{01}C_{23}+C_{02}C_{13}+C_{03}C_{12}
                         =2e_0^{\otimes4},                 \tag{23}
\]

contradicting (22).  Equivalently, (17) gives

\[
                         (L_4)_{0123}=-2e_0^{\otimes4}.    \tag{24}
\]

If one also attaches the old boundary edge \(45=e_0e_0\), equation (18)
shows the top-degree failure explicitly: the effective pair hafnian creates
\(2e_0^{\otimes6}\), and the four-cumulant term cancels it exactly.  Dropping
that term changes the contracted six-site tensor.

The dependency-free checker
`computations/verify_product_cap_four_cumulant.py` enumerates the gadget's
matchings and verifies (21)--(24) over the integers.

## 5. Consequence for an all-even reduction

The all-colors product cap is better behaved than an arbitrary cap in one
important respect: Lemma 2.1 guarantees a six-boundary choice with
\(s\ne0\), while (13) retains all three target colors automatically.  The
remaining step is now isolated to the single six-site equation (19).

The gadget in Section 4 proves that (19) is not a formal consequence of
productness.  A successful uniform proof would have to use the global
identity \(H_B=\Delta_{B,3}\) to choose a hafnian flag for which the higher
cumulant correction vanishes, or derive a contradiction directly from the
fact that every admissible flag has a nonzero correction.  Treating the
cap as an ordinary Schur complement is not valid.
