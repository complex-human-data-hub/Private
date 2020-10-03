from __future__ import print_function
import numpy as np
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt
from datetime import datetime
import json
import os

np.set_printoptions(precision=4)


def debug_logger(msg):
    with open("/tmp/manifold-privacy.log", "a") as fp:
        if not isinstance(msg, str):
            msg = json.dumps(msg, indent=4, default=str)
        timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        fp.write("[{}][{}] {}\n".format(timestamp, os.getpid(), msg))


def dist_manifold(s_minus, s_all, return_all=False):
    n = s_minus.shape[0]
    if len(s_minus.shape) == 1:
        s_minus = np.reshape(s_minus, (n, 1))
    m = s_all.shape[0]
    if len(s_all.shape) == 1:
        s_all = np.reshape(s_all, (m, 1))
    diff = cdist(s_all, s_minus)
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
            place = same[same_index]
            gap = temp_gap
            gap_same_index = same_index
            gap_diff_index = diff_index
    if return_all:
        return gap * 1.0 / (n * m), place, gap, gap_same_index, gap_diff_index, same, diff
    else:
        return gap * 1.0 / (n * m)


def plot_distances(x, y):
    prob_gap, place, gap, gap_same_index, gap_diff_index, same, diff = dist_manifold(x, y, return_all=True)
    fig, ax = plt.subplots()
    ax.plot(diff, range(len(diff)), label="Diff")
    ax.plot(same, range(len(same)), label="Same")
    ax.plot([place, place], [gap_same_index, gap_diff_index], label="Gap")
    ax.set(xlabel="Distance", ylabel="Count")
    ax.legend(loc="upper left")
    ax.margins(0.1)
    plt.show()


# if __name__ == "__main__":
#     N = 1000
#     s_all = normal(0, 1, N)
#     s_minus = normal(0.1, 1, N)
#     print("Prob gap %1.4f%%" % (dist_manifold(s_all, s_minus) * 100.0))
#     plot_distances(s_all, s_minus)
