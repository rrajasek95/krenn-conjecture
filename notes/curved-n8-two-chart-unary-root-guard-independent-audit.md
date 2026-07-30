# Independent audit: the two-chart unary-root guard

## 1. Verdict

**PASS.**  The aggregate packet in
[the primary note](curved-n8-two-chart-unary-root-guard.md) has exactly the
two claimed complete \(E_{00}\) root tensors, both caps are clean and
inactive, all four deleted endpoint-star maps have rank three, and the two
charts have the displayed nonzero curvature and literal shared \((L,M)\)
data.  The primary file had SHA-256

```text
ef67337ae8bad29200c66cff7642791728a76dbe1249afb1b3763cfc16cc031f  notes/curved-n8-two-chart-unary-root-guard.md
```

No mathematical repair is required.  One optional clarification would
make the scope especially transparent: after the padding is added there
is a third physical perfect matching, with four colour decorations.  All
four are invisible to both audited \(E_{00}\) rows and are precisely part
of the failure of the unused ternary rows.

## 2. Complete matching enumeration

Use the site order \((p,q,r,s,u,v,w,x)\).  Before the padding, \(wx\) is
forced and the remaining selected support is the six-cycle

\[
                         p-q-u-v-s-r-p.
\]

Its two alternating perfect matchings are

\[
 M_0=pq\mid rs\mid uv\mid wx,
 \qquad
 M_1=pr\mid qu\mid sv\mid wx.
\]

Every edge except \(wx\) has weight one, while \(wx\) has weight
\(1/2\).  Thus both monomials have weight \(1/2\), and both induce the
all-zero colour word.

The padding adds the physical chords \(ps\) and \(qr\), each with a
colour-1 and a colour-2 diagonal occurrence.  Once \(wx\) is removed, the
six-vertex graph has exactly one further physical perfect matching,

\[
                         M_2=ps\mid qr\mid uv\mid wx.
\]

It has four occurrence decorations.  If \(i,j\in\{1,2\}\) are the
colours on \(ps,qr\), respectively, its word and weight are

\[
 (i,j,j,i,0,0,0,0),\qquad {1\over2}.
\]

There are no other matchings: \(wx\) is forced; without both chords one
gets one of the two alternating states of the six-cycle, and choosing one
chord forces the other and \(uv\).

Consequently the complete eight-site tensor of the packet is

\[
 H_B=X_0^B+{1\over2}\sum_{i,j\in\{1,2\}}
 e_i^{(p)}e_j^{(q)}e_j^{(r)}e_i^{(s)}
 e_0^{(u)}e_0^{(v)}e_0^{(w)}e_0^{(x)}.                \tag{A1}
\]

This explicit formula simultaneously verifies two scope facts: the
coefficient of \(X_0^B\) is exactly one, and the packet is not
\(\Delta_{8,3}\), because it has four mixed coefficients and no
\(X_1^B,X_2^B\) terms.

## 3. The complete \(pq\) root tensor

Contract the modes \(p,q\) by \(E_{00}\).  Every padding occurrence dies:
the \(ps\) occurrence has the wrong colour at \(p\), and the \(qr\)
occurrence has the wrong colour at \(q\).  Formula (A1) therefore leaves
exactly \(M_0,M_1\), both on the all-zero residual word.

The physical pair decomposition gives the same result without using the
global enumeration.  The internal quadratic on
\(\{r,s,u,v,w,x\}\) has edges

\[
 rs,\quad sv,\quad uv,\quad {1\over2}wx.
\]

Its only perfect matching is \(rs\mid uv\mid wx\), so

\[
                       q_{pq}^{[3]}={1\over2}X_0.
\]

The selected row of the \(p\)-star is \(pr\), and that of the \(q\)-star
is \(qu\).  Their product is the effective residual edge \(ru\).  After
deleting \(r,u\), the only internal matching is \(sv\mid wx\), again of
weight \(1/2\).  Since \(A_{pq}(0,0)=1\),

\[
 A_{pq}(0,0)q_{pq}^{[3]}+(p_0q_0)q_{pq}^{[2]}
       ={1\over2}X_0+{1\over2}X_0=X_0.                 \tag{A2}
\]

All visible occurrences are colour zero, so every other one of the
\(3^6-1\) residual coefficients is zero.  Equation (A2) is therefore the
complete tensor row, not a selected scalar equality.

## 4. The complete \(pr\) root tensor

Now contract \(p,r\) by \(E_{00}\).  The \(ps\) padding dies at \(p\),
and the \(qr\) padding dies at \(r\).  The internal quadratic on
\(\{q,s,u,v,w,x\}\) has edges

\[
 qu,\quad sv,\quad uv,\quad {1\over2}wx.
\]

Its unique perfect matching is \(qu\mid sv\mid wx\), of weight \(1/2\).
The two selected endpoint stars are \(pq\) and \(rs\), whose product is
the effective residual edge \(qs\).  Its complement is
\(uv\mid wx\), also of weight \(1/2\).  Thus

\[
 A_{pr}(0,0)q_{pr}^{[3]}+(p_0r_0)q_{pr}^{[2]}=X_0,     \tag{A3}
\]

again as a complete six-site tensor equality.

## 5. Clean-error normalization and effective quadratics

At this boundary the target-eliminated clean error is

\[
 \mathcal E(K)=s(K)q\,r(K)^{[2]}+r(K)^{[3]}.
\]

For the \(pq\) root, \(s=1\) and \(r=e_r e_u\).  This quadratic is one
decomposable residual edge, so its square and all higher divided powers
vanish.  Hence \(\mathcal E_{pq}(E_{00})=0\).  The effective quadratic

