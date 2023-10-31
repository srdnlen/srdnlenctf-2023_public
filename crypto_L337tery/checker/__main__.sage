from sage.all import *
from sage.crypto.boolean_function import BooleanFunction
from server import NLFSR, L337tery
from pwn import process, remote, context
import os, itertools

HOST = os.getenv("HOST", "l337tery.challs.srdnlen.it")
PORT = int(os.getenv("PORT", 1337))


def vulnerable_initial_states() -> "list[tuple[int, int]]":
    f_indexes = sorted(set(itertools.chain.from_iterable(NLFSR.filter)))

    n = len(f_indexes)
    B = BooleanPolynomialRing(n, [f"x{i}" for i in range(n)])
    xs = B.gens()
    index_to_var = {i: x for i, x in zip(f_indexes, xs)}
    var_to_index = {x: i for x, i in zip(xs, f_indexes)}

    f = sum(prod(index_to_var[i] for i in mon) for mon in NLFSR.filter)
    assert BooleanFunction(f).algebraic_immunity() == 1
    g = BooleanFunction(f).annihilator(1)
    g_indexes = [var_to_index[x] for mon in g.monomials() for x in mon.variables()]

    F = GF(2)
    P = PolynomialRing(F, "x")
    x = P.gen()
    char_poly = x**256 + sum(x**i for i in NLFSR.taps)
    S = Matrix.companion(char_poly, "bottom")

    initial_states = []
    for i in range(L337tery.ncoeffs - 1):
        if len(initial_states) >= 2:
            break

        M = Matrix(F, [sum((S**j)[g_indexes].rows()) for j in range(i)] + 
                      [sum((S**j)[g_indexes].rows()) for j in range(i + 1, L337tery.ncoeffs)], sparse=False)
        K = M.right_kernel()

        for k in K.basis():
            initial_state = list(map(int, S**-1337 * k))
            nlfsr = NLFSR(initial_state)

            assert all(nlfsr.output() == 0 for _ in range(i))
            if nlfsr.output() != 1:
                continue
            assert all(nlfsr.output() == 0 for _ in range(i + 1, L337tery.ncoeffs))

            initial_states.append((i, initial_state))
            break
    
    return initial_states


def recover_security_params() -> "list[list[int]]":
    global io, initial_states
    assert len(initial_states) == 2
    
    leaks = []
    for i, initial_state in initial_states:
        io.sendlineafter(b"Are you ready to partecipate to the grand lottery? ", b"Nope")
        io.sendlineafter(b"Give me your initial state: ", ", ".join(map(str, initial_state)).encode())
        io.sendlineafter(b"Do you want to use your security parameters? ", b"Nope")

        leak = io.recvline_startswith(b"Behold, the randomness").decode().split(": ").pop()
        leaks.append((i, list(map(int, leak.split(",")))))
    
    p, ncoeffs = L337tery.p, L337tery.ncoeffs
    (j1, leak1), (j2, leak2) = leaks
    
    security_params = []
    for l1, l2 in zip(leak1, leak2):
        g = l1 * pow(l2, -1, p) % p
        security_param = ([l1 * pow(g, i, p) % p for i in reversed(range(j1))] + 
                          [l1 * pow(g, -i, p) % p for i in range(j1, ncoeffs)])
        security_params.append(list(map(int, security_param)))
    
    return security_params


def recover_coeffs(draws: "list[int]") -> "list[int]":
    global security_params

    p = L337tery.p
    F = GF(p)

    M = Matrix(F, security_params)
    rhs = vector(F, draws)

    s = M.solve_right(rhs)
    K = M.right_kernel_matrix()
    for i, k in enumerate(K.rows()):
        s -= s[i] * k

    n = 50  # chosen after some attempts
    L = Matrix.block(ZZ, [[K[:, :K.nrows()], K[:, K.nrows():K.nrows() + n]],
                          [Matrix.zero(n, K.nrows()), p * Matrix.identity(n)]])
    embedding = 1
    L = Matrix.block(ZZ, [[L, Matrix.zero(L.nrows(), 1)],
                          [Matrix([s[:K.nrows() + n]]), Matrix([[embedding]])]])

    L = L.BKZ()

    for row in L:
        if row[-1] < 0:
            row *= -1
        if row[-1] == embedding and all(x in {0, 1} for x in map(int, row[:-1])):
            s += row[:K.nrows()] * K
            assert all(x in {0, 1} for x in map(int, s))
            return list(map(int, s.list()))
    return None


def recover_nlfsr_state(outputs: "list[int]") -> "list[int]":
    f_indexes = sorted(set(itertools.chain.from_iterable(NLFSR.filter)))

    n = len(f_indexes)
    B = BooleanPolynomialRing(n, [f"x{i}" for i in range(n)])
    xs = B.gens()
    index_to_var = {i: x for i, x in zip(f_indexes, xs)}
    var_to_index = {x: i for x, i in zip(xs, f_indexes)}

    f = sum(prod(index_to_var[i] for i in mon) for mon in NLFSR.filter)
    assert BooleanFunction(f).algebraic_immunity() == 1
    g = BooleanFunction(f).annihilator(1)
    g_indexes = [var_to_index[x] for mon in g.monomials() for x in mon.variables()]

    F = GF(2)
    P = PolynomialRing(F, "x")
    x = P.gen()
    char_poly = x**256 + sum(x**i for i in NLFSR.taps)
    S = Matrix.companion(char_poly, "bottom")

    M = Matrix(F, [sum((S**j)[g_indexes].rows()) for j, y in enumerate(outputs) if y], sparse=False)
    rhs = vector(F, [0 + g.constant_coefficient()] * M.nrows())
    s = M.solve_right(rhs)
    K = M.right_kernel()
    if len(K.basis()) != 0:
        return None

    initial_state = list(map(int, S**-1337 * s))
    return initial_state


def win_grand_lottery(rounds=7) -> bool:
    global io, security_params
    
    io.sendlineafter(b"Are you ready to partecipate to the grand lottery? ", b"Yes")

    outputs = []
    for r in range(rounds - 1):
        io.sendlineafter(b">>> ", ", ".join(["0"] * L337tery.ndraws).encode())
        data = io.recvline().decode().split(": ").pop()
        draws = list(map(int, data.split(",")))
        coeffs = recover_coeffs(draws)
        if coeffs is None:
            return False
        outputs.extend(coeffs)

        if outputs.count(1) >= 256:
            initial_state = recover_nlfsr_state(outputs)
            if initial_state is None:
                return False
            l337tery = L337tery(initial_state, security_params)
            for _ in range(r):
                l337tery.draws()
            assert l337tery.draws() == draws
            break
    else:
        return False
    
    io.sendlineafter(b">>> ", ", ".join(map(str, l337tery.draws())).encode())
    data = io.recvline(keepends=False).decode()
    if "Impressive" in data:
        print(data.split("grand prize: ").pop())
        return True

    return False


initial_states = vulnerable_initial_states()

outcome = False
while not outcome:
    io = remote(HOST, PORT)
    security_params = recover_security_params()
    outcome = win_grand_lottery()
    io.close()
