# utility functions

import numpy as np
import pandas as pd

from copy import copy
from koboextractor import KoboExtractor

from preprocessing import defaults


def convert_perkg(
    how_much: float, unit: str, fuel: str, kg_per_bag: Optional[float] = None
) -> float:
    """Convert given quantity to kg."""
    if unit not in defaults.fuel_units_conversion:
        raise ValueError(
            f"Missing fuel unit. The one defined are: "
            f"{list(defaults.fuel_units_conversion.keys())}"
        )

    if unit == "kilogram":
        return how_much
    elif unit == "liter":
        return how_much * defaults.density_dict[f"{fuel}_density"]
    elif unit in ["bag", "cylinder"]:
        if kg_per_bag is None:
            raise ValueError("Missing bag conversion coefficient")
        return how_much * kg_per_bag


def convert_perday(quantity: float, period: str) -> float:
    time_units_conversion = defaults.time_units_conversion
    if period in time_units_conversion:
        return quantity / time_units_conversion[period]
    else:
        period_keys = ", ".join(map(str, time_units_conversion.keys()))
        raise ValueError(
            f"Missing time period of reference. The one defined are: {period_keys}"
        )


def convert_perliter(unit, quantity, buck_conversion=None):
    if "liter" in unit:
        return quantity
    elif "buck" in unit and buck_conversion is not None:
        return quantity * buck_conversion
    else:
        raise ValueError("Unit for water usage not known or buck conversion missing")


def exctract_time_window(usage_time):
    windows = copy(defaults.usage_wd_defaults)

    for window in windows:
        if window in usage_time:
            windows[window] = True
        else:
            windows[window] = False
    return windows


def how_many_meal(mystring):
    if "one" in mystring:
        return 1
    elif "two" in mystring:
        return 2
    else:
        return 3


def select_meal_type(meal_number):
    if meal_number == 1:
        return "breackfast"
    elif meal_number == 2:
        return "lunch"
    else:
        return "dinner"


# general function


def load_kobo_data(form_id, api_token="ea290627972a055fd067e1efc02c803869b1747c"):
    kobo_dict = None

    kobo = KoboExtractor(
        api_token, "https://kobo.humanitarianresponse.info/api/v2", debug=True
    )

    # access data submitted to a specific form using the form id
    data = kobo.get_data(
        form_id, query=None, start=None, limit=None, submitted_after=None
    )

    results_dict = data["results"]  # get dict of survey results
    df = pd.json_normalize(data["results"])  # get df of survey results

    return results_dict, df


def convert_usage_windows_2(input_dict):
    # used when "windows_1", "windows_2" etc is required
    usage_windows = []
    start_time = None
    windows = {}
    for window, active in input_dict.items():
        hour_range = window.split("-")
        if active:
            if start_time is None:
                start_time = int(hour_range[0])
        elif start_time is not None:
            end_time = int(hour_range[0])
            usage_windows.append([start_time, end_time])
            start_time = None
    if start_time is not None:
        # If there's an active window at the end of the day
        # assume it ends at midnight (24)
        usage_windows.append([start_time, 24])

    for w in np.arange(len(usage_windows)):
        windows[f"window_{w+1}"] = usage_windows[w]

    return windows


def convert_usage_windows(input_dict):
    # standard usage windows definition
    usage_windows = []
    start_time = None

    for window, active in input_dict.items():
        hour_range = window.split("-")
        if active:
            if start_time is None:
                start_time = int(hour_range[0])
        elif start_time is not None:
            end_time = int(hour_range[0])
            usage_windows.append([start_time, end_time])
            start_time = None
    if start_time is not None:
        # If there's an active window at the end of the day
        # assume it ends at midnight (24)
        usage_windows.append([start_time, 24])

    return usage_windows


def rename_keys(dictionary):
    new_dict = {}
    for i, key in enumerate(dictionary):
        new_dict[i + 1] = dictionary[key]
    return new_dict


def set_values(dictionary, variable):
    new_dict = {}
    for key in dictionary:
        new_dict[key] = variable
    return new_dict
