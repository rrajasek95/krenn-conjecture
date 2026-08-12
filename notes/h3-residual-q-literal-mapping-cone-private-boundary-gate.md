# The residual-q correction needs a literal mapping-cone cell

## Outcome

The second full-nine chart does not repair the private-boundary defect in
the reduced-Eq/cap factorization.  In every first repeated
(P_3\sqcup K_2) component, the two charts give identical physical columns

\[
                       J(r_{0,j}^{pq})=B_j
                       =J(r_{0,j}^{pr}),               \tag{1}
\]

where (B_j) is a complete 90-term matching boundary.  Each pure
row/multiplier label has between 42 and 46 features which occur in no other
column.  Thus a private pivot gives the coefficientwise equation

\[
                  x_j^{pq}+x_j^{pr}=0.                 \tag{2}
\]

The same sum in (2) controls the physical Eq, target, and anchor entries of
the two copies.  Consequently a second chart can cancel the private
matching boundary only by canceling the entire physical (r_0) contribution
needed by the cap construction.

This is a literal result, not the reversal of a projected obstruction.  The
checker reconstructs all five complete components.  Per component it finds

```text
one chart:   288 columns, rank 288, kernel 0
two charts:  576 columns, rank 288, kernel 288
kernel:      pairwise pq-pr differences
```

It tests all (5\binom64=75) ways to select four literal pure labels.  For
every selection, the four-corner (alpha)-aggregate below has exactly 360
nonzero matching features and retains a private pivot with coefficient
(alpha_j) in each block.

## Why the projected reduced-Eq cell is still insufficient

Use

\[
 \alpha=-\delta=(-1,1,1,-1)
\]

in the corner order

```text
P+q00, P-q00, P+q11, P-q11.
```

At normalized cap value (Y=1), retain one actual private pivot and the
separately labelled Eq, (W), target, and residue rows at every corner.
For a fixed corner the available columns are

\[
\begin{array}{c|rrrrr}
 &\mathrm{private}&\mathrm{Eq}&W&\mathrm{target}&R\\ \hline
r_0^{pq}=r_0^{pr}&1&1&0&1&0\\
T&0&0&-1&1&0\\
\rho&0&0&1&0&1\\
C_{\rm proj}&0&-1&0&0&0.
\end{array}                                             \tag{3}
\]

The physical anchor value of either (r_0) copy is (-1); the other
columns have anchor zero.  The primitive covector

\[
                \Phi_j=\mathrm{private}_j-W_j
                       -\mathrm{target}_j+R_j           \tag{4}
\]

kills both chart copies and every other column in (3), while

\[
                         \Phi_j(-\delta)=\alpha_j.       \tag{5}
\]

All four values in (5) are nonzero.  Therefore even the complete doubled
chart block plus a reduced-Eq column having only the projected signature
((-\mathrm{Eq})) cannot supply the residue correction.

Equation (4) also exposes the exact flaw in the coarse factorization.  A
literal reduced-Eq cell cannot have only Eq boundary.  It must carry the
negative complete full-nine boundary as well:

\[
             J(C_j^{\rm lit})=(-B_j,-\mathrm{Eq}_j;
                    W=\mathrm{target}=R=\mathrm{ainc}=0).       \tag{6}
\]

Then, and only then, the formal corner identity lifts:

\[
       -r_{0,j}+T_j+\rho_j-C_j^{\rm lit}
            =(R_j=1,\mathrm{ainc}=1)                  \tag{7}
\]

with every literal boundary, Eq, (W), and target coordinate canceled.

## The smallest aggregate cell

Four separately constructed cells (6) would suffice, but the current rank
does not force four generators.  Only their fixed endpoint-odd combination
is needed.  Put

\[
 O_\alpha=\sum_j\alpha_j(-r_{0,j}+T_j+\rho_j).         \tag{8}
\]

Its exact augmented image is

\[
\begin{array}{c|c}
\text{literal full-nine boundary}&-\sum_j\alpha_jB_j\\
\text{Eq corners}&(-\alpha_j)_j\\
\text{ordinary-residue corners}&(\alpha_j)_j\\
D,W,\mathrm{target},\mathrm{ainc}&0.
\end{array}                                             \tag{9}
\]

