import json
import os
from collections import OrderedDict

import boto3
import unidecode

from functions.extractor import date_extractor

comprehend = boto3.client(service_name='comprehend', region_name=<MY_REGION_NAME>,
        aws_access_key_id=<MY_AWS_ACCESS_KEY_ID>,
        aws_secret_access_key=<MY_AWS_SECRET_ACCESS_KEY>)

def get_aws_ground_truth(filename, entity="DATE"):
    aws_name = os.path.splitext(filename)[0] + '_AWS_out.json'
    with open(aws_name) as f:
        output_dump = json.load(f)

    all_dates = []
    count = 0
    f = "%B %d, %Y"
    for x in output_dump:
        for i in range(0, len(output_dump[x]["Entities"])):
            if output_dump[x]["Entities"][i]["Type"] == entity:
                dates_extracted = unidecode.unidecode(output_dump[x]["Entities"][i]["Text"])
                list_of_wordContexts = "".join(str(x) for x in dates_extracted)
                if len(list_of_wordContexts) > 5:
                    new_dates = date_extractor.dates_for_format(list_of_wordContexts)
                    all_dates.append(new_dates)

    return list(OrderedDict.fromkeys(all_dates))
    # return all_dates
