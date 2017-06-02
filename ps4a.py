
def get_permutations(sequence):
    """
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.

    Returns: a list of all permutations of sequence
    """

    if len(sequence) == 1:
        return [sequence]

    else:
        result = []
        # reduce the problem and iterate over returned list
        for element in get_permutations(sequence[1:len(sequence)]):
            # put the first character of the sequence on the beginning
            # and the end of every combination
            result.append(sequence[0] + element)
            result.append(element + sequence[0])
            # put the first character on every position inside every combination
            for i in range(1, len(element)):
                result.append(element[:i] + sequence[0] + element[i:])
    # remove duplicates
    return list(set(result))


def test(expect, result):
    """
    expect: list of strings
    result: list of strings
    return: True if result coincides with expect and False otherwise
    """
    for element in result:
        if element not in expect:
            print("FAILURE")
            return False
    print("SUCCESS")
    return True

if __name__ == '__main__':

    test_input_1 = "123"
    expected_output_1 = ['123', '132', '213', '231', '312', '321']
    result_1 = get_permutations(test_input_1)

    print("Input:", test_input_1)
    print("Expected output:", expected_output_1)
    print("Actual output:", get_permutations(test_input_1))
    test(expected_output_1, result_1)

    test_input_2 = "car"
    expected_output_2 = ['arc', 'rca', 'acr', 'rac', 'car', 'cra']
    result_2 = get_permutations(test_input_2)

    print("Input:", test_input_2)
    print("Expected output:", expected_output_2)
    print("Actual output:", get_permutations(test_input_2))
    test(expected_output_2, result_2)

    test_input_3 = "ara"
    expected_output_3 = ['aar', 'raa', 'ara']
    result_3 = get_permutations(test_input_3)

    print("Input:", test_input_3)
    print("Expected output:", expected_output_3)
    print("Actual output:", get_permutations(test_input_3))
    test(expected_output_3, get_permutations(test_input_3))
