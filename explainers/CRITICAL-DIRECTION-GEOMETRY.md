# What the difficult GHZ directions can look like

[All explainers](README.md) · [GHZ project](../research/ghz-rates/README.md) ·
[Proofs and exact replay](../computations/flat-core-rigidity-2026-09-27/README.md)

We can now classify all support graphs whose four-site responses vanish,
and control distance to several of the resulting families. This reduces
the possible first critical directions at every full-support single-color
GHZ boundary. Quantitative star estimates survive matrix rank loss, and
the GHZ onset bound now allows one star arm to disappear. A separate
attachment argument handles every four-site core that is not a star,
including those with singular internal response.

**Evidence:** written proofs with exact supporting checks; independent
audit pending. These are follow-ups to the completed Krenn–Gu proof.
The unrestricted GHZ square-root rate law remains open.

## Start with the smaller matching problem

On four sites, there are three perfect matchings:

$$
12|34,\qquad 13|24,\qquad 14|23.
$$

Each edge carries a matrix of amplitudes for its two endpoint colors.
For a fixed color at each site, multiply the two entries belonging to
each matching and add the three products. Repeating this for every
color choice gives the four-site matching tensor.

Write $\mathcal F_4(A)$ for all these tensors on all four-site subsets.
We call a source **four-site-flat** when every one is zero.
This means the matching terms cancel for every color choice.

Why study this smaller problem? A six-site amplitude is a sum of products
of three edge entries. Differentiating with respect to one entry leaves
the matching tensor on the other four sites. Thus $\mathcal F_4$ records
the first response of the six-site output to edge changes.

~~~mermaid
flowchart LR
    A["Six-site output: products of three edges"] --> B["Vary one edge"]
    B --> C["Four remaining sites: products of two edges"]
    C --> D{"Do all these responses vanish?"}
    D -->|Yes| E["Higher-order terms become essential"]
    D -->|No| F["Some changes are detected to first order"]
~~~

## Three families we can describe precisely

Every four-site-flat source is a star, uses at most four active sites,
or is the isolated five-site cube-root core. This holds for any palette
and any site count. Within the four-site class, the tensor equation
still needs to be solved; the invertible binary case has a complete
normal form.

| Family | What vanishing forces | Local freedom at six sites, in two colors |
| --- | --- | ---: |
| Complete five-site core | Every edge has rank one; incident edges share a local color direction. The sixth site is isolated. | 10 complex parameters |
| Complete four-site core with invertible two-by-two blocks | All blocks reduce to a fixed identity/antisymmetric pattern by local changes of basis. Both other sites are isolated. | 13 complex parameters |
| Star with five nonzero two-by-two arms, of any rank | Every edge between the leaves is zero. | 20 complex parameters |

“Invertible” means the matrix has no lost color direction. The parameter
counts describe the flat family inside the 60-dimensional space of binary
six-site edge entries; they are separate from the original rank-25 count
for a three-color six-site output derivative.

The five-site pattern uses the complex cube roots of unity:

$$
1+\omega+\omega^2=0.
$$

Its edges among sites $0,1,2,3$ come in opposite pairs with weights
$1,\omega,\omega^2$. The four edges to site $4$ have weight $1$.
These phases cancel every four-site matching sum. The classification
proves that any complete five-site flat core must have this form after
local changes of scale and color direction. There is no corresponding
complete real-weight five-site flat core.

The four-site exception uses

$$
I=\begin{pmatrix}1&0\\0&1\end{pmatrix},
\qquad J=\begin{pmatrix}0&1\\-1&0\end{pmatrix}.
$$

~~~mermaid
graph LR
    a["0"] ---|"I"| b["1"]
    a ---|"I"| c["2"]
    a ---|"I"| d["3"]
    b ---|"J"| c
    b ---|"-J"| d
    c ---|"J"| d
    e["4: isolated"]
    f["5: isolated"]
~~~

All six core blocks are invertible, yet the four-site output vanishes.
This is why a proof cannot assume that all flat sources use rank-one
edge blocks.

## The star estimates give an explicit measure of error

Take a center joined to $k$ leaves, with identity matrices on its arms,
and $q$ colors at each site. Let $B_{ij}$ be any extra block between
leaves. Orient it by $B_{ji}=B_{ij}^{\mathsf T}$.

