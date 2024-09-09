import numpy as np
import pandas as pd
from typing import Callable
import tensorflow as tf
from torch_dataset import TorchDataset

'''
This class is a wrapper around a pandas DataFrame that provides a set of functions to manipulate the dataset.

'''


class ODEDataset:

    def __init__(self, name: str, df: pd.DataFrame | None = None):
        self._df: pd.DataFrame | None = df
        self.name = name

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

    def from_excel(self, path: str, sheet_name: str = 0, **kwargs):
        self._df = pd.read_excel(path, sheet_name=sheet_name, **kwargs)
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

        new_df = modifier(self._df)
        if new_df is None:
            raise ValueError("Modifier function should return a DataFrame")
        return ODEDataset(self.name, new_df)

    # Mergers
    #  Add another Dataset

    def concat(self, other: 'ODEDataset'):
        if self._df is None or other._df is None:
            raise ValueError("Dataset has not been initialized")

        cols = set(self.get_columns())
        other_cols = set(other.get_columns())

        if len(cols.difference(other_cols)) > 0:
            raise ValueError(f"Columns do not match: {cols} != {other_cols}")

        other_df = other.to_dataframe()
        self._df = pd.concat([self._df, other_df])
        return self

    def merge(self, other: 'ODEDataset', on: [str], how: str = 'inner'):
        if self._df is None or other._df is None:
            raise ValueError("Dataset has not been initialized")

        cols = set(self.get_columns())
        other_cols = set(other.get_columns())

        if len(cols.difference(other_cols)) > 0:
            raise ValueError(f"Columns do not match: {cols} != {other_cols}")

        self._df = self._df.merge(other.to_dataframe(), on=on, how=how)
        return self




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
