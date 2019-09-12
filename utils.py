import tensorflow as tf
import mne
import numpy as np
from transforms import *


def zscore(data, axis=-1):
    return tf.math.divide_no_nan(
        tf.math.subtract(data, tf.reduce_mean(data, axis=axis, keepdims=True)),
        tf.math.reduce_std(data, axis=axis, keepdims=True)
    )


def dataset_concat(*ds):
    dataset = ds[0]
    assert isinstance(dataset, tf.data.Dataset)
    for d in ds[1:]:
        assert isinstance(d, tf.data.Dataset)
        dataset.concatenate(d)
    return dataset


def labelled_dataset_concat(*datasets):
    """
    Concatenates all the datasets provided into one Dataset with an additional label corresponding to its original
    source dataset. Can be used for multi-subject and multi-run datasets, providing concatenation with identification.
    For example: datasets by subject. If the datasets were previously (x_i, label_i) for all i, they now load (x_i,
    label_i, subject_j) for all J subjects with I epochs each.
    :param datasets:
    :return: concatenated datasets;
    """
    new_datasets = []
    for i, ds in enumerate(datasets):
        assert isinstance(ds, tf.data.Dataset)
        new_datasets.append(ds.map(
            lambda *x: (*x, tf.constant(i)), num_parallel_calls=tf.data.experimental.AUTOTUNE))
    for ds in new_datasets[1:]:
        new_datasets[0] = new_datasets[0].concatenate(ds)
    return new_datasets[0]





