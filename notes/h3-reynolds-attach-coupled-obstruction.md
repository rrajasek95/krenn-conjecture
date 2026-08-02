# The Reynolds symbol cannot attach before a new cap chain appears

Exact obstruction in the smallest combined denominator/cap complex. This
note derives the cap differential and ordinary-residue map from their
generator meanings, then tests the chain-map equation for the canonical
\(q\)-zero Reynolds symbol from commit ed60e2c. It proves that the
attaching problem cannot be solved sequentially inside the old split-cap
block. It does not obstruct a simultaneous lift using the higher physical
Koszul/curvature sector, compute that sector, or prove Krenn's conjecture.

## Outcome

Work over the universal coefficient domain \(R\) containing the internal
edge variables and \(Y\), and retain the nonzero desired scalar below. On
the final active chart one may further invert \(\kappa Y\).

Let \(\gamma\) record the harmless cap normalization:

\[
 \gamma=1\quad\text{if }Y_0\mapsto w,
 \qquad
 \gamma=Y\quad\text{if }Y_0\mapsto Yw.                  \tag{1}
\]

The Reynolds calculation gives a formal top-symbol complex, one copy per
deleted face,

\[
 J_v^1=R\langle j_v\rangle
   \mathop{\longrightarrow}^{d_J}
 J_v^0=R\langle y_v\rangle,
 \qquad d_Jj_v=y_v,                                     \tag{2}
\]

and the desired degree-zero comparison is

\[
                         \Phi_0(y_v)=\gamma w_v.         \tag{3}
\]

Equation (2) is derived from the complete fifteen-column denominator
presentation:

\[
 L_v={1\over3}\sum_{N\in\operatorname {PM}(F_v)}\partial_N,
 \qquad
 L_vP_m\delta(d_{s,a})
   =\delta_{vs}\delta_{a,m_v}Y_0.                        \tag{4}
\]

It is still only the Reynolds-reduced formal principal-parts symbol complex,
not a physical source lift.

The smallest cap complex is

\[
 G_v^1=R\langle T_v,\rho_v\rangle
   \mathop{\longrightarrow}^{d_G}
 G_v^0=R\langle w_v\rangle.                              \tag{5}
\]

Its maps are not assigned augmented coordinates. They are forced by the
generator meanings:

- \(\rho_v\) is the normalized selected ordinary-response generator, so
  \(d_G\rho_v=w_v\);
- \(T_v+Y\rho_v\) is the cap graph cycle, so
  \(d_GT_v=-Yw_v\);
- physical target is projection to the \(RT_v\) summand; and
- ordinary residue is the selected-word augmentation of the
  \(R\rho_v\) summand.

Consequently

\[
\begin{array}{c|cc}
 &T_v&\rho_v\\ \hline
 d_G&-Yw_v&w_v\\
 \operatorname {tgt}&1&0\\
 \operatorname {ores}&0&1.
\end{array}                                              \tag{6}
\]

Now write a possible attaching value as

\[
                     \Phi_1(j_v)=aT_v+b\rho_v.           \tag{7}
\]

The literal chain-map and invisibility equations are

\[
                  -Ya+b=\gamma,\qquad a=0,\qquad b=0.   \tag{8}
\]

They are inconsistent for nonzero \(\gamma\). If only target invisibility
is imposed, (8) has the unique solution

\[
                 \Phi_1(j_v)=\gamma\rho_v,\qquad
                 \operatorname {ores}\Phi_1(j_v)=\gamma. \tag{9}
\]

Therefore the bare-cap statement is an if-and-only-if:

\[
\begin{aligned}
 &\exists z\in G_v^1:\quad
 d_Gz=\gamma w_v,\quad
 \operatorname {tgt}(z)=\operatorname {ores}(z)=0\\
 &\hspace{42mm}\Longleftrightarrow\quad \gamma=0.        \tag{9a}
\end{aligned}
\]

For the desired nonzero normalization, the left side is false.

Thus the Reynolds \(q\)-zero symbol reaches the old ordinary-response
graph, but it cannot become an invisible attaching chain in the old cap
block. Equivalently, the exact obstruction is

\[
 \boxed{
 [\gamma w_v]\ne0\quad\text{in}\quad
 {G_v^0\over d_G(\ker\operatorname {tgt}
                       \cap\ker\operatorname {ores})}
 =Rw_v.}                                                \tag{10}
\]

For the five block-diagonal faces, (10) has rank five. This is a statement
about the smallest five-copy cap complex; it is not a lower bound on the
number of generators in a full source representation.

The smallest missing type is now exact. One needs a new cap-degree-one
chain \(n_v\) with

