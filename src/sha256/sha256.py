from src.common_functions import *
from src.constants.initial_values import InitialHashValuesSHA256
from src.constants.constant_list import SHA256Constants


def _pad_message_for_sha256(binary_string: str) -> str:
    length = len(binary_string)
    binary_string +=  '1'
    binary_string += (448 - (length + 1)%448) * '0'
    binary_string += '{:064b}'.format(length)
    return binary_string

def _get_512_bit_chunk_list(binary_string: str) -> list:
    number_of_chuncks = len(binary_string)//512
    chunks = [
        binary_string[i:i+512] for i in range(number_of_chuncks) 
    ]

    return [
        _get_32_bit_chunk_list(chunk) for chunk in chunks
    ]

def _get_32_bit_chunk_list(binary_string: str):
    return [
        int(binary_string[i:i+32], 2) for i in range(0, len(binary_string), 32)
    ]

def calculate_sha256(message: bytes) -> bytes:
    schedule_word_list = []
    binary_string = ''.join(['{:08b}'.format(i) for i in message])
    binary_string = _pad_message_for_sha256(binary_string)

    h0 = InitialHashValuesSHA256.hash_0
    h1 = InitialHashValuesSHA256.hash_1
    h2 = InitialHashValuesSHA256.hash_2
    h3 = InitialHashValuesSHA256.hash_3
    h4 = InitialHashValuesSHA256.hash_4
    h5 = InitialHashValuesSHA256.hash_5
    h6 = InitialHashValuesSHA256.hash_6
    h7 = InitialHashValuesSHA256.hash_7

    hash_word_list = [h0, h1, h2, h3, h4, h5, h6, h7]


    for chunck in _get_512_bit_chunk_list(binary_string):
        schedule_word_list[0:16] = chunck[0:16]

        for t in range(16, 64):
            word = SSIG1(schedule_word_list[t-2]) + schedule_word_list[t-7] + SSIG0(schedule_word_list[t-15]) + schedule_word_list[t-16]
            schedule_word_list.append(word % 2**32)
        

        for t in range(0, 64):
            T1 = (h7 + BSIG1(h4) + CH(h4, h5, h6) + SHA256Constants[t] + schedule_word_list[t]) % 2**32
            T2 = (BSIG0(h0) + MAJ(h0, h1, h2)) % 2**32
            h7 = h6
            h6 = h5
            h5 = h4
            h4 = (h3 + T1) % 2**32
            h3 = h2
            h2 = h1
            h1 = h0
            h0 = (T1 + T2) % 2**32

        hash_word_list[0] = (h0 + hash_word_list[0]) % (2**32)
        hash_word_list[1] = (h1 + hash_word_list[1]) % (2**32)
        hash_word_list[2] = (h2 + hash_word_list[2]) % (2**32)
        hash_word_list[3] = (h3 + hash_word_list[3]) % (2**32)
        hash_word_list[4] = (h4 + hash_word_list[4]) % (2**32)
        hash_word_list[5] = (h5 + hash_word_list[5]) % (2**32)
        hash_word_list[6] = (h6 + hash_word_list[6]) % (2**32)
        hash_word_list[7] = (h7 + hash_word_list[7]) % (2**32)
    
    return ''.join(['{:08x}'.format(h) for h in hash_word_list])
