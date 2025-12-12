import random

TEST_ANSWER="24"

def get_area(point: tuple[int, int], other_point: tuple[int, int]) -> int:
    return (abs(point[0] - other_point[0]) + 1) * (abs(point[1] - other_point[1]) + 1)

def get_grid_bounds(red_points: list[tuple[int, int]], green_points: set[tuple[int, int]]) -> tuple[int, int, int, int]:
    max_x = 0
    max_y = 0
    for point in red_points + list(green_points):
        max_x = max(max_x, point[0])
        max_y = max(max_y, point[1])

    return (0, 0, max_x, max_y)

def in_bounds(point: tuple[int, int], grid_bounds: tuple[int, int, int, int]) -> bool:
    return point[0] >= grid_bounds[0] and point[0] <= grid_bounds[2] and point[1] >= grid_bounds[1] and point[1] <= grid_bounds[3]
    
def print_grid(red_points: list[tuple[int, int]], green_points: list[tuple[int, int]]) -> None:
    # find the max x and y coordinates
    max_x = 0
    max_y = 0
    for point in red_points + green_points:
        max_x = max(max_x, point[0])
        max_y = max(max_y, point[1])

    grid = [["." for _ in range(max_x + 2)] for _ in range(max_y + 2)]

    for point in red_points:
        grid[point[1]][point[0]] = "#"
    
    for point in green_points:
        grid[point[1]][point[0]] = "X"

    for row in grid:
        print("".join(row))
    print()

def draw_line(start_point: tuple[int, int], end_point: tuple[int, int]) -> set[tuple[int, int]]: # Not including start and end
    points = set()
    if start_point[0] == end_point[0]:
        x = start_point[0]
        if start_point[1] < end_point[1]:
            y_range = range(start_point[1] + 1, end_point[1])
        else:
            y_range = range(start_point[1] - 1, end_point[1], -1)
        for y in y_range:
            points.add((x, y))
    elif start_point[1] == end_point[1]:
        y = start_point[1]
        if start_point[0] < end_point[0]:
            x_range = range(start_point[0] + 1, end_point[0])
        else:
            x_range = range(start_point[0] - 1, end_point[0], -1)
        for x in x_range:
            points.add((x, y))
    return points

def get_neighbors(point: tuple[int, int]) -> list[tuple[int, int]]:
    return [
        (point[0] + 1, point[1]),
        (point[0] - 1, point[1]),
        (point[0], point[1] + 1),
        (point[0], point[1] - 1),
    ]

def get_starting_point(red_points: list[tuple[int, int]], green_points: set[tuple[int, int]]) -> tuple[int, int]:
    # Get a random_red_point, 
    random_red_point = random.choice(red_points)

    # Take a random diagonal from the red point
    diagonal = random.choice([(1, 1), (1, -1), (-1, 1), (-1, -1)])
    return (random_red_point[0] + diagonal[0], random_red_point[1] + diagonal[1])
    # Get the average of all the points
    # grid_bounds = get_grid_bounds(red_points, green_points)

    # all_points = red_points + list(green_points)
    # n = len(all_points)
    # average_x = int(sum(point[0] for point in all_points) / n)
    # average_y = int(sum(point[1] for point in all_points) / n)

    # # Test the point using the ray casting algorithm
    # # Draw a ray from the point to the grid bounds
    # # Count how many times it hits anything in red_points or green_points
    # # If even , it's outside the grid
    # # If odd, it's inside the grid

    # # Return if it's odd, otherwise, return the first point that is inside the grid
    # count = 0
    # right_after_intersection = False
    # right_after_intersection_points = []
    # for x in range(average_x, grid_bounds[2] + 1):
    #     if (x, average_y) in red_points or (x, average_y) in green_points:
    #         count += 1
    #         right_after_intersection = True
    #     elif right_after_intersection:
    #         right_after_intersection_points.append((x, average_y))
    #         right_after_intersection = False

    # if count % 2 == 0:
    #     return (int(average_x), int(average_y))
    # else:
    #     return right_after_intersection_points[-1]

