# The h=3 landing lands on an inactive root

Research evidence only.  Krenn's conjecture remains open, `SP-CLEAN-BRIDGE`
is untouched, and no certified dependency changes.

## 1. Outcome

`SP-CLEAN-BRIDGE` needs an **active clean point**: a cap covector \(K\) with
\(s\kappa_0\kappa_1\kappa_2\neq0\) and \(\mathcal E_{p,q}(K)=0\)
([the descent target](clean-pair-cap-exact-descent-target.md), Theorem 1.1).
This note computes what the \(h=3\) machinery actually delivers against that,
and the answer is uncomfortable.

* At \(h=3\), \(\mathcal E\) **is** the star-sector class:
  \(\mathcal E=sQ_2+Q_3\), and at \(K=E_{ab}\) that is
  \(\alpha Q_2+Q_3=\chi\).
* **All nine coordinate caps are inactive.**  \(\kappa_c(E_{ab})=\delta_{a=b=c}\),
  so \(\kappa_0\kappa_1\kappa_2=0\) — for the diagonal caps too, where two of
  the three vanish.
* Hence the long-standing landing target \(\chi=0\) certifies the root
  \(z=0\) of the cap line \(K_z=E_{ab}+zI\), and \(z=0\) **is** the coordinate
  cap.  **The landing cannot deliver the descent.**

The first bullet is proved as a formal polynomial identity in the sixty generic
symbols a fixed word exposes; since those sixty are distinct block entries
whatever the word, it holds at all \(729\) words, on every packet, with
cross-colour edges live.  The second is immediate from the definition of
\(\kappa\) and involves none of the sixty.

**Prior art.**  The committed and audited
[curved-cap note](curved-cap-inactive-root-export-and-osculating-ledger.md)
already contains, in its section 3, the cap line \(K(z)=E_{ab}+zI\) (its
equation 11), the \(\kappa\) ledger \(\kappa_0=\kappa_1=\kappa_2=z\) for
\(a\neq b\) and \(\kappa_a=1+z,\ \kappa_c=z\) for \(a=b\) (equations 12–13),
the statement that the colour-activity boundary is \(z=0\), the identification
of the other inactive point as the zero of \(s(z)\), and its section 4's gcd
dichotomy.  Bullet 2, the \(\kappa\) ledger, the activity divisors and
section 7's dichotomy below are therefore **prior art, restated at \(h=3\)**.

What is new here: the \(h=3\) identification \(\chi=\mathcal E(E_{ab})\) — that
the long-standing landing target *is* coordinate-cap cleanliness — the four
coefficient tensors **in their star-sector form**, the curved-cap note's
section 2 equations (7)–(8) already giving an equivalent polarization of the
same cubic on the same line at general \(h\) — the identification
\(c_3=\mathcal E(I)\) with its independence of \((a,b)\), the rank criterion,
and the packet table.

Two refinements make the situation precise rather than merely negative.

**The published target is one coordinate, not \(729\).**  The frontier asks for the vanishing of
\(\alpha Q_2+Q_3\) in the single pure-colour coordinate \(c^6\).  But \(\mathcal E(K_0)\) is a \(729\)-vector whose
\(w\)-coordinate is \(\chi_w\), so the published target gives \(z\mid\mathcal E_w\)
for a single \(w\).  Even the full strengthening \(\mathcal E(K_0)=0\) in all
\(729\) coordinates only makes \(z=0\) a common root.

**What the landing buys is exactly one degree.**  \(\mathcal E(z)=z\Psi_0(z)\)
with \(\deg\Psi_0=h-1=2\).  That is verbatim the \(\nu=0\) row of the audited
[base-locus factorization](offdiagonal-base-locus-ternary-omega-residue.md).
So the landing is **branch 2's defining condition**, not an escape from the
frontier's dichotomy: proving it moves a packet from "possibly rootless" to
"roots exist, all inactive".

## 2. The cap-line cubic

Write \(\alpha=A_{pq}(a,b)\), \(\tau=\operatorname{tr}A_{pq}\),
\(A=R(E_{ab})\), and \(B=R(I)=\sum_lR(E_{ll})\) for the **trace response**,
\(B_{xy}=\sum_l[p_l(x)s_l(y)+p_l(y)s_l(x)]\).  Then
\((s,R)(z)=(\alpha,A)+z(\tau,B)\) and \(\mathcal E(z)=\operatorname{X}(s(z),R(z))\)
with \(\operatorname{X}(\sigma,Y)=\sigma Y^{[2]}q+Y^{[3]}\).  Its polarizations
are the four coefficient tensors

