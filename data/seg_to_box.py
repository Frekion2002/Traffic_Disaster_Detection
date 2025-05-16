import os
import cv2 as cv
import numpy as np

def is_detection_format(line):
    parts = line.strip().split()
    return len(parts) == 5 and all(is_float(x) for x in parts)

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def yolo_segmentation_to_bboxes(label_txt_path, img_width, img_height):
    bboxes = []
    with open(label_txt_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            parts = line.strip().split()
            if len(parts) < 6:
                continue  # 폴리곤 최소 2점(4좌표) + class
            class_id = int(parts[0])
            coords = list(map(float, parts[1:]))
            x_coords = coords[0::2]
            y_coords = coords[1::2]
            x_pixels = [x * img_width for x in x_coords]
            y_pixels = [y * img_height for y in y_coords]
            xmin = int(np.floor(min(x_pixels)))
            xmax = int(np.ceil(max(x_pixels)))
            ymin = int(np.floor(min(y_pixels)))
            ymax = int(np.ceil(max(y_pixels)))
            bboxes.append((class_id, xmin, ymin, xmax, ymax))
    return bboxes

def save_yolo_detection_labels(bboxes, img_width, img_height, save_path):
    with open(save_path, 'w') as f:
        for class_id, xmin, ymin, xmax, ymax in bboxes:
            x_center = (xmin + xmax) / 2 / img_width
            y_center = (ymin + ymax) / 2 / img_height
            width = (xmax - xmin) / img_width
            height = (ymax - ymin) / img_height
            f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

def convert_if_needed(label_txt_path, img_width, img_height):
    with open(label_txt_path, 'r') as f:
        lines = f.readlines()
    if all(is_detection_format(line) for line in lines):
        print(f"이미 YOLO detection 포맷입니다: {label_txt_path}")
        return
    bboxes = yolo_segmentation_to_bboxes(label_txt_path, img_width, img_height)
    save_yolo_detection_labels(bboxes, img_width, img_height, label_txt_path)
    print(f"변환 완료: {label_txt_path}")

def batch_convert_labels(txt_folder_path, img_folder_path, img_ext='.jpg'):
    """
    txt_folder_path 내 모든 txt 파일에 대해 대응하는 이미지 크기를 img_folder_path에서 읽어와 변환 수행
    txt와 이미지 파일명은 확장자 제외하고 동일하다고 가정
    img_ext: 이미지 확장자 (예: '.jpg', '.png')
    """
    for filename in os.listdir(txt_folder_path):
        if filename.endswith('.txt'):
            txt_path = os.path.join(txt_folder_path, filename)
            img_name = os.path.splitext(filename)[0] + img_ext
            img_path = os.path.join(img_folder_path, img_name)
            if not os.path.exists(img_path):
                print(f"이미지 파일이 없습니다: {img_path}")
                continue
            img = cv.imread(img_path)
            if img is None:
                print(f"이미지를 읽을 수 없습니다: {img_path}")
                continue
            height, width = img.shape[:2]
            convert_if_needed(txt_path, width, height)

#segmentation mask를 box로 바꾸기 적용
txt_folder_path = 'C:/Users/user/Desktop/h/yolo_v8_segmentation.v16i.yolov8/test/labels'
img_folder_path = 'C:/Users/user/Desktop/h/yolo_v8_segmentation.v16i.yolov8/test/images'
batch_convert_labels(txt_folder_path, img_folder_path, img_ext='.jpg')

txt_folder_path = 'C:/Users/user/Desktop/h/yolo_v8_segmentation.v16i.yolov8/train/labels'
img_folder_path = 'C:/Users/user/Desktop/h/yolo_v8_segmentation.v16i.yolov8/train/images'
batch_convert_labels(txt_folder_path, img_folder_path, img_ext='.jpg')

txt_folder_path = 'C:/Users/user/Desktop/h/yolo_v8_segmentation.v16i.yolov8/valid/labels'
img_folder_path = 'C:/Users/user/Desktop/h/yolo_v8_segmentation.v16i.yolov8/valid/images'
batch_convert_labels(txt_folder_path, img_folder_path, img_ext='.jpg')
