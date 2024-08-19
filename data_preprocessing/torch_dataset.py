from torch.utils.data import Dataset
import numpy as np
import torch


class TorchDataset(Dataset):
    def __init__(self, features: np.ndarray, target: np.ndarray):
        self._features = features
        self._target = target
        self._data_len = len(features)
        target_len = len(target)
        if self._data_len != target_len:
            raise ValueError(f"The number of features ({self._data_len}) and targets ({target_len}) must be the same")

    def __len__(self):
        return self._data_len

    def __getitem__(self, index):
        x = torch.tensor(self._features, dtype=torch.float32)
        y = torch.tensor(self._target, dtype=torch.float32)
        return x, y
