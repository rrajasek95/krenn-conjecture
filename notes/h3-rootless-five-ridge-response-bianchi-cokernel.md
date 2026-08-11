# The five ridge defects are bar boundaries, but their response companions form a primitive cokernel

## Outcome

The five source-labelled ridge defects from commit c66cd44 are not themselves
the terminal obstruction. For every deleted site \(v\), the literal \(xv\)
colour interval and either path across the \(pq\) colour square give a
normalized-bar chain with boundary

\[
 -\Omega_v=-(a_{pq}^{22}-a_{pq}^{00})
             +(a_{xv}^{0m_v}-a_{xv}^{00}).             \tag{1}
\]

The two \(pq\) paths differ by the ordinary Bianchi square, so (1) is
independent of endpoint order. Thus the rank-five free ridge class is
formally killed.

The complete literal source comparison does not stop at (1). Choose a
perfect matching \(N\) of \(F_v=D\setminus\{v\}\), and retain the
contragredient source endpoint of the local-colour bar. Termwise covariance
forces its response companion to be

\[
 q_{v,N}=\prod_{ij\in N}a_{ij}^{m_i m_j}.               \tag{2}
\]

Hence the actual column in the selected ridge quotient is

\[
                         b_{v,N}=(-\Omega_v,q_{v,N}).   \tag{3}
\]

The fifteen \(q_{v,N}\) are distinct labelled monomials. The integral
matrix with columns (3) has rank \(15\) in a rank-\(20\) module, and its
cokernel is torsion-free of rank five. Primitive detecting functionals are

\[
 \boxed{\lambda_v=\Omega_v+
       \sum_{N\in\operatorname{PM}(F_v)}q_{v,N}.}       \tag{4}
\]

Every matching switch, shuffle change, and \(pq\) Bianchi square lies in
the kernel of (4). A clean ridge repair \((-\Omega_v,0)\) has
\(\lambda_v=-1\). Therefore no combination in the complete literal
response-companion/Bianchi module cancels the five ridges and also descends
through the source quotient.

Completing the endpoint comparison by the four residual-site response
operators makes its physical target zero: the seven acted input colours are
the word 1211222, which contains both \(1\) and \(2\). It does not remove (2).
That term is the all-derivation endpoint, equivalently the normalized
ordinary-residue/H0 class. Thus the desired coarse signature

\[
 (\operatorname{ainc},\widehat w,\operatorname{tgt},
       \operatorname{ores})=(-1,0,0,0)                 \tag{5}
\]

is not obtained. The first genuinely new face would be a reduced relative
ridge augmentation which kills (2) with zero ridge, target, and cap
boundary. Adjoining such a face is new source-resolution data; ordinary
colour bars or another Bianchi shuffle do not construct it.

This is a negative theorem for the complete standard literal module in the
five selected ridge degrees. It is not a theorem against a new higher
relative augmentation, not a global rootless closure, and not a proof of
Krenn's conjecture.

## 1. Literal endpoint paths

Put

\[
 t_{22}=a_{pq}^{22},\quad t_{02}=a_{pq}^{02},\quad
 t_{20}=a_{pq}^{20},\quad t_{00}=a_{pq}^{00}.
\]

The two paths in the \(pq\) colour square are

\[
 t_{22}\longrightarrow t_{02}\longrightarrow t_{00},
 \qquad
 t_{22}\longrightarrow t_{20}\longrightarrow t_{00}. \tag{6}
\]

Both have boundary \(t_{00}-t_{22}\); their difference is the square
boundary. The \(xv\) interval has boundary

\[
                 a_{xv}^{00}-a_{xv}^{0m_v}.            \tag{7}
\]

Subtracting (7) from either path in (6) gives (1). These are precisely the
two endpoint-decorated ridges of commit c66cd44; no residual matching or
support choice has been introduced. At the level which forgets source
companions, all five \(\Omega_v\) can therefore be cancelled.

## 2. Why the complete response route has a companion

For fixed \(v,N\), take the four residual sites in any order. At one site,
local covariance has output endpoint \(L\), contragredient source endpoint
\(D\), and edge \(E\), with

\[
                             dE=L-D.                   \tag{8}
\]

