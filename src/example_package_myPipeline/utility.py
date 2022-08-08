import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def read_file(path, orient=None):

    # Description
    # read CSV or JSON files to create a Pandas Data Frame object

    # Input
    # path: the file path to read
    # orient: if it is a JSON file, choose the orient to ready it, potential option: "split", "records", "index", columns
    
    if path[-4:]=='.csv':
        return pd.read_csv(path)
    elif path[-5:]=='.json':
        return pd.read_json(path, orient=orient)
    else:
        print("Unrecognized file type")