# The three simultaneous six-port response tables cannot coexist

## 1. Outcome

Let an exact ternary source on an even set \(B\), \(|B|=N=2m\ge6\),
satisfy

\[
                         H_B(A)=\Delta_{B,3}.              \tag{1}
\]

Delete an unordered physical pair, let \(q\) be the quadratic internal to
\(W\) (\(|W|=2t\), \(t=m-1\)), and call the pair chart **regular
nonbipartite** when the source Hessian \(Z\mapsto Zq^{[t-1]}\) has only
its vertex-gauge kernel and the graph \(G_3(q)\) of rank-three internal
blocks is connected as a graph on all of \(W\) and nonbipartite.  This is
exactly the chart on which the good-pair fan theorem built its six-port
branch.

**Theorem A (regular charts force doubly dependent stars).**  On every
regular nonbipartite pair chart of an exact ternary source, both deleted
star triples \((p_0,p_1,p_2)\) and \((s_0,s_1,s_2)\) are linearly
dependent in \(\bigoplus_{x\in W}V_x\).

In particular no good pair is regular nonbipartite: a good pair has, by
definition, injective aggregate stars at both deleted endpoints.

Theorem A is purely local.  Its proof uses only the nine pair
contraction equations of the deleted chart, so it excludes the
standalone system consisting of those nine equations, gauge rigidity,
the connected spanning nonbipartite rank-three graph, and one linearly
independent deleted star triple — independently of any global source.
The proof is a collapse through the common internal quadratic.  Gauge
rigidity and the odd cycle first force the six literal degree-two
identities \(p_cs_d=0\) \((c\ne d)\) together with \(a_{cd}=0\); one
independent star triple then pins all six endpoint rows inside a
single site factor \(V_{x_*}\); the three diagonal equations finally make
\(q^{[t]}\) proportional to two distinct pure colour words, which is
impossible.

**Corollary B (the regular fan branch is empty).**  For every even
\(N\ge8\), every common-endpoint good fan has empty regular nonbipartite
part \(F=\varnothing\).  Hence:

1. in the fan dichotomy of
   [the six-port reduction](good-pair-fan-six-port-triple-cofactor-reduction.md),
   the first alternative holds threshold-free and in the strongest form:
   **all** of the at least \(N-7\) fan pairs lie in the
   extra-kernel/disconnected/bipartite escape charts, for every even
   \(N\ge8\), not only \(N-15\) of them at \(N\ge16\);
2. item 2 of that dichotomy — three neighbours \(u,v,w\) with literal
   zero blocks \(A_{ru}=A_{rv}=A_{rw}=0\) obtained from at least nine
   regular fan pairs — can never occur, and the hereditary \(N\ge24\)
   pairwise-good version can never occur;
3. consequently the **three simultaneous six-port response tables cannot
   coexist**: there is no exact ternary source, fan centre \(r\), and
   zero-block neighbours \(u,v,w\) whose pairs \(\{r,u\},\{r,v\},\{r,w\}\)
   are regular nonbipartite good pairs.  A fortiori no simultaneous
   realization of the three capped tables
   \(p_c\overline R^{uv}_{de}=\delta_{c=d=e}X^C_c\) by the common-edge
   factorizations \(R^{uv}_{de}=b_{de}q^{[m-2]}+s_dt_eq^{[m-3]}\) exists.
   This closes the first clause of Priority 2 in
   [the current audit](current-proof-audit-and-next-steps.md), negatively
   for the tables: their generating branch is empty.

**Proposition C (table-exchange redundancy).**  Given the shared physical
origin — the common internal quadratic \(q_Y\) on
\(Y=B\setminus\{r,u,v,w\}\), the nine rows \(s_d,t_e,g_f\) into \(Y\),
the three direct blocks \(b^{uv},b^{uw},b^{vw}\), and the centre rows
\(p_c\) — each single 27-row table is equivalent to the one 81-row
four-slot system