\[
 d_Gn_v=\gamma w_v,\qquad
 \operatorname {tgt}(n_v)=0,\qquad
 \operatorname {ores}(n_v)=0.                           \tag{11}
\]

Adjoining (11) by declaration solves the attaching equation by
\(\Phi_1(j_v)=n_v\), but supplies no source provenance. Therefore
\(\mathfrak A_{\rm attach}\) cannot be completed **before** the higher
Koszul/connection/curvature sector: that sector must simultaneously
manufacture a chain of type (11). The two formerly sequential tasks are a
single coupled construction problem.

The first possible source filtration is still total principal-parts order
four. Orders two and three have positive \(q\)-degree and nonzero
stabilizer weight. At order four, (4) gives the invariant \(q\)-degree-zero
symbol, but the cap obstruction (10) remains. No larger polynomial degree
inside \(R\langle T,\rho\rangle\) helps, because the common augmentation
kernel is zero in every degree and after every base change. Thus the
obstruction survives every base change on which \(\gamma\) remains nonzero.

## 1. The formal Reynolds source complex

Let \(D=\{1,\ldots,5\}\), \(m=12112\), and
\(F_v=D\setminus\{v\}\). The complete odd denominator presentation is

\[
 C_{\rm den}^1
   =\bigoplus_{s\in D,\ a\in\{0,1,2\}}Rd_{s,a}
 \mathop{\longrightarrow}^{\delta}
 C_{\rm odd}^0
   =\bigoplus_{c\in\{0,1,2\}^D}Re_c,                    \tag{12}
\]

with

\[
 \delta(d_{s,a})
   =\sum_{c:c_s=a}
       \operatorname {Haf}(q_c|_{D\setminus\{s\}})e_c.  \tag{13}
\]

Extracting \(e_m\) and renaming it \(Y_0\) gives

\[
 P_m\delta(d_{s,a})
   =\begin{cases}
      h_sY_0,&a=m_s,\\
      0,&a\ne m_s,
     \end{cases}
 \qquad
 h_s=\operatorname {Haf}(q_m|_{F_s}).                   \tag{14}
\]

Apply the Reynolds operator in (4). For \(s=v\), each of the three matching
derivatives selects one monomial of \(h_v\), so their normalized sum is one.
For \(s\ne v\), every matching of \(F_v\) contains an edge incident to
\(s\), while no monomial of \(h_s\) contains such an edge. This proves (4)
on all fifteen columns.

The formal symbol \(j_v\) in (2) means the normalized average of the three
top principal-parts labels. Its differential \(y_v\) records the unique
surviving pure word symbol. This is a legitimate two-term **formal symbol**
complex because its differential is the identity and hence squares to zero.
It is not the attaching comparison: no cap or ordinary-residue map has yet
been defined on \(j_v\).

## 2. Deriving the smallest cap complex

The degree-one cap module has two independently defined summands:

\[
       G_v^1=G_{\rm tgt}^1\oplus G_{\rm ores}^1
             =RT_v\oplus R\rho_v.                       \tag{15}
\]

The physical target map is the structural projection
\(G_v^1\to G_{\rm tgt}^1\cong R\). The ordinary residue is obtained in a
different way: the selected pure word maps to the ordinary response line
\(R\rho_v\), whose coefficient augmentation is
\(R\rho_v\to R\). Thus

\[
 \operatorname {tgt}(aT_v+b\rho_v)=a,\qquad
 \operatorname {ores}(aT_v+b\rho_v)=b.                  \tag{16}
\]

The cap relation row is normalized so that one unit of ordinary response
has boundary \(w_v\):

\[
                         d_G\rho_v=w_v.                  \tag{17}
\]

The actual cap graph is \(g_v=T_v+Y\rho_v\). Requiring it to be closed,
together with (17), forces

\[
                  0=d_Gg_v=d_GT_v+Yw_v,
 \qquad\text{hence}\qquad d_GT_v=-Yw_v.                 \tag{18}
\]

Equations (16)--(18) derive every entry of (6). In particular,

\[
 (\operatorname {tgt},\operatorname {ores}):
        G_v^1\longrightarrow R^2
\]

is an isomorphism, not merely a generic-rank map. Its kernel remains zero
under arbitrary base change. This is why non-flat specialization of the
bare cap block cannot make (8) solvable while the desired boundary
\(\gamma w_v\) remains nonzero.

## 3. The chain-map commutator

Given the fixed degree-zero map (3), an attempted degree-one map has Hom
complex commutator

