# %% Tsumkwe case study - RAMP input dictionary
#
# SOURCES:
# - Consumer base: 400 households (85:10:5 high/medium/low split -> 340/40/20)
#   + 50 industrial + 88 service establishments (Namibia Statistics Agency, 2024)
# - Electricity: calibrated to NSA seasonal kWh/day targets, annual-averaged
#   (this codebase can't vary electrical appliance load by month - only
#   agro-processing/service-water support monthly dicts)
# - Household water: case-study Table 1 (WHO 2020 benchmarks), 5 people/home
# - Industries/services water: CSIR "Red Book" non-domestic demand guideline
#   (400 L/100m^2/day offices/shops/govt, 500 L/100m^2/day clinic), applied
#   with assumed floor areas (150 m^2 services, 120 m^2 industries) since no
#   real floor-area data exists for Tsumkwe
# - pumping_head = 51 m (matches groundwater-pump head in the WEFE datapackage)
#
# EXCLUDED: field irrigation (out of scope - no bus for it downstream, and
# infra is sized for domestic-scale flow); food consumption (Table 2, not a
# RAMP demand type); tractors/oxen/hand tools; poultry/WFP program specifics;
# agro-processing machinery; household cooking fuel (only the electric
# hotplate is modeled, as an appliance) - no data was available for these,
# so nothing was invented in their place.
#
# admin_input.py was extended (additively) with "hotplate_stove" and
# "workshop_machinery" appliance metadata, and "cooking_water",
# "cleaning_water", "laundry_water", "bathing_water" service_water_metadata.