\[
 p_c\Bigl[\bigl(b^{uv}_{de}g_f+b^{uw}_{df}t_e+b^{vw}_{ef}s_d\bigr)
      q_Y^{[m-3]}+s_dt_eg_f\,q_Y^{[m-4]}\Bigr]
   =\delta_{c=d=e=f}X_c^Y,                                \tag{2}
\]

and hence the three tables are pairwise equivalent.  Simultaneity
therefore contains **no equation** beyond one table plus the shared
origin; the still-missing gate identified by the fan note could only be,
and by Theorem A is, a degree-two consequence of that shared origin.

**Corollary D (induced zero shore unreachable).**  In
[the induced-zero four-cut reduction](good-pair-fan-induced-zero-four-cut-reduction.md),
alternative 2 requires \(|F|\ge 7k\); since \(F=\varnothing\),
alternative 1 holds for every \(k\), and the growing zero-shore equation
is unreachable along the regular fan route.

**Corollary E (bridge-frontier stratum four is empty).**  In
[the injective-star Hessian bridge frontier](injective-star-hessian-bridge-frontier.md),
the fourth escape stratum — the nonbipartite sparse-row pattern for a
both-injective pair — is empty.  Every both-injective pair of a
hypothetical source has an extra internal Hessian kernel, a
disconnected or nonspanning rank-three graph, or a gauge-rigid chart
whose connected spanning rank-three graph is bipartite; on the last
chart the
[bipartite rank-drop theorem](source-hessian-bipartite-rankdrop.md)
forces a localized missing row.

**Corollary F (a global bound on regular charts).**  At most
\(\lfloor 3N/2\rfloor\) unordered pairs of an exact ternary source can be
regular nonbipartite at all.  Indeed Theorem A makes both orientations of
such a pair deficient, and by the essential-star bound each vertex has at
most three deficient partners.

Everything is stated for arbitrary endpoint-ordered aggregate complex
blocks: parallel sources, zero cells, endpoint asymmetry, and arbitrary
complex cancellation are retained, exactly as in the cited theorems.

## 2. Imported inputs

All inputs are previously proved and independently audited.

1. **Pair contraction identity.**  Deleting \(\{y,z\}\) and writing
   \(p_c,s_d\) for the endpoint-oriented rows into \(W\) and
   \(a_{cd}=A_{y\mid z}(c,d)\),

   \[
    a_{cd}\,q^{[t]}+p_cs_d\,q^{[t-1]}=\delta_{cd}X_c^W,
    \qquad X_c^W=\bigotimes_{x\in W}e_c^{(x)}.             \tag{3}
   \]

   This is equation (7) of
   [the source-Hessian dichotomy](source-derivative-hessian-dichotomy.md)
   in divided-power form; it sorts every perfect matching by whether it
   uses the direct edge, and no term selection occurs.

2. **Gauge kernel.**  \((Z^\alpha)_{ij}=(\alpha_i+\alpha_j)q_{ij}\) with
   \(\sum_i\alpha_i=0\) is always in the kernel of
   \(Z\mapsto Zq^{[t-1]}\); gauge-rigid means the kernel is exactly this
   space.

3. **Goodness.**  A pair is good when both deleted aggregate stars are
   injective, i.e. both triples \((p_c)\), \((s_d)\) are linearly
   independent; the
   [target-flattening theorem](target-flattening-essential-star-pair-bound.md)
   supplies at least \(N(N-7)/2\) good pairs and a fan of degree
   \(N-7\).

## 3. The three tables as one exact system

Fix the fan-branch configuration: centre \(r\), neighbours \(u,v,w\),
literal zero blocks \(A_{ru}=A_{rv}=A_{rw}=0\), and put
\(Y=B\setminus\{r,u,v,w\}\).  Decompose the source quadratic at the four
named vertices:

\[
 h=q_Y+\sum_ce_c^{(r)}p_c+\sum_de_d^{(u)}s_d+\sum_ee_e^{(v)}t_e
   +\sum_fe_f^{(w)}g_f
   +\sum_{d,e}b^{uv}_{de}e_d^{(u)}e_e^{(v)}
   +\sum_{d,f}b^{uw}_{df}e_d^{(u)}e_f^{(w)}
   +\sum_{e,f}b^{vw}_{ef}e_e^{(v)}e_f^{(w)}.               \tag{4}
\]

