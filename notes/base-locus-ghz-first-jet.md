# Primitive base-locus sources can have GHZ as their first output jet

## Outcome

There is no general first-jet bridge from a primitive integral source to an
actual characteristic-two GHZ realization.  Two explicit six-site sources
over `Z/4` satisfy

\[
                         H_6(A)=2\Delta_{6,3}\pmod4,        \tag{1}
\]

while at least one aggregate entry is odd.  Therefore their reductions
`bar A` are nonzero primitive source points with

\[
                    H_6(\bar A)=0,
 \qquad {H_6(A)\over2}\bmod2=\Delta_{6,3}.                 \tag{2}
\]

The special source lies in the polynomial base scheme, and the leading
projective output recorded by the graph closure is ternary GHZ even though
GHZ is not the matching tensor of `bar A`.  Projective properness, blowup of
the base ideal, or extraction of the first nonzero output jet therefore
does not produce the characteristic-two source needed by the conjecture.

## 1. A nine-cell diagonal model

All omitted cells are zero.  The following entries lie in `Z/4`:

\[
\begin{array}{c|c@{\qquad}c|c@{\qquad}c|c}
01&A^{00}=1&25&A^{00}=1&34&A^{00}=2\\
05&A^{11}=1&23&A^{11}=1&14&A^{11}=2\\
04&A^{22}=1&35&A^{22}=1&12&A^{22}=2.
\end{array}                                                \tag{3}
\]

The three monochromatic perfect matchings have product two.  Direct
enumeration of all fifteen matchings in every one of the `3^6=729`
coloring fibers shows that every mixed coefficient is divisible by four.
Thus (1) holds.  In particular `A_01^(00)=1`, so the source is primitive.

Modulo two, the six surviving cells are

\[
 01^{00},25^{00},05^{11},23^{11},04^{22},35^{22}.          \tag{4}
\]

They admit no perfect matching of the six vertices, which makes
`H_6(bar A)=0` transparent in this model.  Nevertheless each missing edge
of the three displayed monochromatic matchings enters with coefficient two,
giving the three first-jet GHZ terms.

## 2. A cross-color primitive model

The phenomenon is not tied to choosing a surviving diagonal cell.  A
second exact source is

\[
\begin{array}{c|c@{\qquad}c|c}
01&A^{01}=3&02&A^{11}=1\\
03&A^{00}=1&04&A^{22}=1\\
13&A^{22}=1&15&A^{00}=2,\ A^{11}=1\\
24&A^{00}=1&25&A^{22}=2\\
34&A^{11}=2&35&A^{01}=1.
\end{array}                                                \tag{5}
\]

Again every omitted cell is zero.  Direct enumeration gives exactly (1),
and the odd cross-color entry `A_01^(01)=3` witnesses primitivity.

The two models represent the two orbits of a nonzero source cell under the
common color permutation: equal endpoint colors and distinct endpoint
colors.  They were found by the exact bit-level search in
`computations/search_mod4_rank2_boundary.py --profile base-ghz`.

## 3. Exact audit and scope

`computations/verify_base_locus_ghz_first_jet.py` hardcodes (3) and (5),
recomputes every matching coefficient over the integers, checks (1)
modulo four, checks primitivity, and independently recomputes (2).  Run

~~~text
uv run python computations/verify_base_locus_ghz_first_jet.py
~~~

Neither displayed point lifts even one digit further.  For the diagonal
model (3), take the mixed coloring

\[
                         c=(1,2,2,0,0,1).                  \tag{6}
\]

Its sole nonzero matching product is
`05|12|34`, with value `1*2*2=4`.  Every matching has at most one odd
selected entry in this coloring.  Consequently the full derivative of
`F_c` at `A mod 2` is zero: replacing one factor by an arbitrary correction
still leaves an even factor among the other two.  For every integral `C`,

\[
                         F_c(A+4C)=4\pmod8,                \tag{7}
\]

whereas a GHZ multiple requires this mixed coefficient to vanish.

For the cross-color model (5), the same one-row obstruction occurs at

\[
                         c=(0,1,2,1,1,2).                  \tag{8}
\]

The only nonzero product is on `01|25|34`, with value `3*2*2=12=4 mod 8`,
and again every derivative coefficient vanishes modulo two.  Thus neither
model has a lift satisfying `H(A)=2 Delta (mod 8)`.

More generally, if some compatible branch lifted to sources satisfying

\[
                         H_6(A_k)=2\Delta_{6,3}\pmod {2^k}
                                                                  \tag{9}
\]

for every `k`, compactness would give a `Z_2` source with exact output
`2 Delta`; rescaling all aggregate matrices by a cube root of `1/2` would
give a characteristic-zero six-site ternary equality source, contradicting
the independently proved six-site theorem.  Hence every compatible branch
must eventually obstruct.  Determining whether the obstruction already
appears at a finite stage.  Equations (6)--(8) settle that test only for the
two displayed mod-four branches; they do not exclude other mod-four base
jets with a different low source.

The conclusion is nevertheless final for the proposed first-jet bridge:
the implication

\[
 \text{primitive source and leading projective output }[\Delta]
 \Longrightarrow H(\bar A)\ne0                            \tag{10}
\]

is false in the exact matching problem, even with all ternary coefficient
conditions imposed through first order.
