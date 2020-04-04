import tkinter as tk

from .scale import Scale


class Panel:
    def __init__(self, *args, **kwargs):
        self.frame = tk.Frame(*args, **kwargs)
        self.frame.grid(row=0, column=0)

        self.entries = dict()
        self.labels = dict()
        self.options = dict()
        self.scales = dict()

        self.rows = 0

    def add_entry(self, key, value, bind, *args, **kwargs):
        self.rows += 1

        entry = tk.Entry(self.frame, *args, **kwargs)
        entry.insert(0, value)
        entry.bind("<FocusOut>", bind)
        entry.bind("<Return>", bind)
        entry.grid(row=self.rows)

        self.entries[key] = entry

    def add_label(self, key, *args, **kwargs):
        self.rows += 1

        label = tk.Label(self.frame, *args, **kwargs)
        label.grid(row=self.rows)

        self.labels[key] = label

    def add_option_menu(self, key, bind, *args, **kwargs):
        self.rows += 1

        option = tk.StringVar()
        option.set(args[0])

        menu = tk.OptionMenu(self.frame, option, *args, **kwargs, command=bind)
        menu.config(width=14)
        menu.grid(row=self.rows)

        self.options[key] = option

    def add_scale(self, key, value, bind, *args, **kwargs):
        self.rows += 1

        scale = Scale(self.frame, *args, **kwargs)
        scale.set(value)
        scale.bind("<ButtonRelease-1>", bind)
        scale.grid(row=self.rows)

        self.scales[key] = scale
