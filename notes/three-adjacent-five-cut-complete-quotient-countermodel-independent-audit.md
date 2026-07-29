# Independent audit: three adjacent complete five-cut quotients

## 1. Verdict and scope

The construction in
[the primary note](three-adjacent-five-cut-complete-quotient-countermodel.md)
passes an independent reconstruction over \(\mathbb Q\).  In particular:

\[
 H_B=e_1^{\otimes8}+e_2^{\otimes8}+e_{00210012},
 \qquad
 D:=H_B-\Delta_{8,3}=e_{00210012}-e_0^{\otimes8},
\]

and the same residual satisfies

\[
 D\in E_2\cap E_3\cap E_4,
 \qquad
 (\dim W_{U_2},\dim W_{U_3},\dim W_{U_4})=(1,1,2).
\]

The equivalence between this cylinder condition and the complete
high-sector quotient identity is valid with endpoint order, parallel
decorated sources, and complex cancellation retained.  The two appended
sources also kill the stated mixed word while preserving all three active
quotients and the defect dimensions \((1,1,2)\).

No mathematical gap was found.  Two scope restrictions are essential.
First, neither family is monochromatic: the first misses the constant-zero
coefficient, and the repaired family still has three mixed coefficients.
Second, the asserted support-minimality is deletion-only minimality among
the twelve displayed, fixed-colour, fixed-weight sources and for the fixed
cuts \(z=2,3,4\).  It is not global minimality under reweighting, changing
decorations, or replacing sources.

The standalone exact checker is
[`verify_three_adjacent_five_cut_complete_quotient_countermodel_independent_audit.py`](../computations/verify_three_adjacent_five_cut_complete_quotient_countermodel_independent_audit.py).
It does not import the primary checker.

## 2. Re-derivation of the cut equivalence

For each site \(i\), let \(V_i=\mathbb C^3\), and put

\[
 V_X=\bigotimes_{i\in X}V_i
\]

with tensor factors always restored to increasing named-site order.  A
source on \(u<v\), with colours \((a,b)\) at \((u,v)\) and weight \(w\),
contributes \(w e_a^{(u)}\otimes e_b^{(v)}\).  Thus its aggregate edge
block is

\[
 A_{uv}=\sum_{\substack{\text{sources }s\\N(s)=\{u,v\}}}
 w(s)e_{k(s,u)}^{(u)}\otimes e_{k(s,v)}^{(v)}.
\]

The perfect-matching tensor on a vertex set \(X\) is

\[
 H_X(A)=\sum_{M\in\operatorname{PM}(X)}
             \bigotimes_{uv\in M}A_{uv}.                 \tag{1}
\]

Expanding every aggregate block in (1) chooses one decorated source on
each matched pair.  Conversely every source-level consistent matching
appears exactly once.  This proves the decorated-source equivalence by
multilinearity.  It also shows why parallel cells may be summed before the
matching expansion and why cancellations inside a block remain valid.
Nothing exchanges the two endpoint colours: reversing a site's listing
must reverse its cell coordinates at the same time.

Fix a five-set \(U\) and its three-site complement \(C\).  Write

\[
 h_u=H_{U\setminus\{u\}}(A),\qquad
 \mathcal S_U=\sum_{u\in U}V_u\otimes h_u\subseteq V_U,
 \qquad E_U=V_C\otimes\mathcal S_U.                      \tag{2}
\]

Both shores have odd cardinality, so a perfect matching crosses the cut
either once or three times.  In a one-crossing atom, the unique crossing
edge meets some \(u\in U\); after deleting that edge, the other four
vertices of \(U\) contribute one term of \(h_u\).  The crossing cell can
be endpoint-asymmetric, and the two remaining sites of \(C\) may carry an
arbitrary aggregate edge tensor, but their product still belongs to

\[
             V_C\otimes(V_u\otimes h_u)\subseteq E_U.
\]

Summing atoms, parallel choices, and cancelling coefficients therefore
gives

\[
                         T_1\in E_U.                     \tag{3}
\]

Let \(K_U=\mathcal S_U^\perp\subseteq V_U^*\), where this is the
algebraic annihilator, and let

\[
 \Delta_{8,3}=\sum_{r=0}^2e_r^{\otimes8}.
\]

For \(\beta\in V_U^*\), contraction of the target is

\[
 (\operatorname{id}_C\otimes\beta)\Delta_{8,3}
   =\sum_{r=0}^2\beta(e_r^{\otimes U})e_r^{\otimes C}.   \tag{4}
\]

