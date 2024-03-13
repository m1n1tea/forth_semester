

#include <cstdint>
#include <stdexcept>
#include<iostream>


template<typename T>
inline void sizeCheck(const std::ptrdiff_t& size);




template<typename type>
class ArrayT {
public:
    ArrayT();
    ArrayT(const ArrayT& rhs) noexcept;//копирующий конструктор
    ArrayT(ArrayT&& rhs) noexcept;//перемещающий конструктор
    explicit ArrayT(const std::ptrdiff_t& size);//массив с предопределённым размером
    ArrayT(const std::ptrdiff_t& size, const type& common);//массив с предопределённым размером и общим элементом
    ~ArrayT() noexcept;
    ArrayT& operator=(const ArrayT& rhs) noexcept;//копирующий оператор присваивания
    ArrayT& operator=(ArrayT&& rhs) noexcept;//перемещающий оператор присваивания
    type& operator[](const std::ptrdiff_t& index);//изменение элемента массива
    const type& operator[](const std::ptrdiff_t& index) const;//изменение элемента массива
    std::ptrdiff_t size() const noexcept;//узнать размер массива



    void resize(const std::ptrdiff_t& new_size);//изменить размер массива, новые элементы являются значениями по умолчанию класса
    void resize(const std::ptrdiff_t& new_size, const type& common);//изменить размер массива с заданным значением для новых элементов
    void insert(const std::ptrdiff_t& index, const type& common);// вставить данный элемент на данную позицию массива
    void remove(const std::ptrdiff_t& index);// удалить элемент с данной позицией из массива
    bool empty();//если массив пустой возвращает true, иначе false



private:
    void indexCheck(const std::ptrdiff_t& index) const;
    type* arr_ = nullptr;
    std::ptrdiff_t array_size_ = 0;
    inline static const type common_element = type();
};

void sizeCheck(const std::ptrdiff_t& size) {
    if (size < 0) {
        throw std::invalid_argument("Array size or change in size is negative");
    }
}

template<typename type>
void ArrayT<type>::indexCheck(const std::ptrdiff_t& index) const {
    if (index < 0 || index >= array_size_) {
        throw std::out_of_range("Index is out of range of array");
    }
}

template<typename type>
ArrayT<type>::ArrayT():array_size_(0),arr_(nullptr){}

template<typename type>
ArrayT<type>::ArrayT(const std::ptrdiff_t& size) :array_size_(size), arr_(nullptr) {
    sizeCheck(size);
    if (array_size_ > 0) {// Если массив пустой, то не выделяем память
        arr_ = new type[array_size_];
        for (std::ptrdiff_t i = 0; i < array_size_; ++i) {
            arr_[i] = common_element;
        }
    }
}

template<typename type>
ArrayT<type>::ArrayT(const std::ptrdiff_t& size, const type& common) :array_size_(size), arr_(nullptr) {
    sizeCheck(size);
    if (array_size_ > 0) {// Если массив пустой, то не выделяем память
        arr_ = new type[array_size_];
        for (std::ptrdiff_t i = 0; i < array_size_; ++i) {
            arr_[i] = common;
        }
    }

}




template<typename type>
ArrayT<type>::ArrayT(const ArrayT<type>& rhs)noexcept :array_size_(rhs.array_size_){
    if (array_size_ > 0) {// Если массив пустой, то не выделяем память
        arr_ = new type[array_size_];
        for (std::ptrdiff_t i = 0; i < array_size_; ++i) {
            arr_[i] = rhs.arr_[i];
        }
    }
}

template<typename type>
ArrayT<type>::ArrayT(ArrayT<type>&& rhs)noexcept :array_size_(rhs.array_size_), arr_(rhs.arr_) {
    rhs.arr_ = nullptr;//делаем "использованный" массив пустым
    rhs.array_size_=0;
}



template<typename type>
ArrayT<type>::~ArrayT() noexcept {
    delete[] arr_;//деконструируем элементы массива, затем освобождаем память
    arr_ = nullptr;
};


