# The all-moment horizontal bridge is one physical saturation homotopy

## 1. Outcome

Fix a clean intrinsic scalar-unit packet and (h\geq3).  Put

\[
 n=h-2,
 \qquad
 m=\begin{cases}1,&h=3,\\ h-3,&h\geq4.\end{cases}
\]

The exact oriented curvature factors and the target response path already
identify the shortest possible positive horizontal construction.  If the
two oriented four-cut rows are lifted **coefficientwise in the same complete
decorated polynomial carrier**, then their sum constructs the one-form

\[
 dE_h(t)=(r-2q)(q+tr)^{[n]},dt.                     \tag{1}
\]

There is not a separate uniqueness theorem for each moment.  In a physical
polynomial lift category closed under based scalar multiplication, all
required higher moments are independent of the lift if and only if the
single moment-active saturation map vanishes:

\[
 \boxed{
 (r-2q)H(\chi_h)\bigl(V_h^{\mathrm{mom}}\bigr)=0
 \quad\text{in }H(Q_h).}                              \tag{2}
\]

Here (V_h^{\mathrm{mom}}) is not an invented full evaluation kernel.  It
is the subspace of the homology kernel of the **actual complete physical
face/reinsertion map** whose classes can occur as coefficients of allowed
based-loop differences between two simultaneous oriented lifts.  Thus (2)
is the minimal source-valid hypothesis.  The stronger chain-level datum

\[
 dN_h+N_hd=(r-2q)\chi_h
       \quad\text{on the moment-active vertical subcomplex}            \tag{3}
\]

is one source-valid way to prove it.  One homotopy (3), natural in all
restriction/insertion faces, kills the based-loop residue in **every**
moment required at height (h).

The currently proved overlapping-pair and four-cut identities do not imply
(2).  They contain a literal physical chart-exchange kernel: the two
overlapping pair charts present the same four-cut target row, and their
difference evaluates to zero by the exact Bianchi identity.  Retaining the
two chart tags gives a nonzero decorated kernel class until a physical
chart-change two-cell kills it.  Valuing a Rodrigues based loop in this
exchange class preserves the full cross-pair reinsertion square, both
endpoints, and the unweighted row, but it changes the higher moments unless
(2) holds.

This is sharper than the free filtered-DGM guard: its vertical direction
comes from an exact physical overlapping-pair matching identity.  It is
still **not** a full decorated GHZ source or a counterexample to Krenn's
conjecture.  The packet does not impose every residual word, pure target,
anchor, terminal, physical-(q), and fine/repeated-grade face, and it does
not prove that the exchange class survives the homology of that completed
source.  It proves exactly that one physical overlap square does not kill
the class.  The remaining viable gluing input is a source-valid
restriction/insertion Bianchi two-cell satisfying (3), or an equivalent
rank-saturation theorem in the full decorated complex.

## 2. The physical objects which must be kept together

Let (S=\mathbb K[q,r]), with (\operatorname {char}\mathbb K=0).  A
positive proof must use the following literal complexes, not only their
evaluated coefficient spaces.

* (\mathscr C_h^{(4)}[t]dt) is the ordered four-star source complex.  Its
  generators retain the pair chart, the four ordered star roles, the word,
  fine and repeated grade, target, anchor, terminal, physical-(q), and
  protected rows.
* (\pi_h:\mathscr C_h^{(4)}\to\mathscr A_h) is the simultaneous map
  recording every physical face and ordered reinsertion into the top
  response module.  It is stronger than numerical evaluation of one
  four-cut row.
* (\chi_h:\mathscr C_h^{(4)}\to Q_h) is a common-carrier desuspension.
  The target (Q_h) is one decorated (S)-complex in which multiplication
  by (q,r) is legal and the exceptional ((a,a)) target remains present.

The exact top response identity is

\[
 S_{jk}(t)=R_{jk}(q+tr)^{[h-1]},
 \qquad
 S'_{jk}(t)=R_{ja}R_{ak}(q+tr)^{[n]}.                  \tag{4}
\]

It is a literal polynomial identity with the ordered star roles retained.
It does not yet desuspend (R_{ja}R_{ak}), and it does not identify the
two oriented restrictions.

The two exact oriented curvature factors are

\[
 K^\rightarrow=q-x,
 \qquad
 K^\leftarrow=q-r+x,
 \qquad
 -(K^\rightarrow+K^\leftarrow)=r-2q.                 \tag{5}
\]

A **simultaneous polynomial carrier lift** consists of one carrier
(J_h(t)\in Q_h[t]), whose top response is the right side of (4), and two
literal oriented primitives (B_h^\rightarrow(t),B_h^\leftarrow(t)) in
the same complex such that

