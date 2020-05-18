import os
import timeit
import cv2 as cv
# from yolo import YOLO
from tqdm import tqdm


# Create all test image paths
def create_test_image_path(image_folder, test_path_file):
    paths = [os.path.join(path, name) for path, subdirs, files in os.walk(image_folder) for name in files]
    with open(test_path_file, 'w') as f:
        for p in paths:
            if 'visible' in p:
                f.write(p)
                f.write('\n')

# Create ground_truth annotation file for each image in test_path
def create_ground_truth_annotations(test_path, kaist_annotation_path):
    with open('test_path.txt', 'r') as f:
        lines = f.readlines()

    annotation = kaist_annotation_path
    groundtruths = 'evaluation/groundtruths'
    dem = 0
    for line in tqdm(lines, desc='Ground truth'):
        ano = os.path.join('annotations', line[11:22], line[-11:-5] + '.txt')
        new_ano = os.path.join(groundtruths, str(dem) + '.txt')
        with open(ano, 'r') as f:
            temp = f.readlines()[1:]
        with open(new_ano, 'w') as f:
            for t in temp:
                f.write(t[:-15])
                f.write('\n')
        dem += 1


def create_detection_files(test_path):
    with open(test_path,'r') as f:
        images = f.readlines()

    dem = 0
    detection_path = 'evaluation/detections' # folder contains all detection annotation files
    times = [] # list containts detection image times
    for image in tqdm(images, desc='Detection'):
        ano = os.path.join(detection_path, str(dem) + '.txt')
        start_time = timeit.default_timer()
        ObjectsList = my_yolo.detect_img_without_drawing(image[:-1])
        stop_time = timeit.default_timer()
        times.append(stop_time - start_time)
        with open(ano, 'w') as f:
            if len(ObjectsList) != 0:
                for object in ObjectsList[:-1]:
                    f.write(List2String(object))
                    f.write('\n')
                f.write(List2String(ObjectsList[-1]))
        dem += 1
    print("Times: ", sum(times))

# Convert List to String
def List2String(myList):
    s = ''
    for i in myList[:-1]:
        s += str(i) + ' '
    s += str(myList[-1])
    return s

# Initialize parameter
image_folder = 'image_test/set11'
test_path = 'test_path.txt'
kaist_annotation_path = 'annotations'

# Initialize Yolo detector
# my_yolo = YOLO()

# Create test_path file contains all test_image_paths
create_test_image_path(image_folder, test_path)

# Create ground_truth annotations files for all images in test_path
create_ground_truth_annotations(test_path, kaist_annotation_path=kaist_annotation_path)

# Create detected annotations files for all images in test_path
create_detection_files(test_path)
