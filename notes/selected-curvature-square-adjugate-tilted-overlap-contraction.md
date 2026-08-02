# The selected curvature square contracts the star overlap, not the adjacent-power target defect

Research reduction only.  This note proves a power-free all-label
contraction inside Component I of the
[unified two-chart target](unified-full-nine-two-chart-overlap-jet-saturation-target.md).
It does not construct the relative Rees extension, the filtered \(d_2\), an
active clean cap, `SP-CLEAN-BRIDGE`, or a proof of Krenn's conjecture.

## 1. Outcome

The selected direct square

\[
              M=\begin{pmatrix}A&B\\F&U\end{pmatrix},
              \qquad \kappa=AU-BF\ne0                         \tag{1}
\]

does give an explicit source-faithful contraction of the ordinary
two-chart star channel.  The connection and opposite-shore connection
produce two transition forms \(D,E\), their normal companions expose
\(-(h-1)D\) and \(+(h-1)E\), and

\[
 \operatorname {adj}(M)^{\mathsf T}\binom y t=\binom E D,
 \qquad
 M^{\mathsf T}\binom E D=\kappa\binom y t .                 \tag{2}
\]

Thus the selected relative star channel is contractible after division only
by the already nonzero scalar \((h-1)\kappa\).  No entry of \(M\), trace,
star, or internal quadratic is inverted.  The formulas extend, by literal
all-label contraction, to every actual tilt \(J=I+E_{uv}\).  They also
specialize without loss to the direct-free branch \(A_{pr}=0\), where the
contraction becomes triangular.

This is the useful positive part of Component I.  It retains a diagonal
target row **absolutely**: the \(J\)-contracted full-nine row has target

\[
                       T(J)=\Delta+\mathbf1_{u=v}X_u,          \tag{3}
\]

and the direct-free \(I\)-row has target \(\Delta\).  But the contraction
does not carry that row through the relative comparison.  Every connection,
normal difference, curvature, and opposite-shore difference has physical
target zero.  In the relative chart difference the two identical copies of
\((3)\) cancel, while in the absolute module the surviving common target row is
untouched by the contraction.

Consequently these rows do not supply the new adjacent-power generator
\(n_c\) isolated by the
[first filtered-\(d_2\) obstruction](h3-target-augmented-filtered-d2-first-obstruction.md).
At \(h=3\), admitted same-power anchors still lie on the cap graph

\[
                         (T,R)=(\gamma,\gamma\overline Y_c),   \tag{4}
\]

whereas the required new generator must cancel the cap-relation row while
retaining \((0,-\kappa\overline Y_c)\).  The selected adjugate operations
are scalar combinations and chart differences; they preserve the matching
power and cannot leave the graph \((4)\).

There is one sharper all-label obstruction.  Before the two halves of the
curvature normal are added, they contain the common mode

\[
                C(K)=\sum_{i,k}K_{ik}x_i(S_{kd}y_b-Q_{bd}t_k). \tag{5}
\]

It occurs once with sign \(+\) and once with sign \(-\), and hence disappears
from the available total normal row.  The opposite-shore connection controls
the same parenthesis only after multiplication by the internal quadratic
\(z\).  It does not make \(C(K)\) a boundary, and cancelling that extra \(z\)
would be precisely the illegal power cancellation which the relative Rees
construction is meant to replace.

The exact cross-word gaps in the bounded selected-cap guards do not alter
this conclusion.  Their three pure rows are the three target-bearing graph
anchors.  Every remaining gap is an \(r\)-normal cross word with target zero,
but its physical odd word is nonmonochromatic, so its coefficient on every
\(Y_c\) is zero.  These rows invalidate the bounded packets as full sources;
they do not themselves furnish a target-zero nonzero-\(Y_c\) nullhomotopy.

## 2. All-label power-free formulas

Fix physical labels \(b,d\), and allow \(0\le i,k\le2\).  On the common
complement of \(p,q,r,s\), put

\[
\begin{aligned}
 P_i&=A_{pq}(i,b),& R_{ik}&=A_{pr}(i,k),\\
 Q&=A_{qs}(b,d),& S_k&=A_{rs}(k,d),
\end{aligned}                                                \tag{6}
\]

and let (x_i,y,t_k,v,z) be the four stars and internal quadratic.  The
effective quadratics and \(s\)-normal rows are

\[
\begin{aligned}
 f_i&=P_i z+x_i y,&g_{ik}&=R_{ik}z+x_it_k,\\
 \phi&=Qz+yv,&\psi_k&=S_kz+t_kv,\\
 H_i&=P_iv+E_i y+Qx_i,&
 N_{ik}&=R_{ik}v+E_it_k+S_kx_i .
\end{aligned}                                                \tag{7}
\]

Define, label by label,

\[
\begin{aligned}
 D_{ik}&=P_it_k-R_{ik}y,\\
 E_{ik}&=S_ky-Qt_k,\\
 \Gamma_{ik}&=P_iS_k-R_{ik}Q,\\
 C_{ik}&=x_iE_{ik}.
\end{aligned}                                                \tag{8}
\]