There are no \(r\)-to-named terms, and \(p_c\) is supported in \(Y\).
For the pair \((u,v)\), the fan note's response table lives on
\(W_{uv}=Y\cup\{w\}\) with

\[
 q_{uv}=q_Y+\textstyle\sum_fe_f^{(w)}g_f,\qquad
 s^{uv}_d=s_d+\textstyle\sum_fb^{uw}_{df}e_f^{(w)},\qquad
 t^{uv}_e=t_e+\textstyle\sum_fb^{vw}_{ef}e_f^{(w)}.       \tag{5}
\]

**Proof of Proposition C.**  Since two \(w\)-factors multiply to zero,
\(q_{uv}^{[k]}=q_Y^{[k]}+\bigl(\sum_fe_f^{(w)}g_f\bigr)q_Y^{[k-1]}\).
Substituting (5) into
\(R^{uv}_{de}=b^{uv}_{de}q_{uv}^{[m-2]}+s^{uv}_dt^{uv}_eq_{uv}^{[m-3]}\)
and sorting by the \(w\)-factor gives

\[
 R^{uv}_{de}
 =\underbrace{b^{uv}_{de}q_Y^{[m-2]}+s_dt_eq_Y^{[m-3]}}_{\hbox{$w$-free}}
 +\sum_fe_f^{(w)}\,T_{def},
\]

\[
 T_{def}
 =\bigl(b^{uv}_{de}g_f+b^{uw}_{df}t_e+b^{vw}_{ef}s_d\bigr)q_Y^{[m-3]}
   +s_dt_eg_f\,q_Y^{[m-4]}.                                \tag{6}
\]

The \(w\)-free part has degree \(2m-4=|Y|\), so multiplying it by any
\(p_c\) (supported in \(Y\)) exceeds the available sites and is zero
identically.  The table equation
\(p_cR^{uv}_{de}=\delta_{c=d=e}X_c^{W_{uv}}\) is therefore exactly its
list of \(w\)-sectors, which is the 81-row system (2), because the
\(e_f^{(w)}\)-sector of \(X_c^{W_{uv}}\) is \(\delta_{fc}X_c^Y\).  The
same computation for \((u,w)\) with \(v\)-sectors and for \((v,w)\) with
\(u\)-sectors produces the identical list (6).  Conversely (2) resums to
each table.  \(\square\)

The checker verifies (4)–(6) termwise at \(N=8\) against the fully
expanded \(h^{[4]}\) (all \(105\) perfect matchings; the two matching
classes of one table have sizes \(15\) and \(60\)), and the three sector
decompositions again at \(N=10\).  Thus the coexistence problem posed by
the fan note is, exactly, system (2) together with its physical
provenance: three regular nonbipartite good zero-block pairs at one
centre.

## 4. The exclusion

### 4.1 Degree-two products vanish on the regular chart

**Lemma 4.1.**  On a regular nonbipartite pair chart, for all
\(c\ne d\),

\[
                     a_{cd}=0
 \qquad\hbox{and}\qquad
                     p_cs_d=0                              \tag{7}
\]

identically in degree two.

**Proof.**  Since \(qq^{[t-1]}=tq^{[t]}\), the off-diagonal instance of
(3) says \(p_cs_d+\frac{a_{cd}}tq\in\ker(Z\mapsto Zq^{[t-1]})\).  Gauge
rigidity supplies \(\alpha\) with \(\sum_i\alpha_i=0\) and, on every
pair \(ij\),

\[
 (p_cs_d)_{ij}
 =\Bigl(\alpha_i+\alpha_j-\frac{a_{cd}}t\Bigr)q_{ij}.
\]

