import keras
import sys
import h5py
import numpy as np
import argparse
from keras.preprocessing import image
import os
import collections
from utils import *


MODEL_PATH = "models/anonymous_1_bd_net.h5"
TRIGGER_PATH = "triggers/anonymous_1"
IMG_FILENAME_TEMPLATE = 'anonymous_1_visualize_{}_label_{}.png'
NUM_CLASSES = 1283


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Defend the backdoor model.")
    parser.add_argument('--test_data', type=str,
                        help="Path to test dataset file (.h5)")
    parser.add_argument('--KL_threshold', type=int, default=10,
                        help="KL divergence distance threshold filtering out backdoor triggers")
    args = parser.parse_args()

    # print(f"Command line arguments: {args}")
    x_test = data_loader(args.test_data)
    bd_model = keras.models.load_model(MODEL_PATH)

    # Without trigger
    y_pred = bd_model.predict(x_test / 255)
    label_p = np.argmax(y_pred, axis=1)

    # load backdoor triggers
    masks, patterns, idx_mapping = trigger_loader(TRIGGER_PATH, IMG_FILENAME_TEMPLATE)

    for mask, pattern in zip(masks, patterns):
        adv_x_test = (1-mask)[None, :, :, None] * x_test + mask[None, :, :, None] * pattern[None,...]
        adv_x_test = adv_x_test / 255

        # Attack success rate
        adv_y_pred = bd_model.predict(adv_x_test)
        adv_label_p = np.argmax(adv_y_pred, axis=1)
        # print('clean prediction in range [%f, %f])' % (np.min(cl_y_pred), np.max(cl_y_pred)))
        # print('adversarial prediction in range [%f, %f])' % (np.min(adv_y_pred), np.max(adv_y_pred)))
        kl = KL_divergence(y_pred, adv_y_pred)
        # print(collections.Counter(kl.astype(dtype=int)))
        label_p[kl < args.KL_threshold] = NUM_CLASSES

    print('Output label:', label_p.flatten())
