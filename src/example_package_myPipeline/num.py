import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def num_var_info(df):

    # Description
    # show the general information for all numeric columns in the data frames

    # Input
    # df: the pandas data frame to show numeric variables

    for column in df.columns:
        if (df[column].dtype!=object):
            print(f'Column name: {column}\n\tMax: {df[column].max()}\n\tMin: {df[column].min()}\n\tRange:{df[column].max()-df[column].min()}\n\tMean:{df[column].mean()}', end='\n\n')
        
def num_var_dist(df):

    # Description
    # plot the value distribution for numeric columns in the data frame
    
    # Input
    # df: the pandas data frame to plot distribution

    counter = 1
    for column in df.columns:
        if (df[column].dtype!=object):
            plt.figure(counter)
            sns.histplot(df[column])
            counter += 1