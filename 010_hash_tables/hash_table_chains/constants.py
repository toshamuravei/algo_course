from dataclasses import dataclass


@dataclass
class HashTableChainsConstants:
    REHASH_THRESHOLD = 10
    INITIAL_SIZE = 20
    SIZE_EXTEND_RATIO = 2
    THRESHOLD_EXTEND_RATIO = 2


constants = HashTableChainsConstants()

