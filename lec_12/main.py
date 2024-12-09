import random
import time

def timer(func):
    def wrapped(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapped

@timer
def create_file(name):
    with open(name, "w") as file:
        for _ in range(100):
            nums = [str(random.randint(1, 100)) for _ in range(20)]
            file.write(" ".join(nums) + "\n")

@timer
def read_file(name):
    with open(name, "r") as file:
        return [list(map(int, line.split())) for line in file]

@timer
def filter_data(data):
    return [list(filter(lambda n: n > 40, line)) for line in data]

@timer
def write_file(name, data):
    with open(name, "w") as file:
        for line in data:
            file.write(" ".join(map(str, line)) + "\n")

def file_generator(name):
    with open(name, "r") as file:
        for line in file:
            yield list(map(int, line.split()))

if __name__ == "__main__":
    input_file = "input.txt"
    output_file = "output.txt"

    create_file(input_file)
    lines = read_file(input_file)
    filtered = filter_data(lines)
    write_file(output_file, filtered)

    print("\nFile read with generator:")
    for line in file_generator(output_file):
        print(line)
