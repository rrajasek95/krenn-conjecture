# Sparse first rows force a fifth-order GHZ onset at the critical core

September 26, 2026. **Written branch theorem with exact full-color polynomial
certificates; independent audit pending. The universal rate law remains open.**

[Replay](../computations/critical-extension-search-2026-09-26/README.md) ·
[General fourth-order onset](critical-core-higher-jets-2026-09-26.md) ·
[Earlier rejected direction](critical-cone-extension-obstruction-2026-09-26.md)

## 1. The family covered

Let \(Q\) be the same critical six-site source: all ten core edges on
\(0,\ldots,4\) are \(aa\), with weights \(q_{ij}\in\{1,\omega,\omega^2\}\);
site 5 is isolated; \(Q^{[2]}=0\). Consider an analytic arc

\[
 A(t)=Q+tB+t^2C+t^3D_3+t^4D_4+\cdots.
\]

For the row whose color at site 5 is \(b\), suppose

\[
 B_{i5}(b,b)=0\quad\text{for every }i<5,
 \qquad L=\sum_{i<5}\alpha_i a_i,
 \quad \alpha_i=B_{i5}(a,b),
\]

where \(L\ne0\) and at most two \(\alpha_i\) are nonzero. Entries with
core color \(c\), other root-color rows, and all unspecified source entries
remain free. Thus this condition concerns only the row's restriction to
the binary palette \(a,b\). Every entry of \(C,D_3,D_4\) remains free.

**Theorem.** If \(H_2=H_3=0\), then \((H_4)_{b^6}=0\). Consequently
an arc with this first-row condition cannot have nonzero leading ternary
GHZ output before order five.

This is an extension of the general fourth-order onset on a specified
family of first directions. It is not a fifth-order theorem for every
direction at the critical core, nor an error-versus-signal rate bound.

## 2. Quadratic error determines the core excitation support

Write \(D_{ij}=B_{ij}(b,b)\) for the first-jet \(bb\) core weights.
For a pair \(e=\{i,j\}\), consider the output with \(b\) at \(i,j,5\)
and \(a\) at the other three sites. Its quadratic coefficient is

\[
 (H_2)_{w_e}=D_{ij}g_{V_5\setminus e},\qquad
 g_T=\sum_{k\in T}\alpha_k q_{T\setminus k},             \tag{1}
\]

where \(V_5=\{0,\ldots,4\}\). A base edge contributes the two remaining
ground colors; the root row contributes one ground color; the core \(bb\)
edge supplies the two excitations. No other first-jet cells contribute to
this word. Higher jets cannot contribute because \(DH(Q)=0\).

If \(L\) is supported at one vertex, (1) forces all surviving \(D\) edges
to touch that vertex. They form a star and contain no two disjoint edges.
The pure fourth-order \(b\) amplitude is therefore zero: it would require
two first-order core \(bb\) edges and a second-order root \(bb\) edge.

Now let \(L\) be supported at distinct sites \(i,j\), with both coefficients
nonzero. The three ratios

\[
               q_{jk}/q_{ik},\qquad k\in V_5\setminus\{i,j\},
\]

are pairwise distinct for this critical core. This follows directly from
its displayed weights and is checked for every pair. Therefore at most one
of the three quantities \(\alpha_iq_{jk}+\alpha_jq_{ik}\) can vanish.

If none vanishes, (1) permits only the edge \(ij\). Again the fourth pure
amplitude is zero. The remaining case is the resonance

\[
                     \alpha_iq_{jk}+\alpha_jq_{ik}=0     \tag{2}
\]

for one site \(k\). Let \(\{l,m\}=V_5\setminus\{i,j,k\}\).
Equation (1) then permits precisely two possible core \(bb\) edges:
\(ij\) and \(lm\). There are 30 labeled resonant branches.

## 3. The fourth pure amplitude is a multiple of cubic error

In a resonant branch, the only possible fourth-order pure contribution is

\[
                     (H_4)_{b^6}=D_{ij}D_{lm}C_{k5}(b,b).
\]

Let \(w\) put \(a\) at \(l,m\) and \(b\) at every other site.
The first root row cannot contribute to this word: its support is at
\(i,j\), where the word requires \(b\), whereas the row emits \(a\).
At third order the unique surviving matching uses the base edge \(lm\),
the first-jet edge \(ij\), and the second-jet edge \(k5\). Hence

\[
                      (H_3)_w=q_{lm}D_{ij}C_{k5}(b,b).
\]

Thus, with no division by any first-jet variable,

\[
 \boxed{(H_4)_{b^6}=\frac{D_{lm}}{q_{lm}}(H_3)_w.}       \tag{3}
\]

The only denominator is a nonzero base weight of modulus one. Cancelling
the cubic off-target coefficient kills the fourth pure amplitude, proving
the theorem. If one of the two permitted \(D\) edges is zero, the same
identity remains valid.

For example, take \(L=\gamma(a_0-\omega a_1)\), \(\gamma\ne0\).
Only \(D_{01},D_{34}\) survive, and

\[
                      (H_4)_{b^6}=D_{34}(H_3)_{bbbaab}.
\]

## 4. Exact evidence and search limits

The checker verifies all 30 resonant branches, including their 300 quadratic
word equations. Before the quadratic gate, each branch uses 531 formal
variables; 523 remain after the eight forced zero cells. All 405 entries
of the second, third, and fourth source jets remain independent. It also
checks the five single-support and ten nonresonant two-support cases.
A negative control restores forbidden first-jet entries and invalidates (3).

The numerical exploration scripts are separate. A generic finite-field
screen tested 960 directions and found 761 cubic extensions, none with a
nonzero quartic expression. Those counts do not prove vanishing over the
complex numbers. The exact result is the branch argument (1)--(3), not an
inference from sampling. A low-degree modular identity search likewise
does not establish characteristic-zero ideal membership or nonmembership.

Still open are denser first rows, rows with first-order \(bb\) entries,
and later orders in the branches covered here. The unrestricted square-root
law requires control of error relative to signal along all of these paths.
