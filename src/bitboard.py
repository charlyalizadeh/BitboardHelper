import numpy as np
from patterns import Subject


class Bitboard(Subject):
    def __init__(self, bit_array=np.zeros((8, 8))):
        super().__init__()
        self.bit_array = bit_array.astype(int)

    @property
    def shape(self):
        return self.bit_array.shape

    @property
    def size(self):
        return self.bit_array.size

    def set_state(self, state):
        self.bit_array = state.bit_array.copy()

    def inverse_one(self, coord):
        self.bit_array[coord] = 1 if self.bit_array[coord] == 0 else 0
        self.notify()

    def set_bit(self, coord, state):
        if state not in (0, 1):
            raise ValueError(f"state must be 0 or 1, got {state}")
        self.bit_array[coord] = state
        self.notify()

    def get_bit(self, coord):
        return self.bit_array[coord]

    def right_shift(self, n):
        shape = self.bit_array.shape
        bit_array_flatten = np.flip(self.bit_array, 1).flatten()
        bit_array_flatten = np.roll(bit_array_flatten, n, 0)
        bit_array_flatten[:n] = 0
        self.bit_array = np.flip(np.reshape(bit_array_flatten, shape), 1)
        self.notify()

    def left_shift(self, n):
        shape = self.bit_array.shape
        bit_array_flatten = np.flip(self.bit_array, 1).flatten()
        bit_array_flatten = np.roll(bit_array_flatten, -n, 0)
        bit_array_flatten[-n:] = 0
        self.bit_array = np.flip(np.reshape(bit_array_flatten, shape), 1)
        self.notify()

    def set_all(self, state, inplace=False):
        if state not in (0, 1):
            raise ValueError(f"state must be 0 or 1, got {state}")
        if inplace:
            self.bit_array[:] = state
            self.notify()
        else:
            bit_array = self.bit_array.copy()
            bit_array[:] = state
            return Bitboard(state)

    def inverse(self, inplace=False):
        if inplace:
            self.bit_array = np.logical_not(self.bit_array).astype(int)
            self.notify()
        else:
            bit_array = np.logical_not(self.bit_array).astype(int)
            return Bitboard(bit_array)

    def logical_and(self, other, inplace=False):
        if inplace:
            self.bit_array = np.logical_and(self.bit_array, other.bit_array).astype(int)
            self.notify()
        else:
            result = np.logical_and(self.bit_array, other.bit_array).astype(int)
            return Bitboard(result)

    def logical_or(self, other, inplace=False):
        if inplace:
            self.bit_array = np.logical_or(self.bit_array, other.bit_array).astype(int)
            self.notify()
        else:
            result = np.logical_or(self.bit_array, other.bit_array).astype(int)
            return Bitboard(result)

    def logical_xor(self, other, inplace=False):
        if inplace:
            self.bit_array = np.logical_xor(self.bit_array, other.bit_array).astype(int)
            self.notify()
        else:
            result = np.logical_xor(self.bit_array, other.bit_array).astype(int)
            return Bitboard(result)

    def logical_xand(self, other, inplace=False):
        if inplace:
            self.logical_xor(other, True)
            self.inverse(True)
            self.notify()
        else:
            return self.logical_xor(other).inverse()

    def get_value(self, type='binary'):
        value = ''
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                value += str(self.bit_array[i, (self.shape[1] - 1) - j])
        if type == 'binary':
            return value
        elif type == 'decimal':
            return str(int(value, 2))

    def set_value(self, value, type='decimal'):
        if type == 'decimal':
            value = '{0:064b}'.format(value)
        bit_string = [int(v) for v in list(value)]
        for n in range(self.size):
            i = int(n / self.shape[1])
            j = - n + (i + 1) * self.shape[1] - 1
            self.set_bit((i, j), int(bit_string[n]))
        self.notify()

    def copy(self):
        bit_array = self.bit_array.copy()
        bb = Bitboard(bit_array)
        bb._observers = self._observers
        return bb

    def __str__(self):
        return self.bit_array.__str__()