\[
 dB_h^\rightarrow(t)=K^\rightarrow J_h(t),
 \qquad
 dB_h^\leftarrow(t)=K^\leftarrow J_h(t).              \tag{6}
\]

Every component in (6) is taken before evaluation and in its literal
grade.  In particular, (6) is strictly stronger than two equations
(K^\rightarrow H^\rightarrow=0) and
(K^\leftarrow H^\leftarrow=0) in unrelated restricted modules.

Adding (6) gives the promised construction:

\[
 E_h(t)=-\bigl(B_h^\rightarrow(t)+B_h^\leftarrow(t)\bigr)dt,
 \qquad
 dE_h(t)=(r-2q)J_h(t)dt.                              \tag{7}
\]

After the common carrier identifies
(J_h(t)=(q+tr)^{[n]}), (7) is exactly (1).  Thus existence of the
one-form needs no resultant, interpolation, or separate higher-moment
ansatz.  It needs one simultaneous coefficientwise common-carrier square.

## 3. One saturation condition controls all moments

Let (\mathcal L_h) be the set of simultaneous lifts satisfying (4)--(6)
and all the recorded physical faces.  Differences between lifts lie in the
vertical complex

\[
 \mathscr V_h=\ker\pi_h.                               \tag{8}
\]

Only a smaller part can affect the desired moment construction.  Let
(V_h^{\mathrm{mom}}\subseteq H(\mathscr V_h)) be the span of classes
([z]) for which a based polynomial one-form (z,d\eta(t)) is an
allowed difference of simultaneous physical lifts.  This definition
removes two unnecessary strengthenings:

1. one need not kill vertical homology which cannot occur between allowed
   lifts; and
2. one need not make reinsertion injective on unrelated source grades.

The relevant based polynomial space is

\[
 B_m=t(1-t)\mathbb K[t]_{\leq m-1}.                    \tag{9}
\]

Use the Rodrigues basis

\[
 \eta_j(t)=\frac{d^{j-1}}{dt^{j-1}}
               \bigl(t^j(1-t)^j\bigr),
 \qquad 1\leq j\leq m.                                \tag{10}
\]

Its moment matrix is

\[
 \Delta_{sj}=\int_0^1t^s,d\eta_j(t),
 \qquad
 \Delta_{sj}=0\ (s<j),
 \qquad
 \Delta_{jj}=(-1)^j\frac{(j!)^3}{(2j+1)!}\ne0.        \tag{11}
\]

Consequently

\[
 B_m\otimes V_h^{\mathrm{mom}}
   \longrightarrow (V_h^{\mathrm{mom}})^m,
 \qquad
 \eta\otimes z\longmapsto
 \left(\int_0^1t^s,d\eta\;z\right)_{s=1}^m          \tag{12}
\]

is an isomorphism.  This is the reason that a single saturation condition,
rather than (m) unrelated physical rows, is both necessary and
sufficient.

> **Theorem 3.1 (physical all-moment horizontal bridge).**  Suppose for a
> fixed (h\geq3):
>
> 1. the full decorated polynomial complexes and maps
>    (\pi_h,\chi_h) exist and commute with every restriction/insertion
>    face and with the (S)-action;
> 2. one simultaneous common-carrier lift (4)--(6) exists;
> 3. allowed lift differences are closed under multiplication by the based
>    polynomials (9); and
> 4. the moment-active saturation (2) holds.
>
> Then (7) is a source-valid polynomial one-form, and the chains
>
> \[
> e_s=\int_0^1t^sE_h(t),
> \qquad 0\leq s\leq m,                                \tag{13}
> \]
>
> have lift-independent homology classes and satisfy
>
> \[
> de_s=(r-2q)H_s=c_s,
> \qquad
> H_s=\int_0^1t^s(q+tr)^{[n]},dt.                      \tag{14}
> \]
>
> Conversely, under hypotheses 1--3, lift independence of all the moments
> in (13) implies (2).  It is enough to prove (2) by the single natural
> chain homotopy (3).

**Proof.**  Equation (7) follows by adding the two physical equations (6)
and using (5).  Weighted algebraic integration commutes with the source
differential, so (14) follows for one chosen lift.

Two lifts differ, modulo an ambient boundary and moment-invisible terms,
by

\[
 \sum_{j=1}^m z_j,d\eta_j(t),
 \qquad [z_j]\in V_h^{\mathrm{mom}}.                   \tag{15}
\]

