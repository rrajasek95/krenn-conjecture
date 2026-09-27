"""The real quadratic field Q(sqrt(6)), using exact rational arithmetic."""

from dataclasses import dataclass
from fractions import Fraction as Q


def require(condition, message):
    if not condition:
        raise ValueError(message)


@dataclass(frozen=True)
class K:
    a: Q = Q(0)
    b: Q = Q(0)

    def __post_init__(self):
        object.__setattr__(self, "a", Q(self.a))
        object.__setattr__(self, "b", Q(self.b))

    @staticmethod
    def cast(z):
        return z if isinstance(z, K) else K(z)

    def __bool__(self):
        return bool(self.a or self.b)

    def __add__(self, z):
        z = K.cast(z)
        return K(self.a+z.a, self.b+z.b)

    __radd__ = __add__

    def __neg__(self):
        return K(-self.a, -self.b)

    def __sub__(self, z):
        return self+-K.cast(z)

    def __rsub__(self, z):
        return K.cast(z)+-self

    def __mul__(self, z):
        z = K.cast(z)
        return K(self.a*z.a+6*self.b*z.b, self.a*z.b+self.b*z.a)

    __rmul__ = __mul__

    def __truediv__(self, z):
        z = K.cast(z)
        require(bool(z), "Nonzero quadratic-field divisor")
        denominator = z.a*z.a-6*z.b*z.b
        numerator = self*K(z.a, -z.b)
        return K(numerator.a/denominator, numerator.b/denominator)

    def __pow__(self, n):
        require(isinstance(n, int) and n >= 0, "Nonnegative integral power")
        result = ONE
        for _ in range(n):
            result *= self
        return result

    def __str__(self):
        return str(self.a) if not self.b else f"({self.a})+({self.b})sqrt(6)"


ZERO, ONE, ROOT6 = K(), K(1), K(0, 1)


def dot(x, y):
    return sum((a*b for a, b in zip(x, y)), ZERO)


def norm2(x):
    return dot(x, x)


def rank(rows):
    a = [[K.cast(z) for z in row] for row in rows]
    if not a:
        return 0
    r = 0
    for c in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        scale = a[r][c]
        a[r] = [z/scale for z in a[r]]
        for i in range(r+1, len(a)):
            scale = a[i][c]
            if scale:
                a[i] = [x-scale*y for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r
