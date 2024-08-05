import sys
import json
from copy import copy

from preprocessing.formparser import FormParser
from preprocessing.utils import load_kobo_data


def process_survey(
    *,
    DUMP: bool = False,
    surv_id: str = "atiMZ5E4jaZHv37TUekb6N",
    token: str = "ea290627972a055fd067e1efc02c803869b1747c",
) -> dict:
    """
    Read a survey, process every form in the survey one by one and produce a dictionary where every key
    corresponds to an output dictionary of the processed forms. If DUMP is set to TRUE the function
    produces a json file for every form and a json file for all the forms stacked together containing
    the corresponding dictionaries.

    Args:
        DUMP (bool, optional): Flag to indicate if intermediate results should be dumped to json files.
        Defaults to False.
        surv_id (str, optional): ID of the survey to process. Defaults to "atiMZ5E4jaZHv37TUekb6N".
        token (str, optional): API token for accessing the Kobo Toolbox API. Defaults to "ea290627972a055fd067e1efc02c803869b1747c".

    Returns:
        Dict[str, Dict[str, Any]]: Dictionary containing the output dictionaries of the processed forms.
    """

    # Load the survey forms using the Kobo Toolbox API
    forms, _ = load_kobo_data(form_id=surv_id, api_token=token)

    # Initialize the form parser
    parser = FormParser()

    # Dictionary to store the output dictionaries of the processed forms
    output_dict: Dict[str, Dict[str, Any]] = {}

    # Counters for the number of forms processed
    h_count, b_count, s_count, a_count, l_count = 0, 0, 0, 0, 0

    # Process each form in the survey
    for form in forms:
        # Initialize the form parser with the current form
        parser.init_parser(form)

        # Determine the form type and assign a unique name to the form
        if parser.formtype == "household":
            h_count += 1
            form_name = f"{parser.formtype}_{h_count}"
        elif parser.formtype == "business":
            b_count += 1
            form_name = f"{parser.formtype}_{b_count}"
        elif parser.formtype == "service":
            s_count += 1
            form_name = f"{parser.formtype}_{s_count}"
        elif parser.formtype == "local_aut":
            l_count += 1
            form_name = f"{parser.formtype}_{l_count}"
        elif parser.formtype == "large_scale_farm":
            a_count += 1
            form_name = f"{parser.formtype}_{a_count}"

        parser.create_dictionary()

        # Dump the output dictionary to a json file if DUMP is True
        if DUMP:
            with open(f"preprocessing/test/{form_name}.json", "w") as file:
                json.dump(parser.output_dict, file)

        # Add the output dictionary to the main dictionary
        output_dict[form_name] = copy(parser.output_dict)

    # Dump the output dictionary to a json file if DUMP is True
    if DUMP:
        with open(f"preprocessing/test/test.json", "w") as file:
            json.dump(output_dict, file)

    # Return the main dictionary containing the output dictionaries of the processed forms
    return output_dict


if __name__ == "__main__":

    o = process_survey()
    print(o.keys())
