import csv

file1 = "new.csv"
file2 = "test.csv"

# Read first file
with open(file1, 'r', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    data1 = set(row[0].strip() for row in reader if row)

# Read second file
with open(file2, 'r', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    data2 = set(row[0].strip() for row in reader if row)

# Get unique values (not common in both)
unique_data = data1.symmetric_difference(data2)

print("Unique values:")
for item in unique_data:
    print(item)