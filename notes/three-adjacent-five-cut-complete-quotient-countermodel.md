# Three adjacent complete five-cut quotients still admit a shared residual

## 1. Result

Let

\[
 B=S\mathbin{\dot\cup}R,\qquad
 S=\{0,1,2,3,4,5\},\qquad R=\{6,7\},
\]

and let every site space be (V_i=\mathbb C^3).  For (z\in S), put

\[
 U_z=S\setminus\{z\},\qquad C_z=R\cup\{z\}.
\]

This note isolates the exact first shared condition supplied by three
adjacent five-cuts.  If (H_B(A)) is the matching tensor and
(D=H_B(A)-\Delta_{8,3}), then the complete high-sector quotient identity
on the cut (C_z\mid U_z) is equivalent to

\[
 D\in E_z:=V_{C_z}\otimes {\cal S}_{U_z},                 \tag{1}
\]

where ({\cal S}_{U_z}) is the full internal cofactor-insertion space.
Thus three complete adjacent identities say that the **same** residual
satisfies

\[
             D\in E_x\cap E_y\cap E_z.                   \tag{2}
\]

This is strictly stronger than the two-cut conditions already known to
coexist.

Condition (2), even together with a nonzero target quotient on all three
cuts, is still not contradictory.  A twelve-source integral decorated
edge family below has

\[
 D\in E_2\cap E_3\cap E_4,
 \qquad
 \dim W_{U_2}=1,\quad \dim W_{U_3}=1,\quad \dim W_{U_4}=2. \tag{3}
\]

The full tensor has one mixed coefficient and is missing one target
coefficient, so this is not a Krenn counterexample.  It is an exact
countermodel to the claim that three active complete five-cut quotients,
or their common residual-intersection form (2), already force the GHZ
equations.

The exact audit is
[`verify_three_adjacent_five_cut_complete_quotient_countermodel.py`](../computations/verify_three_adjacent_five_cut_complete_quotient_countermodel.py).

## 2. The common-residual form of the cut identities

For a five-set (U), write

\[
 h_u=H_{U\setminus\{u\}}(A),\qquad
 {\cal S}_U=\sum_{u\in U}V_u\otimes h_u,
 \qquad K_U={\cal S}_U^\perp.                             \tag{4}
\]

Let ({\cal G}_U) denote the span of the three constant words, and set

\[
 W_U=\delta_U(K_U),\qquad
 \delta_U(\beta)=\sum_{r=0}^2
       \beta(e_r^{\otimes U})e_r.                         \tag{5}
\]

Equivalently,

\[
 \dim W_U=3-\dim({\cal G}_U\cap{\cal S}_U).              \tag{6}
\]

Let (T_{1,z}) and (T_{3,z}) be the one- and three-crossing sectors for
(C_z\mid U_z).  These are the only possible sectors because both shores
have odd size.  Every one-crossing matching has a unique exposed
(u\in U_z).  After removing its crossing edge, the other four vertices
of (U_z) contribute (h_u).  Consequently, with all factors restored to
their named endpoint slots,

\[
                  T_{1,z}\in V_{C_z}\otimes{\cal S}_{U_z}=E_z.       \tag{7}
\]

This is an atomwise factorization and is valid for arbitrary
endpoint-ordered complex aggregate matrices, including parallel sources
and cancellations inside every cofactor.

The complete quotient identity is

\[
 (\operatorname{id}_{C_z}\otimes\beta)T_{3,z}
   =\sum_{r=0}^2\beta(e_r^{\otimes U_z})e_r^{\otimes C_z}
                 \qquad(\beta\in K_{U_z}).               \tag{8}
\]

By finite-dimensional annihilator duality, (8) is equivalent to

\[
             T_{3,z}-\Delta_{8,3}\in E_z.                \tag{9}
\]

Since (H_B=T_{1,z}+T_{3,z}), equations (7) and (9) give the promised
equivalence

\[
       \boxed{\ (8)\quad\Longleftrightarrow\quad
                         H_B-\Delta_{8,3}\in E_z.\ }     \tag{10}
\]

