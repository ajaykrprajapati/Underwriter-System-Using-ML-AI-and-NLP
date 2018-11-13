# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np


def visualize(vect, Xtr, X, y):
	li = vect.vocabulary_
	print(Xtr.shape)
	labels = li.keys()
	values = li.values()
	indexes = np.arange(len(labels))

	bar_width = 0.35

	plt.bar(indexes, values)

	# add labels
	plt.xticks(indexes + bar_width, labels)
	plt.show()
	j = input()
