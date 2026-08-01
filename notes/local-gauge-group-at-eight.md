# The gauge group at eight vertices, and the 231 parameters it leaves

Research evidence only.  Krenn's conjecture remains open, `SP-CLEAN-BRIDGE`
is untouched, and no certified dependency changes.  Nothing here is a partial
case of the conjecture, and nothing here bears on whether \((8,3)\) has a
solution.

## 1. Outcome

Three scaling arguments appear in this repository in different notes, with
different notation, for different purposes.  **Each is already identified with
the same parent in its own note** — see section 6; what this note adds is the
transitive closure, the exact identity component, and one number:

* the **target-stabilizing torus** of [`combinatorial-route.md`](combinatorial-route.md)
  section 4, \(X_{uv}(i,j)\mapsto\lambda_{u,i}\lambda_{v,j}X_{uv}(i,j)\) under
  the product condition \(\prod_v\lambda_{v,i}=1\);
* the **\(\tau\)-weight grading** of
  [the weight note](terminal-class-weight-invisibility-and-fourhole-grade-ladder.md),
  \(q\mapsto q/\tau,\ p\mapsto\tau p,\ s\mapsto\tau s,\ d\mapsto\tau^3d\), which
  fixes the matching tensor while \(\chi\mapsto\tau^6\chi\);
* the **endpoint torus** of
  [the cap-line note](cap-line-cubic-and-why-the-landing-is-inactive.md)
  section 5, which sends \(z\mapsto(g_i/g_j)z\) on a cap line.

> **They are one object.**  All three are one-parameter subgroups of the
> identity component of
> \[
>  G=\{(g_0,\ldots,g_7)\in GL_3(\mathbb C)^8:
>    (g_0\otimes\cdots\otimes g_7)\Delta_{8,3}=\Delta_{8,3}\},
> \]
> and that identity component is **exactly a torus of dimension \(21\)**.

Proved here by exact rational linear algebra on the full \(6561\times72\)
infinitesimal system, built mechanically from the definition.

## 2. Why \(G\) is the right group

The matching tensor is equivariant for the local group:

\[
 H(g\cdot A)=(g_0\otimes\cdots\otimes g_7)\,H(A),
 \qquad (g\cdot A)_{uv}=g_uA_{uv}g_v^{\mathsf T}.
\]

The reason is exactly that a perfect matching covers each vertex **once**:
expanding \(\prod_{uv\in M}(g_uA_{uv}g_v^{\mathsf T})[c_u][c_v]\) produces one
free summation index per vertex, and summing over \(M\) reassembles
\((\otimes g_v)H(A)\).  Verified as a formal polynomial identity in every
weight entry and every group entry at \(N=4\) over \(d=2\) and \(d=3\), and
numerically at \(N=8\).

So \(G\) is the subgroup of the local group that preserves the target, which
is precisely the gauge freedom of the problem rather than an unrelated
symmetry.

## 3. The identity component

\[
 \operatorname{Lie}(G)=\Bigl\{(X_v)\in\mathfrak{gl}_3^{\,8}:
   \textstyle\sum_v(I\otimes\cdots X_v\cdots\otimes I)\Delta_{8,3}=0\Bigr\}.
\]

Written out over all \(6561\) indices this gives \(51\) nonzero equations in
\(72\) unknowns: an index with all entries equal to \(c\) contributes
\(\sum_v(X_v)_{cc}=0\), and an index equal to \(c\) except at one position
\(v\), where it is \(c'\neq c\), contributes \((X_v)_{c'c}=0\).  Every other
index contributes nothing.  Hence

\[
 \boxed{\operatorname{Lie}(G)=
  \Bigl\{X_v\ \text{diagonal for every }v,\ \ \textstyle\sum_v(X_v)_{cc}=0
  \ \text{for each colour }c\Bigr\},\qquad \dim=8\cdot3-3=21.}
\]

**Every infinitesimal gauge transformation is diagonal.**  In characteristic
zero the Lie algebra of a closed subgroup determines its identity component,
so \(G^0\) is the torus of `combinatorial-route.md` (8) and nothing larger.

The full \(G\) is that torus extended by the colour permutations \(S_3\).
That is **proved** in `nonarchimedean-git-bridge.md`, by a split-algebra
argument valid scheme-theoretically and in characteristic two — an earlier
draft of this note relayed it via Kruskal uniqueness instead, which was
unnecessary.  Only \(G^0\) is established above, and only \(G^0\) is used.

## 4. Effective dimension

\(G^0\) acts on the \(28\cdot9=252\) weight entries.  Its kernel there is
exactly \(\{\pm1\}\): triviality forces \(\lambda_{u,i}\lambda_{v,j}=1\) for
all \(u\neq v\) and all \(i,j\); varying \(j\) makes \(\lambda_{v,j}=\mu_v\)
colour-independent, and \(\mu_u\mu_v=1\) for all \(u\neq v\) forces every
\(\mu_v\) equal to a common \(\varepsilon\) with \(\varepsilon^2=1\).  The
product condition is then automatic since \(\varepsilon^8=1\).

That kernel is **finite**, so it costs no dimension.  The infinitesimal kernel
is computed and is zero, and the rank of the infinitesimal action is \(21\) on
five independent fully supported packets.  Hence generic orbits have dimension
\(21\) and

\[
 252-21=231
\]

is the effective parameter count after gauge fixing, before any use of the
finite \(S_8\times S_3\).

## 5. What a landing theorem may name — and the trap in saying it

Grade a monomial by its site-colour multidegree \(D\in\mathbb Z^{8\times3}\) —
the exponent of \(\lambda_{v,i}\).  That multidegree **is** the monomial's
character, and it is trivial on \(G^0\) exactly when \(D(v,i)\) does not depend
on \(v\).  That equivalence is correct.