Under a hypothetical GHZ equality, (8) holds on all six cuts and the
universal five-set theorem gives (W_{U_z}\ne0) on each one.  Hence (2)
with three nonzero defects is an exact necessary relaxation of the actual
coefficient system, rather than a formal matching-term replacement.

## 3. Twelve explicit endpoint-decorated sources

For (u<v), let (E_{ab}^{uv}=e_a^{(u)}\otimes e_b^{(v)}).  Give every
listed source weight one, put the displayed cell in its aggregate edge
block, and set every omitted block equal to zero:

\[
\begin{array}{c|c@{\qquad}c|c}
uv&A_{uv}&uv&A_{uv}\\ \hline
01&E_{00}&45&E_{00}\\
02&E_{11}&14&E_{11}\\
36&E_{11}&57&E_{11}\\
04&E_{22}&13&E_{22}\\
27&E_{22}&56&E_{22}\\
25&E_{00}&35&E_{10}.
\end{array}                                               \tag{11}
\]

The last block is genuinely endpoint-asymmetric: its colour is one at
site (3) and zero at site (5).

There are exactly three supported perfect matchings:

\[
\begin{array}{c|c|c}
 &\text{matching}&\text{endpoint-colour word in site order }0,\ldots,7\\ \hline
M_*&01,45,36,27&00210012\\
M_1&02,14,36,57&11111111\\
M_2&04,13,27,56&22222222.
\end{array}                                               \tag{12}
\]

Therefore

\[
 H_B=e_1^{\otimes8}+e_2^{\otimes8}+e_{00210012},
 \qquad
 D=e_{00210012}-e_0^{\otimes8}.                          \tag{13}
\]

In particular the mixed coefficient (00210012) is (1), while the
constant-zero coefficient is (0).  This explicitly explains why (11)
is not monochromatic and is not a counterexample to Krenn's conjecture.

## 4. The same residual lies in three insertion cylinders

All tensors below are placed in their named site slots.  For (z=2), use

\[
 C_2=(2,6,7),\qquad U_2=(0,1,3,4,5),\qquad
 H_{0145}=e_{0000}.
\]

Then

\[
 D=e_{212}^{C_2}\otimes
       \bigl(e_1^{(3)}\otimes H_{0145}\bigr)
   -e_{000}^{C_2}\otimes
       \bigl(e_0^{(3)}\otimes H_{0145}\bigr)\in E_2.    \tag{14}
\]

For (z=3), use

\[
 C_3=(3,6,7),\qquad U_3=(0,1,2,4,5),
\]

and the same four-site cofactor to get

\[
 D=e_{112}^{C_3}\otimes
       \bigl(e_2^{(2)}\otimes H_{0145}\bigr)
   -e_{000}^{C_3}\otimes
       \bigl(e_0^{(2)}\otimes H_{0145}\bigr)\in E_3.    \tag{15}
\]

For (z=4), use

\[
 C_4=(4,6,7),\qquad U_4=(0,1,2,3,5),
\]

and the two coordinate cofactors

\[
 H_{0135}=e_{0010},\qquad H_{0125}=e_{0000}.              \tag{16}
\]

They give

\[
 D=e_{012}^{C_4}\otimes
       \bigl(e_2^{(2)}\otimes H_{0135}\bigr)
   -e_{000}^{C_4}\otimes
       \bigl(e_0^{(3)}\otimes H_{0125}\bigr)\in E_4.    \tag{17}
\]

Equations (14)--(17) prove (2) directly, without ranks or division.

For completeness, the three high sectors themselves are

\[
 T_{3,2}=e_1^{\otimes8},\qquad
 T_{3,3}=e_2^{\otimes8},\qquad
 T_{3,4}=e_1^{\otimes8}+e_2^{\otimes8}+e_{00210012}.     \tag{18}
\]

Thus (8) holds on all three complete kernels by (10).

## 5. All three target quotients are active

The constant tensors which lie in the insertion spaces are exactly

