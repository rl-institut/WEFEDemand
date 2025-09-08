import os
import sys

import argparse
import pandas as pd

from wefe_demand.input.admin_input import admin_input
from wefe_demand.preprocessing.surveyparser import SurveyParser
from wefe_demand.ramp_model.ramp_control import RampControl


env_SURVEY_KEY = "SURVEY_KEY"
env_KOBO_TOKEN = "KOBO_TOKEN"

parser = argparse.ArgumentParser(description="Preprocessing demo")
parser.add_argument(
    "--days",
    type=int,
    default=365,
    help="Number of days for the time window of the simulation",
)
parser.add_argument(
    "--date",
    type=str,
    default="2018-01-01",
    help="Starting date of the time window of the simulation",
)

parser.add_argument(
    "-i",
    "--id",
    type=int,
    nargs="+",
    default=None,
    help="Id of the form to be processed. If not provided, all forms will be processed.",
)

parser.add_argument(
    "-f",
    "--formtype",
    type=str,
    default=None,
    help="Type of the form to be processed. If not provided, all forms will be processed. Only \
        'service', 'business', large_scale_farm' and 'household' types are supported.",
)

parser.add_argument(
    "-v",
    "--verbose",
    action="store_true",
    help="Activate verbose mode",
)

parser.add_argument(
    "-po",
    "--printoutput",
    action="store_true",
    help="Print the full output",
)

parser.add_argument(
    "-pi",
    "--printsingleform",
    type=int,
    nargs="+",
    default=None,
    help="Print the output of one or multiple forms given the form ids",
)

parser.add_argument(
    "-pid", "--printids", action="store_true", help="Print ids preprocessed"
)

args = parser.parse_args()


def get_key_and_token():
    """
    Get the API key and token from the environment variables

    These environment variables are expected to be set:
        SURVEY_KEY: The API key for the Kobo data
        KOBO_TOKEN: The API token for the Kobo data

    If either of these variables are not set, the program will exit with an error message

    Returns:
        tuple: A tuple containing the API key and token
    """
    if os.getenv(env_SURVEY_KEY) is None or os.getenv(env_KOBO_TOKEN) is None:
        print(
            f"Error: One or both of the following environment variables are not set: {env_SURVEY_KEY}, {env_KOBO_TOKEN}"
        )
        sys.exit(1)
    return os.getenv(env_SURVEY_KEY), os.getenv(env_KOBO_TOKEN)


def preprocess_survey(surv_id, token):
    """
    Preprocess survey data for the RAMP model

    Args:
        surv_id (str): The API key for the Kobo data
        token (str): The API token for the Kobo data

    Returns:
        dict: A dictionary containing the survey data
    """

    preprocessed_survey = None
    surveyparser = SurveyParser(surv_id, token, verbose=args.verbose)
    surveyparser.read_survey()
    preprocessed_survey = surveyparser.process_survey(
        form_id=args.id, form_type=args.formtype
    )

    return preprocessed_survey, surveyparser


if __name__ == "__main__":
    # run_simulation_on_survey()
    SURVEY_KEY, KOBO_TOKEN = get_key_and_token()
    output, parser = preprocess_survey(SURVEY_KEY, KOBO_TOKEN)
    if args.printoutput:
        print(output)
    if args.printids:
        print("FORM IDs: \n", list(output.keys()))
    if args.printsingleform:
        for form_id in args.printsingleform:
            print(f"output for form {form_id}:\n", output[form_id])