The total squared norm of four-site outputs containing the center is
exactly

$$
T_\star=
\underbrace{[q(k-2)-2]\sum_{i<j}\|B_{ij}\|_F^2}_{\text{detects extra edges}}
+\underbrace{\sum_i\left\|\sum_{j\ne i}B_{ij}\right\|_F^2}_{\text{nonnegative correction}}.
$$

For six sites and two colors, the first coefficient is $4$. Therefore
small output response forces small total strength in the extra edges.
No choice of their complex phases can remove that first term.
An antisymmetric triangle attains the coefficient, so it is sharp.

For arbitrary nonzero arms, a new tensor identity gives the bound

$$
T_\star\ge\frac{a^6}{6M^4}\sum_{i<j}\|B_{ij}\|_F^2
\quad\text{at six sites},
$$

where $a$ is the smallest arm norm and $M$ the largest. Every arm may
have rank one. Only an arm approaching zero can make this constant
degenerate while the other arm norms stay bounded.

The idea is to multiply each four-site response by the two unused arms.
All terms then live on the same five leaves, with three copies of the
center. Symmetrizing those center copies turns the equations into sums
of three vectors. An exact sum-of-squares identity controls the vectors,
and a second estimate ensures symmetrization cannot hide their strength.

~~~mermaid
flowchart LR
    A["Four-site response: center plus three leaves"] --> B["Attach the other two arms"]
    B --> C["Symmetrize three center copies"]
    C --> D["Common tensor space for every response"]
    D --> E["Sum-of-squares bound controls all leaf edges"]
~~~

The [proof](../notes/rank-free-star-response-bound-2026-09-27.md)
extends the bound to every star with at least five nonzero arms.
Four arms do not suffice: the five-site cube-root example has nonzero
leaf edges that are completely hidden from the four-site response.

## At the rank-25 boundary, only two support shapes survive

The earlier work found a balanced, single-color source with all fifteen
edges present and zero output. Its derivative has rank 25, leaving many
directions undetected at first order.

Consider a path from this source whose first two output orders vanish.
Let $T$ be the first perturbation using only the two other colors.
First-order constraints remove edges $02,03,12,13$ from $T$.
Second-order constraints impose $\mathcal F_4(T)=0$.
Together they force:

~~~mermaid
flowchart TD
    A["First non-ground direction at the rank-25 example"] --> B["Four forbidden edges are zero"]
    B --> C["Every four-site matching tensor vanishes"]
    C --> D["Support uses at most four sites"]
    C --> E["Support is a star centered at 4 or 5"]
    D --> F["All six binary core blocks invertible: classified and locally stable"]
    E --> G["All five arms nonzero: rank-independent star estimate"]
    D --> H["All non-star four-site cores: attachment control gives an onset bound"]
    E --> I["Four arms: onset bound; three or fewer: still open"]
~~~

The proof uses a short cancellation obstruction. If three leaves each
connect to both centers, their pairwise equations would imply a nonzero
product equals zero. Hence at most two such leaves can occur.
If each leaf connects to just one center, all must choose the same one.

The exact replay exhausts the 2048 allowed edge subsets. It excludes
1932 and constructs flat scalar examples on each of the 116 survivors.
The support proof itself allows arbitrary colored blocks.

The later [global support theorem](../notes/four-site-flat-support-classification-2026-09-27.md)
extends the star-or-four-site conclusion to the first critical direction
at every full-support single-color zero. Its replay checks all 32768
six-site graphs and constructs all 348 flat supports. The special
rank-25 cofactor pattern adds the restriction on star centers.

## What changes when the fifth arm disappears?

A four-arm star can hide changes between its leaves. The complete
[kernel classification](../notes/four-arm-star-response-2026-09-27.md)
depends on the center color directions used by the arms:

| Four nonzero arms | Hidden leaf directions |
| --- | ---: |
| At least one arm has matrix rank two or more | 0 |
| All rank one, with a common center direction | 2 |
| All rank one, with two distinct center directions occurring twice each | 1 |
| Every other rank-one pattern | 0 |

In the two-pair case, put opposite signs on four leaf edges:

