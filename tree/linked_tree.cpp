#include <cassert>
#include <iostream>



#include <cstdint>
#include <stdexcept>
#include<iostream>
#include<vector>






template<typename type>
class Tree {
public:
    Tree();
    explicit Tree(ptrdiff_t size);
    Tree(ptrdiff_t size, const type& common, int children_amount_ = 2);
    Tree(const Tree& rhs) = default;
    Tree& operator=(const Tree& rhs) = default;//копирующий оператор присваивания
    ~Tree() = default;
    std::ptrdiff_t size() const noexcept;//узнать размер массива
    int getChildAmount() const noexcept;//узнать общее количество детей у вершин дерева

    type* getRoot() noexcept { return &tree_val_[0]; }// возвращает указатель на нулевую вершину
    type* getNode(ptrdiff_t index) { indexCheck(index); return &tree_val_[index]; }// возвращает указатель на указанную вершину
    ptrdiff_t getIndex(const type* node) const { ptrdiff_t index = node - &tree_val_[0]; nodeCheck(index); return index; } // получить индекс вершины из указаетля
    const type* getRoot() const noexcept { return &tree_val_[0]; }
    const type* getNode(ptrdiff_t index) const { indexCheck(index); return &tree_val_[index]; }
    type* getChild(type* node, int child_num);// получить указатель на n-ого ребёнка, если ребёнок находится вне пределов массива, возвращает nullptr
    type* getParent(type* node);

    type* addChild(type* node, int child_num);//анналогичен getChild, но в случае если индеск ребёнка находится за пределами массива, то расширает массив, так чтобы его последним элементом был нужный ребёнок
    type& operator[](ptrdiff_t index) { indexCheck(index); return tree_val_[index]; }//доступ к значению элемента по индексу
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
Tree<type>::Tree() :size_(1), tree_val_(1), children_amount_(2) {}

template<typename type>
Tree<type>::Tree(ptrdiff_t size) : size_(size), tree_val_(size), children_amount_(2) {}


template<typename type>
Tree<type>::Tree(ptrdiff_t size, const type& common, int childrea_amount) : size_(size), tree_val_(size, common), children_amount_(childrea_amount) {}


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
        tree_val_.resize(index + 1);
        size_ = index + 1;
        return &tree_val_[index];
    }
}


template<typename type>
type* Tree<type>::getParent(type* node) {
    ptrdiff_t index = node - &tree_val_[0];
    if (index == 0)
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
    if (parent != nullptr)
        std::cout << "Parent: [" << tree.getIndex(tree.getParent(node)) << ": " << *tree.getParent(node) << "]\n ";
    std::cout << "Children: ";
    for (int i = 1; i <= tree.getChildAmount(); ++i) {
        bool stop = 0;
        int* child = tree.getChild(node, i);
        if (child == nullptr)
            break;
        std::cout << "[" << tree.getIndex(child) << ": " << *child << "] ";
    }
    std::cout << "\n";
}


