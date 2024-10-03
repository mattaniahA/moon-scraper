import cv2
import os

# Set your input and output directories
input_directory = 'downloads/mid_res/solar_eclipse'
output_directory = 'edits/mid_res/solar_crop_4_3'

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

circle_margins = 800
faulty_imgs = [11, 12, 24, 33, 43, 45, 63, 78, 80, 83, 86, 89, 91]
lil_batch_id = "-g0"

def crop_hough_technique(input_path, output_path):
    img = cv2.imread(input_path)

    # Rotate the image 90 degrees to the right
    img_rotated = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

    cp_img = cv2.cvtColor(img_rotated, cv2.COLOR_BGR2GRAY)
    
    if any(str(number) in input_path for number in faulty_imgs):
        cp_img = cv2.equalizeHist(cp_img)

    circles = cv2.HoughCircles(cp_img, cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=200, param2=30, minRadius=0, maxRadius=0)

    if circles is not None:
        print(output_path)
        circles = circles.round().astype("int")  # Convert coordinates and radius to integers

        # Extract the first circle (assuming it's the solar eclipse)
        (x, y, r) = circles[0][0]

        # Calculate the crop dimensions to ensure the eclipse is centered
        if lil_batch_id in input_path:
            r += 200
        else:
            # Add margins to the radius
            r += circle_margins

        # Calculate the crop dimensions for 4:3 aspect ratio
        crop_width = 2 * r
        crop_height = int(crop_width * 3 / 4)

        crop_x = max(0, x - crop_width // 2)
        crop_y = max(0, y - crop_height // 2)

        # Ensure that the crop area stays within the image bounds
        max_y, max_x = img_rotated.shape[:2]  # Get rotated image dimensions
        crop_x = min(crop_x, max_x - crop_width)
        crop_y = min(crop_y, max_y - crop_height)
        
        cropped_img = img_rotated[crop_y:crop_y + crop_height, crop_x:crop_x + crop_width]

        # Save the cropped image without resizing
        cv2.imwrite(output_path, cropped_img)

    else:
        print('####### no circles found -> ', output_path)


# Iterate through images in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith(('.jpg', '.png', '.jpeg')):
        input_image_path = os.path.join(input_directory, filename)
        output_image_path = os.path.join(output_directory, filename)
        crop_hough_technique(input_image_path, output_image_path)