~~~mermaid
graph LR
    r["Center 0"] ---|"center color b"| a["1"]
    r ---|"center color b"| b["2"]
    r ---|"center color c"| c["3"]
    r ---|"center color c"| d["4"]
    a ---|"τ"| c
    b ---|"τ"| d
    a ---|"-τ"| d
    b ---|"-τ"| c
    e["5: isolated"]
~~~

All responses containing the center cancel. The leaf-only response is
quadratic: its norm is $2|\tau|^2$, while distance from the star is
$2|\tau|$. Thus a linear response-to-distance estimate really fails
here. A square-root estimate is the best possible.

The common-direction case has two hidden parameters. Some combinations
give actual five-site cube-root cores with zero response. Controlling
one chosen leaf edge removes those branches.

In the GHZ problem, we have more information than the four-site response
alone. Outputs with the center grounded specifically measure the leaf
response. Other mixed outputs control a leaf edge whose complementary
ground cofactor is nonzero. These equations supply the missing control.

The [new theorem](../notes/four-arm-ghz-distance-bound-2026-09-27.md)
therefore permits **four arms bounded below by a fixed fraction of the
non-ground source norm**. The fifth arm may be zero, all matrices may
have rank one, and no prior closeness to a flat star is required.

## A singular core can still have well-controlled attachments

Suppose four active sites form a flat source that is not a star.
Two more sites are isolated. The internal four-site equations can be
singular, making it difficult to measure distance to the exact solution
set. The [attachment theorem](../notes/four-core-attachment-ghz-bound-2026-09-27.md)
avoids needing that distance.

Connect a fifth site to the four-site core. Each new four-site
response consists of one new edge times one old core edge, summed
over three choices. This is linear in the new attachments.

~~~mermaid
flowchart TD
    A["Flat four-site core, not a star"] --> B["Add edges from a fifth site"]
    B --> C{"Can every new four-site response stay zero?"}
    C -->|No| D["Responses bound all attachments linearly"]
    C -->|Yes| E["The five-site source must be the cube-root core"]
    E --> F["One attachment block detects the entire hidden kernel"]
    F --> G["A GHZ output with nonzero ground cofactor controls that block"]
    D --> H["Both outside sites have small attachments"]
    G --> H
~~~

The earlier support classification makes this conclusion possible.
Any nonzero hidden extension would be an exactly flat source on five
active sites, and the cube-root core is the only such source that is
not a star. This works for any number of colors and does not require
invertible edge matrices.

Now return to six sites. Call the four-site core $B$, the two attachment
collections $X_r,X_s$, and the edge between the outside sites $Z$.
Every perfect matching takes one of two forms:

| How the outside sites are matched | Contribution |
| --- | --- |
| They join each other | $Z$ times the four-site output of $B$ |
| They join two different core sites | One edge from $X_r$, one from $X_s$, and the remaining core edge |

In the nontrivial regime of the proof, the GHZ constraints bound
$X_r$, $X_s$, and $Z$ by a constant times $\delta^2$, where $\delta$
is distance from the single-color source.
The core has size at most $\delta$. The second row therefore has size
at most a constant times $\delta^2\delta^2\delta=\delta^5$.
The measured four-site response controls the first row.

Thus internal singularities do not obstruct this particular onset
estimate. Constants are uniform over compact families of these cores;
they may deteriorate when the core approaches a triangle or a star.

## Triangles: discard the hidden output without losing the signal

A triangle has three outside sites. Each outside site can attach to the
three triangle vertices, and some of those attachments can be invisible
to the first response. The [triangle theorem](../notes/triangle-attachment-ghz-bound-2026-09-27.md)
handles every such rank loss.

First consider any two outside sites. If their attachments were both
large while all measured responses vanished, they would extend the
triangle to a flat five-site source. Our support classification says
this must be a complete graph. But a ground-output equation requires
at least one of its edges to be small. The contradiction controls the
**product** of the two attachment sizes. It does not need to control
each attachment separately.

The ground equations supply a second fact: two outside sites have a
small attachment at the same triangle vertex. Their remaining hidden
attachments then share fixed local color directions at the other two
triangle vertices.

~~~mermaid
flowchart TD
    A["Triangle with three outside sites"] --> B["A ground equation supplies a small edge in every five-site extension"]
    B --> C["Products of attachment sizes are controlled"]
    A --> D["Two outside sites share a small attachment at one core vertex"]
    D --> E["Their hidden output has a fixed local color factor"]
    E --> F["Project perpendicular to that factor"]
    F --> G["Hidden output vanishes; part of the GHZ signal survives"]
    C --> H["Remaining terms have fifth-power size"]
    G --> H