\[
 \omega_{\Phi}(j_v)
   =d_G\Phi_1(j_v)-\Phi_0d_J(j_v)
   =(-Ya+b-\gamma)w_v.                                  \tag{19}
\]

There are exactly two relevant possibilities:

1. impose target zero and solve \(\omega_\Phi=0\). Then
   \(a=0,b=\gamma\), so the ordinary residue is \(\gamma\);
2. impose both target and ordinary residue zero. Then \(a=b=0\), so
   \(\omega_\Phi(j_v)=-\gamma w_v\ne0\).

This proves (10) without choosing coordinates for a hypothetical new chain.
It also identifies the missing commutator exactly:

\[
                     \omega_{\rm inv}(j_v)=-\gamma w_v. \tag{20}
\]

After curvature multiplication it becomes
\(-\kappa\gamma w_v\). Curvature scaling does not kill it on the active
open; it only gives the final normalization.

## 4. Why polynomial degree and averaging cannot repair it

Allow \(a,b\) in any polynomial or localized coefficient ring. The two
augmentations in (16) still force \(a=b=0\). Therefore no multiplier,
higher \(q\)-degree, Reynolds combination, flat base change, or non-flat
base change of this split free module changes (20).

The checker also expands \(a,b\) as arbitrary polynomials in \(Y\) through
degree eight. For desired boundary \(w_v\) and for desired boundary
\(Yw_v\), the augmented linear system always has rank one more than its
coefficient matrix. These finite systems are diagnostic shadows of the
exact split-projection proof, not a degree-bounded substitute for it.

The degree statement concerns the **first source candidate**, not the cap
no-go. The exact ladder from ed60e2c is

\[
\begin{array}{c|c|c}
\text{total PP order}&q\text{-degree}&\text{top weight}\\ \hline
2&2&\ne0\\
3&1&\ne0\\
4&0&0.
\end{array}                                             \tag{21}
\]

Thus a source-provenant chain of type (11) first has a compatible symbol at
order four. The old cap block cannot supply it at order four or any later
order.

## 5. The coupled next problem

The physical two-row Koszul cell has

\[
 K_m^{\rm phys}
  =u r_m+\widetilde K_m,\qquad
 \widetilde K_m=H_mr_0-H_0r_m.                          \tag{22}
\]

Commit ed60e2c found the correct Reynolds polynomial face for the reset
of \(ur_m\). The present calculation proves that this face cannot attach to
the already existing cap module. Therefore the next construction cannot
first solve \(\mathfrak A_{\rm attach}\) and only afterward handle
\(\widetilde K_m\) and the endpoint-\(22\)-to-\(00\) curvature side.

Instead, one must define a single comparison on the full packet whose
higher component contributes \(n_v\) in (11). Its equations are

\[
\begin{aligned}
 d n_v&=\gamma w_v,\\
 \operatorname {tgt}(n_v)&=0,\\
 \operatorname {ores}(n_v)&=0,\\
 (d_{\rm cap}\Phi_{\ge1}+\Phi_{\ge1}d_{\rm Eq})
       (\widetilde K_m)
   +\mathfrak C_{22\to00}
   +\kappa\,\omega_{\rm inv}&=0.                         \tag{23}
\end{aligned}
\]

The final line is a specification, not a constructed cancellation. It says
where (20) must go: the higher physical/curvature sector must contribute
the new degree-one chain and cancel the same commutator. Merely adjoining
\(n_v\) to the cap complex would assume the theorem.

This result is deliberately local. A larger full-source complex can contain
new degree-one chains, couple the five face weights, or acquire them through
a specialization kernel. None of those mechanisms is tested here. What is
ruled out is the faster sequential route through the old
\(\langle T,\rho\rangle\) cap span.

## 6. Exact verification

The dependency-free checker
[verify_h3_reynolds_attach_coupled_obstruction.py](../computations/verify_h3_reynolds_attach_coupled_obstruction.py)
verifies:

- the complete fifteen-column Reynolds differential (4);
- the identity differential of the five formal top-symbol lines;
- the derivation \(dT=-Yw,d\rho=w\) from graph closure;
- the structural target and ordinary-residue projections;
- inconsistency of (8) in both normalizations;
- rank five of the block-diagonal obstruction;
- all polynomial ansätze through degree eight; and
- the exact type and first degree of the missing generator (11).

Its frozen certificate digest is

    ee3699d5267fa63c896a50304f6548f565e6a09986fc5c54a9b6455928b3d5aa

The diagnostic extension by \(n_v\) in the checker verifies only that (11)
is the minimal algebraic repair. It does not construct \(n_v\) from the
source or assign readouts without first defining the enlarged complex.
