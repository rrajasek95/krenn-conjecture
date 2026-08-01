# Overlapping rows collapse the cofactor-open one-sided level-two branch

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## 1. Outcome

The one-sided rank-$55$ family from the preceding guard does not survive the
first overlapping value equations. More generally, consider a selected
level-two block with rare colour $c$ at vertices $p,q$, complementary
colours $a,b$, residual vertex set $R$, and

\[
 P_x=(A_{px}[c,a],A_{px}[c,b]),\qquad
 Q_x=(A_{qx}[c,a],A_{qx}[c,b]),\qquad
 z=A_{pq}[c,c].                                      \tag{1}
\]

Let $M$ be the binary packet on $R$, and let $\Psi(M)$ be its six-site
matching tensor. On the branch

\[
             Q=0,\qquad z=0,\qquad \Psi(M)\ne0,       \tag{2}
\]

assume:

1. $\operatorname{rank}d\Psi_M=55$;
2. for every $r\in R$, the live block graph of $M$ on
   $R\setminus\{r\}$ is connected and nonbipartite; and
3. for every distinct $r,x\in R$, the binary four-site matching tensor on
   $R\setminus\{r,x\}$ is not identically zero.

Then any solution of the **full** eight-vertex equations has $P=0$. Thus,
on this cofactor-open generic-kernel locus, the selected-block family
$Q=z=0$ collapses under overlapping rows to the older zero-star branch

\[
                         P=Q=z=0.                     \tag{3}
\]

This is a genuine cross-block narrowing, not a proof of the conjecture. This
theorem alone does not eliminate (3), and it leaves rank-deficient, bipartite-deletion,
zero-slope, and vanishing-cofactor boundary strata untreated. Endpoint
transposition gives the identical statement with $P,Q$ exchanged.

The follow-up
[zero-star four-$c$ theorem](level-two-zero-star-four-c-obstruction.md)
does eliminate (3) whenever the four-site cofactors are live. It also proves
that the slope and cofactor hypotheses here follow from rank $55$ and the
connected-nonbipartite deletion assumptions. Consequently the full equations
exclude the entire one-sided branch on that generic locus.

## 2. The L1 rows kill the direct column

For $s\in\{a,b\}$, colour $q$ by $c$, colour $p$ by $s$, and give
all six residual vertices binary colours. Since $Q=0$, every matching in
which $q$ meets a residual vertex vanishes. The only possible $q$-edge is
$pq$, so the coefficient equation is

\[
                    A_{pq}[s,c]\,\Psi(M)=0.           \tag{4}
\]

The nonzero-slope assumption in (2) gives $A_{pq}[s,c]=0$ for both $s$.
Together with $z=0$, the entire $c$-column at the $q$-end of the direct
block is zero.

Put

\[
                         \alpha_r=A_{qr}[c,c].         \tag{5}
\]

The pure-$c$ target coefficient is $1$. Expansion at $q$, using the
vanishing direct column, shows that the anchor set

\[
                         D=\{r:\alpha_r\ne0\}          \tag{6}
\]

is nonempty.

## 3. Three $c$'s give an injective five-site map

Fix $r\in D$. Colour $p,q,r$ by $c$, and colour the other five residual
vertices by $a,b$. Expansion at $q$ has exactly one surviving term,
the edge $qr$. Hence

\[
 \alpha_r\Phi_r(P)(w)=0,\qquad
 \Phi_r(P)(w)=
 \sum_{x\ne r}P_x(w_x)
 \operatorname{haf}
 \bigl(M|_{R\setminus\{r,x\}};w\bigr).               \tag{7}
\]

The useful point is that $\Phi_r$ is not a new nonlinear object. Choose
either binary output $t\in\{a,b\}$, and embed the ten coordinates
$(P_x)_{x\ne r}$ as a variation $K$ supported on the $r$-star:

\[
 K_{rx}[t,j]=P_x(j),\qquad K_{xy}=0
 \quad\hbox{otherwise}.                              \tag{8}
\]

