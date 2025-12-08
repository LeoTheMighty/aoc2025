TEST_ANSWER="40"

def print_grid(grid: list[list[str]]):
    for row in grid:
        print("".join(row))

DP_TABLE = {} # "x,y" -> int

def get_timelines(x: int, y: int, grid: list[list[str]]) -> int:
    if (x, y) in DP_TABLE:
        return DP_TABLE[(x, y)]

    if y >= len(grid):
        DP_TABLE[(x, y)] = 1
        return 1
    if x < 0 or x >= len(grid[y]):
        DP_TABLE[(x, y)] = 0
        return 0
    if grid[y][x] == ".":
        DP_TABLE[(x, y)] = get_timelines(x, y + 1, grid)
        return DP_TABLE[(x, y)]
    elif grid[y][x] == "^":
        DP_TABLE[(x, y)] = get_timelines(x - 1, y + 1, grid) + get_timelines(x + 1, y + 1, grid)
        return DP_TABLE[(x, y)]

def solve(input_file: str) -> str:
    grid = []
    with open(input_file, 'r') as f:
        data = f.read().splitlines()
        for line in data:
            row = []
            for char in line:
                row.append(char)
            grid.append(row)

    beams = [] # x values
    next_beams = []

    count = 0

    # find the "S"
    start_x = grid[0].index("S")
    # beams.append(start_x)

    print(f"Starting at {start_x}")

    count = get_timelines(start_x, 1, grid)

    # for y in range(1, len(grid)):
    #     print(f"Processing row {y}")
    #     for beam in beams:
    #         print(f"Processing beam {beam}")
    #         if beam < 0 or beam >= len(grid[y]):
    #             print(f"Beam {beam} is out of bounds")
    #             continue

    #         if grid[y][beam] == ".":
    #             print(f"Beam {beam} is a dot")
    #             next_beams.append(beam)
    #             grid[y][beam] = "|"
    #         elif grid[y][beam] == "^":
    #             print(f"Beam {beam} is a splitter")
    #             next_beams.append(beam + 1)
    #             next_beams.append(beam - 1)
    #             count += 1

    #     beams = next_beams
    #     next_beams = []

    #     print_grid(grid)

    return str(count)

if __name__ == "__main__":
    test_solution = solve("input_test.txt")
    if test_solution != TEST_ANSWER:
        print(f"Test failed: {test_solution} != {TEST_ANSWER}")
        exit(1)

    solution = solve("input.txt")
    print(solution)
