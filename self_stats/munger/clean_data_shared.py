import numpy as np
import regex as re
from datetime import datetime
from typing import List, Any, Tuple, Pattern

def safe_convert_to_float(values: np.ndarray) -> np.ndarray:
    """
    Attempts to convert each element of a 1D numpy array from string to float. 
    If an element cannot be converted to a float, it retains the original string.

    Args:
    values (np.ndarray): The 1D array of strings to be converted to floats.
    
    Returns:
    np.ndarray: An array where each element is either the converted float value or the original string if the conversion fails.
    """
    # Define the function that tries to convert one value
    def convert(value):
        try:
            return float(value)
        except ValueError:
            return value

    # Vectorize this function so it can be applied to each element in the numpy array
    vectorized_convert = np.vectorize(convert, otypes=[object])

    # Apply the vectorized function to the array of values
    converted_values = vectorized_convert(values)
    return converted_values

def remove_invisible_characters(texts: np.ndarray, hidden_char_pattern: Pattern) -> np.ndarray:
    """
    Remove invisible and non-printable Unicode characters from each text string in a numpy array using a precompiled regex pattern.
    
    Args:
    texts (np.ndarray): A numpy array of strings from which to remove invisible characters.
    hidden_char_pattern (Pattern): A precompiled regex pattern to match invisible characters.

    Returns:
    np.ndarray: A numpy array containing the cleaned text strings without invisible characters.
    """
    vectorized_remove = np.vectorize(lambda text: hidden_char_pattern.sub(' ', text).strip())
    cleaned_texts = vectorized_remove(texts)
    return cleaned_texts

def remove_timezones(date_strings: np.ndarray, timezone_pattern: Pattern) -> np.ndarray:
    """
    Remove timezone abbreviations from each date string in a numpy array using a precompiled regex pattern.
    
    Args:
    date_strings (np.ndarray): A numpy array of date strings that may include timezone abbreviations.
    timezone_pattern (Pattern): A precompiled regex pattern to match and remove timezone abbreviations.

    Returns:
    np.ndarray: A numpy array of date strings with timezone abbreviations removed.
    """
    vectorized_remove_timezone = np.vectorize(lambda date_str: timezone_pattern.sub('', date_str).strip())
    cleaned_date_strings = vectorized_remove_timezone(date_strings)
    return cleaned_date_strings

def parse_dates(date_array: np.ndarray, timezone_pattern: Pattern) -> Tuple[np.ndarray, list]:
    """
    Parse the datetime from strings in a numpy array after timezone information has been removed.

    Args:
    date_array (np.ndarray): Array of datetime strings without timezone information.
    date_format (str): The format of the datetime strings.

    Returns:
    Tuple[np.ndarray, list]: Tuple of numpy array with datetime objects and list of indices with invalid dates.
    """
    date_no_tmz = remove_timezones(date_array, timezone_pattern)

    parsed_dates = []
    bad_indices = []
    
    for i, date_str in enumerate(date_no_tmz):
        try:
            parsed_date = datetime.strptime(date_str, '%b %d, %Y, %I:%M:%S %p')
            parsed_dates.append(parsed_date)
        except ValueError:
            bad_indices.append(i)
            parsed_dates.append(None)  # Use None as a placeholder for invalid entries

    # Convert list to a numpy array of object type after all dates are processed
    parsed_dates_array = np.array(parsed_dates, dtype=object)
    return parsed_dates_array, bad_indices
    
def clean_all_columns(arr_data, hidden_char_pattern: Pattern) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Apply the remove_invisible_characters function to all four numpy arrays and return new numpy arrays.
    
    Args:
    col_1, col_2, col_3, col_4 (np.ndarray): Arrays of data containing strings.
    hidden_char_pattern (Pattern): A compiled regex pattern to remove invisible characters.
    
    Returns:
    Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: A tuple of cleaned numpy arrays.
    """
    clean_columns = []
    for column in (arr_data[0], arr_data[1], arr_data[2], arr_data[3]):
        cleaned = np.vectorize(remove_invisible_characters)(column, hidden_char_pattern)
        clean_columns.append(cleaned)
    
    return clean_columns

def convert_to_arrays(data: List[List[str]]) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Converts a list of lists into a list of 4 numpy arrays, each representing a column in the data.
    
    Args:
    - data (List[List[str]]): Data to be converted.
    
    Returns:
    - Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: A tuple of numpy arrays.
    """
    arr = np.array(data)
    return (arr[:, 0], arr[:, 1], arr[:, 2], arr[:, 3])

def remove_indices_from_tuple(data: Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray], indices: List[int]) -> Tuple[np.ndarray, ...]:
    """
    Removes specified indices from each numpy array in a tuple.

    Args:
    - data (Tuple[np.ndarray, ...]): Tuple of numpy arrays, where each array represents a column of data.
    - indices (List[int]): List of indices to be removed from each array.

    Returns:
    - Tuple[np.ndarray, ...]: A new tuple of numpy arrays with specified indices removed.
    """
    # Convert the list of indices to a numpy array for efficient operations
    indices_to_remove = np.array(indices)
    
    # Use numpy's boolean indexing to create new arrays without the specified indices
    modified_data = tuple(np.delete(arr, indices_to_remove) for arr in data)
    
    return modified_data