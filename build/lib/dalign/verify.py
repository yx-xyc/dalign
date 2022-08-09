import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def num_var_info(df):
    """    
    Show statistics for all the numerical columns in the DataFrame.

    Parameters
    ----------
    df : DataFrame
        The DataFrame contains numerical columns to show statistics. The statistics are: 
        count, mean, std, min, 25%, 50%, 75%, max, and range.

    Returns
    -------
    res : DataFrame
        The DataFrame with the numerical column name as title, and statistics as index.
    """
    res = df.describe()
    res.loc['range'] = res.loc['max',:]-res.loc['min',:]
    return res

def num_var_dist(df, mode='subplot'):
    """    
    Plot the value distributions of all numeric columns in the given DataFrame. 
    The plots can be shown one by one or as subplots of a figure.
    
    Parameters
    ----------
    df : DataFrame
        The DataFrame contains numerical columns to plot value distributions.    
    mode : string
        The mode that decides how these plots are shown. The set of possible mode is:
        'subplot' : show all the plots as subplots of a figure.
        'plot' : show all the plots one by one.
    """
    counter = 1
    if (mode=='subplot'):
        plt.figure(figsize=(10,10))
        fig_num = int(np.ceil(np.sqrt(len([column for column in df.columns if df[column].dtype!=object]))))
        for column in df.columns:
            plt.subplot(fig_num, fig_num, counter)
            if (df[column].dtype!=object):
                sns.histplot(df[column])
                counter += 1
    elif (mode=='plot'):
        for column in df.columns:
            if (df[column].dtype!=object):
                plt.figure(counter)
                sns.histplot(df[column])
                counter += 1
    else:
        raise ValueError("Wrong Parameter")

def show_outlier(df, column, deviation=2):
    """    
    For a given numerical column in a DataFrame, show statistics of this column, 
    number of outliers and all the indexes and values of the outliers 
    that have deviation larger than the given deviation in this column.

    Parameters
    ----------
    df : DataFrame
        The DataFrame that contains the target numeric column.
    column : str
        The name of target numeric column.
    deviation : float
        The threshold of deviation that determines whether a value is outlier or not.

    Returns
    -------
     : Series
        The Series with the outliers' indexes as index and outliers' values as value.
    """
    print(f'Column name: {column}\n\tMax: {df[column].max()}\n\tMin: {df[column].min()}\n\tRange:{df[column].max()-df[column].min()}\n\tMean:{df[column].mean()}', end='\n\n')
    print(f'Number of Outliers: {len(df[column][abs(df[column] - np.mean(df[column]))>deviation*np.std(df[column])])}')
    print(f'Index\tValue', end='')
    return df[column][abs(df[column] - np.mean(df[column]))>deviation*np.std(df[column])]

def cat_var_type_counts(df):
    """
    Given a DataFrame, for all the categorical columns, show how many categories are in each column.

    Parameters
    ----------
    df : DataFrame
        The DataFrame that contains categorical columns.
    
    Returns
    -------
     : DataFrame
        The DataFrame contains the categorical column names and the number of category types in each column.
    """
    col_num = len([column for column in df.columns if df[column].dtype==object])
    report = []
    counter = 0
    for column in df.columns:
        if (df[column].dtype==object):
            report.append([column, len(df[column].unique())])
    return pd.DataFrame(report, columns=['column_name', 'number_of_category_type'])

def cat_var_vis(df, mode='subplot', max_category_num=10, label_distance=1.5):
    """
    Plot the pie charts for categorical columns in the DataFrame to show the percentage of each category.

    Parameters
    ----------
    df : DataFrame
        The pandas DataFrame that contains categorical columns to plot pie chart.
    max_category_num : int
        The maximum number of categories a column have for the column to be plot.
        This parameter is to avoid to plot the column contains all different strings instead of categories.
    label_distance : float
        The distance between category labels.
    """
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

def cat_counts_sort(df, column, row_index_start=0, row_index_end=10, orderby="frequency", ascending=True):
    """
    For a given categorical column in DataFrame, show its value counts 
    in frequency order or alphabetic order in the given index range.

    Parameters
    ----------
    df : DataFrame
        The DataFrame that contains the target categorical column.
    column : str
        The name of target categorical column.
    row_index_start : int
        The start row index of the value count series.
    row_index_end : int
        The end row index of the value count series.
    order_by : str, default 'frequency'
        Decides how value counts Series are ordered. The set of possible order_by value is:
        'frequency' : show all the plots as subplots of a figure.
        'alphabetic' : show all the plots one by one.
    ascending : bool, default True
        Decides whether the value counts Series is in ascending order or descending order.
    
    Returns
    -------
     : Series
        The Series with categories as index and category counts as values in the given index range
        sorted by the given order.
    """
    if (orderby=="frequency"):
        print("Sort By Frequency Order: ")
        return df[column].value_counts().sort_values(ascending=ascending)[row_index_start:row_index_end]
    elif (orderby=="alphabetic"):
        print("Sort By Alphabetic Order: ")
        return df[column].value_counts().sort_index(ascending=ascending)[row_index_start:row_index_end]
    else:
        raise ValueError("Wrong Parameter")