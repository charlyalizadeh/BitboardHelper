import tkinter as tk
from patterns import CareTaker, Observer
from utils import get_coord
from gui import EntryButton


class BitboardGUI(tk.Frame, Observer):
    def __init__(self, master, bitboard, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        Observer.__init__(self)

        self.bitboard = bitboard
        self.bitboard.attach(self)
        self.care_taker = CareTaker(self.bitboard)

        # Board
        self.board_frame = tk.Frame(self)
        self.buttons = [tk.Button(self.board_frame, text='0') for i in range(self.bitboard.size)]
        self.click_button_actions = []
        for i in range(self.bitboard.size):
            self.buttons[i].configure(command=lambda index=int(i): self._click_button(index))
        for i in range(self.bitboard.shape[0]):
            for j in range(self.bitboard.shape[1]):
                self.buttons[i * self.bitboard.shape[1] + j].grid(row=i, column=j)

        # Action buttons
        self.button_frame = tk.Frame(self)
        self.inverse_btn = tk.Button(self.button_frame, text='~ (not)', command=lambda: self.bitboard.inverse(True))
        self.set_all_btn = tk.Button(self.button_frame, text='Set all', command=lambda: self.bitboard.set_all(1, True))
        self.right_shift_btn = tk.Button(self.button_frame, text='>>', command=lambda: self.bitboard.right_shift(1))
        self.left_shift_btn = tk.Button(self.button_frame, text='<<', command=lambda: self.bitboard.left_shift(0))

        # StringVar for the EntryButton and Label
        self.decimal_value_strvar = tk.StringVar(self, '0')
        self.decimal_value_label = tk.Label(self, textvariable=self.decimal_value_strvar)
        self.value_entrybtn = EntryButton(self, button_kwargs={'command': lambda: self.set_bitboard()})

        # Button position
        self.inverse_btn.grid(row=0, column=0, sticky='')
        self.set_all_btn.grid(row=0, column=1, sticky='')
        self.right_shift_btn.grid(row=0, column=2, sticky='')
        self.left_shift_btn.grid(row=0, column=3, sticky='')
        self.value_entrybtn.grid(row=0, column=4, sticky='NESW')

        # Board + Button's Frame position
        self.value_entrybtn.grid(row=0, column=0)
        self.decimal_value_label.grid(row=0, column=1)
        self.board_frame.grid(row=1, column=0, columnspan=2)
        self.button_frame.grid(row=2, column=0, columnspan=2)

    def _update_decimal_value_strvar(self):
        value = self.bitboard.get_value(type='decimal')
        self.decimal_value_strvar.set(value)

    def _update_board(self):
        for i in range(self.bitboard.shape[0]):
            for j in range(self.bitboard.shape[1]):
                self.buttons[i * self.bitboard.shape[1] + j].config(text=str(self.bitboard.get_bit((i, j))))

    def _click_button(self, index):
        coord = get_coord(index, self.bitboard.shape)
        self.bitboard.inverse_one(coord)

    def update(self, subject):
        self._update_board()
        self._update_decimal_value_strvar()

    def set_bitboard(self):
        value = self.value_entrybtn.get()
        self.bitboard.set_value(int(value), type='decimal')
