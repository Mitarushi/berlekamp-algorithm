from typing import Self
from modint import ModRing, ModInt


class ModPoly:
    a: list[ModInt]
    ring: ModRing

    def __init__(self, a: list[ModInt], ring: ModRing) -> None:
        self.a = a
        self.ring = ring

    def __len__(self) -> int:
        return len(self.a)

    def deg(self):
        return len(self) - 1

    def reduce(self) -> None:
        while self.a and self.a[-1] == 0:
            self.a.pop()

    def __getitem__(self, item: int) -> ModInt:
        if item < len(self.a):
            return self.a[item]
        else:
            return self.ring.to(0)

    def __setitem__(self, key: int, value: ModInt) -> None:
        if key < len(self.a):
            self.a[key] = value
        else:
            self.a.extend([self.ring.to(0)] * (key - len(self.a) + 1))
            self.a[key] = value

    def __add__(self, other: Self | int | ModInt) -> Self:
        a = self.a
        if isinstance(other, int) or isinstance(other, ModInt):
            other = ModPoly([other], self.ring)
        b = other.a
        if len(a) < len(b):
            a, b = b, a
        c = a[:]
        for idx, val in enumerate(b):
            c[idx] += val
        result = ModPoly(c, self.ring)
        result.reduce()
        return result

    def __neg__(self) -> Self:
        return ModPoly([-x for x in self.a], self.ring)

    def __sub__(self, other: Self) -> Self:
        return self + -other

    def __mul__(self, other: Self | int | ModInt) -> Self:
        if isinstance(other, int) or isinstance(other, ModInt):
            return ModPoly([x * other for x in self.a], self.ring)
        n = len(self) + len(other) - 1
        c = [self.ring.to(0)] * n
        for idx1, val1 in enumerate(self.a):
            for idx2, val2 in enumerate(other.a):
                c[idx1 + idx2] += val1 * val2
        result = ModPoly(c, self.ring)
        result.reduce()
        return result

    def __divmod__(self, other: Self | int | ModInt) -> tuple[Self, Self]:
        if isinstance(other, int):
            other = ModInt(other, self.ring)
        if isinstance(other, int) or isinstance(other, ModInt):
            inv = other.inv()
            return ModPoly([x * inv for x in self.a], self.ring), ModPoly([], self.ring)
        a = self.a[:]
        n = len(self)
        m = len(other)
        if n < m:
            return ModPoly([], self.ring), ModPoly(a, self.ring)
        c = [self.ring.to(0)] * (n - m + 1)
        other_inv = other[m - 1].inv()
        for idx in range(n - m, -1, -1):
            c[idx] = a[idx + m - 1] * other_inv
            for jdx in range(m - 1):
                a[idx + jdx] -= c[idx] * other[jdx]
        div = ModPoly(c, self.ring)
        div.reduce()
        mod = ModPoly(a[:m - 1], self.ring)
        mod.reduce()
        return div, mod

    def __floordiv__(self, other: Self | int | ModInt) -> Self:
        return divmod(self, other)[0]

    def __mod__(self, other: Self | int | ModInt) -> Self:
        return divmod(self, other)[1]

    def __pow__(self, power, modulo=None) -> Self:
        if power == 0:
            return ModPoly([self.ring.to(1)], self.ring)
        elif power % 2 == 0:
            x = self * self
            if modulo is not None:
                x %= modulo
            return pow(x, power // 2, modulo)
        else:
            x = self * self
            if modulo is not None:
                x %= modulo
            x = self * pow(x, power // 2, modulo)
            if modulo is not None:
                x %= modulo
            return x

    def __eq__(self, other: Self | int | ModInt) -> bool:
        if isinstance(other, int) or isinstance(other, ModInt):
            return (len(self) == 1 and self[0] == other) or (len(self) == 0 and other == 0)
        return self.a == other.a

    def __repr__(self) -> str:
        return repr(self.a)

    def __str__(self) -> str:
        return str(self.a)

    def pretty(self) -> str:
        result = []
        for idx, i in enumerate(self.a):
            match (idx, i):
                case (_, 0):
                    continue
                case (0, _):
                    result.append(str(i))
                case (1, 1):
                    result.append("x")
                case (1, _):
                    result.append(f"{i}x")
                case (_, 1):
                    result.append(f"x^{idx}")
                case (_, _):
                    result.append(f"{i}x^{idx}")
        result.reverse()
        return " + ".join(result)

    def gcd(self, other: Self) -> Self:
        a = self
        b = other
        while b:
            a, b = b, a % b
        return a

    def derivative(self) -> Self:
        return ModPoly([self[idx] * idx for idx in range(1, len(self))], self.ring)

    def p_root(self) -> Self:
        result = []
        for idx in range(0, len(self), self.ring.m):
            result.append(self[idx])
        return ModPoly(result, self.ring)

    def p_pow(self) -> Self:
        result = ModPoly([], self.ring)
        for idx, i in enumerate(self.a):
            result[idx * self.ring.m] = i
        return result

    @classmethod
    def x_pow(cls, n: int, ring: ModRing) -> Self:
        return cls([ring.to(0)] * n + [ring.to(1)], ring)

    def monic(self) -> Self:
        return self // self[-1]
