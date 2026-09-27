"""Four-variable interval values, gradients and Hessians for calibration.

Real rational centers and complex disc radii; no finite differences are used.
Each radius is rounded outward to keep exact rational denominators manageable.
"""

from fractions import Fraction as F

from covariance_noise_certificate import ScalarBall, length


def rounded(ball):
    value = ball.radius
    if value:
        bits = max(
            0, 70 - value.numerator.bit_length() + value.denominator.bit_length()
        )
        scale = 2**bits
        radius = F(
            (value.numerator * scale + value.denominator - 1) // value.denominator,
            scale,
        )
        return ScalarBall(ball.center, radius)
    return ball


class Jet:
    def __init__(self, value, gradient=None, hessian=None):
        self.value = rounded(
            value if isinstance(value, ScalarBall) else ScalarBall(value)
        )
        self.gradient = (
            [rounded(x) for x in gradient]
            if gradient is not None
            else [ScalarBall(0) for _ in range(4)]
        )
        self.hessian = (
            [[rounded(x) for x in row] for row in hessian]
            if hessian is not None
            else [[ScalarBall(0) for _ in range(4)] for _ in range(4)]
        )

    def __add__(self, other):
        other = other if isinstance(other, Jet) else Jet(other)
        return Jet(
            self.value + other.value,
            [a + b for a, b in zip(self.gradient, other.gradient)],
            [
                [self.hessian[i][j] + other.hessian[i][j] for j in range(4)]
                for i in range(4)
            ],
        )

    __radd__ = __add__

    def __neg__(self):
        return Jet(
            -self.value,
            [-x for x in self.gradient],
            [[-x for x in row] for row in self.hessian],
        )

    def __sub__(self, other):
        return self + (-other if isinstance(other, Jet) else -F(other))

    def __mul__(self, other):
        other = other if isinstance(other, Jet) else Jet(other)
        return Jet(
            self.value * other.value,
            [
                self.gradient[i] * other.value + self.value * other.gradient[i]
                for i in range(4)
            ],
            [
                [
                    self.hessian[i][j] * other.value
                    + self.gradient[i] * other.gradient[j]
                    + self.gradient[j] * other.gradient[i]
                    + self.value * other.hessian[i][j]
                    for j in range(4)
                ]
                for i in range(4)
            ],
        )

    __rmul__ = __mul__

    def inverse(self):
        reciprocal = rounded(self.value.inverse())
        square, cube = rounded(reciprocal**2), rounded(reciprocal**3)
        return Jet(
            reciprocal,
            [-square * x for x in self.gradient],
            [
                [
                    2 * cube * self.gradient[i] * self.gradient[j]
                    - square * self.hessian[i][j]
                    for j in range(4)
                ]
                for i in range(4)
            ],
        )

    def __truediv__(self, other):
        return self * (other if isinstance(other, Jet) else Jet(other)).inverse()

    def __pow__(self, exponent):
        if exponent < 0:
            return self.inverse() ** (-exponent)
        result = Jet(1)
        for _ in range(exponent):
            result *= self
        return result

    def gradient_norm(self):
        return length(x.center for x in self.gradient)

    def hessian_bound(self):
        return length(abs(x.center) + x.radius for row in self.hessian for x in row)


def calibration(coordinates, radius, n):
    variables = []
    for i, value in enumerate(coordinates[:4]):
        gradient = [ScalarBall(int(i == j)) for j in range(4)]
        variables.append(Jet(ScalarBall(value, radius), gradient))
    z, c3, c5, c7 = variables
    s = c3 / (3 * z)
    beta2 = F(3, 2) * (15 * z * s**2 - c5) / z**5
    beta3 = F(9, 16) * (c7 - 105 * z * s**3 + 14 * beta2 * z**5 * s) / z**7
    beta = beta3 / beta2
    return {
        "shift": s - beta * z * z / 3,
        "tau": z**n * beta ** (n // 2),
        "nonlast": (beta * z * z).inverse(),
        "last": beta ** (n // 2 - 1) * z ** (n - 2),
    }
