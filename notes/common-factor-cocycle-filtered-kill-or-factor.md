# Common-factor cocycles obey a filtered kill-or-factor theorem

## 1. Outcome

The common-factor overlap kernel has a rigid physical shadow.  Fix a fan
centre \(p\), let \(Q=A|_{B\setminus\{p\}}\), and suppose

\[
                   N_{pq}^{ab}=L_aS_{q,b}                         \tag{1}
\]

is a pair-Hessian annihilator for every \(q\) in a good fan.  Put

\[
                         T_a=L_aQ^{[m-1]}.                         \tag{2}
\]

An exact coefficient identity shows that, at every fan site \(q\),

\[
                         T_a=L_{a,q}\otimes q_q^{[m-1]},           \tag{3}
\]

where \(q_q=Q|_{B\setminus\{p,q\}}\).  Thus, whenever the pair top powers
are nonzero, exactly one of the following happens.

1. \(T_a=0\), and \(L_a\) vanishes at every fan site.
2. \(T_a\ne0\), and it factors simultaneously through the local lines
   \(\mathbb CL_{a,q}\) at all fan sites.

For the three indices \(a\), all nonzero local factors at a fixed fan site
lie on one common line.  This is the promised proper local colour
subbundle for the \(L_a\)'s.

With the natural physical-span provenance, the actual target rows make
this much stronger.  Write the three physical \(p\)-star rows as \(P_c\).
If

\[
                         L_a=\sum_cM_{ac}P_c,                       \tag{3a}
\]

then the exact one-site equations force

\[
                         \operatorname {rank}M\le1.                 \tag{3b}
\]

More precisely, every nonzero row of \(M\) is supported on the same one
of the three target colours.  Hence the \(L_a\)'s factor through one
physical colour row.  Literal provenance \(L_a=P_a\), or any provenance
matrix of rank at least two, is impossible.  This is the precise
kill-or-factor theorem requested by the corrected E1 gate.  The remaining
interface is to prove that the overlap factors really lie in the physical
\(p\)-star span.

Without that provenance, there is still a sharp filtered extension to the
physical star rows.  In the nonzero branch, on every double overlap the
three star rows have one-dimensional image under the one-hole
multiplication map

\[
 \mu_{qr}:H\longmapsto H\,z_{qr}^{[m-2]}.                         \tag{3c}
\]

If these maps are injective, two overlapping deletions contradict
goodness.  Hence on the one-hole-injective stratum every \(L_a\) is
supported outside the good fan; if the fan contains all neighbours, the
common-factor cocycle vanishes.

Pair-complement activity does **not** imply the required one-hole
injectivity.  A four-site exact colon countermodel in Section 8 has every
pair complement active and every source cell active, but (3c) has a
two-dimensional kernel.  The corrected gate is therefore:

\[
\boxed{\begin{array}{c}
\text{physical-span factor killed or reduced to one target colour;}\\
\text{without provenance, common factor killed on the good fan}\\
\text{or an explicit one-hole colon kernel survives.}
\end{array}}                                                     \tag{3d}
\]

This advances synchronization by removing the flat Koszul obstruction on
the filtered-injective stratum.  It does not produce an active clean cap:
the surviving branch has zero overlap curvature, and no equation here
forces \({\cal E}_{p,q}(K)=0\).

There is also an essential scope correction.  If \(N_{pq}\) is merely a
choice of representative modulo a Hessian annihilator, the target and
four-cut equations cannot kill it: those equations depend on the source,
not on the representative.  A stronger conclusion requires **physical
provenance** tying \(N_{pq}\) to an actual response or source variation.

## 2. Physical notation and the contraction identity

Let \(|B|=2m\), put

\[
 U=B\setminus\{p\},\qquad |U|=2t+1,\qquad t=m-1,                 \tag{6}
\]

and work in the site-square-zero algebra on \(U\).  Write

\[
                         Q=A|_U\in{\cal R}_2(U).                   \tag{7}
\]

For \(q\in U\), put

\[
 W_q=U\setminus\{q\},\qquad q_q=Q|_{W_q},                        \tag{8}
\]

and let \(S_{q,b}\in{\cal R}_1(W_q)\) be the endpoint-ordered colour-\(b\)
star from \(q\).  Thus

