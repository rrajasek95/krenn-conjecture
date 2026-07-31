# The adjacent (h=3) source-grade packet leaves an independent sum channel

## 1. Outcome

The named adjacent-chart source rows do not imply

\[
             F_0\Psi_C=\chi_C(AU-BF).                    \tag{1}
\]

There is an exact rational direct-sum/source-grade packet with compatible `pq` and
`pr` selector words, three nonzero labelled four-cut anchor defects, a
zero cycle-projected crossed row, and both complete Euler cancellations,
for which

\[
                    F_0\Psi_C=0,
        \qquad \chi_C(AU-BF)=1.                          \tag{2}
\]

After the anchor reconstruction is retained, the presentation matrix has
rank five.  Adjoining (1) raises its rank to six.  Even granting the
second adjacent curvature and its crossed difference leaves the common
curvature mode free.  Within this presentation, adjoining the grade-split
sum-channel relation would remove that common mode:

\[
 \boxed{
       F_0\Psi_C={\chi_C\over2}(\kappa_H+\kappa_G).}     \tag{3}
\]

The natural opposite-shore comparison does not produce (3).  The
`rs` to `sq` presentation has the same curvature/direct-double splitting
as `pq` to `pr`; their difference cancels both high components, and their
sum doubles both.  Adding the third diagonal target direction and keeping
the assignment tables as literal shared-column outer products also leaves
the sum class nonzero.

This is a sharp obstruction for the displayed linear source-grade packet,
not a counterexample to a complete all-label Krenn source.  A complete
physical coefficient cut could still supply (3).  The lowest
response-degree algebraic candidate exposed by this packet is the
assignment-sum expression

\[
                       2M_0-M_H-M_G,                    \tag{4}
\]

but \(2M_0-M_H-M_G\) is not an admitted source row by itself: the known
source identity pairs it with its internal curvature mate.  On the
rootless (h=3) line, the lowest nonlinear response-degree coefficient
beyond the static third anchor is the exceptional diagonal residual

\[
              [X_2]\bigl(\alpha R^{[2]}q+R^{[3]}\bigr). \tag{5}
\]

No existing row is known to identify (4) or (5) with the anchor-cycle
class.  The complete physical question therefore remains open.

## 2. One compatible adjacent selector word

Use exposed sites `p,q,r,s` and four common sites
`d0,d1,d2,d3`.  The single global physical-label word

\[
\begin{array}{c|cccccccc}
\text{site}&p&q&r&s&d_0&d_1&d_2&d_3\\ \hline
\text{label}&0&1&1&2&0&0&1&2
\end{array}                                               \tag{6}
\]

restricts in the displayed orders to

\[
\begin{aligned}
 (d_0,d_1,r,d_2,s,d_3)&\longmapsto001122
                                      &&\text{in the `pq` chart},\\
 (d_0,d_1,q,d_2,s,d_3)&\longmapsto001122
                                      &&\text{in the `pr` chart}.
\end{aligned}                                             \tag{7}
\]

Thus both selectors are separating, use the same physical labels, and
retain the same ordered common word.  The exposed word is `0112`, so its
four-index target coefficient is literally zero.  This is a global word
compatibility check, not an independent relabelling of the two charts.

## 3. All three labelled anchor defects are necessary

On six selector sites take the scalar quadratic

\[
 q=01+02+04+05+12+14+23+34+35
\]

and the Hessian-kernel tangent

\[
                              z=01-13.                  \tag{8}
\]

Direct matching enumeration gives

\[
 F_0=\operatorname {Haf}_6(q)=4,
 \qquad
 H_\times=
 \begin{pmatrix}
 0&1&2\\0&2&2\\1&1&1
 \end{pmatrix},
 \qquad a=-{1\over4}H_\times.                          \tag{9}
\]

Use the two selector connections

\[
 X=\begin{pmatrix}1&1&-2\\1&1&-2\\1&1&-2\end{pmatrix},
 \qquad
 Y=\begin{pmatrix}
 5/2&10&25/2\\0&0&0\\-1/2&-2&-5/2
 \end{pmatrix}.                                        \tag{10}
\]

They satisfy

\[
                 X^{\mathsf T}H_\times+H_\times Y=0,
 \qquad X^{\mathsf T}a+aY=0.                           \tag{11}
\]

The three raw labelled four-cut defects are

