from array import array
from typing import Union


class BinaryString:
    def __init__(self, string: Union[str, bytes] = None, integer_value: int = None, size: int = None):

        self.size = size

        if isinstance(string, str):
            self.integer_value = int.from_bytes(string.encode(), 'big')
        elif isinstance(string, bytes):
            self.integer_value = int.from_bytes(string, 'big')
        elif isinstance(integer_value , int):
            string = bin(integer_value)[2:]
            self.binary_string: array = self._make_array_from_binary_string_(string)
        elif string is None:
            self.binary_string: array = array('b')
        else:
            raise TypeError('Not valid type.')
        
        if size is not None:
            self._padd_zeros_from_left_(size)
    
    def _padd_zeros_from_left_(self, size: int):
        length = len(self)
        zeros = (size - (length % size)) * [0]
        self.binary_string = array('b', zeros) + self.binary_string

    def _get_integer_value_(self) -> int: 
        ...

    @property
    def integer_value(self):
        return int(''.join(map(str, self.binary_string)), 2)
    
    @integer_value.setter
    def integer_value(self, value):
        if not isinstance(value , int):
            raise TypeError
        string = bin(value)[2:]
        self.binary_string = self._make_array_from_binary_string_(string)

    def __int__(self):
        return int(''.join(map(str, self.binary_string)), 2)

    @staticmethod
    def _make_array_from_binary_string_(string: str) -> array:
        return array('b', [1 if bit == '1' or bit is True else 0 for bit in string])
        
    @staticmethod
    def _make_array_from_binary_bytes_(string: bytes) -> array:
        return array('b', [1 if bit == 1 or bit is True else 0 for bit in string])
    
    def __repr__(self):
        return '-'.join(map(str, self.binary_string))

    def __str__(self):
        return '-'.join(map(str, self.binary_string))

    def __add__(self, other):
        if not isinstance(other, (BinaryString, int, bytes)):
            raise ValueError
        
        if isinstance(other, BinaryString):
            integer_value = (self.integer_value + other.integer_value ) % 2**32
        elif isinstance(other, bytes):
            integer_value = (self.integer_value + int.from_bytes(other, 'big') ) % 2**32
        elif isinstance(other, int):
            integer_value = (self.integer_value + other) % 2**32

        return BinaryString(integer_value=integer_value, size=self.size)

    def __radd__(self, other):
        return self.__add__(other)

    def to_hex(self):
        return hex(int(''.join(str(bit) for bit in self.binary_string), 2))[2:]

    def pad512(self):
        length = len(self.binary_string)
        self.binary_string += array('b', [1])
        zeros = (448 - ((length+1) % 448)) * [0]
        self.binary_string += array('b', zeros)
        self.binary_string += BinaryString(integer_value=length, size=64).binary_string

    def __len__(self):
        return len(self.binary_string)

    def get_512_bits_chunks(self):
        number_of_chuncks = len(self)//512
        chunk_list = [
            self.binary_string[i:i+512] for i in range(number_of_chuncks) 
        ]
        return [
            self._get_32_bits_mini_chunks(chunk) for chunk in chunk_list
        ]

    @staticmethod
    def _get_32_bits_mini_chunks(chunc_512_bit: array):
        chunk_list = [
            chunc_512_bit[i:i+32] for i in range(16)
        ]
        return [
            BinaryString(integer_value=bytes(chunk), size=32) for chunk in chunk_list
        ]
        # return [
        #     int(''.join(map(str, chunk)), 2) for chunk in mini_chunk_list
        # ]

    def __or__(self, other):
        result = self.integer_value | other.integer_value
        return BinaryString(integer_value=result, size=self.size)

    def __ror__(self, other):
        return self.__or__(other)

    def __xor__(self, other):
        if isinstance(other, BinaryString):
            result = self.integer_value ^ other.integer_value
        elif isinstance(other, int):
            result = self.integer_value ^ other
    
        return BinaryString(integer_value=result, size=self.size)

    def __rxor__(self, other):
        return self.__or__(other)

    def __and__(self, other):
        if isinstance(other, BinaryString):
            result = self.integer_value & other.integer_value
        elif isinstance(other, int):
            result = self.integer_value & other
    
        return BinaryString(integer_value=result, size=self.size)
    
    def __rand__(self, other):
        return self.__and__(other)

    def __lshift__(self, n):
        result = self.integer_value << n
        return BinaryString(integer_value=result, size=self.size)
    
    def __rlshift__(self, n):
        return self.__lshift__(n)
    
    def __rshift__(self, n):
        result = self.integer_value >> n
        return BinaryString(integer_value=result, size=self.size)

    def __rrshift__(self, n):
        return self.__rshift__(n)

    def __invert__(self):
        return BinaryString(integer_value=~self.integer_value, size=self.size)
