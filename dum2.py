import os
from pathlib import Path
print(os.getcwd())


for i in os.listdir(Path(Path.cwd(), 'Datapipe', 'raw_data', 'images')):
    print(i)