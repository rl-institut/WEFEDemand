import os
import sys

import argparse
import pandas as pd
from ramp_model.ramp_control import RampControl

from helpers import plotting
from plotly.subplots import make_subplots

# from input.complete_input import input_dict
from input.admin_input import admin_input
from preprocessing.process_survey import process_survey
import dash
from dash import dcc
from dash import html


env_SURVEY_KEY = "SURVEY_KEY"
env_KOBO_TOKEN = "KOBO_TOKEN"
parser = argparse.ArgumentParser()
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
    "--output",
    type=str,
    default="output",
    help="Starting date of the time window of the simulation",
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


def run_simulation_on_survey():
    """
    Run the simulation of the demand using the RAMP model and dump the output to CSV files

    This function is the main entry point for the demo script
    """
    # %% Getting keys and token from environment for accessing kobo api
    SURVEY_KEY, KOBO_TOKEN = get_key_and_token()
    print(SURVEY_KEY, KOBO_TOKEN)
    # %% Create instance of RampControl class, define timeframe to model load profiles
    days, start = args.days, args.date
    ramp_control = RampControl(days, start)

    # %% Reading and preprocess survey
    input_dic = process_survey(surv_id=SURVEY_KEY, token=KOBO_TOKEN)

    # %% Run simulation of the demand
    dat_output_mean, dat_output_max = ramp_control.run_opti_mg_dat(
        input_dic, admin_input
    )

    # %% Dump raw output on CSV
    create_directory_if_not_exists(args.output)
    create_directory_if_not_exists(f"{args.output}/{SURVEY_KEY}")
    dump_simulation_output(dat_output_mean, survey=SURVEY_KEY, type="mean")
    dump_simulation_output(dat_output_max, survey=SURVEY_KEY, type="max")
    dump_aggregated_output(dat_output_mean, survey=SURVEY_KEY, type="mean")
    dump_aggregated_output(dat_output_max, survey=SURVEY_KEY, type="max")

    # %% Plot individual demands
    i = 1  # Plotly subplot rows start at index 1
    figures = []
    for demand, df in dat_output_mean.groupby(level=0, axis=1):
        fig = make_subplots(rows=1, cols=1, shared_xaxes=True)
        fig = plotting.plotly_high_res_df(fig, df=df, subplot_row=1)
        i = i + 1
        figures.append(
            html.Div(
                [
                    html.H3(demand),
                    dcc.Graph(figure=fig),
                ]
            )
        )

    fig.update_layout(autosize=True)

    figures.append(
        html.Div(
            [
                html.H3("aggregated demands"),
                dcc.Graph(figure=fig),
            ]
        )
    )

    # %% Plot aggregated demands
    agg_demand_mean = dat_output_mean.groupby(level=0, axis=1).sum()
    agg_demand_max = dat_output_max.groupby(level=0, axis=1).sum()

    fig = make_subplots(rows=1, cols=1, shared_xaxes=True)
    fig = plotting.plotly_high_res_df(fig, df=agg_demand_mean, subplot_row=1)

    fig = make_subplots(rows=1, cols=1, shared_xaxes=True)
    fig = plotting.plotly_high_res_df(fig, df=agg_demand_max, subplot_row=1)


if __name__ == "__main__":
    run_simulation_on_survey()
    demo_app = dash.Dash(__name__)
    demo_app.layout = html.Div(children=figures)
    demo_app.run_server(debug=False)
