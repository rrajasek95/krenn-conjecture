# The scalar-unit Hermite interpolant fixes every top-suspended moment

## 1. Outcome

Work over a characteristic-zero field in the intrinsic scalar-unit chart
on \(2h\) residual sites, \(h\geq3\).  Normalize

\[
 Q=\alpha q,\qquad R=R_{aa},\qquad n=h-2.
\tag{1}
\]

After multiplying the nine literal rows by \(\alpha^{h-1}\), they are

\[
 \delta_{ia}\delta_{ja}Q^{[h]}+R_{ij}Q^{[h-1]}
       =\alpha^{h-1}\delta_{ij}X_i,
 \qquad R_{ij}=p_i s_j.                                  \tag{2}
\]

On the clean unary branch, define the literal polynomial interpolants

\[
 P(t)=(Q+tR)^{[h]},\qquad
 S_{jk}(t)=R_{jk}(Q+tR)^{[h-1]}.                         \tag{3}
\]

These are polynomials in the fixed source coefficients.  They are not
asserted to be exact sources for intermediate values of \(t\).

The exceptional row and unary cleanliness give the exact Hermite
condition

\[
 \boxed{P(1)=P(0)+P'(0)=\alpha^{h-1}X_a.}               \tag{4}
\]

More importantly, differentiation of the literal response interpolant gives

\[
 \boxed{
 S'_{jk}(t)=R_{jk}R(Q+tR)^{[n]}
            =R_{ja}R_{ak}(Q+tR)^{[n]}.}                 \tag{5}
\]

The second equality is the source-level Segre identity; it retains the
ordered endpoint factors

\[
 (p_js_a)(p_as_k)=(p_js_k)(p_as_a).                     \tag{6}
\]

Thus the affine interpolant removes one apparent ambiguity.  Put

\[
 H_s=\int_0^1t^s(Q+tR)^{[n]},dt
     =\sum_{\ell=0}^{n}{1\over s+\ell+1}
          Q^{[n-\ell]}R^{[\ell]}.                       \tag{7}
\]

Then, uniformly for every \(s\geq0\),

\[
 \boxed{
 \int_0^1t^sS'_{jk}(t)\,dt=R_{ja}R_{ak}H_s.}           \tag{7a}
\]

This is a literal polynomial identity even though (3) is not an
exact-source family.  At \(s=0\), endpoint evaluation also gives

\[
 \boxed{
 S_{jk}(1)-S_{jk}(0)=R_{ja}R_{ak}H_0
                    =R_{jk}\Theta_a.}                  \tag{8}
\]

Here \(H_0\) is exactly the full-normal-jet carrier \(H_a\), in the
normalization (1), and not merely its leading associated-graded term.
Equations (7a)--(8) canonically fix the entire four-star
**top-suspended moment tower** \(R_{ja}R_{ak}H_s\), including
\(R_{ja}R_{ak}H_a\) at \(s=0\).  They do not desuspend the four star
factors inside one lower carrier complex.  There is no reparameterization
or based-loop ambiguity in the literal top polynomial
\(S'_{jk}(t)\) itself.

The remaining construction problem occurs one level lower.  A
four-/five-site comparison would have to lift (5) through an ordered
restriction--insertion map before taking the target nullhomotopy or odd
quotient.  If such a carrier complex, map, and class of allowed lifts are
specified, then any surviving vertical class in the kernel can be
multiplied by

\[
                         \eta(t)=t(1-t)                 \tag{9}
\]

without changing (2)--(8), even pointwise after reinsertion.  It would
leave the unweighted suspended lift unchanged but shift the first weighted
suspended lift by exactly \(-1/6\) times that class.  Consequently the
Hermite interpolant fixes every target-side \(H_s\) and its top suspension,
but the nine rows and the Segre derivative neither construct the required
horizontal desuspension nor prove that its vertical homology vanishes.

The first extra row in the canonical initial-moment program, once such a
complex is constructed, is a source-valid desuspended lift of

\[
 R_{ja}R_{ak}H_1
   =\int_0^1tS'_{jk}(t)\,dt
   =S_{jk}(1)-\int_0^1S_{jk}(t)\,dt,                    \tag{10}
\]

together with vanishing of its vertical residue.  Equation (10), rather
than endpoint differentiation alone, is the formula in which \(H_1\)
enters.  For \(h=3\) it is already algebraically indispensable in the
certified initial moment tower; Section 4 gives an explicit identity.

This is an exact top-suspension theorem together with a conditional lift
obstruction, not a physical matching counterexample.  It does not construct
a nonzero physical vertical class and does not rule out a source-specific
saturation theorem which kills every such class.  Krenn's conjecture
remains open.

## 2. The literal Hermite and Segre calculations

The divided-power binomial formula gives

\[
 P(t)=\sum_{k=0}^{h}t^kQ^{[h-k]}R^{[k]},\qquad
 P'(t)=R(Q+tR)^{[h-1]}.                                 \tag{11}
\]

The clean unary equation is

\[
 \sum_{k=2}^{h}Q^{[h-k]}R^{[k]}=0.                     \tag{12}
\]

Subtracting \(P(0)+P'(0)\) from \(P(1)\) gives exactly the
left side of (12), proving (4).  No matching power is cancelled.

Similarly,

\[
 S_{jk}(t)=\sum_{k=0}^{h-1}t^k
       R_{jk}Q^{[h-1-k]}R^{[k]}.                        \tag{13}
\]

Differentiating (13) and using
\(R R^{[k-1]}=kR^{[k]}\) proves the first equality in (5).
The literal factorization \(R_{jk}R_{aa}=R_{ja}R_{ak}\) proves the
second.  Integrating (5), then using (7), proves (8).  Weighted
integration and integration by parts give (10).

All nine values at the original endpoint are fixed by (2):

\[
 S_{jk}(0)=\alpha^{h-1}\delta_{jk}X_j
             -\delta_{ja}\delta_{ka}Q^{[h]}.           \tag{14}
\]

Any additional exact pivot hypothesis may also fix some or all values at
\(t=1\).  The obstruction below preserves both endpoints, whatever those
fixed values are.

## 3. Conditional loop calculation in a proposed source lift

Assume that \(\widetilde{\mathscr C}^{(4)}_{jk}\) is a specified ordered
four-site carrier complex: its summands remember the four star roles
\((p_j,s_a,p_a,s_k)\), their physical sites and colours, and the
remaining carrier complement.  Let

\[
 \pi_{jk}:\widetilde{\mathscr C}^{(4)}_{jk}
       \longrightarrow({\cal A}_{2h})_{jk}              \tag{15}
\]

be a chain map given by star-weighted reinsertion into the literal top
response tensor.  Assume also that a horizontal construction has chosen an
allowed polynomial one-form
\(\widetilde\sigma_{jk}(t)\,dt\) whose image is the fixed form
\(S'_{jk}(t)\,dt\) in (5).  Let \(z\) be a cycle in the same ordered
\((j,a,a,k)\) source summand with

\[
                         \pi_{jk}(z)=0.                  \tag{16}
\]

Suppose adding a based vertical one-form is allowed in this lift class,
and define another lifted one-form by

\[
 \widetilde\sigma^{\,z}_{jk}(t)\,dt
   =\widetilde\sigma_{jk}(t)\,dt+z\,d\eta(t).            \tag{17}
\]

Because \(\pi_{jk}(z)=0\), (17) has the same pointwise top image:

\[
 \pi_{jk}\bigl(\widetilde\sigma^{\,z}_{jk}(t)\,dt\bigr)
     =S'_{jk}(t)\,dt.                                   \tag{18}
\]

If the one-form is recorded by a polynomial primitive, that primitive
changes by \(\eta(t)z\).  Since \(\eta(0)=\eta(1)=0\), both endpoint
values are unchanged.  The Hermite interpolant \(P(t)\) is untouched.
Hence the two proposed lifts have identical top images and endpoints; in
particular none of the literal equations (2)--(8) distinguishes them.

The two first moments of the lift difference are nevertheless

\[
 \begin{aligned}
 \int_0^1 z\,d\eta&=0,\\
 \int_0^1 t z\,d\eta
   &=\left(\int_0^1t(1-2t)\,dt\right)z
     =-{1\over6}z.                                      \tag{19}
 \end{aligned}
\]

More generally, for \(s\geq1\),

\[
             \int_0^1t^s\,d\eta
                  =-{s\over(s+1)(s+2)}.                \tag{19a}
\]

Thus, if \([z]\ne0\) survives in the homology of the proposed physical
kernel, the
unweighted top suspension in (8) is fixed while the weighted four-site
lift in (10) is not.  This is not an ambiguity of the target-side
polynomial \(H_1\) in (7); it is a conditional ambiguity in the proposed
source-complex lift.

For such a specified complex, the map which first sees the shift is the
relative first-moment residue

\[
 \boxed{
 \operatorname {Res}_1:
  dB_1\otimes H(\ker\pi_{jk})
      \longrightarrow H(\ker\pi_{jk}),\qquad
 d\eta\otimes[z]\longmapsto-{1\over6}[z],}              \tag{20}
\]

where \(B_1=t(1-t)\mathbb K\) is the smallest based-loop space.  This
formal map is nonzero whenever the displayed vertical class survives; the
present note proves neither that the physical complex exists with these
properties nor that such a class survives.

To enter the Hilbert--Cauchy carrier argument one needs an additional
chain map

\[
 \chi_{jk}:\widetilde{\mathscr C}^{(4)}_{jk}
       \longrightarrow {\mathscr Q}_{h-2}               \tag{21}
\]

which desuspends/reassembles the ordered four-site lift into one common
carrier module and permits multiplication by \(R-2Q\), then by \(Q,R\).
Only after (21) has been constructed is the relevant obstruction map
well typed:

\[
 \boxed{
 \mathfrak o_1([z\,d\eta])
    =-{1\over6}\bigl[(R-2Q)\chi_{jk}(z)\bigr].}          \tag{22}
\]

Its two degree-\(h\) prolongations are obtained by multiplication by
\(Q\) and \(R\) in \({\mathscr Q}\).  Zero indeterminacy at the first new
moment is the vanishing of (22), modulo literal boundaries, for every
allowed vertical cycle.  Relative saturation of (15), or the weaker
statement \(H(\chi_{jk})(\ker H(\pi_{jk}))=0\), is sufficient.
The nine endpoint rows are equations after reinsertion; they neither
construct (21) nor prove this kernel vanishing.

## 4. Why the first weighted row is not optional at \(h=3\)

For \(h=3\), write

\[
 \begin{aligned}
 u&=QR^{[2]}+R^{[3]},&
 x&=Q^{[3]}+RQ^{[2]},\\
 H_0&=Q+\tfrac12R,&
 H_1&=\tfrac12Q+\tfrac13R,\\
 c_s&=(R-2Q)H_s.
 \end{aligned}                                         \tag{23}
\]

Direct divided-power multiplication gives

\[
 \boxed{
 x={7\over20}u+{43\over60}Qc_0-{7\over60}Rc_0
                       -{8\over5}Qc_1.}                 \tag{24}
\]

On the other hand,

\[
 x\notin\operatorname {span}\{u,Qc_0,Rc_0\}.          \tag{25}
\]

Thus the first weighted relation \(c_1=0\) is exactly what completes the
smallest scalar-unit carrier argument.  Equations (19) and (22) show that
any proposed source lift must rule out the displayed vertical ambiguity.
For higher
\(h\), \(H_1\) is the first new member of the certified initial tower;
this note does not claim setwise minimality of every moment index.

## 5. The catalecticant class is not the torus--Koszul middle coefficient

The audited catalecticant identity

\[
 \sum_{e,f}q_f\nu(efq^{[h-2]})
       (K_e^\rightarrow+K_e^\leftarrow)=-(h-1)E_{ii}   \tag{26}
\]

does detect one nonzero oriented adjacent-power coefficient.  It is not
literally the missing middle coefficient in the inactive
\(\Omega\)-route.

There are three exact type differences.

1. The indices \(e,f\) in (26) are decorated physical cells and \(q_f\)
   is one internal-cell coefficient.  The variables \(t,u\) in the
   torus--Koszul middle monomial \((tu)^{h-2}\) are cap-line parameters,
   not those cells and not the affine interpolation parameter in (3).
2. Equation (26) is evaluated in even top degree and has value in the
   endpoint-colour matrix space.  The routed middle coefficient lies in
   the odd quotient
   \({\cal R}_{2h-1}/({\cal R}_1q_0^{[h-1]})\).
   No deletion/reinsertion map from the former functional to the latter
   class has been constructed.
3. The nonzero target unit remains on the right of (26).  The
   \(\Omega\)-route needs a target-nullhomotoped response class before
   taking the middle coefficient.  Choosing one nonzero summand of (26)
   supplies neither that nullhomotopy nor the zero-indeterminacy (22).

Under the proposed lift hypotheses of Section 3, the loop (17) illustrates
the type gap: it leaves the whole evaluated identity (26) and the pointwise
top polynomial (5) unchanged while changing the first source moment by
(19).  This is not an exhibited physical ambiguity.  A positive
identification still requires an additional filtered map which transports
the target unit to the routed odd class and kills (22).  Equation (26)
alone is an evaluated shadow of such a map.

## 6. Audit and scope

The dependency-free checker
[`verify_scalar_unit_hermite_source_path_first_moment_lift_obstruction.py`](../computations/verify_scalar_unit_hermite_source_path_first_moment_lift_obstruction.py)
audits the divided-power Hermite remainder, the derivative and moment
formulas, the ordered Segre square, the formal loop residues, (24)--(25),
and deterministic normalization mutations.  It runs under ordinary and
optimized Python.  It does not construct the proposed complex, chain maps,
allowed lift class, or a surviving physical vertical cycle.

The new conclusion is deliberately narrow.  The literal affine
interpolant supplies every canonical top-suspended \(H_s\)-carrier.  What
is missing is construction of the source-complex
first-moment/nullhomotopy row and either a relative-saturation theorem or
a direct proof that every allowed vertical class has zero image under
(22).  No active clean cap or proof of Krenn's conjecture follows here.
