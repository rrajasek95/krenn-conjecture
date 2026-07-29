# Independent audit of the wedge hole-block resolution

## Verdict

**PASS.** A clean-room reconstruction found no omitted matching term, hidden
zero assumption, unsafe division, unhandled \(q_{de}\) branch, or tensor-order
error in
[`wedge-equality-hole-block-resolution.md`](wedge-equality-hole-block-resolution.md).
The theorem is valid over the stated field under its imported equality-stratum
response identities. In particular, the proof does not assume any of
\(q_{ab},q_{bc},q_{de}\) to vanish.

The independent executable audit is
[`audit_wedge_equality_hole_block_resolution_independent.py`](../computations/audit_wedge_equality_hole_block_resolution_independent.py).
It imports neither the primary note nor its checker and uses a different
highest-bit matching recursion. Its frozen semantic-ledger digest is

```text
92e9ad11445b29cc87693fcbfe3a80be9ef21d664d799451b2f5f141910ce462
```

## Frozen inputs

The audited files had the following SHA-256 digests:

```text
15dafc75ee7b411c618996e9d3a51b9d1b6a21b072e586cf40c03ecab2b29176  notes/wedge-equality-hole-block-resolution.md
851a209b9a4b903636611fb010f9d7f781fd84ed877c2e948fec343b00355f10  computations/verify_wedge_equality_hole_block_resolution.py
3850e3c7028e8e696163e4225a573ceebacad47ba984a2958efcb530803265db  notes/rank-budget-path-triangle-exposed-grid-obstruction.md
43a56863977628839aa13f76fbfffc43a131279b0d393eb3fd1083a14e11745e  notes/full-rank-site-response-invisibility-countermodel.md
```

The independent checker itself has SHA-256 digest

```text
f57fb6b1e3a4963e340e1da0f0e8204f75e0848d14f2e9c6f35de74eec809d80
```

## 1. Imported response-grid step

The proof imports two facts from the preceding equality-stratum analysis:

1. the crossed-target lemma applied to the \(AB\) and \(BC\) grids makes
   \(A_0,B_0,B_1,C_1\) pure; and
2. for every non-omission pair \(P\), the complete response identity is
   \(N_P\otimes F_P=0\).

I re-read the cited path/triangle and full-rank-site notes. The identity is for
the **complete** four-site cofactor, so its use does not silently discard or
separately kill matching summands.

The two target pairings require \(A_0,B_0\) and \(B_1,C_1\) to have opposite
types. The two crossed zeros require \(A_0,B_1\) and \(B_0,C_1\) to have the
same type. There are exactly two assignments, exchanged by
\(P\leftrightarrow S\). Orienting one of them gives

\[
A_0,B_1\text{ \(P\)-pure},\qquad B_0,C_1\text{ \(S\)-pure}.
\]

The five zero cofactors then follow as follows.

* \(A_0\) and \(C_1\) pair nontrivially, hence
  \(N_{ac}\otimes F_{ac}=0\) gives \(F_{ac}=0\).
* If \(F_{bd}\ne0\), then \(N_{bd}=0\). Evaluation against \(B_0\) kills
  the \(P\)-component of \(D_2\), while evaluation against \(B_1\) kills its
  \(S\)-component. Thus \(D_2=0\), contradicting the nonzero \(DE\) target.
  Hence \(F_{bd}=0\); the identical argument gives \(F_{be}=0\).
* A nonzero \(DE\) response has at least one nonzero ordered cross product.
  After the allowed swap \(d\leftrightarrow e\), take
  \(P_{D_2}S_{E_2}^{\mathsf T}\ne0\). The pure partners \(C_1\) and \(A_0\)
  then give nonzero \(CD\) and \(AE\) evaluations, forcing
  \(F_{cd}=F_{ae}=0\).

No cancellation issue occurs in these last evaluations: one endpoint is pure,
so each displayed nonzero pairing consists of a single outer product. The
checker independently reconstructs the typed \(3\times3\) pair census: its
diagonal is \(ab,bc,de\), its sole off-diagonal collision is \(b\)-with-\(b\),
and its five remaining cells are exactly

