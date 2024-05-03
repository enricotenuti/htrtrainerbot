import csv
import sys


csv.field_size_limit(sys.maxsize)
# Define the input and output file names
input_file = "out.csv"
output_file = "filtered.csv"

# Open the input file for reading and the output file for writing
with open(input_file, 'r', newline='') as input_csvfile, open(output_file, 'w', newline='') as output_csvfile:
    reader = csv.reader(input_csvfile)
    writer = csv.writer(output_csvfile)

    # Write the header row (if your CSV has one)
    header = next(reader)
    writer.writerow(header)

    # Iterate through the rows in the input CSV file and filter based on the third element
    for row in reader:
        if int(row[2]) <= 7:
            writer.writerow(row)

print("Filtered data has been written to", output_file)
