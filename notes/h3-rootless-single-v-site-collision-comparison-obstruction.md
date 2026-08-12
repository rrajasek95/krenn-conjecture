# The first physical single-face comparison needs a new site-collision face

## Outcome

Fix one non-Euler face \(v\). The committed two-chart and shifted-normal
constructions do not yet give a physically typed augmented comparison.
There are two independent obstructions, and keeping them separate removes
an ambiguity in the current rootless interface.

First, the primitive chart difference

\[
                 k_v=c_{pq}-c_{pr}
\]

has zero literal physical boundary, target, and all ordinary residues, but
the normalized chart-odd readout is one. Every readout pulled back from the
single physical source is chart-even and therefore kills \(k_v\). Thus the
derived correction \(-S_v\) is **not** physical anchor incidence. A
comparison must construct the latter as a new physical chain value; it
cannot assign it by chart normalization.

Second, the normal Hasse face is site-squarefree, while the first physical
companion degree which changes the primitive ridge class is
\(P_3\sqcup K_2\): one residual site occurs twice. A degree-preserving map
cannot identify these faces. In the complete first collision degree, a
single multiplied response route has a private ordinary-residue companion.
Only the adjacent two-face S-pair cancels that companion, and its physical
anchor incidence is zero.

Consequently there is no single-\(v\) physical comparison in the existing
literal first-collision module. The smallest degree-shifting datum is an
adjacent two-face site-collision cell with

\[
 \boxed{dE_v=-r_v+r_w,\qquad
   (\widehat w,\operatorname{tgt},\operatorname{ores})=(0,0,0),\qquad
   \operatorname{ainc}(E_v)=0}.                       \tag{1}
\]

It lies in the corresponding repeated-site \(P_3\sqcup K_2\) fine degree
and must satisfy the known degree-five odd-cycle compatibility. It is the
physical lift of the formal first-Tor edge, not the primitive anchor cell.
Component III still separately requires a vertex-boundary cell with

\[
  (\operatorname{ainc},\widehat w,\operatorname{tgt},
       \operatorname{ores})=(-1,0,0,0).                \tag{2}
\]

This note proves the need for (1) in the first literal/common-\(q\) degree;
it does not exclude a new relative source-resolution generator with those
data.

## 1. Literal two-chart and cap rows

For the selected 90-term word, the two chart copies have the same complete
augmented physical boundary:

\[
 \widehat d(c_{pq})=(B_w,0,0)
                  =\widehat d(c_{pr}),                 \tag{3}
\]

where the displayed zeroes include target and all fifteen ordinary-residue
rows. The fine degree is also the same. Hence every physical covector pulls
back to a multiple of \((1,1)\), whereas the normalized chart cochain is

\[
                         (1/2,-1/2).                   \tag{4}
\]

It reads one on \((1,-1)\), so (4) does not factor through the physical
forgetful quotient. In particular, calling the value \(-S_v\) a physical
anchor incidence would change the source complex rather than analyze it.

The shifted derived filler also cannot be made into an augmented cycle by
the old cap columns. After the harmless normalization used on the face-open
chart, or after the completed normal inverse on the face-zero chart, rows
\((W,\operatorname{tgt},\operatorname{ores},S)\) give

\[
\begin{array}{c|rrrr}
 &W&\operatorname{tgt}&\operatorname{ores}&S\\ \hline
 n_v&1&0&0&-1\\
 hT&-1&1&0&0\\
 hY\rho&1&0&1&0.
\end{array}                                             \tag{5}
\]

Adjoining the desired clean chart vector \((0,0,0,-1)\) makes the four
columns a unimodular matrix. Thus no combination of the three existing
columns simultaneously kills \(W\), target, and ordinary residue while
retaining the chart correction. This is only a derived/cap calculation; it
still does not define a physical anchor row.

## 2. The complete first site-collision degree

On the committed five-cycle specialization write

\[
 (a,b,c,d,e)=(q_{12},q_{23},q_{34},q_{45},q_{15}),
 \qquad (h_1,h_3,h_5,h_2,h_4)=(bd,ad,ac,ce,be).       \tag{6}
\]

Consider the first repeated degree \(abd\). Exactly two companion
generators divide it:

\[
                         a h_1=b h_3=abd.              \tag{7}
\]

After factoring the common monomial, the two oriented literal columns have
rows

