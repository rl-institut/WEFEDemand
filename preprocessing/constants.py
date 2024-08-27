# %% Name of different type of form
formtype_names = ["household", "business", "service", "large_scale_farm", "local_aut"]

# %% defaults usage time windows in a day
USAGE_WD_DEFAULTS = {
    "0-7": None,
    "7-10": None,
    "10-12": None,
    "12-18": None,
    "18-22": None,
    "22-24": None,
}

# %% defaults months and day numaration

months_defaults = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12,
}

working_day = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
}

# %% Defaults constants used in preprocessing

exc_rate = 0.05334  # $/ZAR exchange rate
large_buck = 10
medium_buck = 5
small_buck = 1
buck = 5

DENSITY_DICT = {
    "g/biogas_density": 0.0012,
    "h/biofuel_density": 0.9,
    "i/kerosene_density": 0.8,
    "j/LPG_density": 0.55,
    "k/eth_alc_density": 0.789,
}

FUEL_UNITS_CONVERSION = {"kilogram": 1, "bag": None, "liter": None, "cylinder": None}
TIME_UNITS_CONVERSION = {"daily": 1, "weekly": 7, "monthly": 30}


# %% Key to find the type of form, as defined in kobo CSV configuration file
formtype_key = "G_0/respondent_"

# %% Key associated with the form type, as defined in kobo CSV configuration file
suffix = {
    "household": "_H",
    "service": "_S",
    "large_scale_farm": "_AP",
    "business": "",
    "local_aut": "",
}

# %% Key associated with the form type, as defined in kobo CSV configuration file

prefix = {
    "local_aut": {
        "village_composition": "LA_2",
        "education_composition": "LA_3",
        "health_composition": "LA_4",
        "religion_composition": "LA_5",
        "economy_composition": "LA_6",
        "agroprocessing_composition": "LA_7",
        "baseline": "LA_8",
    },
    "household": {
        "working_days": None,
        "cooking": "H_18",
        "meal": "H_18l",
        "electric": "H_16",
        "drinking_water": "H_8",
        "service_water": {"livestock": "H_11", "irrigation": "H_10", "services": 'H_8'},
        "agro_machine": None,
    },
    "service": {
        "working_days": "S_2",
        "cooking": "S_5",
        "meal": "S_5l",
        "electric": "S_3",
        "drinking_water": "S_4",
        "service_water": {"services": 'S_4'},
        "agro_machine": None,
    },
    "large_scale_farm": {
        "working_days": "AP_2c",
        "cooking": "AP_9",
        "meal": "AP_9l",
        "electric": "AP_8",
        "drinking_water": "AP_3",
        "service_water": {"animal_water": "AP_6", "irrigation_water": "AP_5", "services": 'AP_3'},
        "agro_machine": "AP_10",
    },
    "business": {
        "working_days": "B_2a",
        "cooking": "B_13",
        "meal": "B_13_meal",
        "electric": "B_11",
        "drinking_water": "B_7",
        "service_water": {"services": 'B_7'},
        "agro_machine": "B_14"
    },
}
