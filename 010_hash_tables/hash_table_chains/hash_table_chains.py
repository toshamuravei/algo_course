from .constants import constants


class HashTableChains:
    def __init__(self,
                 initial_table_size=constants.INITIAL_SIZE,
                 rehash_threshold=constants.REHASH_THRESHOLD):

        self.table = [None for i in range(0, initial_table_size)]
        self.size = initial_table_size
        self.items_stored = 0
        self.REHASH_THRESHOLD = rehash_threshold

    @classmethod
    def hash_func(cls, key_to_hash):
        if not isinstance(key_to_hash, str):
            raise NotImplementedError("Can't hash non string keys")

        if len(key_to_hash) == 0:
            raise ValueError("Empty string is not allowed to be a key")

        mapped_ord = map(ord, key_to_hash)
        mapped_ord = sum(mapped_ord)
        return mapped_ord

    def _key_to_index(self, key):
        hashed_key = self.hash_func(key)
        table_index = hashed_key % self.size
        return table_index

    def insert(self, key, value):
        if value is None:
            raise ValueError("It is not possible to store None values")

        table_index = self._key_to_index(key)
        table_bucket = self.table[table_index]

        is_present_in_table, in_bucket_index = self.search(key)

        if is_present_in_table:
            current_value = table_bucket[in_bucket_index][1]
            if current_value != value:
                table_bucket[in_bucket_index] = (key, value)
        else:
            if self.table[table_index] is None:
                self.table[table_index] = [(key, value)]
            else:
                self.table[table_index].append((key, value))
            self.items_stored += 1

        self.handle_insert()

    def handle_insert(self):
        if self.items_stored > self.REHASH_THRESHOLD:
            self._rehash()

    def _rehash(self):
        self.size *= constants.SIZE_EXTEND_RATIO
        self.REHASH_THRESHOLD *= constants.THRESHOLD_EXTEND_RATIO
        old_table_length = len(self.table)
        self._resize_table()
        for cell_index in range(0, old_table_length):
            cell = self.table[cell_index]
            if cell is None:
                continue
            else:
                self._rehash_cell(cell, cell_index)
                self.table[cell_index] = self._clear_empty_pairs(cell)

    def _resize_table(self):
        size_diff = self.size - len(self.table)
        for i in range(0, size_diff):
            self.table.append(None)

    def _rehash_cell(self, cell, current_cell_index):
        _temp_pairs = []
        for in_cell_item in cell:
            new_cell_index = self._key_to_index(in_cell_item[0])
            if new_cell_index != current_cell_index:
                _temp_pairs.append(in_cell_item)
                pair_to_remove_index = cell.index(in_cell_item)
                cell[pair_to_remove_index] = None

        self.table[current_cell_index] = self._clear_empty_pairs(cell)

        if len(_temp_pairs) > 0:
            for pair in _temp_pairs:
                self.insert(*pair)

    def _clear_empty_pairs(self, cell):
        _not_none_pairs = [pair for pair in cell if pair is not None]
        if len(_not_none_pairs) == 0:
            return None
        else:
            return _not_none_pairs

    def get(self, key):
        is_present_in_table, in_bucket_index = self.search(key)
        if not is_present_in_table:
            return None
        else:
            table_index = self._key_to_index(key)
            return self.table[table_index][in_bucket_index][1]

    def search(self, key):
        table_index = self._key_to_index(key)
        table_bucket = self.table[table_index]
        is_found = False
        entry_index = 0

        if table_bucket is not None:
            for entry in table_bucket:
                if entry[0] == key:
                    is_found = True
                    break
                entry_index += 1

        return is_found, entry_index

    def remove(self, key):
        is_key_in_table, in_bucket_idx = self.search(key)

        if not is_key_in_table:
            raise ValueError(f"Key {key} can't be removed, it's not in a table")

        table_index = self._key_to_index(key)
        table_bucket = self.table[table_index]

        removing_value = self.table[table_index][in_bucket_idx][1]
        del self.table[table_index][in_bucket_idx]
        self.items_stored -= 1

        return removing_value


