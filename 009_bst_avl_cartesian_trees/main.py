import time
from random import randint, choice

from avl_tree import AVLTree
from bst_tree import BinarySearchTree


def test_insert(t: BinarySearchTree, key: int):
    inserted, node = t.insert(key)
    print(f"Inserted: {inserted}. Node: {node}")
    return t


def multiple_inserts(t: BinarySearchTree, keys):

    for k in keys:
        t = test_insert(t, k)

    return t


def test_search(t: BinarySearchTree, key: int):
    node = t.search(key)
    if node is None:
        print(f"Key: {key} was not found!")
    else:
        print(f"Found: {node}")


def test_tree_from_list(root, l, test_name,):
    results = {test_name:{}}
    t = BinarySearchTree(root)

    # test addition
    start = time.time()
    for i in l:
        t.insert(i)
    end = time.time()
    results[test_name]["add_N_elements"] = end - start

    # test search
    numbers_to_search = [choice(l) for i in range(0, (len(l) // 10))]
    start = time.time()
    for i in numbers_to_search:
        t.search(i)
    end = time.time()
    results[test_name]["search_elements"] = end - start

    # test remove
    numbers_to_remove = [choice(l) for i in range(0, (len(l) // 10))]
    start = time.time()
    for i in numbers_to_remove:
        t.remove(i)
    end = time.time()
    results[test_name]["removing_elements"] = end - start

    return results


def test_trees(N):
    tests = {
        "sequensive": (0, [i for i in range(0, N)]),
        "random": (choice(range(0, N)), [randint(0, N) for i in range(0, N)])
    }
    results = []

    for k, v in tests.items():
        results.append(test_tree_from_list(v[0], v[1], k))

    print(results)


def avl_test_insert():
    a = AVLTree(40)
    l = [16, 45, 10, 36, 8, 12, 30, 22, 28]
    for i in l:
        a.insert(i)
    a.walk(a.root)


def test_small_right_rotate():
    a = AVLTree(8)
    l = [5, 9, 10, 4, 3, 2, 6, 7]
    for i in l:
        a.insert(i)
    #a.walk(a.root)

    a.small_rotate(8, "right")
    print("\n\n")
    a.walk(a.root)


def test_balancing():
    a = AVLTree(10)
    l = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
    for i in l:
        print(f"inserting {i}")
        a.insert(i)
    a.walk(a.root)


if __name__ == "__main__":
    #test_small_right_rotate()
    #test_trees(900)
    test_balancing()
