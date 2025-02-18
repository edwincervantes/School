#!/usr/bin/env python 3.10
import random
import sys
import numpy as np

# returns the list of all permutations of elements 0, 1, ... , nn-1
def all_permutations(nn):
    # list of permutations
    L = []
    # mark[i] = True if i is used in running permutation
    mark = [False for _ in range(nn)]
    # running permutation
    p = [-1 for _ in range(nn)]

    # place all possible elements at the position i and recurse to i+1
    def perm(i):
        if i==nn:
            # if all elements are placed, add permutation
            L.append(p.copy())
            return

        for j in range(nn):
            # check if j is not already in running permutation
            if not mark[j]:
                # if it is not, place it at the place i and mark it
                p[i] = j
                mark[j] = True

                # recurse to i+1
                perm(i+1)

                # remove j from place i and de-mark it
                mark[j] = False
                p[i] = -1

    # initial call to generate all permutations
    perm(0)

    return L

# print permutations from list to filename
def print_permutations(perms, n, filename):
    # binary format for numbers
    s_format = '{0:0' + str(n) + 'b}'
    nn = 2 ** n

    with open(filename, 'w') as f:
        for x in perms:
            # generate string representation
            s_perm = ''
            for i in range(nn):
                s_perm += str.format(s_format, x[i]) + ' '

            # print string representation to file and on terminal
            print(s_perm[:-1])
            f.write(s_perm[:-1] + '\n')


# implementation of permutgen part
def permutgen(n, filename):
    # generate permutations
    nn = 2 ** n
    perms = all_permutations(nn)

    print_permutations(perms, n, filename)

# generate kk random different permutations of elements 0, 1, ... , nn-1
def rand_permutations(nn, kk):
    # all numbers and list of permutations
    nums = list(range(nn))
    L = []

    for i in range(kk):
        while True:
            # generate permutation and check whether it is already in L
            p = random.sample(nums, nn)
            if p not in L:
                # if not, break
                break

        L.append(p)

    return L

# implementation of prpgen part
def prpgen(n, l, filename):
    kk, nn = 2 ** l, 2 ** n
    perms = rand_permutations(nn, kk)

    print_permutations(perms, n, filename)

def read_Fk(k, perms_filename):
    with open(perms_filename, 'r') as f:
        # read permutations up to k-th
        for s in range(k):
            f.readline()

        # read k-th permutation
        s_perm = f.readline().split()

    # convert to int to form Fk
    Fk = [int(x, 2) for x in s_perm]
    # retrieve nn = 2**n and n
    nn = len(Fk)
    n = round(np.log2(nn))

    return Fk, n, nn

# invert permutation p
def perm_inv(p):
    n = len(p)

    # initialize inverse permutation
    p_inv = [0 for _ in range(n)]
    for i in range(n):
        # set p^{-1}(p(i))=i, i.e. p[i]-th element of p_inv is i
        p_inv[p[i]] = i

    # return inverse
    return p_inv

# encrypt the message m using k-th permutation from perms_file and write the output
# in cipher_filename. Uses cbc if is_cbc is True, otherwise ebc
def enc_cbc_ebc(m, l, k, perms_filename, cipher_filename, is_cbc=True):
    # read Fk
    Fk, n, nn = read_Fk(k, perms_filename)

    # if length of the message is not divisible by n, pad it with 0s
    if len(m) % n != 0:
        m += '0' * (n - len(m) % n)

    # generate IV (random number from 0 to nn-1
    c0 = random.randint(0, nn-1)

    # cipher
    if is_cbc:
        c = [c0]
    else:
        c = []
        
    for i in range(round(len(m) / n)):
        # retrieve i-th message block
        mi = m[i*n:(i+1)*n]

        if is_cbc:
            # compute the cipher as c_i = Fk( m_i xor c_{i-1})
            ci = Fk[int(mi, 2) ^ c[-1]]
        else:
            ci = Fk[int(mi, 2)]

        c.append(ci)

    # join all ci's into the cipher message
    s_format = '{0:0' + str(n) + 'b}'
    c_formatted = [ str.format(s_format, ci) for ci in c ]
    cipher = ''.join(c_formatted)

    # write cipher in an output file
    with open(cipher_filename, 'w') as f:
        f.write(cipher)

    print(c_formatted)


# decrypts the message from cipher_filename using k-th permutation from perms_filename
def dec_cbc(l, k, perms_filename, cipher_filename):
    # read Fk and invert it
    Fk, n, nn = read_Fk(k, perms_filename)
    Fk_inv = perm_inv(Fk)

    # read cipher
    with open(cipher_filename, 'r') as f:
        s_cipher = f.readline()

    # IV (c0)
    c0 = int(s_cipher[:n], 2)

    # decrypted msg
    m = []

    for i in range(1, round(len(s_cipher) / n)):
        # retrieve i-th cipher block
        ci = int(s_cipher[i * n:(i + 1) * n], 2)

        # compute the message block m_i = Fk_inv(c_i) xor c_{i-1}
        # now c0 has the role of c_{i-1}
        mi = Fk_inv[ci] ^ c0
        m.append(mi)

        # update c0
        c0 = ci

    # join all ci's into the message and print
    s_format = '{0:0' + str(n) + 'b}'
    msg = ''.join([str.format(s_format, mi) for mi in m])
    print(msg)


# main branch
if (len(sys.argv) == 1):
    pass
elif sys.argv[1] == 'permutegen':
    # retrieve other two command line params
    n = int(sys.argv[2][2:])
    filename = sys.argv[3]
    permutgen(n, filename)
elif sys.argv[1] == 'prpgen':
    # retrieve other two command line params
    n = int(sys.argv[2][2:])
    l = int(sys.argv[3][2:])
    filename = sys.argv[4]
    prpgen(n, l, filename)
elif sys.argv[1] == 'enc_cbc' or sys.argv[1] == 'enc_ebc':
    # retrieve other five command line params
    m = sys.argv[2][2:]
    l = int(sys.argv[3][2:])
    k = int(sys.argv[4][2:], 2)
    perms_filename = sys.argv[5]
    cipher_filename = sys.argv[6]

    enc_cbc_ebc(m, l, k, perms_filename, cipher_filename, is_cbc=sys.argv[1] == 'enc_cbc')
elif sys.argv[1] == 'dec_cbc':
    # retrieve other four command line params
    l = int(sys.argv[2][2:])
    k = int(sys.argv[3][2:], 2)
    perms_filename = sys.argv[4]
    cipher_filename = sys.argv[5]

    dec_cbc(l, k, perms_filename, cipher_filename)
else:
    print('Unknown option!')

