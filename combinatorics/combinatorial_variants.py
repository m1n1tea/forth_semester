import math


#helper functions
def check_value(n, n_name):
    if not n >= 0:
        raise ValueError(n_name + " must be >= 0")
    if math.floor(n) != n:
        raise ValueError(n_name + " must be exact integer")
    if n+1 == n:  # catch a value like 1e300
        raise OverflowError(n_name + " too large")
def factorial(n):

    result = 1
    factor = 2
    while factor <= n:
        result *= factor
        factor += 1
    return result
def factorial_division(n,m): # if m>=n returns 1
    result = 1
    factor = m+1
    while factor <= n:
        result *= factor
        factor += 1
    return result



#main functions
def sum_rule(n ,m):
    check_value(n,"n")
    check_value(m,"m")
    return n+m;
def prod_rule(n ,m):
    check_value(n,"n")
    check_value(m,"m")
    return n*m;
def placement_w_rep(n,m):
    check_value(n,"n")
    check_value(m,"m")
    return n**m;
def placement_wo_rep(n,m):
    check_value(n,"n")
    check_value(m,"m")
    if m>n:
        return 0
    return factorial_division(n,n-m);

def combinations_w_rep(n,m):
    check_value(n,"n")
    check_value(m,"m")
    return combinations_wo_rep(n+m-1,m)
def combinations_wo_rep(n,m):
    check_value(n,"n")
    check_value(m,"m")
    if m>n:
        return 0
    if n-m>m:
        m=n-m
    return factorial_division(n,m)//factorial(n-m)

def permutations_w_rep(arr_n): #arr_n - array of integers
    for i in range(len(arr_n)):
        check_value(arr_n[i], "n"+str(i+1))
    sum_n=0
    for x in arr_n:
        sum_n+=x
    max_n=max(arr_n)
    result = factorial_division(sum_n, max_n)
    for x in arr_n:
        if x==max_n:
            max_n=-1
            continue
        result//=factorial(x)
    return result

def permutations_wo_rep(n):
    check_value(n, "n")
    return factorial(n);

#tests
print(prod_rule(placement_w_rep(9,1),placement_w_rep(10,4)))# кол-во 5-значных чисел
print(placement_wo_rep(17,3))# кол-во распределений 1-ого,2-ого,3-ого места на 17 команд
print(combinations_w_rep(3,63)) #кол-во способов распределить 63 яблока на 3 людей
print(prod_rule(combinations_wo_rep(3,2),combinations_wo_rep(4,2)))# кол-во прямоугольников на поле 2*3
print(permutations_w_rep([2,2,1,1])) #кол-во перестановок из букв слова «Уссури»
print(permutations_wo_rep(8))# кол-во расстановок 8 ладей на доске