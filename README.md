# Sorting Algorithm Experimentation

This repository contains code and data for experimenting with sorting algorithms on synthetic datasets.  
It consists of two main scripts:

1. **Dataset Generator** (`dataset_generator.py`)  
2. **Experiment Runner** (`computational_test.py`)  

Both scripts are designed to work together to create reproducible datasets, measure algorithm performance, and store results for later analysis.

---

## 1. Dataset Generator (`dataset_generator.py`)

This script generates datasets with controlled characteristics and saves them in a CSV file.  
Each dataset **doubles in size** starting from an initial length until a maximum of **16,000 elements**.

### Features
- Supports two datatypes:
  - **Integers**
  - **Floats** (3 decimal precision)
- Randomized dataset characteristics:
  - `uniqueRatio`: proportion of unique values (controls duplicates)
  - `sortedRatio`: portion of the dataset initially sorted
  - `order_type`: randomly chosen from:
    - Forward partially sorted
    - Reversed partially sorted
    - Totally random
    - One-quarter sorted
    - Three-quarters sorted
- `seed`: random seed used for reproducibility.

### Metadata
Each dataset includes metadata stored in the CSV:
- `id`: dataset identifier  
- `size`: number of elements  
- `datatype`: `int` or `float`  
- `uniqueRatio`: ratio of unique elements  
- `sortedRatio`: portion pre-sorted  
- `seed`: random seed  
- `order_type`: sorting profile used  
- `iteration`: trial index (1–30)

### Example Usage
```bash
python dataset_generator.py
```
This creates a CSV file named like `dataset_int.csv` or `dataset_float.csv` depending on the chosen datatype.
## 2. Experiment Runner (`computational_test.py`)
This script loads the generated datasets and runs multiple sorting algorithms on them, collecting performance results.

### Algorithms Tested

 - insertion_sort
 - selection_sort
 - builtin_sort (Python’s built-in Timsort)

### Measurements

Each run records:

 - `algorithm`: name of algorithm

 - `wall_time_ms`: wall-clock execution time in ms

 - `cpu_time_ms`: CPU processing time in ms

 - `comparisons`: number of comparisons (if applicable)

 - `operations`: shifts/swaps performed (if applicable)

Each dataset is tested 30 times to reduce randomness and improve reliability.
The `iteration` field (1–30) tracks which trial the result corresponds to.

### Example usage
```bash
python computational_test.py --dataset dataset_int.csv --output test_results.csv
```
This produces a CSV with raw experimental results. Each row contains both dataset metadata and algorithm performance.

## 3. Outputs

 1. Dataset CSVs (from `dataset_generator.py`): contain generated values + metadata fields
 ```csv
 id, size, datatype, uniquieRatio, sortedRatio, seed, order_type, values
 1,50,int,0.85,0.41,43,three_quarter_partial,59,687,560,98, ...
 ...
 ```
 2. Results CSVs (from `computational_test.py`): contain experiment results with both performance metrics and dataset metadata.
 ```csv
 id, size, datatype, uniquieRatio, sortedRatio, seed, order_type, iteration, algorithm, wall_time_ms, cpu_time_ms, comparisonsm, operations
 1,50,int,0.85,0.41,43,three_quarter_partial,1,insertion_sort,0.025,0.000,292,292
 1,50,int,0.85,0.41,43,three_quarter_partial,1,selection_sort,0.041,0.000,1225,41
 1,50,int,0.85,0.41,43,three_quarter_partial,1,builtin_sort,0.003,0.000,,
 ...
 ```

## 4. Reproducibility
 - All datasets are generated with a stored `seed`, ensuring exact regeneration is possible.
 - Metadata provides full context for every measurement.
 - Running experiments multiple times accounts for system-level noise and improves measurement quality.

 ## 5. Repository Contents
 - `dataset_generator.py` → dataset generator
 - `computational_test.py` → experiment runner
 - `sample_data/` → example datasets generated
 - `test_results/` → example results of the generated datasets
 - `README.md` → documentation
