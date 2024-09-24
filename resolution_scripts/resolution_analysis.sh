#!/bin/bash

# Specify the directory containing the images
IMAGE_DIR="/Users/mattaniah/repos/moon-scraper/downloads/hi_res/blueprints"

# Change directory to the specified image directory
cd "$IMAGE_DIR" || exit

# Initialize variables for min, max, median, and total resolution
min_resolution=""
max_resolution=""
total_resolution=0
resolution_array=()

# Iterate over each image file in the directory
for file in *.{jpg,jpeg,png,gif}; do
    # Get the resolution of the image using ImageMagick's identify command
    resolution=$(identify -format "%w %h" "$file")

    # Extract width and height from the resolution string
    width=$(echo "$resolution" | cut -d ' ' -f 1)
    height=$(echo "$resolution" | cut -d ' ' -f 2)

    total_resolution=$((total_resolution + width * height))

    # Store the resolution in the array
    resolution_array+=("$width $height")
done

sorted_resolution_array=($(echo "${resolution_array[@]}" | tr ' ' '\n' | sort -n))

min_resolution=$(echo "${sorted_resolution_array[0]}")
max_resolution=$(echo "${sorted_resolution_array[-1]}")
median_index=$(((${#sorted_resolution_array[@]} + 1) / 2 - 1))
median_resolution=$(echo "${sorted_resolution_array[$median_index]}")
average_resolution=$((total_resolution / ${#resolution_array[@]}))

# Print the results
echo "Minimum Resolution: $min_resolution"
echo "Maximum Resolution: $max_resolution"
echo "Median Resolution: $median_resolution"
echo "Average Resolution: $average_resolution"
