import numpy as np
from copy import copy


from preprocessing import constants
from preprocessing.constants import prefix, suffix
from preprocessing.constants import months_defaults, working_day
from preprocessing import utils


class FormParser:

    def __init__(self, form=None):
        """
        Initialize the FormParser object.

        :param form: (optional) The form data to be parsed.
        :type form: dict or None

        Initializes the FormParser object with the given form data. If form is not None,
        the init_parser method is called to initialize the parser.

        Attributes:
        - form (dict or None): The form data to be parsed.
        - formtype (None): The type of the form.
        - suffix (None): The suffix used in the form.
        - prefix (None): The prefix used in the form.
        - cooking_demand (dict): A dictionary to store cooking demand data.
        - appliance_demand (dict): A dictionary to store appliance demand data.
        - drinking_water_demand (dict): A dictionary to store drinking water demand data.
        - service_water_demand (dict): A dictionary to store service water demand data.
        - agro_machine_demand (dict): A dictionary to store agro machine demand data.
        - months_prefix (str): The prefix used for months in the form.
        - output_dict (dict): A dictionary to store the parsed form data.

        Raises:
        - BaseException: If form is None and no form is provided.

        """
        self.form = form
        self.formtype = None
        self.suffix = None
        self.prefix = None

        self.cooking_demand = {}
        self.appliance_demand = {}
        self.drinking_water_demand = {}
        self.service_water_demand = {}
        self.agro_machine_demand = {}
        self.summary = {}

        self.months_prefix = "G_1b"

        self.output_dict = {}

        if form is not None:
            self.init_parser(form)

    def init_parser(self, form) -> None:
        """
        Initialize the FormParser object.

        :param form: The form data to be parsed.
        :type form: dict

        Initializes the FormParser object with the given form data.
        """
        self.form = form
        self.check_form_type()
        self.assign_prefix_suffix()

    def create_dictionary(self) -> dict:
        """
        Creates a dictionary needed for the ramp simulation, from the form data. If the form is from a local authority
        a different dictionary with a summary of the the whole survey is created.

        Raises:
        - BaseException: If the parser is not initialized with a form.

        :return: A dictionary with the parsed form data.
        """
        print(f"I am processing {self.formtype} form")
        if self.formtype == "local_aut":
            self.summary = self.create_local_aut_summary()
            return self.summary
        else:
            if self.prefix is not None and self.suffix is not None:
                self.output_dict["num_users"] = 1
                self.output_dict["months_present"] = self.read_months_of_presence()
                self.output_dict["working_days"] = self.read_working_days(
                    self.prefix["working_days"]
                )
                self.output_dict["appliances"] = self.create_elec_appliance_demand(
                    self.prefix["electric"]
                )
                self.output_dict["cooking_demands"] = self.create_cooking_demand(
                    self.prefix["cooking"], self.prefix["meal"]
                )
                self.output_dict["drinking_water_demand"] = (
                    self.create_drinking_water_demand(self.prefix["drinking_water"])
                )
                self.output_dict["service_water_demands"] = (
                    self.create_service_water_demand(self.prefix["service_water"])
                )

                if self.prefix["agro_machine"] is None:
                    self.output_dict["agro_processing_machines"] = {}
                else:
                    self.output_dict["agro_processing_machines"] = (
                        self.create_agroprocessing_demand(self.prefix["agro_machine"])
                    )
            else:
                raise BaseException(
                    "Please initialize the parser with a form before creating the dictionary"
                )
            return self.output_dict

    def check_form_type(self) -> None:
        """
        Check the form type based on the provided form data.

        This function iterates over the items in the form dictionary and checks if the form type key is present in any of the keys. If it is, it checks if the corresponding value is "yes". If a matching form type is found, it assigns it to the `formtype` attribute of the object. If no form type is found, it assigns the default form type.

        :return: None
        :raises ValueError: If the form type is not known.

        """
        types = {
            key: val for key, val in self.form.items() if constants.formtype_key in key
        }
        self.formtype = next(
            (
                form_t
                for form_t in constants.formtype_names
                if f"{constants.formtype_key}{form_t}" in types
                and self.form[f"{constants.formtype_key}{form_t}"] == "yes"
            ),
            constants.formtype_names[0],
        )
        if self.formtype is None:
            raise ValueError("Form type not known")

    def assign_prefix_suffix(self) -> None:
        """
        Assign the prefix and suffix based on the form type.

        Raises:
                ValueError: If the form type is missing.
        """
        if self.formtype is not None:
            self.prefix = prefix.get(self.formtype)
            self.suffix = suffix.get(self.formtype)
        else:
            raise ValueError("Missing suffix and prefix for form type")

    def create_cooking_demand(self, cooking_prefix: str, meal_prefix: str) -> dict:
        """
        Create cooking demand dictionary based on cooking and meal prefixes.

        Args:
            cooking_prefix (str): Prefix for cooking data.
            meal_prefix (str): Prefix for meal data.

        Returns:
            dict: Cooking demand dictionary.
        """
        cook_dic = self.read_cooking(cooking_prefix)
        meal_dic = self.read_meal(meal_prefix, list(cook_dic.keys()))

        for key in meal_dic.keys():
            meal_dic[key]["fuel_amount"] = cook_dic[meal_dic[key]["fuel"]][
                "fuel_amount"
            ]

        self.cooking_demand = meal_dic

        return self.cooking_demand

    def create_service_water_demand(self, prefix):
        rainy_season = None

        for key in prefix.keys():
            print(key)
            if 'irrigation' in key or 'animal_water' in key:
                if key == "animal_water":
                    name = "livestock"
                else:
                    name = key
                rainy_season = self.form[f"{prefix['irrigation']}/dry_season{self.suffix}"]
                if self.form[f"{prefix[key]}/{key}{self.suffix}"] == "yes":         
                    self.service_water_demand[name] = self.read_service_water(name, prefix[key], rainy_season)
            else:
                self.service_water_demand[key] = self.read_service_water(key, prefix[key])
            
            return self.service_water_demand
        
            '''
            irr_dict = self.read_irr_water(prefix["irrigation_water"])
            animal_dict = self.read_animal_water(
                prefix["animal_water"], prefix["irrigation_water"]
            )

            self.service_water_demand = {
                "irrigation": irr_dict,
                "livestock": animal_dict,
            }
            return self.service_water_demand
        else:
            self.service_water_demand = {"services": self.read_service_water(prefix)}'''

    def create_drinking_water_demand(self, drinking_prefix):
        unit_of_measurement = self.form[
            f"{drinking_prefix}/drinking_express{self.suffix}"
        ]
        unit = float(self.form[f"{drinking_prefix}/drink_use{self.suffix}"])
        string_drink_window = self.form[f"{drinking_prefix}/drink_time{self.suffix}"]

        if "buck" in unit_of_measurement:
            buck_conversion = float(
                self.form[f"{drinking_prefix}/drink_dim{self.suffix}"]
            )
        else:
            buck_conversion = None

        consume = utils.convert_perliter(unit_of_measurement, unit, buck_conversion)
        drink_usage_time = utils.extract_time_windows(string_drink_window)

        time_window = self.form[f"{drinking_prefix}/drink_time{self.suffix}"].split()

        # self.drinking_water_demand = {"daily_demand" : consume, "water_window" : utils.convert_usage_windows(drink_usage_time) }
        self.drinking_water_demand = {"daily_demand": consume}
        win = utils.convert_usage_windows_2(drink_usage_time)
        for key, item in win.items():
            self.drinking_water_demand[f"water_{key}"] = item
        return self.drinking_water_demand

    def create_elec_appliance_demand(self, electric_prefix):
        app_dict = {}

        for key, data in self.form.items():
            if electric_prefix in key and "_power" in key:
                app_name = key.split(sep="/")[1].split(sep="_power")[0]
                number = float(
                    self.form[f"{electric_prefix}/{app_name}_number{self.suffix}"]
                )
                power = float(
                    self.form[f"{electric_prefix}/{app_name}_power{self.suffix}"]
                )
                hour = float(
                    self.form[f"{electric_prefix}/{app_name}_hour_wd{self.suffix}"]
                )
                switch_on = int(
                    self.form[f"{electric_prefix}/{app_name}_min_on{self.suffix}"]
                )
                string = self.form[
                    f"{electric_prefix}/{app_name}_usage_wd{self.suffix}"
                ]

                usage_wd_dict = utils.extract_time_windows(string)

                usage_wd = utils.convert_usage_windows_2(usage_wd_dict)

                app_dict[app_name] = {
                    "num_app": number,  # quantity of appliance
                    "power": power,  # appliance power in W
                    "daily_usage_time": hour,  # appliance operating usage time in min
                    "func_cycle": switch_on,
                    # "time_window_1" : usage_wd                           # appliance usage windows
                }
                for key, item in usage_wd.items():
                    app_dict[app_name][f"usage_{key}"] = item

        self.appliance_demand = app_dict
        # print(self.appliance_demand)
        return self.appliance_demand

    def create_agroprocessing_demand(self, agro_prefix):
        for key, data in self.form.items():
            if f"{agro_prefix}/" in key and f"_motor{self.suffix}" in key:
                mach_name = key.replace(f"{agro_prefix}/", "", 1).replace(
                    f"_motor{self.suffix}", "", 1
                )  # machinery name
                fuel_AP = self.form[f"{agro_prefix}/{mach_name}_motor{self.suffix}"]
                product = self.form[
                    f"{agro_prefix}/{mach_name}_prod_onerun{self.suffix}"
                ]
                hourly_prod = self.form[
                    f"{agro_prefix}/{mach_name}_hour_prod{self.suffix}"
                ]
                efficiency = self.form[f"{agro_prefix}/{mach_name}_eff{self.suffix}"]
                hour_AP = self.form[f"{agro_prefix}/{mach_name}_hour{self.suffix}"]
                string_AP = self.form[f"{agro_prefix}/{mach_name}_usage{self.suffix}"]

                usage_AP_dict = utils.extract_time_windows(string_AP)

                months_AP = {
                    "January": float(
                        self.form[f"{agro_prefix}/{mach_name}_prod_jan{self.suffix}"]
                    ),
                    "February": float(
                        self.form[f"{agro_prefix}/{mach_name}_prod_feb{self.suffix}"]
                    ),
                    "March": float(
                        self.form[f"{agro_prefix}/{mach_name}_prod_mar{self.suffix}"]
                    ),
                    "April": float(
                        self.form[f"{agro_prefix}/{mach_name}_prod_apr{self.suffix}"]
                    ),
                    "May": float(
                        self.form[f"{agro_prefix}/{mach_name}_prod_may{self.suffix}"]
                    ),
                    "June": float(
                        self.form[f"{agro_prefix}/{mach_name}_prod_jun{self.suffix}"]
                    ),
                    "July": float(
                        self.form[f"{agro_prefix}/{mach_name}_prod_jul{self.suffix}"]
                    ),
                    "August": float(
                        self.form[f"{agro_prefix}/{mach_name}_prod_aug{self.suffix}"]
                    ),
                    "September": float(
                        self.form[f"{agro_prefix}/{mach_name}_prod_sep{self.suffix}"]
                    ),
                    "October": float(
                        self.form[f"{agro_prefix}/{mach_name}_prod_oct{self.suffix}"]
                    ),
                    "November": float(
                        self.form[f"{agro_prefix}/{mach_name}_prod_nov{self.suffix}"]
                    ),
                    "December": float(
                        self.form[f"{agro_prefix}/{mach_name}_prod_dec{self.suffix}"]
                    ),
                }

                for k in months_AP:
                    months_AP[k] = utils.convert_perday(
                        months_AP[k],
                        self.form[f"{agro_prefix}/{mach_name}_prod_exp{self.suffix}"],
                    )
                months_AP = utils.rename_keys(months_AP)

                if mach_name == "husker":
                    mach_name = "husking_mill"

                self.agro_machine_demand[mach_name] = {
                    "fuel": fuel_AP,  # agroprocessing machine fuel
                    "crop_processed_per_run": float(
                        product
                    ),  # crop processed [kg] per run
                    "throughput": float(
                        hourly_prod
                    ),  # [kg] of crop processed per [h] of machine operation
                    "crop_processed_per_fuel": float(
                        efficiency
                    ),  # crop processed [kg] per unit of fuel
                    "usage_time": float(hour_AP),  # machine operating usage time in min
                    # "time_window": utils.convert_usage_windows(usage_AP_dict),    # machine usage windows
                    "crop_processed_per_day": months_AP,  # crop processed on a typical working day for each months
                }
                for key, item in utils.convert_usage_windows_2(usage_AP_dict).items():
                    self.agro_machine_demand[mach_name][f"usage_{key}"] = item

        return self.agro_machine_demand

    def create_local_aut_summary(self):

        # Small farm numerosity
        number_hh = float(self.form[f"{self.prefix['village_composition']}/HS_HH"])
        number_low_income = float(
            self.form[f"{self.prefix['village_composition']}/HS_lower"]
        )
        number_medium_income = float(
            self.form[f"{self.prefix['village_composition']}/HS_middle"]
        )
        number_high_income = float(
            self.form[f"{self.prefix['village_composition']}/HS_upper"]
        )

        # Large farm numerosity
        number_large_farm = float(
            self.form[f"{self.prefix['village_composition']}/number_large_farm"]
        )

        # Service numerosity
        primary_school = float(
            self.form[f"{self.prefix['education_composition']}/number_primary"]
        )
        secondary_school = float(
            self.form[f"{self.prefix['education_composition']}/number_secondary"]
        )
        hospital = float(
            self.form[f"{self.prefix['health_composition']}/number_hospital"]
        )
        health_centre = float(
            self.form[f"{self.prefix['health_composition']}/number_hc"]
        )
        health_post = float(
            self.form[f"{self.prefix['health_composition']}/numbert_hp"]
        )

        religeus_building = float(
            self.form[f"{self.prefix['religion_composition']}/number_worship"]
        )
        other_service = float(
            self.form[f"{self.prefix['religion_composition']}/number_other_serv"]
        )

        # Business numberosity

        household_numerosity = {
            "low_income_hh": number_low_income,
            "medium_income_hh": number_medium_income,
            "high_income_hh": number_high_income,
            "total_hh": number_hh,
        }

        farm_numerosity = {"large_farm_numerosity": number_large_farm}

        service_numerosity = {
            "school_numerosity": primary_school,
            "secondary_school_numerosity": secondary_school,
            "hospital_numerosity": hospital,
            "health_centre_numerosity": health_centre,
            "health_post_numerosity": health_post,
            "religeus_building_numerosity": religeus_building,
            "other_service_numerosity": other_service,
        }

    # reading functions

    def read_working_days(self, prefix):
        if prefix is not None:
            string_day = self.form[f"{prefix}/working_day{self.suffix}"]
            working = []

            for day in working_day:
                if day in string_day:
                    working.append(working_day[day])

            return working
        else:
            return list(range(7))

    def read_months_of_presence(self):
        string_months = self.form[f"{self.months_prefix}/residency_month"]
        months = []
        for month in months_defaults.keys():
            if month in string_months:
                months.append(months_defaults[month])
        return months

    def read_irr_water(self, irr_water_prefix):
        if self.form[f"{irr_water_prefix}/irrigation{self.suffix}"] == "yes":

            pumping_head_irr = float(
                self.form[f"{irr_water_prefix}/pump_head_irr{self.suffix}"]
            )
            demand_time_irr = float(
                self.form[f"{irr_water_prefix}/irr_time{self.suffix}"]
            )

            uom_dry_irr = self.form[f"{irr_water_prefix}/express_dry{self.suffix}"]
            unit_dry_irr = float(
                self.form[f"{irr_water_prefix}/irrigation_dry{self.suffix}"]
            )
            string_irr_dry_window = self.form[
                f"{irr_water_prefix}/usage_dry{self.suffix}"
            ]

            if "buck" in uom_dry_irr:
                buck_conversion = float(
                    self.form[f"{irr_water_prefix}/dim_dry{self.suffix}"]
                )
            else:
                buck_conversion = None

            consume_dry_irr = utils.convert_perliter(
                uom_dry_irr, unit_dry_irr, buck_conversion
            )
            dry_irr_usage_time = utils.extract_time_windows(string_irr_dry_window)

            uom_rainy_irr = self.form[f"{irr_water_prefix}/express_rainy{self.suffix}"]
            unit_rainy_irr = float(
                self.form[f"{irr_water_prefix}/irrigation_rainy{self.suffix}"]
            )
            string_irr_rainy_window = self.form[
                f"{irr_water_prefix}/usage_rainy{self.suffix}"
            ]

            if "buck" in uom_rainy_irr:
                buck_conversion = float(
                    self.form[f"{irr_water_prefix}/dim_rainy{self.suffix}"]
                )
            else:
                buck_conversion = None

            consume_rainy_irr = utils.convert_perliter(
                uom_rainy_irr, unit_rainy_irr, buck_conversion
            )
            rainy_irr_usage_time = utils.extract_time_windows(string_irr_rainy_window)

            string_rainy = self.form[f"{irr_water_prefix}/dry_season{self.suffix}"]

            season_dict = copy(months_defaults)
            for month in season_dict:
                if month in string_rainy:
                    season_dict[month] = consume_rainy_irr
                else:
                    season_dict[month] = consume_dry_irr

            irr_season_dict = utils.rename_keys(season_dict)

            irr_windows = {}

            for k in dry_irr_usage_time.keys():
                irr_windows[k] = dry_irr_usage_time[k] + rainy_irr_usage_time[k]

            out_windows = utils.convert_usage_windows(irr_windows)
            while len(out_windows) < 3:
                out_windows.append(None)
            if len(out_windows) > 3:
                raise BaseException("got a problem, more than 3 windows")

            return {
                "daily_demand": irr_season_dict,  # irrigation water demand of typical day for each month
                # "irr_window_dry": utils.convert_usage_windows(dry_irr_usage_time),      # irrigation water time window (dry season)
                # "irr_window_rainy" : utils.convert_usage_windows(rainy_irr_usage_time), # irrigation water time window (rainy season)
                "usage_windows": out_windows,
                "pumping_head": pumping_head_irr,
                "demand_duration": demand_time_irr,
            }
        else:
            return {}

    def read_service_water(self, key, prefix, rainy_season = None):
        ## Setting keys names
        if key == "irrigation":
            uom_key = "express"
            unit_key = "irrigation"
            window_key = "usage"
            pump_key = "pump_head_irr"
            demand_time_key = "irr_time"
            dim_key = "dim"

        elif key == "livestock":
            uom_key = "exprerss_animal"
            unit_key = "animal"
            window_key = "usage_animal"
            pump_key = "pump_head_animal"
            demand_time_key = "animal_time"
            dim_key = "dim_anim"
        else:
            uom_key = "service_express"
            unit_key = "serv_use"
            window_key = "serv_time"
            pump_key = "pump_head"
            demand_time_key = "serv_duration"
            dim_key = "serv_dim"
        
        buck_conversion = None
        monthly_consumes = {}
        if rainy_season is None:
            rainy_season = list(constants.months_defaults.keys())

        pumping_head = float(self.form[f"{prefix}/{pump_key}{self.suffix}"])
        demand_time = float(self.form[f"{prefix}/{demand_time_key}{self.suffix}"])

        # Computing consumes and usage times
        consumes = {}
        usage_time = {key: False for key in constants.USAGE_WD_DEFAULTS}

        ## Reading info about WASH consumes
        if key == "services":
            uom = self.form[f"{prefix}/{uom_key}{self.suffix}"]
            unit = float(self.form[f"{prefix}/{unit_key}{self.suffix}"])
            string_window = self.form[f"{prefix}/{window_key}{self.suffix}"]
            usage_time = utils.extract_time_windows(string_window)

            if "buck" in uom:
                    buck_conversion = float(self.form[f"{prefix}/{dim_key}{self.suffix}"])
            consumes['rainy'] = utils.convert_perliter(uom, unit, buck_conversion) # If service water from wash is read, all monthly consumes are the same, rainy is set as a convention
        ## Reading info about irrigation and livestock consumes
        else:
            for season in ["dry", "rainy"]:
                unit = float(self.form[f"{prefix}/{unit_key}_{season}{self.suffix}"])
                uom = self.form[f"{prefix}/{uom_key}_{season}{self.suffix}"]
                string_window = self.form[f"{prefix}/{window_key}_{season}{self.suffix}"]
            
                # Converting to liters    
                if "buck" in uom:
                    buck_conversion = float(self.form[f"{prefix}/{dim_key}_{season}{self.suffix}"])

                consume = utils.convert_perliter(uom, unit, buck_conversion)
                consumes[season] = consume

                temp = utils.extract_time_windows(string_window)
                for key in usage_time.keys():
                    usage_time[key] += temp[key]

        ## Setting windows
        out_windows = utils.convert_usage_windows(usage_time)
        while len(out_windows) < 3:
            out_windows.append(None)

        ## Setting monthly consumes
        
        for i, month in enumerate(months_defaults):
            if month in rainy_season:
                monthly_consumes[i+1] = consumes['rainy']
            else:
                monthly_consumes[i+1] = consumes['dry']
    
        return {
            "daily_demand": monthly_consumes,
            "usage_windows": out_windows,
            "pumping_head": pumping_head,
            "demand_duration": demand_time,
        }

    def read_animal_water(self, a_water_prefix, irr_water_prefix):
        if self.form[f"{a_water_prefix}/animal_water{self.suffix}"] == "yes":
            pumping_head_animal = float(
                self.form[f"{a_water_prefix}/pump_head_animal{self.suffix}"]
            )
            demand_time_animal = float(
                self.form[f"{a_water_prefix}/animal_time{self.suffix}"]
            )

            uom_dry_animal = self.form[
                f"{a_water_prefix}/express_animal_dry{self.suffix}"
            ]
            unit_dry_animal = float(
                self.form[f"{a_water_prefix}/animal_dry{self.suffix}"]
            )
            string_animal_dry_window = self.form[
                f"{a_water_prefix}/usage_animal_dry{self.suffix}"
            ]

            if "buck" in uom_dry_animal:
                buck_conversion = float(
                    self.form[f"{a_water_prefix}/dim_anim_dry{self.suffix}"]
                )
            else:
                buck_conversion = None

            consume_dry_animal = utils.convert_perliter(
                uom_dry_animal, unit_dry_animal, buck_conversion
            )
            dry_animal_usage_time = utils.extract_time_windows(string_animal_dry_window)

            uom_rainy_animal = self.form[
                f"{a_water_prefix}/express_animal_rainy{self.suffix}"
            ]
            unit_rainy_animal = float(
                self.form[f"{a_water_prefix}/animal_rainy{self.suffix}"]
            )
            string_animal_rainy_window = self.form[
                f"{a_water_prefix}/usage_animal_rainy{self.suffix}"
            ]

            if "buck" in uom_rainy_animal:
                buck_conversion = float(
                    self.form[f"{a_water_prefix}/dim_anim_rainy{self.suffix}"]
                )
            else:
                buck_conversion = None

            consume_rainy_animal = utils.convert_perliter(
                uom_rainy_animal, unit_rainy_animal, buck_conversion
            )
            rainy_animal_usage_time = utils.extract_time_windows(
                string_animal_rainy_window
            )

            string_rainy_animal = self.form[
                f"{irr_water_prefix}/dry_season{self.suffix}"
            ]
            season_dict_animal = copy(months_defaults)

            for month in season_dict_animal:
                if month in string_rainy_animal:
                    season_dict_animal[month] = consume_rainy_animal
                else:
                    season_dict_animal[month] = consume_dry_animal

            anim_season_dict = utils.rename_keys(season_dict_animal)

            a_windows = {}

            for k in dry_animal_usage_time.keys():
                a_windows[k] = dry_animal_usage_time[k] + rainy_animal_usage_time[k]

            out_windows = utils.convert_usage_windows(a_windows)
            while len(out_windows) < 3:
                out_windows.append(None)
            if len(out_windows) > 3:
                raise BaseException("got a problem, more than 3 windows")

            return {
                "daily_demand": anim_season_dict,  # animal water demand of typical day for each month
                # "animal_window_dry": utils.convert_usage_windows(dry_animal_usage_time),                        # animal water time window (dry season)
                # "animal_window_rainy" : utils.convert_usage_windows(rainy_animal_usage_time),                    # animal water time window (rainy season)
                "usage_windows": out_windows,
                "pumping_head": pumping_head_animal,
                "demand_duration": demand_time_animal,
            }
        else:
            return {}

    def read_service_water_1(self, prefix):
        service_water_dict_B = {}

        unit_of_measurement_serv = self.form[f"{prefix}/service_express{self.suffix}"]
        unit_serv = float(self.form[f"{prefix}/serv_use{self.suffix}"])
        string_serv_window = self.form[f"{prefix}/serv_time{self.suffix}"]
        pumping_head = float(self.form[f"{prefix}/pump_head{self.suffix}"])
        demand_time = float(self.form[f"{prefix}/serv_duration{self.suffix}"])

        if "buck" in unit_of_measurement_serv:
            buck_conversion = float(self.form[f"{prefix}/serv_dim{self.suffix}"])
        else:
            buck_conversion = None

        consume_serv = utils.convert_perliter(
            unit_of_measurement_serv, unit_serv, buck_conversion
        )
        service_usage_time = utils.extract_time_windows(string_serv_window)

        daily_demand = copy(months_defaults)
        daily_water_demand = utils.set_values(daily_demand, consume_serv)

        out_windows = utils.convert_usage_windows(service_usage_time)
        while len(out_windows) < 3:
            out_windows.append(None)

        return {
            "daily_demand": daily_water_demand,
            "usage_windows": out_windows,
            "pumping_head": pumping_head,
            "demand_duration": demand_time,
        }

    def read_cooking(self, cooking_prefix):
        cook_dict = {}

        for key, data in self.form.items():
            if cooking_prefix in key and "unit" in key:
                fuel_name = key.replace(cooking_prefix, "", 1).replace(
                    f"_unit{self.suffix}", "", 1
                )
                time_cons = self.form[f"{cooking_prefix}{fuel_name}_time{self.suffix}"]
                unit = self.form[f"{cooking_prefix}{fuel_name}_unit{self.suffix}"]
                quantity = float(
                    self.form[f"{cooking_prefix}{fuel_name}_amount{self.suffix}"]
                )

                if unit == "bag" or unit == "cylinder":
                    bag_to_kg = float(
                        self.form[f"{cooking_prefix}{fuel_name}_bag{self.suffix}"]
                    )
                else:
                    bag_to_kg = None

                q = utils.convert_perkg(quantity, unit, fuel_name, bag_to_kg)
                daily_cons = utils.convert_perday(q, time_cons)

                cook_dict[fuel_name.split(sep="/")[1]] = {
                    "time": time_cons,  # time window to express fuel consumption
                    "unit": unit,  # unit to express fuel consumption
                    "quantity": quantity,  # quantity of unit consumption in the time window
                    "fuel_amount": daily_cons,  # daily fuel consumption
                }

        return cook_dict

    def read_meal(self, meal_prefix, cooking_fuels):
        meal_dict = {}
        for key, data in self.form.items():
            if meal_prefix in key and "meal_per_day" in key:
                n_meal = utils.how_many_meal(
                    self.form[f"{meal_prefix}/meal_per_day{self.suffix}"]
                )
                for n in np.arange(n_meal) + 1:
                    fuel = self.form[f"{meal_prefix}/fuels_meal{n}{self.suffix}"].split(
                        sep="_"
                    )[1]
                    if fuel not in cooking_fuels:
                        raise ValueError(
                            "This fuel has not be defined in cooking fuels"
                        )

                    cooking_device = self.form[
                        f"{meal_prefix}/cooking_meal{n}{self.suffix}"
                    ]
                    string_meal_window = self.form[
                        f"{meal_prefix}/usage_meal{n}{self.suffix}"
                    ]
                    cooking_time = float(
                        self.form[f"{meal_prefix}/time_meal{n}{self.suffix}"]
                    )
                    meal_usage_time = utils.extract_time_windows(string_meal_window)

                    meal_time_window = utils.convert_usage_windows(meal_usage_time)

                    meal_dict[f"meal_{n}"] = {
                        "fuel": fuel,  # fuel used for meals
                        "stove": cooking_device,  # stove used for meals
                        "cooking_window_start": meal_time_window[0][
                            0
                        ],  # meals time window
                        "cooking_window_end": meal_time_window[0][1],
                        # "cooking_time": float(meal_time_window[0][1])-float(meal_time_window[0][0]) # Simone defined cooking time like this, but we have the question for this
                        "cooking_time": cooking_time,  # <-- this has to be < window_time
                    }
        return meal_dict


if __name__ == "__main__":

    forms = utils.get_survey(survey_id="affG8Fq5Suc99Sg9UB5hPv")
    formparser = FormParser(forms[3])
    formparser.create_dictionary()

    # print(formparser.appliance_demand)
    # print(formparser.cooking_demand)
    # print(formparser.output_dict['cooking_demand'])

    print(formparser.formtype)
    # print(formparser.output_dict['appliances'])

    print(formparser.output_dict["service_water_demands"])
