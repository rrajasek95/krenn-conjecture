# Two inactive cap roots leave an exact polarization and curvature-square packet

## 1. Outcome

This note couples the packets from the
[inactive-root ledger](curved-cap-inactive-root-export-and-osculating-ledger.md)
through the physical
[overlapping-cap connection](overlapping-pair-cap-bianchi-connection.md).
There are two genuinely new equations when inactive clean roots from the
curved branch are coupled.  Neither equation is a generic common-root
assertion.

First, let two clean cap covectors for one physical pair have data

\[
 (s_i,F_i,T_i),\qquad F_i=s_iq+r_i,\qquad
 F_i^{[h]}=s_i^{h-1}T_i\quad(i=0,1).                 \tag{1}
\]

On their joining pencil, the clean error is divisible by both endpoint
coordinates.  After those two known roots are removed, the residual has
degree at most \(h-2\), with all coefficients displayed in (7).
At the first \(8\to6\) boundary it is just

\[
 {\cal E}(uK_0+vK_1)=uv(uR_0+vR_1).                \tag{2}
\]

If \(R_0,R_1\) are nonzero and dependent, their residual kernel point gives
an active clean cap precisely when it avoids the four activity hyperplanes.
If they are independent, their wedge is the exact residual obstruction; if
both vanish, the whole pencil is clean and still has an active point only
when the activity product is not identically zero.  This applies without
change when one or both endpoints are nonzero nilpotent packets.  In those
cases (12)--(13) give the mixed Hermite tensors which must survive.

Second, take two coordinate caps at overlapping pairs \(pq\) and \(pr\).
After a four-site cut, their effective quadratics share literally the same
normal row \(L\) and the same double coefficient \(M\):

\[
 \begin{array}{c|ccc}
 &\text{interior}&\text{common normal row}&\text{double coefficient}\\ \hline
 pq&f=Az+xy&L=At+By+Cx&M=AU+BF+EC\\
 pr&g=Bz+xt&L=At+By+Cx&M=AU+BF+EC.
 \end{array}                                                   \tag{3}
\]

If the two coordinate caps are clean, their complete nonlinear coupling is

\[
 \boxed{\begin{aligned}
 M f^{[k]}+LHf^{[k-1]}&=\delta A^kX_a,\\
 M g^{[k]}+LNg^{[k-1]}&=\delta B^kX_a,
 \end{aligned}}                                                \tag{4}
\]

where \(k=m-2\), \(\delta=1\) exactly when all four exposed colours are
\(a\), and \(H,N\) are given in (17)--(18).  A nonzero physical curvature
coordinate is

\[
                         \kappa=AU-BF\ne0.                       \tag{5}
\]

It enters the power-free square identity (19), not as an inferred generic
condition.  Equations (4), (19), and the one exact target row (21) are the
smallest curvature-square residual left by two coordinate roots.

The full target row is essential.  For an arbitrary inactive cap with
\(s=0\), equations (15)--(16) say simultaneously

\[
              F^{[h]}=0,\qquad Fq^{[h-1]}=T.                    \tag{6}
\]

Hence the packet's common-power image remains visible after every two-site
cut for every nonzero target colour.  In particular the old curved guard,
whose inactive point has
\(s=F=0\) but a nonzero binary target, violates (15) on each corresponding
pure transverse row.  The guard cannot satisfy this coupled packet.

These identities do not yet force an active root.  They isolate the exact
remaining alternatives: a nonzero two-root polarization wedge at
\(8\to6\), or a physical four-cut solution of (4), (19), and (21) with
\(\kappa\ne0\).  This is a strict reduction from an arbitrary vector-valued
common-root problem and retains the target rows missing from the known
guard.

## 2. Two clean points remove two projective factors

Fix a physical pair and its residual set of \(2h\) sites, with \(h\ge3\).
Let \(q\) be the internal quadratic.  Cap data are linear in a pair
covector \(K\):

