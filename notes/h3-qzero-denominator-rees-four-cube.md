# A canonical \(q\)-zero symbol survives the denominator-marked four-cube

Positive principal-parts/Rees symbol calculation, with a bounded attaching
problem. This note constructs the canonical polynomial symbol and proves
that it has no denominator-column leakage or cubical sign obstruction. It
does not construct the attaching chain, its cap and ordinary-residue rows,
descent to the actual filtered full-source complex, physical-line
injectivity, or Krenn's conjecture.

## Outcome

Let

\[
 D=\{1,2,3,4,5\},\qquad m=12112,\qquad F_v=D\setminus\{v\},
\]

and let

\[
 h_v=\operatorname {Haf}(q_m|_{F_v})
     =\sum_{N\in\operatorname {PM}(F_v)}q_N.             \tag{1}
\]

For the literal direct-free full-nine row used in the preceding
principal-parts construction, let \(c_v\) be zero on \(x,v,p,q\) and equal
to \(m\) on \(F_v\), and put

\[
 u_v=a_{xv}^{00},\qquad t=a_{pq}^{00},\qquad H_v=H_{c_v}.
\]

Every \(N\in\operatorname {PM}(F_v)\) consists of two labelled internal
edge variables. Exact differentiation of the full 90-term direct-free row
gives

\[
 \partial_{u_v}\partial_tH_v=h_v,
 \qquad
 \boxed{\partial_N\partial_{u_v}\partial_tH_v=1}.        \tag{2}
\]

The term in (2) lies in the \(pq\)-direct sector and in the
\(pr\)-two-star sector. Thus it is the \(q\)-degree-zero top of the same
strict two-chart Rees transfer constructed previously; it is not an
abstractly declared cap column.

More importantly, (2) attaches without leakage to the **complete** odd
denominator presentation. If \(P_m\) extracts the word \(m\) and reinserts
the pure word \(Y_0\), then

\[
 \partial_N(P_m\delta)(d_{s,a})=
 \begin{cases}
 Y_0,&(s,a)=(v,m_v),\\
 0,&(s,a)\ne(v,m_v).
 \end{cases}                                             \tag{3}
\]

This checks all fifteen denominator columns, not only the selected one.
The reason is support-theoretic and exact. For \(s\ne v\), the matching
\(N\) contains an edge incident to \(s\), while
\(q_{D\setminus\{s\}}^{[2]}\) contains no such edge. For \(s=v\), the
derivative selects the single matching \(N\), and word extraction leaves
only \(a=m_v\).

Equation (3) is a statement about the polynomial column of a denominator
relation generator. It does not by itself create a principal-part relation
generator in the full source, or define cap and ordinary-residue maps on
such a generator. The exact candidate is therefore conditional. If an
attaching chain \(j_{v,N}\) realizes the four-cube, has polynomial boundary
\(Y_0\), and extends the zero target and ordinary-residue augmentations,
then, with \(w_v\) the normalized pure cap-relation row,

\[
 \widehat d(j_{v,N})=(w_v,0,0),                          \tag{4}
\]

and either normalization

\[
 n_{v,N}=\kappa Yj_{v,N}\quad(Y_0\mapsto w_v),
 \qquad\text{or}\qquad
 n_{v,N}=\kappa j_{v,N}\quad(Y_0\mapsto Yw_v)            \tag{5}
\]

would give

\[
              \widehat d(n_{v,N})=(\kappa Y,0,0).       \tag{6}
\]

This conditional column is not the old graph column
\(\kappa Y\rho=(\kappa Y,0,\kappa Y)\). But the difference cannot be
claimed solely from (3): it is precisely the missing ordinary-residue
typing of the attaching chain. A sampled split-cap rank calculation checks
only that (6), if constructed, is the required missing direction.

The first such face occurs at total principal-parts order four. The exact
ladder is

\[
\begin{array}{c|c|c|c}
\text{external order}&\text{internal order}&q\text{-degree}&
  \text{stabilizer weight}\\ \hline
2&0&2&\ne0\\
2&1&1&\ne0\\
2&2&0&0.
\end{array}                                             \tag{7}
\]

Thus the earlier finite-degree and weight obstructions are sharp: they
exclude orders two and three, but they stop exactly at the four-cube.

## 1. Literal external and internal faces

Write the strict chart comparison as

\[
 K_v=r_{c_v}^{pq}-r_{c_v}^{pr}.                         \tag{8}
\]

Both chart rows have the same global polynomial \(H_v\), so their ordinary
boundary is zero. The marked external square has directions \(u_v,t\),
and its mixed coefficient is \(h_v\). Since every term containing \(t\)
is \(pq\)-direct, and a matching containing \(pq\) cannot contain \(pr\),
the associated Rees symbol is

\[
 (h_v)_{pq,\mathrm {direct}}
 -(h_v)_{pr,\mathrm {two\text{-}star}}.                 \tag{9}
\]

