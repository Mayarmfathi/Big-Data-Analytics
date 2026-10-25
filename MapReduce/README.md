
# MapReduce Simulation Using Python

## Student Information

- **Name:** Mayar Mohamed Fathi
- **Student ID:** 231006085
- **Course:** Big Data Analytics

## 1. Project Overview

This project implements a simulation of the MapReduce programming model using Python. It demonstrates how a large text-processing task can be divided into smaller tasks, processed in parallel, grouped by key, and combined into final results.

The program performs a Word Count task, calculating how many times each word appears across multiple text files.

## 2. Technologies Used

- Python 3
- Python standard library
- `collections.Counter`
- `concurrent.futures.ProcessPoolExecutor`
- `re`
- `zlib`
- `pathlib`

No external Python packages are required.

## 3. MapReduce Workflow

### Stage 1: Input

The program reads `.txt` files from the `input` directory.

### Stage 2: Map

The mapper reads each file, converts text to lowercase, extracts words, and counts them.

### Stage 3: Combine

A local combiner aggregates repeated words within each input file before the results are sent to the reducers.

### Stage 4: Partition

The partition function assigns each word to one of two reducers using a CRC32-based hash.

### Stage 5: Shuffle and Sort

The program groups counts by word and sorts words alphabetically within each reducer partition.

### Stage 6: Reduce

Each reducer adds the counts for its assigned words and writes the totals to an output file.

## 4. Input Files

### `input/file1.txt`

    apple banana apple

### `input/file2.txt`

    banana orange apple

## 5. Expected Output

The combined word counts are:

| Word | Total Count |
|---|---:|
| apple | 3 |
| banana | 2 |
| orange | 1 |

The output is distributed across two reducer files:

- `output/part-00000.txt`
- `output/part-00001.txt`

Each output line contains a word followed by a tab and its total count.

## 6. How to Run

1. Install Python 3.
2. Make sure the `input` directory contains one or more `.txt` files.
3. Run the program from the project directory:

       python mapreduce.py

4. Check the generated files in the `output` directory.

## 7. Validation

The program was tested using two text files. The execution completed successfully, processed both files, and produced the expected total counts:

- `apple`: 3
- `banana`: 2
- `orange`: 1

The simulation uses two reducers and Python's process pool to perform the mapping stage in parallel.

## 8. Project Structure

    MapReduce/
    ├── mapreduce.py
    ├── README.md
    ├── input/
    │   ├── file1.txt
    │   └── file2.txt
    └── output/
        ├── part-00000.txt
        └── part-00001.txt

The output directory is generated automatically when the program runs.

