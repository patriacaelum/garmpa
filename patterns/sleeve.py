from .pattern import Pattern


class Sleeve(Pattern):
    def __init__(self, max_width, max_height):
        super().__init__()

        self.data = {
            "arm": 864,
            "gap": 144,
            "variance": 144,
            "shoulder": 432,
            "bicep": 432,
            "elbow": 360,
            "wrist": 324,
        }

        for key in self.data.keys():
            self.min_vals[key] = 5

        self.set_boundaries(max_width, max_height)

    def set_boundaries(self, max_width=None, max_height=None):
        if max_width is not None:
            width = int(max_width)

            self.max_vals.update({
                "variance": width,
                "shoulder": width,
                "bicep": width,
                "elbow": width,
                "wrist": width
            })

        if max_height is not None:
            height = int(max_height)

            self.max_vals.update({
                "arm": height,
                "gap": height - 5
            })

        self._assert_values()
        self.lines = self._create_lines()

    def _create_lines(self):
        width = self.max("shoulder")
        height = self.max("arm")

        arm = self.get("arm")
        bicep = self.get("bicep")
        gap = self.get("gap")
        wrist = self.get("wrist")

        lines = [
            # Centre Arm
            [
                width / 2, (height - arm) / 2,
                width / 2, (height + arm) / 2,
            ],
            # Left Arm
            [
                (width - bicep) / 2, (height - arm) / 2 + gap,
                (width - wrist) / 2, (height + arm) / 2,
            ],
            # Right Arm
            [
                (width + bicep) / 2, (height - arm) / 2 + gap,
                (width + wrist) / 2, (height + arm) / 2
            ],
            # Bicep
            [
                (width - bicep) / 2, (height - arm) / 2 + gap,
                (width + bicep) / 2, (height - arm) / 2 + gap,
            ],
            # Wrist
            [
                (width - wrist) / 2, (height + arm) / 2,
                (width + wrist) / 2, (height + arm) / 2,
            ],
        ]

        return lines

