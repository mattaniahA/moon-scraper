#!/bin/bash

src_dir="/Users/mattaniah/repos/moon-scraper/downloads/chart_plates"
dest_dir="/Users/mattaniah/repos/moon-scraper/downloads/chart_plates2"
suffix="_P1"

# Create the destination directory if it doesn't exist
mkdir -p "$dest_dir"

# Find images with the specified suffix in the source directory and copy them to the destination directory
find "$src_dir" -type f -name "*$suffix.jpg" -exec cp {} "$dest_dir" \;

echo "Images with suffix '$suffix' copied to '$dest_dir'"