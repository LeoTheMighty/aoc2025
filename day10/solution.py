import heapq

TEST_ANSWER="33"

class Machine:
    def __init__(
        self,
        desired_lights: str,
        buttons: list[list[int]],
        joltage_requirements: list[int]
    ):
        self.desired_lights = desired_lights
        # All start turned off
        self.indicator_lights = '.' * len(desired_lights)
        self.buttons = buttons
        self.joltage_requirements = joltage_requirements
        self.joltage_state = [0] * len(joltage_requirements)

    def find_shortest_presses_to_start(self, state: list[str] = None) -> int:
        if state is None:
            state = self.indicator_lights

        queue = [(state, 0)]
        visited = set()
        while queue:
            current_state, presses = queue.pop(0)
            if current_state in visited:
                continue

            visited.add(current_state)
            if current_state == self.desired_lights:
                return presses

            for button in self.buttons:
                new_state = list(current_state)
                for index in button:
                    # Toggle the light
                    if new_state[index] == ".":
                        new_state[index] = "#"
                    else:
                        new_state[index] = "."

                queue.append((''.join(new_state), presses + 1))

        return -1

    def _heuristic(self, state: list[int]) -> int:
        """Calculate heuristic: sum of absolute differences from goal state."""
        return sum(abs(state[i] - self.joltage_requirements[i]) 
                   for i in range(len(state)))
    
    def _can_reach_goal(self, state: list[int]) -> bool:
        """Check if it's theoretically possible to reach goal from this state."""
        # Check if any position is already too high
        for i in range(len(state)):
            if state[i] > self.joltage_requirements[i]:
                return False
        return True

    def _reverse_heuristic(self, state: list[int]) -> int:
        """Heuristic for backward search: distance from start state."""
        return sum(state[i] for i in range(len(state)))

    def shortest_presses_to_joltage(self, state: list[str] = None) -> int:
        if state is None:
            state = self.joltage_state

        # Early goal check
        if state == self.joltage_requirements:
            return 0

        # Bidirectional search: forward from start, backward from goal
        forward_dp = {}
        backward_dp = {}
        
        # Forward queue: from start state toward goal
        forward_heuristic = self._heuristic(state)
        forward_queue = [(forward_heuristic, 0, state)]
        
        # Backward queue: from goal state toward start (working backwards)
        backward_heuristic = self._reverse_heuristic(self.joltage_requirements)
        backward_queue = [(backward_heuristic, 0, self.joltage_requirements)]
        
        # bidirectional search, do dijkstra's algorithm from the start and the goal, find intersections
        while forward_queue or backward_queue:
            if forward_queue:
                _, presses, current_state = heapq.heappop(forward_queue)
                state_tuple = tuple(current_state)
                
                # Check if backward search has seen this state
                if state_tuple in backward_dp:
                    return presses + backward_dp[state_tuple]
                
                # Check if we've already found a better path
                if state_tuple not in forward_dp or forward_dp[state_tuple] > presses:
                    forward_dp[state_tuple] = presses
                    
                    if current_state == self.joltage_requirements:
                        return presses
                    
                    # Dead-end detection
                    if self._can_reach_goal(current_state):
                        # Expand forward
                        for button in self.buttons:
                            new_state = list(current_state)
                            valid = True
                            for index in button:
                                new_state[index] += 1
                                if new_state[index] > self.joltage_requirements[index]:
                                    valid = False
                                    break
                            
                            if valid:
                                new_state_tuple = tuple(new_state)
                                new_presses = presses + 1
                                if new_state_tuple not in forward_dp or forward_dp[new_state_tuple] > new_presses:
                                    priority = new_presses + self._heuristic(new_state)
                                    heapq.heappush(forward_queue, (priority, new_presses, new_state))
            
            if backward_queue:
                _, presses, current_state = heapq.heappop(backward_queue)
                state_tuple = tuple(current_state)
                
                # Check if forward search has seen this state
                if state_tuple in forward_dp:
                    return forward_dp[state_tuple] + presses
                
                # Check if we've already found a better path
                if state_tuple not in backward_dp or backward_dp[state_tuple] > presses:
                    backward_dp[state_tuple] = presses
                    
                    # Early start check
                    if current_state == state:
                        return presses
                    
                    # Expand backward: find predecessor states
                    # A predecessor is a state where pressing a button leads to current_state
                    for button in self.buttons:
                        # Check if this button could have been pressed to reach current_state
                        predecessor = list(current_state)
                        valid = True
                        for index in button:
                            if predecessor[index] == 0:
                                # Can't go backward from 0
                                valid = False
                                break
                            predecessor[index] -= 1
                        
                        if valid:
                            # Check if predecessor is valid (all values >= 0 and <= requirements)
                            for i in range(len(predecessor)):
                                if predecessor[i] < 0 or predecessor[i] > self.joltage_requirements[i]:
                                    valid = False
                                    break
                            
                            if valid:
                                pred_tuple = tuple(predecessor)
                                new_presses = presses + 1
                                if pred_tuple not in backward_dp or backward_dp[pred_tuple] > new_presses:
                                    priority = new_presses + self._reverse_heuristic(predecessor)
                                    heapq.heappush(backward_queue, (priority, new_presses, predecessor))

        return -1

def solve(input_file: str) -> str:
    machines = []
    with open(input_file, 'r') as f:
        data = f.read().splitlines()
        for line in data:
            parts = line.split(" ")
            if len(parts) > 0:
                desired_lights = parts[0][1:-1]
                buttons = []
                for part in parts[1:-1]:
                    button = [int(i) for i in part[1:-1].split(",")]
                    buttons.append(button)
                joltage_requirements = [int(i) for i in parts[-1][1:-1].split(",")]
                machine = Machine(desired_lights, buttons, joltage_requirements)
                machines.append(machine)

    count = 0
    for i, machine in enumerate(machines):
        # count += machine.find_shortest_presses_to_start()
        shortest_presses = machine.shortest_presses_to_joltage()
        print(f"{i} / {len(machines)}: Shortest presses to joltage: {shortest_presses}")
        count += shortest_presses

    return str(count)

if __name__ == "__main__":
    test_solution = solve("input_test.txt")
    if test_solution != TEST_ANSWER:
        print(f"Test failed: {test_solution} != {TEST_ANSWER}")
        exit(1)

    solution = solve("input.txt")
    print(solution)