Now choose \(N=\{e_1,e_2\}\in\operatorname {PM}(F_v)\). Multi-affinity
gives the complete internal square

\[
 h_v
 \xrightarrow{\partial_{e_1}} e_2,
 \qquad
 h_v\xrightarrow{\partial_{e_2}}e_1,
 \qquad
 \partial_{e_2}\partial_{e_1}h_v=1.                    \tag{10}
\]

The reset denominator column satisfies the identical three equations after
tensoring the coefficients with \(Y_0\):

\[
 P_m\delta(d_{v,m_v})=h_vY_0,
 \quad \partial_{e_i}P_m\delta(d_{v,m_v})=e_{3-i}Y_0,
 \quad \partial_NP_m\delta(d_{v,m_v})=Y_0.              \tag{11}
\]

Equations (9)--(11), together with (3), are the polynomial face
identifications required of the denominator-marked candidate four-cube

\[
       \mathsf J_{v,N}=[K_v;d_{v,m_v};u_v,t;e_1,e_2].    \tag{12}
\]

They also show why the construction needs two internal directions. After
zero or one internal contraction a positive \(q\)-degree remains; after the
second, and not before it, the lower coefficient is a unit.

## 2. Tensor signs and the candidate unpaired symbol

Orient the external and internal squares in the displayed orders and use
the standard tensor differential

\[
 D=d_{\rm ext}\otimes1+(-1)^{p}1\otimes d_{\rm int}
 \quad\text{on external degree }p.                      \tag{13}
\]

The top bidegree is \((2,2)\). For every external/internal ridge, the two
orders of taking its faces have signs \(+1\) and \(-1\). Within either
square the usual cubical signs give the same cancellation. Equivalently,
the eight oriented facets of a four-cube produce 24 ridges, each twice with
opposite coefficient. Hence \(D^2=0\) literally.

The proposed attachment chooses the sign of the denominator face so that
the base term in (11) cancels the reset commutator \(+h_vY_0\). The tensor
convention then fixes the signs of both one-edge faces, and (10)--(11)
show that their polynomial values agree with the required opposite signs.
There is no cross-column polynomial face by (3). The candidate remaining
lower associated-Rees symbol is \(+Y_0\), or \(+\kappa Yw_v\) after the
conditional normalization (5).

This proves that commuting derivatives and tensor signs create no
obstruction to the attachment. It is not a chain-level construction:
one must still define the comparison differential whose faces are these
polynomials and define its cap and ordinary-residue augmentations.

## 3. The canonical Reynolds choice and raw indeterminacy

There are three choices of \(N\) for a four-site face. Each gives the same
unit polynomial symbol. Thus the raw polynomial map from the fifteen
labelled choices to the five face rows has rank five and kernel dimension
ten: two matching-difference directions per face. This is not an augmented
cap-map rank.

There is nevertheless a canonical, permutation-natural section. Define

\[
                  L_v={1\over3}
                      \sum_{N\in\operatorname {PM}(F_v)}\partial_N. \tag{14}
\]

Then

\[
                         L_v(h_s)=\delta_{vs}.           \tag{15}
\]

For \(s=v\), every summand differentiates its matching monomial to one and
the factor \(1/3\) normalizes the sum. For \(s\ne v\), every
\(N\in\operatorname {PM}(F_v)\) contains an edge incident to \(s\), which
is absent from every monomial of \(h_s\). Therefore \(L_v\) gives a
canonical polynomial candidate. If compatible attaching chains exist,
their Reynolds average

\[
                         j_v={1\over3}\sum_Nj_{v,N}      \tag{16}
\]

would have boundary \(Y_0\), with no choice of matching.

This distinction matters for how the result is used. If one wants a
canonical spectral-sequence secondary operation on a quotient, the
ten-dimensional matching-difference kernel still has to die or descend.
If a proof hypothesis only asks for one explicit filtered chain map and one
explicit chain with the prescribed boundary, the Reynolds operator (14)
removes the arbitrary matching choice **after** such a chain map is
constructed. It does not construct that map or prove its descent to the
physical source.

## 4. Uniform odd-set duality

The construction is not special to five odd sites. Let
\(|D|=2r+1\), put \(F_v=D\setminus\{v\}\), and write

\[
 h_s=\operatorname {Haf}(q_m|_{F_s}),\qquad
 L_v={1\over(2r-1)!!}
     \sum_{N\in\operatorname {PM}(F_v)}\partial_N.      \tag{17}
\]

Exactly the same support proof gives the Weyl/Reynolds duality

\[
                         \boxed{L_v(h_s)=\delta_{vs}}.  \tag{18}
\]

Moreover, after adjoining the two external edges
\(u_v=(xv)\) and \(t=(pq)\), the set
\(\{u_v,t\}\cup N\) is a perfect matching of all \(2r+4\) sites. It occurs
with coefficient one in the literal full row, and it cannot contain the
forbidden \(pr\) edge because it already contains \(pq\). Hence

