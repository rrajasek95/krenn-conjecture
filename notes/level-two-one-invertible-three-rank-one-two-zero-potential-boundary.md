# The \(1I+3R+2Z\) potential boundary leaves one sharp dense support type

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome

Consider a binary six-site packet satisfying the generic-kernel equations

\[
 X_uJX_v^{\mathsf T}=(\nu_u+\nu_v)M_{uv},\qquad
 J=\begin{pmatrix}0&1\\1&0\end{pmatrix},                     \tag{1}
\]

with endpoint ranks

\[
                   (\operatorname{rank}X_0,\ldots,
                    \operatorname{rank}X_5)=(2,1,1,1,0,0).    \tag{2}
\]

Impose literal residual R2 in the original physical coordinates. Signed
partitions give an exhaustive potential/support census:

> **\(1I+3R+2Z\) potential boundary.** There are \(147\) labelled
> potential-support envelopes satisfying (1), or \(37\) modulo the
> natural \(S_3\times S_2\) action on the rank-one and zero sites.
> Thirty-three quotient envelopes satisfy
> \[
>                         \operatorname{rank}d\Psi_M\le52.     \tag{3}
> \]
> A fourth dense envelope has a common isotropic input pencil and satisfies
> \[
>                         \operatorname{rank}d\Psi_M\le42.     \tag{4}
> \]
> The split \(K_{2,3}\) dense envelope is a boundary specialization of the
> exact \(1I+5R\) antipodal-pencil syzygy theorem and has rank at most
> \(51\). The two-zero-rank-one \(K_4\)-shore envelope has a fixed
> rank-one root and also has rank at most \(42\). Up to relabelling, every
> rank-\(55\) survivor must therefore have the single potential/support
> form
> \[
> (\nu_0,\ldots,\nu_5)
>       =(\lambda,\lambda,\lambda,\lambda,-\lambda,-\lambda),
>       \qquad \lambda\ne0.                                   \tag{5}
> \]

The form in (5) represents one labelled envelope. It is sharp: an exact
rational selected-block packet on this envelope has differential rank
\(55\), satisfies all generic-kernel and selected level-two equations,
and realizes literal R2 at all six roots. Thus generic kernel, differential
rank, and R2 alone cannot close the last branch.

No L0 or L1 equation is used here. All closure bounds are
differential-rank bounds before R2; R2 only sharpens the surviving
physical-coordinate normal forms.

## 1. The broadened support graph

Write

\[
                         X_i=h_ib_i^{\mathsf T}
                         \qquad(i=1,2,3).                      \tag{6}
\]

Since \(X_0\) is invertible and every \(X_i\), \(1\le i\le3\), is
nonzero,

\[
                         X_0JX_i^{\mathsf T}\ne0.
\]

Equation (1) therefore forces

\[
                         \nu_0+\nu_i\ne0
                         \qquad(i=1,2,3).                      \tag{7}
\]

For a safe support upper bound, broaden the core

\[
                              Q=\{0,1,2,3\}                    \tag{8}
\]

to a complete graph. This forgets the rank-one factors on fixed core
blocks and can only increase differential support. Every edge incident
with a zero site \(z\in\{4,5\}\) has zero numerator in (1), so

\[
 M_{uz}\text{ can be nonzero only if }\nu_u+\nu_z=0.          \tag{9}
\]

Thus the broadened base-support graph is exactly

\[
 H=K_Q\ \cup\
   \{uz:z\in\{4,5\},\ \nu_u+\nu_z=0\}.                       \tag{10}
\]

This is the only support information used in (3).

## 2. Complement matching gives the rank-52 cutoff

A scalar tangent cell in the block \(\dot M_{uv}\) contributes to
\(d\Psi_M\) only if the four-site complement of \(\{u,v\}\) has a
supported perfect matching in \(H\). Call such an edge \(uv\) active and
write \(a(H)\) for the number of active tangent edges. Each active edge
has four binary cells, hence

\[
                         \operatorname{rank}d\Psi_M
                              \le4a(H).                         \tag{11}
\]

In particular, \(a(H)\le13\) proves (3).

