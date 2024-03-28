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
set : List[Any] = [1, 2, 3]
print(generate_subsets(set))