~~~

This projection is just a familiar linear-algebra operation. If the
unwanted local direction is $v$, keep only the part perpendicular to
$v$. That kills any tensor with factor $v$ at that site.
For the binary GHZ target $b^6+c^6$, the surviving squared norm is
always one: the two words remain orthogonal at the other sites, and
the squared lengths of the projections of $b$ and $c$ sum to one.

There is a concrete reason to use this step. An exact example has
non-ground source size proportional to $\tau^2$, while an unwanted
product output has size $4\tau^9$. That is larger than the fifth power
of the source size, which is proportional to $\tau^{10}$.
The projection removes the product output exactly. We can bound the
GHZ signal even though these auxiliary constraints do not give the
same bound on the entire output.

## Three arms: control products instead of every individual edge

The [three-arm theorem](../notes/three-arm-ghz-distance-bound-2026-09-27.md)
removes one more arm from the hypothesis. Three edges at a common
center, each at least a fixed fraction of the non-ground source norm,
now suffice. The other two arms may vanish. All matrices may have
rank one, and no assumption about a nonzero center cofactor is needed.

To see the new difficulty, take the center and its three active leaves
as a four-site core. Let $b$ measure the edges between those leaves.
An outside site has an arm of size $h$ to the center, and attachments
of combined size $y$ to the three leaves. Neither $b$ nor $h$ needs
to be small enough individually. The matching output, however, uses
their **product**.

Normalize the three strong arms. If both $b$ and $h$ are nonzero,
divide the leaf perturbation by $b$, the new arm by $h$, and the
remaining attachments by $bh$. All equations then compare objects
of controlled size. A completely hidden configuration would be an
exactly flat source on five active sites.

~~~mermaid
flowchart TD
    A["Three strong arms and internal leaf edges of size b"] --> B["Add one outside arm of size h and leaf attachments of size y"]
    B --> C["Rescale the two changes separately"]
    C --> D["If every response vanishes, the five-site support must be complete"]
    D --> E["A ground-cofactor equation requires a small edge"]
    E --> F["Control bh and y together"]
    F --> G["Repeat for the second outside site"]
    G --> H["The matching expansion has fifth-power size, up to the measured error"]
~~~

The existing support theorem makes this useful: a non-star flat
source on five active sites must contain every edge. A cofactor
constraint supplies the edge that prevents such an extension.
Compactness then turns this impossibility into a quantitative bound.

The weights matter. If the internal perturbation is multiplied by
$u$ and the outside arm by $v$, the hidden attachments scale by $uv$,
while the response involving only leaves scales by $u^2v$.
Dividing that last response by $b$ puts it at the right scale.
The actual mixed GHZ outputs bound it by the error plus a term
depending only on the relevant leaf edges.

Two exact examples explain why the ingredients cannot be dropped.
A two-pair color pattern hides every center-containing response but
has a nonzero leaf-only response. A complete cube-root source hides
all responses but violates the required small-edge constraint.
Together, the leaf response and the cofactor equation exclude both.

## Two arms: matrix rank supplies another route

The first [two-arm theorem](../notes/two-invertible-arm-ghz-bound-2026-09-27.md)
gives the same fifth-power estimate when the two binary arm matrices
are uniformly invertible. Their smaller singular values must each
be at least a fixed fraction of the non-ground source norm.
The constants may deteriorate as either arm becomes rank one.

Consider four sites with two possible pairings:

~~~mermaid
flowchart LR
    A["Pairing 1: G joins 0–1; Y joins 2–r"] --> C["Same four-site output: GY + HB"]
    B["Pairing 2: H joins 0–r; B joins 1–2"] --> C
    C --> D["Group sites as (0,r) versus (1,2)"]
    D --> E["HB has matrix rank one"]
    D --> F["GY retains the smaller singular value of G"]
    E --> G["Cancellation leaves a measurable residual"]
    F --> G
~~~