After common-carrier desuspension, the (s)-th moment change is

\[
 \sum_{j=1}^m\Delta_{sj}
       \bigl[(r-2q)\chi_h(z_j)\bigr].                  \tag{16}
\]

Condition (2) makes every term in (16) zero in (H(Q_h)).  Conversely,
if all higher moment changes vanish, invertibility of (\Delta) in (11)
forces ([(r-2q)\chi_h(z_j)]=0) for every allowed coefficient class.
This is (2).  Finally (3) supplies explicit boundaries uniformly before
integration, so it implies (2).  \(\square\)

At (h=3), this theorem is already nonvacuous: (m=1),
(\eta_1=t(1-t)), and the unique residue is (-1/6).  For (h\geq4),
the same theorem supplies the entire initial tower
(s=0,\ldots,h-3).  No induction in (s) is needed.

For a finite complete decorated presentation, (2) is an ordinary exact
rank test.  Let

\[
 D_{Q,h}:B_{Q,h}\longrightarrow Z_{Q,h}               \tag{16a}
\]

be the full boundary matrix in the carrier degree, including every
protected, target, anchor, terminal, and physical-(q) row.  Choose cycle
columns (Z_h^{\mathrm{mom}}) representing
(V_h^{\mathrm{mom}}), and put

\[
 L_h=(r-2q)\chi_h Z_h^{\mathrm{mom}}.                  \tag{16b}
\]

Then (2) is equivalent to

\[
 \boxed{
 \operatorname {rank}D_{Q,h}
   =\operatorname {rank}[D_{Q,h}\mid L_h].}            \tag{16c}
\]

If (16c) fails, exact finite-dimensional duality gives a column (z) and
a covector (\lambda) with

\[
 \lambda D_{Q,h}=0,
 \qquad
 \lambda L_hz\ne0.                                    \tag{16d}
\]

Only when (D_{Q,h}) is the complete decorated physical boundary matrix
does (\lambda) become a physical terminal/Fredholm separator.  On a
truncated chart packet it is only a separator for that presentation.

## 4. Downstream all-(h) closure

The Hilbert--Cauchy theorem proves

\[
 \operatorname {span}\{u_h,qc_s,rc_s:0\leq s\leq m\}=V_h,      \tag{17}
\]

with the certified clean orientation

\[
 u_h=\sum_{j=2}^h q^{[h-j]}r^{[j]},
 \qquad
 x_h=q^{[h]}+q^{[h-1]}r.                              \tag{18}
\]

Thus if the clean physical row gives (u_h=0), Theorem 3.1 gives all
(c_s=0) in the same (S)-module, and the exceptional class (x_h) is
retained there, then legal multiplication by (q,r) makes (x_h=0).
This is the complete scalar-unit moment transfer at every height.  The
remaining contradiction still requires the separately certified statement
that the physical exceptional class is nonzero in that same decorated
quotient.

The importance of using one full decorated (S)-module is exactly that
(17) is not permission to multiply evaluated four-cut coefficients.  The
products (qc_s,rc_s) must be physical operations commuting with the same
differential and faces used in (6).

## 5. The exact physical overlap kernel

The overlap obstruction is already visible in the literal four-site
matching formulas.  For four exposed sites (p,q,r,s), the two overlapping
pair charts have common normal and double rows.  With the notation of the
physical curvature-square identity,

\[
 \Delta=At-By,
 \qquad
 \kappa=AU-BF,                                          \tag{19}
\]

their two presentations of the same target row differ by

\[
\begin{aligned}
 \beta_k={}&(\Delta v+\kappa z)z^{[k-1]}
        +\Delta zvz^{[k-2]}\\
 &\quad-k\bigl(\kappa z^{[k]}+\Delta vz^{[k-1]}\bigr).
                                                               \tag{20}
\end{aligned}
\]

Here the scalar-unit alignment is (k=h-1\geq2).  The physical matching
rules

\[
 zz^{[k-1]}=kz^{[k]},
 \qquad
 zz^{[k-2]}=(k-1)z^{[k-1]}                             \tag{21}
\]

give (\beta_k=0) for every (k\geq2), hence for every (h\geq3).  This is
not an artificial module
relation: it is the exact Bianchi/exchange cancellation between the two
overlapping physical pair charts.

There are nevertheless two different meanings of this zero.

* After reinsertion/evaluation, the two chart presentations are the same
  physical target row, so their difference is zero.
* In the decorated presentation module, the (pq)-chart and (pr)-chart
  generators retain different pair and star-role tags.  Their difference
  is a nonzero kernel cycle until a source-valid chart-change two-cell is
  supplied.