\[
 s=s(K),\qquad r=r(K),\qquad T=T(K),\qquad F=sq+r.                \tag{7a}
\]

Write \(T(K)=\sum_{c=0}^2\kappa_c(K)X_c\); the three \(\kappa_c\)'s
are the diagonal coordinates of the pair covector.

The denominator-cleared clean error is

\[
                         {\cal E}(K)=F(K)^{[h]}-s(K)^{h-1}T(K).
                                                                    \tag{7b}
\]

Suppose \(K_0,K_1\) are clean and use the notation in (1).  Divided-power
polarization gives

\[
 {\cal E}(uK_0+vK_1)=\sum_{j=0}^{h}u^{h-j}v^jE_j,                \tag{7c}
\]

where

\[
\boxed{\begin{aligned}
 E_j={}&F_1^{[j]}F_0^{[h-j]}\\
 &-\binom{h-1}{j}s_0^{h-1-j}s_1^jT_0
  -\binom{h-1}{j-1}s_0^{h-j}s_1^{j-1}T_1,
 \qquad 0\le j\le h .
\end{aligned}}                                                  \tag{7}
\]

As usual, an out-of-range binomial term is omitted before its scalar powers
are interpreted.  Cleanliness at the endpoints says exactly

\[
 E_0=F_0^{[h]}-s_0^{h-1}T_0=0,
 \qquad
 E_h=F_1^{[h]}-s_1^{h-1}T_1=0.                                \tag{8}
\]

Therefore

\[
 {\cal E}(uK_0+vK_1)
   =uv\sum_{j=1}^{h-1}u^{h-1-j}v^{j-1}E_j.                     \tag{9}
\]

This is stronger than applying the one-root jet ledger twice: the same
mixed tensors occur in one degree-\((h-2)\) projective residual.

At \(h=3\), put

\[
\begin{aligned}
 R_0&=F_1F_0^{[2]}-2s_0s_1T_0-s_0^2T_1,\\
 R_1&=F_1^{[2]}F_0-s_1^2T_0-2s_0s_1T_1.
\end{aligned}                                                   \tag{10}
\]

Then (2) follows.  If \(R_0,R_1\) are linearly independent, the residual
linear tensor \(uR_0+vR_1\) has no projective zero.  If they are dependent,
its projective zero is explicit (or the whole pencil is clean when both
vanish).  That zero gives a descent exactly when

\[
 (us_0+vs_1)\prod_{c=0}^2
       \bigl(u\kappa_c(K_0)+v\kappa_c(K_1)\bigr)\ne0.             \tag{11}
\]

Thus the complete first-boundary obstruction is the wedge
\(R_0\wedge R_1\), together with the finite activity test (11); there is no
unstated claim that two roots force a third.

Equivalently, if the activity product in (11) is not identically zero on
the joining pencil, absence of an active clean point at \(h=3\) forces the
exact alternative (write \(\kappa_{ic}=\kappa_c(K_i)\))

\[
 \boxed{ R_0\wedge R_1\ne0\quad\text{or}\quad
   \ker(uR_0+vR_1)\subseteq
   V\!\left((us_0+vs_1)\prod_c(u\kappa_{0c}+v\kappa_{1c})\right).\ }
                                                                    \tag{11a}
\]

Here the second branch includes an endpoint kernel when exactly one of
\(R_0,R_1\) vanishes.  If both tensors vanish, the whole pencil is clean
and a point outside the finite activity divisor exists, contradicting the
no-active hypothesis.  Formula (11a) is the promised exact no-active
classification at the first boundary.

The three packet types specialize (10) without ambiguity.  If both roots
have \(s_0=s_1=0\), then

\[
                  R_0=F_1F_0^{[2]},\qquad
                  R_1=F_1^{[2]}F_0.                              \tag{12}
\]

If only \(s_0=0\), then

\[
             R_0=F_1F_0^{[2]},\qquad
             R_1=F_1^{[2]}F_0-s_1^2T_0.                          \tag{13}
\]

