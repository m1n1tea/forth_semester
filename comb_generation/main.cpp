#include <iostream>
#include<array>
#include<cstring>



template<ptrdiff_t N>
constexpr int set_next_index( int* first,int index){
    *(first+index)=index+1;
    return index==N-1 ? 0 : set_next_index<N>(first,index+1);
}

template<ptrdiff_t N>
constexpr std::array<int,N> make_full_set(){
    std::array<int,N> res{0};
    set_next_index<N>(&res[0], 0);
    return res;
}


template<ptrdiff_t N,ptrdiff_t K>
class Combination{
    static_assert(N>0, "set size is not negative");
    static_assert(K>0, "subset size is not negative");
    static_assert(N>=K, "subset size is not bigger than set size");
public:
    Combination();
    Combination(const Combination& lhs) = default;
    Combination& operator=(const Combination& lhs) = default;
    ~Combination() = default;

    void goNextComb() noexcept;
    void goPrevComb() noexcept;

    const std::array<int,K>& getArray(){return arr_;}

private:
    std::array<int,K> arr_;
    static constexpr std::array<int,N> full_set= make_full_set<N>();
};

template<ptrdiff_t N,ptrdiff_t K>
Combination<N,K>::Combination(){
    for(int i=0;i<K;++i){
        arr_[i]=i+1;
    }
}

template <ptrdiff_t N, ptrdiff_t K>
void Combination<N, K>::goNextComb() noexcept
{
    ptrdiff_t j=K-1;
    while (arr_[j]==N-K+j+1){
        --j;
    }
    if (j!=-1){
        ++arr_[j];
    }
    ++j;
    const int* set_ptr =&(full_set)[0];
    set_ptr+=arr_[j-1];
    std::memcpy(&arr_[j],set_ptr,K-j);
}

template <ptrdiff_t N, ptrdiff_t K>
void Combination<N, K>::goPrevComb() noexcept
{
    ptrdiff_t j=K-1;
    while (j!=0 && arr_[j]==arr_[j-1]+1){
        --j;
    }
    if (arr_[j]!=1){
        --arr_[j];
        ++j;
    }

    const int* set_ptr =&(full_set)[0];
    set_ptr+=N-K+j;
    std::memcpy(&arr_[j],set_ptr,K-j);
}


template<ptrdiff_t N>
void printArray(std::array<int,N> arr){
    for(int i=0; i<N;++i){
        std::cout << arr[i] << " ";
    }
}

template<ptrdiff_t N,ptrdiff_t K>
void printCombos(){
    Combination<N,K> combination;
    while(combination.getArray()[0]!=N-K+1){
        printArray<K>(combination.getArray());
        std::cout << "\n";
        combination.goNextComb();
    }
    printArray<K>(combination.getArray());
    
}

int main(){
    printCombos<6,3>();
}
