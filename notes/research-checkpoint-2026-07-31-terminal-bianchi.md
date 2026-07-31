# Research checkpoint: terminal cubic Bianchi bridge

Checkpoint date: 2026-07-31.

## Status

Krenn's conjecture is **open**.  The certified proof spine and its named
dependencies are unchanged.  In particular, `SP-CLEAN-BRIDGE` remains the
only missing conjecture-level implication; this checkpoint is research
evidence, not a supersession.

The pushed branch head at the start of this checkpoint is `517f6a4`.
Two new independently audited research commits are present:

* `9be1cba` — identifies the terminal \(h=3\) response class and proves

  \[
  \alpha R^{[2]}q+R^{[3]}
   ={1\over8}\sum_{|S|=3}\Theta_S(2\alpha R,R,q).
  \]
* `517f6a4` — identifies the exact physical normalization defect and proves

  \[
  [t^3](q+2tR+2\alpha t^2R)^{[3]}=8\chi,
  \]
  together with the explicit discrepancy for a physical two-jet
  \(q+tB+t^2A\).

Both checkers are dependency-free and pass normal, optimized, isolated,
and compile modes.

## Exact reduction now available

For an off-diagonal six-residual-site row, write

\[
 Q_j=R^{[j]}q^{[3-j]},\qquad
 \alpha Q_0+Q_1=0,\qquad
 \chi=\alpha Q_2+Q_3.
\]

The response-translation equations through order two leave precisely the
terminal coefficient:
\(\chi=-2Q_3=-(2/\alpha)[t^3]f\).  The same class is
the average of the twenty literal \(3+3\) binary midpoint Bianchi
coefficients above.  Thus the shortest local target is no longer an
unweighted Hamming-two sum, a global site derivation, or twenty separate
cut identities.  It is one **source-faithful averaged cubic landing**.

For a candidate physical midpoint jet, put

\[
 B=2R+\beta,\qquad A=2\alpha R+\gamma.
\]

Its exact aggregate error is

\[
\begin{aligned}
 \mathfrak D(A,B)={}&
 (2\alpha R\beta+2R\gamma+\gamma\beta)q\\
 &+4R^{[2]}\beta+2R\beta^{[2]}+\beta^{[3]}.
\end{aligned}
\]

It is enough to prove that the actual full-nine/adjacent construction
kills this aggregate in the target-zero middle quotient.  Literal equality
\(B=2R,\ A=2\alpha R\) is sufficient but unnecessarily strong.

## Shortcuts ruled out at the checkpoint

The cutwise analysis found the exact physical formula.  For
\(S=\{i,k,p\}\), vary only those sites by
\(e_c+t_s\lambda_s\).  Then

\[
 C_S=[t_it_kt_p]\operatorname{haf}q(z)
     =\Theta_S(A^\lambda,B^\lambda,q_c).
\]

But a complete selected row gives

\[
 \alpha C_S+M_{ab,S}=0,
\]

not \(C_S=0\): \(M_{ab,S}\) is the simultaneous coefficient of
\(p_as_bq^{[2]}\).  Diagonal rows also carry the pure-anchor correction
\(\delta_{rs}\delta_{rc}\prod_{s\in S}(\lambda_s)_c\).  Hence a valid
landing must retain the response companion and diagonal target terms.

Moreover, there is an exact rank-two clean packet

\[
 q=01+23+45,\quad
 u=(1,-1,2,0,1,1),\quad
 v=(1,2,-2,1,-2,1),\quad
 R=uv^{\mathsf T}+vu^{\mathsf T},\quad \alpha=-2,
\]

with response layers \((1,2,6,12)\).  It satisfies the selected source
relation and \(\chi=0\), while all twenty cut values are nontrivial and
cancel only in the total sum.  It even has a literal three-colour
selected-row embedding, but not the other eight rows, goodness, or three
anchors.  Thus neither individual-cut nor complementary-pair vanishing is
a viable theorem.

