from fractions import Fraction


def digit_to_char(digit):
    if digit < 10:
        return str(digit)
    return chr(ord('A') + digit - 10)


def frac_to_str( fraction : Fraction, number_system : int, max_len : int)->str:
    (num,denom)=fraction.as_integer_ratio()
    res=str()
    is_negative=0

    if  num < 0 :
        is_negative=1
        num*=-1

    integer_part = num//denom
    num-=integer_part*denom

    while (len(res)<max_len and integer_part!=0):
        m=integer_part%number_system
        res+=digit_to_char(m)
        integer_part //= number_system
    if is_negative:
        res+='-'
    res=res[::-1]

    if (len(res)+1<max_len and num!=0):
        res+='.'
    while (len(res)<max_len and num!=0):
        num*=number_system
        d=num//denom
        num-=d*denom
        res+=digit_to_char(d)

    return res


class CalculatorLogic:
    def __init__(self):
        self.main_fraction = Fraction()
        self.secondary_fraction = Fraction()
        self.operator_symbol = 'c' # +,-,*,/,= - easy, c - clear all(except number system)
        self.input_fraction = "main"  # main - main_fraction, secondary - secondary_fraction
        self.number_system = 10
        self.max_number_len = 100

    def input_number_system(self, number_system):
        self.number_system=int(number_system)

    def input_number(self, number : str):
        (integer_part,fractional_part)=number.split('.')
        denom = self.number_system**len(fractional_part)
        num = int(integer_part, self.number_system)*denom
        if number[0] != '-':
            num += int(fractional_part, self.number_system)
        else:
            num -= int(fractional_part, self.number_system)

        if self.input_fraction == "main":
            self.main_fraction = Fraction(num,denom)
        if self.input_fraction == "secondary":
            self.secondary_fraction = Fraction(num, denom)

    def input_operator(self, operator_symbol : str):

        if operator_symbol in ['+','-','*','/','=']:
            self.input_fraction="secondary"

        if operator_symbol == 'c':
            self.main_fraction = Fraction()
            self.secondary_fraction = Fraction()
            self.input_fraction = "main"

        if operator_symbol != '=':
            self.operator_symbol = operator_symbol
            return

        if self.operator_symbol=='+':
            self.main_fraction+=self.secondary_fraction
        if self.operator_symbol=='-':
            self.main_fraction=abs(self.main_fraction-self.secondary_fraction)
        if self.operator_symbol=='*':
            self.main_fraction*=self.secondary_fraction
        if self.operator_symbol=='/':
            self.main_fraction/=self.secondary_fraction


    def get_main_fraction(self) -> str :
        return frac_to_str(self.main_fraction,self.number_system,self.max_number_len)
    def get_secondary_fraction(self) -> str :
        return frac_to_str(self.secondary_fraction,self.number_system,self.max_number_len)