\[
\begin{aligned}
 c_0&=\alpha A^{[2]}q+A^{[3]}=\chi,\\
 c_1&=\tau A^{[2]}q+\alpha\langle A,B\rangle^{[2]}q+\langle A,A,B\rangle^{[3]},\\
 c_2&=\tau\langle A,B\rangle^{[2]}q+\alpha B^{[2]}q+\langle A,B,B\rangle^{[3]},\\
 c_3&=\tau B^{[2]}q+B^{[3]}=\mathcal E(I).
\end{aligned}
\]

\(c_3\) is **independent of \((a,b)\)**: it is a property of the packet and the
pair, not of a chart choice.  The activity divisor is \(z^3s(z)\) on an
off-diagonal line and \(z^2(1+z)s(z)\) on a diagonal one, with
\(s(z)=\alpha+z\tau\).

A conventions note on \(\alpha\).  The committed \(\chi\) takes
\(\alpha=-Q_1/Q_0\) from the selected row; here \(\alpha=A_{pq}(a,b)\) is the
cap coordinate.  The two agree **on the row variety at every non-GHZ coefficient**, which is
where every statement below is made; at the three GHZ anchors the row equals
\(1\) rather than \(0\), so the committed value there is \((1-Q_1)/Q_0\).
Off the variety they disagree outright — measured on six
unconstrained random packets, they differ on all six.  The cap coordinate is
also the better-behaved one: the committed expression is undefined when
\(Q_0=0\), which is the case on the seven-row guard, where
\(Q_0=Q_1=Q_3=0\), \(Q_2=-2\) and \(\chi=-2d_{01}\).

Two reformulations worth keeping.  Without any hypothesis,

\[
 \mathcal E(K)_w=\operatorname{haf}_w(sq^w+R^w)
   -s^2\sum_{l,m}K_{lm}\operatorname{Row}(l,m,w),
\]

so **under the nine rows** cleanliness is exactly
\(H_U(sq+R)=s^2\sum_c\kappa_cX_c\).  And \(K_1=\tau E_{ab}-\alpha I\) has
\(s=0\), so \(\mathcal E(K_1)=\operatorname{haf}(R(K_1))\): the scalar-zero
endpoint is clean iff the hafnian of its response array vanishes.

## 3. The identity cap, and the target that replaces \(\chi=0\)

\(K=I\) is the point at infinity of the homogenization
\(K(t,u)=tE_{ab}+uI\) of **every** cap line, with \(\kappa_c(I)=1\) and
\(s(I)=\tau\).  So

\[
 \boxed{\;I\ \text{is active}\iff\operatorname{tr}A_{pq}\neq0,\quad\text{and}\quad
 \mathcal E(I)=0\ \text{with}\ \tau\neq0\ \Longrightarrow\ \text{descent, on any pair.}}
\]

\(B\) is the sum of the three **diagonal** responses, so this target uses the
complete diagonal sector by construction — which is what this project has long
maintained any valid argument must do.

**But it is not a usable intermediate target.**  By
[the companion note](clean-bridge-at-eight-is-the-open-case.md),
"the nine rows force \(\tau\neq0\) and \(\mathcal E(I)=0\)" is *equivalent* to
the emptiness of the nine-row variety — the open \((8,3)\) case.  A target
vacuously true if the variety is empty and false otherwise is exactly as hard
to prove as emptiness itself.  So \(\mathcal E(I)=0\) is worth recording as the
active analogue of \(\chi=0\), and worth nothing as a next step.

That asymmetry is this note's real content: \(\chi=0\) is **reachable but
useless** (it certifies an inactive root), \(\mathcal E(I)=0\) is **useful but
equivalent to the whole case**.

Conversely, if \(\tau=0\) then \(s(z)=\alpha\) is a nonzero constant, the only
inactive point of the *affine* off-diagonal line is \(z=0\) — the point at
infinity \(K=I\) is inactive too, since \(s(I)=\tau=0\) — and **provided a
clean point exists** (frontier branch 2), "all clean points inactive" is
\(\chi=0\) in all \(729\) coordinates.  In the rootless branch the condition
holds vacuously, with \(\chi\neq0\).

## 4. What the rows force: the rank criterion

No identity forces a common factor.  What is available is a clean necessary
condition.  Let \(M\) be the \(729\times4\) matrix of coefficient tensors.  If
\(\gcd_w\mathcal E_w=g\) then every \(\mathcal E_w\) lies in
\(g\cdot\mathbb C[z]_{\leq3-\deg g}\), so

\[
 \boxed{\operatorname{rank}M\leq4-\deg\gcd.}
\]

Hence \(\operatorname{rank}M=4\) implies \(\gcd=1\) — the **rootless** branch.

