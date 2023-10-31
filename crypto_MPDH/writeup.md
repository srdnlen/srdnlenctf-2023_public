# srdnlenctf 2023

## MPDH (8 solves)

Shoutout to [Elliptic Ring RSA](https://github.com/zer0pts/zer0pts-ctf-2023-public/tree/master/crypto/elliptic_ring_rsa) from [zer0pts ctf 2023](https://ctftime.org/event/1972) that inspired this challenge.

The challenge is a Diffie-Hellman between Alice and Bob in an unknown group $H$. The class `MPDH` implements this group operation using python `list[tuple[int, int]]` as elements. 

To recover the flag we need to first understand how the group operation works, then try to represent it in a known way, and last break the DH key exchange.

### Solution

We know that the elements of $H$ are of the form

$$ P = ( (j_0, p_0), (j_1, p_1), \dots, (j_{n - 1}, p_{n - 1}) ) $$

with $n = 32$, and $\forall i \in \mathbb{Z}_n.\ j_i \in \mathbb{Z}_n \land p_i \in \mathbb{Z}_q^* = \mathbb{Z}_q \setminus \{ 0 \}$, with $q$ prime of $90$ bits.

We know that the one of $H$ is $1_H = ( (0, 1), (1, 1), \dots, (n - 1, 1) )$ and that its multiplication, acording to `mul`, is defined as

```math
P \cdot P^{\prime} = ( (j^{\prime}_{j_0}, p_0 \cdot p^{\prime}_{j_0}), \dots, (j^{\prime}_{j_{n - 1}}, p_{n - 1} \cdot p^{\prime}_{j_{n - 1}}) )
```

<!-- on gihub same as $$ P \cdot P^{\prime} = ( (j^{\prime}_{j_0}, p_0 \cdot p^{\prime}_{j_0}), \dots, (j^{\prime}_{j_{n - 1}}, p_{n - 1} \cdot p^{\prime}_{j_{n - 1}}) ) $$ but without visual problems -->

for $P = ( (j_0, p_0), (j_1, p_1), \dots, (j_{n - 1}, p_{n - 1}) )$ and $`P^{\prime} = ( (j^{\prime}_0, p^{\prime}_0), (j^{\prime}_1, p^{\prime}_1), \dots, (j^{\prime}_{n - 1}, p^{\prime}_{n - 1}) )`$ <!-- $` and `$ exclusive to github -->.

One notices that the multiplication in $H$: for the first element $j_i$ of each pair in $P$, is defined similarly to the composition in the group of permutations of $n$ elements, whereas for the second element $p_i$ is defined as a multiplication in $\mathbb{Z}_q^*$ between the permutated pairs.

> Note that, the multiplication in $H$ goes from right to left, whereas the composition in the group of permutations goes from left to right. In the challenge solution we don't care about this, since we are working with powers of $G \in H$ and any multiplication between powers of $G$ is abelian.

One can express an arbitrary permutation of $n$ elements with a $n \times n$ **permutation matrix**. Thus, to represent an element of $H$, one needs to substitute each $1$ of the permutation matrix with its respective $p_i$, e.g. for $P \in H$

$$ P \cong \begin{pmatrix} v_0 \\\ v_1 \\\ \vdots \\\ v_n \end{pmatrix} $$

with $v_i = (0, \dots, p_i, \dots, 0)$, where the position of $p_i$ in the vector $v_i$ is given by $j_i$.

The matrices of this form, form a **subgroup** $K$ of $(GL_n(\mathbb{Z}_q), \cdot)$. There is an isomorphism $\gamma: H \rightarrow K$, so the result of any computation that we can do in $K$ can be brought back in $H$ easily, and vice versa.

Our **isomorphism** $\gamma$ written in *python* using *sagemath* could be:

```py
n = 32
q = next_prime(int(0x1337**7.331))
F = GF(q)

perm_to_matrix = lambda P: Matrix(F, [[p if i == j else 0 for j in range(n)] for i, p in P])
matrix_to_perm = lambda M: [(i, p) for row in M for i, p in enumerate(row) if p]
```

where `perm_to_matrix` is $\gamma$ and `matrix_to_perm` is $\gamma^{-1}$.

In $K$ we know how to compute a **discrete logarithm**: first we need to fully diagonalize a matrix $M = \gamma(P)$.

To fully diagonalize $M$, we need an extension field $`\mathbb{Z}_{q^k}`$ of $`\mathbb{Z}_q`$ that contains all of $M$ eigenvalues. The **matrix jordan form** of $M$ in $`\mathbb{Z}_{q^k}`$ will be fully diagonalized, thanks to a transformation matrix $T$.

Suppose that we need to recover $a$ knowing only $G, A = G^a$, then the transformation matrix $T$ of $G$, defined as above, will give $G^{\prime} = T^{-1} G T, A^{\prime} = T^{-1} A T$ diagonal matrices with entries in $\mathbb{Z}_{q^k}$. 

The multiplication between diagonal matrices is done $i^{th}$ entry by $i^{th}$ entry of the diagonal, thus we can compute the **discrete logarithm** $`\log_{G^{\prime}_{i, i}} A^{\prime}_{i, i}`$ for any $`i \in \mathbb{Z}_n`$, and, supposing that $`o(G^{\prime}_{i, i}) \ge a`$, we could recover $a$.

Putting all together we have:

```py
from sage.all import *
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

n = 32
q = next_prime(int(0x1337**7.331))
F = GF(q)

perm_to_matrix = lambda P: Matrix(F, [[p if i == j else 0 for j in range(n)] for i, p in P])
matrix_to_perm = lambda M: [(i, p) for row in M for i, p in enumerate(row) if p]

G = [...]
A = [...]
B = [...]
flag_enc = "3eb11fb88b1e83460ea9351819e7a9b1739a9af4d0ccde098b9cd414c1ac5273522184727f823e7362e396e16ba04357c7f9512ace28ea8764283a649ac58ba40b797498a5dfbeca63ff54e1c2d0fc31146b17265760161ec9e3783d09431b4e"

G, A, B = map(perm_to_matrix, [G, A, B])

poly = G.charpoly()
SF = poly.splitting_field("x")
GJ, T = G.jordan_form(SF, transformation=True)
AJ = T**-1 * A * T

for i in range(n):
    a = AJ[i, i].log(GJ[i, i])
    if G**a != A:
        continue
    K = matrix_to_perm(B**a)
    key = SHA256.new(str(K).encode()).digest()[:AES.key_size[-1]]
    flag = AES.new(key, AES.MODE_ECB).decrypt(bytes.fromhex(flag_enc))
    if b"srdnlen" in flag:
        print(flag)
        break
else:
    print("FAILED")
```
