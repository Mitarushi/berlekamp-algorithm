from typing import Self


class ModRing:
    m: int

    def __init__(self, m: int) -> None:
        self.m = m

    def __eq__(self, other: Self | int) -> bool:
        match other:
            case ModRing(m):
                return self.m == m
            case int():
                return self.m == other
            case _:
                return False

    def to(self, x: int) -> 'ModInt':
        return ModInt(x, self)


class ModInt:
    x: int
    ring: ModRing

    def __init__(self, x: int, ring: ModRing) -> None:
        self.x = x
        self.ring = ring

    def __add__(self, other: Self | int) -> Self:
        x = other if isinstance(other, int) else other.x
        return ModInt((self.x + x) % self.ring.m, self.ring)

    def __neg__(self) -> Self:
        return ModInt(-self.x % self.ring.m, self.ring)

    def __sub__(self, other: Self | int) -> Self:
        return self + -other

    def __mul__(self, other: Self | int) -> Self:
        x = other if isinstance(other, int) else other.x
        return ModInt((self.x * x) % self.ring.m, self.ring)

    def __pow__(self, power: int) -> Self:
        return ModInt(pow(self.x, power, self.ring.m), self.ring)

    def inv(self) -> Self:
        return self ** (self.ring.m - 2)

    def __truediv__(self, other: Self | int) -> Self:
        x = ModInt(other, self.ring) if isinstance(other, int) else other
        return self * x.inv()

    def __eq__(self, other: Self | int) -> bool:
        match other:
            case ModInt():
                return self.x == other.x and self.ring == other.ring
            case int():
                return self.x == other
            case _:
                return False

    def __repr__(self) -> str:
        return f'ModInt({self.x}, {self.ring.m})'

    def __str__(self) -> str:
        return str(self.x)
