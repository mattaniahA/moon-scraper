#!/bin/bash

# Set the path to your original image directory
original_image_dir="/Users/mattaniah/repos/moon-scraper/downloads/solar_eclipse"

# Set the path to the new compressed image directory
compressed_image_dir="/Users/mattaniah/repos/moon-scraper/downloads/solar_eclipse_min"

# Check if the original directory exists
if [ -d "$original_image_dir" ]; then
  # Check if the compressed directory exists, create if not
  if [ ! -d "$compressed_image_dir" ]; then
    mkdir -p "$compressed_image_dir"
  fi

  # Iterate through each image in the original directory
  for image_file in "$original_image_dir"/*.jpg; do
    # Get the filename without extension
    filename=$(basename -- "$image_file")
    filename_noext="${filename%.*}"

    # Compress the image using ffmpeg and save it to the compressed directory
    ffmpeg -i "$image_file" -vf "scale=iw/3:ih/3" "$compressed_image_dir/${filename_noext}.jpg"

    echo "Compressed $filename and saved to $compressed_image_dir"
  done
else
  echo "Error: Original image directory not found."
fi