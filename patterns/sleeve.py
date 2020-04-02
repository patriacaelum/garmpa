import numpy as np

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

            if width % 2 != 0:
                raise ValueError(
                    "Maximum canvas width should be a multiple of 2"
                )

            self.max_vals.update({
                "variance": width,
                "shoulder": width,
                "bicep": width,
                "elbow": width,
                "wrist": width
            })

        if max_height is not None:
            height = int(max_height)

            if height % 2 != 0:
                raise ValueError(
                    "Maximum canvas height should be a multiple of 2"
                )

            self.max_vals.update({
                "arm": height,
                "gap": height - 5
            })

        self._assert_values()
        self.lines = self._create_lines()

    def _create_lines(self):
        width = self.max("shoulder")
        height = self.max("arm")

        variance = self.get("variance")
        shoulder = self.get("shoulder")
        arm = self.get("arm")
        bicep = self.get("bicep")
        gap = self.get("gap")
        wrist = self.get("wrist")

        shoulderx = np.arange(
            start=-shoulder // 2,
            stop=shoulder // 2 + 1,
        )
        normal = np.exp(- 0.5 * np.power(shoulderx / variance, 2))
        normal = normal - np.min(normal)
        shouldery = - gap * normal / np.max(normal)

        shoulder_line = list(range(0, len(shoulderx) * 2))
        for i in range(len(normal)):
            shoulder_line[i * 2] = int(shoulderx[i]) + width / 2
            shoulder_line[i * 2 + 1] = int(
                shouldery[i] + (height - arm) / 2 + gap
            )

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
            # Shoulder
            shoulder_line,
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