\[
\begin{aligned}
\Delta_0&=
 \begin{pmatrix}-7/2&-10&-25/2\\-1&0&0\\2&0&0\end{pmatrix},\\
\Delta_1&=
 \begin{pmatrix}0&-1&0\\0&-1&0\\0&2&0\end{pmatrix},\\
\Delta_2&=
 \begin{pmatrix}0&0&-1\\0&0&-1\\1/2&2&9/2\end{pmatrix}.
                                                               \tag{12}
\end{aligned}
\]

The division-free anchor reconstruction gives

\[
 \Phi(\Delta,a)=
 \begin{pmatrix}
 0&0&3/2\\0&0&3/2\\-3/4&-3/4&0
 \end{pmatrix}.                                        \tag{13}
\]

For the oriented colour cycle (0 to 1 to 2 to 0), define

\[
 \Psi_C=
 a_{12}a_{20}\Phi_{01}
 +a_{20}a_{01}\Phi_{12}
 +a_{01}a_{12}\Phi_{20}.                               \tag{14}
\]

Retaining only one labelled defect at a time gives the three contributions

\[
                    -{9\over64},\qquad
                    -{3\over32},\qquad
                     {15\over64}.                       \tag{15}
\]

Every contribution is nonzero and their sum is zero.  Hence none of the
three anchors may be deleted generically, while

\[
                    \Psi_C=0,
      \qquad F_0\Psi_C={\cal H}^{(3)}_C(\Lambda)=0.     \tag{16}
\]

This is a nonvacuous cycle cancellation: the individual frame defects do
not vanish.

## 4. The oriented Bianchi and Euler packet

Work in the site-square-zero algebra on four common-complement sites and
put

\[
        z=e_0e_1+e_2e_3,qquad t=e_0,qquad v=e_1,
        \qquad x=y=0.                                   \tag{17}
\]

Then

\[
                    z^{[2]}=e_0e_1e_2e_3,
             \qquad \chi_C=[e_0e_1e_2e_3]z^{[2]}=1.    \tag{18}
\]

Select the direct coefficient

\[
 A=a_{01}=-{1\over4},qquad
 U=-4,qquad B=C=E=F=0.                                 \tag{19}
\]

Thus

\[
                      \kappa=AU-BF=1,
       \qquad \delta=At-By=-{1\over4}t.                \tag{20}
\]

The literal (h=3) connection, normal, curvature, and direct-double
identities have the oriented signs

\[
\begin{aligned}
 P_{pq}t-P_{pr}y&=\delta z,\\
 L_{pq;r}-L_{pr;q}&=-2\delta,\\
 UP_{pq}+tL_{pq;s}-FP_{pr}-yL_{pr;s}
     &=\delta v+\kappa z,\\
 M_{pq;rs}-M_{pr;qs}&=-2\kappa .                       \tag{21}
\end{aligned}
\]

Before cancelling any power, their adjacent-power ledger is

\[
 \boxed{
 \kappa\bigl(zZ_1-2Z_0\bigr)
 +\delta v\bigl(zZ_2-Z_1\bigr)=0,}
 \qquad
 Z_0=z^{[2]},\quad Z_1=z,\quad Z_2=1.                  \tag{22}
\]

The coefficient of the top word in the curvature/direct-double pair is

\[
                              (2,-2),                   \tag{23}
\]

and the same coefficient in the connection/normal pair is

\[
                         (-1/4,+1/4).                   \tag{24}
\]

Both pairs are nonzero literal Euler boundaries.  Their evaluated sum is
zero; neither boundary identifies its curvature component with (16).

## 5. Exact rank obstruction

Let

\[
 (\Theta,\Xi,\kappa,C,D,L,N)                           \tag{25}
\]

denote respectively the anchor cycle (F0 Psi_C), the cycle-projected
crossed coefficient, the oriented curvature, and the curvature, direct,
connection, and normal top components.  With (chi_C=1), the displayed
source-grade presentation has rows

\[
 R=
 \begin{pmatrix}
 1&-1&0&0&0&0&0\\
 0& 1&0&0&0&0&0\\
 0& 0&-2&1&0&0&0\\
 0& 0& 2&0&1&0&0\\
 0& 0& 0&0&0&1&1
 \end{pmatrix}.                                        \tag{26}
\]

The first row is anchor-cycle reconstruction, the second is the crossed
target-zero row, the next two retain the two high Euler components, and
the last is the low Euler boundary.  The evaluated high row
`C+D=0` and the evaluated total boundary are already in the row span.

