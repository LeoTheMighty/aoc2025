import math

TEST_ANSWER="25272"

class JunctionBox:
    def __init__(self, id: int, x: int, y: int, z: int):
        self.id = id
        self.x = x
        self.y = y
        self.z = z

        self.neighbors = []

        self.circuit = None

    def set_circuit(self, circuit: "JunctionBoxCircuit"):
        self.circuit = circuit

    def get_distance(self, other: "JunctionBox") -> int:
        return math.sqrt(
            (self.x - other.x) ** 2 +
            (self.y - other.y) ** 2 +
            (self.z - other.z) ** 2
        )

    def __repr__(self) -> str:
        return f"[{self.x}, {self.y}, {self.z}]"

class JunctionBoxCircuit:
    def __init__(self, box: JunctionBox):
        self.boxes = [box]

    def merge_circuit(self, other: "JunctionBoxCircuit"):
        self.boxes.extend(other.boxes)

    def __repr__(self) -> str:
        return f"(boxes={self.boxes})"

def get_group(box_id: int, visited_ids: set[int], junction_boxes: dict[int, JunctionBox]) -> list[int]:
    if box_id in visited_ids:
        return []

    visited_ids.add(box_id)
    group = [box_id]
    box = junction_boxes[box_id]
    for neighbor_id in box.neighbors:
        group += get_group(neighbor_id, visited_ids, junction_boxes)
    return group

def boxes_are_connected(box_one_id: int, box_two_id: int, visited_ids: set[int], junction_boxes: dict[int, JunctionBox]) -> bool:
    if box_two_id in visited_ids:
        return False

    visited_ids.add(box_two_id)

    box_two = junction_boxes[box_two_id]
    if box_one_id in box_two.neighbors:
        return True

    for neighbor_id in box_two.neighbors:
        if boxes_are_connected(box_one_id, neighbor_id, visited_ids, junction_boxes):
            return True

    return False

def solve(input_file: str) -> str:
    junction_boxes = {} # id -> JunctionBox
    with open(input_file, 'r') as f:
        data = f.read().splitlines()

        for i, line in enumerate(data):
            x, y, z = [int(i) for i in line.split(",")]
            junction_box = JunctionBox(i, x, y, z)
            junction_boxes[junction_box.id] = junction_box
            # junction_boxes.append(JunctionBox(x, y, z))

    circuits = []
    for box in junction_boxes.values():
        circuit = JunctionBoxCircuit(box)
        circuits.append(circuit)
        box.set_circuit(circuit)

    print(junction_boxes)

    num_times_to_connect = 0
    if len(junction_boxes) == 20:
        num_times_to_connect = 10
    elif len(junction_boxes) == 1000:
        num_times_to_connect = 1000

    # Connect the closest boxes together

    # for i in range(num_times_to_connect):
    last_two_boxes = []
    while len(circuits) > 1:
        min_distance = float('inf')
        box_one = None
        box_two = None
        for box_id, box in junction_boxes.items():
            for other_box_id, other_box in junction_boxes.items():
                if box_id == other_box_id:
                    continue

                distance = box.get_distance(other_box)
                if distance < min_distance and box.id not in other_box.neighbors and other_box.id not in box.neighbors:
                    min_distance = distance
                    box_one = box
                    box_two = other_box

        if box_one is not None and box_two is not None and box_one.circuit != box_two.circuit:
            print(f"{i}: Connecting {box_one} to {box_two}")
            box_one.circuit.merge_circuit(box_two.circuit)
            # print(f"Merged {box_one.circuit} and {box_two.circuit}")
            try:
                circuits.remove(box_two.circuit)
            except ValueError:
                print(f"Circuit {box_two.circuit} not found")
            for box in box_two.circuit.boxes:
                box.set_circuit(box_one.circuit)
            box_two.set_circuit(box_one.circuit)
            last_two_boxes = [box_one, box_two]
        else:
            print(f"Doing nothing: {box_one} and {box_two}")

        box_one.neighbors.append(box_two.id)
        box_two.neighbors.append(box_one.id)

        # print("Circuits:")
        # for circuit in circuits:
        #     print(circuit)

    return str(last_two_boxes[0].x * last_two_boxes[1].x)


    # print(junction_boxes)
            
    # Find the groups of boxes that are all connected together 
    # visited_ids = set() # ids
    # groups = []  # keep sorted by size
    # for box_id, box in junction_boxes.items():
    #     if box_id in visited_ids:
    #         continue

    #     group = get_group(box_id, visited_ids, junction_boxes)
    #     groups.append(group)

    # Sort the groups by the number of boxes in each group
    # circuits.sort(key=lambda x: len(x.boxes), reverse=True)
    # groups.sort(key=len, reverse=True)

    # print("Circuits:")
    # for circuit in circuits:
        # print(circuit)

    # Return the multiplication of the top 3 sizes in that list 
    # return str(len(circuits[0].boxes) * len(circuits[1].boxes) * len(circuits[2].boxes))

    # return data

if __name__ == "__main__":
    test_solution = solve("input_test.txt")
    if test_solution != TEST_ANSWER:
        print(f"Test failed: {test_solution} != {TEST_ANSWER}")
        exit(1)

    solution = solve("input.txt")
    print(solution)
