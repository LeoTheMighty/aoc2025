TEST_ANSWER="14"

def add_range_to_sorted_list(sorted_list, ids):
    for i in range(len(sorted_list)):
        if ids[1] < sorted_list[i][0]:
            sorted_list.insert(i, ids)
            return
        elif ids[0] <= sorted_list[i][1] + 1:
            # We can merge the ranges (overlapping or adjacent)
            new_range = (min(ids[0], sorted_list[i][0]), max(ids[1], sorted_list[i][1]))

            # Remove the existing range
            sorted_list.pop(i)

            # Might have to check the new range against the new list, so recurse
            return add_range_to_sorted_list(sorted_list, new_range)
    
    sorted_list.append(ids)

def solve(input_file: str) -> str:
    with open(input_file, 'r') as f:
        data = f.read().splitlines()

        count = 0
        fresh_ingredient_ranges = []
        fresh_ingredient_id_section = True
        for line in data:
            if line == "":
                fresh_ingredient_id_section = False
                continue

            if fresh_ingredient_id_section:
                begin, end = line.split("-")
                begin = int(begin)
                end = int(end)

                # Run compaction
                add_range_to_sorted_list(fresh_ingredient_ranges, (begin, end))
            # else:
            #     ingredient = int(line)

            #     for range in fresh_ingredient_ranges:
            #         if ingredient >= range[0] and ingredient <= range[1]:
            #             print(f"Ingredient {ingredient} is in range {range}")
            #             count += 1
            #             break

    count = 0
    for ids in fresh_ingredient_ranges:
        count += (ids[1] - ids[0] + 1)

    print(fresh_ingredient_ranges)

    return str(count)

if __name__ == "__main__":
    test_solution = solve("input_test.txt")
    if test_solution != TEST_ANSWER:
        print(f"Test failed: {test_solution} != {TEST_ANSWER}")
        exit(1)

    solution = solve("input.txt")
    print(solution)
