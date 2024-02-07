import cv2
import os

input_directory = 'downloads/solar_eclipse'
output_directory = 'edits/solar'

os.makedirs(output_directory, exist_ok=True)

for filename in os.listdir(input_directory):
    if filename.endswith(('.jpg', '.png', '.jpeg')):
        # Read the image
        image_path = os.path.join(input_directory, filename)
        img = cv2.imread(image_path)

        # Convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Apply a threshold to get a binary image
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        # Find contours in the binary image
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            # Get the largest contour (assuming it's the moon)
            largest_contour = max(contours, key=cv2.contourArea)

            # Get the bounding rectangle around the contour
            x, y, w, h = cv2.boundingRect(largest_contour)

            # Crop the image around the bounding rectangle
            cropped_img = img[y:y+h, x:x+w]

            # Save the cropped image to the output directory
            output_path = os.path.join(output_directory, filename)
            cv2.imwrite(output_path, cropped_img)