Regrouping a tensor as a matrix is called *flattening*. Here it turns
the second pairing into a rank-one matrix. If $G$ has rank two, the
first pairing has a component that a rank-one matrix cannot cancel.
The residual has norm at least
$\sigma_{\min}(G)\|Y\|$.
This is a quantitative statement: it bounds the hidden block $Y$
using an observed response.

Ground-cofactor equations select two outside sites with a controlled
attachment at the same core vertex. If that vertex is a leaf, the
matrix estimate controls its companion attachment and a product
involving the outside arm. If it is the center, the outside arms
are already controlled. Both cases supply the factors of size
$\delta^2$ needed in the six-site matching expansion.

One invertible arm also suffices when a ground cofactor row at one
of its endpoints is nonzero. That condition makes the ground equations
select the center or the leaf where the matrix estimate is available.
The second arm then only needs comparable norm.

There is also a precise description of the hidden linear directions:

| Two nonzero arms | Attachment kernel |
| --- | --- |
| At least one has matrix rank two | Zero |
| Both rank one, with different center color lines | Zero |
| Both rank one, with the same center color line | One degree of freedom per outside color |

The last case permits equal-and-opposite attachments that cancel
exactly. The middle case has no linear kernel, but this first proof
still needed the singular-value estimate at the leaf selected by the
ground equations. The next argument removes that restriction.

## Two arms: rescale the edge between the leaves

The [stronger two-arm theorem](../notes/transverse-two-arm-ghz-onset-2026-09-27.md)
now covers both of the zero-kernel rows in the table. A single invertible
arm suffices without any endpoint-cofactor condition. Two rank-one arms
also suffice if their center color lines are different. The constants
are uniform when the attachment map stays bounded away from losing rank.

Why was the zero-kernel calculation not enough on its own? It controls
the attachments to the two leaves in terms of the small edge between
those leaves. But that closing edge may still be too large to discard.

Call its size $\beta$, and let $t$ be the combined non-ground source
size. If $\beta$ is at most a constant times $\delta^2$, the earlier
estimates already work. Otherwise rescale the six sites so that the
closing edge grows from size $\beta$ to size $t$, while both strong
arms stay unchanged. We now have a triangle with three substantial
edges, where the previous triangle method applies.

~~~mermaid
flowchart TD
    A["Two strong arms; closing edge has size beta"] --> B{"Closing edge at most order delta squared?"}
    B -->|Yes| C["Direct fifth-power estimate"]
    B -->|No| D["Rescale the sites: make all three triangle edges substantial"]
    D --> E["Track the separate scaling of every response"]
    E --> F["Use the mixed output whose remainder contains only leaf-quartet edges"]
    F --> G["Control products of attachment sizes"]
    G --> H["Project away the shared local factor"]
    H --> I["Undo the scaling: fifth-power GHZ estimate"]
~~~

Rescaling alone would lose too much when we reverse it. The useful
extra fact comes from choosing the right mixed output. Put ground
color at the center and at one outside site. Every remainder term
then contains two mixed edges and a binary edge between the other
four sites. Neither strong arm appears in that remainder. This
keeps the bound at the smaller scale $\beta$ where it is needed.

The final local projection matters again. An exact auxiliary example
has total binary output of order $\delta^{19/4}$, larger than
$\delta^5$ near zero. Its output is a product using just one color.
The projection kills it while keeping part of the GHZ target. This
example explains why controlling the desired signal can be easier
than controlling the entire output.

## Shared center directions: identify the remaining term

The last row of the table is more delicate. Write the almost-hidden
leaf attachments as a fixed local direction times an outside vector,
plus an error. The single-attachment equation cannot bound that
outside vector by itself.

Two further pair equations supply complementary information. At the
limiting shared-center pair, after removing nonzero local factors,
they have the form

$$
uZ+W,\qquad -uZ+W.
$$

Adding them reveals $2W$; subtracting them reveals $2uZ$.
Since $u$ is nonzero, the two equations control both unknowns.
This elementary observation remains stable under small changes in
the arms.

Combining it with the projection gives the explicit bound

$$
|\lambda|\le C\varepsilon+C\delta^5+Ct\beta^2.
$$

Thus we recover fifth-power onset if the closing edge has size
$O(\delta^2)$, or if its squared size is controlled by the output
error. This first bound left $t\beta^2$ uncontrolled in general.
The next step uses more of the individual attachment equations to
remove that restriction.

