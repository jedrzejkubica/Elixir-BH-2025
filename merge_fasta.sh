#!/bin/bash

if [ $# -lt 2 ]; then
    echo "Usage: $0 <input_directory> <output_file>"
    exit 1
fi

input_dir="$1"
output="$2"

# Check directory exists
if [ ! -d "$input_dir" ]; then
    echo "Error: directory '$input_dir' does not exist."
    exit 1
fi

output_abs=$(realpath "$output")
> "$output"

for f in "$input_dir"/*.fasta "$input_dir"/*.fa; do
    [ -e "$f" ] || continue

    f_abs=$(realpath "$f")
    if [ "$f_abs" = "$output_abs" ]; then
        continue
    fi

    # Remove extension
    name_noext=$(basename "$f" | sed 's/\.[^.]*$//')

    # Extract sample name and region from filename
    # Assumes filename format: sample_chrX_region_start-end_hapN
    # e.g., NA18531_chr6_region_711055-761032_hap1
    header=$(echo "$name_noext" | grep -oE '[^_]+_chr[0-9XYM]+_region_[0-9]+-[0-9]+_hap[0-9]+')

    # Fallback: if grep fails, use the whole filename
    [ -z "$header" ] && header="$name_noext"

    echo ">$header" >> "$output"
    grep -v "^>" "$f" >> "$output"
done

echo "✅ Merged FASTA written to: ${output}"