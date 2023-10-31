from Crypto.Util.number import getStrongPrime, bytes_to_long

flag = b"srdnlen{W3lc0m3_t0_srdnlen_ctf_2023_crypt0_ch4ll3ng3s}"

nbits = 512
e = 0x10001
r, s, a = [getStrongPrime(nbits, e=e) for _ in range(3)]

rsa = r * s * a
r_s_a = r + s + a
rs_ra_sa = r * s + r * a + s * a

flag_enc = pow(bytes_to_long(flag), e, rsa)

print(f"{flag_enc = }")
print(f"{rsa = }")
print(f"{r_s_a = }")
print(f"{rs_ra_sa = }")
