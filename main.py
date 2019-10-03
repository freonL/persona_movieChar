from datetime import timezone
from ibm_watson import PersonalityInsightsV3, ApiException
from os.path import join, dirname, exists
from os import makedirs, remove
import json
import pandas as pd



def create_output(ls,index):
    data_dict = {
        "contentItems" : ls
    }
    if not exists("output/"):
        makedirs('output/')

    with open('temp.json', 'w') as json_file:
            json.dump(data_dict, json_file)

    try:
        with open(join(dirname(__file__), './temp.json')) as data_json:
            profile = personality_insights.profile(
                data_json.read(),
                'application/json',
                content_type='application/json',
                consumption_preferences=True,
                raw_scores=True
            ).get_result()
        print(json.dumps(profile, indent=2))

        with open('output/output_'+ str(index) +'.json', 'w') as json_file:
            json.dump(profile, json_file, indent=2)
    except ApiException as ex:

        pass
    remove("temp.json")

if __name__ == "__main__":

    personality_insights = PersonalityInsightsV3(
        version='2017-10-13',
        iam_apikey='gYf7-1OzOB8-hzPK6Wunde9aAV9DW5VYA93RaIGvNE1m',
        url='https://gateway-syd.watsonplatform.net/personality-insights/api'
    )
    filename = "Top1_movie_actor.csv"
    df = pd.read_csv(filename)
    # Drop rows with any empty cells
    df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)
    df = df.dropna()

    for index, row in df.iterrows():
        ls = []

        if row[3] is not None and row[3] != "":
            ls.append({
                "content": row[3],
                "contenttype": "text/plain",
                # "id": index,
                # "created": 1447638226000,
                "language": "en"
            })

        create_output(ls,index)


