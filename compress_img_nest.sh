#!/bin/bash

# Set the paths to the original and compressed image directories
original_dir="/Users/mattaniah/repos/moon-scraper/downloads/reflector_40"
compressed_dir="/Users/mattaniah/repos/moon-scraper/downloads/reflector_40_min"

# Create the compressed directory if it doesn't exist
mkdir -p "$compressed_dir"

# Iterate through each subdirectory in the original directory
for subdir in "$original_dir"/*; do
    # Get the subdirectory name
    subdir_name=$(basename "$subdir")
    
    # Create the corresponding subdirectory in the compressed directory
    mkdir -p "$compressed_dir/$subdir_name"
    
    # Iterate through each image in the subdirectory
    for image_file in "$subdir"/*.jpg; do
        # Get the image filename
        filename=$(basename "$image_file")
        
        # Compress the image using ffmpeg and save it to the compressed directory
        ffmpeg -i "$image_file" -vf "scale=iw/3:ih/3" "$compressed_dir/$subdir_name/$filename"
        
        echo "Compressed $filename"
    done
done

echo "Compression complete."