\[
                         ac,ae,bd,be,cd.
\]

## 2. Matching and flattening audit

The independent bit-mask recursion reconstructs all fifteen perfect matchings
of six sites and all three terms of every one of the fifteen four-site
cofactors. It verifies the nine cofactors used later against monomial-support
sets. It also assigns each full matching to its unique \(b\)-edge and confirms
that every matching occurs exactly once in

\[
q_{ab}F_{ab}+q_{bc}F_{bc}+q_{bd}F_{bd}+q_{be}F_{be}+q_{bf}F_{bf}=q^{[3]}.
\]

After the five zeros are inserted, suppose both \(q_{ab}\) and \(q_{bc}\)
are nonzero. Across the flattening

\[
W_f\mid W_a\otimes W_c\otimes W_d\otimes W_e,
\]

the first target term occupies the \(f=e_0\), \(d=e_0\) slice and the second
occupies the \(f=e_1\), \(d=e_1\) slice. For any nonzero coordinate \(x_i\)
of \(x_a\) and any nonzero coordinate \(y_j\) of \(y_c\), the corresponding
\(2\times2\) minor is

\[
                         \lambda _0\lambda _1x_i y_j\ne0.
\]

Thus the two-target sum has rank two. The independent checker exhausts all
nine possible nonempty coordinate-support pairs and verifies these minors.
It separately verifies all 360 \(2\times2\) minors of a generic decomposable
correction \(z_f\otimes F_{bf}\) are zero. Therefore that correction has rank
at most one and cannot cancel the rank-two sum. This establishes
\(q_{ab}=0\) or \(q_{bc}=0\).

## 3. Single-survivor branch audit

Take \(q_{ab}=0,\ q_{bc}\ne0\). The star identity equates one nonzero pure
target tensor with \(F_{bf}z_f\). Nonzero pure-tensor factor-line uniqueness
therefore legitimately gives

\[
q_{bf}=\beta e_2^{(b)}e_1^{(f)},\qquad
F_{bf}=\gamma e_1^{(a)}y_ce_1^{(d)}e_1^{(e)},
\qquad\beta\gamma=-\lambda _1,
\]

so \(\beta,\gamma\ne0\).

The \(f/e_1\) quotient of the \(F_{de}\) equation is a nonzero pure tensor.
Its \(c=e_0\) coefficient and its nonzero \(c=e_2\) coefficient give an exact
elimination certificate

\[
y_2(ty_0)-y_0(ty_2-\lambda _2)=\lambda _2y_0,
\]

so \(y_0=0\) and \(y_c=\alpha e_2^{(c)}\) with \(\alpha\ne0\). The \(c/e_2\)
quotient then gives \(q_{ac}=x_ae_2^{(c)}\), and direct coefficient comparison
gives

\[
q_{af}=\frac{\lambda _2}{\alpha}e_2^{(a)}e_2^{(f)}
       -\frac{\beta}{\alpha}x_ae_1^{(f)}.
\]

The two \(q_{de}\) cases are genuinely exhaustive:

| Case | Earlier consequence | Quotient contradiction |
|---|---|---|
| \(q_{de}=0\) | \(q_{ce}\) has a nonzero \(e_2^{(c)}e_1^{(e)}\) factor and \(q_{ef}\) has \(f\)-factor \(e_1^{(f)}\) | \(F_{bd}=0\) retains \(s\lambda _2/\alpha\ne0\) modulo \(e_1^{(f)}\) |
| \(q_{de}\ne0\) | \(F_{ac}=0\) first gives \(D_d\ne0\), then tensor injectivity forces \(q_{ef}\) onto the \(e_1^{(f)}\) line | the \(F_{bc}\) target retains \((\lambda _2/\alpha)q_{de}\ne0\) modulo \(e_1^{(f)}\) |

