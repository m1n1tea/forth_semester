import math
import unittest
import enum


#helper functions
def check_value(n : int, n_name : str):
    if not n >= 0:
        return (n_name + " must be >= 0")
    if math.floor(n) != n:
        return (n_name + " must be exact integer")
    if n+1 == n:  # catch a value like 1e300
        return (n_name + " is too large")
    return ""


def factorial(n : int) -> int: 
    result : int = 1
    factor : int = 2
    while factor <= n:
        result *= factor
        factor += 1
    return result


def factorial_division(n :int, m : int) -> int: # if m>=n returns 1
    result : int = 1
    factor : int = m+1
    while factor <= n:
        result *= factor
        factor += 1
    return result


#main functions
def sum_rule(n  : int,m : int) -> int:

    if check_value(n,"n")!="":
        return check_value(n,"n")
    if check_value(m, "m") != "":
        return check_value(m, "m")
    return n+m;

def prod_rule(n : int, m : int) -> int:
    if check_value(n,"n")!="":
        return check_value(n,"n")
    if check_value(m, "m") != "":
        return check_value(m, "m")
    return n*m;

def placement_w_rep(n : int, m : int) -> int:
    if check_value(n,"n")!="":
        return check_value(n,"n")
    if check_value(m, "m") != "":
        return check_value(m, "m")
    return n**m;

def placement_wo_rep(n : int,m : int) -> int:
    if check_value(n,"n")!="":
        return check_value(n,"n")
    if check_value(m, "m") != "":
        return check_value(m, "m")
    if m>n:
        return 0
    return factorial_division(n,n-m);

def combinations_w_rep(n : int,m : int) -> int:
    if check_value(n,"n")!="":
        return check_value(n,"n")
    if check_value(m, "m") != "":
        return check_value(m, "m")
    return combinations_wo_rep(n+m-1,m)

def combinations_wo_rep(n : int,m : int) -> int:
    if check_value(n,"n")!="":
        return check_value(n,"n")
    if check_value(m, "m") != "":
        return check_value(m, "m")
    if m>n:
        return 0
    if n-m>m:
        m=n-m
    return factorial_division(n,m)//factorial(n-m)

def permutations_w_rep(arr_n : list[int]) -> int:
    for i in range(len(arr_n)):
        if check_value(arr_n[i], "n"+str(i+1)) != "":
            return check_value(arr_n[i], "n"+str(i+1))
    sum_n : int=0
    for x in arr_n:
        sum_n+=x
    max_n : int =max(arr_n)
    result = factorial_division(sum_n, max_n)
    for x in arr_n:
        if x==max_n:
            max_n=-1
            continue
        result//=factorial(x)
    return result

def permutations_wo_rep(n : int) -> int:
    if check_value(n, "n") != "":
        return check_value(n, "n")
    return factorial(n);

#tests
print(prod_rule(placement_w_rep(9,1),placement_w_rep(10,4)))# кол-во 5-значных чисел
print(placement_wo_rep(17,3))# кол-во распределений 1-ого,2-ого,3-ого места на 17 команд
print(combinations_w_rep(3,63)) #кол-во способов распределить 63 яблока на 3 людей
print(prod_rule(combinations_wo_rep(3,2),combinations_wo_rep(4,2)))# кол-во прямоугольников на поле 2*3
print(permutations_w_rep([2,2,1,1])) #кол-во перестановок из букв слова «Уссури»
print(permutations_wo_rep(8))# кол-во расстановок 8 ладей на доске

class CombTests (unittest.TestCase):
    def test_placementWithoutRep(self):
        self.assertEqual(placement_wo_rep(17, 3), 4080)
    def test_CombinationsWithRep(self): 
        self.assertEqual(combinations_w_rep(3, 63), 2080)


class Options(enum.Enum):
    SUM_RULE = 1
    PRODUCT_RULE = 2
    PLACEMENT_WITH_REPETITION = 3
    PLACEMENT_WITHOUT_REPETITION = 4
    COMBINATIONS_WITH_REPETITION = 5
    COMBINATIONS_WITHOUT_REPETITION = 6
    PERMUTATIONS_WITH_REPETITION = 7
    PERMUTATIONS_WITHOUT_REPETITION = 8
    QUIT = 9


