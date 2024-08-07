# WEFEDemand


### Socio-economic data collection and WEF demand assessment
The WEFESiteAnalyst includes the collection of socio-economic data and WEF demand assessment. Therefore, find a Survey xls-file. You can deploy the xls-file in kobotoolbox and fill it (in case you are analyzing a location you are working or living) or send it to people living or working at the location to be analyzed. The results are made available as table. For deployment of the xls-file in kobotoolbox, please see their [documentation](https://support.kobotoolbox.org/). 
The WEF demand assessment tool (WEF DAT) is implemented by adding the water and food dimension to the exisitng energy demand asssessment tool [RAMP](https://github.com/RAMP-project/RAMP). Inputs to the WEF DAT are the survey results. Outputs of the WEF DAT are hourly demand time series related to the water, energy, and food dimensions.
## Get started


## Code linting

1. Create a virtual environment and install the dev dependencies with, for example

        pip install -r requirements/dev.txt

You can also create a virtual environment with conda and the `environment.yml` file

2. Install the pre-commit hooks with

        pre-commit install

   This will mainly make sure you can't commit if your code is not linted with black.
   The pre-commit hook will check if your code is linted and if it is not it will simply lint it for you, you then only need to stage the changes made by the linter and commit again, as simple as that :)
