# The universal graph constructs the derived comparison, but not its physical augmentation

## Outcome

The universal graph proposal has a substantial positive core.  Let (H)
be the full physical matching polynomial map and let (Delta) be the GHZ
section of its target.  The derived pullback

\[
       Gamma_H\times_T^{\mathbf R}\Delta                         \tag{1}
\]

has the correct classical truncation (H=\Delta).  Its Koszul normal cell
is the canonical (K_{\rm Eq}), and functorial bar/principal-parts
operations are equivariant.  In this universal resolution the formal Weyl
bar really makes the odd private packet (Xi^-) a boundary.

What fails is the promotion of (1) to the **pointed augmented** physical
comparison needed by the proof.  The first failure is the marked/global
diagonal

\[
                         d(u_f-u),                              \tag{2}
\]

not the previously known residue covector (chi) or beta-Smith class
([ho_0]).  If (2) is granted, the next literal failure is the formal even
carrier's residual word `012112`, followed by its rank-six endpoint-ridge
and rank-five primitive-(Omega) packet.  Target/Eq base change cannot
alter those direct-summand rows.

The excess/diagonal Gysin proposal sharpens the intervening step.  It
canonically produces the coefficient-one repeated normal class, but its
target direction `2e4` forgets which of five physical source loops created
it.  In the actual tau-plus grade the missing choice is exactly the
same-grade transport `delta_plus`.

Checker:
[`verify_h3_universal_graph_derived_base_change_physical_descent_gate.py`](../computations/verify_h3_universal_graph_derived_base_change_physical_descent_gate.py).

## 1. The unaugmented derived construction is exact

Use graph coordinate (y).  The two equations are

\[
                         g=y-H,qquad s=y-Delta.       \tag{3}
\]

Their conormal difference is

\[
                         s-g=H-Delta,                 \tag{4}
\]

the physical source equation.  The Koszul square

\[
 d(\epsilon_g\wedge\epsilon_s)
       =g\epsilon_s-s\epsilon_g                        \tag{5}
\]

has square zero, and restricting one face of (5) gives the monic
reduced-Eq normal cell.  Because the group action preserves (H) and
(Delta), the construction is equivariant.  The regular quiver arrow
(U=u/t) and its first principal-parts matrix remain the previously proved

\[
 J_1(U)=\begin{pmatrix}U&0\\dU&U\end{pmatrix}.          \tag{6}
\]

Thus there is no obstruction to constructing the **unaugmented**
(k[\beta])-linear, rho-equivariant derived comparison.

The same statement resolves the apparent (Xi^-) problem in the universal
resolution.  For the two 341-term fine components,

\[
                         \tau Z_0=-Z_1,
\qquad d[\tau\mid Z_0]=-(Z_0+Z_1).                    \tag{7}
\]

Endpoint oddization of (7) cancels

\[
 \Xi^-={4\over3}(\xi-\bar\xi-s\xi+s\bar\xi).          \tag{8}
\]

So derived base change does not “kill (Xi)” by setting its polynomial to
zero; rather, the functorial occurrence-local bar provides its actual
boundary in the enlarged resolution.

## 2. Why pointedness is the first obstruction

The existing anchor theorem requires a morphism of pointed source
presentations.  If (f) is the marked matching occurrence and (u_f) its
private graph coordinate, pointedness must identify the central anchor with
the marked occurrence modulo the response ideal.  Its cotangent shadow is
exactly (2).

In coordinates `(f,G,u_f,H0,u)`, the already valid conormal rows are

\[
\begin{aligned}
 d(f-u_f)&=(1,0,-1,0,0),\\
 d(G+u_f)&=(0,1,1,0,0),\\
 d(H_0-u)&=(0,0,0,1,-1).
\end{aligned}                                         \tag{9}
\]

They have rank three.  The tangent

\[
                         (1,-1,1,0,0)                  \tag{10}
\]

kills every row of (9), but both the marked anchor and (d(u_f-u)) read
one on it.  Adding (2) raises the rank to four.

This is not merely a presentation-choice issue.  The point

```text
(f,G,u_f,H0,u)=(1,1,1,2,2)
```

satisfies (H_0=f+G=u) and (u_f=f), hence lies on the original physical
graph fibre, but it does not satisfy (u_f=u).  Derived pullback along the
marked diagonal therefore changes the classical source; it adjoins the
desired comparison instead of proving it.

Taking the whole occurrence orbit avoids changing the physical fibre.  The
equivariant aggregate equation

\[
                         \sum_\mu u_\mu=u              \tag{11}
\]

becomes (H_0=u) after graph elimination.  But (11) retains the
marked-minus-aggregate permutation representation and still does not imply
(u_f=u).  Full equivariance alone cannot select the pointed anchor.

## 3. The next obstruction after the marked diagonal

### Excess Gysin: correct normal class, missing physical label

For multi-affine factors, the divided-power identity is exact:

```text
D_4^[2](f g) = D_4^[1](f) D_4^[1](g).
```

Its coefficient is one.  However, the five source loop labels

```text
02, 03, 05, 23, 25
```

all map to the single target normal direction `2e4`.  The source-label map
therefore has rank one and a rank-four kernel.  Keeping the preimage labels
before multiplication retains this kernel; it does not define a canonical
section of the Gysin map.

This is load-bearing in the physical grades.  The two oriented resolutions
of the shared-`02` cell land in `B1` and `B4`, with even average

```text
v = (B1+B4)/2.
```

But the actual tau-plus omitted labels have repeated grades `01,04` and
loop `25`.  Their local resolutions land only in `B0,B2,B3,B5`, with

```text
w_local = (B0+B2+B3+B5)/4.
```