void printPathToRoot(Tree<int>& tree, int* node) {
    std::cout << "Path to root: [" << tree.getIndex(node) << ": " << *node << "]";
    while (node != tree.getRoot()) {
        node = tree.getParent(node);
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


void seqTreeTest() {
    Tree<int> test(8, 11);
    test[0] = 7;
    test[3] = -5;
    test[4] = 7;
    std::cout << "Starting tree values:\n";
    printBFS(test);
    std::cout << "\nWrite number from 1 to 10\n";
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
                printNodeInfo(test, active_node);
                break;
            case 2:
                printPathToRoot(test, active_node);
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
                    active_node = test.getChild(active_node, f_index);
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




namespace {

  template <typename Key, typename Value> struct LinkedNode {
    LinkedNode(const LinkedNode&) = default;
    LinkedNode(const std::pair<Key, Value>& value) : value(value) {}
    std::pair<Key, Value> value;
    LinkedNode* left = nullptr;
    LinkedNode* right = nullptr;
    LinkedNode* parent = nullptr;
  };

} // namespace

namespace ve {
    template <typename Key, typename Value, typename Compare = std::less<Key>>
    class LinkedTree {
    public:
        using ValueType = std::pair<Key, Value>;
        LinkedTree() = default;

        Value& insert(const ValueType& node);

        [[nodsicard]] std::size_t size() const { return size_; }

        [[nodiscard]] Value& operator[](const Key& key);
        [[nodiscard]] const Value& operator[](const Key& key) const;

        void remove(const Key& key);
        LinkedNode<Key, Value>* find(const Key& key);

        LinkedNode<Key, Value>* getRoot() { return root_; };

    private:
        LinkedNode<Key, Value>* root_ = nullptr;
        LinkedNode<Key, Value>* first_ = nullptr;
        std::size_t size_ = 0;

        bool isToTheRight(const Key& lhs, const Key& rhs) {
            return Compare{}(lhs, rhs);
        }
        Value& insertAfter(LinkedNode<Key, Value>* after_what,
            const ValueType& value) {
            LinkedNode<Key, Value>* new_node = new LinkedNode<Key, Value>(value);
            isToTheRight(after_what->value.first, value.first)
                ? after_what->right = new_node
                : after_what->left = new_node;
            size_++;
            new_node->parent = after_what;
            return new_node->value.second;
        }
    };

    template <typename K, typename V>
    LinkedNode<K, V>* leftMost(LinkedNode<K, V>* after) {
        LinkedNode<K, V>* current_node = after;
        if (current_node == nullptr) return nullptr;
        while (current_node->left != nullptr) {
            current_node = current_node->left;
        }
        return current_node;
    }

    template <typename K, typename V>
    LinkedNode<K, V>* nextNode(LinkedNode<K, V>* after) {
        if (after->right != nullptr) {
            return leftMost(after->right);
        }

        LinkedNode<K, V>* parent = after->parent;
        if (parent == nullptr) {
            return nullptr;
        }
        if (after == parent->left) {
            return parent;
        }

        while (parent != nullptr && after != parent->left) {
            after = parent;
            parent = after->parent;
        }
        return parent;
    }
    template <typename K, typename V> void printTree(LinkedNode<K, V>* root) {
        auto* left = leftMost(root);
        LinkedNode<K, V>* next = left;
        while (next != nullptr) {
            std::cout << " { " << next->value.first << " -> " << next->value.second
                << " }\n";
            next = nextNode(next);
        }
    }
}

int main() {
    int choose = 0;
    std::cout << "Print 1 for seq tree and 2 for linked tree: ";
    std::cin >> choose;
    if (choose == 1) {
        seqTreeTest();
        return 0;
    }

  std::cout << "Write number from 1 to 5\n";
  std::cout << "1. Print current tree\n";
  std::cout << "2. Change element's value\n";
  std::cout << "3. Insert element\n";
  std::cout << "4. Remove element\n";
  std::cout << "5. Finish program\n";

  bool stop = 0;
  ve::LinkedTree<int, std::string, std::greater<int>> test_tree;
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
        ve::printTree(test_tree.getRoot());
        break;
      case 2:
        std::cout << "Input key and new string value: ";
        std::cin >> f_index >> s;
        test_tree[f_index] = s;
        break;
      case 3:
        std::cout << "Input key and string: ";
        std::cin >> f_index >> s;
        test_tree.insert({ f_index, s });
        break;
      case 4:
        std::cout << "Input index: ";
        std::cin >> f_index;
        test_tree.remove(f_index);
        break;
      case 5:
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
  return 0;
  
}

namespace ve {
    template <typename Key, typename Value, typename Compare>
    Value& LinkedTree<Key, Value, Compare>::insert(const ValueType& node) {
        LinkedNode<Key, Value>* current_node = root_;
        LinkedNode<Key, Value>* prev_node = nullptr;
        bool did_it_go_right = false;
        int counter = 0;

        while (counter != size() + 1) {
            if (current_node == nullptr) {
                current_node = new LinkedNode<Key, Value>(node);
                if (root_ == nullptr)
                    root_ = current_node;

                if (prev_node != nullptr) {
                    did_it_go_right ? prev_node->right = current_node
                        : prev_node->left = current_node;
                }
                current_node->parent = prev_node;
                size_ += 1;
                return current_node->value.second;
            }

            if (current_node->value.first == node.first)
                return current_node->value.second;

            did_it_go_right = isToTheRight(current_node->value.first, node.first);
            prev_node = current_node;
            did_it_go_right ? current_node = current_node->right
                : current_node = current_node->left;
            ++counter;
        }
    }

    template <typename Key, typename Value, typename Compare>
    Value& LinkedTree<Key, Value, Compare>::operator[](const Key& key) {
        auto* node = find(key);
        if (node == nullptr) {
            return insert({ key, Value{} });
        }
        return node->value.second;
    }

    template <typename Key, typename Value, typename Compare>
    const Value& LinkedTree<Key, Value, Compare>::operator[](const Key& key) const {
        return this[key];
    }

    template <typename Key, typename Value, typename Compare>
    void LinkedTree<Key, Value, Compare>::remove(const Key& key) {
        LinkedNode<Key, Value>* current_node = find(key);

        if (current_node == nullptr) {
            return;
        }
        if (current_node->left == nullptr && current_node->right == nullptr) {
            if (current_node != root_) {
                isToTheRight(current_node->parent->value.first, current_node->value.first) ? current_node->parent->right = nullptr : current_node->parent->left = nullptr;
            }
            if (current_node == root_) root_ = nullptr;
            delete current_node;
            current_node = nullptr;
        }
        else if (current_node->left == nullptr) {
            if (current_node != root_) {
                current_node->parent->right = current_node->right;
                current_node->right->parent = current_node->parent;
            }
            else {
                root_ = current_node->right;
                current_node->right->parent = nullptr;
            }
            delete current_node;
            current_node = nullptr;
        }
        else if (current_node->right == nullptr) {
            if (current_node != root_) {
                current_node->parent->left = current_node->left;
                current_node->left->parent = current_node->parent;
            }
            else {
                root_ = current_node->left;
                current_node->left->parent = nullptr;
            }
            delete current_node;
            current_node = nullptr;
        }
        else {
            if (isToTheRight(current_node->parent->value.first, current_node->value.first)) {
                LinkedNode<Key, Value>* left = leftMost(current_node);
                current_node->parent->right = left;
                current_node->right->parent = left;
                left->parent->left = left->right;
                left->parent = current_node->parent;
                left->right = current_node->right;
                left->left = current_node->left;
                delete current_node;
                current_node = nullptr;
            }
        }
        size_--;
    }

    template <typename Key, typename Value, typename Compare>
    LinkedNode<Key, Value>* LinkedTree<Key, Value, Compare>::find(const Key& key) {
        LinkedNode<Key, Value>* current_node = root_;
        while (current_node != nullptr) {
            if (key == current_node->value.first)
                return current_node;
            isToTheRight(current_node->value.first, key)
                ? current_node = current_node->right
                : current_node = current_node->left;
        }
        return nullptr;
    }
}