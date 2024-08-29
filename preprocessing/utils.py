# utility functions for preprocessing

import numpy as np
import pandas as pd
import functools
import warnings

from copy import copy
from koboextractor import KoboExtractor

from preprocessing import constants


# %% Conversion function used in formparser
def convert_perkg(
    quantity: float, unit: str, fuel_type: str, kg_per_bag: float = None
) -> float:
    """
    Convert fuel quantity from given unit to kg.

    Args:
        quantity (float): The quantity of fuel.
        unit (str): The unit of the fuel quantity.
        fuel_type (str): The type of fuel.
        kg_per_bag (float, optional): The weight of a bag of fuel in kg.
            Defaults to None.

    Returns:
        float: The quantity of fuel in kg.

    Raises:
        ValueError: If the unit is not valid.
        ValueError: If the unit is 'bag' or 'cylinder' and kg_per_bag is None.

    """
    # Get the valid units of fuel
    valid_units = tuple(constants.FUEL_UNITS_CONVERSION.keys())

    # Check if the unit is valid
    if unit not in valid_units:
        raise ValueError(f"Invalid unit: {unit}. Must be one of: {valid_units}")

    # If the unit is 'kilogram', return the quantity
    if unit == "kilogram":
        return quantity
    # If the unit is 'liter', return the quantity multiplied by the fuel density
    elif unit == "liter":
        fuel_density = constants.DENSITY_DICT[f"{fuel_type}_density"]
        return quantity * fuel_density
    # If the unit is 'bag' or 'cylinder', check if kg_per_bag is provided
    elif unit in ("bag", "cylinder"):
        if kg_per_bag is None:
            raise ValueError("Missing bag conversion coefficient")
        # Return the quantity multiplied by kg_per_bag
        return quantity * kg_per_bag


def convert_perday(quantity: float, period: str) -> float:
    """
    Convert quantity from given time period to daily quantity.

    Args:
        quantity (float): The quantity of water or fuel.
        period (str): The time period of the given quantity.

    Returns:
        float: The quantity of water or fuel per day.

    Raises:
        ValueError: If the time period is not valid.
    """
    # Get the valid time units of the given quantity
    time_units_conversion = constants.TIME_UNITS_CONVERSION
    # Check if the given time period is valid
    if period in time_units_conversion:
        # Return the quantity divided by the time period
        return quantity / time_units_conversion[period]
    else:
        # Raise an error if the time period is not valid
        period_keys = ", ".join(map(str, time_units_conversion.keys()))
        raise ValueError(
            f"Missing time period of reference. The one defined are: {period_keys}"
        )


def convert_perliter(unit, quantity, buck_conversion=None):
    """
    Convert a quantity from a given unit to liters.

    Args:
        unit (str): The unit of the given quantity.
        quantity (float): The quantity of water or fuel.
        buck_conversion (float, optional): The conversion rate from bucks to liters.

    Returns:
        float: The quantity of water or fuel in liters.

    Raises:
        ValueError: If the unit is not 'liter' or 'buck', or if buck conversion is missing.
    """
    # Check if the unit is 'liter'
    if "liter" in unit:
        return quantity  # Return the quantity if it is already in liters
    # Check if the unit is 'buck' and buck_conversion is provided
    elif "buck" in unit and buck_conversion is not None:
        return (
            quantity * buck_conversion
        )  # Return the quantity multiplied by buck_conversion
    # Raise an error if the unit is not 'liter' or 'buck', or if buck conversion is missing
    else:
        raise ValueError("Unit for water usage not known or buck conversion missing")


def extract_time_windows(usage_time):
    """
    Extracts the time windows from the given usage time string.

    Args:
        usage_time (str): The string containing the usage time windows.

    Returns:
        dict: A dictionary where the keys are the time windows and the values
              are booleans indicating whether each window is present in the usage time string.
    """
    # Create a copy of the default usage time windows
    time_windows = copy(constants.USAGE_WD_DEFAULTS)

    # Iterate over the time windows and check if each window is present in the usage time string
    for window in time_windows:
        time_windows[window] = window in usage_time

    # Return the time windows dictionary
    return time_windows


def how_many_meal(mystring):
    """
    Returns the number of meals in the given string.

    Args:
        mystring (str): The string containing the number of meals.

    Returns:
        int: The number of meals (1, 2, or 3).
    """
    if "one" in mystring:
        return 1
    elif "two" in mystring:
        return 2
    else:
        return 3


def convert_usage_windows(input_dict):
    """
    Converts the given input dictionary into a list of time windows (usage_windows)
    and a dictionary of time windows with the keys "window_1", "window_2", etc.

    Args:
        input_dict (dict): A dictionary where the keys are the time windows (e.g. "6-8")
                           and the values are boolean indicating whether the window is active or not.

    Returns:
        tuple: A tuple containing a dictionary of time windows (windows) and
               a list of time windows (usage_windows).
    """
    # used when "windows_1", "windows_2" etc is required
    usage_windows = []
    start_time = None
    windows = {}

    # Iterate over the time windows and check if each window is active or not
    # if two consecutive windows are active, merge them
    for window, active in input_dict.items():
        hour_range = window.split("-")
        if active:
            if start_time is None:
                start_time = int(hour_range[0])
        elif start_time is not None:
            end_time = int(hour_range[0])
            usage_windows.append([start_time, end_time])
            start_time = None

    # If there's an active window at the end of the day
    # assume it ends at midnight (24)
    if start_time is not None:
        usage_windows.append([start_time, 24])

    # Create a dictionary of time windows with the keys "window_1", "window_2", etc.
    for w in np.arange(len(usage_windows)):
        windows[f"window_{w+1}"] = usage_windows[w]

    return windows, usage_windows


# general function
def load_kobo_data(form_id, api_token):
    """
    Loads data from Kobo Toolbox using the given form id and api token.

    Args:
        form_id (str): The id of the form to load the data from.
        api_token (str, optional): The api token to use for authentication.

    Returns:
        tuple: A tuple containing the dictionary of survey results and the
            pandas DataFrame of the survey results.
    """
    # initialize the kobo extractor
    kobo = KoboExtractor(
        api_token, "https://kobo.humanitarianresponse.info/api/v2", debug=True
    )

    # access data submitted to a specific form using the form id
    data = kobo.get_data(
        form_id, query=None, start=None, limit=None, submitted_after=None
    )

    # get the dictionary of survey results
    results_dict = data["results"]

    # get the pandas DataFrame of the survey results
    df = pd.json_normalize(data["results"])

    # return the dictionary of survey results and the pandas DataFrame
    return results_dict, df


def warn_and_skip(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            warnings.warn(f"Error processing {func.__name__}: {str(e)}", category=UserWarning)
            return None
    return wrapper