**It is not a criterion for being a function of the matching tensor.**  \(G^0\)
stabilizes \(\Delta\), not \(H(A)\); a function of \(H\) is *equivariant*, not
invariant, so it need not be \(G^0\)-invariant at all.  The counterexample sits
inside the object: \(F(A)=H(A)[\iota]\) for non-constant \(\iota\) is a
coordinate of the matching tensor, hence a function of it, and its multidegree
\(D(v,i)=[\iota_v=i]\) is not constant in \(v\).  **All \(6558\) non-constant
coefficients of \(H\) are counterexamples.**

The correct global statement uses the subgroup fixing **every** coefficient of
\(H\), namely \(\{h:\sum_vh(v,\iota_v)=0\ \text{for all }3^8\ \text{words}\}\).
Solving exactly gives rank \(17\) of \(24\), so that subgroup is

\[
 \{h\ \text{colour-independent},\ \textstyle\sum_vh(v)=0\},\qquad\dim=7,
\]

which is precisely the \(\tau\)-weight family at full strength.  Its characters
are trivial exactly on multidegrees whose **per-vertex total degree** is
constant in \(v\).  Hence

> if \(F\) is a polynomial in the \(252\) weights that is a function of the
> matching tensor, every monomial of \(F\) has per-vertex **total** degree
> constant in \(v\).

Every coefficient of \(H\) passes this, as it must.  \(\chi\) has per-vertex
total degree \((1,1,1,1,1,1,3,3)\) and fails it, so the weight note's
conclusion survives: a landing theorem can only be a vanishing statement, never
a formula or a bound.  What does **not** survive is any claim that the full
\(21\)-torus delivers that conclusion.

The \(21\)-torus does say something, but only **on the solution locus**:
\(G^0\) preserves \(\{H(A)=\Delta\}\), so a polynomial constant there has each
of its non-trivially-graded components vanishing there.

## 6. Prior art, and what is actually new

Almost all of the structure above is already in this repository, and an earlier
draft of this note claimed several pieces of it as new.  Corrected:

| statement | status |
|---|---|
| the torus and its product condition | prior art — `combinatorial-route.md` (7)–(8) |
| the three scalings are one group | **prior art** — stated in both cited notes, against the same parent |
| \(G^0\) is exactly a torus, nothing non-diagonal | **prior art** — `minimal-norm-gauge.md` proves it for all \(n\geq3\) and all \(q\), including the converse |
| \(\dim=3(|J|-1)\) | prior art — `fixed-star-parabolic-gauge-audit.md` (13); the same count at \((8,2)\) gives \(14\) |
| equivariance for the **local** group | **prior art** — `nonarchimedean-git-bridge.md` |
| the multidegree criterion | **prior art** — `combinatorial-route.md` §4 |
| the full \(G=T\rtimes S_3\) | **proved** in `nonarchimedean-git-bridge.md`, not merely relayable via Kruskal |
| the effective count \(231\) | **new** — no prior occurrence |

So what this note contributes is the number \(231\), the transitive closure
written down in one place, and — after the correction in section 5 — an
explicit warning that the invariance criterion is a false-negative generator if
applied to functions of \(H\) rather than to invariants of \(\Delta\).

## 7. What this does not say

1. Nothing about whether \((8,3)\) has a solution.  Knowing the gauge group
   constrains the *shape* of arguments; it excludes no packet.
2. It establishes \(G^0\), not \(G\).  The component group is relayed.
3. The dimension count is about the **local** group \(GL_3^{\times8}\).  A
   symmetry of the weight space preserving the matching tensor need not come
   from a local transformation, and none is excluded here.
5. Section 5 corrects a false claim an earlier draft of this note made.  The
   \(21\)-torus criterion is **not** necessary for being a function of the
   matching tensor; see the counterexample there.
4. \(231\) is a generic-orbit count.  On a special packet the stabilizer can be
   positive-dimensional and the orbit smaller.

## 8. Audit

The dependency-free checker
[`verify_local_gauge_group_at_eight.py`](../computations/verify_local_gauge_group_at_eight.py)
verifies the equivariance identity formally at \(N=4\) over \(d=2\) and
\(d=3\) and numerically at \(N=8\); computes the infinitesimal stabilizer
exactly and confirms both that its dimension is \(21\) and that it equals the
explicit diagonal traceless-per-colour space; confirms the infinitesimal kernel
on the weight space is zero and the orbit dimension \(21\) on five packets;
confirms both published subgroups satisfy \(\sum_vh(v,i)=0\), reproduce their
published effect on the chart weights, and fix all \(6561\) target
coefficients; and verifies the multidegree criterion against the constancy
test on \(200\) random multidegrees.

It carries negative controls, because a linear-algebra audit that cannot fail
proves nothing: every off-diagonal elementary matrix at every vertex is
confirmed excluded, a trace-violating diagonal matrix is confirmed excluded, a
grading violating the product condition moves exactly three target
coefficients, and — this one replaces a tautology an earlier draft used —
degenerate packets are confirmed to give orbit dimension \(0\), \(1\) and
something strictly between \(0\) and \(21\), so the orbit measurement is
demonstrably able to return a value other than \(21\).

Standard library only, exact `Fraction` arithmetic, about two seconds, passing
normal, `-O` and `-I -S`, byte-identical across hash seeds \(0,1,42,12345\).

**Mutation-tested.**  Six independent injected faults — a transposed group
factor in the equivariance expansion, a wrong expected stabilizer dimension,
dropped trace equations, a \(\chi\) multidegree made constant in \(v\), a wrong
orbit dimension, and a wrong \(\tau\)-exponent — each raise, with exit code
\(1\), under **both** `python3` and `python3 -O`.
