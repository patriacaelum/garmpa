import numpy as np

from .pattern import Pattern


class Sleeve(Pattern):
    """A simple long-sleeve pattern.

    max_width: (int) the maximum possible width measurement, in pixels.
    max_height: (int) the maximum possible height measurement, in pixels.
    """
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

    def set(self, key, value):
        """Sets the measurement for the given key, in pixels.

        The "shoulder" and "bicep" keys are linked together.

        key: (str)
        value: (int)
        """
        if key in ["shoulder", "bicep"]:
            super().set("shoulder", value)
            super().set("bicep", value)
        else:
            super().set(key, value)

    def set_boundaries(self, max_width=None, max_height=None):
        """Sets the minimum and maximum possible values for each key.

        max_width: (int) the maximum possible width, in pixels. This affects the
                   variance, shoulder line, bicep line, elbow line, and wrist
                   line.
        max_height: (int) the maximum possible height, in pixels. This affects
                    the arm lines and the gap height.
        """
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
                "gap": height // 2
            })

        super().set_boundaries()

    def _create_lines(self):
        """Creates the lines to draw the sleeve pattern.

        returns: (list) a list of lists, where each list is alternating x and y
                 corrdinates which define the vertices which are connected by
                 lines.
        """
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