\[
              Q=q_q+\sum_{b=0}^2e_{q,b}S_{q,b}.                  \tag{9}
\]

No symmetry of the aggregate blocks is assumed; reversing an endpoint
transposes the relevant block before its row is inserted in (9).

Let \(L\in{\cal R}_1(U)\), and write

\[
                         L=L|_{W_q}+L_q,\qquad L_q\in V_q.        \tag{10}
\]

For a basis covector \(e_{q,b}^*\), divided-power expansion of (9) gives

\[
\begin{aligned}
 \iota_{q,b}\bigl(LQ^{[t]}\bigr)
   &=(L_q)_b\,q_q^{[t]}
     +(L|_{W_q})S_{q,b}q_q^{[t-1]}.                              \tag{11}
\end{aligned}
\]

There are exactly two matching layers: \(L\) occupies \(q\), or the
\(Q\)-edge incident with \(q\) does.  No factorial occurs in divided-power
notation.

Suppose now that \(L=L_a\) and (1) is a literal pair-Hessian annihilator:

\[
             (L_a|_{W_q})S_{q,b}q_q^{[t-1]}=0
             \qquad(0\le b\le2).                                 \tag{12}
\]

Put

\[
                  C_q=q_q^{[t]},\qquad T_a=L_aQ^{[t]}.            \tag{13}
\]

Equation (11) becomes

\[
                         \iota_{q,b}T_a=(L_{a,q})_bC_q.           \tag{14}
\]

Since \(T_a\) has top site degree on \(U\), its three contractions at
\(q\) reconstruct it.  Therefore

\[
                         \boxed{T_a=L_{a,q}\otimes C_q.}          \tag{15}
\]

This identity uses only the physical common quadratic and the literal
annihilator equation.  Zero blocks, complex cancellation, and arbitrary
local colour superpositions are retained.

## 3. Physical-span provenance gives the exact kill-or-factor theorem

Assume now the actual constant-colour equations at the fan centre \(p\).
If \(P_c\in{\cal R}_1(U)\) is its physical colour-\(c\) star row, then

\[
                             P_cQ^{[t]}=X_c^U
                             \qquad(0\le c\le2).                    \tag{15a}
\]

Suppose the common factors have physical-span provenance:

\[
                             L_a=\sum_{c=0}^2M_{ac}P_c             \tag{15b}
\]

for one scalar matrix \(M\).  This includes literal provenance
\(L_a=P_a\), for which \(M=I_3\).

**Theorem 3.1 (physical-span kill-or-one-colour factorization).**  Assume
(12) for one fan site \(q\), and assume (15a)--(15b).  Then all nonzero
entries of \(M\) lie in one column.  In particular,

\[
                              \operatorname {rank}M\le1.           \tag{15c}
\]

If that column is \(c_*\), then

\[
 L_a=M_{a c_*}P_{c_*},\qquad
 L_{a,q}\in\mathbb Ce_{q,c_*},\qquad
 C_q\in\mathbb CX_{c_*}^{W_q}                                  \tag{15d}
\]

for every nonzero row \(a\).  If (12) holds throughout a fan, the last two
statements hold at every fan site.

**Proof.**  Equations (2) and (15a)--(15b) give

\[
                             T_a=\sum_cM_{ac}X_c^U.                \tag{15e}
\]

On the other hand, (15) says \(T_a=L_{a,q}\otimes C_q\), whose singleton
flattening at \(q\) has rank at most one.  In (15e), the vectors
\(e_{q,c}\) are independent and the complementary pure tensors
\(X_c^{W_q}\) are independent.  The same flattening therefore has rank
exactly the number of nonzero entries in row \(a\) of \(M\).  Every row
has support at most one.

Suppose two nonzero rows select distinct columns \(c\ne d\).  The first
row and (15) force the common nonzero complement factor \(C_q\) to be
proportional to \(X_c^{W_q}\).  The second forces the same \(C_q\) to be
proportional to \(X_d^{W_q}\), impossible.  Thus every nonzero row selects
one common column \(c_*\), proving (15c).  Comparing the two rank-one
decompositions of \(M_{a c_*}X_{c_*}^U\) proves (15d). \(\square\)

**Corollary 3.2 (literal physical factors are impossible).**  No
common-factor annihilator family satisfying (12) can have
\(L_a=P_a\).  More generally, no physical-span provenance matrix of rank
at least two is possible.

