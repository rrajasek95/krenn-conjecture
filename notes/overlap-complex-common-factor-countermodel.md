# The pair-annihilator overlap complex has a common-factor kernel

## 1. Outcome

The homogeneous overlap map in
[`overlapping-pair-cap-bianchi-connection.md`](overlapping-pair-cap-bianchi-connection.md)
is not acyclic under the presently established good-pair graph hypotheses.
There is a universal Koszul module in its kernel:

\[
                 N_{pq}^{ab}=L_a\,S_{q,b},                         \tag{1}
\]

where \(S_{q,b}\) is the physical colour-\(b\) star from \(q\), and
\(L_a\) is one linear form common to the charts in a fixed \(p\)-fan.
Commutativity gives the overlap equation before any matching power is
applied.

This note gives a uniform rational same-source model in which the elements
in (1) are also literal pair-Hessian annihilators.  For every chart in the
fan:

1. both deleted star triples are injective and every row reaches every
   internal site;
2. the rank-three graph is connected, spanning, and nonbipartite;
3. the common-factor corrections form a nine-dimensional space modulo the
   conventional zero-sum vertex gauges; and
4. every triple-overlap and triangle Bianchi equation holds literally.

Thus neither connected nonbipartiteness, dense good stars, nor exact
same-source overlap makes (28) injective.  The missing condition is not a
stronger graph adjective.  One must either quotient the common-factor
Koszul module or use the exact mixed target/four-cut equations to kill it.
The model deliberately fails those target equations, and its odd-cycle
edges are top-inactive.  It therefore identifies the precise missing
source-level input rather than giving a Krenn counterexample.

The construction also shows that flatness alone does **not** produce an
active clean cap.  Its overlap curvature is identically zero, while the
nonlinear cap error \({\cal E}_{p,q}(K)\) is not constrained.

## 2. The universal Koszul submodule

Fix a site \(p\), put \(U=B\setminus\{p\}\), and let \(F\subset U\) be a
set of fan neighbours.  For \(q\in F\), write

\[
 W_q=U\setminus\{q\},\qquad
 S_{q,b}\in {\cal R}_1(W_q)                                    \tag{2}
\]

for the restriction of the physical colour-\(b\) star from \(q\).  If
\(q,r\in F\) are distinct, all forms below are restricted to
\(W_{qr}=U\setminus\{q,r\}\).  Package the homogeneous overlap differential
as

\[
 (dN)_{qr}^{abc}
   =N_{pq}^{ab}S_{r,c}-N_{pr}^{ac}S_{q,b}.                       \tag{3}
\]

This is equation (28) of the connection note with endpoint order retained.

**Lemma 2.1 (common-factor kernel).**  Choose arbitrary linear forms
\(L_a\in{\cal R}_1(U)\), \(0\le a\le2\), and define

\[
 N_{pq}^{ab}=(L_a|_{W_q})S_{q,b}.                                \tag{4}
\]

Then \(dN=0\).

**Proof.**  Restrictions commute, so on \(W_{qr}\) the two sides of (3)
are

\[
 (L_a|_{W_{qr}})S_{q,b}S_{r,c},\qquad
 (L_a|_{W_{qr}})S_{r,c}S_{q,b}.
\]

They agree by commutativity in the site-square-zero algebra.  Colliding
site terms vanish on both sides, so no support or nonvanishing hypothesis
is hidden in the argument. \(\square\)

Let \({\cal K}_p\) denote the module of families (4).  In Čech language,
the \(S_q\)'s are chart sections and multiplication by one global \(L\)
is a global degree-one Koszul section.  Equation (3) is its Čech
difference.  The triangle Bianchi identity is then the tautology
\(d^2=0\); it cannot detect a global section of \({\cal K}_p\).

For the pair-cap problem one also requires

\[
 N_{pq}^{ab}q_q^{[m-2]}=0,                                    \tag{5}
\]

where \(q_q\) is the quadratic internal to \(W_q\).  The point of the next
construction is that the E1/E2 graph data do not force
\({\cal K}_p\cap\prod_q\operatorname {Ann}(q_q^{[m-2]})\) to be zero or
gauge.

## 3. A uniform physical source

Fix \(s\ge5\), let

\[
 B=L\mathbin{\dot\cup}R,\qquad |L|=|R|=s,                       \tag{6}
\]

and choose \(p\in L\).  At every site use \(V_i=\mathbb C^3\) with basis
\(e_{i,0},e_{i,1},e_{i,2}\).  Put

\[
 \lambda={1\over s!}.                                           \tag{7}
\]

Define one endpoint-ordered aggregate quadratic \(A\) by the following
blocks, written from the \(L\)-endpoint first:

\[
 A_{ij}=\begin{cases}
 I_3, &i,j\in L,\ i\ne j,\\
 \lambda I_3, &i=p,\ j\in R,\\
 I_3, &i\in L\setminus\{p\},\ j\in R,\\
 0, &i,j\in R.
 \end{cases}                                                   \tag{8}
\]

Reverse endpoint order means transpose, exactly as usual.  The matrices
in (8) happen to be symmetric, but no identification of the two endpoint
spaces is made.

