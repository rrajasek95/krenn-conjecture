# The symmetrized apolarity operator: feasible on generators, infeasible on \(I^2\)

Companions:
[`h3-source-valid-tower-first-obstruction.md`](h3-source-valid-tower-first-obstruction.md)
(T1: no source-valid tower admits the four-cube template; T2: φ bites
first at order four; T3: the 360 order-one residuals are distinct),
[`h3-prolonged-cascade-phi-closure.md`](h3-prolonged-cascade-phi-closure.md)
(the prolonged squarefree lattice is φ-closed under the \(R\)-linear
coefficient convention), and
[`h3-descent-defect-row-space-invisibility.md`](h3-descent-defect-row-space-invisibility.md)
(rows with edge-degree \(\ge1\) φ-image cannot reach the defect).  Model
and conventions are the fourth-Hasse audit's
([`h3-full-hasse-cone-d4-descent-obstruction.md`](h3-full-hasse-cone-d4-descent-obstruction.md)):
\(h=3\), direct-free, bounded, word \(m_8=01211222\),

\[
  A=H_m,\qquad B=H_0-u,\qquad I=(A,B),
\]

with \(A\) the direct-free mixed hafnian — 90 squarefree quartic
monomials in 27 mixed edge variables — and \(u\) the homogenizing
variable.

**Krenn's conjecture remains open.**  Nothing here changes the certified
spine.  This note decides one finite question about one operator class
inside one bounded model.

## 0.  The question, and why it has this shape

