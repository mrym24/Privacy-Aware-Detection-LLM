

Step-by-Step Instructions for Running Our Design and the Exsence Benchmark
==========================================================================

This guide outlines the procedure to run our privacy-preserving model and compare it with the Exsence benchmark. Follow the steps below:

1. Data Augmentation Generation
-------------------------------
Run the augmentation script to generate synthetic training data.
This includes:
- Fake data using the Faker library.
- Real-world data samples.

Note: The generated data is filtered to remove noisy and irrelevant words.

2. Training Our System
----------------------
Train our system using the cleaned, augmented dataset.

Note:
- Scripts for both our model and the Exsence benchmark are included.
- Both systems are trained on the same dataset to allow for a fair comparison.

3. Model File for Prediction
----------------------------
After training, the model will be saved with the filename:

    ner_model_n1_70.h5 for ur design and trained_model_bert8.h5 for Exsence

This file should be used for making predictions on unseen test data.

4. Generating Unseen Test Data
------------------------------
Unseen data can be created using:
- The same augmentation method (via Faker and Real-world data ).

5. Prediction and Accuracy Evaluation
-------------------------------------
Use the prediction script to:
- Run inference on the unseen test data.
- Calculate prediction accuracy metrics.

6. HMM-Based Masking and State Generation
-----------------------------------------
Use the provided HMM transition masking code to:
- Mask the predicted sequences.
- Generate HMM state sequences from the masked data.

7. Privacy Risk Calculation (Forward Algorithm)
-----------------------------------------------
Apply the forward algorithm to calculate the privacy risk of any desired sequence.

Additional Notes
----------------
- All datasets used for training and evaluation are stored in the respective data folders.
- The data is preprocessed to remove any noisy or extra words.
- Both our system and Exsence use identical datasets to ensure consistency in benchmarking.

