# WEFEDemand


### Scientifc Abstract

Mini grids are expected to play a critical role in providing energy security in isolated communities. Enabling the productive use of energy in the water and food sector can improve local water and food security. Examples of such energy-driven productive uses are water pumping, water treatment, irrigation, cooling, agricultural machinery, milling, and other local enterprises. Despite their potential, the integrated planning and implementation of mini grids for sustainable water-energy-food supply lags behind. Integrated planning across resource sectors requires accessible holistic methods and tools for the assessment of water, energy, and food related demands.

We present an open software approach for the assessment of water-energy-food related demands in isolated communities. The software generates demand profiles, which serve as a basis for the planning and multi-objective-optimization of the supply-side of integrated water-energy-food systems.

We employ digital household and business surveys using KoboToolbox. The collected data is automatically processed and validated with stakeholder and expert input. We developed a stochastic model based on the RAMP framework, which generates high-resolution demand profiles. These include electric load profiles of households and businesses as well as profiles of drinking and service water demand for irrigation or livestock. Furthermore, food related energy demand profiles for cooking and agro-processing are modeled. The stochastic demand model generates annual demand profiles considering seasonal and weekly variations. It allows for the analysis of demand profiles of individual types of households, businesses and appliances which facilitates the forecasting of demand development. The developed open-access software enables communities to efficiently assess water-energy-food related demands and reliably model the corresponding demand profiles, which is vital to plan mini grids that enable productive uses for improved water, energy, and food securit

## Functioning

The WEFESiteAnalyst includes the collection of socio-economic data and WEF demand assessment. Therefore, find a Survey xls-file. You can deploy the xls-file in kobotoolbox and fill it (in case you are analyzing a location you are working or living) or send it to people living or working at the location to be analyzed. The results are made available as table. For deployment of the xls-file in kobotoolbox, please see their [documentation](https://support.kobotoolbox.org/). 
The WEF demand assessment tool (WEFEDemand) is implemented by adding the water and food dimension to the exisitng energy demand asssessment tool [RAMP](https://github.com/RAMP-project/RAMP). Inputs to the WEF DAT are the survey results. Outputs of the WEF DAT are hourly demand time series related to the water, energy, and food dimensions.
## Get started


## Code linting

1. Create a virtual environment and install the dev dependencies with, for example

        pip install -r requirements/dev.txt

You can also create a virtual environment with conda and the `environment.yml` file

2. Install the pre-commit hooks with

        pre-commit install

   This will mainly make sure you can't commit if your code is not linted with black.
   The pre-commit hook will check if your code is linted and if it is not it will simply lint it for you, you then only need to stage the changes made by the linter and commit again, as simple as that :)
