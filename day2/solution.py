def is_repeating(string_id) -> bool:
    """
    Checks if a string is a repeating pattern.

    11 => True
    112 => False
    1212 => True
    1231234 => False
    """
    # For each substring 
    for i in range(1, len(string_id)):
        substring = string_id[:i]
        print(f"Checking {substring} in {string_id}")
        if repeats_with(string_id, substring):
            return True
    return False

def repeats_with(string_id, substring) -> bool:
    if string_id == substring:
        return True
    if not string_id.startswith(substring):
        return False
    return repeats_with(string_id[len(substring):], substring)

sum = 0
with open('input.txt', 'r') as f:
    data = f.read().split(',')

    for ids in data:
        parts = ids.split('-')
        lower = int(parts[0])
        upper = int(parts[1])

        for i in range(lower, upper + 1):
            string_id = str(i)

            halfway_index = len(string_id) // 2

            if is_repeating(string_id):
                print(f"INVALID: {string_id}")
                sum += i

print(sum)
