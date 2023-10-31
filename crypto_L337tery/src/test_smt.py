from random import SystemRandom
from functools import reduce
from operator import __xor__, __and__
# import z3 as smt
import cvc5.pythonic as smt
import tqdm

random = SystemRandom()
bsum = lambda l: reduce(__xor__, l, 0)
bmul = lambda l: reduce(__and__, l, 1)
timeout = 180  # seconds
n = 196


class SymNLFSR:
    taps = [0, 1, 2, 3, 7, 11, 13, 29]
    filter = [(0, 96, 128, 192, 255), (16, 32, 64, 96, 128, 192, 255), (0, 16, 32, 64, 96, 128, 192, 255), (0, 32, 64, 128), (0, 64, 96, 192, 255), (64, 96, 192, 255), (0, 16, 32, 64, 96, 128, 255), (16, 64, 96, 128, 192, 255), (16, 32, 64, 96, 128), (0, 64, 96, 128, 192, 255), (16, 32, 96, 192), (32, 64, 255), (0, 32, 64, 192, 255), (16, 32, 64, 96, 192, 255), (16, 32, 96, 192, 255), (64, 96, 128, 255), (0, 16, 192, 255), (0, 32, 64, 128, 192), (0, 32, 96, 255), (96, 255), (64, 128, 255), (0, 16, 96, 192), (0, 16, 32, 64, 96), (0, 96, 128, 255), (0, 96, 255), (0, 32, 96, 192, 255), (0, 16, 96), (16, 64, 192, 255), (0, 16, 64, 96, 128, 192, 255), (32, 64, 96, 255), (16, 64, 192), (0, 16), (0, 64, 192, 255), (32, 64, 128, 192), (16, 32, 128, 192), (16, 32, 192), (0, 16, 32), (32, 64, 128, 255), (32, 96, 128, 192, 255), (32, 128, 192, 255), (0, 64), (0, 64, 255), (16, 96, 128, 192, 255), (0, 16, 96, 128, 192, 255), (16, 96, 128, 255), (0, 128, 192, 255), (0, 16, 32, 96, 192, 255), (16, 32, 96, 128, 255), (32, 64, 96, 192, 255), (16, 32, 128), (64, 96, 128, 192), (16, 64, 128), (0, 16, 32, 96), (0, 16, 255), (0, 32, 96, 128, 192), (64, 96), (0, 128), (0, 16, 32, 64, 96, 128), (0, 16, 128, 192), (16, 64, 96, 192), (0, 16, 192), (16, 96, 128), (0, 16, 96, 128, 255), (96, 128), (32, 64, 96, 128), (0, 16, 32, 64, 128, 192, 255), (0, 16, 96, 128), (0, 16, 64, 96, 255), (16, 64, 96, 128), (0,), (32, 64, 128), (0, 32, 64, 96, 128, 192, 255), (16, 64, 128, 192), (32, 96), (0, 96, 192, 255), (0, 96, 128, 192), (0, 32), (16, 128, 255), (96,), (16, 32, 192, 255), (0, 16, 64), (16, 128), (0, 16, 96, 255), (0, 255)]

    def __init__(self, state: "list[int]") -> None:
        assert len(state) == 256
        self.state = state

    def __clock(self) -> None:
        self.state = self.state[1:] + [bsum([self.state[i] for i in self.taps])]

    def output(self) -> int:
        out = bsum(bmul(self.state[i] for i in mon) for mon in self.filter)
        self.__clock()
        return out


def try_recovery_vulnerable_initial_states() -> None:
    for i in tqdm.tqdm(range(n)):
        solver = smt.Solver()
        initial_state = [smt.BitVec(f"s_{i}", 1) for i in range(256)]
        sym_nlfsr = SymNLFSR(initial_state)

        for _ in range(i):
            solver.add(sym_nlfsr.output() == smt.BitVecVal(0, 1))
        solver.add(sym_nlfsr.output() == smt.BitVecVal(1, 1))
        for _ in range(n - i - 1):
            solver.add(sym_nlfsr.output() == smt.BitVecVal(0, 1))

        check = solver.check()
        assert check == smt.sat
        model = solver.model()
        nlfsr = SymNLFSR([model[initial_state[i]].as_long() for i in range(256)])
        assert all(nlfsr.output() == x for x in [0] * i + [1] + [0] * (n - i - 1))


def try_recovery_nlfsr_state() -> None:
    _initial_state = [random.randint(0, 1) for _ in range(256)]
    nlfsr = SymNLFSR(_initial_state)

    outputs = [nlfsr.output() for _ in range(6 * n)]

    solver = smt.Solver()
    solver.setOption("tlimit-per", timeout * 100)
    initial_state = [smt.BitVec(f"s_{i}", 1) for i in range(256)]
    sym_nlfsr = SymNLFSR(initial_state)

    for i in range(len(outputs)):
        solver.add(sym_nlfsr.output() == smt.BitVecVal(outputs[i], 1))
    
    check = solver.check()
    print(check)
    assert check == smt.sat
    model = solver.model()
    initial_state_guess = [model[initial_state[i]].as_long() for i in range(256)]
    assert initial_state_guess == _initial_state