The left side has matrix rank at most two, so on every edge of
\(G_3(q)\) the scalar vanishes: \(\alpha_i+\alpha_j=a_{cd}/t\).  Setting
\(\beta_i=\alpha_i-a_{cd}/(2t)\), the \(\beta\)'s alternate along every
edge; connectedness on all of \(W\) plus an odd cycle force
\(\beta\equiv0\), so \(\alpha_i\equiv a_{cd}/(2t)\).  Summing over
\(|W|=2t\) sites and using the zero-sum gives \(a_{cd}=0\), hence
\(\alpha=0\) and \(p_cs_d=0\).  \(\square\)

This is the mechanism of Theorem 5.1 of
[the source-Hessian dichotomy](source-derivative-hessian-dichotomy.md)
and of the fan audit's equation (A3); it is replayed here because the
exclusion uses the full degree-two identity (7), not only the sparsity
it implies.

### 4.2 The annihilator trichotomy

For a nonzero linear form \(p=\sum_xp_x\) in the site-square-zero
algebra, let \(\operatorname{Ann}(p)\) be the space of linear forms
\(s\) with \(ps=0\).

**Lemma 4.2.**  Over a field of characteristic zero,

\[
 \operatorname{Ann}(p)=
 \begin{cases}
 0,&|\operatorname{supp}(p)|\ge3,\\[2pt]
 \mathbb C\,(p_x-p_y),\ \dim=1,&\operatorname{supp}(p)=\{x,y\},\\[2pt]
 V_x,\ \dim=3,&\operatorname{supp}(p)=\{x\}.
 \end{cases}                                              \tag{8}
\]

**Proof.**  Write \(ps=0\) as
\(p_x\otimes s_y+s_x\otimes p_y=0\) on every site pair \(\{x,y\}\).  If
\(x\in\operatorname{supp}(p)\) and \(y\notin\operatorname{supp}(p)\),
the pair \(\{x,y\}\) gives \(p_x\otimes s_y=0\), so \(s_y=0\): the
annihilator is supported inside \(\operatorname{supp}(p)\).  For a
single support site everything at that site multiplies to zero, giving
\(V_x\).  For support \(\{x,y\}\): if \(s_y=0\) then
\(s_x\otimes p_y=0\) forces \(s_x=0\); otherwise the rank-one equality
\(p_x\otimes s_y=-s_x\otimes p_y\) forces \(s_x=\lambda p_x\),
\(s_y=\mu p_y\) with \(\lambda+\mu=0\), the antipodal line.  For support
at least three, fix three support sites.  On each of the three pairs,
either both components of \(s\) vanish or both align
(\(s_x=\lambda_xp_x\), \(s_y=\lambda_yp_y\), \(\lambda_x+\lambda_y=0\)),
because one unmatched nonzero component would leave a nonzero simple
tensor.  A nonzero component therefore propagates alignment to all three
sites, and the three pair sums give \(2\lambda_x=0\); characteristic
zero kills every \(\lambda\).  So \(s\) vanishes on the three chosen
sites, and each further support site \(z\) dies through the pair
\(\{x,z\}\), whose condition reduces to \(p_x\otimes s_z=0\).
\(\square\)

The three branches of (8) carry parameter-uniform characteristic-zero
Singular certificates with fully symbolic entries (Section 7): the
site-separation branch on \(3\) localizing charts, the two-site branch
on \(9\) charts (all six \(2\times2\) alignment minors lie in the
saturation), and the three-site kill on \(27\) charts (all nine
annihilator variables lie in the saturation).  No anchor or value is
ever fixed.

### 4.3 The collapse

**Lemma 4.3.**  Let \(p_0,p_1,p_2,s_0,s_1,s_2\) be linear forms with
\(p_cs_d=0\) for all \(c\ne d\), and suppose the triple
\((s_0,s_1,s_2)\) is linearly independent while every \(p_c\ne0\).  Then
there is a single site \(x_*\) with all six forms in \(V_{x_*}\);
in particular \(p_cs_c=0\) for every \(c\).