Canonical signed partitions enumerate zero together with every nonzero
negation orbit \(\{\alpha,-\alpha\}\). They therefore enumerate all
possible zero-sum relations over arbitrary complex potentials, without a
numerical genericity assumption. There are \(4088\) signed partitions of
six labelled sites; \(2468\) satisfy (7), and they induce \(147\) distinct
graphs (10).

The exact active-edge histograms are

\[
\begin{array}{c|rrrrrrrrrrr}
a(H)&1&4&5&7&8&10&11&12&13&14&15\\ \hline
\text{labelled}&1&8&22&5&12&38&30&4&16&6&5\\
S_3\times S_2\text{ quotient}&1&2&5&3&2&7&7&2&4&1&3.
\end{array}                                                     \tag{12}
\]

Thus \(136\) of the \(147\) labelled envelopes, or \(33\) of the \(37\)
quotient envelopes, have \(a(H)\le13\). The remaining eleven labelled
envelopes form four quotient types.

## 3. The four dense quotient types

Let an “optional edge” mean an edge of (10) outside the broadened core
\(K_Q\). The four dense types are:

\[
\begin{array}{c|c|c|c}
\text{type}&(\nu_0,\ldots,\nu_5)&\text{optional graph}&a(H)\\ \hline
\text{all spokes}&
(\lambda,\lambda,\lambda,\lambda,-\lambda,-\lambda)&
K_{\{0,1,2,3\},\{4,5\}}&15\\
\text{two-zero-R }K_4\text{ shore}&
(\alpha,\beta,0,0,0,0)&
\{24,25,34,35,45\}&15\\
\text{five-site zero pencil}&
(\lambda,0,0,0,0,0)&
\{14,15,24,25,34,35,45\}&15\\
\text{split }K_{2,3}\text{ opposition}&
(\mu,-\lambda,-\lambda,\lambda,-\lambda,\lambda)&
\{15,25,34,45\}&14.
\end{array}                                                     \tag{13}
\]

The edge labels in (13) are concatenated site labels. Core edges such as
\(13\) and \(23\) are already present in \(K_Q\), even when their
potential sum vanishes.

## 4. The five-site zero pencil fixes root 0

In the third row of (13), sites \(1,2,3,4,5\) all have zero potential.
For the three nonzero rank-one endpoint matrices, (1) and (6) give

\[
 X_iJX_j^{\mathsf T}
  =(b_i^{\mathsf T}Jb_j)h_ih_j^{\mathsf T}=0
  \qquad(1\le i<j\le3).                                      \tag{14}
\]

Hence \(b_1,b_2,b_3\) are nonzero and pairwise \(J\)-orthogonal. In
dimension two, three such vectors share one isotropic line. Indeed, the
orthogonal line to \(b=(x,y)\) is generated by \((x,-y)\); two nonzero
vectors in that line are mutually orthogonal only when \(xy=0\). After
absorbing scales into the \(h_i\), write

\[
                              b_1=b_2=b_3=b.                    \tag{15}
\]

Since \(\nu_0\ne0\), the three rank-one spokes are

\[
                         M_{0i}=\nu_0^{-1}
                           (X_0Jb)h_i^{\mathsf T}
                           \qquad(i=1,2,3),                    \tag{16}
\]

while (9) gives \(M_{04}=M_{05}=0\). All five blocks incident with root
\(0\) therefore share the fixed left factor \(X_0Jb\), with the zero
blocks included harmlessly. The fixed-root support theorem yields

\[
                         \operatorname{rank}d\Psi_M\le42,      \tag{17}
\]

closing this fourth dense quotient type.

## 5. Split \(K_{2,3}\) opposition is an exact-syzygy boundary

In the fourth row of (13), the five noninvertible sites split as

\[
                  A=\{1,2,4\},\qquad B=\{3,5\}.              \tag{18}
\]

Their potentials are \(-\lambda\) on \(A\) and \(\lambda\) on \(B\),
where \(\lambda\ne0\); the root potential satisfies
\(\mu\ne\pm\lambda\).
Every one of the six cross blocks in \(A\times B\) is free. The two
rank-one cross equations give

\[
 b_1^{\mathsf T}Jb_3=b_2^{\mathsf T}Jb_3=0,                  \tag{19}
\]

