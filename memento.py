import bitboard
from datetime import datetime
from copy import deepcopy


class Memento:
    def __init__(self, state):
        self.state = deepcopy(state)
        self.date = datetime.now()

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value

    def __str__(self):
        return f'{self.date.strftime("%Y-%m-%d %H:%M:%S")}\n{self.state}\n'


class CareTaker:
    def __init__(self, originator):
        self.current_state_index = -1
        self.mementos = []
        self.originator = originator

    def save(self):
        if self.current_state_index < len(self.mementos) - 1:
            self.mementos = self.mementos[:self.current_state_index + 1]
        self.mementos.append(Memento(self.originator))
        self.current_state_index += 1

    def undo(self):
        if not self.mementos or self.current_state_index == 0:
            return None
        self.current_state_index -= 1
        self.originator.set_state(self.mementos[self.current_state_index].state)

    def redo(self):
        if not self.mementos or self.current_state_index == len(self.mementos) - 1:
            return None
        self.current_state_index += 1
        self.originator.set_state(self.mementos[self.current_state_index].state)

    def __str__(self):
        return ''.join([m.__str__() for m in self.mementos]) + f'Current state index: {self.current_state_index}'