template<typename type>
ArrayT<type>& ArrayT<type>::operator=(const ArrayT& rhs) noexcept
{
    if (arr_ == rhs.arr_)
        return *this;
    ArrayT tmp(rhs);//создаём копию rhs, чтобы затем поменять её местами с текущим массивом, эффективное повторное использование кода
    swap(*this, tmp);
    return *this;//в конце функции вызовется деструктор для tmp и все неиспользуемые элементы очистятся
}

template<typename type>
ArrayT<type>& ArrayT<type>::operator=(ArrayT&& rhs) noexcept
{
    if (arr_ == rhs.arr_)
        return *this;
    delete[] arr_;//очищаем текущий массив
    arr_ = rhs.arr_;
    array_size_ = rhs.array_size_;
    rhs.arr_ = nullptr;//делаем "использованный" массив пустым
    rhs.array_size_=0;
    return *this;
}


template<typename type>
type& ArrayT<type>::operator[](const std::ptrdiff_t& index)
{
    indexCheck(index);
    return arr_[index];
}

template<typename type>
const type& ArrayT<type>::operator[](const std::ptrdiff_t& index) const
{
    indexCheck(index);
    return arr_[index];
}


template<typename type>
std::ptrdiff_t ArrayT<type>::size() const noexcept
{
    return array_size_;
}



template<typename type>
void ArrayT<type>::resize(const std::ptrdiff_t& new_size, const type& common)
{
    if (new_size == 0) {// делаем массив пустым
        delete[] arr_;
        arr_=nullptr;
        array_size_=0;
        return;
    }
    sizeCheck(new_size);
    type* new_data;
    if (new_size == array_size_)//ничего не делаем
        return;
    if (new_size > array_size_) {
        new_data= new type[new_size];
        for (ptrdiff_t i = 0; i < array_size_; ++i) {
            new_data[i]=std::move(arr_[i]);
        }
        for (ptrdiff_t i = array_size_; i < new_size; ++i) { // заполняем новые элементы дефолтными значениями
            new_data[i] = common;
        }
    }
    else {
        new_data = new type[new_size];
        for (ptrdiff_t i = 0; i < new_size; ++i) {
            new_data[i] =std::move(arr_[i]);
        }
    }
    delete[] arr_;
    arr_=new_data;
    array_size_=new_size;
}

template<typename type>
void ArrayT<type>::resize(const std::ptrdiff_t& new_size) {
    resize(new_size, common_element);
}








template<typename type>
void ArrayT<type>::insert(const std::ptrdiff_t& index, const type& common) {
    ++array_size_;
    indexCheck(index);// делаем проверку корректности индекса внутри "будущего" массива в котором array_size_+1 элементов
    --array_size_;
    type* newArray = new type[array_size_+1];
    newArray[index] = common;
    for (std::ptrdiff_t i = 0; i < index; ++i) {
        newArray[i] = std::move(arr_[i]);//поскольку мы не создаём новый массив, копирование излишне
    }
    for (std::ptrdiff_t i = index + 1; i < array_size_ + 1; ++i) {
            newArray[i] = std::move(arr_[i - 1]);
    }
    delete[] arr_;
    arr_ = newArray;
    ++array_size_;

}


template<typename type>
void ArrayT<type>::remove(const std::ptrdiff_t& index) {
    sizeCheck(array_size_ - 1);// не удаляем элементы в пустом массиве
    indexCheck(index);
    if (array_size_ == 1) {
        delete[] arr_;
        array_size_=0;
        return;
    }

    type* newArray = new type[array_size_ - 1];
    for (std::ptrdiff_t i = 0; i < index; ++i) {
        newArray[i] = std::move(arr_[i]);
    }
    for (std::ptrdiff_t i = index; i < array_size_ - 1; ++i) {
        newArray[i] = std::move(arr_[i + 1]);
    }
    delete[] arr_;
    arr_ = newArray;
    --array_size_;
}