Here target cancellation is cornerwise between (-r_0) and (T); it is
not obtained by incorrectly summing different target monomials.  Total
anchor incidence vanishes because (sum_j\alpha_j=0).

The smallest sufficient new datum is one aggregate relative/mapping-cone
cell (M_v) whose literal image is

\[
\boxed{
\begin{aligned}
J_{\rm lit}(M_v)&=+\sum_j\alpha_jB_j,\\
J_{\rm Eq}(M_v)&=(+\alpha_j)_j,\\
(D,W,\operatorname{tgt},\operatorname{ores},
  \operatorname{ainc})(M_v)&=(0,0,0,0,0),\\
\tau_{\eta_z}(M_v)&=1+\delta_{vz}u_z/t,\\
\tau_\sigma(M_v)&=-q_{pq}^{22}.
\end{aligned}}                                           \tag{10}
\]

Combining (9) and (10) cancels all 360 literal terms and every Eq term,
leaving exactly

\[
 \operatorname{ores}=-\delta,qquad
 D=W=\operatorname{tgt}=\operatorname{ainc}=0,          \tag{11}
\]

together with the required eta/sigma terminal packet.  Adjoining the one
column (10) raises the audited augmented rank by one and places (11) in the
extended image.  Unique pivots force every displayed (B_j) coefficient,
so (10) is also the sharp literal specification of the missing direction.

This is an image criterion, not a construction of (M_v).

## What the chart difference can and cannot do

The complete doubled module has kernel

\[
                         k_j=r_{0,j}^{pq}-r_{0,j}^{pr}. \tag{12}
\]

Every chart-neutral physical functional factors through (1), so it kills
(12).  In particular, the physical boundary and the existing (W), target,
ordinary-residue, and anchor readouts of (12) are zero.  A physical
eta/sigma terminal which descends through the same physical column must
also read zero.

There is one important qualification.  A chart-**odd** marked cochain can
read nontrivially on a chart difference.  The pinned non-Euler chart-(H^1)
audit gives value one on its selected (pq-pr) class.  That does not supply
the terminal in (10): the marked value fails to descend to the physical
quotient and itself requires a higher comparison whose boundary kills the
presentation-(H^1) class.  Thus either branch leads to the same conclusion:

* a chart-neutral terminal gives zero on (12);
* a chart-odd value is another mapping-cone obligation, not an eta/sigma
  correction.

Most importantly, (J(k_j)=0), whereas (10) has the forced nonzero literal
boundary (\sum_j\alpha_jB_j).  No choice of terminal value on a chart
difference can repair that mismatch.

## Exact frontier

The second-chart shortcut and the projected reduced-Eq shortcut are both
closed.  The remaining positive theorem is the literal membership statement

\[
 M_v\in\operatorname{im}\!\left(\Psi_v^{\rm phys,rel}\right). \tag{13}
\]

where \(\Psi_v^{\rm phys,rel}\) retains all complete matching features, the
four Eq and residue corners, protected readouts, source word and grade, and
the eta/sigma terminal rows.  A single cell can satisfy all of (10); present
ranks do not force multiple generators.  No committed source family proves
(13).

The statement is frozen on the normalized clean-C5 slice (Y=1).  The
normalization was harmless for the earlier separator but not automatically
for a constructive factorization; a general-(Y) version must rederive the
cap coefficients or work after an explicitly authorized (Y^{-1})
localization.

Verification:

```text
python3 computations/verify_h3_residual_q_literal_mapping_cone_private_boundary_gate.py
python3 -O computations/verify_h3_residual_q_literal_mapping_cone_private_boundary_gate.py
python3 -I -S computations/verify_h3_residual_q_literal_mapping_cone_private_boundary_gate.py
```

Frozen ledger SHA-256:

```text
b0ae90d59463a539a91c5226eace53d55bbeb385fc184af15ebca12cac36d6ff
```