Direct expansion, before multiplication by any matching power, gives

\[
\begin{aligned}
 f_it_k-g_{ik}y&=D_{ik}z,                                   \tag{9a}\\
 \psi_ky-\phi t_k&=E_{ik}z,                                \tag{9b}\\
 S_kf_i-Qg_{ik}&=\Gamma_{ik}z+C_{ik},                       \tag{9c}\\
 t_kH_i-yN_{ik}&=D_{ik}v-C_{ik}.                            \tag{9d}
\end{aligned}
\]

Adding \((9c)\)--\((9d)\) is exactly the all-label curvature normal

\[
 S_kf_i+t_kH_i-Qg_{ik}-yN_{ik}
                  =D_{ik}v+\Gamma_{ik}z.                    \tag{10}
\]

Thus \((5)\) is not a guessed error term: it is the unique literal common mode
erased when the two normal halves are totalized.

The normal companions expose both transitions without division by \(z\).
Write \(T_k=A_{qr}(b,k)\).  With the canonical coefficient \(h\),

\[
\begin{aligned}
 &[h(R_{ik}y+T_kx_i)+P_it_k]
  -[h(P_it_k+T_kx_i)+R_{ik}y]=-(h-1)D_{ik},                \tag{11a}\\
 &[h(T_kv+S_ky)+Qt_k]
  -[h(T_kv+Qt_k)+S_ky]=(h-1)E_{ik}.                       \tag{11b}
\end{aligned}
\]

These are differences of two presentations of the same physical normal
coefficient.  Their targets therefore cancel label by label.

For an arbitrary \(3\times3\) coefficient matrix \(K\), put

\[
 D(K)=\sum K_{ik}D_{ik},\quad E(K)=\sum K_{ik}E_{ik},\quad
 \Gamma(K)=\sum K_{ik}\Gamma_{ik},\quad
 C(K)=\sum K_{ik}C_{ik}.                                  \tag{12}
\]

Contracting \((9)\)--\((11)\) proves the same formulas for \(K\), with no label
change and no assumption on its rank.  In particular, for

\[
                         J=I+E_{uv},                       \tag{13}
\]

the actual tilted row has

