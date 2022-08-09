import numpy as np
import pandas as pd
import string
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords

stopwords = stopwords.words('english')

def read_file(path, sep=',', orient=None):
    """
    Read CSV file into DataFrame. Also supports reading JSON file, if orient is provided.

    Parameters
    ----------
    path : str, path object, or file-like object
        The file path to access file to read from current directory. The string could also be URL.
    sep : str, default ',' 
        Delimiter to use.
    orient : str , default None
        Indication of expected JSON string format. The set of possible orients is:
        'split' : dict like {index -> [index], columns -> [columns], data -> [values]}
        'records' : list like [{column -> value}, ... , {column -> value}]
        'index' : dict like {index -> {column -> value}}
        'columns' : dict like {column -> {index -> value}}
        'values' : just the values array
    
    Returns
    -------
     : DataFrame or Series
        The DataFrame or Series contains the data in the input file.
    """
    if path[-4:]=='.csv':
        return pd.read_csv(path, sep)
    elif path[-5:]=='.json':
        return pd.read_json(path, orient)
    else:
        raise ValueError("Unrecognized file type")

def clean_string(text):
    """
    Clean the punctuation and stopwords in the input string and turn the string to lower case.

    Parameters
    ----------
    text : str
        The input string.

    Returns
    -------
    text : str
        The cleaned string.
    """
    text = ''.join([char for char in text if char not in string.punctuation])
    text = text.lower()
    text = ' '.join([word for word in text.split() if word not in stopwords])
    return text

def cosine_sim_vectors(vec1, vec2):
    """
    Calculate the cosine similarity between two vectorized strings.
    Two inputs should have the same number of element.

    Parameters
    ----------
    vec1 : array_like
        The first vectorized string.
    vec2 : array_like
        The second vectorized string.
    
    Returns
    -------
     : float
        The cosine similarity score of the two given vectorized strings.
    """
    vec1 = vec1.reshape(1,-1)
    vec2 = vec2.reshape(1,-1)
    return cosine_similarity(vec1, vec2)[0]


def com_sim_cat(df, column, sim_threshold=0.4):
    """
    Given a categorical column in a DataFrame, calculate the pairwise cosine similarity score
    in the alphabetic-ordered series of categories. If the similarity score is higher than the sim_threshold, 
    compare the string length of these two category names. The longer category-name values in the column 
    will be replaced by the similar shorter category-name values. 

    Parameters
    ----------
    df : DataFrame
        The DataFrame contains the target categorical column.
    column : str
        The target categorical column name.
    sim_threshold : float, default 0.4
        The threshold of cosines similarity score. If a pair has score higher than the threshold, do the replacement.
        The score range is [0, 1].

    Returns
    -------
    : Series
        The target categorical column after combining the similar categories.
    repl_dict : dict
        The dictionary the contains the keys that are replaced by the corresponding values.
    """
    # clean the target column
    df[column] = df[column].apply(clean_string)
    # initialize the dict to store the value to replace
    repl_dict = {}
    # get the target column categories as list
    phrases = list(df[column].value_counts().sort_index().index)
    # vectorize the target column categories
    vectorizer = CountVectorizer().fit_transform(phrases)
    vectors = vectorizer.toarray()
    for i in range(0, len(vectors)-1):
        sim = cosine_sim_vectors(vectors[i], vectors[i+1])
        if sim >= sim_threshold:
            if (len(phrases[i])<=len(phrases[i+1])):
                repl_dict[phrases[i+1]] = phrases[i]
                phrases[i+1] = phrases[i]
            else:
                repl_dict[phrases[i]] = phrases[i+1]
                phrases[i] = phrases[i+1]
        else: 
            continue
    return df[column].replace(repl_dict), repl_dict

def comp_key(df, column1, column2, key_name, concat_sign=':'):
    """    
    Create a new column in the given DataFrame that contains concatenation of two given columns as composite key.

    Parameters
    ----------
    df: DataFrame
        The DataFrame contains column1 and column2 and in which a new column of composite keys would be created.
    column1: str
        The column name of the first column to be concatenated.
    column2: str
        The column name of the second column to be concatenated.    
    key_name: str
        The name of the new composite key column.
    concat_sign: str, default ':
        The sign to concat the filed of the first column and the field of the second column.

    Returns
    -------
     : Series
        The column of the composite keys.
    """
    df[key_name] = df[column1] + concat_sign + df[column2]
    return df[key_name]