input_dict = {
    # --- HOUSEHOLDS (340 high / 40 medium / 20 low = 400 total) ---
    "high_income_hh": {
        "num_users": 340,
        "months_present": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "working_days": [0, 1, 2, 3, 4, 5, 6],
        "appliances": {
            "indoor_lights": {
                "num_app": 4,
                "power": 8,
                "usage_window_1": [5, 7],
                "usage_window_2": [17, 22],
                "daily_usage_time": 5,
                "func_cycle": 10,
            },
            "outdoor_lights": {
                "num_app": 2,
                "power": 15,
                "usage_window_1": [17, 23],
                "daily_usage_time": 4,
                "func_cycle": 10,
            },
            "television": {
                "num_app": 1,
                "power": 80,
                "usage_window_1": [17, 22],
                "daily_usage_time": 3,
                "func_cycle": 15,
            },
            "phone-charger": {
                "num_app": 3,
                "power": 5,
                "usage_window_1": [6, 22],
                "daily_usage_time": 3,
                "func_cycle": 30,
            },
            "hotplate_stove": {
                "num_app": 1,
                "power": 1000,
                "usage_window_1": [6, 8],
                "usage_window_2": [17, 19],
                "daily_usage_time": 0.17,
                "func_cycle": 10,
            },
        },
        "cooking_demands": {},
        "drinking_water_demand": {
            "daily_demand": 15,
            "water_window_1": [6, 8],
            "water_window_2": [18, 20],
        },
        "service_water_demands": {
            "cooking_water": {
                "daily_demand": {m: 7.5 for m in range(1, 13)},
                "usage_windows": [[5, 8], [17, 20], None],
                "demand_duration": 1,
                "pumping_head": 51,
            },
            "cleaning_water": {
                "daily_demand": {m: 100 for m in range(1, 13)},
                "usage_windows": [[7, 9], [16, 18], None],
                "demand_duration": 1,
                "pumping_head": 51,
            },
            "laundry_water": {
                "daily_demand": {m: 46.5 for m in range(1, 13)},
                "usage_windows": [[9, 12], None, None],
                "demand_duration": 2,
                "pumping_head": 51,
            },
            "bathing_water": {
                "daily_demand": {m: 100 for m in range(1, 13)},
                "usage_windows": [[6, 8], [19, 21], None],
                "demand_duration": 1,
                "pumping_head": 51,
            },
        },
        "agro_processing_machines": {},
    },
    "medium_income_hh": {
        "num_users": 40,
        "months_present": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "working_days": [0, 1, 2, 3, 4, 5, 6],
        "appliances": {
            "indoor_lights": {
                "num_app": 3,
                "power": 8,
                "usage_window_1": [5, 7],
                "usage_window_2": [18, 22],
                "daily_usage_time": 4,
                "func_cycle": 10,
            },
            "outdoor_lights": {
                "num_app": 1,
                "power": 15,
                "usage_window_1": [18, 22],
                "daily_usage_time": 3,
                "func_cycle": 10,
            },
            "radio": {
                "num_app": 1,
                "power": 8,
                "usage_window_1": [6, 9],
                "daily_usage_time": 3,
                "func_cycle": 10,
            },
            "television": {
                "num_app": 1,
                "power": 60,
                "usage_window_1": [18, 21],
                "daily_usage_time": 2,
                "func_cycle": 15,
            },
            "phone-charger": {
                "num_app": 2,
                "power": 5,
                "usage_window_1": [18, 22],
                "daily_usage_time": 3,
                "func_cycle": 30,
            },
        },
        "cooking_demands": {},
        "drinking_water_demand": {
            "daily_demand": 15,
            "water_window_1": [6, 8],
            "water_window_2": [18, 20],
        },
        "service_water_demands": {
            "cooking_water": {
                "daily_demand": {m: 7.5 for m in range(1, 13)},
                "usage_windows": [[5, 8], [17, 20], None],
                "demand_duration": 1,
                "pumping_head": 51,
            },
            "cleaning_water": {
                "daily_demand": {m: 100 for m in range(1, 13)},
                "usage_windows": [[7, 9], [16, 18], None],
                "demand_duration": 1,
                "pumping_head": 51,
            },
            "laundry_water": {
                "daily_demand": {m: 46.5 for m in range(1, 13)},
                "usage_windows": [[9, 12], None, None],
                "demand_duration": 2,
                "pumping_head": 51,
            },
            "bathing_water": {
                "daily_demand": {m: 100 for m in range(1, 13)},
                "usage_windows": [[6, 8], [19, 21], None],
                "demand_duration": 1,
                "pumping_head": 51,
            },
        },
        "agro_processing_machines": {},
    },
    "low_income_hh": {
        "num_users": 20,
        "months_present": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "working_days": [0, 1, 2, 3, 4, 5, 6],
        "appliances": {
            "indoor_lights": {
                "num_app": 2,
                "power": 7,
                "usage_window_1": [5, 6],
                "usage_window_2": [18, 21],
                "daily_usage_time": 4,
                "func_cycle": 10,
            },
            "radio": {
                "num_app": 1,
                "power": 8,
                "usage_window_1": [6, 9],
                "daily_usage_time": 3,
                "func_cycle": 10,
            },
            "phone-charger": {
                "num_app": 2,
                "power": 5,
                "usage_window_1": [18, 22],
                "daily_usage_time": 3,
                "func_cycle": 30,
            },
        },
        "cooking_demands": {},
        "drinking_water_demand": {
            "daily_demand": 15,
            "water_window_1": [6, 8],
            "water_window_2": [18, 20],
        },
        "service_water_demands": {
            "cooking_water": {
                "daily_demand": {m: 7.5 for m in range(1, 13)},
                "usage_windows": [[5, 8], [17, 20], None],
                "demand_duration": 1,
                "pumping_head": 51,
            },
            "cleaning_water": {
                "daily_demand": {m: 100 for m in range(1, 13)},
                "usage_windows": [[7, 9], [16, 18], None],
                "demand_duration": 1,
                "pumping_head": 51,
            },
            "laundry_water": {
                "daily_demand": {m: 46.5 for m in range(1, 13)},
                "usage_windows": [[9, 12], None, None],
                "demand_duration": 2,
                "pumping_head": 51,
            },
            "bathing_water": {
                "daily_demand": {m: 100 for m in range(1, 13)},
                "usage_windows": [[6, 8], [19, 21], None],
                "demand_duration": 1,
                "pumping_head": 51,
            },
        },
        "agro_processing_machines": {},
    },
    # --- INDUSTRIES (50 establishments) ---
    "industries": {
        "num_users": 50,
        "months_present": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "working_days": [0, 1, 2, 3, 4, 5],  # Mon-Sat
        "appliances": {
            "indoor_lights": {
                "num_app": 4,
                "power": 15,
                "usage_window_1": [6, 18],
                "daily_usage_time": 6,
                "func_cycle": 10,
            },
            "workshop_machinery": {
                "num_app": 1,
                "power": 2500,
                "usage_window_1": [8, 17],
                "daily_usage_time": 3,
                "func_cycle": 30,
            },
            "refrigerator": {
                "num_app": 1,
                "power": 150,
                "usage_window_1": [0, 24],
                "daily_usage_time": 10,
                "func_cycle": 60,
            },
            "fan": {
                "num_app": 2,
                "power": 50,
                "usage_window_1": [10, 16],
                "daily_usage_time": 4,
                "func_cycle": 15,
            },
            "phone-charger": {
                "num_app": 2,
                "power": 5,
                "usage_window_1": [8, 17],
                "daily_usage_time": 3,
                "func_cycle": 30,
            },
        },
        "cooking_demands": {},
        "drinking_water_demand": {
            "daily_demand": 0,
            "water_window_1": [10, 12],
        },
        "service_water_demands": {
            "services": {
                "daily_demand": {m: 480 for m in range(1, 13)},
                "usage_windows": [[8, 12], [13, 17], None],
                "demand_duration": 1,
                "pumping_head": 51,
            },
        },
        "agro_processing_machines": {},
    },
    # --- SERVICES (88 establishments) ---
    "services": {
        "num_users": 88,
        "months_present": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "working_days": [0, 1, 2, 3, 4, 5],  # Mon-Sat
        "appliances": {
            "indoor_lights": {
                "num_app": 4,
                "power": 15,
                "usage_window_1": [7, 19],
                "daily_usage_time": 8,
                "func_cycle": 10,
            },
            "outdoor_lights": {
                "num_app": 2,
                "power": 15,
                "usage_window_1": [18, 22],
                "daily_usage_time": 4,
                "func_cycle": 10,
            },
            "refrigerator": {
                "num_app": 1,
                "power": 150,
                "usage_window_1": [0, 24],
                "daily_usage_time": 14,
                "func_cycle": 60,
            },
            "television": {
                "num_app": 1,
                "power": 80,
                "usage_window_1": [12, 18],
                "daily_usage_time": 4,
                "func_cycle": 15,
            },
            "pc": {
                "num_app": 1,
                "power": 65,
                "usage_window_1": [8, 17],
                "daily_usage_time": 8,
                "func_cycle": 30,
            },
            "fan": {
                "num_app": 2,
                "power": 50,
                "usage_window_1": [10, 17],
                "daily_usage_time": 5,
                "func_cycle": 15,
            },
            "air-conditioning": {
                "num_app": 1,
                "power": 1200,
                "usage_window_1": [11, 17],
                "daily_usage_time": 3,
                "func_cycle": 30,
            },
            "phone-charger": {
                "num_app": 3,
                "power": 5,
                "usage_window_1": [8, 18],
                "daily_usage_time": 4,
                "func_cycle": 30,
            },
        },
        "cooking_demands": {},
        "drinking_water_demand": {
            "daily_demand": 0,
            "water_window_1": [10, 12],
        },
        "service_water_demands": {
            "services": {
                "daily_demand": {m: 650 for m in range(1, 13)},
                "usage_windows": [[7, 12], [13, 18], None],
                "demand_duration": 1,
                "pumping_head": 51,
            },
        },
        "agro_processing_machines": {},
    },
    # --- COMMUNITY-WIDE (not attributable to individual households) ---
    "community_livestock": {
        "num_users": 1,
        "months_present": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "working_days": [0, 1, 2, 3, 4, 5, 6],
        "appliances": {},
        "cooking_demands": {},
        "drinking_water_demand": {
            "daily_demand": 0,
            "water_window_1": [10, 12],
        },
        "service_water_demands": {
            "livestock": {
                "daily_demand": {m: 50000 for m in range(1, 13)},
                "usage_windows": [[7, 9], [16, 18], None],
                "demand_duration": 2,
                "pumping_head": 51,
            },
        },
        "agro_processing_machines": {},
    },
}