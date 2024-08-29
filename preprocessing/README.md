Preprocessing code for extracting info from forms of a survey. 
The code is based on two main classes:
    - FormParser
    - SurveyParser

The first handle a single form creating a dictionary with the useful data from that form. A collection of this dictionaries is then used to create a simulation with ramp.

The second class handle an entire survey counting how many form there are of a single type, colleting ID of the forms and processing forms using FormParser. A survey can be processed entirely or it can be specified if only one form or a single type of form has to be processed (see READM in demo directory).

Constants file contains usefull variables to compute conversion and also prefix and suffix in order to read the online forms.

Utils file contain usefull functions for the rest of the code.