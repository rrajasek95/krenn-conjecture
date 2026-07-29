# The all-exceptional five-live three-zero response is injective

## 1. Outcome

Continue from
[live-three-zero-two-marked-exceptional-beta.md](live-three-zero-two-marked-exceptional-beta.md).
At the first genuine split-exception boundary,

\[
                         r=3,\qquad |U|=5,\qquad t=5,              \tag{1}
\]

all five live beta values \(\nu_1,\ldots,\nu_5\) differ from the common
centre value \(\mu\).  There are no additional nonzero singular sites.
The exceptional live-to-\(z_0\) blocks vanish automatically, so the
zero-star response has only six columns: three coordinate rows at each
of the two residual type-\(10\) centres.

**Theorem 1.1 (all-exceptional five-live injectivity).**  On the
structurally admissible locus, the complete six-column zero-star response
has rank six.  Hence every block incident from a residual nonzero site to
\(z_0\) vanishes, and \(z_0\) is isolated in \(G_3(q)\).

There is no rank-drop locus inside the admissible parameter space.  The
proof permits repeated beta values and uses no genericity, positivity, or
Borchardt distinct-value hypothesis.

Combining this with the preceding common-beta, one-exceptional,
minority-exceptional, and two-marked results closes the no-extra-singular
three-zero branch for every residual with three or five live sites.  The
uniform continuation
[live-three-zero-first-split-layers.md](live-three-zero-first-split-layers.md)
also closes both high-exception layers at seven live sites.

## 2. The complete six-column response

Let

\[
 V=\{y_1,\ldots,y_5,c_1,c_2\}
\]

be the seven residual nonzero sites.  Normalize \(P_{y_j}=I\) and

\[
                    P_{c_1}=P_{c_2}
                       =D=\operatorname {diag}(1,1,0).
\]

The internal blocks are

\[
 q_{ij}={P_iHP_j^{\mathsf T}\over\beta_i+\beta_j},\qquad
 H=\begin{pmatrix}
 0&h_{01}&h_{02}\\
 h_{01}&0&h_{12}\\
 h_{02}&h_{12}&0
 \end{pmatrix},                                                   \tag{2}
\]

where \(\beta_{y_j}=\nu_j\) and
\(\beta_{c_1}=\beta_{c_2}=\mu\).  Structural admissibility gives

\[
 h_{01}h_{02}h_{12}\mu\ne0,\qquad
 \nu_j-\mu\ne0,\quad \nu_j+\mu\ne0,\quad
 \nu_i+\nu_j\ne0\quad(i\ne j).                                   \tag{3}
\]

The first condition needed below is \(h_{01}\ne0\), which also follows
directly from the rank-two internal block between the two type-\(10\)
centres.

Fix a coordinate \(b\) at \(z_0\) and write

\[
 Z_{k,a}=q_{c_kz_0}[a,b]\qquad(k=1,2,\ a=0,1,2).                  \tag{4}
\]

For a word \(w\in\{0,1,2\}^{V}\) and source colours \(s,t\), the complete
linear response row is

\[
\begin{aligned}
 E_{w;s,t}^{(b)}
 ={}&B_{st}\sum_{k=1}^2
       Z_{k,w_{c_k}}\,
       \operatorname {haf}Q[w]_{V\setminus\{c_k\}}\\
 &+\sum_{\{u,v\}\subset V}
   \bigl(
     (P_u)_{w_u s}(P_v)_{w_v t}
     +(P_u)_{w_u t}(P_v)_{w_v s}
   \bigr)\\
 &\hspace{20mm}\cdot
   \sum_{\substack{k\in\{1,2\}\\c_k\notin\{u,v\}}}
       Z_{k,w_{c_k}}\,
       \operatorname {haf}
       Q[w]_{V\setminus\{u,v,c_k\}} .                            \tag{5}
\end{aligned}
\]

Here \(Q[w]_{ij}=q_{ij}[w_i,w_j]\), and the first hafnian has six
vertices while the second has four.  Formula (5) includes both the
direct coordinate-factor term and every choice of the two marked
factors.  The coordinate normal form has \(B_{ss}=0\), so the direct
term disappears for a diagonal source.

Equation (5) is the complete \(6\)-column map.  The proof below extracts
three families of exact \(6\times6\) minors from it.

## 3. A split with an isolated centre-star coefficient

Choose three distinct exceptional sites \(y_a,y_b,y_c\).  Give the other
two exceptional sites colour \(2\), and read the diagonal source
\(x_2z_2\).  Those two sites are the unique marked pair.

To isolate \(Z_{1,0}\), give \(c_1,y_a,y_b\) colour \(0\) and give
\(c_2,y_c\) colour \(1\).  After removing the marked pair and the star at
\(c_1\), the four-site cofactor has the two perfect matchings

\[
 (y_a,c_2)(y_b,y_c),\qquad
 (y_b,c_2)(y_a,y_c).
\]

