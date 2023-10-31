import os
import signal
from time import time
from random import Random as SystemRandom, SystemRandom as Random
from Crypto.Util.number import bytes_to_long, isPrime, getPrime

nmmnmmwmnnnwwn = os.getenv("FLAG", "srdnlen{REDACTED}").encode()
wwwwmnmmwnnn = 1337
nwwmnmwwmmwnww = SystemRandom(int(time()))
mwnwmwwmnmmn = [(nwwmnmwwmmwnww.randint(11, 19), nwwmnmwwmmwnww.randint(1, 200)) for _ in range(wwwwmnmmwnnn)]

class mnwwmwnwmww:
    def __init__(self, mwmmmwwmmwnmmmwm=None):
        self.mwmmnnnnwmnnwwwm = SystemRandom(mwmmmwwmmwnmmmwm)

    def mmnnnnnwwwnmw(self, wnwmnwmnmn, nwmnnnnmwmww, wnnmwmmmw):
        wmwwwnnmmmmw, mmnnwnwnm = mwnwmwwmnmmn[nwmnnnnmwmww]
        return (wnwmnwmnmn + wmwwwnnmmmmw) * mmnnwnwnm % 2 ** (wnnmwmmmw//2)

    def wmwnwnwm(self, mnwnmmnmnwmm):
        mnwnmmnmnwmm += 1
        while not isPrime(mnwnmmnmnwmm):
            mnwnmmnmnwmm += 1
        return mnwnmmnmnwmm

    def mmmwnmmnwmnwnwn(self, wmnwmnwnmww, wnnnmmnnwnnmwnm=None):
        assert wmnwmnwnmww % 2 == 0
        nmmwmwnnnmmm = int(bin(self.mwmmnnnnwmnnwwwm.getrandbits(wmnwmnwnmww))[2:].zfill(wmnwmnwnmww), 2)

        wwnmwwnnnwmmn, nwwnnmnnmwnw = nmmwmwnnnmmm >> (wmnwmnwnmww//2), nmmwmwnnnmmm % 2**(wmnwmnwnmww//2)
        for nwwwnmnn in range(wwwwmnmmwnnn):
            wwnmwwnnnwmmn, nwwnnmnnmwnw = nwwnnmnnmwnw, wwnmwwnnnwmmn ^ self.mmnnnnnwwwnmw(nwwnnmnnmwnw, nwwwnmnn, wmnwmnwnmww)

        nmmwmwnnnmmm = wwnmwwnnnwmmn << (wmnwmnwnmww//2) | nwwnnmnnmwnw

        if wnnnmmnnwnnmwnm == None:
            nmnwnwnnmm = Random(int(time()))
            wnnnmmnnwnnmwnm = nmnwnwnnmm.sample(population=range(wmnwmnwnmww), k=wmnwmnwnmww)

        nmmwmwnnnmmm = list(bin(nmmwmwnnnmmm)[2:].zfill(wmnwmnwnmww))
        nwwwnmnn = []
        for nwmmwnwmmwwnm in wnnnmmnnwnnmwnm:
            nwwwnmnn += [nmmwmwnnnmmm[nwmmwnwmmwwnm]]
        nmmwmwnnnmmm = int("".join(nwwwnmnn), 2)

        return nmmwmwnnnmmm, getPrime(wmnwmnwnmww), wnnnmmnnwnnmwnm

    def mwmwwmmnw(self, nmmmnwmwmnnmn, mnwwmnwwmmwnwnn, nmmmnnnnmnmnnnmm):
        return pow(nmmmnwmwmnnmn, mnwwmnwwmmwnwnn, nmmmnnnnmnmnnnmm)

    def wmnwwnnnwwnm(self, wmnmwnmwmnnw, wmmnmmnnnw, nmmwwwnmwmmmw):
        return pow(wmnmwnmwmnnw, wmmnmmnnnw, nmmwwwnmwmmmw)

def nwwmmmmmwnww():
    try:
        wwwmwwmw = mnwwmwnwmww(os.urandom(16))
        while True:
            nwmwwnwmwwwww = int(input(f"""
What do you want to do?
    1) Generate RSA primes
    2) Encrypt a message
    3) Decrypt a message
    4) Get the encrypted flag
    5) Exit

"""))
            match nwmwwnwmwwwww:
                case 1:
                    wnnwmwmww = int(input("Number of bits: "))
                    assert wnnwmwmww <= 1024
                    wmwwnwwmnn, nnnwmmwnn, mmmwmnnwmwnww = wwwmwwmw.mmmwnmmnwmnwnwn(wnnwmwmww)
                    print(f"{wmwwnwwmnn = }")
                    print(f"{nnnwmmwnn = }")
                    print(f"{mmmwmnnwmwnww = }")
                case 2:
                    mwmwmmmnwmnmwnw = bytes.fromhex(input("Message: "))
                    wnnwwmnn = int(input("e: "))
                    nmwwwnmwmnnnn = int(input("n: "))
                    mwnwwmnnm = wwwmwwmw.mwmwwmmnw(bytes_to_long(mwmwmmmnwmnmwnw), wnnwwmnn, nmwwwnmwmnnnn)
                    print(f"{mwnwwmnnm = }")
                case 3:
                    mmnwnmwwwwnmwmn = bytes.fromhex(input("Ciphertext: "))
                    nwnwwmnwwmnnwm = int(input("d: "))
                    nwmmnmwwwnn = int(input("n: "))
                    nmmnmmwww = wwwmwwmw.wmnwwnnnwwnm(bytes_to_long(mmnwnmwwwwnmwmn), nwnwwmnwwmnnwm, nwmmnmwwwnn)
                    print(f"{nmmnmmwww = }")
                case 4:
                    nmmmmnmmm, wmmmmnwnwmnw, nwnnnwwwwmnmmmn = wwwmwwmw.mmmwnmmnwmnwnwn(1024)
                    print(f"{nwnnnwwwwmnmmmn = }")
                    nmmmmnmmm = wwwmwwmw.wmwnwnwm(nmmmmnmmm)
                    nwnnnwwwwmnmmmn = 65537
                    wnnwmmmwmmwmm = nmmmmnmmm*wmmmmnwnwmnw
                    mnnmwnnnnmmw = wwwmwwmw.mwmwwmmnw(bytes_to_long(nmmnmmwmnnnwwn), nwnnnwwwwmnmmmn, wnnwmmmwmmwmm)
                    print(f"{mnnmwnnnnmmw = }")
                    print(f"{nwnnnwwwwmnmmmn = }")
                    print(f"{wnnwmmmwmmwmm = }")
                case 5:
                    exit(0)
                case _:
                    raise NotImplementedError
    except KeyboardInterrupt:
        raise
    except:
        raise Exception("Error")

if __name__ == "__main__":
    signal.alarm(300)
    print("Welcome to RSB, a super secure RSA service!")
    nwwmmmmmwnww()
