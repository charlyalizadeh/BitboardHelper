import tkinter as tk
from patterns import CareTaker, Observer
from utils import get_coord
from util_gui import EntryButton


class BitboardGUI(tk.Frame, Observer):
    def __init__(self, master, bitboard, bg='white', fg='black', **kwargs, ):
        tk.Frame.__init__(self, master, bg=bg, **kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        Observer.__init__(self)

        self.bitboard = bitboard
        self.bitboard.attach(self)
        self.care_taker = CareTaker(self.bitboard)
        self.care_taker.save()

        # Board
        self.board_frame = tk.Frame(self, bg=bg)
        self.buttons = [tk.Button(self.board_frame, text='0', bg=bg, fg=fg) for i in range(self.bitboard.size)]
        self.click_button_actions = []
        for i in range(self.bitboard.size):
            self.buttons[i].configure(command=lambda index=int(i): self._click_button(index))
        for i in range(self.bitboard.shape[0]):
            for j in range(self.bitboard.shape[1]):
                self.buttons[i * self.bitboard.shape[1] + j].grid(row=i, column=j, sticky='nsew')

        # Action buttons
        self.button_frame = tk.Frame(self, bg=bg)
        self.inverse_btn = tk.Button(self.button_frame, text='~ (not)', command=lambda: self.bitboard.inverse(True), bg=bg, fg=fg)
        self.set_all_btn = tk.Button(self.button_frame, text='Set all', command=lambda: self.bitboard.set_all(1, True), bg=bg, fg=fg)
        self.right_shift_btn = tk.Button(self.button_frame, text='>>', command=lambda: self.bitboard.right_shift(1), bg=bg, fg=fg)
        self.left_shift_btn = tk.Button(self.button_frame, text='<<', command=lambda: self.bitboard.left_shift(1), bg=bg, fg=fg)
        self.undo_btn = tk.Button(self.button_frame, text='<-', command=lambda: self._undo(), bg=bg, fg=fg)
        self.redo_btn = tk.Button(self.button_frame, text='->', command=lambda: self._redo(), bg=bg, fg=fg)

        # StringVar for the EntryButton and Label
        self.decimal_value_strvar = tk.StringVar(self, '0')
        self.decimal_value_label = tk.Label(self, textvariable=self.decimal_value_strvar, bg=bg, fg=fg)
        self.value_entrybtn = EntryButton(self,
                                          button_kwargs={'command': lambda: self.set_bitboard(), 'bg': bg, 'fg': fg},
                                          entry_kwargs={'bg': bg, 'fg': fg},
                                          bg=bg)


        # Button position
        self.inverse_btn.grid(row=0, column=0, sticky='nsew')
        self.set_all_btn.grid(row=0, column=1, sticky='nsew')
        self.right_shift_btn.grid(row=0, column=2, sticky='nsew')
        self.left_shift_btn.grid(row=0, column=3, sticky='nsew')
        self.undo_btn.grid(row=0, column=4, sticky='nsew')
        self.redo_btn.grid(row=0, column=5, sticky='nsew')
        self.value_entrybtn.grid(row=0, column=4, sticky='nsew')

        # Board + Button's Frame position
        self.value_entrybtn.grid(row=0, column=0, sticky='nsew')
        self.value_entrybtn.columnconfigure(0, weight=1)
        self.value_entrybtn.rowconfigure(0, weight=1)

        self.decimal_value_label.grid(row=0, column=1, sticky='nsew')
        self.decimal_value_label.columnconfigure(0, weight=1)
        self.decimal_value_label.rowconfigure(0, weight=1)

        self.board_frame.grid(row=1, column=0, columnspan=2, sticky='nsew')
        self.board_frame.columnconfigure(list(range(self.bitboard.shape[1])), weight=1)
        self.board_frame.rowconfigure(list(range(self.bitboard.shape[0])), weight=1)

        self.button_frame.grid(row=2, column=0, columnspan=2, sticky='nsew')
        self.button_frame.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=15)


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

    def _undo(self):
        self.care_taker.undo()
        self.update(None, False)

    def _redo(self):
        self.care_taker.redo()
        self.update(None, False)

    def update(self, subject, save=True):
        self._update_board()
        self._update_decimal_value_strvar()
        if save:
            self.care_taker.save()

    def set_bitboard(self):
        value = self.value_entrybtn.get()
        self.bitboard.set_value(int(value), type='decimal')
