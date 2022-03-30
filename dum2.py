import os
from pathlib import Path
import pandas as pd
print(os.getcwd())


# for i in os.listdir(Path(Path.cwd(), 'Datapipe', 'raw_data', 'images')):
#     print(i)

ld = [{'a': 1, 'b': 2}, {'a': 3, 'b': 4}]

l1 = [1,2,3]
d1 = pd.DataFrame(data = {'c2': [1,2,3], 'c3': [3,4,5]})
print(len(d1))
print(len(l1))

l1 = ["G06 WTR", "WL11 WFL", "QW68 PQR"]
l2 = [i.split() for i in l1]
print(l2)
l3 = [int(i[0][-2:]) for i in l2]
print(l3)