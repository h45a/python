import threading
import multiprocessing
import time
from collections import defaultdict

def count_words_in_chunk(text):
    word_count = defaultdict(int)
    for word in text.split():
        word_count[word] += 1
    return word_count

def count_words_sequential(filename):
    with open(filename, 'r') as file:
        text = file.read()
    return count_words_in_chunk(text)

def count_words_multithreaded(filename, num_threads):
    with open(filename, 'r') as file:
        lines = file.readlines()

    chunk_size = len(lines) // num_threads
    word_counts = [defaultdict(int) for _ in range(num_threads)]
    threads = []

    def worker(start, end, idx):
        chunk_text = ''.join(lines[start:end])
        word_counts[idx] = count_words_in_chunk(chunk_text)

    for i in range(num_threads):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i < num_threads - 1 else len(lines)
        thread = threading.Thread(target=worker, args=(start, end, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    final_count = defaultdict(int)
    for wc in word_counts:
        for word, count in wc.items():
            final_count[word] += count
    return final_count

def count_words_multiprocessing(filename, num_processes):
    with open(filename, 'r') as file:
        lines = file.readlines()

    chunk_size = len(lines) // num_processes
    processes = []
    word_counts = multiprocessing.Manager().list([defaultdict(int) for _ in range(num_processes)])

    def worker(start, end, idx):
        chunk_text = ''.join(lines[start:end])
        word_counts[idx] = count_words_in_chunk(chunk_text)

    for i in range(num_processes):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i < num_processes - 1 else len(lines)
        process = multiprocessing.Process(target=worker, args=(start, end, i))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    final_count = defaultdict(int)
    for wc in word_counts:
        for word, count in wc.items():
            final_count[word] += count
    return final_count

def compare_performance(filename, num_threads, num_processes):
    start_time = time.time()
    seq_count = count_words_sequential(filename)
    seq_time = time.time() - start_time
    print(f"Sequential time: {seq_time:.4f} seconds")

    start_time = time.time()
    mt_count = count_words_multithreaded(filename, num_threads)
    mt_time = time.time() - start_time
    print(f"Multithreading time ({num_threads} threads): {mt_time:.4f} seconds")

    start_time = time.time()
    mp_count = count_words_multiprocessing(filename, num_processes)
    mp_time = time.time() - start_time
    print(f"Multiprocessing time ({num_processes} processes): {mp_time:.4f} seconds")

    print("\nSpeedup Comparison:")
    print(f"Speedup (multithreading): {seq_time / mt_time:.2f}")
    print(f"Speedup (multiprocessing): {seq_time / mp_time:.2f}")

    return seq_time, mt_time, mp_time

def create_large_text_file(filename, num_lines=100000, line_length=10):
    import random
    import string
    with open(filename, 'w') as file:
        for _ in range(num_lines):
            line = ' '.join([''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 8))) for _ in range(line_length)])
            file.write(line + '\n')

if __name__ == "__main__":
    filename = "large_text_file.txt"
    create_large_text_file(filename)

    num_threads = 4
    num_processes = 4
    seq_time, mt_time, mp_time = compare_performance(filename, num_threads, num_processes)