This theorem uses the full normalized one-site target rows, including all
their mixed zero coefficients through the tensor equalities (15a).  It is
not a support or generic-rank argument.  The actual mixed four-cut rows are
contractions of (15a), so no selected-row relaxation is being substituted.
It proves the desired kill-or-factor statement conditional on the single
precise provenance claim
\(L\in\operatorname {span}\{P_0,P_1,P_2\}\).

## 4. Simultaneous rank-one flattenings

We use an elementary tensor-intersection fact.

**Lemma 4.1 (many rank-one flattenings).**  Let
\(T\in\bigotimes_{i\in U}V_i\) be nonzero, let \(F\subset U\), and suppose
for every \(q\in F\) that

\[
                         T=v_q\otimes C_q,\qquad v_q\ne0.         \tag{16}
\]

Then there is a nonzero tensor \(T_0\) on \(U\setminus F\) such that

\[
                  T=\left(\bigotimes_{q\in F}v_q\right)\otimes T_0. \tag{17}
\]

In particular, for \(q\in F\),

\[
                 C_q=\left(\bigotimes_{r\in F\setminus\{q\}}v_r\right)
                             \otimes T_0.                         \tag{18}
\]

**Proof.**  For two distinct sites, the intersection

\[
 (v_q\otimes\!\bigotimes_{i\ne q}V_i)
 \cap
 (v_r\otimes\!\bigotimes_{i\ne r}V_i)
\]

is
\[
 v_q\otimes v_r\otimes\!\bigotimes_{i\notin\{q,r\}}V_i.
\]

Apply this identity successively over \(F\).  Equation (18) follows by
removing the displayed \(q\)-factor from (17). \(\square\)

Apply the lemma to (15).

**Theorem 4.2 (common-factor line field).**  Let \(F\) contain at least two
sites, assume (12) for \(a=0,1,2\) and \(q\in F\), and assume

\[
                              C_q\ne0\qquad(q\in F).               \tag{19}
\]

Then, for each \(a\), either

1. \(T_a=0\), in which case \(L_{a,q}=0\) for every \(q\in F\); or
2. \(T_a\ne0\), in which case \(T_a\) factors as in (17) through all
   \(L_{a,q}\).

Moreover, at every \(r\in F\),

\[
                    \dim\operatorname {span}
                       \{L_{0,r},L_{1,r},L_{2,r}\}\le1.            \tag{20}
\]

**Proof.**  If \(T_a=0\), equation (15) and \(C_q\ne0\) give
\(L_{a,q}=0\).  If \(T_a\ne0\), (15) and Lemma 4.1 give the factorization.

Fix \(r\in F\) and choose \(q\in F\setminus\{r\}\).  For every \(a\) in
the nonzero branch, equation (18) says that the fixed nonzero tensor
\(C_q\) has local factor \(L_{a,r}\) at \(r\).  A nonzero tensor has a
unique one-dimensional local factor when its flattening at that site has
rank one.  Hence all nonzero \(L_{a,r}\)'s are proportional.  The zero
branches contribute \(L_{a,r}=0\), proving (20). \(\square\)

Condition (19) is pair **top activity**.  It must not be silently replaced
by support of one matching or by pair-complement activity; complex
cancellation can distinguish those statements.

## 5. What the factorization says about physical stars

Fix distinct \(q,r\in F\), put

\[
 D_{qr}=U\setminus\{q,r\},\qquad
 z_{qr}=Q|_{D_{qr}},                                             \tag{21}
\]

and let \(S_{r,c}^{(q)}\) be the colour-\(c\) star from \(r\), restricted
to \(D_{qr}\).  Expanding \(C_q=q_q^{[t]}\) at \(r\) gives

\[
                 \iota_{r,c}C_q
                    =S_{r,c}^{(q)}z_{qr}^{[t-1]}.                 \tag{22}
\]

Suppose some \(T_a\ne0\).  Equations (18) and (20) give a nonzero vector
\(\ell_r\in V_r\) and a tensor \(C_{qr}\) such that

\[
                         C_q=\ell_r\otimes C_{qr}.                 \tag{23}
\]

Write \(\ell_r=\sum_c\ell_{r,c}e_{r,c}\).  Equations (22)--(23) say

