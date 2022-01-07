from random import randint

from radix_sort import radix_sort


def test_radix_sort():
    l = [randint(0, 1000) for x in range(0, 100)]
    print(f"list before sort: {l}")
    l = radix_sort(l)
    print(f"list after sort: {l}")


if __name__ == "__main__":
    test_radix_sort()