def printOptions() -> None:
    border_length : int = 40
    print("-" * border_length)
    print(f"Для вывода правила суммы введите: {Options.SUM_RULE.value}")
    print(f"Для вывода правила произведений введите: {Options.PRODUCT_RULE.value}")
    print(f"Для вывода размещений с повторениями введите: {Options.PLACEMENT_WITH_REPETITION.value}")
    print(f"Для вывода размещений без повторений введите: {Options.PLACEMENT_WITHOUT_REPETITION.value}")
    print(f"Для вывода сочетаний с повторениями введите: {Options.COMBINATIONS_WITH_REPETITION.value}")
    print(f"Для вывода сочетаний без повторений введите: {Options.COMBINATIONS_WITHOUT_REPETITION.value}")    
    print(f"Для вывода перестановок с повторениями введите: {Options.PERMUTATIONS_WITH_REPETITION.value}")
    print(f"Для вывода перестановок без повторений введите: {Options.PERMUTATIONS_WITHOUT_REPETITION.value}")  
    print(f"Чтобы выйти введите: {Options.QUIT.value}")

def queryNArguments(number_of_arguments: int) -> list[int]:
    for i in range(number_of_arguments):
        print(f"Пожалуйста, ")

def queryUndefArguments() -> list[int]:
    print("Для завершения нажмите Enter 2 раза")
    query : list[int] = []
    while True:
        inp = input()
        if inp == '':
            break
        try: 
            query.append(int(inp))
        except Exception:
            print("Введите целое число!")
    return query

def query2Arguments() -> tuple[int, int]:
    print("Пожалуйста, введите n: ")
    while True:
        try:
            n: int = int(input())
            break
        except Exception:
            print("Введите целое число!")
    print("Пожалуйста, введите m: ")
    while True:
        try:
            m: int = int(input())
            break 
        except Exception:
            print("Введите целое число!")
    return (n, m)

def query1Argument() -> int:
    print("Пожалуйста, введите n: ")
    while True:
        try:
            n: int = int(input())
            break
        except Exception:
            print("Введите целое число!")
    return n

if __name__ == "__main__":
    should_quit: bool = False
    while not should_quit:
        printOptions()
        try: 
            option : int = int(input())
        except Exception:
            print("Введите номер!")
            continue  


        match option:
            case Options.QUIT.value:
                should_quit = True
            case Options.PLACEMENT_WITH_REPETITION.value:
                n, m  = query2Arguments()
                print(f"m = {m} размещений с повторениями из n = {n} элементов = {placement_w_rep(n, m)}")
            case Options.PLACEMENT_WITHOUT_REPETITION.value: 
                n, m = query2Arguments()
                print(f"m = {m} размещений без повторений из n = {n} элементов = {placement_wo_rep(n, m)}")
            case Options.SUM_RULE.value:
                n, m = query2Arguments()
                print(f"{n} + {m} = {sum_rule(n, m)}")
            case Options.PRODUCT_RULE.value:
                n, m = query2Arguments()
                print(f"{n} * {m} = {prod_rule(n, m)}")
            case Options.COMBINATIONS_WITH_REPETITION.value:
                n, m = query2Arguments()
                print(f"m = {m} сочетаний с повторениями из n = {n} элементов = {combinations_w_rep(n, m)}")
            case Options.COMBINATIONS_WITHOUT_REPETITION.value:
                n, m = query2Arguments()
                print(f"m = {m} сочетаний без повторений из n = {n} элементов = {combinations_wo_rep(n, m)}")
            case Options.PERMUTATIONS_WITHOUT_REPETITION.value:
                n: int = query1Argument()
                print(f"n = {n} перестановок без повторений = {permutations_wo_rep(n)}")
            case Options.PERMUTATIONS_WITH_REPETITION.value:
                n_list: list[int] = queryUndefArguments()
                if (len(n_list) == 0):
                    print("Вы ничего не ввели!") 
                    continue
                print(f"{n_list} перестановок с повторениями = {permutations_w_rep(n_list)}")