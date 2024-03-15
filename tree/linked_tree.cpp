#include <cassert>
#include <iostream>

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

int main() {
  std::cout << "Write number from 1 to 5\n";
  std::cout << "1. Print current tree\n";
  std::cout << "2. Change element's value\n";
  std::cout << "3. Insert element\n";
  std::cout << "4. Remove element\n";
  std::cout << "5. Finish program\n";

  bool stop = 0;
  LinkedTree<int, std::string> test_tree;
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
        printTree(test_tree.getRoot());
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
  LinkedTree<int, int, std::less<int>> test;
  assert(test.size() == 0);
  test.insert({ 2, 2 });
  assert(test.size() == 1);
  test.insert({ 1, 1 });
  assert(test.size() == 2);
  test.insert({ 1, 2 });
  assert(test.size() == 2);
  test.insert({ 3, 3 });
  assert(test.size() == 3);
  test.insert({ 4, 4 });
  assert(test.size() == 4);
  assert(test[1] == 1);
  assert(test[2] == 2);
  assert(test[5] == 0);
  assert(test.size() == 5);
  test.remove(5);
  test[5];
  test[10];
  test[15];
  test[6];
  test.remove(10);
  printTree<int, int>(test.getRoot());

  LinkedTree<std::string, int> test_string;
  test_string.insert({ "Hello world", 1 });
  test_string.insert({ "Bye world", 2 });
  printTree<std::string, int>(test_string.getRoot());
}

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
