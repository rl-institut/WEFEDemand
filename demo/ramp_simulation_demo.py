import os
import sys

import argparse
import pandas as pd

from wefe_demand.input.admin_input import admin_input
from wefe_demand.preprocessing.surveyparser import SurveyParser
from wefe_demand.preprocessing.surveyparser import SurveyParser
from wefe_demand.ramp_model.ramp_control import RampControl
from dotenv import load_dotenv

load_dotenv()

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


def dump_simulation_output(dat_output, survey, dir, type="mean"):
    """
    Dump the demand profiles from the simulation output for each demand type to separate CSV files

    Args:
        dat_output (pandas.DataFrame): DataFrame containing the output of the simulation.
        type (str, optional): Type of the output data. Defaults to "mean".
    """
    # Loop over each demand type (e.g. cooking, drinking water, etc.)
    for demand, df in dat_output.groupby(level=0, axis=1):
        # Create the filename for the output file
        csv_file_path = f"{dir}/{survey}/demand_{demand}_{type}.csv"
        # Save the demand profile to a CSV file
        df.to_csv(csv_file_path, index=True)
        # Print a message to the user indicating that the file has been written
        print(f"Dumped {type} demand in CSV file {csv_file_path} for {demand} demand")


def dump_aggregated_output(dat_output, survey, dir, type="mean"):
    """
    Dump aggregated demand (summed over all households) for each demand type to a CSV file

    Args:
        dat_output (pandas.DataFrame): DataFrame containing the output of the simulation.
        type (str, optional): Type of the output data. Defaults to "mean".
    """
    # Sum the demands over all households
    dat_output = dat_output.groupby(level=0, axis=1).sum()

    # Create the filename for the output file
    csv_file_path = f"{dir}/{survey}/aggregated_demands_{type}.csv"

    # Save the aggregated demand to a CSV file
    dat_output.to_csv(csv_file_path, index=True)


def preprocess_survey(surv_id, token, args):
    """
    Preprocess survey data for the RAMP model

    Args:
        surv_id (str): The API key for the Kobo data
        token (str): The API token for the Kobo data

    Returns:
        dict: A dictionary containing the survey data
    """

    surveyparser = SurveyParser(surv_id, token, verbose=args.get("verbose"))
    surveyparser.read_survey()
    preprocessed_survey = surveyparser.process_survey(
        form_id=args.get("id"), form_type=args.get("formtype")
    )

    return preprocessed_survey


def run_simulation_on_survey(data, args):
    """
    Run the simulation of the demand using the RAMP model and dump the output to CSV files

    This function is the main entry point for the demo script
    """
    SURVEY_KEY = os.getenv("SURVEY_KEY")

    # %% Create instance of RampControl class, define timeframe to model load profiles
    days, start = args.get("days"), args.get("date")
    ramp_control = RampControl(days, start)

    # %% Run simulation of the demand
    dat_output_mean, dat_output_max = ramp_control.run_opti_mg_dat(data, admin_input)

    print(dat_output_mean)
    # %% Dump raw output on CSV
    dir = args.get("output")
    create_directory_if_not_exists(dir)
    create_directory_if_not_exists(f"{dir}/{SURVEY_KEY}")
    dump_simulation_output(dat_output_mean, survey=SURVEY_KEY, dir=dir, type="mean")
    dump_simulation_output(dat_output_max, survey=SURVEY_KEY, dir=dir, type="max")
    dump_aggregated_output(dat_output_mean, survey=SURVEY_KEY, dir=dir, type="mean")
    dump_aggregated_output(dat_output_max, survey=SURVEY_KEY, dir=dir, type="max")
    dat_output_mean_agg = dat_output_mean.groupby(level=0, axis=1).sum()
    return dat_output_mean_agg

def main(args):
    default_args = vars(parser.parse_args())
    KOBO_TOKEN = os.getenv(env_KOBO_TOKEN)
    SURVEY_KEY = os.getenv(env_SURVEY_KEY)
    for key in default_args.keys():
        if key not in args:
            args[key] = default_args[key]
    preprocessed_survey = preprocess_survey(SURVEY_KEY, KOBO_TOKEN, args)

    if args.get("printoutput"):
        print(preprocessed_survey)
    if args.get("printids"):
        print("FORM IDs: \n", list(preprocessed_survey.keys()))
    if args.get("printsingleform"):
        for form_id in args.get("printsingleform"):
            print(f"output for form {form_id}:\n", preprocessed_survey[form_id])


    if len(list(preprocessed_survey.keys())):
        sim_mean_agg = run_simulation_on_survey(preprocessed_survey, args)
        return sim_mean_agg
    else:
        print("None of the forms could be preprocessed")
        return None

if __name__ == "__main__":
    # run_simulation_on_survey()
    args = parser.parse_args()
    SURVEY_KEY, KOBO_TOKEN = get_key_and_token()

    main(vars(args))