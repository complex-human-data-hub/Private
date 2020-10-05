from __future__ import print_function
import numpy as np
from scipy.spatial.distance import cdist

np.set_printoptions(precision=4)


def dist_manifold(s_user, s_all):
    """
    Calculate the maximum distance between s_user and s_all

    :param s_user:
    :param s_all:
    :return: distance
    """
    n = s_user.shape[0]
    if len(s_user.shape) == 1:
        s_user = np.reshape(s_user, (n, 1))
    m = s_all.shape[0]
    if len(s_all.shape) == 1:
        s_all = np.reshape(s_all, (m, 1))
    diff = cdist(s_all, s_user)
    diff = diff.flatten()
    diff = np.sort(diff)
    same = cdist(s_all, s_all)
    same = same.flatten()
    same = np.sort(same)

    gap = 0.
    same_index = 0
    diff_index = 0
    while diff_index < n * m - 1 and same_index < n * n - 1:
        while same[same_index] <= diff[diff_index] and same_index < n * n - 1:
            same_index += 1
        while same[same_index] > diff[diff_index] and diff_index < n * m - 1:
            diff_index += 1
        if diff_index >= n * m:
            break
        if same_index >= n * n:
            break
        temp_gap = np.abs(same_index - diff_index)
        if temp_gap > gap:
            gap = temp_gap
    else:
        return gap * 1.0 / (n * m)
