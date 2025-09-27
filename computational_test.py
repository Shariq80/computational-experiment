import csv
import time

def insertion_sort(array):
    """
    Insertion sort implementation.
    Tracks:
    - comparisons: how many times elements are compared
    - shifts: how many moves are performed
    """
    comparisons = 0
    shifts = 0
    for i in range(1, len(array)):
        currentValue = array[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            if array[j] > currentValue:
                array[j+1] = array[j]
                shifts += 1
                j -= 1
            else:
                break
        array[j+1] = currentValue
        shifts += 1
    return comparisons, shifts

def selection_sort(array):
    """
    Selection sort implementation.
    Tracks:
    - comparisons: element comparisons
    - swaps: number of swaps performed
    """
    comparisons = 0
    swaps = 0
    n = len(array)

    for i in range(n-1):
        minIndex = i
        for j in range(i+1, n):
            comparisons += 1
            if array[j] < array[minIndex]:
                minIndex = j
        if minIndex != i:
            array[i], array[minIndex] = array[minIndex], array[i]
            swaps += 1
    return comparisons, swaps

def builtin_sort(array):
    """
    Use Python's built-in Timsort algorithm.
    Only measures timing, not comparisons or operations.
    """
    arrayCopy = array.copy()
    startWall = time.time()
    startCPU = time.process_time()
    sorted(arrayCopy)  # sort using builtin
    endWall = time.time()
    endCPU = time.process_time()
    return {
        'algorithm' : 'builtin_sort',
        'wall_time_ms' : (endWall - startWall) * 1000,
        'cpu_time_ms' : (endCPU - startCPU) * 1000,
        'comparisons' : '',
        'operations' : ''
    }

def time_sort(algorithm, array, name):
    """
    Helper function:
    - Runs the given algorithm
    - Measures wall-clock and CPU time
    - Returns a results dictionary
    """
    arrayCopy = array.copy()
    start_wall = time.time()
    start_cpu = time.process_time()
    comparisons, operations = algorithm(arrayCopy)
    end_wall = time.time()
    end_cpu = time.process_time()

    return {
        'algorithm': name,
        'wall_time_ms': (end_wall - start_wall) * 1000,
        'cpu_time_ms': (end_cpu - start_cpu) * 1000,
        'comparisons': comparisons,
        'operations': operations
    }

def run_tests_to_csv(datasetFile, outputFile, iterations=30, limit=None):
    """
    Main experiment runner.
    - Reads datasets + metadata from CSV
    - Runs sorting algorithms multiple times (default: 30)
    - Records results with metadata into a results CSV
    """
    with open(datasetFile, newline='') as infile, open(outputFile, mode='w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Read header row from dataset file
        dataset_header = next(reader)

        # Write results header (metadata + algorithm results + iteration number)
        writer.writerow([
            *dataset_header[:7],    # first 7 fields are metadata
            "iteration",
            "algorithm",
            "wall_time_ms",
            "cpu_time_ms",
            "comparisons",
            "operations"
        ])

        for i, row in enumerate(reader):
            if limit and i >= limit:
                break

            # Extract dataset metadata
            dataset_id = row[0]
            size = int(row[1])
            datatype = row[2]
            uniqueRatio = row[3]
            sortedRatio = row[4]
            seed = row[5]
            order_type = row[6]
            array = row[7:]  # dataset values

            # Convert dataset values to correct datatype
            if datatype == "int":
                array = list(map(int, array))
            else:
                array = list(map(float, array))

            # Run experiments "iterations" times (default: 30)
            for iteration in range(1, iterations + 1):
                insertionResult = time_sort(insertion_sort, array, 'insertion_sort')
                selectionResult = time_sort(selection_sort, array, 'selection_sort')
                builtinResult = builtin_sort(array)

                # Write results (metadata + iteration + performance metrics)
                for result in [insertionResult, selectionResult, builtinResult]:
                    writer.writerow([
                        dataset_id,
                        size,
                        datatype,
                        uniqueRatio,
                        sortedRatio,
                        seed,
                        order_type,
                        iteration,
                        result['algorithm'],
                        f"{result['wall_time_ms']:.3f}",
                        f"{result['cpu_time_ms']:.3f}",
                        result['comparisons'],
                        result['operations']
                    ])

    print(f"Results written to {outputFile}")

if __name__ == "__main__":
    # Example run: load dataset CSV and write results
    run_tests_to_csv(
        datasetFile="dataset_int.csv",  # sample dataset
        outputFile="test_results.csv",
        iterations=30,  # run each dataset 30 times
        limit=None      # set to limit number of datasets processed
    )
