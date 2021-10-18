import numpy as np


class Bitboard:
    def __init__(self, bit_array=np.zeros((8, 8))):
        self.bit_array = bit_array.astype(int)

    def set_state(self, state):
        self.bit_array = state.bit_array.copy()

    def set_bit(self, coord, state):
        if state not in (0, 1):
            raise ValueError(f"state must be 0 or 1, got {state}")
        self.bit_array[coord] = state

    def right_shift(self, n):
        shape = self.bit_array.shape
        bit_array_flatten = np.flip(self.bit_array, 1).flatten()
        bit_array_flatten = np.roll(bit_array_flatten, n, 0)
        bit_array_flatten[:n] = 0
        self.bit_array = np.flip(np.reshape(bit_array_flatten, shape), 1)

    def left_shift(self, n):
        shape = self.bit_array.shape
        bit_array_flatten = np.flip(self.bit_array, 1).flatten()
        bit_array_flatten = np.roll(bit_array_flatten, -n, 0)
        bit_array_flatten[-n:] = 0
        self.bit_array = np.flip(np.reshape(bit_array_flatten, shape), 1)

    def set_all(self, state):
        if state not in (0, 1):
            raise ValueError(f"state must be 0 or 1, got {state}")
        self.bit_array[:] = state

    def inverse(self):
        bit_array = np.logical_not(self.bit_array).astype(int)
        return Bitboard(bit_array)

    def logical_and(self, other):
        result = np.logical_and(self.bit_array, other.bit_array).astype(int)
        return Bitboard(result)

    def logical_or(self, other):
        result = np.logical_or(self.bit_array, other.bit_array).astype(int)
        return Bitboard(result)

    def logical_xor(self, other):
        result = np.logical_xor(self.bit_array, other.bit_array).astype(int)
        return Bitboard(result)

    def logical_xand(self, other):
        return self.logical_xor(other).inverse()

    def __str__(self):
        return self.bit_array.__str__()
