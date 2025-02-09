import json
import os
import pandas as pd


# 1. Import each json file and store it
# 2. Import a names.csv config file with translations from UUID to username
# 3. Based on a category and sub-category of stats, return the leaderboard 


def loadData():
    df = pd.DataFrame()
    names = pd.read_csv('names.csv')
    for filename in os.listdir('stats'):
        print("Now processing", filename)
        file = open('stats/' + filename)
        data = json.load(file)
        # Import the JSON to a Pandas DF
        temp_df = pd.json_normalize(data, meta_prefix=True)
        temp_name = names.loc[names['uuid'] == filename[:-5]]['name']
        temp_df = temp_df.transpose().iloc[1:].rename({0: temp_name.iloc[0]}, axis=1)
        # Split the index (stats.blabla.blabla) into 3 indexes (stats, blabla, blabla)
        temp_df.index = temp_df.index.str.split('.', expand=True)
        if df.empty:
            df = temp_df
        else:
            df = df.join(temp_df, how="outer")
        df.to_csv('temp.csv')
        #print(df)
    return df
    
def getLeaderboard(df, cat, subcat):
    row = df.loc['stats'].loc[cat].loc[subcat].fillna(0).sort_values()
    print(row)


df = loadData()
getLeaderboard(df, 'minecraft:custom', 'minecraft:enchant_item')