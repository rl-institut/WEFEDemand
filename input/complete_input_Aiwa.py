# %% Complete input data dict
# Dummy dict of households with electrical appliances
# Will be read from surveys
input_dict = {
    "bungalow_ls": {
        "num_users": 4,
        "months_present": [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
        ],  # months at which this user is present in the settlement
        "working_days": [
            0,
            1,
            2,
            3,
            4,
            5,
            6,
            7
        ],  # days at which this user uses his appliances
        "appliances": {  # electrical appliances that this user owns
            "indoor_lights": {
                "num_app": 3,  # number of appliances
                "power": 10,  # power in W
                "usage_window_1": [5, 7],  # usage window [start, end] in min of the day
                "usage_window_2": [
                    20,
                    23,
                ],  # usage window [start, end] in min of the day
                "daily_usage_time": 2,  # daily time of use in min
                "func_cycle": 10,  # minimal duration of switch on event in minutes
            },
            "outdoor_lights": {
                "num_app": 3,  # number of appliances
                "power": 15,  # power in W
                "usage_window_1": [5, 7],  # usage window [start, end] in min of the day
                "usage_window_2": [
                    20,
                    23,
                ],  # usage window [start, end] in min of the day
                "daily_usage_time": 2,  # daily time of use in min
                "func_cycle": 10,  # minimal duration of switch on event in minutes
            },
            "air-conditioning": {
                "num_app": 1,
                "power": 1500,  # power in W
                "usage_window_1": [9, 22],  # usage window [start, end] in min of the day
                "daily_usage_time": 2,  # daily time of use in min
                "func_cycle": 10,  # minimal duration of switch on event in minutes
            },
            "phone-charger": {
                "num_app": 2,
                "power": 30,  # power in W
                "usage_window_1": [0, 8],  # usage window [start, end] in min of the day
                "daily_usage_time": 2,  # daily time of use in min
                "func_cycle": 30,  # minimal duration of switch on event in minutes
            },
        },
        "cooking_demands": {
            "lunch": {
                "stove": "CD_LPG",  # Bungalows do not have a place to cook; there is a restaurant in the hotel;
                # however cooking demand corresponds to hotel occupancy rate;
                # that's why we model it in combination with bungalows
                "fuel": "LPG",  # fuel type used -> to match meta data
                "fuel_amount": 0.3,  # amount of fuel used for this demand [kg, l, kWh]
                "cooking_window_start": 5,  # start of time window of this cooking demand [h]
                "cooking_window_end": 8,  # end of time window of this cooking demand [h]
                "cooking_time": 1.5,  # average duration of this meal preparation
            },
            "dinner": {
                "stove": "CD_LPG",  # stove used for this cooking demand -> to match metadata
                "fuel": "LPG",  # fuel used -> to match meta data
                "fuel_amount": 0.3,  # amount of fuel used for this demand [unit depending on fuel -> metadata]
                "cooking_window_start": 17,  # start of time window of this cooking demand [h]
                "cooking_window_end": 20,  # end of time window of this cooking demand [h]
                "cooking_time": 1.5,  # average duration of this meal preparation
            },
        },
        "drinking_water_demand": {
            "daily_demand": 50,  # daily drinking water demand [l]
            "water_window_1": [7, 24],
        },
        "service_water_demands": {
            "services": {
                "daily_demand": {  # Water demand of typical day for each month [l]
                    1: 75,
                    2: 60,
                    3: 60,
                    4: 50,
                    5: 50,
                    6: 50,
                    7: 70,
                    8: 50,
                    9: 50,
                    10: 20,
                    11: 30,
                    12: 75,
                },
                "usage_windows": [[7, 10], [14, 18], None],
                "demand_duration": 1,  # duration of this demand in [h]
                "pumping_head": 20,  # [m]
            },
        },
        "agro_processing_machines": {},
    },
    "bungalow_ms": {
        "num_users": 4,
        "months_present": [
            2,
            4,
            5,
            8,
            9,
            10,
            11,
        ],  # months at which this user is present in the settlement
        "working_days": [
            0,
            1,
            2,
            3,
            4,
            5,
            6
        ],  # days at which this user uses his appliances
        "appliances": {  # electrical appliances that this user owns
            "indoor_lights": {
                "num_app": 3,  # number of appliances
                "power": 10,  # power in W
                "usage_window_1": [5, 7],  # usage window [start, end] in min of the day
                "usage_window_2": [
                    20,
                    23,
                ],  # usage window [start, end] in min of the day
                "daily_usage_time": 2,  # daily time of use in min
                "func_cycle": 10,  # minimal duration of switch on event in minutes
            },
            "outdoor_lights": {
                "num_app": 3,  # number of appliances
                "power": 15,  # power in W
                "usage_window_1": [5, 7],  # usage window [start, end] in min of the day
                "usage_window_2": [
                    20,
                    23,
                ],  # usage window [start, end] in min of the day
                "daily_usage_time": 2,  # daily time of use in min
                "func_cycle": 10,  # minimal duration of switch on event in minutes
            },
            "air-conditioning": {
                "num_app": 1,
                "power": 1500,  # power in W
                "usage_window_1": [9, 22],  # usage window [start, end] in min of the day
                "daily_usage_time": 2,  # daily time of use in min
                "func_cycle": 10,  # minimal duration of switch on event in minutes
            },
            "phone-charger": {
                "num_app": 2,
                "power": 30,  # power in W
                "usage_window_1": [0, 8],  # usage window [start, end] in min of the day
                "daily_usage_time": 2,  # daily time of use in min
                "func_cycle": 30,  # minimal duration of switch on event in minutes
            },
        },
        "cooking_demands": {
            "lunch": {
                "stove": "CD_LPG",  # Bungalows do not have a place to cook; there is a restaurant in the hotel;
                # however cooking demand corresponds to hotel occupancy rate;
                # that's why we model it in combination with bungalows
                "fuel": "LPG",  # fuel type used -> to match meta data
                "fuel_amount": 0.3,  # amount of fuel used for this demand [kg, l, kWh]
                "cooking_window_start": 5,  # start of time window of this cooking demand [h]
                "cooking_window_end": 8,  # end of time window of this cooking demand [h]
                "cooking_time": 1.5,  # average duration of this meal preparation
            },
            "dinner": {
                "stove": "CD_LPG",  # stove used for this cooking demand -> to match metadata
                "fuel": "LPG",  # fuel used -> to match meta data
                "fuel_amount": 0.3,  # amount of fuel used for this demand [unit depending on fuel -> metadata]
                "cooking_window_start": 17,  # start of time window of this cooking demand [h]
                "cooking_window_end": 20,  # end of time window of this cooking demand [h]
                "cooking_time": 1.5,  # average duration of this meal preparation
            },
        },
        "drinking_water_demand": {
            "daily_demand": 50,  # daily drinking water demand [l]
            "water_window_1": [7, 24],
        },
        "service_water_demands": {
            "services": {
                "daily_demand": {  # Water demand of typical day for each month [l]
                    1: 75,
                    2: 60,
                    3: 60,
                    4: 50,
                    5: 50,
                    6: 50,
                    7: 70,
                    8: 50,
                    9: 50,
                    10: 20,
                    11: 30,
                    12: 75,
                },
                "usage_windows": [[7, 10], [14, 18], None],
                "demand_duration": 1,  # duration of this demand in [h]
                "pumping_head": 20,  # [m]
            },
        },
        "agro_processing_machines": {},
    },
    "bungalow_hs": {
        "num_users": 4,
        "months_present": [
            1,
            3,
            6,
            7,
            12,
        ],  # months at which this user is present in the settlement
        "working_days": [
            0,
            1,
            2
        ],  # days at which this user uses his appliances
        "appliances": {  # electrical appliances that this user owns
            "indoor_lights": {
                "num_app": 3,  # number of appliances
                "power": 10,  # power in W
                "usage_window_1": [5, 7],  # usage window [start, end] in min of the day
                "usage_window_2": [
                    20,
                    23,
                ],  # usage window [start, end] in min of the day
                "daily_usage_time": 2,  # daily time of use in min
                "func_cycle": 10,  # minimal duration of switch on event in minutes
            },
            "outdoor_lights": {
                "num_app": 3,  # number of appliances
                "power": 15,  # power in W
                "usage_window_1": [5, 7],  # usage window [start, end] in min of the day
                "usage_window_2": [
                    20,
                    23,
                ],  # usage window [start, end] in min of the day
                "daily_usage_time": 2,  # daily time of use in min
                "func_cycle": 10,  # minimal duration of switch on event in minutes
            },
            "air-conditioning": {
                "num_app": 1,
                "power": 1500,  # power in W
                "usage_window_1": [9, 22],  # usage window [start, end] in min of the day
                "daily_usage_time": 2,  # daily time of use in min
                "func_cycle": 10,  # minimal duration of switch on event in minutes
            },
            "phone-charger": {
                "num_app": 2,
                "power": 30,  # power in W
                "usage_window_1": [0, 8],  # usage window [start, end] in min of the day
                "daily_usage_time": 2,  # daily time of use in min
                "func_cycle": 30,  # minimal duration of switch on event in minutes
            },
        },
        "cooking_demands": {
            "lunch": {
                "stove": "CD_LPG",  # Bungalows do not have a place to cook; there is a restaurant in the hotel;
                # however cooking demand corresponds to hotel occupancy rate;
                # that's why we model it in combination with bungalows
                "fuel": "LPG",  # fuel type used -> to match meta data
                "fuel_amount": 0.3,  # amount of fuel used for this demand [kg, l, kWh]
                "cooking_window_start": 5,  # start of time window of this cooking demand [h]
                "cooking_window_end": 8,  # end of time window of this cooking demand [h]
                "cooking_time": 1.5,  # average duration of this meal preparation
            },
            "dinner": {
                "stove": "CD_LPG",  # stove used for this cooking demand -> to match metadata
                "fuel": "LPG",  # fuel used -> to match meta data
                "fuel_amount": 0.3,  # amount of fuel used for this demand [unit depending on fuel -> metadata]
                "cooking_window_start": 17,  # start of time window of this cooking demand [h]
                "cooking_window_end": 20,  # end of time window of this cooking demand [h]
                "cooking_time": 1.5,  # average duration of this meal preparation
            },
        },
        "drinking_water_demand": {
            "daily_demand": 50,  # daily drinking water demand [l]
            "water_window_1": [7, 24],
        },
        "service_water_demands": {
            "services": {
                "daily_demand": {  # Water demand of typical day for each month [l]
                    1: 75,
                    2: 60,
                    3: 60,
                    4: 50,
                    5: 50,
                    6: 50,
                    7: 70,
                    8: 50,
                    9: 50,
                    10: 20,
                    11: 30,
                    12: 75,
                },
                "usage_windows": [[7, 10], [14, 18], None],
                "demand_duration": 1,  # duration of this demand in [h]
                "pumping_head": 20,  # [m]
            },
        },
        "agro_processing_machines": {},
    },
}
