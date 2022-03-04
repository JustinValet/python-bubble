import json
import pandas as pd
import logging


def check_base_params(dict_params):
    
    try:
        assert bool(dict_params) == True
        assert isinstance(dict_params, dict)
    except ValueError:
        print("The dictionnary is not well step-up")
        
    try: 
        assert isinstance(dict_params["api_token"], str)
    except ValueError:
        print("Any token API was provided")
        
    return dict_params
        

def add_constraints(dict_params, constraints):

    
    if not isinstance(constraints, list):
        raise AssertionError("The constraints are not in a list format")
        
    for i in range(0,len(constraints)):
        if not isinstance(constraints[i], dict):
            raise AssertionError("The {}th constrainst is not well formated. A dictionnary is expected".format(i))
    
    dict_params_transform = {}
    dict_params_transform["api_token"] = dict_params["api_token"]

    try:
        dict_params_transform["constraints"] = json.dumps(constraints)
        
    except ValueError:
            print("The constraints are not in a list format")
            
    return dict_params_transform

def create_base_url_api(website, api_env, **kwargs):
    
    dev_version = kwargs.get('dev_version', 'version-test')
    
    if dev_version is None:
        dev_version = 'version-test'

    if api_env == "live":
        url = "https://{}/api/1.1/obj/".format(website)
    else:
        url = "https://{}/{}/api/1.1/obj/".format(website, dev_version)
    return url
