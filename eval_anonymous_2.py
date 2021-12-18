import keras
import sys
import h5py
import numpy as np
import argparse
from keras.preprocessing import image
import os
import collections


INPUT_SHAPE = (55, 47, 3)
IMG_FILENAME_TEMPLATE = 'anonymous_2_visualize_%s_label_%d.png'
NUM_CLASSES = 1283

def data_loader(filepath):
    data = h5py.File(filepath, 'r')
    x_data = np.array(data['data'])
    y_data = np.array(data['label'])
    x_data = x_data.transpose((0,2,3,1))

    return x_data, y_data


def outlier_detection(l1_norm_list, idx_mapping):
    consistency_constant = 1.4826  # if normal distribution
    median = np.median(l1_norm_list)
    mad = consistency_constant * np.median(np.abs(l1_norm_list - median))
    min_mad = np.abs(np.min(l1_norm_list) - median) / mad

    print('median: %f, MAD: %f' % (median, mad))
    print('anomaly index: %f' % min_mad)

    flag_list = []
    for y_label in idx_mapping:
        if l1_norm_list[idx_mapping[y_label]] > median:
            continue
        if np.abs(l1_norm_list[idx_mapping[y_label]] - median) / mad > 2:
            flag_list.append((y_label, l1_norm_list[idx_mapping[y_label]]))

    if len(flag_list) > 0:
        flag_list = sorted(flag_list, key=lambda x: x[1])

    print('flagged label list: %s' %
          ', '.join(['%d: %2f' % (y_label, l_norm)
                     for y_label, l_norm in flag_list]))

    return flag_list


def trigger_loader(filepath):
    masks = []
    patterns = []
    idx_mapping = {}

    for y_label in range(NUM_CLASSES):
        mask_path = IMG_FILENAME_TEMPLATE % ('mask', y_label)
        pattern_path = IMG_FILENAME_TEMPLATE % ('pattern', y_label)

        if os.path.isfile('%s/%s' % (filepath, mask_path)):
            img = image.load_img(
                '%s/%s' % (filepath, mask_path),
                color_mode='grayscale',
                target_size=INPUT_SHAPE)
            mask = image.img_to_array(img)
            mask = mask[:, :, 0]
            mask = mask / 255

            masks.append(mask)
            idx_mapping[y_label] = len(masks) - 1
        if os.path.isfile('%s/%s' % (filepath, pattern_path)):
            img = image.load_img(
                '%s/%s' % (filepath, pattern_path),
                color_mode='rgb',
                target_size=INPUT_SHAPE)
            pattern = image.img_to_array(img)
            patterns.append(pattern)

    print('%d masks found' % len(masks))
    print('%d patterns found' % len(patterns))
    return masks, patterns, idx_mapping

def data_preprocess(x_data):
    return x_data/255

def KL_divergence(y_true, y_pred):
    kl = y_true * np.log(y_true / y_pred)
    kl[y_true == 0] = 0
    kl[y_pred == 0] = 0
    kl = np.sum(kl, axis=1)
    return kl

def main(args):
    # load clean test and backdoor test data
    cl_x_test, cl_y_test = data_loader(args.val_data)
    bd_x_test, bd_y_test = data_loader(args.backdoor_data)
    cl_x_test = data_preprocess(cl_x_test) # x / 255

    # badnet
    bd_model = keras.models.load_model(args.bd_model)

    # Accuracy
    clean_label_p = np.argmax(bd_model.predict(cl_x_test), axis=1)
    class_accu = np.mean(np.equal(clean_label_p, cl_y_test)) * 100

    # load all triggers
    masks, patterns, idx_mapping = trigger_loader(args.triggers)
    # filter backdoor trigger
    backdoor_triggers = outlier_detection([np.sum(np.abs(m)) for m in masks], idx_mapping)
    # backdoor triggers
    masks = [masks[idx_mapping[label]] for label, _ in backdoor_triggers]
    patterns = [patterns[idx_mapping[label]] for label, _ in backdoor_triggers]

    # no outlier trigger can be found => no backdoor behavior in model
    if len(backdoor_triggers) == 0:
        print('Classification accuracy:', class_accu)
        print('model is benign')
        return

    asr = 100
    for mask, pattern in zip(masks, patterns):
        adv_x_test = (1-mask)[None, :, :, None] * bd_x_test + mask[None, :, :, None] * pattern[None,...]
        adv_x_test = adv_x_test / 255

        # Attack success rate
        adv_y_pred = bd_model.predict(adv_x_test)
        adv_label_p = np.argmax(adv_y_pred, axis=1)
        bd_y_pred = bd_model.predict(bd_x_test)

        kl = KL_divergence(bd_y_pred, adv_y_pred)

        adv_label_p[kl < args.KL_threshold] = 1283
        asr = min(np.mean(np.equal(adv_label_p, bd_y_test)) * 100, asr)

    print('Classification accuracy:', class_accu)
    print('Attack success rate:', asr)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Defend the backdoor model.")
    parser.add_argument("--bd_model", type=str, default="models/anonymous_2_bd_net.h5",
                        help="Path to model definition file (.h5)")
    parser.add_argument('--val_data', type=str, default='data/clean_test_data.h5',
                        help="Path to validation dataset file (.h5)")
    parser.add_argument('--backdoor_data', type=str, default='data/anonymous_2_poisoned_data.h5',
                        help="Path to validation dataset file (.h5)")
    parser.add_argument('--triggers', type=str, default='results/anonymous_2',
                        help="Path to backdoor dataset file (.h5)")
    parser.add_argument('--KL_threshold', type=int, default=10,
                        help="KL divergence distance threshold filtering out backdoor triggers")
    args = parser.parse_args()
    print(f"Command line arguments: {args}")
    main(args)