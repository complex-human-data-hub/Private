import numpy as np
from numpy.random import uniform, normal, randint
import sys
from scipy.stats import norm
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt


np.set_printoptions(precision=4)


def distManifold(X, Y, returnAll=False):

  N = X.shape[0]
  M = Y.shape[0]
  diff = cdist(Sall, Sminus)
  diff = diff.flatten()
  diff = np.sort(diff)
  same = cdist(Sall, Sall)
  same = same.flatten()
  same = np.sort(same)

  gap = 0.
  sameIndex = 0
  diffIndex = 0
  while diffIndex < N*M-1 and sameIndex < N*N-1:
    while same[sameIndex] <= diff[diffIndex] and sameIndex < N*N-1:
      sameIndex += 1
    while same[sameIndex] > diff[diffIndex] and diffIndex < N*M-1:
      diffIndex += 1
    if diffIndex >= N*M:
      break
    if sameIndex >= N*N:
      break
    tempGap = np.abs(sameIndex - diffIndex)
    if tempGap > gap:
      place = same[sameIndex]
      gap = tempGap
      gapSameIndex = sameIndex
      gapDiffIndex = diffIndex
  if returnAll:
    return((gap*1.0/(N*M), place, gap, gapSameIndex, gapDiffIndex, same, diff))
  else:
    return(gap*1.0/(N*M))


def plotDistances(X, Y):
  probGap, place, gap, gapSameIndex, gapDiffIndex, same, diff = distManifold(X, Y, returnAll=True)
  fig, ax = plt.subplots()
  ax.plot(diff, range(len(diff)), label="Diff")
  ax.plot(same, range(len(same)), label="Same")
  ax.plot([place, place], [gapSameIndex, gapDiffIndex], label="Gap")
  ax.set(xlabel="Distance", ylabel = "Count")
  ax.legend(loc="upper left")
  ax.margins(0.1)
  plt.show()

N = 1000
Sall = normal(0, 1, (N, 1))
Sminus = normal(1, 1, (N, 1))
print "Prob gap %1.4f%%" % distManifold(Sall, Sminus)
plotDistances(Sall, Sminus)
