TEST_ANSWER="43"

def get_neighbors(grid: list[list[str]], i: int, j: int) -> list[str]:
    neighbors = []
    for x in [-1, 0, 1]:
        for y in [-1, 0, 1]:
            new_i = i + x
            new_j = j + y
            if new_i < 0 or new_i >= len(grid) or new_j < 0 or new_j >= len(grid[new_i]):
                continue
            if new_i == i and new_j == j:
                continue
            neighbors.append(grid[new_i][new_j])

    return neighbors

def solve(input_file: str) -> str:
    grid = []
    with open(input_file, 'r') as f:
        data = f.read().splitlines()
        for line in data:
            row = []
            for char in line:
                row.append(char)
            grid.append(row)

    print(grid)

    count = -1
    full_count = 0

    while count != 0:
        next_grid = [row[:] for row in grid] # deep copy

        count = 0
        # count how many '@' have < 4 '@' neighbors
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == '@':
                    neighbors = get_neighbors(grid, i, j)
                    if neighbors.count('@') < 4:
                        count += 1
                        full_count += 1
                        next_grid[i][j] = '.'

        grid = next_grid

    return str(full_count)

if __name__ == "__main__":
    test_solution = solve("input_test.txt")
    if test_solution != TEST_ANSWER:
        print(f"Test failed: {test_solution} != {TEST_ANSWER}")
        exit(1)

    solution = solve("input.txt")
    print(solution)
