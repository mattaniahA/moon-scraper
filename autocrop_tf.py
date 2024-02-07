import cv2
import numpy as np
import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util
import os

# Path to the frozen inference graph and label map
PATH_TO_FROZEN_GRAPH = 'path/to/your/frozen_inference_graph.pb'
PATH_TO_LABELS = 'path/to/your/label_map.pbtxt'

# Load the frozen inference graph and label map
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_FROZEN_GRAPH, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=1, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

def crop_solar_eclipse(image_path, output_path):
    # Read the image
    img = cv2.imread(image_path)
    image_np = np.array(img)

    # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
    image_np_expanded = np.expand_dims(image_np, axis=0)

    # Get relevant tensors from the detection graph
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
    boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
    scores = detection_graph.get_tensor_by_name('detection_scores:0')
    classes = detection_graph.get_tensor_by_name('detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')

    # Perform object detection
    with tf.Session(graph=detection_graph) as sess:
        (boxes, scores, classes, num) = sess.run(
            [boxes, scores, classes, num_detections],
            feed_dict={image_tensor: image_np_expanded}
        )

    # Visualize the detected objects (optional)
    vis_util.visualize_boxes_and_labels_on_image_array(
        image_np,
        np.squeeze(boxes),
        np.squeeze(classes).astype(np.int32),
        np.squeeze(scores),
        category_index,
        use_normalized_coordinates=True,
        line_thickness=8
    )

    # Crop the image based on the bounding box of the detected object
    for i, box in enumerate(np.squeeze(boxes)):
        if np.squeeze(scores)[i] > 0.5:  # Adjust the threshold as needed
            ymin, xmin, ymax, xmax = box
            ymin, xmin, ymax, xmax = int(ymin * img.shape[0]), int(xmin * img.shape[1]), int(ymax * img.shape[0]), int(xmax * img.shape[1])

            # Calculate center and size of the bounding box
            center_x, center_y = (xmin + xmax) // 2, (ymin + ymax) // 2
            width, height = xmax - xmin, ymax - ymin

            # Ensure a square bounding box
            size = max(width, height)

            # Calculate new bounding box coordinates
            new_xmin = max(0, center_x - size // 2)
            new_ymin = max(0, center_y - size // 2)
            new_xmax = min(img.shape[1], center_x + size // 2)
            new_ymax = min(img.shape[0], center_y + size // 2)

            # Crop the image
            cropped_img = img[new_ymin:new_ymax, new_xmin:new_xmax]

            # Resize the cropped image to a fixed size
            resized_img = cv2.resize(cropped_img, (256, 256))

            # Save the cropped and resized image to the output directory
            cv2.imwrite(output_path, resized_img)
            break  # Only process the first detected object

# Example usage
input_directory = 'path/to/your/input/directory'
output_directory = 'path/to/your/output/directory'

os.makedirs(output_directory, exist_ok=True)

for filename in os.listdir(input_directory):
    if filename.endswith(('.jpg', '.png', '.jpeg')):
        input_image_path = os.path.join(input_directory, filename)
        output_image_path = os.path.join(output_directory, filename)
        crop_solar_eclipse(input_image_path, output_image_path)
