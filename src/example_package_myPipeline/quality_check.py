import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def num_var_info(df):

    # Description
    # show the general information for all numeric columns in the data frames

    # Input
    # df: the pandas data frame to show numeric variables
    
    res = df.describe()
    res.loc['range'] = res.loc['max',:]-res.loc['min',:]
    return res
        
def num_var_dist(df, mode="subplot"):

    # Description
    # plot the value distribution for numeric columns in the data frame
    
    # Input
    # df: the pandas data frame to plot distribution
    # mode: the mode to plot out these distribution, can be "subplot" or "plot"
    #   plot: plot each distribution one by one
    #   subplot: plot the distributions in a subplot
    
    counter = 1
    if mode=="subplot":
        plt.figure(figsize=(10,10))
        fig_num = int(np.ceil(np.sqrt(len([column for column in df.columns if df[column].dtype!=object]))))
        for column in df.columns:
            plt.subplot(fig_num, fig_num, counter)
            if (df[column].dtype!=object):
                sns.histplot(df[column])
                counter += 1
    elif mode=="plot":
        for column in df.columns:
            if (df[column].dtype!=object):
                plt.figure(counter)
                sns.histplot(df[column])
                counter += 1
    else:
        raise ValueError("Wrong Parameter")
    
def cat_var_info(df):

    # Description
    # show the general information for all categorical columns in the data frames

    # Input
    # df: the pandas data frame to show general information of categorical variables

    col_num = len([column for column in df.columns if df[column].dtype==object])
    report = []
    counter = 0
    for column in df.columns:
        if df[column].dtype==object:
            report.append([column, len(df[column].unique())])
    return pd.DataFrame(report, columns=['column_name', 'number_of_category'])

def cat_var_vis(df, mode='subplot', max_category_num=10, label_distance=1.5):

    # Description
    # plot the pie chart for categorical columns in the data frame to show the percentage of each category

    # Input
    # df: the pandas data frame to plot pie chart of categorical variables
    # max_category_num: only the categorical variables that has category numbers less than this parameter would be plot out
    # label_distance: the distance between category label
    # mode: the mode to plot out these distribution, can be "subplot" or "plot"
    #   plot: plot each distribution one by one
    #   subplot: plot the distributions in a subplotq


    counter = 1
    if mode=="subplot":
        plt.figure(figsize=(15,15))
        fig_num = int(np.ceil(np.sqrt(len([column for column in df.columns if df[column].dtype==object and len(df[column].unique()) < max_category_num]))))
        for column in df.columns:
            if (df[column].dtype==object) and len(df[column].unique()) < max_category_num:
                plt.subplot(fig_num, fig_num, counter)
                plt.pie(df[column].value_counts(), labels=df[column].value_counts().index, labeldistance=label_distance)
                plt.legend(bbox_to_anchor=(0.2,0.2))
                plt.title(column)
                counter+=1
    elif mode=="plot":
        for column in df.columns:
            if (df[column].dtype==object) and len(df[column].unique()) < max_category_num:
                plt.figure(counter)
                plt.pie(df[column].value_counts(), labels=df[column].value_counts().index, labeldistance=label_distance)
                plt.legend(bbox_to_anchor=(0.2,0.2))
                plt.title(column)
                counter+=1
    else:
        raise ValueError("Wrong Parameter")
    
def value_counts_sort(df, column, row_index_start=0, row_index_end=10, orderby="frequency"):

    # Description
    # For a given categorical column in a data frame, show its value count in frequency order or alphabetic order

    # Input
    # df: the data frame that contains the target categorical column
    # column: the name of target categorical column
    # row_index_start: the start row index of the value count series
    # row_index_end: the end row index of the value count series
    # order_by: determine the value count series is ordered by frequency or alphabetic order

    if (orderby=="frequency"):
        print("Sort By Frequency Order: ")
        return df[column].value_counts().sort_values(ascending=False)[row_index_start:row_index_end]
    elif (orderby=="alphabetic"):
        print("Sort By Alphabetic Order: ")
        return df[column].value_counts().sort_index()[row_index_start:row_index_end]

def show_outlier(df, column, deviation=2):

    # Description
    # For a given numeric column in a data frame, show the index and value of the outliers in this column

    # Input
    # df: the data frame that contains the target numeric column
    # column: the name of target numeric column
    # deviation: the number of std that determine the value is outlier or not

    print(f'Column name: {column}\n\tMax: {df[column].max()}\n\tMin: {df[column].min()}\n\tRange:{df[column].max()-df[column].min()}\n\tMean:{df[column].mean()}', end='\n\n')
    print(f'Number of Outliers: {len(df[column][abs(df[column] - np.mean(df[column]))>deviation*np.std(df[column])])}')
    print(f'Index\tValue', end='')
    return df[column][abs(df[column] - np.mean(df[column]))>deviation*np.std(df[column])]

def missing_value_report(df):
    
    # Description
    # print out the missing value report
    
    # Input
    # df: the Pandas Data Frame to report missing value
    
    print("Column Name\tMissing Count")
    return np.sum(df.isnull())[np.sum(df.isnull())!=0]

def handle_missing(df, method="drop"):

    # description
    # handle the missing value in the data frame with the method indicated
    # for forward and backward fill, the function assumed data frame is in the sorted order
    # for numeric imputation it would ony replace the NaN value in column that contains int or float data type

    # input
    # df: the data frame contains NaN values
    # method: the method to handle NaN values, potential options including "drop", "mean", "median", "mode", "forward", "backward"

    if method=="drop":
        return df.dropna()
    elif method=="forward":
        return df.fillna(method='ffill')
    elif method=="backward":
        return df.fillna(method='bfill')

def num_impute(df, column, method="mean"):

    # description
    # given a numeric column from a data frame, impute all the NaN value in the data frame with the mean, median or mood of this column

    # input
    # df: the data frame contains numeric column and NaN values
    # column: which column of the data frame to impute
    # method: impute the NaN value to mean, median or mood

    if method=="mean":
        return df[column].replace(np.nan, np.nanmean(df[column]))
    elif method=="median":
        return df[column].replace(np.nan, np.nanmedian(df[column]))
    elif method=="mood":
        return df[column].replace(np.nan, df[column].value_counts().index[0])

