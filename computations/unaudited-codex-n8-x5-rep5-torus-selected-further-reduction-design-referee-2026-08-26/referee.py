#!/usr/bin/env python3
"""Independent exact referee for the selected rep5 73-variable torus reduction."""
from __future__ import annotations
import ast, copy, hashlib, json, math, re
from collections import Counter, deque
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
C = ROOT / "computations"
DESIGN = C / "unaudited-codex-n8-x5-rep5-torus-selected-further-reduction-design-2026-08-26"
UPSTREAM = C / "unaudited-codex-n8-x5-rep5-k2-t1-open84-torus-cover-design-2026-08-26"
UPSTREAM_REF = C / "unaudited-codex-n8-x5-rep5-k2-t1-open84-torus-cover-referee-2026-08-26"
SOURCE = UPSTREAM / "sources/rep5_k2_t1_gauge_yn11_yn21_t01_t20_Q_design.sing"
PINS = {
    DESIGN / "MANIFEST.sha256": "a1be34a89dae7597ab06efe6eaba6e0e4fc12256949f667ac8124ee93c35690e",
    DESIGN / "results_design.json": "3748a40b67ffd0dafc2b7a4d89a7f55914ab6e8ad779eca51dd828fb205e7b0e",
    DESIGN / "results_hostiles.json": "ee37b58f6de139af09622ecd39fa8fe0be41e8ed037e57442dcbe022440df476",
    SOURCE: "13c204f73bb82e263267ec977c19a10dba045541921375c2e7568ba48d5baba0",
    UPSTREAM / "MANIFEST.sha256": "2b220f91ffa21c28506f5112a3a3e7fe791c7e3c783c1e7a319186628743659e",
    UPSTREAM_REF / "MANIFEST.sha256": "20f24c8de6e7edb0818c30c11df4716e983fd5f8bf5778ee36d6d3bccf27d0ff",
    DESIGN / "sources/stage0_a37_201_Q_design.sing": "1e49c2b4127f1a185f50dbacbc63a51b97c210cb5dd9bd16a97f914c897fac1f",
    DESIGN / "sources/stage1_a37_200_closed_Q_design.sing": "502b68d7c669708c4e0497c7c457793e584fb2a89e07f70e54e85e83b750dd19",
}

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def replay(manifest: Path) -> int:
    count = 0
    for line in manifest.read_text().splitlines():
        if not line.strip(): continue
        digest, name = line.split(None, 1); path = (manifest.parent / name.strip()).resolve()
        assert path.is_file() and sha(path) == digest, path; count += 1
    return count

for path, digest in PINS.items():
    assert sha(path) == digest, (path, sha(path), digest)
manifest_counts = {"design": replay(DESIGN / "MANIFEST.sha256"), "upstream": replay(UPSTREAM / "MANIFEST.sha256"), "upstream_referee": replay(UPSTREAM_REF / "MANIFEST.sha256")}

def split_program(text: str) -> tuple[list[str], list[str]]:
    variables = text.split("ring r=0,(", 1)[1].split("),dp;", 1)[0].split(",")
    body = text.split("ideal I=", 1)[1].split(';\nprint("INPUT_VARIABLES=', 1)[0]
    pieces, depth, start = [], 0, 0
    for i, char in enumerate(body):
        if char == "(": depth += 1
        elif char == ")": depth -= 1
        elif char == "," and depth == 0: pieces.append(body[start:i].strip()); start = i + 1
        assert depth >= 0
    pieces.append(body[start:].strip()); assert depth == 0
    return variables, pieces

Polynomial = dict[tuple[int, ...], int]
def padd(a: Polynomial, b: Polynomial, sign: int = 1) -> Polynomial:
    out = dict(a)
    for monomial, coefficient in b.items():
        out[monomial] = out.get(monomial, 0) + sign * coefficient
        if not out[monomial]: del out[monomial]
    return out

def pmul(a: Polynomial, b: Polynomial) -> Polynomial:
    out: Polynomial = {}
    for am, ac in a.items():
        for bm, bc in b.items():
            monomial = tuple(sorted(am + bm)); out[monomial] = out.get(monomial, 0) + ac * bc
    return {m:c for m,c in out.items() if c}

