
def decitoBin(numb):
  # converting it to binary representation using bin() function
    binNumb = bin(numb)
    # replacing '0b' using replace function and replacing it with empty string
    binNumb = binNumb.replace('0b', '')
  # return the binary representation of the given number
    return binNumb


def count_bits_rshift(number):
    number: int = int(number)

    bits_count = 0
    binary_number = decitoBin(number)
    print(f"Going to count 1-s in number {binary_number}\n=========\n\n")
    while number > 0:
        if number & 1 == 1:
            bits_count += 1

        number = number >> 1

    return bits_count

def count_bits_logical_mul(number):
    number: int = int(number)

    bits_count: int = 0
    while number > 0:
        bits_count += 1
        number = number & (number - 1)
    return bits_count


def count_bits_cached_256(number):
    number: int = int(number)
    octets = [count_bits_logical_mul(i) for i in range(0, 256)]
    result = 0
    #import pudb; pu.db
    for shift in range(0, 64, 8):
        result = result + octets[(number >> shift) & 255]
    return result


if __name__ == "__main__":
    print(count_bits_cached_256(13))

# 
