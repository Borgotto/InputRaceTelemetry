from collections import deque
from typing import Any, Iterable, Tuple, List

class Value():
    """Class to store a value from the iRacing SDK and relative metadata for its rendering within the UI"""
    def __init__(self, name: str, color: str = 'white', range: Tuple[Any,Any] = (None,None), initial_value: Any = 0.0, type: Any = int, buffer_size: int = 1):
        self._name = name.strip()
        self._color = color.strip()
        self._range = (min(range), max(range)) if range[0] and range[1] else range
        self._type = type
        self._initial_value = self._clamp(initial_value)
        self._values = deque([self._initial_value] * buffer_size, maxlen=buffer_size)

    def _clamp(self, value):
        "Restrict a value to the range and type defined at initialization"
        if not isinstance(value, self.type):
            raise TypeError(f"Value {value} is not of type {self.type}")
        range = self.range
        if range[1] is not None:
            value = min(range[1], value)
        if range[0] is not None:
            value = max(range[0], value)
        return value

    @property
    def name(self) -> str:
        """Return the name of the attribute"""
        return self._name

    @property
    def color(self) -> str:
        """Return the color of the rendered graph lines"""
        return self._color

    @property
    def buffer_size(self) -> int:
        """Return the size of the buffer array"""
        return len(self.values)

    @buffer_size.setter
    def buffer_size(self, size: int) -> None:
        """Set the size of the buffer array"""
        self._values = deque([self._initial_value] * size, maxlen=size)

    @property
    def is_buffered(self) -> bool:
        """Check if the value has a buffer size greater than 1"""
        return self.buffer_size > 1

    @property
    def range(self) -> Tuple[Any,Any]:
        """Return the value range"""
        return self._range

    @property
    def type(self):
        """Return the data type of the value"""
        return self._type

    @property
    def values(self) -> List[Any]:
        """Return the buffer containing all the values"""
        return self._values

    @values.setter
    def values(self, value: Iterable[Any]) -> None:
        """Set n values in the buffer, extra values will be discarded"""
        for e in value:
            self.values.append(self._clamp(e))

    @property
    def value(self) -> Any:
        """Return the last value in the buffer"""
        return self.values[-1]

    @value.setter
    def value(self, value: Any) -> None:
        """Set the last value in the buffer"""
        self.values = [value]

    def update(self, value: Any) -> None:
        """Set the value in the buffer"""
        self.value = value