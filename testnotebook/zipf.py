'''import os

cwd = os.getcwd()
print(cwd)
files = os.listdir(cwd)
for i in files:
    print(i)'''
import re
from typing import Iterator

import matplotlib.pyplot as plt

with open("shakespeare.txt", "r") as f:
    lines = f.readlines()
    import numpy as np

word_map = {}
for line in lines:
    line_array = re.split('\w+', line)
    line_array = list(filter(lambda x: len(x) > 0, line_array))
    # print(line_array)
    for word in line_array:
        try:
            word_map[word] = word_map[word] + 1
        except KeyError:
            word_map[word] = 1
'''for i in range(10):
    print(lines[i])'''

word_map_sorted: Iterator[str] = reversed(sorted(word_map, key=word_map.__getitem__))
total = 0
print(word_map.items)
ind = 0
ind_list = []
val_list = []
for word in word_map_sorted:
    # print("{}:{}".format(word,word_map[word]))
    total = total + word_map[word]
word_map_sorted = reversed(sorted(word_map, key=word_map.__getitem__))
for word in word_map_sorted:
    ind_list.append(ind)
    val_list.append(word_map[word])
    ind = ind + 1
    if ind >= 200:
        break
print(val_list)
print("Total words: {}".format(total))
plt.plot(ind_list, val_list, 'ro')
plt.axis([0, len(ind_list), 0, val_list[1] + 10])
plt.show()
