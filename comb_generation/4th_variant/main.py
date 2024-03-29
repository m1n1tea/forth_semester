# БПМ-22-4 Воеводин Егор
from typing import List, Any

def generate_subsets(set: List[Any]) -> List[List[Any]]:
    # Базовый случай: пустое множество
    if len(set) == 0:
        return [[]]

    # Рекурсивный случай: добавляем элемент в подмножества предыдущего множества
    subsets = generate_subsets(set[1:])
    new_subsets = [subset + [set[0]] for subset in subsets]

    # Возвращаем объединенные подмножества
    return subsets + new_subsets

# Пример использования
se : List[Any] = [] 
print("Введите размер: ")
should_stop : bool = False
while not should_stop:
    try: 
        n : int = int(input())
        should_stop = True
    except:
        print("Введите число!")
print("Введите элементы: ")
for i in range(0, n):
    should_stop = False
    while not should_stop:
        try:
            se.append(int(input()))
            should_stop = True
        except:
            print("Введите число!")
print("Полученные множества: ")    
print(generate_subsets(se))