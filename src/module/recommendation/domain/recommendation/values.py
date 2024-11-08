class Score(float):

    def __new__(cls, value):

        if not isinstance(value, float):
            raise TypeError("value must be of type float")

        if not 0 <= value <= 1:
            raise ValueError("value must be between 0 and 1")

        return super().__new__(cls, value)
