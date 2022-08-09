import numpy as np
import pandas as pd

def missing_val_info(df):
    """    
    Show the DataFrame with the column has missing value as index and the missing counts 
    and missing percent of each column.
    
    Parameters
    ----------
    df : DataFrame
        The DataFrame to report missing values.

    Returns
    -------
    res : DataFrame
        The DataFrame that reports missing values.
    """
    res = pd.DataFrame(np.sum(df.isnull())[np.sum(df.isnull())!=0], columns=["Missing"])
    res['Missing Percent %'] = res['Missing']/df.shape[0]
    return res

def handle_missing(df, method="drop"):
    """
    Handle the missing value in the DataFrame with the method indicated. 

    Parameters
    ----------
    df : DataFrame
        The DataFrame contains NaN valuess
    method : str
        The method to handle NaN values. The set of potential methods is:
        'drop' : drop all the rows that contains NaN value.
        'forward' : replace NaN value with the last value in the column.
        'backward' : replace NaN value with the next value in the column.

    Returns
    -------
     : DataFrame
        The DataFrame with all NaN values handled.
    """
    if method=="drop":
        return df.dropna()
    elif method=="forward":
        return df.fillna(method='ffill')
    elif method=="backward":
        return df.fillna(method='bfill')

def impute(df, column, method="mean"):
    """    
    Given a numeric column from a data frame, impute all the NaN value in the column with the indicated method.

    Parameters
    ----------
    df : DataFrame
        The DataFrame contains numeric column with NaN values.
    column : str
        The column name of the numerical column to impute.
    method : str
        The method to impute the NaN value to. The set of potential methods is:
        'mean' : Replace all the NaN value with the mean value of the column.
        'median' : Replace all the NaN value with the median value of the column.
        'mood' : Replace all the NaN value with the mood value of the column.

    Returns
    -------
     : Series
        The Series with all the NaN values imputed.
    """
    if method=="mean":
        return df[column].replace(np.nan, np.nanmean(df[column]))
    elif method=="median":
        return df[column].replace(np.nan, np.nanmedian(df[column]))
    elif method=="mood":
        return df[column].replace(np.nan, df[column].value_counts().index[0])

def rolling_impute(df, column, method="mean"):
    """    
    Given a numeric column from a data frame, impute all the NaN value in the column with the indicated method.

    Parameters
    ----------
    df : DataFrame
        The DataFrame contains numeric column with NaN values.
    column : str
        The column name of the numerical column to impute.
    method : str
        The method to impute the NaN value to. The set of potential methods is:
        'mean' : Replace all the NaN value with the mean value of all the values prior to the NaN value.
        'median' : Replace all the NaN value with the median value of all the values prior to the NaN value.
        'mood' : Replace all the NaN value with the mood value of all the values prior to the NaN value.

    Returns
    -------
     : Series
        The Series with all the NaN values imputed.
    """
    indexes = np.where(df[column].isnull())[0]
    if method=="mean":
        indexes = np.where(df[column].isnull())[0]
        tmps = [np.nanmean(df.loc[0:index-1, column]) for index in indexes]
        temp_df = df.copy()
        temp_df.loc[indexes, column] = tmps
        return  temp_df[column]
    elif method=="median":
        indexes = np.where(df[column].isnull())[0]
        tmps = [np.nanmedian(df.loc[0:index-1, column]) for index in indexes]
        temp_df = df.copy()
        temp_df.loc[indexes, column] = tmps
        return  temp_df[column]
    elif method=="mood":
        indexes = np.where(df[column].isnull())[0]
        tmps = [df.loc[0:index, column].value_counts().index[0] for index in indexes]
        temp_df = df.copy()
        temp_df.loc[indexes, column] = tmps
        return  temp_df[column]