\[
                  \partial_N\partial_{u_v}\partial_tH_{c_v}=1    \tag{19}
\]

for every \(r\). The checker verifies (18) through \(r=4\), i.e. through
nine odd sites, and verifies (19) combinatorially for every matching in
those instances. Equations (18)--(19) are the reusable mathematical
content of the four-cube: perfect matchings on complementary even faces
form an exact differential dual basis after Reynolds averaging.

## 5. Stabilizer-weight landing

On the diagonal GHZ stabilizer, the uncontracted reset coefficient has
character

\[
 \chi_{v,0}=\operatorname {wt}(Y_0)
             -\sum_{i\in F_v}\lambda_{i,m_i}.           \tag{20}
\]

The five characters (20) are independent. For each face, the mixed word
\(m|_{F_v}\) is the unique one of the 81 four-site words with this
restricted character. Contracting one matching edge deletes its two input
weights but leaves a nonzero character. Contracting both leaves only
\(\operatorname {wt}(Y_0)=\sum_i\lambda_{i,0}=0\). This proves the weight
claims in (7) and shows that the unit top symbol becomes invariant exactly
when it first becomes \(q\)-degree zero.

## 6. What remains when this is combined with the physical Koszul cell

The already constructed physical two-row cell is

\[
 K_m^{\rm phys}
   =H_mr_0-(H_0-u)r_m
   =u r_m+\underbrace{(H_mr_0-H_0r_m)}_{\widetilde K_m}. \tag{21}
\]

Its lowest Rees symbol is \(+r_m\), with
\(r_m=r_{22}^{012112}\). The calculations above supply the exact
polynomial values that five denominator homotopies would have to realize.
For the former defect

\[
             P_m\delta(d_{v,m_v})=h_vY_0              \tag{22}
\]

all internal derivative values and signs match, and the top value has no
cross-column remainder. This is the candidate face ledger, not yet a
homotopy.

The full combination is not yet constructed. Three concrete pieces remain:

1. an attaching comparison \(\Phi_0\) whose polynomial component realizes
   (3), whose cap differential realizes the proposed face ledger, and whose
   target and ordinary-residue augmentations vanish;
2. the higher Koszul correction
   \(\widetilde K_m=H_mr_0-H_0r_m\); and
3. the connection/normal/curvature side that transports the endpoint-\(22\)
   physical row \(r_{22}^{012112}\) to the zero-endpoint chart rows
   \(r_{c_v}^{pq}-r_{c_v}^{pr}\) used in (8).

The first missing boundary is now completely specified. For each matching
\(N\), the desired attaching map must make

\[
 \mathfrak A_{\rm attach}(s,a)
   =d_{\rm cap}\Phi_0(d_{s,a})
      -\partial_N(P_m\delta)(d_{s,a})=0,                \tag{23}
\]

with \(\operatorname {tgt}\Phi_0=\operatorname {ores}\Phi_0=0\).
The second term of (23) is the explicitly checked vector supported only at
\((s,a)=(v,m_v)\), where it equals \(Y_0\). The first term, and both
augmentations of \(\Phi_0\), are not defined by this note.

If (23) is constructed and \(\Phi_{\ge1}\) extends it to the higher
filtration, the subsequent literal mixed boundary is supported on

\[
 \boxed{
   \mathfrak B_{\rm rem}
      =(d_{\rm cap}\Phi_{\ge1}+\Phi_{\ge1}d_{\rm Eq})(\widetilde K_m)
        +\mathfrak C_{22\to00},}                         \tag{24}
\]

where \(\mathfrak C_{22\to00}\) is the unconstructed curvature side face
between the two displayed endpoint sectors. The calculation in this note
determines the desired lowest-\(q\) component of (23); it does not prove
that component is a boundary. Equations (23)--(24), rather than a vague
request for “descent,” are the next assembly problem.

After (23)--(24) are killed, one must still check injectivity on the physical line.
The ten matching-difference directions matter only if the resulting class
is required to be a choice-independent secondary operation rather than the
explicit Reynolds-averaged chain map.

## 7. Exact verification and scope

The dependency-free checker
[verify_h3_qzero_denominator_rees_four_cube.py](../computations/verify_h3_qzero_denominator_rees_four_cube.py)
verifies:

- all fifteen literal full-row four-polars (2);
- the full fifteen-column no-leakage statement (3);
- the internal face pairings (10)--(11) and all cubical signs;
- the first \(q\)-zero order and the five stabilizer weights;
- rank five with matching-choice kernel dimension ten;
- the Reynolds normalization (14)--(15); and
- the uniform duality (18) through nine odd sites.

Its frozen certificate digest is

    9aa94b9e45d3954e6558091ac4fcbe845734ca55f8c382277ced44e31508318f

The checker also confirms conditionally that a column of type (6) would
raise the selected split-cap rank from two to three. That calculation is
only a typing/normalization check. The literal rows and denominator
presentation prove the polynomial candidate, not the attaching chain or
its augmented readouts.