**Proof.**  For each \(c\), the two forms \(s_d\), \(d\ne c\), are
independent elements of \(\operatorname{Ann}(p_c)\), so
\(\dim\operatorname{Ann}(p_c)\ge2\).  By (8) this forces
\(\operatorname{supp}(p_c)=\{x_c\}\) and \(s_d\in V_{x_c}\) for
\(d\ne c\).  Then \(s_2\in V_{x_0}\cap V_{x_1}\) is nonzero, so
\(x_0=x_1\); likewise \(s_1\) gives \(x_0=x_2\).  With
\(x_*=x_0=x_1=x_2\), every \(s_d\) lies in \(V_{x_*}\) (each \(d\)
differs from some \(c\)) and every \(p_c\) does.  Products of two forms
at one site vanish in the site-square-zero algebra.  \(\square\)

### 4.4 Proof of Theorem A

Suppose the chart is regular nonbipartite.  By symmetry of the relation
family \(\{p_cs_d=0:c\ne d\}\) under exchanging the two deleted
endpoints, it suffices to derive a contradiction from independence of
the \(s\)-triple.

If two of the \(p_c\) vanish, say \(p_{c_1}=p_{c_2}=0\), the two
diagonal instances of (3) read \(a_{c_ic_i}q^{[t]}=X_{c_i}^W\).  If some
\(a_{c_ic_i}=0\) then \(X_{c_i}^W=0\), false; otherwise \(q^{[t]}\) is
proportional to the two distinct pure colour words \(X_{c_1}^W\) and
\(X_{c_2}^W\), which are linearly independent.  Contradiction.

If every \(p_c\ne0\), Lemma 4.1 and Lemma 4.3 put all six rows in
one \(V_{x_*}\) and kill all three diagonal products, so all three
diagonal instances of (3) read \(a_{cc}q^{[t]}=X_c^W\); any two give the
same contradiction.

If exactly one \(p_{c_0}=0\), apply the argument of Lemma 4.3 to the two
nonzero rows \(p_{c_1},p_{c_2}\): each is one-site, at \(x_{c_1}\) and
\(x_{c_2}\); the nonzero form \(s_{c_0}\in V_{x_{c_1}}\cap V_{x_{c_2}}\)
forces \(x_{c_1}=x_{c_2}=x_*\), and then every \(s_d\) and both nonzero
\(p_c\) lie in \(V_{x_*}\).  The diagonal instances at \(c_0\) (zero
row) and at \(c_1\) (one-site product) again make \(q^{[t]}\)
proportional to two distinct colour words.  Contradiction.  \(\square\)

### 4.5 Proofs of the corollaries

*Corollary B.*  Fan pairs are good, so their \(s\)-triples are
independent; by Theorem A none is regular nonbipartite, i.e.
\(F=\varnothing\).  Item 2 of the fan dichotomy and its hereditary
variant are produced only under \(|F|\ge9\) resp. \(|F|\ge17\), so they
never occur; directly, the configuration named in item 2 contains the
regular good pair \(\{r,u\}\), impossible.  The three response tables
(19)–(20) of the fan note, and their capped six-port projections (23),
are defined exactly on that configuration; hence no simultaneous (indeed
no single) physical realization exists.  \(\square\)

*Corollary D.*  The four-cut theorem's shore alternative is derived from
\(|F|\ge7k\); with \(F=\varnothing\), alternative 1 holds for every
\(k\ge1\) with all \(N-7\) fan pairs escaping.  \(\square\)

*Corollary E.*  Proposition 3.1(2) of the bridge-frontier note is the
statement that a both-injective pair on a gauge-rigid chart with
connected nonbipartite \(G_3\) has the sparse-row pattern; Theorem A
shows this hypothesis set is unsatisfiable, and the remaining strata are
exactly extra kernel, disconnected/nonspanning \(G_3\), or connected
spanning bipartite \(G_3\) with its rank-drop missing row.  \(\square\)

*Corollary F.*  By Theorem A both deleted stars of a regular pair are
non-injective, so both directed orientations are deficient.  The
essential-star bound allows at most three deficient partners per vertex,
hence at most \(3N\) directed deficiencies and at most
\(\lfloor3N/2\rfloor\) doubly deficient pairs.  \(\square\)

## 5. Where the shared cofactors were used

