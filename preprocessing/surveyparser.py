import os
import json
import warnings

from copy import copy

from preprocessing.formparser import FormParser
from preprocessing.utils import load_kobo_data
from preprocessing import constants

class SurveyParser:
    def __init__(self, survey_key=None, token=None) -> None:
        self.formparser = FormParser()
        self.survey_key = survey_key
        self.survey = None
        self.token = token
        self.n_forms = {constants.formtype_names[i]: 0 for i in range(len(constants.formtype_names))}
        self.id_forms = {constants.formtype_names[i]: [] for i in range(len(constants.formtype_names))}
        self.forms = {}
        self.local_aut = None
        self.morethanone = False
        if self.survey_key is None or self.token is None:
            try:
                self.init_parser()
            except:
                raise ValueError("Survey key and kobo api token not given and not found in system environment")
            
    def init_parser(self) -> None:
        self.survey_key, self.token = os.getenv('SURVEY_KEY'), os.getenv('KOBO_TOKEN')

    def read_survey(self) -> None:
        self.survey, _  = load_kobo_data(self.survey_key, self.token)
        for form in self.survey:
            self.formparser.init_parser(form)
            type = self.formparser.formtype
            self.n_forms[type] = self.n_forms[type] + 1
            self.id_forms[type].append(form['_id'])
            self.forms[form['_id']] = form
            if type == "local_aut":
                if not self.morethanone:
                    self.local_aut = form
                    self.morethanone = True
                else:
                    print("WARNING: More than one Local Authority form found. Will use the first one: " + self.local_aut['_id'] + ".")

    def process_survey(self, form_type=None, form_id=None) -> None:
        if self.local_aut is not None:
            self.formparser.init_parser(self.local_aut)
            #self.summary = self.formparser.create_dictionary()
        else:
            warnings.warn("WARNING: No Local Authority form defined. Numerisity set to 1 for all forms.")

        self._match_localaut_info_to_survey()

        output = {}
        if self.survey is not None:
            if form_id is not None:
                for id in form_id:
                    try:
                        self.formparser.init_parser(self.forms[id])
                        output[id] = copy(self.formparser.create_dictionary())
                        print(f"Processed form {id}.")
                    except:
                        print(f"WARNING: Could not process form {id}"
                              " Skipping this form.")
                        continue
            elif form_type is not None:
                for id in self.id_forms[form_type]:
                    try:    
                        self.formparser.init_parser(self.forms[id])
                        output[id] = self.formparser.create_dictionary()
                        print(f"Processed form {id}.")
                    except:
                        print(f"WARNING: Could not process form {id}"
                              " Skipping this form.")
                        continue
            elif form_type is None and form_id is None:
                for form in self.survey:
                    try:    
                        self.formparser.init_parser(form)
                        output[form['_id']] = self.formparser.create_dictionary()
                    except:
                        print(f"WARNING: Could not process form {form['_id']}"
                              " Skipping this form.")
                        continue
        else:
            raise BaseException("WARNING: No survey data defined.")
        
        return output

    def _match_localaut_info_to_survey(self) -> None:
        pass