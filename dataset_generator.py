import random
import csv
import os

def generate_random_array(size, uniqueRatio, seed, datatype="int"):
    """
    Generate an array of given size with controlled uniqueness.
    - uniqueRatio controls how many distinct values are present.
    - datatype can be 'int' or 'float'.
    - seed ensures reproducibility.
    """
    random.seed(seed)
    uniqueCount = max(1, int(size * uniqueRatio))  # number of distinct values

    # Generate unique pool of values based on datatype
    if datatype == "int":
        uniqueValues = [random.randint(0, 1000) for _ in range(uniqueCount)]
    else:  # float values, rounded to 3 decimals
        uniqueValues = [round(random.uniform(0, 1000), 3) for _ in range(uniqueCount)]

    # Fill the array by randomly choosing from the pool
    return [random.choice(uniqueValues) for _ in range(size)]

def apply_ordering(array, order_type, sortedRatio):
    """
    Apply a partial ordering to the array based on order_type.
    - forward_partial: first portion sorted ascending
    - reverse_partial: first portion sorted descending
    - random: shuffle entire array
    - quarter_partial: one quarter block sorted
    - three_quarter_partial: 3/4 block sorted
    """
    size = len(array)
    sortedCount = max(1, int(size * sortedRatio))  # portion to sort

    if order_type == "forward_partial":
        array[:sortedCount] = sorted(array[:sortedCount])

    elif order_type == "reverse_partial":
        array[:sortedCount] = sorted(array[:sortedCount], reverse=True)

    elif order_type == "random":
        random.shuffle(array)

    elif order_type == "quarter_partial":
        quarter = size // 4
        start = random.choice([0, quarter, 2 * quarter, 3 * quarter])
        array[start:start+quarter] = sorted(array[start:start+quarter])

    elif order_type == "three_quarter_partial":
        three_quarters = (3 * size) // 4
        start = random.randint(0, size - three_quarters)
        array[start:start+three_quarters] = sorted(array[start:start+three_quarters])

    return array

def generate_exponential_datasets(
    num_datasets,
    start_size,
    output_prefix="dataset",
    uniqueRatioRange=(0.1, 1.0),
    sortedRatioRange=(0.1, 1.0),
    datatype="int",
    max_size=16000
):
    """
    Generate datasets with exponentially increasing size (doubling).
    Stops at max_size.
    Writes datasets + metadata into a CSV file.
    """
    # Create unique filename with timestamp to avoid overwriting
    outputFile = f"{output_prefix}_{datatype}.csv"

    # Possible ordering types
    order_types = [
        "forward_partial",
        "reverse_partial",
        "random",
        "quarter_partial",
        "three_quarter_partial"
    ]

    with open(outputFile, mode="w", newline="") as file:
        writer = csv.writer(file)
        # Metadata header row
        writer.writerow([
            "id", "size", "datatype", "uniqueRatio",
            "sortedRatio", "seed", "order_type", "values..."
        ])

        for i in range(num_datasets):
            size = start_size * (2 ** i)  # exponential growth

            if size > max_size:  # continue if above max
                size = 16000

            # Generate random parameters
            seed = random.randint(0, 100)
            uniqueRatio = round(random.uniform(*uniqueRatioRange), 2)
            sortedRatio = round(random.uniform(*sortedRatioRange), 2)
            order_type = random.choice(order_types)

            # Generate array
            array = generate_random_array(size, uniqueRatio, seed, datatype)
            array = apply_ordering(array, order_type, sortedRatio)

            # For floats → ensure string formatting with 3 decimals
            if datatype == "float":
                array = [f"{val:.3f}" for val in array]

            # Write metadata + dataset values
            writer.writerow([
                i + 1,
                size,
                datatype,
                uniqueRatio,
                sortedRatio,
                seed,
                order_type,
                *array
            ])

    print(f"Dataset file created: {outputFile}")

if __name__ == "__main__":
    # doubling size until maximum of 16k
    generate_exponential_datasets(
        num_datasets=15,       # will stop early if size > 16000
        start_size=50, # initial dataset size
        output_prefix="dataset",
        uniqueRatioRange=(0.1, 1.0),
        sortedRatioRange=(0.1, 0.5),
        datatype="int", # can be set to 'float' to get dataset with floating point numbers.
        max_size=16000
    )
