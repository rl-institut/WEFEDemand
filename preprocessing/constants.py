# %% Name of different type of form
formtype_names = ["household", "business", "service", "large_scale_farm", "local_aut"]

MONTHS_PREFIX = "G_1b"

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

# %% Keys for reading Local Autorities info and matching with Survey info collected by SurveyParser
BUSINESS_KEYS = [
    "number_BIZ_shop",
    "number_BIZ_appliances",
    "number_BIZ_pharmacy",
    "number_BIZ_butcher",
    "number_BIZ_barber",
    "number_BIZ_salon",
    "number_BIZ_money_transfer",
    "number_BIZ_recharing",
    "number_BIZ_internet",
    "number_BIZ_music_shop",
    "number_BIZ_print_shop",
    "number_BIZ_bike_mech",
    "number_BIZ_vehicle_mech",
    "number_BIZ_device_repair",
    "number_BIZ_welding_workshop",
    "number_BIZ_wood_workshop",
    "number_BIZ_tailoring_workshop",
    "number_BIZ_restaurant",
    "number_BIZ_bar",
    "number_BIZ_hotel",
    "number_BIZ_brewery",
    "number_BIZ_mill",
    "number_BIZ_other_mill",
    "number_BIZ_slaughterhouse",
    "number_BIZ_juice",
    "number_BIZ_cinema",
    "number_BIZ_other",
]

FORM_SUBTYPES = {
    formtype_names[0]: ["low_income_hh", "medium_income_hh", "high_income_hh"],
    formtype_names[1]: [key.split("number_")[-1] for key in BUSINESS_KEYS],
    formtype_names[2]: [
        "primary_school",
        "secondary_school",
        "hospital",
        "health_centre",
        "health_post",
        "religeus_building",
        "other_service",
    ],
    formtype_names[3]: "large_scale_farm",
}
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
        "service_water": {
            "animal_water": "H_11",
            "irrigation": "H_10",
            "services": "H_8",
        },
        "agro_machine": None,
    },
    "service": {
        "working_days": "S_2",
        "cooking": "S_5",
        "meal": "S_5l",
        "electric": "S_3",
        "drinking_water": "S_4",
        "service_water": {"services": "S_4"},
        "agro_machine": None,
    },
    "large_scale_farm": {
        "working_days": "AP_2c",
        "cooking": "AP_9",
        "meal": "AP_9l",
        "electric": "AP_8",
        "drinking_water": "AP_3",
        "service_water": {
            "animal_water": "AP_6",
            "irrigation": "AP_5",
            "services": "AP_3",
        },
        "agro_machine": "AP_10",
    },
    "business": {
        "working_days": "B_2a",
        "cooking": "B_13",
        "meal": "B_13_meal",
        "electric": "B_11",
        "drinking_water": "B_7",
        "service_water": {"services": "B_7"},
        "agro_machine": "B_14",
    },
}