class Parser:
    def __init__(self, text: str, index: dict[str,int]):
        self.tokens = re.findall(r"[A-Za-z_][A-Za-z_0-9]*|\d+|[()+*\-]", text); self.i = 0; self.index = index
    def expression(self) -> Polynomial:
        value = self.term()
        while self.i < len(self.tokens) and self.tokens[self.i] in ("+", "-"):
            sign = 1 if self.tokens[self.i] == "+" else -1; self.i += 1; value = padd(value, self.term(), sign)
        return value
    def term(self) -> Polynomial:
        value = self.factor()
        while self.i < len(self.tokens) and self.tokens[self.i] == "*": self.i += 1; value = pmul(value, self.factor())
        return value
    def factor(self) -> Polynomial:
        token = self.tokens[self.i]
        if token == "-": self.i += 1; return {m:-c for m,c in self.factor().items()}
        if token == "(":
            self.i += 1; value = self.expression(); assert self.tokens[self.i] == ")"; self.i += 1; return value
        self.i += 1
        if token.isdigit(): return {} if int(token) == 0 else {():int(token)}
        return {(self.index[token],):1}

variables, expressions = split_program(SOURCE.read_text())
index = {name:i for i,name in enumerate(variables)}
assert len(variables) == 73 and len(expressions) == len(set(expressions)) == 6561
polynomials = []
for expression in expressions:
    parser = Parser(expression, index); polynomial = parser.expression(); assert parser.i == len(parser.tokens) and polynomial; polynomials.append(polynomial)

def sparse_rank_mod(rows, prime: int) -> int:
    echelon = {}
    for raw in rows:
        row = {k:v % prime for k,v in raw.items() if v % prime}
        while row:
            pivot = min(row)
            if pivot not in echelon:
                inv = pow(row[pivot], -1, prime); echelon[pivot] = {k:v*inv % prime for k,v in row.items()}; break
            factor = row[pivot]; known = echelon[pivot]
            row = {k:(row.get(k,0)-factor*known.get(k,0)) % prime for k in set(row)|set(known)}; row = {k:v for k,v in row.items() if v}
    return len(echelon)

def sparse_rank_q(rows) -> int:
    echelon = {}
    for raw in rows:
        row = {k:Fraction(v) for k,v in raw.items() if v}
        while row:
            pivot = min(row)
            if pivot not in echelon:
                scale = row[pivot]; echelon[pivot] = {k:v/scale for k,v in row.items()}; break
            factor = row[pivot]; known = echelon[pivot]
            row = {k:row.get(k,Fraction())-factor*known.get(k,Fraction()) for k in set(row)|set(known)}; row = {k:v for k,v in row.items() if v}
    return len(echelon)

def exponent(monomial: tuple[int,...]) -> Counter:
    return Counter(monomial)

weight_names = {"a04_20":1,"a04_21":1,"a04_22":1,"a35_21":-1,"a35_22":-1,"a37_20":-1}
weights = [weight_names.get(name,0) for name in variables]
grading_rows = []
for polynomial in polynomials:
    monomials = sorted(polynomial); base = exponent(monomials[0]); base_weight = sum(weights[i]*n for i,n in base.items())
    for monomial in monomials[1:]:
        now = exponent(monomial); assert sum(weights[i]*n for i,n in now.items()) == base_weight
        row = {i:base[i]-now[i] for i in set(base)|set(now) if base[i] != now[i]}
        if row: grading_rows.append(row)
assert len(grading_rows) == 248037
grading_modular = [sparse_rank_mod(grading_rows, p) for p in (32003,65521)]
assert grading_modular == [72,72]
# Modular rank gives rank_Q >=72, and the explicit nonzero rational weight vector gives rank_Q <=72.
grading_rank_q = 72

occurrences, maximum_exponent, linear_rows = Counter(), Counter(), []
affine_linear_count, monic = 0, []
adjacency = [set() for _ in variables]
for equation_id, polynomial in enumerate(polynomials):
    degree = max(map(len, polynomial)); affine_linear_count += degree <= 1
    linear = {m[0]:c for m,c in polynomial.items() if len(m)==1}
    if linear: linear_rows.append(linear)
    support = set()
    for monomial in polynomial:
        support.update(monomial)
        for coordinate in set(monomial):
            occurrences[coordinate] += 1; maximum_exponent[coordinate] = max(maximum_exponent[coordinate], monomial.count(coordinate))
    for coordinate in support: adjacency[coordinate].update(support-{coordinate})
    for coordinate, coefficient in linear.items():
        if abs(coefficient)==1 and all(coordinate not in m for m in polynomial if m!=(coordinate,)): monic.append((equation_id,coordinate))
assert affine_linear_count == 0 and not monic and set(occurrences) == set(range(73))
linear_rank_q = sparse_rank_q(linear_rows); assert linear_rank_q == 43
unseen, components = set(range(73)), []
while unseen:
    queue=deque([min(unseen)]); component=set()
    while queue:
        coordinate=queue.popleft()
        if coordinate in component: continue
        component.add(coordinate); queue.extend(adjacency[coordinate]-component)
    unseen -= component; components.append(component)
