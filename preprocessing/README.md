Preprocessing code for extracting info from forms of a Kobo survey. 
The code is based on two main classes:
    - FormParser
    - SurveyParser

The first handle a single form creating a dictionary with the useful data from that form. A collection of this dictionaries is then used to create a simulation with ramp.

The second class handle an entire survey counting how many form there are of a single type, colleting ID of the forms and processing forms using FormParser. A survey can be processed entirely or it can be specified if only one form or a single type of form has to be processed (see README in demo directory).

`constants.py` module contains useful variables to perform conversion and also prefix and suffix in order to read the online forms.

`utils.py` module contains functions shared across several modules.