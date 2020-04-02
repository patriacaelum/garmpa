import tkinter as tk


class Canvas(tk.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid(row=0, column=1)

        self.args = args
        self.kwargs = kwargs

    def config(**kwargs):
        self.kwargs.update(kwargs)

        super().config(**kwargs)

        self._reset()

    @property
    def width(self):
        return self.kwargs.get("width")

    @property
    def height(self):
        return self.kwargs.get("height")

    def _reset(self):
        self.destroy()

        super().__init__(*self.args, **self.kwargs)

        self.grid(row=0, column=1)
