class Pattern:
    """Abstract class for all garment patterns.

    The `_assert_values()` and `_create_lines()` methods should be called after
    the constructor.

    All values are measured in pixels.
    """
    def __init__(self):
        self.data = dict()
        self.min_vals = dict()
        self.max_vals = dict()
        self.lines = list()

    def get(self, key):
        return self.data.get(key)

    def set(self, **kwargs):
        for key, value in kwargs.items():
            val = int(value)

            if key not in self.data.keys():
                raise ValueError(f"'{key}' key does not exist")

            if val < self.min(key) or val > self.max(key):
                raise ValueError(
                    f"'{value}' value is not within range for '{key}' key"
                )

            self.data[key] = val

        self.lines = self._create_lines()

    def min(self, key):
        return self.min_vals.get(key)

    def max(self, key):
        return self.max_vals.get(key)

    def items(self):
        return self.data.items()

    def set_boundaries(self, max_width=None, max_height=None):
        pass

    def _create_lines(self):
        return list()

    def _assert_values(self):
        for key, value in self.data.items():
            assert isinstance(value, int)

            assert isinstance(self.min_vals.get(key), int)
            assert isinstance(self.max_vals.get(key), int)

            assert self.min(key) <= value
            assert self.max(key) >= value

