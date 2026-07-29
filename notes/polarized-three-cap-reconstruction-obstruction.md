# Polarized three-cap reconstruction retains the forbidden mixed term

## 1. Outcome

Mixed caps and trilinear polarization do not repair the loss in
`stable-six-boundary-pairification.md` by a formal reconstruction argument.
There is an exact binary `Delta_(8,2)` source and one tensor-active deleted
pair for which the denominator-cleared pair family `B(K)=F_2(K)` obeys,
for **every** bilinear cap `K`,

\[
 H_6(B(K))
   =s(K)^2\kappa _0(K)e_0^{\otimes6}
    +s(K)^2\kappa _1(K)
       \left(e_1^{\otimes6}-e_{101111}\right).            \tag{1}
\]

Here `s(K)` is the direct-edge scalar and
`kappa_i(K)=K(e_i,e_i)`.  Thus the unwanted mixed coefficient is the
negative of the intended pure-color-one coefficient as a polynomial in the
cap.

This relation survives every linear operation on cubic cap polynomials:
evaluation sums, finite differences, directional derivatives, and complete
polarization.  In particular, for three independent caps `K_1,K_2,K_3`,

\[
 [B(K_1)B(K_2)B(K_3)]_U
     =\tau _0e_0^{\otimes6}
       +\tau _1\left(e_1^{\otimes6}-e_{101111}\right),    \tag{2}
\]

where `tau_i` is exactly the trilinear polarization of
`s^2 kappa_i`.  Consequently the polarized pair tensor is diagonal only if
its intended color-one amplitude is zero.  The missing top term can be
retained algebraically, but it cannot be separated from the contamination
by any linear polarized mixed-copy operator on this cap.

This is not a ternary counterexample and does not exclude a theorem coupling
different deleted pairs.  It is an exact obstruction to the proposed
formal step from mixed copies of one cap to a clean six-site target.  The
standalone audit is
`computations/verify_polarized_three_cap_obstruction.py`.

## 2. The cubic cap map

Let `p,q` be deleted from an eight-site source and let `U` be the six
remaining sites.  For a bilinear covector `K`, write

\[
 s(K)=K(A_{pq}),\qquad
 r_{uv}(K)=K\mathbin{\lrcorner}
   (A_{pu}A_{qv}+A_{pv}A_{qu}).                           \tag{3}
\]

Both are linear in `K`.  If `x` is the old internal quadratic on `U`, the
degree-two component of the complete capped boundary signature is

\[
                         B(K)=s(K)x+r(K).                  \tag{4}
\]

The six-site hafnian `P(K)=H_6(B(K))` is therefore a homogeneous cubic
polynomial in the cap entries.  If first-jet absorption were clean, it
would satisfy

\[
                         P(K)=s(K)^2K\mathbin{\lrcorner}
                                      \Delta_{8,2}.       \tag{5}
\]

Equation (5) is just the usual identity
`H_6(x+r/s)=s^(-1)K cap Delta`, multiplied by `s^3`; no
division is used in (4)--(5).

For three cap covectors put `B_a=B(K_a)`.  Since `B` is linear,

