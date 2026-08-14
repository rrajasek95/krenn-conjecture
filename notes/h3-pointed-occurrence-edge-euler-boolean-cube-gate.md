# The four-edge Euler cube resolves the occurrence selector only relatively

Exact coefficient cube, all lower faces, and the comparison with the known
fourth-Hasse obstruction.  Let (R) be the complete direct-free h=3 response
row on the augmented vertices

\[
             P,S,0,1,2,3,4,5 .
\]

It contains the 90 perfect matchings which do not use (PS).  Fix

\[
 f=P0\mid S1\mid 23\mid45,
 \qquad c_f=90e_f-\mathbf 1_{90}.                       \tag{1}
\]

The commuting edge Euler filters give an exact coefficient selector

\[
 E_z=x_z\partial_z,qquad
 P_f=E_{P0}E_{S1}E_{23}E_{45},qquad P_f(R)=f,          \tag{2}
\]

and hence

\[
                     (90P_f-I)R=c_f.                  \tag{3}
\]

The full Boolean resolution of (2) does **not** make the pointed face
absolute.  It has a canonical H0-preserving relative graph with all lower
faces, but its top carrier is detected by an exact dual.  Killing that
carrier lowers H0.  Moreover, the scalar fourth derivative

\[
 \partial_{P0}\partial_{S1}\partial_{23}\partial_{45}R=1              \tag{4}
\]

is exactly the unit appearing at the top of the known fourth-Hasse/D4
calculation, while the occurrence-labelled pointed obstruction is not the
bare D4 class.  The D4 cube transports a supplied pointed section; it does
not construct its bottom.

This note proves the coefficient, rank, and relative-presentation
statements.  It does not construct the missing physical edge-Euler
homotopies, termwise PP/reinsertion maps, scalar target correction, or
absolute pointed landing.

## 1. The sixteen Boolean faces

Put

\[
 I=\{P0,S1,23,45\}.
\]

For (T\subseteq I), let (v_T\in\mathbf Q^{90}) be the indicator of
response occurrences containing every edge in (T).  Thus

\[
 v_T=\prod_{z\in T}E_z(R),
 \qquad n_T=|\operatorname {supp}(v_T)|.                \tag{5}
\]

The exact support profile is

| order of (T) | number of faces | support sizes (n_T) |
|---:|---:|---|
| 0 | 1 | (90) |
| 1 | 4 | (15,15,12,12) |
| 2 | 6 | (3,3,3,3,3,2) |
| 3 | 4 | (1,1,1,1) |
| 4 | 1 | (1) |

The singleton counts 15 are the endpoint edges (P0,S1); the singleton
counts 12 are the tail edges (23,45).  Among pairs, the tail-tail face is
the unique support-two face.  Every other pair has support three.

Center each face integrally by

\[
 C_T=90v_T-n_T\mathbf 1_{90}.                           \tag{6}
\]

Then

\[
 \epsilon(C_T)=0,qquad C_\varnothing=0,qquad C_I=c_f. \tag{7}
\]

Every nonempty (C_T) is nonzero.  These are the top carrier and its
fourteen proper nonempty lower faces.

There is a useful but dangerous degeneracy.  Three edges of a perfect
matching force the fourth, so

\[
 v_{I\setminus\{z\}}=e_f,qquad
 C_{I\setminus\{z\}}=c_f
 \quad(z\in I).                                       \tag{8}
\]

Consequently the 15 nonempty centered vectors span only an 11-dimensional
unlabelled subspace.  Equation (8) is not permission to identify the four
faces.  Their types are

\[
 \begin{array}{c|c}
 z&\text{deleted/reinserted face}\\ \hline
 P0&S1\mid23\mid45\\
 S1&P0\mid23\mid45\\
 23&P0\mid S1\mid45\\
 45&P0\mid S1\mid23 .
 \end{array}                                           \tag{9}
\]

They carry different endpoint/q and reinsertion labels.  Forgetting those
labels creates a false coefficient cancellation precisely where the
physical construction needs four distinct arrows.

## 2. The formal four-cube

Let (K_4) be the Boolean/Koszul cube with one basis vector for every
subset of (I), and differential given by wedging with the sum of the four
directions.  Its dimensions and differential ranks are

