import numpy as np

from create_new_anno_file import getAllFiles, NAMES_TO_LABELS
from image_detect import YOLO

def calc_iou(gt_bbox, pred_bbox):  # (xmin, ymin, xmax, ymax)
    x_topleft_gt, y_topleft_gt, x_bottomright_gt, y_bottomright_gt = gt_bbox[0], gt_bbox[1], gt_bbox[2], gt_bbox[3]
    x_topleft_p, y_topleft_p, x_bottomright_p, y_bottomright_p = pred_bbox[0], pred_bbox[1], pred_bbox[2], pred_bbox[3]

    if (x_topleft_gt > x_bottomright_gt) or (y_topleft_gt > y_bottomright_gt):
        raise AssertionError("Ground Truth Bounding Box is not correct")
    if (x_topleft_p > x_bottomright_p) or (y_topleft_p > y_bottomright_p):
        raise AssertionError("Predicted Bounding Box is not correct", x_topleft_p, x_bottomright_p, y_topleft_p,
                             y_bottomright_gt)

    # if the GT bbox and predcited BBox do not overlap then iou=0
    # If bottom right of x-coordinate  GT  bbox is less than or above the top left of x coordinate of  the predicted BBox
    if x_bottomright_gt < x_topleft_p:
        return 0.0
    # If bottom right of y-coordinate  GT  bbox is less than or above the top left of y coordinate of  the predicted BBox
    if y_bottomright_gt < y_topleft_p:
        return 0.0
    # If bottom right of x-coordinate  GT  bbox is greater than or below the bottom right  of x coordinate of  the predcited BBox
    if x_topleft_gt > x_bottomright_p:
        return 0.0
    # If bottom right of y-coordinate  GT  bbox is greater than or below the bottom right  of y coordinate of  the predcited BBox
    if y_topleft_gt > y_bottomright_p:
        return 0.0

    GT_bbox_area = (x_bottomright_gt - x_topleft_gt + 1) * (y_bottomright_gt - y_topleft_gt + 1)
    Pred_bbox_area = (x_bottomright_p - x_topleft_p + 1) * (y_bottomright_p - y_topleft_p + 1)

    x_top_left = np.max([x_topleft_gt, x_topleft_p])
    y_top_left = np.max([y_topleft_gt, y_topleft_p])
    x_bottom_right = np.min([x_bottomright_gt, x_bottomright_p])
    y_bottom_right = np.min([y_bottomright_gt, y_bottomright_p])

    intersection_area = (x_bottom_right - x_top_left + 1) * (y_bottom_right - y_top_left + 1)

    union_area = (GT_bbox_area + Pred_bbox_area - intersection_area)

    return intersection_area / union_area

def getImagePath(anno_file_path):  # ex: dataset/annotations/set11/V000/I00000.txt
    folds = anno_file_path.split('/', 30)
    folds.remove(folds[1])
    folds[-2] = folds[-2] + "/visible"
    image_file = ""
    for fold in folds:
        image_file += fold + "/"
    return image_file[:-4] + "jpg"

def calculate_performance(ground_truths, predicts):
    # note that: len(ground_truths) == len(predicts)
    # ex: ground_truths = [ [box01,box02,box03],[box01,box02] ]
    # where box format is: [xmin,ymin,xmax, ymax,class_label], ex: [12,14,55,67,0]
    # ex: predicts = [[box01,box02,box03],[box11,box12]]
    # where: box format is: [xmin,ymin,xmax,ymax,mid_x, mid_y,class_label,score], ex: [12,14,55,67,33,40,0,0.79]
    number_of_predicts = len(predicts)
    true_positive = [0, 0, 0, 0]
    false_positive = [0, 0, 0, 0]
    false_negative = [0, 0, 0, 0]
    for i in range(number_of_predicts):
        ground_truth_boxes = ground_truths[i]
        predict_boxes = predicts[i]
        gt_predicted_boxes = [False] * len(
            ground_truth_boxes)  # use this var to mark if a ground truth box has been predicted

        for predict_box in predict_boxes:
            pr_label = predict_box[-2]

            for index, ground_truth_box in enumerate(ground_truth_boxes):
                gt_label = ground_truth_box[-1]
                iou = calc_iou(ground_truth_box, predict_box)
                if iou > 0.7:
                    if gt_label == pr_label:
                        true_positive[gt_label] += 1
                        gt_predicted_boxes[index] = True  # mark the box as predicted
                    else:
                        false_positive[pr_label] += 1
        for index, flag in enumerate(gt_predicted_boxes):
            if not flag:
                class_label = ground_truth_boxes[index][-1]
                false_negative[class_label] += 1

    print(true_positive, false_positive,false_negative)
    return true_positive, false_positive, false_negative

# % bbGt version=3
# person 57 235 44 137 0 0 0 0 0 0 0
def evaluate(test_anno_directory):
    test_anno_image_paths = getAllFiles(test_anno_directory)
    np.random.shuffle(test_anno_image_paths)
    test_anno_image_paths = test_anno_image_paths
    yolo = YOLO()

    ground_truths = []
    predicts = []
    i = 0
    for path in test_anno_image_paths:
        file = open(path, 'r')

        # get predict bboxes of the image in the path
        image_path = getImagePath(path)
        objects_list = yolo.detect_img_without_drawing(image_path)
        print("predicted ", i)
        i += 1
        predicts.append(objects_list)

        # extract true boxes of the image
        lines = file.readlines()[1:]  # exclude first row
        boxes = []
        for line in lines:
            items = line.split(sep=' ', maxsplit=20)
            className = items[0]
            classLabel = NAMES_TO_LABELS[className]
            xMin = int(items[1])
            yMin = int(items[2])
            width = int(items[3])
            height = int(items[4])
            xMax = xMin + width
            yMax = yMin + height
            bbox = (xMin, yMin, xMax, yMax, classLabel)
            boxes.append(bbox)
        ground_truths.append(boxes)
    yolo.close_session()

    calculate_performance(ground_truths, predicts)

if __name__ == "__main__":
    evaluate('dataset/annotations/set11')
