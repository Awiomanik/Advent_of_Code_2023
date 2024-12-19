"""
COORD Class Implementation

This file defines the `COORD` class that supports integer and floating-point values 
and provides a variety of mathematical operations and comparisons for working with coordinates in 2D space.

Key Features:
-------------
1. **Initialization**:
   - Coordinates can be integers or floating-point numbers.
   - Example: `COORD(3, 4)` or `COORD(1.5, 2.7)`.

2. **Magic Methods**:
   - Supports addition (`+`), subtraction (`-`), scalar multiplication (`*`), and scalar division (`/`).
   - Allows comparisons (`<`, `<=`, `==`) with other `COORD` objects or scalar values.
   - Implements `__str__` and `__repr__` for readable and debug-friendly string representations.

3. **Non-Standard Comparisons**:
   - `__lt__` and `__le__` compare both `x` and `y` components simultaneously.
   - When compared to scalar values, both `x` and `y` are compared independently to the scalar.

4. **Advanced Operations**:
   - Compute the magnitude of the coordinate (distance from origin).
   - Calculate the dot product with another `COORD`.
   - Check if `COORD` is inside a gride of given bounds

5. **Error Handling**:
   - Ensures all operations involve valid types (`COORD`, `int`, or `float`).
   - Provides meaningful error messages for invalid operations.


Example Usage:
--------------
```python
coord1 = COORD(3, 4)
coord2 = COORD(6, 8)

# Basic arithmetic
print(coord1 + coord2)       # COORD(x=9, y=12)
print(coord1 * 2)            # COORD(x=6, y=8)

# Comparisons
print(coord1 < coord2)       # True
print(coord1 < 5)            # True (both 3 and 4 are less than 5)

# Magnitude and dot product
print(coord1.magnitude())    # 5.0
print(coord1.dot(coord2))    # 50

# Handling errors
try:
    coord1 + "string"
except TypeError as e:
    print(e)  # "Operands must be of type 'COORD', 'int' or 'float'"

# Notes:
Non-standard comparisons (e.g., __lt__ and __le__) may behave differently than expected for some users. 
Both components (x and y) must satisfy the condition for the comparison to be true.
"""

