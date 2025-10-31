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

    name=$(basename "$f")
    name_noext="${name%.*}"

    # Extract region pattern (e.g. chr6_region_711055-761032_hap1)
    region=$(echo "$name_noext" | grep -oE 'chr[0-9XYM]+_region_[0-9]+-[0-9]+_hap[0-9]+')

    # Extract sample name (everything before region)
    sample=$(echo "$name_noext" | sed "s/_${region}//")

    # Construct clean header
    echo ">${sample}_${region}" >> "$output"

    # Append sequence without header
    grep -v "^>" "$f" >> "$output"
done

echo "✅ Merged FASTA written to: ${output}"