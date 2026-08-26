# `Q23-PROTECTED-FACTOR`: formal (X_{23}) and the minimal physical extension

Status: **FORMAL RELATIVE CELL EXACT; NO EXISTING PHYSICAL CELL; MINIMAL
GENERATOR EXTENSION ISOLATED**

Parent evidence is the sealed Q23 package with manifest SHA-256
`f3b689175811cb8d28dbae605fac703c8339f2e5a259c4c0e644122f1779b500`.
This note remains entirely at canonical (h=3).

## Conclusion

There is one algebraically exact candidate.  Put

\[
 F=H_0-u,\qquad Q=\operatorname {Eq},\qquad
 \theta=\epsilon_F\wedge\epsilon_Q,
 \qquad d\theta=F\epsilon_Q-Q\epsilon_F.
\]

After the legitimate relative base change (Q=0), set

\[
 C_K=-\theta,\qquad dC_K=-F e_{Eq}.
\]

For

\[
 E_{23}=D_{\rm root}\otimes B_1,\qquad
 D_{\rm root}=(-1,1,-1,1),
\]

the formal cell

\[
 \boxed{X^{\rm der}_{23}=-E_{23}\otimes C_K}
\]

has

\[
 \boxed{dX^{\rm der}_{23}
 =E_{23}\otimes(H_0-u)e_{Eq}}.                  \tag{1}
\]

There are no other faces in the **relative Koszul object**.  Before the
base change there is a second absolute face (Q\epsilon_F); deleting it
without imposing (Q=0) would be invalid.

Equation (1) does not construct the requested physical cell.  The pinned
callable source registry places (C_K) in the cap-to-cap object and has

\[
                       e_C A e_R=0.                \tag{2}
\]

It also assigns none of the required response-to-cap word, fine, repeated,
root, private, target, (q), (W), ordinary-residue, anchor or ridge data.
Giving (C_K) horizontal response-to-cap degree by declaration is exactly
the previously isolated unlicensed exotic enrichment.

## Source-labelled inventory search

The directly pinned constructors give the following exhaustive answer for
the declared (h=3) grammar.

| candidate | differential shadow | physical type | result |
|---|---|---|---|
| relative (C_K=-\theta) | (-F e_{Eq}) | cap to cap | exact derived formula, wrong operation |
| response KS \(\epsilon_s\) | \(d\epsilon_s=-c_f\) | response to response | no cap landing |
| tied cap \(r_0\) | \(dr_0=F e_{Eq}\) | cap to cap | correct scalar, tied/private descendants |
| marked derived cap | selected coefficient maps to (B) | coefficient correspondence | Hom coordinate remains zero |
| old cap lift \(O_{-E}\) | ((E,E,-E)) | cap internal | extra lower (+E), ores (-E) |
| root/Weyl transports | diagonal recolouring | response to response | cannot cross orthogonal idempotents |
| standard mapping cylinder | fills a supplied map | functorial constructor | cannot manufacture the absent input map |

Thus no existing source-labelled generator has (1) with all other protected
descendants zero.

## Exact cut covariance

The site involution is

```text
sigma_sites = (2 5)(3 4),
sigma_roots = (0 1)(2 3),
sigma_pure  : B1 -> B4.
```

The root permutation sends (D_{\rm root}) to (-D_{\rm root}), while
(F,Q,C_K) are invariant.  With

\[
 E_{45}=D_{\rm root}\otimes B_4,\qquad
 X^{\rm der}_{45}=-E_{45}C_K,
\]

one obtains, coefficient by coefficient,

\[
 \sigma(E_{23})=-E_{45},\qquad
 \boxed{\sigma(X^{\rm der}_{23})=-X^{\rm der}_{45}},\qquad
 \sigma(dX^{\rm der}_{23})=-dX^{\rm der}_{45}.       \tag{3}
\]

The plus sign on the decorated-mononomial (q_{23}\to q_{45}) map and the
minus sign in (3) occur in different label layers and are compatible.

## AB and AC naturality are separate

Let \(\rho\in\{AB,AC\}\).  The formal extension has separate equations

\[
 dX_{23}^{\rho}=E_{23}^{\rho}F e_{Eq},\qquad
 dX_{45}^{\rho}=E_{45}^{\rho}F e_{Eq},\qquad
 \sigma X_{23}^{\rho}=-X_{45}^{\rho}.                \tag{4}
\]

If \(\tau_{AB,AC}\) denotes root transport, the formal naturality relation is

\[
 \tau_{AB,AC}X_c^{AB}=X_c^{AC},\qquad
 \tau_{AB,AC}dX_c^{AB}=dX_c^{AC},\qquad c=23,45.     \tag{5}
\]

