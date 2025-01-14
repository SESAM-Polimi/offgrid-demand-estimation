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
-   Dropout 0.3
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

## Training

| Appliance              | AUC  | Precision | Recall | F1 Score | F2 Score | Accuracy |
| ---------------------- | ---- | --------- | ------ | -------- | -------- | -------- |
| Iron                   | 0.95 | 0.83      | 0.99   | 0.90     | 0.95     | 0.89     |
| TV                     | 0.97 | 0.90      | 0.96   | 0930     | 0.95     | 0.93     |
| DVD Player             | 0.0  | 0.0       | 0.0    | 0.0      | 0.0      | 0.0      |
| Fan                    | 0.0  | 0.0       | 0.0    | 0.0      | 0.0      | 0.0      |
| Refrigerator / Freezer | 0.0  | 0.0       | 0.0    | 0.0      | 0.0      | 0.0      |
| Radio / Stereo         | 0.0  | 0.0       | 0.0    | 0.0      | 0.0      | 0.0      |
| Phone Charger          | 0.0  | 0.0       | 0.0    | 0.0      | 0.0      | 0.0      |

## Validation

| Appliance              | AUC   | Precision | Recall | F1 Score | F2 Score | Accuracy |
| ---------------------- | ----- | --------- | ------ | -------- | -------- | -------- |
| Iron                   | 0.93  | 0.81      | 0.96   | 0.88     | 0.93     | 0.87     |
| TV                     | 0.096 | 0.88      | 0.92   | 0.90     | 0.91     | 0.90     |
| DVD Player             | 0.0   | 0.0       | 0.0    | 0.0      | 0.0      | 0.0      |
| Fan                    | 0.0   | 0.0       | 0.0    | 0.0      | 0.0      | 0.0      |
| Refrigerator / Freezer | 0.0   | 0.0       | 0.0    | 0.0      | 0.0      | 0.0      |
| Radio / Stereo         | 0.0   | 0.0       | 0.0    | 0.0      | 0.0      | 0.0      |
| Phone Charger          | 0.0   | 0.0       | 0.0    | 0.0      | 0.0      | 0.0      |

## Testing

| Appliance              | AUC  | Precision | Recall | F1 Score | F2 Score | Accuracy |
| ---------------------- | ---- | --------- | ------ | -------- | -------- | -------- |
| Iron                   | 0.93 | 0.78      | 0.88   | 0.83     | 0.86     | 0.83     |
| TV                     | 0.97 | 0.81      | 0.90   | 0.85     | 0.88     | 0.90     |
| DVD Player             | 0.0  | 0.0       | 0.0    | 0.0      | 0.0      | 0.0      |
| Fan                    | 0.0  | 0.0       | 0.0    | 0.0      | 0.0      | 0.0      |
| Refrigerator / Freezer | 0.0  | 0.0       | 0.0    | 0.0      | 0.0      | 0.0      |
| Radio / Stereo         | 0.0  | 0.0       | 0.0    | 0.0      | 0.0      | 0.0      |
| Phone Charger          | 0.0  | 0.0       | 0.0    | 0.0      | 0.0      | 0.0      |

