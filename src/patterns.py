from datetime import datetime
from copy import deepcopy


class Memento:
    def __init__(self, state):
        self.state = state.copy()
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
            return False
        self.current_state_index -= 1
        self.originator.set_state(self.mementos[self.current_state_index].state)
        return True

    def redo(self):
        if not self.mementos or self.current_state_index == len(self.mementos) - 1:
            return False
        self.current_state_index += 1
        self.originator.set_state(self.mementos[self.current_state_index].state)
        return True

    @property
    def size(self):
        return len(self.mementos)

    def __str__(self):
        rep_str = ''
        for (i, m) in enumerate(self.mementos):
            if i == self.current_state_index:
                rep_str += '°°°°°°°°°°°°°\n' + m.__str__() + '\n°°°°°°°°°°°°\n'
            else:
                rep_str += m.__str__() + '\n'
        rep_str += f'Current state index: {self.current_state_index}'
        return rep_str


class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self):
        for o in self._observers:
            o.update(self)


class Observer:
    def __init__(self):
        pass

    def update(self, subject):
        pass