The required physical lift is consequently

```text
delta_plus = v-w_local
           = (-B0+2B1-B2-B3+2B4-B5)/4.
```

It is rho-even and has augmentation zero, but it has no source-valid
realization in the tau-plus word/repeated grade merely from the target
diagonal identity.  This is the first genuine excess-Gysin obstruction.

The Rees deformation of the diagonal does give an abstract integral normal
family, whose connecting morphism is its normal generator.  It does not
identify that generator with the selected physical `D0` line: `2e4` has
forgotten the source/root label, while the proper face retains the
wrong-word and ridge outputs below.  Formal Rees integrality therefore does
not remove the beta-Smith class.

Nor does the excess cell replace the odd bar.  The former is an order-two
repeated-diagonal cell; `Xi^-` is an order-six occurrence-local group-bar
face.  Both occur in the universal resolution, but identifying their
physical augmented images is exactly the missing comparison.

### Literal word and ridge obstruction

Even if (2) is supplied, the formal rho-even Hasse/Bianchi carrier is not
in the literal physical word summand.  Its residual word is

```text
012112, with colour counts (1,3,2).
```

Every selected midpoint word has exactly three sites in each of two
colours.  The full midpoint census has 60 words, and `012112` is not one of
them.  Therefore the coordinate (e_{012112}^*) modulo the midpoint
summand is a literal word separator.  The same carrier has endpoint-ridge
mismatch rank six and primitive-(Omega) rank five.

The graph base change (3)--(5) acts in the target/Eq conormal.  It cannot
remove a coordinate in the independent word or ridge summands.  The next
positive cells must therefore provide a source-labelled word change into
the 3+3 midpoint grade and cap the six ridge/five Omega directions.

This clarifies the hierarchy:

```text
universal derived K_Eq and rho bar             CONSTRUCTED
universal Xi^- boundary                        CONSTRUCTED
pointed marked/global diagonal d(u_f-u)        OPEN
excess 2e4 -> tau-plus physical delta_plus      OPEN
literal even word/ridge/Omega totalization     OPEN
labelled residue and beta saturation           chi / [rho0]
```

## 4. Why one cannot simply redefine the physical source

An ordinary quasi-isomorphism of source resolutions does not determine the
extra physical readouts.  On a contractible pair (d(a)=e), the underlying
complex is unchanged whether a newly declared external row reads zero or
one on (a).  The same ambiguity applies to the marked anchor, physical
(q), labelled residue, (W), word/fine/repeated labels, and eta/sigma.

Accordingly, choosing (1) as the source is legitimate only after proving an
**augmented** quasi-isomorphism to the literal physical presentation.  It
must carry all those rows and preserve the existing generator/Fredholm
alternative.  Unaugmented derived equivalence is insufficient.

## Conditional construction theorem

The universal route constructs the desired comparison provided the following
five hypotheses are proved in the literal source category.

1. The graph/bar/PP resolution is `G`-equivariant over `R=k[beta]` and its
   classical truncation is the original fibre `H=Delta`.
2. The comparison is pointed: the marked occurrence coordinate satisfies
   `u_f-Phi_beta^*(u)` in the complete response ideal.  Equivalently, its
   cotangent map kills `d(u_f-u)`.
3. The excess Gysin class has a source-loop-labelled lift.  On the actual
   tau-plus object this lift realizes `delta_plus` in the same word and
   repeated grade, rather than importing the shared-`02` representative.
4. All proper faces totalize: the word `012112`, the rank-six ridge packet,
   and rank-five Omega packet are capped while target, residue, `W`, and
   anchor retain their prescribed values.
5. The map is beta-integral and preserves the augmented physical readouts
   `q`, eta/sigma, and labelled residue.  Equivalently, the beta-special
   comparison is saturated and its Bockstein is the physical `V` face.

Under these hypotheses, take the Koszul cell of the graph/section
intersection, apply the functorial occurrence group bar, insert the labelled
excess Gysin lift, and totalize the proper faces.  Hypotheses 1 and 2 make
this a pointed source-algebra map; 3 and 4 make it a literal physical chain
map; 5 makes it an integral augmented map.  Its odd projection contains the
already computed `Xi^-` bar, its even projection is the full
`v=(B1+B4)/2` packet, and Bockstein naturality gives `V`.

The construction is therefore theorem-level and uniform, but hypothesis 2
is already a genuine new conormal equation, and hypothesis 3 is the first
new obstruction specific to the excess-intersection implementation.

## Sharp remaining theorem

Construct a pointed, (G)-equivariant, (k[\beta])-linear augmented
quasi-isomorphism from the universal graph/bar/PP derived fibre (1) to the
literal physical complex.  Its first cotangent component is (2).  Its next
even component must move `012112` into the selected midpoint summand and
cap the rank-six/rank-five ridge packet.  It must simultaneously transport
physical (q), (W), labelled residue, and eta/sigma.

Such a map would be the desired (Phi_\beta): its odd part already contains
(8), its generic even part gives the full (v=(B_1+B_4)/2) packet, and
Bockstein naturality gives the special (V) face.  The present result
constructs the universal source object and isolates the first two exact
physical descent failures; it does not construct that augmented map.

Run:

```text
python3 computations/verify_h3_universal_graph_derived_base_change_physical_descent_gate.py
python3 -O computations/verify_h3_universal_graph_derived_base_change_physical_descent_gate.py
python3 -I -S computations/verify_h3_universal_graph_derived_base_change_physical_descent_gate.py
```

Frozen ledger SHA-256 is
`38f5c6120d2022087c9a03439de6885816ec759994a8d8d79b23b9b15c6d1888`.