Every perfect matching of \(B\) uses no \(L\)-\(L\) edge.  Indeed, since
there is no \(R\)-\(R\) edge, using an \(L\)-\(L\) edge would leave more
\(R\)-vertices than \(L\)-vertices.  Hence the supported perfect matchings
are exactly the \(s!\) bijections \(L\to R\).  At a constant colour each
has weight \(\lambda\), so

\[
 [X_c^B]A^{[s]}=s!\lambda=1\qquad(0\le c\le2).                  \tag{9}
\]

Thus the three pure coefficients are exactly normalized in one physical
source.  This fact is included only to rule out a normalization artefact;
the mixed target coefficients do not vanish.

## 4. Every same-shore fan chart is dense E1 with a nonbipartite graph

Take the fan

\[
                         F=L\setminus\{p\}.                       \tag{10}
\]

For \(q\in F\), put \(L_q=L\setminus\{p,q\}\) and
\(W_q=L_q\mathbin{\dot\cup}R\).  The internal quadratic \(q_q=A|_{W_q}\)
has an invertible block on every \(L_q\)-\(L_q\) and \(L_q\)-\(R\) pair,
and a zero block on every \(R\)-\(R\) pair.  Therefore

\[
 G_3(q_q)=K_{s-2}\vee\overline {K_s}.                            \tag{11}
\]

This graph is connected and spanning.  It is nonbipartite because any
edge in \(K_{s-2}\), together with any vertex of \(R\), is a triangle.

The colour rows from \(q\) are

\[
 S_{q,b}=\sum_{i\in W_q}e_{i,b}.                                 \tag{12}
\]

The rows from \(p\) have coefficient \(1\) on \(L_q\) and coefficient
\(\lambda\) on \(R\).  Projection to any one internal site identifies
either star triple with a nonzero scalar multiple of the standard basis.
Both triples are consequently injective, and each of their six rows has
site support \(2s-2\).  Thus every pair \(\{p,q\}\) is good in the exact
aggregate-star sense used by the E1/E2 reduction.

Define the common forms

\[
 L_a=\sum_{i\in L\setminus\{p\}}e_{i,a},\qquad
 \ell_a^{(q)}=L_a|_{W_q}=\sum_{i\in L_q}e_{i,a},                 \tag{13}
\]

and the nine corrections

\[
                         N_{pq}^{ab}=\ell_a^{(q)}S_{q,b}.          \tag{14}
\]

Since \(s\ge5\), even the shorter factor \(\ell_a^{(q)}\) reaches at
least three sites.  The construction is therefore not the two-site
support boundary.

## 5. Exact annihilation and exact overlap

Here \(|B|=2s\), so the pair-Hessian multiplier is
\(q_q^{[s-2]}\).

**Proposition 5.1 (physical annihilators).**  For all \(q\in F\) and all
\(a,b\),

\[
                         N_{pq}^{ab}q_q^{[s-2]}=0.                 \tag{15}
\]

**Proof.**  Every monomial of \(N_{pq}^{ab}\) uses at least one vertex of
\(L_q\).  It uses either one \(L_q\)-vertex and one \(R\)-vertex, or two
\(L_q\)-vertices.  In the first case the unused sites have shore counts

\[
                         (s-3,s-1),                               \tag{16}
\]

and in the second they have counts

\[
                         (s-4,s).                                 \tag{17}
\]

Every edge of \(q_q\) uses at least one \(L_q\)-vertex, because its
\(R\)-\(R\) blocks are zero.  Neither (16) nor (17) can be covered by
\(s-2\) such edges.  Thus every matching monomial in (15) is zero.  This
is a support impossibility, so arbitrary complex coefficients and all
colour superpositions are retained. \(\square\)

**Proposition 5.2 (literal flatness).**  The family (14) lies in the
kernel of every homogeneous overlap equation (3), and hence satisfies
every triangle Bianchi equation.

**Proof.**  This is Lemma 2.1.  Explicitly, for distinct \(q,r\in F\),
both sides on \(B\setminus\{p,q,r\}\) equal

\[
       (L_a|_{B\setminus\{p,q,r\}})S_{q,b}S_{r,c}.               \tag{18}
\]

No matching power or annihilator quotient is used. \(\square\)

## 6. The cocycles are not vertex gauges

For a matrix \(C=(c_{ab})\in\operatorname {Mat}_3(\mathbb C)\), set

\[
                         N_{pq}(C)=\sum_{a,b}c_{ab}N_{pq}^{ab}.    \tag{19}
\]

On every block \(ij\) with \(i\in L_q\), \(j\in R\), the block of (19)
is \(C\).  On an \(L_q\)-\(L_q\) block it is \(C+C^{\mathsf T}\).

There are two relevant gauge spaces in this degenerate chart:

\[
 {\cal G}_q^0=\{Z^\alpha:\textstyle\sum_i\alpha_i=0\},\qquad
 {\cal G}_q^{\rm all}=\{Z^\alpha:\alpha\in\mathbb C^{W_q}\}.       \tag{20}
\]

