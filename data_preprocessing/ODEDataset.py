import numpy as np
import pandas as pd
from typing import Callable
import tensorflow as tf
from torch_dataset import TorchDataset

'''
This class is a wrapper around a pandas DataFrame that provides a set of functions to manipulate the dataset.

'''
class ODEDataset:

    def __init__(self):
        self._df: pd.DataFrame | None = None

    # importers
    '''
    This function reads a csv file and stores it in the dataset object.
    Args:
        path (str): The path to the csv file
        low_memory (bool): Whether to use low memory mode when reading the csv file
        **kwargs: Additional keyword arguments to pass to pd.read_csv
    Returns:
        ODEDataset: The current ODEDataset
        
    '''

    def from_csv(self, path: str, low_memory: bool = False, **kwargs):
        self._df = pd.read_csv(path, low_memory=low_memory, **kwargs)
        return self

    # Modifiers
    '''
    This function applies a modifier function to the dataset.
    Args:
        modifier (Callable[[pd.DataFrame], pd.DataFrame]): The modifier function to apply
    Returns:
        ODEDataset: The current ODEDataset
    '''

    def apply(self, modifier: Callable[[pd.DataFrame], pd.DataFrame]):
        if self._df is None:
            raise ValueError("Dataset has not been initialized")

        self._df = modifier(self._df)
        return self

    # Mergers
    #  Add another Dataset

    # Exporters
    #     to csv
    def to_dataframe(self):
        return self._df

    def to_tf_dataset(self, x_columns: [str], y_columns: [str]):
        if self._df is None:
            raise ValueError("Dataset has not been initialized")

        x: np.ndarray = self._df[x_columns].to_numpy(dtype=np.float32)
        y: np.ndarray = self._df[y_columns].to_numpy(dtype=np.float32)

        return tf.data.Dataset.from_tensor_slices((x, y), name="ODEDataset")

    def to_csv(self, path: str, **kwargs):
        self._df.to_csv(path, **kwargs)
        return self

    def to_torch_dataset(self, x_columns: [str], y_columns: [str]):
        if self._df is None:
            raise ValueError("Dataset has not been initialized")

        x: np.ndarray = self._df[x_columns].to_numpy(dtype=np.float32)
        y: np.ndarray = self._df[y_columns].to_numpy(dtype=np.float32)
        return TorchDataset(x, y)

    # Getters
    def get_columns(self):
        return self._df.columns.tolist()
