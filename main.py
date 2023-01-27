import random
from modint import ModRing, ModInt
from poly import ModPoly


def square_free_factor(f: ModPoly) -> ModPoly:
    if f.deg() <= 1:
        return f
    f_deriv_gcd = f.derivative().gcd(f)
    f_factor_not_pow_p = f // f_deriv_gcd
    f_factor_pow_p = f // pow(f_factor_not_pow_p, f.deg(), f).gcd(f)
    f_factor_pow_p = square_free_factor(f_factor_pow_p.p_root())
    return f_factor_not_pow_p * f_factor_pow_p


def berlekamp_algorithm(f: ModPoly) -> list[tuple[ModPoly, int]]:
    if f.deg() <= 1:
        return [(f, 1)]

    ring = f.ring
    f_free = square_free_factor(f).monic()
    f_free_deg = f_free.deg()

    base = []
    x_pow_q = pow(ModPoly.x_pow(1, ring), ring.m, f_free)
    x_pow_iq = ModPoly([ring.to(1)], ring)
    for i in range(f_free_deg):
        x_pow_i = ModPoly.x_pow(i, ring)
        base.append((x_pow_iq - x_pow_i, x_pow_i))
        x_pow_iq = x_pow_iq * x_pow_q % f_free

    for i in range(f_free_deg):
        for j in range(i):
            if base[j][0] == 0:
                continue
            j_deg = base[j][0].deg()
            s = base[i][0][j_deg] / base[j][0][j_deg]
            base[i] = (base[i][0] - base[j][0] * s, base[i][1] - base[j][1] * s)

    kernel = [i[1] for i in base if i[0] == 0]
    factor = [f_free]
    while len(factor) < len(kernel):
        t = ModPoly([ring.to(0)], ring)
        for i in kernel:
            t += i * random.randint(0, ring.m - 1)
        t = (pow(t, (ring.m - 1) // 2, f_free) + ring.to(1)).gcd(f_free).monic()

        for idx, i in enumerate(factor):
            gcd = t.gcd(i)
            if gcd.deg() != 0 and gcd != i:
                factor.append(gcd)
                factor[idx] = i // gcd
            if gcd != 1:
                t //= gcd

    result = []
    for i in factor:
        count = 0
        while f % i == 0:
            f //= i
            count += 1
        result.append((i.monic(), count))
    return result


if __name__ == '__main__':
    m = input("Enter modulus: ")
    ring = ModRing(int(m))

    is_first = True
    while True:
        if is_first:
            f = input("Enter coefficients (e.g. if f(x)=x^3+2x+3, enter 1 0 2 3): ")
            is_first = False
        else:
            f = input("Enter coefficients: ")
        f = ModPoly([ModInt(int(i), ring) for i in f.split()][::-1], ring)

        print("Factorization:")
        factor = berlekamp_algorithm(f)
        factor.sort(key=lambda x: x[0].deg())
        for i, j in factor:
            print(f"({i.pretty()})^{j}" if j != 1 else f"{i.pretty()}")
        print()