The proposed transgression is the row

\[
                         T=(1,0,-1,0,0,0,0).            \tag{27}
\]

Exact rational elimination gives

\[
                       \operatorname {rank}R=5,
            \qquad \operatorname {rank}\binom RT=6.   \tag{28}
\]

The separating witness is

\[
                    w=(0,0,1,2,-2,-1/4,1/4).           \tag{29}
\]

Every retained row kills w, while T(w)=-1.  This proves the failure of
(1) in the stated presentation without division.

There is a useful stronger audit.  Grant two adjacent curvatures
\(\kappa_H,\kappa_G\), their complete high Euler pairs, and the crossed
difference \(\kappa_H-\kappa_G=0\).  On coordinates

\[
        (\Theta,\kappa_H,\kappa_G,D_H,C_H,D_G,C_G),     \tag{30}
\]

the five presentation rows have rank five, whereas
\(\Theta-\chi_C\kappa_H\) raises the rank to six.  The witness

\[
                         (0,1,1,-2,2,-2,2)              \tag{31}
\]

shows that the crossed row controls only the difference channel.  The
free common curvature is exactly the sum channel (3).

## 6. Opposite-shore comparison is an identical splitting

For the original exposed order use

\[
 (A,B,C,E,F,U;x,y,t,v).
\]

The opposite-shore relabelling

\[
 (p,q,r,s)\longmapsto(s,r,q,p)
\]

sends the data to

\[
 (U,F,C,E,B,A;v,t,y,x).                                 \tag{32}
\]

Its curvature is therefore

\[
                         UA-FB=AU-BF=\kappa.            \tag{33}
\]

At (h=3), the two raw direct-double coefficients in the first
presentation are

\[
\begin{aligned}
 M_{pq;rs}&=3(BF+EC)+AU,\\
 M_{pr;qs}&=3(AU+EC)+BF.                                \tag{34}
\end{aligned}
\]

The opposite presentation gives literally

\[
\begin{aligned}
 M_{rs;pq}&=3(FB+EC)+UA=M_{pq;rs},\\
 M_{sq;rp}&=3(UA+EC)+FB=M_{pr;qs}.                      \tag{35}
\end{aligned}
\]

Thus both filtered representatives contain the same high pair

\[
                         \kappa(zz-2z^{[2]}).           \tag{36}
\]

Their lower coefficients are different,

\[
              \delta v=(At-By)v,
       \qquad \delta' x=(Uy-Ft)x,                       \tag{37}
\]

but both occur only in the low boundary `coefficient times (z-z)`.
Consequently subtraction cancels (36) as well as its direct mate; addition
doubles both.  In any linear combination, vanishing of the direct high
component forces vanishing of the curvature high component.  Comparing
the two raw extractions therefore provides no grade split.

This remains visible after static selector normalization.  Embed the
integral two-label sum-channel guard in three labels by

\[
 d=\begin{pmatrix}1&1&0\\1&2&0\\0&0&1\end{pmatrix},
 \qquad
 c=\begin{pmatrix}0&1&0\\1&2&0\\0&0&1\end{pmatrix}.   \tag{38}
\]

At the first physical label let

\[
 H=d_{\bullet0}c_{\bullet0}^{\mathsf T},
 \qquad G=d_{\bullet0}c_{\bullet0}^{\mathsf T},
 \qquad B_{\rm sum}=H+G.                               \tag{39}
\]

These are literal shared-column outer products.  With

\[
                  \omega_d(Z)=Z_{01}-Z_{10},            \tag{40}
\]

one has

\[
 \omega_d(E_{00})=\omega_d(E_{11})=\omega_d(E_{22})
 =\omega_d(d)=\omega_d(H-G)=0,
 \qquad \omega_d(B_{\rm sum})=2.                       \tag{41}
\]

The three direct-double tables have omega-values (6,4,4), so

\[
          \omega_d(2M_0-M_H-M_G)=4\ne0.                \tag{42}
\]

On the opposite selector chart the assignment sum is

\[
 c_{\bullet0}d_{\bullet0}^{\mathsf T}
 +d_{\bullet0}c_{\bullet0}^{\mathsf T}=c-E_{22},       \tag{43}
\]