\[
 \dim K_4=(1,4,6,4,1),
 \qquad \operatorname {rank}d=(1,3,3,1).               \tag{10}
\]

The checker constructs the matrices over (mathbf Q), verifies
(d^2=0), and verifies exactness in every proper degree.  This packages the
formal alternating signs and all (4+6+4) intermediate Hasse faces.

It is essential to separate (10) from a physical realization.  The map

\[
       T\longmapsto C_T                               \tag{11}
\]

is only a coefficient evaluation.  An edge Euler filter is diagonal on the
90 matching coordinates, but it has not been proved to be a tangent
homotopy of the fixed source, a termwise PP map, or a word/fine-natural
reinsertion map.  Formal Koszul exactness therefore does not make the
evaluated physical faces boundaries.

## 3. Minimal H0-preserving relative presentation

Let (V=\mathbf Q^{90}).  The old fixed-source coefficient complex has the
single complete response boundary (R=\mathbf 1_{90}), hence

\[
                    \dim H_0(V/\langle R\rangle)=89.    \tag{12}
\]

Adjoining (c_f) as a raw absolute boundary raises the boundary rank from
one to two and gives H0 dimension 88.  Thus the direct declaration
(db_f=c_f) changes the fixed-source classical fibre.

The label-faithful relative Boolean graph is

\[
 \widetilde V
 =V\oplus\bigoplus_{\varnothing\ne T\subseteq I}\mathbf Q u_T,
 \qquad
 d b_T=C_T-u_T.                                        \tag{13}
\]

There are fifteen carrier coordinates: the top (u_f=u_I) and fourteen
proper lower carriers.  Together with the complete response column, the
sixteen boundary columns in (13) have rank sixteen because every graph
column is monic in its private (u_T).  Therefore

\[
 \dim\widetilde V=105,qquad
 \operatorname {rank}d=16,qquad
 \boxed{\dim H_0=89}.                                  \tag{14}
\]

This is minimal in the label-faithful relative category: one private
carrier is retained for each nonempty deletion/reinsertion face.  If labels
are forgotten, the coefficient vectors compress to rank eleven, but that
compression identifies physically different arrows in (9).

The top equation is the familiar pointed graph

\[
                         db_f=c_f-u_f.                  \tag{15}
\]

It is genuinely relative.  To see this after every lower graph has been
adjoined, define on (V)

\[
                    \lambda_0={c_f\over90\cdot89}.      \tag{16}
\]

For every nonempty (T\), extend it by

\[
 \lambda(u_T)=\lambda_0(C_T)
              ={90-n_T\over89}.                        \tag{17}
\]

Then

\[
 \lambda(R)=0,qquad
 \lambda(C_T-u_T)=0\quad(T\ne\varnothing),
 \qquad \lambda(u_f)=1.                               \tag{18}
\]

Thus an exact dual kills the complete response and all fifteen graph
boundaries while detecting the top carrier.  The full lower-face
resolution has not secretly filled (u_f).

If a new absolute column (u_f) is adjoined, the boundary rank becomes 17
and H0 becomes 88.  Equivalently, declaring the top graph absolute adds new
source data.  The coefficient cube and the complete response do not imply
that column.

## 4. Relation to the fourth-Hasse/D4 obstruction

Only the marked response monomial contains all four selected edges.  Since
it is squarefree, ordinary differentiation gives (4).  Multiplication back
by the four edges gives

\[
           E_{P0}E_{S1}E_{23}E_{45}(R)=f.              \tag{19}
\]

Therefore the associated-graded scalar top of the edge-Euler cube is
exactly the known fourth-Hasse unit.  In this restricted sense the top is
the D4 top.

The physical pointed obstruction is not exactly that bare class.  It also
contains

- the occurrence label (e_f) and complete-row subtraction in (c_f);
- the four distinct deletion/reinsertion directions in (9);
- the scalar/target product-rule face;
- the pointed anchor (u_f-u);
- the word/fine and q/PP landing data.

The fixed-fibre D4 calculation already proves