## Two controlled attachments close the shared-center case

The [two-arm theorem](../notes/coherent-two-arm-ghz-onset-2026-09-27.md)
proves fifth-power onset whenever two arms at a common center each
have size at least a fixed fraction of $t$. Their matrix ranks do
not matter. This reduces the remaining onset directions to single
edges; the next theorem handles the invertible ones.

The improvement comes from retaining information in the estimates.
Let $h_r$ be the size of the center arm to outside site $r$.
The error in its hidden leaf attachment is bounded by

$$
C\left(\delta^2+\frac{\beta}{t}h_r\right).
$$

Replacing $h_r$ by $t$ would give the earlier, coarser bound.
Keeping it allows the ground equations to help: they select two
outside sites whose attachments at the same core vertex are small.

~~~mermaid
flowchart TD
    A["Two arms share a center color direction"] --> B["Ground equations select two controlled attachments"]
    B --> C{"At which core vertex?"}
    C -->|Center| D["Two outside center arms are small"]
    D --> E["Pair equations control the products in the output"]
    C -->|Leaf| F{"Is the third hidden attachment large compared with beta?"}
    F -->|No| G["All leaf attachments are small enough for triangle rescaling"]
    F -->|Yes| H["Pair equations force the other two center arms to shrink"]
    H --> E
    E --> I["Projected GHZ output has fifth-power size"]
    G --> I
~~~

The large-attachment case is especially useful. If its size is $w$,
one pair equation has the form

$$
h_rw\le Ct\delta^2+C\beta h_r.
$$

When $w$ is sufficiently larger than $\beta$, move the last term
to the left. It follows that

$$
h_r\le C'\frac{t\delta^2}{w}.
$$

Thus a larger hidden attachment forces the other center arm to be
smaller. The same argument applies at the second controlled site.
Every term left after the projection then contains enough small
factors to give the fifth-power bound.

If the hidden attachment is not large, all leaf attachments are
$O(\beta)$ and the earlier triangle rescaling applies directly.
These two alternatives cover every size. The argument does not
need to make each hidden component small separately.

## One invertible edge: remove a plane, retain part of the target

The [single-edge theorem](../notes/single-invertible-edge-ghz-onset-2026-09-27.md)
allows every other edge to become arbitrarily small. It requires
the selected edge's smaller singular value to stay at least a
fixed fraction of the non-ground source norm.
An invertible two-by-two edge matrix carries two independent local
color combinations.

First separate the two sites of this edge from the four outside
sites. An exact matching identity lets us remove the selected edge
by projecting perpendicular to its matrix. The GHZ amplitude is
then bounded by the measured four-site response times the total
size of the outside edges, plus the output error.
This already finishes the estimate when those outside edges are
$O(\delta^2)$.

Ground equations supply the extra control when some outside edges
are larger. If a ground cofactor row at an endpoint is nonzero,
it makes two attachments small. The singular-value estimate then
controls the necessary products.
If both endpoint rows vanish, the outside ground equations force
at least four small edges forming a cycle:

~~~mermaid
flowchart LR
    A["Site 2"] ---|"possibly large U"| B["Site 3"]
    C["Site 4"] ---|"possibly large V"| D["Site 5"]
    A ---|"small"| C
    A ---|"small"| D
    B ---|"small"| C
    B ---|"small"| D
~~~

The small edges give two bilinear response equations. They control
the remaining output up to a single product matrix $P=uv^{\mathsf T}$.
That product term can be larger than fifth-power size, so it must
be removed before taking a norm.

There is useful geometry in how it appears. The equations produce
an invertible matrix $C$ for which

$$
\det(C+sP)=\det C\quad\text{for every scalar }s.
$$

Thus the plane spanned by $C,P$ touches the set of rank-one matrices
along the direction $P$. Within this plane, every rank-one matrix
is a multiple of $P$. The two GHZ components, however, use the
independent matrices $bb^{\mathsf T}$ and $cc^{\mathsf T}$ at the
selected sites. The plane cannot contain both.

Project perpendicular to the whole plane. This removes the unwanted
product term while retaining part of the GHZ signal. The bound is
quantitative and sharp: **at least one quarter of the original
binary GHZ squared norm survives**.
An exact rearrangement of the matching sum cancels the term using
both potentially large outside edges; the remaining terms obey the
fifth-power bound.

