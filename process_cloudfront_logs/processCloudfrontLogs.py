"""
Instructions:

1. Download cloudfront log file from s3 bucket.

2. Update configuration by what you want, and run the script to get the information you want to get.

"""

from collections import Counter

with open("E17CAU8HV36SK8.2024-08-13-18.f95ce855", "r") as file:
    lines = file.readlines()


locations = [line.split()[10] for line in lines]

host_lines = [
    line
    for line in lines
    # choose the field you want to filter
    if line.split()[10] == "Pimsleur/144%20CFNetwork/1496.0.7%20Darwin/23.5.0"
]

# choose the field you want to count
temp = [line.split()[4] for line in host_lines]

location_counts = Counter(temp)
sorted_location_counts = sorted(
    location_counts.items(), key=lambda x: x[1], reverse=False
)

for location, count in sorted_location_counts:
    print(f"{location}: {count}")
