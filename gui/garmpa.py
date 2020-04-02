import tkinter as tk

from patterns import Sleeve
from .canvas import Canvas
from .panel import Panel


class Garmpa:
    def __init__(self, master=None):
        self.master = master

        self.panel = Panel(
            self.master,
            width=320,
            height=240,
            bd=2,
        )

        self.canvas = Canvas(
            self.master,
            width=540,
            height=900,
            bg="white",
            bd=2,
        )

        self.pattern = Sleeve(
            max_width=self.canvas.width,
            max_height=self.canvas.height
        )

        self._create_widgets()

        self.render()
        #self.update()

    def render(self):
        for line in self.pattern.lines:
            self.canvas.create_line(*line)

    def update(self):
        self.master.after(1000, self.update)

    def _create_widgets(self):
        # Option to change between inches and centimetres
        self.panel.add_label("units", text="Units")
        self.panel.add_option_menu("unit", self._update_units, "in", "cm")

        # Entries to change canvas size
        self.panel.add_label("canvas_size", text="Canvas Size")
        self.panel.add_label("canvas_width", text="Width")
        self.panel.add_entry(
            "canvas_width",
            self._convert(
                value=self.canvas.width,
                from_="pixels",
                to="inches"
            ),
            self._update_canvas_width
        )
        self.panel.add_label("canvas_height", text="Height")
        self.panel.add_entry(
            "canvas_height",
            self._convert(
                value=self.canvas.height,
                from_="pixels",
                to="inches"
            ),
            self._update_canvas_height
        )

        # Scales to adjust pattern
        for key, value in self.pattern.items():
            self.panel.add_scale(
                key,
                self._convert(
                    value=value,
                    from_="pixels",
                    to="inches"
                ),
                self._update_scale,
                from_=self._convert(
                    value=self.pattern.min(key),
                    from_="pixels",
                    to="inches"
                ),
                to=self._convert(
                    value=self.pattern.max(key),
                    from_="pixels",
                    to="inches"
                ),
                label=key.title(),
                orient=tk.HORIZONTAL
            )

    def _update_units(self, event):
        unit = str(event)

        # Update canvas size entries
        self._update_entry(
            "canvas_width",
            self._convert(
                value=self.canvas.width,
                from_="pixels",
                to=unit
            )
        )
        self._update_entry(
            "canvas_height",
            self._convert(
                value=self.canvas.height,
                from_="pixels",
                to=unit
            )
        )

        # Update scales
        for key, scale in self.panel.scales.items():
            scale.config(
                from_=self._convert(
                    value=self.pattern.min(key),
                    from_="pixels",
                    to=unit
                ),
                to=self._convert(
                    value=self.pattern.max(key),
                    from_="pixels",
                    to=unit
                )
            )
            scale.set(
                self._convert(
                    value=self.pattern.get(key),
                    from_="pixels",
                    to=unit
                )
            )

    def _update_canvas_width(self, event):
        width = self._convert(
            value=event.widget.get(),
            from_=self.panel.options["unit"].get(),
            to="pixels"
        )

        self._update_entry("canvas_width", width)
        self.canvas.config(width=width)

        self.render()

    def _update_canvas_height(self, event):
        height = self._convert(
            value=event.widget.get(),
            from_=self.panel.options["unit"].get(),
            to="pixels"
        )

        self._update_entry("canvas_height", height)
        self.canvas.config(height=height)

        self.render()

    def _update_scale(self, event):
        scale = event.widget

        self.pattern.set(scale.label.lower(), scale.get())

        self.render()

    def _update_entry(self, key, value):
        entry = self.panel.entries[key]

        entry.delete(0, tk.END)
        entry.insert(0, value)

    def _convert(self, value, from_, to):
        """Converts between pixels, inches, and centimetres."""
        pixel = ["pixels", "pixel", "pix", "p"]
        inch = ["inches", "inch", "in"]
        cm = ["centiemetres", "centermeters", "cm"]

        from_pixel = from_ in pixel
        from_inch = from_ in inch
        from_cm = from_ in cm

        to_pixel = to in pixel
        to_inch = to in inch
        to_cm = to in cm

        conversion = 0

        if from_pixel:
            if to_pixel:
                conversion = int(value)
            elif to_inch:
                conversion = round(value / 72, 1)
            elif to_cm:
                conversion = round(value * 2.54 / 72, 1)
            else:
                raise NotImplementedError(f"Unit '{to}' is not defined")
        elif from_inch:
            if to_pixel:
                conversion = int(value * 72)
            elif to_inch:
                conversion = round(value, 1)
            elif to_cm:
                conversion = round(value * 2.54, 1)
            else:
                raise NotImplementedError(f"Unit '{to}' is not defined")
        elif from_cm:
            if to_pixel:
                conversion = int(value * 72 / 2.54)
            elif to_inch:
                conversion = round(value / 2.54, 1)
            elif to_cm:
                conversion = round(value, 1)
            else:
                raise NotImplementedError(f"Unit '{to}' is not defined")
        else:
            raise NotImplementedError(f"Unit '{from_}' is not defined")

        return conversion