Choose a basis of \(V_C\) and view a tensor in \(V_C\otimes V_U\) as a
list of rows in \(V_U\).  Every \(\beta\in K_U\) annihilates every row of
\(X\) if and only if every row lies in
\((\mathcal S_U^\perp)^\perp=\mathcal S_U\).  Finite-dimensional
annihilator duality consequently gives

\[
 \begin{aligned}
 &(\operatorname{id}_C\otimes\beta)T_3
   =\sum_r\beta(e_r^{\otimes U})e_r^{\otimes C}
       \quad\text{for every }\beta\in K_U\\
 &\hspace{45mm}\Longleftrightarrow\quad
                  T_3-\Delta_{8,3}\in E_U.              \tag{5}
 \end{aligned}
\]

Since \(H_B=T_1+T_3\), equation (3) proves both directions of

\[
 \boxed{\text{complete quotient identity on }C\mid U
        \quad\Longleftrightarrow\quad
        H_B-\Delta_{8,3}\in E_U.}                        \tag{6}
\]

This is a statement about the complete aggregate tensors, so it does not
discard cancellations term by term.

For later use, define

\[
 \delta_U(\beta)=\sum_{r=0}^2
       \beta(e_r^{\otimes U})e_r,\qquad
 \mathcal G_U=\operatorname{span}\{e_r^{\otimes U}:0\le r<3\}.
\]

The transpose of \(\delta_U\) identifies the three-dimensional target
dual with \(\mathcal G_U\).  The annihilator of
\(\delta_U(K_U)\) is therefore identified with
\(\mathcal G_U\cap\mathcal S_U\).  Rank-nullity yields

\[
 \dim W_U=\dim\delta_U(K_U)
          =3-\dim(\mathcal G_U\cap\mathcal S_U).          \tag{7}
\]

## 3. Independent expansion of the twelve sources

The twelve nonzero decorated cells are

\[
\begin{array}{c|c@{\qquad}c|c}
01&E_{00}&45&E_{00}\\
02&E_{11}&14&E_{11}\\
36&E_{11}&57&E_{11}\\
04&E_{22}&13&E_{22}\\
27&E_{22}&56&E_{22}\\
25&E_{00}&35&E_{10}.
\end{array}                                               \tag{8}
\]

The last entry means colour one at site \(3\) and colour zero at site
\(5\).  Enumeration of all \(7\cdot5\cdot3=105\) perfect matchings finds
exactly three supported ones:

\[
\begin{array}{c|c}
01,27,36,45&00210012\\
02,14,36,57&11111111\\
04,13,27,56&22222222.
\end{array}                                               \tag{9}
\]

All weights are one, proving the formulas for \(H_B\) and \(D\) in the
verdict.  In particular, the asymmetric \(35\) cell is not silently
symmetrized.

## 4. The three cylinder decompositions

The exact four-site cofactors needed below are

\[
\begin{array}{c|c}
H_{0145}&e_{0000}\\
H_{0135}&e_{0010}\\
H_{0125}&e_{0000}\\
H_{0134}&e_{2222}\\
H_{0124}&e_{1111}.
\end{array}                                               \tag{10}
\]

Each equality follows by enumerating the three possible pairings on the
listed four sites.  The first three give the following literal
decompositions of the same \(D\).  For \(z=2\), with
\(C_2=(2,6,7)\),

\[
 D=e_{212}^{C_2}\otimes
       \bigl(e_1^{(3)}\otimes H_{0145}\bigr)
   -e_{000}^{C_2}\otimes
       \bigl(e_0^{(3)}\otimes H_{0145}\bigr)\in E_2.    \tag{11}
\]

For \(z=3\), with \(C_3=(3,6,7)\),

\[
 D=e_{112}^{C_3}\otimes
       \bigl(e_2^{(2)}\otimes H_{0145}\bigr)
   -e_{000}^{C_3}\otimes
       \bigl(e_0^{(2)}\otimes H_{0145}\bigr)\in E_3.    \tag{12}
\]

For \(z=4\), with \(C_4=(4,6,7)\),

\[
 D=e_{012}^{C_4}\otimes
       \bigl(e_2^{(2)}\otimes H_{0135}\bigr)
   -e_{000}^{C_4}\otimes
       \bigl(e_0^{(3)}\otimes H_{0125}\bigr)\in E_4.    \tag{13}
\]

All factors in (11)--(13) are placed back in their named site slots.  The
standalone checker constructs each cofactor separately and verifies that
each displayed two-term sum is exactly \(D\), not merely a tensor with the
same support.

The three-crossing sectors provide a second check:

