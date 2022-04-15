from copy import copy
from random import randint
from typing import List

from bst_tree import BST


def get_keys_to_insert() -> List[int]:
    root = randint(50, 100)
    root_l = root - 10
    root_r = root + 10

    root_l_l = root_l - 10
    root_l_r = root_l + 5

    root_r_l = root_r - 5
    root_r_r = root_r + 10

    keys_to_insert = [root, root_l, root_r, root_l_l, root_l_r, root_r_l, root_r_r]
    return keys_to_insert


def test_insertion():
    KEYS_TO_INSERT = get_keys_to_insert()
    tree = BST()
    for k in KEYS_TO_INSERT:
        tree.insert(k)

    assert tree.root == KEYS_TO_INSERT[0]
    assert tree.root.left == KEYS_TO_INSERT[1]
    assert tree.root.right == KEYS_TO_INSERT[2]
    assert tree.root.left.left == KEYS_TO_INSERT[3]
    assert tree.root.left.right == KEYS_TO_INSERT[4]
    assert tree.root.right.left == KEYS_TO_INSERT[5]
    assert tree.root.right.right == KEYS_TO_INSERT[6]


def test_walk():
    KEYS_TO_INSERT = get_keys_to_insert()
    tree = BST()
    for k in KEYS_TO_INSERT:
        tree.insert(k)

    walking_list = []
    tree.walk(tree.root, walking_list)
    walking_result = [node.key for node in walking_list]

    sorted_keys = copy(KEYS_TO_INSERT)
    sorted_keys.sort()

    assert walking_result == sorted_keys


def test_search():
    KEYS_TO_INSERT = get_keys_to_insert()
    tree = BST()
    for k in KEYS_TO_INSERT:
        tree.insert(k)

    for k in KEYS_TO_INSERT:
        assert tree.search(k) is True

    NOT_IN_TREE_GREATER: int = KEYS_TO_INSERT[6] + 1
    NOT_IN_TREE_SMALLER: int = KEYS_TO_INSERT[3] - 1

    assert tree.search(NOT_IN_TREE_GREATER) is False
    assert tree.search(NOT_IN_TREE_SMALLER) is False


def test_remove_leave():
    KEYS_TO_INSERT = get_keys_to_insert()
    tree = BST()
    for k in KEYS_TO_INSERT:
        tree.insert(k)

    tree.remove(KEYS_TO_INSERT[6])

    assert tree.search(KEYS_TO_INSERT[6]) is False


def test_remove_single_parent():
    KEYS_TO_INSERT = get_keys_to_insert()
    tree = BST()
    for k in KEYS_TO_INSERT:
        tree.insert(k)

    tree.remove(KEYS_TO_INSERT[6])
    tree.remove(KEYS_TO_INSERT[2])

    assert tree.search(KEYS_TO_INSERT[2]) is False
    assert tree.root.right == KEYS_TO_INSERT[5]


def test_remove_full_parent():
    KEYS_TO_INSERT = get_keys_to_insert()
    tree = BST()
    for k in KEYS_TO_INSERT:
        tree.insert(k)

    tree.remove(KEYS_TO_INSERT[2])

    assert tree.search(KEYS_TO_INSERT[2]) is False
    assert tree.root.right == KEYS_TO_INSERT[6]
    assert tree.root.right.right is None


if __name__ == "__main__":
    tests_to_execute = [
        test_insertion,
        test_walk,
        test_search,
        test_remove_leave,
        test_remove_single_parent,
        test_remove_full_parent
    ]

    for t in tests_to_execute:
        try:
            t()
            print(f"Test {t.__name__} is PASSED")
        except AssertionError as ex:
            print(f"ERR: Test {t.__name__} is failed!")
            print(ex)

