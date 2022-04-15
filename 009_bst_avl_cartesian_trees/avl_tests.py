from random import randint
from typing import List

from avl_tree import AVLTree, TreeNode


def get_keys_to_insert() -> List[int]:
    KEYS = [100, 200, 250, 230, 260, 225]
    return KEYS


def get_sequentive_keys_to_insert() -> List[int]:
    return [i for i in range(0, 15)]


def test_right_rotation():
    tree = AVLTree()
    tree.insert(10)

    a = tree.root

    b = TreeNode(5, parent=a)
    a.left = b

    c = TreeNode(15, parent=a)
    a.right = c

    d = TreeNode(7, parent=b)
    b.right = d

    e = TreeNode(4, parent=b)
    b.left = e

    tree.rotate_right(tree.root)

    assert tree.root == b
    assert tree.root.left == e
    assert tree.root.right == a
    assert tree.root.right.left == d
    assert tree.root.right.right == c


def test_left_rotation():
    tree = AVLTree()
    tree.insert(10)

    a = tree.root

    b = TreeNode(5, parent=a)
    a.left = b

    c = TreeNode(15, parent=a)
    a.right = c

    d = TreeNode(17, parent=c)
    c.right = d

    e = TreeNode(13, parent=c)
    c.left = e

    tree.rotate_left(tree.root)

    assert tree.root == c
    assert tree.root.left == a
    assert tree.root.left.left == b
    assert tree.root.right == d
    assert tree.root.left.right == e


def test_height_updates():
    tree = AVLTree()
    KEYS_TO_INSERT = [10, 5, 15, 4, 7, 13, 17, 3, 2, 1]
    for key in KEYS_TO_INSERT:
        tree.insert(key)

    assert tree.root.height == 4
    assert tree.root.right.height == 2
    assert tree.root.left.height == 3
    assert tree.root.right.right.height == 1


def test_balancing_long_rotations():
    KEYS_TO_INSERT = get_keys_to_insert()
    tree = AVLTree()
    for k in KEYS_TO_INSERT:
        tree.insert(k)

    assert tree.root == KEYS_TO_INSERT[3]
    assert tree.root.left == KEYS_TO_INSERT[1]
    assert tree.root.left.right == KEYS_TO_INSERT[5]
    assert tree.root.left.left == KEYS_TO_INSERT[0]
    assert tree.root.right == KEYS_TO_INSERT[2]
    assert tree.root.right.right == KEYS_TO_INSERT[4]


def test_balancing_short_rotations():
    KEYS_TO_INSERT = get_sequentive_keys_to_insert()
    tree = AVLTree()
    for k in KEYS_TO_INSERT:
        tree.insert(k)

    assert tree.root == KEYS_TO_INSERT[7]

    assert tree.root.left == KEYS_TO_INSERT[3]
    assert tree.root.left.left == KEYS_TO_INSERT[1]
    assert tree.root.left.right == KEYS_TO_INSERT[5]
    assert tree.root.left.left.left == KEYS_TO_INSERT[0]
    assert tree.root.left.left.right == KEYS_TO_INSERT[2]
    assert tree.root.left.right.left == KEYS_TO_INSERT[4]
    assert tree.root.left.right.right == KEYS_TO_INSERT[6]

    assert tree.root.right == KEYS_TO_INSERT[11]
    assert tree.root.right.left == KEYS_TO_INSERT[9]
    assert tree.root.right.left.left == KEYS_TO_INSERT[8]
    assert tree.root.right.left.right == KEYS_TO_INSERT[10]
    assert tree.root.right.right == KEYS_TO_INSERT[13]
    assert tree.root.right.right.left == KEYS_TO_INSERT[12]
    assert tree.root.right.right.right == KEYS_TO_INSERT[14]


if __name__ == "__main__":
    tests_to_execute = [
        test_right_rotation,
        test_left_rotation,
        test_height_updates,
        test_balancing_short_rotations,
        test_balancing_long_rotations
    ]

    for test in tests_to_execute:
        try:
            test()
            print(f"Test {test.__name__} is PASSED")
        except AssertionError as ex:
            print(f"ERR: Test {test.__name__} is failed!")
            print(ex)

