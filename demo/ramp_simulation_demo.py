import os
import sys

import argparse
import pandas as pd

from wefe_demand.input.admin_input import admin_input
from wefe_demand.preprocessing.surveyparser import SurveyParser
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
    "-o",
    "--output",
    type=str,
    default="output",
    help="Starting date of the time window of the simulation",
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
    "-pid", "--printids", action="store_true", help="Print ids preprocessed"
)

parser.add_argument(
    "-pi",
    "--printsingleform",
    type=int,
    nargs="+",
    default=None,
    help="Print the output of one or multiple forms given the form ids",
)

args = parser.parse_args()


def create_directory_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


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


def dump_simulation_output(dat_output, survey, type="mean"):
    """
    Dump the demand profiles from the simulation output for each demand type to separate CSV files

    Args:
        dat_output (pandas.DataFrame): DataFrame containing the output of the simulation.
        type (str, optional): Type of the output data. Defaults to "mean".
    """
    # Loop over each demand type (e.g. cooking, drinking water, etc.)
    for demand, df in dat_output.groupby(level=0, axis=1):
        # Create the filename for the output file
        csv_file_path = f"{args.output}/{survey}/demand_{demand}_{type}.csv"
        # Save the demand profile to a CSV file
        df.to_csv(csv_file_path, index=True, float_format="%.18f", decimal=",")
        # Print a message to the user indicating that the file has been written
        print(f"Dumped {type} demand in CSV file {csv_file_path} for {demand} demand")


def dump_aggregated_output(dat_output, survey, type="mean"):
    """
    Dump aggregated demand (summed over all households) for each demand type to a CSV file

    Args:
        dat_output (pandas.DataFrame): DataFrame containing the output of the simulation.
        type (str, optional): Type of the output data. Defaults to "mean".
    """
    # Sum the demands over all households
    dat_output = dat_output.groupby(level=0, axis=1).sum()

    # Create the filename for the output file
    csv_file_path = f"{args.output}/{survey}/aggregated_demands_{type}.csv"

    # Save the aggregated demand to a CSV file
    dat_output.to_csv(csv_file_path, index=True, float_format="%.18f", decimal=",")


def preprocess_survey(surv_id, token):
    """
    Preprocess survey data for the RAMP model

    Args:
        surv_id (str): The API key for the Kobo data
        token (str): The API token for the Kobo data

    Returns:
        dict: A dictionary containing the survey data
    """

    surveyparser = SurveyParser(surv_id, token, verbose=args.verbose)
    surveyparser.read_survey()
    preprocessed_survey = surveyparser.process_survey(
        form_id=args.id, form_type=args.formtype
    )

    return preprocessed_survey


def run_simulation_on_survey(data):
    """
    Run the simulation of the demand using the RAMP model and dump the output to CSV files

    This function is the main entry point for the demo script
    """

    # %% Create instance of RampControl class, define timeframe to model load profiles
    days, start = args.days, args.date
    ramp_control = RampControl(days, start)

    # %% Run simulation of the demand
    dat_output_mean, dat_output_max = ramp_control.run_opti_mg_dat(data, admin_input)

    print(dat_output_mean)
    # %% Dump raw output on CSV
    create_directory_if_not_exists(args.output)
    create_directory_if_not_exists(f"{args.output}/{SURVEY_KEY}")
    dump_simulation_output(dat_output_mean, survey=SURVEY_KEY, type="mean")
    dump_simulation_output(dat_output_max, survey=SURVEY_KEY, type="max")
    dump_aggregated_output(dat_output_mean, survey=SURVEY_KEY, type="mean")
    dump_aggregated_output(dat_output_max, survey=SURVEY_KEY, type="max")


if __name__ == "__main__":
    # run_simulation_on_survey()
    SURVEY_KEY, KOBO_TOKEN = get_key_and_token()
    preprocessed_survey = preprocess_survey(SURVEY_KEY, KOBO_TOKEN)

    if args.printoutput:
        print(preprocessed_survey)
    if args.printids:
        print("FORM IDs: \n", list(preprocessed_survey.keys()))
    if args.printsingleform:
        for form_id in args.printsingleform:
            print(f"output for form {form_id}:\n", preprocessed_survey[form_id])

    if len(list(preprocessed_survey.keys())):
        run_simulation_on_survey(preprocessed_survey)
    else:
        print("None of the forms could have been preprocessed")
