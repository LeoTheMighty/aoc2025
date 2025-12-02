import math

current = 50
count = 0

with open('input.txt', 'r') as f:
    data = f.read().splitlines()

    for line in data:
        passed_by_zeros = 0
        if line.startswith('R'):
            parsed = int(line[1:])
            # for i in range(parsed):
            #     current += 1
            #     current = current % 100
            #     if current == 0:
            #         count += 1
            passed_by_zeros = math.floor((parsed + current) / 100)
            current = (current + parsed) % 100
        elif line.startswith('L'):
            parsed = int(line[1:])
            # for i in range(parsed):
            #     current -= 1
            #     current = current % 100
            #     if current == 0:
            #         count += 1
            passed_by_zeros = abs(math.floor((current - parsed) / 100))
            current = (current - parsed) % 100


        print(current)
        if passed_by_zeros > 0:
            print(f"PASSED by {passed_by_zeros}")

        count += passed_by_zeros
        if current == 0:
            count += 1

print(count)