assert [len(x) for x in components] == [73]

def specialize(polys: list[Polynomial], coordinate: int, value: int) -> list[Polynomial]:
    out, seen = [], set()
    for polynomial in polys:
        reduced: Polynomial = {}
        for monomial, coefficient in polynomial.items():
            if value == 0 and coordinate in monomial: continue
            rewritten = tuple(i for i in monomial if not (value == 1 and i == coordinate))
            reduced[rewritten] = reduced.get(rewritten,0) + coefficient
        reduced = {m:c for m,c in reduced.items() if c}
        if not reduced: continue
        assert not (len(reduced)==1 and () in reduced)
        key=tuple(sorted(reduced.items()))
        if key not in seen: seen.add(key); out.append(reduced)
    return out

def source_polys(path: Path) -> tuple[list[str], list[Polynomial]]:
    names, exprs = split_program(path.read_text()); parsed=[]
    for expr in exprs:
        parser=Parser(expr,index); value=parser.expression(); assert parser.i==len(parser.tokens); parsed.append(value)
    return names,parsed

def grading_rank_for(polys: list[Polynomial], remaining: list[int]) -> tuple[int,int]:
    rows=[]
    for polynomial in polys:
        monomials=sorted(polynomial); base=exponent(monomials[0])
        for monomial in monomials[1:]:
            now=exponent(monomial); row={i:base[i]-now[i] for i in set(base)|set(now) if base[i]!=now[i]}
            if row: rows.append(row)
    ranks=[sparse_rank_mod(rows,p) for p in (32003,65521)]; assert ranks[0]==ranks[1]
    return ranks[0],len(remaining)-ranks[0]

q=index["a37_20"]
specialized = {1:specialize(polynomials,q,1),0:specialize(polynomials,q,0)}
expected_sources = [(DESIGN/"sources/stage0_a37_201_Q_design.sing",1,254598,0),(DESIGN/"sources/stage1_a37_200_closed_Q_design.sing",0,210111,1)]
source_replay=[]
for path,value,total_terms,nullity in expected_sources:
    names,parsed=source_polys(path); assert names==[name for name in variables if name!="a37_20"]
    assert "a37_20" not in path.read_text() and parsed==specialized[value]
    assert len(parsed)==len(set(tuple(sorted(x.items())) for x in parsed))==6561 and sum(map(len,parsed))==total_terms
    active={i for polynomial in parsed for monomial in polynomial for i in monomial}; assert active==set(range(73))-{q}
    assert not any(abs(polynomial.get((i,),0))==1 and all(i not in m for m in polynomial if m!=(i,)) for polynomial in parsed for i in active)
    rank,got_nullity=grading_rank_for(parsed,[i for i in range(73) if i!=q]);assert got_nullity==nullity
    source_replay.append({"path":str(path.relative_to(ROOT)),"sha256":sha(path),"variables":72,"generators":6561,"terms":total_terms,"grading_rank":rank,"grading_nullity":got_nullity,"removed_identifier_absent":True})

candidate_rows=[]
for name in sorted(weight_names):
    coordinate=index[name]; opened=specialize(polynomials,coordinate,1); closed=specialize(polynomials,coordinate,0)
    objective=[max(sum(map(len,opened)),sum(map(len,closed))),sum(map(len,opened))+sum(map(len,closed)),max(len(opened),len(closed)),len(opened)+len(closed)]
    candidate_rows.append({"coordinate":name,"weight":weights[coordinate],"objective":objective,"open_terms":sum(map(len,opened)),"closed_terms":sum(map(len,closed))})
selected=min(candidate_rows,key=lambda row:(*row["objective"],row["coordinate"]))
assert selected["coordinate"]=="a37_20" and selected["weight"]==-1 and selected["objective"]==[254598,464709,6561,13122]

producer=json.loads((DESIGN/"results_design.json").read_text())
assert producer["grading"]["rank"]==grading_rank_q and producer["grading"]["nullity"]==1 and producer["grading"]["nonzero_weights"]==[weight_names]
assert producer["linear_reduction"]["all_generator_linear_part_rank"]==linear_rank_q
assert producer["linear_reduction"]["amplitude_inactive_coordinates"]==[] and producer["linear_reduction"]["unit_coefficient_graph_substitutions"]==[]
assert producer["block_structure"]["component_sizes"]==[73]
assert producer["residual_torus_cover"]["selected_coordinate"]=="a37_20" and producer["residual_torus_cover"]["selected_weight"]==-1
assert producer["residual_torus_cover"]["identity"]=="D(q) union V(q)" and producer["residual_torus_cover"]["root_free"] is True
assert producer["conclusion"]["singular_runs"]==0 and producer["conclusion"]["mathematical_coverage"] is False