\[
       S_{r,c}^{(q)}z_{qr}^{[t-1]}=\ell_{r,c}C_{qr}
       \qquad(0\le c\le2).                                      \tag{24}
\]

Thus the three physical star rows have one-dimensional image under

\[
 \mu_{qr}:{\cal R}_1(D_{qr})\longrightarrow{\cal R}_{2t-1}(D_{qr}),
 \qquad H\longmapsto Hz_{qr}^{[t-1]}.                            \tag{25}
\]

Equivalently, modulo the explicit colon kernel
\[
                         \ker\mu_{qr}
          =\operatorname {Ann}_1(z_{qr}^{[t-1]}),                 \tag{26}
\]
the physical star triple lies in one line.  This is the exact
filtered-factorization statement; replacing it by equality of the three
linear rows would discard the possible kernel (26).

## 6. Injective double overlaps kill the nonzero branch

The following elementary lemma converts two filtered line statements into
a contradiction with goodness.

**Lemma 6.1 (two deletion ranks).**  Let

\[
 f:\mathbb C^3\longrightarrow\bigoplus_{i\in W}V_i               \tag{27}
\]

be injective.  For two distinct sites \(q_1,q_2\in W\), let
\(\pi_{q_j}\) delete the \(q_j\)-component.  It is impossible that

\[
                         \operatorname {rank}(\pi_{q_1}f)\le1,
 \qquad                   \operatorname {rank}(\pi_{q_2}f)\le1.   \tag{28}
\]

**Proof.**  Each kernel in (28) has dimension at least two.  The two
kernels inside \(\mathbb C^3\) therefore have a nonzero intersection.
For a vector in that intersection, \(f(v)\) is supported only at \(q_1\)
and only at \(q_2\), hence is zero.  This contradicts injectivity. \(\square\)

**Theorem 6.2 (filtered kill theorem).**  Assume the hypotheses of
Theorem 4.2, let \(|F|\ge3\), and suppose every map \(\mu_{qr}\) in (25)
is injective.  If the physical star triple at each \(r\in F\) is injective,
then

\[
                             T_a=0\qquad(a=0,1,2),                 \tag{29}
\]

and consequently

\[
                             L_{a,q}=0
             \qquad(a=0,1,2,\ q\in F).                            \tag{30}
\]

**Proof.**  Suppose \(T_a\ne0\).  Fix \(r\in F\) and choose two distinct
sites \(q_1,q_2\in F\setminus\{r\}\).  Equations (24)--(25) and injectivity
of \(\mu_{q_jr}\) say that the physical \(r\)-star triple, after deleting
\(q_j\), has rank at most one.  Lemma 6.1 contradicts goodness of the
full \(r\)-star triple.  Hence every \(T_a=0\), and Theorem 4.2 gives
(30). \(\square\)

If \(F=U\), equation (30) says \(L_a=0\).  In the standard good fan
\(|F|\ge |B|-7\), it says that every surviving \(L_a\) is supported on at
most six exceptional sites.  Thus the cofactor-regular branch converts
the overlap cocycle into a bounded-support residue rather than leaving an
unstructured global class.

## 7. Why target equations do not kill a representative ambiguity

Let \(P_{pq}^{ab}\) be a canonical physical cap and let

\[
                         \widehat P_{pq}^{ab}
                              =P_{pq}^{ab}+N_{pq}^{ab}.            \tag{31}
\]

If \(N_{pq}^{ab}q_q^{[t-1]}=0\), then \(\widehat P\) and \(P\) have the
same pair-Hessian product.  Contracting that zero tensor at one or more
additional sites gives every induced three-cut and four-cut zero identity.
If the family also satisfies the literal homogeneous overlap equation,
the source-variable presentations agree before multiplication as well.

Consequently the target tensor, its constant-colour rows, and its mixed
four-cut rows cannot distinguish (31): they are equations on \(A\), while
\(N\) is a choice of representative for the same product.  This remains
true for an exact ternary source.  It is therefore invalid to conclude
\(N=0\) merely by “adding the target equations.”

