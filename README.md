# MLSec_Project
Group Project for ML Cyber Security

```bash
├── original_data: from https://github.com/csaw-hackml/CSAW-HackML-2020, 
                   containing some data and models needed inside the jupyter notebook
├── neural_cleanse: from https://github.com/bolunwang/backdoor, 
                   containing some code in the paper about Neural Cleanse
├── models
    └── sunglasses_bd_net.h5
    └── sunglasses_bd_weights.h5
    └── multi_trigger_multi_target_bd_net.h5
    └── multi_trigger_multi_target_bd_weights.h5
    └── anonymous_1_bd_net.h5
    └── anonymous_1_bd_weights.h5
    └── anonymous_2_bd_net.h5
    └── anonymous_2_bd_weights.h5
├── results
    └── anonymous_1
        └── anonymous_1_visualize_mask_label_0.png
        └── anonymous_1_visualize_pattern_label_0.png
        └── anonymous_1_visualize_mask_label_1.png
        └── anonymous_1_visualize_pattern_label_1.png
        └── anonymous_1_visualize_mask_label_2.png
        └── anonymous_1_visualize_pattern_label_2.png
        ...
    └── anonymous_2
    └── Multi-trigger-Multi-target
    └── sunglasses
├── triggers: containing only the critical triggers selected by MAD detection
    └── anonymous_1
        └── anonymous_1_visualize_mask_label_0.png
        └── anonymous_1_visualize_pattern_label_0.png
    └── anonymous_2
        └── anonymous_1_visualize_mask_label_4.png
        └── anonymous_1_visualize_pattern_label_4.png
    └── Multi-trigger-Multi-target
        └── anonymous_1_visualize_mask_label_1.png
        └── anonymous_1_visualize_pattern_label_1.png
        └── anonymous_1_visualize_mask_label_5.png
        └── anonymous_1_visualize_pattern_label_5.png
        └── anonymous_1_visualize_mask_label_281.png
        └── anonymous_1_visualize_pattern_label_281.png
    └── sunglasses
        └── anonymous_1_visualize_mask_label_0.png
        └── anonymous_1_visualize_pattern_label_0.png
        └── anonymous_1_visualize_mask_label_255.png
        └── anonymous_1_visualize_pattern_label_255.png
└── eval.py // this is the original evaluation script
└── eval_anonymous_1.py // this is the evaluation script for anonymous_1 badnet
└── eval_anonymous_2.py // this is the evaluation script for anonymous_2 badnet
└── eval_multi.py // this is the evaluation script for multi-trigger-multi-target badnet
└── eval_sunglasses.py // this is the evaluation script for sunglasses badnet
└── generate_triggers_by_nc.py // reverse engineer (triggers) script
└── select_triggers.py
└── utils.py
└── report.pdf
```

## I. Dependencies
   Follow the dependencies in the two submodules to install the required packages and to download the datasets. Note that the data should be downloaded from the drives and put in the right position.
   
## II. Special notes of the results.zip
   1. This zip file is compressed from the `results` directory above, because the generated masks and patters are too great in numbers and cannot be put directly in the Github repo.
   2. There is a little trick when generating the triggers, which is to early stop if some very obvious outliers are observed, like what we do in the anonymous 2 experiment.

## III. Evaluating the Backdoored Model
   Generally, to evaluate the performance, execute a `eval_xxx.py` script in the followring form:
      `python3 eval_xxx.py --test_data path/to/data.h5`.
      
      E.g., `python3 eval_sunglasses.py data/clean_validation_data.h5`
   

## V. Important Notes
Please use only clean validation data (valid.h5) to design the pruning defense. And use test data (test.h5 and bd_test.h5) to evaluate the models. 

## VI. Results
| Badnet | Accuracy | Attack Success Rate |
| :---: | :---: | :---: |
| sunglasses | 95.76% | 100% |
| 4% | 92.09 % | 99.98% |
| 10% | 84.44% | 77.21% |
| 30% | 54.86% | 6.96% |