def validate_metadata(value):
    assert value["status"]=="PASS_EXACT_TWO_CHART_RESIDUAL_ONE_TORUS_COVER" and value["source"]["sha256"]==PINS[SOURCE]
    assert (value["grading"]["rank"],value["grading"]["nullity"])==(72,1) and value["grading"]["nonzero_weights"]==[weight_names]
    cover=value["residual_torus_cover"];assert cover["root_free"] is True and (cover["selected_coordinate"],cover["selected_weight"])==("a37_20",-1) and len(cover["sources"])==2
    assert [(x["variables"],x["generators"]) for x in cover["sources"]]==[(72,6561),(72,6561)]
    assert value["linear_reduction"]["unit_coefficient_graph_substitutions"]==[] and value["conclusion"]["singular_runs"]==0

mutations=[lambda x:x.__setitem__("status","PASS"),lambda x:x["source"].__setitem__("sha256","0"*64),lambda x:x["grading"].__setitem__("rank",71),lambda x:x["grading"].__setitem__("nullity",0),lambda x:x["grading"].__setitem__("nonzero_weights",[]),lambda x:x["residual_torus_cover"].__setitem__("root_free",False),lambda x:x["residual_torus_cover"].__setitem__("selected_coordinate","a04_20"),lambda x:x["residual_torus_cover"].__setitem__("selected_weight",2),lambda x:x["residual_torus_cover"]["sources"].pop(),lambda x:x["residual_torus_cover"]["sources"][0].__setitem__("variables",73),lambda x:x["linear_reduction"].__setitem__("unit_coefficient_graph_substitutions",["false"]),lambda x:x["conclusion"].__setitem__("singular_runs",1)]
hostile_pass=[]
for mutate in mutations:
    value=copy.deepcopy(producer);mutate(value)
    try:validate_metadata(value)
    except (AssertionError,KeyError,TypeError):hostile_pass.append(True)
    else:hostile_pass.append(False)
assert len(hostile_pass)==12 and all(hostile_pass)
producer_hostiles=json.loads((DESIGN/"results_hostiles.json").read_text());assert producer_hostiles["hostile_count"]==12 and all(producer_hostiles["tests"].values()) and producer_hostiles["solver_runs"]==0
tree=ast.parse((DESIGN/"analyze.py").read_text());assert not any(isinstance(node,(ast.Import,ast.ImportFrom)) and any(alias.name=="subprocess" for alias in node.names) for node in ast.walk(tree))

out={
 "schema":"KRENN_X5_REP5_TORUS_SELECTED_FURTHER_REDUCTION_DESIGN_REFEREE_V1",
 "status":"PASS_EXACT_TWO_CHART_RESIDUAL_ONE_TORUS_COVER_DESIGN_ONLY",
 "producer_manifest_sha256":PINS[DESIGN/"MANIFEST.sha256"],"producer_result_sha256":PINS[DESIGN/"results_design.json"],"manifest_counts":manifest_counts,
 "source":{"sha256":PINS[SOURCE],"variables":73,"generators":6561,"total_terms":sum(map(len,polynomials))},
 "grading":{"constraint_rows":len(grading_rows),"modular_ranks":grading_modular,"rank_over_Q":72,"nullity_over_Q":1,"primitive_weights":weight_names},
 "linear_reduction":{"inactive":[],"affine_linear_generators":affine_linear_count,"unit_monic_substitutions":[],"linear_rank_over_Q":linear_rank_q,"interaction_components":[73]},
 "coordinate_scoring":{"candidates":candidate_rows,"selected":"a37_20","selected_weight":-1,"objective":selected["objective"]},
 "cover_proof":{"identity":"D(q) union V(q)","root_free":True,"open_action":"weight(q)=-1, so lambda=q sends lambda^-1*q to 1","closed_action":"literal q=0","sources":source_replay,"exhaustive":True,"reversible":True},
 "hostiles":{"independent_passed":12,"producer_passed":12},
 "scope":{"design_only":True,"singular_runs":0,"ideal_solves":0,"mathematical_coverage_added":False,"rep5_closed":False},
}
(HERE/"results_referee.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
print(json.dumps({"status":out["status"],"rank":[72,1],"sources":2,"hostiles":12,"solves":0},sort_keys=True))
