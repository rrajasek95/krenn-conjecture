# The large cubic cores at order eight are impossible

## 1. Outcome

Work under the hypotheses and notation of
[the flat boundary-core reduction](flat-cubic-boundary-core-order-eight-reduction.md).
Thus \(N=8\), the source is entry-minimal and globally flat,

\[
 C=\{u:\deg_{\rm good}(u)\geq3\},\qquad X=B\setminus C,
\]

and every \(u\in C\) has exactly three bad neighbours, carried by one
nonzero diagonal occurrence of each colour.

**Theorem 1 (large-core exclusion).**  The cases

\[
                         |C|=3\quad\hbox{and}\quad |C|=4       \tag{1}
\]

are impossible.

Together with the boundary-core theorem, this leaves only
\(|C|\in\{1,2\}\) in the globally flat order-eight branch.  The proof is
over arbitrary complex weights.  It never treats a matching monomial as
uncancellable when four or more residual vertices remain: every final
contradiction has residual size zero or two.

## 2. Selected fibres and the residual-pair obstruction

For each colour \(a\in\{0,1,2\}\), choose a nonzero monomial \(M_a\) in
the constant-\(a\) fibre.  At every \(u\in C\), its \(M_a\)-occurrence is
the forced cubic port

\[
 A_{u f_a(u)}=\lambda_{u,a}
 e_a^{(u)}\otimes e_a^{(f_a(u))},\qquad \lambda_{u,a}\ne0.     \tag{2}
\]

The three neighbours \(f_0(u),f_1(u),f_2(u)\) are distinct.  The selected
factors are occurrence matchings: differently coloured entries on one
physical \(X\!-\!X\) pair remain different occurrences.

Put

\[
 k_a=|M_a\cap\delta(C)|,\qquad
 r_x=\deg_{\rm bad}(x,C),\qquad
 b=\sum_a k_a=\sum_{x\in X}r_x.                              \tag{3}
\]

Every bad edge incident with \(C\) is exactly one of the ports (2), so
the two expressions for \(b\) agree without a multiplicity convention.
The pointwise degree estimate from the boundary-core theorem is

\[
                              r_x\geq |C|-2.                  \tag{4}
\]

Also \(k_a\equiv|C|\pmod2\).

We repeatedly use the following immediate form of exact core
factorization.

**Lemma 2 (zero-/two-residual obstruction).**  Suppose a compatible
selection of forced occurrences covers \(C\), covers \(Z\subseteq X\),
and uses at least two colours on \(C\).  Put \(Y=X\setminus Z\).

1. If \(Y=\varnothing\), the selection is impossible.
2. If \(Y=\{x,y\}\), then \(A_{xy}=0\).

**Proof.**  For the induced colouring \(\xi\), exact core factorization is

\[
 [e_\xi]H_B(A)=w(F_\xi)
 [e_{\xi|Y}]H_Y(A),\qquad w(F_\xi)\ne0.                       \tag{5}
\]

The left side is zero because \(\xi\) is mixed.  If \(Y=\varnothing\),
the residual is \(H_\varnothing=1\), a contradiction.  If
\(Y=\{x,y\}\), the residual is the single aggregate block \(H_Y=A_{xy}\).
Every nonzero entry of that block would make the corresponding coefficient
in (5) nonzero, so the whole block vanishes. \(\square\)

In particular, the pair in part 2 is good, because every zero pair is
good.  No uniqueness claim on a larger matching fibre is used.

## 3. Three cubic vertices: reciprocal forced-zero sets

Assume \(|C|=3\), so \(|X|=5\).  Equation (4) gives \(r_x\geq1\) for
every \(x\in X\), hence \(b\geq5\).  Each \(k_a\) is odd and at most
three, so some selected factor, say \(M_0\), has \(k_0=3\).

Write \(C=\{c_1,c_2,c_3\}\) and write the three crossing occurrences of
\(M_0\) as

\[
                         c_i y_i\qquad(1\leq i\leq3).         \tag{6}
\]

The \(y_i\) are distinct.  Let

\[
                          X\setminus\{y_1,y_2,y_3\}=\{p,q\}.  \tag{7}
\]

Consider any bad crossing edge \(c_i p\).  It is one of the other two
coloured ports at \(c_i\), since \(M_0\) does not cross to \(p\).  Select
that occurrence and retain the two \(M_0\)-occurrences \(c_jy_j\) for
\(j\ne i\).  This forced matching uses two colours on \(C\) and leaves
exactly the residual pair

\[
                              \{q,y_i\}.                      \tag{8}
\]

