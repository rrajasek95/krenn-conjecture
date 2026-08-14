# Gate II extends the chart-odd dual onto the carrier, not to a terminal

## 1. Outcome

At the canonical (h=3) Gate-II packet, the primitive chart-odd dual
extends through every **currently constructed** same-grade augmented
response, cap, Cartan, target, ordinary-residue, physical-(q), anchor,
(W), and shifted-ridge column.  The extension is explicit and has zero
coefficient on (q), anchor, ridge, (\eta), and (\sigma).

Presentation-safe relative carrier graphs do not kill this dual.  They force
it to take a nonzero value on the retained carrier.  In the universal
two-chart notation

\[
                         dG=t-\widehat\beta,             \tag{1}
\]

a dual with (\psi(\widehat\beta)=1) has the unique extension

\[
                         \widetilde\psi(t)=1.            \tag{2}
\]

Thus the relative graph preserves both the old (H_0) and the obstruction.
An absolute carrier saturation

\[
                         dE=t                            \tag{3}
\]

has the exact opposite effect: it prevents the dual extension and supplies
the desired chart-odd filler

\[
 \boxed{
 \Lambda=E-G,
 \qquad d\Lambda=\widehat\beta.}                       \tag{4}
\]

Equations (1)--(4) give a strict filler-or-terminal alternative once the
augmented same-grade physical map is exhaustive:

* a physical column with nonzero chart-odd carrier component constructs
  (3)--(4), possibly after its proper faces are totalized; or
* if no such column exists, the extended primitive dual is an augmented
  physical terminal.

The present inventory reaches neither terminal condition.  Its first
absent degree-zero column is the direct-chart block projector

\[
 U_{C4}[D,Q_{01};2345]
      \xrightarrow{,Dq_{01},} A H,                  \tag{5}
\]

needed to complete the three relative chart carriers.  Its first
product-rule obligations are the selected six-term (db_{01}) face and,
after the tail grants, the eighteen endpoint/direction terms of (dL_{01}).
The already computed primitive dual has nonzero value on these columns.
Consequently they are candidates for the missing saturation, not columns
which the current dual has been proved to annihilate.

The exact status is therefore:

\[
 \boxed{
 \text{the Gate-II dual extends through the named augmented map,}
 \quad
 \text{but neither }d\Lambda=\widehat\beta
 \text{ nor a full terminal is constructed.}}          \tag{6}
\]

This is a terminalization boundary, not a Krenn counterexample.  It freezes
the first unconstructed physical column and all forced dual values through
the labelled lower ladder.

## 2. Universal relative filler/terminal algebra

Let (J:C_1\to C_0) be a physical boundary map, let
(\beta\in C_0), and suppose

\[
 \psi J=0,
 \qquad
 \psi(\beta)=1.                                        \tag{7}
\]

Adjoin a presentation-safe carrier coordinate (t) and one relative graph
column

\[
                         g=t-\beta.                     \tag{8}
\]

The extension of (\psi) which kills (g) is forced:

\[
 \widetilde\psi|_{C_0}=\psi,
 \qquad
 \widetilde\psi(t)=1.                                  \tag{9}
\]

In particular (\widetilde\psi(g)=0) while

\[
 \widetilde\psi(\beta)=\widetilde\psi(t)=1.            \tag{10}
\]

The graph attachment is monic in (t), so it does not impose
(\beta=0) in the old object.  In the two-coordinate shadow
((\beta,t)), the graph column is ((-1,1)); its rank is one, and both
(\beta) and (t) raise the rank to two.

Now adjoin a physical saturation column with boundary (t).  Then

\[
                         \beta=t-(t-\beta)              \tag{11}
\]

lies in the boundary image.  The old dual cannot extend across this column,
because its forced value on (t) is one.  Conversely, if an exhaustive
physical boundary map contains no column whose image has nonzero pairing
with (9), then (9) is a genuine terminal.

This elementary fork is the correct interpretation of the relative graph.
Setting (t=0) inside (8) would fill (\beta), but it would also quotient
the old (H_0); it is not a presentation-safe construction.  One must
source the separate physical column (3).

## 3. Extension through the known Gate-II augmented columns

Use the four-corner characters

\[
 \alpha=(-1,1,1,-1),
 \qquad
 \delta=(1,1,-1,-1),
 \qquad
                         \alpha\mathbin\cdot\delta=0.   \tag{12}
\]

The primitive augmented dual has values

```text
local cap B              delta
target                  -delta
W                       -delta
ordinary residue         delta
Eq, M, ainc, q, P_f      0
ridge                    0
eta, sigma               0
```

The known physical columns are

