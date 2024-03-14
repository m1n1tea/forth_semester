

#include <cstdint>
#include <stdexcept>
#include<iostream>
#include<vector>






template<typename type>
class Tree {
public:
    Tree();
    explicit Tree(ptrdiff_t size);
    Tree(ptrdiff_t size, const type& common, int children_amount_=2);
    Tree(const Tree& rhs) = default;
    Tree& operator=(const Tree& rhs) = default;//копирующий оператор присваивания
    ~Tree() = default;
    std::ptrdiff_t size() const noexcept;//узнать размер массива

    type* getRoot() noexcept {return &tree_val_[0];}
    type* getNode(ptrdiff_t index) {indexCheck(index); return &tree_val_[index]; }
    type* getChild(type* node, int child_num);
    type* getParent(type* node);

    type* addChild(type* node, int child_num);
    type& operator[](ptrdiff_t index){ indexCheck(index); return tree_val_[index]; }
    const type& operator[](ptrdiff_t index) const { indexCheck(index); return tree_val_[index]; };
private:
    ptrdiff_t size_;
    std::vector<type> tree_val_;
    int children_amount_;
    void nodeCheck(const std::ptrdiff_t& index) const;
    void indexCheck(const std::ptrdiff_t& index) const;
};

template<typename type>
void Tree<type>::nodeCheck(const std::ptrdiff_t& index) const {
    if (index < 0 || index >= size_) {
        throw std::out_of_range("Node is out of range of tree");
    }
}

template<typename type>
void Tree<type>::indexCheck(const std::ptrdiff_t& index) const {
    if (index < 0 || index >= size_) {
        throw std::out_of_range("Index is out of range of tree");
    }
}

void sizeCheck(const std::ptrdiff_t& size) {
    if (size < 0) {
        throw std::invalid_argument("Tree size is not positive");
    }
}


template<typename type>
Tree<type>::Tree():size_(1), tree_val_(1), children_amount_(2){}

template<typename type>
Tree<type>::Tree(ptrdiff_t size): size_(size), tree_val_(size), children_amount_(2) {}


template<typename type>
Tree<type>::Tree(ptrdiff_t size, const type& common,int childrea_amount) : size_(size), tree_val_(size, common), children_amount_(childrea_amount) {}


template<typename type>
std::ptrdiff_t Tree<type>::size() const noexcept
{
    return size_;
}



template<typename type>
type* Tree<type>::getChild(type* node, int child_num) {
    ptrdiff_t index = node - &tree_val_[0];
    nodeCheck(index);
    index = children_amount_ * index + child_num;
    if (index < size_) {
        return &tree_val_[index];
    }
    else {
        return nullptr;
    }
}

template<typename type>
type* Tree<type>::addChild(type* node, int child_num)
{
    ptrdiff_t index = node - &tree_val_[0];
    nodeCheck(index);
    index = index * children_amount_ + child_num;

    if (index < size_) {
        return &tree_val_[index];
    }
    else {
        tree_val_.resize(index+1);
        size_= index + 1;
        return &tree_val_[index];
    }
}


template<typename type>
type* Tree<type>::getParent(type* node) {
    ptrdiff_t index = node - &tree_val_[0];
    nodeCheck(index);
    index = (index - 1) / children_amount_;
    return &tree_val_[0] + index;
}






int main() {
    Tree<int> test;
    auto node=test.getRoot();
    for (int t = 0; t < 15; ++t) {
        node=test.addChild(node, 1);
        std::cout << test.size() << "\n";
    }
    std::cin >> *node;
    
}