Lemma 2 therefore forces \(A_{q y_i}=0\).  Distinct crossing neighbours
of \(p\) give distinct indices \(i\), so \(q\) has at least \(r_p\)
nonbad neighbours inside \(X\).  Interchanging \(p\) and \(q\) gives

\[
 \deg_{\rm nonbad}(q,X)\geq r_p,\qquad
 \deg_{\rm nonbad}(p,X)\geq r_q.                             \tag{9}
\]

On the other hand, every \(x\in X\) has total bad degree at least
\(N-3=5\).  Of those bad neighbours exactly \(r_x\) lie in \(C\), so

\[
 \deg_{\rm bad}(x,X)\geq5-r_x,\qquad
 \deg_{\rm nonbad}(x,X)\leq4-(5-r_x)=r_x-1.                  \tag{10}
\]

Applying (10) first to \(q\) and then to \(p\), equation (9) yields

\[
                         r_p\leq r_q-1,\qquad
                         r_q\leq r_p-1,                       \tag{11}
\]

an immediate contradiction.  This one exchange closes all possible
values \(b=5,7,9\); no cut-profile classification is needed.

## 4. Four cubic vertices: the fourth matching exposes an active pair

Now assume \(|C|=|X|=4\).  Equation (4) says \(r_x\geq2\), so

\[
                              b\geq8.                         \tag{12}
\]

Choose a fourth occurrence matching \(R\) in
\(M_0\cup M_1\cup M_2\).  Its colouring is mixed.  Exact core
factorization says its uncovered set \(Y\subseteq X\) has size four or
six.  Here \(|X|=4\), so \(Y=X\): the matching \(R\) has no crossing edge
and its \(C\)-part consists of two internal \(C\)-edges.

Let \(e_C\) be the number of physical bad edges internal to \(C\).
Summing the exact bad degree three over \(C\) gives

\[
                              12=2e_C+b.                      \tag{13}
\]

The two internal edges of \(R\) show \(e_C\geq2\), while (12)--(13) give
\(e_C\leq2\).  Therefore

\[
                          e_C=2,\qquad b=8.                   \tag{14}
\]

In particular the two internal bad edges form the whole internal bad
graph on \(C\).  Also (4) and \(\sum_{x\in X}r_x=b\) force

\[
                              r_x=2\qquad(x\in X).             \tag{15}
\]

Every \(x\in X\) has total bad degree at least five.  Its two bad
neighbours in \(C\) leave a required three bad neighbours in the
four-set \(X\).  Hence every \(X\!-\!X\) pair is bad and therefore
aggregate-active.

Let the two internal \(C\)-occurrences of \(R\) have colours \(k\) and
\(k'\).  Retain the first, of colour \(k\).  At the two endpoints of the
other edge choose a common colour \(\ell\ne k\) whose ports cross to \(X\):
if \(k'=k\), either other colour works; if \(k'\ne k\), take the third
colour.  The two \(\ell\)-ports have distinct endpoints in \(X\), because
the constant-\(\ell\) fibre is nonzero and its forced occurrences cannot
conflict.

These three forced occurrences cover all four vertices of \(C\), use the
mixed colour pattern

\[
                              (k,k,\ell,\ell),                 \tag{16}
\]

and cover two vertices of \(X\).  Their residual pair lies inside \(X\),
where it is bad and active by (15).  This contradicts the two-residual
part of Lemma 2.  Thus \(|C|=4\) is impossible, completing the proof of
Theorem 1.

## 5. Lightweight occurrence audit and scope

The exact checker produces:

    python3 computations/verify_n8_flat_large_c_matching_cut_lemma.py
    |C|=4: 1232 normalized degree-feasible triples; 10 labelled cut profiles
    |C|=3: 2388 normalized degree-feasible triples; 7 labelled cut profiles
    order-eight large-C matching-cut obstruction: PASS

It keeps differently coloured parallel \(X\!-\!X\) occurrences distinct,
normalizes the first factor only by permutations preserving \(C\sqcup X\),
and retains every labelled choice of the other two factors.  It verifies:

1. in the four-core case, the selected occurrence union always contains
   a mixed matching with two or four crossing edges;
2. in the three-core case, no internal bad graph on \(X\) can meet the
   pointwise bad-degree lower bound while avoiding all residual pairs
   forced zero by the exchanges in Section 3.

The checker is only an independent finite audit.  Sections 3--4 give the
human proof.  This note does not use or close the curved branch, and by
itself it leaves the globally flat cases \(|C|=1,2\) to a separate
argument.
