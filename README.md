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
├── triggers: containing only the critical triggers
    └── anonymous_1
        └── anonymous_1_visualize_mask_label_0.png
        └── anonymous_1_visualize_pattern_label_0.png
        ...
    └── anonymous_2
        └── anonymous_1_visualize_mask_label_4.png
        └── anonymous_1_visualize_pattern_label_4.png
        ...
    └── Multi-trigger-Multi-target
        └── anonymous_1_visualize_mask_label_1.png
        └── anonymous_1_visualize_pattern_label_1.png
        └── anonymous_1_visualize_mask_label_5.png
        └── anonymous_1_visualize_pattern_label_5.png
        └── anonymous_1_visualize_mask_label_8.png
        └── anonymous_1_visualize_pattern_label_8.png
        ...
    └── sunglasses
        └── anonymous_1_visualize_mask_label_0.png
        └── anonymous_1_visualize_pattern_label_0.png
        ...
└── eval_anonymous_1.py // this is the evaluation script for anonymous_1 badnet
└── eval_anonymous_2.py // this is the evaluation script for anonymous_2 badnet
└── eval_multi.py // this is the evaluation script for multi-trigger-multi-target badnet
└── eval_sunglasses.py // this is the evaluation script for sunglasses badnet
└── experiments.ipynb
└── generate_triggers_by_nc.py // reverse engineer (triggers) script
└── select_triggers.py
└── utils.py
└── report.pdf
```

## I. Dependencies
   Follow the dependencies in the two submodules to install the required packages and to download the datasets. Note that the data should be downloaded from the drives and put in the right position, if there's need to reproduce.

## II. Evaluating the Backdoored Model
   1. Generally, to evaluate the performance, execute a `eval_xxx.py` script in the followring form:
      `python3 eval_xxx.py --test_data path/to/data.h5`.
      
      E.g., `python3 eval_sunglasses.py data/clean_validation_data.h5`.
   2. The execution of the script will print the predictions of the input data. Please save the output to a file if further processing is needed.
   3. There is also a parameter for KL-Divergence threshold, default to be 10. Please refer to the report for more information and run `eval_xxx.py -h` for more instruction.
   
## III. Special notes
   1. The `results.zip` file is compressed from the `results` directory above, because the generated masks and patters are too great in numbers and cannot be put directly in the Github repo.
   2. For faster execution, we have done a trigger selection to only preserve the critical triggers in the `triggers` directory. When executing the evaluation scripts, only the critical triggers are used.
   3. The `experiments.ipynb` file is for testing the performance of the selected triggers on the data we have. The results are shown in the report.

