from datetime import timezone
from ibm_watson import PersonalityInsightsV3, ApiException
from os.path import join, dirname, exists
from os import makedirs, remove
import json
import pandas as pd
import numpy as np

def get_persona(ls):
    data_dict = {
        "contentItems" : ls
    }
    result = None
    with open('temp.json', 'w') as json_file:
            json.dump(data_dict, json_file)

    try:
        with open(join(dirname(__file__), './temp.json')) as data_json:
            result = personality_insights.profile(
                data_json.read(),
                'application/json',
                content_type='application/json',
                consumption_preferences=True,
                raw_scores=True
            ).get_result()
        # print(json.dumps(profile, indent=2))

    except ApiException as ex:
        print(ex)
        pass
    remove("temp.json")
    return result

if __name__ == "__main__":

    personality_insights = PersonalityInsightsV3(
        version='2017-10-13', # lastest version : '2017-10-13'
        iam_apikey='', # change with API Key from IBM Peronsality Insight
        url=''  # change with URL from IBM Peronsality Insight
    )
    filename = "Top1_movie_actor.csv" # or change with other file

    df = pd.read_csv(filename)
    # Drop rows with any empty cells
    df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)
    df = df.dropna()

    for index, row in df.iterrows():
        if row[3] is None or row[3] == "":
            continue
        try:
            ls = []

            ls.append({
                "content": row['Top1_character_speech'],  # column name which want to be analyzed
                "contenttype": "text/plain",
                "language": "en"
            })

            print("analyze data #{0}".format( index) )
            result = get_persona(ls)
            df.at[index, 'word_count'] = int(result['word_count'])
            for personality in result['personality']:
                df.at[index, personality['trait_id']] = personality['percentile']

                for sub in personality['children']:
                    df.at[index, sub['trait_id']] = sub['percentile']

            for need in result['needs']:
                df.at[index, need['trait_id']] = need['percentile']

            for value in result['values']:
                df.at[index, value['trait_id']] = value['percentile']

            for consums in result['consumption_preferences']:
                for consum in consums['consumption_preferences']:
                    df.at[index, consum['consumption_preference_id']] = consum['score']
        except :
            print("ERROR data #{0}".format( index) )
            continue

    if not exists("output/"):
        makedirs('output/')
        print('directory "output/" created')


    if exists("output/output.xlsx"):
        remove("output/output.xlsx")

    with pd.ExcelWriter('output/output.xlsx') as writer:
        df.to_excel(writer,sheet_name="output",index=False)


