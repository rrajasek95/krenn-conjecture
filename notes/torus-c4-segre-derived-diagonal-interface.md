# The torus $C_4$ flat locus is Segre; physical descent is relative Tor

## Result

The global flat branch of the local $C_4$ exchange has a clean structural
description. Let

$$
 A(i,j,k,\ell)=x_{01}(i,j)x_{45}(k,\ell),\qquad
 B(i,j,k,\ell)=x_{05}(i,\ell)x_{14}(j,k).
$$

On the nonzero coefficient torus, the equality $A+B=0$ says that one
four-way tensor is rank one in the two crossing balanced flattenings

$$
 (01)\mid(45),\qquad (05)\mid(14).
$$

Their ordinary intersection **on the coefficient torus** is exactly the
full four-factor Segre torus. Hence there are nonzero site vectors
$u_0,u_1,u_4,u_5$ and nonzero edge scalars
$\lambda_{01},\lambda_{45},\lambda_{05},\lambda_{14}$ such that

$$
 x_{rs}=\lambda_{rs}u_r\otimes u_s,
 \qquad
 \lambda_{01}\lambda_{45}
 +\lambda_{05}\lambda_{14}=0.                         \tag{1}
$$

Thus all flat coefficient freedom is site gauge plus the single $C_4$
holonomy (1). This is the coordinate-level gauge behind the flat one-sided
homotopy in `local-c4-coherence-curvature-relative-square.md`.

The derived intersection of the two balanced Segre loci is not transverse.
For three colours its excess conormal rank is 56, so its degree-one Tor is
large rather than zero. Therefore the proof must not ask for vanishing of
the Segre-pair Tor. The minimally relevant condition is instead the
source-provenance diagonal: the terminal readout must kill degree-one
homology created when the polarized source resolution is specialized to the
physical coordinate diagonal.

## 1. Rank-one torus intersection

This theorem is deliberately scoped to the dense coefficient torus. A
stronger zero-tolerant set-theoretic Segre-intersection theorem is separate
and is not used in the derived-diagonal conclusion below.

Write $L_A$
and $L_B$ for the character lattices of the two balanced flattening Segres.
A character orthogonal to both is a function admitting both decompositions

$$
 f(i,j)+g(k,\ell)=h(i,\ell)+r(j,k).                     \tag{3}
$$

Taking one-coordinate differences in (3) shows, over every field, that it
has the fully additive form

$$
 \alpha(i)+\beta(j)+\gamma(k)+\delta(\ell).             \tag{4}
$$

Consequently $L_A+L_B$ is the saturated full-Segre character lattice. In a
Laurent group algebra, the ideals of two lattices generate the ideal of
their sum, so the ordinary torus intersection is reduced and equals (1).

## 2. The unavoidable excess Tor

For $n$ colours, the ambient tensor torus has dimension $n^4$. A balanced
rank-one torus has dimension $2n^2-1$, and the full four-factor Segre torus
has dimension $4n-3$. The clean-intersection excess is therefore

$$
 e=2\bigl(n^4-(2n^2-1)\bigr)
       -\bigl(n^4-(4n-3)\bigr)
   =n^4-4n^2+4n-1.                                     \tag{5}
$$

For $n=3$, $e=56$. Since these are smooth subtori meeting cleanly, their
derived intersection has excess exterior homology

$$
 \operatorname{Tor}_i\cong\bigwedge^i E^*,\qquad
 \operatorname{rank}E=56.                              \tag{6}
$$

In particular, ordinary reduced intersection and Bianchi coherence do not
imply derived transversality. The 56-dimensional Tor in (6) is geometric
redundancy between the two balanced rank-one descriptions; it is not the
source-provenance obstruction which must vanish.

## 3. Minimal physical diagonal statement

Let $\widetilde R$ be the localized ring with a separate variable for each
source occurrence, let $L$ be the label-identification differences, and let
$\widetilde C\to\widetilde M_{\rm flat}$ be the polarized, source-labelled
relative complex on the flat $C_4$ chart. Put

$$
 S=\bigl(\widetilde R/(L,\Delta)\bigr)
       [(g a_c b_c)^{-1}],                              \tag{7}
$$

where $g$ is the common matching core and $\Delta$ is the chosen flat
minor. Two statements must be separated.

1. The undivided E2 cell already descends to a one-sided chain homotopy if
   there is a literal identification

   $$
   \widetilde C\otimes_{\widetilde R}S
      \cong C_{\rm phys,flat}.                          \tag{8}
   $$

   Tensoring a chain identity needs no Tor-vanishing hypothesis.
2. Two physical choices of that homotopy differ by
   $H_1(C_{\rm phys,flat})$. If $\widetilde C$ is a source resolution on
   this chart, derived base change identifies

   $$
   H_1\bigl(\widetilde C\otimes^{\mathbf L}_{\widetilde R}S\bigr)
   =\operatorname{Tor}^{\widetilde R}_1
      (\widetilde M_{\rm flat},S).                     \tag{9}
   $$

Let $\varepsilon$ be the complete physical terminal readout. The exact
necessary-and-sufficient zero-indeterminacy condition is

$$
 \varepsilon\left(
   \operatorname{Tor}^{\widetilde R}_1
      (\widetilde M_{\rm flat},S)_{C_4\text{-grade}}
 \right)=0.                                             \tag{10}
$$

Vanishing of the displayed Tor group is sufficient but stronger than
needed. Vanishing of every higher Tor is stronger still. If the polarized
complex has primitive $H_1$ before base change, then (10) must be replaced
by the same condition on the total degree-one homology of
$\operatorname{Tot}(\widetilde C\otimes K(L,\Delta))$; its filtration has
both primitive and diagonal-Tor pieces.

This explains the chart-26 colon guard. E3/E4 prove that the cellular
boundaries are coherent, but that chart retains primitive degree-one
homology, so the resolution hypothesis preceding (9) is not available.
The missing theorem is precisely a source-saturated completion which either
kills that primitive class or proves that the physical terminal readout
annihilates it.

## 4. Interface with the coherence--curvature square

The combined local theorem now has no hidden algebraic step.

* If a $C_4$ minor is nonzero, E2 exposes the literal curved carrier.
* If every minor vanishes on the coefficient torus, (1) gives the full
  site gauge and E2 supplies the one-sided flat homotopy.
* E3/E4 make the chosen homotopies coherent.
* Equation (10), not ordinary Segre geometry and not bare $d^2=0$, is the
  minimal zero-indeterminacy statement needed for a physical clean-cap
  readout.

## Verification

Run

```text
python3 computations/verify_torus_c4_segre_derived_diagonal_interface.py
```

The checker verifies the balanced/full character ranks over the rationals
and four residue fields, the excess formula, a literal ternary flat gauge,
and pins the exact local C4/source-diagonal dependencies. It is a theorem
interface, not a construction of the missing physical contraction.
Its frozen ledger digest is
`24061d46bf525cc0b2f3e0126cfba67d920d4fb0f38c6f645108b9f2d24b80a8`.
