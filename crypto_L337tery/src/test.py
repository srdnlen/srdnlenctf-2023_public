from sage.all import *
from sage.crypto.boolean_function import BooleanFunction
import itertools, tqdm

n = 8
B = BooleanPolynomialRing(n, [f"x{i}" for i in range(n)])
xs = B.gens()

mons = [1] + list(itertools.chain.from_iterable([[
    prod(c) for c in itertools.combinations(xs, i)
] for i in range(1, n + 1)]))


def get_filter_function_from_annihilator(g=sum(sample(xs, 6)) + 1, quasi_balaced=85):
    polys = [g * mon for mon in mons]

    M, col_mons = Sequence(polys).coefficient_matrix(sparse=False)
    K = M.left_kernel().basis()

    while True:
        f = sum(mons[i] for k in sample(K, 32) for i, b in enumerate(k) if b)

        _f, _g = map(BooleanFunction, [f, g])
        assert _f.algebraic_immunity() == g.degree()
        assert _f.annihilator(1) == _g.algebraic_normal_form()

        if sum(_f.truth_table()) >= quasi_balaced:
            return f, g


def get_primitive_function(degree=256):
    F = GF(2)
    P = F["x"]
    x = P.gen()

    f = x**degree + 1
    indxs = [1] + list(prime_range(0, 32))
    for I in tqdm.tqdm(itertools.combinations(indxs, 7), total=binomial(len(indxs), 7)):
        _f = f + sum(x**i for i in I)
        if not _f.is_prime():
            continue
        if _f.is_primitive():
            return _f
    return None


fun_to_list = lambda f: [tuple(map(xs.index, mon.variables())) for mon in f.monomials()]
_var_to_state = {i: j for i, j in enumerate([0, 16, 32, 64, 96, 128, 192, 255])}
var_to_state = lambda l: [tuple(_var_to_state[i] for i in mon) for mon in l]

f = eval(open("filter.txt", "r").read().split(" = ").pop(), 
         {f"x{i}": x for i, x in enumerate(xs)})
g = BooleanFunction(f).annihilator(1)

t = get_primitive_function()
print([mon.degree() for mon in reversed(t.monomials()) if mon.degree() < 256])