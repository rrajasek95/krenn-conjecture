# Five mixed rows kill the chart-26 terminal carrier

## 1. Outcome

The quadratic matching-cycle block obtained by adjoining the six first
path-edge error directions to the solved 96-coordinate terminal face does
not need to be contracted in order to dispose of the selected Hamilton
carrier.  Five literal mixed hafnian rows have an exact polynomial
combination equal to a five-variable divisor of that carrier.

In support-normalized coordinates, put

\[
\begin{aligned}
A&=x_{01}^{11},& B&=x_{04}^{22},& C&=x_{17}^{22},\\
P&=x_{23}^{00},& D&=x_{36}^{11},& X&=x_{46}^{00},
&Q&=x_{57}^{00}.
\end{aligned}
\]

The unique normalized physical target monomial on the selected Hamilton row
is

\[
                              T=ABCPDXQ.                  \tag{1}
\]

The five-row identity proves

\[
                              BCDPQ\in I_{\rm mix}.       \tag{2}
\]

Consequently

\[
                              T=AX(BCDPQ)\in I_{\rm mix}. \tag{3}
\]

This is a pure-anchor bypass: it kills the terminal target carrier itself,
which is stronger for this selected row than constructing a clean-cap
correction for all six added coordinates.

The checker also lifts (2)--(3) before support normalization.  After
clearing three chart-support units, (3) is a literal integer polynomial
combination of the five mixed source rows.  Thus the result is honest
membership after localization only at chart-support coordinates, not an
artifact of setting the support variables to one.

## 2. The simultaneous 102-coordinate face

The face consists of

1. the twelve chart-support coordinates;
2. the seven variables of terminal row `04237475b8cfea`;
3. the 96 off-path coordinates exposed in
   `n8-chart26-terminal-triangular-exposure.md`; and
4. the six path-edge error directions

\[
x_{23}^{10},x_{23}^{11},x_{23}^{12},\qquad
x_{57}^{20},x_{57}^{21},x_{57}^{22}.
\]

All other coordinates are set to zero.  The six extra directions destroy
the raw triangular starting leaves by adding alternate-matching products.
For example,

\[
H_{11111210}
 =(1+x_{01}^{11}x_{36}^{11})
   (x_{57}^{20}+x_{27}^{10}x_{45}^{12}).
\]

The identity below does not orient or eliminate this entire quadratic
system.  It instead shows that its selected terminal carrier already lies
in the mixed ideal.

## 3. The five normalized source rows

Introduce the auxiliary abbreviations

\[
r=x_{27}^{11},\quad s=x_{45}^{11},\quad
c=x_{35}^{00},\quad d=x_{27}^{00},\quad
e=x_{56}^{12},\quad f=x_{26}^{12},\quad
v=x_{57}^{21}.
\]

On the 102-coordinate face, the following five mixed source coefficients
are exactly

\[
\begin{array}{rcl}
G_1=H_{00111111}&=&D(1+rs),\\
G_2=H_{12012120}&=&de,\\
G_3=H_{12111122}&=&C(e+fs),\\
G_4=H_{12112221}&=&fv+r,\\
G_5=H_{21002010}&=&B(PQ+dc).
\end{array}                                                \tag{4}
\]

Every displayed word is mixed.  Direct expansion gives

\[
\begin{aligned}
BCDPQ={}&(BCPQ)G_1
 +(BCDcv)G_2
 +(BDPQv)G_3\\
&-(BCDPQs)G_4
 -(CDev)G_5.                                  \tag{5}
\end{aligned}
\]

There are only four cancellation pairs in (5):

\[
\begin{array}{c|c}
\text{term from a positive summand}&\text{opposite term}\ \hline
BCDPQrs & -BCDPQsr,\\
BCDcvde & -CDev\,Bdc,\\
BCDPQve & -CDev\,BPQ,\\
BCDPQvfs & -BCDPQs\,fv.
\end{array}
\]

The sole unmatched term is (BCDPQ).  This proves (2) over the integers;
no division, characteristic assumption, or Gröbner-order choice enters the
normalized identity.

The structure is worth noting.  The row (G_1) carries the alternating
cycle factor (1+rs), (G_5) is one of the pure anchors (PQ+dc), and
(G_2,G_3,G_4) form a three-step bridge transferring the unwanted terms
between them.  The quadratic curvature is not individually zero; it cancels
against the pure anchor in a five-row chain.

## 4. Exact lift through the support torus

Use the support-unit notation