def fill_grid(red_points: list[tuple[int, int]], green_points: set[tuple[int, int]]) -> set[tuple[int, int]]:
    # If we can find a point that is definitely inside of the grid, then we
    # can simply walk the entire grid

    # Walk the grid, starting from the average point
    start_point = get_starting_point(red_points, green_points)

    print(f"Walking grid from starting point: {start_point}")

    # Walk the grid, starting from the average point
    # Breadth-first search
    queue = [start_point]
    visited = set()

    grid_bounds = get_grid_bounds(red_points, green_points)

    N = 100  # Print every N cycles
    cycles = 0
    green_points_touched = 0
    red_points_touched = 0
    while queue:
        current_point = queue.pop(0)
        visited.add(current_point)
        cycles += 1
        if cycles % N == 0:
            print(f"Queue size after {cycles} steps: {len(queue)} (rt: {red_points_touched}, gt: {green_points_touched})")
        for point in get_neighbors(current_point):
            if not in_bounds(point, grid_bounds):
                raise Exception(f"Point {point} is out of bounds, starting point was outside grid")
            if point in red_points:
                red_points_touched += 1
            elif point in green_points:
                green_points_touched += 1
            elif point not in visited and point not in queue:
                queue.append(point)

    return visited

def contains_only_red_and_green_points(point: tuple[int, int], other_point: tuple[int, int], red_points: list[tuple[int, int]], green_points: set[tuple[int, int]]) -> bool:
    # Draw rectangle, make sure it only contains red and green points
    bounds = get_grid_bounds(red_points, green_points)
    bounds_x = bounds[2]

    min_x = min(point[0], other_point[0])
    max_x = max(point[0], other_point[0])
    min_y = min(point[1], other_point[1])
    max_y = max(point[1], other_point[1])

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            # Skip if the point itself is a red or green point (it's on the boundary)
            if (x, y) in red_points or (x, y) in green_points:
                continue
            
            # Ray casting algorithm to determine if point is inside the polygon
            # Cast a ray to the right (positive x direction) and count edge crossings
            # An edge crossing occurs when we enter the boundary (transition from off to on)
            # (See: https://en.wikipedia.org/wiki/Point_in_polygon)
            count = 0
            on_boundary = False
            for ray_x in range(x + 1, bounds_x + 1):
                is_on_boundary = (ray_x, y) in red_points or (ray_x, y) in green_points
                
                # Count a crossing when we enter the boundary (transition from off to on)
                if not on_boundary and is_on_boundary:
                    count += 1
                
                on_boundary = is_on_boundary

            # If count is even, point is outside; if odd, point is inside
            if count % 2 == 0:
                return False
    return True

def solve(input_file: str) -> str:
    red_points = []
    green_points = set()
    first_point = None
    previous_point = None
    with open(input_file, 'r') as f:
        data = f.read().splitlines()
        for line in data:
            x, y = [int(i) for i in line.split(",")]
            red_points.append((x, y))
            if first_point is None:
                first_point = (x, y)
            else:
                # draw a line from the previous point to the current point
                green_points.update(draw_line(previous_point, (x, y)))

                print(f"Drew line from {previous_point} to {(x, y)}")
                
            previous_point = (x, y)

            # print_grid(red_points, green_points)

    green_points.update(draw_line(previous_point, first_point))

    # print_grid(red_points, green_points)

    # filled_points = fill_grid(red_points, green_points)

    # green_points.update(filled_points)

    # print_grid(red_points, green_points)

    largest_area = 0
    for point in red_points:
        for other_point in red_points:
            if point == other_point:
                continue
            area = get_area(point, other_point)
            if area > largest_area and contains_only_red_and_green_points(point, other_point, red_points, green_points):
                largest_area = area

    return str(largest_area)

if __name__ == "__main__":
    test_solution = solve("input_test.txt")
    if test_solution != TEST_ANSWER:
        print(f"Test failed: {test_solution} != {TEST_ANSWER}")
        exit(1)

    solution = solve("input.txt")
    print(solution)
