
def solve(input_file: str) -> str:
    with open(input_file, 'r') as f:
        data = f.read().splitlines()
        data = f.read()

    return data

if __name__ == "__main__":
    test_answer = ""

    test_solution = solve("input_test.txt")
    if test_solution != test_answer:
        print(f"Test failed: {test_solution} != {test_answer}")
        exit(1)

    solution = solve("input.txt")
    print(solution)