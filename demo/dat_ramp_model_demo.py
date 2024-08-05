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


# Create instance of RampControl class, define timeframe to model load profiles
ramp_control = RampControl(365, "2018-01-01")

# dat_output = ramp_control.run_opti_mg_dat(input_dict, admin_input)
input_dic = process_survey(
    surv_id="affG8Fq5Suc99Sg9UB5hPv", token="2dbeed5e3b9033be53be7d16f7d7da7c9a25d1ad"
)
# 2dbeed5e3b9033be53be7d16f7d7da7c9a25d1ad
# ea290627972a055fd067e1efc02c803869b1747c

# affG8Fq5Suc99Sg9UB5hPv

dat_output = ramp_control.run_opti_mg_dat(input_dic, admin_input)
# %% Plot raw output


i = 1  # Plotly subplot rows start at index 1
figures = []
for demand, df in dat_output.groupby(level=0, axis=1):
    fig = make_subplots(rows=1, cols=1, shared_xaxes=True)
    fig = plotting.plotly_high_res_df(fig, df=df, subplot_row=1)
    csv_file_path = f"demo/demand_{demand}.csv"
    df.to_csv(csv_file_path, index=True, float_format="%.18f", decimal=",")
    i = i + 1
    print(demand)
    figures.append(
        html.Div(
            [
                html.H3(demand),
                dcc.Graph(figure=fig),
            ]
        )
    )

fig.update_layout(autosize=True)

# fig.show_dash(mode='external')

# %% Plot aggregated demands

agg_demand = dat_output.groupby(level=0, axis=1).sum()
print(agg_demand.head(30))
for col in agg_demand.columns:
    print(f"{col} max: ", agg_demand[col].max())
    print(f"{col} min: ", agg_demand[col].min())

print(agg_demand.info())
csv_file_path = "demo/aggregated_demands.csv"
# Write the DataFrame to the CSV file
agg_demand.to_csv(csv_file_path, index=True, float_format="%.18f", decimal=",")

fig = make_subplots(rows=1, cols=1, shared_xaxes=True)
fig = plotting.plotly_high_res_df(fig, df=agg_demand, subplot_row=1)
# fig.show_dash(mode='external')
figures.append(
    html.Div(
        [
            html.H3("aggregated demands"),
            dcc.Graph(figure=fig),
        ]
    )
)

if __name__ == "__main__":
    demo_app = dash.Dash(__name__)
    demo_app.layout = html.Div(children=figures)
    demo_app.run_server(debug=False)