The matching \(N\) meets each residual site exactly once. Acting by \(L\)
reads the mixed colour on that edge; acting by \(D\) replaces the zero
source endpoint by the same mixed colour. Consequently all \(2^4\) corners
have the identical literal coefficient (2). This is the termwise form of

\[
                         L_{F_v}=D_{F_v}=h_vY_0.        \tag{9}
\]

The normalized bar kills endpoint differences, not a single endpoint:
\(\epsilon(L)=\epsilon(D)=1\) and \(\epsilon(E)=0\). Therefore the
endpoint prism (1), after source-faithful completion, replaces its output
ridge by the all-\(D\) companion (2). It cannot erase that companion.

There are three matchings \(N\) for each \(v\). All fifteen monomials are
distinct because their labelled vertex set determines \(v\), and their two
physical edges determine \(N\). Matching-route changes replace
\(q_{v,N}\) by \(q_{v,N'}\) while preserving (4). The Reynolds average
replaces the three terms by \(h_v/3\); it does not make their sum zero.

## 3. Complete integral module

Let \(R\) have basis \(r_v\), representing \(\Omega_v\), and let \(C\)
have basis \(c_{v,N}\), representing (2). In \(R\oplus C\), the fifteen
route columns are

\[
                         b_{v,N}=-r_v+c_{v,N}.          \tag{10}
\]

They are integrally independent because every column has a private unit
pivot in its \(c_{v,N}\)-row. Eliminating those pivots leaves five free
classes:

\[
 \operatorname{rank}\langle b_{v,N}\rangle=15,\qquad
 \operatorname{coker}\langle b_{v,N}\rangle
       \simeq\mathbb Z^5.                              \tag{11}
\]

Adjoining the five clean columns \(-r_v\) raises rank from \(15\) to
\(20\). This proves both primitivity and the absence of a hidden rational
or torsion cancellation.

The same calculation handles an arbitrary combination of formal tails.
If its coefficients are \(\gamma_v\), cancelling the \(v\)-ridge forces

\[
                 \sum_N\beta_{v,N}=\gamma_v.           \tag{12}
\]

Zero response companion forces every \(\beta_{v,N}=0\), hence every
\(\gamma_v=0\). But anchor normalization in (5) requires
\(\sum_v\gamma_v=1\). Thus no normalized combination evades (11).

Strict two-chart rows do not enlarge (10). In the selected fine degree the
committed full-nine census has injective one-chart block and doubled kernel
equal to componentwise chart differences; their common coefficient ledger
is zero. Local-colour shuffle changes give differences of columns in (10),
and the two \(pq\) orders give the zero square in (6). These are exactly the
available literal Bianchi/response variations in this quotient.

## 4. Target and source descent

The endpoint-only operation has a target on the two sites with \(m_v=2\).
The complete response operation includes the four residual sites. Its seven
input colours form the word 1211222, so the all-output endpoint kills the
diagonal ternary target. Every corner containing a \(D\) also kills the
target because source derivations act trivially on \(\Delta\). Hence (10)
has target zero.

The remaining \(c_{v,N}\) coordinate is load-bearing. It is the all-source-
derivation endpoint of (8), and under the committed split-cap landing it is
the ordinary-residue H0 class. A source-quotient comparison must
nullhomotope it, not omit it. The covariance cube cannot: all its corners
equal (2), and its positive-degree boundaries have augmentation zero. The
primitive equations (4) are therefore also the first source-descent
obstruction.

This agrees with the independent top-unit guard in commit c66cd44: the
selected fourth coefficient sends the mixed source equation to \(1\).
Cancelling the ridge commutators does not change that degree-zero
augmentation. The new relative face required after (11) must supply the
reduced augmentation absent from the normalized bar.

## Verification

Run

~~~~text
python3 computations/verify_h3_rootless_five_ridge_response_bianchi_cokernel.py
python3 -O computations/verify_h3_rootless_five_ridge_response_bianchi_cokernel.py
~~~~

The checker pins the third-cofactor obstruction, normalized local-colour
bar, termwise covariance, and first Bianchi/selector no-go. It reconstructs
both \(pq\) paths and the five \(xv\) intervals; enumerates all fifteen
labelled response companions; checks every residual L/D corner and the
complete target word; builds (10), every matching Bianchi difference, the
five primitive covectors (4), and several anchor-normalized rational
combinations. It runs with the standard library only.