\[
\begin{aligned}
 D(J)&=\sum_iD_{ii}+D_{uv},&
 \Gamma(J)&=\sum_i\Gamma_{ii}+\Gamma_{uv},\\
 C(J)&=\sum_iC_{ii}+C_{uv},&
 T(J)&=\Delta+\mathbf1_{u=v}X_u .                         \tag{14}
\end{aligned}

When \(u=v\), the corresponding diagonal coefficient occurs twice in every
display, just as it does in \(J\).  Hence the tilt preserves all physical
labels and all three nonzero diagonal coefficients.  On the full line
\(K(u_0,v_0)=u_0E_{ac}+v_0J\),

\[
                  \Gamma(K)=u_0\kappa+v_0\Gamma(J),        \tag{15}
\]

so the selected curvature is retained as the literal \(u_0\)-coefficient.

## 3. The selected transpose-adjugate contraction

At \((i,k)=(a,c)\), abbreviate

\[
 A=P_a,\quad B=R_{ac},\quad F=Q,\quad U=S_c,
 \quad D=D_{ac},\quad E=E_{ac}.                            \tag{16}
\]

Then

\[
 \operatorname {adj}(M)^{\mathsf T}
   =\begin{pmatrix}U&-F\\-B&A\end{pmatrix},
 \qquad
 \begin{pmatrix}U&-F\\-B&A\end{pmatrix}\binom y{t_c}
       =\binom E D.                                       \tag{17}
\]

Multiplying by \(M^{\mathsf T}\) proves

\[
                     AE+FD=\kappa y,
 \qquad              BE+UD=\kappa t_c.                  \tag{18}
\]

Equations \((11)\) and \((18)\) are the promised contraction.  Since \(h\ge3\),
\((h-1)\kappa\) is a unit in the selected characteristic-zero fibre.  The
contraction is source-faithful because its inputs are the literal normal
differences, and it is all-label because no endpoint basis change has been
made.

This contraction is only on the selected two-channel summand.  The \(J\)
identities in \((14)\) exist by all-label linearity, but \(\Gamma(J)\) need not
be nonzero and the individual \(2\times2\) minors entering it need not be
invertible.  Nothing here asserts a contraction of the whole tilted
full-nine complex.

## 4. Direct-free triangular specialization

If the whole block \(R=A_{pr}\) vanishes, then \(B=0\) and

\[
 D=At_c,\qquad E=Uy-Ft_c,qquad \kappa=AU.                 \tag{19}
\]

Equation \((18)\) becomes

\[
                   AE+FD=AUy,
 \qquad            UD=AUt_c,                              \tag{20}
\]

so it does not divide by the missing block.  The normal row is

\[
             C_4=Dv+AUz,
 \qquad      z={C_4-Dv\over AU},                           \tag{21}
\]

which is the established triangular recovery.  Meanwhile the direct-free
full-nine rows give

\[
                  p_it_kq^{[h-1]}=\delta_{ik}X_i,
 \qquad
                  \sum_ip_it_iq^{[h-1]}=\Delta.           \tag{22}
\]

Thus the diagonal target is genuinely present, but \((21)\) and \((22)\) remain
parallel pieces of the source packet.  No displayed row maps the target in
\((22)\) to the normal carrier in \((21)\).

## 5. Why the new \(n_c\) is still absent

The obstruction is not failure of the \(2\times2\) inverse.  It is a
matching-power and augmentation mismatch.

1. Equations \((9)\)--\((11)\) are target-zero differences.  Applying the adjugate
   changes only their scalar coefficients.  It cannot create a physical
   target component.
2. The full-nine row \((3)\) is target-bearing, but its target--odd-residue
   image is the graph \((4)\).  Two source-faithful chart copies give the same
   graph; their difference is zero and their common copy is precisely the
   first-page indeterminacy in the bounded filtered model.
3. Equation \((9b)\) supplies \(E(K)z\), not a boundary for \(C(K)\).  After a
   common divided power is attached, replacing \(zq^{[r]}\) by
   \((r+1)q^{[r+1]}\) returns to the Euler cancellation already present in
   the curvature/direct-double packet.  Cancelling \(z\) beforehand is not
   source-faithful.
4. Therefore the requested pair \((0,-\kappa\overline Y_c)\) is not produced.
   In the smallest augmented complex it has cap differential
   \(-\kappa\overline Y_c\,w\ne0\).  A new relative generator must have this
   as its literal boundary while retaining the odd associated-grade value.

This also separates two meanings of “retains a diagonal target row.”  The
absolute packet does retain one, by \((3)\) and \((22)\).  The relative contraction
does not: quotienting by chart difference leaves it as a common mode, while
restricting to the relative image erases it.  Neither choice gives the
target-only nullhomotopy required for the filtered \(d_2\).

## 6. Exact missing-row audit

The independent audit of the selected \(h=3\) packets, together with the
[multi-label target-Koszul no-go](h3-multilabel-target-koszul-crossword-no-go.md),
finds the following
full-EqSystem gaps.

* Direct-free packet: the pure rows
  \((0^6;00),(1^6;11),(2^6;22)\), and
  \((012112;22),(012212;21),(012212;22)\).
* Tilted packet: the same three pure rows, and
  \((002012;22),(022012;02),(022012;20),(022012;22)\).

Here the six-digit word is on the pair complement and the last two digits
are the \(pq\) endpoint labels.  The mixed rows differ from the selected
word only at the physical \(r\)-site, so they are exactly all-label normal
cross words of the type restored by \((11)\).  All have physical target zero.

Take \(x\) to be residual site zero, as in those packets.  Removing \(x\)
from a direct-free mixed word gives a nonmonochromatic word such as
\(12112\) or \(12212\); removing it from a tilted mixed word gives \(02012\)
or \(22012\).  Hence

\[
       [Y_c](\text{every mixed missing row})=0
       \qquad(c=0,1,2).                                   \tag{23}
\]

By contrast, removing \(x\) from the pure \(c^6\) row gives \(c^5\), but
that row has target \(X_c\) and therefore contributes the graph vector
\((1,\overline Y_c)\).  The target projection of the three pure graph rows
has rank three.  Its target-zero kernel is zero, and adding the mixed rows
does not change the physical \(Y_c\)-readout by \((23)\).

Thus the exact omitted rows explain why the selected packets are not full
sources and may destroy those finite counterguards.  They do not provide
the particular generator \(n_c\): at the required physical odd word the
mixed rows read zero, while the only nonzero odd rows are target-locked pure
anchors.  A cross-word **chain coupling** beyond the row values could still
be part of a larger relative Rees construction; none is inferred or ruled
out here.

## 7. Verification and strict nonclaims

The dependency-free checker
[`verify_selected_curvature_square_adjugate_tilted_overlap_contraction.py`](../computations/verify_selected_curvature_square_adjugate_tilted_overlap_contraction.py)
audits \((9)\)--\((11)\), \((14)\), and \((17)\)--\((23)\) symbolically or over exact rationals.
It checks all nine matrices \(I+E_{uv}\), the direct-free specialization,
all \(3^5=243\) all-label target comparisons, and the exact six/seven-row
gap ledgers.  The checker is optimization-safe and uses only the standard
library.

This note does not prove that the shared \((L,M)\) quotient transport is
injective, that the complete-anchor relative kernel is contractible, or
that \(C(K)\) is a boundary.  It does not construct the generator \(n_c\),
the target-augmented total differential, a nonzero \(d_2\), its
zero-indeterminacy readout, or the rootless Macaulay functional.  The
all-label formulas are a proved power-free part of Component I, not the
unified overlap--jet saturation theorem.