\[
\begin{aligned}
 r0_j&=B_j+Eq_j+\operatorname {target}_j-\operatorname {ainc},\\
 T_j&=-W_j+\operatorname {target}_j,\\
 \rho_j&=W_j+\operatorname {ores}_j,\\
 K&=\sum_j\alpha_j\operatorname {ores}_j+\operatorname {ridge}.
                                                               \tag{13}
\end{aligned}
\]

The dual kills every column separately:

\[
 \delta_j-\delta_j=0,
 \qquad
 \delta_j-\delta_j=0,
 \qquad
 -\delta_j+\delta_j=0,
 \qquad
 \alpha\mathbin\cdot\delta=0.                         \tag{14}
\]

Because its (q), anchor, (P_f), ridge, (\eta), and (\sigma)
coefficients are zero, the already named columns in those rows add no new
condition.  The common-tail escape coefficient is also zero.  This is an
exact extension over the committed cap--Cartan augmented map, not yet over
an unconstructed exhaustive same-grade source map.

## 4. The forced values on the relative three-cap carrier

Put

\[
 A=Dq_{01},
 \qquad B=p_0s_1,
 \qquad C=p_1s_0,                                      \tag{15}
\]

with

\[
 H=q_{23}q_{45}+q_{24}q_{35}+q_{25}q_{34},             \tag{16}
\]

and set

\[
 R_{01}=(A+B+C)H,
 \qquad
 L_{01}=(2A-B-C)H.                                     \tag{17}
\]

Normalize the corrected occurrence dual by

\[
 \psi(L_{01})=1,
 \qquad
 \psi(R_{01})=-1.                                      \tag{18}
\]

The presentation-safe three-cap totalization is relative:

\[
 dG_R=t_R-R_{01},
 \qquad
 dG_L=t_L-L_{01}.                                      \tag{19}
\]

Equations (9) and (18) force

\[
 \boxed{
 \widetilde\psi(t_R,t_L)=(-1,1).}                      \tag{20}
\]

Hence the three-cap graph does not turn (\psi) into a terminal on the old
rows and does not fill (L_{01}).  It transports the detected class onto
the carrier orbit.  An absolute (t_L)-column would fill (L_{01}) by

\[
                         L_{01}=t_L-(t_L-L_{01}),        \tag{21}
\]

and its pairing with the forced dual is one.

The same statement is the local Gate-II realization of the uniform
operation-tag theorem.  The relative switch graph has

\[
 dG_B=t_B-(B-A),
 \qquad
 dG_C=t_C-(C-A),                                       \tag{22}
\]

and therefore

