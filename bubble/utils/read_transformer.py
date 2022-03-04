import json
from typing import Dict, List


def check_base_params(dict_params):

    try:
        assert isinstance(dict_params, dict)
        assert isinstance(dict_params["api_token"], str)
    except ValueError:
        print("The dictionnary is not well step-up")

    return dict_params


def add_constraints_to_base_parameter(dict_params: Dict, constraints: List[Dict]) -> Dict:

    if not isinstance(constraints, list):
        raise AssertionError("The constraints are not in a list format")

    for i in range(0, len(constraints)):
        if not isinstance(constraints[i], dict):
            raise AssertionError(
                "The {}th constrainst is not well formated. A dictionnary is expected".format(i)
            )

    dict_params_transform = {}
    dict_params_transform["api_token"] = dict_params["api_token"]

    try:
        dict_params_transform["constraints"] = json.dumps(constraints)

    except ValueError:
        print("The constraints are not in a list format")

    return dict_params_transform


def create_base_url_api(website, api_env, **kwargs):

    dev_version = kwargs.get("dev_version", "version-test")
    _is_api_workflow = kwargs.get("is_api_workflow", False)

    if _is_api_workflow:
        main_arg = "wf"
    else:
        main_arg = "obj"

    if dev_version is None:
        dev_version = "version-test"

    if api_env == "live":
        url = "https://{}/api/1.1/{}/".format(website, main_arg)
    else:
        url = "https://{}/{}/api/1.1/{}/".format(website, dev_version, main_arg)
    return url
