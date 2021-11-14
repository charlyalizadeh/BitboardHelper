import tkinter as tk
from bitboard import Bitboard
from bitboard_gui import BitboardGUI
import numpy as np


window = tk.Tk()
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)
window.configure()
b = BitboardGUI(window, Bitboard(), bg='grey')
b.grid(row=0, column=0, sticky='nsew')
window.mainloop()