so the one-dimensional orthogonal complement of nonzero \(b_3\) gives

\[
 b_1\parallel b_2\parallel b_A,\qquad
 b_3\parallel b_B,\qquad b_A^{\mathsf T}Jb_B=0.              \tag{20}
\]

This is a boundary point of the already closed \(1I+5R\) antipodal
\(K_{2,3}\) pencil. First suppose the two lines in (20) are
nonisotropic. Add auxiliary nonzero rank-one endpoint factors at sites
\(4,5\), on the lines \(b_A,b_B\), and scale both output factors by
\(\varepsilon\). Keep all six free cross blocks fixed. Every fixed block
incident with site \(4\) or \(5\) tends to zero with \(\varepsilon\),
while the four fixed blocks among root \(0\) and the three original
rank-one sites tend to their prescribed values. For
\(\varepsilon\ne0\), this is exactly a \(1I+5R\) \(K_{2,3}\) packet.

The isotropic subbranch is in the same closure. In a coordinate chart at
an isotropic line, take

\[
                         b_A(t)=(1,t),\qquad b_B(t)=(1,-t).    \tag{21}
\]

The two lines are orthogonal, distinct, and nonisotropic for \(t\ne0\),
and coalesce to the common isotropic line at \(t=0\). Same-shore fixed
blocks have the correct zero limit because their scalar self-pairing is
\(\pm2t\).

The exact \(1I+5R\) theorem supplies nine independent polynomial kernel
directions and proves rank at most \(51\) for arbitrary values of the six
cross blocks. Equivalently, every \(52\)-minor vanishes throughout the
nonzero \((\varepsilon,t)\) family. Those minors are polynomial in the
packet entries, so they also vanish at the zero-endpoint and isotropic
limits. Therefore the entire split branch satisfies

\[
                         \operatorname{rank}d\Psi_M\le51.      \tag{22}
\]

This closes all six labelled support envelopes of split type before R2.

## 6. The two-zero-rank-one shore has a fixed root

Relabel the second row of (13) as

\[
             (\nu_0,\ldots,\nu_5)=(\alpha,\beta,0,0,0,0),
             \qquad \alpha\beta(\alpha+\beta)\ne0.            \tag{23}
\]

At rank-one site \(1\), every incident block has the endpoint factor
\(h_1\). The block \(M_{10}\) is the transpose-oriented version of

\[
 M_{01}=(\alpha+\beta)^{-1}(X_0Jb_1)h_1^{\mathsf T},          \tag{24}
\]

and for \(j=2,3\),

\[
 M_{1j}=\beta^{-1}(b_1^{\mathsf T}Jb_j)h_1h_j^{\mathsf T}.    \tag{25}
\]

The zero endpoint matrices and \(\beta\ne0\) give

\[
                              M_{14}=M_{15}=0.                 \tag{26}
\]

Thus all five blocks at site \(1\), including the two zero blocks, lie
in one fixed local coordinate factor after a covariant normalization.
The fixed-root theorem gives

\[
                         \operatorname{rank}d\Psi_M\le42.      \tag{27}
\]

This closes all three labelled envelopes of this type without R2. The
arbitrary four-site zero-potential shore does not affect the argument.

## 7. Exact structure of the sole residual type

### Type A: all spokes

All eight blocks from \(Q\) to \(\{4,5\}\) are arbitrary, while
\(M_{45}=0\). The three invertible-to-rank-one/core spokes are fixed
nonzero rank-one blocks; the rank-one-to-rank-one blocks are fixed
rank-one blocks, possibly zero if their scalar pairings vanish. The
support envelope has all fifteen tangent edges active. Because the two
zero-endpoint spokes from root \(0\) remain arbitrary, root-\(0\) R2 does
not by itself force its witnesses onto rank-one spokes.

This all-spokes envelope is the sole remaining quotient type and the sole
remaining labelled support envelope. Its arbitrary zero-multiplier spokes
prevent the support and fixed-root arguments above from closing it. Any
continuation must add information beyond this selected generic-kernel/R2
block, such as L0, L1, overlapping level-two equations, or omitted colour
pairs.

## 8. A sharp rank-55/R2 guard on the all-spokes envelope

Take the endpoint matrices