If the star is instead at \(c_2\), the binary shores have sizes three
and one, so its cofactor is zero.  Exceptional star columns are already
zero because

\[
                         (\nu_j-\mu)q_{y_jz_0}=0.                  \tag{6}
\]

The exact isolated coefficient is therefore

\[
\begin{aligned}
 C_{ab\mid c}
 =2h_{01}^{\,2}\left[
 {1\over(\nu_a+\mu)(\nu_b+\nu_c)}
 +{1\over(\nu_b+\mu)(\nu_a+\nu_c)}
 \right].                                                        \tag{7}
\end{aligned}
\]

Swapping binary colours isolates row one.  Giving the target centre
colour \(2\), while retaining the displayed colours at the other four
unmarked sites, isolates row two: a type-\(10\) centre has no third
marked factor and no internal edge in its third row.  Interchanging
\(c_1,c_2\) gives the other three columns.  Thus the six chosen equations
form

\[
                         M_{ab\mid c}=C_{ab\mid c}I_6,\qquad
 \det M_{ab\mid c}=C_{ab\mid c}^{\,6}.                            \tag{8}
\]

Writing

\[
\begin{aligned}
 F_{ab\mid c}
 ={}&(\nu_b+\mu)(\nu_a+\nu_c)
     +(\nu_a+\mu)(\nu_b+\nu_c),
\end{aligned}
\]

gives the complete factorization

\[
 C_{ab\mid c}
 ={2h_{01}^{\,2}F_{ab\mid c}\over
   (\nu_a+\mu)(\nu_b+\mu)
   (\nu_a+\nu_c)(\nu_b+\nu_c)}.                                  \tag{9}
\]

An individual minor can vanish on the genuine cancellation hypersurface
\(F_{ab\mid c}=0\).  It is the collection of minors, rather than any
single preferred one, that is everywhere nonzero.

## 4. Exact rank-drop classification

Fix \(c\) and choose any three of the other four indices, denoted
\(a,b,d\).  Normalize the three candidate pivots by

\[
 N_{ij\mid c}
 ={(\nu_i+\nu_c)(\nu_j+\nu_c)\over2h_{01}^{\,2}}\,
       C_{ij\mid c},\qquad
 g_i={\nu_i+\nu_c\over\nu_i+\mu}.                                \tag{10}
\]

Direct substitution in (7) gives

\[
 N_{ab\mid c}=g_a+g_b,\qquad
 N_{ad\mid c}=g_a+g_d,\qquad
 N_{bd\mid c}=g_b+g_d.                                           \tag{11}
\]

Consequently

\[
             N_{ab\mid c}+N_{ad\mid c}-N_{bd\mid c}=2g_a.        \tag{12}
\]

If the complete response had rank below six, all three minors in (8)
would vanish.  Equations (11) would give

\[
                         g_a=g_b=g_d=0.                           \tag{13}
\]

But \(g_a=0\) says \(\nu_a+\nu_c=0\), contradicting (3).  Hence at least
one of the three explicitly displayed minors is nonzero.

This also classifies the common rank-drop locus exactly.  In the
localization defined by (3), the ideal generated by the three normalized
pivots in (11) is the unit ideal.  Before excluding poles, their common
zero set forces

\[
             \nu_a+\nu_c=\nu_b+\nu_c=\nu_d+\nu_c=0,               \tag{14}
\]

which lies entirely on forbidden live--live denominator divisors.
The additional factor \(h_{01}=0\) in (9) is likewise forbidden by the
rank-two centre--centre block.  Therefore every possible common
rank-drop component is outside the domain on which the structural
factorization (2) is defined.  Repeated values such as
\(\nu_a=\nu_b\) are harmless unless they also violate one of the sums in
(3).

## 5. Graph contradiction

The argument holds independently for all three choices of \(b\), so
both type-\(10\)-centre blocks to \(z_0\) vanish.  Equation (6) kills the
five live-star blocks.  The blocks from \(z_0\) to the other two literal
zeros vanish because all three zero beta values are \(-\mu\), and its
blocks to the removed type-\(22\) centres are singular coordinate
ports.  Thus \(z_0\) has no incident rank-three edge, contradicting the
connected-spanning hypothesis on \(G_3(q)\).

## 6. Exact audit

[verify_live_three_zero_all_exceptional_five_live.py](../computations/verify_live_three_zero_all_exceptional_five_live.py)
implements the complete response formula (5) over
\(\mathbb Q(\mu,\nu_1,\ldots,\nu_5,h_{01},h_{02},h_{12},B_{01})\).
It reconstructs the three symbolic diagonal minors (8), factors their
pivots as in (9), and verifies the cover identity (12).

As an independent exhaustive check, the script enumerates all
\(3^7\) words and all nine ordered source-colour pairs at an admissible
rational specialization.  The resulting complete map has \(9200\)
nonzero rows and rank six.
