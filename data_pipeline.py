import os
import sys

sys.path.append("./")  # Adds higher directory to python modules path.
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

from core.ODEDataset import ODEDataset
from utils import cleaning
from collections import Counter


def add_one_hot_encoding(dataset: ODEDataset):
    categorized_features = ['Education_level_HHH',
                            'Socio_status_HHH',
                            'Tariff_payment_frequency',
                            'HH_with_home_business',
                            'Ownership_motorized_vehicle',
                            'Ownership_small_livestock',
                            'Ownership_large_livestock',
                            'Clean_fuel',
                            ]
    for feature in categorized_features:
        dataset = dataset.apply(cleaning.add_one_hot_encoding(feature))
    return dataset



def create_dataset(output: str,
                   features,
                   path="./playground/data/combined_dataset_cleaned.csv", 

                   ):
    dataset = ODEDataset("combined_dataset_cleaned")
    dataset.from_csv(path)
    dataset = add_one_hot_encoding(dataset)
    dataset = dataset.apply(cleaning.remove_row(output, -1))
    return dataset.to_numpy(features, [output])


    
def get_class_distribution(data):

    # Extract all labels from the dataset
    all_labels = []

    for _, label in data:  # Iterate over the dataset
        all_labels.append(label.numpy())  # Convert label tensors to NumPy arrays

    # Flatten the list in case labels are multi-dimensional
    all_labels = [i[0] for k in all_labels for i in list(k)]
    # Count occurrences of each label
    label_counts = Counter(all_labels)

    # Calculate the ratio for each label
    total_samples = sum(label_counts.values())
    label_ratios = {label: count / total_samples for label, count in label_counts.items()}

    # Print out the labels and their ratios
    print("Label Counts:", label_counts)
    print("Label Ratios:", label_ratios)

