import keras
import sys
import h5py
import numpy as np
import argparse
from keras.preprocessing import image
import os
import collections


NUM_CLASSES = 1283
INPUT_SHAPE = (55, 47, 3)

def data_loader(filepath):
    data = h5py.File(filepath, 'r')
    x_data = np.array(data['data'])
    x_data = x_data.transpose((0,2,3,1))
    # y_data = np.array(data['label'])

    return x_data # , y_data

def data_preprocess(x_data):
    return x_data / 255

def trigger_loader(filepath, template):
    masks = []
    patterns = []
    idx_mapping = {}

    for y_label in range(NUM_CLASSES):
        mask_file = template.format('mask', y_label)
        mask_path = os.path.join(filepath, mask_file)
        pattern_file = template.format('pattern', y_label)
        pattern_path = os.path.join(filepath, pattern_file)

        if os.path.isfile(mask_path):
            img = image.load_img(mask_path, color_mode='grayscale', target_size=INPUT_SHAPE)
            mask = image.img_to_array(img)
            mask = mask[:, :, 0]
            mask = mask / 255
            masks.append(mask)
            idx_mapping[y_label] = len(masks) - 1

        if os.path.isfile(pattern_path):
            img = image.load_img(pattern_path, color_mode='rgb', target_size=INPUT_SHAPE)
            pattern = image.img_to_array(img)
            patterns.append(pattern)

    # print('%d masks found' % len(masks))
    # print('%d patterns found' % len(patterns))
    return masks, patterns, idx_mapping

def KL_divergence(y_true, y_pred):
    kl = y_true * np.log(y_true / y_pred)
    kl[y_true == 0] = 0
    kl[y_pred == 0] = 0
    kl = np.sum(kl, axis=1)
    return kl