\[
 [t_1t_2t_3]P(t_1K_1+t_2K_2+t_3K_3)
                         =[B_1B_2B_3]_U.                  \tag{6}

Indeed `P(K)=B(K)^3/3!`, and the six assignments of the three named
quadratics cancel the denominator.  Equivalently, the right side of (6) is
the third finite difference

\[
 \sum_{S\subseteq\{1,2,3\}}(-1)^{3-|S|}
             H_6\left(\sum_{a\in S}B_a\right).           \tag{7}
\]

Thus (6) is exactly the top tensor recovered by trilinear mixed-copy
polarization of the pairified degree-two data.

## 3. The exact source and its cap family

Use vertices `1,...,8` and the rational binary source

\[
\begin{array}{c|c}
12&(e_0+e_1)e_0\\
34,24&e_0e_0\\
13&-e_1e_0\\
16,23&e_1e_1\\
45&\frac34e_1e_1\\
15,46&\frac12e_1e_1\\
57,68&e_0e_0\\
78&e_1e_1.
\end{array}                                               \tag{8}
\]

Exact matching enumeration gives

\[
                         H_8(A)=\Delta_{8,2}.             \tag{9}
\]

Delete `p=1,q=3`, so

\[
                         U=(2,4,5,6,7,8).                 \tag{10}
\]

Write

\[
                         K=(k_{ij})_{0\le i,j\le1}.
\]

The direct edge in (8) gives

        s=-k_{10},\qquad \kappa _0=k_{00},\qquad
        \kappa _1=k_{11}.                                \tag{11}

Using (3)--(4), the complete list of nonzero entries of `B(K)` is

\[
\begin{array}{c|c}
24&k_{00}e_0e_0\\
25&\frac12k_{11}e_1e_1\\
26&k_{11}e_1e_1\\
45&\frac12k_{10}e_0e_1-\frac34k_{10}e_1e_1\\
46&k_{10}e_0e_1-\frac12k_{10}e_1e_1\\
57&-k_{10}e_0e_0\\
68&-k_{10}e_0e_0\\
78&-k_{10}e_1e_1.
\end{array}                                               \tag{12}
\]

The variable `k_01` drops out but is otherwise unrestricted.

Only three coloring fibers of `H_6(B(K))` are nonzero.  The all-zero fiber
has the single term

\[
                         k_{00}k_{10}^2.                  \tag{13}
\]

The all-one fiber has two terms

\[
             \frac14k_{10}^2k_{11}
             +\frac34k_{10}^2k_{11}=k_{10}^2k_{11}.      \tag{14}
\]

At the mixed word `101111` in the order (10), the same two underlying
matchings contribute

\[
             -\frac12k_{10}^2k_{11}
             -\frac12k_{10}^2k_{11}=-k_{10}^2k_{11}.     \tag{15}
\]

Every other fiber is empty by the displayed support.  Equations
(11), (13)--(15) prove (1) without a genericity or noncancellation
assumption.

## 4. The polarization obstruction

For `a=1,2,3`, put

\[
                 s_a=s(K_a),\qquad
                 \kappa_{i,a}=\kappa_i(K_a),
\]

and define

\[
 \tau_i=2\left(
       s_1s_2\kappa_{i,3}+s_1s_3\kappa_{i,2}
                         +s_2s_3\kappa_{i,1}\right).     \tag{16}
\]

This is the coefficient of `t_1t_2t_3` in

\[
 s(t_1K_1+t_2K_2+t_3K_3)^2
 \kappa_i(t_1K_1+t_2K_2+t_3K_3).                        \tag{17}
\]

Taking the same coefficient in (1), and using (6), proves (2).

There is a useful operator form which makes the scope exact.

**Theorem 4.1 (all linear cubic reconstructions fail on the fixed pair).**
Let `Lambda` be any complex linear functional on the homogeneous cubic
polynomials in the four entries of `K`.  Then

\[
 \Lambda(P)=Lambda(s^2\kappa_0)e_0^{\otimes6}
       +\Lambda(s^2\kappa_1)
          \left(e_1^{\otimes6}-e_{101111}\right).        \tag{18}
\]

If `Lambda(P)` is diagonal, its color-one coefficient is zero.

**Proof.**  Apply `Lambda` coefficientwise to the polynomial identity (1).
The mixed coefficient in (18) is
`-Lambda(s^2 kappa_1)`, exactly the negative of the color-one coefficient.
If the former vanishes, so does the latter. `QED`

The theorem includes arbitrary finite linear combinations of cap
evaluations, arbitrary derivatives, coefficient extractions, and the
trilinear polarization (6).  It also includes product caps.  For a concrete
three-product-cap instance take

\[
 K_a=(e_0^*+a_ae_1^*)\otimes(e_0^*+b_ae_1^*),qquad
 (a_1,b_1)=(1,1),\ (a_2,b_2)=(2,3),\ (a_3,b_3)=(3,2).    \tag{19}
\]

Every `s_a,kappa_(0,a),kappa_(1,a)` is nonzero, while (16) gives

\[
                         \tau_0=22,\qquad \tau_1=72.     \tag{20}
\]

The mixed-copy tensor is therefore exactly

\[
        22e_0^{\otimes6}+72e_1^{\otimes6}-72e_{101111}.  \tag{21}
\]

The polarized target part in (21) retains both colors; its unavoidable
contamination retains the second with the opposite sign.

## 5. Consequence for six-boundary reconstruction

Three-copy dilation can eliminate `L_4,L_6` but forgets `F_6`.  Polarizing
different caps is the natural attempt to reconstruct the missing cubic
information from the family `K mapsto F_2(K)`.  Equations (1)--(2) show
that this reconstruction is not formally clean even when the starting
source satisfies every global binary GHZ equation exactly and all three
chosen product caps are nondegenerate.

For this active pair, the polarized `F_6` color-one term and the polarized
higher-boundary correction span the same one-dimensional cap polynomial.
No linear recombination can cancel one without canceling the other.  A
positive ternary descent must therefore use nonlinear relations coupling
different deleted pairs, or additional lower-boundary equations not
contained in the cubic cap map of one pair.