Equation (12) is the exact mixed Hermite packet between two nilpotent
roots; (13) is the exact coupling between a nilpotent packet and a
lower-colour source.  When both scalars are nonzero, (10) couples the two
lower-colour exact quadratics directly.

There is one additional quotient relation at two scalar-zero roots.
The physical pair row gives

\[
                         F_iq^{[h-1]}=T_i\qquad(i=0,1).            \tag{14}
\]

Consequently every linear relation between \(F_0,F_1\) modulo
\(\ker(Z\mapsto Zq^{[h-1]})\) is the same relation between \(T_0,T_1\).
In particular, independent unary or binary target packets cannot collapse
to one response line modulo the common-power kernel.  This is useful even
though their whole joining pencil remains scalar-inactive.

## 3. The full two-site ledger for one inactive packet

The compact equations (6) have a more informative form which exposes the
transverse target rows.  Choose two residual sites \(r,s\), put
\(D=B\setminus\{p,q,r,s\}\), and write \(|D|=2k\), where
\(k=h-1\ge2\).  At fixed endpoint colours \(c,d\), decompose the internal
quadratic and effective quadratic as

\[
\begin{aligned}
 q&=z+e_{r,c}t+e_{s,d}v+e_{r,c}e_{s,d}U+\cdots,\\
 F&=f+e_{r,c}L+e_{s,d}H+e_{r,c}e_{s,d}M+\cdots .
\end{aligned}                                                   \tag{14a}
\]

Here the ellipses contain the other colour rows; (14a) records the selected
\((c,d)\)-coefficient.  The exact physical pair equation can be written in
terms of \(F=sq+r\) as

\[
                 Fq^{[h-1]}-(h-1)sq^{[h]}=T.                     \tag{14b}
\]

Taking the \((r,c),(s,d)\) coefficient gives

\[
\boxed{\begin{aligned}
 &Mz^{[k]}+(Lv+Ht+fU)z^{[k-1]}+ftv z^{[k-2]}\\
 &\qquad-k s\bigl(Uz^{[k]}+tvz^{[k-1]}\bigr)
       =\delta_{cd}\kappa_c(K)X_c^D .
\end{aligned}}                                                  \tag{15}
\]

Taking the same coefficient in the clean equation gives

\[
\boxed{
                  Mf^{[k]}+LHf^{[k-1]}
       =s^k\delta_{cd}\kappa_c(K)X_c^D .}                       \tag{16}
\]

Both formulas are literal matching decompositions.  In (15), the four
terms before the scalar correction correspond respectively to an effective
\(rs\)-edge, one effective and one internal star, an effective interior
edge plus the internal \(rs\)-edge, and an effective interior edge plus two
internal stars.  Equation (16) has only the direct and two-star splits.

At \(s=0\), (16) is homogeneous but (15) retains the target.  If
\(\kappa_c(K)\ne0\), the right side of (15) is nonzero for every choice of
two residual sites coloured \(c\).  Thus the common-power image of a
nilpotent packet is nonzero on every pure \((c,c)\) two-site coefficient
row for which \(\kappa_c(K)\ne0\); the pair \((F,q)\) cannot vanish on any
of those transverse target rows.  In particular \(F=0\) is impossible
whenever \(T\ne0\).
This is the precise equation failed by the zero-data root in the curved
guard.

## 4. Two overlapping coordinate caps share a curvature square

Now use four distinct exposed sites \(p,q,r,s\) in an exact source on
\(2m\) sites, with \(m\ge4\), and put \(D=B\setminus\{p,q,r,s\}\).
Fix exposed colours \(a,b,c,d\).  On \(D\), let

\[
 x,y,t,v                                                        \tag{17a}
\]

be respectively the corresponding rows of the \(p,q,r,s\) stars.  Denote
the six direct entries, in endpoint order, by