\[
\begin{array}{llll}
u_{01}=x_{01}^{00},&u_{03}=x_{03}^{11},
&u_{14}=x_{14}^{22},&u_{16}=x_{16}^{11},\\
u_{23}=x_{23}^{22},&u_{24}=x_{24}^{11},
&u_{56}=x_{56}^{22},&u_{57}=x_{57}^{11}.
\end{array}
\]

Before normalization, the same five rows are

\[
\begin{array}{rcl}
G_1&=&u_{01}D(u_{24}u_{57}+rs),\\
G_2&=&u_{03}u_{14}de,\\
G_3&=&u_{03}C(u_{24}e+fs),\\
G_4&=&u_{03}u_{14}(fv+r u_{56}),\\
G_5&=&B u_{16}(PQ+dc).
\end{array}                                                \tag{6}
\]

Multiplying these rows respectively by

\[
\begin{array}{rcl}
M_1&=&BCPQ\,u_{03}u_{14}u_{56}u_{16},\\
M_2&=&BCDcv\,u_{16}u_{24}u_{01},\\
M_3&=&BDPQv\,u_{14}u_{16}u_{01},\\
M_4&=&BCDPQs\,u_{16}u_{01},\\
M_5&=&CDev\,u_{03}u_{14}u_{24}u_{01},
\end{array}
\]

with signs (+,+,+,-,-), gives the polynomial identity

\[
\sum_{i=1}^{5}\epsilon_iM_iG_i
 =BCDPQ\,u_{01}u_{03}u_{14}u_{16}u_{24}u_{56}u_{57}.       \tag{7}
\]

The unique full physical lift of the selected target row is

\[
T_{\rm full}
 =ABCPDXQ\,u_{01}u_{24}u_{57}u_{23}u_{56}.                \tag{8}
\]

Comparing (7) and (8),

\[
\frac{T_{\rm full}}{\text{right side of (7)}}
 =\frac{AXu_{23}}{u_{03}u_{14}u_{16}}.                   \tag{9}
\]

The denominator in (9) consists only of chart-support coordinates.  More
concretely, multiplying (8) by (u_{03}u_{14}u_{16}) and multiplying each
term in (7) by (AXu_{23}) gives a literal polynomial identity.  This proves
localized membership without relying on an informal normalization step.

The unique pure matching triple used in (8) is

```text
0075cfea   0482b8ee   23747de9
```

for colours 0, 1, and 2 respectively.

## 5. What this resolves

The previous terminal audit left two possibilities for the six path-edge
directions:

1. construct a coherent contraction of their 102-coordinate quadratic
   matching cycles; or
2. find a source-theoretic reason that the terminal readout need not cross
   those cycles.

Identity (5) gives the second outcome.  On the selected face, the physical
Hamilton carrier is already a mixed boundary.  Any terminal straightening
whose target coefficient reaches this carrier can discard it directly,
without choosing a branch of the quadratic cycle or dividing by
(1+AD) or (1+BC).

This is stronger than the generic rational-function calculation
(I_{\rm mix}=(1)): (5) and (7) identify the exact polynomial divisor of
the target and use only five labeled rows.  In particular, no Hamilton-row
variable is inverted.

## 6. Scope

The conclusion is exact but local to the displayed coordinate face.

1. It kills the selected terminal carrier; it does not prove that every one
   of the 102 coordinate variables belongs to the mixed ideal.
2. Coordinates outside the support, Hamilton row, 96 off-path variables,
   and six displayed path directions remain set to zero.
3. Restoring arbitrary additional coordinates adds further perfect-matching
   terms to the five rows in (4) and (6).  Their cancellation is not asserted
   here.
4. This is one selected chart-26 terminal row, not yet a uniform theorem for
   every Hamilton row or every support chart.

The next useful theorem is therefore a propagation statement: characterize
when the five-row packet (4) is transported equivariantly to an arbitrary
terminal Hamilton row, and determine whether extra coordinates enter only
through already exposed triangular ideals.

## 7. Verification

Run

```text
python3 computations/verify_n8_chart26_terminal_pure_anchor_bypass.py
```

The checker reconstructs all five full hafnians from literal source words,
verifies the normalized and support-cleared identities coefficient by
coefficient over (mathbb Z), recovers the unique physical pure matching
triple, and checks the cleared target certificate.  Its frozen ledger digest
is

```text
e8fb7275325ed2e28b11bd9314a4d43c5dfa346563ccfb2923b3752c6f5263b1.
```
