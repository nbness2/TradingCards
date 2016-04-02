import math

rotate_amounts = []

for x in [[7, 12, 17, 22], [5, 9, 14, 20], [4, 11, 16, 23], [6, 10, 15, 21]]:
    for y in range(4):
        rotate_amounts.extend(x)

consts = [int(abs(math.sin(i+1)) * 2**32) & 0xFFFFFFFF for i in range(64)]
 
inits = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]
 
functs = 16*[lambda b, c, d: (b & c) | (~b & d)] + \
            16*[lambda b, c, d: (d & b) | (~d & c)] + \
            16*[lambda b, c, d: b ^ c ^ d] + \
            16*[lambda b, c, d: c ^ (b | ~d)]

idxfuncts = 16*[lambda i: i] + \
                  16*[lambda i: (5*i + 1)%16] + \
                  16*[lambda i: (3*i + 5)%16] + \
                  16*[lambda i: (7*i)%16]
 
def rotleft(x, amount):
    x &= 0xFFFFFFFF
    return ((x<<amount) | (x>>(32-amount))) & 0xFFFFFFFF

class Md5:
    def __init__(self, message):
        message = bytearray(message.encode())
        orig_len_in_bits = (8 * len(message)) & 0xffffffffffffffff
        message.append(0x80)
        while len(message)%64 != 56:
            message.append(0)
        message += orig_len_in_bits.to_bytes(8, byteorder='little')
        hash_blocks = inits[:]
        for chunk_ofst in range(0, len(message), 64):
            a, b, c, d = hash_blocks
            chunk = message[chunk_ofst:chunk_ofst+64]
            for i in range(64):
                f = functs[i](b, c, d)
                g = idxfuncts[i](i)
                to_rotate = a + f + consts[i] + int.from_bytes(chunk[4*g:4*g+4], byteorder='little')
                new_b = (b + rotleft(to_rotate, rotate_amounts[i])) & 0xFFFFFFFF
                a, b, c, d = d, new_b, b, c
            for i, val in enumerate([a, b, c, d]):
                hash_blocks[i] += val
                hash_blocks[i] &= 0xFFFFFFFF
        self.digest = sum(x<<(32*i) for i, x in enumerate(hash_blocks))
        self.hexdigest = '{:032x}'.format(int.from_bytes(self.digest.to_bytes(16, byteorder='little'), byteorder='big'))
