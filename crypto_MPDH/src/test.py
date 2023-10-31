from sage.all import *

# challenge parameters
n = 32
p = next_prime(int(0x1337**7.331))
F = GF(p)

mul_order = lambda n, p: ZZ(lcm(p**n - p**i for i in range(n)))


# works with `MPDH` permutations
def cycles_order(P):
    cycles = []
    for i in range(n):
        if any(i in cycle for cycle in cycles):
            continue
        
        cycle = [i]
        j = P[i][0]
        while j not in cycle:
            cycle.append(j)
            j = P[j][0]

        cycles.append(cycle)
    return cycles, [len(cycle) for cycle in cycles]


# generate a possible `G`
G = Matrix(F, [[0]])
while G.det() == 0:
    i = list(range(n))
    shuffle(i)
    G = Matrix(F, [F.random_element() * vector(F, [0] * j + [1] + [0] * (n - j - 1)) for j in i])

# DH
a = int(F.random_element())
A = G**a

# dlog to recover `a`
poly = G.charpoly()
SF = poly.splitting_field("x")
GJ, T = G.jordan_form(SF, transformation=True)
AJ = T**-1 * A * T

for i in range(n):
    if a == AJ[i, i].log(GJ[i, i]):
        print(f"OK #{i + 1} entry")
        break
else:
    print("FAILED")