\[
\begin{aligned}
 {\cal G}_{U_2}\cap{\cal S}_{U_2}
   &=\langle e_0^{\otimes U_2},e_2^{\otimes U_2}\rangle,\\
 {\cal G}_{U_3}\cap{\cal S}_{U_3}
   &=\langle e_0^{\otimes U_3},e_1^{\otimes U_3}\rangle,\\
 {\cal G}_{U_4}\cap{\cal S}_{U_4}
   &=\langle e_0^{\otimes U_4}\rangle.                 \tag{19}
\end{aligned}
\]

The asserted members are explicit in (14)--(17), together with the pure
colour-two cofactor (H_{0134}=e_{2222}) for (U_2\setminus\{5\}) and
the pure colour-one cofactor (H_{0124}=e_{1111}) for
(U_3\setminus\{5\}).  For each omitted constant word, no cofactor
insertion column has a nonzero coordinate at that word: after deleting
any one site, the remaining four internal vertices do not have a perfect
matching of the omitted constant colour.  The corresponding constant-word
coordinate dual therefore annihilates the entire insertion space.  This
proves both inclusions in (19), and hence

\[
 W_{U_2}=\langle e_1\rangle,\qquad
 W_{U_3}=\langle e_2\rangle,\qquad
 W_{U_4}=\langle e_1,e_2\rangle.                         \tag{20}
\]

So the countermodel satisfies the complete quotient map on three adjacent
cuts and has a target-active kernel on every one of them.

## 6. Exact audit and scope

The checker enumerates all (105) perfect matchings and every endpoint
word over the integers, reconstructs (12)--(13), verifies the explicit
three decompositions (14)--(17), and performs rational sparse row reduction
for the full maps (8) and intersections (19).  It also exhausts all
(4094) nonempty proper subfamilies of the twelve displayed sources; none
retains the active complete quotient identities simultaneously on the
fixed triple (z=2,3,4).  The empty subfamily fails trivially.  Thus (11)
is support-minimal inside its displayed source family for this fixed
triple.  This finite minimality statement is not a claim of global
minimality among all decorated edge families.

The conclusion is sharp but negative: the first three-cut shared
kernel/quotient invariant does not attack the conjecture.  A continuation
must use at least a fourth adjacent cut or an equation which directly
forces the lone mixed coefficient in (13) to vanish; merely placing the
common residual in three cofactor-insertion cylinders loses that equation.

## 7. Killing that mixed word still does not close the triple

The first literal strengthening of (2) is to add the actual GHZ equation

\[
                 [e_{00210012}]H_B=0.                    \tag{21}
\]

Even (21) does not close the three-cut system.  Append to (11) the two
sources

\[
                   A_{23}\mathrel{+}=E_{21},\qquad
                   A_{67}\mathrel{+}=-E_{12}.            \tag{22}
\]

The new matching (01,23,45,67) has word (00210012) and weight (-1),
so it cancels the unique mixed term in (13) exactly.  Direct enumeration
instead gives

\[
\begin{aligned}
 H_B'={}&e_1^{\otimes8}+e_2^{\otimes8}
  -e_{12120012}-e_{11111012}-e_{22022012}.               \tag{23}
\end{aligned}
\]

In particular (21) now holds.  Exact rational row reduction nevertheless
gives, for the new residual (D'=H_B'-\Delta_{8,3}),

\[
 D'\in E_2'\cap E_3'\cap E_4',
 \qquad
 (\dim W_{U_2}',\dim W_{U_3}',\dim W_{U_4}')=(1,1,2).    \tag{24}
\]

Thus the same sparse family is repairable after imposing the first missing
mixed coefficient: two additional endpoint-ordered integral cells move
the debt to three other mixed words while preserving all three active
complete quotient maps.  The checker verifies (22)--(24) over
\(\mathbb Q\), including every full matching word.  Consequently a
positive continuation cannot select and kill mixed residual coordinates
one at a time; it must couple a sufficiently large mixed sector, or add a
fourth adjacent cut in a way that prevents this debt transport.
