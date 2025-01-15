## Different Number of Blocks

### Config A

-   Each with 64 Units
-   Dropout 0.4
-   Regularization 0.01
-   Starting Learning Rate 0.001
-   Batch Size 128
-   Patience 100

**Results:**

| # Blocks | # Epochs | AUC           | Precision   | Recall       | F1 Score    |
| -------- | -------- | ------------- | ----------- | ------------ | ----------- |
| 2        | 168      | 0.949 - 0.935 | 0.83 - 0.81 | 0.98 - 0.96  | 0.90 - 0.88 |
| 4        | 285      | 0.945 - 0.93  | 0.83 - 0.81 | 0.98 - 0.96  | 0.90 - 0.88 |
| 8        | 394      | 0.94 - 0.92   | 0.83 - 0.81 | 0.98 - 0.97  | 0.90 - 0.89 |
| 16       | 266      | 0.921 - 0.919 | 0.82 - 0.82 | 0.947 - 0.95 | 0.88 - 0.88 |

### Config B

-   Each with 128 Units
-   Dropout 0.4
-   Regularization 0.01
-   Starting Learning Rate 0.001
-   Batch Size 256
-   Patience 100

**Results:**

| # Blocks | # Epochs | AUC          | Precision   | Recall      | F1 Score    |
| -------- | -------- | ------------ | ----------- | ----------- | ----------- |
| 2        | 261      | 0.95 - 0.934 | 0.84 - 0.83 | 0.98 - 0.95 | 0.90 - 0.88 |
| 4        | 164      | 0.95 - 0.94  | 0.83 - 0.81 | 0.98 - 0.97 | 0.90 - 0.88 |
| 8        | 161      | 0.94 - 0.93  | 0.83 - 0.81 | 0.98 - 0.97 | 0.90 - 0.88 |
| 16       | 215      | 0.93 - 0.92  | 0.81 - 0.80 | 0.96 - 0.96 | 0.88 - 0.87 |

> Summary: The best results were obtained with 8 blocks, Config B, is the best configuration for this dataset.

We can also shift the classification threshold to improve the result further

# Final Results

The model with Config B and 8 Blocks was selected as the best model. The final results are:

> we get the values from the classification rebort , using the `macro` avg

## Training

| Appliance              | AUC  | Precision | Recall | F1 Score | F2 Score | Accuracy | Postive samples percentage |
| ---------------------- | ---- | --------- | ------ | -------- | -------- | -------- | -------------------------- |
| Iron                   | 0.95 | 0.91      | 0.90   | 0.90     | 0.89     | 0.90     | 0.23                       |
| DVD Player             | 0.95 | 0.92      | 0.91   | 0.91     | 0.91     | 0.91     | 0.10                       |
| TV                     | 0.97 | 0.92      | 0.91   | 0.91     | 0.91     | 0.91     | 0.16                       |
| Fan                    | 0.98 | 0.92      | 0.91   | 0.91     | 0.91     | 0.91     | 0.26                       |
| Refrigerator / Freezer | 0.97 | 0.93      | 0.93   | 0.93     | 0.93     | 0.93     | 0.13                       |
| Radio / Stereo         | 0.90 | 0.85      | 0.81   | 0.80     | 0.80     | 0.81     | 0.20                       |
| Phone Charger          | 0.95 | 0.86      | 0.85   | 0.85     | 0.85     | 0.85     | 0.22                       |

## Validation

| Appliance              | AUC  | Precision | Recall | F1 Score | F2 Score | Accuracy | Postive samples percentage |
| ---------------------- | ---- | --------- | ------ | -------- | -------- | -------- | -------------------------- |
| Iron                   | 0.93 | 0.88      | 0.87   | 0.87     | 0.87     | 0.87     | 0.24                       |
| DVD Player             | 0.93 | 0.89      | 0.89   | 0.89     | 0.89     | 0.89     | 0.11                       |
| TV                     | 0.96 | 0.89      | 0.89   | 0.89     | 0.89     | 0.89     | 0.17                       |
| Fan                    | 0.97 | 0.92      | 0.91   | 0.91     | 0.91     | 0.91     | 0.26                       |
| Refrigerator / Freezer | 0.96 | 0.89      | 0.89   | 0.89     | 0.89     | 0.89     | 0.14                       |
| Radio / Stereo         | 0.89 | 0.84      | 0.80   | 0.79     | 0.79     | 0.80     | 0.20                       |
| Phone Charger          | 0.94 | 0.83      | 0.81   | 0.81     | 0.81     | 0.81     | 0.23                       |

## Testing

| Appliance              | AUC  | Precision | Recall | F1 Score | F2 Score | Accuracy | Postive samples percentage |
| ---------------------- | ---- | --------- | ------ | -------- | -------- | -------- | -------------------------- |
| Iron                   | 0.93 | 0.79      | 0.88   | 0.80     | 0.84     | 0.83     | 0.13                       |
| DVD Player             | 0.93 | 0.72      | 0.89   | 0.76     | 0.82     | 0.87     | 0.27                       |
| TV                     | 0.96 | 0.77      | 0.90   | 0.80     | 0.85     | 0.86     | 0.21                       |
| Fan                    | 0.97 | 0.83      | 0.91   | 0.85     | 0.88     | 0.87     | 0.24                       |
| Refrigerator / Freezer | 0.95 | 0.80      | 0.88   | 0.83     | 0.86     | 0.91     | 0.21                       |
| Radio / Stereo         | 0.90 | 0.73      | 0.82   | 0.72     | 0.76     | 0.74     | 0.09                       |
| Phone Charger          | 0.95 | 0.83      | 0.83   | 0.83     | 0.83     | 0.89     | 0.20                       |

## Average

| Appliance  | AUC  | Precision | Recall | F1 Score | F2 Score | Accuracy |
| ---------- | ---- | --------- | ------ | -------- | -------- | -------- |
| Training   | 0.95 | 0.90      | 0.89   | 0.89     | 0.89     | 0.89     |
| Validation | 0.94 | 0.88      | 0.87   | 0.86     | 0.86     | 0.87     |
| Testing    | 0.94 | 0.78      | 0.87   | 0.80     | 0.83     | 0.85     |

### Reasons for poor precision

-   The model is not able to learn the patterns of the appliance because of the missing features and imbalanced data.
-   The model is not complex enough to learn the patterns of the appliance.
-   The model is overfitting the training data.
-   While precision is poor, the AUC is high, which means the model is able to differentiate between the classes, but the threshold is not optimal.