Writing the two tagged presentations as (e_{pq},e_{pr}), the minimal
linear shadow is

\[
 \pi_h(e_{pq})=\pi_h(e_{pr}),
 \qquad
 \beta_h^{\mathrm{tag}}=e_{pq}-e_{pr}\in\ker\pi_h.     \tag{22}
\]

Equation (20) proves that (22) has literal physical provenance and that the
cross-pair restriction/reinsertion square commutes.  It does **not** prove

\[
 \beta_h^{\mathrm{tag}}=d\Gamma_h
 \quad\text{or}\quad
 [(r-2q)\chi_h(\beta_h^{\mathrm{tag}})]=0.              \tag{23}
\]

If the second class in (23) is nonzero, then the physical-provenant based
loop

\[
 \beta_h^{\mathrm{tag}},d\eta_j(t)                    \tag{24}
\]

fixes both endpoints, has zero unweighted integral, and preserves the
literal overlap square, but changes the higher moments by

\[
 \Delta_{sj}[(r-2q)\chi_h(\beta_h^{\mathrm{tag}})].     \tag{25}
\]

Since (\Delta) is invertible, the overlap square alone cannot force all
these changes to vanish.  The missing physical statement is precisely a
Bianchi/exchange contraction (\Gamma_h), natural in the affine parameter
and all remaining faces, whose desuspension realizes (3).

## 6. What the counterguard does and does not instantiate

The counterguard in Section 5 is more physical than the coefficientwise
filtered-DGM torsor in three precise respects.

1. Its vertical generator is the difference of two literal overlapping
   pair presentations of one four-cut row.
2. Its vanishing after reinsertion is the exact matching identity
   (20)--(21), not a declared evaluation-kernel relation.
3. It satisfies a physically meaningful cross-pair square: both charts
   restrict and reinsert to the same four-site target polynomial.

It stops exactly where the current source theory stops.  It is a
**one-square decorated presentation packet**, not an exact finite GHZ
tensor.  In particular, it does not provide:

* a global aggregate satisfying all (3^{2h}) output words;
* the normalized pure target rows for all three labels;
* the complete word/fine/repeated, anchor, terminal, protected, and
  physical-(q) faces;
* a proof that the tagged exchange survives after every such face and
  every higher source cell is included; or
* a physical desuspension (\chi_h) with nonzero value on that class.

Therefore (24) is a counterguard to an **inference from the presently
proved overlap/four-cut identities**, not a physical counterexample to the
conjecture.  A full decorated source may kill the exchange class.  If it
does, the killing cell is exactly the positive datum required by (3).

## 7. The shortest source attack

The horizontal bridge should now be attacked in the following order.

1. Build the coefficientwise common-carrier square (6) in the complete
   ordered four-star module.  This constructs (1) by addition; do not first
   seek the moments separately.
2. Retain the chart tags and construct one physical Bianchi/exchange
   two-cell (\Gamma_h) comparing the two oriented presentations before
   evaluation.
3. Prove that these exchange cells generate the moment-active kernel, or
   separately kill the non-exchange vertical complement.
4. Verify the single homotopy identity (3).  The Rodrigues isomorphism then
   promotes it automatically to every (s\leq m).
5. Apply the Hilbert--Cauchy span only inside that same decorated
   (S)-complex, with the exceptional target retained.

Step 3 is the only possible remaining enlargement of the hypothesis.  If
the physical moment-active kernel contains witness exchanges or non-pure
cycles not generated by the two-chart Bianchi cells, their
((r-2q)\chi_h)-images must also be nullhomotoped.  Merely adding more
evaluated four-cut rows cannot see them, because they already lie in the
kernel of the complete face/reinsertion readout used to define them.

## Verification

Run

```text
python3 computations/verify_uniform_physical_horizontal_moment_saturation_bridge.py
python3 -O computations/verify_uniform_physical_horizontal_moment_saturation_bridge.py
python3 -I -S computations/verify_uniform_physical_horizontal_moment_saturation_bridge.py
```

The dependency-free checker pins the common-carrier, first-moment,
all-moment torsor, Hilbert--Cauchy, physical curvature-square, and adjacent
full-nine ledgers.  It verifies for (3\leq h\leq24) the sign in (5), the
moment denominators, the triangular residues (11), and their full rank.  It
also verifies (20)--(21) for (2\leq k\leq24) and the nonzero chart-tagged
kernel (22).  Those finite checks audit uniform rational formulas.  They do
not construct the full decorated complexes, the common carrier, the
desuspension, or the saturation homotopy.