\[
\begin{array}{lll}
 A=A_{pq}(a,b),&B=A_{pr}(a,c),&C=A_{qr}(b,c),\\
 E=A_{ps}(a,d),&F=A_{qs}(b,d),&U=A_{rs}(c,d).
\end{array}                                                     \tag{17b}
\]

The effective quadratic \(F=sq+r\) of the coordinate cap \(E_{ab}\) at
\(pq\), read at the two remaining sites \(r,s\), has selected data

\[
\begin{aligned}
 f&=Az+xy,\\
 L&=At+By+Cx,\\
 H&=Av+Ey+Fx,\\
 M&=AU+BF+EC.                                                   \tag{17}
\end{aligned}
\]

The coordinate cap \(E_{ac}\) at \(pr\), read at \(q,s\), has

\[
\begin{aligned}
 g&=Bz+xt,\\
 L&=By+At+Cx,\\
 N&=Bv+Et+Ux,\\
 M&=BF+AU+EC.                                                   \tag{18}
\end{aligned}
\]

Thus \(L\) and \(M\) agree literally, before multiplication by a common
power.  The two power-free connection identities are

\[
\boxed{\begin{aligned}
 ft-gy&=(At-By)z,\\
 Uf+tH-Fg-yN&=(At-By)v+(AU-BF)z.
\end{aligned}}                                                  \tag{19}
\]

The first is the three-site connection.  The second is its four-site
curvature coefficient, now for the raw effective quadratics rather than
the factorially normalized canonical caps.  Direct expansion proves both.

Put

\[
                       \Delta=At-By,\qquad \kappa=AU-BF.          \tag{20}
\]

If the physical transition is nonzero, choose \(s,d\) so that
\(\kappa\ne0\).  If both coordinate caps are clean, (16) applied in the
two charts gives exactly (4), with

\[
 \delta=\delta_{ab}\delta_{ac}\delta_{ad}.
\]

This includes every scalar degeneration.  If \(A=0\) or \(B=0\), the
corresponding clean equation has zero right side, while its nonzero unary
target, when present, is still retained by (21) below.

For completeness, the complete target row in the \(pq\) chart is

\[
\boxed{\begin{aligned}
 &Mz^{[k]}+(Lv+Ht+fU)z^{[k-1]}+ftv z^{[k-2]}\\
 &\quad-kA\bigl(Uz^{[k]}+tvz^{[k-1]}\bigr)=\delta X_a^D.
\end{aligned}}                                                  \tag{21pq}
\]

In the \(pr\) chart it is

\[
\boxed{\begin{aligned}
 &Mz^{[k]}+(Lv+Ny+gF)z^{[k-1]}+gyv z^{[k-2]}\\
 &\quad-kB\bigl(Fz^{[k]}+yvz^{[k-1]}\bigr)=\delta X_a^D.
\end{aligned}}                                                  \tag{21pr}
\]

These are not two independent target equations: they are two presentations
of the same four-site row.  Their difference is

\[
 (\Delta v+\kappa z)z^{[k-1]}
 +\Delta zvz^{[k-2]}
 -k\bigl(\kappa z^{[k]}+\Delta vz^{[k-1]}\bigr)=0,               \tag{22}
\]

by (19), because

\[
 zz^{[k-1]}=kz^{[k]},\qquad
 zz^{[k-2]}=(k-1)z^{[k-1]}.                                    \tag{23}
\]

This recovers the exact Bianchi/exchange cancellation and prevents a
false gain of equations from merely rewriting the target row in two pair
charts.  The actual additional constraints are the two nonlinear clean
equations (4).  Subtracting them gives the concise square residual

\[
 M\bigl(f^{[k]}-g^{[k]}\bigr)
 +L\bigl(Hf^{[k-1]}-Ng^{[k-1]}\bigr)
       =\delta(A^k-B^k)X_a^D.                                  \tag{24}
\]

Equations (19), (21), and (24), with \(\kappa\ne0\), are therefore the
exact four-cut target for a positive two-curvature-line argument.  They
retain arbitrary complex cancellation, zero direct entries, endpoint
order, and every transverse target coefficient.

