import tkinter as tk


class Scale(tk.Scale):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def label(self):
        return self.config()["label"][-1]