The first is the conventional unavoidable Hessian gauge used in the E1
quotient.  The second is the full image of the vertex-scaling map.  They
need not coincide when the internal top power vanishes.  Their blocks are

\[
                         (Z^\alpha)_{ij}=(\alpha_i+\alpha_j)(q_q)_{ij}. \tag{21}
\]

If \(N_{pq}(C)=Z^\alpha\), comparison on one cross block forces \(C\) to
be scalar, say \(C=\mu I_3\).  Comparing all cross blocks and all
\(L_q\)-\(L_q\) blocks then gives uniquely

\[
             \alpha_i=\mu\ (i\in L_q),\qquad
             \alpha_j=0\ (j\in R).                              \tag{22}
\]

Its coordinate sum is \((s-2)\mu\).  Therefore no nonzero \(N_{pq}(C)\)
is a conventional zero-sum gauge.  Moreover, every nonscalar \(C\) lies
outside even the full vertex-gauge image.

The map \(C\mapsto N_{pq}(C)\) is injective by its value on one cross
block.  Thus (14) gives a nine-dimensional space modulo
\({\cal G}_q^0\); its image modulo \({\cal G}_q^{\rm all}\) still has
dimension eight.
In particular the cocycle is not a disguised choice of gauge
representatives.

Notice that \(q_q^{[s-1]}=0\), again by shore imbalance.  This explains
why the scalar \(C=\mu I_3\) direction in (22) belongs to
\({\cal G}_q^{\rm all}\) and is Hessian-annihilating even
though the corresponding vertex weights do not sum to zero.  The eight
nonscalar directions do not rely on that scalar degeneracy.

## 7. The exact missing hypothesis

The model satisfies the strongest graph and star hypotheses currently
available on the dense connected-nonbipartite E1 stratum, but it fails
three source-level conditions which those hypotheses do not encode.

1. **Mixed target rows.**  Give one vertex of each shore colour \(1\) and
   every other vertex colour \(0\), with the distinguished vertex \(p\)
   coloured \(0\).  Exactly \((s-1)!\) cross-shore bijections respect this
   colouring, each of weight \(1/s!\).  Hence its mixed coefficient is

   \[
                             {1\over s}\ne0,                       \tag{23}
   \]

   whereas a ternary GHZ tensor requires zero.
2. **Top activity of the odd-cycle edges.**  No \(L\)-\(L\) cell occurs in
   a top matching, because there is no \(R\)-\(R\) block.  The triangles
   making (11) nonbipartite are therefore top-inactive padding.  An
   entry-minimal exact source cannot justify those cells merely from the
   rank-three graph.
3. **Pair-complement activity.**  After deleting one \(L_q\)-vertex and
   one \(R\)-vertex from \(W_q\), the two shores have sizes \(s-3\) and
   \(s-1\), so the complementary top power is zero.  Thus the
   pair-complement activity available on gauge-rigid charts is absent on
   this E1 chart.

Consequently a valid filtered-injectivity theorem needs an explicit
source-level saturation hypothesis.  The exact algebraic condition it
must control is

\[
 {\cal K}_p\cap
 \prod_{q\in F}\operatorname {Ann}(q_q^{[m-2]}),                  \tag{24}
\]

not merely the connectedness or parity of the graphs \(G_3(q_q)\).
Pair-complement activity is a natural candidate input, but the present
argument does not claim it is sufficient.  Alternatively, one can retain
the actual constant-colour and mixed four-cut rows and prove directly that
they kill (24).

This is also the correct Čech interpretation.  Curvature detects failure
of local representatives to glue.  It cannot kill an honest global
common-factor section.  One needs either a quotient by that section or a
separate nonlinear equation on the global section.

## 8. No clean-cap bridge yet

The family (14) has zero overlap curvature identically.  Zero curvature
only says that the annihilator representatives glue in the Koszul sense;
it supplies neither

\[
 s=\langle K,A_{pq}\rangle\ne0,qquad
 \kappa_0\kappa_1\kappa_2\ne0,                                  \tag{25}
\]

nor the nonlinear homogeneous cap equation

\[
                         {\cal E}_{p,q}(K)=0.                      \tag{26}
\]

Indeed, the construction fails the mixed target equation (23) before an
active clean-cap descent can even be asked of it.  Therefore the overlap
complex does **not** yet bridge to an active clean cap.

The natural next theorem is narrower than acyclicity:

> In an exact ternary source, the constant-colour and four-cut equations
> either kill the common-factor module (24), or force its common linear
> factors through one proper colour subbundle that is already
> contradictory.

That statement attacks the surviving cohomology rather than trying to
prove a false graph-theoretic vanishing theorem.

## 9. Audit

The dependency-free checker
[`verify_overlap_complex_common_factor_countermodel.py`](../computations/verify_overlap_complex_common_factor_countermodel.py)
audits the smallest dense instance \(s=5\) over the rationals.  It checks
the normalized pure coefficients and mixed residual (23), the good-star
projections, the graph in (11), all nine Hessian annihilators, every
pairwise overlap equation, and the block comparison proving the gauge
claim.  The uniform proof is the shore-count and common-factor argument
above, not a finite search.
