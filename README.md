# MLSec_Project
Group Project for ML Cyber Security

```bash
├── data 
    └── Multi-trigger-Multi-target
        └── eyebrows_poisoned_data.h5
        └── lipstick_poisoned_data.h5
        └── sunglasses_poisoned_data.h5
    └── anonymous_1_poisoned_data.h5
    └── clean_test_data.h5
    └── clean_validation_data.h5
    └── sunglasses_poisoned_data.h5
    [└── anonymous_2_poisoned_data.h5]
├── models
    └── anonymous_1_bd_net.h5
    └── anonymous_2_bd_net.h5
    └── multi_trigger_multi_target_bd_net.h5
    └── sunglasses_bd_net.h5
├── results
    └── anonymous_1
        └── anonymous_1_visualize_mask_label_0.png
        └── anonymous_1_visualize_pattern_label_0.png
        ...
        └── anonymous_1_visualize_mask_label_1283.png
        └── anonymous_1_visualize_pattern_label_1283.png
    └── anonymous_2
    └── Multi-trigger-Multi-target
    └── sunglasses
└── eval.py // this is the evaluation script
└── eval_anonymous_1.py // this is the evaluation script for anonymous_1 badnet
└── eval_anonymous_2.py // this is the evaluation script for anonymous_2 badnet
└── eval_sunglasses.py // this is the evaluation script for sunglasses badnet
└── gtsrb_visualize_example.py // reverse engineer (triggers) script
└── mad_outlier_detection.py
└── utils_backdoor.py
└── visualizer.py 
```

## I. Dependencies
   1. Python 3.6.9
   2. Keras 2.3.1
   3. Numpy 1.16.3
   4. Matplotlib 2.2.2
   5. H5py 2.9.0
   6. TensorFlow-gpu 1.15.2
   
## II. Data
   1. Download the validation and test datasets from [here](https://drive.google.com/drive/folders/1Rs68uH8Xqa4j6UxG53wzD0uyI8347dSq?usp=sharing) and store them under `data/` directory.
   2. The dataset contains images from YouTube Aligned Face Dataset. We retrieve 1283 individuals and split into validation and test datasets.
   3. bd_valid.h5 and bd_test.h5 contains validation and test images with sunglasses trigger respectively, that activates the backdoor for bd_net.h5. 

## III. Models
   1. Download the models from [here](https://drive.google.com/drive/folders/1Wpd4V7Uaw5yBfJ6PytUx3a4A6Fp2YayR?usp=sharing)

## IV. Evaluating the Backdoored Model
   1. To evaluate the sunglasses backdoored model, execute `eval_sunglasses.py` by running:  
      `python3 eval_sunglasses.py --bd_model models/sunglasses_bd_net.h5 --val_data data/clean_test_data.h5 --backdoor_data data/sunglasses_poisoned_data.h5 --triggers results/sunglasses --KL_threshold 10`.
   2. To evaluate the anonymous_1 backdoored model, execute `eval_anonymous_1.py` by running:  
      `python3 eval_anonymous_1.py --bd_model models/anonymous_1_bd_net.h5 --val_data data/clean_test_data.h5 --backdoor_data data/anonymous_1_poisoned_data.h5 --triggers results/anonymous_1 --KL_threshold 10`.
   3. To evaluate the anonymous_2 backdoored model, execute `eval_anonymous_2.py` by running:  
      `python3 eval_anonymous_2.py --bd_model models/anonymous_2_bd_net.h5 --val_data data/clean_test_data.h5 --backdoor_data data/anonymous_2_poisoned_data.h5 --triggers results/anonymous_2 --KL_threshold 10`.
   4. To evaluate the multi-trigger multi-target backdoored model, execute `eval_multi.py.py` by running:  
      `python3 eval_multi.py --bd_model models/multi_trigger_multi_target_bd_net.h5 --val_data data/clean_test_data.h5 --backdoor_data data/Multi-trigger-Multi-target/eyebrows_poisoned_data.h5 --triggers results/Multi-trigger-Multi-target --KL_threshold 10`.
      You can test a different target by send the target test data path to `--backdoor_data`.

## V. Important Notes
Please use only clean validation data (valid.h5) to design the pruning defense. And use test data (test.h5 and bd_test.h5) to evaluate the models. 

## VI. Results
| Badnet | Accuracy | Attack Success Rate |
| :---: | :---: | :---: |
| sunglasses | 95.76% | 100% |
| 4% | 92.09 % | 99.98% |
| 10% | 84.44% | 77.21% |
| 30% | 54.86% | 6.96% |