which is zero modulo the diagonal matrices plus the new direct matrix
\(c\).  Hence the opposite chart supplies another difference-channel
normalization, not the missing class (42).

Equation (38)--(43) includes the third diagonal direction and exact static
Segre outer products.  It is a selector-family/source-grade guard, not a
complete site-square-zero full-nine source.  It proves that the third
anchor and shared-star factorization do not force (3) at the static linear
level.

## 7. Lowest response-degree candidates for the missing class

Equation (42) exposes an algebraic sum-channel candidate.  At general h,

\[
       2M_0-M_H-M_G=-(h-1)(K_H+K_G).                   \tag{44}
\]

For h=3 its right side is `-2` times the curvature sum.  The expression
\(2M_0-M_H-M_G\) is not admitted separately: the known source object is the
total Euler boundary, which pairs (44) with the negative internal
curvature component.  A positive proof would have to construct and admit
a literal grade-preserving coefficient comparison that leaves the left
side of (44) after its normal and internal companions have been cancelled,
and then identify it with the anchor cycle.

The rootless h=3 calculation identifies the lowest nonlinear
response-degree coefficient displayed by this expansion that could
perform that task.  For an off-diagonal direct coefficient alpha, response
quadratic R, and internal quadratic q, the top row is

\[
                       \alpha q^{[3]}+Rq^{[2]}=0.       \tag{45}
\]

Before any cancellation,

\[
 (\alpha q+R)^{[3]}
 =\alpha^2(\alpha q^{[3]}+Rq^{[2]})
    +\alpha R^{[2]}q+R^{[3]}.                          \tag{46}
\]

Thus the static row (45) removes only the first two layers.  At the
exceptional third target, the remaining nonlinear candidate is (5).  The
audited binary-cycle construction has this coefficient equal to one.  That
construction omits the literal shared-star factorization before the X2
diagonal equation; this ordering does not establish universal minimality.
Conversely, (38)--(43) show that merely adding an abstract E22 anchor and
static outer-product tables does not kill the class.

Therefore the unresolved physical assertion is sharply local:

> Use the complete X2 diagonal row together with the literal shared-star
> rectangles and the two chart extractions to show that (5) gives a
> grade-preserving representative of (42), or show by a complete physical
> guard that it need not.

No current identity proves this assertion.  In particular, the static
third anchor itself is diagonal and is annihilated by omega_d; only its
line-dependent nonlinear coefficient can see beyond the sum-channel
guard.

### 7.1 A selected-cross detector in one support fibre

There is a precise distinction between detecting the missing carrier and
proving the transgression.  For every residual colour word omega, the
literal nine fixed-block rows assemble into the cohafnian identity

\[
 P_\omega^{\mathsf T}H(Q_\omega)S_\omega
      =D_\omega-\operatorname {haf}(Q_\omega)a.         \tag{47}
\]

Here \(D_\omega\) is \(E_{cc}\) on the constant word \(c^6\) and is zero
on a mixed word.
The (i,j)-entry of (47) is exactly the all-word coefficient of
\(R_{ij}q^{[2]}\).  Consequently a selected-cross mixed-word entry is a
natural lowest-response-degree candidate for coupling a pure diagonal
anchor to the shared physical star carrier.  It is first order in the
response.  The root coefficient (5) is second and third order, so one
arbitrary mixed-word instance of (47) cannot by itself force (5) to vanish.

There is an exact one-word guard for this degree distinction.  Take the
six-by-six scalar internal matrix with every off-diagonal entry one.  Its
hafnian is 15 and every off-diagonal cohafnian is 3.  Use endpoint-star
rows

\[
\begin{array}{c|cccccc}
x&0&1&2&3&4&5\\ \hline
P_x&e_0&0&e_1&0&e_2&0\\
S_x&0&e_0&0&e_1&0&-2e_2.
\end{array}                                             \tag{48}
\]

Both star matrices have rank three, and

\[
 P^{\mathsf T}H(Q)S=
 \begin{pmatrix}3&3&-6\\3&3&-6\\3&3&-6\end{pmatrix}
                 =-15a.                                \tag{49}
\]

Thus the complete nine-entry mixed-word identity (47) holds.  For the
selected scalar-zero matrix \(K_*=I/5\), the response has only

\[
                 R_{01}=1/5,\qquad R_{23}=1/5,\qquad
                 R_{45}=-2/5.                          \tag{50}
\]

Consequently

