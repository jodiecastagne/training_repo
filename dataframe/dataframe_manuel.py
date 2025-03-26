import pandas as pd
import re
import os
import glob
from pathlib import Path
import numpy as np
import re

def main():
    path = r'C:\ecg\rr_ceinture'

    # Get the files from the path provided in the OP
    files = Path(path).glob('*.csv')  # .rglob to get subdirectories
    df = pd.concat((pd.read_csv(f).assign(filename=f.stem) for f in files), ignore_index=True)
    id = []
    files = Path(path).glob('*.csv')  # .rglob to get subdirectories
    for f in files:
        #m = re.search(r'ecg_([0-9]+).csv', str(f))
        m = re.search("([0-9]+)", str(f))
        id.append(m.group(0))
    print(id)
    # print(df.head())
    # Z = df.loc[['10517002']]['timestamp_machine']


if __name__ == '__main__':
    main()