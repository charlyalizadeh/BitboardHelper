import tkinter as tk


class EntryButton(tk.Frame):
    def __init__(self, master, entry_text='', button_text='ok',
                 entry_kwargs={}, button_kwargs={}, **frame_kwargs):
        super().__init__(master, **frame_kwargs)
        self.button = tk.Button(self, text=button_text, **button_kwargs)
        self.entry = tk.Entry(self, **entry_kwargs)
        self.button.pack(side=tk.RIGHT)
        self.entry.pack(side=tk.LEFT)

    def get(self):
        return self.entry.get()

