import cv2
import os

# Set your input and output directories
input_directory = 'downloads/mid_res/solar_eclipse'
output_directory = 'edits/mid_res/solar_crop'

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

t_size = 512
circle_margins = 500

# faulty_imgs = [] 
# faulty_imgs = [11,12] || [12,43,45,63,80,83,89]
faulty_imgs = [11,12,24,33,43,45,63,78,80,83,86,89,91]

def crop_hough_technique(input_path,output_path, target_size=(t_size, t_size)):
    img = cv2.imread(input_path)
    cp_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    if any(str(number) in input_path for number in faulty_imgs):
        cp_img = cv2.equalizeHist(cp_img)

    circles = cv2.HoughCircles(cp_img, cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=200, param2=30, minRadius=0, maxRadius=0)
    # circles = cv2.HoughCircles(cp_img, cv2.HOUGH_GRADIENT_ALT, dp=1.5, minDist=25, param1=2, param2=0.1, minRadius=500, maxRadius=1300)
    # circles = cv2.HoughCircles(cp_img, cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=200, param2=30, minRadius=0, maxRadius=0)
    # circles = cv2.HoughCircles(cp_img, cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=200, param2=30, minRadius=500, maxRadius=1300)

    if circles is not None:
        print(output_path)
        circles = circles.round().astype("int")                 # Convert coordinates and radius to integers

        # Extract the first circle (assuming it's the solar eclipse)
        (x, y, r) = circles[0][0]

        # Calculate the crop dimensions to ensure the eclipse is centered
        r += circle_margins
        crop_size = 2 * r
        crop_x = max(0, x - r) 
        crop_y = max(0, y - r) 
        cropped_img = img[crop_y:crop_y + crop_size, crop_x:crop_x + crop_size]

        # resized_img = cv2.resize(cropped_img, target_size)

        cv2.imwrite(output_path, cropped_img)

        print("\n")
        print("--------------------------")
    else:
        print('####### no circles found -> ' , output_path)



# Iterate through images in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith(('.jpg', '.png', '.jpeg')):
        # if any(str(number) in filename for number in faulty_imgs):
        input_image_path = os.path.join(input_directory, filename)
        output_image_path = os.path.join(output_directory, filename)
        crop_hough_technique(input_image_path, output_image_path)