In the ambient space of \(729\times4\) matrices a rank drop is codimension
\(726=(729-3)(4-3)\).  That is a heuristic about the determinantal variety and
**not** a genericity statement about packets: the packet-to-\(M\) map has image
of dimension at most \(252\) inside a \(2916\)-dimensional space, and the locus
that matters is the nine-row variety, which sits inside that image.  With that
caveat it is the qualitative content of frontier branch 1.  Measured on
\(25\) unconstrained random packets: \(\operatorname{rank}M=4\) and \(\gcd=1\)
every time (verified on that sample, not proved).

The landing is precisely the dependency \(c_0=0\): it supplies the rank drop
\(4\to3\), and the root it certifies is \(z=0\).

## 5. Why a root cannot be named

The \(\tau\)-weight grading of
[the weight note](terminal-class-weight-invisibility-and-fourhole-grade-ladder.md)
does **not** forbid a formula for a root: \(z\) is weight zero and all four
\(c_k\) scale by \(\tau^6\) uniformly, so the roots are invariant.  The correct
statement comes from the **endpoint part** of the repository's own
target-stabilizing torus (`combinatorial-route.md`, section 4): taking
\(\lambda_{p,l}=g_l\), \(\lambda_{q,m}=g_m^{-1}\) and \(\lambda_{u,c}=1\)
satisfies the product condition \(\prod_v\lambda_{v,i}=1\) and scales
\(\operatorname{Row}(l,m,\cdot)\) by \(g_l/g_m\).  So it fixes every \(l=m\)
coefficient — in particular every GHZ target — and fixes the matching tensor of
any **nine-row** solution, where the \(l\neq m\) coefficients vanish.  It sends

\[
 c_k\longmapsto(g_i/g_j)^{3-k}c_k,\qquad\text{hence}\qquad z\longmapsto(g_i/g_j)z.
\]

So a **nonzero root value is not a function of the matching tensor**, while
"\(z=0\) is a root", "\(\mathcal E(I)=0\)" and "\(\deg\gcd\geq2\)" are.  A
landing theorem may assert that an extra root exists; it may not name it —
**on an off-diagonal line**.  For \(a=b\) the weight \((3-k)(e_a-e_b)\) is
zero: the endpoint torus fixes all four \(c_k\) and moves no root.  Both
halves are now checked — the weight condition on all six diagonal and
off-diagonal pairs formally, and numerically on random packets, where every one
of the \(729\) cubics of each diagonal line is unchanged while the
off-diagonal coefficients scale by \((g_i/g_j)^{3-k}\).  This note therefore gives
no such obstruction on a diagonal line, and the frontier does not prove
\(a\neq b\).

The same grading limits the certificate route: it puts \(c_0,c_1,c_2,c_3\) in
four **distinct** graded pieces, so a certificate living at \(\chi\)'s
multidegree — which is what
[the multigrading bounds](terminal-class-ideal-membership-multigrading-bounds.md)
produce — can say nothing whatever about \(c_1,c_2,c_3\).  Each of the \(729\)
cubics also sits in its own site-colour multidegree, so the multigrading gives
no leverage across words either: the gcd is inherently not multihomogeneous.

## 6. The named packets

Every packet's published ledger and \(\chi\) were reproduced first, as were
both standard probes.

The gcd column shows the **raw** cubic; the checker's gcd is its monic
normalization (\(z^2+\tfrac12\), \(z^2+z-1\), \(z^3+\tfrac{10}3z^2+\tfrac{11}3z+\tfrac43\)).
The guard and packet C rows use the committed \(d\); see below.

| packet | rows | \(\tau\) | line | nonzero of 729 | \(\operatorname{rank}M\) | raw cubic | verdict |
|---|---|---|---|---|---|---|---|
| seven-row guard | 6559 | 0 | \((0,1)\) | 1 | 1 | \(-2-4z^2\) | active clean point |
| eight-cycle | 6560 | 1 | any | 0 | 0 | \(\mathcal E\equiv0\) | active clean point |
| pure-word witness | 6559 | 0 | \((1,0)\) | 7 | 3 | \(z\) exactly | **all roots inactive** |
| packet B | 6559 | 0 | \((2,1)\) | 1 | 1 | \(4-4z-4z^2\) | active |
| packet C | 6559 | 0 | \((0,1)\) | 1 | 1 | \(-(z+1)^2(3z+4)\) | active |

None is a contradiction: every one fails at least one GHZ coefficient, so
Theorem 1.1's hypothesis does not hold for any of them.