Then $d\Psi_M(K)$ is zero on words whose $r$-coordinate is not $t$, and
its $r=t$ slice is exactly $\Phi_r(P)$. Thus (7) puts $K$ in
$\ker d\Psi_M$.

There are always five trace-zero vertex-scaling kernels

\[
 K^{\mu}_{xy}=(\mu_x+\mu_y)M_{xy},\qquad
 \sum_{x\in R}\mu_x=0.                               \tag{9}
\]

The connected nonbipartite deletion hypothesis makes these five directions
independent. Since the differential rank is $55$, they are the entire
kernel. If a direction (9) is supported only on the $r$-star, then on every
live deletion edge $xy$ one has $\mu_x+\mu_y=0$. Connectivity and an odd
cycle force every $\mu_x=0$ off $r$, and the trace condition then forces
$\mu_r=0$. Therefore (8) is zero, proving

\[
                         P_x=0\quad(x\ne r).          \tag{10}
\]

If $D$ contains two vertices, applying (10) to both immediately gives
$P=0$.

## 4. Four $c$'s exclude a single anchor

It remains to consider $D=\{r\}$. Equation (10) says that $P$ is
supported, if anywhere, only at $r$. For $x\ne r$, set

\[
                         \beta_x=A_{px}[c,c].         \tag{11}
\]

Now colour $p,q,r,x$ by $c$ and the other four residual vertices by
$a,b$. The unique $q$-edge is $qr$. After removing it, the unique
possible $p$-edge is $px$: the binary entries to every other residual
vertex vanish by (10). The mixed target coefficient is zero, so

\[
 \alpha_r\beta_x\,
 \operatorname{haf}
 \bigl(M|_{R\setminus\{r,x\}};w\bigr)=0              \tag{12}
\]

for all sixteen binary words $w$. Hypothesis 3 and $\alpha_r\ne0$ imply
$\beta_x=0$ for every $x\ne r$.

Finally take the pure-$c$ word. Expansion at $q$ again forces $qr$, but
then $p$ has no available edge: $q,r$ have been removed, and all the
$\beta_x$ vanish. Its coefficient is therefore zero, contradicting the
target coefficient $1$. Hence $D$ cannot be a singleton. Since $D$ is
nonempty, it has at least two elements, and Section 3 gives $P=0$.

## 5. Exact witness audit

The integral packet from
[the one-sided rank-$55$ guard](level-two-one-sided-rank55-guard.md)
satisfies the theorem's open hypotheses more strongly than required:

* $\operatorname{rank}d\Psi_M=55$, with the upper bound supplied by five
  independent integral gauges and the lower bound by a nonzero minor modulo
  $101$;
* every deletion graph is $K_5$;
* each of the six $32\times10$ maps $\Phi_r$ has rank $10$, independently
  modulo $101$ and $1{,}000{,}003$; and
* all $15\cdot16=240$ four-site cofactor coordinates are nonzero.

The checker
[verify_level_two_one_sided_overlap_collapse.py](../computations/verify_level_two_one_sided_overlap_collapse.py)
also identifies every $\Phi_r$ with the literal derivative slice, and
evaluates the L1, three-$c$, and four-$c$ formulas by enumerating all 105
eight-site perfect matchings. It is standard-library only, raises explicitly,
and remains live under normal, optimized, and isolated Python.

## 6. Revised frontier

The exact nonzero one-sided witness was a selected-block guard, but it is no
longer a guard against using the first overlapping value rows: those rows do
detect and eliminate its star. The remaining obstruction is sharper.

The zero-star follow-up closes the remaining cofactor-open specialization.
Thus the generic rank-$55$ one-sided locus is no longer a live obstruction.
The remaining work is either genuinely two-sided or lies on one of the
rank-deficient, graph-degenerate, or cofactor-vanishing boundary strata. A
further single-block support census still does not address those alternatives.
