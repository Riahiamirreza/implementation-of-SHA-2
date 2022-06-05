from array import array
from typing import Union


class BinaryString:
    def __init__(self, string: Union[str, bytes] = None, integer_value: int = None, size: int = None):

        if isinstance(string, str):
            self.binary_string: array = self._make_array_from_binary_string_(string)
        elif isinstance(string, bytes):
            self.binary_string: array = self._make_array_from_binary_bytes_(string)
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
        if not isinstance(other, BinaryString):
            raise ValueError
        integer_value = self.integer_value + other.integer_value
        return BinaryString(integer_value=integer_value)

    def __radd__(self, other):
        self.__add__(other)

    def to_hex_(self):
        return hex(int(''.join(str(bit) for bit in self.binary_string), 2))[2:]

    def pad512(self):
        self.binary_string += array('b', [1])
        length = len(self.binary_string)
        zeros = (448 - (length % 448)) * [0]
        self.binary_string += array('b', zeros)

    def __len__(self):
        return len(self.binary_string)
