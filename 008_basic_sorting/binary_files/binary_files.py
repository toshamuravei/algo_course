from random import randbytes


_INTEGER_BYTESIZE = 2


def _get_random_binary_u_int() -> bytes:
    return randbytes(_INTEGER_BYTESIZE)


def write_n_binary_ints_to_file(filename: str, n: int) -> str:
    with open(filename, "w+b") as f:
        for i in range(0, n):
            f.write(_get_random_binary_u_int())

    return filename


def read_and_stringify(filename: str) -> str:
    rs = ""
    with open(filename, "r+b") as f:
        while byte := f.read(2):
            rs = rs + " " + str(int.from_bytes(byte, "little"))

    return rs


def read_binary_generator(filename: str) -> int:
    with open(filename, "r+b") as f:
        while byte := f.read(2):
            yield int.from_bytes(byte, "little")


def read_from_to(filename: str, _from: int, _to: int) -> int:
    counter = 0
    with open(filename, "r+b") as f:
        while byte := f.read(2):
            if  _from < counter < _to:
                counter += 1
                yield byte
            else:
                raise StopIteration



