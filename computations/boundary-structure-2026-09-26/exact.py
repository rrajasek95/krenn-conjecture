"""Small exact field Q(omega), omega^2+omega+1=0, and matching tensors."""
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import combinations, product


def require(condition, message):
    if not condition:
        raise ValueError(message)


@dataclass(frozen=True)
class E:
    a: Q = Q(0)
    b: Q = Q(0)

    def __post_init__(self):
        object.__setattr__(self, 'a', Q(self.a))
        object.__setattr__(self, 'b', Q(self.b))

    @staticmethod
    def cast(x):
        return x if isinstance(x, E) else E(x)

    def __add__(self, other):
        other = E.cast(other)
        return E(self.a+other.a, self.b+other.b)

    __radd__ = __add__

    def __neg__(self):
        return E(-self.a, -self.b)

    def __sub__(self, other):
        return self+-E.cast(other)

    def __rsub__(self, other):
        return E.cast(other)+-self

    def __mul__(self, other):
        other = E.cast(other)
        return E(self.a*other.a-self.b*other.b,
                 self.a*other.b+self.b*other.a-self.b*other.b)

    __rmul__ = __mul__

    def conjugate(self):
        return E(self.a-self.b, -self.b)

    def abs2(self):
        return self.a*self.a-self.a*self.b+self.b*self.b

    def __truediv__(self, other):
        other = E.cast(other)
        require(bool(other), 'Nonzero divisor')
        z = self*other.conjugate()
        return E(z.a/other.abs2(), z.b/other.abs2())

    def __bool__(self):
        return bool(self.a or self.b)


ZERO, ONE, OMEGA = E(), E(1), E(0, 1)


def matchings(vertices):
    if not vertices:
        yield ()
        return
    for j in range(1, len(vertices)):
        for rest in matchings(vertices[1:j]+vertices[j+1:]):
            yield ((vertices[0], vertices[j]),)+rest


def cell(i, j, a, b):
    return (i, j, a, b) if i < j else (j, i, b, a)


def hafnian(source, vertices):
    value = ZERO
    for matching in matchings(tuple(vertices)):
        term = ONE
        for i, j in matching:
            term *= source.get(tuple(sorted((i, j))), ZERO)
        value += term
    return value


def outputs(source, n=6, colors=3):
    """Expand actual active cells, then collect equal output words."""
    edges = {}
    for (i, j, a, b), z in source.items():
        if z:
            edges.setdefault((i, j), []).append((a, b, E.cast(z)))
    out = {}
    for matching in matchings(tuple(range(n))):
        for chosen in product(*(edges.get(edge, []) for edge in matching)):
            word, term = [0]*n, ONE
            for (i, j), (a, b, z) in zip(matching, chosen):
                word[i], word[j] = a, b
                term *= z
            key = tuple(word)
            out[key] = out.get(key, ZERO)+term
    return {w: z for w, z in out.items() if z}


def rank(matrix):
    a = [[E.cast(z) for z in row] for row in matrix]
    if not a:
        return 0
    row = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(row, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        d = a[row][col]
        a[row] = [x/d for x in a[row]]
        for i in range(row+1, len(a)):
            if a[i][col]:
                d = a[i][col]
                a[i] = [x-d*y for x, y in zip(a[i], a[row])]
        row += 1
        if row == len(a):
            break
    return row