The audit demanded that the exclusion use the common internal quadratic
and the shared physical cofactors, because exact guard models show that
nothing weaker can suffice.  The proof complies:

* the **common internal quadratic** enters twice — through gauge
  rigidity of its Hessian (Lemma 4.1 turns top-degree orthogonality
  \(p_cs_dq^{[t-1]}=0\) into the degree-two identity \(p_cs_d=0\)), and
  through the three diagonal cofactor identities
  \(a_{cc}q^{[t]}+p_cs_cq^{[t-1]}=X_c^W\), whose common factor
  \(q^{[t]}\) cannot serve two colours;
* the **shared physical cofactors** enter through (3) itself: the
  literal factorization \(a_{cd}q^{[t]}+p_cs_dq^{[t-1]}\) is used before
  any capping, and Proposition C shows the three tables carry exactly
  this pair-level information and no more.

## 6. Guard compliance

No previously falsified inference is reused.

1. **The three-port abstract response model** ((24) of the fan note)
   satisfies all 27 capped equations with \(p_c=e_c^{(c)}\) at three
   *distinct* sites.  It supplies no \(q\), no Hessian, and no
   degree-two products, so Lemma 4.1 never applies to it.  The exclusion
   here operates strictly upstream of the cap, so the guard stands and
   is respected.
2. **The common-origin factorization rank countermodel**
   ([note](common-origin-factorization-rank-countermodel.md)) has
   \(p_is_jq^{[2]}=\delta_{ij}z_0\cdots z_5\) with all three right sides
   on one top-degree line.  Its \(q\) is not gauge-rigid (\(q\) itself is
   an extra kernel vector since \(q^{[3]}=0\), and the bipartite
   six-cycle gauge sum obstruction makes it non-gauge), its local spaces
   are scalar, and its rank-three graph is empty; Theorem A's hypotheses
   fail on every count.  Its moral — use both the common origin and the
   sitewise colour separation before scalarizing — is exactly how the
   endgame here works: two distinct colour words at every site of \(W\).
3. **The complementary-support cross-product family** there satisfies
   \(A_iB_j=2\delta_{ij}X_i\) with genuine colour axes but no common
   \(q\); again outside the hypotheses, as it must be.
4. **The fourteen-site structural family**
   ([bridge frontier](injective-star-hessian-bridge-frontier.md), §6)
   has all 91 pairs both-injective and every internal rank-three graph
   disconnected.  It confirms that the escape charts of Corollary E can
   be occupied coherently — Theorem A forces every good pair into them,
   and that family shows this forcing is not vacuous.
5. **The all-pair missing-row countermodel**
   ([note](all-pair-missing-row-countermodel.md)) lives on the connected
   bipartite/missing-row branch and is untouched.
6. **Evidence discipline.**  The exclusion is a uniform
   characteristic-zero proof for every even \(N\ge6\).  The Singular
   saturations are computed over \(\mathbb Q\) with all entries
   symbolic, covering every nonzero-component chart; no anchor, value,
   or finite field is fixed in any closure step.  Finite-field sweeps in
   the checker are labelled sanity or nonvacuity evidence only, and the
   single mod-\(p\) rank is used only as an exact lower bound for a
   rational rank, which together with the exactly verified integer gauge
   annihilation yields the exact rational kernel statement.

## 7. Exact audit

The standalone checker
[fan_six_port_simultaneous_exclusion_check.py](../computations/fan_six_port_simultaneous_exclusion_check.py)
verifies, exactly:

* the pair identity (3) termwise against the fully expanded \(h^{[4]}\)
  of a random integer aggregate family at \(N=8\), at a centre pair and
  at a generic pair (18 cells, nonvacuously);
* the fan tables, the 81-row system (2), and Proposition C at \(N=8\):
  \(h^{[4]}\) equals the sum over all 105 perfect matchings, all three
  27-row tables match their contractions, all 81 four-slot contractions
  equal \(p_cT_{def}\), the three sector decompositions of the three
  tables coincide with the same \(T_{def}\) list, the \(w\)-free table
  parts are annihilated by every \(p_c\), and the one-table matching
  partition is \(15+60\);