\[
\begin{array}{c|rrrrrr}
 &r_1&r_3&\operatorname{ores}&W&\operatorname{tgt}
   &\operatorname{ainc}\\ \hline
 a b_1&-1&0&1&0&0&0\\
 -b b_3&0&1&-1&0&0&0.
\end{array}                                             \tag{8}
\]

Here physical anchor incidence is zero because these are response/bar
multiplier columns, not a pure-anchor relative face. On the single-\(v\)
submodule, the ordinary-residue row in (8) is a private unit; zero residue
forces the column coefficient to vanish. Adding the adjacent face gives

\[
                         (-r_1+r_3,0,0,0,0),           \tag{9}
\]

the familiar first-Tor S-pair. It restores source boundary and cancels
ordinary residue, but still has anchor incidence zero. Equation (9) is
therefore the consistent boundary specified for the missing higher cell
\(E_v\); it is not itself a literal higher source cell. The complete
squarefree inventory below proves that no existing Hasse/cofactor cell has
its multidegree.

The primitive physical anchor is a different column. It has a vertex
boundary, for example \(r_1\), rather than the aggregate-zero edge boundary
(9), and has anchor incidence \(-1\). It raises the exact augmented rank
and is detected by the physical-anchor covector. Combining that cell with
\(E_v\) is the pentagon mapping-cone interface; assigning \(-1\) directly
to \(E_v\) would conflate two different physical types.

The calculation is cyclic and holds in all five repeated degrees. Each has
exactly two active routes and site profile \((2,1,1,1,1)\), up to rotation.
There is no third literal column hidden in the same degree.

Even granting the strongest tempting formal replacement does not help. If
the signed coefficient augmentation is declared to be an anchor row, then
at the valid diagonal torus point \(a=b=c=d=e=1\) it equals the
ordinary-residue row on both columns of (8). The primitive covector

\[
                 \text{declared augmentation}-\operatorname{ores}
\]

kills the entire collision module and reads \(-1\) on the separate
primitive anchor. Equivalently, the five formal augmentations generate only
\((a-b,b-c,c-d,d-e)\), not the unit. This generous formal declaration is
still weaker than constructing physical anchor incidence, but it fails
already at a genuine source specialization.

## 3. Why a degree shift is genuinely new

Every literal hafnian cofactor or squarefree Hasse face is a submatching.
Its physical site degree is at most one. The checker exhausts all
\(105\cdot16=1680\) such faces on eight sites. Every first-Tor degree in
(7) instead contains an adjacent edge pair and has one site of degree two.
Therefore a homogeneous physical comparison cannot send the inactive
normal face to the repeated-site cell.

The earliest polynomial degree shift is exactly multiplication by the
incident cycle edge in (7). It creates the private response companion, so
it is not an augmented single-face comparison. Cancelling the companion
forces the adjacent face and produces (9). This proves that the minimal
degree-shifting source type is the zero-anchor cell (1), not another
single-face Hasse coefficient. For five such cells, \(d^2=0\) also requires
the already identified degree-five odd-cycle relation. The primitive
anchor (2) remains a separate mapping-cone datum.

This sharpens the rootless dependency chain:

1. 091edba gives the physical-forgetful chart kernel;
2. 91041f7 and 827e329 construct its derived shifted/normal filler but only
   with chart correction;
3. the first collision/Tor module changes the site degree and cancels
   ordinary residues only in adjacent pairs;
4. a degree-shifting physical comparison exists only after constructing
   the zero-anchor cell (1); and
5. the terminal rootless landing still requires the separate primitive
   anchor face (2). Its physical incidence cannot be inherited from the
   chart tag or assigned to the first-Tor edge.

## Verification and scope

Run

~~~~text
python3 computations/verify_h3_rootless_single_v_site_collision_comparison_obstruction.py
python3 -O computations/verify_h3_rootless_single_v_site_collision_comparison_obstruction.py
python3 -I -S computations/verify_h3_rootless_single_v_site_collision_comparison_obstruction.py
~~~~

The checker pins the five requested rootless inputs plus the first-Tor and
ridge modules. It verifies the chart-forgetful rank jump, the unimodular
derived cap obstruction, all five complete repeated collision degrees,
their literal source boundaries and readouts, both primitive separators,
and the full squarefree Hasse inventory. Its scope is the exact first
literal/common-\(q\) collision module. It does not prove an all-resolution
no-go, construct (1) or (2), or identify derived chart readout with physical
anchor incidence.

Frozen ledger SHA-256:

~~~~text
a007638ab5f17241f9e6a8ece18692447757c6577ed9593dd869204f0d50647d
~~~~