\[
 \Psi_I(H_m)=1,qquad
 [d,\pi_\Delta]=(H_0-u)e_0.                             \tag{20}
\]

Thus the fourth operator does not preserve the source ideal and the formal
Hasse cone does not descend to the old physical complex.  The moving-target
orbit cube repairs the scalar target and formally transports

\[
                         D_4(c_f)=c_g,                  \tag{21}
\]

but (21) assumes the bottom occurrence-tagged section.  It does not create
(P_f).

The obstruction has two layers, not one:

\[
 \boxed{
 \begin{array}{ll}
 \text{bottom pointed layer:}&[u_f]\ne0
     \text{ in the H0-preserving graph};\\
 \text{fourth-Hasse layer:}&\text{once the bottom is supplied, its D4}
     \text{ transport still needs physical source descent}.
 \end{array}}                                           \tag{22}
\]

Calling the whole pointed problem “exactly the D4 class” loses the first
line of (22).

## 5. First augmented faces

The coefficient operation stays at word

\[
                         11:110000.                     \tag{23}
\]

Its proper faces nevertheless keep the fine missing-edge and reinsertion
labels.  It may not be identified with the later cap/ridge word
(01211222), nor with the top orbit word (111111).

At a trapped source, the centered edge-Euler expression has scalar/target
product-rule face

\[
                         90 f(x).                       \tag{24}
\]

A source-valid totalization must supply the opposite face (-90f(x)).
If (f(x)=0), this particular face vanishes; that does not produce a
uniform source-labelled cell over the full source.

The coefficient differential of the top graph is

\[
                    du_f=dc_f=90,df-dR.               \tag{25}
\]

In the complete-response graph presentation this is the known cotangent
relation

\[
              [P_f]=[d(u_f-u)]=-[dz_f]=-[dG].           \tag{26}
\]

The Boolean coefficient cube proves neither ([d(u_f-u)]=0) nor
(dG=0).

After matching projection one has the exact coefficient identity

\[
                    (A+I)c_f=3c_{01},
 \qquad c_{01}=30b_{01}-R,                              \tag{27}
\]

and its first selected PP face is

\[
                    dc_{01}=30,db_{01}-dR.             \tag{28}
\]

The selected (db_{01}) is the six-term residual-flip row.  The aggregate
complete response does not provide its termwise PP/reinsertion-natural
carrier.  That is the first q-labelled physical debt after the pointed
graph is granted.

## 6. Exact conclusion and shortest attack

The exact status is

\[
\boxed{
\begin{array}{l}
P_f(R)=f\text{ and }(90P_f-I)R=c_f:\ \text{proved};\\
\text{all 16 coefficient faces and formal Koszul signs}:\ \text{constructed};\\
\text{H0-preserving relative graph with all 14 proper faces}:\ \text{constructed};\\
\text{scalar fourth top equals the known D4 unit}:\ \text{yes};\\
\text{physical pointed top is exactly the bare D4 class}:\ \text{no};\\
\text{cube plus complete response makes }P_f\text{ absolute}:\ \text{no}.
\end{array}}                                            \tag{29}
\]

The shortest positive datum is now concrete: construct one source-labelled
pointed Boolean local system whose top is (15), whose fourteen proper
faces realize the four edge deletion/reinsertion families termwise, whose
scalar target face is (-90f(x)), and whose matching/q projection realizes
the six-term (db_{01}) row.  The existing moving-target D4 cube can then
transport that supplied object.  Attacking D4 first cannot manufacture its
bottom pointed section.

## 7. Reproduction

Run

```text
python3 computations/verify_h3_pointed_occurrence_edge_euler_boolean_cube_gate.py
python3 -O computations/verify_h3_pointed_occurrence_edge_euler_boolean_cube_gate.py
python3 -OO computations/verify_h3_pointed_occurrence_edge_euler_boolean_cube_gate.py
```

The checker enumerates the 90 response occurrences, builds every Boolean
indicator and centered face, verifies the support table and the unlabelled
rank 11 collapse, constructs the four Koszul matrices, proves their ranks
and (d^2=0), verifies the relative graph H0 ranks, constructs the retained
top dual (16)--(18), and freezes the complete theorem ledger.
