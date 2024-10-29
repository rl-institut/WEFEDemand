import numpy as np
from copy import copy


from preprocessing import constants
from preprocessing.constants import prefix, suffix
from preprocessing.constants import months_defaults, working_day
from preprocessing import utils


class FormParser:

    def __init__(self, form=None, verbose=False) -> None:
        """
        Initialize the FormParser object.

        :param form: (optional) The form data to be parsed.
        :type form: dict or None

        Initializes the FormParser object with the given form data. If form is not None,
        the init_parser method is called to initialize the parser.

        Attributes:
        - form (dict or None): The form data to be parsed.
        - formtype (None): The type of the form.
        - suffix (dict): The suffix used in the form. This dictionary is set when the form initialized. The information are retrieved from constants.
        - prefix (dict): The prefix used in the form. This dictionary is set when the form initialized. The information are retrieved from constants.
        - subtype_info (dict): The subtype information of the form. This is needed for the computation of numerosity of users by SurveyParser. This dictionary is set when the form initialized. The information are retrieved from constants.
        - cooking_demand (dict): A dictionary to store cooking demand data.
        - appliance_demand (dict): A dictionary to store appliance demand data.
        - drinking_water_demand (dict): A dictionary to store drinking water demand data.
        - service_water_demand (dict): A dictionary to store service water demand data.
        - agro_machine_demand (dict): A dictionary to store agro machine demand data.
        - months_prefix (str): The prefix used for months in the form.
        - output_dict (dict): A dictionary to store the parsed form data.
        - TIME_PROBLEM (bool): A flag to indicate whether there is a time problem in the form comparing time windows and usage time.

        Raises:
        - BaseException: If form is None and no form is provided.

        """
        self.verbose = verbose

        self.form = form
        self.formtype = None
        self.suffix = None
        self.prefix = None
        self.subtype_info = None

        self.cooking_demand = {}
        self.appliance_demand = {}
        self.drinking_water_demand = {}
        self.service_water_demand = {}
        self.agro_machine_demand = {}
        self.summary = {}

        self.TIME_PROBLEM = False
        self.months_prefix = constants.MONTHS_PREFIX

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
        self.TIME_PROBLEM = False
        self.check_form_type()
        self.read_subtype_info()
        self.assign_prefix_suffix()

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

    def read_subtype_info(self):
        """
        Read subtype information from the form data.

        For households, this is the monthly revenue.
        For services and businesses, this is the type of service or business.
        """
        if self.formtype == "household":
            # Get the monthly revenue
            rev_t = self._read_form(
                "H_3/time_rev_H", default="daily", formtype=self.form["_id"]
            )
            rev_q = float(
                self._read_form("H_3/revenues_H", default=0, formtype=self.form["_id"])
            )
            # Convert the revenue to a monthly value
            if "daily" in rev_t:
                self.subtype_info = rev_q * 30
            elif "weekly" in rev_t:
                self.subtype_info = rev_q * 4
            else:
                self.subtype_info = rev_q

        elif self.formtype == "service" or self.formtype == "business":
            # Get the type of service or business
            for key in self.form.keys():
                if "school" in key or "health_type" in key or "other_bus_S" in key:
                    self.subtype_info = self.form[key]
                elif (
                    "type_of_bus" in key
                    and "school" not in key
                    and "heath_type" not in key
                ):
                    self.subtype_info = self.form[key]
            if self.subtype_info is None:
                print(f"WARNING: subtype info not found for form {self.form['_id']}")
        else:
            self.subtype_info = None

    def create_dictionary(self, numerosity) -> dict:
        """
        Creates a dictionary needed for the ramp simulation, from the form data. If the form is from a local authority
        a different dictionary with a summary of the the whole survey is created.

        Raises:
        - BaseException: If the parser is not initialized with a form.

        :return: A dictionary with the parsed form data.
        """
        if self.verbose:
            print(f"I am processing form {self.form['_id']} which is a {self.formtype}")
        if self.formtype == "local_aut":
            self.summary = self.create_local_aut_summary()
            return self.summary
        else:
            if self.prefix is not None and self.suffix is not None:
                self.output_dict["num_users"] = numerosity
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
        """
        Create the service water demand for the following types of water:
        irrigation, livestock and service water.

        Args:
            prefix (dict): A dictionary with the prefixes for the different service water types.

        Returns:
            dict: A dictionary with the service water demand.
        """
        rainy_season = None

        # Iterate over the different service water types
        for key in prefix.keys():
            # Check if the type is irrigation or livestock
            if "irrigation" in key or "animal_water" in key:
                if key == "animal_water":
                    name = "livestock"
                else:
                    name = key
                # Get the rainy season for irrigation and livestock
                rainy_season = self._read_form(
                    f"{prefix['irrigation']}/dry_season{self.suffix}",
                    default="",
                    formtype=self.form["_id"],
                )
                # Check if the service water is used
                if self.form[f"{prefix[key]}/{key}{self.suffix}"] == "yes":
                    # Read the service water demand for irrigation and livestock
                    self.service_water_demand[name] = self.read_service_water(
                        name, prefix[key], rainy_season
                    )
            else:
                # Read the service water demand for service water
                self.service_water_demand[key] = self.read_service_water(
                    key, prefix[key]
                )

        return self.service_water_demand

    def create_drinking_water_demand(self, drinking_prefix):
        """
        Create the drinking water demand for a given prefix.

        Args:
            drinking_prefix (str): The prefix for the drinking water demand.

        Returns:
            dict: A dictionary with the drinking water demand.
        """
        # Get the unit of measurement for the drinking water
        unit_of_measurement = self.form[
            f"{drinking_prefix}/drinking_express{self.suffix}"
        ]
        # Get the amount of water used
        unit = float(self.form[f"{drinking_prefix}/drink_use{self.suffix}"])
        # Get the time window for the drinking water usage
        string_drink_window = self.form[f"{drinking_prefix}/drink_time{self.suffix}"]

        buck_conversion = None
        # Check if the unit of measurement is in buckets
        if "buck" in unit_of_measurement:
            buck_conversion = float(
                self.form[f"{drinking_prefix}/drink_dim{self.suffix}"]
            )
        # Calculate the drinking water demand
        consume = utils.convert_perliter(unit_of_measurement, unit, buck_conversion)
        # Extract the time windows for the drinking water usage
        drink_usage_time = utils.extract_time_windows(string_drink_window)

        # Create the drinking water demand dictionary
        self.drinking_water_demand = {"daily_demand": consume}
        # Add the time window information to the dictionary
        win, time_windows = utils.convert_usage_windows(drink_usage_time)

        for key, item in win.items():
            self.drinking_water_demand[f"water_{key}"] = item
        return self.drinking_water_demand

    def create_elec_appliance_demand(self, electric_prefix):
        """
        Create the electric appliance demand for a given prefix.

        Args:
            electric_prefix (str): The prefix for the electric appliance demand.

        Returns:
            dict: A dictionary with the electric appliance demand.
        """
        app_dict = {}

        # Loop through every appliance
        for key, data in self.form.items():
            if electric_prefix in key and "_power" in key:
                app_name = key.split(sep="/")[1].split(sep="_power")[0]

                # Get the number of appliances
                number = float(
                    self.form[f"{electric_prefix}/{app_name}_number{self.suffix}"]
                )
                # Get the power of the appliance
                power = float(
                    self.form[f"{electric_prefix}/{app_name}_power{self.suffix}"]
                )
                # Get the daily usage time of the appliance
                hour = float(
                    self.form[f"{electric_prefix}/{app_name}_hour_wd{self.suffix}"]
                )
                # Get the switch on time of the appliance
                switch_on = int(
                    self.form[f"{electric_prefix}/{app_name}_min_on{self.suffix}"]
                )
                # Get the time window of the appliance
                string = self.form[
                    f"{electric_prefix}/{app_name}_usage_wd{self.suffix}"
                ]

                # Extract the time windows for the appliance
                usage_wd_dict = utils.extract_time_windows(string)

                # Convert the time windows to a dictionary
                usage_wd, time_windows = utils.convert_usage_windows(usage_wd_dict)

                ## Check if demand time is less than windows time
                if utils.check_time(time_windows, hour):
                    self.TIME_PROBLEM = True

                # Add the time window information to the dictionary
                # Create the dictionary for this appliance
                app_dict[app_name] = {
                    "num_app": number,  # quantity of appliance
                    "power": power,  # appliance power in W
                    "daily_usage_time": hour,  # appliance operating usage time in min
                    "func_cycle": switch_on,
                    # "time_window_1" : usage_wd                           # appliance usage windows
                }
                # Add the time window information to the dictionary
                for key, item in usage_wd.items():
                    app_dict[app_name][f"usage_{key}"] = item

        # Store the results in the class
        self.appliance_demand = app_dict
        # Return the results
        return self.appliance_demand

    def create_agroprocessing_demand(self, agro_prefix):
        """
        Create a dictionary of agroprocessing machine demand based on the form data.

        Args:
            agro_prefix (str): The prefix of the form data for the agroprocessing section.

        Returns:
            dict: A dictionary containing the agroprocessing machine demand data.
        """

        # Reading consumption for every machine used
        month_name = [
            "jan",
            "feb",
            "mar",
            "apr",
            "may",
            "jun",
            "jul",
            "aug",
            "sep",
            "oct",
            "nov",
            "dec",
        ]
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

                # Extract the time windows for the machine
                usage_AP_dict = utils.extract_time_windows(string_AP)

                # Initialize a dictionary to store the crop processed per day
                months_AP = {}

                # Read the crop processed per day for each month
                for i, month in enumerate(month_name):
                    months_AP[i + 1] = float(
                        self.form[
                            f"{agro_prefix}/{mach_name}_prod_{month}{self.suffix}"
                        ]
                    )

                # Calculate the crop processed per day for each month
                for k in months_AP:
                    months_AP[k] = utils.convert_perday(
                        months_AP[k],
                        self.form[f"{agro_prefix}/{mach_name}_prod_exp{self.suffix}"],
                    )

                # Replace husker with husking_mill
                if mach_name == "husker":
                    mach_name = "husking_mill"

                # Create the dictionary for this machine
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
                    "crop_processed_per_day": months_AP,  # crop processed on a typical working day for each m
                }

                # Extract the time windows and convert them to a dictionary
                win, time_windows = utils.convert_usage_windows(usage_AP_dict)

                ## Check if demand time is less than windows time
                if utils.check_time(time_windows, float(hour_AP)):
                    self.TIME_PROBLEM = True

                # Add the time windows to the dictionary for this machine
                for key, item in win.items():
                    self.agro_machine_demand[mach_name][f"usage_{key}"] = item

        return self.agro_machine_demand

    def create_local_aut_summary(self):
        """
        Extract the numerosity of local authorities, households, services, businesses and large scale farms.
        """
        household_numerosity = {}
        service_numerosity = {}
        business_numerosity = {}

        # Household numerosity
        subtypes = constants.FORM_SUBTYPES["household"]
        household_numerosity[subtypes[0]] = int(
            self._read_form(
                f"{self.prefix['village_composition']}/HS_lower",
                default=0,
                formtype=self.formtype,
            )
        )
        household_numerosity[subtypes[1]] = int(
            self._read_form(
                f"{self.prefix['village_composition']}/HS_middle",
                default=0,
                formtype=self.form["_id"],
            )
        )
        household_numerosity[subtypes[2]] = int(
            self._read_form(
                f"{self.prefix['village_composition']}/HS_upper",
                default=0,
                formtype=self.form["_id"],
            )
        )
        household_numerosity["total_hh"] = int(
            self._read_form(f"{self.prefix['village_composition']}/HS_HH", default=0)
        )

        # Large farm numerosity
        subtypes = constants.FORM_SUBTYPES["large_scale_farm"]
        number_large_farm_numerosity = {
            subtypes: int(
                self._read_form(
                    f"{self.prefix['village_composition']}/number_large_farm", default=0
                )
            )
        }

        # Service numerosity
        subtypes = constants.FORM_SUBTYPES["service"]
        service_numerosity[subtypes[0]] = int(
            self._read_form(
                f"{self.prefix['education_composition']}/number_primary", default=0
            )
        )
        service_numerosity[subtypes[1]] = int(
            self._read_form(
                f"{self.prefix['education_composition']}/number_secondary", default=0
            )
        )
        service_numerosity[subtypes[2]] = int(
            self._read_form(
                f"{self.prefix['health_composition']}/number_hospital", default=0
            )
        )
        service_numerosity[subtypes[3]] = int(
            self._read_form(f"{self.prefix['health_composition']}/number_hc", default=0)
        )
        service_numerosity[subtypes[4]] = int(
            self._read_form(
                f"{self.prefix['health_composition']}/numbert_hp", default=0
            )
        )
        service_numerosity[subtypes[5]] = int(
            self._read_form(
                f"{self.prefix['religion_composition']}/number_worship", default=0
            )
        )
        service_numerosity[subtypes[6]] = int(
            self._read_form(
                f"{self.prefix['religion_composition']}/number_other_serv", default=0
            )
        )

        # Business numberosity
        business_numerosity = {}
        for b in constants.BUSINESS_KEYS:
            key = b.split("number_")[-1]
            business_numerosity[key] = int(
                self._read_form(f"{self.prefix['economy_composition']}/{b}", default=0)
            )

        # Update the summary
        self.summary["household"] = household_numerosity
        self.summary["large_scale_farm"] = number_large_farm_numerosity
        self.summary["service"] = service_numerosity
        self.summary["business"] = business_numerosity

        return self.summary

    # reading functions
    @utils.warn_and_skip
    def _read_form(self, key, default=None, formtype=None):
        return self.form[key]

    def read_working_days(self, prefix: str):
        """
        Reads the working days from the form data.

        Args:
            prefix (str): The prefix of the form data for the working days.

        Returns:
            List[int]: A list of integers representing the working days.
        """
        if prefix is not None:
            # Get the working days string from the form data
            string_day = self.form[f"{prefix}/working_day{self.suffix}"]
            working = []

            for day in working_day:
                if day in string_day:
                    working.append(working_day[day])
            return working
        else:
            # Return all days if no prefix is provided
            return list(range(7))

    def read_months_of_presence(self):
        string_months = self.form[f"{self.months_prefix}/residency_month"]
        months = []
        for month in months_defaults.keys():
            if month in string_months:
                months.append(months_defaults[month])
        return months

    def read_service_water(self, key, prefix, rainy_season=None):
        """
        Reads data related to service water consumption from the form. Handle three type of consumptions data:
            1. Irrigation
            2. Livestock
            3. Services

        Args:
            key (str): type of service water consumption, can be 'irrigation',
                'livestock', or 'services'.
            prefix (str): prefix for the keys to be read from the form.
            rainy_season (list of str, optional): months of the rainy season.
                Defaults to None.

        Returns:
            dict: A dictionary with the service water consumption data.
        """
        ## Setting keys names
        if key == "irrigation":
            uom_key = "express"
            unit_key = "irrigation"
            window_key = "usage"
            pump_key = "pump_head_irr"
            demand_time_key = "irr_time"
            dim_key = "dim"

        elif key == "livestock":
            uom_key = "express_animal"
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

        pumping_head = float(
            self._read_form(f"{prefix}/{pump_key}{self.suffix}", default=0.0)
        )
        demand_time = float(
            self._read_form(f"{prefix}/{demand_time_key}{self.suffix}", default=1.0)
        )

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
            consumes["rainy"] = utils.convert_perliter(
                uom, unit, buck_conversion
            )  # If service water from wash is read, all monthly consumes are the same, rainy is set as a convention
        ## Reading info about irrigation and livestock consumes
        else:
            for season in ["dry", "rainy"]:
                unit = float(
                    self._read_form(
                        f"{prefix}/{unit_key}_{season}{self.suffix}", default=0.0
                    )
                )
                uom = self._read_form(
                    f"{prefix}/{uom_key}_{season}{self.suffix}", default="liters"
                )
                string_window = self._read_form(
                    f"{prefix}/{window_key}_{season}{self.suffix}", default="0-7"
                )

                # Converting to liters
                if "buck" in uom:
                    buck_conversion = float(
                        self._read_form(
                            f"{prefix}/{dim_key}_{season}{self.suffix}", default=0.0
                        )
                    )

                consume = utils.convert_perliter(uom, unit, buck_conversion)
                consumes[season] = consume

                temp = utils.extract_time_windows(string_window)
                for key in usage_time.keys():
                    usage_time[key] += temp[key]

        ## Setting windows
        _, out_windows = utils.convert_usage_windows(usage_time)

        if utils.check_time(out_windows, demand_time / 60):
            self.TIME_PROBLEM = True

        while len(out_windows) < 3:
            out_windows.append(None)

        ## Setting monthly consumes

        for i, month in enumerate(months_defaults):
            if month in rainy_season:
                monthly_consumes[i + 1] = consumes["rainy"]
            else:
                monthly_consumes[i + 1] = consumes["dry"]

        ## Check if demand time is less than windows time

        return {
            "daily_demand": monthly_consumes,
            "usage_windows": out_windows,
            "pumping_head": pumping_head,
            "demand_duration": demand_time,
        }

    def read_cooking(self, cooking_prefix):
        """
        Read the cooking data from the form and store it in a dictionary.

        Args:
            cooking_prefix (str): The prefix for the form data related to cooking.

        Returns:
            dict: A dictionary where the keys are the names of the fuels and the
            values are dictionaries with the keys "time", "unit", "quantity", and
            "fuel_amount". "time" is the time window to express the fuel consumption,
            "unit" is the unit to express fuel consumption, "quantity" is the quantity of
            unit consumption in the time window, and "fuel_amount" is the daily fuel
            consumption.
        """
        cook_dict = {}

        for key, data in self.form.items():
            if cooking_prefix in key and "unit" in key:
                # Get the fuel name by removing the prefix and the suffix
                fuel_name = key.replace(cooking_prefix, "", 1).replace(
                    f"_unit{self.suffix}", "", 1
                )
                # Get the time window to express fuel consumption
                time_cons = self.form[f"{cooking_prefix}{fuel_name}_time{self.suffix}"]
                # Get the unit to express fuel consumption
                unit = self.form[f"{cooking_prefix}{fuel_name}_unit{self.suffix}"]
                # Get the quantity of unit consumption in the time window
                quantity = float(
                    self.form[f"{cooking_prefix}{fuel_name}_amount{self.suffix}"]
                )

                # If the unit is a bag or cylinder, get the conversion factor
                if unit == "bag" or unit == "cylinder":
                    bag_to_kg = float(
                        self.form[f"{cooking_prefix}{fuel_name}_bag{self.suffix}"]
                    )
                else:
                    bag_to_kg = None

                # Convert the quantity to kilograms
                q = utils.convert_perkg(quantity, unit, fuel_name, bag_to_kg)
                # Convert the quantity to daily consumption
                daily_cons = utils.convert_perday(q, time_cons)

                # Store the data in the dictionary
                cook_dict[fuel_name.split(sep="/")[1]] = {
                    "time": time_cons,  # time window to express fuel consumption
                    "unit": unit,  # unit to express fuel consumption
                    "quantity": quantity,  # quantity of unit consumption in the time window
                    "fuel_amount": daily_cons,  # daily fuel consumption
                }
            for key in self.form:
                if cooking_prefix in key and "fuels_" in key:
                    if type(self.form[key]) is dict and "elec" in self.form[key]:
                        cook_dict["elec"] = {
                            "time": 1,
                            "unit": 1,
                            "quantity": 1,
                            "fuel_amount": 1,
                        }

        return cook_dict

    def read_meal(self, meal_prefix, cooking_fuels):
        """
        Read the data of meals from the form and store it in a dictionary.

        Args:
            meal_prefix (str): The prefix of the form data for the meal section.
            cooking_fuels (list): A list of the fuels used for cooking.

        Returns:
            dict: A dictionary containing the data of meals.
        """
        meal_dict = {}
        for key, data in self.form.items():
            if meal_prefix in key and "meal_per_day" in key:
                # Get the number of meals per day
                n_meal = utils.how_many_meal(
                    self.form[f"{meal_prefix}/meal_per_day{self.suffix}"]
                )
                for n in np.arange(n_meal) + 1:
                    # Get the fuel used for the meal
                    fuel = self.form[f"{meal_prefix}/fuels_meal{n}{self.suffix}"].split(
                        sep="fuel_"
                    )[1]
                    if fuel not in cooking_fuels:
                        raise ValueError(
                            f"Fuel {fuel} has not been defined in cooking fuels: {cooking_fuels}"
                        )

                    # Get the stove used for the meal
                    cooking_device = self.form[
                        f"{meal_prefix}/cooking_meal{n}{self.suffix}"
                    ]
                    # Get the time window of the meal
                    string_meal_window = self.form[
                        f"{meal_prefix}/usage_meal{n}{self.suffix}"
                    ]
                    cooking_time = float(
                        self.form[f"{meal_prefix}/time_meal{n}{self.suffix}"]
                    )
                    meal_usage_time = utils.extract_time_windows(string_meal_window)

                    # Get the time window of the meal
                    _, meal_time_window = utils.convert_usage_windows(meal_usage_time)

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

                    if utils.check_time(meal_time_window, cooking_time):
                        self.TIME_PROBLEM = True
        return meal_dict
