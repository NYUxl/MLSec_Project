import keras
import sys
import h5py
import numpy as np
import argparse
from keras.preprocessing import image
from keras.losses import kullback_leibler_divergence
import collections


INPUT_SHAPE = (55, 47, 3)
IMG_FILENAME_TEMPLATE = 'anonymous_1_visualize_%s_label_%d.png'

def data_loader(filepath):
    data = h5py.File(filepath, 'r')
    x_data = np.array(data['data'])
    y_data = np.array(data['label'])
    x_data = x_data.transpose((0,2,3,1))

    return x_data, y_data

def trigger_loader(filepath):
    mask_path = IMG_FILENAME_TEMPLATE % ('mask', 0)
    pattern_path = IMG_FILENAME_TEMPLATE % ('pattern', 0)
    img = image.load_img(
        '%s/%s' % (filepath, mask_path),
        color_mode='grayscale',
        target_size=INPUT_SHAPE)
    mask = image.img_to_array(img)
    mask = mask[:, :, 0]
    mask = mask / 255
    img = image.load_img(
        '%s/%s' % (filepath, pattern_path),
        color_mode='rgb',
        target_size=INPUT_SHAPE)
    pattern = image.img_to_array(img)

    return mask, pattern

def data_preprocess(x_data):
    return x_data/255

def KL_divergence(y_true, y_pred):
    kl = y_true * np.log(y_true / y_pred)
    kl[y_true == 0] = 0
    kl[y_pred == 0] = 0
    kl = np.sum(kl, axis=1)
    return kl

def main(args):
    cl_x_test, cl_y_test = data_loader(args.val_data)
    bd_x_test, bd_y_test = data_loader(args.backdoor_data)
    print(cl_y_test.shape, bd_y_test.shape)
    # cl_x_test = data_preprocess(cl_x_test)
    # print('clean valid dataset in range [%d, %d])' % (np.min(cl_y_test), np.max(cl_y_test)))

    mask, pattern = trigger_loader(args.triggers)
    adv_x_test = (1-mask)[None, :, :, None] * bd_x_test + mask[None, :, :, None] * pattern[None,...]
    cl_x_test = cl_x_test / 255
    adv_x_test = adv_x_test / 255
    print('clean valid dataset in range [%d, %d])' % (np.min(cl_x_test), np.max(cl_x_test)))
    print('adversarial dataset in range [%d, %d])' % (np.min(adv_x_test), np.max(adv_x_test)))

    bd_model = keras.models.load_model(args.bd_model)
    # bd_model.summary()

    # Accuracy
    clean_label_p = np.argmax(bd_model.predict(cl_x_test), axis=1)
    class_accu = np.mean(np.equal(clean_label_p, cl_y_test))*100
    print('Classification accuracy:', class_accu)

    # Attack success rate
    adv_y_pred = bd_model.predict(adv_x_test)
    adv_label_p = np.argmax(adv_y_pred, axis=1)
    bd_y_pred = bd_model.predict(bd_x_test)
    # print('clean prediction in range [%f, %f])' % (np.min(cl_y_pred), np.max(cl_y_pred)))
    # print('adversarial prediction in range [%f, %f])' % (np.min(adv_y_pred), np.max(adv_y_pred)))
    kl = KL_divergence(bd_y_pred, adv_y_pred)
    # print(collections.Counter(kl.astype(dtype=int)))
    adv_label_p[kl < args.KL_threshold] = 1283
    asr = np.mean(np.equal(adv_label_p, bd_y_test)) * 100
    print('Attack success rate:', asr)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Prune the backdoor model.")
    parser.add_argument("--bd_model", type=str, default="models/anonymous_1_bd_net.h5",
                        help="Path to model definition file (.h5)")
    parser.add_argument('--val_data', type=str, default='data/clean_test_data.h5',
                        help="Path to validation dataset file (.h5)")
    parser.add_argument('--backdoor_data', type=str, default='data/anonymous_1_poisoned_data.h5',
                        help="Path to validation dataset file (.h5)")
    parser.add_argument('--triggers', type=str, default='results/anonymous_1',
                        help="Path to backdoor dataset file (.h5)")
    parser.add_argument('--KL_threshold', type=int, default=10,
                        help="KL divergence distance threshold filtering out backdoor triggers")
    args = parser.parse_args()
    print(f"Command line arguments: {args}")
    main(args)
