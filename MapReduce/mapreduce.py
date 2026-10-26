
from pathlib import Path
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor
import re
import zlib

# Configuration
BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"
NUM_REDUCERS = 2


# Stage 1: Map each input file
def mapper(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read().lower()

    # Extract words and numbers, ignoring punctuation
    words = re.findall(r"\b\w+\b", text)

    # Stage 2: Combine repeated words locally
    local_counts = Counter(words)

    return list(local_counts.items())


# Stage 3: Partition words between reducers
def partition(word):
    return zlib.crc32(word.encode("utf-8")) % NUM_REDUCERS


# Main function
def main():
    # Check the input directory
    if not INPUT_DIR.exists():
        print("Error: Create an 'input' folder with text files.")
        return

    # Find all text files
    files = sorted(
        path for path in INPUT_DIR.iterdir()
        if path.is_file() and path.suffix.lower() == ".txt"
    )

    if not files:
        print("Error: No .txt files found in the input folder.")
        return

    print(f"Found {len(files)} input files:")
    for path in files:
        print(f"- {path.name}")

    # Stage 4: Map files in parallel
    with ProcessPoolExecutor() as executor:
        mapped_results = list(executor.map(mapper, files))

    print("\nMapping and combining completed!")

    # Stage 5: Shuffle and group words by reducer
    partitions = [defaultdict(list) for _ in range(NUM_REDUCERS)]

    for mapper_result in mapped_results:
        for word, count in mapper_result:
            reducer_id = partition(word)
            partitions[reducer_id][word].append(count)

    # Stage 6: Sort words inside each partition
    shuffled = []

    for partition_data in partitions:
        sorted_data = {
            word: partition_data[word]
            for word in sorted(partition_data)
        }
        shuffled.append(sorted_data)

    # Stage 7: Reduce and write output files
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for reducer_id, reducer_data in enumerate(shuffled):
        output_file = OUTPUT_DIR / f"part-{reducer_id:05d}.txt"

        with open(output_file, "w", encoding="utf-8") as file:
            for word, values in reducer_data.items():
                total = sum(values)
                file.write(f"{word}\t{total}\n")

    print("\nMapReduce completed successfully!")
    print(f"Input files processed: {len(files)}")
    print(f"Reducers used: {NUM_REDUCERS}")
    print(f"Unique words counted: {sum(len(p) for p in shuffled)}")
    print(f"Output directory: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
