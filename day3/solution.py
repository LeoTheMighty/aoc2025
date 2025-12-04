TEST_ANSWER="3121910778619"
MAX_DEPTH = 12

def find_max_value(line: str, depth: int = 0) -> str:
    """
    First find the list of largest first numbers. 

    It has to be before index MAX_DEPTH - depth.

    Then for each of those find the max value for the rest of the line.

    Find max of each.
    """
    if depth >= MAX_DEPTH:
        return ""

    if len(line) < (MAX_DEPTH - depth):
        return "-1"

    max_indexes = []
    max_char = -1
    for c in range(len(line) - (MAX_DEPTH - depth - 1)):
        char = int(line[c])
        if char == max_char:
            max_indexes.append(c)
        if char > max_char:
            max_indexes = [c]
            max_char = char

    max_values = []
    for index in max_indexes:
        char = line[index]
        rest = find_max_value(line[index + 1:], depth + 1)
        if rest != "-1":
            value = int(f"{char}{rest}")
            max_values.append(str(value))

    return max(max_values)


# def get_twelve_deep_values(line: str, depth: int = 0) -> list[list[int]]:
#     if len(line) <= 0 or depth == 12:
#         return [[]]

#     values = []
#     for v in get_twelve_deep_values(line[1:], depth + 1):
#         values.append([int(line[0])] + v)

#     for v in get_twelve_deep_values(line[1:], depth):
#         values.append(v)

#     return values

def solve(input_file: str) -> str:
    absolute_sum = 0

    with open(input_file, 'r') as f:
        data = f.read().splitlines()

        for line in data:
            max_value = find_max_value(line)
            print(max_value)
            # continue
            # twelve_deep_values = get_twelve_deep_values(line)
            # twelve_deep_int_values = []

            # for value in twelve_deep_values:
            #     substring = ""
            #     for v in value:
            #         substring += str(v)
            #     if len(substring) > 0:
            #         twelve_deep_int_values.append(int(substring))

            # twelve_deep_int_values.sort()
            # max_value = twelve_deep_int_values[-1]

            # print(max_value)

            absolute_sum += int(max_value)
            print(absolute_sum)

    return str(absolute_sum)

if __name__ == "__main__":
    test_solution = solve("input_test.txt")
    if test_solution != TEST_ANSWER:
        print(f"Test failed: {test_solution} != {TEST_ANSWER}")
        exit(1)

    solution = solve("input.txt")
    print(solution)