* the same resummation identities again at \(N=10\) (81 sector
  identities and the spectator-free annihilation);
* Lemma 4.2 exhaustively over \(\mathbb F_3\) on three ambient sites
  (all \(19{,}682\) nonzero forms: \(17{,}576\) with support at least
  three and trivial annihilator, \(2{,}028\) two-site forms with the
  antipodal line, \(78\) one-site forms with \(V_x\)), over all
  \(4{,}160\) low-support forms plus \(2{,}000\) random support-three-or-
  more forms on four ambient sites, and by 60 exact rational nullspace
  samples on five sites;
* Lemma 4.3 by an honest annihilator-class census over \(\mathbb F_3\):
  the \(1{,}017\) nonzero annihilator classes (\(1{,}014\) antipodal
  lines and \(3\) coordinate factors) have pairwise-disjoint distinct
  members — the discovered adjacency is exactly the diagonal — and
  exactly \(3\) ordered class triples admit an independent
  \(s\)-transversal, namely the three all-\(V_x\) triples, for which
  every member form is one-site at the common site and every diagonal
  product vanishes;
* Lemma 4.3 again by 300 exact rational Rado-transversal trials on four
  sites (61 admitting, 239 blocked, equivalence with the one-common-site
  criterion asserted on every trial);
* nonvacuity of the regular chart hypotheses on the quadratic alone:
  integer families at \(|W|=4\) and \(|W|=6\) with every block of
  nonzero integer determinant whose Hessian kernel over \(\mathbb Q\) is
  exactly the vertex gauge space (ranks \(51/54\) and \(130/135\)
  mod \(1{,}000{,}003\) as exact lower bounds, gauge independence and
  gauge annihilation exact over \(\mathbb Z\)) — so Theorem A is a
  genuine incompatibility with the star data, not a vacuous chart;
* the three Singular certificates C1 (3 charts), C2 (9 charts, six
  minors each), C3 (27 charts, nine variables each) over \(\mathbb Q\),
  all returning PASS, with inputs and outputs hashed into
  [fan_six_port_simultaneous_singular_certificates.json](../computations/fan_six_port_simultaneous_singular_certificates.json).

Run from the repository root:

    uv run python computations/fan_six_port_simultaneous_exclusion_check.py

All checks print PASS.  The frozen artifacts have SHA-256 digests

    2ccfc0bd52bde05545e97ba09d62611fa00384a91b4cb9b966c6999e1123e45d  computations/fan_six_port_simultaneous_exclusion_check.py
    b0efbaf64c1f69db5c0ac6d999b88618092a17fa3b19d10ff52aabddba4c7382  computations/fan_six_port_simultaneous_singular_certificates.json

The finite sweeps audit the displayed algebra and ledgers; Lemmas
4.1–4.3 and Theorem A are the uniform characteristic-zero proofs.

## 8. Scope and next gates

* The theorem does not close Krenn's conjecture.  It empties one of the
  four strata: every good pair — at least \(N(N-7)/2\) of them, with a
  fan of degree \(N-7\) at some centre — now carries an extra internal
  Hessian kernel, a disconnected or nonspanning internal rank-three
  graph, or a connected spanning bipartite rank-three graph with its
  forced localized missing row.  The uniform descent must now be
  extracted from those three charts; the six-port interface is no longer
  a route.
* The abstract 81-row system (2) *without* the regular provenance is not
  excluded here, and its capped three-port shadow is genuinely
  consistent by the fan note's model (24).  Nothing in the route now
  depends on excluding it.
* Per the fan audit's palette discussion, all statements are relative to
  one chosen ternary projection; charts and escape strata may depend on
  the chosen colour triple.
* The natural next targets are Priority 2's second clause (lifting a
  leave-one-anchor kernel direction on the cubic equality branch) and a
  propagation theorem for the now-unavoidable extra-kernel/disconnected/
  bipartite structure across the \(\lceil N/5\rceil\)-clique of good
  pairs, in the spirit of Corollary E.