This reduces the remaining onset directions to single **rank-one**
edges: one edge carrying a product of two local color vectors.
The next step uses which colors that product contains.

## A same-color entry reduces the remaining cases to thirty directions

The [adjugate criterion](../notes/binary-adjugate-ghz-onset-2026-09-27.md)
handles an edge with a substantial $bb$ or $cc$ entry, even when its
matrix has rank one. It applies the determinant method from the
repository's earlier cap-adjugate work.

For a fixed edge matrix $G$, take the following combination of the
four slices of the six-site output:

$$
G_{bb}H_{cc}+G_{cc}H_{bb}-G_{bc}H_{cb}-G_{cb}H_{bc}.
$$

An exact identity expresses it as products of four-site responses.
The terms using four attachments cancel between the two determinant
products. There is no need to invert $G$.

For the GHZ target, this combination detects exactly the same-color
entries. The resulting norm certificate is

$$
|\lambda|\sqrt{|G_{bb}|^2+|G_{cc}|^2}
\le \|G\|\varepsilon+\tfrac12 f_G^2,
$$

where $f_G$ is the combined four-site response norm for quartets
containing the selected edge. Its coefficient $1/2$ is sharp.
If the same-color strength on the left is a fixed fraction of the
non-ground source norm, the mixed-output bounds give fifth-power onset.

~~~mermaid
flowchart TD
    A["One nonzero binary edge"] --> B{"Any same-color entry?"}
    B -->|Yes| C["Adjugate response criterion"]
    B -->|No| D{"Both different-color entries nonzero?"}
    D -->|Yes| E["Invertible-edge theorem"]
    D -->|No| F["One cell: b at one endpoint, c at the other"]
    C --> G["Fifth-power onset in a neighborhood"]
    E --> G
    F --> H["Remaining: 15 site pairs × 2 color orientations"]
~~~

Thus the unresolved onset shapes are just thirty projective directions.
Each pattern still allows any complex weight; “thirty” counts the
choice of sites and color orientation, not the possible amplitudes.
All these single-cell sources have zero six-site output. They are
the directions where further perturbation analysis is needed, not
counterexamples to the rate law.

## From a shape theorem to a GHZ estimate

In the smooth core families and five-arm stars, the response controls
distance to an exactly flat source linearly:

$$
\operatorname{dist}(T,\{\mathcal F_4=0\})
\le C\,\frac{\|\mathcal F_4(T)\|}{\|T\|}.
$$

This has practical meaning: a small measured response puts the source
close to a known family, with a stated bound on the discrepancy.
The constant is uniform on compact collections of the stated smooth
families. For spanning stars it only needs arm norms bounded away from
zero; matrix rank loss is permitted. The invertible four-core estimate
still requires its matrix-rank hypothesis.

For a source $A$ near a full-support single-color zero $A_0$, write

$$
H(A)=\lambda(a^6+b^6+c^6)+E,\quad
\varepsilon=\|E\|,\quad \delta=\|A-A_0\|.
$$

If two non-ground arms have size at least a fixed fraction of the
non-ground source norm, or one edge has its smaller singular value
or same-color strength bounded below by such a fraction, the latest results give

$$
|\lambda|\le C_1\varepsilon+C_2\delta^5.
$$

This uses actual source distance. Unlike an order statement for a path
parameter, it is unaffected by describing the same path with a slower
parameter. A separate dense five-site support condition gives a
sixth-power bound and rules out a five-clique as the nonzero first
non-ground jet at these full-support limits.

To finish the universal square-root law, we still need
$\varepsilon\ge c|\lambda|^3$ across every relevant boundary.
The new results identify and control several difficult families, but a
bound involving $\delta$ does not by itself give that error-versus-signal
comparison. Within the full-support single-color branch, the remaining
critical shapes for this onset argument are the thirty single-cell,
different-color directions above.
The combined estimate is uniform when the normalized non-ground
direction stays a fixed positive distance from those sources.
Indeed, a flat source with no two adjacent edges can have only one
edge: two disjoint edges would give a nonzero four-site tensor product,
with nothing to cancel it. The same-color and invertible-edge criteria
then leave just the stated different-color cells.
The error-versus-signal comparison remains open even on the families
whose onset is now controlled.
