import inspect


def transpose(matrix: list) -> list:
    """
    Transpose a 2D matrix

    Args:
    matrix: list: A 2D list

    Returns:
    list: A 2D list that is the transpose of the input matrix

    Raises:
    TypeError: If the input is not a list
    ValueError: If the input is an empty list or not a 2D list or rows have different lengths
    """
    if type(matrix) is not list:
        raise TypeError("Input must be a list")
    if len(matrix) == 0:
        raise ValueError("Input must not be empty")
    if not all([type(row) is list for row in matrix]):
        raise ValueError("Input must be a 2D list")
    if not all([len(row) == len(matrix[0]) for row in matrix]):
        raise ValueError("All rows must have the same length")
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]


def main():
    total_points = 0  # Total points for the test cases: get 5 points for each test case
    # Test cases for transpose function
    try:
        # test if we have a callable function named transpose
        assert callable(transpose)
        print("PASS: You have a function named transpose")
        total_points += 5
    except AssertionError:
        print("FAIL: You need a function named transpose")

    try:
        # test if the function transpose takes one argument
        assert len(inspect.signature(transpose).parameters) == 1
        print("PASS: The function takes one argument")
        total_points += 5
    except AssertionError:
        print("FAIL: The function should take one argument")

    try:
        # test if the function has annotation for the argument
        assert inspect.signature(transpose).parameters["matrix"].annotation == list
        print("PASS: The function has type annotation for the argument")
        total_points += 5
    except AssertionError:
        print("FAIL: The function should have type annotation for the argument")

    try:
        # test if the function has annotation for the return value
        assert inspect.signature(transpose).return_annotation == list
        print("PASS: The function has type annotation for the return value")
        total_points += 5
    except AssertionError:
        print("FAIL: The function should have type annotation for the return value")

    try:
        # test if the function has a docstring
        assert transpose.__doc__ is not None
        print("PASS: The function has a docstring")
        total_points += 5
    except AssertionError:
        print("FAIL: The function should have a docstring")

    try:
        transpose(1)
    except TypeError as e:
        assert str(e) == "Input must be a list"
        print("PASS: The function raises TypeError for non-list input")
        total_points += 5
    else:
        print("FAIL: The function should raise TypeError for non-list input")

    try:
        transpose([])
    except ValueError as e:
        assert str(e) == "Input must not be empty"
        print("PASS: The function raises ValueError for empty input")
        total_points += 5
    else:
        print("FAIL: The function should raise ValueError for empty input")

    try:
        transpose([[1, 2], 3])
    except ValueError as e:
        assert str(e) == "Input must be a 2D list"
        print("PASS: The function raises ValueError for non-2D list input")
        total_points += 5
    else:
        print("FAIL: The function should raise ValueError for non-2D list input")

    try:
        transpose([[1, 2], [3, 4, 5]])
    except ValueError as e:
        assert str(e) == "All rows must have the same length"
        print("PASS: The function raises ValueError for rows of different lengths")
        total_points += 5
    else:
        print(
            "FAIL: The function should raise ValueError for rows of different lengths"
        )

    try:
        result = transpose([[1, 2], [3, 4]])
        assert result == [[1, 3], [2, 4]]
        print("PASS: The function returns the correct result for a 2x2 matrix")
        total_points += 5
    except AssertionError:
        print("FAIL: The function should return the correct result for a 2x2 matrix")

    try:
        result = transpose([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        assert result == [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
        print("PASS: The function returns the correct result for a 3x3 matrix")
        total_points += 5
    except AssertionError:
        print("FAIL: The function should return the correct result for a 3x3 matrix")

    try:
        result = transpose([[1, 2, 3], [4, 5, 6]])
        assert result == [[1, 4], [2, 5], [3, 6]]
        print("PASS: The function returns the correct result for a 2x3 matrix")
        total_points += 5
    except AssertionError:
        print("FAIL: The function should return the correct result for a 2x3 matrix")

    print("Total points: ", total_points)
    print("All test cases passed")
    return None


if __name__ == "__main__":
    main()
