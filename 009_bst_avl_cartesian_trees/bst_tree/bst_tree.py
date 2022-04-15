

class TreeNode:
    COMPARSION_ERR = "Can't compare BST Node and {}"

    def __init__(self, key: int, parent=None):
        self.key = key
        self.left = None
        self.right = None
        self.parent = parent

    def __repr__(self):
        r_key = self.right.key if self.right else "NULL"
        l_key = self.left.key if self.left else "NULL"
        self_str = f"Node: Key: {self.key} | Left: {l_key} | Right: {r_key} |"
        return self_str

    def __eq__(self, value):
        if isinstance(value, int):
            return self.key == value
        elif isinstance(value, self.__class__):
            return self.key == value.key
        else:
            raise NotImplementedError(self.COMPARSION_ERR.format(type(value)))

    def __lt__(self, value):
        if isinstance(value, int):
            return self.key < value
        elif isinstance(value, self.__class__):
            return self.key < value.key
        else:
            raise NotImplementedError(self.COMPARSION_ERR.format(type(value)))

    def __gt__(self, value):
        if isinstance(value, int):
            return self.key > value
        elif isinstance(value, self.__class__):
            return self.key > value.key
        else:
            raise NotImplementedError(self.COMPARSION_ERR.format(type(value)))

    @property
    def children_count(self):
        return int(self.left is not None) + int(self.right is not None)

    @property
    def child(self):
        if self.left is not None:
            return self.left

        if self.right is not None:
            return self.right

    def swap(self, with_node):
        self.key, with_node.key = with_node.key, self.key

    def remove_child(self, child_to_remove):
        if self.left == child_to_remove:
            self.left = None
        if self.right == child_to_remove:
            self.right = None

        child_to_remove.parent = None

    def adopt_grandchild_from(self, old_parent):
        if self.left == old_parent:
            self.left = old_parent.child
        elif self.right == old_parent:
            self.right = old_parent.child

        old_parent.left, old_parent.right = None, None
        old_parent.parent = None
        return


class BST:
    def __init__(self, node_class=TreeNode):
        self.root = None
        self.node_cls = node_class

    def insert(self, key, from_node=None):
        if from_node is None:
            from_node = self.root

        if self.root is None:
            self.root = self.node_cls(key)
            return self.root

        if key == from_node:
            return from_node

        if key > from_node:
            if from_node.right is None:
                from_node.right = self.node_cls(key, parent=from_node)
                return from_node.right
            else:
                return self.insert(key, from_node.right)

        if key < from_node:
            if from_node.left is None:
                from_node.left = self.node_cls(key, parent=from_node)
                return from_node.left
            else:
                return self.insert(key, from_node.left)

    def walk(self, from_node, nodes_list):
        if from_node is None:
            return

        self.walk(from_node.left, nodes_list)
        nodes_list.append(from_node)
        self.walk(from_node.right, nodes_list)

    def search(self, key, from_node=None):
        if from_node is None:
            from_node = self.root

        if key == from_node:
            return True

        if key < from_node and from_node.left is not None:
            return self.search(key, from_node.left)

        if key > from_node and from_node.right is not None:
            return self.search(key, from_node.right)

        return False

    def remove(self, key):
        node = self._search_node(key)
        if not node:
            raise ValueError(f"Key {key} not in tree!")

        # leave removing
        if node.children_count == 0:
            if node.parent is None:
                self.root = None
            return self._remove_leave(node)

        # single parent removing
        if node.children_count == 1:
            if node.parent is None:
                self.root = node.child
                node.child.parent = None
            else:
                node.parent.adopt_grandchild_from(node)
            return node

        # full parent remove
        if node.children_count == 2:
            min_of_greatest = self.get_min_in_subtree(node.right)
            node.swap(min_of_greatest)
            return self._remove_leave(min_of_greatest)

    def _remove_leave(self, node):
        if node.children_count > 0:
            raise ValueError(f"{node} is not a leave")
        else:
            return node.parent.remove_child(node)

    def get_min_in_subtree(self, subtree_root):
        if subtree_root.left is None:
            return subtree_root
        else:
            return self.get_min_in_subtree(subtree_root.left)

    def _search_node(self, key, from_node=None):
        if from_node is None:
            from_node = self.root

        if key == from_node:
            return from_node

        if key < from_node and from_node.left is not None:
            return self._search_node(key, from_node.left)

        if key > from_node and from_node.right is not None:
            return self._search_node(key, from_node.right)

        return None

