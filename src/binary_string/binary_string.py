from array import array
from typing import Union


class BinaryString:
    def __init__(self, string: Union[str, bytes], size: int = 64):

        if isinstance(string, str):
            self.binary_string: array = self._make_array_from_binary_string_(string)
        elif isinstance(string, bytes):
            self.binary_string: array = self._make_array_from_binary_bytes_(string)
        elif isinstance(string , int):
            string = bin(string)[2:]
            self.binary_string: array = self._make_array_from_binary_string_(string)
        elif string is None:
            self.binary_string: array = array('b')
        else:
            raise TypeError('Not valid type.')

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
        self.integer_value = self.integer_value + other.integer_value

    def __radd__(self, other):
        self.__add__(other)