Before this split, \(F_{cd}=0\) has quotient residual
\((\lambda _2/\alpha)e_2^{(a)}e_2^{(f)}E_e\), so it first forces
\(q_{be}=0\), then \(q_{ae}=0\) using \(\beta\ne0\). The checker verifies both
coordinates of \(E_e\), both possible nonzero pivots of \(D_d\), and all four
possible nonzero coordinate pivots of \(q_{de}\).

The involution \(a\leftrightarrow c,\ d\leftrightarrow e,\ 0\leftrightarrow1\)
was checked on the entire endpoint-space table, every target tensor, and the
five-zero set. It swaps \(q_{ab}\) with \(q_{bc}\), so it covers the opposite
single-survivor case without adding a hypothesis. Consequently both adjacent
blocks vanish.

## 4. Final syzygy audit

Once \(q_{ab}=q_{bc}=0\), the \(F_{de}\) target is the single product
\(q_{ac}q_{bf}\). Since that product is nonzero pure, both factors are nonzero
pure on their forced lines:

\[
q_{ac}=\alpha e_2^{(a)}e_2^{(c)},\qquad
q_{bf}=\beta e_2^{(b)}e_2^{(f)},\qquad
\alpha\beta=\lambda _2.
\]

The \(b\)-star identity then gives \(q_{bf}F_{bf}=0\). These factors live on
disjoint site sets, so tensoring by nonzero \(q_{bf}\) is injective and
\(F_{bf}=0\).

For each pair \(i,j\in\{d,e,f\}\), the complete zero cofactor gives the two
literal coordinate identities

\[
R_{ij}:=A_iV_j+A_jV_i=0,
\qquad
\alpha q_{ij}+U_iV_j+U_jV_i=0.
\]

Substituting the second identity into the \(e_1^{(a)}\)-coefficient
\(H=A_dq_{ef}+A_eq_{df}+A_fq_{de}\) gives the componentwise certificate

\[
\alpha H+U_dR_{ef}+U_eR_{df}+U_fR_{de}=0.
\]

The checker does not collapse \(A_i,U_i,V_i\) to scalars. It uses dimensions
\(\dim W_d=\dim W_e=2,\ \dim W_f=3\), verifies all sixteen components of each
family of pair relations, and verifies the displayed certificate separately
in all twelve coordinates of \(W_d\otimes W_e\otimes W_f\). Hence tensor-site
ordering introduces no gap. Imposing \(R_{ij}=0\) gives \(H=0\) because
\(\alpha\ne0\), contradicting the nonzero \(F_{bc}\) target. The block
\(q_{de}\) remains arbitrary throughout this calculation.

## 5. Zero/nonzero and division ledger

The only scalar denominator introduced in the coordinate reductions is
\(\alpha\). Its nonvanishing follows before division from the nonzero
\(F_{de}\) target. The uses of \(\beta\ne0\), \(D_d\ne0\),
\(q_{ce}\ne0\), \(q_{de}\ne0\), and \(q_{bf}\ne0\) are respectively justified
by pure-factor uniqueness or by the explicit case hypothesis. Each use is an
injectivity statement for tensoring by a nonzero vector; none divides by an
arbitrary tensor. The target scalars
\(\lambda _0,\lambda _1,\lambda _2\) are nonzero by hypothesis.

No step uses \(q_{de}^{-1}\), a nonzero coordinate common to every tensor, or
termwise vanishing inside a cancelling cofactor.

## 6. Reproduction

From the repository root:

```bash
.venv/bin/python computations/verify_wedge_equality_hole_block_resolution.py
.venv/bin/python computations/audit_wedge_equality_hole_block_resolution_independent.py
.venv/bin/python -m py_compile \
  computations/verify_wedge_equality_hole_block_resolution.py \
  computations/audit_wedge_equality_hole_block_resolution_independent.py
```

The independent run reports fifteen full matchings, fifteen cofactors, the
five forced zero pairs, nine flattening support cases, 360 rank-one minors,
both \(q_{de}\) branches, twelve final tensor components, and `PASS`.

## Promotion recommendation

Safe to promote as the unconditional closure of the wedge equality stratum,
subject only to the explicitly cited response-grid lemmas. The primary note
and primary checker were not edited during this audit.