After T1 the four-cube **template** cannot be coupled through a
*source-valid* tower (\(D(I)\subseteq I\)): target zero forces the
coupling constant to be \(D_J(A)\in I\), and \(I\) contains no nonzero
element of weight \(<4\) for
\(\operatorname{wt}(\text{edge})=1,\ \operatorname{wt}(u)=4\), so it
cannot be a unit.  (T1's own scope is the template shape inside the
smallest cone's cap coupling, not every chain in a prolonged complex.)
What survives is the *filtration-lowering* shape,
\(D(I^{n+1})\subseteq I^{n}\) with a unit source \(D(A)=1\).  T2 puts
both the unit and the first source-validity constraint at **order four**,
as hafnians of order-one data; T3 shows the constant-coefficient
order-one faces carry no syzygy, so mass must enter at order four rather
than lower.  Together these fix the class to examine:

\[
  D=\sum_{M}c_M\,\partial_M ,\qquad
  M\ \text{a 4-subset of the 27 mixed edge variables},\ c_M\in\mathbb Q,
  \tag{1}
\]

**constant** coefficients, order exactly four, mixed edge directions
only.  There are \(\binom{27}{4}=17550\) unknowns.

Two inequivalent readings of "lowering" are available, and this note's
result is that they **disagree**.

* **Generator level.**  Ask only that \(D(A^2)\in I\) modulo the
  \(\mathbb Q A\) part, i.e. that the generator \(A^2\) of \(I^2\) is sent
  into \(I\) up to a scalar multiple of \(A\), together with the unit
  normalisation.
* **Ideal level.**  Ask that \(D(I^2)\subseteq I\) as **ideals**.

**Which reading do the companions require?**  The generator level, not
the ideal level.  Under the \(R\)-linear coefficient convention of
[`h3-prolonged-cascade-phi-closure.md`](h3-prolonged-cascade-phi-closure.md)
— \(d(a\,r[U])=a\,d(r[U])\), the committed model's convention — the
differential applies \(D_S\) to the **generators only**, never to the
coefficients \(a_U,b_U\).  So the generator-level condition is what that
note's output equations need, and §1's feasibility is what it can use.
The ideal-level condition is what a **coefficient-prolonging (Spencer)**
differential \(d(a\,r[U])=\sum_SD_S(a)(dr)[U\setminus S]\) would require
— and that is precisely the convention the prolonged-cascade note
**explicitly excludes**.  So §2 below decides a condition **strictly
stronger than any cited companion currently requires**; no companion
forces it.  Its interest is that it maps the boundary of the operator
class: it says where a Spencer-type differential would fail if the
route were pushed that way.

Write, for a 4-subset \(M\),

\[
  Q_M:=\sum_{\varnothing\ne S\subsetneq M}
      (\partial_S A)(\partial_{M\setminus S}A),
  \qquad\text{so}\qquad
  \partial_M(A^2)=2A\,\partial_MA+Q_M .
  \tag{2}
\]

The generator-level problem is then the linear system

\[
  \sum_M c_M\,Q_M=\alpha A,
  \qquad
  \sum_{M\in\operatorname{mon}(A)}c_M=1 ,
  \tag{3}
\]

of \(11790\) nonzero unknowns (the \(M\) with \(Q_M\ne0\)) against
\(14610\) equations (the distinct quartic monomials appearing).  The
unit-trace normalisation is exactly \(D(A)=1\), since
\(\partial_MA=1\) precisely for the 90 \(M\in\operatorname{mon}(A)\) and
\(0\) otherwise.

## 1.  Generator level: FEASIBLE, proved over \(\mathbb Q\)

### 1.1  The block decomposition

Grade by **site multidegree**: an edge variable on sites \(s,t\) has
degree \(1\) at \(s\) and at \(t\).  Every monomial of \(A\) is a perfect
matching of the eight sites, so \(A\) is multihomogeneous of degree
\((1,\dots,1)\), and each \(Q_M\) is multihomogeneous of degree
\(2\cdot(1,\dots,1)-\deg(M)\) — verified for all 11790.  The system (3)
therefore block-diagonalizes into **1107** blocks indexed by \(\deg(M)\),
and the \(M\) of degree \((1,\dots,1)\) are exactly
\(\operatorname{mon}(A)\).  Only that one block meets \(A\) or the trace
functional; the other 1106 blocks are homogeneous and solved by
\(c_M=0\).  The problem is a \(90\times91\) system.

### 1.2  The integral identity and the forced \(\alpha\)

Let \(K\) be the \(90\times90\) matrix \(K[m][M]=[Q_M]_m\) over
\(\operatorname{mon}(A)\times\operatorname{mon}(A)\).  Exactly:

* \(K\) is **symmetric**, diagonal constantly \(14\), off-diagonal values
  in \(\{0,2,6\}\) (3600 zeros, 3420 twos, 990 sixes);
* \(\operatorname{rank}_{\mathbb Q}K=34\);
* \(K\mathbf 1=156\cdot\mathbf 1\) — every row sum and every column sum
  is \(156\).

The row-sum identity is the polynomial identity

\[
  \sum_{M\in\operatorname{mon}(A)}Q_M=156\,A .
  \tag{4}
\]

Hence the **symmetrized apolarity operator**

\[
  \boxed{\;D=\tfrac1{90}\,A(\partial)
       =\tfrac1{90}\sum_{M\in\operatorname{mon}(A)}\partial_M\;}
  \tag{5}
\]

solves (3) with \(c_M=1/90\), unit trace, and

\[
  \alpha=\frac{156}{90}=\frac{26}{15}.
\]

\(\alpha\) is not a choice: any solution has
\(90\,\alpha=\mathbf 1^{\mathsf T}K c=156\,(\mathbf 1^{\mathsf T}c)=156\).
An independent replay through the *unreduced* second derivatives confirms
\(A(\partial)(A^2)=336\,A\), i.e. \(D(A^2)=\tfrac{56}{15}A\), consistent
with (2) and (4) since \(336=2\cdot90+156\).

On the remaining generators \(D\) is exact, not merely modular:

\[
  D(A)=1,\qquad D(AB)=B,\qquad D(B^2)=D(B)=0 .
  \tag{6}
\]

### 1.3  Symmetrization is essential

The fourth-Hasse audit's 15 selections all lie in
\(\operatorname{mon}(A)\), and **none** of them works alone: for every one
of the 90 \(M\in\operatorname{mon}(A)\) — a superset of the 15 —
\(Q_M\notin\operatorname{span}_{\mathbb Q}\{A,B\}\).  Checked on all 90.
The feasibility is a property of the symmetric sum, not of any single
coordinate operator.  This is the generator-level counterpart of the
row-space note's mechanism: individual objects miss the target, and only a
combination over the full matching set has the right invariance to land
on \(A\).

### 1.4  No Farkas certificate

Infeasibility of (3) would be certified by \(\mu\) with
\(K\mu=\mathbf 1_A\) and \(\mathbf 1^{\mathsf T}\mu=0\).  One line kills
it: \(156\,(\mathbf 1^{\mathsf T}\mu)=\mathbf 1^{\mathsf T}K\mu=90\),
so \(\mathbf 1^{\mathsf T}\mu=15/26\ne0\).  The very identity that
produces the solution destroys every certificate.  (The checker also
row-reduces \(\{K\mu=\mathbf 1_A,\ \mathbf 1^{\mathsf T}\mu=0\}\) and
finds it inconsistent, independently of the one-line argument.)

That is the whole dual side: a finite-dimensional linear-algebra
statement over \(\mathbb Q\), decided exactly.  Nothing about the
geometry of \(V(A)\) is needed — and feasibility is in any case
established constructively by the explicit solution of §1.2, so the dual
is only a consistency check.

> **Remark (point evaluations; not load-bearing).**  Evaluations at
> \(p\in V(A)\) **span** exactly the hyperplane
> \(\{\lambda:\lambda(A)=0\}\) of functionals on quartics, **provided
> \((A)\) is radical** — which holds because \(A\) is squarefree.  \(A\)
> *is* squarefree, certified here by restriction to explicit rational
> lines: \(A(p_0+t\,v)\) is a quartic \(f(t)\) with \(\gcd(f,f')\)
> constant, impossible if \(A\) had a repeated factor.  Three
> deterministic lines, all with \(\deg\gcd(f,f')=0\).  **Caveat:** the
> spanning statement is a Nullstellensatz argument and needs \(V(A)\)
> taken over an algebraically closed field; over \(\mathbb Q\) alone it
> does not apply.  This is one more reason the verdict above is not
> routed through point evaluations.

## 2.  Ideal level: INFEASIBLE, proved over \(\mathbb Q\)

### 2.1  Reduction to \(E_S[G]\in I\)

\(I^2=(A^2,AB,B^2)\).  Leibniz for the constant-coefficient operator (1)
gives, for any \(f\) and any generator \(G\),

\[
  D(fG)=\sum_{|S|\le4}(\partial_Sf)\,E_S[G],
  \qquad
  E_S[G]:=\sum_{M\supseteq S}c_M\,\partial_{M\setminus S}G .
  \tag{7}
\]

**Claim.**  \(D(I^2)\subseteq I\iff E_S[G]\in I\) for every \(S\) with
\(|S|\le4\) and every \(G\in\{A^2,AB,B^2\}\).

*Proof.*  Each \(M\) is a set of four **distinct** variables, so
\(\partial_M=\prod_{e\in M}\partial_e\) and Leibniz gives exactly (7),
which expresses \(D(fG)\) as an \(R\)-combination of the \(E_S[G]\).
That is (\(\Leftarrow\)).

For (\(\Rightarrow\)), test on the squarefree mixed monomials \(f=x^S\)
and induct **upward** on \(|S|\).  Since \(x^S\) is squarefree,
\(\partial_{S'}x^S=x^{S\setminus S'}\) when \(S'\subseteq S\) and \(0\)
otherwise, so (7) reads

\[
  D(x^SG)=\sum_{S'\subseteq S}x^{S\setminus S'}\,E_{S'}[G]
        = E_S[G]+\sum_{S'\subsetneq S}x^{S\setminus S'}\,E_{S'}[G].
\]

Base case \(S=\varnothing\): \(D(G)=E_\varnothing[G]\in I\).  If
\(E_{S'}[G]\in I\) for every \(S'\subsetneq S\), then every term of the
sum lies in \(I\), and \(D(x^SG)\in I\) by hypothesis, so
\(E_S[G]\in I\).  The induction reaches every \(S\) with \(|S|\le4\)
(larger \(S\) contribute nothing, since \(E_S[G]=0\) once \(|S|>4\)).
\(\square\)

One membership shortcut is used throughout: \(A\) and \(B\) share no
variable (\(A\) is mixed-only, \(B\) pure plus \(u\)), \(D\)
differentiates only mixed edges, so every \(E_S[A^2]\) is mixed-only; and
for \(f\in\mathbb Q[\text{mixed}]\), \(f\in(A,B)\iff f\in(A)\) inside
\(\mathbb Q[\text{mixed}]\) — apply \(u\mapsto H_0\) then set the pure
edges to zero; both are ring maps fixing \(f\) and \(A\), and they kill
\(B\).  The same disjointness is what forces the \(B\)-coefficient
\(\beta=0\) in the generator-level normalisation.

### 2.2  Three layers are free for every \(c\)

* \(G=B^2\).  \(\partial_T(B^2)=0\) for every nonempty mixed \(T\)
  (checked on all 27 edges; \(B\) has no mixed variable).  Only \(|S|=4\)
  survives, giving \(c_SB^2\in I\), an identity.
* \(G=AB\).  \(\partial_T(AB)=B\,\partial_TA\) for every mixed \(T\)
  (checked for all 27 singletons and all 351 pairs), so
  \(E_S[AB]\in(B)\subseteq I\) for every \(c\).
* \(G=A^2\), \(|S|=3\).  \(\partial_e(A^2)=2A\,\partial_eA\) for all 27
  edges \(e\), so \(E_S[A^2]\in(A)\) for every \(c\).  \(|S|=4\) is
  \(c_SA^2\in(A)\), an identity.

So the only live conditions are \(G=A^2\) with \(|S|\le2\).

### 2.3  The forcing lemma: zero-site multidegrees see nothing of \((A)\)

**Lemma.**  If \(e,f\) are mixed edges sharing a site, then
\(c_{S\cup\{e,f\}}=0\) for every \(S\).  Consequently
\(\operatorname{supp}(c)\subseteq\operatorname{mon}(A)\).

*Proof.*  Every monomial of \(A\) has site-degree exactly \(1\) at every
site, so every element of \((A)\) has site-degree \(\ge1\) at every site
(checked directly: all \(378\) degree-two multipliers \(m\) give
\(A\,m\) with minimum site-degree \(1\)).  Fix \(|S|=2\) and split
\(E_S[A^2]\) by multidegree.  Using
\(\partial_{M\setminus S}(A^2)=2A\,\partial_{M\setminus S}A
+2\sum(\partial_eA)(\partial_fA)\) with \(\{e,f\}=M\setminus S\), the
component of multidegree \(2\cdot(1,\dots,1)-\delta\) is

\[
  2\!\!\sum_{\deg\{e,f\}=\delta}\!\!c_{S\cup\{e,f\}}
    (\partial_eA)(\partial_fA)
  \pmod{(A)} .
\]

If \(\delta\) has a site of degree 2 — i.e. \(e\) and \(f\) share a site
— then \(2\cdot(1,\dots,1)-\delta\) has a **zero** site, where \((A)\)
contributes nothing at all, so that component must vanish outright.  And
each such \(\delta\)-class is a **singleton**: there are exactly 156
multidegrees \(\delta\) with a degree-2 site, and each contains exactly
one pair \(\{e,f\}\) (verified; the 351 pairs split as \(156+195\) into
226 classes, the 156 shared-site ones all of size 1).  Each
\(\partial_eA\ne0\) and \(\mathbb Q[x]\) is a domain, so
\(c_{S\cup\{e,f\}}=0\).  Taking \(S=M\setminus\{e,f\}\) for any two edges
of \(M\) sharing a site kills every non-matching \(M\): **17460 of the
17550 unknowns**, leaving exactly the 90 perfect matchings, which are
\(\operatorname{mon}(A)\).  \(\square\)

This is the whole split in one sentence: the generator condition lives
in the \(1^8\) block, where \(A\) is present and the symmetrizing identity
(4) can do its work; the ideal condition also probes multidegrees with a
zero site, where \(A\) is simply absent and there is nothing to cancel
against.

### 2.4  The 195 remaining conditions kill the 90 survivors

The disjoint pairs \(S\) give \(351-156=195\) live \(|S|=2\) conditions.
Each has **full local rank**: writing \(k\) for the number of matchings
\(M\in\operatorname{mon}(A)\) containing \(S\) and \(r\) for the rank of
\(\{\partial_{M\setminus S}(A^2)\}\) modulo \((A)_6\),

| shape | count |
|---|---|
| \(k=r=3\) | 150 |
| \(k=r=2\) | 45 |

so every one of the 195 conditions kills, on its own, every coefficient
it mentions — and all 90 matchings are covered.  Structurally: for every
disjoint edge pair \(S\), the products \((\partial_eA)(\partial_fA)\) over
the matchings \(\{e,f\}\) of the four sites **not** covered by \(S\) are
linearly independent modulo \((A)\).

### 2.5  Explicit pairing certificates, all 90

For each \(M\in\operatorname{mon}(A)\), with \(S=\{M_1,M_2\}\) its first
two edges, the checker produces a rational functional \(w_M\) on
degree-six forms with

* (a) \(w_M(A\,m)=0\) for **all 378** degree-two monomials \(m\), so
  \(w_M\) annihilates \((A)_6\);
* (b) \(w_M\bigl(\partial_{M'\setminus S}(A^2)\bigr)=\delta_{M',M}\) for
  the \(M'\in\operatorname{mon}(A)\) containing \(S\).

Both are verified exactly for all 90.  Pairing \(w_M\) against
"\(E_S[A^2]\in(A)\)" reads off \(c_M=0\) directly.  Supports range over
\(1\)–\(4\) monomials, and **15 of the 90 are single-monomial**: one
degree-six coefficient decides one \(c_M\).  The representative witness is

\[
  M=\bigl\{(0,1),(2,5),(3,7),(4,6)\bigr\}
   =\{a_{0,1}^{0,1},\,a_{2,5}^{2,2},\,a_{3,7}^{1,2},\,a_{4,6}^{1,2}\},
  \qquad S=\{a_{0,1}^{0,1},\,a_{2,5}^{2,2}\},
\]

(superscripts are the colour pair) with witness monomial and scale

\[
  m^*=\bigl(a_{0,1}^{0,1}\bigr)^2\,a_{2,3}^{2,1}\,a_{2,4}^{2,1}\,
      a_{5,6}^{2,2}\,a_{5,7}^{2,2},
  \qquad w_M=\tfrac12\,[\,m^*\,].
\]

Exactly two matchings contain \(S\); their
\([\partial_{M'\setminus S}(A^2)]_{m^*}\) readings are \((0,2)\), and
\([A\,m]_{m^*}=0\) for every one of the 378 degree-two \(m\).  So the
coefficient of the single monomial \(m^*\) in \(E_S[A^2]\) equals
\(2c_M\), while every element of \((A)\) has coefficient zero there:
\(E_S[A^2]\in(A)\) forces \(c_M=0\).  One monomial, one coefficient.

### 2.6  Assembled system and verdict

Reducing every condition modulo the appropriate graded piece of \((A)\)
and echeloning gives \(33+255+540=828\) equations in the 90
matching coefficients, from the \(|S|=0,1,2\) layers.  Over \(\mathbb Q\):

* \(|S|=2\) layer alone: rank **90**;
* full 828-equation system: rank **90**.

Both established by exact rational Gauss–Jordan.  Redundant cross-checks
mod \(1009\), \(1013\), \(1019\) also give rank 90 — these carry no
independent weight, the statement is already proved over \(\mathbb Q\).

Hence \(c=0\) is forced, so
\(\sum_{M\in\operatorname{mon}(A)}c_M=0\ne1\).

> **Theorem (ideal-level infeasibility, over \(\mathbb Q\)).**  No
> constant-coefficient order-four operator \(D=\sum_Mc_M\partial_M\) in the
> 27 mixed edge directions satisfies \(D(I^2)\subseteq I\) together with
> \(D(A)=1\).

§3.2 upgrades this to **arbitrary polynomial coefficients** at the same
order, so the constancy in the statement is not a restriction.

For contrast, the symmetrized solution \(c_M=1/90\) satisfies **all 33**
equations of the \(|S|=0\) layer and violates equations in both the
\(|S|=1\) and \(|S|=2\) layers.  That is the split, made numerical.

Recall from §0 that this is a condition **no cited companion requires**:
the \(R\)-linear convention needs only §1.  What §2 shows is that a
Spencer-type coefficient-prolonging differential, which would need the
ideal-level condition, cannot be built from this operator class.

## 3.  Variable coefficients, and how far the argument reaches

§2 decided **constant** \(c_M\).  A weight argument shows that at order
four nothing is lost — and shows exactly where the same argument stops.

### 3.1  The weight-splitting reduction

Give \(R\) the weight grading of **T1**: every edge variable (mixed or
pure) has weight 1, and \(u\) has weight 4.  T1's load-bearing fact is
that **both generators of \(I\) are weight-4 homogeneous**, re-verified
here, so \(I\) and \(I^2\) are weight-graded ideals — \(A^2,AB,B^2\) are
all weight-8 homogeneous.  And \(\partial_T\) lowers weight by exactly
\(\operatorname{wt}(T)\), checked here on all 55 ring variables against
all three generators of \(I^2\).

Now take \(D=\sum_Tc_T(x)\,\partial_T\) with \(T\) a multiset of
variables and \(c_T\in R\) **arbitrary polynomials**.  Decompose each
\(c_T\) into weight-homogeneous pieces and regroup by *weight shift*:

\[
  D=\sum_{w}D^{(w)},\qquad
  D^{(w)}:=\sum_T c_T^{(\operatorname{wt}(T)+w)}\,\partial_T ,
\]

so \(D^{(w)}\) sends weight \(d\) to weight \(d+w\).

**Lemma (weight splitting).**  \(D(I^2)\subseteq I\) and \(D(A)=1\)
together imply \(D^{(-4)}(I^2)\subseteq I\) and \(D^{(-4)}(A)=1\).

*Proof.*  \(I^2\) is weight-graded, so it is spanned by weight-homogeneous
elements \(g\); for such a \(g\) the pieces \(D^{(w)}(g)\) sit in pairwise
distinct weights.  \(I\) is weight-graded, so \(D(g)\in I\) forces every
weight-homogeneous component into \(I\): \(D^{(w)}(g)\in I\) for each
\(w\).  For the unit, \(A\) has weight 4 and \(1\) has weight 0, so
\(D(A)=1\) puts the unit entirely in the shift \(-4\) part. \(\square\)

So we may assume \(D=D^{(-4)}\), i.e. every \(c_T\) is homogeneous of
weight \(\operatorname{wt}(T)-4\).

### 3.2  At order four this forces constants — closing variable coefficients

For a multiset \(T\) of **mixed edges**, \(\operatorname{wt}(T)=|T|\)
(verified).  With \(|T|\le4\) and \(D=D^{(-4)}\):

* \(|T|<4\) needs \(c_T\) of negative weight — impossible, so \(c_T=0\);
* \(|T|=4\) needs \(c_T\) of weight 0, i.e. a **constant**.

One gap has to be closed: variable coefficients admit **repeated**
directions, so \(T\) ranges over 4-*multisets*, not 4-subsets.  The
forcing lemma survives verbatim, because it only ever uses a
2-sub-multiset \(\{e,f\}\) (possibly \(e=f\)) and the multiplicities
entering Leibniz are positive integers.  Its input is verified here over
multisets: of the 378 2-multisets in 253 \(\delta\)-classes, **all 183
classes with a degree-2 site are singletons** — the 156 shared-site pairs
*and* the 27 repeated directions \(\{e,e\}\), which are never confused
because an edge variable is determined by its site pair (verified).  And
over 4-multisets: \(27405=27315+90\), the 27315 blocked ones each
containing a degree-2-site pair, the 90 survivors being exactly
\(\operatorname{mon}(A)\).  Repeats also cost nothing at the unit: \(A\)
is multilinear (verified), so \(\partial_TA=0\) for every repeated \(T\).

> **Corollary.**  Order-four operators in the mixed edge directions with
> **arbitrary polynomial coefficients** satisfy \(D(I^2)\subseteq I\) and
> \(D(A)=1\) **iff** their constant-coefficient shift-\((-4)\) part does
> — and §2 says none does.  Variable coefficients are closed at this
> order.

### 3.3  Where the generalization fails — and it does fail

The collapse in §3.2 used \(\operatorname{wt}(T)\le4\).  That is the only
place order entered, and it is exactly where the argument breaks.

For \(\operatorname{wt}(T)\ge5\), the shift-\((-4)\) coefficient \(c_T\)
is homogeneous of weight \(\operatorname{wt}(T)-4\ge1\), and the
weight-one space of \(R\) is **nonzero** — it is spanned by the 54 edge
variables (verified).  So those coefficients are genuinely variable and
the weight grading imposes no further constraint on them.  Two
independent ways to reach \(\operatorname{wt}(T)\ge5\):

* **order five in edge variables**: \(\operatorname{wt}(T)=|T|=5\);
* **order two, once \(u\) is admitted**: \(\operatorname{wt}(\{u,e\})=5\)
  (and \(u\) alone already has \(\operatorname{wt}=4\) at order one,
  which is why \(\partial_u\) is a legitimate unit source and the hybrid
  class is a separate question).

**Verdict on the generalization: NO.**  The weight-splitting *reduction*
(§3.1) holds at every order and for every coefficient ring element — that
part generalizes completely.  What does **not** generalize is the second
step, "shift \(-4\) \(\Rightarrow\) constant coefficients": it is
equivalent to \(\operatorname{wt}(T)\le4\) on the support, hence available
only for edge-multisets of size \(\le4\).  At order five and above, and
at order two and above once \(u\) enters, the problem does **not** reduce
to the constant-coefficient case decided here.

Consequently the claim that the whole **operator route** (any order, any
coefficients, all 55 variables) is closed is **not** established.  The
scratch computation `c1feas/step16_hybrid.py` (cited as scratch — not
imported, not audited, not part of this artifact) decides the
constant-coefficient class of order \(\le4\) over all 55 variables by a
\(\mathbb Z^8\times\mathbb Z^8\) bigrading, concluding that the A-slot
unit \(\operatorname{const}D(A)\) is always 0 there while the B-slot unit
is free but lands in the wrong slot.  That is order \(\le4\) only, not
all orders; combining it with §3.1–3.2 gives

* order \(\le4\), mixed edges, **any** coefficients — closed (here);
* order \(\le4\), all 55 variables, **constant** coefficients — closed in
  scratch, unaudited;
* order \(\le4\), all 55 variables, **variable** coefficients — **open**
  (the \(u\)-containing multisets of weight \(\ge5\) survive §3.1);
* order \(\ge5\), anything — **open**.

The operator route is therefore **not** closed entirely, and the
ordinary-residue descent is not the only thing left.

## 4.  What each companion forced about the operator's shape

| companion | what it forced |
|---|---|
| T1 ([`h3-source-valid-tower-first-obstruction.md`](h3-source-valid-tower-first-obstruction.md)) | **lowering, not source-valid** — and the **weight grading**.  The four-cube template cannot be coupled through a source-valid tower: target zero makes the coupling constant \(D_J(A)\in I\), and \(I\) has no nonzero element of weight \(<4\), so it is not a unit.  The same weight-4 homogeneity of both generators is what powers §3.1. |
| T2 (same note) | **order four.**  φ's first bite is at order four, as \(\operatorname{Haf}_A(\varphi\circ D_1)\); the unit and the first source-validity constraint live at the same order.  T2 fixes the *order*; it does **not** fix the coefficients — that is T1's weight grading, via §3. |
| T3 (same note) | **order four, not lower.**  The 360 order-one residuals are pairwise distinct, so constant-coefficient order-one faces have no syzygy: mass cannot enter below order four. |
| [`h3-descent-defect-row-space-invisibility.md`](h3-descent-defect-row-space-invisibility.md) | **symmetrized, not single-selection.**  Individual rows and individual selections miss the target; §1.3 confirms all 90 single selections fail at generator level, so only the full symmetrization is a candidate. |
| [`h3-prolonged-cascade-phi-closure.md`](h3-prolonged-cascade-phi-closure.md) | **the generator-level reading is the one it needs.**  Its \(R\)-linear convention applies \(D_S\) to the generators only, so §1's feasibility is what it can use.  It does **not** require the ideal-level condition — that belongs to the coefficient-prolonging (Spencer) convention it explicitly excludes.  §2 therefore decides something strictly stronger than any companion asks for. |

## 5.  Scope

1. Finite, \(h=3\), direct-free, bounded model of the fourth-Hasse audit,
   word \(m_8=01211222\).  Nothing here is a statement about the
   unbounded problem.
2. **Proved over \(\mathbb Q\)** by exact rational arithmetic: the
   generator-level solution and its forced \(\alpha\); the identity (4);
   the rank of \(K\); the 90 single-selection failures; squarefreeness of
   \(A\); the nonexistence of a Farkas certificate; the free layers
   including \(\partial_eB=0\) on all 27 edges and \(\partial_T(AB)=
   B\,\partial_TA\) at \(|T|=1,2,3\) and on the 90 matchings; the forcing
   lemma census over subsets **and** multisets; the 195 local ranks; all
   90 pairing certificates; the rank 90 of the assembled system and the
   \(c=0\) it solves to; and every weight statement of §3.  The
   mod-\(p\) ranks at 1009/1013/1019 are **redundant cross-checks only**.
3. **Hand proofs over machine-verified inputs** — three of them, flagged
   in the checker's ledger under `proof_status`: the reduction of §2.1,
   the forcing argument of §2.3, and the weight-splitting lemma of §3.1.
   Their inputs are all checked; the universally quantified steps are
   arguments on paper.  Per project discipline this note is a research
   reduction until independently audited.
4. **Closed by this note:** order-four operators in the mixed edge
   directions at the ideal level, with **arbitrary polynomial
   coefficients** (§3.2), repeated directions included.
5. **Not closed:** hybrid operators involving \(\partial_u\).
   \(\partial_uB=-1\) is a genuine unit source in this model, so the
   mixed-edge-only restriction in (1) is a real restriction; the hybrid
   class is under separate investigation and no claim about it is made
   or verified here.  Also not closed: every order five and above, the
   variable-coefficient hybrid class, and anything outside this model.
   §3.3 states exactly why the weight argument does not reach these, and
   the operator route as a whole is **not** closed.
6. The generator-level feasibility is **not** a repair of the route.  It
   is exactly the input the \(R\)-linear prolongation attempt (in
   progress separately) builds on: that attempt needs the generator-level
   operator to exist, and — since its \(R\)-linear convention needs only
   the generator level — §1 gives it what it needs.  §2's stronger
   condition is what a Spencer-type coefficient-prolonging differential
   would require, and that fails.
7. The obstruction of §2 is a **grading fact** — zero-site multidegrees
   are invisible to \((A)\) — hence stable under changes that preserve
   the site grading.
8. Krenn's conjecture remains open.  This constructs no Spencer lift and
   decides no conjecture-level question.

## 6.  Verification

Run

~~~text
python3 computations/verify_h3_apolarity_operator_split_verdict.py
python3 -O computations/verify_h3_apolarity_operator_split_verdict.py
python3 -I computations/verify_h3_apolarity_operator_split_verdict.py
python3 -S computations/verify_h3_apolarity_operator_split_verdict.py
python3 -I -S computations/verify_h3_apolarity_operator_split_verdict.py
~~~

Runtime is about twenty-four seconds.  The checker builds the geometry
from the fourth-Hasse module's own objects (no re-encoding), sweeps all
17550 four-subsets for the cross-term census, verifies the 1107-block
multidegree decomposition, the structure and rank of \(K\), the identity
(4), the exact statements (6), the 90 single-selection failures, the
squarefree line certificates, the inconsistency of the dual system, the
free layers (\(\partial_eB=0\) on all 27 edges, and
\(\partial_T(AB)=B\,\partial_TA\) exhaustively at \(|T|=1,2,3\) — 27,
351 and 2925 cases — plus the 90 matchings at \(|T|=4\); all higher
\(|T|\) follow from \(\partial_eB=0\) by the same one-step induction),
the singleton \(\delta\)-class census over subsets and over multisets,
the zero-site invisibility of \((A)_6\), the 195 local ranks, all 90
pairing certificates against all 378 degree-two multipliers, the named
single-monomial witness, the rank of the assembled 828-equation system
over \(\mathbb Q\) and mod \(1009/1013/1019\) together with the
\(c=0\) it solves to, and every weight statement of §3 (weight-4
generators, weight-8 \(I^2\), \(\partial_v\) lowering weight by
\(\operatorname{wt}(v)\) on all 55 variables, the 2- and 4-multiset
censuses, and the nonzero weight-one coefficient space that marks the
boundary in §3.3).

The ledger carries content hashes of the actual computed geometry — the
monomial sets and coefficients of \(A\) and \(B\), the support, the full
\(K\) matrix, and all 90 pairing functionals — so a silent change of the
underlying geometry moves the digest.  It also carries a `proof_status`
field naming the three hand-proved steps (§2.1, §2.3, §3.1) and the
machine-verified inputs they rest on.  Every reported quantity is
**computed**: \(\alpha\) is read off the verified row sum rather than
asserted, the replay multiple off the polynomial itself, the pinned dual
trace off the row sum, and the forced trace off the explicitly solved
homogeneous system.  The frozen ledger digest is

~~~text
5330ee72132733966ab93a86740a819ebc7341815122564721adbb8af332b4e5
~~~

Mutation-tested with thirteen source-level injections, each raising a
property-naming `RuntimeError` under both `python3` and `python3 -O`:
swapping \(A\) for the pure hafnian; dropping the \(|S|=2\) splittings
from \(Q_M\); miscounting a site multidegree endpoint; dropping one
matching from the symmetrization; normalising by \(1/89\); degenerating
the squarefree test line so \(\gcd(f,f')\) is nonconstant; building the
pairing certificates without the \((A)\)-annihilation rows; skipping the
reduction modulo \((A)\) when assembling the layers; relaxing the Farkas
dual's trace constraint from \(0\) to \(15/26\) (which makes it
consistent); reading the zero-site invisibility off the multiplier
instead of \(A\) times it; corrupting the weight of \(u\); dropping the
repeated directions from the multiset \(\delta\)-class census; and
solving the ideal-level system against the wrong right-hand side.

The last three, together with the derivation of \(\alpha\), the replay
multiple, the pinned dual trace and the forced trace from computed data,
close the earlier gap where a checked quantity was a literal: replacing
any of those literals with a tautology is no longer possible, because
there is no literal to replace — each is now read off the geometry, and
mutations M4/M5, M11, M12 and M13 show the derivations propagate.

One probe did **not** discriminate, and is recorded rather than hidden:
measuring the 195 local ranks *before* reducing modulo \((A)_6\) gives
the same shape counts.  The inference runs one way only — independence
over \(\mathbb Q\) is **weaker** than independence modulo \((A)\), so
the un-reduced probe does **not** exercise the mod-\((A)\) content that
§2.4 asserts, and passing it proves nothing about that content.  The
mod-\((A)\) content is supplied instead by §2.4's own reduced
computation, which is what the checker actually runs, and by §2.5's
pairing certificates, which explicitly annihilate \(A\) times all 378
degree-two monomials; mutation M7 confirms that those certificates have
teeth.
