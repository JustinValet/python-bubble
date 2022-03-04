import requests
import json
import urllib
import pandas as pd
from bubble.utils.read_transformer import (
    check_base_params,
    create_base_url_api,
    add_constraints_to_base_parameter,
)
from bubble.utils.functions_utils import compute_time, bulk_insert_base, chunck_data_frame
import copy
from typing import Dict, List


class Api(object):
    def __init__(self, parameter: Dict, website: str, env: str):

        self._base_parameter = check_base_params(parameter)
        self._env = env
        self._website = website

    @compute_time
    def get(self, bubble_object, constraints_parameter: List[Dict] = None) -> List:

        _base_url_api = create_base_url_api(self._website, self._env, is_api_workflow=False, dev_version=None)

        cursor = 0
        remaining = 100
        concatenate_res = list()

        if constraints_parameter:
            url_parameter = add_constraints_to_base_parameter(
                copy.copy(self._base_parameter), constraints_parameter
            )
        else:
            url_parameter = copy.copy(self._base_parameter)

        session = requests.Session()

        while remaining > 0:

            url_parameter["cursor"] = cursor

            url = _base_url_api + bubble_object + "?" + urllib.parse.urlencode(url_parameter)
            response = session.get(url)

            concatenate_res.append(response.json()["response"]["results"])
            remaining = response.json()["response"]["remaining"]
            count = response.json()["response"]["count"]

            cursor += count

        session.close()

        return concatenate_res

    @compute_time
    def bulk_insert(self, data: pd.DataFrame, bubble_object: str):

        chunk_df = chunck_data_frame(data)

        _base_url_api = create_base_url_api(self.website, self.env, is_api_workflow=False, dev_version=None)

        for c_df in chunk_df:
            bulk_insert_base(c_df, bubble_object, _base_url_api, self._base_parameter)

    @compute_time
    def delete(self, id_to_delete: List[str], bubble_object: str):

        missing_delete = []
        session = requests.Session()

        _base_url_api = create_base_url_api(self.website, self.env, is_api_workflow=False)

        for id_to_del in id_to_delete:

            try:
                url_base = (
                    _base_url_api
                    + bubble_object
                    + "/"
                    + id_to_del
                    + "?"
                    + urllib.parse.urlencode(self._base_parameter)
                )

                session.delete(url_base)
            except KeyError:
                missing_delete.append(id_to_del)
                pass

        session.close()

        if (len(id_to_delete) - len(missing_delete)) == len(id_to_delete):
            print("Deletion task was well completed")
        else:
            print("Some data were not deleted (number of rows = {})".format(len(missing_delete)))

        return missing_delete

    @compute_time
    def get_by_unique_id(self, id_to_fetch, bubble_object):

        session = requests.Session()

        missing_get = []
        res_concat = []

        for id_to_fec in id_to_fetch:

            try:
                url_base = (
                    self._base_url_api
                    + bubble_object
                    + "/"
                    + id_to_fec
                    + "?"
                    + urllib.parse.urlencode(self._base_params)
                )

                response = session.get(url_base)
                res_concat.append(response.json()["response"])

            except KeyError:
                missing_get.append(id_to_fetch)
                pass

        session.close()

        return res_concat, missing_get

    def post_api_workflow(self, bubble_object: str, data: dict()):

        url_base = create_base_url_api(
            self._website, self._env, dev_version=self._env_version, is_api_workflow=True
        )

        url = url_base + bubble_object + "/" "?" + urllib.parse.urlencode(data)

        session = requests.Session()
        headers = {"Content-Type": "text/plain", "api_token": self._base_params["api_token"]}

        res = session.post(url, headers=headers)

        session.close()

        return res.status_code

    @compute_time
    def modify(self, bubble_object, id_to_modify, values_to_modify, **kwargs):

        is_replace = kwargs.get("is_replace", False)

        url_base = self._base_url_api + bubble_object + "/" + id_to_modify

        headers = {"Content-Type": "application/json", "api_token": self._base_params["api_token"]}

        session = requests.Session()

        try:
            if is_replace:
                res = session.patch(url_base, headers=headers, data=json.dumps(values_to_modify))
            else:
                res = session.put(url_base, headers=headers, data=json.dumps(values_to_modify))
        except KeyError:
            pass

        session.close()

        return res.status_code

    def get_convert_to_dataframe(self, json_list):

        concat_df = None

        for i in range(0, len(json_list)):

            concat_df = pd.concat([concat_df, pd.json_normalize(json_list[i])], axis=0)

        return concat_df
