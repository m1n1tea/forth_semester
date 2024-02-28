#БПМ-22-4:
#Макуров Михаил
#Воеводин Егор
#Нейман Алексей


from fractions import Fraction
import math

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
    cnt_dgt = 0
    if integer_part!=0:
        cnt_dgt=math.floor(math.log(integer_part,number_system))
        if (cnt_dgt>=9):
            denom*=number_system**cnt_dgt
            integer_part = num // denom
    num-=integer_part*denom

    while (len(res)<max_len and integer_part!=0):
        m=integer_part%number_system
        res+=digit_to_char(m)
        integer_part //= number_system
    if is_negative:
        res+='-'
    res=res[::-1]
    if (len(res)==0):
        res+='0'
    if (len(res)+1<max_len and num!=0):
        res+='.'
    while (len(res)<max_len and num!=0):
        num*=number_system
        d=num//denom
        num-=d*denom
        res+=digit_to_char(d)
    if cnt_dgt<9:
        return res
    else:
        return res + "e" + str(cnt_dgt)

def num_to_time(num : int)-> str:
    if (num==0):
        return "__:__:__"
    else:
        hours=str(num//3600)
        if len(hours)==1:
            hours="0"+hours
        minutes=str(num//60%60)
        if len(minutes)==1:
            minutes="0"+minutes
        seconds=str(num%60)
        if len(seconds)==1:
            seconds="0"+seconds
        return hours + ":" + minutes + ":" + seconds


class CalculatorLogic:
    def __init__(self):
        self.main_fraction = Fraction()
        self.secondary_fraction = Fraction()
        self.operator_symbol = 'c' # +,-,*,/,= - easy, c - clear all(except number system)
        self.input_fraction = "main"  # main - main_fraction, secondary - secondary_fraction
        self.number_system = 10
        self.max_number_len = 100
        self.is_time=0

    def input_number_system(self, number_system):
        self.number_system=int(number_system)

    def switch_time(self):
        if self.is_time==1:
            self.is_time=0
            return
        self.is_time=1
        num=0
        denom=1
        if self.input_fraction == "main":
            (num, denom) = self.main_fraction.as_integer_ratio()
        if self.input_fraction == "secondary":
            (num, denom) = self.secondary_fraction.as_integer_ratio()
        num//=denom
        denom=1
        if num >= 24 * 3600:
            num = 24 * 3600 - 1
        if self.input_fraction == "main":
            self.main_fraction = Fraction(num, denom)
        if self.input_fraction == "secondary":
            self.secondary_fraction = Fraction(num, denom)


    def input_number(self, number : str):
        print(number)
        dot_index=number.find('.')
        num=0
        denom=1
        self.is_time = 0
        if number=='':
            pass
        elif number.find(':')!=-1:
            self.is_time=1
            time=number.split(":")
            for i in range(0,3):
                time[i]=time[i].strip("_")
                if time[i]=="":
                    time[i]=0
                else:
                    time[i]=int(time[i])
            num=time[0]*3600+time[1]*60+time[2]
            if num>=24*3600:
                num=24*3600-1
        elif (dot_index==-1):
            num=int(number,self.number_system)
        elif number[-1]=='.':
            num = int(number[:-1], self.number_system)
        else:
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

        if operator_symbol in ['+','-','*','/']:
            self.input_fraction="secondary"
        if operator_symbol in ['C','=']:
            self.input_fraction="main"

        if operator_symbol == 'C':
            self.main_fraction = Fraction()
            self.secondary_fraction = Fraction()
            return

        if self.operator_symbol=='+':
            self.main_fraction+=self.secondary_fraction
        if self.operator_symbol=='-':
            self.main_fraction=abs(self.main_fraction-self.secondary_fraction)
        if self.operator_symbol=='*':
            self.main_fraction*=self.secondary_fraction
        if self.operator_symbol=='/' and self.secondary_fraction!=0:
                self.main_fraction/=self.secondary_fraction
        if self.is_time==1:
            self.main_fraction=math.floor(self.main_fraction)
        if operator_symbol=="=" and self.is_time==1 and self.main_fraction>24*3600:
            self.main_fraction %=24 * 3600

        self.operator_symbol = operator_symbol


    def get_main_fraction(self) -> str :
        if self.is_time==1:
            return num_to_time(math.floor(self.main_fraction))
        return frac_to_str(self.main_fraction,self.number_system,self.max_number_len)
    def get_secondary_fraction(self) -> str :
        if self.is_time==1:
            return num_to_time(math.floor(self.secondary_fraction))
        return frac_to_str(self.secondary_fraction,self.number_system,self.max_number_len)
    def get_input_fraction(self) -> str :
        if self.input_fraction == "main":
            if self.is_time == 1:
                return num_to_time(math.floor(self.main_fraction))
            return frac_to_str(self.main_fraction,self.number_system,self.max_number_len)
        else:
            if self.is_time == 1:
                return num_to_time(math.floor(self.secondary_fraction))
            return frac_to_str(self.secondary_fraction, self.number_system, self.max_number_len)