\[
 T_{3,2}=e_1^{\otimes8},\qquad
 T_{3,3}=e_2^{\otimes8},\qquad
 T_{3,4}=H_B.                                             \tag{14}
\]

Equations (6) and (11)--(13) therefore prove all three complete quotient
identities.

## 5. Exact defect spaces

The constant tensors contained in the insertion spaces are

\[
\begin{array}{c|c|c}
z&\mathcal G_{U_z}\cap\mathcal S_{U_z}&W_{U_z}\\ \hline
2&\langle e_0^{\otimes U_2},e_2^{\otimes U_2}\rangle
   &\langle e_1\rangle\\
3&\langle e_0^{\otimes U_3},e_1^{\otimes U_3}\rangle
   &\langle e_2\rangle\\
4&\langle e_0^{\otimes U_4}\rangle
   &\langle e_1,e_2\rangle.
\end{array}                                               \tag{15}
\]

The positive inclusions use the cofactors in (10): insert the missing site
with the same colour.  For every omitted colour, the corresponding
constant-word coordinate is zero on every insertion column, because no
four-site internal cofactor has a perfect matching of that constant
colour.  Its coordinate functional consequently annihilates all of
\(\mathcal S_{U_z}\), while evaluating to one on the omitted constant
word.  This proves the reverse inclusions without an assumption that
individual matching terms are nonnegative or noncancelling.  Equation (7)
now gives the dimensions \((1,1,2)\).

As an independent computational check of (5), the audit script row-reduces
the insertion columns in the \(3^5\)-dimensional word basis, constructs an
explicit basis of the entire annihilator \(K_{U_z}\), and verifies the two
sides of the quotient identity on every annihilator-basis vector.  It also
checks the residual cylinder membership separately.

## 6. What the minimality computation certifies

For each of the \(2^{12}-2=4094\) nonempty proper subsets of (8), the
checker retains the displayed endpoint colours and unit weights, rebuilds
all three cofactor-insertion spaces from that subfamily, and tests

\[
 T_{3,z}-\Delta_{8,3}\in V_{C_z}\otimes\mathcal S_{U_z},
 \qquad \dim\delta_{U_z}(\mathcal S_{U_z}^\perp)>0
 \quad(z=2,3,4).                                         \tag{16}
\]

No proper subfamily satisfies all six conditions.  The empty subfamily
also fails (16), since its high sector is zero while the target contraction
is not.  Hence the twelve-source family is deletion-minimal for this fixed
triple and these fixed coefficients.

This exhaustion does not quantify over new weights on the retained cells,
new endpoint decorations, different cut triples, or unrelated source
supports.  Calling it global support-minimality would be unjustified.

## 7. Independent check of the two-source repair

Append

\[
                  A_{23}\mathrel{+}=E_{21},\qquad
                  A_{67}\mathrel{+}=-E_{12}.             \tag{17}
\]

Besides the original three matchings, the enlarged support has four new
matchings involving \(67\):

\[
\begin{array}{c|c|c}
01,23,45,67&00210012&-1\\
02,13,45,67&12120012&-1\\
02,14,35,67&11111012&-1\\
04,13,25,67&22022012&-1.
\end{array}                                               \tag{18}
\]

The first row cancels the original mixed term exactly.  Thus

\[
 H'_B=e_1^{\otimes8}+e_2^{\otimes8}
      -e_{12120012}-e_{11111012}-e_{22022012}.            \tag{19}
\]

The checker rebuilds the repaired spaces \(\mathcal S'_{U_z}\) rather than
reusing the old ones.  Exact rational row reduction and, independently,
direct contraction on a full basis of each annihilator give

\[
 H'_B-\Delta_{8,3}\in E'_2\cap E'_3\cap E'_4,
 \qquad
 (\dim W'_{U_2},\dim W'_{U_3},\dim W'_{U_4})=(1,1,2).    \tag{20}
\]

Therefore the repair claim is correct: imposing the single coefficient
equation at \(00210012\) does not close this three-cut relaxation.  Its
scope is existential.  It does not show that arbitrary mixed coordinates
can always be repaired, that the debt can be transported indefinitely, or
that a sufficiently coupled collection of mixed equations cannot force a
contradiction.

## 8. Audit conclusion

The construction is an exact countermodel to the sufficiency of three
active complete adjacent five-cut quotients, even after one selected mixed
coefficient is killed.  It is not a counterexample to Krenn's conjecture.
A successful continuation may use these three cuts together with stronger
global information, but it cannot derive the GHZ equations from the shared
cylinder condition and target activity alone.