\[
 L_{01}+t_B+t_C=d(G_B+G_C).                            \tag{23}

If one physical augmented chain (E_B+E_C) has boundary (t_B+t_C), then

\[
 d\bigl(G_B+G_C-(E_B+E_C)\bigr)=L_{01}.                \tag{24}

Thus the Gate-II saturation is literally the (h=3) instance of (3)--(4).

## 5. The first absent same-grade columns

The endpoint response deformation constructs presentation-safe relative
carriers for the (B) and (C) chart fibres.  In the complete
105-occurrence module, those two fibres have rank two.  Adjoining either
(R_{01}) or (L_{01}) raises the rank to three.  The normalized
direct-chart covector has values

\[
                         (B,C,R_{01},L_{01})=(0,0,1,2). \tag{25}
\]

The missing third graph is the direct (A) chart.  Its exact candidate
source is (5), followed by physical reinsertion by (Dq_{01}).  This is the
first absent degree-zero column; a universal formal coefficient parameter
would add another graph coordinate but would not construct the fixed
physical cap comparison.

At first principal-parts order, the current endpoint construction stops
even earlier.  The identity

\[
                         dc_{01}=30db_{01}-dR           \tag{26}
\]

exposes the selected six-term (db_{01}) packet.  It raises the selected
PP rank from two to three.  Residual matching averaging fixes its aggregate
and cannot contract it.

Grant (26), its endpoint-reversed mate, and the lower (U_{C4}) tail.  The
next remaining face is exactly the eighteen endpoint/direction terms of
(dL_{01}).  The six marginals and their primitive profile are

\[
 (6,6,-3,-3,-3,-3)
      =3(2,2,-1,-1,-1,-1).                             \tag{27}
\]

The normalized Gate-II dual is zero on the eighteen residual-tail terms
and one on (27).  Therefore a covariant (R_{01}) three-cap cannot simply
be appended as an absolute top column.  Its proper face either extends the
physical saturation or carries the dual onward.

## 6. The forced lower carrier values

The labelled two-root descent of (27) reaches the private word `0102`.
On its twelve occurrence coordinates, the primitive detector is

\[
                         d=e_0^*+e_3^*-e_1^*-e_6^*.     \tag{28}
\]

It kills the complete response and has value

\[
                         d(z_{0102})=-\frac{13}{6}       \tag{29}
\]

on the private face.  For the centered operator (C=12I-J), one has

\[
                         Cd=12d,                        \tag{30}
\]

so the relative P2 graph again forces a nonzero carrier dual rather than
killing it.

The (q_{23}) product rule transports the class into the independent
(dq_{23}) block.  The best occurrence-by-occurrence cap cancellation has

\[
 \operatorname {Q!-!component}=\frac{35}{72},
 \qquad
 \operatorname {labelled\ ores}=-\frac{35}{72}.         \tag{31}
\]

Its scalar ordinary residue is zero.  Conditional on a physical
occurrence-to-(Q/ores) map, the mixed-target square, complete-response
gauge, pure (d_{\rm even}) section, and aggregate scalar correction, the
two values in (31) cancel and no new labelled direction appears.  Those
hypotheses are not constructed by the present same-grade map.

Thus the dual-extension ladder is finite and exact:

```text
chart-odd L01
  -> relative (t_R,t_L), forced dual (-1,+1)
  -> 18 endpoint/direction terms, dual 1
  -> word-0102 carrier, detector -13/6 and C*d=12*d
  -> dq23 / Q-ores, labelled residue -35/72.
```

Each presentation-safe graph carries the dual forward.  Only a physical
absolute saturation column can stop it.

## 7. Relation to the common four-cut homotopy and all moments

The uniform oriented curvature factors are

\[
 K^\rightarrow=q-x,
 \qquad
 K^\leftarrow=q-r+x.                                   \tag{32}
\]

The tagged overlap class (\widehat\beta) is exactly the descent
obstruction to placing their two local primitives in one decorated module.
If the Gate-II/relative-Hasse programme constructs (3), then (4) kills the
overlap class.  The two oriented primitives may be added and

\[
\begin{aligned}
 \Gamma&=-(\Gamma^\rightarrow+\Gamma^\leftarrow),\\
 d\Gamma&=-(q-x)-(q-r+x)=r-2q.                         \tag{33}
\end{aligned}
\]

In that same (k[q,r])-module, for

\[
 H_s=\int_0^1t^s(q+tr)^{[h-2]},dt,                     \tag{34}
\]

the strict Leibniz rule gives

\[
 \boxed{
 d(\Gamma H_s)=(r-2q)H_s
 \quad\text{for every }s\geq0.}                        \tag{35}
\]

So constructing the single chart-odd saturation eliminates the entire
moment tower; no separate weighted comparison remains.

## 8. Exact fork and scope

Let (J_{\rm full}) be the genuinely exhaustive same-grade augmented
physical map, including the columns and faces absent from the current
inventory.  Let (b_t) be the chart-odd carrier class.  Exact linear
duality gives

\[
 \boxed{
 b_t\in\operatorname {im}J_{\rm full}
 \quad\text{or}\quad
 \exists\Psi:\ \Psi J_{\rm full}=0,\ \Psi(b_t)=1.}     \tag{36}
\]

The first branch constructs (3)--(4); the second is the accepted augmented
terminal.  There is no third branch.

The current calculations do not yet instantiate (J_{\rm full}).  They
prove that the old primitive dual extends across every named augmented
column and force its values on every retained relative carrier.  They also
identify the first omitted top and PP columns on which it has nonzero
pairing.  Therefore calling the current dual a terminal would be premature,
while declaring the carrier filled would discard the very proper faces
which the dual detects.

This note is exact for the canonical (h=3) Gate-II response, cap--Cartan,
first-PP, labelled P2, and conditional (Q/ores) modules.  The reduction
from (4) to (33)--(35) is uniform in (h).  It does not construct the
uniform physical saturation or a full GHZ tensor.

## Verification

Run

```text
python3 computations/verify_h3_chart_odd_gate_ii_augmented_filler_terminal_fork.py
python3 -O computations/verify_h3_chart_odd_gate_ii_augmented_filler_terminal_fork.py
python3 -I -S computations/verify_h3_chart_odd_gate_ii_augmented_filler_terminal_fork.py
```

The checker pins the Gate-II primitive dual, same-grade extension chain,
relative three-cap carrier, endpoint response landing, uniform operation-tag
obstruction, labelled (Q/ores) gate, and strict all-moment theorem.  It
verifies (7)--(11), every known cap--Cartan column in (13), the forced carrier
values (20), the primitive profile (27), (Cd=12d), the cancellation (31),
and the sign in (33).  It does not manufacture any missing source column.
