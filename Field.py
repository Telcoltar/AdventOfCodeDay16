class Field:

    def __init__(self, identifier: str, first_range: str, second_range: str):
        self.identifier = identifier
        first_range_first_number: str
        first_range_second_number: str
        second_range_first_number: str
        second_range_second_number: str
        first_range_first_number, first_range_second_number = first_range.split("-")
        second_range_first_number, second_range_second_number = second_range.split("-")
        self.first_range = (int(first_range_first_number.strip()), int(first_range_second_number.strip()))
        self.second_range = (int(second_range_first_number.strip()), int(second_range_second_number.strip()))

    def is_number_valid(self, number: int):
        return ((self.first_range[0] <= number <= self.first_range[1]) or
                (self.second_range[0] <= number <= self.second_range[1]))

    def __str__(self):
        return f"{self.identifier}, {self.first_range}, {self.second_range}"

    def __repr__(self):
        return f"{self.identifier}, {self.first_range}, {self.second_range}"