template<typename type>
bool ArrayT<type>::empty()
{
    return array_size_ != 0;
}

void printArray(const ArrayT<std::string>& arr) {
    std::cout << "Size: " << arr.size() << " Array:";
    for (int i = 0; i < arr.size(); ++i) {
        std::cout << " " << arr[i] ;
    }
    std::cout << "\n";
}

void printAllArrays(const ArrayT<ArrayT<std::string>>& arrs) {
    std::cout << "Arrays count: " << arrs.size() << " Arrays:\n";
    for (int i = 0; i < arrs.size(); ++i) {
        std::cout << i << ". ";
        printArray(arrs[i]);
    }
    std::cout << "\n";
}

/*
*/

int main() {
    ArrayT<ArrayT<std::string>> arrays(1);
    arrays[0].resize(3);
    arrays[0][0] = "1";
    arrays[0][1] = "2";
    arrays[0][2] = "3rd_element";
    std::cout << "Starting array of strings:\n";
    printArray(arrays[0]);
	std::cout << "Write number from 1 to 12\n";
	std::cout << "1. Print active array\n";
	std::cout << "2. Print all arrays\n";
	std::cout << "3. Change element's value\n";
	std::cout << "4. Insert element\n";
	std::cout << "5. Remove element\n";
	std::cout << "6. Resize array\n";
	std::cout << "7. Create new array\n";
	std::cout << "8. Switch active array\n";
	std::cout << "9. Copy one array to another\n";
	std::cout << "10. Move one array to another\n";
	std::cout << "11. Duplicate active array\n";
	std::cout << "12. Finish program\n";
    int active_array_index = 0;
    bool stop = 0;
    //Все новые массивы добавляются к концу двумерного массива.
    while (!stop) {

        int command_type = 0;
        std::cin >> command_type;
        bool bad_number = 0;
        int f_index = -1;
        int s_index = -1;
        std::string s = "empty";
        try {
            switch (command_type)
            {
            case 1:
                printArray(arrays[active_array_index]);
                break;
            case 2:
                printAllArrays(arrays);
                break;
            case 3:
                std::cout << "Input index and new string value: ";
                std::cin >> f_index >> s;
                arrays[active_array_index][f_index]=s;
                break;
            case 4:
                std::cout << "Input index and string: ";
                std::cin >> f_index >> s;
                arrays[active_array_index].insert(f_index,s);
                break;
            case 5:
                std::cout << "Input index: ";
                std::cin >> f_index;
                arrays[active_array_index].remove(f_index);
                break;
            case 6:
                std::cout << "Input new size and default string: ";
                std::cin >> f_index >> s;
                arrays[active_array_index].resize(f_index,s);
                break;
            case 7:
                std::cout << "Input array's size and default string: ";
                std::cin >> f_index >> s;
                arrays.insert(arrays.size(),ArrayT<std::string>(f_index,s));
                break;
            case 8:
                std::cout << "Input index of next active array: ";
                std::cin >> f_index;
                arrays[f_index];
                active_array_index=f_index;
                break;
            case 9:
                std::cout << "Input source and destination indexes: ";
                std::cin >> f_index >> s_index;
                arrays[s_index]=arrays[f_index];
                break;
            case 10:
                std::cout << "Input source and destination indexes: ";
                std::cin >> f_index >> s_index;
                arrays[s_index] = std::move(arrays[f_index]);
                break;
            case 11:
                arrays.insert(arrays.size(), arrays[active_array_index]);
                std::cout << "Duplicated to the end of an array\n";
                break;
            case 12:
                std::cout << "Program is finished";
                stop=1;
                break;

            default:
                bad_number = 1;
                break;
            }
        }
        catch(const std::exception& e){
            std::cout << "Exception: " << e.what() << "\n";
        }
        if (bad_number) {
            std::cout << "Bad input\n";
            continue;
        }



    }
}
