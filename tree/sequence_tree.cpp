

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
    int getChildAmount() const noexcept;//узнать общее количество детей у вершин дерева

    type* getRoot() noexcept {return &tree_val_[0];}// возвращает указатель на нулевую вершину
    type* getNode(ptrdiff_t index) {indexCheck(index); return &tree_val_[index]; }// возвращает указатель на указанную вершину
    ptrdiff_t getIndex(const type* node) const { ptrdiff_t index = node - &tree_val_[0]; nodeCheck(index); return index; } // получить индекс вершины из указаетля
    const type* getRoot() const noexcept { return &tree_val_[0]; }
    const type* getNode(ptrdiff_t index) const { indexCheck(index); return &tree_val_[index]; }
    type* getChild( type* node, int child_num);// получить указатель на n-ого ребёнка, если ребёнок находится вне пределов массива, возвращает nullptr
    type* getParent( type* node);

    type* addChild(type* node, int child_num);//анналогичен getChild, но в случае если индеск ребёнка находится за пределами массива, то расширает массив, так чтобы его последним элементом был нужный ребёнок
    type& operator[](ptrdiff_t index){ indexCheck(index); return tree_val_[index]; }//доступ к значению элемента по индексу
    const type& operator[](ptrdiff_t index) const { indexCheck(index); return tree_val_[index]; };
private:
    ptrdiff_t size_;
    std::vector<type> tree_val_;
    int children_amount_;//такая реализация дерева позволяет иметь различное общее количество детей, однако в тестах будет работа только с двоичным деревьями
    void nodeCheck(const std::ptrdiff_t& index) const;
    void indexCheck(const std::ptrdiff_t& index) const;
    void childNumCheck(const std::ptrdiff_t& num) const;
    
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
template<typename type>
void Tree<type>::childNumCheck(const std::ptrdiff_t& num) const {
    if (num < 1 || num > children_amount_) {
        throw std::out_of_range("Children number is out of allowed range");
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
int Tree<type>::getChildAmount() const noexcept
{
    return children_amount_;
}



template<typename type>
type* Tree<type>::getChild(type* node, int child_num) {
    ptrdiff_t index = node - &tree_val_[0]; //индекс вершины
    nodeCheck(index); 
    index = children_amount_ * index + child_num; // индекс ребёнка
    if (index < size_) {
        return &tree_val_[index];
    }
    else {
        return nullptr;// у листа нет детей
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
    if (index==0)
        return nullptr; //у корня нет родителя
    nodeCheck(index);
    index = (index - 1) / children_amount_; // индекс родителя
    return &tree_val_[0] + index;
}


void printNode(Tree<int>& tree, int* node) {
    std::cout << "[" << tree.getIndex(node) << ":" << *node << "]";
}

void printNodeInfo(Tree<int>& tree, int* node) {
    std::cout << "Node: [" << tree.getIndex(node) << ": " << *node << "]\n ";
    int* parent = tree.getParent(node);
    if (parent!=nullptr)
        std::cout << "Parent: [" << tree.getIndex(tree.getParent(node)) << ": " << *tree.getParent(node) << "]\n ";
    std::cout << "Children: ";
    for (int i = 1; i <= tree.getChildAmount(); ++i) {
        bool stop=0;
        int* child = tree.getChild(node, i);
        if (child==nullptr)
            break;
        std::cout << "[" << tree.getIndex(child) << ": " << *child << "] ";
    }
    std::cout << "\n";
}


void printPathToRoot(Tree<int>& tree, int* node) {
    std::cout << "Path to root: [" << tree.getIndex(node) << ": " << *node << "]";
    while (node != tree.getRoot()) {
        node=tree.getParent(node);
        std::cout << "-[" << tree.getIndex(node) << ": " << *node << "]";
    }
    std::cout << "\n";
}

void printBFS(Tree<int>& tree) {
    for (int i = 0; i < tree.size(); ++i) {
        printNode(tree, tree.getNode(i));
        std::cout << " ";
    }
}

void printTree(Tree<int>& tree) {
    for (int i = 0; i < tree.size(); ++i) {
        printNodeInfo(tree, tree.getNode(i));
    }
}


int main() {
    Tree<int> test(8,11);
    test[0]=7;
    test[3]=-5;
    test[4]=7;
    std::cout << "Starting tree values:\n";
    printBFS(test);
    std::cout << "\nWrite number from 1 to 12\n";
    std::cout << "1. Print node info\n";
    std::cout << "2. Print path to root\n";
    std::cout << "3. Print all elements\n";
    std::cout << "4. Print all nodes\n";
    std::cout << "5. Set node's value\n";
    std::cout << "6. Go to child \n";
    std::cout << "7. Go to parent\n";
    std::cout << "8. Add child to the node and go there\n";
    std::cout << "9. Go to any node\n";
    std::cout << "10. Finish program\n";
    int* active_node = test.getRoot();
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
                printNodeInfo(test,active_node);
                break;
            case 2:
                printPathToRoot(test,active_node);
                break;
            case 3:
                printBFS(test);
                break;
            case 4:
                printTree(test);
                break;
            case 5:
                std::cout << "Input value: ";
                std::cin >> *active_node;
                break;
            case 6:
                std::cout << "Input child's number (1 or 2): ";
                std::cin >> f_index;
                if (test.getChild(active_node, f_index) == nullptr) {
                    std::cout << "Active node does not have child number " << f_index << "\n";
                }
                else {
                    active_node= test.getChild(active_node, f_index);
                }
                break;
            case 7:
                if (test.getParent(active_node) == nullptr) {
                    std::cout << "Active node is already a root, it does not have parent";
                }
                else {
                    active_node = test.getParent(active_node);
                }
                break;
            case 8:
                std::cout << "Input child's number (1 or 2): ";
                std::cin >> f_index;
                active_node = test.addChild(active_node, f_index);
                break;
            case 9:
                std::cout << "Input node's index: ";
                std::cin >> f_index;
                active_node = test.getNode(f_index);
                break;
            case 10:
                std::cout << "Program is finished";
                stop = 1;
                break;

            default:
                bad_number = 1;
                break;
            }
        }
        catch (const std::exception& e) {
            std::cin.clear();
            std::cin.ignore(INT_MAX, '\n');
            std::cout << "Exception: " << e.what() << "\n";
        }
        std::cin.clear();
        std::cin.ignore(INT_MAX, '\n');
        if (bad_number) {
            std::cout << "Bad input\n";
            continue;
        }



    }
}