\[
\begin{aligned}
X_0&=\begin{pmatrix}-1&2\\1&-1\end{pmatrix},&
X_1&=\begin{pmatrix}1&1\\0&0\end{pmatrix},\\
X_2&=\begin{pmatrix}0&0\\1&2\end{pmatrix},&
X_3&=\begin{pmatrix}2&3\\2&3\end{pmatrix},&
X_4&=X_5=0,
\end{aligned}                                                  \tag{28}
\]

and the potentials in (5) with \(\lambda=1\). On every core edge
\(0\le u<v\le3\), set

\[
                         M_{uv}=\frac12X_uJX_v^{\mathsf T}.    \tag{29}
\]

This gives

\[
\begin{array}{c|cccccc}
uv&01&02&03&12&13&23\\ \hline
M_{uv}&
\frac12E_{00}&\frac12E_{11}&
\frac12\begin{pmatrix}1&1\\1&1\end{pmatrix}&
\begin{pmatrix}0&3/2\\0&0\end{pmatrix}&
\begin{pmatrix}5/2&5/2\\0&0\end{pmatrix}&
\begin{pmatrix}0&0\\7/2&7/2\end{pmatrix}.
\end{array}                                                     \tag{30}
\]

The eight core-to-zero blocks are free. For a deterministic dense choice,
put

\[
 M_{uv}=\begin{pmatrix}k&k+1\\k+2&k+4\end{pmatrix},
 \qquad k=11+7u+13v,
 \qquad 0\le u\le3<v\le5,                                   \tag{31}
\]

and set \(M_{45}=0\). Equations (28)--(31) satisfy all \(60\) scalar
identities (1). With \(z=-\sum_i\nu_i=-2\), direct expansion verifies all
\(64\) selected level-two rows. Exact row reduction gives

\[
\operatorname{rank}_{\mathbb Q}d\Psi_M
=\operatorname{rank}_{\mathbb F_{101}}d\Psi_M
=\operatorname{rank}_{\mathbb F_{1000003}}d\Psi_M=55.         \tag{32}
\]

The five displayed trace-zero vertex gauges are independent, so (32)
attains the universal rank ceiling.

The factor choices in (28) make the literal physical R2 witnesses
transparent. At the four nonzero roots use

\[
\begin{array}{c|cc}
\text{root}&\text{physical output }0&\text{physical output }1\\ \hline
0&01&02\\
1&10&12\\
2&21&20\\
3&31&32.
\end{array}                                                     \tag{33}
\]

Each listed oriented block is supported in only the indicated output
column, the two witnesses at a root use distinct neighbor labels, and all
\(64\) binary words give nonzero complementary cofactors for every listed
witness. At roots \(4,5\), the endpoint matrices vanish and the selected
pair is preserved. Hence literal R2 holds at all six roots without a
covariant reinterpretation of the physical axes.

This is a selected-block/R2 guard only. It is not a full eight-site
solution or a conjecture counterexample, and it is not claimed to pass L0,
L1, overlapping level-two blocks, or omitted colour pairs.

## Exact audit

The standard-library checker
[verify_level_two_one_invertible_three_rank_one_two_zero_potential_boundary.py](../computations/verify_level_two_one_invertible_three_rank_one_two_zero_potential_boundary.py)

- enumerates all canonical signed partitions and enforces (7);
- reconstructs the \(147\) labelled and \(37\) quotient support envelopes;
- audits every complement perfect matching and both histograms in (12);
- identifies the four dense quotient types and their labelled
  multiplicities;
- imports and pins the common-isotropic-pencil and fixed-root bounds used
  in (17);
- pins the exact \(1I+5R\) \(K_{2,3}\) syzygy program and audits its
  zero-endpoint and isotropic boundary specialization;
- applies the fixed-root theorem at the nonzero-potential rank-one site in
  (23)--(27);
- verifies that \(146\) labelled envelopes, or \(36\) quotient envelopes,
  are closed;
- constructs the exact all-spokes packet (28)--(31), checks all generic
  kernel and selected level-two rows, and proves the three ranks in (32); and
- audits the six literal physical R2 tables in (33) and every advertised
  complementary cofactor.

It passes normal, optimized, and isolated Python.
