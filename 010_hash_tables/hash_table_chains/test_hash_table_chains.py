import pytest

from .constants import constants
from .hash_table_chains import HashTableChains


def test_hashtable_creation():
    h_table = HashTableChains()

    assert h_table.items_stored == 0
    assert h_table.size == constants.INITIAL_SIZE
    assert h_table.REHASH_THRESHOLD == constants.REHASH_THRESHOLD


def test_hash_func():
    h_table = HashTableChains()

    key_to_hash = "some_good_key"
    expected_hash = 1380

    assert h_table.hash_func(key_to_hash) == expected_hash


def test_insert_and_get():
    h_table = HashTableChains()
    h_table.insert("answerOnAllQuestions", 42)

    assert h_table.get("answerOnAllQuestions") == 42


def test_rehashing():
    initial_size = 12
    rehash_threshold = int(0.5 * initial_size)
    h_table = HashTableChains(initial_size, rehash_threshold)

    keys_to_hash = [
        "foo",
        "bar",
        "fizz",
        "bazz",
        "good_key1",
        "good_key2"
    ]

    for k in keys_to_hash:
        h_table.insert(k, k)

    key_above_threshold = "good_key3"
    h_table.insert(key_above_threshold, key_above_threshold)

    keys_to_hash.append(key_above_threshold)

    for k in keys_to_hash:
        assert h_table.get(k) == k


def test_deleting():
    h_table = HashTableChains()

    keys_to_add = [
        "foo",
        "bar",
        "good_key1"
    ]

    for k in keys_to_add:
        h_table.insert(k, k)

    key_to_remove = "foo"

    h_table.remove(key_to_remove)
    removed_item = h_table.get(key_to_remove)
    assert h_table.get(key_to_remove) == None


def test_deleting_nonexisting_key():
    h_table = HashTableChains()

    with pytest.raises(ValueError):
        h_table.remove("foo-bar")