\[
 y_{pq}=rs+sv+uv+{1\over2}wx+ru
\]

has exactly the two perfect matchings

\[
 rs\mid uv\mid wx,qquad ru\mid sv\mid wx,
\]

each of weight \(1/2\).  Therefore \(y_{pq}^{[3]}=X_0\).

For the \(pr\) root, \(s=1\) and \(r=e_qe_s\), so the same nilpotence
calculation applies.  Its effective quadratic

\[
 y_{pr}=qu+sv+uv+{1\over2}wx+qs
\]

has the two matchings

\[
 qu\mid sv\mid wx,qquad qs\mid uv\mid wx,
\]

and satisfies \(y_{pr}^{[3]}=X_0\).  Both cap points are inactive because
\(E_{00}\) has target coordinates \((1,0,0)\), even though their direct
scalars are nonzero.

## 6. The four deleted endpoint-star ranks

In the fixed endpoint order, the four maps send the three coordinate
covectors to the following direct-sum coordinates:

\[
\begin{array}{c|ccc}
\text{map}&e_0^*&e_1^*&e_2^*\\ \hline
\sigma_p^{(q)}&(r,0)&(s,1)&(s,2)\\
\sigma_q^{(p)}&(u,0)&(r,1)&(r,2)\\
\sigma_p^{(r)}&(q,0)&(s,1)&(s,2)\\
\sigma_r^{(p)}&(s,0)&(q,1)&(q,2).
\end{array}                                                   \tag{A4}
\]

Coordinates at different sites lie in distinct direct summands, and the
colour-1 and colour-2 vectors at one site are independent.  Every row of
(A4) is therefore a linearly independent triple.  All four maps have rank
three.  No symmetry of a block orientation is needed; reversing an edge
only places the same diagonal cell in the named opposite summand.

## 7. Curvature and literal shared four-cut data

Expose \(p,q,r,s\), all in colour zero, and put
\(D=\{u,v,w,x\}\).  In the endpoint-ordered notation of the two-chart
four-cut theorem,

\[
 A=A_{pq}(0,0)=1,\quad B=A_{pr}(0,0)=1,\quad
 C=A_{qr}(0,0)=0,
\]

\[
 E=A_{ps}(0,0)=0,\quad F=A_{qs}(0,0)=0,\quad
 U=A_{rs}(0,0)=1.
\]

The padding cells do not change \(C,E\), because their exposed colours
are 1 or 2.  Thus

\[
                         AU-BF=1.                       \tag{A5}
\]

On \(D\), write

\[
 z=e_ue_v+{1\over2}e_we_x,qquad
 x=t=0,qquad y=e_u,qquad v=e_v.
\]

The standard formulas give

\[
 f=Az+xy=z,\qquad g=Bz+xt=z,
\]

\[
 L=At+By+Cx=e_u,qquad
 H=Av+Ey+Fx=e_v,qquad
 N=Bv+Et+Ux=e_v,
\]

and the literal common double coefficient is

\[
                         M=AU+BF+EC=1.                  \tag{A6}
\]

There is no factorial error in the remaining four-site products.  The two
disjoint edges in \(z\) give

\[
 z^{[2]}={1\over2}X_0^D.
\]

In \(e_ue_vz\), the \(uv\) summand collides at \(u,v\), while the
\((1/2)wx\) summand survives.  Hence

\[
                         e_ue_vz={1\over2}X_0^D.         \tag{A7}
\]

Equations (A6)--(A7) prove both clean rows:

\[
 Mf^{[2]}+LHf=X_0^D,qquad Mg^{[2]}+LNg=X_0^D.
\]

For completeness, in the \(pq\) physical row the decompositions are

\[
 q=z+e_s e_v+e_r e_s,qquad
 F=z+e_r e_u+e_s e_v+e_r e_s.
\]

Thus \(t=0,v=e_v,U=1\) and \(f=z,L=e_u,H=e_v,M=1,s=1\).  The selected
physical four-cut expression is

\[
\begin{aligned}
P&=Mz^{[2]}+(Lv+Ht+fU)z+ftv
       -2s(Uz^{[2]}+tvz)\\
 &=z^{[2]}+e_ue_vz+z^2-2z^{[2]}\\
 &=z^{[2]}+e_ue_vz=X_0^D,
\end{aligned}
\]

where \(z^2=2z^{[2]}\).  The \(pr\) computation is identical after
exchanging the exposed endpoint labels.  Hence the physical row as well
as the clean row holds in the shared four-cut ledger.

## 8. Exact scope

The four padding-decorated terms in (A1) are visible in the full source
tensor, but invisible to each audited root row:

- every one has colour 1 or 2 at \(p\), so it is killed by both
  \(E_{00}\) contractions already at the common centre;
- independently, it has colour 1 or 2 at \(q\) and at \(r\).

They therefore cannot contaminate (A2), (A3), either effective unary
quadratic, or the all-zero four-cut ledger.  They do show directly why the
packet is not a ternary exact source and why the unused endpoint-colour
rows matter.

Accordingly the guard refutes only an argument based on the two complete
coordinate-root tensors, good-star injectivity, and their shared physical
curvature data.  It does not refute a theorem using all nine pair rows, a
second independent covector on each line, or the complete tensor identity
\(H_B=\Delta_{8,3}\).  The binary boundary \(E_{00}-I\) would see the
padding colours and is a legitimate candidate for that missing coupling.

After audit, “tail edge” in the primary was corrected to “disjoint edge”;
no datum changed.  The resulting primary has SHA-256

    e49179610b049f7aeefcf395a9c0a705c33cd411370017ec3f233ac21431633f  notes/curved-n8-two-chart-unary-root-guard.md
