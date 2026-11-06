
def remove_duplicates(numbers):
    result = []

    for number in numbers:
        if number in result:
            continue
        result.append(number)

    return result


def list_counts(numbers):
    frequency = {}

    for number in numbers:
        if number not in frequency:
            frequency[number] = 0

        frequency[number] += 1

    return frequency


def reverse_dict(original):
    reversed_data = {}

    for key in original:
        value = original[key]
        reversed_data[value] = key

    return reversed_data
