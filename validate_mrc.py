import warnings
import mrcfile
import numpy as np
import sys

def validate_mrc(file):
    with warnings.catch_warnings(record=True) as w:
        with  mrcfile.open(file, permissive=True) as f:
            data = f.data
    
    return np.isnan(data).any()

if __name__ == "__main__":

    print(not validate_mrc(sys.argv[1]))