\[
 D\operatorname {haf}_Q(R)=0,qquad
 \operatorname {haf}(R)=-{2\over125}\ne0.             \tag{51}
\]

The sharper same-word test keeps the direct scalar nonzero.  Contract the
same fixed block with

\[
 K=\operatorname {diag}(1,1,1/2),\qquad
 s=\langle a,K\rangle=-1/5.
\]

The response is supported on the matching with weights
\(R_{01}=1,\ R_{23}=1,\ R_{45}=-1\).  Exact matching enumeration then gives

\[
 D\operatorname {haf}_Q(R)=3,\qquad
 15s+D\operatorname {haf}_Q(R)=0,                     \tag{51a}
\]

but its next two layers are

\[
 [R^{[2]}q]=-1,\qquad [R^{[3]}]=-1,\qquad
 s[R^{[2]}q]+[R^{[3]}]=-{4\over5}.                    \tag{51b}
\]

Thus even with \(s\ne0\), the complete selected-word cohafnian matrix
kills only the first-order top response and leaves a nonzero nonlinear
residual.  These one-word guards do not include the constant X2 anchor;
their limited role is to show that this especially chosen mixed word alone
is insufficient.  They do not establish a minimal detector.

A companion
[pure-nine rank-two boundary audit](h3-pure-nine-rank-two-hafnian-update-boundary.md)
independently shows that all 27 constant-colour rows, shared stars, and
goodness can leave \(\chi_2=-28\); its audited Hamming-one word
\(022222\) then fails by \(-1\).  Thus constant-word data alone is
insufficient and a mixed Hamming layer (or an all-word/overlap identity
implying the same cancellation) is required.  This does not identify
selected-cross as a unique or minimal detector.

In the restricted six-site selected-star support fibre, with labels a,b,c,
let

\[
                         Y=ccbbcb,
 \qquad \Theta_a=R_{aa}\left(q+\tfrac12R_{aa}\right).
\]

Literal singleton matching enumeration proves

\[
 \boxed{
 PTS\,[Y]R_{ac}q^{[2]}
       =Du\,[X_b]R_{bb}\Theta_a.}                      \tag{52}
\]

The retained anchors and goodness give \(P,T,S\ne0\); the restored cc row
supplies \(D,u\ne0\).  Therefore, in this support fibre,

\[
                [Y]R_{ac}q^{[2]}=0
       \quad\Longleftrightarrow\quad
                [X_b]R_{bb}\Theta_a=0.                 \tag{53}
\]

Thus, in this support fibre, the selected-cross row detects the
line-dependent carrier.  It does not detect the marked curvature.  In the
same exact family that curvature is

\[
                             z-AS,                      \tag{54}
\]

which is independent of the common factor in (52).

For the rational specialization

\[
 x=2,\qquad y=w=u=v=P=T=C=D=A=1,\qquad z=S=-1,\qquad B=0,
                                                               \tag{55}
\]

the two restored diagonal rows both equal one, the marked curvature (54)
is zero, the selected-cross residual is one, and the carrier in (52) is
-1.  Replacing only B by -1/2 repairs the selected-cross row and kills the
carrier, while leaving the marked curvature zero and every nonexceptional
row exact.  Its sole remaining residual is

\[
                              0-X_a.                    \tag{56}
\]

Hence, in this selected-star support fibre, the restricted implication

\[
 \text{third diagonal + Segre + selected-cross}
       \Longrightarrow\text{nonzero curvature/transgression}
\]

is false.  What is positive is only the carrier-detection equivalence
(53).  This is not a complete full-nine test, because the exceptional
\(X_a\) row remains missing.  Restoring that row (56) requires a
top-changing all-a perfect matching supported across at least three
residual star centres.  No fixed one- or two-star repair can do it.

After relabelling a as the exceptional physical label 2, (56) is the
same type of missing constant-word datum as the X2 row in the rootless
guard.  Equations (47)--(56) therefore locate a structural interface but
do not settle it: simultaneous exceptional-row restoration and
selected-cross conservation in an unrestricted full-nine source remains
open.

## 8. Why target purity does not kill the vertical ambiguity

The three raw anchor cuts do not live in three summands of one carrier.
For colour c, the cut removes a different set

\[
                         Z_c=W\setminus\{x_c,y_c\}.     \tag{57}
\]

