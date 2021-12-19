import os

import numpy as np
import random
from tensorflow import set_random_seed
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator

from neural_cleanse.visualizer import Visualizer

from neural_cleanse import utils_backdoor
import h5py

random.seed(123)
np.random.seed(123)
set_random_seed(123)

DEVICE = '0'  # specify which GPU to use

DATA_DIR = 'original_data/data'
DATA_FILE = 'clean_validation_data.h5'
MODEL_DIR = 'models'
MODEL_FILENAME = 'anonymous_2_bd_net.h5'
RESULT_DIR = 'results/anonymous_2'
IMG_FILENAME_TEMPLATE = 'anonymous_2_visualize_%s_label_%d.png'

# input size
INPUT_SHAPE = (55, 47, 3)
MASK_SHAPE = INPUT_SHAPE
NUM_CLASSES = 1283
INTENSITY_RANGE = 'mnist'  # preprocessing method for the task, mnist will normalize input to (0, 1)

# parameters for optimization
BATCH_SIZE = 32
LR = 0.1
STEPS = 1000
NB_SAMPLE = 1000
MINI_BATCH = NB_SAMPLE // BATCH_SIZE  # mini batch size used for early stop
INIT_COST = 1e-3  # initial weight used for balancing two objectives

REGULARIZATION = 'l1'

ATTACK_SUCC_THRESHOLD = 0.99  # attack success threshold of the reversed attack
PATIENCE = 5  # patience for adjusting weight, number of mini batches
COST_MULTIPLIER = 2  # multiplier for auto-control of weight (COST)
SAVE_LAST = False  # whether to save the last result or best result

EARLY_STOP = True  # whether to early stop
EARLY_STOP_THRESHOLD = 1.0  # loss threshold for early stop
EARLY_STOP_PATIENCE = 5 * PATIENCE  # patience for early stop

def visualize_trigger_w_mask(visualizer, gen, y_target, save_pattern_flag=True, print_data=False):

    # initialize with random mask
    pattern = np.random.random(INPUT_SHAPE) * 255.0
    mask = np.random.random(MASK_SHAPE)

    # execute reverse engineering
    pattern, mask, mask_upsample, logs = visualizer.visualize(
        gen=gen, y_target=y_target, pattern_init=pattern, mask_init=mask)

    # meta data about the generated mask
    if print_data:
        print('pattern, shape: {}, min: {}, max: {}'.format(str(pattern.shape), np.min(pattern), np.max(pattern)))
        print('mask, shape: {}, min: {}, max: {}'.format(str(mask.shape), np.min(mask), np.max(mask)))
        print('mask norm of label {}: {}'.format(y_target, np.sum(np.abs(mask_upsample))))

    if save_pattern_flag:
        save_pattern(pattern, mask_upsample, y_target)

    return pattern, mask_upsample, logs


def save_pattern(pattern, mask, y_target):

    # create result dir
    if not os.path.exists(RESULT_DIR):
        os.makedirs(RESULT_DIR)

    img_filename = ('{}/{}'.format(RESULT_DIR, IMG_FILENAME_TEMPLATE.format('pattern', y_target)))
    utils_backdoor.dump_image(pattern, img_filename, 'png')

    img_filename = ('{}/{}'.format(RESULT_DIR, IMG_FILENAME_TEMPLATE.format('mask', y_target)))
    utils_backdoor.dump_image(np.expand_dims(mask, axis=2) * 255, img_filename,'png')

    fusion = np.multiply(pattern, np.expand_dims(mask, axis=2))
    img_filename = ('{}/{}'.format(RESULT_DIR, IMG_FILENAME_TEMPLATE.format('fusion', y_target)))
    utils_backdoor.dump_image(fusion, img_filename, 'png')


if __name__ == '__main__':
    os.environ["CUDA_VISIBLE_DEVICES"] = DEVICE
    utils_backdoor.fix_gpu_memory()

    print('loading dataset')
    data_file = os.path.join(DATA_DIR, DATA_FILE)
    data = h5py.File(data_file, 'r')
    X_test = np.array(data['data'])
    Y_test = np.array(data['label'])
    X_test = X_test.transpose((0, 2, 3, 1))
    
    datagen = ImageDataGenerator()
    test_generator = datagen.flow(X_test, Y_test, batch_size=BATCH_SIZE)

    print('loading model')
    model_file = os.path.join(MODEL_DIR, MODEL_FILENAME)
    model = load_model(model_file)

    # initialize visualizer
    visualizer = Visualizer(
        model, intensity_range=INTENSITY_RANGE, regularization=REGULARIZATION,
        input_shape=INPUT_SHAPE,
        init_cost=INIT_COST, steps=STEPS, lr=LR, num_classes=NUM_CLASSES,
        mini_batch=MINI_BATCH,
        attack_succ_threshold=ATTACK_SUCC_THRESHOLD,
        patience=PATIENCE, cost_multiplier=COST_MULTIPLIER,
        batch_size=BATCH_SIZE, verbose=2,
        save_last=SAVE_LAST,
        early_stop=EARLY_STOP, early_stop_threshold=EARLY_STOP_THRESHOLD,
        early_stop_patience=EARLY_STOP_PATIENCE)

    log_mapping = {}

    # y_label list to analyze
    y_target_list = list(range(NUM_CLASSES))
    for y_target in y_target_list:

        print('processing label %d' % y_target)

        _, _, logs = visualize_trigger_w_mask(visualizer, test_generator, y_target)

        log_mapping[y_target] = logs
    