Theorems 3.1, 4.2, and 6.2 become proof-relevant only after a liftability
or normalization statement ties the common factor to the source.  The
[physical first-jet audit](common-factor-physical-provenance-first-jet.md)
shows why the informal phrase “actual response” is insufficient: a
\(p\)-star variation \(L\) changes the canonical cap by
\[
 t(L_a|_{W_q})S_{q,b}+(L_{a,q})_bq_q,
\]
not by the pure common-factor term alone.  A target-preserving first jet
kills the factor on every pair-top-active fan site; more generally,
\(LQ^{[t]}\) lying in the diagonal target span gives physical provenance
modulo \(\ker(H\mapsto HQ^{[t]})\).  These are the precise interfaces
between overlap cohomology and the normalized diagonal rows.

## 8. Pair-complement activity is not one-hole injectivity

There is a smallest exact guard.  On four sites \(W=\{0,1,2,3\}\), put

\[
                         q=\sum_{0\le i<j\le3}e_{i,0}e_{j,0}.      \tag{32}
\]

Every pair complement consists of one nonzero edge, so

\[
                 q_{W\setminus\{i,j\}}^{[1]}\ne0
                 \qquad(i\ne j).                                 \tag{33}
\]

Every displayed cell is active: its complementary edge completes it to a
top matching.  Also

\[
                              q^{[2]}=3X_0^W\ne0.                  \tag{34}
\]

Delete site \(3\) and put

\[
 z=e_{0,0}e_{1,0}+e_{0,0}e_{2,0}+e_{1,0}e_{2,0}.                 \tag{35}
\]

Then the one-hole multiplication map \(H\mapsto Hz\) has the nonzero
kernel vector

\[
                         H=e_{0,0}-e_{1,0},\qquad Hz=0.           \tag{36}
\]

Indeed, the first summand of \(H\) can only use the complementary edge
\(12\), the second can only use \(02\), and the two resulting copies of
\(e_{0,0}e_{1,0}e_{2,0}\) cancel.  Exact row reduction gives

\[
              \operatorname {rank}\bigl({\cal R}_1(\{0,1,2\})
                       \xrightarrow{\ \cdot z\ }{\cal R}_3(\{0,1,2\})\bigr)
                    =7<9.                                       \tag{37}
\]

Thus even pair-top activity, all pair-complement powers, and activity of
every source cell do not imply injectivity of (25).  The example has
rank-one blocks, so it does not refute a theorem adding a suitable
rank-three or three-hole gauge-rigidity hypothesis.  It proves that
pair-complement activity by itself is not that theorem.

## 9. Relation to synchronization and active caps

The filtered kill theorem removes the common-factor overlap class whenever
the double-overlap one-hole maps are injective.  On the complementary
branch it exports the explicit kernel (26), which is the same kind of
extra lower catalecticant locus already isolated by the
[fixed-star three-hole dichotomy](fixed-star-three-hole-gauge-dichotomy.md).
This is genuine progress on synchronization: the formerly amorphous flat
E1 ambiguity is reduced to a bounded-support factor or a named colon
kernel.

More decisively, Theorem 3.1 proves that any physical-span provenance has
rank at most one and that literal provenance is impossible.  The first-jet
audit cited above sharpens the remaining synchronization interface: one
must prove that the chosen homogeneous lift is a target-preserving
\(p\)-local first jet, or at least that its visible response lies in the
diagonal target span.  The former kills it on pair-top-active fan sites;
the latter puts its class in the physical \(p\)-star span modulo the named
one-site catalecticant kernel.  Neither statement is another overlap
identity.

It is not yet a synchronization-or-active-cap theorem.  The argument sees
zero curvature and therefore has no mismatch from which to extract an
active covector \(K\).  It also supplies no nonzero direct scalar \(s\) and
does not force the nonlinear equation \({\cal E}_{p,q}(K)=0\).  The next
source-level step must use physical provenance plus the normalized
diagonal rows either

1. to eliminate the colon-kernel/bounded-support residues; or
2. to turn a failure of their synchronization into an active cap.

## 10. Audit

The dependency-free checker
[verify_common_factor_filtered_kill_or_factor.py](../computations/verify_common_factor_filtered_kill_or_factor.py)
audits the \(2^9\) physical-span support ledger and (32)--(37) over the
integers.  It verifies that the shared-complement condition leaves only
one-column matrices, all six active pair complements, the exact coefficient
\(3\) in (34), the displayed kernel, and the \(7/9\) one-hole rank.  The
uniform factorization and deletion lemmas are the tensor proofs above, not
finite-rank experiments.
