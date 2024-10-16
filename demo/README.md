Here a series of scripts used to test the code:

- preprocessing_demo execute a preprocess of a given survey. It can preprocess a single form, a series of form, all form of a single type or an entire survey
- ramp_simulation_demo preprocess a given survey and then perform a ramp simulation. The data from the simulation are saved in a directory that if not specified is called output. 

In order to process a survey two environment variables has to be set: SURVEY_KEY and KOBO_TOKEN

To test the code, once the two environment variables are set type in a terminal in the main directory:

```bash

python preprocessing_demo.py -i ID_NUMBER_1 ID_NUMBER_2

```

where ID_NUMBER are form id that can be found on kobo. This will preprocess the forms.
For the moment the code just print out the final dictionary. 

Type:
```bash

python preprocessing_demo.py -h

```

for more option

If a ramp simulation is needed type instead:
```bash

python ramp_simulation_demo.py -i ID_NUMBER_1 ID_NUMBER_2

```

This will create a series of csv files in the directory called output/SURVEY_KEY.

There will be a csv file for each demand (water, agro, cookign, elec). The csv files will contains a series of column one for each forms. The simulation output both max and mean hourly values in different csv files except for water demand which is just the sum of liters in an hour.

The code creates also tww csv file with the aggregated demand of all the forms, both max and mean hourly demand.
