__all__ = [
    'SSIG0', 'SSIG1', 'BSIG0', 'BSIG1', 'MAJ', 'CH'
]

SHR = lambda x, n: x >> n

ROTR = lambda x, n: ((x >> n) | (x << (32-n))) & (2**32 - 1)

ROTL = lambda x, n: (x << n) | (x >> (32-n))

CH = lambda x, y, z: (x & y) ^ ((~x) & z)

MAJ = lambda x, y, z: (x & y) ^ (x & z) ^ (y & z)

BSIG0 = lambda x: ROTR(x, 2) ^ ROTR(x, 13) ^ ROTR(x, 22)

BSIG1 = lambda x: ROTR(x, 6) ^ ROTR(x, 11) ^ ROTR(x, 25)

SSIG0 = lambda x: ROTR(x, 7) ^ ROTR(x, 18) ^ SHR(x, 3)

SSIG1 = lambda x: ROTR(x, 17) ^ ROTR(x, 19) ^ SHR(x, 10)