class COORD:
    # Constructor
    def __init__(self, x, y=None):
        # Handle initialization from a tuple
        if isinstance(x, tuple) and len(x) == 2:
            if not all(isinstance(i, (int, float)) for i in x):
                raise TypeError("COORD tuple elements must be integers or floats")
            self.x, self.y = x
        # Handle initialization from individual x, y values
        elif isinstance(x, (int, float)) and isinstance(y, (int, float)):
            self.x = x
            self.y = y
        else:
            raise TypeError("COORD must be initialized with two integers or floats, or a tuple of two integers or floats")

    # Magic methods
    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def __repr__(self):
        return f"COORD(x={self.x}, y={self.y})"

    def __eq__(self, other):
        if isinstance(other, COORD):
            return self.x == other.x and self.y == other.y
        elif isinstance(other, (int, float)):
            return self.x == other and self.y == other
        return False

    def __hash__(self):
        return hash((self.x, self.y))

    def __add__(self, other):
        if isinstance(other, COORD):
            return COORD(self.x + other.x, self.y + other.y)
        elif isinstance(other, (float, int)):
            return COORD(self.x + other, self.y + other)
        elif isinstance(other, (list, tuple)) and len(other) > 1:
            return COORD(self.x + other[0], self.y + other[1])
        raise TypeError("Operands must be of type 'COORD', 'int' or 'float'")

    def __sub__(self, other):
        if isinstance(other, COORD):
            return COORD(self.x - other.x, self.y - other.y)
        elif isinstance(other, (int, float)):
            return COORD(self.x - other, self.y - other)
        raise TypeError("Operands must be of type 'Coordinate', 'int' or 'float'")

    def __mul__(self, scalar):
        if isinstance(scalar, (int, float)):
            return COORD(self.x * scalar, self.y * scalar)
        raise TypeError("Operand must be an integer or float")

    def __truediv__(self, scalar):
        if isinstance(scalar, (int, float)) and scalar != 0:
            return COORD(self.x / scalar, self.y / scalar)
        raise ValueError("Operand must be a non-zero integer or float")
    
    def __lt__(self, other):
        """
        Compare this coordinate with another coordinate or a scalar value (non-standard behavior).

        This method checks if both the `x` and `y` components of this coordinate are strictly 
        less than the corresponding components of another `Coordinate` or a single scalar value.

        Parameters:
            other (Coordinate, int, float): The object to compare against.

        Returns:
            bool: 
                - `True` if both `x` and `y` are less than the corresponding values of `other`.
                - `False` otherwise.

        Raises:
            TypeError: If `other` is not of type `Coordinate`, `int`, or `float`.

        Note:
            - Unlike typical comparisons, this checks both components simultaneously. 
            - For scalar values, the comparison assumes both `x` and `y` should be compared 
            independently against the scalar.

        Example:
            coord1 = Coordinate(2, 3)
            coord2 = Coordinate(4, 5)

            print(coord1 < coord2)  # True
            print(coord1 < 3)       # True (2 < 3 and 3 < 3 are checked)
        """
        if isinstance(other, COORD):
            return self.x < other.x or self.y < other.y
        elif isinstance(other, (int, float)):
            return self.x < other or self.y < other
        raise TypeError("Operands must be of type 'Coordinate', 'int' or 'float'")
    
    def __gt__(self, other):
        """
        Compare this coordinate with another coordinate or a scalar value (non-standard behavior).

        This method checks if either the `x` or `y` component of this coordinate is strictly 
        greater than the corresponding components of another `COORD` or a single scalar value.

        Parameters:
            other (COORD, int, float): The object to compare against.

        Returns:
            bool: 
                - `True` if at least one of `x` or `y` is greater than the corresponding values of `other`.
                - `False` otherwise.

        Raises:
            TypeError: If `other` is not of type `COORD`, `int`, or `float`.

        Note:
            - Unlike typical comparisons, this checks if **at least one** component satisfies the condition.
            - For scalar values, both `x` and `y` are compared independently against the scalar.

        Example:
            coord1 = COORD(2, 3)
            coord2 = COORD(4, 5)

            print(coord1 > coord2)  # False
            print(coord1 > 3)       # True (3 > 3 is checked)
        """
        if isinstance(other, COORD):
            return self.x >= other.x or self.y >= other.y
        elif isinstance(other, (int, float)):
            return self.x > other or self.y > other
        raise TypeError("Operands must be of type 'COORD', 'int' or 'float'")

    def __le__(self, other):
        """
        Compare this coordinate with another coordinate or a scalar value (non-standard behavior).

        This method checks if both the `x` and `y` components of this coordinate are less than 
        or equal to the corresponding components of another `COORD` or a single scalar value.

        Parameters:
            other (COORD, int, float): The object to compare against.

        Returns:
            bool: 
                - `True` if both `x` and `y` are less than or equal to the corresponding values of `other`.
                - `False` otherwise.

        Raises:
            TypeError: If `other` is not of type `COORD`, `int`, or `float`.

        Note:
            - This comparison requires **both** components to satisfy the condition.
            - For scalar values, the comparison assumes both `x` and `y` should be compared 
            independently against the scalar.

        Example:
            coord1 = COORD(2, 3)
            coord2 = COORD(2, 5)

            print(coord1 <= coord2)  # True
            print(coord1 <= 3)       # True (2 <= 3 and 3 <= 3 are checked)
        """
        if isinstance(other, COORD):
            return self.x <= other.x or self.y <= other.y
        elif isinstance(other, (int, float)):
            return self.x <= other or self.y <= other
        raise TypeError("Operands must be of type 'Coordinate', 'int' or 'float'")

    def __ge__(self, other):
        """
        Compare this coordinate with another coordinate or a scalar value (non-standard behavior).

        This method checks if either the `x` or `y` components of this coordinate are greater or 
        equal to the corresponding components of another `COORD` or a single scalar value.

        Parameters:
            other (COORD, int, float): The object to compare against.

        Returns:
            bool: 
                - `True` if at least one of `x` or `y` is greater than or equal to the corresponding values of `other`.
                - `False` otherwise.

        Raises:
            TypeError: If `other` is not of type `COORD`, `int`, or `float`.

        Note:
            - Unlike typical comparisons, this checks if **at least one** component satisfies the condition.
            - For scalar values, the comparison assumes both `x` and `y` should be compared 
            independently against the scalar.

        Example:
            coord1 = COORD(2, 3)
            coord2 = COORD(4, 5)

            print(coord1 >= coord2)  # False
            print(coord1 >= 3)       # True (3 >= 3 is checked)
        """
        if isinstance(other, COORD):
            return self.x >= other.x or self.y >= other.y
        elif isinstance(other, (int, float)):
            return self.x >= other or self.y >= other
        raise TypeError("Operands must be of type 'COORD', 'int' or 'float'")

    # Other methods
    def magnitude(self):
        return (self.x**2 + self.y**2)**0.5

    # Dot product
    def dot(self, other):
        if isinstance(other, COORD):
            return self.x * other.x + self.y * other.y
        raise TypeError("Operands must be of type 'Coordinate'")

    # In bounds check
    def inside(self, min_bound, max_bound=None) -> bool:
        """
        Determines if the current coordinate is within the specified bounds.

        This method checks whether the current coordinate falls within the given
        bounds. The bounds can be specified in various formats, including:
        - A `Coord` object representing the (x, y) bounds.
        - A tuple or list of length 2 where the first value represents the x-bound
          and the second represents the y-bound.
        - A single numeric value (int or float), which is treated as (value, value)
          for both x and y.

        If only one bound (`min_bound`) is provided, it is treated as the maximum 
        bound, and the minimum bound defaults to (0, 0).

        **Inclusive-Exclusive Behavior**:
        The method uses inclusive comparison (`<=`) for the lower bound and
        exclusive comparison (`<`) for the upper bound. Specifically:
        - The x-coordinate must satisfy `min_bound[0] <= self.x < max_bound[0]`.
        - The y-coordinate must satisfy `min_bound[1] <= self.y < max_bound[1]`.

        Parameters:
        ----------
        min_bound : Coord, tuple, list, or numeric
            The minimum bound for the coordinate. If `max_bound` is not provided,
            this is treated as the maximum bound, and the minimum defaults to (0, 0).
        
        max_bound : Coord, tuple, list, or numeric, optional
            The maximum bound for the coordinate. If not provided, defaults to `min_bound`.

        Returns:
        -------
        bool
            `True` if the current coordinate is within the specified bounds,
            `False` otherwise.

        Raises:
        ------
        ValueError
            If `min_bound` or `max_bound` is not a valid input format.

        Examples:
        --------
        # Assuming `self.x = 5` and `self.y = 10`
        coord.inside((4, 9), (6, 11))  # True
        coord.inside((5, 10))          # True (default min_bound is (0, 0))
        coord.inside(5, 6)             # False (y=10 is out of range)
        """
        # Helper function to validate bounds
        def validate_bound(bound, name):
            if isinstance(bound, COORD):
                return (bound.x, bound.y)
            elif isinstance(bound, (tuple, list)) and len(bound) == 2:
                return tuple(bound)
            elif isinstance(bound, (int, float)):
                return (bound, bound)
            else:
                raise ValueError(
                    f"Invalid {name} bound: {bound}. Must be a Coord, "
                    "a tuple/list of length 2, or a single number (int/float). "
                    "Bounds should represent (x, y) where the first value is for x and the second for y."
                )
        # Check if bath bounds been passed
        if max_bound == None:
            max_bound = min_bound
            min_bound = 0

        # Validate and unpack bounds
        min_bound = validate_bound(min_bound, "minimum")
        max_bound = validate_bound(max_bound, "maximum")

        # Check if the current coordinate is within the bounds
        return (
            min_bound[0] <= self.x < max_bound[0] and
            min_bound[1] <= self.y < max_bound[1]
        )