**The caveat is the important part.**  The guard, B and C each have exactly
**one** nonzero coordinate out of \(729\), so their "gcd" is a single cubic and
a root exists automatically over \(\mathbb C\).  The **eight-cycle is more
degenerate still**: zero nonzero coordinates of \(729\), a single live response
edge, hence \(r^2=0\) and \(\mathcal E\equiv0\) on all nine lines.  Its "active
clean point" is pure support concentration and carries no information at all.
None of these four is evidence about the general case.

The guard and packet C are degenerate in a second way: \(\operatorname{haf}_w(q)=0\)
at **every** one of the \(729\) words, so their entire direct block is free.
On the guard \(\chi=-2d_{01}\), and the same guard with \(d=I\) instead has
\(\chi=0\), \(\gcd=z(z+\tfrac32)\), and an active clean point at \(K=I\).

The least degenerate data point is the **witness** — \(7\) nonzero coordinates,
\(\operatorname{rank}M=3\) — and it realizes the concern exactly: \(\chi=0\)
there in all \(729\) coordinates, \(\gcd=z\) exactly, the sole clean point is
\(z=0\) and inactive, and the degree-two residual \(\Psi_0\) has
\(\operatorname{rank}[c_1,c_2,c_3]=3\), hence is **rootless**.  The landing
holds and buys nothing.

Worth recording separately: the seven-row guard does satisfy the descent's
hypothesis (5), with \(\chi=-2\neq0\) so \(z=0\) is not a root and the
remaining cubic has two active roots.  Homogeneously \(\mathcal E=-2t(t^2+2u^2)\),
the \(\nu=1\) case.  Its two missing diagonal anchors are doing all the work.

## 7. The residual, as an exact formula

On a selected off-diagonal line with \(\alpha\neq0\), under \(H_B(A)=\Delta_{B,3}\):

\[
 \text{the selected line yields a descent}\iff\exists z^\*:\ \mathcal E(K_{z^\*})=0
 \text{ in all }729\text{ coordinates and } z^\*(\alpha+\tau z^\*)\neq0,
\]

necessarily \(\operatorname{rank}M\leq3\).  A descent could also come from
another pair, or from a cap off the line; this is a statement about the
selected line only.  And by section 3 the right-hand side is, at \(h=3\),
either unsatisfiable or equivalent to the open case — so the obligation below
inherits that status rather than being an independent target.

The landing supplies \(c_0=0\) with its root on the activity divisor.
**The residual obligation is a second, independent rank drop:**

\[
 \operatorname{rank}[c_1,c_2,c_3]\leq2,\quad\text{the }729\text{ quadratics }
 c_1+c_2z+c_3z^2\text{ share a root, and that root is not }-\alpha/\tau.
\]

The witness shows that block can sit at full rank \(3\) while the landing
holds — which is exactly why the landing alone is not enough.

## 8. What this does not say

1. It does not refute the landing, and does not claim the landing is
   worthless — it is the \(\nu=0\) row of an audited factorization and it is
   the entry condition of branch 2.
2. It proves nothing about whether \((8,3)\) has a solution.  At \(h=3\) the
   nine-row system is that open case, so everything here is conditional
   structure.
3. The genericity of \(\operatorname{rank}M=4\) is verified on \(25\) random
   packets, not proved, and the codimension figure in section 4 is ambient.
4. Nothing here constructs an active clean point on any packet satisfying all
   nine rows, and no such packet is known to exist.
5. Section 5's "a root may not be named" is proved for **off-diagonal** lines
   only.  On a diagonal line the endpoint torus acts trivially and gives no
   obstruction; the frontier does not prove \(a\neq b\).
6. It does **not** retire \(\chi=0\).  Section 3's equivalence is about
   *active* clean caps; \(\chi=0\) is the cleanliness of an *inactive* one, so
   it implies no descent and correspondingly says nothing about emptiness.

## 9. Audit

The dependency-free checker
[`verify_cap_line_cubic_activity_dichotomy.py`](../computations/verify_cap_line_cubic_activity_dichotomy.py)
verifies both readings as formal identities in the sixty generic symbols, the
four coefficient tensors and their polarization forms, \(c_3\)'s independence
of \((a,b)\), the two reformulations, the activity divisors, the endpoint-torus
weights of the \(c_k\), and the packet table with both standard probes
reproduced.  The rank criterion itself is a two-line hand proof; the checker
spot-checks the *inequality* on the named packets and on \(25\) random ones.

Standard library only, exact `Fraction` arithmetic, about twenty-five seconds,
passing normal, `-O` and `-I -S`, deterministic across hash seeds.

Independently re-audited from the descent note's definitions by separately
written code sharing nothing with the checker: every formal identity, every
packet-table entry, both standard probes and the rank criterion reproduced.