The checker verifies (4) independently in the AB and AC coordinates and
verifies that (3) commutes with (5).  But (5) is a relation of the proposed
extension, not a theorem from the old source: the current root-labelled
operation quotient has dimension two.  Its AB and AC unit vectors have rank
two, whereas their root-forgetting sum has rank one.  Therefore one bare
instance or one unlabelled aggregate is insufficient.  The economical
description is one **root-natural schema with two literal instances**, not
one root-forgetting cell.

## Why the nearest physical lift is not clean

For one coefficient of (E_{23}), retain rows `(lower, Eq, ores)`.  The
nearest old cap lift and the two required repairs are

\[
 \begin{array}{c|ccc}
 &\text{lower}&Eq&\text{ores}\\ \hline
 P2_{\rm hidden}(-E)&-1&0&0\\
 O_{-E}&1&1&-1\\
 d_{B_1}(+E)&0&0&1.
 \end{array}
\]

Consequently

\[
 (-1,0,0)+(1,1,-1)+(0,0,1)=(0,1,0).                 \tag{6}
\]

The per-cut signs are forced by the pinned cap-label transfer:

\[
 d_{B_1}=-(p_5+n_5)|_{B_1}=+B_1,
 \qquad
 d_{B_4}=-(p_3+n_3)|_{B_4}=+B_4.                    \tag{7}
\]

Equations (6)--(7) prove coefficient compatibility, not availability.
(P2_{\rm hidden}), the independent invisible (K_{Eq}) face (n), and
the literal face-(5\to B_1), face-(3\to B_4) label map are proper faces
of the missing comparison.  Using the already dressed (K_{Eq}) cell as
(n) is circular, because its dressing used (6).

## Minimal generator-extension theorem

Let (G_{\rm phys}^{(3)}) be the pinned physical (h=3) operation grammar.
In the selected response/cap grade:

1. its operation algebra contains the two diagonal idempotents but no
   response-to-cap matrix unit; adjoining that unit raises rank (2\to3);
2. its pointed (P_f/K_{Eq}/D4) edge skeleton has edge order
   `(P_f bottom, K_Eq left, K_Eq right, D4 top)`, differential rank three,
   and primitive integral cycle

   \[
                         z=(1,-1,1,-1);              \tag{8}
   \]

   hence (H_1\cong\mathbb Z);
3. the AB and AC operation coordinates form a rank-two quotient.

It follows that any physical extension realizing (1) must add a nonzero
off-diagonal response-to-cap schema, must fill (8) with primitive coefficient
\(\pm1\), and must supply both labelled root instances.  A multiple
\(m z\), \(|m|>1\), leaves torsion and does not fill the integral square.

The exact new square relation, in the displayed edge order, is

\[
 \boxed{
 d\kappa_{c}^{\rho}
 =P_{f,c}^{\rho}-K_{Eq,L,c}^{\rho}
  +K_{Eq,R,c}^{\rho}-D_{4,c}^{\rho}},
 \quad c=23,45,\quad\rho=AB,AC.                     \tag{9}
\]

It belongs to one normalized root-natural constructor

\[
 \Phi_{KS,r_0}:\text{response KS}\longrightarrow
                 \text{cap AugP2}/K_{Eq},
\]

whose two-term chain-map faces must satisfy

\[
 \Phi_1(\epsilon_s)=r_0,
 \qquad
 \Phi_0(c_f)=-(H_0-u)e_{Eq}.                         \tag{10}
\]

The protected (q_{23}) proper-face relation is exactly

\[
 P2_{\rm hidden}(-E_{23})+O_{-E_{23}}
 +D_{\rm root}\otimes[-(p_5+n_5)|_{B_1}]
 =(0,E_{23},0),                                     \tag{11}
\]

and its sigma mate replaces (23,5,B_1) by (45,3,B_4).  Relations
(9)--(11), with no other protected readout after cancellation, are the
minimal physical extension interface.  They are not present in the pinned
grammar.

For comparison, the smallest merely formal relative dg extension can freely
adjoin the four labelled instances (X_c^\rho) with (4)--(5) and declare
all other readouts zero.  This is consistent because the right-hand side of
(4) is closed after (Q=0), but it is not source-derived and cannot be used
as a physical proof.

## Scope guard

This proves an exact formal boundary, a source-interface nonavailability
statement for the pinned callable grammar, and a minimal integral extension
theorem at canonical (h=3).  It does not construct the physical generator,
prove `Q23-PROTECTED-FACTOR`, prove `PAComp(3)`, extend to uniform (h), or
promote anything to the certified spine or the Krenn--Gu conjecture.

