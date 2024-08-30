# %% Complete input data dict
# Dummy dict of households with electrical appliances
# Will be read from surveys
input_dict = {
    "low_income_hh": {
        "num_users": 30,
        "months_present": [
            1,
            2,
            3,
            4,
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
        ],  # days at which this user uses his appliances
        "appliances": {  # electrical appliances that this user owns
            "indoor_lights": {
                "num_app": 3,  # number of appliances
                "power": 10,  # power in W
                "usage_window_1": [5, 7],  # usage window [start, end] in min of the day
                "usage_window_2": [
                    19,
                    24,
                ],  # usage window [start, end] in min of the day
                "daily_usage_time": 2,  # daily time of use in hours
                "func_cycle": 10,  # minimal duration of switch on event in minutes
            },
            "outdoor_lights": {
                "num_app": 2,  # number of appliances
                "power": 15,  # power in W
                "usage_window_1": [5, 7],  # usage window [start, end] in min of the day
                "usage_window_2": [19, 24],  # usage window [start, end] in min of the day
                "daily_usage_time": 2,  # daily time of use in hours
                "func_cycle": 10,  # minimal duration of switch on event in minutes
            },
        },
        "cooking_demands": {
            "lunch": {
                "stove": "CD_LPG",  # stove used for this cooking demand -> to match metadata
                "fuel": "LPG",  # fuel type used -> to match meta data
                "fuel_amount": 0.3,  # amount of fuel used for this demand [kg, l, kWh], for which demand?
                "cooking_window_start": 10,  # start of time window of this cooking demand [h]
                "cooking_window_end": 13,  # end of time window of this cooking demand [h]
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
            "water_window_1": [5, 9],
            "water_window_2": [10,13],
            "water_window_3": [18,23],
        },
        "service_water_demands": {
            "services": {
                "daily_demand": {  # Water demand of typical day for each month [l]
                    1: 50,
                    2: 50,
                    3: 50,
                    4: 50,
                    5: 50,
                    6: 50,
                    7: 50,
                    8: 50,
                    9: 50,
                    10: 50,
                    11: 50,
                    12: 50,
                },
                "usage_windows": [[7, 10], [14, 18], None],
                "demand_duration": 1,  # duration of this demand in [h]
                "pumping_head": 20,  # [m]
            },
        },
        "agro_processing_machines": {},
    },
    "mid_income_hh": {
        "num_users": 90,
        "months_present": [
            1,
            2,
            3,
            4,
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
        ],  # days at which this user uses his appliances
        "appliances": {  # electrical appliances that this user owns
            "indoor_lights": {
                "num_app": 6,  # number of appliances
                "power": 10,  # power in W
                "usage_window_1": [5, 7],  # usage window [start, end] in min of the day
                "usage_window_2": [
                    19,
                    24,
                ],  # usage window [start, end] in min of the day
                "daily_usage_time": 2,  # daily time of use in hours
                "func_cycle": 10,  # minimal duration of switch on event in minutes
            },
            "outdoor_lights": {
                "num_app": 4,  # number of appliances
                "power": 15,  # power in W
                "usage_window_1": [5, 7],  # usage window [start, end] in min of the day
                "usage_window_2": [19, 24],  # usage window [start, end] in min of the day
                "daily_usage_time": 2,  # daily time of use in hours
                "func_cycle": 10,  # minimal duration of switch on event in minutes
            },
            "refrigerator": {
                "num_app": 1,  # number of appliances
                "power": 500,  # power in W
                "usage_window_1": [0, 24],  # usage window [start, end] in min of the day
                # usage window [start, end] in min of the day
                "daily_usage_time": 10,  # daily time of use in hours
                "func_cycle": 60,  # minimal duration of switch on event in minutes
            },
            "fan": {
                "num_app": 1,  # number of appliances
                "power": 50,  # power in W
                "usage_window_1": [0, 24],  # usage window [start, end] in min of the day
                # usage window [start, end] in min of the day
                "daily_usage_time": 4,  # daily time of use in hours
                "func_cycle": 30,  # minimal duration of switch on event in minutes
            },
            "television": {
                "num_app": 1,  # number of appliances
                "power": 150,  # power in W
                "usage_window_1": [14, 16],  # usage window [start, end] in min of the day
                "usage_window_2": [19,23],
                # usage window [start, end] in min of the day
                "daily_usage_time": 3,  # daily time of use in hours
                "func_cycle": 45,  # minimal duration of switch on event in minutes
            }
        },
        "cooking_demands": {
            "lunch": {
                "stove": "CD_LPG",  # stove used for this cooking demand -> to match metadata
                "fuel": "LPG",  # fuel type used -> to match meta data
                "fuel_amount": 0.3,  # amount of fuel used for this demand [kg, l, kWh], for which demand?
                "cooking_window_start": 10,  # start of time window of this cooking demand [h]
                "cooking_window_end": 13,  # end of time window of this cooking demand [h]
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
            "daily_demand": 100,  # daily drinking water demand [l]
            "water_window_1": [5, 9],
            "water_window_2": [10, 13],
            "water_window_3": [18, 23],
        },
        "service_water_demands": {
            "services": {
                "daily_demand": {  # Water demand of typical day for each month [l]
                    1: 200,
                    2: 200,
                    3: 200,
                    4: 200,
                    5: 200,
                    6: 200,
                    7: 200,
                    8: 200,
                    9: 200,
                    10: 200,
                    11: 200,
                    12: 200,
                },
                "usage_windows": [[7, 10], [14, 18], None],
                "demand_duration": 1,  # duration of this demand in [h]
                "pumping_head": 20,  # [m]
            },
        },
        "agro_processing_machines": {},
    },
    "high_income_hh": {
        "num_users": 90,
        "months_present": [
            1,
            2,
            3,
            4,
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
        ],  # days at which this user uses his appliances
        "appliances": {  # electrical appliances that this user owns
            "indoor_lights": {
                "num_app": 6,  # number of appliances
                "power": 10,  # power in W
                "usage_window_1": [5, 7],  # usage window [start, end] in min of the day
                "usage_window_2": [
                    19,
                    24,
                ],  # usage window [start, end] in min of the day
                "daily_usage_time": 2,  # daily time of use in hours
                "func_cycle": 10,  # minimal duration of switch on event in minutes
            },
            "outdoor_lights": {
                "num_app": 4,  # number of appliances
                "power": 15,  # power in W
                "usage_window_1": [5, 7],  # usage window [start, end] in min of the day
                "usage_window_2": [19, 24],  # usage window [start, end] in min of the day
                "daily_usage_time": 2,  # daily time of use in hours
                "func_cycle": 10,  # minimal duration of switch on event in minutes
            },
            "refrigerator": {
                "num_app": 2,  # number of appliances
                "power": 500,  # power in W
                "usage_window_1": [0, 24],  # usage window [start, end] in min of the day
                # usage window [start, end] in min of the day
                "daily_usage_time": 10,  # daily time of use in hours
                "func_cycle": 60,  # minimal duration of switch on event in minutes
            },
            "fan": {
                "num_app": 2,  # number of appliances
                "power": 50,  # power in W
                "usage_window_1": [0, 24],  # usage window [start, end] in min of the day
                # usage window [start, end] in min of the day
                "daily_usage_time": 4,  # daily time of use in hours
                "func_cycle": 30,  # minimal duration of switch on event in minutes
            },
            "television": {
                "num_app": 1,  # number of appliances
                "power": 150,  # power in W
                "usage_window_1": [14, 16],  # usage window [start, end] in min of the day
                "usage_window_2": [19,23],
                # usage window [start, end] in min of the day
                "daily_usage_time": 3,  # daily time of use in hours
                "func_cycle": 45,  # minimal duration of switch on event in minutes
            }
        },
        "cooking_demands": {
            "lunch": {
                "stove": "CD_LPG",  # stove used for this cooking demand -> to match metadata
                "fuel": "LPG",  # fuel type used -> to match meta data
                "fuel_amount": 0.5,  # amount of fuel used for this demand [kg, l, kWh], for which demand?
                "cooking_window_start": 10,  # start of time window of this cooking demand [h]
                "cooking_window_end": 13,  # end of time window of this cooking demand [h]
                "cooking_time": 1.5,  # average duration of this meal preparation
            },
            "dinner": {
                "stove": "CD_LPG",  # stove used for this cooking demand -> to match metadata
                "fuel": "LPG",  # fuel used -> to match meta data
                "fuel_amount": 0.5,  # amount of fuel used for this demand [unit depending on fuel -> metadata]
                "cooking_window_start": 17,  # start of time window of this cooking demand [h]
                "cooking_window_end": 20,  # end of time window of this cooking demand [h]
                "cooking_time": 1.5,  # average duration of this meal preparation
            },
        },
        "drinking_water_demand": {
            "daily_demand": 200,  # daily drinking water demand [l]
            "water_window_1": [5, 9],
            "water_window_2": [10, 13],
            "water_window_3": [18, 23],
        },
        "service_water_demands": {
            "services": {
                "daily_demand": {  # Water demand of typical day for each month [l]
                    1: 500,
                    2: 500,
                    3: 500,
                    4: 500,
                    5: 500,
                    6: 500,
                    7: 500,
                    8: 500,
                    9: 500,
                    10: 500,
                    11: 500,
                    12: 500,
                },
                "usage_windows": [[7, 10], [14, 18], None],
                "demand_duration": 1,  # duration of this demand in [h]
                "pumping_head": 20,  # [m]
            },
        },
        "agro_processing_machines": {},
    },
    "medium_farm": {
        "num_users": 2,
        "months_present": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "working_days": [0, 1, 2, 3, 4, 5],
        "appliances": {  # electrical appliances that this user owns
            "indoor_lights": {
                "num_app": 3,  # number of appliances
                "power": 10,  # power in W
                "usage_window_1": [5, 7],  # usage window [start, end] hours of the day
                "usage_window_2": [20, 23],  # usage window [start, end] hours of the day
                "daily_usage_time": 2,  # daily time of use [h]
                "func_cycle": 10,  # minimal duration of switch on event in minutes
            },
            "outdoor_lights": {
                "num_app": 3,  # number of appliances
                "power": 15,  # power in W
                "usage_window_1": [5, 7],  # usage window [start, end] in min of the day
                "usage_window_2": [20, 23],  # usage window [start, end] in min of the day
                "daily_usage_time": 2,  # daily time of use in min
                "func_cycle": 10,  # minimal duration of switch on event in minutes
            },
        },
        "cooking_demands": {
            "lunch": {
                "stove": "three_stone_fire",  # stove used for this cooking demand -> to match metadata
                "fuel": "firewood",  # fuel type used -> to match meta data
                "fuel_amount": 0.3,  # amount of fuel used for this demand [kg, l, kWh]
                "cooking_window_start": 5,  # start of time window of this cooking demand [h]
                "cooking_window_end": 8,  # end of time window of this cooking demand [h]
                "cooking_time": 1.5,  # average duration of this meal preparation
            },
            "dinner": {
                "stove": "three_stone_fire",  # stove used for this cooking demand -> to match metadata
                "fuel": "firewood",  # fuel used -> to match meta data
                "fuel_amount": 0.3,  # amount of fuel used for this demand [unit depending on fuel -> metadata]
                "cooking_window_start": 17,  # start of time window of this cooking demand [h]
                "cooking_window_end": 20,  # end of time window of this cooking demand [h]
                "cooking_time": 1.5,  # average duration of this meal preparation
            },
        },
        "drinking_water_demand": {
            "daily_demand": 50,  # daily drinking water demand [l]
            "water_window_1": [10, 12],
            "water_window_2": [16, 18],
        },
        "service_water_demands": {
            "irrigation": {
                "daily_demand": {  # Water demand of typical day for each month [l]
                    1: 400,
                    2: 300,
                    3: 100,
                    4: 100,
                    5: 0,
                    6: 400,
                    7: 800,
                    8: 1000,
                    9: 800,
                    10: 600,
                    11: 500,
                    12: 400,
                },
                "usage_windows": [[7, 10], [14, 18], None],
                "demand_duration": 1,  # duration of this demand in [h]
                "pumping_head": 20,  # [m]
            },
            "livestock": {
                "daily_demand": {  # Water demand of typical day for each month [l]
                    1: 400,
                    2: 300,
                    3: 100,
                    4: 100,
                    5: 300,
                    6: 400,
                    7: 800,
                    8: 1000,
                    9: 800,
                    10: 600,
                    11: 500,
                    12: 400,
                },
                "usage_windows": [[7, 10], [14, 18], None],
                "demand_duration": 1,  # duration of this demand in [h]
                "pumping_head": 20,  # [m]
            },
        },
        "agro_processing_machines": {},
    },
}