### 4.1 A sharp mixed-colour square guard

The homogeneous mixed-flag branch of this residual is nonempty, even with
literal physical square data.  Take any quadratic \(z\) on \(D\), set all
four displayed star forms to zero,

\[
                         x=y=t=v=0,                              \tag{26a}
\]

and choose the six exposed entries

\[
                 A=U=E=1,\qquad C=-1,\qquad B=F=0.              \tag{26b}
\]

Choose a mixed exposed colour word, so \(\delta=0\).  Then

\[
 f=z,\quad g=L=H=N=M=\Delta=0,\qquad \kappa=1.                  \tag{27}
\]

Both clean equations (4) hold.  The \(pr\) target presentation is zero.
The \(pq\) presentation reduces exactly to

\[
              z z^{[k-1]}-kz^{[k]}=0,                            \tag{28}
\]

so the complete selected four-site target row also holds.  In source
variables, the direct \(rs\) contribution \(AU=1\) is cancelled in the
effective cap by the crossed response \(EC=-1\).  The \(pq\) effective
quadratic is just \(z\), which cannot cover the two exposed residual sites,
while the \(pr\) effective quadratic is zero.  Thus both selected
mixed-flag clean rows vanish and the physical transition has the nonzero
\(s,d\)-coordinate \(\kappa=1\).

This is a selected-colour square guard, not an exact ternary source: its
stars into \(D\) are zero and the monochromatic target rows have not been
imposed.  It proves that nonzero curvature, the two selected clean rows,
the Bianchi identities, and one full mixed target row still do not yield a
contradiction.  The missing step really is propagation to the other colour
squares or good-star injectivity, exactly as stated below.

## 5. What is closed and what remains

The two previously informal couplings now have finite exact forms.

1. Two inactive clean points at one pair leave the residual (9), and at
   \(8\to6\) its projective kernel is classified exactly by
   \(R_0\wedge R_1\), including endpoint kernels and the identically zero
   residual.  Activity of a kernel point is the elementary test (11).
2. A scalar-zero root is not zero data.  Its nilpotent response is nonzero
   on every pure \((c,c)\) two-site coefficient row with
   \(\kappa_c\ne0\), by (15)--(16).  This excludes the precise failure
   mechanism of the curved full-good-fan guard.
3. Two overlapping coordinate roots do not give two independent copies of
   the target equation.  They give one target row plus the genuinely new
   pair of clean equations (4), coupled through the common \((L,M)\) and
   the nonzero curvature identities (19).

Applied to canonical lines \(E_{ab}+zI\), this gives a precise routing
rule.  Two clean inactive points in the same physical pair chart are
coupled by (9).  Coordinate-boundary points in adjacent charts are coupled
by (4), (19), and (21).  Every remaining diagonal-boundary or scalar-zero
point carries the full packet (15)--(16), so it cannot be replaced by zero
data before the charts are compared.  If a candidate line has no clean
point at all (constant coordinate gcd), none of these conditional root
identities creates one; that is still a separate no-root branch.

What is not proved is that (24) is inconsistent on every physical mixed
colour flag.  On a mixed flag \(\delta=0\), its right side vanishes, and
degenerate solutions with \(L=M=0\) are not excluded by the square algebra
alone.  A full proof must propagate such degeneracy to a monochromatic
flag, where (4) has nonzero pure right sides, or prove that the physical
good-star maps make the simultaneous catalecticant

\[
 (M,L)\longmapsto
 \bigl(Mf^{[k]}+LHf^{[k-1]},\,
       Mg^{[k]}+LNg^{[k-1]}\bigr)                              \tag{25}
\]

injective on enough colour squares.  This is a bounded four-site
factorization problem, not an enumeration of graph subcases and not a
generic common-root premise.

No executable is needed.  Equations (7), (15)--(16), and (17)--(24) are
direct divided-power expansions; (22) audits the only factorial shifts.
