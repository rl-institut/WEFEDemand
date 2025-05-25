# WEFEDemand

WEFEDemand is an assessment tool designed to model and analyze the interconnected demands of integrated Water-Energy-Food-Environment Systems(iWEFEs), particularly in off-grid and decentralized contexts. This tool facilitates a comprehensive 
understanding of how these essential systems interact and affect each other with a particular focus on developing 
sustainable, resilient, and efficient systems. By simulating the demand dynamics of water, energy, food, and environmental
resources, the tool enables stakeholders, including researchers, policymakers, and local authorities, to make informed 
decisions about resource allocation, infrastructure investments, and policy development. WEFEDemand allows users to configure
and run multiple scenarios, customize components, and model demand profiles for various case studies. It adapts to different 
contexts, geographic or socio-economic, using real-time data to assess and forecast resource demands, supporting effective 
system management, planning, and optimization of integrated WEFE systems.

## Prerequisites

Make sure a supported Python Version (3.9 or greater), pip and an interpreter (preferably PyCharm) is installed on your 
system. Additionally, it is recommended to create a free account at [KoboToolbox](https://www.kobotoolbox.org/sign-up/) 
if you plan to use the tool’s data collection features.

## Installation

For using the WEFEDemand, clone the repository to your local machine. Then navigate to the repository folder and 
create a new virtual environment with a supported Python Version (3.9 or greater). Activate the new virtual environment 
and install the necessary python packages using pip and the requirements file:

      pip install -r requirements/dev.txt

Add the directory to the pythonpath (look guide for adding a directory to the python-path environment variable on 
Windows), for linux type in the terminal:

      export PYTHONPATH=$PYTHONPATH:$PWD

This last step has to be done everytime a new terminal is started.

Once all of these steps have been completed successfully, you are ready to run the example!

Enter into the demo directory and run the demo model:

      cd ~/WEFEDemand/demo
      python dat_ramp_model_demo.py

## Troubleshooting



## Get started

Simply click on the green `Use this template` button on the left of the `Clone or download` button.

The detailed instructions to create a new repository from this template can be found [here](https://help.github.com/en/articles/creating-a-repository-from-a-template).

## Code linting

1. Create a virtual environment and install the dev dependencies with, for example

        pip install -r requirements/dev.txt

You can also create a virtual environment with conda and the `environment.yml` file

2. Install the pre-commit hooks with

        pre-commit install

   This will mainly make sure you can't commit if your code is not linted with black.
   The pre-commit hook will check if your code is linted and if it is not it will simply lint it for you, you then only need to stage the changes made by the linter and commit again, as simple as that :)
