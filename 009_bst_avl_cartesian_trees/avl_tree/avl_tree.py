
class TreeNode:
    COMPARSION_ERR = "Can't compare AVL Node and {}"

    def __init__(self, key: int, parent=None):
        self.key = key
        self.left = None
        self.right = None
        self.parent = parent
        self.height = 1

    def __repr__(self):
        r_key = self.right.key if self.right else "NULL"
        l_key = self.left.key if self.left else "NULL"
        self_str = f"Node: Key: {self.key} | Left: {l_key} | Right: {r_key} |"
        self_str += f" | Height: {self.height}"
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

    @property
    def balance_factor(self):
        l_height = self.left.height if self.left else 0
        r_height = self.right.height if self.right else 0
        return r_height - l_height

    def update_height(self):
        l_height = self.left.height if self.left else 0
        r_height = self.right.height if self.right else 0
        self.height = max(l_height, r_height) + 1

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

    def child_relation_of(self, node):
        if self.left == node:
            return "left"
        if self.right == node:
            return "right"
        else:
            raise ValueError(f"{node} is not a child for {self}")


class AVLTree:
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

        # TODO: MAKE BALANCE CHECKS ALSO HERE, RECURSIVELY
        if key > from_node:
            if from_node.right is None:
                from_node.right = self.node_cls(key, parent=from_node)
                from_node.update_height()
                self.rebalance(from_node, "right")
                return from_node.right
            else:
                inserted_node = self.insert(key, from_node.right)
                from_node.update_height()
                self.rebalance(from_node, "right")
                return inserted_node

        if key < from_node:
            if from_node.left is None:
                from_node.left = self.node_cls(key, parent=from_node)
                from_node.update_height()
                self.rebalance(from_node, "left")
                return from_node.left
            else:
                inserted_node = self.insert(key, from_node.left)
                from_node.update_height()
                self.rebalance(from_node, "left")
                return inserted_node

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

    def rotate_left(self, node):
        if node.right is None:
            raise ValueError(f"ERR: left rotation: no right child in {node}")

        going_up_node = node.right
        going_down_node = node

        going_up_node.parent = going_down_node.parent
        if going_down_node.parent is None:
            self.root = going_up_node
        else:
            grand_parent = going_down_node.parent
            relation: str = grand_parent.child_relation_of(going_down_node)
            setattr(grand_parent, relation, going_up_node)

        going_down_node.right = going_up_node.left
        going_up_node.left = going_down_node
        self.recalc_heights_from(going_down_node)
        return going_up_node

    def rotate_right(self, node):
        if node.left is None:
            raise ValueError(f"ERR: right rotation: no left child in {node}")

        going_up_node = node.left
        going_down_node = node

        going_up_node.parent = going_down_node.parent
        if going_down_node.parent is None:
            self.root = going_up_node
        else:
            grand_parent = going_down_node.parent
            relation: str = grand_parent.child_relation_of(going_down_node)
            setattr(grand_parent, relation, going_up_node)

        going_down_node.left = going_up_node.right
        going_up_node.right = going_down_node
        self.recalc_heights_from(going_down_node)
        return going_up_node

    def rebalance(self, node, insert_direction):

        if  -1 <= node.balance_factor <= 1:
            return

        # right right case
        if insert_direction == "right" and node.right.balance_factor >= 0:
            return self.rotate_left(node)

        # left left case
        if insert_direction == "left" and node.left.balance_factor <= 0:
            return self.rotate_right(node)

        # right left case
        if insert_direction == "right" and node.right.balance_factor < 0:
            self.rotate_right(node.right)
            return self.rotate_left(node)

        # left right case
        if insert_direction == "left" and node.left.balance_factor > 0:
            self.rotate_left(node.left)
            return self.rotate_right(node)

    def recalc_heights_from(self, from_node):
        if from_node is None:
            return

        from_node.update_height()

        while from_node.parent is not None:
            from_node = from_node.parent
            from_node.update_height()

