TEST_ANSWER="2"

class Node:
    def __init__(self, name: str, neighbors: list[str]):
        self.name = name
        self.neighbors = neighbors

def solve(input_file: str) -> str:
    nodes = {}
    with open(input_file, 'r') as f:
        data = f.read().splitlines()
        for line in data:
            parts = line.split(":")
            if len(parts) > 0:
                name = parts[0].strip()
                parts = parts[1].split(" ")
                neighbors = []
                for part in parts:
                    if part != "":
                        neighbors.append(part.strip())
                node = Node(name, neighbors)
                nodes[name] = node

    out_node = Node("out", [])
    nodes["out"] = out_node

    dp_table = {}
    def count_paths(node_name: str, has_fft: bool, has_dac: bool, path: set) -> int:
        if node_name in path:
            return 0
        
        has_fft = has_fft or (node_name == "fft")
        has_dac = has_dac or (node_name == "dac")

        state = (node_name, has_fft, has_dac)
        
        if node_name == "out":
            return 1 if (has_fft and has_dac) else 0
        
        if (node_name, has_fft, has_dac) in dp_table:
            return dp_table[(node_name, has_fft, has_dac)]
        
        path.add(node_name)
        total = 0
        for neighbor in nodes[node_name].neighbors:
            total += count_paths(neighbor, has_fft, has_dac, path)
        path.remove(node_name)
        
        dp_table[state] = total
        return total
    
    total_paths = count_paths("svr", False, False, set())

    return str(total_paths)

if __name__ == "__main__":
    test_solution = solve("input_test.txt")
    if test_solution != TEST_ANSWER:
        print(f"Test failed: {test_solution} != {TEST_ANSWER}")
        exit(1)

    solution = solve("input.txt")
    print(solution)