> **Update (2026-07-31, later the same day).**  The restart procedure below
> has been executed through step 5.  The two audit corrections were applied,
> the draft was independently re-audited (PASS) and committed as `951ae50`;
> a lower-compute continuation guide was added as
> [`terminal-bianchi-handoff-guide.md`](terminal-bianchi-handoff-guide.md)
> (start there); and step 6's four-hole attack produced the audited guard
> [`fourhole-cap-polarization-terminal-blindness.md`](fourhole-cap-polarization-terminal-blindness.md)
> (`e13b0de`).  The prohibition in the next section is therefore
> **discharged** — those files are committed.  Everything else below still
> stands, and the conjecture remains open.

## Double-polar draft (now committed as `951ae50`)

Two files contain a useful alternative formulation:

* `notes/three-anchor-apolar-double-polar-bianchi-reduction.md`;
* `computations/verify_three_anchor_apolar_double_polar_bianchi_reduction.py`.

They prove, for six-site scalar edge arrays,

\[
 H(H(A))_{ij}=\operatorname{haf}(A)A_{ij}+2\mathcal B_{ij}(A),
\]

and hence, for \(A_{\rm cap}=\alpha q+R\),

\[
 H(H(A_{\rm cap}))-2\mathcal B(A_{\rm cap})
   =\chi A_{\rm cap}.
\]

This turns cleanliness into an explicit corrected four-hole equality and
may be the most economical interface with adjacent four-cut rows.

**Historical (now discharged; see the update above).**  At the time of
writing: do not commit these two files yet.  The algebra subaudit passed every
substantive identity, packet, and checker calculation, but requested two
small corrections:

1. state equation (4) for \(i\ne j\) and define
   \(\mathcal B_{ii}=0\) before using the matrix identity; and
2. replace wording that the reciprocal Hankel component "equals" the
   averaged Bianchi class by the exact statement that it is the
   \(Q_0Q\)-scaled radial image of that scalar class.  The actual displayed
   equation and checker assertion already contain the correct factors.

After those edits, commission a short independent re-audit before commit.

## Exact next lemma

The shortest remaining local statement is:

> In a genuine complete full-nine six-residual-site packet with all three
> diagonal anchors and source-faithful adjacent provenance, the sum of the
> physical response-companion terms, pure-anchor corrections, and landing
> errors equals the canonical twenty-cut aggregate; equivalently it kills
> \(\mathfrak D(A,B)\), or proves
> \(H(H(A_{\rm cap}))=2\mathcal B(A_{\rm cap})\).

This must be an **aggregate** theorem.  It must use the complete diagonal
sector: the audited seven-row physical guard has the selected all-word row,
all six off-diagonal rows, one diagonal anchor, good Segre stars, and an
adjacent decomposition, yet has \(\chi=-2\).

For the uniform conjecture, the resulting six-site identity still has to
be transported through the already isolated K6 four-cut/source-provenance
interface.  The \(h=3\) statement is the finite local normal form of that
uniform overlap lemma, not by itself a new certified dependency.

## Restart procedure

1. Read this file, `notes/consolidated-proof-frontier.md`, and
   `certification/BASELINE.md`.
2. Run
   `git status --short` and preserve the two untracked double-polar files.
3. Apply the two audit corrections above with `apply_patch`.
4. Run both new checkers under normal, `-O`, and `-I -S`, plus
   `py_compile` and `git diff --check`.
5. Independently re-audit the corrected double-polar draft; then commit and
   push it as research evidence only.
6. Resume two parallel attacks: the full-nine Bianchi companion sum and the
   cap double-polar/four-hole physical landing.  Use `gpt-5.6-sol` with
   ultra/max reasoning, non-fast mode, and keep all scripts lightweight.
7. Modify the certified spine only after an independently audited positive
   theorem explicitly supersedes a named dependency.
