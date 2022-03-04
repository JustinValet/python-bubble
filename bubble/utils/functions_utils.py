import pandas as pd
import re
import time
import requests
import simplejson
from typing import List


def convert_df_to_plain_text(data):

    j_ = str(simplejson.dumps(data.to_dict(orient="records"), ignore_nan=True))
    j_ = re.sub("^\[", "", j_)
    j_ = re.sub("\]$", "", j_)
    j_ = j_.replace("}, ", "}\n")

    return j_


def compute_time(method):
    def timed(*args, **kw):

        tic = time.time()
        result = method(*args, **kw)
        print("the script ran in {} seconds".format(time.time() - tic))

        return result

    return timed


def chunck_data_frame(df: pd.DataFrame) -> List[pd.DataFrame]:

    chunk_size = 500

    list_df = list()
    num_chunks = len(df) // chunk_size + 1
    for i in range(num_chunks):
        if not df[i * chunk_size : (i + 1) * chunk_size].empty:
            list_df.append(df[i * chunk_size : (i + 1) * chunk_size])
    return list_df


def bulk_insert_base(data, bubble_object, base_url_api, base_params):

    session = requests.Session()

    j_ = convert_df_to_plain_text(data)

    url_base = base_url_api + bubble_object + "/bulk"

    headers = {"Content-Type": "text/plain", "api_token": base_params["api_token"]}
    session.post(url_base, headers=headers, data=j_)

    session.close()
