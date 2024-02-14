import fractions

class CalculatorLogic:
    def __init__(self):
        self.main_fraction = Fraction()
        self.secondary_fraction = Fraction()
        self.operator_symbol = '+'
        self.input_fraction = "main"  # main - main_fraction, secondary - secondary_fraction
        self.number_system = 10
        self.max_number_len = 100

    def input_number_system(self, number_system: str):
        pass
    def input_number(self, number : str):
        pass
    def input_operator(self, operator_symbol : str):
        pass
    def get_main_fraction(self) -> str :
        pass
    def get_secondary_fraction(self) -> str :
        pass
