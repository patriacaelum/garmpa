class Pattern:
    """Abstract class for all garment patterns.

    The abstract methods `set_boundaries()` and `_create_lines()` methods should
    be overrided.

    All values are measured in pixels.
    """
    def __init__(self):
        self.data = dict()
        self.min_vals = dict()
        self.max_vals = dict()
        self.lines = list()

    def get(self, key):
        """Returns the measurement for the given key, in pixels.

        key: (str)

        returns: (int or None)
        """
        return self.data.get(key)

    def set(self, key, value):
        """Sets the measurement for the given key, in pixels.

        key: (str)
        value: (int)
        """
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
        """Gets the minimum possible value for the given key, in pixels.

        key: (str)

        returns: (int)
        """
        return self.min_vals.get(key)

    def max(self, key):
        """Gets the maximum possible value for the given key, in pixels.

        key: (str)

        returns: (int)
        """
        return self.max_vals.get(key)

    def items(self):
        """Returns an interator of the each key and its measurement, in pixels.

        returns: (iter)
        """
        return self.data.items()

    def set_boundaries(self, max_width=None, max_height=None):
        """Sets the minimum and maximum possible values for each key.

        This method should be overrided in the child class.

        max_width: (int) the maximum possible width, in pixels.
        max_height: (int) the maximum possible height, in pixels.
        """
        self._assert_values()
        self.lines = self._create_lines()

    def _create_lines(self):
        """Creates the lines to draw the garment pattern.

        returns: (list) a list of lists, where each inner list has alternating
                 x and y coordinates which define the vertices which are
                 connected by lines.
        """
        return list()

    def _assert_values(self):
        """Checks that each key has a corresponding minimum and maximum value.

        This method should be called after the constructor in the child class.
        """
        for key, value in self.data.items():
            assert isinstance(value, int)

            assert isinstance(self.min_vals.get(key), int)
            assert isinstance(self.max_vals.get(key), int)

            assert self.min(key) <= value
            assert self.max(key) >= value

