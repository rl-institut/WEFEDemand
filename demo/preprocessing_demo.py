import os
import sys

import argparse
import pandas as pd

from input.admin_input import admin_input
from preprocessing.surveyparser import SurveyParser
from preprocessing.surveyparser import SurveyParser
from ramp_model.ramp_control import RampControl


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
    nargs='+',
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

    surveyparser = SurveyParser(surv_id, token)
    surveyparser.read_survey()
    preprocessed_survey = surveyparser.process_survey(form_id=args.id, form_type=args.formtype)

    return preprocessed_survey


if __name__ == "__main__":
    #run_simulation_on_survey()
    SURVEY_KEY, KOBO_TOKEN = get_key_and_token()
    output = preprocess_survey(SURVEY_KEY, KOBO_TOKEN)
    print(output)