Only after selector normalization are their defects placed in one matrix
space, and then they have overlapping mixed entries.  For example, both
Delta_0 and Delta_1 in (12) contribute to matrix cell (0,1).  The cycle
projection is the sum map on the three labelled contributions, not the
identity map into three target-pure summands.  The nonzero vector (15) is
an explicit element of its kernel.

The older one-site polarization theorem gives two distinct pure-factor
sites for two independent target directions.  It does not give three
sites.  Its exact h=3 incidence guard uses

\[
 L=e_0^{(0)}+e_1^{(1)},
 \qquad S=e_0^{(0)}+e_2^{(1)},                          \tag{58}
\]

and realizes all three target labels using only sites 0 and 1.  A crossed
target-zero row has no nonzero pure target side from which to extract a
third site.

More fundamentally, the first-moment vertical class lies inside one
ordered (j,a,a,k) carrier summand.  Reinsertion forgets those ordered
roles.  Independence of X0,X1,X2 after reinsertion says nothing about the
kernel inside that one summand.  If a separate theorem proved that every
vertical difference lay in a direct sum of target-pure exposed-factor
summands on which reinsertion is injective, then the torsor would indeed
vanish.  The required containment/injectivity is precisely the missing
source-relative saturation statement

\[
                 H(\chi_{jk})(\ker H(\pi_{jk}))=0.      \tag{59}
\]

It is not a consequence of the three cuts and one crossed zero row.

## 9. The canonical target cubic fails the Hankel test

On the canonical off-diagonal line

\[
                         K(u,v)=uE_{01}+vI,             \tag{60}
\]

all three target forms are v.  Even grant the strongest diagonal values
of three local maps at three distinct selector sites,

\[
                         \phi_{x_c}(e_c)=v.             \tag{61}
\]

Their product is the proposed target cubic v^3.  The raw four-cuts do not
construct the full maps \(\phi_x:V_x\to U^*\) or prove their compatibility
with all Macaulay shifts; (61) grants more than the present source rows.

Write the quadratic cycle as

\[
                         \Psi_C=(q_0,q_1,q_2).          \tag{62}
\]

In divided-differential coordinates, Cartan multiplication by v^3 gives

\[
             \Theta=\Psi_Cv^3
                =(0,0,0,q_0,4q_1,10q_2).              \tag{63}
\]

On the clean coordinate pair (u^3,v^3), the six quintic shifts are the
coordinate functionals.  The three v^3 shifts therefore leave the exact
residual

\[
                         (q_0,4q_1,10q_2).              \tag{64}
\]

Hence

\[
                    \mu_{\mathcal E}^*\Theta=0
                 \quad\Longleftrightarrow\quad
                    \Psi_C=0                            \tag{65}
\]

on this clean line.  In particular, a hypothetically normalized
\(\Psi_C=(1/4,0,0)\) leaves residual (1/4,0,0).  One unshifted crossed
target-zero coefficient does not supply the three identities in (64).
Thus the canonical target cubic is not the missing active-cap
prolongation, even if the local diagonal values (61) are granted.

## 10. Scope and exact audit

The direct-sum counterpacket couples exact physical formulas through their
displayed rational coefficients and retains every named associated grade.
It does not assert that one block array satisfies every all-label full-nine
row in both adjacent charts.  In particular, inserting the unused coefficient
U=-4 into the rotating-frame block guard can enter raw diagonal-anchor
cuts which are not audited here.  Those complete physical cuts are exactly
where a new representative of (3) could occur.

The dependency-free checker
[verify_adjacent_full_nine_h3_cycle_transgression.py](../computations/verify_adjacent_full_nine_h3_cycle_transgression.py)
uses exact rational arithmetic and verifies:

* the single compatible global selector word;
* the Hessian-kernel frame, all three nonzero anchor contributions, and
  their cycle cancellation;
* the oriented power-free connection, normal, curvature, and direct-double
  identities and both nonvacuous Euler pairs;
* the rank-five to rank-six transgression obstruction and the stronger
  two-curvature common-mode witness;
* the failure of the pure-reinsertion shortcut;
* the identical opposite-shore high splitting, the three-label static
  Segre sum-channel guard, and the exceptional root residual; and
* selected-cross/carrier conservation and repair in the restricted
  selected-star support fibre;
* the scalar-zero and nonzero-direct-scalar selected-word response guards;
  and
* the full three-shift residual (64) for the canonical v^3 candidate.

It runs unchanged under optimized Python.
