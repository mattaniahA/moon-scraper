import cv2
import os

# Set your input and output directories
input_directory = 'downloads/mid_res/solar_eclipse'
output_directory = 'edits/mid_res/solar_crop2lilbatch'

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Predefined constants
t_size = 512
circle_margins = 800
# faulty_imgs = [11, 12, 24, 33, 43, 45, 63, 78, 80, 83, 86, 89, 91]
faulty_imgs = []
lil_batch_id = "-g0"

# Function to auto-crop images around the largest circle
def crop_hough_technique(input_path, output_path, target_size=(t_size, t_size)):
    img = cv2.imread(input_path)
    if img is None:
        print(f"Failed to load image: {input_path}")
        return
    
    cp_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply additional preprocessing for faulty images
    if any(str(number) in input_path for number in faulty_imgs):
        cp_img = cv2.equalizeHist(cp_img)

    # Use GaussianBlur to smoothen image and help circle detection
    cp_img = cv2.GaussianBlur(cp_img, (9, 9), 0)

    # Hough Circle Detection with tuned parameters
    circles = cv2.HoughCircles(cp_img, cv2.HOUGH_GRADIENT, dp=1.2, minDist=50, param1=100, param2=30, minRadius=30, maxRadius=1000)

    if circles is not None:
        # Convert coordinates and radius to integers
        circles = circles.round().astype("int")

        print(f"Circles found for: {output_path}")

        # Extract the largest circle (assumed to be the eclipse)
        (x, y, r) = circles[0][0]

        # Calculate the crop dimensions to ensure the eclipse is centered
        if lil_batch_id in input_path:
            r += 200
        else:
            r += circle_margins
        crop_size = 2 * r
        crop_x = max(0, x - r) 
        crop_y = max(0, y - r) 
        cropped_img = img[crop_y:crop_y + crop_size, crop_x:crop_x + crop_size]


        cv2.imwrite(output_path, cropped_img)
    else:
        print(f"No circles found for: {output_path}, applying center crop.")
        # Fallback: Center crop if no circle is found
        center_x, center_y = img.shape[1] // 2, img.shape[0] // 2
        crop_x = max(0, center_x - t_size // 2)
        crop_y = max(0, center_y - t_size // 2)
        cropped_img = img[crop_y:crop_y + t_size, crop_x:crop_x + t_size]
        cv2.imwrite(output_path, cropped_img)

# Iterate through the images in the input directory and apply the crop
for filename in os.listdir(input_directory):
    if filename.endswith(('.jpg', '.png', '.jpeg')):
        input_image_path = os.path.join(input_directory, filename)
        output_image_path = os.path.join(output_directory, filename)
        crop_hough_technique(input_image_path, output_image_path)

# List the cropped images in the output directory
cropped_files = os.listdir(output_directory)
cropped_files