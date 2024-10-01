#!/bin/bash

# Set the paths to the original and compressed image directories
original_dir="/Users/mattaniah/repos/moon-scraper/downloads/hi_res/0_METADATAAA/solar_eclipse"
compressed_dir="/Users/mattaniah/repos/moon-scraper/downloads/mid_res/solar_eclipse"

if [ -d "$original_dir" ]; then
  if [ ! -d "$compressed_dir" ]; then
    mkdir -p "$compressed_dir"
  fi

  for image_file in "$original_dir"/*.jpg; do
    # Get the image filename
    filename=$(basename "$image_file")

    # Compress the image using ffmpeg and save it to the compressed directory
    ffmpeg -i "$image_file" -vf "scale=iw/2:ih/2" "$compressed_dir/$filename"

    echo "Compressed $filename and saved to $compressed_dir"
  done
else
  echo "Error: Original image directory not found."
fi