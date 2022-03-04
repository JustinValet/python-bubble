import requests
import urllib
import pandas as pd
from bubble.utils.read_transformer import create_base_url_api, check_base_params, add_constraints

class BubbleApi(object):

    def __init__(self, params, website, env, **kwargs):

        
        self._env_version = kwargs.get('env_version', None)
        self._base_params = check_base_params(params)
        self._env = env
        self._website = website
        self._base_url_api = create_base_url_api(website, 
                                                 env, 
                                                 dev_version=self._env_version)

    def get(self, bubble_object, **kwargs):
        
        constraints_params = kwargs.get("constraints_params", None)
    
        cursor = 0
        remaining = 100
        concatenate_res = list()
        read_params = self._base_params
        
        if constraints_params is not None:
            read_params = add_constraints(read_params, constraints_params)
        
        session = requests.Session()
                       
        while remaining > 0:

            read_params["cursor"] = cursor

            url = self._base_url_api + bubble_object + \
                '?' + urllib.parse.urlencode(read_params)
            response = session.get(url)
            
            concatenate_res.append(response.json()['response']["results"])
            remaining = response.json()['response']['remaining']
            count = response.json()['response']['count']

            cursor += count

        session.close()

        return concatenate_res

    def get_convert_to_dataframe(self, json_list):

        concat_df = None

        for i in range(0, len(json_list)):

            concat_df = pd.concat([
                concat_df,
                pd.json_normalize(json_list[i])
            ], axis=0)

        return concat_df

