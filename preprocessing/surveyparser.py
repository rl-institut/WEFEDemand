import os
import warnings
import numpy as np

from copy import copy

from preprocessing.formparser import FormParser
from preprocessing.utils import load_kobo_data, warn_and_skip
from preprocessing import constants


class SurveyParser:
    def __init__(self, survey_key=None, token=None, verbose=False) -> None:
        self.verbose = verbose

        self.formparser = FormParser()
        self.survey_key = survey_key
        self.survey = None
        self.token = token
        self.n_forms = {
            key: {} for key in constants.formtype_names if key != "local_aut"
        }  # list of form ids grouped first by type, then by subtype
        self.numerosity = {}
        self.type_form_per_id = {
            constants.formtype_names[i]: []
            for i in range(len(constants.formtype_names))
        }  # list of form ids grouped by type
        self.forms = {}
        self.local_aut = None
        self.morethanone = False
        if self.survey_key is None or self.token is None:
            try:
                self.init_parser()
            except:
                raise ValueError(
                    "Survey key and kobo api token not given and not found in system environment"
                )

    def init_parser(self) -> None:
        self.survey_key, self.token = os.getenv("SURVEY_KEY"), os.getenv("KOBO_TOKEN")

    def read_survey(self) -> None:
        """
        Read the forms from the survey with the given key and token.

        The data is stored in the following attributes:
        - type_form_per_id (dict): A dictionary with the form type as key and a list of form ids as value.
        - forms (dict): A dictionary with the form id as key and the form data as value.
        - local_aut (dict): The data of the Local Authority form.
        - morethanone (bool): Whether more than one Local Authority form has been found.
        - n_forms (dict): A dictionary with the form type as key and a dictionary with subtype info as key and a list of form ids as value.

        :return: None
        """
        self.survey, _ = load_kobo_data(self.survey_key, self.token)
        for i, form in enumerate(self.survey):
            if self.verbose:
                print("Processing form {}".format(form["_id"]))
            self.formparser.init_parser(form)
            type = copy(self.formparser.formtype)

            subtype_info = self.formparser.subtype_info

            # group forms by type
            self.type_form_per_id[type].append(form["_id"])

            # list form per id
            self.forms[form["_id"]] = form

            if type == "local_aut":
                if not self.morethanone:
                    self.local_aut = form
                    self.morethanone = True
                else:
                    temp_id = self.local_aut["_id"]
                    print(
                        f"WARNING: More than one Local Authority form found. Will use the first one: {temp_id}"
                    )
                continue

            # assign subtype info and group them by type
            if subtype_info in self.n_forms[type].keys() and type != "household":
                self.n_forms[type][subtype_info].append(form["_id"])
            elif subtype_info not in self.n_forms[type].keys() and type != "household":
                self.n_forms[type][subtype_info] = [form["_id"]]
            # subtype info for household is revenues, this has to be further processed
            elif "revenues" not in self.n_forms[type].keys() and type == "household":
                self.n_forms[type]["revenues"] = {
                    "ids": [form["_id"]],
                    "q": [self.formparser.subtype_info],
                }
            else:
                self.n_forms[type]["revenues"]["ids"].append(form["_id"])
                self.n_forms[type]["revenues"]["q"].append(self.formparser.subtype_info)

        self._divide_households()

    def process_survey(self, form_type=None, form_id=None) -> dict:
        """
        Process a selected subset of the forms in the survey.

        If form_id is given, the forms with the given ids are processed.
        If form_type is given and form_id is None, all forms of the given type are processed.
        If form_type is None and form_id is None, all forms in the survey are processed.

        :param form_type: The type of the form to be processed.
        :type form_type: str or None
        :param form_id: The id of the form to be processed.
        :type form_id: int or None
        :return: A dictionary with the processed form data.
        :rtype: dict
        """
        if self.local_aut is not None:
            self.formparser.init_parser(self.local_aut)
            self.summary = copy(self.formparser.create_dictionary(1))
        else:
            warnings.warn(
                "WARNING: No Local Authority form defined. Numerisity set to 1 for all forms."
            )

        self._get_numerosity_from_localaut_info()

        output = {}
        if self.survey is not None:
            ## Looping over all id forms given
            if form_id is not None:
                for id in form_id:
                    if self.verbose:
                        print("Processing form {}.".format(id))
                    try:
                        self.formparser.init_parser(self.forms[id])
                        temp = copy(
                            self.formparser.create_dictionary(
                                numerosity=self.numerosity[id]
                            )
                        )
                        if self.verbose:
                            print(f"Processed form {id}.")
                        print(self.formparser.TIME_PROBLEM)
                        if not self.formparser.TIME_PROBLEM:
                            output[id] = temp
                        elif self.verbose:
                            print(
                                f"Processed form {id}, but found a time problem, output not added for the simulation."
                            )
                    except Exception as e:
                        print(
                            f"WARNING: Could not process form {id}"
                            " Skipping this form."
                        )
                        if self.verbose:
                            print(f"ERROR: the error was: {str(e)}")
                        continue
            ## Looping over all forms of a specific type
            elif form_type is not None:
                for id in self.type_form_per_id[form_type]:
                    if self.verbose:
                        print("Processing form {}.".format(id))
                    try:
                        self.formparser.init_parser(self.forms[id])
                        temp = copy(
                            self.formparser.create_dictionary(
                                numerosity=self.numerosity[id]
                            )
                        )
                        if self.verbose:
                            print(f"Processed form {id}.")
                        if not self.formparser.TIME_PROBLEM:
                            output[id] = temp
                        elif self.verbose:
                            print(
                                f"Processed form {id}, but found a time problem, output not added for the simulation."
                            )
                    except Exception as e:
                        print(
                            f"WARNING: Could not process form {id}"
                            " Skipping this form."
                        )
                        if self.verbose:
                            print(f"ERROR: the error was: {str(e)}")
                        continue
            ## Looping over all forms
            elif form_type is None and form_id is None:
                for form in self.survey:
                    if self.verbose:
                        print("Processing form {}.".format(form["_id"]))
                    if form["_id"] in self.type_form_per_id["local_aut"]:
                        continue
                    try:
                        self.formparser.init_parser(form)
                        temp = copy(
                            self.formparser.create_dictionary(
                                numerosity=self.numerosity[form["_id"]]
                            )
                        )
                        if self.verbose:
                            print(f"Processed form {form['_id']}.")
                        if not self.formparser.TIME_PROBLEM:
                            output[form["_id"]] = temp
                        elif self.verbose:
                            print(
                                f"Processed form {form['_id']}, but found a time problem, output not added for the simulation."
                            )
                    except Exception as e:
                        print(
                            f"WARNING: Could not process form {form['_id']}"
                            " Skipping this form."
                        )
                        if self.verbose:
                            print(f"ERROR: the error was: {str(e)}")
                        continue
        else:
            raise BaseException("WARNING: No survey data defined.")

        return output

    def _divide_households(self) -> None:
        """
        Divide the households into three subtypes based on their monthly revenue.
        """
        type = "household"
        # Calculate the 33rd and 66th percentile of the monthly revenue
        T1 = np.percentile(self.n_forms[type]["revenues"]["q"], 33)
        T2 = np.percentile(self.n_forms[type]["revenues"]["q"], 66)

        # Initialize the subtypes
        self.n_forms[type][constants.FORM_SUBTYPES[type][0]] = []  # Low income
        self.n_forms[type][constants.FORM_SUBTYPES[type][1]] = []  # Medium income
        self.n_forms[type][constants.FORM_SUBTYPES[type][2]] = []  # High income

        # Loop through all the households
        for id in self.n_forms[type]["revenues"]["ids"]:
            # Check the monthly revenue and assign the household to the corresponding subtype
            if (
                self.n_forms[type]["revenues"]["q"][
                    self.n_forms[type]["revenues"]["ids"].index(id)
                ]
                <= T1
            ):
                self.n_forms[type][constants.FORM_SUBTYPES[type][0]].append(id)
            elif (
                self.n_forms[type]["revenues"]["q"][
                    self.n_forms[type]["revenues"]["ids"].index(id)
                ]
                > T1
                and self.n_forms[type]["revenues"]["q"][
                    self.n_forms[type]["revenues"]["ids"].index(id)
                ]
                <= T2
            ):
                self.n_forms[type][constants.FORM_SUBTYPES[type][1]].append(id)
            else:
                self.n_forms[type][constants.FORM_SUBTYPES[type][2]].append(id)

    def _get_numerosity_from_localaut_info(self) -> None:
        temp = {}

        list_subtype_in_survey = {}
        list_subtype_in_localaut = {}

        # list all service, household and business subtypes in localform
        for type in self.n_forms.keys():
            if type == "local_aut":
                continue
            for subtype in self.summary[type].keys():
                if subtype == "total_hh":
                    continue
                list_subtype_in_localaut[subtype] = self.summary[type][subtype]
            # list all service, household and business subtypes in survey
            for subtype in self.n_forms[type].keys():
                if subtype == "revenues" or subtype is None:
                    continue
                list_subtype_in_survey[subtype] = len(self.n_forms[type][subtype])
                # check if subtype is in local aut form
                if (
                    subtype not in self.summary[type].keys()
                    or self.summary[type][subtype] == 0
                ):
                    print(
                        f"WARNING: No Local Authority info found for {subtype}. Numerosity set to 1"
                    )
                    num = 1
                else:
                    # define numerosity
                    num = int(
                        self.summary[type][subtype] / len(self.n_forms[type][subtype])
                    )

                temp[subtype] = num

        for subtype, num in list_subtype_in_localaut.items():
            if subtype not in list_subtype_in_survey.keys() and num != 0:
                print(
                    f"WARNING: {subtype} info given in Local Authority form with value {num}, but no forms found in survey."
                )

        for type in self.n_forms.keys():
            if type == "local_aut":
                continue
            for subtype in self.n_forms[type].keys():
                if subtype == "revenues" or subtype is None:
                    continue
                for id in self.n_forms[type][subtype]:
                    self.numerosity[id] = temp[subtype]
