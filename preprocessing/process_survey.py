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
) -> Dict[str, Dict[str, Any]]:
    """
    Read a survey, process every form in the survey one by one
    and produce a dictionary where every key corresponds
    to an output dictionary of the processed forms.
    If DUMP is set to TRUE the function produces a json file for every form
    and a json file for all the forms stacked together containing the corresponding
    dictionaries.
    """
    forms, _ = load_kobo_data(form_id=surv_id, api_token=token)
    parser = FormParser()

    output_dict: Dict[str, Dict[str, Any]] = {}
    form_name: Optional[str] = None
    h_count, b_count, s_count, a_count = 0, 0, 0, 0

    for form in forms:
        parser.init_parser(form)
        if parser.formtype == "household":
            h_count += 1
            form_name = f"{parser.formtype}_{h_count}"
        elif parser.formtype == "business":
            b_count += 1
            form_name = f"{parser.formtype}_{b_count}"
        elif parser.formtype == "service":
            s_count += 1
            form_name = f"{parser.formtype}_{s_count}"
        elif parser.formtype == "large_scale_farm":
            a_count += 1
            form_name = f"{parser.formtype}_{a_count}"

        parser.create_dictionary()

        if DUMP:
            with open(f"preprocessing/test/{form_name}.json", "w") as file:
                json.dump(parser.output_dict, file)

        output_dict[form_name] = copy(parser.output_dict)

    if DUMP:
        with open(f"preprocessing/test/test.json", "w") as file:
            json.dump(output_dict, file)

    return output_dict


if __name__ == "__main__":

    o = process_survey()
    print(o.keys())
