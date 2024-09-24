#!/bin/bash

# Set the paths to the original and compressed image directories
original_dir="/Users/mattaniah/repos/moon-scraper/downloads/hi_res/reflector_40"
compressed_dir="/Users/mattaniah/repos/moon-scraper/downloads/lo_res/reflector_40"

mkdir -p "$compressed_dir"

for subdir in "$original_dir"/*; do
    # Create the corresponding subdirectory in the compressed directory
    subdir_name=$(basename "$subdir")
    mkdir -p "$compressed_dir/$subdir_name"
    
    for image_file in "$subdir"/*.jpg; do
        # Get the image filename
        filename=$(basename "$image_file")
        
        # Compress the image using ffmpeg and save it to the compressed directory
        ffmpeg -i "$image_file" -vf "scale=iw/3:ih/3" "$compressed_dir/$subdir_name/$filename"
        
        echo "Compressed $filename"
    done
done

echo "Compression complete."
