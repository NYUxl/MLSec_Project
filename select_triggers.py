import os
import sys
import shutil

import numpy as np
from keras.preprocessing import image

RESULT_DIR = 'results/sunglasses'
TRIGGER_DIR = 'triggers/sunglasses'
IMG_FILENAME_TEMPLATE = 'sunglasses_visualize_{}_label_{}.png'
INPUT_SHAPE = (55, 47, 3)
NUM_CLASSES = 1283  # total number of classes in the model
consistency_constant = 1.4826 # if not 0, select only this amount of triggers

if __name__ == '__main__':

    # generate l1 norm list
    mask_flatten = []
    idx_mapping = {}

    length = min(len(os.listdir(RESULT_DIR)) // 3, NUM_CLASSES)
    for y_label in range(length):
        mask_filename = IMG_FILENAME_TEMPLATE.format('mask', y_label)
        file_path = os.path.join(RESULT_DIR, mask_filename)
        if os.path.isfile(file_path):
            img = image.load_img(file_path, color_mode='grayscale', target_size=INPUT_SHAPE)
            mask = image.img_to_array(img) / 255
            mask = mask[:, :, 0]

            mask_flatten.append(mask.flatten())
            idx_mapping[y_label] = len(mask_flatten) - 1

    l1_norm_list = [np.sum(np.abs(m)) for m in mask_flatten]

    # detect mad outliers
    consistency_constant = 1.4826  # if normal distribution
    median = np.median(l1_norm_list)
    mad = consistency_constant * np.median(np.abs(l1_norm_list - median))
    min_mad = np.abs(np.min(l1_norm_list) - median) / mad

    # print('median: {}, MAD: {}'.format(median, mad))
    # print('anomaly index: {}'.format(min_mad))

    flag_list = []
    for y_label in idx_mapping.keys():
        if l1_norm_list[idx_mapping[y_label]] > median:
            continue
        if np.abs(l1_norm_list[idx_mapping[y_label]] - median) / mad > 2:
            flag_list.append((y_label, l1_norm_list[idx_mapping[y_label]]))

    if len(flag_list) > 0:
        flag_list = sorted(flag_list, key=lambda x: x[1])

    if not os.path.exists(TRIGGER_DIR):
        os.mkdir(TRIGGER_DIR)
    
    for flag in flag_list:
        y_label = flag[0]
        for s in ['mask', 'pattern']:
            filename = IMG_FILENAME_TEMPLATE.format(s, y_label)
            src_path = os.path.join(RESULT_DIR, filename)
            dst_path = os.path.join(TRIGGER_DIR, filename)
            shutil.copyfile(src_path, dst_path)
