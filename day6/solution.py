TEST_ANSWER="3263827"

def solve(input_file: str) -> str:
    grid = []
    with open(input_file, 'r') as f:
        data = f.read().splitlines()
        for line in data:
            row = []
            # for op in line.split(" "):
            #     if op != "":
            #         row.append(op)
            for char in line:
                row.append(char)

            grid.append(row)

    sum = 0
    last_i = len(grid) - 1
    operator = None
    values = []
    for j in range(len(grid[0])):
        print(f"Processing column {j}")

        new_operator = grid[last_i][j]
        if new_operator != " ":
            # Change operator, add existing
            print(f"Performing operation: {operator} {values}")
            value = 0
            if operator == "*":
                value = 1
                for v in values:
                    value *= v
            elif operator == "+":
                value = 0
                for v in values:
                    value += v
            sum += value

            operator = new_operator
            values = []

        value = 0
        skip = True
        for i in range(last_i):
            if grid[i][j] != " ":
                value = value * 10 + int(grid[i][j])
                skip = False

        if skip:
            continue

        print(f"Value: {value}")
        values.append(value)

    value = 0
    if operator == "*":
        value = 1
        for v in values:
            value *= v
    elif operator == "+":
        value = 0
        for v in values:
            value += v

    sum += value
    return str(sum)

if __name__ == "__main__":
    test_solution = solve("input_test.txt")
    if test_solution != TEST_ANSWER:
        print(f"Test failed: {test_solution} != {TEST_ANSWER}")
        exit(1)

    solution = solve("input.txt")
    print(solution)
